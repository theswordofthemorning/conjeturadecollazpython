# paseodeladeuda.py
#
# LA CADENA (k, c) - EL TEOREMA DE LEONAS: el sistema simbolico COMPLETO
# (04-08-2026; el ataque al punto 1 del norte -- "es el paseo genuinamente
# recurrente sobre las clases?" -- y lo que salio al construir el
# instrumento es mas grande que la pregunta).
#
#   EL DESCUBRIMIENTO. Todo estado de un par vivo (no fundido) cuyas dos
#   trayectorias siguen acopladas es una FORMA
#
#       { v, 3^k v + c }        (k >= 1: "torre de nivel k", c en Z)
#       { v, v + g }            (k = 0: "frontera", gap g >= 1 constante)
#
#   y la dinamica del par la decide UN SOLO BIT FRESCO por paso (la
#   paridad del menor, que por Terras es una moneda justa sobre la
#   clase). LAS SEIS LEYES, cada una un calculo de una linea:
#
#     nucleo k >= 1, c PAR (paso compartido):
#       N1  bit 0:  (k, c)   ->  (k, c/2)
#       N2  bit 1:  (k, c)   ->  (k, (3c + 1 - 3^k)/2)
#     nucleo k >= 1, c IMPAR (paso mixto):
#       N3  bit 0:  (k, c)   ->  (k+1, (3c+1)/2)         [ASCIENDE: deuda +1]
#       N4  bit 1:  k >= 2:  ->  (k-1, (c - 3^(k-1))/2)  [COMPENSA: deuda -1]
#                   k == 1:  ->  gap g' = (c-1)/2:
#                       g' = 0  ->  FUSION  (el vortice: c = 1)
#                       g' != 0 ->  frontera (0, |g'|)
#     frontera k = 0, g PAR:
#       F1  bit 0:  (0, g)   ->  (0, g/2)
#       F2  bit 1:  (0, g)   ->  (0, 3g/2)
#     frontera k = 0, g IMPAR (mixto):
#       F3  bit 0:  (0, g)   ->  (1, (3g+1)/2)           [reentra al nucleo]
#       F4  bit 1:  (0, g)   ->  (1, (1-3g)/2)           [vuelco, reentra]
#
#   (mixto <=> c impar, porque gap = (3^k - 1)v + c y 3^k - 1 es par;
#   y en un mixto el mayor es impar <=> v es par: la moneda del paseo.)
#
#   EL ZOOLOGICO ENTERO SON ESTADOS DE ESTA CADENA:
#     (0, 1)  el par consecutivo            (1, 1)  el vortice (D = 0)
#     (1, 2)  el tramo D = 1 de Perras      (2, 2)  el rebote {w, 9w+2}
#     (2,-1)  la forma h {w, 9w-1}          (2, 1)  la puerta {u, 9u+1}
#     (1,-2), (1,-4)  el grafo {-3,-5} de los chanchitos (D = c - 1)
#     la contraccion de Gatas = el lazo (0,1) -1-> (1,-1) -1-> (0,1)
#     Garner (8k+4, 8k+5) = la palabra 0,0,1 desde (0,1)
#     las torres = k >= 2, la deuda = k, la moneda = el bit de v
#
#   Y LA CONSECUENCIA QUE SE COMPRUEBA ABAJO: la cadena, iterada como
#   puro sistema simbolico (sin tocar UN SOLO par de enteros), reproduce
#   a(k) EXACTO. La densidad de fusion phi es la probabilidad de
#   absorcion de esta cadena, y la pregunta del programa ("phi = 1?")
#   es la recurrencia de este paseo con monedas justas: el nucleo hace
#   un paseo +-1 simetrico en k (N3/N4), la frontera es una cuenta
#   atras de v_2 (F1/F2) que reentra (F3/F4), y la unica absorcion es
#   el vortice (1,1) con bit 1.
#
#   Mapa del ATAJO, enteros exactos, SystemExit antes de concluir.

A_PUBLICADA = [1, 3, 8, 18, 39, 82, 170, 351, 721, 1476]   # a(3)..a(12)

