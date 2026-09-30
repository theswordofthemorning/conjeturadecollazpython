# Clases "malas" de Wirsching: B_l = { a unidad mod 3^l : c_l(a) > l }, donde
# c_l(a) = min { k : e_l(k, a) > 0 } (ver costo.py). En a de B_l la funcion Elka
# se anula en k = l, luego (*1) falla en la sucesion k_l = l para esa clase.
#
# Si un mismo 3-adico a* esta en B_l para infinitos l, entonces
# lim inf e_l(l, a*)/ebar_l(l) = 0 y (*1) falla en a* para todo delta y mu;
# por las implicaciones demostradas (*3) => (*2) => (*1), tambien falla (*3), y
# como (*4) esta demostrada (Tavares 2026), la Conjetura 2 de Wirsching seria falsa
# tal como esta enunciada sobre Z_3^x. Por el teorema de Baire basta que, para
# cada m, los B_l con l grande corten todas las clases unidad mod 3^m.
#
# Este script mide, para l <= L_MAX:
#   1. si B_l corta cada clase unidad mod 3^m (m = 1..M_MAX);
#   2. cuantas clases a mod 3^L_MAX estan en B_l para todos los l de un tramo final;
#   3. la clase mod 3^L_MAX con mas niveles malos entre L_MIN y L_MAX.
# Calculo finito y exacto. No prueba nada para l grande.
import sys
import numpy as np

L_MAX = 16
L_MIN = 8
M_MAX = 12
INF = 127

costes = {0: np.zeros(1, dtype=np.int16)}
for l in range(1, L_MAX + 1):
    m = 3 ** l
    mp = m // 3
    a = np.arange(m, dtype=np.int32)
    unid = (a % 3) != 0
    if l == 1:
        vivo_prev = np.zeros(1, dtype=np.int16)
    else:
        vivo_prev = costes[l - 1].copy()
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

print(f"1. B_l corta todas las clases unidad mod 3^m?  (l <= {L_MAX}, m <= {M_MAX})")
for l in range(L_MIN, L_MAX + 1):
    m3 = 3 ** l
    a = np.arange(m3, dtype=np.int64)
    malo = (costes[l] > l) & (costes[l] < INF)
    fila = []
    for mm in range(1, min(M_MAX, l) + 1):
        q = 3 ** mm
        clases = np.unique(a[malo] % q)
        total = 2 * 3 ** (mm - 1)
        fila.append(f"{len(clases)}/{total}")
    print(f"  l={l:2d}: " + " ".join(fila))

print()
print(f"2. Clases a mod 3^{L_MAX} malas en todos los niveles de un tramo final")
m_top = 3 ** L_MAX
a_top = np.arange(m_top, dtype=np.int64)
unid_top = (a_top % 3) != 0
cuenta = np.zeros(m_top, dtype=np.int16)
racha = np.ones(m_top, dtype=bool)
for l in range(L_MAX, L_MIN - 1, -1):
    malo_l = costes[l][a_top % (3 ** l)] > l
    cuenta = cuenta + malo_l
    racha = racha & malo_l
    print(f"  malas en todo l de [{l}, {L_MAX}]: {int((racha & unid_top).sum())}")
mejor_a = int(np.argmax(np.where(unid_top, cuenta, -1)))
niveles = [l for l in range(L_MIN, L_MAX + 1) if costes[l][mejor_a % (3 ** l)] > l]
print()
print(f"3. Clase con mas niveles malos en [{L_MIN}, {L_MAX}]: a = {mejor_a} mod 3^{L_MAX}, "
      f"{int(cuenta[mejor_a])} niveles: {niveles}")
print("   excesos c_l - l:", [int(costes[l][mejor_a % (3 ** l)]) - l for l in range(1, L_MAX + 1)])
