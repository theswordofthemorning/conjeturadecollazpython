# lamperti.py
#
# EL ATAQUE DE LAMPERTI SOBRE LA CADENA MODIFICADA (09-08-2026; el
# ataque 1 de la lista post-Abejas).
#
#   EL CRITERIO (derivado en la sesion del 09-08): sea la CADENA
#   MODIFICADA la de Leonas con UNA sola diferencia -- en el vortice
#   (1,1) el bit se fuerza a 0 (rebote a (2,2)) en vez de absorber.
#   Cada visita al vortice de la cadena real sobrevive con moneda 1/2,
#   asi que  P(no fundir jamas) = E_mod[ 2^(-N) ]  con N = visitas de
#   la cadena modificada a (1,1). Positivo sii N puede ser finito:
#
#       phi = 1   <=>   (1,1) es RECURRENTE en la cadena modificada.
#
#   Y EN LA CADENA MODIFICADA NO HAY CONDICIONAMIENTO A VIVO: el
#   problema del h-transform (Bessel) desaparece. La estructura que
#   este fichero mide y certifica por enumeracion:
#
#   (A) LA DERIVA EXACTA DE k (comprobacion 1): en el nucleo todo
#       paso mixto es moneda justa +-1 (E[dk] = 0); los UNICOS estados
#       con deriva positiva son el borde (frontera impar: +1 seguro;
#       (1,1) modificado: +1 seguro); nada tiene deriva negativa.
#       Entonces k_t = M_t + A_t con M martingala de incrementos
#       acotados y A creciente SOLO en el borde. Si hay infinitos
#       mixtos, M oscila (teorema de oscilacion de martingalas:
#       converge o lim inf = -inf), y k >= 0 fuerza A -> infinito:
#       INFINITAS VISITAS AL FONDO. La recurrencia de la banda baja
#       queda colgando de UN lema: (L2) hay infinitos mixtos c.s.
#   (L2) = "no hay trampa todo-par": quedarse sin mixtos exige c par
#       para siempre; con c != 0 las halvings agotan v2(c) en pasos
#       forzados, y c = 0 sale con el bit 1. La comprobacion 3 mide
#       la masa con v2(c) >= j contra 2^(-j), uniforme en t -- el
#       insumo cuantitativo del lema.
#   (B) EL EMPALME POR VISITA: del fondo a (1,1) via HORMIGAS: la
#       palabra del constructor mide <= 2.5(k + log2|c| + 1), o sea
#       la probabilidad de tocar (1,1) desde una visita al fondo es
#       >= |c|^(-2.5) (aprox). La comprobacion 6 mide ese piso por
#       visita: E[ (1+|c|)^(-5/2) | banda k <= 1 ] por nivel.
#
#   ETIQUETAS: C1 es enumeracion exacta (decide); C3-C6 son medidas
#   exactas de la masa simbolica (sin muestreo) que ORIENTAN los
#   lemas; ninguna medida decide el limite (la leccion de la casa).
#
#   Mapa del ATAJO, enteros exactos, SystemExit antes de concluir.

import math

PROF = 30
TOPE_ESTADOS = 9 * 10 ** 6


