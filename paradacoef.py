# -*- coding: utf-8 -*-
#
# paradacoef.py
#
# LA CONJETURA DEL TIEMPO DE PARADA POR COEFICIENTE (CST)
# =============================================================================
#
# Terras 1976, definición 1.5 y conjetura 2.9. Lagarias la bautizó
# "coefficient stopping time conjecture". Es, de todo lo que este laboratorio ha
# mirado, lo más cercano al CUARTO CAMINO escrito por otro hace cincuenta años.
#
# -----------------------------------------------------------------------------
# EL MAPA. AQUÍ SE USA EL DEL ATAJO, Y SÓLO ÉSE
# -----------------------------------------------------------------------------
#
#     T(n) = n/2          si n es par
#     T(n) = (3n+1)/2     si n es impar
#
# El clásico (3n+1 sin dividir) daría OTROS números en cada línea de este
# fichero. Cada print dice qué mapa usa. El control usa
#
#     U(n) = n/2          si n es par
#     U(n) = (3n-1)/2     si n es impar
#
# que es Collatz sobre los enteros negativos vuelto del revés.
#
# -----------------------------------------------------------------------------
# LAS DOS CANTIDADES
# -----------------------------------------------------------------------------
#
#     sigma(x)  = min{ k >= 1 : T^k(x) < x }             el tiempo de caída REAL
#     sigma*(x) = min{ k >= 1 : 2^k > 3^{m_k(x)} }       sólo el COEFICIENTE
#
# con m_k(x) = cuántos de los k primeros pasos fueron impares.
#
# CST:  sigma*(x) = sigma(x)  para todo x >= 2.
#
# Falla en x = 1, y por eso la conjetura dice "x >= 2": T(1)=2, T(2)=1, el 1
# nunca baja de sí mismo, luego sigma(1) = infinito; pero su vector de paridad
# es I,E, o sea m_2 = 1 y 2^2 = 4 > 3, luego sigma*(1) = 2. El único ciclo del
# 3n+1 ES el único contraejemplo conocido a CST.
#
# -----------------------------------------------------------------------------
# POR QUÉ ESTA VÍA Y NO OTRA: EL DETECTOR DE CONTABILIDAD
# -----------------------------------------------------------------------------
#
# El repo descartó hoy gamma(rho), Res >= 1 y el argumento de la moneda con un
# detector: si un enunciado sólo se puede evaluar sobre trayectorias que YA
# llegaron a 1, no es un criterio, es contabilidad.
#
# sigma* PASA el detector, y es lo único que se ha medido aquí que lo pase:
#
#     sigma*(x) se calcula ENTERO a partir de x mod 2^k, sin conocer x, y sin
#     seguir la trayectoria hasta el final. Si sigma*(x) = s, ese valor ya
#     estaba escrito en los s bits bajos de x.
#
# Eso es la comprobación 1, y es la razón de todo el fichero. sigma, en cambio,
# compara VALORES: para eso hace falta x. La conjetura CST dice que las dos
# cosas coinciden, o sea que un dato de trayectoria es en realidad un dato de
# resto. Ése es literalmente el enunciado del cuarto camino.
#
# -----------------------------------------------------------------------------
# LA IDENTIDAD QUE LO GOBIERNA TODO (Terras 1.1, la del repo)
# -----------------------------------------------------------------------------
#
#     2^k * T^k(x) = 3^{m_k} * x + c_k          con  c_0 = 0
#     paso par:    c -> c
#     paso impar:  c -> 3c + 2^{k}              (k = pasos ya dados)
#
# c_k >= 0 SIEMPRE, y ahí está el "+1". De ahí sale, en una línea:
#
#     T^k(x) < x  =>  3^{m_k} x + c_k < 2^k x  =>  3^{m_k} < 2^k  =>  sigma* <= sigma
#
# LA DIFERENCIA sigma - sigma* ES EXACTAMENTE EL "+1": sigma* mira sólo el
# coeficiente 3^{m_k}/2^k e ignora c_k; sigma incluye los dos. Y como c_k >= 0,
# ignorarlo sólo puede hacer que la desigualdad se declare ANTES. El margen es
# medible clase a clase, y es la MEDIDA 2 de este fichero:
#
#     CST falla en x  <=>  x <= c_k / (2^k - 3^{m_k})   con k = sigma*(x)
#
# El lado derecho depende SÓLO del resto de x módulo 2^k. O sea: dentro de cada
# clase residual los contraejemplos son los elementos PEQUEÑOS, y son finitos y
# calculables. Eso convierte "comprobar CST" en un barrido de clases, no de
# números.
#
# -----------------------------------------------------------------------------
# ES UNA COTA, NO UN PROMEDIO
# -----------------------------------------------------------------------------
#
# De la desigualdad de arriba, con una acotación de c_k que se demuestra en
# cinco líneas y se verifica exhaustivamente aquí, sale:
#
#     si x >= 2 es contraejemplo de CST y sigma*(x) = k, entonces
#
#         x  <  B(k) = k * 3^{m*} / (2 * (2^k - 3^{m*}))
#
#     con 3^{m*} la mayor potencia de 3 por debajo de 2^k.
#
# B(k) es calculable con enteros exactos para cualquier k. Y entonces una
# verificación por fuerza bruta hasta X0 demuestra que NO HAY contraejemplo con
# sigma*(x) <= K, para todo K con max_{j<=K} B(j) <= X0. Eso NO es "comprobado
# hasta X0": es un enunciado sobre infinitos números, incluidos números
# gigantescos, y tiene forma de teorema.
#
# -----------------------------------------------------------------------------
# EL CONTROL A/B, QUE ES LO QUE DECIDE SI ESTO SIRVE
# -----------------------------------------------------------------------------
#
# El repo exige medir toda cantidad también sobre 3n-1, porque el signo del +1
# es lo que convierte un mapa con UN ciclo en uno con TRES. Aquí el control sale
# con una respuesta más fina que "sirve" o "no sirve", y está en la MEDIDA 4:
#
#   - La IGUALDAD sigma = sigma* se cumple también en 3n-1. Es ciega al signo.
#   - Pero la DIRECCIÓN de la desigualdad se DA LA VUELTA, y eso es demostrable:
#     en 3n-1 el análogo de c_k es <= 0, luego allí sigma <= sigma*.
#   - Y lo que de verdad separa los dos mapas no es la igualdad sino la
#     FINITUD de sigma*: en 3n-1 hay x >= 2 con sigma* = infinito (los mínimos
#     de los tres ciclos), y en 3n+1 no se conoce ninguno.
#
# Además se demuestra aquí POR QUÉ la mitad del coeficiente tiene que ser ciega:
# el espejo n -> -n manda 3n-1 sobre positivos a 3n+1 sobre negativos, conserva
# la paridad, y por tanto conserva el vector de paridad y todo lo que se calcule
# de él. CUALQUIER cantidad que sea función sólo del vector de paridad da lo
# mismo en los dos mapas, POR TEOREMA, y correr el A/B sobre ella no informa de
# nada. Eso incluye sigma*, incluye el conteo de clases supervivientes, y
# —comprobado aquí— incluye la sucesión a(k) de clasesfusion.py, cuya igualdad
# entre los dos mapas se midió hoy y resulta ser forzosa.
#
# -----------------------------------------------------------------------------
# BIBLIOGRAFÍA, CON EL ESTADO DE VERIFICACIÓN DE CADA COSA
# -----------------------------------------------------------------------------
#
# [VERIFICADO, leído en OEIS A126241, comentario del propio índice]
#   "Terras defines a coefficient stopping time (definition 1.5) tau(n) = d
#    which is the smallest d for which 3^u/2^d < 1 ... Clearly tau(n) <= a(n),
#    and Terras conjectures (conjecture 2.9) that tau(n) = a(n) for n >= 2."
#   A126241 es la sucesión de los tiempos de caída del mapa del atajo.
#
# [LEÍDO, NO VERIFICADO] Que Lagarias la bautizara "coefficient stopping time"
#   aparece en varias fuentes secundarias; no se ha visto el texto de Lagarias.
#
# [AVISO, y es el mismo del que este repo ya se quemó hoy] Existe un artículo de
#   2025 en SCIRP (Adv. Pure Math. / journal de la misma casa) que afirma
#   DEMOSTRAR "sigma(s) = omega(s) para todo s" y deducir que no hay ciclos no
#   triviales. No está arbitrado en ningún sitio serio, y la casa editorial es
#   la misma cuya cita de 19.478.780.533 hubo que retirar. Aquí se trata como
#   NO DEMOSTRADO. CST se sigue considerando abierta.
#
# [OBSERVACIÓN PROPIA] El comentario de K. Spage en A126241 dice, sin reservas:
#   "For n>1 and m>1, all m congruent to n mod 2^(a(n)) have a dropping time
#    equal to a(n)". Eso es EQUIVALENTE a CST (se argumenta en la MEDIDA 2 de
#   este fichero), o sea que una conjetura abierta está publicada en OEIS con
#   forma de hecho.
#
# =============================================================================

