# minorizacion.py
#
# EL ATAQUE 2 AL PISO: LA REDUCCION POR MINORIZACION (09-08-2026).
# Aqui viven EL LEMA DE ABEJAS (el lema de bloques: cada visita a la
# colmena paga miel) y LA IDENTIDAD DE PALOMAS (b(t) = N_t(1,1): las
# nuevas vuelven del pre-vortice, como mensajeras) -- bautizados por
# el usuario el 09-08-2026. La pieza (A) que el lema necesita es el
# teorema de HORMIGAS (accesibilidad.py).
#
#   EL ARGUMENTO, entero, porque es elemental y hay que tenerlo delante:
#
#   Supongamos phi < 1. Entonces la masa viva L(t) decrece hacia
#   1 - phi >= eps > 0, o sea L(t) >= eps para todo t. Si ademas
#
#     (i)   [MOSCAS, demostrado] la masa viva con |u| > x es
#           <= B_theta / x^theta, UNIFORME en t;
#     (ii)  [LA PIEZA QUE FALTA] la masa viva con nivel de torre k > K
#           es <= h(K) con h(K) -> 0, UNIFORME en t;
#     (iii) [ACCESIBILIDAD] desde todo estado (k, c) con k <= K y
#           |c| <= x * 3^K hay una PALABRA de largo <= T que fusiona
#           (la rejilla es FINITA: T = max finito si cada estado fusiona),
#
#   entonces: elegido (x, K) con B/x^theta + h(K) <= eps/2, la masa viva
#   dentro de la rejilla es >= eps/2 en TODO t. Cada palabra viva de la
#   rejilla tiene una continuacion de largo <= T que fusiona, y
#   continuaciones de palabras distintas son disjuntas (prefijos
#   distintos): cada bloque de T niveles absorbe >= (eps/2) * 2^(-T).
#   Infinitos bloques disjuntos absorben masa infinita -- y la masa
#   absorbida total es <= 1. CONTRADICCION. Luego phi = 1.
#
#   O sea: phi = 1 queda REDUCIDO a (ii) + (iii). Y LA FORMA AFILADA,
#   que es la que de verdad importa (la version uniforme de (ii) es
#   probablemente FALSA -- ver C4: el frente difusivo avanza por la
#   torre), sale del mismo argumento de bloques SIN la uniformidad:
#
#   LEMA DE ABEJAS (el lema de bloques; elemental, dado (iii) en la
#   rejilla G): si
#   phi < 1, entonces para toda rejilla finita G con cota T_G,
#
#       suma sobre bloques disjuntos de largo T_G de M_G(t_i)  <=  2^T_G
#
#   donde M_G(t) = masa viva en G al nivel t (normalizada por 2^t).
#   CONTRAPOSITIVO: si la ocupacion viva de UNA rejilla finita es NO
#   SUMABLE sobre bloques (p. ej. M_G(t) >= c/t^alfa con alfa <= 1),
#   entonces phi = 1. La recurrencia del paseo de RATAS predice
#   ocupacion ~ 1/sqrt(t): NO sumable. El blanco del teorema queda:
#   "la ocupacion de la rejilla decae a lo sumo polinomialmente con
#   exponente <= 1" -- y la serie M_G(t) se mide abajo.
#
#   ⇢⇢ CORRECCION (REVISION EXTERNA ADVERSARIAL, 09-08-2026, acta en
#   actarevision0908.txt): LA DESIGUALDAD DE ARRIBA ES CIERTA PERO
#   INCONDICIONAL -- no necesita phi < 1. Es Kraft: las continuaciones
#   fusionantes son palabras ABSORBIDAS, conjunto libre de prefijos,
#   masa total <= phi <= 1 SIEMPRE. Luego Sigma_t M_G(t) <= T_G*2^T_G
#   pase lo que pase con phi: EL CONTRAPOSITIVO ERA VACUO (antecedente
#   insatisfacible) y el blanco "M_G >= c/t" era DEMOSTRABLEMENTE
#   FALSO. La frase "RATAS predice ~1/sqrt(t)" confundia la cadena
#   REAL (con absorcion: su M_G es sumable por fuerza) con la
#   MODIFICADA (sin absorcion). EL BLANCO NO-VACUO es la ocupacion
#   CONDICIONADA A VIVO, M_G(t)/L(t) -- o directamente la cadena
#   modificada, que es el criterio de retorno11.py (la formulacion
#   buena, que AGUANTO la revision). Halconas tambien es incondicional
#   y no discrimina phi. Las series de este fichero siguen siendo
#   medidas exactas correctas; lo corregido es SU LECTURA.
#
#   ⇢ Y EL COROLARIO DE HALCONAS (bautizado el 09-08-2026; la rapaz
#   que obliga a la presa a subir), que sale SOLO de piezas ya
#   demostradas (Abejas + Hormigas + Moscas):
#
#       phi < 1  ==>  para TODO K fijo, masa_viva(k <= K, t) -> 0.
#
#   Demostracion: sumable (Abejas sobre los T_G desfases de bloque)
#   implica M_G(t) -> 0 para la rejilla {k <= K, |u| <= x}; y
#   masa(k <= K, |u| > x) <= B_theta/x^theta UNIFORME en t (Moscas).
#   Luego limsup_t masa(k <= K) <= B/x^theta para TODO x: es 0.
#   CONTRAPOSITIVO: si alguna banda finita de la torre conserva masa
#   viva (limsup > 0), phi = 1. El escenario phi < 1 exige que TODA
#   la masa viva suba la torre y no vuelva -- contra la recurrencia
#   del paseo de RATAS y contra el 93% medido en k <= 8 a t = 34.
#
#   Este fichero mide y comprueba las piezas:
#     - (iii) por BFS HACIA ATRAS desde la fusion: T(k, c) exacto para
#       toda la rejilla nucleo k <= 8, |c| <= 2000 y frontera g <= 2000,
#       y el crecimiento de T con log|c| y con k (si T ~ a + b*log2|c|,
#       la minorizacion se degrada polinomialmente: sana).
#     - (ii) midiendo sup_t masa_viva(k, t) * 2^k: si ese supremo esta
#       acotado (y se alcanza temprano), la conjetura h(K) ~ 2^(-K)
#       uniforme tiene soporte exacto -- y es el blanco del teorema.
#
#   Y DE REGALO LA IDENTIDAD QUE AFILA A ZORRAS, comprobada exacta:
#   la absorcion solo ocurre desde (1,1) con bit 1, luego
#       b(t) = N_t(1,1)  EXACTO
#   (las clases nuevas del nivel t+1 SON las palabras sentadas en el
#   pre-vortice al nivel t). La serie p_t del piso es b(t)/masa(k=1).
#
#   Cadena de paseodeladeuda.py (duplicada a proposito). Mapa del
#   ATAJO, enteros exactos, SystemExit antes de concluir.