# b(k) = a(k+1) - 2a(k), k = 3..31: la sucesion entera de sucesiones.txt,
# incluida la cola cara (b(31) = 9.701.007 salio del barrido a 2^32)
B_PUBLICADA = [1, 2, 2, 3, 4, 6, 11, 19, 34, 60, 106, 190, 341, 623, 1148,
               2124, 3963, 7451, 14072, 26699, 50913, 97379, 186769, 359164,
               692079, 1336125, 2583668, 5002992, 9701007]

# los DOS niveles nuevos que produce este fichero:
#   a(33) = 3.761.106.610   b(32) = 18.831.364   razon 1,9412
#   a(34) = 7.558.807.251   b(33) = 36.594.031   razon 1,9432
# ESTADO: sostenidos por segundo camino (segundocamino.py): cumplen la
# identidad-teorema a(k+2) = a(k) + (2^k-1) + G(k) + H(k) en k = 31, 32
# con G y H de barridos separados de los pisos g y h. El camino
# totalmente independiente (clasesparalelo.py con K_MAX = 33, horas de
# CPU) queda como opcion si algun dia se publican fuera del repo.

PROF_MAX = 34         # profundidad del barrido simbolico (estados exactos)
TOPE_ESTADOS = 6 * 10 ** 6   # corta el barrido si el diccionario crece mas


def paso(x):
    return (3 * x + 1) // 2 if x % 2 else x // 2


def transicion(k, c, bit):
    # la cadena simbolica; devuelve ('estado', k', c') o ('fusion',)
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
# COMPROBACION 1: LAS SEIS LEYES CONTRA PARES REALES.
#   Para cada forma (k, c) y cada paridad de v, el paso real del par
#   aterriza EXACTAMENTE en la forma que dicta la cadena. Tambien la ley
#   de la moneda: mixto <=> c impar, y en el mixto el mayor es impar
#   <=> v par. El unico cuidado es v grande (v > |c|), para que el par
#   este ordenado y lejos del atractor.
# ---------------------------------------------------------------------------

probadas = 0
for k in range(0, 8):
    for c in range(1 if k == 0 else -60, 61):
        if c == 0 and k == 0:
            continue
        for v in range(200, 400):
            x, y = v, (3 ** k * v + c) if k >= 1 else v + c
            if y <= x:
                raise SystemExit("C1: forma invalida k=%d c=%d v=%d" % (k, c, v))
            # ley de la moneda
            es_mixto = (x % 2) != (y % 2)
            if es_mixto != (c % 2 == 1):
                raise SystemExit("C1 moneda: k=%d c=%d v=%d" % (k, c, v))
            if es_mixto and ((y % 2 == 1) != (v % 2 == 0)):
                raise SystemExit("C1 lado impar: k=%d c=%d v=%d" % (k, c, v))
            nx, ny = paso(x), paso(y)
            t = transicion(k, c, v % 2)
            if t[0] == 'fusion':
                if nx != ny:
                    raise SystemExit("C1 fusion: k=%d c=%d v=%d" % (k, c, v))
            else:
                _, k2, c2 = t
                lo, hi = min(nx, ny), max(nx, ny)
                objetivo = (3 ** k2 * lo + c2) if k2 >= 1 else lo + c2
                if hi != objetivo:
                    raise SystemExit("C1 ley: (%d,%d) v=%d bit=%d -> real "
                                     "(%d,%d), cadena (%d,%d)"
                                     % (k, c, v, v % 2, lo, hi, k2, c2))
            probadas += 1

print("COMPROBACION 1 OK: las seis leyes y la ley de la moneda, exactas en")
print("%d instancias (k = 0..7, c = -60..60, v = 200..399, ambas paridades)."
      % probadas)

# ---------------------------------------------------------------------------
# COMPROBACION 2: EL ZOOLOGICO, COMO ARITMETICA DE LA CADENA.
#   Cada pieza del programa es una identidad de transicion. Se comprueban
#   con la funcion, no con pares: son afirmaciones sobre la cadena misma.
# ---------------------------------------------------------------------------

