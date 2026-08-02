# atacacst.py
#
# EL ATAQUE A LA CONJETURA CST (Terras 1976), AUTOCONTENIDO.
#
#   sigma(n)  = primer k con T^k(n) < n          (la parada de verdad, atajo)
#   sigma*(n) = primer k con 2^k > 3^{S_k(n)}    (solo el coeficiente)
#
#   Siempre sigma* <= sigma. CST dice que son IGUALES para todo n >= 2.
#   Si CST es cierta, no hay ciclos no triviales.
#
# LA PALANCA, y es la identidad de Terras del repo:
#
#   T^k(2^k*m + r) = 3^{S}*m + T^k(r)     con S = S_k(r)   (recta en m)
#
#   Si en la clase r el coeficiente cae en el paso k (3^S < 2^k), la bajada
#   REAL  T^k(n) < n  equivale a  3^S*m + t < 2^k*m + r  con t = T^k(r),
#   o sea  (2^k - 3^S)*m > t - r.  Como 2^k - 3^S >= 1, eso se cumple para
#   TODO m > t - r.  LUEGO EL FALLO DE CST EN ESA CLASE SOLO PUEDE VIVIR EN
#   m <= t - r: UN TRAMO FINITO Y CALCULABLE. Se revisan esos m uno a uno y
#   la clase queda DECIDIDA PARA SUS INFINITOS NUMEROS.
#
#   Este programa recorre todas las clases mod 2^k, k = 1..K_MAX, y decide
#   CST para todo n >= 2 con sigma*(n) <= K_MAX -- sin asumir ningun barrido
#   ajeno, sin X0 importado, sin floats. El companero atacacst.lean demuestra
#   la palanca en Lean 4 para todo k, todo r y todo m.
#
# QUE NO ES: no demuestra CST (las clases supervivientes -3^S >= 2^k- siguen
# vivas para todo K, y a(k) >= 1 lo garantiza: la criba nunca se vacia).
# Acota donde puede fallar, y decide un tramo infinito de casos.

K_MAX = 27          # nivel maximo de la criba (memoria ~ a(K_MAX) clases).
                    # 27 a proposito: es el primer jump value grande de la
                    # Tabla C (2^27/3^17 = 1,039), donde el denominador
                    # 2^k - 3^S se hace chico y el tramo finito puede abrirse.
K_CRUZA = 12        # hasta aqui se cruza contra fuerza bruta por clase

import sys

def atajo(n):
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2

# ---------------------------------------------------------------- COMPROBACION 1
# La identidad-palanca, contra iteracion cruda: 2.000 casos al azar reproducible.
import random
random.seed(2026)
for _ in range(2000):
    k = random.randint(1, 14)
    r = random.randint(0, 2 ** k - 1)
    m = random.randint(0, 50)
    S = 0
    t = r
    for _ in range(k):
        S += t % 2
        t = atajo(t)
    n = 2 ** k * m + r
    x = n
    for _ in range(k):
        x = atajo(x)
    if x != 3 ** S * m + t:
        raise SystemExit("COMPROBACION 1 ROTA: la identidad falla en k=%d r=%d m=%d" % (k, r, m))
print("COMPROBACION 1 OK: la identidad T^k(2^k*m+r) = 3^S*m + T^k(r), 2.000 casos, 0 fallos")

# ---------------------------------------------------------------- LA CRIBA
# survivors: clases (r, S, t) con el coeficiente todavia >= 1 (3^{S_j} >= 2^j
# para todo j <= k). Al doblar el modulo, cada clase r se parte en r y r+2^k,
# y el bit siguiente sale de la paridad de 3^S*b + t (b = 0 o 1), sin volver
# a iterar la trayectoria: O(1) por clase y por nivel.

survivors = [(0, 0, 0)]        # k = 0: la clase unica, S_0 = 0, T^0(0) = 0
pot2 = 1                       # 2^k
candidatos_revisados = 0
peor_tramo = 0                 # el t - r mas grande visto (tamano del tramo finito)
contraejemplos = []
a_serie = []

