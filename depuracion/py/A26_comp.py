# Comprobacion propia del comparador para A26 (mapa CLASICO)
# No lee nada del repo ni de los ficheros de los agentes.

def paso(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1

def tramo(n, t):
    e = o = 0
    for _ in range(t):
        if n % 2 == 0:
            e += 1
            n //= 2
        else:
            o += 1
            n = 3 * n + 1
    return n, e, o

fallos = []

# 1. Caso comun (4,5): fusion en t=3, e=2, o=1 los dos
v4, e4, o4 = tramo(4, 3)
v5, e5, o5 = tramo(5, 3)
if not (v4 == v5 == 4 and e4 == e5 == 2 and o4 == o5 == 1):
    fallos.append(("base 4/5", v4, e4, o4, v5, e5, o5))

# 2. Teorema con r=3 (= e+1) para k = 0..200 y k grandes, y forma cerrada
for k in list(range(201)) + [10**6 + 7, 10**50 + 12345]:
    a, ea, oa = tramo(2**3 * k + 4, 3)
    b, eb, ob = tramo(2**3 * k + 5, 3)
    cerrada = 3**1 * 2**(3 - 2) * k + 4
    if not (a == b == cerrada and (ea, oa) == (2, 1) and (eb, ob) == (2, 1)):
        fallos.append(("k", k, a, b, cerrada))

# 3. Borde r = e = 2: debe fallar en algun k (los impares)
rotos = sum(1 for k in range(1, 21) if tramo(4 * k + 4, 3)[0] != tramo(4 * k + 5, 3)[0])
if rotos == 0:
    fallos.append(("r=e no fallo nunca",))

# 4. Borde (3,20): se cruzan en el 10 en t=1 pero con cuentas distintas
v3, e3, o3 = tramo(3, 1)
v20, e20, o20 = tramo(20, 1)
assert v3 == v20 == 10
prop = sum(1 for r in (8, 10, 12) for k in range(1, 41)
           if tramo(2**r * k + 3, 1)[0] == tramo(2**r * k + 20, 1)[0])
if (e3, o3) == (e20, o20):
    fallos.append(("(3,20) cuentas iguales?!",))

# 5. Barrido propio independiente: todos los pares n1<n2<=120 que se funden en
#    el mismo indice con las mismas cuentas; probar r=e+1, k=1..25
import itertools
probados = 0
for n1, n2 in itertools.combinations(range(1, 121), 2):
    a, b = n1, n2
    ea = oa = eb = ob = 0
    for t in range(1, 200):
        if a % 2 == 0: a //= 2; ea += 1
        else: a = 3 * a + 1; oa += 1
        if b % 2 == 0: b //= 2; eb += 1
        else: b = 3 * b + 1; ob += 1
        if a == b and (ea, oa) == (eb, ob):
            r = ea + 1
            for k in range(1, 26):
                x, _, _ = tramo(2**r * k + n1, t)
                y, _, _ = tramo(2**r * k + n2, t)
                if x != y:
                    fallos.append(("barrido", n1, n2, t, k))
            probados += 1
            break
        if a == b:
            break  # se cruzan con cuentas distintas: fuera de hipotesis

print("pares con hipotesis probados:", probados)
print("(3,20) propagaciones (deberia ser bajo/0):", prop, "de 120")
print("r=e rotos (deberia ser >0):", rotos, "de 20")
print("FALLOS:", fallos if fallos else "ninguno")
