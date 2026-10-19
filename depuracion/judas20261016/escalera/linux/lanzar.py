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
Con --ensayo sólo calibra y prueba el vigía con "java -version". Para
probar el lanzador sin tocar resultados/, la variable TANDA_RESULTADOS
indica otra carpeta.
"""
import datetime
import os
import platform
import shutil
import subprocess
import sys
import time

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
RES = os.environ.get("TANDA_RESULTADOS") or os.path.join(AQUI, "resultados")
GB = 2 ** 30

PELDANO5 = os.path.join(ESCALERA, "peldano5_completo.srs")
P1 = os.path.join(ESCALERA, "peldano1_X.srs")
P3 = os.path.join(ESCALERA, "peldano3_ramaA.srs")
P4 = os.path.join(ESCALERA, "peldano4_ramaB.srs")
BUCLE = os.path.join(ESCALERA, "turnos", "bucle.srs")

# Técnicas a la vez. AProVE las reparte entre max(4, 2 × procesadores)
# hilos de trabajo (PrioritizableThreadPool del jar), y cada una guarda sus
# datos en el heap y puede lanzar su MiniSat: eso es lo que gasta memoria.
# Java ve los mismos procesadores que en Windows (-XX:ActiveProcessorCount):
# 4, u 8 técnicas, en el portafolio y las acotadas, y 6, o 12, en los turnos.
# Así sólo cambia la memoria. La afinidad es la de los 6 núcleos físicos
# en todas, y los solucionadores los aprovechan.
# Pruebas cortas: (nombre, estrategia o None para el portafolio, segundos,
# entrada, esperado, procesadores).
PRUEBAS = [
    ("prueba_portafolio_peldano1", None, 60, P1, "YES", 4),
    ("prueba_derecho_peldano3", "aprove.Turnos.derecho", 120, P3, "YES", 6),
    ("prueba_derecho_peldano4", "aprove.Turnos.derecho", 120, P4, "YES", 6),
    ("prueba_reves_peldano3", "aprove.Turnos.reves", 120, P3, "YES", 6),
    ("prueba_reves_peldano4", "aprove.Turnos.reves", 120, P4, "YES", 6),
    ("prueba_lazos_bucle", "aprove.Turnos.lazos", 60, BUCLE, "NO", 6),
    ("prueba_acotadaA_peldano4", "aprove.Piloto.peldano5", 120, P4, "YES", 4),
    ("prueba_acotadaB_peldano4", "aprove.Piloto.peldano5b", 120, P4, "YES", 4),
]
# La tanda sobre el peldaño 5, en el orden del LEEME: (nombre, estrategia,
# segundos, procesadores).
LARGAS = [
    ("portafolio_300s", None, 300, 4),
    ("portafolio_3600s", None, 3600, 4),
    ("acotadaA", "aprove.Piloto.peldano5", 5400, 4),
    ("acotadaB", "aprove.Piloto.peldano5b", 5400, 4),
    ("derecho", "aprove.Turnos.derecho", 8100, 6),
    ("reves", "aprove.Turnos.reves", 8100, 6),
    ("lazos", "aprove.Turnos.lazos", 1800, 6),
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


def reparto(libre, tecnicas, lazos=False):
    """(heap de Java, tope de cada solucionador), en GB, para una corrida con
    `libre` GB libres y `tecnicas` técnicas a la vez.

    El ensayo del 19-10 (portafolio a 300 s, -Xmx10g, 8 técnicas) llenó el
    heap en 30 s, con 13 recolecciones completas, mientras los solucionadores
    no pasaron de 3,2 GB y quedaron 7 GB libres: el heap es el cuello de
    botella. Java se lleva, de lo libre menos 2 GB, el 70 % con 8 técnicas y
    el 64 % con 12, que lanzan más solucionadores (4,8 GB en Windows). Lazos
    corre dentro de Java: todo menos 4 GB. Cada solucionador puede crecer
    hasta el 60 % de lo que quede."""
    if lazos:
        java = max(4, min(14, int(libre - 4)))
    else:
        java = max(4, min(14, int((0.70 if tecnicas <= 8 else 0.64) * (libre - 2))))
    return java, round(max(2.0, min(6.0, 0.6 * (libre - 2 - java))), 1)


def calibrar():
    """Mide la RAM libre y elige los núcleos."""
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
    return {"libre": libre, "fisicos": fisicos, "logicos": logicos,
            "nucleos": ",".join(str(i) for i in sorted(primeros))}


def memoria_para(nombre, tecnicas, c0):
    """Antes de cada corrida larga: si la RAM libre bajó más de 1 GB desde el
    principio, espera hasta 10 min a que vuelva, y reparte lo que haya. Nunca
    da más memoria que con la RAM libre del principio (c0).
    Devuelve (heap de Java, tope de cada solucionador, RAM libre)."""
    c = calibrar()
    if c["libre"] < c0["libre"] - 1:
        apuntar("%s: hay %.1f GB libres y al empezar había %.1f; espero hasta 10 min"
                % (nombre, c["libre"], c0["libre"]))
        limite = time.time() + 600
        while c["libre"] < c0["libre"] - 1 and time.time() < limite:
            time.sleep(30)
            c = calibrar()
    heap, tope = reparto(min(c["libre"], c0["libre"]), tecnicas, nombre == "lazos")
    return heap, tope, c["libre"]


def correr(nombre, estrategia, segundos, heap, tope, procesadores, entrada, c, entorno, orden_java=None):
    """Corre AProVE bajo el vigía y devuelve la primera línea de su salida.
    Java usa cabeceras de objeto compactas (JEP 519, de Java 25): en el
    ensayo del 19-10, de un 5 a un 16 % menos de heap ocupado."""
    java = orden_java or (
        [JAVA, "-ea", "-Xmx%dg" % heap, "-XX:+UseCompactObjectHeaders",
         "-XX:ActiveProcessorCount=%d" % procesadores,
         "-Xlog:gc:file=%s.gc.txt" % nombre, "-cp", CP,
         "aprove.Main", "-m", "wst", "-p", "plain", "-t", str(segundos)]
        + (["-s", estrategia] if estrategia else []) + [entrada])
    orden = [sys.executable, "-I", VIGIA,
             "--salida", nombre + ".salida.txt", "--errores", nombre + ".errores.txt",
             "--registro", nombre + ".vigia.txt", "--nucleos", c["nucleos"],
             "--tiempo-max", str(segundos + 240), "--tmp", TMP,
             "--tope-hijo-gb", str(tope), "--aviso-gb", "1.8",
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
    java8, tope8 = reparto(c["libre"], 8)
    java12, tope12 = reparto(c["libre"], 12)
    java_lazos, tope_lazos = reparto(c["libre"], 12, True)
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
        "portafolio y acotadas (8 técnicas a la vez, Java ve 4 procesadores): Java %d GB, "
        "cada solucionador hasta %.1f GB" % (java8, tope8),
        "derecho y revés (12 técnicas a la vez, Java ve 6): Java %d GB, cada solucionador hasta %.1f GB"
        % (java12, tope12),
        "lazos (12 técnicas a la vez): Java %d GB, cada solucionador hasta %.1f GB" % (java_lazos, tope_lazos),
        "Java con -XX:+UseCompactObjectHeaders",
        "vigía: cada 1 s; aviso 1,8 GB (corta solucionadores de mayor a menor), mínimo 1,2 GB "
        "(corta todos los solucionadores y, si no basta, la corrida); OOM del núcleo: solucionadores 1000, "
        "Java 300; tiempo máximo = el de AProVE + 240 s",
        "antes de cada corrida larga: si faltan más de 1 GB libres, espera hasta 10 min; nunca más memoria que ésta",
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
        correr("ensayo_java", None, 60, 0, tope8, c["fisicos"], "", c, entorno,
               orden_java=[JAVA, "-version"])
        return 0

    if not sin_pruebas:
        print("\nPrimero, %d pruebas cortas (unos minutos)." % len(PRUEBAS), flush=True)
        for nombre, estrategia, segundos, entrada, esperado, procesadores in PRUEBAS:
            if correr(nombre, estrategia, segundos, 2, tope8, procesadores, entrada, c, entorno) != esperado:
                apuntar("validación fallida en %s: se esperaba %s; la tanda no sigue" % (nombre, esperado))
                return 1
    if solo_pruebas:
        apuntar("pruebas cortas: todas dan lo esperado")
        return 0

    for nombre, estrategia, segundos, procesadores in LARGAS:
        if solo is not None and nombre not in solo:
            continue
        tecnicas = max(4, 2 * procesadores)
        heap, tope, libre = memoria_para(nombre, tecnicas, c)
        fin = ahora() + datetime.timedelta(seconds=segundos + 60)
        print("", flush=True)
        apuntar("%s: empieza con %.1f GB libres; Java %d GB, %d técnicas a la vez, cada solucionador "
                "hasta %.1f GB; termina hacia las %s, como mucho"
                % (nombre, libre, heap, tecnicas, tope, fin.strftime("%H:%M")))
        veredicto = correr(nombre, estrategia, segundos, heap, tope, procesadores, PELDANO5, c, entorno)
        if veredicto in ("YES", "NO"):
            apuntar("tanda detenida por %s: un YES se certifica con CeTA y un NO se revisa a mano" % veredicto)
            break
    apuntar("FIN")
    return 0


if __name__ == "__main__":
    sys.exit(main())
