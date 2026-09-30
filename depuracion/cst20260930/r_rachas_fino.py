# Metodo de Ocelotas para r rachas: exploracion numerica, no certificado.
#
# Para una palabra de primer cruce con r rachas impares (ver r_rachas.py), un
# contraejemplo a CST obliga a
#     q < F_r * log2(M),   M = (r+1) 3^q / Delta,   F_r = (L^r - 1)/(L - 1), L = log2 3,
# y a n < M. Con Rhin entero (3^q <= Delta k^14): q < F_r * log2((r+1) k^14), lo que
# acota k <= K_r. Para cada q <= Q_r (k = kmin(q), el unico posible) se decide si q
# sobrevive al test, y para los supervivientes se toma la cota n < M.
#
# Precision: log2(Delta) = k + log2(1 - 2^(-delta)), delta = k - q L, con L = log2 3
# en 60 cifras (modulo decimal) y 1 - 2^(-delta) se evalua con expm1 para reducir
# la cancelacion. No hay intervalos dirigidos ni cota demostrada del error total:
# ni la holgura 1e-6 ni ceil garantizan por si solas redondear conservadoramente.
# K_de_r tambien requiere una prueba de la cola infinita. Para una reduccion
# exacta reproducible, ver certificar_rachas.py y REVISION_RACHAS.md.
import math
import sys
from decimal import Decimal, getcontext

getcontext().prec = 60
L = Decimal(3).ln() / Decimal(2).ln()
Lf = float(L)
LN2 = math.log(2)


def K_de_r(F, r):
    ultimo = 0
    k = 4
    while True:
        q_max = F * (math.log2(r + 1) + 14 * math.log2(k))
        if k < q_max * Lf + 1:
            ultimo = k
        elif k > 2 * ultimo + 1000:
            return ultimo
        k += 1


def estudio(r):
    F = (Lf ** r - 1) / (Lf - 1)
    K = K_de_r(F, r)
    Q = int(K / Lf) + 2
    sobreviven = []
    for q in range(1, Q + 1):
        qL = q * L
        k = int(qL) + 1                     # menor k con 2^k > 3^q
        if k > K:
            continue
        delta = float(k - qL)               # en (0, 1), con precision relativa plena
        log2D = k + math.log2(-math.expm1(-delta * LN2))
        log2M = math.log2(r + 1) + float(qL) - log2D
        if q < F * log2M + 1e-6:
            n_max = math.ceil(2 ** log2M)   # n + 1 < M
            sobreviven.append((q, k, n_max))
    return F, K, Q, sobreviven


def main():
    r_min = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    r_max = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    if not 1 <= r_min <= r_max:
        raise SystemExit("Uso: r_rachas_fino.py R_MAX [R_MIN], con 1 <= R_MIN <= R_MAX")
    for r in range(r_min, r_max + 1):
        F, K, Q, s = estudio(r)
        peor = max(s, key=lambda t: t[2])
        print(f"r={r:2d} F={F:9.1f} K_r={K:9d} Q_r={Q:8d} supervivientes={len(s):5d} "
              f"k_max={max(t[1] for t in s):7d} n_max={peor[2]} (q={peor[0]}, k={peor[1]})")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
