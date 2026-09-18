"""
REVISION 12 -- ADVERSARIO 1, TANDA 5 (Gacelas).

Verificacion independiente desde la ley `paso`, sin leer
transferencia.py: el contraejemplo de (G1), la cota de supervivencia
(G2) con la identidad de balota, las probabilidades de Q, la identidad
afin de la seccion 3, y los certificados numericos de (G4)-(G5).
"""
from fractions import Fraction as F
from collections import defaultdict
from math import comb, isqrt

def paso(k, c, bit):
    if c % 2 == 0:
        return (k, (3 * c + 1 - 3**k) // 2 if bit else c // 2)
    if bit:
        return (k - 1, (c - 3**(k - 1)) // 2) if k > 2 else None
    return (k + 1, (3 * c + 1) // 2)

print("A. EL CONTRAEJEMPLO DE LA SECCION 1")
print("   [Gacelas: desde (2,0), S_4=12/16; de las 12 supervivientes,")
print("    ocho empiezan en bit 0 y cuatro en bit 1; P(bit0|tau>4)=2/3]")
vivas = []
def explora(est, palabra, prof):
    if prof == 0:
        vivas.append(palabra)
        return
    for b in (False, True):
        p = paso(est[0], est[1], b)
        if p is not None:
            explora(p, palabra + [b], prof - 1)
explora((2, 0), [], 4)
n0 = sum(1 for w in vivas if w[0] is False)
n1 = sum(1 for w in vivas if w[0] is True)
print("   palabras supervivientes de 4 bits: %d de 16  -> S_4 = %s"
      % (len(vivas), F(len(vivas), 16)))
print("   empiezan en bit 0: %d    en bit 1: %d" % (n0, n1))
print("   P(bit 0 | tau>4) = %s   [Q daria 1/2]"
      % F(n0, len(vivas)))
print("   coincide con la nota:",
      len(vivas) == 12 and n0 == 8 and n1 == 4
      and F(n0, len(vivas)) == F(2, 3))

print()
print("B. (G2): S_t >= q_t = 2^-t C(t, floor(t/2)) >= 1/sqrt(2t+3)")
print("   c0        t   S_t         q_t         1/sqrt(2t+3)   ok")
malB = 0
for c0 in (0, 1, -1, 27, 999983, -1398101):
    est = {(2, c0): 1}
    for t in range(1, 17):
        nue = defaultdict(int)
        for (k, c), n in est.items():
            for b in (False, True):
                p = paso(k, c, b)
                if p is not None:
                    nue[p] += n
        est = nue
        St = F(sum(est.values()), 1 << t)
        qt = F(comb(t, t // 2), 1 << t)
        ok = St >= qt
        # 1/sqrt(2t+3) sin flotantes: qt >= 1/sqrt(2t+3) <=> qt^2(2t+3)>=1
        ok2 = qt * qt * (2 * t + 3) >= 1
        if not (ok and ok2):
            malB += 1
        if t in (8, 16):
            print("   %-9d %2d  %.8f  %.8f  %.8f     %s"
                  % (c0, t, float(St), float(qt),
                     (2 * t + 3) ** -0.5, "ok" if ok and ok2 else "FALLA"))
print("   fallos en 6 semillas x t=1..16:", malB)

print()
print("C. LA IDENTIDAD DE BALOTA:  (2m+1)^2(4m+5) - (2m+2)^2(4m+1) = 1")
mal = sum(1 for m in range(0, 5000)
          if (2 * m + 1)**2 * (4 * m + 5) - (2 * m + 2)**2 * (4 * m + 1) != 1)
print("   m=0..4999: discrepancias =", mal)
a = F(1)
malA = 0
for m in range(0, 3000):
    if a * a * (4 * m + 1) < 1:
        malA += 1
    a = a * F(2 * m + 1, 2 * m + 2)
print("   a_m >= 1/sqrt(4m+1) para m=0..2999: fallos =", malA)
malq = 0
for m in range(0, 300):
    am = F(comb(2 * m, m), 4**m)
    am1 = F(comb(2 * m + 2, m + 1), 4**(m + 1))
    if F(comb(2 * m, m), 1 << (2 * m)) != am:
        malq += 1
    if F(comb(2 * m + 1, m), 1 << (2 * m + 1)) != am1:
        malq += 1
print("   q_2m = a_m  y  q_(2m+1) = a_(m+1), m=0..299: fallos =", malq)

print()
print("D. LAS PROBABILIDADES DE Q (h-transform con h=k-1)")
malQ = 0
for k in range(2, 40):
    arriba = F(k, 2 * (k - 1))
    abajo = F(k - 2, 2 * (k - 1))
    if arriba + abajo != 1 or arriba < 0 or abajo < 0:
        malQ += 1
print("   suma 1 y no negativas para k=2..39:", malQ == 0)
print("   desde k=2 la bajada tiene probabilidad", F(0, 2), "-> cero: True")

print()
print("E. LA IDENTIDAD AFIN  u' = A u + delta,  A=1/2 (bit0), 3/2 (bit1)")
malE = 0
casos = 0
for k in range(2, 10):
    for c in range(-500, 501):
        u = F(c, 3**k)
        for b in (False, True):
            p = paso(k, c, b)
            if p is None:
                continue
            kk, cc = p
            up = F(cc, 3**kk)
            A = F(3, 2) if b else F(1, 2)
            delta = up - A * u
            casos += 1
            # delta debe depender solo de (k, paridad de c, bit)
            if b is False and c % 2 == 0 and delta != 0:
                malE += 1
            if b is True and c % 2 == 0 and delta != F(3**(-0) , 1) * (F(1, 3**k) - 1) / 2:
                malE += 1
            if b is False and c % 2 == 1 and delta != F(1, 2 * 3**(k + 1)):
                malE += 1
            if b is True and c % 2 == 1 and delta != F(-1, 2):
                malE += 1
print("   %d transiciones: A siempre 1/2 o 3/2 y delta con la forma"
      " prevista; fallos = %d" % (casos, malE))

print()
print("F. LOS CERTIFICADOS DE (G4)-(G5), en enteros exactos")
# lambda^2 = (2+sqrt3)/4 < 15/16  <=>  4(2+sqrt3) < 15  <=>  4 sqrt3 < 7
print("   4*sqrt(3) < 7  <=>  48 < 49 :", 48 < 49)
print("   (15/16)/(31/32) = 30/31 :", F(15, 16) / F(31, 32) == F(30, 31))
print("   30/31 < (61/62)^2 :", F(30, 31) < F(61, 62)**2,
      "  (diferencia = %s)" % (F(61, 62)**2 - F(30, 31)))
# la propagacion: 61^2(2T+5) <= 62^2(2T+3) para T>=29
umbral = min(T for T in range(1, 200)
             if 61**2 * (2 * T + 5) <= 62**2 * (2 * T + 3))
print("   61^2(2T+5) <= 62^2(2T+3) desde T =", umbral, " [la nota dice 29]")
# f(1024) = 124 (61/62)^1024 sqrt(2051) <= 1  <=>  f^2 <= 1
f2 = 124**2 * F(61, 62)**2048 * 2051
print("   f(1024)^2 = 124^2 (61/62)^2048 * 2051 <= 1 :", f2 <= 1,
      "  (vale %.3e)" % float(f2))
print("   luego 62(61/62)^T <= (1/2)/sqrt(2T+3) para todo T>=1024.")