import time
from fractions import Fraction

# ----------------------------------------------------------------------------
# CONSTANTES EDITABLES
# ----------------------------------------------------------------------------

K_DEP = 14              # comprobación 1: exhaustivo sobre los 2^K_DEP restos
REPS_DEP = 6            # representantes por resto
K_ESPEJO = 14           # comprobación 5: el espejo n -> -n, exhaustivo mod 2^K

K_CLASES = 27           # criba de clases: niveles 1..K_CLASES. 27 -> unos 6 s
LIMITE_FUERZA = 20_000_000     # fuerza bruta 3n+1 (impares). 2e7 -> unos 30 s
LIMITE_MENOS = 2_000_000       # fuerza bruta 3n-1. Más caro por número
TOPE_PASOS = 4000              # salvavidas: en 3n-1 hay ciclos y sigma no existe

K_COTA = 20_000         # hasta dónde se calcula la cota B(k). 20000 -> unos 11 s

K_AK = 14               # comprobación de la sucesión a(k) bajo el espejo

# ----------------------------------------------------------------------------
# LAS FUNCIONES. Explícitas y sin trucos: todo con int.
# ----------------------------------------------------------------------------

POT3 = [3 ** i for i in range(TOPE_PASOS + 2)]


def paso(y, signo):
    """Un paso del mapa del atajo. signo = +1 da 3n+1, signo = -1 da 3n-1."""
    if y & 1:
        return (3 * y + signo) // 2, 1
    return y // 2, 0


def sigma_estrella(x, signo, tope):
    """min{k>=1 : 2^k > 3^{m_k}}. Se calcula del VECTOR DE PARIDAD y nada más.
    Devuelve None si no se decide en `tope` pasos."""
    y = x
    m = 0
    for k in range(1, tope + 1):
        y, imp = paso(y, signo)
        m += imp
        if (1 << k) > POT3[m]:
            return k
    return None


def sigma_real(x, signo, tope):
    """min{k>=1 : el iterado k-esimo es MENOR que x}. Compara VALORES.
    Devuelve None si no baja en `tope` pasos (en 3n-1 pasa: hay ciclos)."""
    y = x
    for k in range(1, tope + 1):
        y, _ = paso(y, signo)
        if y < x:
            return k
    return None


def vector_paridad(x, k, signo):
    """Las k primeras paridades del mapa del atajo."""
    v = []
    y = x
    for _ in range(k):
        v.append(y & 1)
        y, _ = paso(y, signo)
    return tuple(v)


