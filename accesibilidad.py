# accesibilidad.py
#
# EL TEOREMA DE HORMIGAS -- LA ACCESIBILIDAD (bautizado por el
# usuario el 09-08-2026: siempre hay camino a casa): desde TODO
# estado (k, c) de la cadena hay una palabra finita que fusiona.
# Es la pieza (A) de la reduccion del lema de ABEJAS
# (minorizacion.py).
#
#   EL CONSTRUCTOR (la politica de bits, una regla por caso):
#
#     nucleo k >= 2:  c par, c != 0 -> bit 0 (N1: halvar c)
#                     c = 0         -> bit 1 (N2: sale del cero)
#                     c impar       -> bit 1 (N4: DESCIENDE la torre)
#     nucleo k = 1:   c par, c != 0 -> bit 0;  c = 0 -> bit 1
#                     c impar       -> bit 1 (fusiona si c = 1;
#                                      si no, sale a la frontera)
#     frontera k = 0: g par         -> bit 0 (F1: halvar g)
#                     g = 1         -> bit 0 (la ventana de Perras:
#                                      (0,1)->(1,2)->(1,1)->FUSION)
#                     g impar > 1   -> bit 1 (F4: el vuelco)
#
#   LA DEMOSTRACION DE TERMINACION, entera (es la induccion que
#   convierte la BFS de minorizacion.py en teorema):
#
#   FASE 1 (torre): cada N4 baja k en 1; entre dos N4 solo hay
#   halvings de c (finitos: v_2(c)) y a lo sumo una salida del cero
#   (N2 desde c = 0 da c' = (1-3^k)/2 != 0, y un halving nunca
#   produce 0 desde c != 0; N4 produce c' = 0 solo desde c = 3^(k-1),
#   que aterriza en (k-1, 0): k ya bajo). Luego k llega a 1.
#
#   FASE 2 (nucleo bajo): halvings finitos hasta c impar; c = 1
#   fusiona; c impar != 1 sale a (0, |(c-1)/2|).
#
#   FASE 3 (frontera), el descenso del gap: para g impar > 1, el
#   vuelco F4 da (1, c) con c = (1-3g)/2, |c| = (3g-1)/2. Tras
#   j = v_2(c) halvings queda c' = -(3g-1)/2^(1+j) impar, y la
#   salida da el gap nuevo g' = ((3g-1)/2^(1+j) + 1)/2. Entonces:
#     j = 0:   g' = (3g+1)/4        < g  <=>  g > 1     (estricto)
#     j >= 1:  g' <= (3g-1)/8 + 1/2 < g  <=>  5g > 3    (siempre)
#   O sea EL GAP DECRECE ESTRICTAMENTE en cada viaje de ida y vuelta,
#   hasta g = 1; los pares intermedios solo halvan (F1). Y en g = 1,
#   la ventana de Perras fusiona en 3 pasos exactos. QED.
#
#   (El unico lazo que la politica esquiva es el de Gatas:
#   (0,1) -1-> (1,-1) -1-> (0,1) -- por eso g = 1 va con bit 0.)
#
#   Con esto, la pieza (iii)/(A) del lema de bloques de
#   minorizacion.py vale para TODA rejilla finita, con
#   T(G) <= max de la palabra del constructor sobre G. Este fichero
#   verifica el constructor (1) contra la rejilla entera de la BFS,
#   (2) en estados aleatorios ENORMES (hasta 10^30), y (3) que el
#   largo crece como O(k + log|c|), que es lo que la minorizacion
#   necesita para degradarse solo polinomialmente.
#
#   Mapa del ATAJO, enteros exactos, SystemExit antes de concluir.

import math
import random

K_REJILLA = 8
C_REJILLA = 2000
G_REJILLA = 2000

N_ALEATORIOS = 2000
K_MAX_ALEA = 40
DIGITOS_ALEA = 30          # |c| hasta 10^30
TOPE_PASOS = 100000


def transicion(k, c, bit):
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


def bit_politica(k, c):
    if k == 0:
        if c == 1:
            return 0            # la ventana de Perras, no el lazo de Gatas
        return 0 if c % 2 == 0 else 1
    if c % 2 == 0:
        return 1 if c == 0 else 0
    return 1


