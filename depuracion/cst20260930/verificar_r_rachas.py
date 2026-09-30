# Cotejo sobre datos reales del metodo de r rachas y barrido directo de CST.
#
# Para cada 2 <= n < 2^M se calcula el primer cruce del coeficiente k = tau(n), la
# palabra de paridad hasta k y sus r rachas impares 1^a1 0^b1 ... 1^ar 0^br. Se
# comprueba:
#   1. CST: T^k(n) < n (barrido directo; cubre los n_max de r_rachas_fino.py);
#   2. el lema del termino aditivo: B = 2^k T^k(n) - 3^q n cumple 0 <= B < r 3^q;
#   3. el lema de las congruencias: para cada i, (n + 1) 3^(p_i) >= 2^(a_1+...+a_i),
#      con p_i = a_1 + ... + a_(i-1);
#   4. la forma de la palabra: '0' (n par, r = 0) o empieza por 1 y termina en 0.
# Informa del numero de semillas por r y del r maximo observado.
import sys
from collections import Counter

M = int(sys.argv[1]) if len(sys.argv) > 1 else 22


def T(x):
    return (3 * x + 1) >> 1 if x & 1 else x >> 1


por_r = Counter()
fallos = Counter()
for n in range(2, 1 << M):
    x = n
    p3 = 1
    p2 = 1
    palabra = []
    while True:
        bit = x & 1
        palabra.append(bit)
        if bit:
            p3 *= 3
        x = T(x)
        p2 <<= 1
        if p3 < p2:
            break
    k = len(palabra)
    if palabra == [0]:
        # n par: primer cruce en k = 1, sin rachas impares (r = 0)
        por_r[0] += 1
        if not (x < n):
            fallos["CST"] += 1
        continue
    # rachas
    rachas = []
    for bit in palabra:
        if rachas and rachas[-1][0] == bit:
            rachas[-1][1] += 1
        else:
            rachas.append([bit, 1])
    if rachas[0][0] != 1 or rachas[-1][0] != 0 or len(rachas) % 2:
        fallos["forma"] += 1
        continue
    impares = [rachas[j][1] for j in range(0, len(rachas), 2)]
    r = len(impares)
    q = sum(impares)
    por_r[r] += 1
    if not (x < n):
        fallos["CST"] += 1
    B = p2 * x - p3 * n                      # p2 = 2^k, p3 = 3^q
    if not (0 <= B < r * p3):
        fallos["B"] += 1
    acumulado = 0
    for a in impares:
        # (n+1) 3^(p_i) >= 2^(p_i + a_i)
        if (n + 1) * 3 ** acumulado < 1 << (acumulado + a):
            fallos["congruencias"] += 1
            break
        acumulado += a
print(f"Barrido 2 <= n < 2^{M}: semillas por numero de rachas impares r:")
print("  " + ", ".join(f"r={r}: {c}" for r, c in sorted(por_r.items())))
print(f"  r maximo observado: {max(por_r)}")
print(f"  fallos: {dict(fallos) if fallos else 'ninguno'} (CST, lema de B, lema de congruencias, forma)")
sys.exit(0 if not fallos else 1)