print()
print("=" * 78)
print("EL TIEMPO DE PARADA POR COEFICIENTE (CST) -- Terras 1976, conjetura 2.9")
print("=" * 78)
print("  MAPA: el del ATAJO.  T(n) = n/2 si par, (3n+1)/2 si impar.")
print("  CONTROL: U(n) = n/2 si par, (3n-1)/2 si impar.")
print()

t_ini = time.time()

# ============================================================================
# COMPROBACION 1 -- sigma* SE CALCULA SOLO DEL RESTO. Es lo que lo hace un
# criterio y no contabilidad, y por eso va la primera.
# ============================================================================

print("-" * 78)
print("COMPROBACION 1 -- sigma* depende SOLO de n mod 2^k")
print("-" * 78)

fallos_vec = 0
fallos_se = 0
n_clases_decididas = 0
DOSK = 1 << K_DEP

for r in range(DOSK):
    base = r if r > 0 else DOSK          # el 0 se representa por 2^K, no por 0
    v0 = vector_paridad(base, K_DEP, +1)
    s0 = sigma_estrella(base, +1, K_DEP)
    for j in range(1, REPS_DEP):
        x = base + j * DOSK
        if vector_paridad(x, K_DEP, +1) != v0:
            fallos_vec += 1
        if sigma_estrella(x, +1, K_DEP) != s0:
            fallos_se += 1
    if s0 is not None:
        n_clases_decididas += 1

print("  restos mod 2^%d          : %d" % (K_DEP, DOSK))
print("  representantes por resto: %d" % REPS_DEP)
print("  fallos de vector de paridad: %d" % fallos_vec)
print("  fallos de sigma*           : %d" % fallos_se)
print("  restos con sigma* ya decidido en <= %d pasos: %d de %d  (%.4f%%)"
      % (K_DEP, n_clases_decididas, DOSK, 100.0 * n_clases_decididas / DOSK))

if fallos_vec or fallos_se:
    raise SystemExit("sigma* NO depende solo del resto. Todo lo que sigue es falso.")

# La demostracion en vivo: un numero enorme decidido sin mirarlo entero.
# Se busca primero una semilla chica con sigma* largo (si fuera un numero
# cualquiera saldria sigma* = 1 y no se veria nada), y se le suma un multiplo
# enorme de 2^{sigma*}: el resto no cambia, luego el sigma* tampoco.
semilla = None
for x in range(3, 2_000_000, 2):
    s = sigma_estrella(x, +1, 120)
    if s is not None and s >= 40:
        semilla = (x, s)
        break
if semilla is None:
    raise SystemExit("No se encontro semilla con sigma* >= 40. Sube el rango.")
base_g, s_base = semilla
GRANDE = base_g + (1 << s_base) * (10 ** 40)
s_g = sigma_estrella(GRANDE, +1, 400)
resto_g = GRANDE % (1 << s_base)
print("  demostracion en vivo:")
print("    semilla chica x0 = %d           ->  sigma*(x0) = %d" % (base_g, s_base))
print("    x = x0 + 2^%d * 10^40  (tiene %d cifras)  ->  sigma*(x) = %s"
      % (s_base, len(str(GRANDE)), s_g))
print("    x mod 2^%d = %d = x0, y de ahi solo sale el mismo %d"
      % (s_base, resto_g, s_base))
if s_g != s_base or resto_g != base_g:
    raise SystemExit("El resto no reproduce el sigma* del numero grande.")
print("  OK: sigma* pasa el detector. Es un criterio, no contabilidad.")
print()

# ============================================================================
# COMPROBACION 2 -- sigma* <= sigma, y la razon algebraica (c_k >= 0)
# ============================================================================

print("-" * 78)
print("COMPROBACION 2 -- sigma* <= sigma  (3n+1), y su razon: c_k >= 0")
print("-" * 78)

fallos_desig = 0
for x in range(2, 200_001):
    s = sigma_real(x, +1, TOPE_PASOS)
    se = sigma_estrella(x, +1, TOPE_PASOS)
    if s is None or se is None:
        raise SystemExit("sigma o sigma* sin definir en x = %d con 3n+1." % x)
    if se > s:
        fallos_desig += 1

print("  x de 2 a 200000, mapa del atajo 3n+1")
print("  casos con sigma* > sigma: %d" % fallos_desig)
if fallos_desig:
    raise SystemExit("sigma* > sigma. Contradice a Terras: revisa el codigo.")
print("  OK. La razon se comprueba en la comprobacion 3 sobre TODAS las clases.")
print()

# Contra la publicacion: los terminos que OEIS A126241 imprime en su cabecera
# (copiados literalmente de las lineas %S/%T/%U el 01-08-2026). A126241 fija
# a(1) = 0 por convenio; nuestro sigma(1) no existe, asi que se compara de 2
# en adelante.
A126241 = [int(v) for v in (
    "0,1,4,1,2,1,7,1,2,1,5,1,2,1,7,1,2,1,4,1,2,1,5,1,2,1,59,1,2,1,56,1,2,"
    "1,4,1,2,1,8,1,2,1,5,1,2,1,54,1,2,1,4,1,2,1,5,1,2,1,7,1,2,1,54,1,2,1,"
    "4,1,2,1,51,1,2,1,5,1,2,1,8,1,2,1,4,1,2,1,5,1,2,1,45,1,2,1,8,1,2,1,4"
).split(",")]
fallos_oeis = 0
for n in range(2, len(A126241) + 1):
    if sigma_real(n, +1, TOPE_PASOS) != A126241[n - 1]:
        fallos_oeis += 1
print("  contra OEIS A126241 (tiempos de caida publicados, %d terminos):"
      % len(A126241))
