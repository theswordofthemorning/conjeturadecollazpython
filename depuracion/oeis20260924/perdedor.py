# -*- coding: utf-8 -*-
"""Por que gana uno de los dos candidatos de la columna j = 2.

Los dos candidatos son r = 2^(n-2)-2 y r = 3*2^(n-2)-2. Ambos recorren
n-1 posiciones de igual paridad y llegan a la posicion n-1 con un par
que cumple  y = 3x+1.  Confluyen en el paso n si y solo si ademas x es
IMPAR: entonces T(x) = (3x+1)/2 = y/2 = T(y). Si x es par, T(x) = x/2
mientras T(y) = (3y+1)/2, y no funden.

    python -B -X utf8 depuracion/oeis20260924/perdedor.py
"""


def T(x):
    return (3 * x + 1) // 2 if x & 1 else x // 2


def en_posicion(r, i):
    x, y = r, r + 1
    for _ in range(i):
        x, y = T(x), T(y)
    return x, y


print("Posicion n-1 de los dos candidatos de cada nivel")
print()
print("  n |      candidato |    x_(n-1) |    y_(n-1) | y=3x+1 | x impar | funde")
malos = 0
for n in range(3, 26):
    for etiqueta, q in (("ganador ", 3 if n % 2 else 1),
                        ("perdedor", 1 if n % 2 else 3)):
        r = q * 2 ** (n - 2) - 2
        x, y = en_posicion(r, n - 1)
        rel = (y == 3 * x + 1)
        imp = bool(x & 1)
        fun = (T(x) == T(y))
        # la tesis: y=3x+1 siempre, y funde exactamente cuando x es impar
        if not (rel and (fun == imp)):
            malos += 1
        print("%3d | %s %6d | %10d | %10d | %6s | %7s | %5s"
              % (n, etiqueta, r, x, y, rel, imp, fun))
    print()

print("filas que violan la tesis (y=3x+1 siempre; funde <=> x impar):", malos)
print()
print("Comprobacion directa del criterio: si x es impar y y = 3x+1,")
print("entonces T(x) = (3x+1)/2 = y/2 = T(y), luego funden.")
print("Si x es par y y = 3x+1 (impar), T(x) = x/2 y T(y) = (3y+1)/2 = (9x+4)/2;")
print("son iguales solo si x/2 = (9x+4)/2, es decir x = -1/2: imposible.")
fallos = 0
for x in range(1, 100000):
    y = 3 * x + 1
    if (T(x) == T(y)) != bool(x & 1):
        fallos += 1
print("x probados con y = 3x+1, discrepancias con el criterio:", fallos)


print()
print("Identificacion de esos pares: x_k = (3^k-1)/2, y_k = 3x_k+1 = (3^(k+1)-1)/2")
print()
print("  k |        x_k | impar | T(x_k) si funde = (3^(k+1)-1)/4")
for k in range(0, 14):
    xk = (3 ** k - 1) // 2
    yk = 3 * xk + 1
    assert yk == (3 ** (k + 1) - 1) // 2
    imp = bool(xk & 1)
    m = (3 ** (k + 1) - 1) // 4 if imp else None
    assert (k % 2 == 1) == imp, k         # x_k impar <=> k impar
    if imp:
        assert T(xk) == T(yk) == m
    print("%3d | %10d | %5s | %s" % (k, xk, imp, m if imp else "-- (no funde)"))

print()
print("x_k impar <=> k impar: 3^k = 3 (mod 4) si k impar, luego (3^k-1)/2 es")
print("impar; y 3^k = 1 (mod 4) si k par, luego (3^k-1)/2 es par. Sin excepcion")
print("en los k probados.")
print()
print("Para k impar, k+1 es par y (3^(k+1)-1)/4 = (9^((k+1)/2)-1)/4: son")
print("exactamente los puntos de fusion 2, 20, 182, 1640, ... y de ahi la")
print("recurrencia m -> 9m+2, que ya no es una observacion sino la forma")
print("cerrada de esta familia.")
comprob = all((3 ** (k + 1) - 1) // 4 == (9 ** ((k + 1) // 2) - 1) // 4
              for k in range(1, 40, 2))
print("identidad (3^(k+1)-1)/4 = (9^((k+1)/2)-1)/4 para k impar:", comprob)
print("recurrencia m_(j+1) = 9 m_j + 2:",
      all((9 ** (j + 2) - 1) // 4 == 9 * ((9 ** (j + 1) - 1) // 4) + 2
          for j in range(40)))


print()
print("Ultimo eslabon: con que k llega cada candidato a la posicion n-1")
print()
print("  n | ganador | k | 2*floor((n-1)/2)-1 | perdedor | k' | k' par ?")
fallos_k = 0
for n in range(3, 24):
    def kde(r):
        x, _ = en_posicion(r, n - 1)
        k = 0
        while (3 ** k - 1) // 2 < x:
            k += 1
        return k if (3 ** k - 1) // 2 == x else None
    g = (3 if n % 2 else 1) * 2 ** (n - 2) - 2
    d = (1 if n % 2 else 3) * 2 ** (n - 2) - 2
    kg, kd = kde(g), kde(d)
    pred = 2 * ((n - 1) // 2) - 1
    # el ganador cae en el k impar predicho; el perdedor en un k vecino
    # (k+1 si n es par, k-1 si n es impar), y lo que importa es que sea PAR
    ok = (kg == pred) and (kg % 2 == 1) and (kd % 2 == 0) and abs(kd - kg) == 1
    fallos_k += (not ok)
    print("%3d | %7d | %d | %18d | %8d | %2d | %s"
          % (n, g, kg, pred, d, kd, "si" if ok else "NO"))
print()
print("fallos de: k = 2*floor((n-1)/2)-1 impar, k' vecino y par:", fallos_k)
print()
print("El ganador llega siempre con el k impar predicho; el perdedor con un")
print("k vecino, que por serlo es par, y por eso no funde. El vecino es k+1")
print("si n es par y k-1 si n es impar; para el criterio solo cuenta que sea")
print("par. Falta demostrar que la trayectoria de q*2^(n-2)-2 alcanza")
print("(3^k-1)/2 en el paso n-1.")
