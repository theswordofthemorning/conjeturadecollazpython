# -*- coding: utf-8 -*-
"""Amplia el barrido exhaustivo del teorema de la libelula con numpy.

Comprueba, para cada nivel n, la tabla completa e_j(n) sobre los 2^n
residuos: que no hay ningun j impar, que j >= 2, y que e_2(n) = e_4(n) = 1.

    python -B -X utf8 depuracion/oeis20260924/libelula_amplia.py
"""
import numpy as np

NDESDE, NHASTA, BLOQUE = 3, 26, 1 << 22


def tabla_nivel(n):
    """Diccionario j -> numero de pares balanceados que funden en el paso n."""
    cuenta = {}
    for ini in range(0, 1 << n, BLOQUE):
        fin = min(ini + BLOQUE, 1 << n)
        x = np.arange(ini, fin, dtype=np.int64)
        y = x + 1
        sx = np.zeros(fin - ini, dtype=np.int32)
        sy = np.zeros(fin - ini, dtype=np.int32)
        j = np.zeros(fin - ini, dtype=np.int32)
        vivo = np.ones(fin - ini, dtype=bool)   # aun no ha fundido
        funde_en_n = np.zeros(fin - ini, dtype=bool)
        for t in range(1, n + 1):
            px = (x & 1).astype(bool)
            py = (y & 1).astype(bool)
            sx += (px & vivo)
            sy += (py & vivo)
            j += (px ^ py) & vivo
            x = np.where(px, (3 * x + 1) >> 1, x >> 1)
            y = np.where(py, (3 * y + 1) >> 1, y >> 1)
            fundiendo = vivo & (x == y)
            if t == n:
                funde_en_n = fundiendo
            vivo &= ~fundiendo
        buenos = funde_en_n & (sx == sy)
        for jv, c in zip(*np.unique(j[buenos], return_counts=True)):
            cuenta[int(jv)] = cuenta.get(int(jv), 0) + int(c)
    return cuenta


print("Barrido exhaustivo de 2^%d a 2^%d residuos." % (NDESDE, NHASTA))
print()
print("  n |    e2    e4  | j impares | j < 2 | sum_j e_j(n)")
impares_total = menores_total = 0
sumas = []
for n in range(NDESDE, NHASTA + 1):
    c = tabla_nivel(n)
    imp = sum(v for k, v in c.items() if k % 2)
    men = sum(v for k, v in c.items() if k < 2)
    impares_total += imp
    menores_total += men
    s = sum(c.values())
    sumas.append(s)
    print(" %2d | %5d %5d  | %9d | %5d | %12d"
          % (n, c.get(2, 0), c.get(4, 0), imp, men, s))

print()
print("total de pares con j IMPAR en todo el barrido :", impares_total)
print("total de pares con j < 2 en todo el barrido   :", menores_total)
print("sum_j e_j(n) para n = %d..%d:" % (NDESDE, NHASTA))
print("  ", sumas)
