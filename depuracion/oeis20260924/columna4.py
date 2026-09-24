# -*- coding: utf-8 -*-
"""La columna j = 4 se reduce a la columna j = 2 de dos niveles antes.

Observacion: en el par de j=4 del nivel n las posiciones de paridad
opuesta son exactamente 0, 1, 2 y n-1. Tras dos pasos el par vuelve a ser
consecutivo, (z, z+1), y z es congruente modulo 2^(n-2) con el
representante de j=2 del nivel n-2, que esta demostrado unico.

    python -B -X utf8 depuracion/oeis20260924/columna4.py
"""


def T(x):
    return (3 * x + 1) // 2 if x & 1 else x // 2


def r4(n):
    return (3 if n % 2 == 0 else 1) * 2 ** (n - 2) - 3


def r2(n):
    return (3 if n % 2 else 1) * 2 ** (n - 2) - 2


print(" n |  r4(n) | opuestas | z tras 2 pasos | r2(n-2) | z = r2(n-2) mod 2^(n-2)")
fallos = 0
for n in range(6, 40):
    r = r4(n)
    x, y, opuestas = r, r + 1, []
    for i in range(0, n):
        if (x & 1) != (y & 1):
            opuestas.append(i)
        if i == 2:
            z = x
            consecutivos = (y == x + 1)
        x, y = T(x), T(y)
        if x == y:
            break
    esperadas = [0, 1, 2, n - 1]
    base = r2(n - 2)
    congruente = (z % 2 ** (n - 2) == base % 2 ** (n - 2))
    ok = (opuestas == esperadas) and consecutivos and congruente
    fallos += (not ok)
    if n < 14 or not ok:
        print("%2d | %6d | %-8s | %14d | %7d | %s"
              % (n, r, opuestas if n < 12 else "0,1,2,n-1", z, base,
                 "si" if congruente else "NO"))
print("...")
print()
print("niveles contrastados: n = 6..39")
print("fallos (opuestas = {0,1,2,n-1}, par consecutivo en i=2, congruencia):",
      fallos)
print()
print("Consecuencia: si se prueba que toda solucion de j=4 tiene sus")
print("opuestas en 0,1,2,n-1, entonces e_4(n) = e_2(n-2) = 1 y la columna")
print("queda cerrada. Esa implicacion es lo que falta; la reduccion en si")
print("esta comprobada en todo el rango de arriba.")


print()
print("=" * 70)
print("Caracterizacion: la posicion i es opuesta  <=>  d_i = y_i - x_i es IMPAR")
print("(dos numeros difieren en paridad exactamente cuando su resta es impar)")
print()
print("De ahi, todo depende de r modulo 4. Con d_0 = 1:")
print("  r PAR       : d_1 = r+2, par   -> la posicion 1 NO es opuesta")
print("  r = 1 (mod 4): x_1=(3r+1)/2 par, y_1=(r+1)/2 impar, y entonces")
print("                x_2=(3r+1)/4, y_2=(3r+5)/4, luego d_2 = 1 EXACTO:")
print("                el par vuelve a ser consecutivo tras 2 pasos")
print("  r = 3 (mod 4): d_2 = -2r-1, impar -> la posicion 2 tambien es opuesta")
print()

fall = 0
for r in range(1, 200000):
    x, y = r, r + 1
    x1, y1 = T(x), T(y)
    d1 = y1 - x1
    if r % 2 == 0:
        if d1 % 2 != 0 or d1 != r + 2:
            fall += 1
    else:
        x2, y2 = T(x1), T(y1)
        d2 = y2 - x2
        if r % 4 == 1:
            if d2 != 1 or x1 != (3 * r + 1) // 2 or y1 != (r + 1) // 2:
                fall += 1
        else:
            if d2 != -2 * r - 1 or d2 % 2 == 0:
                fall += 1
print("r probados: 1..199999   discrepancias con el analisis mod 4:", fall)
print()
print("Consecuencia: un par con r = 1 (mod 4) gasta sus opuestas 0 y 1 y")
print("reaparece como par consecutivo (x_2, x_2+1) con n-2 pasos por delante.")
print("Si ademas j = 4, a ese par le quedan exactamente 2 opuestas en n-2")
print("pasos, es decir es el par de j=2 del nivel n-2: e_4(n) = e_2(n-2) = 1.")
print("Falta solo descartar que un par con j=4 tenga r par.")
r4s = [(3 if n % 2 == 0 else 1) * 2 ** (n - 2) - 3 for n in range(5, 40)]
print("los representantes de j=4 son todos = 1 (mod 4):",
      all(r % 4 == 1 for r in r4s))
