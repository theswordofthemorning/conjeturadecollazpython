# -*- coding: utf-8 -*-
"""Reduccion de la columna j = 2 a dos candidatos, y contraste.

Cadena del argumento:
  - las posiciones opuestas de un par con j=2 son exactamente i=0 e i=n-1;
  - luego d_i = y_i - x_i es PAR para i=1..n-2 e IMPAR en i=n-1;
  - cada paso intermedio multiplica d por 1/2 (ambos pares) o 3/2 (ambos
    impares), luego |d_1| = 2^(n-2) * q con q impar;
  - si r fuese impar, |d_1| = r seria impar, imposible para n >= 3:
    todo par con j=2 tiene r PAR, y entonces |d_1| = r+2;
  - r+2 = 2^(n-2) q  y  0 <= r < 2^n  fuerzan q < 4 + 2^(3-n), luego
    q en {1,3}: solo quedan r = 2^(n-2)-2 y r = 3*2^(n-2)-2.

    python -B -X utf8 depuracion/oeis20260924/unicidad.py
"""


def T(x):
    return (3 * x + 1) // 2 if x & 1 else x // 2


def perfil(r, n):
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


NMAX = 22
print("Barrido exhaustivo de 2^n residuos, n = 3..%d" % NMAX)
print()
print("  n | pares con j=2 | r par? | r+2 = 2^(n-2)*q, q impar | q  | formula")
fallos = 0
for n in range(3, NMAX + 1):
    dos = [r for r in range(2 ** n)
           if (p := perfil(r, n)) and p[0] == n and p[2] and p[1] == 2]
    assert len(dos) == 1, (n, dos)
    r = dos[0]
    par = (r % 2 == 0)
    v = r + 2
    e = 0
    while v % 2 == 0:
        v //= 2
        e += 1
    q_ok = (e == n - 2 and v % 2 == 1)
    esperada = "2^(n-2)-2" if v == 1 else ("3*2^(n-2)-2" if v == 3 else "OTRA")
    coincide = (r == v * 2 ** (n - 2) - 2) and v in (1, 3)
    if not (par and q_ok and coincide):
        fallos += 1
    print("%3d | %13d | %6s | %24s | %2d | %s %s"
          % (n, len(dos), "si" if par else "NO",
             "si (exponente %d)" % e if q_ok else "NO (exponente %d)" % e,
             v, esperada, "" if coincide else "<-- FALLO"))

print()
print("filas que violan la reduccion:", fallos)
print()
print("Comprobacion de la cota sobre q: r+2 = 2^(n-2) q con 0 <= r < 2^n")
print("da q < 4 + 2^(3-n), luego q <= 4; siendo impar, q en {1,3}.")
for n in range(3, 12):
    cota = 4 + 2 ** (3 - n) if n <= 3 else 4 + 1 / 2 ** (n - 3)
    qs = [q for q in range(1, 20, 2) if 0 <= q * 2 ** (n - 2) - 2 < 2 ** n]
    print("   n=%-3d q admisibles por el rango: %s" % (n, qs))

print()
print("Cual de los dos candidatos gana, segun la paridad de n:")
print("  n | q=1: r=2^(n-2)-2        | q=3: r=3*2^(n-2)-2")
for n in range(3, 15):
    a, b = 2 ** (n - 2) - 2, 3 * 2 ** (n - 2) - 2
    pa, pb = perfil(a, n), perfil(b, n)
    ga = pa and pa[0] == n and pa[2] and pa[1] == 2
    gb = pb and pb[0] == n and pb[2] and pb[1] == 2
    print("%3d | %8d  %-14s | %8d  %s"
          % (n, a, "SIRVE" if ga else "no", b, "SIRVE" if gb else "no"))
    assert ga != gb, n
print()
print("exactamente uno de los dos sirve en cada nivel: si")
print("q=1 cuando n es par, q=3 cuando n es impar (contrastado arriba)")
