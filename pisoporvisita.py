# pisoporvisita.py
#
# EL PISO DE ABSORCION POR VISITA, MEDIDO COMO SERIE (09-08-2026; el
# ataque 1 de la ruta de RutaTeoremas.md, seccion "EL ESTADO Y LOS
# PROXIMOS PASOS").
#
#   LA PREGUNTA (afirmacion #162 de la base, la ultima pieza del
#   programa de la densidad): sea
#
#       p_t = masa de palabras vivas en el pre-vortice (1, c=1)
#             ---------------------------------------------------
#             masa de palabras vivas con k = 1
#
#   al nivel t del barrido simbolico de la cadena (k, c) de Leonas.
#   Hasta hoy solo existia LA FOTO: p_34 = 0,0457 (aranas.py, T4).
#   Este fichero mide LA SERIE ENTERA t = 1..34, sus cocientes y su
#   exponente local, mas la serie companera que el argumento del piso
#   por estructura (Doeblin / minorizacion) necesita: la masa de la
#   rejilla finita |c| <= C dentro de k = 1.
#
#   QUE DECIDE Y QUE NO (la leccion de la casa, pegada al instrumento):
#   una serie que baja despacio NO distingue "tiende a constante > 0"
#   de "tiende a 0 como 1/log t" -- el muro de b(k), tres veces; y el
#   precedente de dispersionc.py: la medicion oriento y el mecanismo
#   la revirtio en una hora. ESTA SERIE ORIENTA EL RUMBO; el veredicto
#   phi = 1 contra phi < 1 lo dara el mecanismo (ataque 2), no esta
#   tabla.
#
#   La cadena es la de paseodeladeuda.py (duplicada a proposito, como
#   manda el repo: cada fichero se lee entero y corre solo). Mapa del
#   ATAJO, enteros exactos, SystemExit antes de concluir.

import math

PROF_MAX = 34               # profundidad del barrido (la de aranas.py)
TOPE_ESTADOS = 9 * 10 ** 6  # corta si el diccionario crece mas que esto
CUBETAS_C = (1, 2, 4, 8, 16, 32)   # la rejilla finita: |c| <= C en k = 1

# a(3)..a(12) publicadas (sucesiones.txt): el control del motor
A_PUBLICADA = [1, 3, 8, 18, 39, 82, 170, 351, 721, 1476]

# la foto previa del pre-vortice (aranas.py T4, redondeada a 4 cifras)
P34_FOTO = 0.0457


def paso(x):
    # el mapa del atajo sobre un entero
    return (3 * x + 1) // 2 if x % 2 else x // 2


def transicion(k, c, bit):
    # la cadena simbolica de Leonas; ('estado', k', c') o ('fusion',)
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


# ---------------------------------------------------------------------------
# EL BARRIDO, guardando en cada nivel lo que la serie necesita:
#   viva(t), masa_k1(t), masa del pre-vortice (1,1), y la masa de la
#   rejilla |c| <= C dentro de k = 1 para cada C de CUBETAS_C.
# ---------------------------------------------------------------------------

estados = {(0, 1): 1}
absorbidas = 0
a_cadena = []       # a(k) acumulada, para el control del motor
serie = []          # (t, viva, mk1, m11, {C: masa de |c| <= C en k=1})

for prof in range(1, PROF_MAX + 1):
    nuevo = {}
    nuevas_abs = 0
    for (k, c), n in estados.items():
        for bit in (0, 1):
            t = transicion(k, c, bit)
            if t[0] == 'fusion':
                nuevas_abs += n
            else:
                clave = (t[1], t[2])
                nuevo[clave] = nuevo.get(clave, 0) + n
    absorbidas = 2 * absorbidas + nuevas_abs
    estados = nuevo
    a_cadena.append(absorbidas)
    if len(estados) > TOPE_ESTADOS:
        raise SystemExit("tope de estados en prof %d: %d" % (prof, len(estados)))

    viva = sum(estados.values())
    mk1 = m11 = 0
    rejilla = dict((C, 0) for C in CUBETAS_C)
    for (k, c), n in estados.items():
        if k == 1:
            mk1 += n
            if c == 1:
                m11 += n
            for C in CUBETAS_C:
                if abs(c) <= C:
                    rejilla[C] += n
    serie.append((prof, viva, mk1, m11, rejilla))

# ---------------------------------------------------------------------------
# COMPROBACION 1: EL MOTOR. La cadena tiene que reproducir a(k) publicada
# (k = 3..12). Si esto falla, la serie de abajo no vale nada.
# ---------------------------------------------------------------------------

for i, k in enumerate(range(3, 13)):
    if a_cadena[k - 1] != A_PUBLICADA[i]:
        raise SystemExit("C1: a(%d) cadena=%d, publicada=%d"
                         % (k, a_cadena[k - 1], A_PUBLICADA[i]))