print("    discrepancias de n = 2 a %d: %d" % (len(A126241), fallos_oeis))
if fallos_oeis:
    raise SystemExit("Nuestro sigma no reproduce A126241. El mapa esta mal.")
print("    a(27) = %d en OEIS y aqui. El 27 de siempre." % A126241[26])
print()

# ============================================================================
# LA CRIBA DE CLASES. Es el motor de las comprobaciones 3 y 4 y de la medida 2.
#
# Un "superviviente de nivel j" es una clase r mod 2^j cuyo vector de paridad
# cumple 2^i <= 3^{m_i} para todo i <= j, o sea que todavia no ha parado.
# Se guarda (r, c_j, m_j). Al subir de nivel, la clase r mod 2^j se parte en
# r y r + 2^j mod 2^{j+1}, y las dos tienen paridad OPUESTA en el paso j+1.
# ============================================================================

print("-" * 78)
print("COMPROBACION 3 y 4 -- la criba de clases hasta 2^%d" % K_CLASES)
print("-" * 78)

t0 = time.time()
sup = [(0, 0, 0)]            # (resto, c, m) al nivel 0
paradas_por_nivel = {}       # k -> (num_clases, mejor_c, mejor_D, mejor_r, mejor_m)
fallo_c_negativo = 0
fallo_cota_c = 0
fallo_ultimo_impar = 0
candidatos = 0
contraejemplos = []
margen_min = None            # min sobre clases de (menor x >= 2 de la clase)/umbral
margen_info = None

for j in range(K_CLASES):
    dosj = 1 << j
    dosj1 = 1 << (j + 1)
    nuevos = []
    n_par = 0
    mejor_c = -1
    mejor_D = 1
    mejor_r = None
    mejor_m = None
    for (r, c, m) in sup:
        tres = POT3[m]
        for lift in (r, r + dosj):
            # T^j(lift) = (3^m * lift + c) / 2^j, entero exacto
            tj = (tres * lift + c) // dosj
            if tj & 1:
                c2 = 3 * c + dosj
                m2 = m + 1
                impar = True
            else:
                c2 = c
                m2 = m
                impar = False
            t3 = POT3[m2]
            if c2 < 0:
                fallo_c_negativo += 1
            if dosj1 > t3:
                # NIVEL DE PARADA: aqui sigma* = j+1 para toda la clase
                n_par += 1
                if impar:
                    fallo_ultimo_impar += 1
                # la cota que sostiene B(k):  c_k <= m_k * 3^{m_k} / 2
                if 2 * c2 > m2 * t3:
                    fallo_cota_c += 1
                D = dosj1 - t3
                if c2 * mejor_D > mejor_c * D:
                    mejor_c, mejor_D, mejor_r, mejor_m = c2, D, lift, m2
                # el menor x >= 2 de la clase
                xmin = lift if lift >= 2 else lift + dosj1
                if c2 > 0:
                    # margen = xmin / umbral = xmin * D / c2
                    if margen_min is None or xmin * D * margen_min[1] < margen_min[0] * c2:
                        margen_min = (xmin * D, c2)
                        margen_info = (j + 1, lift, xmin, c2, D)
                # candidatos a contraejemplo: x en la clase con x <= c2/D
                x = xmin
                while x * D <= c2:
                    candidatos += 1
                    if t3 * x + c2 >= dosj1 * x:
                        contraejemplos.append((x, j + 1))
                    x += dosj1
            else:
                nuevos.append((lift, c2, m2))
    if n_par:
        paradas_por_nivel[j + 1] = (n_par, mejor_c, mejor_D, mejor_r, mejor_m)
    sup = nuevos

print("  c_k < 0 en alguna clase                    : %d" % fallo_c_negativo)
print("  ultimo paso IMPAR en un nivel de parada    : %d" % fallo_ultimo_impar)
print("  clases con 2*c_k > m_k * 3^{m_k}           : %d" % fallo_cota_c)
print("  supervivientes al nivel %d                 : %d" % (K_CLASES, len(sup)))

if fallo_c_negativo:
    raise SystemExit("c_k negativo: la desigualdad sigma* <= sigma no se sostiene.")
if fallo_ultimo_impar:
    raise SystemExit("Un nivel de parada termina en paso impar. La cota B(k) cae.")
if fallo_cota_c:
    raise SystemExit("La cota c_k <= m_k*3^{m_k}/2 falla. La cota B(k) cae.")

# CONTABILIDAD: paradas acumuladas + supervivientes tiene que dar 2^K exacto.
acumulado = 0
for k in range(1, K_CLASES + 1):
    n_par = paradas_por_nivel.get(k, (0,))[0]
    acumulado += n_par * (1 << (K_CLASES - k))
total = acumulado + len(sup)
print("  contabilidad: paradas levantadas a 2^%d + supervivientes = %d"
      % (K_CLASES, total))
print("                2^%d = %d" % (K_CLASES, 1 << K_CLASES))
if total != (1 << K_CLASES):
    raise SystemExit("La criba de clases pierde clases. No sigas.")
print("  OK. La criba es exhaustiva sobre los 2^%d restos.  (%.1f s)"
      % (K_CLASES, time.time() - t0))
print()

# ============================================================================
# COMPROBACION 5 -- EL ESPEJO n -> -n. Por que la mitad del coeficiente tiene
# que ser ciega al signo del +1.
#
#   Si n = -y con y > 0:  n par -> n/2 = -(y/2)
#                         n impar -> (3n+1)/2 = -((3y-1)/2)
#   O sea T sobre negativos ES U sobre positivos, y la PARIDAD se conserva.
#   Luego el vector de paridad de r bajo U = el de (-r) mod 2^k bajo T,
#   y todo lo que se calcule del vector de paridad -- sigma* incluido -- es
#   identico en los dos mapas POR TEOREMA, no por casualidad.
# ============================================================================

