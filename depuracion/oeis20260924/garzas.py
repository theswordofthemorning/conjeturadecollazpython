# -*- coding: utf-8 -*-
"""Lema de la garza y teorema de la libelula.

Verificador autocontenido: no importa nada del laboratorio, para que sirva
de contraste independiente frente a estratoscadena.py. Reproduce ademas
A398792, A398793 y las series historicas e8, e10, e12.

    python -B -X utf8 depuracion/oeis20260924/garzas.py
"""


def T(x):
    """Aplicacion de Collatz acortada, A014682."""
    return (3 * x + 1) // 2 if x & 1 else x // 2


def preimagenes(m):
    """Preimagenes de m bajo T: 2m siempre; (2m-1)/3 si es entero impar."""
    pre = [2 * m]
    if (2 * m - 1) % 3 == 0 and ((2 * m - 1) // 3) & 1:
        pre.append((2 * m - 1) // 3)
    return pre


def perfil(r, tope):
    """Primera fusion de (r, r+1): (paso, j, balanceado, punto de fusion).

    j es el numero de posiciones de paridad opuesta entre las dos
    trayectorias; balanceado indica igual numero de entradas impares.
    """
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


def r_columna2(n):
    """Representante conjeturado de la columna j = 2 del nivel n."""
    return (3 if n % 2 else 1) * 2 ** (n - 2) - 2


def r_columna4(n):
    """Representante conjeturado de la columna j = 4 del nivel n."""
    return (1 if n % 2 else 3) * 2 ** (n - 2) - 3


def fusion_columna(k):
    """Punto de fusion de las columnas extremas: 2, 20, 182, 1640, ..."""
    return (9 ** (k + 1) - 1) // 4


def linea(titulo):
    print()
    print(titulo)
    print("-" * len(titulo))


# --- 1. Lema de la garza -----------------------------------------------------
linea("1. Lema de la garza: dos preimagenes  <=>  m = 2 (mod 3)")

TOPE_GARZA = 200000
fallos_pre = sum(1 for m in range(1, TOPE_GARZA)
                 for p in preimagenes(m) if T(p) != m)
discrepancias = sum(1 for m in range(1, TOPE_GARZA)
                    if (len(preimagenes(m)) == 2) != (m % 3 == 2))
print("m probados                                    :", TOPE_GARZA - 1)
print("preimagenes que no vuelven a m                :", fallos_pre)
print("discrepancias con 'dos preimagenes <=> 2 mod 3':", discrepancias)

# --- 2. Teorema de la libelula ----------------------------------------------
linea("2. Teorema de la libelula: j es par y j >= 2  (barrido exhaustivo)")

NMAX = 18
tabla = {}
for n in range(1, NMAX + 1):
    cuenta = {}
    for r in range(2 ** n):
        p = perfil(r, n)
        if p is not None and p[0] == n and p[2]:
            cuenta[p[1]] = cuenta.get(p[1], 0) + 1
    tabla[n] = cuenta

impares = sum(v for n in tabla for j, v in tabla[n].items() if j % 2)
menores = sum(v for n in tabla for j, v in tabla[n].items() if j < 2)
total = sum(v for n in tabla for v in tabla[n].values())
print("residuos barridos                : 2^1 .. 2^%d" % NMAX)
print("pares balanceados hallados       :", total)
print("de ellos con j IMPAR             :", impares)
print("de ellos con j < 2               :", menores)

# --- 3. Contraste con las series del laboratorio ----------------------------
linea("3. Contraste independiente con estratoscadena.py (desde N = 10)")

HIST = {
    8:  [3, 7, 15, 27, 45, 73, 111, 166, 237],
    10: [0, 1, 4, 12, 30, 65, 131, 247, 447],
    12: [0, 0, 0, 1, 5, 18, 52, 134, 315],
}
for j in sorted(HIST):
    mio = [tabla[n].get(j, 0) for n in range(10, 19)]
    print("e%-2d  laboratorio: %s" % (j, HIST[j]))
    print("     este fichero: %s   %s"
          % (mio, "coincide" if mio == HIST[j] else "DISCREPA"))
print("e8(9) precedente esperado 1, obtenido", tabla[9].get(8, 0))

# --- 4. Reproduccion de A398792 y A398793 -----------------------------------
linea("4. Reproduccion de las sucesiones aprobadas")

A398793 = [0, 1, 1, 2, 2, 3, 4, 6, 11, 19, 34, 60, 106, 190, 341, 623, 1148]
sumas = [sum(tabla[n].values()) for n in range(1, NMAX + 1)]
esperado = A398793[1:NMAX - 1]
obtenido = sumas[2:NMAX]
print("sum_j e_j(n) para n = 3..%d :" % NMAX)
print("   obtenido :", obtenido)
print("   A398793  :", esperado)
print("   identidad sum_j e_j(n) = A398793(n-1):",
      "coincide" if obtenido == esperado else "DISCREPA")

# --- 5. Columnas j = 2 y j = 4 ----------------------------------------------
linea("5. Columnas extremas: formulas cerradas hasta n = 120")

fallos_col = []
for n in range(3, 121):
    for nombre, r, j_esp, k in (("j=2", r_columna2(n), 2, (n - 3) // 2),
                                ("j=4", r_columna4(n), 4, (n - 4) // 2)):
        if nombre == "j=4" and n < 5:
            continue
        p = perfil(r, 400)
        if not (p and p[0] == n and p[1] == j_esp and p[2]
                and p[3] == fusion_columna(k)):
            fallos_col.append((n, nombre, r, p))
print("comprobaciones (paso = n, j correcto, balanceado, punto de fusion):",
      118 + 116)
print("fallos:", len(fallos_col))
print("puntos de fusion (9^(k+1)-1)/4 :", [fusion_columna(k) for k in range(8)])
print("recurrencia m -> 9m + 2        :",
      all(fusion_columna(k + 1) == 9 * fusion_columna(k) + 2
          for k in range(60)))
print("unicidad e_2(n) = e_4(n) = 1 comprobada por barrido hasta n = 22;")
print("para n > 22 queda como conjetura, no como teorema.")

# --- 6. Testigos minimos ----------------------------------------------------
linea("6. Testigo minimo de cada nivel (menor r con primera fusion en n)")

RANGO = 300000
primero = {}
for r in range(RANGO):
    p = perfil(r, 200)
    if p is not None and p[2] and p[0] not in primero:
        primero[p[0]] = (r, p[1], p[3])
niveles = sorted(k for k in primero if k >= 3)
print("barrido r = 0 .. %d, en orden creciente (luego son minimos)" % RANGO)
print(" n      r   j   punto de fusion")
for n in niveles:
    r, j, m = primero[n]
    print("%2d %6d %3d %8d" % (n, r, j, m))
print()
contiguo = niveles[0]
while contiguo + 1 in primero:
    contiguo += 1
print("tramo contiguo garantizado : n = %d .. %d" % (niveles[0], contiguo))
print("nivel mas alto alcanzado   : n =", niveles[-1], "(por encima del tramo")
print("contiguo hay huecos: son niveles cuyo testigo minimo cae fuera del")
print("rango barrido, no niveles vacios)")
print("todos los testigos con j par:", all(primero[n][1] % 2 == 0 for n in niveles))
