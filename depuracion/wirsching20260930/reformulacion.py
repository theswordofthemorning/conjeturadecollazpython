# Dos comprobaciones finitas para la ficha de Wirsching.
#
# 1. Reformulacion de las funciones Elka con sucesiones monotonas:
#      e_l(k, a) = #{ 0 <= d_0 <= ... <= d_(l-1) <= k :
#                     sum_i (3/2)^i 2^(-d_i) = 2a  (mod 3^l) }.
#    Sale de T^n(b) = (3^l b + sum_i 3^(l-1-i) 2^(s_i)) / 2^n con s_i la posicion del
#    i-esimo paso impar, contando los impares desde el final y d_i = pasos pares
#    posteriores a ese impar... Se coteja contra la recurrencia de elka.py.
#
# 2. Conjuntos encajados S_l = { a mod 3^l : c_j(a) > j para todo j en [J0, l] }:
#    tamanos y fraccion de unidades, con c_j el coste minimo de costo.py.
#    Si ningun S_l es vacio, su interseccion (compacidad de Z_3) da un a* con
#    e_l(l, a*) = 0 para todo l >= J0.
import itertools
import math
import numpy as np

# ---------- 1 ----------
L1 = 6
K1 = 6


def elka_recurrencia(L, K):
    tablas = {}
    previo = None
    for l in range(0, L + 1):
        m = 3 ** l
        tabla = np.zeros((K + 1, m), dtype=np.int64)
        if l == 0:
            tabla[:, 0] = 1
        else:
            a = np.arange(m, dtype=np.int64)
            doble = (2 * a) % m
            es2 = (a % 3) == 2
            destino = ((2 * a - 1) // 3) % (m // 3)
            for k in range(K + 1):
                subida = np.where(es2, previo[k][destino], 0)
                tabla[k] = subida if k == 0 else tabla[k - 1][doble] + subida
        tablas[l] = tabla
        previo = tabla
    return tablas


tablas = elka_recurrencia(L1, K1)
fallos = 0
for l in range(1, L1 + 1):
    m = 3 ** l
    inv2 = pow(2, -1, m)
    for k in range(K1 + 1):
        hist = np.zeros(m, dtype=np.int64)
        for d in itertools.combinations_with_replacement(range(k + 1), l):
            s = 0
            for i, di in enumerate(d):
                s = s + pow(3, i, m) * pow(inv2, i + di, m)
            hist[(s * inv2) % m] += 1        # s = 2a  =>  a = s/2
        if not np.array_equal(hist, tablas[l][k]):
            fallos = fallos + 1
print(f"1. Reformulacion monotona contra la recurrencia (l <= {L1}, k <= {K1}): "
      f"{'OK' if fallos == 0 else str(fallos) + ' FALLOS'}")

# ---------- 2 ----------
L2 = 16
J0 = 8
INF = 127
costes = {0: np.zeros(1, dtype=np.int16)}
for l in range(1, L2 + 1):
    m = 3 ** l
    mp = m // 3
    a = np.arange(m, dtype=np.int32)
    unid = (a % 3) != 0
    vivo_prev = np.zeros(1, dtype=np.int16) if l == 1 else costes[l - 1].copy()
    if l > 1:
        vivo_prev[np.arange(mp) % 3 == 0] = INF
    x = a.copy()
    mejor = np.full(m, INF, dtype=np.int16)
    j = 0
    while True:
        es2 = (x % 3) == 2
        destino = ((2 * x - 1) // 3) % mp
        cand = np.where(es2, vivo_prev[destino] + j, INF).astype(np.int16)
        np.minimum(mejor, cand, out=mejor)
        j = j + 1
        if j >= int(mejor[unid].max()):
            break
        x = (2 * x) % m
    mejor[~unid] = INF
    costes[l] = mejor

print(f"2. Conjuntos encajados S_l (malos en todo nivel de [{J0}, l])")
print("   l | #S_l       | fraccion de unidades | #S_l / (3 #S_(l-1))")
previo = None
for l in range(J0, L2 + 1):
    m = 3 ** l
    a = np.arange(m, dtype=np.int64)
    dentro = np.ones(m, dtype=bool)
    for j in range(J0, l + 1):
        dentro &= costes[j][a % (3 ** j)] > j
    dentro &= (a % 3) != 0
    n = int(dentro.sum())
    frac = n / (2 * 3 ** (l - 1))
    tasa = "" if previo is None else f"{n / (3 * previo):.4f}"
    print(f"  {l:2d} | {n:10d} | {frac:.5f}              | {tasa}")
    previo = n
