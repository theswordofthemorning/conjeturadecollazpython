# Cotejo independiente de Pandas (bloque 2 del plan del 28-09).
#
# Mapa clasico C(n) = n/2 si n es par, 3n+1 si es impar. Hasta la primera
# llegada a 1: TAU = divisiones por 2 (sigma_inf de Gao), S = pasos 3n+1,
# H = TAU + S la altura. Residuo de Roosendaal: 2^TAU = 3^S * n * Res(n).
#
# Este script no reutiliza pandas_gao.py. Calcula el residuo por otra via:
# el producto de (3y+1)/(3y) sobre las iteradas impares y de la orbita,
# propagado hacia atras con Res(n) = f(n) * Res(C(n)), y lo compara con
# 2^TAU / (3^S * n) por productos cruzados de enteros.
#
# Comprueba:
#   1. la formula del producto, exacta, para 1 <= n < 2^M_EXACTO;
#   2. Res >= 1 y el maximo de Res en [1, 2^M), con su fraccion exacta;
#   3. el nucleo aritmetico `seis` de Pandas.lean por fuerza bruta en una caja;
#   4. la pregunta de Gao en los pares n, n+1 < 2^M con igual altura, y en que
#      paso j se encuentran por primera vez; cuantos quedan cubiertos por la
#      cota sin residuos 2^j + 3 < 15 n (equilibrio_quince de Pandas.lean);
#   5. la hipotesis de base de Marmotas con B = 2^M: max Res < 4/3.
#
# Es un calculo finito: no prueba nada para todo n.
from fractions import Fraction
import math
import sys

M = 20            # rango principal: 1 <= n < 2^M
M_EXACTO = 14     # rango de la comprobacion exacta del producto
CAJA_N = 30       # caja de fuerza bruta para `seis`
CAJA_E = 14
CAJA_Y = 8

N = 2 ** M


def C(n):
    if n % 2 == 0:
        return n // 2
    return 3 * n + 1


# Altura, divisiones y pasos impares con memoria sobre la orbita completa.
H = {1: 0}
TAU = {1: 0}
S = {1: 0}
RES = {1: 1.0}   # flotante, solo para localizar candidatos al maximo


def calcular(n):
    pila = []
    x = n
    while x not in H:
        pila.append(x)
        x = C(x)
    while pila:
        y = pila.pop()
        z = C(y)
        H[y] = H[z] + 1
        if y % 2 == 0:
            TAU[y] = TAU[z] + 1
            S[y] = S[z]
            RES[y] = RES[z]
        else:
            TAU[y] = TAU[z]
            S[y] = S[z] + 1
            RES[y] = RES[z] * (3 * y + 1) / (3 * y)


for n in range(1, N + 1):
    calcular(n)

# 1. Formula del producto, exacta.
malos = 0
for n in range(1, 2 ** M_EXACTO):
    num = 1
    den = 1
    x = n
    while x != 1:
        if x % 2 == 1:
            num = num * (3 * x + 1)
            den = den * (3 * x)
        x = C(x)
    if num * 3 ** S[n] * n != den * 2 ** TAU[n]:
        malos = malos + 1
print(f"1. Producto de (3y+1)/(3y) = 2^TAU/(3^S n) para 1 <= n < 2^{M_EXACTO}: "
      f"{'OK' if malos == 0 else 'FALLA en ' + str(malos)}")

# 2. Res >= 1 y maximo exacto.
bajo_uno = 0
for n in range(1, N):
    if 2 ** TAU[n] < 3 ** S[n] * n:
        bajo_uno = bajo_uno + 1
tope = max(RES[n] for n in range(1, N))
candidatos = [n for n in range(1, N) if RES[n] > tope * (1 - 1e-9)]
mejor = max(Fraction(2 ** TAU[n], 3 ** S[n] * n) for n in candidatos)
donde = [n for n in candidatos if Fraction(2 ** TAU[n], 3 ** S[n] * n) == mejor]
# Confirmacion exacta de que ningun n fuera de los candidatos lo supera.
supera = 0
for n in range(1, N):
    if n not in donde and 2 ** TAU[n] * mejor.denominator >= mejor.numerator * 3 ** S[n] * n:
        supera = supera + 1
print(f"2. Res < 1 en [1, 2^{M}): {bajo_uno} casos")
print(f"   maximo exacto: {mejor} = {float(mejor):.12f}")
print(f"   se alcanza en {donde}; otros n con Res >= maximo: {supera}")

# 3. Fuerza bruta del nucleo `seis`.
contra = 0
casos = 0
for n in range(0, CAJA_N + 1):
    for Y in range(0, CAJA_Y + 1):
        for t1 in range(CAJA_E + 1):
            for s1 in range(CAJA_E + 1):
                for t2 in range(CAJA_E + 1):
                    s2 = t1 + s1 - t2
                    if s2 < 0 or s2 > CAJA_E:
                        continue
                    L1 = 3 ** s1 * n <= 2 ** t1 * Y
                    L2 = 3 ** s2 * (n + 1) <= 2 ** t2 * Y
                    U1 = 2 ** t1 * Y <= 6 * (3 ** s1 * n)
                    U2 = 2 ** t2 * Y < 6 * (3 ** s2 * n)
                    if L1 and L2 and U1 and U2:
                        casos = casos + 1
                        if t1 != t2:
                            contra = contra + 1
print(f"3. Nucleo `seis` en la caja n<={CAJA_N}, Y<={CAJA_Y}, exponentes<={CAJA_E}: "
      f"{casos} casos con hipotesis, {contra} con t1 != t2")

# 4. Pregunta de Gao y primer encuentro.
iguales = 0
distinto_tau = 0
cubiertos = 0
j_max_rel = 0.0
peor = None
for n in range(1, N - 1):
    if H[n] != H[n + 1]:
        continue
    iguales = iguales + 1
    if TAU[n] != TAU[n + 1]:
        distinto_tau = distinto_tau + 1
    x = n
    y = n + 1
    j = 0
    while x != y:
        x = C(x)
        y = C(y)
        j = j + 1
    if 2 ** j + 3 < 15 * n:
        cubiertos = cubiertos + 1
    rel = j - math.log2(n)
    if rel > j_max_rel:
        j_max_rel = rel
        peor = (n, j)
print(f"4. Pares n, n+1 < 2^{M} con igual altura: {iguales}; con distinto TAU: {distinto_tau}")
print(f"   primer encuentro con 2^j + 3 < 15n (sin hipotesis de residuo): {cubiertos}")
print(f"   sin esa cobertura: {iguales - cubiertos}; mayor j - log2(n): "
      f"{j_max_rel:.3f} en n = {peor[0]}, j = {peor[1]}")

# 5. Base de Marmotas con B = 2^M.
cota = Fraction(4, 3)
print(f"5. Base de Marmotas, B = 2^{M}: max Res = {float(mejor):.9f} "
      f"{'<' if mejor < cota else '>='} 4/3")
print(f"   factor de transporte admitido: (1 + 1/(3B))^S con S <= 2B = {2 * N}, a lo sumo 3")
print(f"   cota resultante para Res: 3 * max Res = {float(3 * mejor):.6f} < 4")

sys.exit(0 if (malos == 0 and bajo_uno == 0 and contra == 0 and distinto_tau == 0
               and supera == 0 and mejor < cota) else 1)