from collections import deque

# --- ventana del BFS hacia atras (generosa alrededor de la rejilla) ---
K_BFS = 14              # nivel de torre maximo explorado
C_BFS = 120000          # |c| maximo explorado en el nucleo
G_BFS = 120000          # gap maximo explorado en la frontera

# --- la rejilla que hay que cubrir entera (el enunciado (iii)) ---
K_REJILLA = 8
C_REJILLA = 2000
G_REJILLA = 2000

# b(3)..b(15) publicadas, para la identidad b(t) = N_t(1,1)
B_PUBLICADA = [1, 2, 2, 3, 4, 6, 11, 19, 34, 60, 106, 190, 341]

PROF_TENSION = 30       # profundidad del barrido para la pieza (ii)


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


# ---------------------------------------------------------------------------
# COMPROBACION 0: b(t) = N_t(1,1), la identidad que afila a Zorras.
#   Barrido corto (t <= 15): las nuevas absorbidas del nivel t+1 tienen
#   que ser EXACTAMENTE la masa del pre-vortice (1,1) al nivel t, y esa
#   masa tiene que ser la b(t) publicada.
# ---------------------------------------------------------------------------

estados = {(0, 1): 1}
absorbidas = 0
m11_por_t = {}
for prof in range(1, 17):
    m11_por_t[prof - 1] = estados.get((1, 1), 0)
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
    if nuevas_abs != m11_por_t[prof - 1]:
        raise SystemExit("C0: nuevas_abs(%d)=%d != N_%d(1,1)=%d"
                         % (prof, nuevas_abs, prof - 1, m11_por_t[prof - 1]))
    absorbidas = 2 * absorbidas + nuevas_abs
    estados = nuevo

for i, t in enumerate(range(3, 16)):
    if m11_por_t[t] != B_PUBLICADA[i]:
        raise SystemExit("C0: N_%d(1,1)=%d, b publicada=%d"
                         % (t, m11_por_t[t], B_PUBLICADA[i]))

