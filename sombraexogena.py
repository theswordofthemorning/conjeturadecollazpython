# sombraexogena.py
#
# LA PRUEBA DE CIRCULARIDAD DE L-A (11-08-2026; idea del usuario: escribir
# L-A como enunciado autonomo -- paseo perezoso y excursiones, sin Collatz
# ni cadena -- y ver si lo que queda es "el paseo es recurrente" u otra
# cosa genuinamente mas debil).
#
#   AL ESCRIBIRLO, EL ENUNCIADO SE ESTRATIFICA EN TRES, segun cuanta
#   estructura de la cadena conserva -- y eso lo vuelve un EXPERIMENTO:
#
#   V1 (paseo y perpetuidad INDEPENDIENTES, reloj exogeno): la excursion
#      de un paseo justo perezoso decide CUANDO termina; una perpetuidad
#      critica {u/2, (3u-1)/2} con monedas PROPIAS decide cuanto
#      contrajo. Sin acoplamiento. El analisis clasico da
#      phi(x) ~ (log x)^(-1/2) -- LA FORMA QUE LA 7a REVISION EXCLUYO
#      en la cadena real. Si V1 difiere de la real, el acoplamiento
#      importa.
#
#   V2 (EL ACOPLAMIENTO DEL BIT, reloj exogeno): el MISMO bit que mueve
#      el paseo elige el mapa de u -- bit 0: k sube y u contrae x1/2;
#      bit 1: k baja y u expande x3/2 (la estructura exacta de N3/N4).
#      El reloj (que pasos son mixtos) es exogeno: V2a moneda justa por
#      paso, V2b rachas geometricas (la foto sin aritmetica del reloj
#      v2 de la cadena). ESTE es el enunciado autonomo honesto de L-A:
#      pura probabilidad clasica, cero aritmetica.
#
#   V3 (control): la cadena REAL (k, c) modificada por Monte Carlo, la
#      misma semantica del barrido exacto de pisoporarranque.py -- para
#      validar el Monte Carlo contra la masa exacta.
#
#   EL VEREDICTO QUE SE BUSCA:
#     - si phi_V2(x) decae POLINOMIAL con gamma cayendo (como la real):
#       el fenomeno es probabilistico puro => L-A autonoma es un
#       problema clasico bien planteado => EL MURO ES DE UN METRO.
#     - si phi_V2(x) decae ~1/sqrt(log x) (como el analisis naive
#       predice): toda la dificultad extra de la cadena vive en el
#       RELOJ ENDOGENO (la aritmetica v2 que TORTOLAS describe) => la
#       version autonoma debil es FALSA para la cadena y el enunciado
#       de L-A no se deja despegar de la aritmetica: el muro es el de
#       siempre, visto de frente. (Y se ahorran meses de atacar V2.)
#
#   Semantica de la excursion (identica a pisoporarranque.py): arranque
#   en k = 2 con u0 = c0/9; la excursion termina al pisar k <= 1;
#   exito si aterriza con |u| <= 25/3 (la ventana de Doeblin |c| <= 25
#   en k = 1). Horizonte T_MAX emparejado; censuradas contadas aparte.
#
#   Monte Carlo con semilla fija; el azar SOLO en los bits.

import math
import random

# ---- las perillas ---------------------------------------------------------

SEMILLA = 20260811
X_LISTA = [2000, 20000, 200000, 2000000]   # los mismos c0 de la escalera
N_CADENAS = 200000            # excursiones por punto y por modelo
T_MAX = 150                   # horizonte emparejado (el de la escalera)
U_VENTANA = 25.0 / 3.0        # |u| <= 25/3  <=>  |c| <= 25 en k = 1

# los phi_min certificados por el barrido exacto a T = 130 (bitacora
# 10-08 (16)), para el cruce del control V3 (el MC debe caer cerca;
# el barrido es cota inferior del truncado, el MC estima el mismo
# truncado a T_MAX = 150, un poco mayor)
PHI_BARRIDO_130 = {2000: 0.1182, 20000: 0.0586, 200000: 0.0354}