print("-" * 78)
print("COMPROBACION 5 -- el espejo n -> -n y la ceguera al signo")
print("-" * 78)

DOSE = 1 << K_ESPEJO
fallos_esp_vec = 0
fallos_esp_se = 0
for r in range(DOSE):
    a = r if r > 0 else DOSE
    b = (-a) % DOSE
    if b == 0:
        b = DOSE
    if vector_paridad(a, K_ESPEJO, -1) != vector_paridad(b, K_ESPEJO, +1):
        fallos_esp_vec += 1
    if sigma_estrella(a, -1, K_ESPEJO) != sigma_estrella(b, +1, K_ESPEJO):
        fallos_esp_se += 1

print("  restos mod 2^%d: %d" % (K_ESPEJO, DOSE))
print("  fallos de  vector_paridad_U(r) == vector_paridad_T(-r) : %d" % fallos_esp_vec)
print("  fallos de  sigma*_U(r) == sigma*_T(-r)                 : %d" % fallos_esp_se)
if fallos_esp_vec or fallos_esp_se:
    raise SystemExit("El espejo n -> -n no conserva el vector de paridad. Revisa.")
print("  OK. TODA cantidad que sea funcion solo del vector de paridad sale")
print("  IDENTICA en 3n+1 y en 3n-1. Correr el A/B sobre ella no informa.")
print()

# ============================================================================
# MEDIDA 1 -- fuerza bruta. Hasta donde aguanta la igualdad.
# ============================================================================

print("-" * 78)
print("MEDIDA 1 -- CST por fuerza bruta (3n+1, atajo)")
print("-" * 78)

t0 = time.time()
# Los pares son triviales: x par -> T(x) = x/2 < x, luego sigma = 1; y m_1 = 0
# con 2^1 = 2 > 1 = 3^0, luego sigma* = 1. Se comprueba y se salta.
fallos_par = 0
for x in range(2, 2002, 2):
    if sigma_real(x, +1, 10) != 1 or sigma_estrella(x, +1, 10) != 1:
        fallos_par += 1
if fallos_par:
    raise SystemExit("Un x par no tiene sigma = sigma* = 1. Imposible.")

dif = 0
peor = None
for x in range(3, LIMITE_FUERZA + 1, 2):
    y = x
    k = 0
    m = 0
    se = 0
    while True:
        if y & 1:
            y = (3 * y + 1) >> 1
            m += 1
        else:
            y >>= 1
        k += 1
        if se == 0 and (1 << k) > POT3[m]:
            se = k
        if y < x:
            break
    if se != k:
        dif += 1
        if peor is None:
            peor = (x, se, k)

print("  pares comprobados de 2 a 2000: sigma = sigma* = 1, 0 fallos")
print("  impares de 3 a %d" % LIMITE_FUERZA)
print("  casos con sigma* != sigma: %d" % dif)
if dif:
    print("  primero: x = %d, sigma* = %d, sigma = %d" % peor)
    raise SystemExit("CST falla por fuerza bruta. Esto seria un hallazgo enorme;"
                     " antes de creerlo, revisa el codigo.")
print("  LIMITE EXACTO ALCANZADO: CST verificada para todo x de 2 a %d."
      % LIMITE_FUERZA)
print("  (%.1f s)" % (time.time() - t0))
print()

# ============================================================================
# MEDIDA 2 -- EL MARGEN, CLASE A CLASE. Aqui esta el "+1" cuantificado.
#
#   CST falla en x  <=>  x <= c_k/(2^k - 3^{m_k}),  k = sigma*(x)
#
#   El lado derecho es el UMBRAL de la clase y no depende de x. Dentro de cada
#   clase residual, los contraejemplos son los elementos por DEBAJO del umbral,
#   y son finitos. Por eso "comprobar CST" se puede hacer clase a clase.
#
#   Y de aqui sale que el comentario de K. Spage en A126241 -- "todo m > 1
#   congruente con n modulo 2^{a(n)} tiene el mismo tiempo de caida" -- es
#   EQUIVALENTE a CST: decir que la clase entera comparte a(n) es decir que
#   ningun elemento de la clase cae por debajo del umbral.
# ============================================================================

print("-" * 78)
print("MEDIDA 2 -- el umbral de cada clase (el '+1' cuantificado)")
print("-" * 78)
print("  umbral(clase) = c_k / (2^k - 3^{m_k}).  CST falla en x  <=>  x <= umbral")
print()
print("   k   clases que paran   umbral maximo        el resto que lo alcanza")
for k in sorted(paradas_por_nivel):
    n_par, mc, mD, mr, mm = paradas_por_nivel[k]
    u = Fraction(mc, mD)
    print("  %2d   %14d   %16.4f   r = %d (mod 2^%d), m = %d"
          % (k, n_par, float(u), mr, k, mm))
print()
print("  candidatos revisados (x >= 2 por debajo del umbral de su clase): %d"
      % candidatos)
print("  contraejemplos: %s" % ("ninguno" if not contraejemplos else contraejemplos))
if contraejemplos:
    raise SystemExit("Contraejemplo a CST en la criba de clases. Revisa el codigo.")

k_m, r_m, xmin_m, c_m, D_m = margen_info
print("  el margen mas apretado de toda la criba:")
print("    clase r = %d (mod 2^%d), umbral = %s, menor x >= 2 de la clase = %d"
      % (r_m, k_m, str(Fraction(c_m, D_m)), xmin_m))
print("    factor de seguridad = %.4f  (x / umbral)"
      % (float(margen_min[0]) / float(margen_min[1])))
print()
print("  CONCLUSION: cero candidatos en 2^%d restos. CST no es que se cumpla por"
      % K_CLASES)
