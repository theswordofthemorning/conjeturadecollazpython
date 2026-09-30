# Cuantas ternas de dos rachas sobreviven a los filtros exactos que no necesitan
# el representante minimo, con la forma entera de Rhin  3^q <= Delta * k^14.
#
# Si la terna (a, b, c) tuviera un contraejemplo n (Delta n <= B), entonces
#   (F1) (2^a - 1) Delta <= B                        [n >= 2^a - 1]
#   (F2) Delta (2^(a+b) (2^c - 1) + 2^a - 3^a) <= 3^a B   [3^a (n+1) >= 2^(a+b)(2^c-1) + 2^a]
# Con 3^q <= Delta k^14 y B < 2 3^q sale n < 2 k^14, y de ahi una cota K1 de k que
# se prueba solo con enteros: 3^a < 4^a, 3^c < 4^c (ver LEEME.md). Aqui se calcula
# K1 por busqueda directa y se cuentan las ternas con k <= K1 que pasan F1 y F2.
import math
import sys

# Cota K1: el menor k0 tal que para todo k >= k0 es imposible
#   2^a <= 2 k^14 (F1'), 2^(a+1) (2^c - 1) < 3^a (2 k^14 + 1) (F2'), 2^(k-1) < 3^(a+c).
# Se usa la cota cruda del LEEME: 3^(a+c) <= 36 k^84; basta 2^(k-1) >= 36 k^84.
k0 = 2
while not all((1 << (k - 1)) >= 36 * k ** 84 for k in range(k0, k0 + 200)):
    k0 += 1
K1 = k0 - 1
print(f"Cota entera cruda: para k >= {k0} es 2^(k-1) >= 36 k^84 (comprobado en un tramo); K1 = {K1}")

# Comprobacion de la forma entera de Rhin en el tramo k <= K1 (es un teorema; aqui
# solo se coteja numericamente con enteros exactos).
malos_rhin = 0
q = 1
while True:
    tq = 3 ** q
    k = tq.bit_length()
    if k > K1:
        break
    if tq > ((1 << k) - tq) * k ** 14:
        malos_rhin += 1
    q += 1
print(f"Forma entera de Rhin 3^q <= (2^k - 3^q) k^14 falla en k <= {K1}: {malos_rhin} veces")

total = 0
pasan_f1 = 0
pasan = []
q = 2
while True:
    tq = 3 ** q
    k = tq.bit_length()
    if k > K1:
        break
    delta = (1 << k) - tq
    for a in range(1, q):
        c = q - a
        ta = 3 ** a
        tc = 3 ** c
        b = 1
        while (1 << (a + b)) < ta:
            total += 1
            B = tc * (ta - (1 << a)) + (1 << (a + b)) * (tc - (1 << c))
            if ((1 << a) - 1) * delta <= B:
                pasan_f1 += 1
                if delta * ((1 << (a + b)) * ((1 << c) - 1) + (1 << a) - ta) <= ta * B:
                    pasan.append((k, a, b, c))
            b += 1
    q += 1
print(f"Ternas con k <= {K1}: {total}; pasan F1: {pasan_f1}; pasan F1 y F2: {len(pasan)}")
print(f"k maximo entre las supervivientes: {max(t[0] for t in pasan)}")
por_k = {}
for t in pasan:
    por_k[t[0]] = por_k.get(t[0], 0) + 1
print("supervivientes por k (k: numero):", dict(sorted(por_k.items())))
sys.exit(0)
