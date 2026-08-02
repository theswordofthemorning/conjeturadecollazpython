# A8 - verificacion independiente
# ENUNCIADO: los patrones de paridad alcanzables en k pasos del mapa CLASICO
#            (n par -> n/2 ; n impar -> 3n+1) son F(k+2), los Fibonacci.
# Ambito declarado en la base: k = 1..10. Aqui se verifica k = 0..16.
#
# Derivacion propia:
#  - patron de paridad = tupla de k bits, bit_i = paridad del numero ANTES del paso i
#    (1 = impar, 0 = par).
#  - tras un paso impar (3n+1) el resultado es par, luego "11" es imposible.
#  - cadenas binarias de largo k sin "11" = F(k+2) (conteo clasico).
#  - falta ver que TODAS las cadenas sin "11" se alcanzan de verdad.
#
# Todo con enteros de Python. Nada de floats en lo que decide.

import sys

def paso(n):
    # mapa clasico
    if n % 2 == 0:
        return n // 2
    return 3 * n + 1

def patron(n, k):
    bits = []
    for _ in range(k):
        bits.append(n % 2)
        n = paso(n)
    return tuple(bits)

def fib(m):
    # F(1) = 1, F(2) = 1
    a, b = 0, 1
    for _ in range(m):
        a, b = b, a + b
    return a

def cuenta_sin_11(k):
    # DP: cadenas binarias de largo k sin dos 1 seguidos
    if k == 0:
        return 1
    term0, term1 = 1, 1   # cadenas de largo 1 que terminan en 0 / en 1
    for _ in range(k - 1):
        term0, term1 = term0 + term1, term0
    return term0 + term1

fallos = 0

# ---------------------------------------------------------------
# COMPROBACION 0: el patron de k pasos depende solo de n mod 2^k
# (necesario para que barrer residuos cubra todos los n positivos)
# ---------------------------------------------------------------
import random
random.seed(12345)
for k in range(1, 17):
    for _ in range(50):
        n = random.randint(1, 10**9)
        if patron(n, k) != patron(n + (1 << k), k):
            print("FALLO invariancia mod 2^k: k=%d n=%d" % (k, n))
            fallos += 1
print("[0] invariancia mod 2^k: k=1..16, 50 muestras aleatorias por k, fallos =", fallos)

# ---------------------------------------------------------------
# COMPROBACION 1: conteo exacto de patrones alcanzables, k = 0..16
# representantes n = 2^k + r  (r = 0..2^k-1), todos positivos,
# cubren todas las clases mod 2^k
# ---------------------------------------------------------------
print()
print("  k   alcanzados   F(k+2)   sin'11'   veredicto")
for k in range(0, 17):
    vistos = set()
    base = 1 << k
    for r in range(base):
        vistos.add(patron(base + r, k))
    esperado = fib(k + 2)
    dp = cuenta_sin_11(k)
    ok = (len(vistos) == esperado == dp)
    if not ok:
        fallos += 1
    # ademas: ningun patron alcanzado contiene "11"
    con11 = 0
    for p in vistos:
        for i in range(k - 1):
            if p[i] == 1 and p[i + 1] == 1:
                con11 += 1
                break
    if con11:
        fallos += 1
    print("%3d   %10d   %6d   %7d   %s%s" % (
        k, len(vistos), esperado, dp,
        "OK" if ok else "FALLO",
        "  (patrones con 11: %d)" % con11 if con11 else ""))

# ---------------------------------------------------------------
# COMPROBACION 2: igualdad de CONJUNTOS, no solo de cardinales:
# alcanzados == {cadenas sin "11"}, para k = 0..14
# ---------------------------------------------------------------
from itertools import product
for k in range(0, 15):
    vistos = set()
    base = 1 << k
    for r in range(base):
        vistos.add(patron(base + r, k))
    sin11 = set()
    for cad in product((0, 1), repeat=k):
        if not any(cad[i] == 1 and cad[i + 1] == 1 for i in range(k - 1)):
            sin11.add(cad)
    if vistos != sin11:
        print("FALLO conjuntos k=%d: solo_alcanzados=%d solo_sin11=%d"
              % (k, len(vistos - sin11), len(sin11 - vistos)))
        fallos += 1
print()
print("[2] igualdad de conjuntos alcanzados == sin'11': k=0..14, fallos =", fallos)

# ---------------------------------------------------------------
# COMPROBACION 3: barrido directo sobre n = 1..300000 (sin residuos)
# para k = 1..10 (el ambito declarado): debe dar lo mismo
# ---------------------------------------------------------------
LIM = 300000
for k in range(1, 11):
    vistos = set()
    for n in range(1, LIM + 1):
        vistos.add(patron(n, k))
    esperado = fib(k + 2)
    if len(vistos) != esperado:
        print("FALLO barrido directo k=%d: %d contra %d" % (k, len(vistos), esperado))
        fallos += 1
print("[3] barrido directo n=1..%d, k=1..10: fallos = %d" % (LIM, fallos))

# ---------------------------------------------------------------
# BORDES: k=0 (patron vacio), n=1, n=2, el ciclo 1-4-2
# ---------------------------------------------------------------
assert patron(1, 3) == (1, 0, 0)     # 1 impar -> 4 par -> 2 par
assert patron(2, 2) == (0, 1)        # 2 par -> 1 impar
assert fib(2) == 1 and fib(3) == 2 and fib(6) == 8 and fib(8) == 21
assert fib(10) == 55 and fib(12) == 144
print("[4] bordes: k=0 da 1 patron (el vacio) = F(2); n=1 y n=2 cuadran; anclas de la base (8,21,55,144) cuadran")

if fallos:
    raise SystemExit("TOTAL FALLOS: %d" % fallos)
print()
print("VEREDICTO DEL SCRIPT: 0 fallos. Alcanzables en k pasos (mapa clasico) = F(k+2), k = 0..16;")
print("igualdad de conjuntos (no solo cardinales) hasta k = 14; barrido directo hasta n = 300000 para k = 1..10.")