print("  poco: en ninguna clase hasta ese nivel EXISTE un x >= 2 que pudiera")
print("  romperla. Esto decide INFINITOS numeros, no un rango.")
print()

# ============================================================================
# MEDIDA 3 -- LA COTA. Lo unico de este fichero con forma de teorema.
#
#   Sea k = sigma*(x) y m = m_k. En un nivel de parada el ultimo paso es PAR
#   (comprobacion 3), y todos los niveles anteriores cumplen 2^j <= 3^{m_j}.
#   El aporte del paso impar j a c_k es 2^{j-1} * 3^{m_k - m_j}, y
#
#       3^{m_k - m_j} = 3^{m_k}/3^{m_j} <= 3^{m_k}/2^j
#
#   luego cada aporte es <= 3^{m_k}/2 y hay m_k de ellos:
#
#       c_k <= m_k * 3^{m_k} / 2                    (comprobado exhaustivamente)
#
#   Metido en  x <= c_k/(2^k - 3^m), y usando que m <= m* (la mayor potencia de
#   3 por debajo de 2^k) y que m*3^m/(2^k - 3^m) crece con m:
#
#       x < B(k) = k * 3^{m*} / (2 * (2^k - 3^{m*}))
#
#   B(k) se calcula con enteros exactos. No hay ni un float en la cadena.
# ============================================================================

print("-" * 78)
print("MEDIDA 3 -- LA COTA B(k), y que rango INFINITO deja demostrado")
print("-" * 78)
print("  Si x >= 2 rompe CST y sigma*(x) = k, entonces x < B(k).")
print()

t0 = time.time()
m = 0
pot = 1
record = Fraction(0)
records = []
B_max_hasta = []          # B_max_hasta[k] = max_{j<=k} B(j)
for k in range(1, K_COTA + 1):
    dosk = 1 << k
    while pot * 3 < dosk:
        pot *= 3
        m += 1
    D = dosk - pot
    B = Fraction(k * pot, 2 * D)
    if B > record:
        record = B
        records.append((k, m, B))
    B_max_hasta.append(record)

print("   los k donde B(k) bate record (los primeros 20):")
print("     k        m         B(k)")
for k, mm, B in records[:20]:
    print("  %6d   %6d   %.6e" % (k, mm, float(B)))
print()
# Y no se afirma: se comprueba. La lista de la Tabla C que el CLAUDE.md ya
# tenia tabulada, contra los k donde B(k) bate record.
JUMP_TERRAS = [1, 2, 5, 8, 27, 46, 65, 149, 233, 317, 401, 485, 1539, 2593]
JUMP_B = [94, 147, 200, 253, 306, 971, 1636]        # los m de las ultimas filas
mios = [k for k, mm, B in records][:len(JUMP_TERRAS)]
mios_m = [mm for k, mm, B in records][7:14]
print("  contra la Tabla C de Terras que este repo ya tenia tabulada:")
print("    jump values publicados: %s" % JUMP_TERRAS)
print("    k donde B(k) bate record: %s" % mios)
print("    coinciden: %s" % (mios == JUMP_TERRAS))
if mios != JUMP_TERRAS or mios_m != JUMP_B:
    raise SystemExit("Los records de B(k) NO son los jump values de Terras."
                     " Antes de contar nada, averigua por que.")
print("  La MISMA tabla de convergentes de log2(3) que gobierna la exclusion")
print("  de ciclos gobierna el margen de CST. No es analogia: es la misma lista.")
print()

# El K seguro: el mayor K con max_{j<=K} B(j) <= LIMITE_FUERZA
K_seguro = 0
for k in range(1, K_COTA + 1):
    if B_max_hasta[k - 1] <= LIMITE_FUERZA:
        K_seguro = k
    else:
        break

print("  fuerza bruta verificada hasta X0 = %d" % LIMITE_FUERZA)
print("  max B(j) para j <= %d  =  %.6e" % (K_seguro, float(B_max_hasta[K_seguro - 1])))
print("  primer k con B(k) > X0 : %d" % (K_seguro + 1))
print()
print("  RESULTADO: no existe contraejemplo a CST con sigma*(x) <= %d." % K_seguro)
print("  No es 'comprobado hasta 2e7'. Es un enunciado sobre TODOS los naturales")
print("  cuyo sigma* no pase de %d, por grandes que sean." % K_seguro)
print("  (%.1f s)" % (time.time() - t0))
print()

# Cuanto queda fuera: los x con sigma* > K_seguro. Sobrevivir al nivel K exige
# 3^{m_K} >= 2^K, o sea m_K >= m_min(K). El numero de cadenas binarias de
# longitud K con al menos m_min unos es una COTA SUPERIOR exacta del numero de
# clases indecisas, y se calcula con enteros.
def cota_supervivientes(K):
    mm = 0
    p = 1
    dosK = 1 << K
    while p < dosK:
        p *= 3
        mm += 1
    c = 1
    j = K
    tot = 1
    while j > mm:
        c = c * j // (K - j + 1)
        j -= 1
        tot += c
    return mm, tot

print("  cuanto queda sin decidir (cota superior exacta, contando cadenas):")
print("     K        clases medidas    cota por conteo binomial")
for K in (10, 20, K_CLASES):
    mm, cot = cota_supervivientes(K)
    # medida real solo la tenemos en K_CLASES
    med = len(sup) if K == K_CLASES else "-"
    print("  %6d   %16s   %s" % (K, str(med), cot))
mm_s, cot_s = cota_supervivientes(K_seguro)
bits = cot_s.bit_length()
print("  para K = %d: densidad de los indecisos <= 2^-%d, o sea menos de 10^-%d"
      % (K_seguro, K_seguro - bits, int((K_seguro - bits) * 0.30103)))
