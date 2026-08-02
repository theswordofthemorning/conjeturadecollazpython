# A3.py - AGENTE 2 (independiente). Verificacion del ITEM A3:
#
#   log2( altitud_atajo(n)/n ) >= racha(n) * log2(3/2)
#
# que en enteros exactos (sin logaritmos, sin floats) equivale a:
#
#   altitud_atajo(n) * 2^r >= n * 3^r      con r = racha(n)
#
# MAPA USADO: el ATAJO:  n par -> n/2 ;  n impar -> (3n+1)/2.
# (El clasico seria n impar -> 3n+1; el enunciado dice explicitamente atajo.)
#
# Definiciones derivadas desde cero:
#   racha(n)          = numero de valores IMPARES consecutivos al arrancar la
#                       trayectoria del atajo en n (n impar cuenta; se corta en
#                       el primer par). n par -> racha 0.
#   altitud_atajo(n)  = maximo de la trayectoria del atajo desde n hasta
#                       llegar a 1, INCLUYENDO n. (Convencion A: si n == 1 la
#                       trayectoria es [1] y la altitud es 1. Convencion B:
#                       se da al menos una vuelta, 1 -> 2 -> 1, altitud 2.
#                       El borde n = 1 se examina con las dos.)
#
# Todo lo que decide es int de Python. Los floats solo aparecen en prints.

import sys

LIMITE = 300000          # rango del barrido principal (n = 2 .. LIMITE)
fallos = 0

def paso_atajo(n):
    if n % 2 == 0:
        return n // 2
    return (3 * n + 1) // 2      # 3n+1 es par si n impar: division exacta

def racha(n):
    r = 0
    v = n
    while v % 2 == 1:
        r += 1
        v = paso_atajo(v)
    return r

def altitud_atajo(n):
    # Convencion A: hasta llegar a 1; si n == 1 no se da ningun paso.
    alt = n
    v = n
    while v != 1:
        v = paso_atajo(v)
        if v > alt:
            alt = v
    return alt

# ---------------------------------------------------------------------------
# COMPROBACION 0: sanidad de las definiciones en casos calculados a mano.
#   racha(1) = 1 (1 impar -> 2 par). racha(7): 7,11,17,26 -> 3 impares.
#   racha(2^k - 1) = k.
# ---------------------------------------------------------------------------
if racha(1) != 1: raise SystemExit("FALLO sanidad: racha(1)")
if racha(2) != 0: raise SystemExit("FALLO sanidad: racha(2)")
if racha(7) != 3: raise SystemExit("FALLO sanidad: racha(7)")
for k in range(1, 21):
    if racha(2**k - 1) != k:
        raise SystemExit("FALLO sanidad: racha(2^%d - 1)" % k)
# altitud de 7 bajo el atajo: 7,11,17,26,13,20,10,5,8,4,2,1 -> max 26
if altitud_atajo(7) != 26: raise SystemExit("FALLO sanidad: altitud_atajo(7)")
print("[0] sanidad de definiciones: OK (racha y altitud a mano)")

# ---------------------------------------------------------------------------
# COMPROBACION 1: la identidad que demuestra el piso, verificada aparte.
# En la racha, cada paso impar cumple 2*v' = 3*v + 1, luego tras r pasos:
#   2^r * v_r = 3^r * n + C   con   C = 3^(r-1) + 3^(r-2)*2 + ... + 2^(r-1) > 0
# y v_r esta en la trayectoria, luego altitud >= v_r y el piso sale ESTRICTO
# para r >= 1. Verifico la identidad exacta en un rango de impares.
# ---------------------------------------------------------------------------
for n in range(1, 20002, 2):
    r = racha(n)
    v = n
    for _ in range(r):
        v = paso_atajo(v)
    C = 2**r * v - 3**r * n
    C_teorico = sum(3**(r - 1 - i) * 2**i for i in range(r))
    if C != C_teorico or (r >= 1 and C <= 0):
        fallos += 1
        print("FALLO identidad en n =", n)
if fallos: raise SystemExit("FALLO en la comprobacion 1")
print("[1] identidad 2^r*v_r = 3^r*n + C con C > 0: OK en 10.001 impares (n = 1..20001)")

# ---------------------------------------------------------------------------
# COMPROBACION 2: el enunciado en enteros, barrido n = 2 .. LIMITE.
#   alt * 2^r >= n * 3^r
# Cuento tambien igualdades y el minimo de holgura relativa para informar.
# ---------------------------------------------------------------------------
igualdades = 0
casos = 0
for n in range(2, LIMITE + 1):
    r = racha(n)
    alt = altitud_atajo(n)
    izq = alt * 2**r
    der = n * 3**r
    casos += 1
    if izq < der:
        fallos += 1
        print("CONTRAEJEMPLO: n =", n, "r =", r, "alt =", alt)
    elif izq == der:
        igualdades += 1
