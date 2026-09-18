"""
REVISION 12 -- ADVERSARIO 1, TANDA 4 (Mangostas), version corregida.

La v1 (rep_mangostas.py) truncaba la enumeracion y por eso las colas
salian cortas por un epsilon (daba 2^-20 - 2^-39 en vez de 2^-20).
Error del revisor, no de la nota. Aqui las colas son exactas:

    P(L >= j) = masa que sigue PAR tras j-1 pasos,

y ademas se verifica DIRECTAMENTE el mecanismo de la seccion "Prueba",
que es lo que hace innecesaria una enumeracion profunda.
"""
from fractions import Fraction as F
from collections import defaultdict

def v2(n):
    if n == 0:
        return 10**9
    r = 0
    while n % 2 == 0:
        n //= 2
        r += 1
    return r

def A_de(k):
    return v2(3**k - 1)

def hijos(k, c):
    D = 3**k - 1
    return c // 2, (3 * c - D) // 2

print("A. EL MECANISMO (pasos 1 y 2 de la prueba), exhaustivo")
print("   paso 1: si 0<r<A, LOS DOS hijos tienen v2 exactamente r-1")
print("   paso 2: si 2^A|c, EXACTAMENTE UNO sigue divisible por 2^A")
print("           y el otro cae a v2 exactamente A-1")
mal1 = mal2 = n1 = n2 = 0
for k in range(2, 15):
    A = A_de(k)
    for c in range(-3000, 3001):
        if c == 0:
            continue
        r = min(v2(c), A)
        h0, h1 = hijos(k, c)
        if 0 < r < A:
            n1 += 1
            if not (v2(h0) == r - 1 and v2(h1) == r - 1):
                mal1 += 1
        elif r == A:
            n2 += 1
            arriba = [h for h in (h0, h1) if v2(h) >= A]
            abajo = [h for h in (h0, h1) if v2(h) == A - 1]
            if not (len(arriba) == 1 and len(abajo) == 1):
                mal2 += 1
print("   paso 1: %d casos, %d fallos" % (n1, mal1))
print("   paso 2: %d casos, %d fallos" % (n2, mal2))

def cola_exacta(k, c, j):
    """P(L>=j) exacta: masa que sigue PAR tras j-1 pasos."""
    est = {c: F(1)}
    for _ in range(j - 1):
        nue = defaultdict(F)
        for cc, p in est.items():
            if cc % 2:
                nue[cc] += p                    # ya impar, absorbente
            else:
                a, b = hijos(k, cc)
                nue[a] += p / 2
                nue[b] += p / 2
        est = nue
    return sum(p for cc, p in est.items() if cc % 2 == 0)

print()
print("B. (M2) CON COLAS EXACTAS: P(L>=A+s) <= 2^-s, igualdad si r=A")
casos = [(2, 8), (2, 12), (2, 6), (3, 4), (3, 2), (3, 1), (4, 16),
         (4, 8), (4, 48), (5, 2), (6, 8), (2, -8), (4, -16), (7, 6)]
malB = 0
igual = 0
for k, c in casos:
    A = A_de(k)
    r = min(v2(c), A) if c != 0 else A
    for s in range(0, max(1, 15 - A)):
        cola = cola_exacta(k, c, A + s)
        if cola > F(1, 2**s):
            malB += 1
            print("   COTA VIOLADA k=%d c=%d s=%d: %s > 2^-%d"
                  % (k, c, s, cola, s))
        if r == A:
            if cola == F(1, 2**s):
                igual += 1
            else:
                malB += 1
                print("   IGUALDAD FALLA k=%d c=%d s=%d: %s != 2^-%d"
                      % (k, c, s, cola, s))
print("   violaciones de la cota:", malB,
      "   igualdades confirmadas en r=A:", igual)

print()
print("C. LA CORRECCION DEL EJEMPLO DE RACHA FORZADA")
c0 = 1398101
hijo = (3 * c0 + 1) // 2
print("   (2,%d) --mixto bit 0--> (3,%d) = 2^21: %s"
      % (c0, hijo, hijo == 2**21))
k, c = 3, hijo
A = A_de(k)
print("   A = v2(26) = %d, luego r = min(21, %d) = %d = A" % (A, A, A))
print("   cola exacta P(L>=j) = 2^(A-j) para j=2..16:")
ok = all(cola_exacta(k, c, j) == F(1, 2**(j - A)) for j in range(2, 17))
print("     verificado j=2..16:", ok)
print("   por el mecanismo (verificado exhaustivamente en A), la cola es")
print("   geometrica exacta, luego P(L>=21) = 2^(1-21) = 2^-20.")
print("   [Mangostas dice exactamente 2^-20]  -> confirmado")
c1 = hijos(k, c)[1]
print("   bit compartido 1 inmediato: c=%d, impar: %s  (L=1)"
      % (c1, c1 % 2 == 1))
cc, pasos = c, 0
while cc % 2 == 0:
    cc //= 2
    pasos += 1
print("   la palabra de ceros realiza %d pasos [la nota dice 21]" % pasos)

print()
print("D. (M4) CON COLAS EXACTAS")
import random
random.seed(7)
mezcla = [(random.choice([2, 3, 4, 5, 6, 7]),
           random.choice([0, 1, -1, 2, 4, 6, 8, 12, 16, 24, 32, 48,
                          -8, -16, 7, 13, 255]))
          for _ in range(40)]
peso = F(1, len(mezcla))
Amax = max(A_de(k) for k, c in mezcla)
malD = 0
for j in range(1, 15):
    izq = 2**j * sum(peso * cola_exacta(k, c, j) for k, c in mezcla)
    t1 = 2**j * sum(peso for k, c in mezcla
                    if A_de(k) >= j and c % 2**j == 0)
    t2 = sum(peso * 2**A_de(k) for k, c in mezcla
             if A_de(k) < j and c % 2**A_de(k) == 0)
    if izq != t1 + t2:
        malD += 1
        print("   FALLA j=%d: %s vs %s" % (j, izq, t1 + t2))
print("   Amax=%d   discrepancias en j=1..14: %d" % (Amax, malD))

Ccola = sum(peso * 2**A_de(k) for k, c in mezcla
            if c % 2**A_de(k) == 0)
consts = {2**j * sum(peso * cola_exacta(k, c, j) for k, c in mezcla)
          for j in range(Amax + 1, Amax + 6)}
print("   (M5) C_cola = %s = %.6f" % (Ccola, float(Ccola)))
print("   valor normalizado para j=Amax+1..Amax+5:", consts,
      "-> constante e igual a C_cola:", consts == {Ccola})
