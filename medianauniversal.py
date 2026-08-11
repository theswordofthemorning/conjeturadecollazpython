# medianauniversal.py
#
# LA PIEZA 3 (L3) DEL TEOREMA V2, PUESTA A PRUEBA POR SUS DOS PUNTAS
# (11-08-2026 (2), tras leer AGKV 2005 entero -- ficha: fichaagkv.txt).
#
#   L3 pide: P( |W_tau| <= M | tau en [T, 2T] ) >= 1/2 con M UNIVERSAL
#   (independiente de x, o sea de T = 30 log x). La lectura de AGKV
#   dio el mecanismo: REVERTIR LA EXCURSION EN LA ABSORCION.
#
#     W_tau = Sigma_j d_j Prod_{i>j} A_i  =  Sigma_r d~_r P~_{r-1}
#
#   con P~_r = producto de los ULTIMOS r multiplicadores. La excursion
#   condicionada, leida desde el final, converge localmente a la
#   cadena h-transformada con h(k) = k - 1 (el paseo perezoso justo
#   condicionado a no volver a 1: Bessel-3 discreto, h EXPLICITA):
#
#     compartido w.p. 1/2 (bit libre justo);
#     mixto: k~ sube w.p. k/(2(k-1))  [bit forward 1, mult 3/2],
#            k~ baja w.p. (k-2)/(2(k-1)) [bit forward 0, mult 1/2].
#
#   Bajo esa cadena, log P~_r <= log(3/2)*(k~_r - 1) - 0,1438*(parte
#   libre) -> -inf geometrico (k~ crece como sqrt, la libre lineal):
#   W~_inf = Sigma d~_r P~_{r-1} converge c.s. y su ley es UN OBJETO
#   FIJO -- la mediana universal se puede simular directo.
#
#   EL TEST: si la ley de W_tau | tau en [T, 2T] del modelo forward
#   converge (T creciente) a la ley de W~_inf de la cadena revertida,
#   el mecanismo de L3 esta verificado por dos caminos sin codigo
#   comun (forward: excursion V2a de sombraexogena; reverso: el
#   h-transform de AGKV). Si no convergen, el esquema (i)-(iii) de la
#   ficha esta mal y hay que saberlo AHORA.
#
#   COMPROBACIONES (SystemExit):
#     C1  invariante de signo: W_tau < 0 en TODA excursion absorbida
#         (W es suma de terminos -1/2 * producto positivo).
#     C2  sanidad de la balota: P(tau > T) * sqrt(T) estable en T
#         (el c1/sqrt(T) del Lema 1; se imprime, falla si se sale
#         de [0,5, 2,5] -- rango generoso, es sanidad no medicion).
#     C3  la cola truncada del reverso es despreciable: P~ final
#         < 1e-9 en todas las corridas (el drift la manda a 0).
#     C4  LA CONVERGENCIA: la mediana de |W_tau| en la ventana mas
#         profunda cae a menos del 20% de la mediana de |W~_inf|
#         (y se imprime la serie entera de cuantiles por T).
#     C5  L3 A LA VISTA: con M = cuantil 75 de |W~_inf|, el exito
#         P(|W_tau| <= M | ventana) >= 0,40 en las dos ventanas mas
#         profundas (el enunciado pide >= 1/2 con el M del limite;
#         0,40 es el suelo duro del test con muestra finita).
#
#   Semillas FIJAS por fase (leccion de la semilla salada, 8a rev).
#   Todo float: aqui se mide una LEY, no se certifica una cota.

import random
import math

VENTANAS_T = [100, 400, 1600, 6400]   # T de la ventana [T, 2T]
OBJETIVO = [4000, 4000, 4000, 1500]   # muestras por ventana
TOPE_CORRIDAS = 3 * 10 ** 6           # tope de excursiones por ventana
N_REVERSO = 20000                     # corridas de la cadena revertida
PASOS_REVERSO = 6000                  # horizonte del reverso
UMBRAL_COLA = 1e-15                   # P~ bajo esto: cola despreciable
SEMILLA = 20260811

CUANTILES = [10, 25, 50, 75, 90]


def cuantil(datos, p):
    s = sorted(datos)
    i = max(0, min(len(s) - 1, int(round(p / 100.0 * (len(s) - 1)))))
    return s[i]


# ---------------------------------------------------------------------------
# FORWARD: la excursion V2a (misma dinamica que sombraexogena.py),
# siguiendo W directo: bit 0 -> W <- W/2; bit 1 -> W <- (3W - 1)/2.
# Devuelve (tau, W_tau) si absorbe antes de t_max, si no None.
# ---------------------------------------------------------------------------


def excursion_forward(azar, t_max):
    k = 2
    w = 0.0
    for t in range(1, t_max + 1):
        r = azar.getrandbits(2)
        bit = r & 1
        es_mixto = (r >> 1) & 1
        w = w / 2.0 if bit == 0 else (3.0 * w - 1.0) / 2.0
        if es_mixto:
            if bit == 1:
                k -= 1
                if k <= 1:
                    return (t, w)
            else:
                k += 1
    return None


# ---------------------------------------------------------------------------
# REVERSO: la cadena h-transformada desde la absorcion.
#   r = 1 es el paso absorbente forward (mixto, bit 1): d~ = -1/2,
#   P~ *= 3/2, k~: 1 -> 2. Despues, cada paso: compartido w.p. 1/2
#   (bit libre), mixto w.p. 1/2 con las probabilidades h(k) = k - 1.
#   Corta cuando P~ < UMBRAL_COLA (el drift negativo manda);
#   devuelve (W~, P~_final, pasos).
# ---------------------------------------------------------------------------


