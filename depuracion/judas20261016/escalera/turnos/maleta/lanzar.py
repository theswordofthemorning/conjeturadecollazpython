"""Corre en este equipo la cadena de turnos de AProVE sobre el peldaño 5.

Es la cadena del PC de escritorio (escalera/turnos/lanzar_turnos.sh): cinco
pruebas cortas y luego derecho, revés y lazos, con los mismos tiempos. Sólo
cambia la memoria, que se reparte aquí según la RAM libre al empezar. Todo
lo que sale queda en la carpeta resultados.

Uso: doble clic en lanzar.bat, o bien  python -I lanzar.py [--ensayo]
Con --ensayo sólo calibra y prueba el vigía con "java -version".
"""
import ctypes
import datetime
import os
import platform
import shutil
import subprocess
import sys
import winreg

import psutil

AQUI = os.path.dirname(os.path.abspath(__file__))
HERR = os.path.join(AQUI, "herramientas")
JAVA = os.path.join(AQUI, "jdk-27", "bin", "java.exe")
JAR = os.path.join(HERR, "aprove", "aprove_parche_stop.jar")
CP = JAR + ";" + os.path.join(AQUI, "turnos", "estrategia")
VIGIA = os.path.join(HERR, "bin", "vigia.py")
TMP = os.path.join(HERR, "aprove", "tmp")
Z3 = os.path.join(HERR, "z3", "z3-5.3.1-x64-win", "bin")
PY_YICES = r"C:\Python314\python.exe"  # el adaptador yices.exe llama a este Python
TURNOS = os.path.join(AQUI, "turnos")
RES = os.path.join(AQUI, "resultados")
GB = 2 ** 30

# Las cinco pruebas del PC de escritorio, con lo que tienen que dar.
PRUEBAS = [
    ("prueba_derecho_peldano3", "derecho", 120, "peldano3_ramaA.srs", "YES"),
    ("prueba_derecho_peldano4", "derecho", 120, "peldano4_ramaB.srs", "YES"),
    ("prueba_reves_peldano3", "reves", 120, "peldano3_ramaA.srs", "YES"),
    ("prueba_reves_peldano4", "reves", 120, "peldano4_ramaB.srs", "YES"),
    ("prueba_lazos_bucle", "lazos", 60, "bucle.srs", "NO"),
]
# Los turnos largos, con los tiempos del PC de escritorio.
LARGOS = [("derecho", 8100), ("reves", 8100), ("lazos", 1800)]


def ahora():
    return datetime.datetime.now()


def apuntar(linea):
    """Escribe una línea en pantalla y en resultados/cadena.txt, con fecha y hora."""
    linea = ahora().strftime("%d-%m %H:%M:%S ") + linea
    print(linea, flush=True)
    with open(os.path.join(RES, "cadena.txt"), "a", encoding="utf-8") as f:
        f.write(linea + "\n")


def procesador():
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                            r"HARDWARE\DESCRIPTION\System\CentralProcessor\0") as k:
            return winreg.QueryValueEx(k, "ProcessorNameString")[0].strip()
    except OSError:
        return platform.processor()


def calibrar():
    """Reparte la RAM libre entre Java y los solucionadores."""
    libre = psutil.virtual_memory().available / GB
    fisicos = psutil.cpu_count(logical=False) or 1
    logicos = psutil.cpu_count() or fisicos
    # Un hilo por núcleo físico; los hermanos SMT quedan para Windows.
    paso = 2 if logicos == 2 * fisicos else 1
    c = {"libre": libre, "fisicos": fisicos, "logicos": logicos,
         "nucleos": ",".join(str(i) for i in range(0, logicos, paso))}
    # Turnos de terminación: Java se lleva el 55 % de lo libre, descontado un
    # margen de 2 GB, y cada solucionador puede crecer hasta el 60 % del resto.
    # Con los 11,6 GB libres del PC de escritorio daría Java 5 GB y tope
    # 2,8 GB (allí se usó 3).
    c["java"] = max(4, min(12, int(0.55 * (libre - 2))))
    c["tope"] = round(max(2.0, min(6.0, 0.6 * (libre - 2 - c["java"]))), 1)
    # Lazos corre dentro de Java: se lleva todo menos 4 GB.
    c["java_lazos"] = max(4, min(14, int(libre - 4)))
    return c


