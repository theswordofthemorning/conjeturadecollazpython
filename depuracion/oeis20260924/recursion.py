# -*- coding: utf-8 -*-
"""Recursion de los estratos en la clase r = 1 (mod 4).

Para r = 4k+1 el calculo es directo:

    x_0 = 4k+1 (impar)   y_0 = 4k+2 (par)     -> posicion 0 opuesta, signo +
    x_1 = 6k+2 (par)     y_1 = 2k+1 (impar)   -> posicion 1 opuesta, signo -
    x_2 = 3k+1           y_2 = 3k+2           -> d_2 = 1: par consecutivo

de modo que el par reaparece como (r', r'+1) con r' = 3k+1 = (3r+1)/4,
habiendo gastado exactamente dos posiciones opuestas de signos contrarios.
Por tanto, para todo r = 1 (mod 4):

    n(r) = 2 + n(r'),   j(r) = 2 + j(r'),   y r es balanceado <=> r' lo es.

Consecuencia: j(r) = 4 exige j(r') = 2, que exige r' par, y
r' = 3k+1 es par si y solo si k es impar, es decir r = 5 (mod 8).

    python -B -X utf8 depuracion/oeis20260924/recursion.py
"""


def T(x):
    return (3 * x + 1) // 2 if x & 1 else x // 2


def perfil(r, tope=600):
    x, y, sx, sy, j = r, r + 1, 0, 0, 0
    for t in range(1, tope + 1):
        px, py = x & 1, y & 1
        sx += px
        sy += py
        if px != py:
            j += 1
        x, y = T(x), T(y)
        if x == y:
            return t, j, sx == sy
    return None


print("1. Las dos primeras posiciones, calculadas a mano")
malos = 0
for k in range(0, 100000):
    r = 4 * k + 1
    if (T(r), T(r + 1)) != (6 * k + 2, 2 * k + 1):
        malos += 1
    if (T(6 * k + 2), T(2 * k + 1)) != (3 * k + 1, 3 * k + 2):
        malos += 1
print("   k probados: 100000   discrepancias:", malos)

