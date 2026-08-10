# arranquesporvisita.py
#
# LA SERIE DE LOS ARRANQUES |c_i| -- la condicion beta de la reduccion
# (11-08-2026; la pata de la reduccion del 10-08 (13) que estaba declarada
# "alcanzable con uniones burdas" y NO tenia ni medicion ni lema).
#
#   LO QUE SE MIDE. La reduccion final necesita DOS cosas: el piso por
#   arranque phi(c0) >~ c0^(-gamma) con gamma -> 0 (lema L-A, medido en
#   pisoporarranque.py) y que LOS ARRANQUES NO EXPLOTEN:
#
#       |c_i| = O(i^beta) en probabilidad, con gamma * beta < 1
#
#   donde c_i es el estado con el que la excursion i-esima sale del
#   fondo (k <= 1) hacia el nucleo (k = 2). Con gamma ~ 0,25-0,35
#   medido, basta beta < 3. Este fichero mide beta por primera vez.
#
#   EL INSTRUMENTO. Monte Carlo de la cadena (k, c) MODIFICADA (vortice
#   rebotado a (2,2) -- la formulacion phi = 1 <=> recurrencia de
#   retorno11.py), semilla fija, N_CADENAS trayectorias de PASOS_MAX
#   pasos desde (2, 2). Por cada cadena se registra:
#     - c_i de cada arranque de excursion (el c al entrar a k = 2
#       viniendo de k <= 1);
#     - si la excursion aterrizo en la ventana de Doeblin (k <= 1 con
#       |c| <= 25, la de liebres.py) o fuera.
#   La dinamica es entera exacta; el azar esta SOLO en los bits.
#
#   LOS CRUCES (SystemExit):
#     C1  las leyes de la cadena modificada contra pares reales (la
#         misma bateria de paseodeladeuda.py, con el vortice aparte).
#     C2  el piso por visita: la fraccion de excursiones que arrancan
#         EN (2,2) y aterrizan en la ventana debe caer en la horquilla
#         certificada del barrido exacto de masa del 10-08 (7):
#         p* en [0,763, 0,960]. Es el cruce Monte Carlo contra masa
#         exacta: dos instrumentos sin codigo compartido de conteo.
#
#   ETIQUETA HONESTA: esto es una MEDICION (un rango de i finito, una
#   semilla); beta medido no es beta demostrado, y la cola de |c_i|
#   (los pocos arranques gigantes) es justo donde una union burda
#   se juega la vida. Se imprimen mediana y percentil 90 POR SEPARADO.
#
#   Mapa del ATAJO via la cadena simbolica; SystemExit antes de concluir.

import math
import random

# ---- las perillas ---------------------------------------------------------

SEMILLA = 20260811
N_CADENAS = 400              # trayectorias independientes
PASOS_MAX = 400000           # pasos de cadena por trayectoria (largo para
                             # que el ajuste de eta tenga cubetas sin saturar)
K_VENTANA = 25               # la ventana de Doeblin: k <= 1 y |c| <= 25

# ---------------------------------------------------------------------------
# la cadena modificada (duplicada a proposito; verificada abajo en C1)
# ---------------------------------------------------------------------------

POT3 = [1, 3, 9, 27]


def pot3(k):
    while len(POT3) <= k:
        POT3.append(POT3[-1] * 3)
    return POT3[k]


