# liebres.py
#
# LA REDUCCION A UN CONJUNTO FINITO (09-08-2026, tarde): el ataque n.2
# de RutaTeoremas.md ("el piso por estructura... es el argumento de
# Doeblin/minorizacion sobre un conjunto pequenio -- el nombre tecnico a
# buscar"), construido. Dos piezas nuevas, propuestas para bautizo:
#
#   ⇢ TEOREMA (propuesto: LIEBRES -- basta con volver a la madriguera).
#     En la CADENA MODIFICADA (la de Leonas con el vortice rebotado a
#     (2,2); ver retorno11.py), sea C un conjunto FINITO de estados con
#     (1,1) en C. Entonces
#
#         phi = 1   <=>   Sigma_t P(X_t en C) = infinito.
#
#     DEMOSTRACION. (=>) Si phi = 1, (1,1) es recurrente (retorno11:
#     phi = 1 <=> N = # visitas a (1,1) es infinito c.s., porque cada
#     visita sobrevive con moneda 1/2 y P(no fundir) = E[2^-N]), luego
#     Sigma_t P(X_t = (1,1)) = infinito y con mas razon sobre C.
#     (<=) Si la serie diverge y C es FINITO, algun y en C tiene funcion
#     de Green G(x,y) = Sigma_t P_x(X_t = y) = infinito. Como
#     G(x,y) = P_x(T_y < inf) * G(y,y), sale G(y,y) = infinito: y es
#     RECURRENTE. Para el C concreto de este fichero, la COMPROBACION 2
#     demuestra por calculo exacto que desde TODO estado de C se
#     alcanza (1,1) con probabilidad >= eps en <= L pasos; para C
#     finito ARBITRARIO, la accesibilidad de (1,1) desde todo estado
#     es el teorema de HORMIGAS en su version cualitativa
#     (accesibilidad.py, redemostrado por la 4a revision) -- cita
#     exigida por la 5a revision: sin ella el enunciado general tenia
#     un cuantificador escondido. En particular y -> (1,1). Un estado recurrente
#     lleva a su clase y la clase de un recurrente es cerrada y
#     recurrente, luego (1,1) es recurrente; y como (0,1) y (1,1) se
#     COMUNICAN (COMPROBACION 1, los dos caminos explicitos), el
#     arranque (0,1) esta en esa clase cerrada: N = infinito c.s. y
#     E[2^-N] = 0, o sea phi = 1. QED.
#
#     LO QUE CAMBIA. El criterio de retorno11 pedia una serie sobre UN
#     estado; este pide la MISMA serie sobre cualquier ventana finita.
#     (AVISO de la 5a revision sobre la medicion: a PROF = 30 la
#     ventana C_625 contiene el 99,99% del fondo, asi que su serie es
#     la del fondo entero -- que DIVERGE bajo las dos hipotesis por
#     Golondrinas; el alfa ~0,40 es el exponente del retorno al fondo,
#     NO evidencia sobre phi. La informacion esta en si la ventana
#     FIJA pierde cuota del fondo, y eso a t = 30 esta INDECIDIDO.)
#     Y sobre todo: la minorizacion deja de necesitar el
#     piso por visita con |c| NO acotado -- que es justo donde la 4a
#     revision rompio la constante 2,5 de Hormigas (muestra tomada por
#     constante). Sobre un conjunto FINITO la constante de Doeblin es un
#     calculo exacto, y aqui esta calculado: eps >= 17887/131072.
#     Este fichero NO usa la constante fina de Hormigas para nada.
#
#     EL CONTRARRECIPROCO, que es la forma testeable: phi < 1 <=> la
#     cadena modificada es TRANSITORIA <=> abandona TODA ventana finita.
#     Y por GOLONDRINAS (oscilacion.py: el fondo k <= 1 se visita
#     infinitas veces c.s.), phi < 1 obliga a |c| -> infinito A LO LARGO
#     de esas infinitas visitas al fondo. La COMPROBACION 4 mide
#     exactamente eso.
#
#   ⇢ LEMA (CEBRAS -- el sesgo se lee en las rayas), REENUNCIADO POR LA
#     5a REVISION (acta: actarevision0908b.txt). Lo que es EXACTO:
#     (a) LA CLASIFICACION AFIN: en la sombra de ARANAS (u = c/3^k)
#     cada paso es u' = rama + delta con |delta| <= 3^-k/2, donde la
#     rama es u/2 o (3u-1)/2, y la rama EXPANSIVA (3u-1)/2 es
#     exactamente: nucleo k >= 1 con bit 1, o frontera con g PAR y
#     bit 1 (frontera con g IMPAR: los dos bits contraen; el rebote
#     (1,1)->(2,2) queda FUERA: multiplica |u| por 2/3 y viola la cota
#     en ese estado). (b) EL UMBRAL:
#
#         q1*log(3/2) + (1-q1)*log(1/2)  <  0
#         <=>  q1  <  log2 / log3  =  0,6309297...
#
#     (log2 + log(3/2) = log3: LA constante clasica, otra vez) -- que
#     es el EXPONENTE DE LYAPUNOV de los multiplicadores: la hipotesis
#     de Kesten que la perpetuidad de ARANAS necesita.
#     LO QUE LA 5a REVISION ROMPIO Y QUEDA RETIRADO: esa formula NO es
#     la deriva de log|u| de la cadena. El desplazamiento -1/2 de la
#     rama expansiva es el IFS mismo (no la perturbacion) y en el
#     fondo domina: alli |u| >= 1/3 SIEMPRE y la deriva real medida es
#     +0,02 nats/paso, no -0,13. MEDIDO, con las TRES q1 separadas
#     (correccion de la 5a): q1 global 0,4585 (foto a t = 30, sube
#     hacia 1/2), q1 historico del fondo 0,5095 (pico en t~25 y baja),
#     q1 instantaneo del fondo 0,420 y bajando. El margen al umbral es
#     de 12,1 puntos, pero SIN el puente de la deriva ese margen ya no
#     es mecanismo: la reduccion exacta que lo reemplaza es URRACAS
#     (urracas.py: el sesgo condicionado contra 0,26186, umbral
#     efectivo ~0,2446 con el error del modelo IFS medido).
#
#   ETIQUETAS HONESTAS (revisadas: 5a revision, actarevision0908b.txt).
#   LIEBRES es demostracion (con la cita de HORMIGAS de arriba). De
#   CEBRAS es exacta la clasificacion afin y el umbral COMO exponente
#   de Lyapunov de los multiplicadores; la lectura "deriva de log|u|
#   de la cadena" esta RETIRADA. Lo MEDIDO orienta y no decide, y la
#   5a revision degrado la lectura del exponente: el alfa ~0,40 de la
#   ventana grande es el exponente del retorno al fondo (divergente
#   bajo las dos hipotesis, Golondrinas), no margen sobre phi; las
#   ventanas que SI muerden (r_5, r_25) bajan sin estabilizar --
#   INDECIDIDO. Ademas hay estados (k, 0) en el espacio (inalcanzables
#   desde (0,1): invariante mod 3 demostrado por el revisor 1 -- toda
#   entrada a la torre da c = 2 mod 3 y las ramas nunca fabrican
#   c = 0 mod 3; por eso el salto de c = 0 en C0 es inocuo y 17
#   estados de C son fantasmas que solo abaratan eps).
#
#   Mapa del ATAJO, enteros exactos, SystemExit antes de concluir.

