# oscilacion.py
#
# EL TEOREMA DE GOLONDRINAS -- LAS VISITAS AL FONDO NO SE ACABAN
# (09-08-2026; bautizado de la lista del usuario: las golondrinas
# siempre vuelven). Sobre la CADENA MODIFICADA (Leonas con el vortice
# rebotado; ver lamperti.py):
#
#   TEOREMA. La cadena modificada visita la banda del fondo (k <= 1)
#   infinitas veces, casi seguramente, desde todo estado inicial.
#
#   DEMOSTRACION (dos piezas, ambas con sus comprobaciones abajo):
#
#   PIEZA 1 -- EL LEMA DEL DESCENSO DE v2 (L2: hay infinitos mixtos).
#   Entre dos mixtos, k esta CONGELADO. Sea A = v2(3^k - 1) (finito:
#   1 si k impar, 2 + v2(k) si k par). Para c par en el nucleo:
#     (a) si v2(c) > A: bit 0 da v2 - 1 y bit 1 (N2) da EXACTO A - 1
#         (v2(3c) > A = v2(1-3^k) fija la suma en A; entre 2, A-1).
#         Los dos bits BAJAN. (c = 0 cuenta como v2 = inf: igual.)
#     (b) si v2(c) < A: los DOS bits dan exacto v2 - 1: descenso
#         DETERMINISTA hasta c impar = mixto.
#     (c) la unica subida posible es bit 1 exactamente en v2 = A.
#   En la frontera (g par): F1 y F2 restan 1 a v2(g) los dos --
#   determinista puro, mixto en v2(g) pasos.
#   ⇢ CORRECCION (REVISION EXTERNA, 09-08-2026): la frase original
#   "toda ventana de A+1 ceros fuerza un mixto" era FALSA al pie de la
#   letra (contraejemplos: c = 0, donde los ceros dejan 0 en 0; y
#   v2(c) > 2A+1). LA PRUEBA CORREGIDA usa la palabra DEPENDIENTE DEL
#   ESTADO, de largo <= A: si v2(c) > A o c = 0, el bit 1 (N2)
#   aterriza EXACTO en v2 = A - 1 (verificado en C1a) y siguen <= A-1
#   ceros; si v2(c) <= A, bastan v2 ceros. En cada epoca de largo A la
#   probabilidad condicional de mixto es >= 2^-A, y Borel-Cantelli
#   condicional (Levy) da infinitos mixtos c.s.  QED L2 (corregido).
#
#   PIEZA 2 -- LA OSCILACION (la tabla de derivas de lamperti.py C1,
#   exacta): k_t = M_t + A_t con M martingala de incrementos acotados
#   y A_t = numero de visitas al borde (frontera impar, vortice
#   rebotado) antes de t -- creciente, y SOLO crece en el fondo.
#   ⇢ CORRECCION (REVISION EXTERNA, 09-08-2026): "por L2 hay infinitos
#   incrementos +-1 de M" no se seguia directo -- los mixtos de BORDE
#   (frontera impar, vortice) alimentan A, no M. EL CASO PARTIDO
#   cierra: por L2 hay infinitos mixtos; si infinitos son de NUCLEO,
#   M tiene infinitos incrementos +-1, no converge, liminf M = -inf
#   (oscilacion de martingalas de incrementos acotados) y k >= 0
#   fuerza A -> inf = infinitas visitas al borde; si infinitos son de
#   BORDE, las visitas al fondo son directas. Ambas ramas dan el
#   teorema.  QED (corregido).
#
#   LO QUE ESTO REDUCE: con phi = 1 <=> (1,1) recurrente (criterio del
#   09-08), queda UNA pieza: el EMPALME POR VISITA -- de las infinitas
#   visitas al fondo, tocar (1,1) infinitas veces. Hormigas da
#   P >= ~|c|^(-2.5) por visita; falta que |c| en las visitas no se
#   disperse del todo (la serie de abajo lo mide).
#
#   Mapa del ATAJO, enteros exactos, SystemExit antes de concluir.

PROF = 34
TOPE_ESTADOS = 9 * 10 ** 6


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


def v2(c):
    if c == 0:
        return None          # v2 = infinito
    j = 0
    while c % 2 == 0:
        c //= 2
        j += 1
    return j


# ---------------------------------------------------------------------------
# COMPROBACION 1: EL LEMA DEL DESCENSO, por enumeracion exacta.
#   Para k = 1..10 y todo c par en una ventana grande, verificar (a),
#   (b), (c) y el valor de A = v2(3^k - 1).
# ---------------------------------------------------------------------------

