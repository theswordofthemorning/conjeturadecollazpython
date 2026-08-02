# A15_comp - comprobaciones propias del comparador (tercera implementacion)
# No comparte codigo con A15.py ni con A15.lean: T se escribe como tabla de casos.

def T(m):
    return m // 2 if m % 2 == 0 else 3 * m + 1

# 1) caso comun de los dos agentes: k = 6, n = 40
lhs = T(2**6 - 40)
rhs = 2**5 - T(40)
print("caso comun k=6 n=40:", lhs, rhs, "OK" if lhs == rhs else "FALLO")

# 2) barrido propio independiente: k = 1..14, n par 0..2^k (Z, sin truncar)
fallos = 0
casos = 0
for k in range(1, 15):
    for n in range(0, 2**k + 1, 2):
        casos += 1
        if T(2**k - n) != 2**(k-1) - T(n):
            fallos += 1
print("barrido propio k=1..14 n par 0..2^k:", casos, "casos,", fallos, "fallos")

# 3) el borde que separa Nat de Z: n > 2^k sobre Z de verdad (espejo negativo)
#    agente 1 lo cerro por truncacion de Nat; agente 2 por Z. Compruebo Z:
def Tz(m):
    return m // 2 if m % 2 == 0 else 3 * m + 1  # // de Python es floor; sobre pares es exacto
f3 = 0
for k in range(1, 11):
    for n in range(2**k + 2, 2**k + 200, 2):
        if Tz(2**k - n) != 2**(k-1) - Tz(n):
            f3 += 1
print("n > 2^k sobre Z (espejo negativo par):", "0 fallos" if f3 == 0 else f"{f3} FALLOS")

# 4) n impar debe fallar SIEMPRE en clasico (ningun acierto casual)
aciertos = 0
tot = 0
for k in range(1, 13):
    for n in range(1, 2**k, 2):
        tot += 1
        if T(2**k - n) == 2**(k-1) - T(n):
            aciertos += 1
print("n impar clasico: aciertos casuales =", aciertos, "de", tot)

# 5) k = 0: sobre Z el termino 2^(-1) no es entero -> no definido; anotado.
print("k = 0: 2^(k-1) = 1/2, no entero; el enunciado exige k >= 1 implicitamente")
