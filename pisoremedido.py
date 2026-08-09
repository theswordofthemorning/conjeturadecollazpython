# pisoremedido.py
#
# EL PISO POR VISITA, REMEDIDO CON EL EXPONENTE HONESTO (09-08-2026;
# la remedicion que exigio la cuarta revision externa: el 2,5 de la
# cota de Hormigas era una muestra; el sup exhaustivo es ~2,73 y la
# candidata DEMOSTRABLE del peor caso es 2/log2(4/3) ~ 4,8).
#
#   Sobre la CADENA MODIFICADA (el objeto del criterio de retorno):
#
#   MEDIDA 1 -- la tasa de Hormigas con TRES exponentes: el viejo 2,5
#   (para comparar), el sup medido 2,75 y el demostrable 5 (margen
#   sobre 4,8). tasa_e(t) = E[ 2^(-e*(k + log2(1+|c|))) ]: cota
#   inferior (heuristica del largo de palabra) de P(tocar (1,1) en
#   ~e*(k+log|c|) pasos). Si el alfa local de la tasa con e = 5 sigue
#   < 1, "E[toques] diverge" SOBREVIVE al exponente honesto.
#
#   MEDIDA 2 -- la estacionaria condicionada, sondada por RENOVACION:
#   la distribucion de |c| del FLUJO DE ENTRADA al fondo (masa que
#   cruza de k >= 2 o de la frontera impar hacia k <= 1... aqui:
#   transiciones cuyo destino tiene k <= 1 y cuyo origen tiene k = 2)
#   en t = 22, 26, 30, 34. Si la ley de entrada por visita se
#   estabiliza, el piso por visita converge positivo -- es la version
#   por epocas de la MEDIDA 1 de empalme.py (que iba por fotos de
#   tiempo). El paso teorico que decidiria (convergencia a la
#   estacionaria condicionada del perturbed IFS) sigue ABIERTO; esto
#   lo sondea, no lo demuestra.
#
#   Mapa del ATAJO, enteros exactos, SystemExit antes de concluir.

import math

PROF = 34
TOPE_ESTADOS = 9 * 10 ** 6
EXPONENTES = (2.5, 2.75, 5.0)
CORTES_C = (1, 2, 4, 8, 16, 32, 64)


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


estados = {(0, 1): 1}
tasas = {e: {} for e in EXPONENTES}
entradas = {}          # t -> histograma de |c| del flujo k=2 -> k=1
for prof in range(1, PROF + 1):
    nuevo = {}
    flujo = {}
    for (k, c), n in estados.items():
        for bit in (0, 1):
            k2, c2 = transicion_mod(k, c, bit)
            nuevo[(k2, c2)] = nuevo.get((k2, c2), 0) + n
            if k == 2 and k2 == 1:
                # la entrada al fondo por descenso de torre
                for x in CORTES_C:
                    if abs(c2) <= x:
                        flujo[x] = flujo.get(x, 0) + n
                flujo['tot'] = flujo.get('tot', 0) + n
    estados = nuevo
    if len(estados) > TOPE_ESTADOS:
        raise SystemExit("tope en prof %d" % prof)
    for e in EXPONENTES:
        t = 0.0
        for (k, c), n in estados.items():
            t += n * 2.0 ** (-e * (k + math.log2(1 + abs(c))))
        tasas[e][prof] = t / 2.0 ** prof
    if prof in (22, 26, 30, 34):
        entradas[prof] = flujo

# ---------------------------------------------------------------------------
# MEDIDA 1: las tasas con los tres exponentes y sus alfas locales.
# ---------------------------------------------------------------------------

print("MEDIDA 1 -- la tasa de Hormigas por exponente (alfa local entre")
print("t-6 y t; alfa < 1 sostenido = la esperanza de toques diverge):")
print("  t     e=2.5 (viejo)  alfa   e=2.75 (sup)   alfa   e=5 (demostrable)  alfa")
for t in range(14, PROF + 1, 4):
    fila = "%3d " % t
    for e in EXPONENTES:
        v = tasas[e][t]
        alfa = -(math.log(tasas[e][t]) - math.log(tasas[e][t - 6])) \
            / (math.log(t) - math.log(t - 6))
        fila += "   %10.3e %6.3f" % (v, alfa)
    print(fila)

alfa5 = -(math.log(tasas[5.0][PROF]) - math.log(tasas[5.0][PROF - 6])) \
    / (math.log(PROF) - math.log(PROF - 6))
if alfa5 >= 1.0:
    print()
    print("AVISO: con e = 5 el alfa local llego a %.3f >= 1 -- la" % alfa5)
    print("divergencia en media NO sobrevive al exponente honesto.")
else:
    print()
    print("con e = 5 (margen sobre la demostrable 4,8) el alfa local es")
    print("%.3f < 1: 'E[toques] diverge' SOBREVIVE al exponente honesto." % alfa5)

# ---------------------------------------------------------------------------
# MEDIDA 2: la ley de entrada al fondo por epocas (renovacion).
# ---------------------------------------------------------------------------

print()
print("MEDIDA 2 -- P(|c| <= x) del FLUJO de entrada al fondo (k=2 -> k=1):")
print("   x   " + "".join("     t=%2d" % t for t in sorted(entradas)))
for x in CORTES_C:
    fila = " %3d " % x
    for t in sorted(entradas):
        tot = entradas[t].get('tot', 0)
        fila += "   %6.4f" % (entradas[t].get(x, 0) / tot if tot else 0.0)
    print(fila)
print()
print("VEREDICTO (medido, orienta): columnas casi iguales en la MEDIDA 2")
print("= la ley de entrada por visita se estabiliza y el piso por visita")
print("converge positivo (la version por epocas del deslizamiento")
print("geometrico que ya midio empalme.py). El paso que DECIDIRIA sigue")
print("siendo la convergencia a la estacionaria condicionada del")
print("perturbed IFS -- abierto; esto lo sondea con el exponente honesto.")
