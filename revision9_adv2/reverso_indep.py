# revision9_adv2/reverso_indep.py
# ADVERSARIO 2, 9a revision: simulacion INDEPENDIENTE (semilla y codigo
# propios, sin abrir medianauniversal.py) de:
#   1) el objeto limite W~_inf del reverso h-transformado: cuantiles
#      contra los publicados (mediana 17,50; M = 53,55);
#   2) LA DERIVA de log P~_R bajo P~+ (el ataque a la NOTA DE TASA:
#      el repo publica "log P~_R = -0,057 R +- 0,6 sqrt(R)");
#   3) el forward V2a condicionado a tau en [T, 2T] con T = 400:
#      mediana de |W_tau| y exito contra M (publicado: 16,14 y 0,769).
import random
import math

SEMILLA = 777
N_REV = 40000
CORTE = 1e-250          # corte hondo: sin sesgo de truncamiento en la deriva
HORIZONTE = 4000
CHECKPOINTS = [40, 80, 160, 320, 640]

azar = random.Random(SEMILLA)
absw = []
logs = {R: [] for R in CHECKPOINTS}
kmed = {R: [] for R in CHECKPOINTS}
for _ in range(N_REV):
    w = -0.5
    p = 1.5
    k = 2
    lp = math.log(1.5)
    r = 1
    while p > CORTE and r < HORIZONTE:
        r += 1
        if azar.random() < 0.5:            # compartido: bit libre justo
            bit = 1 if azar.random() < 0.5 else 0
        else:                               # mixto: h-transform
            if azar.random() < k / (2.0 * (k - 1)):
                bit = 1
                k += 1
            else:
                bit = 0
                k -= 1
        if bit == 1:
            w -= 0.5 * p
            p *= 1.5
            lp += math.log(1.5)
        else:
            p *= 0.5
            lp -= math.log(2.0)
        if r in logs:
            logs[r].append(lp)
            kmed[r].append(k)
    absw.append(abs(w))

absw.sort()


def q(v, pc):
    return v[min(len(v) - 1, int(round(pc / 100.0 * (len(v) - 1))))]


print("REVERSO independiente (semilla %d, N = %d):" % (SEMILLA, N_REV))
print("  |W~_inf| cuantiles 10/25/50/75/90 = %.3f / %.3f / %.3f / %.3f / %.3f"
      % tuple(q(absw, pc) for pc in (10, 25, 50, 75, 90)))
print("  publicados (medianauniversal): 3.612 / 7.117 / 17.495 / 53.553 "
      "/ 181.384")
M_pub = 53.5532
exito_rev = sum(1 for v in absw if v <= M_pub) / float(len(absw))
print("  P(|W~_inf| <= 53,553) con MI muestra = %.3f (deberia ~ 0,75)"
      % exito_rev)
print()
print("LA DERIVA de log P~_R bajo P~+ (ataque a la NOTA DE TASA):")
print("    R    media(logP~_R)  media/R    sd      sd/sqrt(R)   k~ medio")
for R in CHECKPOINTS:
    v = logs[R]
    n = len(v)
    mu = sum(v) / n
    sd = math.sqrt(sum((x - mu) ** 2 for x in v) / n)
    km = sum(kmed[R]) / float(n)
    print("  %4d    %8.2f      %+.4f   %6.2f     %.3f      %.1f"
          % (R, mu, mu / R, sd, sd / math.sqrt(R), km))
print("  la NOTA DE TASA del repo dice: -0,057 R +- 0,6 sqrt(R)")
print()

# forward V2a, T = 400: dinamica desde el modelo, no desde el codigo del repo
T = 400
OBJ = 1500
azar = random.Random(SEMILLA + 1)
muestra = []
corridas = 0
while len(muestra) < OBJ and corridas < 10 ** 6:
    corridas += 1
    k = 2
    w = 0.0
    tau = None
    for t in range(1, 2 * T + 1):
        bit = 1 if azar.random() < 0.5 else 0
        mixto = azar.random() < 0.5
        w = (3.0 * w - 1.0) / 2.0 if bit == 1 else w / 2.0
        if mixto:
            if bit == 1:
                k -= 1
                if k <= 1:
                    tau = t
                    break
            else:
                k += 1
    if tau is not None and T <= tau <= 2 * T:
        muestra.append(abs(w))
muestra.sort()
print("FORWARD independiente T = %d (%d muestras, %d corridas):" %
      (T, len(muestra), corridas))
print("  mediana |W_tau| = %.3f (publicado 16,14);  P(|W| <= M=53,55) = %.3f"
      " (publicado 0,769)"
      % (q(muestra, 50),
         sum(1 for v in muestra if v <= M_pub) / float(len(muestra))))
print()

# la raiz de la pieza 2 (Lema 3), con las constantes de verdad
mu_l = 0.5 * math.log(4.0 / 3.0)      # 0,14384
sig = math.log(3.0) / 2.0             # 0,54931
a = 12 * mu_l - 1                     # 0,72608
b = 2 * sig * math.sqrt(12)           # 3,80559
c = math.log(1.5)                     # 0,40546
z = (b + math.sqrt(b * b + 4 * a * c)) / (2 * a)
print("PIEZA 2: raiz exacta sqrt(log x) = %.4f (el texto dice 5,347);"
      % z)
print("  log x minimo = %.2f -> basta log x >= 29: %s ; en log x = 28 el"
      % (z * z, z * z <= 29))
print("  margen es %.3f (el texto dice 'falla por 0,2')"
      % (a * 28 - b * math.sqrt(28) - c))