import math
from fractions import Fraction

PROF = 30                  # profundidad del barrido de la cadena modificada
TOPE_ESTADOS = 4 * 10 ** 6
K_DOEBLIN = 25             # la ventana C: k <= 1 y |c| <= K_DOEBLIN
L_DOEBLIN = 22             # pasos permitidos para tocar (1,1) desde C
VENTANAS = (1, 5, 25, 125, 625)


def transicion(k, c, bit):
    # la cadena REAL de Leonas; ('fusion',) es el vortice con bit 1
    if k == 0:
        if c % 2 == 0:
            return ('estado', 0, c // 2) if bit == 0 else ('estado', 0, 3 * c // 2)
        return ('estado', 1, (3 * c + 1) // 2) if bit == 0 \
            else ('estado', 1, (1 - 3 * c) // 2)
    if c % 2 == 0:
        return ('estado', k, c // 2) if bit == 0 \
            else ('estado', k, (3 * c + 1 - 3 ** k) // 2)
    if bit == 0:
        return ('estado', k + 1, (3 * c + 1) // 2)
    if k >= 2:
        return ('estado', k - 1, (c - 3 ** (k - 1)) // 2)
    g = (c - 1) // 2
    if g == 0:
        return ('fusion',)
    return ('estado', 0, abs(g))


def modificada(k, c, bit):
    # la misma cadena con el vortice REBOTADO: (1,1) -> (2,2) con los dos
    # bits (el bit se gasta pero no cambia el estado: por eso los bits de
    # las visitas son monedas justas independientes de la trayectoria)
    if k == 1 and c == 1:
        return (2, 2)
    t = transicion(k, c, bit)
    if t[0] == 'fusion':
        raise SystemExit("modificada: fusion fuera del vortice (%d,%d)" % (k, c))
    return (t[1], t[2])


# ---------------------------------------------------------------------------
# COMPROBACION 0: LA FUSION SOLO NACE DE (1,1) CON BIT 1, y la modificada
# coincide con la real en todo lo demas. Sin esto, ni el acoplamiento
# E[2^-N] ni la equivalencia de LIEBRES tienen sentido.
# ---------------------------------------------------------------------------

fusiones = []
distintas = 0
for k in range(0, 9):
    rango = range(1, 3001) if k == 0 else range(-3000, 3001)
    for c in rango:
        if k >= 1 and c == 0:
            continue
        for bit in (0, 1):
            t = transicion(k, c, bit)
            if t[0] == 'fusion':
                fusiones.append((k, c, bit))
                continue
            if modificada(k, c, bit) != (t[1], t[2]):
                distintas += 1

if fusiones != [(1, 1, 1)]:
    raise SystemExit("C0: la fusion nace de mas sitios que (1,1)-bit1: %s"
                     % fusiones[:5])
if distintas != 0:
    raise SystemExit("C0: la modificada difiere en %d estados que no son el "
                     "vortice" % distintas)
if modificada(1, 1, 0) != (2, 2) or modificada(1, 1, 1) != (2, 2):
    raise SystemExit("C0: el rebote del vortice no es (2,2) con los dos bits")

print("COMPROBACION 0 OK: en la rejilla k <= 8, |c| <= 3000 la fusion nace")
print("EXACTAMENTE de (1,1) con bit 1 y de ningun otro estado; la cadena")
print("modificada coincide con la real salvo ahi, y en (1,1) los dos bits")
print("van a (2,2) -- el bit se gasta sin tocar el estado, que es lo que")
print("hace que P(no fundir | trayectoria) = 2^-N con N = visitas a (1,1).")

# ---------------------------------------------------------------------------
# COMPROBACION 1: (0,1) Y (1,1) SE COMUNICAN, con la funcion real.
#   Es la pieza que mete el ARRANQUE en la clase recurrente.
# ---------------------------------------------------------------------------

e = (0, 1)
for bit in (0, 0):
    e = modificada(e[0], e[1], bit)
if e != (1, 1):
    raise SystemExit("C1 ida: %s" % (e,))
e = (1, 1)
for bit in (0, 1, 1, 0, 1):
    e = modificada(e[0], e[1], bit)
if e != (0, 1):
    raise SystemExit("C1 vuelta: %s" % (e,))

print()
print("COMPROBACION 1 OK: (0,1) -00-> (1,1) e (1,1) -rebote,1,1,0,1-> (0,1).")

# ---------------------------------------------------------------------------
# COMPROBACION 2: LA CONSTANTE DE DOEBLIN, EXACTA.
#   A_j(s) = numero de palabras de largo j desde s que TOCAN (1,1) en
#   algun momento <= j. Recursion: A_j((1,1)) = 2^j, y si no,
#   A_j(s) = A_{j-1}(s0) + A_{j-1}(s1). Los estados que se salen de la
#   ventana explorada cuentan 0: el resultado es una COTA INFERIOR
#   rigurosa. eps = min sobre C de A_L(s)/2^L.
#   Que eps > 0 es la accesibilidad de (1,1) desde TODO C -- calculada,
#   no heredada de la constante fina de Hormigas (que la 4a revision
#   dejo abierta). Aqui no hace falta: C es finito.
# ---------------------------------------------------------------------------

C = [(0, g) for g in range(1, K_DOEBLIN + 1)] + \
    [(1, c) for c in range(-K_DOEBLIN, K_DOEBLIN + 1)]

ventana = set(C)
frente = set(C)
for _ in range(L_DOEBLIN):
    nuevo = set()
    for (k, c) in frente:
        for bit in (0, 1):
            s = modificada(k, c, bit)
            if s not in ventana:
                ventana.add(s)
                nuevo.add(s)
    frente = nuevo

A = dict((s, 1 if s == (1, 1) else 0) for s in ventana)
for j in range(1, L_DOEBLIN + 1):
    B = {}
    for s in ventana:
        if s == (1, 1):
            B[s] = 2 ** j
        else:
            B[s] = sum(A.get(modificada(s[0], s[1], bit), 0) for bit in (0, 1))
    A = B

peor = min(C, key=lambda s: A[s])
eps = Fraction(A[peor], 2 ** L_DOEBLIN)
if eps <= 0:
    raise SystemExit("C2: hay un estado de C que no alcanza (1,1) en %d pasos: "
                     "%s" % (L_DOEBLIN, peor))

print()
print("COMPROBACION 2 OK: sobre C = {k <= 1, |c| <= %d} (%d estados, ventana"
      % (K_DOEBLIN, len(C)))
print("explorada %d estados), TODO estado toca (1,1) en <= %d pasos con"
      % (len(ventana), L_DOEBLIN))
print("probabilidad EXACTA >= %s = %.8f   (el peor es %s)."
      % (eps, float(eps), peor))
print("Esa es la constante de Doeblin del conjunto pequenio, calculada y no")
print("estimada: sobre un conjunto FINITO la minorizacion es aritmetica.")

# ---------------------------------------------------------------------------
# COMPROBACION 3 (CEBRAS): LA CLASIFICACION DE RAMAS Y EL UMBRAL.
#   (a) el multiplicador de |u| es 1/2 o 3/2 salvo perturbacion exacta,
#       y la rama expansiva es la que dice el lema;
#   (b) el umbral es log2/log3, por la identidad log2 + log(3/2) = log3.
# ---------------------------------------------------------------------------

def expansiva(k, c, bit):
    if k >= 1:
        return bit == 1
    return c % 2 == 0 and bit == 1


peor_pert = Fraction(0)
peor_donde = None
for k in range(1, 9):
    for c in range(-400, 401):
        if c == 0 or (k == 1 and c == 1):
            continue
        u = Fraction(c, 3 ** k)
        for bit in (0, 1):
            k2, c2 = modificada(k, c, bit)
            u2 = Fraction(c2, 3 ** k2)
            rama = u / 2 if not expansiva(k, c, bit) else (3 * u - 1) / 2
            # la frontera pliega el signo (F4/la salida de k=1): se compara
            # en modulo, que es lo unico que usa la deriva de log|u|
            d = abs(abs(u2) - abs(rama))
            if d * 3 ** k > peor_pert * 3 ** (peor_donde[0] if peor_donde else k):
                peor_pert, peor_donde = d, (k, c, bit)
            if d > Fraction(1, 2 * 3 ** k):
                raise SystemExit("C3: perturbacion %s > 3^-k/2 en k=%d c=%d bit=%d"
                                 % (d, k, c, bit))

# el umbral, con la identidad exacta detras
if abs((math.log(2) + math.log(1.5)) - math.log(3)) > 1e-12:
    raise SystemExit("C3: log2 + log(3/2) != log3")
UMBRAL = math.log(2) / math.log(3)
if abs(math.log(1.5) * UMBRAL + math.log(0.5) * (1 - UMBRAL)) > 1e-12:
    raise SystemExit("C3: el umbral no anula la deriva")

print()
print("COMPROBACION 3 OK (CEBRAS): en el nucleo k = 1..8, |c| <= 400 el paso")
print("en u es la rama que dice el lema, con perturbacion <= 3^-k/2 (peor")
print("caso relativo en %s). El umbral de la deriva es" % (peor_donde,))
print("q1* = log2/log3 = %.7f, y anula %.2e la deriva q1*log(3/2) + "
      % (UMBRAL, abs(math.log(1.5) * UMBRAL + math.log(0.5) * (1 - UMBRAL))))
print("(1-q1)*log(1/2) -- la constante clasica de Collatz, otra vez.")

# ---------------------------------------------------------------------------
# COMPROBACION 4: EL BARRIDO DE LA CADENA MODIFICADA.
#   Se mide, nivel a nivel:
#     - P(X_t = (1,1)) y P(X_t en C_K) para varias ventanas K (LIEBRES);
#     - el exponente local alfa (P ~ t^-alfa): alfa < 1 = serie divergente
#       = phi = 1;  el umbral es 1, no 1/2;
#     - r_K(t) = P(k<=1, |c|<=K) / P(k<=1): la TENSION EN EL FONDO, que es
#       lo que phi < 1 tendria que mandar a cero (por Golondrinas);
#     - q1(fondo): la frecuencia de rama expansiva en la historia de la
#       masa que esta en el fondo, contra el umbral de CEBRAS.
#   Cada estado lleva [masa, expansivos acumulados, pasos acumulados].
# ---------------------------------------------------------------------------

estados = {(0, 1): [1, 0, 0]}
hist = {}
for t in range(1, PROF + 1):
    nuevo = {}
    for (k, c), (n, se, sp) in estados.items():
        for bit in (0, 1):
            s = modificada(k, c, bit)
            e = 1 if expansiva(k, c, bit) else 0
            v = nuevo.get(s)
            if v is None:
                nuevo[s] = [n, se + e * n, sp + n]
            else:
                v[0] += n
                v[1] += se + e * n
                v[2] += sp + n
    estados = nuevo
    if len(estados) > TOPE_ESTADOS:
        print("[barrido cortado en t = %d: %d estados]" % (t, len(estados)))
        break
    tot = 2.0 ** t
    fondo = exp_f = pasos_f = 0
    porK = [0] * len(VENTANAS)
    for (k, c), (n, se, sp) in estados.items():
        if k <= 1:
            fondo += n
            exp_f += se
            pasos_f += sp
            for i, K in enumerate(VENTANAS):
                if abs(c) <= K:
                    porK[i] += n
    hist[t] = (estados.get((1, 1), [0])[0] / tot, fondo / tot,
               [p / tot for p in porK], exp_f / pasos_f if pasos_f else 0.0,
               len(estados))

ult = max(hist)
# el control (recalibrado por la 5a revision): r_625 NO puede disparar a
# PROF = 30 -- el cuantil 99,9% de |c| en el fondo es ~238, la masa no
# llega a 625 en 30 pasos ni aunque phi < 1 fuese verdad. El guardian
# con poder real es una ventana que SI muerde: r_25 (0,9952 -> 0,9237
# en t = 12..30); un colapso de verdad la hundiria.
r_final = hist[ult][2][-1] / hist[ult][1]      # r_625: informativo
r_guard = hist[ult][2][2] / hist[ult][1]       # r_25: el guardian
if r_guard < 0.5:
    raise SystemExit("C4: la tension del fondo se rompio: r_%d(%d) = %.4f"
                     % (VENTANAS[2], ult, r_guard))

print()
print("la serie de LIEBRES en la cadena modificada (umbral de divergencia:")
print("alfa < 1). alfa local con ventana 6 niveles.")
print("   t    P(X=(1,1))   alfa       P(X en C_625)   alfa      estados")
for t in range(12, ult + 1, 2):
    a11, fondo, porK, q1, nest = hist[t]
    b11 = hist[t - 6][0]
    bK = hist[t - 6][2][-1]
    al11 = -(math.log(a11) - math.log(b11)) / (math.log(t) - math.log(t - 6))
    alK = -(math.log(porK[-1]) - math.log(bK)) / (math.log(t) - math.log(t - 6))
    print("  %3d    %9.6f   %6.3f      %9.6f   %6.3f   %10d"
          % (t, a11, al11, porK[-1], alK, nest))

print()
print("la tension del fondo: r_K(t) = P(k<=1, |c|<=K) / P(k<=1).")
print("   t    P(k<=1)   " + "  ".join("r_%-4d" % K for K in VENTANAS))
for t in range(12, ult + 1, 2):
    _, fondo, porK, _, _ = hist[t]
    print("  %3d   %8.6f   " % (t, fondo) +
          "  ".join("%6.4f" % (p / fondo) for p in porK))

print()
print("CEBRAS medido: frecuencia de rama expansiva, umbral q1* = %.6f"
      % UMBRAL)
print("   t    q1(masa en el fondo)    margen al umbral")
for t in range(12, ult + 1, 2):
    q1 = hist[t][3]
    print("  %3d         %8.6f              %8.6f" % (t, q1, UMBRAL - q1))

# ---------------------------------------------------------------------------
# EL VEREDICTO, con las etiquetas de la casa.
# ---------------------------------------------------------------------------

print()
print("VEREDICTO:")
print("  DEMOSTRADO (LIEBRES): phi = 1 <=> Sigma_t P(X_t en C) = infinito")
print("  para C finito con (1,1) dentro -- la funcion de Green mas la")
print("  accesibilidad calculada en C2 mas la comunicacion de C1. El")
print("  contrarreciproco: phi < 1 <=> la cadena modificada es TRANSITORIA")
print("  y abandona toda ventana finita; con GOLONDRINAS (fondo visitado")
print("  infinitas veces c.s.) eso obliga a |c| -> infinito en el fondo.")
print("  EXACTO (CEBRAS, reenunciada por la 5a revision): el exponente de")
print("  Lyapunov de los multiplicadores es negativo si y solo si la")
print("  frecuencia de rama expansiva es < log2/log3 = %.6f --" % UMBRAL)
print("  hipotesis de Kesten para la perpetuidad de Aranas, NO la deriva")
print("  de log|u| de la cadena (en el fondo |u| >= 1/3 y la deriva real")
print("  medida es positiva: la lectura vieja queda retirada).")
print("  MEDIDO (orienta, NO decide; leido con el acta de la 5a): r_625 =")
print("  %.4f al nivel %d, o sea la ventana grande AUN NO MUERDE -- su"
      % (r_final, ult))
print("  serie es la del fondo, que diverge bajo las dos hipotesis")
print("  (Golondrinas). Las que muerden: r_5 = %.4f, r_25 = %.4f, bajando"
      % (hist[ult][2][1] / hist[ult][1], hist[ult][2][2] / hist[ult][1]))
print("  sin estabilizar: INDECIDIDO. q1 historico del fondo %.4f (pico y"
      % (hist[ult][3],))
print("  baja), a %.4f del umbral -- pero sin el puente de la deriva ese"
      % (UMBRAL - hist[ult][3]))
print("  margen no es mecanismo. La casa avisa: una serie que baja despacio")
print("  no distingue limite positivo de cero.")
print("  LO QUE QUEDA (la reduccion exacta vive en urracas.py): acotar el")
print("  sesgo condicionado a_V + a_D - a_K bajo el umbral efectivo ~0,2446")
print("  -- el h-transform del paseo critico de k sesga O(1/k), no")
print("  exponencialmente; ahi esta el ultimo paso.")
