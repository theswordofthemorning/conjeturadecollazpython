# Viabilidad del metodo de Ocelotas para r rachas impares.
#
# Palabra hasta el primer cruce: 1^a1 0^b1 1^a2 0^b2 ... 1^ar 0^br, q = sum a_i,
# P = 3^q, Delta = 2^k - P, M = (r+1) P / Delta.
#   * B / P < r  (cada racha aporta menos de 1), y el fallo da Delta n <= B < r P,
#     luego n + 1 < M.
#   * congruencias: x_i + 1 >= 2^(a_i) y 3^(a_i)(x_i + 1) >= 2^(a_i)(x_(i+1) + 1),
#     luego n + 1 >= U_i / 3^(p_i), con U_i = 2^(a_1+...+a_i), p_i = a_1+...+a_(i-1).
#   * version entera (la de Lean): 3^a < (2^a)^2 da U_r < M^(2^r - 1), es decir
#       2^q Delta^E < ((r+1) P)^E,  E = 2^r - 1.
#   * version fina: 3^a = (2^a)^(log2 3) da q < log2(M) (1.585^r - 1)/0.585.
# Con Rhin entero (P <= Delta k^14): M <= (r+1) k^14, lo que acota k (K_r).
# Test por q hasta K_r: sobreviven los q con 2^q Delta^E < ((r+1)P)^E (entero) o con
# q < log2(M) F_r (fino). Para ellos, n < M y k conocido: basta CST para n pequenos.
#
# Calculo exacto con enteros para la version entera (r <= 4) y con logaritmos en
# doble precision, con holgura, para la fina. Es un estudio de viabilidad.
import math

LOG2_3 = math.log2(3)


def cota_k(r, E_exp):
    """Mayor k compatible con q < E_exp * log2((r+1) k^14) y k < q log2 3 + 1."""
    ultimo = 0
    for k in range(4, 10 ** 6):
        q_max = E_exp * (math.log2(r + 1) + 14 * math.log2(k))
        if k < q_max * LOG2_3 + 1:
            ultimo = k
        elif k > 2 * ultimo + 1000:
            break
    return ultimo


def estudio(r, exacto):
    E = 2 ** r - 1
    F = (LOG2_3 ** r - 1) / (LOG2_3 - 1)
    K = cota_k(r, E if exacto else F)
    sobreviven = []
    q = 1
    while True:
        P = 3 ** q
        k = P.bit_length()
        if k > K:
            break
        D = (1 << k) - P
        if exacto:
            falla_test = (1 << q) * D ** E < ((r + 1) * P) ** E
        else:
            log2M = math.log2(r + 1) + math.log2(P) - math.log2(D)
            falla_test = q < log2M * F + 1e-6
        if falla_test:
            n_max = ((r + 1) * P) // D       # n + 1 < M
            sobreviven.append((q, k, n_max))
        q += 1
    return K, sobreviven


for r in (2, 3, 4):
    K, s = estudio(r, exacto=True)
    print(f"r={r} (entera, E={2**r-1}): K_r={K}; sobreviven {len(s)} valores de q; "
          f"k max={max(t[1] for t in s)}; n max={max(t[2] for t in s)}")
for r in (2, 3, 4, 5, 6, 8, 10):
    K, s = estudio(r, exacto=False)
    print(f"r={r} (fina, F={((LOG2_3**r)-1)/(LOG2_3-1):.1f}): K_r={K}; sobreviven {len(s)} q; "
          f"k max={max(t[1] for t in s)}; n max={max(t[2] for t in s)}")
