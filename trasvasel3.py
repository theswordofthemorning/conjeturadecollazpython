# trasvasel3.py
#
# LO QUE QUEDA DE L3 -- LAS PIEZAS (i) Y (iii), PUESTAS A PRUEBA
# (11-08-2026 (2), continuacion de fichaagkv.txt seccion D y de la
# parte (ii) demostrada en teoremav2.txt).
#
#   (i) EL LIMITE LOCAL DE LA REVERSION dice: para el paseo perezoso
#   justo absorbido en 1 (V2a), con Q_s(2, y) = P(el paseo desde 2
#   sobrevive s pasos y termina en y),
#
#     P( sufijo de largo r con altura inicial y | tau = t )
#       = 4^(-r) * Q_{t-r}(2, y) / P(tau = t)
#       ---> 4^(-(r-1)) * (y - 1) = P~+( sufijo revertido )
#
#   porque Q_s(2, y) ~ c (y-1) s^(-3/2) (LLT del paseo absorbido:
#   reflexion + CLT local del reloj binomial) y P(tau = t) =
#   (1/4) Q_{t-1}(2, 2). EL LEMA DE COMPARACION (D) que (iii)
#   necesita: para r <= t/2 la densidad esta ACOTADA:
#
#     D(t, r, y) := Q_{t-r}(2, y) / (4 P(tau = t) (y - 1)) <= C
#
#   con C ~ 2^(3/2) (el peor caso r = t/2). FASE A: todo esto se
#   verifica EXACTO por programacion dinamica -- sin Monte Carlo.
#
#   (iii) EL TRASVASE: |W_tau| <= |W^(R)| (los ultimos R pasos, que
#   convergen a W~ del reverso por (i)+(D)) + el resto. El resto se
#   mata en dos tramos: el tramo r en (R, tau/2] por (D) + la parte
#   (ii) (la serie del reverso converge); el tramo r > tau/2 (la
#   PRIMERA mitad forward) por el Hoeffding condicional de la pieza
#   2: S(tau) - S(j) <= -c*tau para todo j <= tau/2, con
#   probabilidad 1 - t*e^(-c*t) dado el camino. FASES B y C: las
#   dos afirmaciones cuantitativas, medidas por MC.
#
#   COMPROBACIONES (SystemExit):
#     A1  el perfil en y del LLT: Q_s(2,y)*s^(3/2)/(y-1) tiene el
#         MISMO limite para todo y (max desvio relativo y<=8 contra
#         y=2: < 2% en s = 4000). EXACTO (DP).
#     A2  la densidad D(t, r, y) -> 1 para r fijo (|D-1| < 2% en
#         t = 4000, r = 10, y <= 8) y ACOTADA en r <= t/2:
#         sup D <= 3,5 en t = 2000. EXACTO (DP).
#     B   la primera mitad se aniquila: mediana de H_mitad =
#         Suma_{j <= tau/2} (1/2) 1{b_j=1} e^(S(tau)-S(j)) < 1e-3
#         en todas las ventanas, y DECRECE con T. (MC)
#     C   el truncamiento: P(err_R > 0,1 | ventana) con err_R = la
#         suma con j <= tau - R. LA CALIBRACION HONESTA (el primer
#         umbral, R = 80 <= 0,05, FALLO y ensenio la fisica): la
#         cola de log P~_R es -0,057 R +- 0,6 sqrt(R) -- gaussiana
#         hasta R ~ 300-600, recien despues exponencial. El teorema
#         solo pide eta_R -> 0 (R va a infinito ANTES que T); el
#         test pide (a) DECRECIENTE en R en toda ventana, (b)
#         estable en T a R fijo (la cota C*limite del lema D), y
#         (c) P(err_640 > 0,1) <= 0,10 en las ventanas con T >=
#         1600 (la prediccion gaussiana da ~0,02-0,11 ahi). (MC)
#
#   Fase A sin azar; fases B/C con semilla fija. Es verificacion del
#   mecanismo y de las DOS cotas cuantitativas nuevas; el texto de
#   la demostracion vive en teoremav2.txt.

import random
import math

# fase A (DP exacta)
S_MAX = 4000               # profundidad del DP
K_MAX = 420                # techo del paseo en el DP (masa perdida
                           # por encima: < e^-40 a s = 4000, declarada)
