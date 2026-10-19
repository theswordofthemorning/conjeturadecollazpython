"""Pasa los peldaños de la escalera del formato SRS de la TPDB (el que lee
AProVE) al formato de Yolcu-Aaronson-Heule con --spaced: una regla por línea,
símbolos separados por espacios y "->" para las reglas estrictas.

Después lee cada .srs escrito con el propio lector de YAH
(prover/rules.py) y comprueba que da exactamente las mismas reglas, en el
mismo orden, todas estrictas y de terminación completa. Si algo no
coincide, no escribe nada más y sale con código 1.

Uso:  python3 -I convertir.py
Escribe sistemas/peldanoN_*.srs junto a este archivo.
"""
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ESCALERA = os.path.dirname(AQUI)
YAH = "/home/oem/herramientas/yah/rewriting-collatz"
SALIDA = os.path.join(AQUI, "sistemas")

PELDANOS = [
    "peldano1_X.srs",
    "peldano2_sinL.srs",
    "peldano3_ramaA.srs",
    "peldano4_ramaB.srs",
    "peldano5_completo.srs",
]


def leer_tpdb(ruta):
    """Devuelve la lista de reglas (izquierda, derecha) como tuplas de símbolos."""
    with open(ruta, encoding="utf-8") as f:
        texto = f.read()
    # quita los (COMMENT ...), que pueden ocupar varias líneas
    texto = re.sub(r"\(COMMENT.*?\)\s*(?=\(|$)", "", texto, flags=re.S)
    m = re.search(r"\(RULES(.*)\)\s*$", texto, flags=re.S)
    if m is None:
        sys.exit(f"ERROR: {ruta} no tiene bloque (RULES ...)")
    reglas = []
    for trozo in m.group(1).split(","):
        trozo = trozo.strip()
        if not trozo:
            continue
        if "->=" in trozo or trozo.count("->") != 1:
            sys.exit(f"ERROR: regla no estricta o mal formada en {ruta}: {trozo}")
        izq, der = trozo.split("->")
        reglas.append((tuple(izq.split()), tuple(der.split())))
    return reglas


def escribir_yah(reglas, ruta):
    with open(ruta, "w", encoding="utf-8") as f:
        for izq, der in reglas:
            f.write(" ".join(izq) + " -> " + " ".join(der) + "\n")


def leer_con_yah(ruta):
    sys.path.insert(0, os.path.join(YAH, "prover"))
    import rules
    sistema = rules.parserules(ruta, True)
    if not sistema.full or sistema.rev:
        sys.exit(f"ERROR: YAH no lee {ruta} como terminación completa")
    if not all(r.strict and not r.top for r in sistema.rules):
        sys.exit(f"ERROR: YAH lee alguna regla de {ruta} como no estricta")
    return [(tuple(r.left), tuple(r.right)) for r in sistema.rules]


def main():
    os.makedirs(SALIDA, exist_ok=True)
    for nombre in PELDANOS:
        reglas = leer_tpdb(os.path.join(ESCALERA, nombre))
        destino = os.path.join(SALIDA, nombre)
        escribir_yah(reglas, destino)
        if leer_con_yah(destino) != reglas:
            sys.exit(f"ERROR: la ida y vuelta de {nombre} no coincide")
        simbolos = sorted({s for izq, der in reglas for s in izq + der})
        print(f"{nombre:24s} {len(reglas):2d} reglas, símbolos {' '.join(simbolos)}: idénticas")
    print("Conversión comprobada.")


if __name__ == "__main__":
    main()
