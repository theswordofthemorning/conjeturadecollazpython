# -*- coding: utf-8 -*-
# COMPARADOR - Item A2. Tercera implementacion, corta, para arbitrar.
# No comparte codigo con A2.py (recursion con dict en vez de bucles while identicos).

import sys
sys.setrecursionlimit(100000)

def alt_para(n, seguir_desde_1=False):
    """altitud clasica; si seguir_desde_1, la trayectoria de 1 da el paso 1->4."""
    valores = [n]
    m = n
    if n == 1 and seguir_desde_1:
        valores += [4, 2, 1]
        return max(valores)
    while m != 1:
        m = m // 2 if m % 2 == 0 else 3 * m + 1
        valores.append(m)
    return max(valores)

def racha(n):
    r = 0
    while n % 2 == 1:
        n = (3 * n + 1) // 2
        r += 1
    return r

def entera(n, alt, r):
    return alt * 2 ** r >= 2 * n * 3 ** r

# ---- casos comunes que calcularon los dos agentes ----
print("== CASOS COMUNES ==")
casos = [7, 27, 3, 63]
for n in casos:
    a, r = alt_para(n), racha(n)
    print("n=%d racha=%d alt=%d  entera: %d*2^%d=%d >= 2*%d*3^%d=%d -> %s"
          % (n, r, a, a, r, a * 2 ** r, n, r, 2 * n * 3 ** r, entera(n, a, r)))
# esperado agente 1: caso_7 416>=378, caso_27 36928>=486, caso_3 64>=54, caso_63 racha 6

# ---- el borde n=1, los dos convenios ----
print()
print("== BORDE n=1 ==")
r1 = racha(1)
print("racha(1) =", r1)
print("convenio A (trayectoria de 1 = [1]):      alt=1 ->", entera(1, alt_para(1), r1))
print("convenio B (1 -> 4 -> 2 -> 1):            alt=4 ->", entera(1, alt_para(1, True), r1))

# ---- barrido propio, limite NO redondo, ambos sentidos ----
print()
print("== BARRIDO PROPIO impares 1..131071 (limite 2^17-1, otra clase que 10^k) ==")
fallos = []
for n in range(1, 131072, 2):
    if not entera(n, alt_para(n), racha(n)):
        fallos.append(n)
print("fallos:", fallos, " (esperado: [1] con el convenio A)")

# ---- pares: reconteo del 28.325 ----
print()
fp = sum(1 for n in range(2, 100001, 2) if not entera(n, alt_para(n), 0))
print("pares 2..100000 que fallan:", fp, "de 50000  (la base decia 28.325)")

# ---- el cociente minimo del agente 2 ----
from fractions import Fraction
n = 200001
a, r = alt_para(n), racha(n)
print()
print("n=200001: racha =", r, " alt =", a,
      " cociente =", Fraction(a * 2 ** r, 2 * n * 3 ** r),
      " (agente 2 decia 600004/600003)")

# ---- ataque: hay algun impar >=3 donde la desigualdad NO sea estricta? ----
igualdades = [n for n in range(3, 50001, 2)
              if alt_para(n) * 2 ** racha(n) == 2 * n * 3 ** racha(n)]
print()
print("impares 3..50000 con IGUALDAD exacta:", igualdades,
      " (si vacio, la >= es estricta en el rango, como dijo el agente 2)")
