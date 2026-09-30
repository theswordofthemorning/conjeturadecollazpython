# Coste minimo de los caminos de Wirsching: c_l(a) = min { k : e_l(k, a) > 0 }.
#
# e_l(k, a) cuenta caminos b -> ... -> a del atajo con k pasos n/2 y l pasos
# (3n+1)/2; depende de a mod 3^l (Wirsching 2003, (1.2)). Como anadir pasos n/2 al
# principio del camino conserva su extremo, e_l(k+1, a) >= e_l(k, a): c_l(a) es el
# umbral a partir del cual la cuenta es positiva.
#
# Recurrencia hacia atras: antes del ultimo paso impar hay j pasos n/2, con
# 2^j a = 2 mod 3; ese paso impar viene de (2^(j+1) a - 1)/3. Por tanto
#   c_l(a) = min_j ( j + c_(l-1)( (2^(j+1) a - 1)/3 mod 3^(l-1) ) ),
# con c_0 = 0 y c_(l-1)(x) = infinito si x = 0 mod 3 y l-1 >= 1 (un multiplo de 3
# no tiene predecesor impar).
#
# Si c_l(a) > l, entonces e_l(k, a) = 0 para todo k <= l: la condicion (*1) de
# Wirsching falla en la sucesion k_l = l para esa clase.
#
# Calculo finito y exacto. No prueba nada para l grande.
import sys
import numpy as np

L_MAX = 16
INF = 127

print(f"Coste minimo c_l(a) sobre las unidades a mod 3^l, l <= {L_MAX}")
print(" l | max c - l | #(c > l)  fraccion | c(7) - l | c(5) - l | a con c maximo (menores)")
previo = np.zeros(1, dtype=np.int16)      # nivel 0: c_0 = 0
for l in range(1, L_MAX + 1):
    m = 3 ** l
    mp = m // 3
    a = np.arange(m, dtype=np.int32)
    unid = (a % 3) != 0
    # base(x) = c_(l-1)((2x-1)/3) si x = 2 mod 3, infinito en otro caso
    if l == 1:
        vivo_prev = np.zeros(1, dtype=np.int16)
    else:
        vivo_prev = previo.copy()
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
    cu = mejor[unid].astype(np.int64)
    exceso = int(cu.max()) - l
    malos = int((cu > l).sum())
    peores = a[unid][cu == cu.max()][:5].tolist()
    c7 = int(mejor[7 % m]) - l if 7 % m % 3 else None
    c5 = int(mejor[5 % m]) - l
    print(f"{l:2d} | {exceso:9d} | {malos:8d} {malos / unid.sum():9.4f} | {c7!s:>8} | {c5:8d} | {peores}")
    previo = mejor
    sys.stdout.flush()
