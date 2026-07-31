# descensoresto.py
#
# EL TIEMPO DE DESCENSO, Y SI TIENE UNA COTA EN FUNCION DE LOS BITS.
#
# Esta es la primera pregunta del laboratorio que apunta a la conjetura en vez
# de a su alrededor. Conviene decir por que.
#
# ---------------------------------------------------------------------------
# LA PREGUNTA
# ---------------------------------------------------------------------------
#
# El TIEMPO DE DESCENSO (stopping time, o "planeo"/glide) de n es
#
#     sigma(n) = el primer j >= 1 tal que el iterado j-esimo de n es MENOR que n
#
# Si existiera una constante C con
#
#     sigma(n) <= C * log2(n)     para todo n >= 2
#
# la conjetura de Collatz saldria por induccion fuerte en tres lineas: todo n
# baja por debajo de si mismo en un numero finito de pasos, y el numero al que
# baja ya estaba resuelto por hipotesis de induccion. Nadie ha demostrado que
# esa C exista. Este programa la mide.
#
# ES UNA COTA, NO UN PROMEDIO, Y POR ESO IMPORTA. El CLAUDE.md de este repo
# ya tiene anotado por que los promedios no pueden demostrar nada: la conjetura
# habla de CADA numero, y un promedio nunca decide un caso individual. Una cota
# uniforme si lo haria. La medida de aqui es "el maximo sobre todos los n de k
# bits", que es la forma de una cota; lo que NO puede hacer es demostrarla,
# porque medir un maximo acotado en 27 escalones no dice nada de los infinitos
# escalones que faltan. Ese error ya se cometio en este repo dos veces: con el
# 1,7345 del coral (era el valor de una muestra) y con la holgura minima del
# piso de la altitud (le faltaba una hipotesis). Aqui se declara por delante.
#
# ---------------------------------------------------------------------------
# QUE MAPA SE USA. HAY DOS, Y AQUI SE USAN LOS DOS A PROPOSITO
# ---------------------------------------------------------------------------
#
# EL MAPA PRINCIPAL DE ESTE FICHERO ES EL DEL ATAJO:
#
#     T(n) = n/2          si n es par
#     T(n) = (3n+1)/2     si n es impar
#
# El atajo es el mapa adecuado para esta pregunta porque es donde el teorema de
# Terras (1976) es exacto: los primeros k pasos de T los decide n modulo 2^k, y
# la correspondencia resto <-> patron de paridades es una BIYECCION. Con la
# regla clasica no lo es (salen los Fibonacci, ver mallaresiduos.py), asi que
# contar clases de resto seria contar mal.
#
# Pero los records publicados de planeo (ericr.nl, y el records.json de este
# repo) estan en el mapa CLASICO. La conversion es exacta y no cuesta nada:
#
#     sigma_clasico = sigma_atajo + (numero de pasos impares dentro de ellos)
#
# porque cada paso impar del atajo son dos pasos clasicos (3n+1 y luego /2), y
# el valor intermedio 3n+1 es siempre MAYOR que n, asi que nunca puede ser el
# que dispara el descenso. Se imprimen las dos columnas en todas las tablas.
#
# ---------------------------------------------------------------------------
# LAS CUATRO COSAS QUE SE MIDEN
# ---------------------------------------------------------------------------
#
# 1. sigma_max(k) = el mayor sigma sobre todos los n < 2^k, con el n que lo
#    alcanza y el cociente sigma_max(k)/k. Fuerza bruta vectorizada.
#
# 2. La version por CLASES, que es la que compone: cuantos restos modulo 2^k
#    quedan RESUELTOS mirando solo k bits y cuantos SOBREVIVEN. Los que
#    sobreviven son la sucesion A076227 de OEIS, "Number of surviving Collatz
#    residues mod 2^n", y aqui se comprueba contra los terminos publicados.
#
# 3. Como decae la densidad de supervivientes. El CLAUDE.md afirma que va como
#    2^(-0,05*k), con exponente H(log_3 2) = 0,94996. Se mide el exponente real.
#
# 4. El cruce contra los 34 records de planeo de records.json.
#
# ---------------------------------------------------------------------------
# LO QUE CUESTA CADA k (medido en esta maquina, 30-07-2026)
# ---------------------------------------------------------------------------
#
# La fuerza bruta del punto 1 recorre el rango [2^(k-1), 2^k), o sea 2^(k-1)
# numeros, asi que CADA k CUESTA EL DOBLE QUE EL ANTERIOR:
#
#     k = 20 -> 0,08 s      k = 24 -> 1,4 s      k = 28 -> ~22 s
#     k = 22 -> 0,33 s      k = 26 -> ~5,6 s     k = 30 -> ~90 s
#
# Todo hasta k = 28 son unos 45 segundos en total. Lo que lo hace barato es la
# COMPACTACION: en cuanto un numero baja se saca del array, y con el atajo la
# mitad baja en el primer paso (los pares) y el 99% antes del paso 34. Sin
# compactar habria que iterar el bloque entero unos 300 pasos.
#
# La memoria se controla troceando en bloques de BLOQUE numeros, igual que hace
# clasesfusion.py: con BLOQUE = 2^22 el pico se queda en ~120 MB sea cual sea k.
# Sin trocear, el rango de k = 30 serian 8 GB.
#
# El punto 2 no cuesta casi nada porque no recorre los 2^k restos: los cuenta
# con una programacion dinamica sobre patrones de paridad, que es O(k^2) con
# enteros grandes. Llegar a k = 1400 tarda menos de un segundo. La criba
# directa sobre restos de verdad se hace solo hasta K_CRIBA, como control.

