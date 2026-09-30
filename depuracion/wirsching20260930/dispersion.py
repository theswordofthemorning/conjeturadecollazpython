# Dispersion de las funciones Elka de Wirsching entre las clases mod 3^l.
#
# e_l(k, a): caminos del atajo que llegan a a con k pasos n/2 y l pasos (3n+1)/2
# (misma recurrencia que elka.py). Para k = l y k = l + floor(sqrt(l)) se mide,
# sobre las unidades a mod 3^l con peso uniforme, el cociente r(a) = e_l(k,a)/ebar:
#   - cuantiles 10 %, 25 % y 50 % de r;
#   - M2 = media de r^2 (1 si la cuenta fuera uniforme; crece si se concentra);
#   - masa del 10 % de clases mas cargadas.
# (*1) de Wirsching pide r(a) >= mu para toda a en la ventana |k - l| <= delta*sqrt(l).
#
# Calculo finito y exacto (enteros); los cocientes se imprimen en coma flotante.
import math
import numpy as np

L_MAX = 14
EXTRA = 4          # k llega hasta l + EXTRA + ... (ver K_MAX)
K_MAX = L_MAX + int(math.isqrt(L_MAX)) + 1


def niveles():
    previo = None
    for l in range(0, L_MAX + 1):
        m = 3 ** l
        tabla = np.zeros((K_MAX + 1, m), dtype=np.int32)
        if l == 0:
            tabla[:, 0] = 1
        else:
            a = np.arange(m, dtype=np.int64)
            doble = (2 * a) % m
            es2 = (a % 3) == 2
            destino = ((2 * a - 1) // 3) % (m // 3)
            for k in range(0, K_MAX + 1):
                subida = np.where(es2, previo[k][destino], 0)
                tabla[k] = subida if k == 0 else tabla[k - 1][doble] + subida
        yield l, tabla
        previo = tabla


print(f"Dispersion de e_l(k, a)/ebar_l(k) sobre las unidades mod 3^l, l <= {L_MAX}")
print(" l   k |  q10     q25     q50  |   M2     | masa del 10% mas cargado")
for l, tabla in niveles():
    if l < 2:
        continue
    m = 3 ** l
    u = (np.arange(m) % 3) != 0
    for k in (l, l + math.isqrt(l)):
        fila = tabla[k][u].astype(np.float64)
        total = float(math.comb(k + l, k))
        assert abs(fila.sum() - total) < 0.5
        r = fila / (total / u.sum())
        q10, q25, q50 = np.quantile(r, [0.10, 0.25, 0.50])
        m2 = float((r * r).mean())
        orden = np.sort(fila)[::-1]
        top = float(orden[: max(1, len(orden) // 10)].sum() / total)
        print(f"{l:2d} {k:3d} | {q10:6.3f}  {q25:6.3f}  {q50:6.3f} | {m2:8.3f} | {top:6.3f}")
