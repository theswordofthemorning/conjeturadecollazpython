"""Corre en el Victus con Linux la tanda pendiente de AProVE sobre el peldaño 5.

Es la de LEEME §4 a §6: el portafolio por omisión a 300 s y a 3600 s, las
estrategias acotadas A y B, y los turnos derecho, revés y lazos, con los
tiempos de Windows. Antes corre las pruebas cortas de calibración, que
tienen que dar lo esperado. La memoria se reparte según la RAM libre al
empezar, como en la maleta (../turnos/maleta/lanzar.py). Todo lo que sale
queda en resultados/.

Las herramientas son las de la imagen Docker jckassing/aprove del 23-09-2026
(AProVE commit ae097c6, Yices 1.0.40, MiniSat), copiadas en
/home/oem/herramientas/aprove/bundle, con el OpenJDK 25 del sistema.

Uso:  python3 -I lanzar.py [--solo nombre,nombre] [--sin-pruebas] [--solo-pruebas] [--ensayo]
Con --ensayo sólo calibra y prueba el vigía con "java -version".
"""
import datetime
import os
import platform
import shutil
import subprocess
import sys

import psutil

AQUI = os.path.dirname(os.path.abspath(__file__))
ESCALERA = os.path.dirname(AQUI)
BUNDLE = "/home/oem/herramientas/aprove/bundle"
JAVA = "/usr/lib/jvm/java-25-openjdk-amd64/bin/java"
JAR = os.path.join(BUNDLE, "aprove.jar")
CP = ":".join([JAR, os.path.join(ESCALERA, "turnos", "estrategia"),
               os.path.join(ESCALERA, "acotada", "estrategia")])
VIGIA = os.path.join(AQUI, "vigia.py")
TMP = "/home/oem/herramientas/aprove/tmp"
RES = os.path.join(AQUI, "resultados")
GB = 2 ** 30

PELDANO5 = os.path.join(ESCALERA, "peldano5_completo.srs")
P1 = os.path.join(ESCALERA, "peldano1_X.srs")
P3 = os.path.join(ESCALERA, "peldano3_ramaA.srs")
P4 = os.path.join(ESCALERA, "peldano4_ramaB.srs")
BUCLE = os.path.join(ESCALERA, "turnos", "bucle.srs")

# Pruebas cortas: (nombre, estrategia o None para el portafolio, segundos, entrada, esperado).
PRUEBAS = [
    ("prueba_portafolio_peldano1", None, 60, P1, "YES"),
    ("prueba_derecho_peldano3", "aprove.Turnos.derecho", 120, P3, "YES"),
    ("prueba_derecho_peldano4", "aprove.Turnos.derecho", 120, P4, "YES"),
    ("prueba_reves_peldano3", "aprove.Turnos.reves", 120, P3, "YES"),
    ("prueba_reves_peldano4", "aprove.Turnos.reves", 120, P4, "YES"),
    ("prueba_lazos_bucle", "aprove.Turnos.lazos", 60, BUCLE, "NO"),
    ("prueba_acotadaA_peldano4", "aprove.Piloto.peldano5", 120, P4, "YES"),
    ("prueba_acotadaB_peldano4", "aprove.Piloto.peldano5b", 120, P4, "YES"),
]
# La tanda sobre el peldaño 5, en el orden del LEEME.
LARGAS = [
    ("portafolio_300s", None, 300),
    ("portafolio_3600s", None, 3600),
    ("acotadaA", "aprove.Piloto.peldano5", 5400),
    ("acotadaB", "aprove.Piloto.peldano5b", 5400),
    ("derecho", "aprove.Turnos.derecho", 8100),
    ("reves", "aprove.Turnos.reves", 8100),
    ("lazos", "aprove.Turnos.lazos", 1800),
]


def ahora():
    return datetime.datetime.now()


def apuntar(linea):
    """Escribe una línea en pantalla y en resultados/cadena.txt, con fecha y hora."""
    linea = ahora().strftime("%d-%m %H:%M:%S ") + linea
    print(linea, flush=True)
    with open(os.path.join(RES, "cadena.txt"), "a", encoding="utf-8") as f:
        f.write(linea + "\n")


def procesador():
    with open("/proc/cpuinfo") as f:
        for linea in f:
            if linea.startswith("model name"):
                return linea.split(":", 1)[1].strip()
    return platform.processor()


def salida_de(orden):
    try:
        r = subprocess.run(orden, capture_output=True, text=True)
        return (r.stdout + r.stderr).strip()
    except OSError as e:
        return str(e)


def calibrar():
    """Reparte la RAM libre entre Java y los solucionadores, como la maleta."""
    libre = psutil.virtual_memory().available / GB
    fisicos = psutil.cpu_count(logical=False) or 1
    logicos = psutil.cpu_count() or fisicos
    # Un hilo por núcleo físico; los hermanos SMT quedan para el escritorio.
    # El primero de cada núcleo sale de la topología del sistema.
    primeros = set()
    for i in range(logicos):
        try:
            with open("/sys/devices/system/cpu/cpu%d/topology/thread_siblings_list" % i) as f:
                primeros.add(int(f.read().replace("-", ",").split(",")[0]))
        except OSError:
            primeros.add(i)
    c = {"libre": libre, "fisicos": fisicos, "logicos": logicos,
         "nucleos": ",".join(str(i) for i in sorted(primeros))}
    # Terminación: Java se lleva el 55 % de lo libre, descontado un margen de
    # 2 GB, y cada solucionador puede crecer hasta el 60 % del resto.
    c["java"] = max(4, min(12, int(0.55 * (libre - 2))))
    c["tope"] = round(max(2.0, min(6.0, 0.6 * (libre - 2 - c["java"]))), 1)
    # Lazos corre dentro de Java: se lleva todo menos 4 GB.
    c["java_lazos"] = max(4, min(14, int(libre - 4)))
    return c