import json
import math
import os
import random
import time

import numpy as np

# ---------------------------------------------------------------------------
# Cambia esto aqui, guarda, y dale a Ctrl+B en Sublime.
# ---------------------------------------------------------------------------

K_MAX = 28          # fuerza bruta: el mayor sigma sobre todos los n < 2^K_MAX
BLOQUE = 1 << 22    # de cuantos numeros en cuantos se trabaja (memoria)

K_DP = 1400         # hasta donde llega la cuenta exacta de restos supervivientes
K_TABLA = 40        # hasta donde se imprime esa tabla
K_CRIBA = 20        # hasta donde se criban los restos DE VERDAD, como control

CUANTOS_AL_AZAR = 5000   # casos para comprobar el sigma vectorizado
SEMILLA_AZAR = 20260730

ARCHIVO_RECORDS = "records.json"

TOPE_PASOS = 200000      # salvavidas del sigma lento (n = 1 no baja nunca)


LOG2_3 = math.log2(3.0)          # 1,5849625...  el punto de equilibrio
LOG3_2 = 1.0 / LOG2_3            # 0,6309297...  la fraccion de impares limite


# ---------------------------------------------------------------------------
# EL PASO. Se define aqui y no se importa de collatz.py: en este repo cada
# programa suelto se lee entero sin saltar a otro fichero.
# ---------------------------------------------------------------------------

def sigma_lento(n):
    """El tiempo de descenso de n, a pelo, con enteros de Python.

    Devuelve (sigma_atajo, sigma_clasico) o None si n no baja nunca (el 1).
    """
    v = n
    pasos = 0
    impares = 0
    while pasos < TOPE_PASOS:
        if v % 2 == 1:
            v = (3 * v + 1) // 2
            impares += 1
        else:
            v = v // 2
        pasos += 1
        if v < n:
            return pasos, pasos + impares
    return None


def sigmas_de_array(ns):
    """El tiempo de descenso de cada n del array, vectorizado.

    Devuelve dos arrays: sigma del atajo y sigma clasico.

    LA COMPACTACION es lo que lo hace barato: cada vuelta se sacan del array
    los que ya bajaron, asi que el trabajo se derrumba enseguida. Ningun numero
    resuelto se sigue iterando, y de paso eso evita que los valores crezcan.
    """
    cuantos = len(ns)
    sig_atajo = np.zeros(cuantos, dtype=np.int32)
    sig_clasico = np.zeros(cuantos, dtype=np.int32)

    donde = np.arange(cuantos, dtype=np.int64)   # a que posicion pertenece cada vivo
    origen = np.array(ns, dtype=np.int64)        # el n de partida de cada vivo
    valor = origen.copy()                        # por donde va
    impares = np.zeros(cuantos, dtype=np.int32)  # cuantos pasos impares lleva

    paso = 0
    while donde.size and paso < TOPE_PASOS:
        paso += 1
        es_impar = (valor & 1).astype(bool)
        impares += es_impar
        rama_impar = (3 * valor + 1) >> 1
        valor >>= 1                               # la rama par, en sitio
        np.copyto(valor, rama_impar, where=es_impar)
        del rama_impar

        bajo = valor < origen
        if bajo.any():
            posiciones = donde[bajo]
            sig_atajo[posiciones] = paso
            sig_clasico[posiciones] = paso + impares[bajo]
            siguen = ~bajo
            donde = donde[siguen]
            origen = origen[siguen]
            valor = valor[siguen]
            impares = impares[siguen]

    return sig_atajo, sig_clasico