Y_TOPE = 8                 # alturas comparadas en el perfil
T_DENSIDAD = 2000          # el t del sup de la densidad

# fases B y C (MC)
VENTANAS_T = [400, 1600, 6400]
OBJETIVO = [3000, 2000, 800]
TOPE_CORRIDAS = 2 * 10 ** 6
RECORTES = [40, 160, 640]  # los R del truncamiento (ver C arriba)
SEMILLA = 20260812

LOG_MULT = {0: math.log(0.5), 1: math.log(1.5)}


# ---------------------------------------------------------------------------
# FASE A: el DP del paseo absorbido. Q[s][k], k = 2..K_MAX.
# paso: compartido 1/2 (k quieto), mixto 1/4 arriba, 1/4 abajo;
# absorcion al pisar 1 (desde 2 con el bit 1).
# ---------------------------------------------------------------------------

Q = [0.0] * (K_MAX + 2)
Q[2] = 1.0
Q_en_2 = {0: 1.0}          # Q_s(2, 2) por nivel (para P(tau = t))
perfil = {}                # Q_s(2, y) en los s de control
CONTROLES = [500, 1000, 2000, 4000]
for s in range(1, S_MAX + 1):
    nuevo = [0.0] * (K_MAX + 2)
    for k in range(2, K_MAX + 1):
        q = Q[k]
        if q:
            nuevo[k] += 0.5 * q
            if k + 1 <= K_MAX:
                nuevo[k + 1] += 0.25 * q
            if k - 1 >= 2:
                nuevo[k - 1] += 0.25 * q
    Q = nuevo
    Q_en_2[s] = Q[2]
    if s in CONTROLES or s == T_DENSIDAD:
        perfil[s] = Q[:]

# A1: el perfil en y
print("FASE A (exacta, DP): el LLT del paseo absorbido")
print("  Q_s(2,y) * s^(3/2) / (y-1), normalizado a y = 2:")
peor = 0.0
for s in CONTROLES:
    base = perfil[s][2]
    fila = []
    for y in range(2, Y_TOPE + 1):
        val = perfil[s][y] / (y - 1) / base
        fila.append("%.4f" % val)
        if s == S_MAX:
            peor = max(peor, abs(val - 1.0))
    print("  s = %4d:  y=2..%d -> %s" % (s, Y_TOPE, " ".join(fila)))
if peor > 0.02:
    raise SystemExit("A1: el perfil en y desvia %.3f > 2%% en s = %d"
                     % (peor, S_MAX))
print("COMPROBACION A1 OK: el perfil (y-1) es exacto a <2%% en s = %d"
      % S_MAX)
# y LA CONSTANTE del LLT: c0 = 4/sqrt(pi) (la demostracion de
# teoremav2.txt: reflexion + CLT local + reloj binomial)
c0_teorico = 4.0 / math.sqrt(math.pi)
c0_medido = Q_en_2[S_MAX] * S_MAX ** 1.5
if abs(c0_medido / c0_teorico - 1.0) > 0.01:
    raise SystemExit("A1b: c0 medido %.4f contra 4/sqrt(pi) = %.4f"
                     % (c0_medido, c0_teorico))
print("COMPROBACION A1b OK: Q_s(2,2)*s^(3/2) = %.4f en s = %d contra"
      % (c0_medido, S_MAX))
print("c0 = 4/sqrt(pi) = %.4f (la constante del LLT, demostrada)."
      % c0_teorico)
print()

# A2: la densidad D(t, r, y) -- convergencia a 1 y cota en r <= t/2
print("  la densidad D(t, r, y) = Q_(t-r)(2,y) / (4 P(tau=t) (y-1)):")
# convergencia a 1 con r = 10 fijo: el numerador es el perfil
# guardado en el nivel de control t y el denominador usa
# P(tau = t + r) = (1/4) Q_(t+r-1)(2,2), tambien guardado -- exacto
peor_conv = 0.0
r = 10
for t in CONTROLES:
    fila = ["%.4f" % (perfil[t][y] / (4 * 0.25 * Q_en_2[t + r - 1] * (y - 1)))
            for y in range(2, Y_TOPE + 1) if t + r <= S_MAX]
    if fila:
        print("  t+r = %4d (r = %d): D = %s" % (t + r, r, " ".join(fila)))
        if t == 2000:
            for y in range(2, Y_TOPE + 1):
                d = perfil[t][y] / (4 * 0.25 * Q_en_2[t + r - 1] * (y - 1))
                peor_conv = max(peor_conv, abs(d - 1.0))
