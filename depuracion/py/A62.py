# A62 - verificacion independiente (agente 2, Python, a ciegas del .lean)
#
# ENUNCIADO: las casillas (A,B) que sobreviven al barrido (candidatas a ciclo)
# son (semi)convergentes de log2(3), pero SOLO las que lo aproximan POR ENCIMA.
#
# Convenios derivados desde cero (mapa CLASICO: n par -> n/2, n impar -> 3n+1):
#   A = numero de pasos impares (3n+1) del tramo/ciclo
#   B = numero de divisiones entre 2
# Para un tramo, manteniendo (a, b, c) con  2^b * n_j = 3^a * n_0 + c:
#   paso par :  b -> b+1                       (c igual)
#   paso impar: a -> a+1, c -> 3c + 2^b        (3n+1)
#   (para 3n-1: c -> 3c - 2^b)
# En un ciclo (n_j = n_0):  (2^B - 3^A) * n_0 = C.
#   3n+1: C > 0 si A >= 1  =>  2^B > 3^A  =>  B/A > log2(3)  (POR ENCIMA)
#   3n-1: C < 0            =>  2^B < 3^A  =>  B/A < log2(3)  (POR DEBAJO)
#
# Comparacion exacta:  B/A > log2(3)  <=>  2^B > 3^A   (solo enteros).
#
# Todo lo que decide es int / Fraction. Ningun float decide nada.

from fractions import Fraction
import sys

fallos = []

def chequeo(nombre, cond):
    print(("OK   " if cond else "FALLO") + " - " + nombre)
    if not cond:
        fallos.append(nombre)

# ----------------------------------------------------------------------
# 1. (Semi)convergentes de log2(3) por descenso de Stern-Brocot EXACTO.
#    Los nodos visitados en la busqueda binaria de Stern-Brocot hacia un
#    irracional son exactamente sus convergentes y semiconvergentes, y el
#    lado (encima/debajo) es el lado del que se aparta el mediante.
# ----------------------------------------------------------------------
def lado(p, q):
    # compara p/q con log2(3): devuelve +1 si p/q > log2 3 (2^p > 3^q), -1 si <
    d = 2**p - 3**q
    if d == 0:
        raise SystemExit("imposible: 2^p == 3^q con p,q > 0")
    return 1 if d > 0 else -1

Q_MAX = 20000
lo = (1, 1)   # 1/1 < log2 3
hi = (2, 1)   # 2/1 > log2 3
chequeo("1/1 esta por debajo de log2(3)", lado(1, 1) == -1)
chequeo("2/1 esta por encima de log2(3)", lado(2, 1) == +1)

visitados = [(1, 1, -1), (2, 1, +1)]   # (p, q, lado)
while True:
    p = lo[0] + hi[0]
    q = lo[1] + hi[1]
    if q > Q_MAX:
        break
    s = lado(p, q)
    visitados.append((p, q, s))
    if s < 0:
        lo = (p, q)
    else:
        hi = (p, q)

arriba = set((p, q) for (p, q, s) in visitados if s > 0)
abajo  = set((p, q) for (p, q, s) in visitados if s < 0)
print("semiconvergentes visitados (q <= %d): %d  (encima: %d, debajo: %d)"
      % (Q_MAX, len(visitados), len(arriba), len(abajo)))

# convergentes clasicos conocidos, clasificados aqui de forma exacta
for (p, q) in [(3, 2), (19, 12), (84, 53), (1054, 665)]:
    chequeo("%d/%d es (semi)convergente y aproxima POR DEBAJO" % (p, q),
            (p, q) in abajo)
for (p, q) in [(2, 1), (8, 5), (65, 41), (485, 306)]:
    chequeo("%d/%d es (semi)convergente y aproxima POR ENCIMA" % (p, q),
            (p, q) in arriba)

# ----------------------------------------------------------------------
# 2. El barrido: para cada A, la casilla viva es (A, B) con B minimo tal
#    que 2^B > 3^A (unica que puede alojar un ciclo 3n+1: C > 0 y ademas
#    n_0 = C/(2^B - 3^A) solo puede ser grande si 2^B/3^A esta pegado a 1).
#    "Sobrevivir" = marcar record de cercania 2^B/3^A -> 1 por encima.
# ----------------------------------------------------------------------
A_MAX = 400
records = []          # casillas record (A, B)
mejor = None          # mejor razon 2^B/3^A vista (Fraction exacta)
pow3 = 1
B = 0
pow2 = 1
for A in range(1, A_MAX + 1):
    pow3 *= 3
    while pow2 <= pow3:
        pow2 *= 2
        B += 1
    razon = Fraction(pow2, pow3)          # > 1 por construccion
    if mejor is None or razon < mejor:
        mejor = razon
        records.append((A, B))