print("COMPROBACION 0 OK: b(t) = N_t(1,1) EXACTO (t = 3..15 contra la")
print("sucesion publicada, y nuevas_abs(t+1) = N_t(1,1) en los 16 niveles).")
print("La serie de las nuevas ES la masa del pre-vortice: p_t = b(t)/m_k1.")

# ---------------------------------------------------------------------------
# COMPROBACION 1: EL BFS HACIA ATRAS DESDE LA FUSION.
#   T(estado) = largo minimo de una palabra que fusiona. Predecesores de
#   cada ley, dentro de la ventana. La fusion solo nace de (1,1)-bit1.
# ---------------------------------------------------------------------------

def predecesores(k, c):
    # todos los (k', c') con transicion(k', c', bit) = (k, c) para algun bit
    p = []
    if k == 0:
        g = c
        p.append((0, 2 * g))                       # F1
        if (2 * g) % 3 == 0 and (2 * g // 3) % 2 == 0:
            p.append((0, 2 * g // 3))              # F2
        p.append((1, 2 * g + 1))                   # salida k=1, g > 0
        p.append((1, 1 - 2 * g))                   # salida k=1, g < 0 (abs)
        return p
    # N1: (k, 2c)
    p.append((k, 2 * c))
    # N2: c' = (2c - 1 + 3^k) / 3, par
    num = 2 * c - 1 + 3 ** k
    if num % 3 == 0 and (num // 3) % 2 == 0:
        p.append((k, num // 3))
    # N3 desde (k-1, impar): c' = (2c - 1)/3
    if k >= 2:
        num = 2 * c - 1
        if num % 3 == 0 and (num // 3) % 2 == 1:
            p.append((k - 1, num // 3))
    # N4 desde (k+1, impar): c' = 2c + 3^k
    p.append((k + 1, 2 * c + 3 ** k))
    if k == 1:
        # F3: g = (2c - 1)/3 impar >= 1;  F4: g = (1 - 2c)/3 impar >= 1
        num = 2 * c - 1
        if num % 3 == 0 and (num // 3) % 2 == 1 and num // 3 >= 1:
            p.append((0, num // 3))
        num = 1 - 2 * c
        if num % 3 == 0 and abs(num // 3) % 2 == 1 and num // 3 >= 1:
            p.append((0, num // 3))
    return p


def en_ventana(k, c):
    if k == 0:
        return 1 <= c <= G_BFS
    return k <= K_BFS and abs(c) <= C_BFS


T = {(1, 1): 1}                 # (1,1) fusiona en un paso (bit 1)
cola = deque([(1, 1)])
while cola:
    est = cola.popleft()
    t = T[est]
    for kp, cp in predecesores(est[0], est[1]):
        if not en_ventana(kp, cp):
            continue
        if (kp, cp) not in T:
            T[(kp, cp)] = t + 1
            cola.append((kp, cp))

print()
print("COMPROBACION 1: BFS hacia atras terminado. %d estados alcanzan la"
      % len(T))
print("fusion dentro de la ventana (k <= %d, |c| <= %d, g <= %d)."
      % (K_BFS, C_BFS, G_BFS))

# ---------------------------------------------------------------------------
# COMPROBACION 2: LA REJILLA ENTERA FUSIONA.
#   Todo estado del nucleo k <= K_REJILLA, |c| <= C_REJILLA (c != 0 o no:
#   c = 0 incluido) y toda frontera g <= G_REJILLA tiene que tener T
#   finito. Un estado sin T seria o un agujero de la ventana (ampliar) o
#   UN ESTADO QUE NO PUEDE FUSIONAR -- y eso tumbaria phi = 1.
# ---------------------------------------------------------------------------

sin_camino = []
for k in range(1, K_REJILLA + 1):
    for c in range(-C_REJILLA, C_REJILLA + 1):
        if (k, c) not in T:
            sin_camino.append((k, c))
for g in range(1, G_REJILLA + 1):
    if (0, g) not in T:
        sin_camino.append((0, g))

if sin_camino:
    print()
    print("C2: %d estados de la rejilla SIN camino a fusion en la ventana."
          % len(sin_camino))
    for e in sin_camino[:20]:
        print("   ", e)
    raise SystemExit("C2: rejilla no cubierta -- ampliar ventana o "
                     "investigar si son estados que no fusionan")

print()
print("COMPROBACION 2 OK: TODA la rejilla fusiona -- los %d estados del"
      % ((2 * C_REJILLA + 1) * K_REJILLA + G_REJILLA))
print("nucleo k <= %d, |c| <= %d y la frontera g <= %d tienen palabra"
      % (K_REJILLA, C_REJILLA, G_REJILLA))
print("finita hacia la fusion. La pieza (iii) vale en esta rejilla, con")
print("T = %d como cota del bloque." % max(T[e] for e in T
                                           if e[0] <= K_REJILLA and
                                           (e[0] >= 1 and abs(e[1]) <= C_REJILLA
                                            or e[0] == 0 and 1 <= e[1] <= G_REJILLA)))

# ---------------------------------------------------------------------------
# COMPROBACION 3: EL CRECIMIENTO DE T.
#   (a) en k = 1, el maximo de T sobre 2^(j-1) < |c| <= 2^j, por bits;
#   (b) a |c| <= 64, el maximo de T por nivel k.
#   Si T crece ~ a + b*log2|c| y ~ lineal en k, entonces T(rejilla de
#   (x, K)) ~ a + b*(K*log2(3) + log2(x)) y la minorizacion 2^(-T) se
#   degrada POLINOMIALMENTE en x: suficiente para el argumento, porque
#   (x, K) se eligen UNA vez (dependen de eps, no de t).
# ---------------------------------------------------------------------------

import math

print()
print("crecimiento de T con |c| (nucleo k = 1):")
print("   |c| en (2^(j-1), 2^j]    max T    max T / j")
j = 1
while 2 ** j <= C_REJILLA:
    lo, hi = 2 ** (j - 1), 2 ** j
    ts = [T[(1, c)] for c in range(-hi, hi + 1)
          if lo < abs(c) <= hi and (1, c) in T]
    if ts:
        print("   j = %2d                  %5d      %6.2f"
              % (j, max(ts), max(ts) / j))
    j += 1

print()
print("crecimiento de T con el nivel k (|c| <= 64):")
print("   k    max T")
for k in range(1, K_REJILLA + 1):
    ts = [T[(k, c)] for c in range(-64, 65) if (k, c) in T]
    print("  %2d    %5d" % (k, max(ts)))

# ---------------------------------------------------------------------------
# COMPROBACION 4: LA PIEZA (ii) -- LA TENSION EN LA DIRECCION DE k.
#   Barrido a PROF_TENSION midiendo, para cada k, la masa viva
#   normalizada m(k, t) = masa(k) / 2^t, y el producto m(k, t) * 2^k.
#   Si sup_t m(k, t) * 2^k esta acotado y se alcanza temprano, la
#   conjetura "h(K) ~ 2^(-K) uniforme en t" tiene soporte exacto.
#   OJO: esto es MEDIDO, no demostrado -- es el blanco del teorema que
#   falta, el analogo de Moscas para la torre.
# ---------------------------------------------------------------------------

def en_rejilla(k, c):
    return (1 <= k <= K_REJILLA and abs(c) <= C_REJILLA) or \
           (k == 0 and c <= G_REJILLA)


estados = {(0, 1): 1}
sup_por_k = {}       # k -> (max de m(k,t)*2^k, t donde se alcanza)
ultimo_por_k = {}
MG = {}              # t -> ocupacion viva de la rejilla (normalizada)
flujos = {}          # t -> (absorcion desde G, salida de G, entrada a G)
for prof in range(1, PROF_TENSION + 1):
    nuevo = {}
    f_abs = f_sale = f_entra = 0
    for (k, c), n in estados.items():
        dentro = en_rejilla(k, c)
        for bit in (0, 1):
            t = transicion(k, c, bit)
            if t[0] == 'fusion':
                if dentro:
                    f_abs += n
                continue
            clave = (t[1], t[2])
            nuevo[clave] = nuevo.get(clave, 0) + n
            dentro2 = en_rejilla(t[1], t[2])
            if dentro and not dentro2:
                f_sale += n
            elif dentro2 and not dentro:
                f_entra += n
    flujos[prof] = (f_abs / 2.0 ** prof, f_sale / 2.0 ** prof,
                    f_entra / 2.0 ** prof)
    estados = nuevo
    masa_k = {}
    mg = 0
    for (k, c), n in estados.items():
        masa_k[k] = masa_k.get(k, 0) + n
        if (k >= 1 and k <= K_REJILLA and abs(c) <= C_REJILLA) or \
           (k == 0 and c <= G_REJILLA):
            mg += n
    MG[prof] = mg / 2.0 ** prof
    for k, n in masa_k.items():
        val = n / 2.0 ** prof * 2 ** k
        if k not in sup_por_k or val > sup_por_k[k][0]:
            sup_por_k[k] = (val, prof)
        ultimo_por_k[k] = val

print()
print("la tension en k (prof %d): m(k,t) = masa_viva(k)/2^t" % PROF_TENSION)
print("   k    sup_t m(k,t)*2^k   (en t)    m(k,%d)*2^k" % PROF_TENSION)
for k in sorted(sup_por_k):
    if k <= 16:
        print("  %2d       %10.6f     %4d      %10.6f"
              % (k, sup_por_k[k][0], sup_por_k[k][1], ultimo_por_k.get(k, 0.0)))

# ---------------------------------------------------------------------------
# LA SERIE DE OCUPACION DE LA REJILLA: el objeto cuya NO-sumabilidad
# implica phi = 1 (lema de bloques del encabezado). Se imprime M_G(t)
# y el exponente local alfa_t = -d log M_G / d log t (ventana t-4..t).
# alfa <= 1 sostenido = no sumable = phi = 1 por el lema.
# ---------------------------------------------------------------------------

print()
print("ocupacion viva de la rejilla (k <= %d, |c| <= %d; g <= %d):"
      % (K_REJILLA, C_REJILLA, G_REJILLA))
print("  t      M_G(t)      alfa_t")
for t in range(2, PROF_TENSION + 1, 2):
    if t in MG:
        alfa = ""
        if t - 4 in MG and MG[t] > 0 and MG[t - 4] > 0:
            alfa = "   %7.4f" % (-(math.log(MG[t]) - math.log(MG[t - 4]))
                                 / (math.log(t) - math.log(t - 4)))
        print("%3d   %9.6f%s" % (t, MG[t], alfa))

# ---------------------------------------------------------------------------
# LOS FLUJOS DE LA REJILLA: el mecanismo detras de la caida de M_G.
#   Balance exacto: M_G(t+1) - M_G(t) = entra(t) - sale(t) - absorbe(t).
#   Si la caida de M_G es sobre todo ABSORCION (que alimenta phi) y el
#   cociente entra/sale ronda 1 (intercambio recurrente), la fuga neta
#   es chica y la no-sumabilidad de M_G es lo esperable. Si sale >>
#   entra + absorbe, hay fuga real: el escenario phi < 1.
# ---------------------------------------------------------------------------

print()
print("flujos de la rejilla por nivel (normalizados por 2^t):")
print("  t     absorbe      sale       entra     entra/sale   fuga neta/caida")
for t in range(4, PROF_TENSION + 1, 2):
    fa, fs, fe = flujos[t]
    caida = fa + fs - fe
    print("%3d   %9.6f  %9.6f  %9.6f    %7.4f      %7.4f"
          % (t, fa, fs, fe, fe / fs if fs else 0.0,
             (fs - fe) / caida if caida > 0 else 0.0))

# ---------------------------------------------------------------------------
# EL VEREDICTO, con las etiquetas de la casa.
# ---------------------------------------------------------------------------

print()
print("VEREDICTO DE LA REDUCCION:")
print("  DEMOSTRADO AQUI (por enumeracion exacta): (iii) en la rejilla --")
print("  todo estado con k <= %d, |c| <= %d (y frontera g <= %d) tiene"
      % (K_REJILLA, C_REJILLA, G_REJILLA))
print("  palabra finita a la fusion, con T medido y crecimiento suave.")
print("  EXACTO (PALOMAS): b(t) = N_t(1,1) -- las nuevas SON el pre-vortice.")
print("  MEDIDO: el frente difusivo avanza por la torre (los sup de")
print("  m(k,t)*2^k con k >= 6 se alcanzan en el ultimo nivel): la")
print("  version UNIFORME de (ii) es dudosa y el lema de bloques la")
print("  esquiva -- lo que decide es la SUMABILIDAD de M_G(t).")
print("  CORREGIDO POR LA REVISION EXTERNA (09-08, acta en el repo): la")
print("  desigualdad de Abejas es INCONDICIONAL (Kraft) y su")
print("  contrapositivo era VACUO -- M_G es sumable pase lo que pase.")
print("  El blanco no-vacuo es M_G(t)/L(t) (condicionado a vivo) o la")
print("  cadena MODIFICADA: el criterio de retorno11.py, que es la")
print("  formulacion buena del programa y aguanto la revision.")