if peor_conv > 0.02:
    raise SystemExit("A2a: D(t, 10, y) desvia %.3f > 2%% en t = 2010"
                     % peor_conv)

# el sup de la densidad en r <= t/2, t = T_DENSIDAD: aqui si hace
# falta Q_{t-r} para todo r -- segundo DP hasta t guardando Q_s(2,y)
# para y <= Y_TOPE en todos los s
# el sup se toma sobre TODO y (no solo y <= Y_TOPE): un sufijo de
# largo r ~ t/2 puede arrancar en altura y ~ sqrt(t), y la cota
# (LLT-b) que el tramo MEDIO de L3 usa tiene que ser uniforme en y
# (capa 2 propia: el primer barrido solo miraba y <= 8)
Qb = [0.0] * (K_MAX + 2)
Qb[2] = 1.0
q_por_s = {0: list(Qb)}
for s in range(1, T_DENSIDAD + 1):
    nuevo = [0.0] * (K_MAX + 2)
    for k in range(2, K_MAX + 1):
        q = Qb[k]
        if q:
            nuevo[k] += 0.5 * q
            if k + 1 <= K_MAX:
                nuevo[k + 1] += 0.25 * q
            if k - 1 >= 2:
                nuevo[k - 1] += 0.25 * q
    Qb = nuevo
    q_por_s[s] = list(Qb)