print("records del barrido (A <= %d):" % A_MAX)
for (A, B) in records:
    print("   A=%3d  B=%3d   B/A = %d/%d   2^B/3^A = %.6f"
          % (A, B, B, A, float(Fraction(2**B, 3**A))))

import math
def mcd(a, b):
    while b:
        a, b = b, a % b
    return a

# 2a. TODO record es (semi)convergente POR ENCIMA (la mitad "solo por encima")
for (A, B) in records:
    g = mcd(B, A)
    chequeo("record (A=%d,B=%d): B/A reducido %d/%d es (semi)convergente POR ENCIMA"
            % (A, B, B // g, A // g), (B // g, A // g) in arriba)
    chequeo("record (A=%d,B=%d) es irreducible" % (A, B), g == 1)

# 2b. Reciproco: TODO (semi)convergente por encima con q <= A_MAX es record
arriba_en_rango = sorted((q, p) for (p, q) in arriba if q <= A_MAX)
rec_set = set((B, A) for (A, B) in records)
for (q, p) in arriba_en_rango:
    chequeo("(semi)convergente por encima %d/%d aparece como record" % (p, q),
            (p, q) in rec_set)
chequeo("los dos conjuntos coinciden exactamente (q <= %d)" % A_MAX,
        set((p, q) for (q, p) in arriba_en_rango) == rec_set)

# 2c. Ningun (semi)convergente POR DEBAJO aparece entre los records
for (p, q) in sorted(abajo, key=lambda t: t[1]):
    if q <= A_MAX:
        chequeo("por-debajo %d/%d NO es record (excluido)" % (p, q),
                (p, q) not in rec_set)

# ----------------------------------------------------------------------
# 3. El signo de C, medido sobre tramos reales (no solo derivado).
#    Para n = 1..500, 60 pasos del mapa clasico 3n+1: c >= 0 siempre,
#    y c > 0 exactamente cuando a >= 1.
# ----------------------------------------------------------------------
mal_signo = 0
casos = 0
for n0 in range(1, 501):
    n, a, b, c = n0, 0, 0, 0
    for _ in range(60):
        if n % 2 == 0:
            n //= 2
            b += 1
        else:
            c = 3 * c + 2**b
            n = 3 * n + 1
            a += 1
        casos += 1
        if 2**b * n != 3**a * n0 + c:
            mal_signo += 1
        if (a >= 1 and c <= 0) or (a == 0 and c != 0):
            mal_signo += 1
        if n == 1 and n0 != 1:
            break
chequeo("identidad 2^b*n_j = 3^a*n_0 + c y signo de c (3n+1): %d comprobaciones, 0 fallos"
        % casos, mal_signo == 0)

# ----------------------------------------------------------------------
# 4. Los ciclos reales caen donde dice el enunciado.
#    4a. 3n+1 positivo: {1,4,2} -> (A,B) = (1,2), B/A = 2/1, POR ENCIMA.
#    4b. 3n-1 positivo (= negativos de 3n+1): busqueda de ciclos por fuerza
#        bruta n = 1..2000; se esperan exactamente 3 ciclos, todos POR DEBAJO.
# ----------------------------------------------------------------------
def extraer_ciclo(n_en_ciclo, regla):
    ciclo = [n_en_ciclo]
    n = n_en_ciclo // 2 if n_en_ciclo % 2 == 0 else 3 * n_en_ciclo + regla
    while n != n_en_ciclo:
        ciclo.append(n)
        n = n // 2 if n % 2 == 0 else 3 * n + regla
    return ciclo

def AB_y_C_de_ciclo(ciclo, regla):
    n0 = ciclo[0]
    n, a, b, c = n0, 0, 0, 0
    for _ in ciclo:
        if n % 2 == 0:
            n //= 2
            b += 1
        else:
            c = 3 * c + regla * 2**b
            n = 3 * n + regla
            a += 1
    if n != n0:
        raise SystemExit("el ciclo no cierra")
    return a, b, c

# 4a
c31 = extraer_ciclo(1, +1)
a, b, c = AB_y_C_de_ciclo(c31, +1)
print("ciclo 3n+1: %s  A=%d B=%d C=%d" % (c31, a, b, c))
chequeo("ciclo trivial 3n+1: (A,B)=(1,2), 4 = 3 + 1, C=+1 > 0",
        (a, b, c) == (1, 2, 1) and 2**b > 3**a)
chequeo("2/1 (el ciclo trivial) es (semi)convergente POR ENCIMA y es record",
        (2, 1) in arriba and (2, 1) in rec_set)

# 4b
ciclos_3nm1 = {}
for n0 in range(1, 2001):
    n = n0
    vistos = set()
    for _ in range(5000):
        if n in vistos:
            break
        vistos.add(n)
        n = n // 2 if n % 2 == 0 else 3 * n - 1
    # n esta ya dentro del ciclo (o casi); iterar hasta repetir de verdad
    lento = n
    ciclo = extraer_ciclo(lento, -1)
    m = min(ciclo)
    ciclos_3nm1[m] = ciclo

print("ciclos de 3n-1 hallados (fuerza bruta n=1..2000): minimos = %s"
      % sorted(ciclos_3nm1))
chequeo("3n-1 tiene exactamente 3 ciclos con minimos {1, 5, 17}",
        sorted(ciclos_3nm1) == [1, 5, 17])
for m in sorted(ciclos_3nm1):
    ciclo = extraer_ciclo(m, -1)
    a, b, c = AB_y_C_de_ciclo(ciclo, -1)
    ok_id = (2**b - 3**a) * m == c
    g = mcd(b, a)
    print("   ciclo min=%d largo=%d  A=%d B=%d C=%d  B/A=%d/%d" % (m, len(ciclo), a, b, c, b // g, a // g))
    chequeo("ciclo 3n-1 min=%d: C=%d < 0 y 2^B < 3^A (por debajo)" % (m, c),
            c < 0 and 2**b < 3**a and ok_id)
    chequeo("ciclo 3n-1 min=%d: B/A = %d/%d es (semi)convergente POR DEBAJO"
            % (m, b // g, a // g), (b // g, a // g) in abajo)
    chequeo("ciclo 3n-1 min=%d: B/A NO esta entre los records de arriba" % m,
            (b // g, a // g) not in rec_set)

chequeo("la casilla (A=7,B=11) del lado descartado es el ciclo de 11 pasos de 3n-1",
        any(True for m in ciclos_3nm1 if AB_y_C_de_ciclo(extraer_ciclo(m, -1), -1)[:2] == (7, 11)))

# ----------------------------------------------------------------------
# 5. Bordes.
#    A=0: sin pasos impares no hay ciclo positivo (2^B * n = n exige B=0);
#         la "casilla" (0,B) no define B/A. Comprobado directamente.
#    (A,B)=(1,1): 2 < 3, por debajo -> no puede ser ciclo 3n+1; es
#         exactamente el ciclo {1,2} de 3n-1. Ya cubierto arriba.
#    n=1, n=2: viven en los ciclos triviales ya comprobados.
# ----------------------------------------------------------------------
sin_ciclo_A0 = all(2**B * n != n for B in range(1, 20) for n in range(1, 50))
chequeo("borde A=0: ningun n>=1 cumple 2^B*n = n con B>=1 (no hay ciclo sin impares)",
        sin_ciclo_A0)

# ----------------------------------------------------------------------
# 6. Matiz sobre "las 10 mas cercanas": si en vez de records se toman las
#    10 casillas mas cercanas de una rejilla grande, se cuelan sumas de
#    records (no reducibles a semiconvergente). Se mide y se informa.
# ----------------------------------------------------------------------
def diez_mas_cercanas(a_max):
    filas = []
    pow3 = 1
    B = 0
    pow2 = 1
    for A in range(1, a_max + 1):
        pow3 *= 3
        while pow2 <= pow3:
            pow2 *= 2
            B += 1
        filas.append((Fraction(pow2, pow3), A, B))
    filas.sort()
    return filas[:10]

for a_max in (40, 306):
    top = diez_mas_cercanas(a_max)
    exc = []
    for (r, A, B) in top:
        g = mcd(B, A)
        if (B // g, A // g) not in arriba:
            exc.append((A, B))
    print("rejilla A<=%d: 10 casillas mas cercanas -> %s ; excepciones (no (semi)convergente): %s"
          % (a_max, [(A, B) for (_, A, B) in top], exc))

print()
if fallos:
    print("RESULTADO: %d FALLOS" % len(fallos))
    for f in fallos:
        print("  - " + f)
    raise SystemExit(1)
print("RESULTADO: 0 fallos en todas las comprobaciones que deciden")