if fallos: raise SystemExit("FALLO en la comprobacion 2")
print("[2] piso alt*2^r >= n*3^r: OK,", casos, "casos (n = 2..%d), 0 fallos," % LIMITE,
      igualdades, "igualdades (todas con r = 0)")

# ---------------------------------------------------------------------------
# COMPROBACION 3: bordes.
#   n = 1 con las dos convenciones de altitud.
#   n = 2, potencias de 2 (r = 0, igualdad exacta), n par generico,
#   2^k - 1 (racha maxima).
# ---------------------------------------------------------------------------
# n = 1, convencion A (trayectoria [1], altitud 1): 1*2^1 = 2 < 3 = 1*3^1
alt1_A = altitud_atajo(1)
izq_A, der_A = alt1_A * 2**racha(1), 1 * 3**racha(1)
print("[3a] n = 1, convencion A (parar en 1): alt =", alt1_A,
      "->", izq_A, ">=", der_A, ":", izq_A >= der_A)

# n = 1, convencion B (dar la vuelta 1 -> 2 -> 1, altitud 2): 2*2 = 4 >= 3
alt1_B = 2
izq_B = alt1_B * 2**racha(1)
print("[3b] n = 1, convencion B (una vuelta): alt = 2 ->", izq_B, ">=", der_A, ":", izq_B >= der_A)

# potencias de 2: r = 0, alt = n, igualdad exacta
for k in range(1, 40):
    n = 2**k
    r = racha(n)
    if r != 0: raise SystemExit("FALLO borde: racha(2^%d) != 0" % k)
    # altitud de una potencia de 2 es ella misma (solo divide)
    v, alt = n, n
    while v != 1:
        v = paso_atajo(v)
        if v > alt: alt = v
    if alt * 2**r != n * 3**r:
        raise SystemExit("FALLO borde: potencia de 2 sin igualdad, k = %d" % k)
print("[3c] potencias de 2 hasta 2^39: r = 0 y IGUALDAD exacta alt = n, 0 fallos")

# 2^k - 1: racha k, el piso es el mas exigente posible
for k in range(2, 26):
    n = 2**k - 1
    r = racha(n)
    v = n
    for _ in range(r):
        v = paso_atajo(v)
    # v esta en la trayectoria, luego alt >= v; basta comprobar v * 2^r >= n * 3^r
    if v * 2**r < n * 3**r:
        raise SystemExit("FALLO borde: 2^%d - 1" % k)
print("[3d] n = 2^k - 1, k = 2..25: racha = k y el piso aguanta (via v_r, sin recorrer la trayectoria entera)")

# ---------------------------------------------------------------------------
# COMPROBACION 4: reproducir el conteo del repo: n = 2..100000 son 99.999 casos.
# ---------------------------------------------------------------------------
casos_repo = 100000 - 2 + 1
print("[4] el rango n = 2..100000 tiene", casos_repo, "casos: coincide con los '99.999 casos, 0 fallos' declarados")

# ---------------------------------------------------------------------------
# COMPROBACION 5: holgura minima con r >= 1 (debe ser estricta: C > 0).
# La holgura entera minima es alt*2^r - n*3^r; para impares de racha 1 vale
# exactamente C = 1 cuando alt = v_1 = (3n+1)/2... la reporto medida.
# ---------------------------------------------------------------------------
min_holg = None
arg = None
for n in range(3, 100001, 2):
    r = racha(n)
    alt = altitud_atajo(n)
    h = alt * 2**r - n * 3**r
    if h <= 0:
        raise SystemExit("FALLO: holgura no positiva con r >= 1 en n = %d" % n)
    if min_holg is None or h < min_holg:
        min_holg, arg = h, n
print("[5] holgura entera minima con n impar (3..99999):", min_holg, "en n =", arg,
      "-> estricta siempre que r >= 1, como exige C > 0")

print()
print("VEREDICTO LOCAL: el piso alt*2^r >= n*3^r se sostiene en todo el rango")
print("verificado (n = 2..%d), con igualdad solo en r = 0 y estricto si r >= 1." % LIMITE)
print("El unico borde delicado es n = 1: falla con la convencion 'parar en 1'")
print("(2 < 3) y se cumple si la altitud da la vuelta 1 -> 2 (4 >= 3).")