def corrida_reversa(azar):
    w = -0.5              # el paso de la absorcion (P~_0 = 1, bit 1)
    p = 1.5
    k = 2
    for r in range(2, PASOS_REVERSO + 1):
        if azar.getrandbits(1):          # compartido: bit libre justo
            bit = azar.getrandbits(1)
        else:                            # mixto: h-transform
            # sube w.p. k/(2(k-1)) -> bit forward 1; baja si no
            if azar.random() < k / (2.0 * (k - 1)):
                bit = 1
                k += 1
            else:
                bit = 0
                k -= 1
        if bit == 1:
            w -= 0.5 * p
            p *= 1.5
        else:
            p *= 0.5
        if p < UMBRAL_COLA:
            return (w, p, r)
    return (w, p, PASOS_REVERSO)


# ---------------------------------------------------------------------------
# FASE 1: el reverso (el objeto limite, fijo)
# ---------------------------------------------------------------------------

azar = random.Random(SEMILLA)
muestra_rev = []
p_max_final = 0.0
pasos_max = 0
for _ in range(N_REVERSO):
    w, p_fin, pasos = corrida_reversa(azar)
    muestra_rev.append(abs(w))
    p_max_final = max(p_max_final, p_fin)
    pasos_max = max(pasos_max, pasos)
if p_max_final >= 1e-9:
    raise SystemExit("C3: cola del reverso no despreciable (P~ = %g)"
                     % p_max_final)
print("COMPROBACION 3 OK: %d corridas del reverso, P~ final maximo %.1e,"
      % (N_REVERSO, p_max_final))
print("horizonte usado maximo %d de %d pasos." % (pasos_max, PASOS_REVERSO))
print()
q_rev = {p: cuantil(muestra_rev, p) for p in CUANTILES}
print("|W~_inf| del reverso (h-transform, objeto limite):")
print("  cuantiles %s = %s"
      % (CUANTILES, ["%.4f" % q_rev[p] for p in CUANTILES]))
M_UNIVERSAL = q_rev[75]
print("  M (cuantil 75) = %.4f   mediana = %.4f" % (M_UNIVERSAL, q_rev[50]))
print()

# ---------------------------------------------------------------------------
# FASE 2: el forward por ventanas, contra el limite
# ---------------------------------------------------------------------------

print("forward V2a condicionado a tau en [T, 2T]:")
print("   T     muestras  corridas   P(tau>T)*sqrt(T)   cuantiles 10/25/50/75/90 de |W_tau|   P(|W|<=M)")
resultados = {}
for T, objetivo in zip(VENTANAS_T, OBJETIVO):
    azar = random.Random(SEMILLA + T)
    muestra = []
    corridas = 0
    supera_T = 0
    while len(muestra) < objetivo and corridas < TOPE_CORRIDAS:
        corridas += 1
        res = excursion_forward(azar, 2 * T)
        if res is None:
            supera_T += 1          # censurado en 2T: paso por T seguro
            continue
        tau, w = res
        if w >= 0:
            raise SystemExit("C1: W_tau = %g >= 0 en tau = %d" % (w, tau))
        if tau > T:
            supera_T += 1
        if T <= tau <= 2 * T:
            muestra.append(abs(w))
    balota = (supera_T / float(corridas)) * math.sqrt(T)
    if not (0.5 <= balota <= 2.5):
        raise SystemExit("C2: P(tau>T)*sqrt(T) = %.3f fuera de rango" % balota)
    qs = {p: cuantil(muestra, p) for p in CUANTILES}
    exito = sum(1 for v in muestra if v <= M_UNIVERSAL) / float(len(muestra))
    resultados[T] = (qs, exito, len(muestra))
    print("  %5d  %7d  %8d      %.3f            %s   %.3f"
          % (T, len(muestra), corridas, balota,
             "/".join("%.3f" % qs[p] for p in CUANTILES), exito))
print("COMPROBACION 1 OK (signo) y 2 OK (balota) en todas las ventanas.")
print()

# ---------------------------------------------------------------------------
# COMPROBACIONES 4 y 5: la convergencia y L3 a la vista
# ---------------------------------------------------------------------------

T_max = VENTANAS_T[-1]
med_fwd = resultados[T_max][0][50]
med_rev = q_rev[50]
desvio = abs(med_fwd - med_rev) / med_rev
print("la mediana por ventana contra el limite:")
for T in VENTANAS_T:
    print("  T = %5d:  mediana fwd = %.4f   (limite %.4f, desvio %.1f%%)"
          % (T, resultados[T][0][50], med_rev,
             100 * abs(resultados[T][0][50] - med_rev) / med_rev))
if desvio > 0.20:
    raise SystemExit("C4: la mediana forward a T = %d desvia %.1f%% > 20%%"
                     % (T_max, 100 * desvio))
print("COMPROBACION 4 OK: la mediana condicionada converge al objeto")
print("limite del reverso (desvio %.1f%% en T = %d)." % (100 * desvio, T_max))
print()
for T in VENTANAS_T[-2:]:
    if resultados[T][1] < 0.40:
        raise SystemExit("C5: exito %.3f < 0,40 en T = %d"
                         % (resultados[T][1], T))
print("COMPROBACION 5 OK -- L3 A LA VISTA: con M = %.4f (cuantil 75 del"
      % M_UNIVERSAL)
print("limite), P(|W_tau| <= M | ventana) = %s en las ventanas: la"
      % ", ".join("%.3f" % resultados[T][1] for T in VENTANAS_T))
print("mediana universal EXISTE y es la del h-transform de AGKV.")
print()
print("Lectura honesta: esto verifica el MECANISMO (i)-(iii) de")
print("fichaagkv.txt seccion D por dos caminos sin codigo comun; el")
print("teorema L3 sigue pendiente de escribir (limite local de la")
print("reversion + trasvase tipo Lemma 2.5). Es medicion, no cota.")
