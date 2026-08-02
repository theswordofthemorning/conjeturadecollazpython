# A11 - comparador: tercera implementacion minima, sin mirar las otras dos.
# Mapa clasico. Cuenta pasos iterando sin memoizar y sin listas.

def S(n):
    c = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        c += 1
    return c

def pos(n, k):
    for _ in range(k):
        n = n // 2 if n % 2 == 0 else 3 * n + 1
    return n

# caso comun de los dos agentes: el 221
s221 = S(221)
p57 = pos(221, 57)
print("221: S =", s221, "| seq[57] =", p57, "| S(seq[57]) =", S(p57))

# contraejemplo de paridad de los dos agentes: n = 5
print("5: S =", S(5), "| seq[2] =", pos(5, 2), "| S(seq[2]) =", S(pos(5, 2)))

# caso chico del agente 1: n = 6
print("6: S =", S(6), "| seq[4] =", pos(6, 4), "| S(seq[4]) =", S(pos(6, 4)))

# conteo del 10.011 de la base: n con S par en 2..20000
pares = sum(1 for n in range(2, 20001) if S(n) % 2 == 0)
print("n con S par en 2..20000:", pares)

# muestreo de la parte 1 fuera del rango de la base (limite NO redondo, n grande)
import random
random.seed(11)
fallos = 0
for _ in range(200):
    n = random.randrange(20011, 5_000_017)
    s = S(n)
    k = random.randrange(0, s + 1)
    if S(pos(n, k)) != s - k:
        fallos += 1
        print("FALLO", n, k)
print("muestreo fuera de rango (200 casos, n hasta 5e6): fallos =", fallos)