def correr(nombre, estrategia, segundos, heap, entrada, c, entorno, orden_java=None):
    """Corre AProVE bajo el vigía y devuelve la primera línea de su salida."""
    java = orden_java or (
        [JAVA, "-ea", "-Xmx%dg" % heap, "-XX:ActiveProcessorCount=%d" % c["fisicos"],
         "-Xlog:gc:file=%s.gc.txt" % nombre, "-cp", CP,
         "aprove.Main", "-m", "wst", "-p", "plain", "-t", str(segundos)]
        + (["-s", estrategia] if estrategia else []) + [entrada])
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
    args = sys.argv[1:]
    ensayo = "--ensayo" in args
    sin_pruebas = "--sin-pruebas" in args
    solo_pruebas = "--solo-pruebas" in args
    solo = None
    if "--solo" in args:
        solo = args[args.index("--solo") + 1].split(",")
        desconocidas = [n for n in solo if n not in [x[0] for x in LARGAS]]
        if desconocidas:
            print("No conozco: %s. Las corridas son: %s"
                  % (", ".join(desconocidas), ", ".join(x[0] for x in LARGAS)))
            return 2
    faltan = [r for r in (JAVA, JAR, VIGIA, os.path.join(BUNDLE, "bin", "yices"),
                          os.path.join(BUNDLE, "bin", "minisat"), PELDANO5) if not os.path.exists(r)]
    if faltan:
        print("Faltan estos archivos:\n  " + "\n  ".join(faltan))
        return 1
    bateria = psutil.sensors_battery()
    if bateria is not None and not bateria.power_plugged and not ensayo:
        print("El portátil está con batería. Enchufa el cargador y vuelve a lanzar.")
        return 1

    os.makedirs(RES, exist_ok=True)
    os.makedirs(TMP, exist_ok=True)
    c = calibrar()
    informe = [
        "fecha: " + ahora().strftime("%Y-%m-%d %H:%M:%S"),
        "equipo: %s; %s" % (procesador(), platform.platform()),
        "uname: " + salida_de(["uname", "-a"]),
        "RAM: %.1f GB en total, %.1f GB libres al empezar; swap %.1f GB"
        % (psutil.virtual_memory().total / GB, c["libre"], psutil.swap_memory().total / GB),
        "núcleos: %d físicos, %d lógicos; se usan %s" % (c["fisicos"], c["logicos"], c["nucleos"]),
        "java: " + salida_de([JAVA, "-version"]).splitlines()[0],
        "aprove: %s (imagen jckassing/aprove del 23-09-2026)" % JAR,
        "yices: " + salida_de([os.path.join(BUNDLE, "bin", "yices"), "--version"]),
        "terminación (portafolio, acotadas, derecho, revés): Java %d GB, cada solucionador hasta %.1f GB"
        % (c["java"], c["tope"]),
        "lazos: Java %d GB" % c["java_lazos"],
        "vigía: aviso 1,8 GB, mínimos 1,2 GB; tiempo máximo = el de AProVE + 240 s",
    ]
    with open(os.path.join(RES, "calibracion.txt"), "a", encoding="utf-8") as f:
        f.write("\n".join(informe) + "\n\n")
    print("\n".join(informe), flush=True)
    if c["libre"] < 14:
        print("\nOjo: hay poca RAM libre. Si hay programas abiertos, ciérralos y vuelve a empezar.",
              flush=True)

    entorno = dict(os.environ)
    entorno["PATH"] = os.pathsep.join([os.path.join(BUNDLE, "bin"), entorno.get("PATH", "")])

    if ensayo:
        correr("ensayo_java", None, 60, 0, "", c, entorno, orden_java=[JAVA, "-version"])
        return 0

    if not sin_pruebas:
        print("\nPrimero, %d pruebas cortas (unos minutos)." % len(PRUEBAS), flush=True)
        for nombre, estrategia, segundos, entrada, esperado in PRUEBAS:
            if correr(nombre, estrategia, segundos, 2, entrada, c, entorno) != esperado:
                apuntar("validación fallida en %s: se esperaba %s; la tanda no sigue" % (nombre, esperado))
                return 1
    if solo_pruebas:
        apuntar("pruebas cortas: todas dan lo esperado")
        return 0

    for nombre, estrategia, segundos in LARGAS:
        if solo is not None and nombre not in solo:
            continue
        heap = c["java_lazos"] if nombre == "lazos" else c["java"]
        fin = ahora() + datetime.timedelta(seconds=segundos + 60)
        print("\n%s: empieza ahora y termina hacia las %s, como mucho." % (nombre, fin.strftime("%H:%M")),
              flush=True)
        veredicto = correr(nombre, estrategia, segundos, heap, PELDANO5, c, entorno)
        if veredicto in ("YES", "NO"):
            apuntar("tanda detenida por %s: un YES se certifica con CeTA y un NO se revisa a mano" % veredicto)
            break
    apuntar("FIN")
    return 0


if __name__ == "__main__":
    sys.exit(main())