def pot3(k, _cache=[1, 3, 9, 27]):
    while len(_cache) <= k:
        _cache.append(_cache[-1] * 3)
    return _cache[k]


# ---------------------------------------------------------------------------
# V3: la cadena real (k, c) modificada -- el control del Monte Carlo.
#   Duplicada a proposito de pisoporarranque.py (regla de la casa).
# ---------------------------------------------------------------------------


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


def excursion_v3(azar, c0, t_max):
    # devuelve 'exito' / 'fallo' / 'censura'
    k, c = 2, c0
    for _ in range(t_max):
        k, c = transicion_mod(k, c, azar.getrandbits(1))
        if k <= 1:
            return 'exito' if abs(c) <= 25 else 'fallo'
    return 'censura'


# ---------------------------------------------------------------------------
# V2: el enunciado autonomo -- acoplamiento del bit, reloj exogeno.
#   mixto:  bit 0 -> k+1, u <- u/2   |   bit 1 -> k-1, u <- (3u-1)/2
#   compartido: bit 0 -> u <- u/2    |   bit 1 -> u <- (3u-1)/2
#   (los delta ~ 3^-k/2 de Aranas se omiten: son < 1/18 en k >= 2 y
#   no cambian la forma del decaimiento -- etiqueta declarada)
#   V2a: cada paso es mixto con moneda justa independiente.
#   V2b: rachas -- tras cada mixto, largo compartido ~ Geometrica(1/2)
#        (P(j) = 2^-(j+1)), la foto sin aritmetica del reloj v2.
# ---------------------------------------------------------------------------


def excursion_v2(azar, u0, t_max, rachas):
    k, u = 2, u0
    compartidos = 0           # pasos compartidos pendientes antes del mixto
    if rachas:
        # la primera racha compartida, geometrica(1/2)
        j = 0
        while azar.getrandbits(1):
            j += 1
        compartidos = j
    for t in range(t_max):
        bit = azar.getrandbits(1)
        if rachas:
            es_mixto = (compartidos == 0)
            if es_mixto:
                j = 0
                while azar.getrandbits(1):
                    j += 1
                compartidos = j
            else:
                compartidos -= 1
        else:
            es_mixto = azar.getrandbits(1) == 1
        u = u / 2.0 if bit == 0 else (3.0 * u - 1.0) / 2.0
        if es_mixto:
            k += 1 if bit == 0 else -1
            if k <= 1:
                return 'exito' if abs(u) <= U_VENTANA else 'fallo'
    return 'censura'


# ---------------------------------------------------------------------------
# V1: el control SIN acoplamiento -- el paseo usa su propio bit y la
#   perpetuidad el suyo. Todo lo demas identico a V2a.
# ---------------------------------------------------------------------------


def excursion_v1(azar, u0, t_max):
    k, u = 2, u0
    for t in range(t_max):
        bit_paseo = azar.getrandbits(1)
        bit_u = azar.getrandbits(1)
        es_mixto = azar.getrandbits(1) == 1
        u = u / 2.0 if bit_u == 0 else (3.0 * u - 1.0) / 2.0
        if es_mixto:
            k += 1 if bit_paseo == 0 else -1
            if k <= 1:
                return 'exito' if abs(u) <= U_VENTANA else 'fallo'
    return 'censura'


# ---------------------------------------------------------------------------
# EL EXPERIMENTO
# ---------------------------------------------------------------------------

modelos = [
    ('V1 sin acople', lambda azar, x: excursion_v1(azar, x / 9.0, T_MAX)),
    ('V2a acople', lambda azar, x: excursion_v2(azar, x / 9.0, T_MAX, False)),
    ('V2b rachas', lambda azar, x: excursion_v2(azar, x / 9.0, T_MAX, True)),
    ('V3 cadena', lambda azar, x: excursion_v3(azar, x, T_MAX)),
]

print("la prueba de circularidad: phi(x) por modelo, %d excursiones/punto,"
      % N_CADENAS)
