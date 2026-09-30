# CST de Terras para palabras de dos rachas impares: 1^a 0^b 1^c 0^d.
#
# Atajo T(n) = n/2 (par), (3n+1)/2 (impar). Sea n >= 2 con primer cruce del
# coeficiente en k = kappa(n) y vector de paridad V_k(n) = 1^a 0^b 1^c 0^d
# (a, b, c, d >= 1). Se quiere T^k(n) < n.
#
# Hechos usados (prueba escrita en LEEME.md):
#   * primer cruce en k  <=>  2^(a+b) < 3^a  y  k = bitlen(3^q), q = a + c;
#     d = k - a - b - c >= 1 sale solo.
#   * 2^k T^k(n) = 3^q n + B,  B = 3^c (3^a - 2^a) + 2^(a+b) (3^c - 2^c).
#   * falla el descenso  <=>  Delta * n <= B,  Delta = 2^k - 3^q.
#   * la clase de n mod 2^k es r = -B * 3^(-q) mod 2^k; basta la menor semilla
#     admisible n_min (r si r >= 2, si no r + 2^k), porque Delta > 0.
#   * cota a priori: si hay contraejemplo, n < 2 * 3^q / Delta <= 2 k^E / C0 con
#     Rhin (1987): k log 2 - q log 3 >= C0 * k^(-E), (C0, E) = (1, 13.3); ademas
#     n >= 2^a - 1 y 3^a (n + 1) >= 2^(a+b) (2^c - 1) + 2^a. Eso acota k.
#
# El script calcula la cota K_max para dos pares (C0, E) y recorre exhaustivamente
# todas las ternas (a, b, c) con k <= K_max, en enteros exactos.
import math
import sys

LOG2_3 = math.log2(3)
PARES = [(1.0, 13.3), (1e-3, 13.3)]   # Rhin literal y una version conservadora


def cota_k(c0, e):
    """Mayor k compatible con las desigualdades de la cota a priori (en coma
    flotante con holgura: se toma el primer k a partir del cual falla durante
    un tramo largo)."""
    ultimo = 0
    for k in range(4, 20000):
        N = 2.0 * k ** e / c0                     # n < N
        a_max = math.floor(math.log2(N + 1)) + 1  # 2^a - 1 < N  (holgura +1)
        q_max = 0
        for a in range(1, a_max + 1):
            # 2^(a+1) (2^c - 1) < 3^a (N + 1)  (b >= 1)
            c_max = math.floor(math.log2(1.5 ** a * (N + 1) / 2 + 1)) + 1
            q_max = max(q_max, a + c_max)
        if k < q_max * LOG2_3 + 1:
            ultimo = k
    return ultimo


def examinar(k_max, muestra_paridad=2000):
    triples = 0
    contra = []
    peor = None          # menor cociente Delta * n_min / B
    comprobadas = 0
    q = 2
    while True:
        tq = 3 ** q
        k = tq.bit_length()
        if k > k_max:
            break
        dos_k = 1 << k
        delta = dos_k - tq
        inv = pow(tq, -1, dos_k)
        for a in range(1, q):
            c = q - a
            ta = 3 ** a
            tc = 3 ** c
            b = 1
            while (1 << (a + b)) < ta:
                d = k - a - b - c
                assert d >= 1
                B = tc * (ta - (1 << a)) + (1 << (a + b)) * (tc - (1 << c))
                r = (-B * inv) % dos_k
                n = r if r >= 2 else r + dos_k
                triples += 1
                if delta * n <= B:
                    contra.append((a, b, c, d, n))
                cociente = (delta * n) / B
                if peor is None or cociente < peor[0]:
                    peor = (cociente, a, b, c, d, n)
                # comprobacion directa de la palabra en una muestra (k pequeno)
                if comprobadas < muestra_paridad and k <= 120:
                    x = n
                    palabra = []
                    for _ in range(k):
                        palabra.append(x & 1)
                        x = (3 * x + 1) // 2 if x & 1 else x // 2
                    esperada = [1] * a + [0] * b + [1] * c + [0] * d
                    assert palabra == esperada, (a, b, c, d, n)
                    assert (1 << k) * x == tq * n + B
                    comprobadas += 1
                b += 1
        q += 1
    return triples, contra, peor, comprobadas


for c0, e in PARES:
    print(f"Cota a priori con Lambda >= {c0} * k^-{e}: K_max = {cota_k(c0, e)}")

k_max = max(cota_k(c0, e) for c0, e in PARES)
print(f"\nRecorrido exhaustivo de las ternas con k <= {k_max}")
triples, contra, peor, comprobadas = examinar(k_max)
print(f"  ternas (a, b, c) examinadas: {triples}")
print(f"  palabras comprobadas directamente (k <= 120): {comprobadas}")
print(f"  contraejemplos (Delta * n_min <= B): {len(contra)}")
for t in contra[:10]:
    print("   ", t)
print(f"  menor cociente Delta * n_min / B: {peor[0]:.6g} en a={peor[1]}, b={peor[2]}, "
      f"c={peor[3]}, d={peor[4]}, n_min={peor[5]}")
sys.exit(0 if not contra else 1)