def maximo_del_rango(lo, hi, bloque=BLOQUE):
    """El mayor sigma clasico sobre n en [lo, hi), troceado en bloques.

    Devuelve (mejor_sigma_clasico, el n, su sigma del atajo). Solo guarda el
    maximo: guardar el sigma de cada numero costaria 4 bytes por numero y para
    k = 30 serian 4 GB por nada.
    """
    mejor_c = -1
    mejor_n = 0
    mejor_a = 0
    for inicio in range(lo, hi, bloque):
        fin = min(inicio + bloque, hi)
        ns = np.arange(inicio, fin, dtype=np.int64)
        sa, sc = sigmas_de_array(ns)
        i = int(np.argmax(sc))
        if int(sc[i]) > mejor_c:
            mejor_c = int(sc[i])
            mejor_n = inicio + i
            mejor_a = int(sa[i])
        del ns, sa, sc
    return mejor_c, mejor_n, mejor_a


# ---------------------------------------------------------------------------
# LOS RESTOS QUE SOBREVIVEN
#
# Criterio de Brown / Terras: el resto r modulo 2^k queda RESUELTO si en alguno
# de los primeros k pasos del atajo se garantiza el descenso, y eso pasa cuando
#
#     3^{S_j} < 2^j       para algun j <= k
#
# donde S_j es cuantos de los j primeros pasos fueron impares. El resto
# SOBREVIVE si 3^{S_j} > 2^j para los k pasos. (El caso 3^S = 2^j no existe:
# no hay potencia de 3 que sea potencia de 2.)
#
# Como el patron de paridades depende solo del resto y la correspondencia es
# biyectiva, contar restos supervivientes es contar PATRONES, y eso se hace con
# una programacion dinamica sobre (paso, cuantos impares llevo) sin tocar ni un
# resto. Es exacto: enteros de Python, sin coma flotante en ningun sitio.
# ---------------------------------------------------------------------------

def impares_minimos(hasta):
    """Smin[j] = el menor S con 3^S > 2^j. Todo con enteros exactos."""
    smin = [0] * (hasta + 1)
    S = 0
    tres = 1
    for j in range(1, hasta + 1):
        dos = 1 << j
        while tres <= dos:
            S += 1
            tres *= 3
        smin[j] = S
    return smin


def contar_supervivientes(hasta, smin):
    """a[k] = cuantos restos modulo 2^k sobreviven, para k = 0 .. hasta.

    El estado es "cuantos impares llevo", y en cada paso se prueban las dos
    ramas y se tira la que ya no cumple 3^S > 2^j. a[0] = 1 es la palabra vacia.
    """
    a = [1]
    estado = {0: 1}
    for j in range(1, hasta + 1):
        necesarios = smin[j]
        nuevo = {}
        for S, cuantos in estado.items():
            for bit in (0, 1):
                S2 = S + bit
                if S2 >= necesarios:
                    nuevo[S2] = nuevo.get(S2, 0) + cuantos
        estado = nuevo
        a.append(sum(estado.values()))
    return a


def cribar_restos_de_verdad(k, smin, bloque=BLOQUE):
    """Cuenta los restos supervivientes modulo 2^k recorriendolos uno a uno.

    Es el control de la programacion dinamica: aqui no se cuentan patrones, se
    itera el mapa del atajo sobre los 2^k restos con numpy. Solo vale para k
    pequenos porque el coste es 2^k * k.
    """
    vivos = 0
    for inicio in range(0, 1 << k, bloque):
        fin = min(inicio + bloque, 1 << k)
        valor = np.arange(inicio, fin, dtype=np.int64)
        impares = np.zeros(fin - inicio, dtype=np.int32)
        vivo = np.ones(fin - inicio, dtype=bool)
        for j in range(1, k + 1):
            es_impar = (valor & 1).astype(bool)
            impares += es_impar
            rama_impar = (3 * valor + 1) >> 1
            valor >>= 1
            np.copyto(valor, rama_impar, where=es_impar)
            del rama_impar
            vivo &= impares >= smin[j]
        vivos += int(vivo.sum())
        del valor, impares, vivo
    return vivos


# ---------------------------------------------------------------------------
# A076227 publicada. Copiada del b-file de OEIS (terminos n = 0 .. 44).
# Si estos numeros no salen, hay un bug y el programa se para.
# ---------------------------------------------------------------------------

