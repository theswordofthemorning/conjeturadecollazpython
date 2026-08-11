# revision9_adv2/exacto_fracciones.py
# ADVERSARIO 2, 9a revision: verificacion EXACTA (fractions) de
#  (a) el TELESCOPIO del h-transform del Lema D:
#      P~+(sigma revertido) = 4^-(r-1) * (y-1), para TODO sufijo de
#      absorcion de largo r (enumeracion completa, r = 2..7), y la
#      biyeccion: Suma_sigma P~+(sigma rev) = 1.
#  (b) la FACTORIZACION de Markov del Lema D:
#      Suma_sigma 4^-r Q_{t-r}(2, y(sigma)) = P(tau = t)  (exacto, t=12, r=4;
#      la particion del evento {tau = t} por su sufijo de largo r es completa).
#  (c) la IDENTIDAD DE PARADA OPCIONAL del Lema (iii-b):
#      P~+(tau_m <= R) = (m-1) * P_2(tau_m <= R, tau_m < tau_1)
#      EXACTA por DP racional (mas fuerte que el MC del repo).
from fractions import Fraction as F
from itertools import product

# simbolos forward: 0 = compartido bit0, 1 = compartido bit1,
#                   2 = mixto bit0 (sube), 3 = mixto bit1 (baja)

def sufijos_absorbentes(r):
    """todas las palabras de largo r que, desde su altura inicial y,
    absorben EXACTO en el paso r sin pisar 1 antes; devuelve (word, y)."""
    out = []
    for word in product(range(4), repeat=r):
        m1 = sum(1 for c in word if c == 3)
        m0 = sum(1 for c in word if c == 2)
        y = 1 + m1 - m0
        if y < 2 or word[-1] != 3:
            continue
        k = y
        ok = True
        for i, c in enumerate(word):
            if c == 3:
                k -= 1
            elif c == 2:
                k += 1
            if i < r - 1 and k <= 1:
                ok = False
                break
        if ok and k == 1:
            out.append((word, y))
    return out


def prob_reverso(word):
    """P~+ del camino revertido: el primer paso revertido (el absorbente,
    word[-1] = mixto bit1) es deterministico en P~+ (k~: 1->2);
    despues, cada simbolo forward leido hacia atras:
      compartido: 1/2 reloj * 1/2 bit = 1/4
      mixto bit1 (forward baja) = reverso SUBE: 1/2 * k/(2(k-1))
      mixto bit0 (forward sube) = reverso BAJA: 1/2 * (k-2)/(2(k-1))
    devuelve (prob, k_final)."""
    k = 2
    p = F(1)
    for c in reversed(word[:-1]):
        if c in (0, 1):
            p *= F(1, 4)
        elif c == 3:
            p *= F(1, 2) * F(k, 2 * (k - 1))
            k += 1
        else:
            p *= F(1, 2) * F(k - 2, 2 * (k - 1))
            k -= 1
    return p, k


print("(a) TELESCOPIO P~+(sigma rev) = 4^-(r-1) (y-1), enumeracion completa:")
for r in range(2, 8):
    lote = sufijos_absorbentes(r)
    total = F(0)
    fallos = 0
    for word, y in lote:
        p, kf = prob_reverso(word)
        if kf != y or p != F(1, 4) ** (r - 1) * (y - 1):
            fallos += 1
        total += p
    if fallos or total != 1:
        raise SystemExit("(a) ROTO en r=%d: %d fallos, suma=%s"
                         % (r, fallos, total))
    print("  r=%d: %5d sufijos, telescopio EXACTO en todos, suma P~+ = 1"
          % (r, len(lote)))

# --- DP exacto de Q_s(2,y) ---
def dp_Q(s_max, k_max):
    q = {2: F(1)}
    hist = {0: dict(q)}
    for s in range(1, s_max + 1):
        nq = {}
        for k, p in q.items():
            nq[k] = nq.get(k, F(0)) + p / 2
            if k + 1 <= k_max:
                nq[k + 1] = nq.get(k + 1, F(0)) + p / 4
            if k - 1 >= 2:
                nq[k - 1] = nq.get(k - 1, F(0)) + p / 4
        q = {k: p for k, p in nq.items() if p}
        hist[s] = dict(q)
    return hist

T = 12
R = 4
hist = dp_Q(T, T + 3)
p_tau_t = F(1, 4) * hist[T - 1].get(2, F(0))
suma = F(0)
for word, y in sufijos_absorbentes(R):
    suma += F(1, 4) ** R * hist[T - R].get(y, F(0))
print("(b) FACTORIZACION: Suma_sigma 4^-r Q_{t-r}(2,y) = %s ; P(tau=%d) = %s"
      % (suma, T, p_tau_t))
if suma != p_tau_t:
    raise SystemExit("(b) ROTO: la particion por sufijos NO reconstruye "
                     "P(tau=t)")
print("    EXACTO: la particion del evento {tau=t} por sufijos es completa.")

# --- (c) parada opcional ---
def p2_exito(m, R):
    dist = {2: F(1)}
    win = F(0)
    for _ in range(R):
        nd = {}
        for k, p in dist.items():
            for k2, pr in ((k, F(1, 2)), (k + 1, F(1, 4)), (k - 1, F(1, 4))):
                if k2 == m:
                    win += p * pr
                elif k2 <= 1:
                    pass
                else:
                    nd[k2] = nd.get(k2, F(0)) + p * pr
        dist = nd
    return win


def ptilde_exito(m, R):
    dist = {2: F(1)}
    win = F(0)
    for _ in range(R):
        nd = {}
        for k, p in dist.items():
            trans = [(k, F(1, 2)),
                     (k + 1, F(k, 4 * (k - 1))),
                     (k - 1, F(k - 2, 4 * (k - 1)))]
            for k2, pr in trans:
                if pr == 0:
                    continue
                if k2 == m:
                    win += p * pr
                else:
                    nd[k2] = nd.get(k2, F(0)) + p * pr
        dist = nd
    return win


print("(c) PARADA OPCIONAL P~+(tau_m <= R) = (m-1) P_2(tau_m <= R, < tau_1):")
for (m, R) in ((4, 10), (6, 12), (9, 20), (12, 40), (9, 40)):
    izq = ptilde_exito(m, R)
    der = (m - 1) * p2_exito(m, R)
    ok = "EXACTO" if izq == der else "ROTO"
    print("  (m=%2d, R=%2d): P~+ = %.10f, (m-1)P_2 = %.10f  -> %s"
          % (m, R, float(izq), float(der), ok))
    if izq != der:
        raise SystemExit("(c) ROTA la identidad en (m=%d, R=%d)" % (m, R))
print("TODO EXACTO: telescopio, factorizacion e identidad de parada.")