zoo = [
    # la contraccion de Gatas: (0,1) -1-> (1,-1) -1-> (0,1)  [r = 1 mod 4]
    (('estado', 1, -1), transicion(0, 1, 1)),
    (('estado', 0, 1), transicion(1, -1, 1)),
    # la rama h: (0,1) -1-> (1,-1) -0-> (2,-1)  [r = 3 mod 4 -> {w, 9w-1}]
    (('estado', 2, -1), transicion(1, -1, 0)),
    # Perras: (0,1) -0-> (1,2); el lazo compartido-impar (1,2) -1-> (1,2);
    # la caida a D = 0: (1,2) -0-> (1,1); y el vortice (1,1) -1-> FUSION
    (('estado', 1, 2), transicion(0, 1, 0)),
    (('estado', 1, 2), transicion(1, 2, 1)),
    (('estado', 1, 1), transicion(1, 2, 0)),
    (('fusion',), transicion(1, 1, 1)),
    # el rebote: (1,1) -0-> (2,2)  [{w, 9w+2}, el estado g]
    (('estado', 2, 2), transicion(1, 1, 0)),
    # la puerta P1: (2,2) -1-> (2,-1)  [g entra a h en un paso]
    (('estado', 2, -1), transicion(2, 2, 1)),
    # la puerta P2: (2,2) -0-> (2,1)  [{u, 9u+1}]
    (('estado', 2, 1), transicion(2, 2, 0)),
    # P3: (2,1) -1-> (1,-1)  [aterriza en D = -2: c - 1 = -2]
    (('estado', 1, -1), transicion(2, 1, 1)),
    # T2 (la torre asciende): (2,1) -0-> (3,2); T1: (3,2) -0-> (3,1)
    (('estado', 3, 2), transicion(2, 1, 0)),
    (('estado', 3, 1), transicion(3, 2, 0)),
    # el grafo de los chanchitos (D = c-1 en k=1): (1,-2) <-> (1,-4),
    # aterrizajes (1,-1) [D=-2] y (1,-7) [D=-8]
    (('estado', 1, -1), transicion(1, -2, 0)),
    (('estado', 1, -4), transicion(1, -2, 1)),
    (('estado', 1, -2), transicion(1, -4, 0)),
    (('estado', 1, -7), transicion(1, -4, 1)),
]
for esperado, real in zoo:
    if esperado != real:
        raise SystemExit("C2 zoo: esperado %s, cadena %s" % (esperado, real))

# Garner: la palabra 0,0,1 desde (0,1) fusiona (8k+4 / 8k+5 en 3 pasos)
e = ('estado', 0, 1)
for bit in (0, 0, 1):
    e = transicion(e[1], e[2], bit)
if e != ('fusion',):
    raise SystemExit("C2 Garner: %s" % (e,))

print()
print("COMPROBACION 2 OK: Gatas (el lazo 1,1), la rama h, la ventana de")
print("Perras, el vortice, el rebote (2,2), las puertas P1-P3, la torre")
print("T1/T2, el grafo {-3,-5} y la palabra de Garner: TODOS son")
print("identidades de transicion de la cadena.")

# ---------------------------------------------------------------------------
# COMPROBACION 3: LA CADENA REPRODUCE a(k) SIN TOCAR UN PAR.
#   Barrido simbolico desde (0,1): las palabras de largo k son las clases
#   r mod 2^k (cada paso lee un bit fresco del menor: Terras), y las
#   absorbidas en <= k pasos deben ser EXACTAMENTE a(k). Se compara
#   contra la sucesion publicada Y contra un recomputo directo con pares.
# ---------------------------------------------------------------------------

def a_directa(k):
    n = 0
    for r in range(2 ** k - 1):
        x, y = r, r + 1
        Sx = Sy = 0
        for _ in range(k):
            if x % 2:
                Sx += 1
            if y % 2:
                Sy += 1
            x, y = paso(x), paso(y)
            if x == y:
                if Sx == Sy:
                    n += 1
                break
    return n


estados = {(0, 1): 1}
absorbidas = 0            # cuenta acumulada, doblandose con el nivel
a_cadena = []
historial = []
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
    historial.append((prof, absorbidas, len(estados)))
    if len(estados) > TOPE_ESTADOS:
        print("[barrido cortado en prof %d: %d estados]" % (prof, len(estados)))
        break

# el doblado (a(k+1) >= 2a(k)), que es el teorema de Gao, debe salir solo
for i in range(1, len(a_cadena)):
    if a_cadena[i] < 2 * a_cadena[i - 1]:
        raise SystemExit("C3 doblado: a(%d)=%d < 2*a(%d)=%d"
                         % (i + 1, a_cadena[i], i, 2 * a_cadena[i - 1]))
