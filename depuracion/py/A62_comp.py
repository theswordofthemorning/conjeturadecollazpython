# A62_comp.py - comparador (agente 3). Tercera derivacion, sin Stern-Brocot
# y sin las definiciones de los otros dos agentes.
#
# 1. Records por-encima parametrizados POR B (como el agente 1) hasta B=65.
# 2. Records por-encima parametrizados POR A (como el agente 2) hasta A=400.
# 3. Semiconvergentes de log2(3) via FRACCION CONTINUA calculada desde cero
#    con comparaciones enteras 2^p vs 3^q (tercer metodo, distinto de ambos).
# 4. Lados de 3/2, 19/12, 84/53, 1054/665 y de 2/1, 8/5, 65/41, 485/306.
# 5. Ciclos de 3n-1 y sus (A,B,C).
# 6. El matiz de las "10 mas cercanas" de rejilla.

from fractions import Fraction

fallos = []
def ck(nombre, cond):
    print(("OK   " if cond else "FALLO") + " " + nombre)
    if not cond:
        fallos.append(nombre)

# --- 1. records por B (independiente del agente 1, misma parametrizacion) ---
def bestA(b):
    a = 0
    while 3 ** (a + 1) < 2 ** b:
        a += 1
    return a if 3 ** a < 2 ** b else 0

recB = []
mejor = None  # razon 3^A/2^B mas cercana a 1 por debajo => maximizar Fraction
for b in range(1, 66):
    a = bestA(b)
    r = Fraction(3 ** a, 2 ** b)
    if mejor is None or r > mejor:
        mejor = r
        recB.append((a, b))
print("records por B (B<=65):", recB)
ck("records por B = Tabla C [(0,1),(1,2),(3,5),(5,8),(17,27),(29,46),(41,65)]",
   recB == [(0, 1), (1, 2), (3, 5), (5, 8), (17, 27), (29, 46), (41, 65)])

# --- 2. records por A (independiente del agente 2, misma parametrizacion) ---
recA = []
mejor = None
p3 = 1; p2 = 1; B = 0
for A in range(1, 401):
    p3 *= 3
    while p2 <= p3:
        p2 *= 2; B += 1
    r = Fraction(p2, p3)
    if mejor is None or r < mejor:
        mejor = r
        recA.append((A, B))
print("records por A (A<=400):", recA)
ck("records por A coinciden con los 11 del agente 2",
   recA == [(1,2),(3,5),(5,8),(17,27),(29,46),(41,65),(94,149),(147,233),(200,317),(253,401),(306,485)])

# --- 3. fraccion continua de log2(3) desde cero, con enteros ---
# log2(3) = [a0; a1, a2, ...]. x0 = log2(3). a_i = floor(x_i).
# Representamos x como (u,v) significando x = (u*L + ...)? Mas simple:
# calculamos convergentes h_i/k_i por el algoritmo de floor con comparaciones
# exactas: floor de log2(3) restringido... En vez de eso: obtenemos los
# terminos de la CF por busqueda: a_i maximo tal que el semiconvergente
# sigue del mismo lado. Metodo: partimos de p_-1/q_-1 = 1/0 (encima),
# p_0/q_0 = 1/1 (debajo). En cada etapa el siguiente convergente es
# p = a*p_i + p_{i-1} con a maximo tal que mediante sucesivo cruza el lado.
def lado(p, q):
    # +1 si p/q > log2 3, -1 si <; comparacion exacta 2^p vs 3^q
    d = 2 ** p - 3 ** q
    assert d != 0
    return 1 if d > 0 else -1

# algoritmo estandar de CF por mediantes: identico en espiritu a Stern-Brocot
# pero registrando los TERMINOS a_i, y de ellos los convergentes clasicos.
lo, hi = (1, 1), (2, 1)
semis = {(1, 1): -1, (2, 1): +1}
terms = []
cur_side = None
count = 0
p_prev, q_prev = None, None
while True:
    p, q = lo[0] + hi[0], lo[1] + hi[1]
    if q > 1000:
        break
    s = lado(p, q)
    semis[(p, q)] = s
    if s < 0:
        lo = (p, q)
    else:
        hi = (p, q)

arriba = set(k for k, v in semis.items() if v > 0)
abajo = set(k for k, v in semis.items() if v < 0)

