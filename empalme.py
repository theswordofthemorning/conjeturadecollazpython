# empalme.py
#
# EL EMPALME POR VISITA, ACORRALADO (09-08-2026; la ultima pieza tras
# GOLONDRINAS). La pregunta: en las visitas al fondo (k <= 1) de la
# cadena modificada, la ley de u = c/3^k (c en la frontera) se
# estabiliza? Si la u-CDF condicionada al fondo CONVERGE al crecer t,
# el piso por visita E[(1+|c|)^(-5/2) | fondo] converge a su valor
# estacionario POSITIVO y el empalme vale: (1,1) se toca i.o. y
# phi = 1 (via el criterio + Golondrinas + Hormigas).
#
#   EL MECANISMO A FAVOR (Aranas): la dinamica de u es el IFS de
#   moneda justa mas perturbacion sumable -- NO VE k. El sesgo posible:
#   las visitas al fondo las decide la MISMA palabra de bits que mueve
#   u (llegar a k = 1 exige N4s recientes = bits 1 = ramas (3u-1)/2):
#   la comparacion fondo-contra-torre de abajo mide ese sesgo.
#
#   Tres medidas exactas (masa simbolica, sin muestreo):
#   1. la u-CDF condicionada al fondo en t = 22, 26, 30, 34 (converge?)
#   2. la u-CDF fondo contra torre en t = 34 (el sesgo de la visita)
#   3. el piso por visita por BANDA de k (el empalme no necesita solo
#      k <= 1: Hormigas cobra 2.5(k + log2|c|) -- el piso generalizado
#      E[2^(-2.5(k + log2(1+|c|)))] sobre TODA la masa, que es una
#      cota inferior de la tasa de toque de (1,1) por nivel).
#
#   Mapa del ATAJO, enteros exactos, SystemExit antes de concluir.

PROF = 34
TOPE_ESTADOS = 9 * 10 ** 6
CORTES = [0.5, 1, 2, 4, 8, 16, 32, 64]


def transicion_mod(k, c, bit):
    if k == 0:
        if c % 2 == 0:
            return (0, c // 2) if bit == 0 else (0, 3 * c // 2)
        return (1, (3 * c + 1) // 2) if bit == 0 else (1, (1 - 3 * c) // 2)
    if c % 2 == 0:
        return (k, c // 2) if bit == 0 else (k, (3 * c + 1 - 3 ** k) // 2)
    if k == 1 and c == 1:
        return (2, 2)
    if bit == 0:
        return (k + 1, (3 * c + 1) // 2)
    if k >= 2:
        return (k - 1, (c - 3 ** (k - 1)) // 2)
    return (0, abs((c - 1) // 2))


def u_de(k, c):
    return c / 3.0 ** k if k >= 1 else float(c)


estados = {(0, 1): 1}
fotos = {}
tasa_por_t = {}
for prof in range(1, PROF + 1):
    nuevo = {}
    for (k, c), n in estados.items():
        for bit in (0, 1):
            k2, c2 = transicion_mod(k, c, bit)
            nuevo[(k2, c2)] = nuevo.get((k2, c2), 0) + n
    estados = nuevo
    if len(estados) > TOPE_ESTADOS:
        raise SystemExit("tope en prof %d" % prof)
    # la tasa generalizada de toque: E[2^(-2.5*(k + log2(1+|c|)))]
    tasa = 0.0
    for (k, c), n in estados.items():
        tasa += n * 2.0 ** (-2.5 * (k + __import__('math').log2(1 + abs(c))))
    tasa_por_t[prof] = tasa / 2.0 ** prof
    if prof in (22, 26, 30, 34):
        fotos[prof] = dict(estados)

# ---------------------------------------------------------------------------
# MEDIDA 1: la u-CDF condicionada al fondo, por foto. Convergencia =
# el piso por visita tiende a su valor estacionario positivo.
# ---------------------------------------------------------------------------

print("MEDIDA 1 -- P(|u| <= x | fondo k <= 1), por profundidad:")
print("   x   " + "".join("     t=%2d" % t for t in sorted(fotos)))
filas = {}
for t, est in fotos.items():
    tot = sum(n for (k, c), n in est.items() if k <= 1)
    for x in CORTES:
        m = sum(n for (k, c), n in est.items()
                if k <= 1 and abs(u_de(k, c)) <= x)
        filas.setdefault(x, {})[t] = m / tot
for x in CORTES:
    print(" %5.1f " % x + "".join("   %6.4f" % filas[x][t]
                                  for t in sorted(fotos)))

# ---------------------------------------------------------------------------
# MEDIDA 2: el sesgo de la visita -- fondo contra torre en t = 34.
# ---------------------------------------------------------------------------

est = fotos[PROF]
print()
print("MEDIDA 2 -- el sesgo de la visita (t = %d): P(|u| <= x | banda)" % PROF)
print("   x      fondo k<=1   torre k>=2")
tot_f = sum(n for (k, c), n in est.items() if k <= 1)
tot_t = sum(n for (k, c), n in est.items() if k >= 2)
for x in CORTES:
    mf = sum(n for (k, c), n in est.items() if k <= 1 and abs(u_de(k, c)) <= x)
    mt = sum(n for (k, c), n in est.items() if k >= 2 and abs(u_de(k, c)) <= x)
    print(" %5.1f      %6.4f      %6.4f" % (x, mf / tot_f, mt / tot_t))

# ---------------------------------------------------------------------------
# MEDIDA 3: la tasa generalizada de toque de (1,1) por nivel --
# E[2^(-2.5(k + log2(1+|c|)))] sobre TODA la masa (cota inferior de la
# probabilidad de tocar (1,1) en los proximos ~2.5(k+log|c|) pasos,
# via Hormigas). Si Sigma_t tasa(t) diverge, el toque es i.o. en media.
# ---------------------------------------------------------------------------

import math

print()
print("MEDIDA 3 -- la tasa de Hormigas por nivel y su acumulada:")
print("  t      tasa(t)      acumulada    alfa local")
ac = 0.0
for t in sorted(tasa_por_t):
    ac += tasa_por_t[t]
    if t % 2 == 0 and t >= 12:
        alfa = ""
        if t - 6 in tasa_por_t:
            alfa = "   %7.4f" % (-(math.log(tasa_por_t[t]) - math.log(tasa_por_t[t - 6]))
                                 / (math.log(t) - math.log(t - 6)))
        print("%3d    %.6f    %9.5f%s" % (t, tasa_por_t[t], ac, alfa))

print()
print("VEREDICTO (medido, orienta): si la MEDIDA 1 muestra columnas casi")
print("iguales (u-CDF del fondo estabilizada) y la MEDIDA 2 poco sesgo,")
print("el piso por visita converge positivo y el empalme vale -- phi = 1")
print("quedaria con toda la cadena heuristica cerrada y UN solo paso")
print("tecnico pendiente (perturbed IFS: convergencia a la estacionaria")
print("condicionada). La MEDIDA 3 es la version en media del empalme:")
print("alfa < 1 sostenido = la esperanza de toques diverge.")