A076227_PUBLICADA = [
    1, 1, 1, 2, 3, 4, 8, 13, 19, 38, 64, 128, 226, 367, 734, 1295, 2114,
    4228, 7495, 14990, 27328, 46611, 93222, 168807, 286581, 573162, 1037374,
    1762293, 3524586, 6385637, 12771274, 23642078, 41347483, 82694966,
    151917636, 263841377, 527682754, 967378591, 1934757182, 3611535862,
    6402835000, 12805670000, 23711865322, 41700700058, 83401400116,
]


print("EL TIEMPO DE DESCENSO, Y SI TIENE COTA EN FUNCION DE LOS BITS")
print()
print("  mapa principal : ATAJO   T(n) = n/2 si par, (3n+1)/2 si impar")
print("  mapa secundario: CLASICO 3n+1, que es donde estan los records"
      " publicados")
print("  conversion exacta: sigma_clasico = sigma_atajo + pasos impares")
print()
print(f"  K_MAX = {K_MAX}   BLOQUE = {BLOQUE:,}   K_DP = {K_DP}"
      f"   K_CRIBA = {K_CRIBA}")


reloj_total = time.time()

smin = impares_minimos(K_DP)
a = contar_supervivientes(K_DP, smin)


# ===========================================================================
# COMPROBACION 1 -- el sigma vectorizado contra la definicion cruda
# ===========================================================================

print()
print("=" * 74)
print("COMPROBACION 1 -- el sigma vectorizado contra la definicion cruda")
print("=" * 74)
print()

random.seed(SEMILLA_AZAR)
muestra = [random.randrange(2, 1 << 40) for _ in range(CUANTOS_AL_AZAR)]
muestra += [2, 3, 4, 5, 6, 7, 27, 703, 10087, 35655, 270271, 8088063]

sa_vec, sc_vec = sigmas_de_array(np.array(muestra, dtype=np.int64))

fallos_1 = []
for i, n in enumerate(muestra):
    lento = sigma_lento(n)
    if lento is None:
        fallos_1.append((n, None, None))
        continue
    if lento[0] != int(sa_vec[i]) or lento[1] != int(sc_vec[i]):
        fallos_1.append((n, lento, (int(sa_vec[i]), int(sc_vec[i]))))

print(f"  numeros probados : {len(muestra):,}"
      f"  (al azar por debajo de 2^40, mas doce a mano)")
print(f"  fallos           : {len(fallos_1)}")
if fallos_1:
    for cual in fallos_1[:5]:
        print(f"    {cual}")
    raise SystemExit("El sigma vectorizado no coincide con el lento. No sigas.")
print("  -> las dos implementaciones dan lo mismo, en el atajo y en el clasico.")

# y de paso, que la conversion entre mapas es la que se dijo
n_ejemplo = 27
at, cl = sigma_lento(n_ejemplo)
print()
print(f"  ejemplo de la conversion, n = {n_ejemplo}:")
print(f"    sigma atajo   = {at}")
print(f"    sigma clasico = {cl}   (= {at} + {cl - at} pasos impares)")


# ===========================================================================
# COMPROBACION 2 -- la cuenta de patrones contra la criba de restos de verdad
# ===========================================================================

print()
print("=" * 74)
print("COMPROBACION 2 -- la cuenta de patrones contra la criba de restos"
      " de verdad")
print("=" * 74)
print()
print("  A la izquierda, contando patrones de paridad (programacion dinamica).")
print("  A la derecha, iterando los 2^k restos uno a uno con numpy.")
print("  Si la biyeccion resto <-> patron del atajo es cierta, tienen que")
print("  coincidir en todos los k.")
print()
print(f"  {'k':>3} {'por patrones':>14} {'por restos':>14}   {'igual?':>7}")
print(f"  {'-'*3} {'-'*14} {'-'*14}   {'-'*7}")

fallos_2 = 0
for k in range(1, K_CRIBA + 1):
    por_restos = cribar_restos_de_verdad(k, smin)
    igual = (a[k] == por_restos)
    if not igual:
        fallos_2 += 1
    print(f"  {k:>3} {a[k]:>14,} {por_restos:>14,}   {str(igual):>7}")

if fallos_2:
    raise SystemExit("La cuenta de patrones no cuadra con la criba de restos.")
print()
print(f"  -> {K_CRIBA} de {K_CRIBA} coinciden. La biyeccion aguanta y la")
print(f"     programacion dinamica cuenta lo que dice contar.")


# ===========================================================================
# COMPROBACION 3 -- contra A076227 publicada en OEIS
# ===========================================================================

print()
print("=" * 74)
print("COMPROBACION 3 -- contra A076227 publicada en OEIS")
print("=" * 74)
print()

