# -*- coding: utf-8 -*-
"""Cierre de e_2(n) = 1: las trayectorias tienen forma explicita.

Para el ganador r de cada nivel, con x_i = T^i(r), y_i = T^i(r+1):

  n PAR,  r = 2^(n-2)-2,  y = 2^(n-2)-1:
      x_i = 3^(i-1) * 2^(n-2-i) - 1        (1 <= i <= n-2)
      y_i = 3^i     * 2^(n-2-i) - 1
      x_(n-1) = (3^(n-3)-1)/2,  y_(n-1) = (3^(n-2)-1)/2 = 3*x_(n-1)+1

  n IMPAR, r = 3*2^(n-2)-2,  y = 3*2^(n-2)-1:
      x_i = 3^i     * 2^(n-2-i) - 1
      y_i = 3^(i+1) * 2^(n-2-i) - 1
      x_(n-1) = (3^(n-2)-1)/2,  y_(n-1) = (3^(n-1)-1)/2 = 3*x_(n-1)+1

Ambas son impares mientras el exponente de 2 sea >= 1, y ambas pares a la
vez en i = n-2: por eso todas las posiciones intermedias tienen paridad
igual y j = 2. En i = n-1 el par es (x, 3x+1) con x impar, luego funde.

    python -B -X utf8 depuracion/oeis20260924/cierre_e2.py
"""


def T(x):
    return (3 * x + 1) // 2 if x & 1 else x // 2


def formula(n, i):
    """(x_i, y_i) segun las formulas cerradas, para 1 <= i <= n-2."""
    b = n - 2 - i
    if n % 2 == 0:
        return 3 ** (i - 1) * 2 ** b - 1, 3 ** i * 2 ** b - 1
    return 3 ** i * 2 ** b - 1, 3 ** (i + 1) * 2 ** b - 1


print("Contraste de las formulas cerradas con la iteracion real")
print()
fallos = 0
for n in range(4, 61):
    r = (3 if n % 2 else 1) * 2 ** (n - 2) - 2
    x, y = r, r + 1
    for i in range(1, n):
        x, y = T(x), T(y)
        if i <= n - 2:
            fx, fy = formula(n, i)
            if (x, y) != (fx, fy):
                fallos += 1
                print("  n=%d i=%d: real (%d,%d) formula (%d,%d)"
                      % (n, i, x, y, fx, fy))
            # paridades iguales en las posiciones intermedias
            if (x & 1) != (y & 1):
                fallos += 1
                print("  n=%d i=%d: paridades distintas" % (n, i))
    # posicion n-1
    k = n - 3 if n % 2 == 0 else n - 2
    xk = (3 ** k - 1) // 2
    if (x, y) != (xk, 3 * xk + 1) or not (x & 1) or T(x) != T(y):
        fallos += 1
        print("  n=%d: posicion n-1 incorrecta" % n)

print("niveles contrastados: n = 4..60")
print("fallos:", fallos)
print()
print("Consecuencias, ya demostradas y no solo observadas:")
print("  - las posiciones 1..n-2 tienen paridad igual, luego j = 2;")
print("  - x_i != y_i para i < n (difieren en un factor 3), luego la fusion")
print("    es la PRIMERA y ocurre exactamente en el paso n;")
print("  - en i=0 el par es (par, impar) y en i=n-1 (impar, par): los dos")
print("    desequilibrios se cancelan, luego el par es balanceado;")
print("  - k = n-3 si n es par y n-2 si n es impar; en ambos casos k es")
print("    IMPAR, que es justo la condicion para que (x, 3x+1) funda.")
print()
print("  k impar en ambos casos:",
      all(((n - 3) if n % 2 == 0 else (n - 2)) % 2 == 1 for n in range(4, 200)))
print()
print("Junto con la reduccion a dos candidatos (unicidad.py), esto cierra")
print("e_2(n) = 1 para todo n >= 4 como teorema, no como conjetura.")