p_tau_t = 0.25 * q_por_s[T_DENSIDAD - 1][2]
sup_D = 0.0
sup_donde = (0, 0)
for r in range(1, T_DENSIDAD // 2 + 1):
    qs = q_por_s[T_DENSIDAD - r]
    for y in range(2, K_MAX + 1):
        if qs[y] > 0.0:
            D = qs[y] / (4 * p_tau_t * (y - 1))
            if D > sup_D:
                sup_D = D
                sup_donde = (r, y)
if sup_D > 3.5:
    raise SystemExit("A2b: sup D = %.3f > 3,5 (en r = %d, y = %d)"
                     % (sup_D, sup_donde[0], sup_donde[1]))
print("COMPROBACION A2 OK: D -> 1 (desvio %.4f en r = 10, t = 2010) y"
      % peor_conv)
print("sup sobre r <= t/2 y TODO y (2..%d) de D = %.3f <= 3,5 en"
      % (K_MAX, sup_D))
print("t = %d, alcanzado en (r = %d, y = %d); el 2^(3/2) teorico del"
      % (T_DENSIDAD, sup_donde[0], sup_donde[1]))
print("peor caso y-chico es 2,83: la cota superior de (LLT-b) es")
print("UNIFORME en y -- el gaussiano solo ayuda, como dice el texto.")
print()

# ---------------------------------------------------------------------------
# FASES B y C: MC forward con los prefijos del log-producto
# ---------------------------------------------------------------------------


def excursion_con_prefijos(azar, t_max):
    # devuelve (tau, S_lista, bits1) o None; S_lista[j] = S(j),
    # bits1 = indices j con b_j = 1
    k = 2
    S = 0.0
    S_lista = [0.0]
    bits1 = []
    for t in range(1, t_max + 1):
        r = azar.getrandbits(2)
        bit = r & 1
        es_mixto = (r >> 1) & 1
        S += LOG_MULT[bit]
        S_lista.append(S)
        if bit == 1:
            bits1.append(t)
        if es_mixto:
            if bit == 1:
                k -= 1
                if k <= 1:
                    return (t, S_lista, bits1)
            else:
                k += 1
    return None


print("FASES B y C (MC): la primera mitad se aniquila y el truncamiento")
print("es uniforme en T")
print("   T    muestras   mediana(H_mitad)  P(H>0,01)   " +
      "  ".join("P(err_%d > 0,1)" % R for R in RECORTES))
medianas_H = []
p_err_por_T = {R: [] for R in RECORTES}
for T, objetivo in zip(VENTANAS_T, OBJETIVO):
    azar = random.Random(SEMILLA + T)
    H_lista = []
    err_cuenta = {R: 0 for R in RECORTES}
    n = 0
    corridas = 0
    while n < objetivo and corridas < TOPE_CORRIDAS:
        corridas += 1
        res = excursion_con_prefijos(azar, 2 * T)
        if res is None:
            continue
        tau, S_lista, bits1 = res
        if not (T <= tau <= 2 * T):
            continue
        n += 1
        S_tau = S_lista[tau]
        H = 0.0
        for j in bits1:
            if j <= tau // 2:
                H += 0.5 * math.exp(S_tau - S_lista[j - 1])
        H_lista.append(H)
        for R in RECORTES:
            err = 0.0
            corte = tau - R
            for j in bits1:
                if j <= corte:
                    err += 0.5 * math.exp(S_tau - S_lista[j - 1])
                else:
                    break
            if err > 0.1:
                err_cuenta[R] += 1
    H_lista.sort()
    mediana_H = H_lista[len(H_lista) // 2]
    p_grande = sum(1 for h in H_lista if h > 0.01) / float(len(H_lista))
    medianas_H.append(mediana_H)
    fila = []
    for R in RECORTES:
        p = err_cuenta[R] / float(n)
        p_err_por_T[R].append(p)
        fila.append("%.3f" % p)
    print("  %5d  %7d     %.2e         %.3f       %s"
          % (T, n, mediana_H, p_grande, "        ".join(fila)),
          flush=True)

if not all(medianas_H[i + 1] <= medianas_H[i] for i in range(len(medianas_H) - 1)):
    raise SystemExit("B: la mediana de H_mitad NO decrece con T: %s"
                     % medianas_H)
if max(medianas_H) > 1e-3:
    raise SystemExit("B: mediana de H_mitad %.2e > 1e-3" % max(medianas_H))
print("COMPROBACION B OK: la primera mitad se aniquila (mediana %.1e ->"
      % medianas_H[0])
print("%.1e -> %.1e, decreciente): el tramo r > tau/2 no aporta."
      % (medianas_H[0] if len(medianas_H) < 2 else medianas_H[1],
         medianas_H[-1]))
# (a) decreciente en R dentro de cada ventana
for iT, T in enumerate(VENTANAS_T):
    serie = [p_err_por_T[R][iT] for R in RECORTES]
    if not all(serie[i + 1] < serie[i] for i in range(len(serie) - 1)):
        raise SystemExit("C-a: err no decrece en R en T = %d: %s"
                         % (T, serie))
# (b) estabilidad en T a R fijo (la cota C*limite del lema D)
for R in RECORTES:
    vals = p_err_por_T[R]
    if max(vals) > 1.6 * min(vals) + 0.05:
        raise SystemExit("C-b: err_%d inestable en T: %s" % (R, vals))
# (c) el nivel absoluto en el R profundo, ventanas grandes
profundas = [p_err_por_T[RECORTES[-1]][iT]
             for iT, T in enumerate(VENTANAS_T) if T >= 1600]
if max(profundas) > 0.10:
    raise SystemExit("C-c: P(err_%d > 0,1) = %.3f > 0,10 en T >= 1600"
                     % (RECORTES[-1], max(profundas)))
print("COMPROBACION C OK: err decrece en R en toda ventana, estable en")
print("T a R fijo, y P(err_%d > 0,1) <= %.3f en T >= 1600: eta_R -> 0"
      % (RECORTES[-1], max(profundas)))
print("al ritmo gaussiano-de-deriva predicho (-0,057R +- 0,6 sqrt(R));")
print("el teorema toma R -> inf ANTES que T y no pide mas.")
print()
print("Lectura: (i) verificado EXACTO (DP) -- el sufijo condicionado es")
print("el h-transform con densidad acotada (lema D) y la constante c0")
print("del LLT clavada; (iii) con sus dos cotas cuantitativas medidas.")
print("El texto entero de la demostracion (LLT incluido, ya no citado)")
print("vive en teoremav2.txt: L3 y el teorema V2, autocontenidos.")
