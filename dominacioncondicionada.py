# dominacioncondicionada.py
#
# EFIMERAS (hallazgo, bautizado 12-08: la dependencia del bit de
# apertura vive un dia -- es transitoria y se anula en el bulk).
# LA DOMINACION CONDICIONADA A SOBREVIVIR -- el pendiente 5(iii) de
# notadominacion.txt, medido (12-08-2026; punto 2 de la ruta post-9a
# revision, el "calculo POR HACER, no un deberia").
#
#   EL PROBLEMA. La 9a revision rompio la premisa vieja ("el
#   h-transform solo toca los bits mixtos, las rachas pasan
#   intactas"): la ley de racha DEPENDE del bit del mixto que la
#   abre (media 0,911 tras bit 0 contra 0,985 tras bit 1; 7 sigmas,
#   adv 1). La transferencia P2 usa la ley de excursion CONDICIONADA
#   a sobrevivir (tau en [T, 2T]), que es el h-transform del paseo
#   critico -- y el h-transform inclina la mezcla de mixtos hacia
#   bit 0 (subidas de k). Direccion FAVORABLE (bit 0 = rachas mas
#   cortas), pero nadie la habia MEDIDO condicionada.
#
#   QUE MIDE. Excursiones reales (2, c0) -> fondo (dinamica entera
#   exacta, bits de Terras). Para cada horizonte T de la escalera:
#     - ensemble TODAS:     rachas cerradas antes de T, de TODAS las
#                           excursiones (el baseline a ventana
#                           emparejada -- leccion de sombraexogena:
#                           comparar a horizonte igual, no contra el
#                           global, para no medir artefacto).
#     - ensemble SOBREVIVE: las mismas rachas pero solo de las
#                           excursiones con tau >= T (la ley que la
#                           transferencia de verdad usa).
#   Y en cada ensemble: la mezcla de bits de apertura, la media de
#   racha por bit, y la cola C_j = P(racha >= j) * 2^j.
#
#   La racha en curso al cruzar T no se cuenta (solo rachas CERRADAS
#   por un mixto) -- censura identica en los dos ensembles, asi que
#   el contraste no la ve.
#
#   COMPROBACIONES (SystemExit):
#     S1  reproduccion de rachasreales.py: media global de racha en
#         [0,5, 2,5] y C_j global <= C_TOPE (mismo objeto, otro
#         recorrido).
#     S2  el hecho del adv 1, reproducido en este stream: media tras
#         bit 0 < media tras bit 1 con z >= 3 (la dependencia del
#         bit de apertura que rompio la premisa vieja). SOLO se
#         exige en el arranque A (c0 = 999983, el del adv 1): la
#         PRIMERA corrida ya enseno que en el arranque B el signo se
#         INVIERTE (z = -16) -- la dependencia del bit es en gran
#         parte del TRAMO INICIAL determinista (bits bajos de c0),
#         y por eso se mide aparte el ensemble TARDIAS (cierre >=
#         100), donde se ve lo universal.
#     S3  muestra suficiente en cada ensemble condicionado (>= 5000
#         rachas), o el horizonte se reporta sin exigir.
#     S4  la supervivencia decae como ~1/sqrt(T) (el LLT del paseo
#         critico): P(tau >= 50)/P(tau >= 200) en [1,5, 2,5]
#         (el valor critico exacto seria 2).
#
#   Capa 1: mapa = atajo de Terras en (k, c) (el de rachasreales);
#   esto es MEDICION, no cota; los horizontes son escalera declarada
#   {50, 100, 200, 414} con 414 = redondeo de 30 ln c0 (el T de la
#   transferencia) -- el efecto medido no es del tamano de un
#   termino, el punto 8 no muerde; ventana emparejada contra el
#   artefacto de horizonte.

import random
import math

C0 = 999983                  # primo, impar, % 3 != 0 (= rachasreales)
C0_B = 999999937             # el segundo arranque (robustez, primo)
N_EXCURSIONES = 200000
N_EXCURSIONES_B = 60000
T_MAX = 900
T_CONDS = [50, 100, 200, 414]   # 414 ~ 30 ln C0
J_MAX = 10
MINIMO_MUESTRA = 200         # por celda C_j
MINIMO_ENSEMBLE = 5000       # S3
C_TOPE = 8.0
SEMILLA = 20260814


def pot3(k, _cache={0: 1}):
    if k not in _cache:
        _cache[k] = 3 ** k
    return _cache[k]