cuantos_3 = min(len(A076227_PUBLICADA), K_DP + 1)
fallos_3 = [(k, A076227_PUBLICADA[k], a[k])
            for k in range(cuantos_3) if A076227_PUBLICADA[k] != a[k]]

print(f"  terminos comparados (n = 0 .. {cuantos_3 - 1}): {cuantos_3}")
print(f"  discrepancias: {len(fallos_3)}")
if fallos_3:
    for k, pub, mio in fallos_3[:5]:
        print(f"    n = {k}: publicado {pub}, calculado {mio}")
    raise SystemExit("No reproduzco A076227. Hay un bug. Para y dilo.")
print(f"  -> los {cuantos_3} terminos salen identicos.")
print(f"     a(34) = {a[34]:,}, que es el numero que el CLAUDE.md cita")
print(f"     como el tamano de la criba clasica ({100 * a[34] / 2**34:.3f}%).")
print()
print("  Nota de definicion, para que no haya duda de que es lo mismo:")
print("  OEIS lo enuncia como \"el numero de palabras binarias v(1)...v(n) con")
print("  2^m < 3^(v(1)+...+v(m)) para todo m = 1..n\". Eso es exactamente el")
print("  criterio de Brown / Terras escrito sobre el vector de paridad.")


# ===========================================================================
# COMPROBACION 4 -- los 34 records de planeo de records.json
# ===========================================================================

print()
print("=" * 74)
print("COMPROBACION 4 -- los records de planeo publicados")
print("=" * 74)
print()

records_planeo = []
if not os.path.exists(ARCHIVO_RECORDS):
    print(f"  AVISO: no existe {ARCHIVO_RECORDS}. Me salto la comprobacion.")
else:
    try:
        with open(ARCHIVO_RECORDS, encoding="utf-8") as f:
            datos = json.load(f)
        crudos = datos.get("glide_records")
    except Exception as problema:
        crudos = None
        print(f"  AVISO: no pude leer {ARCHIVO_RECORDS} ({problema}).")
    if not crudos:
        print(f"  AVISO: {ARCHIVO_RECORDS} no trae 'glide_records'."
              f" Me salto la comprobacion.")
    else:
        for r in crudos:
            records_planeo.append((int(r["n"]), int(r["glide"])))
        records_planeo.sort()

if records_planeo:
    print("  El planeo (glide) de ericr.nl ES el tiempo de descenso, en el mapa")
    print("  CLASICO. Se recalcula desde cero con enteros exactos.")
    print()
    print(f"  {'n':>21} {'bits':>7} {'publicado':>10} {'calculado':>10}"
          f" {'atajo':>7} {'planeo/bits':>12}")
    print(f"  {'-'*21} {'-'*7} {'-'*10} {'-'*10} {'-'*7} {'-'*12}")

    fallos_4 = 0
    for n, planeo in records_planeo:
        at, cl = sigma_lento(n)
        bits = math.log2(n)
        marca = "" if cl == planeo else "   <- NO CUADRA"
        if cl != planeo:
            fallos_4 += 1
        print(f"  {n:>21,} {bits:>7.3f} {planeo:>10} {cl:>10}"
              f" {at:>7} {cl / bits:>12.3f}{marca}")

    print()
    print(f"  records comprobados: {len(records_planeo)}   fallos: {fallos_4}")
    if fallos_4:
        raise SystemExit("Mi sigma no reproduce los planeos publicados."
                         " No sigas.")
    print("  -> los 34 planeos publicados salen identicos recalculandolos.")
    print("     Y eso valida de paso la conversion atajo -> clasico, porque el")
    print("     numero de la columna 'clasico' se obtuvo sumando los impares.")


# ===========================================================================
# MEDIDA 1 -- sigma_max(k) por fuerza bruta
# ===========================================================================

print()
print("=" * 74)
print(f"MEDIDA 1 -- el mayor tiempo de descenso sobre todos los n < 2^k")
print("=" * 74)
print()
print("  Fuerza bruta de verdad: se miran TODOS los n. El maximo es acumulado")
print("  (el de k incluye a los de k-1), que es lo que hace falta para una cota.")
print()
print(f"  {'k':>3} {'sigma_C max':>12} {'el n':>12} {'sigma_T max':>12}"
      f" {'sigma_C/k':>10} {'sigma_T/k':>10} {'seg':>7}")
print(f"  {'-'*3} {'-'*12} {'-'*12} {'-'*12} {'-'*10} {'-'*10} {'-'*7}")