# y la sucesion b entera, incluida la cola cara del barrido a 2^32
for i, k in enumerate(range(3, 32)):
    if k < len(a_cadena):
        b = a_cadena[k] - 2 * a_cadena[k - 1]
        if b != B_PUBLICADA[i]:
            raise SystemExit("C3 b: b(%d) cadena=%d, publicada=%d"
                             % (k, b, B_PUBLICADA[i]))

for i, k in enumerate(range(3, 13)):
    if k - 1 <= len(a_cadena) and a_cadena[k - 1] != A_PUBLICADA[i]:
        raise SystemExit("C3 publicada: a(%d) cadena=%d, publicada=%d"
                         % (k, a_cadena[k - 1], A_PUBLICADA[i]))
for k in range(3, 15):
    d = a_directa(k)
    if a_cadena[k - 1] != d:
        raise SystemExit("C3 directa: a(%d) cadena=%d, directa=%d"
                         % (k, a_cadena[k - 1], d))

print()
print("COMPROBACION 3 OK: el barrido SIMBOLICO reproduce a(k) EXACTO --")
print("contra la sucesion publicada (k = 3..12) y contra el recomputo")
print("directo con pares (k = 3..14). La cadena ES el programa de fusion.")

# ---------------------------------------------------------------------------
# COMPROBACION 4 (el regalo): LA EXTENSION DE a(k) Y b(k) POR LA CADENA.
#   El barrido simbolico coalesce estados (la renovacion en accion), asi
#   que llega donde el barrido de restos no podia: cada nivel de
#   clasesfusion.py costaba 2^k pares; aqui el costo es el numero de
#   estados VIVOS distintos. Se imprime a(k), b(k) = a(k+1) - 2a(k) y la
#   razon de nuevas -- la pregunta de la razon 2, con niveles nuevos.
# ---------------------------------------------------------------------------

print()
print("  k          a(k)        b(k-1)   razon b   estados vivos   masa viva")
prev_a = prev_b = None
for prof, absa, vivos in historial:
    b = absa - 2 * prev_a if prev_a is not None else None
    razon = (" %7.4f" % (b / prev_b)) if b and prev_b else "        "
    masa = 1.0 - absa / 2.0 ** prof
    print("%3d  %12d  %12s %s  %13d   %8.6f"
          % (prof, absa, b if b is not None else "", razon, vivos, masa))
    prev_a, prev_b = absa, (b if b else prev_b)

print()
print("COMPROBACION 4: la columna 'masa viva' es 1 - a(k)/2^k (cota")
print("superior de 1 - phi en el nivel); 'estados vivos' mide la")
print("coalescencia de la renovacion (contra los 2^k restos del barrido).")
print("b(k) cruzada contra la sucesion publicada ENTERA (k = 3..31),")
print("incluida la cola del barrido a 2^32: 0 discrepancias. a(33) y")
print("a(34) son NUEVOS, de la cadena sola: pendientes de segundo camino.")

# ---------------------------------------------------------------------------
# COMPROBACION 5: DONDE VIVE LA MASA VIVA -- la firma de la recurrencia.
#   El paseo de la deuda es el nivel k de la cadena. Si la masa viva
#   escapara hacia k grande, la torre seria una fuga real (paseo
#   transitorio); si se apila en k chico con c dispersandose, la
#   obstruccion a phi = 1 no es la torre sino la DISPERSION DE c en la
#   frontera -- y el paseo en k es recurrente tambien sobre las clases.
# ---------------------------------------------------------------------------

masa_por_k = {}
total_vivo = sum(estados.values())
for (k, c), n in estados.items():
    masa_por_k[k] = masa_por_k.get(k, 0) + n
prof_final = historial[-1][0]
print()
print("masa viva por nivel k de torre (prof %d, fraccion del total vivo):"
      % prof_final)
acum = 0.0
for k in sorted(masa_por_k):
    frac = masa_por_k[k] / total_vivo
    acum += frac
    if k <= 8 or frac > 1e-6:
        print("  k =%3d : %10.6f   (acumulado %8.6f)" % (k, frac, acum))
print()
print("COMPROBACION 5: si el acumulado hasta k pequenio es ~1, la torre no")
print("retiene masa (el paseo vuelve) y la pregunta phi = 1 vive entera en")
print("la dispersion de c sobre la frontera y el nucleo bajo.")
