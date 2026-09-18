"""
REVISION 12 -- ADVERSARIO 1, TANDA 3 (Erizas).

DP propio sobre palabras de bits justas, construido desde `paso` (que
ya verifique contra pares enteros reales en rep_cadena_real.py), con
conteos ENTEROS exactos. Comprueba, sin leer obstruccion.py:

  (E1) E X_t = 1,  E X_t^2 <= t+1,  E X_t^4 <= (t+1)(3t+1)
  (E2) S_t >= 1/(t+1)
  (E3) E U_t <= |c0|/9 + t/2
  (E5) 1 >= A_t >= 1/(4 D_t)  con la caja de la seccion 3
  y los dos decimales publicados: A_{t+1}/(2 A_t) en 19->20 y 27->28.
"""
import sys
from fractions import Fraction as F
from math import ceil

def paso(k, c, bit):
    if c % 2 == 0:
        return (k, (3 * c + 1 - 3**k) // 2 if bit else c // 2)
    if bit:
        return (k - 1, (c - 3**(k - 1)) // 2) if k > 2 else None
    return (k + 1, (3 * c + 1) // 2)

def raiz4_techo(n):
    """techo de n^(1/4) en enteros exactos, sin flotantes."""
    x = int(round(n ** 0.25))
    while x**4 < n:
        x += 1
    while x > 0 and (x - 1)**4 >= n:
        x -= 1
    return x

def corrida(c0, TMAX, verbose_hasta=20):
    est = {(2, c0): 1}          # (k,c) -> numero de palabras de bits
    A = {}
    print("c0 = %d" % c0)
    print(" t  estados   S_t>=1/(t+1)  EX=1  EX2<=t+1  EX4<=(t+1)(3t+1)"
          "  EU<=|c0|/9+t/2  A_t>=1/(4D_t)")
    for t in range(0, TMAX + 1):
        total = 1 << t
        vivos = sum(est.values())
        St = F(vivos, total)
        EX = F(sum(n * (k - 1) for (k, c), n in est.items()), total)
        EX2 = F(sum(n * (k - 1)**2 for (k, c), n in est.items()), total)
        EX4 = F(sum(n * (k - 1)**4 for (k, c), n in est.items()), total)
        EU = F(sum(n * F(abs(c), 3**k) for (k, c), n in est.items()), 1) / total
        # A_t
        porf = {}
        for (k, c), n in est.items():
            porf.setdefault(k, []).append(n)
        At = F(0)
        for k, lst in porf.items():
            nk = sum(lst)
            At += F(sum(n * n for n in lst), nk)
        At = At / vivos
        A[t] = At
        # la caja de la seccion 3
        ht = raiz4_techo(4 * (t + 1)**2 * (3 * t + 1))
        Jt = 4 * (t + 1) * (abs(c0) + t + 1)
        Lt = Jt * 3**(ht + 1)
        Dt = ht * (2 * Lt + 1)
        ok = (St >= F(1, t + 1), EX == 1, EX2 <= t + 1,
              EX4 <= (t + 1) * (3 * t + 1),
              EU <= F(abs(c0), 9) + F(t, 2),
              At >= F(1, 4 * Dt) and At <= 1)
        if t <= verbose_hasta or t == TMAX:
            print("%3d %8d      %s        %s     %s        %s"
                  "              %s              %s"
                  % (t, len(est), *["ok" if x else "FALLA" for x in ok]))
        if not all(ok):
            print("   *** FALLA EN t=%d ***" % t)
        if t == TMAX:
            break
        nue = {}
        for (k, c), n in est.items():
            for bit in (False, True):
                p = paso(k, c, bit)
                if p is not None:
                    nue[p] = nue.get(p, 0) + n
        est = nue
    return A

TMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 28
A = corrida(1, TMAX)

print()
print("EL COCIENTE EN ESCALA  A_{t+1}/(2 A_t)")
print("[Erizas: aprox 0,450422 en 19->20 y 0,469286 en 27->28]")
for t in sorted(A):
    if t + 1 in A and (t >= 17 or t % 5 == 0):
        r = A[t + 1] / (2 * A[t])
        marca = ""
        if t == 19:
            marca = "   <-- Erizas dice 0.450422"
        if t == 27:
            marca = "   <-- Erizas dice 0.469286"
        print("  %2d -> %2d : %.6f%s" % (t, t + 1, float(r), marca))
