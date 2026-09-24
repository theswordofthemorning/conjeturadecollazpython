# -*- coding: utf-8 -*-
"""Contraste con la literatura: Garner, Wu-Huang, Elia-Tucker.

  - Las dos columnas extremas resultan ser las familias clasicas:
    j = 2 da la familia de Garner (8k+4, 8k+5); j = 4 da las de
    Wu y Huang (32m+5, 32m+6), (64m+45, 64m+46), (128m+29, 128m+30).
  - El teorema 2.1 de Elia y Tucker (n = 4 mod 8, n > 4, funden en el
    tercer paso) se reproduce exactamente.
  - Su contraejemplo a la conjetura de Garner, la familia 2^19*m+3067,
    esta clasificado sin problema por el parametro j y cumple la
    libelula: la conjetura que falla es otra.

    python -B -X utf8 depuracion/oeis20260924/literatura.py
"""


def T(x):
    return (3 * x + 1) // 2 if x & 1 else x // 2


def perfil(r, tope=800):
    x, y, sx, sy, j = r, r + 1, 0, 0, 0
    for t in range(1, tope + 1):
        px, py = x & 1, y & 1
        sx += px
        sy += py
        if px != py:
            j += 1
        x, y = T(x), T(y)
        if x == y:
            return t, j, sx == sy, x
    return None


def r2(n):
    return (3 if n % 2 else 1) * 2 ** (n - 2) - 2


def r4(n):
    return (1 if n % 2 else 3) * 2 ** (n - 2) - 3


print("1. Las columnas extremas son las familias clasicas")
print("   Garner (8k+4): 2^3 = 8, representante 4 = r2(3):", r2(3) == 4)
print("   Wu-Huang, citadas en la bibliografia de Lagarias:")
for n, base in ((5, 5), (6, 45), (7, 29)):
    print("     (2^%d m + %2d, +1): r4(%d) = %2d  %s"
          % (n, base, n, r4(n), "coincide" if r4(n) == base else "NO"))

print()
print("2. Teorema 2.1 de Elia y Tucker: n = 4 (mod 8), n > 4, funde en 3")
mal = sum(1 for n in range(12, 200000, 8)
          if (p := perfil(n)) is None or p[0] != 3)
print("   casos probados: 24999   fallos:", mal)

print()
print("3. Su contraejemplo a la conjetura de Garner: la familia 2^19 m + 3067")
p = perfil(3067)
print("   (3067, 3068): paso %d, j = %d, balanceado %s, punto de fusion %d"
      % p)
print("   punto de fusion mod 3 =", p[3] % 3, "(lema de la garza: 2)")
print("   3067 mod 8 =", 3067 % 8)
todos = [perfil(2 ** 19 * m + 3067) for m in range(40)]
print("   los 40 primeros miembros: mismo paso y mismo j:",
      len({(q[0], q[1]) for q in todos}) == 1)
print("   j par en todos ellos:", all(q[1] % 2 == 0 for q in todos))
print()
print("   La conjetura de Garner que falla caracteriza pares de igual")
print("   altura por sus 'stems'. El parametro j es otra cosa y no se ve")
print("   afectado: clasifica el contraejemplo igual que a los demas.")
