"""Cotejo del teorema de Korec completo (CasaKorec.lean), sin Lean.

Uso, desde la raíz del repositorio:

    python -B -X utf8 depuracion/casa20261004/cotejo_korec.py

Comprueba con cuentas exactas lo que dice CasaKorec.lean y lo que cuenta el LEEME:

1. La entropía: (2c+1)^(2c) < 4^c * (c+1)^(c+1) * c^(c-1) para 1 <= c <= 300
   (margen_entropia), y la desigualdad en reales de entropia_real.
2. El bloque: para varios exponentes u/v con 3^v < 4^u, el menor c que cumple los dos
   márgenes de existe_bloque; c crece cuando u/v se acerca a log 3/log 4.
3. El descenso con parámetros (baja_param) en números de verdad: con u/v = 9/10 y su bloque,
   una muestra de números n entre 2^(2c) y 2^(2c+1) que suben menos de c+1 veces en 2c pasos.
4. Korec en números de verdad: qué fracción de cada tramo baja por debajo de n^theta en a lo
   sumo log2(n) pasos, para theta = 0,95, 0,9, 0,85 y 0,8.
5. La rareza al nivel de Lagarias (rareza_lagarias): 3^6309 < 2^10000, el margen de los pesos
   6309 y 3691, y la cuenta exacta de patrones de largo 10000 con al menos 6309 subidas.
"""

from fractions import Fraction
from math import comb, log, log2
import random

# Números que se pueden cambiar.
EXPONENTES = [(19, 20), (9, 10), (17, 20), (4, 5), (159, 200)]
MUESTRA = 3000                 # parte 3
TRAMOS = range(10, 17)         # parte 4
SEMILLA = 20261007


def siguiente(n):
    """El atajo: n/2 si n es par, (3n+1)/2 si es impar."""
    if n % 2 == 0:
        return n // 2
    return (3 * n + 1) // 2


# 1. La entropía
print("1. Entropía")
for c in range(1, 301):
    assert (2 * c + 1) ** (2 * c) < 4 ** c * (c + 1) ** (c + 1) * c ** (c - 1)
    y = Fraction(4 * c * (c + 1))
    assert (1 + 1 / y) ** c * c < c + 1
for c in (1, 10, 100, 300):
    margen = 2 * c + (c + 1) * log2(c + 1) + (c - 1) * log2(c) - 2 * c * log2(2 * c + 1)
    print(f"   c={c}: (2c+1)^(2c) < 4^c*(c+1)^(c+1)*c^(c-1), sobran 2^{margen:.4f}")
print("   se cumple para 1 <= c <= 300, y la de reales también")


# 2. El bloque
def margenes(u, v, c):
    k1 = 2 ** v * (3 ** ((c + 1) * v) * 2 ** ((2 * c + 1) * (v - u))) <= 2 ** (2 * c * v)
    k2 = 2 ** v * 3 ** (2 * c * v) < 2 ** (2 * c * (u + v))
    return k1, k2


def menor_bloque(u, v):
    c = 1
    while True:
        k1, k2 = margenes(u, v, c)
        if k1 and k2:
            return c
        c += 1


print("2. El menor bloque para cada exponente (log 3/log 4 = %.5f)" % (log(3) / log(4)))
bloques = {}
for u, v in EXPONENTES:
    assert 3 ** v < 4 ** u and u < v
    c = menor_bloque(u, v)
    bloques[(u, v)] = c
    # y desde ahí siguen valiendo (las razones son menores que 1)
    for d in range(c, c + 30):
        assert all(margenes(u, v, d))
    print(f"   u/v = {u}/{v} = {u / v:.4f}: c = {c}, bloques de {2 * c} pasos")
lista = [bloques[e] for e in EXPONENTES]
assert lista == sorted(lista)

# 3. El descenso con parámetros
print("3. baja_param con u/v = 9/10")
u, v = 9, 10
c = bloques[(u, v)]
azar = random.Random(SEMILLA)
probados = 0
while probados < MUESTRA:
    n = azar.randrange(2 ** (2 * c), 2 ** (2 * c + 1))
    x = n
    s = 0
    for _ in range(2 * c):
        s += x % 2
        x = siguiente(x)
    if s < c + 1:
        assert x ** v < n ** u
        probados += 1
print(f"   c = {c}: {probados} números entre 2^{2 * c} y 2^{2 * c + 1} con menos de {c + 1} subidas"
      f" en {2 * c} pasos terminan por debajo de n^0,9")


# 4. Korec en números de verdad
def baja(n, num, den):
    """¿Hay k <= log2(n) con T^k(n)^den < n^num?"""
    tope = n ** num
    x = n
    for k in range(n.bit_length()):
        if x ** den < tope:
            return True
        x = siguiente(x)
    return False


print("4. Fracción que baja por debajo de n^theta en a lo sumo log2(n) pasos")
print("   tramo   0,95     0,9      0,85     0,8")
for j in TRAMOS:
    total = 2 ** j
    filas = []
    for num, den in [(19, 20), (9, 10), (17, 20), (4, 5)]:
        cuenta = sum(1 for n in range(2 ** j, 2 ** (j + 1)) if baja(n, num, den))
        filas.append(cuenta / total)
    assert filas == sorted(filas, reverse=True)
    print(f"   2^{j:<2}    " + "   ".join(f"{f:.4f}" for f in filas))

# 5. La rareza al nivel de Lagarias
print("5. Rareza con el exponente de Lagarias")
assert 3 ** 6309 < 2 ** 10000
assert 10000 ** 10000 <= 2 ** 9500 * 6309 ** 6309 * 3691 ** 3691
sobra = 9500 + 6309 * log2(6309) + 3691 * log2(3691) - 10000 * log2(10000)
exacto = sum(comb(10000, j) for j in range(6309, 10001))
assert exacto <= 2 ** 9500
print(f"   3^6309 < 2^10000 (sobran 2^{10000 - 6309 * log2(3):.3f}); margen de los pesos 2^{sobra:.3f}")
print(f"   patrones de largo 10000 con al menos 6309 subidas: 2^{log2(exacto):.2f}, bajo el tope 2^9500")

print("OK: todo coincide.")