print("horizonte T = %d, ventana |u| <= 25/3 (|c| <= 25 en k = 1)" % T_MAX)
print()
resultados = {}
for nombre, correr in modelos:
    fila = {}
    for x in X_LISTA:
        azar = random.Random(SEMILLA * 7 + hash((nombre, x)) % 10 ** 6)
        exitos = censuras = 0
        for _ in range(N_CADENAS):
            r = correr(azar, x)
            if r == 'exito':
                exitos += 1
            elif r == 'censura':
                censuras += 1
        fila[x] = (exitos / N_CADENAS, censuras / N_CADENAS)
    resultados[nombre] = fila
    linea = "  %-14s" % nombre
    for x in X_LISTA:
        linea += "  phi(%7d)=%.4f (cens %.3f)" % (x, fila[x][0], fila[x][1])
    print(linea)

# ---------------------------------------------------------------------------
# COMPROBACION 1: V3 (Monte Carlo de la cadena real) contra el barrido
#   exacto de masa. El MC a T=150 debe quedar >= el phi_min certificado
#   a T=130 y cerca de el (misma distribucion, mas horizonte, sin poda).
#   Tolerancia: [phi_130 - 3 err.std., phi_130 + 0.05].
# ---------------------------------------------------------------------------

for x, phi130 in sorted(PHI_BARRIDO_130.items()):
    phi_mc = resultados['V3 cadena'][x][0]
    err = 3 * math.sqrt(phi_mc * (1 - phi_mc) / N_CADENAS)
    if not (phi130 - err <= phi_mc <= phi130 + 0.05):
        raise SystemExit("C1: V3 MC phi(%d) = %.4f fuera del entorno del "
                         "barrido exacto %.4f" % (x, phi_mc, phi130))
print()
print("COMPROBACION 1 OK: el Monte Carlo de la cadena real reproduce los")
print("phi_min del barrido exacto de masa (a horizonte mayor, sin poda).")

# ---------------------------------------------------------------------------
# LA TABLA DEL VEREDICTO: gamma por decada y la forma del decaimiento.
#   gamma = log10(phi(x)/phi(10x)). Y el test de forma 1/sqrt(log):
#   si phi ~ C/sqrt(ln x), entonces phi(x)*sqrt(ln x) es constante.
# ---------------------------------------------------------------------------

print()
print("gamma por decada (y phi*sqrt(ln x), constante <=> forma 1/sqrt(log)):")
print("   modelo          g(2k->20k)  g(20k->200k)  g(200k->2M)   phi*sqrt(ln x) en la escalera")
for nombre, _ in modelos:
    fila = resultados[nombre]
    gs = []
    for a, b in zip(X_LISTA, X_LISTA[1:]):
        pa, pb = fila[a][0], fila[b][0]
        gs.append(math.log10(pa / pb) if pa > 0 and pb > 0 else float('nan'))
    forma = "  ".join("%.3f" % (fila[x][0] * math.sqrt(math.log(x)))
                      for x in X_LISTA)
    print("  %-14s   %6.3f      %6.3f       %6.3f      [%s]"
          % (nombre, gs[0], gs[1], gs[2], forma))

print()
print("LECTURA (el veredicto es del mecanismo, no de una pasada):")
print(" - si V2 (a o b) muestra gammas ~0 y phi*sqrt(ln x) ~constante,")
print("   el enunciado autonomo pierde el fenomeno: la degradacion")
print("   polinomial de la cadena viene del RELOJ ENDOGENO (aritmetica")
print("   v2) y L-A no se deja despegar de la cadena -- circularidad")
print("   parcial: atacar V2 seria atacar otro problema.")
print(" - si V2 muestra los gammas de la cadena (0,2-0,3 cayendo), L-A")
print("   es un problema de probabilidad clasica sin aritmetica dentro:")
print("   el muro es de un metro y V2 es EL enunciado a demostrar.")
print(" - V1 calibra cuanto aporta el acoplamiento; V3 valida el MC.")