print()
print("2. Recursion n(r) = 2 + n(r'), j(r) = 2 + j(r'), r' = (3r+1)/4")
fallos = casos = 0
for r in range(1, 300000, 4):
    p, q = perfil(r), perfil((3 * r + 1) // 4)
    if p is None or q is None:
        continue
    casos += 1
    if not (p[0] == 2 + q[0] and p[1] == 2 + q[1] and p[2] == q[2]):
        fallos += 1
print("   pares r = 1 (mod 4) contrastados:", casos)
print("   fallos (incluida la equivalencia de balance):", fallos)

print()
print("3. Consecuencia: j = 4 solo puede darse con r = 5 (mod 8)")
clases = sorted({r % 8 for r in range(400000)
                 if (p := perfil(r)) and p[2] and p[1] == 4})
print("   clases modulo 8 observadas con j = 4:", clases)
print("   r' = 3k+1 par <=> k impar <=> r = 5 (mod 8):",
      all((((3 * r + 1) // 4) % 2 == 0) == (r % 8 == 5)
          for r in range(1, 200000, 4)))

print()
print("4. Lo que queda fuera de la recursion")
vistos = {}
for r in range(0, 400000):
    p = perfil(r)
    if p and p[2]:
        c = r % 4
        vistos.setdefault(c, set()).add(p[1])
for c in sorted(vistos):
    print("   r = %d (mod 4): j observados = %s"
          % (c, sorted(vistos[c])[:6]))
print()
print("   La recursion cubre r = 1 (mod 4). Para cerrar e_4(n) = 1 falta")
print("   demostrar que r par y r = 3 (mod 4) no pueden dar j = 4; ambos")
print("   casos estan comprobados en todo el rango de arriba, pero no")
print("   demostrados. Un barrido finito no es una prueba universal.")


print()
print("5. Las clases pares, calculadas igual")
print("   r = 4l+2 : x_1 = 2l+1, y_1 = 6l+5, ambos IMPARES -> no opuesta;")
print("             x_2 = 3l+2, y_2 = 9l+8, d_2 = 6l+6 par -> tampoco.")
print("   r = 4l   : x_1 = 2l,   y_1 = 6l+2, ambos PARES  -> no opuesta;")
print("             x_2 = l,    y_2 = 3l+1, d_2 = 2l+1 IMPAR -> opuesta.")
print("             y si ademas l es impar, x_3 = y_3 = (3l+1)/2: FUNDE en 3.")
m = 0
for l in range(0, 100000):
    r = 4 * l + 2
    if (T(r), T(r + 1)) != (2 * l + 1, 6 * l + 5):
        m += 1
    if (T(2 * l + 1), T(6 * l + 5)) != (3 * l + 2, 9 * l + 8):
        m += 1
    r = 4 * l
    if (T(r), T(r + 1)) != (2 * l, 6 * l + 2):
        m += 1
    if (T(2 * l), T(6 * l + 2)) != (l, 3 * l + 1):
        m += 1
    if l % 2 == 1 and T(l) != T(3 * l + 1):
        m += 1
print("   l probados: 100000   discrepancias:", m)
print()
print("   Asi el analisis se ramifica por clases modulo 2^s. El j minimo")
print("   por clase modulo 8 resulta ser:")
minimo = {}
for r in range(0, 200000):
    p = perfil(r)
    if p is None or not p[2]:
        continue
    c = r % 8
    if c not in minimo or p[1] < minimo[c]:
        minimo[c] = p[1]
print("     " + "  ".join("%d->%d" % (c, minimo[c]) for c in sorted(minimo)))
print("   es decir j=2 solo en las clases 2,4,6 y j=4 solo en la clase 5.")


print()
print("6. Identidad de conteo que se deriva de la recursion")
print("   La biyeccion r -> (3r+1)/4 lleva {r = 1 mod 4} sobre {r' = 1 mod 3}")
print("   y baja dos niveles y dos estratos. Con el rango correcto")
print("   (r < 2^n da r' < 3*2^(n-2)) el conteo cuadra exactamente:")
print()


def perfil_n(r, n):
    x, y, sx, sy, j = r, r + 1, 0, 0, 0
    for t in range(1, n + 1):
        px, py = x & 1, y & 1
        sx += px
        sy += py
        if px != py:
            j += 1
        x, y = T(x), T(y)
        if x == y:
            return t, j, sx == sy
    return None


dif = 0
for n in range(7, 19):
    izq, der = {}, {}
    for r in range(1, 2 ** n, 4):
        p = perfil_n(r, n)
        if p and p[0] == n and p[2]:
            izq[p[1]] = izq.get(p[1], 0) + 1
    for r2 in range(1, 3 * 2 ** (n - 2), 3):
        p = perfil_n(r2, n - 2)
        if p and p[0] == n - 2 and p[2]:
            der[p[1]] = der.get(p[1], 0) + 1
    for j in sorted(set(izq) | {k + 2 for k in der}):
        if izq.get(j, 0) != der.get(j - 2, 0):
            dif += 1
print("   #{r = 1 mod 4, nivel n, estrato j}")
print("     = #{r' = 1 mod 3 en [0, 3*2^(n-2)), nivel n-2, estrato j-2}")
print("   niveles n = 7..18, todos los estratos; filas que difieren:", dif)


print()
print("7. La clase r = 3 (mod 4), calculada igual")
print("   r = 4k+3: x_1 = 6k+5 (impar), y_1 = 2k+2 (par)  -> opuesta en 1")
print("             x_2 = 9k+8,  y_2 = k+1,  d_2 = -2r-1 impar -> opuesta en 2")
print("     k impar (r = 7 mod 8): d_3 = -13k-12, IMPAR -> opuesta en 3.")
print("       con la de n-1 son cinco posiciones; siendo j par, j >= 6,")
print("       luego esta clase NO puede dar j = 4. Descartada.")
print("     k par   (r = 3 mod 8): d_3 = -3k-2, par. Caso abierto.")
m = 0
for k in range(0, 100000):
    r = 4 * k + 3
    x1, y1 = T(r), T(r + 1)
    x2, y2 = T(x1), T(y1)
    if (x1, y1) != (6 * k + 5, 2 * k + 2) or (x2, y2) != (9 * k + 8, k + 1):
        m += 1
        continue
    d3 = T(y2) - T(x2)
    esperado = -13 * k - 12 if k % 2 else -3 * k - 2
    if d3 != esperado or (d3 % 2 != 0) != (k % 2 == 1):
        m += 1
print("   k probados: 100000   discrepancias:", m)
print()
print("   Estado de e_4(n) = 1 por clases modulo 8:")
print("     r = 5 (mod 8) : a lo sumo uno, por la recursion  [resuelto]")
print("     r = 1 (mod 8) : j >= 6 por la recursion          [resuelto]")
print("     r = 7 (mod 8) : j >= 6 por el calculo de arriba  [resuelto]")
print("     r = 3 (mod 8) : abierto")
print("     r par         : abierto")