mejor_c = -1
mejor_n = 0
mejor_a = 0
tabla_sigma = []
for k in range(2, K_MAX + 1):
    lo = max(2, 1 << (k - 1))
    hi = 1 << k
    reloj = time.time()
    c, n, at = maximo_del_rango(lo, hi)
    if c > mejor_c:
        mejor_c, mejor_n, mejor_a = c, n, at
    tabla_sigma.append((k, mejor_c, mejor_n, mejor_a))
    print(f"  {k:>3} {mejor_c:>12} {mejor_n:>12,} {mejor_a:>12}"
          f" {mejor_c / k:>10.3f} {mejor_a / k:>10.3f}"
          f" {time.time() - reloj:>7.2f}")


# el cruce fino: mis maximos tienen que ser los records publicados
if records_planeo:
    print()
    print("  CRUCE: cada maximo de arriba tiene que ser un record publicado.")
    desacuerdos = 0
    comparados = 0
    for k, c, n, at in tabla_sigma:
        publicado = max((g for m, g in records_planeo if m < (1 << k)),
                        default=None)
        if publicado is None:
            continue
        comparados += 1
        if publicado != c:
            desacuerdos += 1
            print(f"    k = {k}: yo {c}, records.json {publicado}")
    print(f"    k comparados: {comparados}   desacuerdos: {desacuerdos}")
    if desacuerdos:
        raise SystemExit("Mi maximo no coincide con el record publicado.")
    print(f"    -> los {comparados} escalones coinciden con ericr.nl.")


# ===========================================================================
# MEDIDA 2 -- la version por clases, que es la que compone
# ===========================================================================

print()
print("=" * 74)
print("MEDIDA 2 -- cuantos restos quedan resueltos mirando solo k bits")
print("=" * 74)
print()
print("  Un resto queda RESUELTO si TODO numero de esa clase baja por debajo de")
print("  si mismo en <= k pasos del atajo. Los demas SOBREVIVEN: mirar k bits")
print("  no basta para decidirlos. Esto es A076227.")
print()
print(f"  {'k':>3} {'2^k':>16} {'resueltos':>16} {'sobreviven':>14}"
      f" {'densidad':>11} {'1 de cada':>10}")
print(f"  {'-'*3} {'-'*16} {'-'*16} {'-'*14} {'-'*11} {'-'*10}")
for k in range(1, min(K_TABLA, K_DP) + 1):
    total = 1 << k
    dens = a[k] / total
    print(f"  {k:>3} {total:>16,} {total - a[k]:>16,} {a[k]:>14,}"
          f" {dens:>10.6%} {1 / dens:>10.1f}")

print()
print("  Y LO QUE NUNCA PASA, que es el punto: a(k) >= 1 PARA TODO k.")
print("  El resto 2^k - 1 (el que en binario son todos unos) da S_j = j en")
print("  todos los pasos, y 3^j > 2^j siempre. Ese resto no lo mata ninguna")
print(f"  criba, por grande que sea k. a({min(K_TABLA, K_DP)}) ="
      f" {a[min(K_TABLA, K_DP)]:,} y a({K_DP}) tiene"
      f" {len(str(a[K_DP]))} cifras.")


# ===========================================================================
# MEDIDA 3 -- como decae la densidad
# ===========================================================================

print()
print("=" * 74)
print("MEDIDA 3 -- el exponente de decaimiento de la densidad")
print("=" * 74)
print()

H = -(LOG3_2 * math.log2(LOG3_2) + (1 - LOG3_2) * math.log2(1 - LOG3_2))
print(f"  El CLAUDE.md afirma que la densidad va como 2^(-0,05*k), con")
print(f"  exponente de crecimiento H(log_3 2). Recalculado aqui:")
print(f"    log_3 2       = {LOG3_2:.6f}")
print(f"    H(log_3 2)    = {H:.6f}")
print(f"    1 - H         = {1 - H:.6f}    <- el 0,05 del decaimiento")
print()
print("  Pendiente medida de log2(a(k)) por tramos (esto es a(k) ~ 2^(pend*k)):")
print()
print(f"  {'tramo de k':>16} {'pendiente':>11} {'decaim. 1-pend':>15}"
      f" {'1 de cada, x2^k':>16}")
print(f"  {'-'*16} {'-'*11} {'-'*15} {'-'*16}")

tramos = [(10, 20), (20, 40), (40, 80), (80, 160), (160, 320), (320, 640),
          (640, 1280)]
pendientes = []
for lo, hi in tramos:
    if hi > K_DP:
        continue
    pend = (math.log2(a[hi]) - math.log2(a[lo])) / (hi - lo)
    pendientes.append((lo, hi, pend))
    print(f"  {f'{lo} .. {hi}':>16} {pend:>11.6f} {1 - pend:>15.6f}"
          f" {2 ** (1 - pend):>16.4f}")