def palabra_a_fusion(k, c):
    # devuelve el largo de la palabra del constructor, o -1 si excede
    pasos = 0
    while pasos < TOPE_PASOS:
        b = bit_politica(k, c)
        t = transicion(k, c, b)
        pasos += 1
        if t[0] == 'fusion':
            return pasos
        k, c = t[1], t[2]
    return -1


# ---------------------------------------------------------------------------
# COMPROBACION 1: LA REJILLA ENTERA, por el constructor (sin BFS).
# ---------------------------------------------------------------------------

peor = 0
peor_estado = None
for k in range(1, K_REJILLA + 1):
    for c in range(-C_REJILLA, C_REJILLA + 1):
        n = palabra_a_fusion(k, c)
        if n < 0:
            raise SystemExit("C1: el constructor no fusiona en (%d, %d)" % (k, c))
        if n > peor:
            peor, peor_estado = n, (k, c)
for g in range(1, G_REJILLA + 1):
    n = palabra_a_fusion(0, g)
    if n < 0:
        raise SystemExit("C1: el constructor no fusiona en (0, %d)" % g)
    if n > peor:
        peor, peor_estado = n, (0, g)

print("COMPROBACION 1 OK: el constructor fusiona en TODA la rejilla")
print("(k <= %d, |c| <= %d; g <= %d). Palabra mas larga: %d pasos, en %s."
      % (K_REJILLA, C_REJILLA, G_REJILLA, peor, peor_estado))
print("(La BFS de minorizacion.py da T = 23 optimo; el constructor es mas")
print("largo pero DEMOSTRADO para todo estado: es la cota del teorema.)")

# ---------------------------------------------------------------------------
# COMPROBACION 2: ESTADOS ALEATORIOS ENORMES -- el rango donde ninguna
# BFS llega. Semilla fija para reproducibilidad.
# ---------------------------------------------------------------------------

random.seed(20260809)
peor_a = 0
peor_cota = 0.0
for _ in range(N_ALEATORIOS):
    k = random.randint(0, K_MAX_ALEA)
    magnitud = random.randint(1, 10 ** random.randint(1, DIGITOS_ALEA))
    if k == 0:
        c = magnitud
    else:
        c = magnitud * random.choice((1, -1))
    n = palabra_a_fusion(k, c)
    if n < 0:
        raise SystemExit("C2: el constructor no fusiona en (%d, %d)" % (k, c))
    cota = n / (k + math.log(abs(c) + 2, 2) + 1)
    if n > peor_a:
        peor_a = n
    if cota > peor_cota:
        peor_cota = cota

print()
print("COMPROBACION 2 OK: %d estados aleatorios con k <= %d y |c| hasta"
      % (N_ALEATORIOS, K_MAX_ALEA))
print("10^%d fusionan todos. Palabra mas larga: %d pasos." % (DIGITOS_ALEA, peor_a))

# ---------------------------------------------------------------------------
# COMPROBACION 3: EL LARGO ES O(k + log2|c|).
#   El cociente largo / (k + log2|c| + 1) tiene que estar acotado --
#   la fase 3 hace ~log_{4/3} viajes con ~2-3 pasos cada uno, o sea
#   la constante ronda 5-8. Se exige < 12 con margen.
# ---------------------------------------------------------------------------

if peor_cota >= 12:
    raise SystemExit("C3: el largo crecio mas que 12*(k + log2|c|): %.2f"
                     % peor_cota)
print()
print("COMPROBACION 3 OK: largo <= %.2f * (k + log2|c| + 1) en todo lo"
      % peor_cota)
print("probado: el constructor es O(k + log|c|), como pide la")
print("minorizacion (la cota 2^-T se degrada solo polinomialmente).")

print()
print("VEREDICTO -- HORMIGAS: la pieza (A) de la reduccion es TEOREMA: la politica")
print("de bits fusiona desde todo estado, con la demostracion de")
print("terminacion escrita en el encabezado (torre desciende, gap")
print("decrece estricto g -> ~3g/4 por viaje, ventana de Perras cierra)")
print("y verificacion exhaustiva en rejilla + aleatoria a 10^30.")
print("Con el LEMA DE BLOQUES de minorizacion.py, phi = 1 queda")
print("reducido a UNA desigualdad: M_G(t) no sumable (p.ej. >= c/t).")
