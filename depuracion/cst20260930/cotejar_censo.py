"""Cotejo independiente del censo de CST; no importa censo_cst.py.

1. Recorrido completo 2<=n<=2^E con numpy, sin criba de residuos: cada n se
   itera hasta su primer cruce, comparando 3^S<2^j con enteros exactos.
2. Muestra aleatoria (semilla fija) en [desde, N] con enteros de Python.
"""

import argparse
import json
from pathlib import Path
import random

import numpy as np


def cst(n):
    x, S, j = n, 0, 0
    while True:
        if x % 2:
            x, S = (3 * x + 1) // 2, S + 1
        else:
            x //= 2
        j += 1
        if 3 ** S < 2 ** j:
            return x < n


def completo(E, bloque=1 << 22):
    tope = []
    S = 0
    for j in range(400):
        while 3 ** (S + 1) < 2 ** j:
            S += 1
        tope.append(S if 3 ** S < 2 ** j else -1)
    tope = np.array(tope, dtype=np.int64)
    fallos = 0
    for inicio in range(2, (1 << E) + 1, bloque):
        n = np.arange(inicio, min(inicio + bloque, (1 << E) + 1), dtype=np.uint64)
        x, S, vivo = n.copy(), np.zeros(n.size, np.int64), np.ones(n.size, bool)
        j = 0
        while vivo.any():
            j += 1
            impar = (x & np.uint64(1)).astype(bool)
            x = np.where(impar, (x * np.uint64(3) + np.uint64(1)) // np.uint64(2), x // np.uint64(2))
            S = S + impar
            cruza = vivo & (S <= tope[j])
            fallos += int((cruza & (x >= n)).sum())
            vivo &= ~cruza
    return fallos


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--N", type=int, required=True)
    ap.add_argument("--E", type=int, default=27)
    ap.add_argument("--muestra", type=int, default=1000000)
    ap.add_argument("--desde", type=int, default=2, help="extremo inferior de la muestra")
    ap.add_argument("--salida", type=Path, required=True)
    a = ap.parse_args()
    f1 = completo(a.E)
    rnd = random.Random(20261012)
    f2 = sum(1 for _ in range(a.muestra) if not cst(rnd.randint(max(2, a.desde), a.N)))
    salida = {"completo_hasta": 1 << a.E, "fallos_completo": f1,
              "muestra": a.muestra, "rango_muestra": [max(2, a.desde), a.N], "fallos_muestra": f2,
              "semilla_aleatoria": 20261012}
    a.salida.write_text(json.dumps(salida, indent=2) + "\n", encoding="utf-8")
    print(salida)


if __name__ == "__main__":
    main()
