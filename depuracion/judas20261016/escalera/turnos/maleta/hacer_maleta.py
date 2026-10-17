"""Arma en el Escritorio la maleta del Victus: la cadena de turnos con todo lo que necesita.

Uso, en el PC de escritorio:  python -I -B hacer_maleta.py
Copia el JDK, Python, las herramientas de C:\\Users\\Home\\herramientas y las
estrategias de ../estrategia; los binarios no van al repo.
"""
import os
import shutil

import psutil

DESTINO = r"C:\Users\Home\Desktop\maleta_victus"
HERR = r"C:\Users\Home\herramientas"
PY = r"C:\Python314"
FUENTES = os.path.dirname(os.path.abspath(__file__))
ESC = os.path.dirname(os.path.dirname(FUENTES))

assert not os.path.exists(DESTINO), "la maleta ya existe"
os.makedirs(DESTINO)

# Java entero, menos lo que sólo sirve para compilar.
shutil.copytree(r"C:\Program Files\Java\jdk-27", os.path.join(DESTINO, "jdk-27"),
                ignore=lambda d, fs: [f for f in fs if f in ("jmods", "include", "src.zip")])

# Python mínimo: intérprete, biblioteca estándar y psutil (el vigía lo usa).
dpy = os.path.join(DESTINO, "python")
os.makedirs(dpy)
for f in os.listdir(PY):
    if f.lower().endswith((".exe", ".dll")) or f == "LICENSE.txt":
        shutil.copy2(os.path.join(PY, f), dpy)
shutil.copytree(os.path.join(PY, "DLLs"), os.path.join(dpy, "DLLs"),
                ignore=shutil.ignore_patterns("__pycache__"))
SIN = {"test", "idlelib", "tkinter", "turtledemo", "ensurepip", "site-packages"}
lib = os.path.normcase(os.path.join(PY, "Lib"))
shutil.copytree(os.path.join(PY, "Lib"), os.path.join(dpy, "Lib"),
                ignore=lambda d, fs: [f for f in fs if f == "__pycache__"
                                      or (os.path.normcase(d) == lib and f in SIN)])
shutil.copytree(os.path.dirname(psutil.__file__), os.path.join(dpy, "Lib", "site-packages", "psutil"),
                ignore=shutil.ignore_patterns("__pycache__", "tests"))

# Herramientas: AProVE parcheado, MiniSat, el adaptador de Yices, el vigía y Z3.
dh = os.path.join(DESTINO, "herramientas")
os.makedirs(os.path.join(dh, "aprove", "tmp"))
shutil.copy2(os.path.join(HERR, "aprove", "aprove_parche_stop.jar"), os.path.join(dh, "aprove"))
os.makedirs(os.path.join(dh, "bin"))
for f in ("minisat.exe", "minisat2.exe", "yices.exe", "vigia.py"):
    shutil.copy2(os.path.join(HERR, "bin", f), os.path.join(dh, "bin"))
# El adaptador busca Z3 en una ruta fija de este PC; en la maleta, junto a sí.
with open(os.path.join(HERR, "bin", "yices_shim.py"), encoding="utf-8") as f:
    shim = f.read()
viejo = 'Z3 = r"C:\\Users\\Home\\herramientas\\z3\\z3-5.3.1-x64-win\\bin\\z3.exe"'
nuevo = 'Z3 = os.path.join(os.path.dirname(AQUI), "z3", "z3-5.3.1-x64-win", "bin", "z3.exe")'
assert shim.count(viejo) == 1
with open(os.path.join(dh, "bin", "yices_shim.py"), "w", encoding="utf-8") as f:
    f.write(shim.replace(viejo, nuevo))
zb = os.path.join(HERR, "z3", "z3-5.3.1-x64-win", "bin")
dz = os.path.join(dh, "z3", "z3-5.3.1-x64-win", "bin")
os.makedirs(dz)
for f in os.listdir(zb):
    if f.lower().endswith((".exe", ".dll")):
        shutil.copy2(os.path.join(zb, f), dz)
for f in ("LICENSE.txt",):
    if os.path.exists(os.path.join(HERR, "z3", "z3-5.3.1-x64-win", f)):
        shutil.copy2(os.path.join(HERR, "z3", "z3-5.3.1-x64-win", f), os.path.dirname(dz))

# Las estrategias por turnos y las entradas: los peldaños 3, 4 y 5 y el bucle de prueba.
dt = os.path.join(DESTINO, "turnos")
shutil.copytree(os.path.join(ESC, "turnos", "estrategia"), os.path.join(dt, "estrategia"))
for f in ("peldano3_ramaA.srs", "peldano4_ramaB.srs", "peldano5_completo.srs"):
    shutil.copy2(os.path.join(ESC, f), dt)
shutil.copy2(os.path.join(ESC, "turnos", "bucle.srs"), dt)

# El lanzador; el .bat y el LEEME con fin de línea de Windows.
shutil.copy2(os.path.join(FUENTES, "lanzar.py"), DESTINO)
for f in ("lanzar.bat", "LEEME.txt"):
    with open(os.path.join(FUENTES, f), encoding="utf-8") as g:
        texto = g.read()
    with open(os.path.join(DESTINO, f), "w", encoding="utf-8", newline="\r\n") as g:
        g.write(texto)

total = n = 0
for raiz, _, fs in os.walk(DESTINO):
    for f in fs:
        total += os.path.getsize(os.path.join(raiz, f))
        n += 1
print("maleta: %d archivos, %.0f MB" % (n, total / 2 ** 20))
for d in sorted(os.listdir(DESTINO)):
    p = os.path.join(DESTINO, d)
    s = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(p) for f in fs) if os.path.isdir(p) else os.path.getsize(p)
    print("  %-12s %7.1f MB" % (d, s / 2 ** 20))