print("COMPROBACION 1 OK: el motor reproduce a(k) publicada, k = 3..12.")

# ---------------------------------------------------------------------------
# COMPROBACION 2: LA FOTO. p_34 tiene que dar el 0,0457 de aranas.py T4
# (misma cadena, mismo arranque, misma profundidad; tolerancia por el
# redondeo a 4 cifras de la foto).
# ---------------------------------------------------------------------------

t34 = serie[-1]
if t34[0] != PROF_MAX:
    raise SystemExit("C2: el barrido no llego a %d" % PROF_MAX)
p34 = t34[3] / t34[2]
if abs(p34 - P34_FOTO) > 5e-4:
    raise SystemExit("C2: p_34 = %.6f, la foto decia %.4f" % (p34, P34_FOTO))
print("COMPROBACION 2 OK: p_34 = %.6f, compatible con la foto 0,0457." % p34)

# ---------------------------------------------------------------------------
# LA SERIE. p_t = m11/mk1, q_t = m11/viva, s_t = mk1/viva, y el cociente
# p_t / p_{t-2} (dos niveles, porque la cadena tiene ritmo de paridad:
# el lazo de Gatas y la ventana de Perras van de dos en dos).
# ---------------------------------------------------------------------------

print()
print("LA SERIE DEL PISO: p_t = masa(1,1) / masa(k=1), nivel a nivel")
print("  t      viva          s_t = k1/viva   p_t = (1,1)/k1   p_t/p_(t-2)")
prev = {}
for (t, viva, mk1, m11, rejilla) in serie:
    if mk1 == 0:
        print("%3d  %12d   [sin masa en k = 1]" % (t, viva))
        continue
    p = m11 / mk1
    s = mk1 / viva
    coc = ""
    if t - 2 in prev and prev[t - 2] > 0:
        coc = "   %8.5f" % (p / prev[t - 2])
    print("%3d  %12d      %10.6f      %10.6f%s" % (t, viva, s, p, coc))
    prev[t] = p

# ---------------------------------------------------------------------------
# EL EXPONENTE LOCAL: si p_t ~ t^(-alfa), alfa_t = -d log p / d log t
# estimada entre t-4 y t (ventana corta, mismo criterio que beta_t de
# dispersionc.py). alfa -> 0 apunta a piso positivo; alfa estabilizada
# > 0 apunta a desvanecimiento polinomial; alfa creciendo, a algo peor.
# ---------------------------------------------------------------------------

print()
print("exponente local alfa_t (ajuste log-log entre t-4 y t):")
print("  t     alfa_t")
ps = dict((t, m11 / mk1) for (t, viva, mk1, m11, r) in serie if mk1 > 0)
for t in range(8, PROF_MAX + 1, 2):
    if t in ps and (t - 4) in ps and ps[t] > 0 and ps[t - 4] > 0:
        alfa = -(math.log(ps[t]) - math.log(ps[t - 4])) \
            / (math.log(t) - math.log(t - 4))
        print("%3d   %8.4f" % (t, alfa))

# ---------------------------------------------------------------------------
# LA REJILLA FINITA (lo que el ataque 2 necesita): masa de |c| <= C
# dentro de k = 1. Si estas fracciones tienden a constantes positivas,
# la cadena visita la rejilla finita con frecuencia acotada abajo -- la
# mitad de la minorizacion. Se imprimen las tres ultimas profundidades
# y la serie de C = 8 entera.
# ---------------------------------------------------------------------------

print()
print("la rejilla finita en k = 1: masa(|c| <= C) / masa(k = 1)")
print("  t   " + "".join("   C<=%-3d" % C for C in CUBETAS_C))
for (t, viva, mk1, m11, rejilla) in serie:
    if t < PROF_MAX - 5 or mk1 == 0:
        continue
    fila = "".join("  %7.4f" % (rejilla[C] / mk1) for C in CUBETAS_C)
    print("%3d %s" % (t, fila))

print()
print("serie entera de C = 8 (la cubeta central), t = 6..%d:" % PROF_MAX)
for (t, viva, mk1, m11, rejilla) in serie:
    if t >= 6 and mk1 > 0 and t % 2 == 0:
        print("  t =%3d :  %8.5f" % (t, rejilla[8] / mk1))

# ---------------------------------------------------------------------------
# EL VEREDICTO HONESTO, con las etiquetas de la casa.
# ---------------------------------------------------------------------------

print()
print("VEREDICTO (medido, NO decide): la serie p_t esta impresa entera")
print("con sus cocientes bianuales y su exponente local. Lo que esta")
print("tabla NO puede hacer es distinguir 'liminf > 0' de 'cae como")
print("1/log t' -- el muro de b(k), tres veces --; el veredicto phi = 1")
print("contra phi < 1 es del MECANISMO (ataque 2: minorizacion sobre la")
print("rejilla finita), y las columnas de la rejilla son su insumo.")