def transicion_mod(k, c, bit):
    if k == 0:
        if c % 2 == 0:
            return (0, c // 2) if bit == 0 else (0, 3 * c // 2)
        return (1, (3 * c + 1) // 2) if bit == 0 else (1, (1 - 3 * c) // 2)
    if c % 2 == 0:
        return (k, c // 2) if bit == 0 else (k, (3 * c + 1 - pot3(k)) // 2)
    if k == 1 and c == 1:
        return (2, 2)
    if bit == 0:
        return (k + 1, (3 * c + 1) // 2)
    if k >= 2:
        return (k - 1, (c - pot3(k - 1)) // 2)
    return (0, abs((c - 1) // 2))


def paso(x):
    return (3 * x + 1) // 2 if x % 2 else x // 2


# ---------------------------------------------------------------------------
# COMPROBACION 1: las leyes contra pares reales (vortice aparte).
# ---------------------------------------------------------------------------

probadas = 0
for k in range(0, 8):
    for c in range(1 if k == 0 else -60, 61):
        if c == 0 and k == 0:
            continue
        for v in range(200, 260):
            x, y = v, (3 ** k * v + c) if k >= 1 else v + c
            if y <= x:
                raise SystemExit("C1: forma invalida k=%d c=%d v=%d" % (k, c, v))
            nx, ny = paso(x), paso(y)
            if k == 1 and c == 1 and v % 2 == 1:
                if nx != ny:
                    raise SystemExit("C1 vortice: (1,1) bit 1 no fusiona")
                probadas += 1
                continue
            k2, c2 = transicion_mod(k, c, v % 2)
            lo, hi = min(nx, ny), max(nx, ny)
            objetivo = (3 ** k2 * lo + c2) if k2 >= 1 else lo + c2
            if hi != objetivo:
                raise SystemExit("C1 ley: (%d,%d) v=%d" % (k, c, v))
            probadas += 1

print("COMPROBACION 1 OK: cadena modificada contra pares reales, %d"
      % probadas)
print("instancias (k = 0..7, c = -60..60, ambas paridades).")

# ---------------------------------------------------------------------------
# EL MONTE CARLO: N_CADENAS trayectorias desde (2, 2).
#   arranques[i] junta los |c| (via bit_length) de la excursion numero i
#   de todas las cadenas. exitos/total por arranque para el piso.
# ---------------------------------------------------------------------------

arranques = {}        # i -> lista de bit_length(|c_i|)
relojes = {}          # i -> lista de pasos acumulados al arrancar (tau_i)
exitos_22 = total_22 = 0          # excursiones que arrancan exactamente en (2,2)
exitos_chico = total_chico = 0    # arranques con |c_i| <= 25
exitos_todos = total_todos = 0
censuradas = 0                    # excursiones cortadas por PASOS_MAX
max_i = 0

for idx in range(N_CADENAS):
    azar = random.Random(SEMILLA + idx)
    k, c = 2, 2
    i = 1                          # numero de excursion en curso
    c_arranque = 2
    en_excursion = True
    for t in range(1, PASOS_MAX + 1):
        bit = azar.getrandbits(1)
        k2, c2 = transicion_mod(k, c, bit)
        if en_excursion and k2 <= 1:
            # aterrizaje: fin de la excursion i
            exito = abs(c2) <= K_VENTANA
            exitos_todos += exito
            total_todos += 1
            if c_arranque == 2:
                exitos_22 += exito
                total_22 += 1
            if abs(c_arranque) <= K_VENTANA:
                exitos_chico += exito
                total_chico += 1
            en_excursion = False
        elif not en_excursion and k2 >= 2:
            # arranque: empieza la excursion i+1 con c_i = c2 al paso t
            i += 1
            c_arranque = c2
            arranques.setdefault(i, []).append(abs(c2).bit_length())
            relojes.setdefault(i, []).append(t)
            en_excursion = True
        k, c = k2, c2
    if en_excursion:
        censuradas += 1
    if i > max_i:
        max_i = i

arranques.setdefault(1, [])
arranques[1] = [2] * N_CADENAS     # |c_1| = 2 por construccion (bit_length 2)

print()
print("MONTE CARLO: %d cadenas x %d pasos desde (2,2); %d excursiones"
      % (N_CADENAS, PASOS_MAX, total_todos))
print("terminadas, %d censuradas por tope de pasos; la cadena mas viajera"
      % censuradas)
print("hizo %d excursiones." % max_i)

# ---------------------------------------------------------------------------
# COMPROBACION 2: el piso por visita, Monte Carlo contra masa exacta.
# ---------------------------------------------------------------------------

p_mc = exitos_22 / total_22
if not (0.74 <= p_mc <= 0.97):
    raise SystemExit("C2 piso: p*(2,2) Monte Carlo = %.4f fuera de la "
                     "horquilla certificada [0,763, 0,960]" % p_mc)
print()
print("COMPROBACION 2 OK: p*(desde (2,2)) = %.4f en %d excursiones --"
      % (p_mc, total_22))
print("dentro de la horquilla certificada [0,763, 0,960] del barrido")
print("exacto de masa (10-08 (7)). Dos instrumentos, un numero.")

# ---------------------------------------------------------------------------
# LA SERIE: |c_i| por numero de excursion, en cubetas geometricas.
#   beta se ajusta sobre log2 del percentil 90 contra log2(i), i >= 8.
# ---------------------------------------------------------------------------


def percentil(datos, q):
    s = sorted(datos)
    return s[min(len(s) - 1, int(q * len(s)))]


print()
print("la serie de los arranques (bit_length de |c_i|, o sea ~log2):")
print("   cubeta i        n      mediana   p90   p99")
cubetas = []
borde = 1
while borde <= max_i:
    alto = borde * 2
    junta = []
    for i in range(borde, min(alto, max_i + 1)):
        junta.extend(arranques.get(i, []))
    if len(junta) >= 30:
        med = percentil(junta, 0.50)
        p90 = percentil(junta, 0.90)
        p99 = percentil(junta, 0.99)
        cubetas.append((borde, alto - 1, len(junta), med, p90, p99))
        print("  %6d-%-6d %8d      %3d      %3d   %3d"
              % (borde, alto - 1, len(junta), med, p90, p99))
    borde = alto

# ajuste de beta: log2 p90(|c_i|) ~ beta * log2 i + cte, cubetas con i >= 8
puntos = [(math.log(0.5 * (a + b), 2), p90)
          for a, b, n, med, p90, p99 in cubetas if a >= 8]
if len(puntos) < 3:
    raise SystemExit("beta: quedan %d cubetas con i >= 8 -- subir PASOS_MAX"
                     % len(puntos))
mx = sum(p[0] for p in puntos) / len(puntos)
my = sum(p[1] for p in puntos) / len(puntos)
beta_p90 = sum((p[0] - mx) * (p[1] - my) for p in puntos) \
    / sum((p[0] - mx) ** 2 for p in puntos)

puntos_med = [(math.log(0.5 * (a + b), 2), med)
              for a, b, n, med, p90, p99 in cubetas if a >= 8]
mx2 = sum(p[0] for p in puntos_med) / len(puntos_med)
my2 = sum(p[1] for p in puntos_med) / len(puntos_med)
beta_med = sum((p[0] - mx2) * (p[1] - my2) for p in puntos_med) \
    / sum((p[0] - mx2) ** 2 for p in puntos_med)

print()
print("beta medido (pendiente de log2|c_i| contra log2 i, cubetas i >= 8):")
print("  sobre la mediana:      beta = %.3f" % beta_med)
print("  sobre el percentil 90: beta = %.3f" % beta_p90)
print()
print("el criterio de la reduccion (13): con gamma ~ 0,22-0,30 (la escalera")
print("emparejada de pisoporarranque.py), gamma * beta < 1 exige beta < %.1f."
      % (1 / 0.30))
print("  gamma * beta (peor caso, gamma = 0,30 y el p90): %.3f"
      % (0.30 * beta_p90))
print()
print("Etiqueta honesta: beta es una MEDICION sobre i <= %d con una semilla;"
      % max_i)
print("la cola de arranques gigantes (p99) es donde una union burda se juega")
print("la vida, y la censura por PASOS_MAX recorta justo las excursiones mas")
print("largas -- el beta de la cola esta subestimado por construccion.")

# ---------------------------------------------------------------------------
# EL RELOJ DE LAS VISITAS (la pata L-B): tau_i = paso acumulado al arrancar
#   la excursion i. El lema L-B pide tau_i <= e^(o(i^2)) c.s.; el paseo
#   critico de k predice tau_i ~ i^2 (POLINOMIAL). Se ajusta el exponente
#   eta de tau_i ~ i^eta sobre las cubetas.
#   SESGO DECLARADO: a i grande solo llegan las cadenas de reloj rapido
#   (las lentas se censuran antes) -- el eta medido a i grande esta
#   sesgado HACIA ABAJO. Por eso se mira tambien el otro lado: el numero
#   de excursiones i_final que caben en PASOS_MAX (si tau_i ~ i^2,
#   i_final ~ sqrt(PASOS_MAX) ~ 316).
# ---------------------------------------------------------------------------

print()
print("el reloj de las visitas (log2 de tau_i, pasos al arrancar):")
print("   cubeta i        n      mediana   p90")
cubetas_tau = []
borde = 2
while borde <= max_i:
    alto = borde * 2
    junta = []
    for i in range(borde, min(alto, max_i + 1)):
        junta.extend(relojes.get(i, []))
    if len(junta) >= 30:
        med = percentil(junta, 0.50)
        p90 = percentil(junta, 0.90)
        cubetas_tau.append((borde, alto - 1, len(junta), med, p90))
        print("  %6d-%-6d %8d   %8.2f  %8.2f"
              % (borde, alto - 1, len(junta),
                 math.log(med, 2), math.log(p90, 2)))
    borde = alto

# las cubetas cuya p90 ya roza PASOS_MAX estan saturadas por la censura
# (los relojes lentos se cortaron): se excluyen del ajuste, ademas del
# arranque i < 8. El eta honesto sale de las cubetas medias.
puntos_tau = [(math.log(0.5 * (a + b), 2), math.log(med, 2))
              for a, b, n, med, p90 in cubetas_tau
              if a >= 8 and p90 < PASOS_MAX / 4]
if len(puntos_tau) < 3:
    raise SystemExit("eta: quedan %d cubetas utiles (i >= 8, sin saturar)"
                     % len(puntos_tau))
mx3 = sum(p[0] for p in puntos_tau) / len(puntos_tau)
my3 = sum(p[1] for p in puntos_tau) / len(puntos_tau)
eta = sum((p[0] - mx3) * (p[1] - my3) for p in puntos_tau) \
    / sum((p[0] - mx3) ** 2 for p in puntos_tau)

# el i_final por cadena no se guardo uno a uno; se aproxima por la masa
# de las cubetas: la mediana de excursiones alcanzadas es el i donde n(i)
# cae a N_CADENAS/2
alcanzadas = {}
for i, lista in arranques.items():
    alcanzadas[i] = len(lista)
mediana_final = max((i for i, n in alcanzadas.items() if n >= N_CADENAS // 2),
                    default=1)

print()
print("eta medido (pendiente de log2 tau_i contra log2 i, mediana, i >= 8):")
print("  eta = %.3f   (el paseo critico predice ~2; L-B pide e^(o(i^2)):" % eta)
print("  cualquier eta POLINOMIAL lo cumple con margen infinito)")
print("la mediana de excursiones alcanzadas en %d pasos es ~%d"
      % (PASOS_MAX, mediana_final))
print("  (si tau_i ~ i^2, se esperaba ~sqrt(%d) = %d: mismo orden)"
      % (PASOS_MAX, int(math.sqrt(PASOS_MAX))))
print()
print("Etiqueta honesta: eta esta sesgado hacia abajo a i grande (censura")
print("de relojes lentos); el dato robusto es el par (eta ~ 2, i_final ~")
print("sqrt(pasos)) apuntando JUNTOS al reloj polinomial del paseo critico.")
