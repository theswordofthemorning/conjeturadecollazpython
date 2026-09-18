"""
REVISION 12 -- ADVERSARIO 1, TANDA 1 (Suricatas / invariantes).
Reproduccion INDEPENDIENTE escrita solo desde las definiciones de
depuracion/frente20260910/LEEME.md (secciones 2-4), sin leer
invariantes.py ni contraccion.py.

Definicion usada (LEEME 2): tau_k(x) = 3x + (1-3^k)/2  mod 2^m,
es decir tau_k(x) = 3x - (3^k-1)/2.
"""
from fractions import Fraction
import numpy as np

def tau(k, x, mod):
    return (3 * x - (3**k - 1) // 2) % mod

def perm(k, m):
    mod = 1 << m
    return [tau(k, x, mod) for x in range(mod)]

def componentes(ks, m):
    """Componentes conexas del grafo generado por los tau_k, k in ks."""
    mod = 1 << m
    padre = list(range(mod))
    def raiz(a):
        while padre[a] != a:
            padre[a] = padre[padre[a]]
            a = padre[a]
        return a
    def une(a, b):
        ra, rb = raiz(a), raiz(b)
        if ra != rb:
            padre[ra] = rb
    for k in ks:
        for x in range(mod):
            une(x, tau(k, x, mod))
    return len({raiz(x) for x in range(mod)})

print("A. COMPONENTES COMUNES (reproduccion independiente)")
print("   m : comp(3,5) comp(2,3)   [LEEME afirma 2 y 1]")
ok_comp = True
for m in range(2, 13):
    c35 = componentes([3, 5], m)
    c23 = componentes([2, 3], m)
    marca = "ok" if (c35 == 2 and c23 == 1) else "DISCREPA"
    if marca != "ok":
        ok_comp = False
    print(f"   m={m:2d}:    {c35}         {c23}       {marca}")

print()
print("B. IDENTIDAD DE TRASLACION  tau_2(tau_3^{-1}(x)) == x+9 (mod 2^m)")
total = 0
fallos = 0
for m in range(2, 13):
    mod = 1 << m
    inv3 = pow(3, -1, mod)
    for x in range(mod):
        y = (inv3 * (x + 13)) % mod      # tau_3^{-1}(x)
        if tau(2, y, mod) != (x + 9) % mod:
            fallos += 1
        total += 1
print(f"   identidades comprobadas = {total}   fallos = {fallos}"
      f"   [LEEME afirma 8188]")

print()
print("C. chi = (1,-1,-1,1) mod 4 : invariancias (exacto, enteros)")
for m in range(2, 13):
    mod = 1 << m
    chi = [1 if (x % 4 in (0, 3)) else -1 for x in range(mod)]
    i3 = all(chi[tau(3, x, mod)] == chi[x] for x in range(mod))
    i5 = all(chi[tau(5, x, mod)] == chi[x] for x in range(mod))
    i2 = all(chi[tau(2, x, mod)] == chi[x] for x in range(mod))
    media = sum(chi)
    if m == 2 or m == 12:
        print(f"   m={m:2d}: inv_tau3={i3}  inv_tau5={i5}  inv_tau2={i2}"
              f"  suma={media}")
    else:
        assert i3 and i5 and not i2 and media == 0

print()
print("D. ENERGIA  ||M2 chi||^2 / ||chi||^2   con M_k=(I+P_k)/2  (Fraction)")
for m in range(2, 9):
    mod = 1 << m
    chi = [Fraction(1) if (x % 4 in (0, 3)) else Fraction(-1)
           for x in range(mod)]
    # convencion pullback: (P_k v)(x) = v(tau_k(x))
    p2chi = [chi[tau(2, x, mod)] for x in range(mod)]
    m2chi = [(chi[x] + p2chi[x]) / 2 for x in range(mod)]
    num = sum(z * z for z in m2chi)
    den = sum(z * z for z in chi)
    print(f"   m={m:2d}: {num}/{den} = {num/den}   [LEEME afirma 1/2]")

print()
print("E. NORMA ESPECTRAL DE M2 M3 EN MEDIA CERO (medicion flotante)")
print("   LEEME: 0.707107 0.707107 0.809017 0.859923 0.893467 "
      "0.912601 0.931140 para m=2..8")
for m in range(2, 9):
    mod = 1 << m
    I = np.eye(mod)
    def Pmat(k):
        P = np.zeros((mod, mod))
        for x in range(mod):
            P[x, tau(k, x, mod)] = 1.0     # pullback (P v)(x)=v(tau x)
        return P
    M2 = (I + Pmat(2)) / 2
    M3 = (I + Pmat(3)) / 2
    # base ortonormal de media cero
    Q, _ = np.linalg.qr(np.eye(mod) - np.ones((mod, mod)) / mod)
    base = Q[:, :mod - 1]
    A = base.T @ (M2 @ M3) @ base
    B = base.T @ (M3 @ M2) @ base
    print(f"   m={m:2d}: ||M2M3||={np.linalg.svd(A, compute_uv=False)[0]:.12f}"
          f"   ||M3M2||={np.linalg.svd(B, compute_uv=False)[0]:.12f}")
