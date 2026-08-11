# revision9_adv2/dp_indep.py
# ADVERSARIO 2, 9a revision: DP INDEPENDIENTE del LLT del paseo perezoso
# absorbido. NO abre trasvasel3.py; re-deriva desde el modelo:
#   paso: 1/2 quieto (compartido), 1/4 arriba, 1/4 abajo (mixto);
#   absorcion al pisar 1 (solo posible desde 2, bajando).
# Techo DISTINTO del repo (500 vs 420) para sensibilidad al cap.
import math

S_MAX = 4000
K_CAP = 500

prob = [0.0] * (K_CAP + 2)
prob[2] = 1.0
q22 = {0: 1.0}            # Q_s(2,2)
hist = {0: prob[:]}       # historial completo hasta 2000 (para sup D)
snap = {}
T_D = 2000

for s in range(1, S_MAX + 1):
    nx = [0.0] * (K_CAP + 2)
    for k in range(2, K_CAP + 1):
        p = prob[k]
        if p:
            nx[k] += 0.5 * p
            if k + 1 <= K_CAP:
                nx[k + 1] += 0.25 * p
            if k >= 3:
                nx[k - 1] += 0.25 * p
    prob = nx
    q22[s] = prob[2]
    if s <= T_D:
        hist[s] = prob[:]
    if s in (500, 1000, 2000, 4000):
        snap[s] = prob[:]

c0_teo = 4.0 / math.sqrt(math.pi)
c0_med = q22[4000] * 4000 ** 1.5
print("c0: medido s=4000 -> %.4f ; 4/sqrt(pi) = %.4f ; cociente %.5f"
      % (c0_med, c0_teo, c0_med / c0_teo))

# perfil (y-1): Q_s(2,y)/(y-1) normalizado a y=2
for s in (1000, 4000):
    base = snap[s][2]
    fila = ["%.4f" % (snap[s][y] / (y - 1) / base) for y in range(2, 9)]
    print("perfil s=%4d y=2..8: %s" % (s, " ".join(fila)))

# sup D sobre r <= t/2 y TODO y, t = 2000:
#   D = Q_{t-r}(2,y) / (Q_{t-1}(2,2) * (y-1))   [4 P(tau=t) = Q_{t-1}(2,2)]
den = q22[T_D - 1]
supD = 0.0
arg = (0, 0)
for r in range(1, T_D // 2 + 1):
    qs = hist[T_D - r]
    for y in range(2, K_CAP + 1):
        if qs[y] > 0.0:
            d = qs[y] / (den * (y - 1))
            if d > supD:
                supD = d
                arg = (r, y)
print("sup D (t=2000, r<=1000, y<=%d) = %.3f en (r=%d, y=%d);"
      % (K_CAP, supD, arg[0], arg[1]))
print("  2^(3/2) = %.3f" % 2 ** 1.5)

# D -> 1 con r = 10 fijo, t = 2000
r = 10
fila = ["%.4f" % (hist[T_D - r][y] / (den * (y - 1))) for y in range(2, 9)]
print("D(t=2000, r=10, y=2..8): %s" % " ".join(fila))

# la cola de la ventana: P(tau en [T,2T])*sqrt(T) contra (c0/2)(1-2^-0.5)
for T in (500, 1000, 2000):
    m = sum(0.25 * q22[t - 1] for t in range(T, 2 * T + 1))
    print("P(tau en [%d,%d])*sqrt(T) = %.4f ; (c0/2)(1-2^-1/2) = %.4f"
          % (T, 2 * T, m * math.sqrt(T),
             (c0_teo / 2) * (1 - 2 ** -0.5)))