for k in range(1, K_MAX + 1):
    nuevos = []
    caen = []                  # clases cuyo coeficiente cae exactamente en k
    for (r, S, t) in survivors:
        for b in (0, 1):
            r2 = r + pot2 * b
            base = 3 ** S * b + t          # T^k(n) para n = r2 (m interno 0)
            bit = base % 2
            S2 = S + bit
            t2 = (3 * base + 1) // 2 if bit else base // 2
            if 3 ** S2 >= 2 * pot2:
                nuevos.append((r2, S2, t2))
            else:
                caen.append((r2, S2, t2))
    pot2 *= 2                  # ahora 2^k
    # decidir cada clase caida: el fallo solo puede vivir en m <= t2 - r2
    con_tramo = 0
    for (r2, S2, t2) in caen:
        tramo = t2 - r2
        if tramo >= 0 and r2 >= 2:
            con_tramo += 1
        if tramo > peor_tramo:
            peor_tramo = tramo
        m = 0
        while m <= tramo:      # si t2 <= r2 solo se mira m = 0
            n = pot2 * m + r2
            if n >= 2:
                candidatos_revisados += 1
                x = n
                for _ in range(k):
                    x = atajo(x)
                if x >= n:
                    contraejemplos.append((n, k))
            m += 1
    survivors = nuevos
    a_serie.append(len(survivors))
    if con_tramo:
        print("   k=%2d: %d clases caidas con tramo >= 0 (candidatas de verdad)" % (k, con_tramo))

print("COMPROBACION 2 (la decision): %d candidatos finitos revisados en k = 1..%d"
      % (candidatos_revisados, K_MAX))
print("   tramo finito mas grande (max t - r): %d" % peor_tramo)
if contraejemplos:
    raise SystemExit("CONTRAEJEMPLO DE CST: %r" % contraejemplos[:10])
print("   contraejemplos de CST encontrados: 0")

# ---------------------------------------------------------------- COMPROBACION 3
# Cruce contra fuerza bruta pura: para k <= K_CRUZA, TODAS las clases mod 2^k
# recalculadas desde cero (sin la criba incremental), y la misma decision.
pot = 1
sobreviven_bruto = []
for k in range(1, K_CRUZA + 1):
    pot *= 2
    vivos = 0
    for r in range(pot):
        S = 0
        t = r
        ok = True
        for j in range(1, k + 1):
            S += t % 2
            t = atajo(t)
            if 3 ** S < 2 ** j:
                ok = False
                break
        if ok:
            vivos += 1
    sobreviven_bruto.append(vivos)
if sobreviven_bruto != a_serie[:K_CRUZA]:
    raise SystemExit("COMPROBACION 3 ROTA: la criba incremental no cuadra con la bruta: %r vs %r"
                     % (sobreviven_bruto, a_serie[:K_CRUZA]))
print("COMPROBACION 3 OK: criba incremental == fuerza bruta, k = 1..%d: %r"
      % (K_CRUZA, a_serie[:K_CRUZA]))

# ---------------------------------------------------------------- COMPROBACION 4
# Control directo sobre numeros de verdad: sigma(n) == sigma*(n) calculados
# los dos por definicion, n = 2..100.000. (Esto NO es el teorema: es la red
# de seguridad de que las definiciones de arriba son las de verdad.)
def sigma_directo(n):
    x = n
    k = 0
    while True:
        k += 1
        x = atajo(x)
        if x < n:
            return k

def sigma_estrella_directo(n):
    x = n
    S = 0
    k = 0
    while True:
        k += 1
        S += x % 2
        x = atajo(x)
        if 2 ** k > 3 ** S:
            return k

for n in range(2, 100001):
    if sigma_directo(n) != sigma_estrella_directo(n):
        raise SystemExit("COMPROBACION 4 ROTA: sigma != sigma* en n = %d" % n)
print("COMPROBACION 4 OK: sigma == sigma* por definicion directa, n = 2..100.000")

# ---------------------------------------------------------------- EL RESULTADO
print()
print("=" * 74)
print("RESULTADO: para todo n >= 2 con sigma*(n) <= %d, se cumple" % K_MAX)
print("           sigma(n) = sigma*(n).  DECIDIDO, no muestreado: cada clase")
print("           mod 2^k donde el coeficiente cae queda cerrada para sus")
print("           INFINITOS numeros revisando un tramo finito (m <= t - r).")
print("           Clases vivas al final (a(%d) de la criba): %d -- esas no" % (K_MAX, a_serie[-1]))
print("           afirman nada todavia: su sigma* es > %d." % K_MAX)
print("           La palanca esta demostrada en Lean para todo k, r, m:")
print("           atacacst.lean (nucleo, sin Mathlib, sin sorryAx).")
print("=" * 74)