probadas = 0
for k in range(1, 11):
    A = v2(3 ** k - 1)
    esperado = 1 if k % 2 == 1 else 2 + v2(k)
    if A != esperado:
        raise SystemExit("C1: A(%d) = %d, esperado %d" % (k, A, esperado))
    for c in range(-6000, 6001, 2):
        w = v2(c)                       # None = infinito (c = 0)
        _, c0 = transicion_mod(k, c, 0)
        _, c1 = transicion_mod(k, c, 1)
        w0, w1 = v2(c0), v2(c1)
        if w is None or w > A:          # caso (a): ambos bajan
            if c != 0 and w0 != w - 1:
                raise SystemExit("C1a bit0: k=%d c=%d" % (k, c))
            if w1 != A - 1:
                raise SystemExit("C1a bit1: k=%d c=%d w1=%s != A-1=%d"
                                 % (k, c, w1, A - 1))
        elif w < A:                     # caso (b): descenso determinista
            if w0 != w - 1 or w1 != w - 1:
                raise SystemExit("C1b: k=%d c=%d w=%d -> %s,%s"
                                 % (k, c, w, w0, w1))
        else:                           # w == A: bit0 baja; bit1 puede subir
            if w0 != A - 1:
                raise SystemExit("C1c bit0: k=%d c=%d" % (k, c))
            if w1 is not None and w1 < A:
                raise SystemExit("C1c bit1 bajo A: k=%d c=%d w1=%d" % (k, c, w1))
        probadas += 1

print("COMPROBACION 1 OK -- el lema del descenso de v2, exacto en %d"
      % probadas)
print("instancias (k = 1..10, |c| <= 6000 par): con v2 != A los DOS bits")
print("bajan v2 (y bajo A el descenso es determinista); la unica subida")
print("es bit 1 exactamente en v2 = A = v2(3^k - 1). L2 demostrado con")
print("la palabra DEPENDIENTE DEL ESTADO de largo <= A (ver la")
print("correccion de la revision externa en el encabezado).")

# ---------------------------------------------------------------------------
# COMPROBACION 2: LA FRONTERA ES DETERMINISTA: F1 y F2 restan 1 a v2(g).
# ---------------------------------------------------------------------------

for g in range(2, 20001, 2):
    _, g0 = transicion_mod(0, g, 0)
    _, g1 = transicion_mod(0, g, 1)
    if v2(g0) != v2(g) - 1 or v2(g1) != v2(g) - 1:
        raise SystemExit("C2: g=%d" % g)
print()
print("COMPROBACION 2 OK: en la frontera par los DOS bits restan 1 a")
print("v2(g) -- el mixto llega en v2(g) pasos, determinista puro.")

# ---------------------------------------------------------------------------
# LA SERIE DEL EMPALME (la pieza que queda), a PROF = 34:
#   ocupacion del fondo y su acumulada (Golondrinas la hace divergir),
#   masa y acumulada de (1,1) (la serie del criterio phi = 1), y el
#   piso por visita E[(1+|c|)^(-5/2) | fondo] con su exponente local.
# ---------------------------------------------------------------------------

import math

estados = {(0, 1): 1}
serie = []
for prof in range(1, PROF + 1):
    nuevo = {}
    for (k, c), n in estados.items():
        for bit in (0, 1):
            k2, c2 = transicion_mod(k, c, bit)
            nuevo[(k2, c2)] = nuevo.get((k2, c2), 0) + n
    estados = nuevo
    if len(estados) > TOPE_ESTADOS:
        raise SystemExit("tope en prof %d" % prof)
    tot = 2.0 ** prof
    m11 = fondo = 0
    piso = 0.0
    for (k, c), n in estados.items():
        if (k, c) == (1, 1):
            m11 += n
        if k <= 1:
            fondo += n
            piso += n * (1 + abs(c)) ** -2.5
    serie.append((prof, fondo / tot, m11 / tot,
                  (piso / fondo) if fondo else 0.0))

print()
print("  t   fondo(k<=1)   acum.fondo   m(1,1)      acum(1,1)   piso/visita   alfa(piso)")
ac_f = ac_v = 0.0
pisos = {}
for (prof, ffondo, f11, piso) in serie:
    ac_f += ffondo
    ac_v += f11
    pisos[prof] = piso
    alfa = ""
    if prof - 6 in pisos and pisos[prof] > 0 and pisos[prof - 6] > 0:
        alfa = "   %7.4f" % (-(math.log(pisos[prof]) - math.log(pisos[prof - 6]))
                             / (math.log(prof) - math.log(prof - 6)))
    if prof % 2 == 0 and prof >= 12:
        print("%3d     %7.4f    %8.3f    %.6f    %8.5f      %7.5f%s"
              % (prof, ffondo, ac_f, f11, ac_v, piso, alfa))

print()
print("VEREDICTO -- GOLONDRINAS: las visitas al fondo son infinitas c.s.")
print("en la cadena modificada (L2 demostrado aqui + tabla de derivas de")
print("lamperti.py + oscilacion de martingalas). El programa de phi = 1")
print("queda en UNA pieza: el empalme por visita -- si el piso de la")
print("ultima columna no se desvanece (o decae no-sumablemente sobre")
print("las visitas), (1,1) se toca infinitas veces y phi = 1. La serie")
print("ORIENTA (alfa local abajo de 1 y decelerando = favorable); el")
print("veredicto es del mecanismo: la estacionaria del IFS de Aranas")
print("condicionada al fondo, el paso tecnico de perturbed IFS.")
