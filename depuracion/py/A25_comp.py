# A25 comparador: tercera implementacion, sin mirar la de los agentes al escribirla.
# Comprueba: (a) forma cerrada T^6(32m+5) = T^6(32m+6) = 18m+4 contra iteracion
# cruda con Fraction-free enteros, en m dispersos NO redondos; (b) que nadie toca
# el 1 antes del paso 6 con m >= 1; (c) el borde m = 0; (d) caso comun m = 3125.

def T(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1

def it(k, n):
    for _ in range(k):
        n = T(n)
    return n

# m elegidos a proposito NO redondos y NO de la lista de la base
muestras = [1, 3, 11, 17, 511, 512, 513, 2047, 2048, 3125, 65537, 10**7 + 7, 2**60 + 3]
for m in muestras:
    a, b = 32 * m + 5, 32 * m + 6
    va, vb = it(6, a), it(6, b)
    assert va == vb == 18 * m + 4, (m, va, vb)
    # nadie toca 1 antes del paso 6 (m >= 1)
    for j in range(6):
        assert it(j, a) != 1 and it(j, b) != 1, (m, j)
print("forma cerrada 18m+4 y no-1-antes: OK en", len(muestras), "m dispersos, incl. 2^60+3")

# desfase: el primer encuentro es exactamente en j = 6 (mismo indice)?
for m in [1, 3, 11, 3125]:
    a, b = 32 * m + 5, 32 * m + 6
    j = 0
    x, y = a, b
    while x != y:
        x, y = T(x), T(y)
        j += 1
    assert j == 6, (m, j)
print("primer encuentro con mismo indice = paso 6: OK")

# altura igual (consecuencia)
def altura(n):
    c = 0
    while n != 1:
        n = T(n)
        c += 1
    return c

for m in [1, 3, 11, 3125, 65537]:
    assert altura(32 * m + 5) == altura(32 * m + 6), m
print("alturas iguales en los m probados: OK")

# borde m = 0: fusion en paso 6 SI, altura NO
assert it(6, 5) == it(6, 6) == 4
assert altura(5) == 5 and altura(6) == 8
print("borde m=0: fusiona en paso 6 (ambos 4) pero alturas 5 y 8: OK")

# caso comun de los dos agentes: m = 3125 -> 56254
assert it(6, 100005) == it(6, 100006) == 56254 == 18 * 3125 + 4
print("caso comun m=3125: T^6(100005) = T^6(100006) = 56254: OK")
print("COMPARADOR: 0 fallos")