if pendientes:
    ultima = pendientes[-1]
    print()
    print(f"  Pendiente en el ultimo tramo: {ultima[2]:.6f}")
    print(f"  Valor teorico H(log_3 2)    : {H:.6f}")
    print(f"  Diferencia                  : {H - ultima[2]:+.6f}"
          f"  ({100 * (ultima[2] - H) / H:+.3f}%)")
    print()
    print("  La pendiente medida SUBE tramo a tramo y se acerca a H por debajo.")
    print("  O sea que el 2^(-0,05*k) del CLAUDE.md es el limite, no el valor")
    print("  local: en el rango que usa la criba de Barina (k = 34) el")
    print("  decaimiento real es mas lento, mas cerca de 2^(-0,10*k).")

print()
print("  LO QUE ESTO IMPLICA, Y ES EL PUNTO ESTRUCTURAL:")
print("  la densidad decae exponencialmente pero NUNCA llega a cero en un k")
print("  finito -- ya se dijo arriba, a(k) >= 1 siempre. Cribar por restos")
print("  puede dar \"casi todos\" con la densidad que se quiera, y no da")
print("  \"todos\" para ningun k. Es el mismo muro de pinzaciclos.py por otra")
print("  puerta: alli el barrido de restos no podia encontrar ciclos porque")
print("  cada clase es un candidato distinto; aqui no puede cerrar el descenso")
print("  porque siempre queda clase viva.")


# ===========================================================================
# MEDIDA 4 -- lo que la densidad predice para el maximo, contra lo medido
# ===========================================================================

print()
print("=" * 74)
print("MEDIDA 4 -- la densidad predice el maximo, y se cruza con los records")
print("=" * 74)
print()
print("  El argumento, que es de valores extremos y NO es una demostracion:")
print("  entre los n < 2^k, los que aguantan j pasos sin bajar son los que caen")
print("  en una clase superviviente modulo 2^j, y de esas hay a(j). Cuantos n")
print("  por debajo de 2^k caben en ellas: a(j) * 2^(k-j) por termino medio. El")
print("  mayor j en que ese numero todavia llega a 1 es la prediccion del")
print("  maximo. Y el sigma clasico se saca sumando los impares minimos.")
print()
print(f"  {'k':>3} {'pred sigma_T':>13} {'pred sigma_C':>13}"
      f" {'medido sigma_C':>15} {'pred/medido':>12} {'pred_C/k':>9}")
print(f"  {'-'*3} {'-'*13} {'-'*13} {'-'*15} {'-'*12} {'-'*9}")


def prediccion(k):
    """El mayor j con a(j) * 2^(k-j) >= 1, o sea a(j) >= 2^(j-k)."""
    mejor = 0
    for j in range(1, K_DP + 1):
        if j <= k or a[j] >= (1 << (j - k)):
            mejor = j
        if j - k > 4000:
            break
    return mejor


medido_por_k = {k: c for k, c, n, at in tabla_sigma}
if records_planeo:
    for k in range(2, 72):
        publicado = max((g for m, g in records_planeo if m < (1 << k)),
                        default=None)
        if publicado is not None:
            medido_por_k.setdefault(k, publicado)

for k in list(range(5, K_MAX + 1, 1)) + [30, 35, 40, 45, 50, 55, 60, 61]:
    if k > 70:
        continue
    j = prediccion(k)
    if j >= K_DP:
        continue
    pred_c = j + smin[j]
    med = medido_por_k.get(k)
    if med is None:
        continue
    print(f"  {k:>3} {j:>13} {pred_c:>13} {med:>15}"
          f" {pred_c / med:>12.3f} {pred_c / k:>9.3f}")

print()
print("  La prediccion viene de una densidad y el dato es un maximo, asi que")
print("  no tienen por que cuadrar. Cuadran mejor de lo que merecen, y el sitio")
print("  donde mas importa es el ultimo: a 60 bits el planeo record publicado")
print("  es 1614 y la densidad predice 1613 sin haber mirado ningun numero.")
print()
print("  Y la prediccion tiene LIMITE FINITO, que es lo unico que aqui se")
print("  parece a una respuesta:")
lim_t = 1.0 / (1.0 - H)
lim_c = lim_t * (1.0 + LOG3_2)
print(f"    sigma_T/k  ->  1/(1-H)           = {lim_t:.4f}")
print(f"    sigma_C/k  ->  (1+log_3 2)/(1-H) = {lim_c:.4f}")
print("  porque cuando la pendiente local llega a H, el j critico es k/(1-H) y")
print("  la fraccion de impares de ese patron es log_3 2. O sea que el modelo")
print("  de densidad SI predice una C, y la predice en torno a 32,6 para el")
print("  mapa clasico. Los records van por 26,8 a 61 bits, subiendo despacio.")