def transicion_mod(k, c, bit):
    # la cadena de Leonas con el vortice rebotado (sin absorcion)
    if k == 0:
        if c % 2 == 0:
            return (0, c // 2) if bit == 0 else (0, 3 * c // 2)
        return (1, (3 * c + 1) // 2) if bit == 0 else (1, (1 - 3 * c) // 2)
    if c % 2 == 0:
        return (k, c // 2) if bit == 0 else (k, (3 * c + 1 - 3 ** k) // 2)
    if k == 1 and c == 1:
        return (2, 2)                       # EL VORTICE, REBOTADO (ambos bits)
    if bit == 0:
        return (k + 1, (3 * c + 1) // 2)
    if k >= 2:
        return (k - 1, (c - 3 ** (k - 1)) // 2)
    return (0, abs((c - 1) // 2))

# ---------------------------------------------------------------------------
# COMPROBACION 1: LA TABLA EXACTA DE DERIVAS DE k, por enumeracion.
#   Para cada estado de una ventana grande, E[dk] sobre los dos bits.
#   Exigido: deriva 0 en todo el nucleo (mixto y compartido), +1 en
#   frontera impar y en (1,1); >= 0 en todas partes (A creciente).
# ---------------------------------------------------------------------------

clases = {}
for k in range(0, 12):
    for c in range(1 if k == 0 else -3 ** min(k + 1, 7), 3 ** min(k + 1, 7) + 1):
        if k >= 1 and c == 0:
            pass  # c = 0 se incluye
        d0 = transicion_mod(k, c, 0)[0] - k
        d1 = transicion_mod(k, c, 1)[0] - k
        deriva = (d0 + d1) / 2.0
        if k == 1 and c == 1:
            etiqueta = 'vortice(1,1)'
            if deriva != 1:
                raise SystemExit("C1: vortice con deriva %s" % deriva)
        elif k == 0 and c % 2 == 1:
            etiqueta = 'frontera impar'
            if deriva != 1:
                raise SystemExit("C1: frontera impar deriva %s en g=%d" % (deriva, c))
        elif k == 0:
            etiqueta = 'frontera par'
            if deriva != 0:
                raise SystemExit("C1: frontera par deriva %s" % deriva)
        elif c % 2 == 1:
            etiqueta = 'nucleo mixto'
            if k >= 2 and deriva != 0:
                raise SystemExit("C1: mixto k>=2 deriva %s en (%d,%d)" % (deriva, k, c))
            if k == 1 and c != 1 and deriva != 0:
                raise SystemExit("C1: mixto k=1 deriva %s en c=%d" % (deriva, c))
        else:
            etiqueta = 'nucleo compartido'
            if deriva != 0:
                raise SystemExit("C1: compartido deriva %s" % deriva)
        clases[etiqueta] = clases.get(etiqueta, 0) + 1

print("COMPROBACION 1 OK -- LA TABLA DE DERIVAS, exacta por enumeracion:")
for e, n in sorted(clases.items()):
    print("   %-18s : %6d estados" % (e, n))
print("deriva de k: 0 en TODO el nucleo y la frontera par; +1 SOLO en la")
print("frontera impar y el vortice rebotado. k = martingala + proceso")
print("creciente A que solo crece en el borde: si hay infinitos mixtos,")
print("la oscilacion de la martingala fuerza A -> inf, o sea INFINITAS")
print("VISITAS AL FONDO. (El lema que falta es L2: infinitos mixtos.)")

# ---------------------------------------------------------------------------
# EL BARRIDO SIMBOLICO DE LA CADENA MODIFICADA, guardando por nivel:
#   masa por k, masa mixta (c impar), masa con v2(c) >= j, masa en
#   (1,1), masa banda k <= 1, y E[(1+|c|)^(-5/2)] sobre la banda.
# ---------------------------------------------------------------------------

def v2(c):
    if c == 0:
        return 99
    j = 0
    while c % 2 == 0:
        c //= 2
        j += 1
    return j


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
        raise SystemExit("tope de estados en prof %d" % prof)
    tot = 2.0 ** prof
    mixta = m11 = fondo = 0
    v2masa = {}
    piso_visita = 0.0
    for (k, c), n in estados.items():
        if (k >= 1 and c % 2 == 1) or (k == 0 and c % 2 == 1):
            mixta += n
        if k >= 1:
            j = min(v2(c), 12)
            v2masa[j] = v2masa.get(j, 0) + n
        if (k, c) == (1, 1):
            m11 += n
        if k <= 1:
            fondo += n
            piso_visita += n * (1 + abs(c)) ** -2.5
    serie.append((prof, mixta / tot, m11 / tot, fondo / tot,
                  (piso_visita / fondo) if fondo else 0.0, v2masa, tot))

# ---------------------------------------------------------------------------
# COMPROBACION 3: LA MASA DE v2(c) >= j CONTRA 2^(-j), uniforme en t.
#   El insumo del lema L2: si sup_t masa(v2 >= j)*2^j esta acotado,
#   los estados "muy pares" son exponencialmente raros SIEMPRE y el
#   trampeo todo-par tiene probabilidad 0 (Borel-Cantelli condicional).
# ---------------------------------------------------------------------------

sup_v2 = {}
for (prof, fmix, f11, ffondo, piso, v2masa, tot) in serie:
    if prof < 8:
        continue
    for j, n in v2masa.items():
        val = n / tot * 2 ** j
        if j not in sup_v2 or val > sup_v2[j][0]:
            sup_v2[j] = (val, prof)

print()
print("COMPROBACION 3 -- la masa 'muy par' (nucleo), sup_t masa(v2(c) >= j)*2^j:")
print("   j    sup_t masa*2^j   (en t)")
acotado = True
for j in sorted(sup_v2):
    if j <= 10:
        print("  %2d      %8.4f       %4d" % (j, sup_v2[j][0], sup_v2[j][1]))
    if sup_v2[j][0] > 4.0 and j <= 10:
        acotado = False
if not acotado:
    raise SystemExit("C3: la masa muy-par NO parece geometricamente rara")
print("acotado por debajo de 4 en toda la ventana: los estados a j")
print("halvings de un mixto pesan ~2^(-j) UNIFORME -- el insumo de L2.")

# ---------------------------------------------------------------------------
# LAS SERIES DEL VEREDICTO (medidas, orientan):
#   - fraccion mixta por nivel (L2 pide que no se desvanezca);
#   - ocupacion del fondo (k <= 1) y su acumulada (recurrencia: la
#     acumulada debe DIVERGER, tipo sqrt(t));
#   - masa en (1,1) y su acumulada: E[visitas a (1,1) hasta t] -- LA
#     SERIE DEL CRITERIO: recurrente sii diverge (phi = 1);
#   - el piso por visita E[(1+|c|)^(-5/2) | fondo] (el empalme B).
# ---------------------------------------------------------------------------

print()
print("  t   frac.mixta   fondo(k<=1)   acum.fondo   m(1,1)      acum(1,1)   piso/visita")
ac_f = ac_v = 0.0
for (prof, fmix, f11, ffondo, piso, v2masa, tot) in serie:
    ac_f += ffondo
    ac_v += f11
    if prof % 2 == 0 or prof >= 26:
        print("%3d    %7.4f      %7.4f     %8.3f    %.6f    %8.5f     %7.5f"
              % (prof, fmix, ffondo, ac_f, f11, ac_v, piso))

print()
print("VEREDICTO (con etiquetas):")
print("  EXACTO: la tabla de derivas (C1) -- k es martingala con empuje")
print("  de borde en la cadena modificada; el argumento de oscilacion")
print("  reduce la recurrencia de la banda baja al lema L2.")
print("  MEDIDO: la fraccion mixta por nivel, la masa muy-par (C3), la")
print("  ocupacion acumulada del fondo y de (1,1) -- si la acumulada de")
print("  (1,1) crece sin techo, la recurrencia (phi = 1) es lo esperado;")
print("  si se aplana hacia una constante, phi < 1. La serie ORIENTA;")
print("  las piezas que decidirian son L2 (infinitos mixtos, via C3)")
print("  y el empalme por visita (Hormigas + el piso de la ultima")
print("  columna). El nombre tecnico sigue siendo Lamperti/Foster,")
print("  pero el camino corto es la oscilacion de la martingala.")
