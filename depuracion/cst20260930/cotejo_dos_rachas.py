# Cotejos independientes de dos_rachas.py.
#
# 1. Muestra aleatoria de ternas (a, b, c) con k <= K_MAX: se construye el menor
#    representante n de la clase bit a bit (sin la formula r = -B 3^-q mod 2^k):
#    cambiar el bit j de n cambia T^j(n) en 3^(s_j), impar, y por tanto su paridad.
#    Luego se itera T sobre n: se comprueba la palabra 1^a 0^b 1^c 0^d, que el
#    primer cruce del coeficiente es k y que T^k(n) < n directamente.
# 2. Barrido de todos los 2 <= n < 2^M: se calcula kappa(n) y la palabra hasta
#    kappa(n); si tiene dos rachas impares, se comprueba que (a, b, c) cumple la
#    caracterizacion usada (2^(a+b) < 3^a, k = bitlen(3^q)) y que T^k(n) < n.
#    Tambien se cuentan las palabras de una racha (control: Rozier-Terracol, ap. A).
import random
import sys

K_MAX = 539
MUESTRA = 20000
M = 22
random.seed(20260930)


def T(x):
    return (3 * x + 1) // 2 if x & 1 else x // 2


# ---------- 1 ----------
ternas = []
q = 2
while True:
    k = (3 ** q).bit_length()
    if k > K_MAX:
        break
    for a in range(1, q):
        b = 1
        while (1 << (a + b)) < 3 ** a:
            ternas.append((a, b, q - a, k))
            b += 1
    q += 1
fallos1 = 0
for a, b, c, k in random.sample(ternas, MUESTRA):
    d = k - a - b - c
    palabra = [1] * a + [0] * b + [1] * c + [0] * d
    # construccion bit a bit con la identidad de Terras:
    # T^j(n_j + 2^j t) = T^j(n_j) + 3^(s_j) t, con n_j = n mod 2^j e y = T^j(n_j)
    n = 0
    y = 0
    p3 = 1
    for j in range(k):
        if (y & 1) != palabra[j]:
            n += 1 << j
            y += p3
        if palabra[j]:
            y = (3 * y + 1) // 2
            p3 *= 3
        else:
            y //= 2
    if n < 2:
        n += 1 << k
    x = n
    unos = 0
    ok = True
    for j in range(k):
        if (x & 1) != palabra[j]:
            ok = False
        unos += x & 1
        if j + 1 < k and 3 ** unos < 2 ** (j + 1):
            ok = False                     # cruce antes de k
        x = T(x)
    if 3 ** unos >= 2 ** k:
        ok = False
    if not ok or not (x < n):
        fallos1 += 1
print(f"1. Muestra de {MUESTRA} ternas (de {len(ternas)}) con k <= {K_MAX}, construccion bit a bit "
      f"e iteracion directa: {'OK' if fallos1 == 0 else str(fallos1) + ' FALLOS'}")

# ---------- 2 ----------
dos = 0
una = 0
fallos2 = 0
ternas_vistas = set()
for n in range(2, 1 << M):
    x = n
    p3 = 1
    p2 = 1
    j = 0
    palabra = []
    while True:
        bit = x & 1
        palabra.append(bit)
        if bit:
            p3 *= 3
        x = T(x)
        j += 1
        p2 *= 2
        if p3 < p2:
            break
    k = j
    # rachas
    rachas = []
    for bit in palabra:
        if rachas and rachas[-1][0] == bit:
            rachas[-1][1] += 1
        else:
            rachas.append([bit, 1])
    impares = [r for r in rachas if r[0] == 1]
    if len(impares) == 1:
        una += 1
        if not (x < n):
            fallos2 += 1
    elif len(impares) == 2:
        dos += 1
        (_, a), (_, b), (_, c), (_, d) = rachas
        if not ((1 << (a + b)) < 3 ** a and (3 ** (a + c)).bit_length() == k):
            fallos2 += 1
        if not (x < n):
            fallos2 += 1
        ternas_vistas.add((a, b, c))
print(f"2. Barrido 2 <= n < 2^{M}: {una} semillas de una racha y {dos} de dos rachas "
      f"({len(ternas_vistas)} ternas distintas); caracterizacion y descenso: "
      f"{'OK' if fallos2 == 0 else str(fallos2) + ' FALLOS'}")
sys.exit(0 if fallos1 == 0 and fallos2 == 0 else 1)
