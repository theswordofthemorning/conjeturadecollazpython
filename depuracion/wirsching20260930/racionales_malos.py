# Candidatos estructurados a a* (W1): racionales p/q, con 3 que no divide a p ni a q,
# vistos como unidades 3-adicas, que son malos (c_l > l) en todos los niveles de
# [J0, L]. Para cada uno se imprime su perfil de excesos c_l - l, l = 1..L.
# c_l es el coste minimo de costo.py. Calculo finito y exacto.
import math
import numpy as np

L = 16
J0 = 8
Q_MAX = 40
P_MAX = 400
INF = 127

costes = {0: np.zeros(1, dtype=np.int16)}
for l in range(1, L + 1):
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


def perfil(p, q):
    return [int(costes[l][(p * pow(q, -1, 3 ** l)) % 3 ** l]) - l for l in range(1, L + 1)]


vistos = set()
hallados = []
for q in range(1, Q_MAX + 1):
    if q % 3 == 0:
        continue
    for p in range(-P_MAX, P_MAX + 1):
        if p % 3 == 0 or math.gcd(p, q) != 1:
            continue
        pr = perfil(p, q)
        if all(pr[l - 1] > 0 for l in range(J0, L + 1)):
            clave = (p, q)
            if clave not in vistos:
                vistos.add(clave)
                hallados.append((sum(pr[J0 - 1:]), p, q, pr))

hallados.sort(reverse=True)
print(f"Racionales p/q (|p| <= {P_MAX}, q <= {Q_MAX}) malos en todo nivel de [{J0}, {L}]: {len(hallados)}")
for s, p, q, pr in hallados[:40]:
    malos_desde = next((l for l in range(1, L + 1) if all(pr[j - 1] > 0 for j in range(l, L + 1))), None)
    print(f"  {p:5d}/{q:<3d} malo en todo [{malos_desde}, {L}]  excesos: {pr}")