print()
print("  O sea: CST queda verificada para todo x >= 2 SALVO un conjunto de")
print("  densidad menor que 10^-%d. Es el primer instrumento propio del repo del"
      % int((K_seguro - bits) * 0.30103))
print("  tipo 'casi todo n' -- pero con el aviso de siempre: densidad cero NO es")
print("  vacio. Los indecisos son infinitos, y ahi vive la conjetura entera.")
print()

# ============================================================================
# MEDIDA 4 -- EL CONTROL A/B SOBRE 3n-1. El resultado mas importante del fichero.
# ============================================================================

print("-" * 78)
print("MEDIDA 4 -- EL CONTROL: CST sobre 3n-1")
print("-" * 78)
print("  En 3n-1 la identidad es  2^k U^k(x) = 3^{m_k} x + d_k  con")
print("  d -> 3d - 2^k en los impares, luego d_k <= 0 SIEMPRE.")
print("  Consecuencia inmediata, y es la del reves que en 3n+1:")
print("    lambda_k < 1  =>  U^k(x) = lambda_k x + d_k/2^k < x  =>  sigma <= sigma*")
print()

t0 = time.time()
igual = 0
menor = []
mayor = []
sin_sigma = []
sin_estrella = []
for x in range(2, LIMITE_MENOS + 1):
    # bucle fundido: sigma y sigma* del mismo recorrido, para que 2e6 numeros
    # con salvavidas de 4000 pasos no se coman el presupuesto
    y = x
    k = 0
    m = 0
    s = None
    se = None
    while k < TOPE_PASOS:
        if y & 1:
            y = (3 * y - 1) >> 1
            m += 1
        else:
            y >>= 1
        k += 1
        if se is None and (1 << k) > POT3[m]:
            se = k
        if s is None and y < x:
            s = k
        if s is not None and se is not None:
            break
    if se is None:
        sin_estrella.append(x)
    if s is None:
        sin_sigma.append(x)
    if s is None or se is None:
        continue
    if s == se:
        igual += 1
    elif s < se:
        menor.append((x, s, se))
    else:
        mayor.append((x, s, se))

print("  x de 2 a %d, mapa del atajo 3n-1" % LIMITE_MENOS)
print("    sigma == sigma*        : %d" % igual)
print("    sigma <  sigma*        : %d" % len(menor))
print("    sigma >  sigma*        : %d   (imposible: d_k <= 0)" % len(mayor))
print("    sigma  sin definir     : %d   -> %s" % (len(sin_sigma), sin_sigma[:10]))
print("    sigma* sin definir     : %d   -> %s" % (len(sin_estrella), sin_estrella[:10]))
if mayor:
    raise SystemExit("sigma > sigma* en 3n-1. Contradice d_k <= 0.")
print("  (%.1f s)" % (time.time() - t0))
print()

# Los x sin sigma son los minimos de los ciclos de 3n-1. Se identifican y se
# mide su balance, que es lo que decide la finitud de sigma*.
print("  los x >= 2 sin sigma son minimos de ciclo (el tercero es x = 1, que")
print("  queda fuera por la hipotesis x >= 2). Su balance:")
for x in sin_sigma:
    y = x
    k = 0
    m = 0
    while True:
        y, imp = paso(y, -1)
        m += imp
        k += 1
        if y == x:
            break
    print("    x = %2d: ciclo de %d pasos del atajo, %d impares."
          " m/k = %d/%d = %.6f   B/A = %d/%d = %.6f"
          % (x, k, m, m, k, m / k, k, m, k / m))
print("    umbral: sigma* es finito si y solo si m_j/j baja de log_3(2) =")
print("    0.630930 en algun j, o sea si B/A sube por encima de log2(3) = 1.584963.")
print("    Los tres ciclos de 3n-1 estan por DEBAJO de la linea, y por eso su")
print("    sigma* es infinito. El unico ciclo de 3n+1 (el 1-2) esta por ENCIMA")
print("    (B/A = 2/1), y por eso alli sigma* SI es finito -- y por eso el 1 es")
print("    el unico contraejemplo conocido a CST.")
print()

# La criba de clases para 3n-1: mismos supervivientes, otros restos.
t0 = time.time()
sup_m = [(0, 0, 0)]
cand_m = 0
rotos_m = []
conteos_mas = []
conteos_menos = []
for j in range(K_CLASES):
    dosj = 1 << j
    dosj1 = 1 << (j + 1)
    nuevos = []
    for (r, d, m) in sup_m:
        tres = POT3[m]
        for lift in (r, r + dosj):
            uj = (tres * lift + d) // dosj
            if uj & 1:
                d2 = 3 * d - dosj
                m2 = m + 1
            else:
                d2 = d
                m2 = m
            t3 = POT3[m2]
            if dosj1 > t3:
                continue          # aqui sigma* = j+1; en 3n-1 no puede fallar
            nuevos.append((lift, d2, m2))
            # sobrevive: si ademas U^{j+1}(x) < x, entonces sigma < sigma*
            den = t3 - dosj1
            if den > 0:
                xmin = lift if lift >= 2 else lift + dosj1
                x = xmin
                while x * den < -d2:
                    cand_m += 1
                    if t3 * x + d2 < dosj1 * x:
                        rotos_m.append((x, j + 1))
                    x += dosj1
    sup_m = nuevos

print("  criba de clases de 3n-1 hasta 2^%d:" % K_CLASES)
print("    supervivientes al nivel %d: %d   (3n+1 da %d)"
      % (K_CLASES, len(sup_m), len(sup)))
print("    candidatos revisados: %d, rupturas de la igualdad: %s"
      % (cand_m, "ninguna" if not rotos_m else rotos_m))
if len(sup_m) != len(sup):
    raise SystemExit("Los supervivientes NO coinciden entre los dos mapas."
                     " Contradice la comprobacion 5.")
