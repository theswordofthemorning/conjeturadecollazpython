# A10 - verificacion independiente (Agente 2, Python, a ciegas)
#
# ENUNCIADO: "Collatz sobre los enteros negativos es exactamente el mapa 3m-1
#             sobre los positivos", para todo m >= 1.
#
# MAPA DEL ENUNCIADO: el CLASICO (n par -> n/2, n impar -> 3n+1), aplicado a
# enteros negativos n = -m. El mapa espejo sobre positivos es el 3m-1 clasico
# (m par -> m/2, m impar -> 3m-1).
#
# Derivacion propia (dos lineas, y luego se comprueba con numeros):
#   n = -m par   ->  n/2   = -(m/2)
#   n = -m impar ->  3n+1  = -3m+1 = -(3m-1)
# o sea T_neg(-m) = -T_3m1(m) paso a paso, para todo m >= 1.
#
# Todo con int exacto. Ningun float decide nada.

import sys

FALLOS = []

def fallo(msg):
    FALLOS.append(msg)
    print("FALLO:", msg)

# ---------------------------------------------------------------------------
# Implementacion A del lado negativo: opera directamente sobre el entero
# negativo. La paridad se mira con n % 2 (en Python (-7) % 2 == 1, correcto).
# La division SOLO se aplica si el numero es par, y se comprueba que es exacta
# con divmod, para que ningun floor de negativos pueda colarse.
def paso_neg_directo(n):
    if n % 2 == 0:
        q, r = divmod(n, 2)
        if r != 0:
            raise AssertionError("division no exacta en " + str(n))
        return q
    else:
        return 3 * n + 1

# Implementacion B del lado negativo: separa signo y magnitud. Nunca divide
# un negativo: trabaja con la magnitud positiva y le pega el signo al final.
def paso_neg_magnitud(n):
    if n >= 0:
        raise AssertionError("esta implementacion es solo para negativos")
    m = -n
    if m % 2 == 0:
        return -(m // 2)
    else:
        # 3n+1 con n = -m:  3*(-m)+1 = -(3m-1)
        return -(3 * m - 1)

# El mapa 3m-1 clasico sobre positivos.
def paso_3m1(m):
    if m % 2 == 0:
        return m // 2
    else:
        return 3 * m - 1

# ---------------------------------------------------------------------------
# COMPROBACION 0 (bordes y algebra): identidad de un paso, exhaustiva
# para m = 1 .. 200.000 (incluye m=1, m=2, pares e impares).
# m = 0 se mira aparte: el enunciado tiene ambito m >= 1.
print("[0] identidad de un paso, m = 1 .. 200000")
for m in range(1, 200001):
    n = -m
    a = paso_neg_directo(n)
    b = paso_neg_magnitud(n)
    c = paso_3m1(m)
    if a != b:
        fallo("las dos implementaciones negativas discrepan en n=%d: %d vs %d" % (n, a, b))
        break
    if a != -c:
        fallo("T_neg(-m) != -T_3m1(m) en m=%d: %d vs %d" % (m, a, -c))
        break
else:
    print("    0 fallos en 200000 valores (paso unico, dos implementaciones)")

# borde m=0 (fuera del ambito, se documenta): n=0 -> 0, y 3m-1 sobre 0 -> 0
print("[0b] borde m=0: T(0) =", paso_neg_directo(0), " (par, queda en 0; fuera del ambito m>=1)")

# borde de paridad en Python: -7 % 2 debe ser 1 (impar detectado bien)
if (-7) % 2 != 1:
    fallo("la paridad de -7 salio mal")
else:
    print("[0c] paridad de negativos en Python: (-7) %% 2 == 1, correcto")

# ---------------------------------------------------------------------------
# COMPROBACION 1: trayectorias enteras en paralelo, m = 1 .. 100000,
# cada una hasta entrar en un ciclo del mapa 3m-1 (los tres conocidos,
# construidos aqui mismo caminando, no copiados).
def ciclo_desde(semilla):
    vistos = {}
    x = semilla
    i = 0
    while x not in vistos:
        vistos[x] = i
        x = paso_3m1(x)
        i += 1
    arranque = vistos[x]
    # reconstruir el ciclo
    ciclo = []
    y = semilla
    for _ in range(arranque):
        y = paso_3m1(y)
    z = y
    while True:
        ciclo.append(z)
        z = paso_3m1(z)
        if z == y:
            break
    return ciclo

c1 = ciclo_desde(1)
c2 = ciclo_desde(5)
c3 = ciclo_desde(17)
print("[1] ciclos construidos caminando: largos", len(c1), len(c2), len(c3))
SUMIDEROS = set(c1) | set(c2) | set(c3)

pasos_totales = 0
sin_clasificar = 0
LIMITE_PASOS = 100000  # tope de seguridad por trayectoria

for m in range(1, 100001):
    n = -m
    pos = m
    pasos = 0
    while pos not in SUMIDEROS:
        n2 = paso_neg_directo(n)
        n3 = paso_neg_magnitud(n)
        p2 = paso_3m1(pos)
        if n2 != n3 or n2 != -p2:
            fallo("discrepancia en trayectoria de m=%d, paso %d" % (m, pasos))
            break
        n, pos = n2, p2
        pasos += 1
        if pasos > LIMITE_PASOS:
            sin_clasificar += 1
            break
    else:
        # ya en sumidero: comprobar que el lado negativo esta en el ciclo espejo
        if -n not in SUMIDEROS:
            fallo("el lado negativo no cayo en el ciclo espejo, m=%d" % m)
    pasos_totales += pasos

print("    m = 1 .. 100000: pasos comparados =", pasos_totales,
      "| sin clasificar =", sin_clasificar)

# ---------------------------------------------------------------------------
# COMPROBACION 2: el floor de Python nunca actua sobre un impar negativo.
# (-7)//2 == -4 seria un peligro, pero los impares multiplican, no dividen.
# Se comprueba que en la implementacion directa jamas se llama a dividir
# con resto distinto de 0 (el divmod de arriba ya corta con AssertionError;
# si llegamos aqui, no salto nunca).
print("[2] ninguna division inexacta salto en", pasos_totales + 200000, "pasos")

# ---------------------------------------------------------------------------
if FALLOS:
    raise SystemExit("HAY %d FALLOS - el enunciado NO se sostiene tal cual" % len(FALLOS))
print()
print("VEREDICTO LOCAL: 0 fallos. T_neg(-m) = -T_3m1(m) paso a paso,")
print("comprobado exhaustivo m = 1..200000 (un paso) y m = 1..100000")
print("(trayectorias enteras hasta ciclo), con dos implementaciones")
print("negativas que no comparten la division.")
