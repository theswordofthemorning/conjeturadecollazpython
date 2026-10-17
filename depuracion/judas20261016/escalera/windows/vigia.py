"""Vigía: corre una orden larga (AProVE) sin dejar que agote la memoria del equipo.

Uso:
  python -I vigia.py --salida S.txt --errores E.txt --registro R.txt
         [--nucleos 0,2,4,6] [--tiempo-max 420] [--tmp CARPETA] -- orden args...

Reglas, comprobadas cada 2 segundos:
  1. Un proceso hijo (MiniSat, Z3, ...) que pase de --tope-hijo-gb se corta.
  2. Si la RAM libre del equipo baja de --aviso-gb, se corta el hijo mayor.
  3. Si baja de --libre-min-gb, o el compromiso libre baja de
     --compromiso-min-gb, se corta todo.
  4. Si se pasa de --tiempo-max segundos, se corta todo.
La orden corre con prioridad baja y en los núcleos pedidos; sus hijos heredan
las dos cosas. Al final se cortan los hijos que queden vivos y se borra la
carpeta temporal de la corrida. Cortar un hijo sólo hace fallar la técnica
que lo usaba: AProVE lo toma como "no encontrado", nunca como prueba.
"""
import argparse
import ctypes
import os
import shutil
import subprocess
import time

import psutil

GB = 1024 ** 3
RESOLVEDORES = {"minisat.exe", "minisat2.exe", "z3.exe", "yices.exe"}
JAVAS = {"java.exe", "javaw.exe"}


class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]


def memoria_equipo():
    """RAM libre y compromiso libre (RAM + archivo de paginación) del equipo, en GB."""
    m = MEMORYSTATUSEX()
    m.dwLength = ctypes.sizeof(m)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.ullAvailPhys / GB, m.ullAvailPageFile / GB


def privada(proc):
    """Memoria privada de un proceso en GB (0 si ya terminó)."""
    try:
        return proc.memory_info().private / GB
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return 0.0


def nombre(proc):
    try:
        return proc.name()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return "?"


def cortar(proc):
    """Corta un proceso y todos sus descendientes."""
    try:
        familia = proc.children(recursive=True)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        familia = []
    for q in familia + [proc]:
        try:
            q.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass


def tamano(carpeta):
    total = 0
    for raiz, _, ficheros in os.walk(carpeta):
        for f in ficheros:
            try:
                total += os.path.getsize(os.path.join(raiz, f))
            except OSError:
                pass
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", required=True)
    ap.add_argument("--errores", required=True)
    ap.add_argument("--registro", required=True)
    ap.add_argument("--nucleos", default="")
    ap.add_argument("--tiempo-max", type=float, default=0)
    ap.add_argument("--tope-hijo-gb", type=float, default=1.5)
    ap.add_argument("--aviso-gb", type=float, default=3.0)
    ap.add_argument("--libre-min-gb", type=float, default=2.0)
    ap.add_argument("--compromiso-min-gb", type=float, default=1.5)
    ap.add_argument("--tmp", default="")
    ap.add_argument("orden", nargs=argparse.REMAINDER)
    a = ap.parse_args()
    orden = a.orden[1:] if a.orden[:1] == ["--"] else a.orden

    inicio = time.time()
    registro = open(a.registro, "w", encoding="utf-8", buffering=1)

    def apuntar(msg, pantalla=False):
        linea = "%7.1fs  %s" % (time.time() - inicio, msg)
        registro.write(linea + "\n")
        if pantalla:
            print(linea, flush=True)

    # Carpeta temporal propia de esta corrida: Java (java.io.tmpdir) y el
    # adaptador de Yices la toman de TMP. Sólo se borra esta subcarpeta.
    entorno = dict(os.environ)
    carpeta_tmp = ""
    if a.tmp:
        carpeta_tmp = os.path.join(a.tmp, "vigia_%d" % int(inicio))
        os.makedirs(carpeta_tmp)
        entorno["TMP"] = entorno["TEMP"] = carpeta_tmp

    libre, comp = memoria_equipo()
    apuntar("orden: " + " ".join(orden), True)
    apuntar("antes: RAM libre %.1f GB, compromiso libre %.1f GB" % (libre, comp), True)

    with open(a.salida, "wb") as fs, open(a.errores, "wb") as fe:
        p = subprocess.Popen(orden, stdout=fs, stderr=fe, stdin=subprocess.DEVNULL, env=entorno,
                             creationflags=subprocess.BELOW_NORMAL_PRIORITY_CLASS)
        jefe = psutil.Process(p.pid)
        if a.nucleos:
            jefe.cpu_affinity([int(x) for x in a.nucleos.split(",")])

        vistos = {}
        cortes = 0
        motivo = "terminó solo"
        pico = {"java": 0.0, "hijos": 0.0, "juntos": 0.0, "n": 0}
        minimo = {"libre": libre, "comp": comp}
        pico_real_java = 0.0
        pids_java = {p.pid}
        ultimo = -10.0
        while p.poll() is None:
            time.sleep(2)
            t = time.time() - inicio
            libre, comp = memoria_equipo()
            try:
                arbol = [jefe] + jefe.children(recursive=True)
            except psutil.NoSuchProcess:
                break
            # Java (o el lanzador que la arranca) nunca entra en las reglas 1
            # y 2: su tope es -Xmx.
            javas = [q for q in arbol if q is jefe or nombre(q).lower() in JAVAS]
            hijos = [q for q in arbol if q not in javas]
            for q in arbol[1:]:
                vistos.setdefault(q.pid, q)
            for q in javas:
                pids_java.add(q.pid)
                try:
                    pico_real_java = max(pico_real_java, q.memory_info().peak_pagefile / GB)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            mem = {h: privada(h) for h in hijos}
            m_java = sum(privada(q) for q in javas)
            m_hijos = sum(mem.values())
            pico["java"] = max(pico["java"], m_java)
            pico["hijos"] = max(pico["hijos"], m_hijos)
            pico["juntos"] = max(pico["juntos"], m_java + m_hijos)
            pico["n"] = max(pico["n"], len(hijos))
            minimo["libre"] = min(minimo["libre"], libre)
            minimo["comp"] = min(minimo["comp"], comp)

            # Regla 1: ningún hijo pasa del tope.
            for h in list(mem):
                if mem[h] > a.tope_hijo_gb:
                    apuntar("corto %s (pid %d): %.2f GB, más que el tope" % (nombre(h), h.pid, mem[h]), True)
                    cortar(h)
                    cortes += 1
                    mem[h] = 0.0
            # Regla 2: con poca RAM libre se corta el hijo mayor.
            if libre < a.aviso_gb and mem:
                h = max(mem, key=mem.get)
                if mem[h] > 0.2:
                    apuntar("RAM libre %.2f GB: corto %s (pid %d, %.2f GB)" % (libre, nombre(h), h.pid, mem[h]), True)
                    cortar(h)
                    cortes += 1
            # Regla 3: el equipo nunca baja del mínimo.
            if libre < a.libre_min_gb or comp < a.compromiso_min_gb:
                motivo = "CORTADO por memoria del equipo (RAM libre %.2f GB, compromiso libre %.2f GB)" % (libre, comp)
                apuntar(motivo, True)
                cortar(jefe)
                break
            # Regla 4: tiempo máximo.
            if a.tiempo_max and t > a.tiempo_max:
                motivo = "CORTADO por tiempo (%.0f s)" % t
                apuntar(motivo, True)
                cortar(jefe)
                break
            if t - ultimo >= 10:
                ultimo = t
                cuenta = {}
                for h in hijos:
                    n = nombre(h)
                    cuenta[n] = cuenta.get(n, 0) + 1
                apuntar("RAM libre %.1f GB, compromiso libre %.1f GB | java %.2f GB | hijos %d, %.2f GB %s"
                        % (libre, comp, m_java, len(hijos), m_hijos,
                           " ".join("%s x%d" % kv for kv in sorted(cuenta.items()))))
        codigo = p.wait()

    # Restos: los hijos vistos que sigan vivos y cualquier resolvedor o hijo de
    # Java nacido durante la corrida.
    restos = 0
    for h in vistos.values():
        if h.is_running():
            cortar(h)
            restos += 1
    for q in psutil.process_iter(["name", "create_time", "ppid"]):
        nacido_durante = (q.info["create_time"] or 0) >= inicio
        es_resolvedor = (q.info["name"] or "").lower() in RESOLVEDORES
        hijo_de_java = q.info["ppid"] in pids_java
        if nacido_durante and (es_resolvedor or hijo_de_java):
            cortar(q)
            restos += 1

    apuntar("FIN: código de salida %s, %.1f s; %s" % (codigo, time.time() - inicio, motivo), True)
    apuntar("picos cada 2 s: java %.2f GB, hijos %.2f GB (hasta %d a la vez), juntos %.2f GB"
            % (pico["java"], pico["hijos"], pico["n"], pico["juntos"]), True)
    apuntar("pico real de java (memoria privada): %.2f GB" % pico_real_java, True)
    apuntar("mínimos del equipo: RAM libre %.2f GB, compromiso libre %.2f GB"
            % (minimo["libre"], minimo["comp"]), True)
    apuntar("hijos cortados por memoria: %d; restos cortados al final: %d" % (cortes, restos), True)
    if carpeta_tmp:
        mb = tamano(carpeta_tmp) / 2 ** 20
        shutil.rmtree(carpeta_tmp, ignore_errors=True)
        apuntar("temporales: %.1f MB, borrados" % mb, True)
    libre, comp = memoria_equipo()
    apuntar("después: RAM libre %.1f GB, compromiso libre %.1f GB" % (libre, comp), True)
    registro.close()


if __name__ == "__main__":
    main()