# ===========================================================================
# CONCLUSION
# ===========================================================================

print()
print("=" * 74)
print("CONCLUSION")
print("=" * 74)
print()

cocientes = [(k, c / k) for k, c, n, at in tabla_sigma]
peor_k, peor = max(cocientes, key=lambda par: par[1])
ultimo_k, ultimo = cocientes[-1]

print(f"  1. EL COCIENTE CRECE, y no despacio del todo.")
print(f"     sigma_C_max(k)/k por fuerza bruta: {cocientes[0][1]:.2f} en k = 2,")
print(f"     {ultimo:.2f} en k = {ultimo_k}; el mayor del barrido es"
      f" {peor:.2f} (k = {peor_k}).")
if records_planeo:
    n_gordo, planeo_gordo = records_planeo[-1]
    print(f"     Y con los records publicados, que llegan mucho mas lejos:")
    print(f"     {planeo_gordo} / {math.log2(n_gordo):.1f} bits ="
          f" {planeo_gordo / math.log2(n_gordo):.2f} a"
          f" {math.log2(n_gordo):.0f} bits.")
print(f"     No se estabiliza en el rango medido. Crece, y crece de forma")
print(f"     compatible con acercarse a un techo, no con dispararse.")
print()
print(f"  2. NO, ESTO NO DEMUESTRA QUE LA COTA EXISTA, y hay que decirlo con")
print(f"     todas las letras. Medir un cociente que sube despacio en"
      f" {K_MAX - 1} escalones")
print(f"     no dice nada de los infinitos que faltan. Es exactamente el error")
print(f"     que este repo ya cometio dos veces: el 1,7345 del coral (que era")
print(f"     el valor de una muestra) y el piso de la altitud (al que le")
print(f"     faltaba una hipotesis, y lo cazo un control, no los extremos).")
print(f"     Ademas el maximo esta medido sobre 2^{K_MAX} numeros y la conjetura")
print(f"     habla de infinitos: es un maximo de muestra, no una cota.")
print()
print(f"  3. LO QUE SI ES DURO. Dos cosas, y las dos son cotas o identidades:")
print(f"     - a(k) >= 1 para todo k, demostrado en una linea: el resto")
print(f"       2^k - 1 sobrevive siempre. Ninguna criba modular vacia el")
print(f"       conjunto de candidatos, para ningun k.")
print(f"     - sigma_clasico = sigma_atajo + impares, exacto, verificado en")
print(f"       {len(muestra):,} numeros y en los {len(records_planeo)} records"
      f" publicados.")
print()
print(f"  4. LA CONCLUSION ESTRUCTURAL, que era la pregunta de verdad.")
print(f"     Aunque la cota existiera empiricamente, cribar restos da densidad")
print(f"     -> 1 pero NUNCA cobertura total. Mis datos APOYAN eso, y no de")
print(f"     forma estadistica: es un teorema de una linea, no una tendencia.")
print(f"     Un contraejemplo de la conjetura tendria que vivir justo en el")
print(f"     conjunto que la criba no ve, y ese conjunto nunca se queda vacio:")
print(f"     su densidad tiende a cero pero su cardinal tiende a infinito")
print(f"     (a(k) crece como 2^0,95k). Medida cero, cardinal infinito. La")
print(f"     criba compra densidad; no compra cobertura.")
print()
print(f"     Dicho de otro modo, y es el mismo muro que ya tiene anotado")
print(f"     pinzaciclos.py: el metodo de restos no esta lento, esta topado por")
print(f"     construccion. Lo que aporta esta sesion es medir DONDE esta el")
print(f"     tope y con que exponente se acerca.")
print()
print(f"  5. EL CUARTO CAMINO. Lo que si es una regla que da el comportamiento")
print(f"     sin generar la trayectoria: 'el resto modulo 2^k decide si n baja")
print(f"     en <= k pasos', y la cuenta exacta de cuantos restos lo hacen es")
print(f"     A076227, calculada aqui hasta k = {K_DP} sin tocar un solo numero.")
print(f"     Eso es el cuarto camino funcionando. Lo que NO hace es cerrarse:")
print(f"     siempre queda resto vivo.")

print()
print(f"Tiempo total: {time.time() - reloj_total:.1f} s")
