# censo_propio.py  (ADVERSARIO 3, 9a revision)
#
# CENSO DE PARES ENTEROS REALES, CAMINO PROPIO. Sin transicion(), sin
# gramatica: 2^24 pares consecutivos (x, x+1) con x = 2^24 * 2^20 + r,
# caminados con el mapa del ATAJO (n/2 si par, (3n+1)/2 si impar),
# vectorizado en numpy int64.
#
# Cuenta, por paso t = 1..24:
#   A_censo[t] = pares cuya PRIMERA igualdad x==y ocurre en t sin haber
#                pasado antes por |y-x| == 1 (absorcion del bloque)
#   R_censo[t] = pares cuyo PRIMER |y-x| == 1 (t >= 1) ocurre en t sin
#                haberse fundido antes (primer retorno al lazo)
#   F[t]       = pares con x == y en el paso t (fundidos ACUMULADO)
#
# Cruces:
#   (1) F[t] debe ser a(t) * 2^(24-t) con la a(k) publicada del repo
#       (fuerza bruta historica, k = 3..24) -- esto ata phi a la
#       definicion real de a(k)/2^k SIN pasar por la gramatica.
#   (2) R_censo / A_censo se guardan en censo_propio_RA.txt para
#       compararlos con la gramatica propia (gramatica_propia.py).
#   (3) margen: maximo del par < 2^62 en todo paso (sin overflow) y
#       ningun valor baja de 2^20 (el ciclo {1,2} inalcanzable).
#
# Nota de la casa: L = 24 NO es redondo en el sentido del punto 8
# (aqui se cuenta masa por nivel, no un efecto de un termino), y el
# cruce (1) usa TODOS los t = 3..24, no solo el borde.

import numpy as np

L = 24
M = 2 ** 20
BASE = (2 ** L) * M

A_PUBLICADA = {  # a(k), k = 3..24, de sucesiones.txt (fuerza bruta)
    3: 1, 4: 3, 5: 8, 6: 18, 7: 39, 8: 82, 9: 170, 10: 351, 11: 721,
    12: 1476, 13: 3012, 14: 6130, 15: 12450, 16: 25241, 17: 51105,
    18: 103358, 19: 208840, 20: 421643, 21: 850737, 22: 1715546,
    23: 3457791, 24: 6966495,
}


def paso(v):
    # el mapa del atajo, vectorizado; enteros int64
    impar = (v & 1).astype(bool)
    return np.where(impar, (3 * v + 1) >> 1, v >> 1)


x = BASE + np.arange(2 ** L, dtype=np.int64)
y = x + 1

# primer evento por par: 0 = vivo, 1 = retorno, 2 = fusion
evento = np.zeros(2 ** L, dtype=np.int8)

R_censo = {}
A_censo = {}
F = {}

for t in range(1, L + 1):
    x = paso(x)
    y = paso(y)
    tope = max(int(x.max()), int(y.max()))
    piso = min(int(x.min()), int(y.min()))
    if tope >= 2 ** 62:
        raise SystemExit("overflow inminente en t = %d" % t)
    if piso < M:
        raise SystemExit("un valor bajo de M en t = %d" % t)
    d = y - x
    vivo = (evento == 0)
    fusion_nueva = vivo & (d == 0)
    retorno_nuevo = vivo & ((d == 1) | (d == -1))
    A_censo[t] = int(fusion_nueva.sum())
    R_censo[t] = int(retorno_nuevo.sum())
    evento[fusion_nueva] = 2
    evento[retorno_nuevo] = 1
    F[t] = int((d == 0).sum())   # acumulado real: fundido queda fundido

# cruce (1): F[t] contra a(t) * 2^(L-t)
fallos = 0
for k in range(3, L + 1):
    esperado = A_PUBLICADA[k] * 2 ** (L - k)
    if F[k] != esperado:
        fallos += 1
        print("FALLA a(%d): censo %d, publicado*2^(L-k) %d"
              % (k, F[k], esperado))
for k in (1, 2):
    if F[k] != 0:
        fallos += 1
        print("FALLA: fusiones en t = %d (%d)" % (k, F[k]))
if fallos:
    raise SystemExit("el censo contradice la a(k) publicada en %d niveles"
                     % fallos)
print("CRUCE 1 OK: los fundidos acumulados del censo clavan a(k)*2^(24-k)")
print("para k = 3..24 contra la serie publicada de fuerza bruta.")
print()

# resumen y volcado para el cruce con la gramatica propia
rho = 0.0
alfa = 0.0
lineas = []
for t in range(1, L + 1):
    rho += R_censo.get(t, 0) / float(2 ** L)
    alfa += A_censo.get(t, 0) / float(2 ** L)
    lineas.append("%d %d %d" % (t, R_censo.get(t, 0), A_censo.get(t, 0)))
    if t >= 20 and t % 2 == 0:
        phi = alfa / (1 - rho)
        print("t = %2d   rho_acum %.6f   alfa_acum %.6f   phi_trunc %.6f"
              % (t, rho, alfa, phi))

with open("revision9_adv3/censo_propio_RA.txt", "w") as f:
    f.write("\n".join(lineas) + "\n")
print()
print("R/A por nivel guardados en revision9_adv3/censo_propio_RA.txt")
print("(t  R_censo(t)  A_censo(t), sobre 2^24 pares).")