def correr(nombre, turno, segundos, heap, entrada, c, entorno, orden_java=None):
    """Corre una estrategia bajo el vigía y devuelve la primera línea de su salida."""
    java = orden_java or [
        JAVA, "-ea", "-Xmx%dg" % heap, "-XX:ActiveProcessorCount=%d" % c["fisicos"],
        "-Xlog:gc:file=%s.gc.txt" % nombre, "-cp", CP,
        "aprove.Main", "-m", "wst", "-p", "plain", "-t", str(segundos),
        "-s", "aprove.Turnos." + turno, os.path.join(TURNOS, entrada)]
    orden = [sys.executable, "-I", VIGIA,
             "--salida", nombre + ".salida.txt", "--errores", nombre + ".errores.txt",
             "--registro", nombre + ".vigia.txt", "--nucleos", c["nucleos"],
             "--tiempo-max", str(segundos + 240), "--tmp", TMP,
             "--tope-hijo-gb", str(c["tope"]), "--aviso-gb", "1.8",
             "--libre-min-gb", "1.2", "--compromiso-min-gb", "1.2", "--"] + java
    subprocess.run(orden, cwd=RES, env=entorno)
    try:
        with open(os.path.join(RES, nombre + ".salida.txt"), encoding="utf-8", errors="replace") as f:
            veredicto = f.readline().strip()
    except OSError:
        veredicto = ""
    apuntar("%s: %s" % (nombre, veredicto or "sin salida"))
    return veredicto


def main():
    ensayo = "--ensayo" in sys.argv[1:]
    if " " in AQUI or not AQUI.isascii():
        print("La ruta de la maleta tiene espacios o acentos:\n  %s\n"
              "Cópiala a C:\\maleta_victus y vuelve a dar doble clic." % AQUI)
        return 1
    if ctypes.windll.kernel32.GetDriveTypeW(os.path.splitdrive(AQUI)[0] + "\\") == 2:
        print("La maleta está en un pendrive. Cópiala a C:\\maleta_victus y vuelve a dar doble clic.")
        return 1
    faltan = [r for r in (JAVA, JAR, VIGIA, PY_YICES, os.path.join(Z3, "z3.exe"))
              if not os.path.exists(r)]
    if faltan:
        print("Faltan estos archivos:\n  " + "\n  ".join(faltan))
        return 1
    bateria = psutil.sensors_battery()
    if bateria is not None and not bateria.power_plugged and not ensayo:
        print("El portátil está con batería. Enchufa el cargador y vuelve a dar doble clic.")
        return 1

    os.makedirs(RES, exist_ok=True)
    c = calibrar()
    informe = [
        "fecha: " + ahora().strftime("%Y-%m-%d %H:%M:%S"),
        "equipo: %s; %s" % (procesador(), platform.platform()),
        "RAM: %.1f GB en total, %.1f GB libres al empezar"
        % (psutil.virtual_memory().total / GB, c["libre"]),
        "núcleos: %d físicos, %d lógicos; se usan %s" % (c["fisicos"], c["logicos"], c["nucleos"]),
        "derecho y revés: Java %d GB, cada solucionador hasta %.1f GB" % (c["java"], c["tope"]),
        "lazos: Java %d GB" % c["java_lazos"],
        "vigía: aviso 1,8 GB, mínimos 1,2 GB; tiempo máximo = el de AProVE + 240 s",
    ]
    with open(os.path.join(RES, "calibracion.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(informe) + "\n")
    print("\n".join(informe), flush=True)
    if c["libre"] < 14:
        print("\nOjo: hay poca RAM libre. Si hay programas abiertos, ciérralos y vuelve a empezar.",
              flush=True)

    entorno = dict(os.environ)
    entorno["PATH"] = os.pathsep.join([os.path.join(HERR, "bin"), Z3, entorno.get("PATH", "")])

    if ensayo:
        correr("ensayo_java", "", 60, 0, "", c, entorno, orden_java=[JAVA, "-version"])
        return 0

    # Que Windows no se duerma ni apague la pantalla mientras esto corre; el
    # pedido se deshace solo al cerrarse la ventana.
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001 | 0x00000002)

    print("\nPrimero, cinco pruebas cortas (unos 2 minutos).", flush=True)
    for nombre, turno, segundos, entrada, esperado in PRUEBAS:
        if correr(nombre, turno, segundos, 2, entrada, c, entorno) != esperado:
            apuntar("validación fallida en %s: se esperaba %s; la cadena no sigue" % (nombre, esperado))
            return 1

    for turno, segundos in LARGOS:
        heap = c["java_lazos"] if turno == "lazos" else c["java"]
        fin = ahora() + datetime.timedelta(seconds=segundos + 60)
        print("\n%s: empieza ahora y termina hacia las %s." % (turno, fin.strftime("%H:%M")), flush=True)
        veredicto = correr(turno, turno, segundos, heap, "peldano5_completo.srs", c, entorno)
        if veredicto in ("YES", "NO"):
            apuntar("cadena detenida por " + veredicto)
            break
    log = os.path.join(HERR, "bin", "yices_shim.log")
    if os.path.exists(log):
        shutil.copy2(log, RES)
    apuntar("FIN")
    return 0


if __name__ == "__main__":
    sys.exit(main())