if rotos_m:
    raise SystemExit("La igualdad se rompe en 3n-1 dentro de la criba.")
print("  (%.1f s)" % (time.time() - t0))
print()
print("  VEREDICTO DEL CONTROL, en tres lineas y las tres importan:")
print("    1. La IGUALDAD sigma = sigma* sale IGUAL en los dos mapas. Es ciega")
print("       al signo del +1, y la comprobacion 5 dice por que tiene que serlo:")
print("       sigma* es funcion del vector de paridad, y el espejo n -> -n lo")
print("       conserva. Medir esto en 3n-1 no podia dar otra cosa.")
print("    2. Lo que SI cambia de signo es la DIRECCION: 3n+1 da sigma* <= sigma,")
print("       3n-1 da sigma <= sigma*. Ese es el +1 entero, y es demostrable.")
print("    3. Y lo que separa de verdad los dos mapas es la FINITUD de sigma*:")
print("       en 3n-1 hay x >= 2 con sigma* infinito (los tres minimos de ciclo)")
print("       y en 3n+1 no se conoce ninguno. La conjetura de Collatz es")
print("       CST (igualdad, ciega) + finitud de sigma* (no ciega).")
print("    Moraleja para el protocolo del repo: que una cantidad salga igual en")
print("    3n-1 NO basta para tirarla. Hay que localizar QUE mitad es ciega.")
print()

# ============================================================================
# MEDIDA 5 -- POR QUE a(k) DE clasesfusion.py SALIO IGUAL EN LOS DOS MAPAS
#
# Hoy se midio que la sucesion a(k) es identica para 3n+1 y 3n-1 y se concluyo
# que por eso deja de servir. Aqui se demuestra que la igualdad era FORZOSA y
# se exhibe la biyeccion. El criterio de clasesfusion mira la pareja (r, r+1);
# el espejo manda esa pareja a (-r-1, -r), o sea r -> (-(r+1)) mod 2^k.
# NO se re-ejecuta clasesfusion.py: se recalcula a(k) aqui para k pequeno.
# ============================================================================

print("-" * 78)
print("MEDIDA 5 -- por que a(k) de clasesfusion.py salio igual en los dos mapas")
print("-" * 78)


def clases_que_se_funden(k, signo):
    """El criterio de clasesfusion.py: r es buena si S_k(r) == S_k(r+1) y
    T^k(r) == T^k(r+1). Devuelve la lista ordenada de restos buenos."""
    N = 1 << k
    S = [0] * N
    V = list(range(N))
    for _ in range(k):
        nv = []
        for i, y in enumerate(V):
            if y & 1:
                nv.append((3 * y + signo) // 2)
                S[i] += 1
            else:
                nv.append(y // 2)
        V = nv
    return [r for r in range(N)
            if S[r] == S[(r + 1) % N] and V[r] == V[(r + 1) % N]]


print("   k    a(k) 3n+1   a(k) 3n-1   mismos restos   la biyeccion r -> -(r+1)")
fallo_biy = 0
for k in range(3, K_AK + 1):
    N = 1 << k
    a = clases_que_se_funden(k, +1)
    b = clases_que_se_funden(k, -1)
    img = sorted(((-(r + 1)) % N) for r in a)
    ok = (img == sorted(b))
    if not ok:
        fallo_biy += 1
    print("  %2d   %10d   %9d   %13s   %s"
          % (k, len(a), len(b), str(a == b), "coincide" if ok else "NO COINCIDE"))
if fallo_biy:
    raise SystemExit("La biyeccion del espejo no explica la igualdad de a(k).")
print()
print("  Los conteos son iguales, los RESTOS no, y la biyeccion r -> -(r+1)")
print("  mod 2^k manda unos en otros exactamente. O sea: a(k) tenia que salir")
print("  igual, no es una medicion. Lo que NO es ciego es el CONJUNTO de restos.")
print("  Regla que se puede usar de aqui en adelante, y ahorra correr controles:")
print("  si tu cantidad es invariante bajo n -> -n, el A/B contra 3n-1 va a dar")
print("  igual por teorema y no hace falta medirlo.")
print()

# ============================================================================
# CONCLUSIONES
# ============================================================================

print("=" * 78)
print("CONCLUSIONES")
print("=" * 78)
print("  [1] sigma* se calcula SOLO de n mod 2^k. Pasa el detector de")
print("      contabilidad: es un criterio FINITO sobre INFINITOS numeros.")
print("  [2] sigma* <= sigma siempre, y la razon es c_k >= 0: el '+1'.")
print("  [3] Fuerza bruta: CST cierta para todo x de 2 a %d." % LIMITE_FUERZA)
print("  [4] Criba de clases: cero candidatos en los 2^%d restos." % K_CLASES)
print("  [5] COTA (lo unico con forma de teorema): un contraejemplo con")
print("      sigma* = k cumple x < B(k) = k*3^{m*}/(2*(2^k - 3^{m*})). Con la")
print("      fuerza bruta de [3] eso descarta TODO x >= 2 con sigma* <= %d."
      % K_seguro)
print("      Queda fuera un conjunto de densidad menor que 10^-%d."
      % int((K_seguro - bits) * 0.30103))
print("  [6] Un contraejemplo tendria que ser un x >= 2 cuyo vector de paridad")
print("      mantenga m_j/j >= log_3(2) durante mas de %d pasos, y ADEMAS caer" % K_seguro)
print("      por debajo del umbral de su propia clase. Las dos cosas a la vez.")
print("  [7] El control 3n-1 sale IGUAL en la igualdad y DISTINTO en la finitud.")
print("      La ceguera esta demostrada, no medida: espejo n -> -n.")
print()
print("  Tiempo total: %.1f s" % (time.time() - t_ini))
print("=" * 78)
print()
