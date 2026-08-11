# rachasreales.py
#
# LA DOMINACION GEOMETRICA DE LAS RACHAS REALES -- el input del lema
# de racha de la transferencia P2 (11-08-2026 (2), quinta pasada;
# sigue a medianareal.py y a la pista LTE: v2(3^k - 1) = 1 (k impar)
# / 2 + v2(k) (k par), asi que A = v2(3^k - 1) <= 2 + log2(k) y las
# ventanas heladas del mecanismo de L2 son O(log k)).
#
#   QUE MIDE. En excursiones reales (2, c0) -> fondo (dinamica
#   entera exacta, bits de Terras), el largo de cada RACHA de pasos
#   compartidos (k quieto) que sigue a cada paso mixto. La
#   transferencia V2b -> real pide que esas rachas esten dominadas
#   por geometricas: P(racha >= j) <= C * 2^-j con C uniforme
#   (modulo el offset A = O(log k) que LTE acota).
#
#   COMPROBACIONES (SystemExit):
#     C1  la cola global: C_j := P(racha >= j) * 2^j acotada por
#         C_TOPE = 8 para todo j <= J_MAX con muestra suficiente
#         (el sesgo v2 medido por la 8a era x1,8 saturando: se
#         espera C_j ~ 2-4).
#     C2  el offset es chico y LOCAL: en la franja k >= 9 el C_j
#         maximo no supera al de la franja k <= 3 por mas de x4
#         (el offset A crece como log k: a k <= 2000 es <= 12,
#         y en las alturas tipicas de la excursion, <= 6).
#     C3  la media de racha esta cerca del 1 del reloj geometrico
#         puro (E[Geom(1/2)] = 1): media global en [0,5, 2,5].
#
#   Semilla fija; los largos se recogen de TODAS las excursiones
#   (la dominacion del reloj no se condiciona a sobrevivir).

import random
import math

C0 = 999983                # primo, impar, % 3 != 0 (como medianareal)
N_EXCURSIONES = 150000
T_MAX = 600
J_MAX = 12                 # cola medida hasta aqui
MINIMO_MUESTRA = 200       # C_j solo se exige con muestra suficiente
C_TOPE = 8.0
SEMILLA = 20260814
FRANJAS = [(1, 3), (4, 8), (9, 99)]


def pot3(k, _cache={0: 1}):
    if k not in _cache:
        _cache[k] = 3 ** k
    return _cache[k]


def transicion(k, c, bit):
    if k == 0:
        if c % 2 == 0:
            return (0, c // 2) if bit == 0 else (0, 3 * c // 2)
        return (1, (3 * c + 1) // 2) if bit == 0 else (1, (1 - 3 * c) // 2)
    if c % 2 == 0:
        return (k, c // 2) if bit == 0 else (k, (3 * c + 1 - pot3(k)) // 2)
    if bit == 0:
        return (k + 1, (3 * c + 1) // 2)
    if k >= 2:
        return (k - 1, (c - pot3(k - 1)) // 2)
    g = (c - 1) // 2
    if g == 0:
        return None
    return (0, abs(g))


azar = random.Random(SEMILLA)
rachas_global = {}
rachas_franja = {f: {} for f in FRANJAS}
total_rachas = 0
suma_largos = 0
for _ in range(N_EXCURSIONES):
    k, c = 2, C0
    racha = None           # largo de la racha compartida en curso
    k_racha = None
    for t in range(T_MAX):
        k0 = k
        r = transicion(k, c, azar.getrandbits(1))
        if r is None:
            break
        k, c = r
        if k == k0 and k0 >= 1:
            # paso compartido: alarga la racha en curso
            if racha is not None:
                racha += 1
        else:
            # paso mixto (o frontera): cierra la racha anterior...
            if racha is not None:
                rachas_global[racha] = rachas_global.get(racha, 0) + 1
                total_rachas += 1
                suma_largos += racha
                for f in FRANJAS:
                    if f[0] <= k_racha <= f[1]:
                        rachas_franja[f][racha] = \
                            rachas_franja[f].get(racha, 0) + 1
            # ...y abre la siguiente (la que sigue a ESTE mixto)
            racha = 0
            k_racha = k
        if k <= 1:
            break

print("LA DOMINACION GEOMETRICA DE LAS RACHAS REALES (input de P2)")
print("%d excursiones desde (2, %d); %d rachas medidas; media %.3f"
      % (N_EXCURSIONES, C0, total_rachas, suma_largos / float(total_rachas)))
print()


def cola(tabla):
    n = sum(tabla.values())
    acum = {}
    vivos = n
    for j in range(0, J_MAX + 1):
        acum[j] = vivos / float(n) if n else 0.0
        vivos -= tabla.get(j, 0)
    return n, acum


n_g, cola_g = cola(rachas_global)
print("la cola global: j, P(racha >= j), C_j = P * 2^j, muestra 2^j-esima")
peor_C = 0.0
for j in range(1, J_MAX + 1):
    muestra_j = cola_g[j] * n_g
    Cj = cola_g[j] * (2 ** j)
    marca = ""
    if muestra_j >= MINIMO_MUESTRA:
        peor_C = max(peor_C, Cj)
    else:
        marca = "   (muestra fina: no se exige)"
    print("  j = %2d:  P = %.6f   C_j = %.3f   (n ~ %d)%s"
          % (j, cola_g[j], Cj, int(muestra_j), marca))
if peor_C > C_TOPE:
    raise SystemExit("C1: C_j = %.2f > %.1f -- la cola NO es geometrica"
                     % (peor_C, C_TOPE))
print("COMPROBACION 1 OK: C_j <= %.2f <= %.1f en toda la cola con"
      % (peor_C, C_TOPE))
print("muestra: P(racha >= j) <= C * 2^-j -- la dominacion geometrica")
print("de las rachas reales, medida (la 8a habia visto el x1,8).")
print()

print("por franjas de k (el offset A = O(log k) de LTE):")
peores = {}
for f in FRANJAS:
    n_f, cola_f = cola(rachas_franja[f])
    peor = 0.0
    for j in range(1, J_MAX + 1):
        if cola_f[j] * n_f >= MINIMO_MUESTRA:
            peor = max(peor, cola_f[j] * 2 ** j)
    peores[f] = peor
    print("  k en [%d, %d]: %7d rachas, C_j maximo %.3f"
          % (f[0], f[1], n_f, peor))
if peores[FRANJAS[2]] > 4.0 * max(peores[FRANJAS[0]], 0.5):
    raise SystemExit("C2: el C_j de k >= 9 (%.2f) supera x4 al de "
                     "k <= 3 (%.2f)" % (peores[FRANJAS[2]],
                                        peores[FRANJAS[0]]))
print("COMPROBACION 2 OK: el offset por altura es chico (LTE lo predice")
print("logaritmico; las alturas tipicas llevan A <= 6).")
media = suma_largos / float(total_rachas)
if not (0.5 <= media <= 2.5):
    raise SystemExit("C3: media de racha %.3f fuera de [0,5, 2,5]" % media)
print("COMPROBACION 3 OK: media de racha %.3f ~ el 1 del reloj" % media)
print("geometrico puro de V2b.")
print()
print("Lectura: el lema de racha de P2 (dominacion estocastica del")
print("reloj real por geometricas con offset O(log k)) tiene sus dos")
print("mitades medidas: la cola C * 2^-j aqui, el offset LTE por")
print("aritmetica. El paso analitico es escribir la dominacion desde")
print("los lemas v2 de tortolas.lean/aterrizajen2.lean. Medicion.")