for (p, q) in [(3, 2), (19, 12), (84, 53), (1054, 665)]:
    if q <= 1000:
        ck("%d/%d por debajo (2^%d < 3^%d)" % (p, q, p, q), lado(p, q) == -1 and (p, q) in abajo)
    else:
        ck("%d/%d por debajo (2^%d < 3^%d)" % (p, q, p, q), lado(p, q) == -1)
for (p, q) in [(2, 1), (8, 5), (65, 41), (485, 306)]:
    ck("%d/%d por encima (2^%d > 3^%d)" % (p, q, p, q), lado(p, q) == +1 and (p, q) in arriba)

# los records de 1 y 2 son semiconvergentes por encima
def mcd(a, b):
    while b: a, b = b, a % b
    return a
for (A, B) in recA:
    g = mcd(B, A)
    ck("record (A=%d,B=%d) reducido %d/%d es semiconvergente POR ENCIMA (q<=400)"
       % (A, B, B // g, A // g),
       g == 1 and ((B, A) in arriba))
# reciproco en rango
arr_rango = set((q, p) for (p, q) in arriba if q <= 400)
ck("reciproco: todo semiconvergente por encima q<=400 es record",
   arr_rango == set(recA))

# numeros concretos que cita el agente 1
ck("2^19 = 524288 < 531441 = 3^12", 2**19 == 524288 and 3**12 == 531441 and 2**19 < 3**12)
ck("2^1054 < 3^665", 2**1054 < 3**665)

# --- 5. ciclos de 3n-1, tercera implementacion ---
def paso_m(n):
    return n // 2 if n % 2 == 0 else 3 * n - 1

minimos = set()
info = {}
for n0 in range(1, 3001):
    n = n0
    vistos = {}
    i = 0
    while n not in vistos:
        vistos[n] = i
        n = paso_m(n)
        i += 1
    # n repite: extraer ciclo
    ciclo = []
    m0 = n
    ciclo.append(n)
    n = paso_m(n)
    while n != m0:
        ciclo.append(n)
        n = paso_m(n)
    mn = min(ciclo)
    minimos.add(mn)
    if mn not in info:
        A = sum(1 for x in ciclo if x % 2 == 1)
        B = sum(1 for x in ciclo if x % 2 == 0)
        info[mn] = (A, B, len(ciclo))
ck("3n-1: minimos de ciclo = {1,5,17}", minimos == {1, 5, 17})
print("info ciclos 3n-1:", info)
ck("ciclo min=1: (A,B)=(1,1), 2^1 < 3^1", info.get(1) == (1, 1, 2) and 2**1 < 3**1)
ck("ciclo min=5: (A,B)=(2,3), 2^3 < 3^2", info.get(5) == (2, 3, 5) and 2**3 < 3**2)
ck("ciclo min=17: (A,B)=(7,11), 2^11 < 3^7", info.get(17) == (7, 11, 18) and 2**11 < 3**7)
ck("11/7 es semiconvergente POR DEBAJO", (11, 7) in abajo)

# ciclo trivial 3n+1
n, a, b, c = 1, 0, 0, 0
for _ in range(3):
    if n % 2 == 0:
        n //= 2; b += 1
    else:
        c = 3 * c + 2 ** b; n = 3 * n + 1; a += 1
ck("ciclo trivial 3n+1: vuelve a 1 con (A,B,C)=(1,2,1) y 2^2=3+1",
   n == 1 and (a, b, c) == (1, 2, 1) and 2**2 == 3**1 + 1)

# --- 6. matiz de las 10 mas cercanas de una rejilla ---
def top10(a_max):
    filas = []
    p3 = 1; p2 = 1; B = 0
    for A in range(1, a_max + 1):
        p3 *= 3
        while p2 <= p3:
            p2 *= 2; B += 1
        filas.append((Fraction(p2, p3), A, B))
    filas.sort()
    return [(A, B) for (_, A, B) in filas[:10]]

for a_max in (20, 40, 306):
    t = top10(a_max)
    exc = []
    for (A, B) in t:
        g = mcd(B, A)
        if (B // g, A // g) not in arriba:
            exc.append((A, B))
    print("rejilla A<=%d: top10=%s  no-semiconvergentes=%s" % (a_max, t, exc))

print()
print("RESULTADO COMPARADOR: %d fallos" % len(fallos))
for f in fallos:
    print("  - " + f)
