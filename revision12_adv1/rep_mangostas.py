"""
REVISION 12 -- ADVERSARIO 1, TANDA 4 (Mangostas).

Enumeracion exacta de la racha compartida desde la ley `paso`, sin
leer rachas.py. Comprueba (M1), (M2), (M3), (M4), la identidad de A,
y la correccion del ejemplo de racha forzada.

Paso compartido (c par, k fijo):  c -> c/2   o   c -> (3c - D)/2,
con D = 3^k - 1.  La racha termina cuando c es impar.
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

def ley_L(k, c, nmax):
    """distribucion exacta de L por enumeracion de palabras de bits.
    devuelve dict L -> Fraction(prob), y la masa aun no terminada."""
    D = 3**k - 1
    est = {c: F(1)}
    ley = defaultdict(F)
    for n in range(nmax):
        nue = defaultdict(F)
        for cc, p in est.items():
            if cc % 2 == 1:
                ley[n] += p              # ya era impar: L = n
                continue
            for hijo in (cc // 2, (3 * cc - D) // 2):
                nue[hijo] += p / 2
        est = nue
    resto = sum(est.values())
    return ley, resto

print("A. (M1): r<A da L=r determinista; r=A da L=A+G con G~Geom(1/2)")
print("   k    c            A  r   ley empirica de L (exacta)   veredicto")
casos = [(2, 8), (2, 12), (2, 6), (2, 0), (3, 4), (3, 2), (3, 1),
         (4, 16), (4, 8), (4, 48), (5, 2), (6, 8), (6, 24),
         (2, -8), (2, -12), (4, -16), (7, 6), (8, 256)]
fallos = 0
for k, c in casos:
    A = A_de(k)
    r = min(v2(c), A) if c != 0 else A
    NM = A + 18
    ley, resto = ley_L(k, c, NM)
    if r < A:
        ok = (ley.get(r, F(0)) == 1)
        desc = "L=%d con prob %s" % (r, ley.get(r, F(0)))
    else:
        # esperado: P(L = A+s) = 2^{-s-1}
        ok = all(ley.get(A + s, F(0)) == F(1, 2**(s + 1))
                 for s in range(0, 12))
        desc = "P(L=A+s)=2^-(s+1) para s=0..11"
    if not ok:
        fallos += 1
    print("  %2d  %-12d %2d %2d   %-32s %s"
          % (k, c, A, r, desc, "ok" if ok else "FALLA"))
print("   fallos:", fallos)

print()
print("B. (M2): P(L >= A+s) <= 2^-s, con IGUALDAD si r=A")
mal = 0
for k, c in casos:
    A = A_de(k)
    r = min(v2(c), A) if c != 0 else A
    ley, _ = ley_L(k, c, A + 18)
    for s in range(0, 10):
        cola = sum(p for L, p in ley.items() if L >= A + s)
        if cola > F(1, 2**s):
            mal += 1
        if r == A and cola != F(1, 2**s):
            mal += 1
print("   violaciones de la cota / de la igualdad en r=A:", mal)

print()
print("C. (M3): V(A,r,n) = numero de palabras que siguen PAR tras n pasos")
mal3 = 0
for k, c in casos:
    A = A_de(k)
    r = min(v2(c), A) if c != 0 else A
    D = 3**k - 1
    est = {c: 1}
    for n in range(0, min(A + 8, 14)):
        V = sum(m for cc, m in est.items() if cc % 2 == 0)
        if r < A:
            esp = 2**n if n < r else 0
        else:
            esp = 2**n if n < A else 2**(A - 1)
        if V != esp:
            mal3 += 1
            print("   FALLA k=%d c=%d n=%d: V=%d esperado=%d"
                  % (k, c, n, V, esp))
        nue = defaultdict(int)
        for cc, m in est.items():
            if cc % 2 == 0:
                nue[cc // 2] += m
                nue[(3 * cc - D) // 2] += m
            else:
                nue[cc] += 2 * m      # ya impar: se queda, cuenta impar
        est = nue
print("   discrepancias:", mal3)

print()
print("D. LA IDENTIDAD  A=1 (k impar), A=2+v2(k) (k par), y 2^A <= 4k")
mal4 = 0
for k in range(1, 3000):
    A = A_de(k)
    esp = 1 if k % 2 else 2 + v2(k)
    if A != esp or 2**A > 4 * k:
        mal4 += 1
print("   k=1..2999: discrepancias =", mal4)

print()
print("E. LA CORRECCION DEL EJEMPLO DE RACHA FORZADA")
c0 = 1398101
hijo = (3 * c0 + 1) // 2
print("   (2,%d) --mixto bit 0--> (3,%d)   2^21=%d -> %s"
      % (c0, hijo, 2**21, hijo == 2**21))
k, c = 3, hijo
A = A_de(k)
print("   A = v2(3^3-1) = v2(26) =", A)
ley, _ = ley_L(k, c, 40)
cola21 = sum(p for L, p in ley.items() if L >= 21)
print("   P(L>=21) =", cola21, "= 2^-20 ->", cola21 == F(1, 2**20),
      "  [Mangostas dice 2^-20]")
c1 = (3 * c - (3**k - 1)) // 2
print("   bit compartido 1 inmediato: c =", c1, " impar:", c1 % 2 == 1)
cc, pasos = c, 0
while cc % 2 == 0:
    cc //= 2
    pasos += 1
print("   la palabra de ceros realiza", pasos, "pasos  [dice 21]")

print()
print("F. (M4): 2^j P(L>=j) = 2^j mu(A>=j, 2^j|c) + E[2^A 1_{A<j, 2^A|c}]")
import random
random.seed(7)
mezcla = [(random.choice([2, 3, 4, 5, 6, 7, 8]),
           random.choice([0, 1, -1, 2, 4, 6, 8, 12, 16, 24, 32, 48,
                          64, -8, -16, 96, 128, 7, 13, 255]))
          for _ in range(60)]
peso = F(1, len(mezcla))
mal6 = 0
Amax = max(A_de(k) for k, c in mezcla)
for j in range(1, 20):
    izq = F(0)
    for k, c in mezcla:
        ley, _ = ley_L(k, c, max(30, j + 2))
        izq += peso * sum(p for L, p in ley.items() if L >= j)
    izq *= 2**j
    t1 = 2**j * sum(peso for k, c in mezcla
                    if A_de(k) >= j and (c % 2**j == 0))
    t2 = sum(peso * 2**A_de(k) for k, c in mezcla
             if A_de(k) < j and c % 2**A_de(k) == 0)
    if izq != t1 + t2:
        mal6 += 1
        print("   FALLA j=%d: %s vs %s" % (j, izq, t1 + t2))
print("   Amax de la mezcla =", Amax, "  discrepancias en j=1..19:", mal6)
Ccola = sum(peso * 2**A_de(k) for k, c in mezcla
            if c % 2**A_de(k) == 0)
print("   (M5) C_cola =", Ccola, "= %.6f" % float(Ccola))
print("   constante para j>Amax:",
      all(2**j * sum(peso * sum(p for L, p in ley_L(k, c, j + 25).items()
                                if L >= j) for k, c in mezcla) == Ccola
          for j in range(Amax + 1, Amax + 5)))
