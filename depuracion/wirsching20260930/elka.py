# Instancia limitada del eslabon abierto de Wirsching (2003): la condicion (*1).
#
# Mapa del atajo T(n) = n/2 (par) o (3n+1)/2 (impar). Funcion Elka de Wirsching:
#   e_l(k, a) = numero de caminos b -> ... -> a con k pasos n/2 y l pasos (3n+1)/2.
# Depende solo de a mod 3^l. Su media de Haar sobre las unidades de Z_3 es
#   ebar_l(k) = C(k+l, k) / (2 * 3^(l-1))                  [Wirsching, (1.4)].
# (*1): existen delta, mu > 0 con e_l(k, a) >= mu * ebar_l(k) para todo l grande,
# toda k con |k - l| <= delta*sqrt(l) y toda unidad a. Por el Teorema 1 de
# Wirsching, (*1) da densidad positiva uniforme de predecesores.
#
# Recurrencia hacia atras desde a: el paso n/2 viene de 2a; el paso (3n+1)/2 viene
# de (2a-1)/3, que existe si y solo si a = 2 mod 3 (y entonces es impar). Asi
#   e_l(k, a) = e_l(k-1, 2a) + [a = 2 mod 3] * e_(l-1)(k, (2a-1)/3),
# con e_0(k, a) = 1 y e_l(-1, a) = 0.
#
# Generadores g_l(k, a) de Wirsching, (2.1): g_0(k, a) = [k = 0] y
#   g_(l+1)(k, a) = sum_{j=0}^{2*3^l - 1} g_l(k - j, (2^(j+1) a - 1)/3).
# Para k < 2*3^(l-1) el tope de j no actua y vale la misma recurrencia de dos
# terminos con g en lugar de e; en niveles bajos se aplica el tope.
#
# Cotejo independiente: para l <= L_BRUTO se enumeran todas las palabras de
# paridad y se calcula el extremo r = 2^(-n) * sum_i 3^(l-1-i) 2^(s_i) mod 3^l.
#
# Calculo finito y exacto (enteros). No prueba nada para l grande.
import math
import sys
import numpy as np

L_MAX = 13        # nivel maximo
DELTA = 1.0       # radio de la ventana |k - l| <= DELTA * sqrt(l)
L_BRUTO = 7       # niveles cotejados por enumeracion de palabras
K_MAX = L_MAX + int(math.ceil(DELTA * math.sqrt(L_MAX))) + 1


def niveles(base_e):
    """Genera (l, tabla) con tabla[k] = array de e_l(k, a), a = 0..3^l - 1.

    base_e=True da las funciones Elka; False, los generadores g."""
    previo = None
    for l in range(0, L_MAX + 1):
        m = 3 ** l
        tabla = np.zeros((K_MAX + 1, m), dtype=np.int64)
        if l == 0:
            if base_e:
                tabla[:, 0] = 1
            else:
                tabla[0, 0] = 1
        else:
            a = np.arange(m, dtype=np.int64)
            doble = (2 * a) % m
            es2 = (a % 3) == 2
            destino = ((2 * a - 1) // 3) % (m // 3)
            tope = 2 * 3 ** (l - 1)       # numero de j admitidos en g
            for k in range(0, K_MAX + 1):
                subida = np.where(es2, previo[k][destino], 0)
                if k == 0:
                    tabla[k] = subida
                elif base_e or k < tope:
                    tabla[k] = tabla[k - 1][doble] + subida
                else:
                    # g con tope: suma directa sobre j < tope (solo niveles bajos)
                    total = np.zeros(m, dtype=np.int64)
                    potencia = a.copy()
                    for j in range(0, tope):
                        potencia_j = (a * pow(2, j + 1, 3 * m)) % (3 * m)
                        valido = (potencia_j % 3) == 1
                        if k - j >= 0:
                            d = ((potencia_j - 1) // 3) % (m // 3)
                            total = total + np.where(valido, previo[k - j][d], 0)
                    tabla[k] = total
        yield l, tabla
        previo = tabla


def bruto(l, k):
    """Histograma de extremos mod 3^l por enumeracion de palabras."""
    from itertools import combinations
    n = k + l
    m = 3 ** l
    inv = pow(2, -n, m) if m > 1 else 0
    hist = np.zeros(m, dtype=np.int64)
    for pos in combinations(range(n), l):
        s = 0
        for i, p in enumerate(pos):
            s = s + 3 ** (l - 1 - i) * 2 ** p
        hist[(s * inv) % m] += 1
    return hist


def unidades(m):
    a = np.arange(m)
    return (a % 3) != 0


print(f"Elka: l <= {L_MAX}, ventana |k - l| <= {DELTA} * sqrt(l), k <= {K_MAX}")
fallos = 0
tablas_e = {}
print(" l |  k=l: min e/ebar   max e/ebar   a del minimo   ceros | ventana: min e/ebar (k)")
for l, tabla in niveles(True):
    if l == 0:
        continue
    m = 3 ** l
    u = unidades(m)
    # comprobacion (1.4): suma sobre unidades = C(k+l, k), cero fuera de unidades
    for k in range(K_MAX + 1):
        if tabla[k][u].sum() != math.comb(k + l, k) or tabla[k][~u].any():
            fallos = fallos + 1
    if l <= L_BRUTO:
        for k in range(0, min(K_MAX, 9) + 1):
            if not np.array_equal(bruto(l, k), tabla[k]):
                fallos = fallos + 1
    media = lambda k: math.comb(k + l, k) / (2 * 3 ** (l - 1))
    fila = tabla[l][u]
    cocientes = fila / media(l)
    amin = int(np.arange(m)[u][np.argmin(fila)])
    ceros = int((fila == 0).sum())
    radio = DELTA * math.sqrt(l)
    ventana = [k for k in range(K_MAX + 1) if abs(k - l) <= radio]
    peor = min((tabla[k][u].min() / media(k), k) for k in ventana)
    print(f"{l:2d} | {cocientes.min():14.6f} {cocientes.max():12.4f} {amin:14d} {ceros:7d} |"
          f" {peor[0]:10.6f} ({peor[1]})")
    tablas_e[l] = tabla

print()
print("Generadores g (condicion (*2)/(*3)):")
print(" l |  k=l: min g/gbar   max g/gbar   ceros | ventana: min g/gbar (k)")
for l, tabla in niveles(False):
    if l == 0:
        continue
    m = 3 ** l
    u = unidades(m)
    fila = tabla[l][u]
    gbar = fila.sum() / u.sum()
    ceros = int((fila == 0).sum())
    radio = DELTA * math.sqrt(l)
    ventana = [k for k in range(K_MAX + 1) if abs(k - l) <= radio]
    peor = min(((tabla[k][u].min() / (tabla[k][u].sum() / u.sum())) if tabla[k][u].sum() else 0.0, k)
               for k in ventana)
    print(f"{l:2d} | {fila.min() / gbar:14.6f} {fila.max() / gbar:12.4f} {ceros:7d} |"
          f" {peor[0]:10.6f} ({peor[1]})")

print()
print(f"Comprobaciones (suma = C(k+l,k), soporte en unidades, enumeracion l <= {L_BRUTO}): "
      f"{'OK' if fallos == 0 else str(fallos) + ' FALLOS'}")
sys.exit(0 if fallos == 0 else 1)
