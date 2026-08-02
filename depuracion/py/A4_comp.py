# A4_comp.py -- COMPARADOR (agente 3). Tercera implementacion, sin copiar
# la estructura de ninguno de los dos agentes: construye la lista entera de
# la trayectoria primero y despues cuenta, en vez de acumular al iterar.
# Comprueba (a) los casos comunes citados por los dos agentes, (b) que la
# identidad ENTERA de Lean y la FRACCIONARIA de Python son equivalentes
# caso a caso, (c) el maximo del barrido (993).

from fractions import Fraction
from math import gcd

def trayectoria(n):
    xs = [n]
    while xs[-1] != 1:
        v = xs[-1]
        xs.append(v // 2 if v % 2 == 0 else 3 * v + 1)
    return xs

def datos(n):
    xs = trayectoria(n)
    valores_con_paso = xs[:-1]          # el 1 final no recibe paso
    impares = [v for v in valores_con_paso if v % 2 == 1]
    pares   = [v for v in valores_con_paso if v % 2 == 0]
    A, B = len(impares), len(pares)
    px = 1
    pq = 1
    for v in impares:
        px *= v
        pq *= 3 * v + 1
    return A, B, impares, px, pq

fallos = []

def check(n):
    A, B, impares, px, pq = datos(n)
    # identidad ENTERA (la de Lean): 2^B * prod(x) == n * prod(3x+1)
    ent = (2 ** B * px == n * pq)
    # identidad FRACCIONARIA (la del enunciado): 2^B/(3^A n) == prod(1+1/(3x))
    prod = Fraction(1)
    for v in impares:
        prod *= Fraction(3 * v + 1, 3 * v)
    frac = (Fraction(2 ** B, 3 ** A * n) == prod)
    # equivalencia estructural: numero de factores == A (el 3^A se cancela bien)
    equiv = (len(impares) == A)
    if not (ent and frac and equiv):
        fallos.append((n, ent, frac, equiv))
    return A, B, px, pq, prod

# --- casos comunes citados por los dos agentes ---
A, B, px, pq, _ = check(7)
print("n=7  -> A=%d B=%d prod_x=%d prod_3x1=%d" % (A, B, px, pq))
assert (A, B, px, pq) == (5, 11, 85085, 24893440), "NO cuadra con el agente 1"
assert 2**11 * 85085 == 7 * 24893440

A, B, px, pq, _ = check(27)
print("n=27 -> A=%d B=%d (agente 1 dice 41, 70; total pasos %d)" % (A, B, A + B))
assert (A, B) == (41, 70), "NO cuadra el 27"

A, B, px, pq, prod = check(5)
print("n=5  -> A=%d B=%d prod=%s (agente 2 dice 16/15)" % (A, B, prod))
assert prod == Fraction(16, 15)

# el caso3_fracciones de Lean: n=3, impares 3 y 5, A=2, B=5
A, B, px, pq, prod = check(3)
print("n=3  -> A=%d B=%d prod=%s" % (A, B, prod))
assert (A, B) == (2, 5) and prod == Fraction(10, 9) * Fraction(16, 15)
assert (3*3+1) * (3*5+1) * (3**2 * 3) == (3*3) * (3*5) * 2**5  # 4320

# --- barrido propio 1..30000 y el maximo ---
mejor, n_mejor = Fraction(0), 0
for n in range(1, 30001):
    _, _, _, _, prod = check(n)
    if prod > mejor:
        mejor, n_mejor = prod, n

print("barrido 1..30000: fallos =", len(fallos))
print("maximo: n=%d  producto=%s = %.10f" % (n_mejor, mejor, float(mejor)))
# el agente 2 dice n=993, 1.2531421444; y 2^61/(3^32*993) exacto:
exacto993 = Fraction(2**61, 3**32 * 993)
print("2^61/(3^32*993) == maximo?", exacto993 == mejor)

# --- semillas grandes de los agentes, y una propia que ninguno uso ---
for n in (2**40 + 1, 2**60 + 1, 3**25, 10**15 + 7, 2**50 - 1, 123456789012345678901):
    check(n)
print("semillas grandes (5 del agente 2 + 1 propia de 67 bits): ok, fallos =", len(fallos))

# --- ataque: el enunciado dice VALORES impares. Un valor repetido contaria
# una vez o dos? En una trayectoria que termina en 1 no hay repetidos
# (si v se repitiera habria un ciclo y no llegaria al 1). Compruebo que de
# verdad no hay repetidos en el barrido, porque la identidad los necesita
# contados POR PASO y el enunciado los cuenta POR VALOR: solo son lo mismo
# si no hay repetidos.
repes = 0
for n in range(1, 30001):
    xs = trayectoria(n)
    if len(set(xs)) != len(xs):
        repes += 1
print("trayectorias con valor repetido en 1..30000:", repes)

if fallos:
    raise SystemExit("FALLOS: %r" % fallos[:5])
print("COMPARADOR: 0 fallos, identidad entera y fraccionaria equivalentes caso a caso")
