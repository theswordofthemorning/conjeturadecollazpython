# A22_comp.py - tercera implementacion del comparador (no lee ningun fichero de los agentes ni del repo)
# Mapa del ATAJO: T(n) = n/2 si par, (3n+1)/2 si impar.
from fractions import Fraction

def T(n):
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2

def S_y_Tk(n, k):
    s = 0
    for _ in range(k):
        if n % 2 == 1:
            s += 1
        n = T(n)
    return s, n

def a(k):
    # clase r buena si S_k(r)==S_k(r+1) y T^k(r)==T^k(r+1), iterando sobre los ENTEROS r y r+1
    cuenta = 0
    for r in range(2 ** k):
        s1, t1 = S_y_Tk(r, k)
        s2, t2 = S_y_Tk(r + 1, k)
        if s1 == s2 and t1 == t2:
            cuenta += 1
    return cuenta

publicada = [1, 3, 8, 18, 39, 82, 170, 351, 721, 1476, 3012, 6130, 12450, 25241]
mios = [a(k) for k in range(3, 17)]
print("a(k) k=3..16 propios :", mios)
print("publicada            :", publicada)
if mios != publicada:
    raise SystemExit("DISCREPANCIA en a(k)")
print("a(k) 14/14 identicos")

# aritmetica del porcentaje
v = Fraction(1871137623, 2 ** 32)
print("1871137623/2^32 =", float(v))
assert 435658 * 2 ** 32 <= 1871137623 * 10 ** 6 < 435659 * 2 ** 32
print("43,5658% correcto (truncado)")

# altura clasica por fuerza bruta (mapa clasico), para cruzar clase buena -> misma altura, m>=1
def altura_clasica(n):
    p = 0
    while n != 1:
        n = 3 * n + 1 if n % 2 else n // 2
        p += 1
    return p

k = 8
buenas = [r for r in range(2 ** k)
          if S_y_Tk(r, k) == S_y_Tk(r + 1, k)]
fallos = 0
casos = 0
for r in buenas:
    for m in (1, 2, 5, 37, 1000):
        n = 2 ** k * m + r
        casos += 1
        if altura_clasica(n) != altura_clasica(n + 1):
            fallos += 1
            print("FALLO", r, m)
print(f"fusion/altura m>=1: {casos} casos, {fallos} fallos (k=8, {len(buenas)} clases buenas)")

# contraejemplo m=0 que citan los dos agentes
print("altura(5) =", altura_clasica(5), " altura(6) =", altura_clasica(6))
print("altura(4) =", altura_clasica(4), " altura(5) =", altura_clasica(5))

# el borde r = 2^k - 1 nunca es bueno (S = k >= 1 vs S(2^k) = 0)
for kk in range(3, 12):
    s1, _ = S_y_Tk(2 ** kk - 1, kk)
    s2, _ = S_y_Tk(2 ** kk, kk)
    assert s1 == kk and s2 == 0
print("borde 2^k-1: nunca bueno, k=3..11")