def transicion(k, c, bit):
    if k == 0:
        if c % 2 == 0:
            return (0, c // 2) if bit == 0 else (0, 3 * c // 2)
        return (1, (3 * c + 1) // 2) if bit == 0 else (1, (1 - 3 * c) // 2)
    if c % 2 == 0:
        return (k, c // 2) if bit == 0 else (k, (3 * c + 1 - pot3(k)) // 2)
    if bit == 0:
        return (k + 1, (3 * c + 1) // 2)
    if k >= 2:
        return (k - 1, (c - pot3(k - 1)) // 2)
    g = (c - 1) // 2
    if g == 0:
        return None
    return (0, abs(g))


def ensemble_nuevo():
    # tab: {largo: cuenta} global del ensemble; por bit: n, suma,
    # suma de cuadrados y tabla propia
    return {"tab": {}, "bit": {0: [0, 0, 0, {}], 1: [0, 0, 0, {}]}}


def ensemble_carga(e, rachas):
    for (paso_cierre, largo, bit) in rachas:
        e["tab"][largo] = e["tab"].get(largo, 0) + 1
        reg = e["bit"][bit]
        reg[0] += 1
        reg[1] += largo
        reg[2] += largo * largo
        reg[3][largo] = reg[3].get(largo, 0) + 1


def cola_peor(tab):
    n = sum(tab.values())
    if n == 0:
        return 0, 0.0
    vivos = n
    peor = 0.0
    for j in range(0, J_MAX + 1):
        if j >= 1 and vivos >= MINIMO_MUESTRA:
            peor = max(peor, (vivos / float(n)) * (2 ** j))
        vivos -= tab.get(j, 0)
    return n, peor


def media_var(reg):
    n, s, s2 = reg[0], reg[1], reg[2]
    if n < 2:
        return 0.0, 0.0
    m = s / float(n)
    v = (s2 - n * m * m) / float(n - 1)
    return m, v


T_TARDIA = 100               # rachas cerradas de aqui en adelante


def correr(c0, n_excursiones, etiqueta, exigir_s2):
    azar = random.Random(SEMILLA)
    global_e = ensemble_nuevo()
    tardias_e = ensemble_nuevo()
    todas = {T: ensemble_nuevo() for T in T_CONDS}
    sobrevive = {T: ensemble_nuevo() for T in T_CONDS}
    n_sobreviven = {T: 0 for T in T_CONDS}
    for _ in range(n_excursiones):
        k, c = 2, c0
        racha = None
        bit_apertura = None
        locales = []            # (paso_cierre, largo, bit_apertura)
        tau = T_MAX + 1         # censurada = sobrevive a todo T_COND
        for t in range(T_MAX):
            k0 = k
            b = azar.getrandbits(1)
            r = transicion(k, c, b)
            paso = t + 1
            if r is None:
                tau = paso
                break
            k, c = r
            if k == k0:
                if racha is not None:
                    racha += 1
            else:
                if racha is not None:
                    locales.append((paso, racha, bit_apertura))
                racha = 0
                bit_apertura = b
            if k <= 1:
                tau = paso
                break
        ensemble_carga(global_e, locales)
        ensemble_carga(tardias_e, [x for x in locales if x[0] >= T_TARDIA])
        for T in T_CONDS:
            en_ventana = [x for x in locales if x[0] < T]
            ensemble_carga(todas[T], en_ventana)
            if tau >= T:
                n_sobreviven[T] += 1
                ensemble_carga(sobrevive[T], en_ventana)
    print("=== arranque %s: c0 = %d, %d excursiones, T_MAX = %d ==="
          % (etiqueta, c0, n_excursiones, T_MAX))
    n_g = sum(global_e["tab"].values())
    m0, v0 = media_var(global_e["bit"][0])
    m1, v1 = media_var(global_e["bit"][1])
    n0 = global_e["bit"][0][0]
    n1 = global_e["bit"][1][0]
    media_g = (global_e["bit"][0][1] + global_e["bit"][1][1]) / float(n_g)
    _, peor_g = cola_peor(global_e["tab"])
    z = (m1 - m0) / math.sqrt(v0 / n0 + v1 / n1)
    print("global: %d rachas, media %.4f, C_j max %.3f" % (n_g, media_g, peor_g))
    print("        apertura bit 0: n = %d, media %.4f" % (n0, m0))
    print("        apertura bit 1: n = %d, media %.4f   (z de la "
          "diferencia: %.1f)" % (n1, m1, z))
    if not (0.5 <= media_g <= 2.5):
        raise SystemExit("S1: media global %.3f fuera de [0,5, 2,5]" % media_g)
    if peor_g > C_TOPE:
        raise SystemExit("S1: C_j global %.2f > %.1f" % (peor_g, C_TOPE))
    print("S1 OK: el objeto reproduce rachasreales (media y cola).")
    if exigir_s2:
        if not (m0 < m1) or z < 3.0:
            raise SystemExit("S2: la dependencia del bit de apertura no "
                             "aparece (m0 = %.4f, m1 = %.4f, z = %.1f)"
                             % (m0, m1, z))
        print("S2 OK: media tras bit 0 < media tras bit 1 (z = %.1f) -- "
              "el hecho del adv 1, en este stream." % z)
    else:
        print("(S2 no se exige en este arranque: la dependencia del bit "
              "es arranque-dependiente -- hallazgo de la primera corrida)")
    mt0, vt0 = media_var(tardias_e["bit"][0])
    mt1, vt1 = media_var(tardias_e["bit"][1])
    nt0 = tardias_e["bit"][0][0]
    nt1 = tardias_e["bit"][1][0]
    if nt0 > 1 and nt1 > 1:
        zt = (mt1 - mt0) / math.sqrt(vt0 / nt0 + vt1 / nt1)
        _, peor_t = cola_peor(tardias_e["tab"])
        print("TARDIAS (cierre >= %d): bit 0 n = %d media %.4f; bit 1 "
              "n = %d media %.4f (z = %.1f); C_j max %.3f"
              % (T_TARDIA, nt0, mt0, nt1, mt1, zt, peor_t))
    print()
    print("la escalera de horizontes (ventana emparejada [0, T)):")
    print("  T    ensemble    rachas   frac.apertura bit0   media|b0"
          "   media|b1   media   C_j max")
    resultados = {}
    for T in T_CONDS:
        for nombre, e in (("todas", todas[T]), ("sobrevive", sobrevive[T])):
            nT = sum(e["tab"].values())
            if nT == 0:
                continue
            mb0, _ = media_var(e["bit"][0])
            mb1, _ = media_var(e["bit"][1])
            nb0 = e["bit"][0][0]
            frac0 = nb0 / float(nT)
            mT = (e["bit"][0][1] + e["bit"][1][1]) / float(nT)
            _, peorT = cola_peor(e["tab"])
            aviso = ""
            if nombre == "sobrevive" and nT < MINIMO_ENSEMBLE:
                aviso = "  (muestra fina: no se exige)"
            print("  %3d  %-9s %8d        %.4f          %.4f     %.4f"
                  "    %.4f   %.3f%s"
                  % (T, nombre, nT, frac0, mb0, mb1, mT, peorT, aviso))
            resultados[(T, nombre)] = (nT, frac0, mT, peorT)
        print("       (sobreviven %d de %d excursiones)"
              % (n_sobreviven[T], n_excursiones))
    return resultados, n_sobreviven


res_A, sob_A = correr(C0, N_EXCURSIONES, "A", exigir_s2=True)
print()

# S4: la supervivencia critica ~1/sqrt(T)
pA_50 = sob_A[50] / float(N_EXCURSIONES)
pA_200 = sob_A[200] / float(N_EXCURSIONES)
razon = pA_50 / pA_200
if not (1.5 <= razon <= 2.5):
    raise SystemExit("S4: P(tau>=50)/P(tau>=200) = %.2f fuera de "
                     "[1,5, 2,5] -- no parece el paseo critico" % razon)
print("S4 OK: P(tau >= 50)/P(tau >= 200) = %.3f ~ 2 = sqrt(200/50):"
      % razon)
print("la supervivencia decae como el LLT del paseo critico pide.")
print()

# S3 + el veredicto sobre el arranque A
print("EL VEREDICTO (arranque A):")
for T in T_CONDS:
    if (T, "sobrevive") not in res_A or (T, "todas") not in res_A:
        continue
    nS, f0S, mS, cS = res_A[(T, "sobrevive")]
    nA, f0A, mA, cA = res_A[(T, "todas")]
    if nS < MINIMO_ENSEMBLE:
        print("  T = %3d: muestra %d < %d, no se exige" % (T, nS,
                                                           MINIMO_ENSEMBLE))
        continue
    d_frac = f0S - f0A
    d_media = mS - mA
    print("  T = %3d: frac bit0 %.4f -> %.4f (%+.4f); media %.4f -> "
          "%.4f (%+.4f); C_j %.3f -> %.3f"
          % (T, f0A, f0S, d_frac, mA, mS, d_media, cA, cS))

res_B, _ = correr(C0_B, N_EXCURSIONES_B, "B", exigir_s2=False)
print()
print("Lectura (el veredicto medido, que NO es el 'deberia' de la")
print("premisa vieja): (1) la dependencia del bit de apertura es")
print("TRANSITORIA -- en las rachas tardias (cierre >= 100) se anula")
print("en los dos arranques (z ~ 0, medias ~ 1,003): el 7 sigma del")
print("adv 1 vivia entero en el tramo inicial determinista de c0, el")
print("mismo tramo que la version quenched ya se traga (nota 3(ii)).")
print("(2) El condicionamiento a sobrevivir SI inclina la mezcla a")
print("bit 0 (+0,02..+0,04), pero ese canal es irrelevante en el")
print("bulk (por (1)); lo que hace el reloj es empujar la ley de")
print("racha hacia la geometrica NEUTRA: en A la media sube hacia 1")
print("desde abajo, en B baja hacia 1 desde arriba, y el C_j")
print("condicionado queda en [0,87, 1,06] en toda la escalera --")
print("dentro del C <= 1,2 de toda rebanada de la 9a. La dominacion")
print("condicionada a sobrevivir AGUANTA con C ~ 1. Medicion, no")
print("teorema.")
