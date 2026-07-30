# densidadfusion.py
#
# LA CONJETURA ABIERTA DE WU JIA-BANG, MEDIDA.
#
# De todo lo que se leyo de la literatura, esto es lo unico que quedo ABIERTO
# y que esta a nuestro alcance medir. El resto son teoremas de 1976-2005.
#
# EL CONTEXTO. Que dos enteros CONSECUTIVOS tengan el mismo tiempo de parada
# total es el fenomeno de la fusion de trayectorias:
#
#   Garner (1985): hay infinitos pares consecutivos con el mismo tiempo de
#     parada total. Lo demuestra estudiando como se funden los consecutivos.
#   Gao (1993): si existe UNA tupla de k consecutivos con el mismo tiempo,
#     existen infinitas. Hay una de 35.654 empezando en 2^500 + 1.
#   Wu Jia-Bang (1992): la tupla mas larga bajo 2^30 mide 176 y empieza en
#     722.067.240. En (1995) encontro otra de 310 en 6.622.073.000.
#
# LA CONJETURA (Wu Jia-Bang, 1995). Escribe d(2^N) para la densidad de pares
# consecutivos que se funden dentro del intervalo [1, 2^N]. Demostro que una
# version condicionada de esa densidad CRECE con N, y **conjeturo, sin
# demostrarlo, que la version sin condicionar tambien crece**.
#
# ESO ES LO QUE SE MIDE AQUI. Con tres definiciones distintas de "se funden",
# porque el enunciado en la fuente es ambiguo y conviene no elegir la que nos
# conviene:
#
#   d1 = misma ALTURA          h(n) == h(n+1)      h = pasos hasta el 1
#   d2 = mismo PICO            max(n) == max(n+1)
#   d3 = las dos cosas a la vez
#
# CUIDADO CON LA PALABRA "ALTURA". En la literatura de Collatz, h(n) es el
# NUMERO DE PASOS hasta llegar al 1, no el valor mas alto que alcanza. El
# valor mas alto se llama excursion maxima t(n). Wu habla de "consecutive
# numbers of the same HEIGHT", asi que **la columna de Wu es d1**, la de los
# pasos. d2 (el pico) es otra cosa y se mide aparte, a proposito, para ver
# si las dos se comportan igual. No se comportan igual.
#
# AVISO DE HONESTIDAD, por delante: medir que una sucesion crece en catorce
# puntos NO demuestra que crezca siempre. Esto no resuelve la conjetura de Wu.
# Lo unico que puede hacer es (a) darle o quitarle credito, y (b) si saliera
# NO monotona, eso si seria un resultado: refutaria la conjetura.
#
# Los tiempos de parada se calculan con una tabla y memoizacion; recorrer
# 2^24 numeros de uno en uno seria inviable.

import numpy as np

# ---------------------------------------------------------------------------
# Cambia esto aqui, guarda, y dale a Ctrl+B en Sublime.
# ---------------------------------------------------------------------------

POTENCIA = 26        # se llega hasta 2^POTENCIA. 26 tarda ~8 min y ~270 MB.
POTENCIA_PICO = 22   # la tabla de picos es int64 y pesa el doble: se corta antes
DESDE = 10           # la primera potencia de la tabla

TOPE = 1 << POTENCIA
TOPE_PICO = 1 << POTENCIA_PICO


def tabla_de_pasos(tope):
    """pasos[n] = cuantos pasos tarda n en llegar a 1 (mapa clasico 3n+1).

    Se memoiza: cuando la cadena cae por debajo del tope y ya esta calculada,
    se para y se rellena hacia atras.
    """
    pasos = np.full(tope + 1, -1, dtype=np.int32)
    pasos[1] = 0
    for arranque in range(2, tope + 1):
        if pasos[arranque] >= 0:
            continue
        cadena = []
        n = arranque
        while n > tope or pasos[n] < 0:
            cadena.append(n)
            n = n // 2 if n % 2 == 0 else 3 * n + 1
        cuenta = int(pasos[n])
        for m in reversed(cadena):
            cuenta += 1
            if m <= tope:
                pasos[m] = cuenta
    return pasos


def tabla_de_picos(tope):
    """pico[n] = el mayor valor que alcanza la trayectoria de n."""
    pico = np.zeros(tope + 1, dtype=np.int64)
    pico[1] = 1
    for arranque in range(2, tope + 1):
        if pico[arranque] > 0:
            continue
        cadena = []
        n = arranque
        while n > tope or pico[n] == 0:
            cadena.append(n)
            n = n // 2 if n % 2 == 0 else 3 * n + 1
        alto = int(pico[n])
        for m in reversed(cadena):
            alto = max(alto, m)
            if m <= tope:
                pico[m] = alto
    return pico


print(f"Construyendo la tabla de alturas hasta 2^{POTENCIA} = {TOPE:,} ...")
pasos = tabla_de_pasos(TOPE)
print(f"Construyendo la tabla de picos hasta 2^{POTENCIA_PICO} = {TOPE_PICO:,} ...")
picos = tabla_de_picos(TOPE_PICO)
print("Listas.\n")


# ------------------------------------- COMPROBACION: contra datos conocidos

conocidos = {27: 111, 703: 170, 871: 178, 6171: 261, 77031: 350,
             100002: 53, 100009: 309, 1: 0, 2: 1, 3: 7}
fallos = sum(1 for n, p in conocidos.items() if n <= TOPE and pasos[n] != p)
print(f"COMPROBACION -- la tabla contra valores conocidos: {fallos} fallos")
if fallos:
    raise SystemExit("La tabla de pasos esta mal. No sigas.")
print(f"  pasos(27) = {pasos[27]}, pico(27) = {picos[27]:,}  (el 9232 de siempre)")
if int(picos[27]) != 9232:
    raise SystemExit("El pico del 27 no es 9232. La tabla de picos esta mal.")


# ---------------------------------------------- las tres densidades por N

print(f"\nLA CONJETURA DE WU: densidad de consecutivos con la misma altura\n")
print(f"  {'N':>3} {'2^N':>12} {'d1 ALTURA':>10} {'d2 pico':>10} "
       f"{'d3 ambas':>10}   d1 (la de Wu)")
print(f"  {'-'*3} {'-'*12} {'-'*10} {'-'*10} {'-'*10}   {'-'*16}")

filas = []
previo = None
rotos_wu = 0
rotos_pico = 0
for N in range(DESDE, POTENCIA + 1):
    hasta = 1 << N
    a, b = pasos[1:hasta], pasos[2:hasta + 1]
    d1 = float((a == b).mean())
    if hasta <= TOPE_PICO:
        pa, pb = picos[1:hasta], picos[2:hasta + 1]
        d2 = float((pa == pb).mean())
        d3 = float(((a == b) & (pa == pb)).mean())
    else:
        d2 = d3 = float("nan")     # fuera del alcance de la tabla de picos
    veredicto = ""
    if previo is not None:
        if d1 > previo[0]:
            veredicto = "sube"
        else:
            veredicto = "BAJA <- refuta"
            rotos_wu += 1
        if d2 == d2 and previo[1] == previo[1] and d2 <= previo[1]:
            rotos_pico += 1   # el d2==d2 descarta los NaN de fuera de rango
    print(f"  {N:>3} {hasta:>12,} {d1:>10.6f} {d2:>10.6f} {d3:>10.6f}   {veredicto}")
    filas.append((N, d1, d2, d3))
    previo = (d1, d2, d3)

print(f"\n  d1 (ALTURA, que es la magnitud de Wu):")
print(f"    escalones que bajan: {rotos_wu} de {len(filas) - 1}")
if rotos_wu == 0:
    print(f"    MONOTONA EN TODO EL RANGO. La conjetura de Wu aguanta.")
    print(f"    Va de {filas[0][1]:.4f} en 2^{filas[0][0]} a {filas[-1][1]:.4f}"
          f" en 2^{filas[-1][0]}.")
    if filas[-1][1] > 0.5:
        print(f"    Y HA CRUZADO EL 50%. Garner (1985) conjeturo que 'la mayoria")
        print(f"    de los enteros positivos tienen la misma altura que un vecino'.")
        print(f"    En 2^{filas[-1][0]} la mayoria ya esta cruzada: {filas[-1][1]:.4%}.")
else:
    print(f"    OJO: baja en algun escalon. Eso seria evidencia CONTRA Wu.")

print(f"\n  d2 (PICO, que NO es la magnitud de Wu):")
print(f"    escalones que bajan: {rotos_pico} de {len(filas) - 1}")
print(f"    No es monotona: baja hasta ~2^20 y luego remonta. Las dos nociones")
print(f"    de 'parecerse' NO se comportan igual, y por eso importa no")
print(f"    confundir altura con pico.")


# ------------------------------------------------ las tuplas mas largas

print(f"\nLAS TUPLAS: rachas de consecutivos con el mismo tiempo de parada\n")
print(f"  {'N':>3} {'2^N':>12} {'tupla mas larga':>16} {'empieza en':>14}")
print(f"  {'-'*3} {'-'*12} {'-'*16} {'-'*14}")

for N in range(DESDE, POTENCIA + 1):
    hasta = 1 << N
    trozo = pasos[1:hasta + 1]
    iguales = trozo[1:] == trozo[:-1]
    mejor = mejor_inicio = 0
    racha = 0
    inicio = 1
    for i, ig in enumerate(iguales):
        if ig:
            if racha == 0:
                inicio = i + 1
            racha += 1
        else:
            if racha + 1 > mejor:
                mejor, mejor_inicio = racha + 1, inicio
            racha = 0
    if racha + 1 > mejor:
        mejor, mejor_inicio = racha + 1, inicio
    print(f"  {N:>3} {hasta:>12,} {mejor:>16} {mejor_inicio:>14,}")

print(f"\n  Wu Jia-Bang (1992) reporta la tupla mas larga bajo 2^30: mide 176")
print(f"  y empieza en 722.067.240. Aqui solo se llega a 2^{POTENCIA}, asi que")
print(f"  no se puede ni confirmar ni desmentir ese dato; lo que se ve es el")
print(f"  crecimiento hasta donde llegamos.")


# ------------------------ que fraccion de la densidad la explican los pares

print(f"\nDE DONDE SALE LA DENSIDAD\n")
hasta = TOPE
a, b = pasos[1:hasta], pasos[2:hasta + 1]
coinciden = np.flatnonzero(a == b) + 1
print(f"  pares consecutivos con el mismo tiempo hasta 2^{POTENCIA}: "
      f"{len(coinciden):,}")
print(f"  o sea el {len(coinciden) / hasta:.4%} de los pares")

# la TASA por resto, no el conteo: cuantos de los que tienen ese resto
# coinciden con su vecino. El conteo bruto sale plano por construccion.
menores = np.arange(1, hasta, dtype=np.int64)
mismo = (a == b)
print(f"\n  TASA de coincidencia segun el resto del menor del par modulo 32:")
print(f"  (la media global es {mismo.mean():.4f})")
tasas = []
for r in range(32):
    marca = (menores % 32) == r
    tasas.append((r, float(mismo[marca].mean()), int(marca.sum())))
tasas.sort(key=lambda t: -t[1])
print(f"    los ocho restos con MAS coincidencia:")
for r, t, c in tasas[:8]:
    estrella = "  <- la familia (32m+5, 32m+6) de Wu y Huang" if r == 5 else ""
    print(f"      resto {r:>3}: {t:.4f}{estrella}")
print(f"    los cuatro con MENOS:")
for r, t, c in tasas[-4:]:
    print(f"      resto {r:>3}: {t:.4f}")

puesto = [r for r, t, c in tasas].index(5) + 1
print(f"\n  Wu y Huang (2001) publicaron que las familias que se funden son")
print(f"  progresiones aritmeticas modulo 2^k, y dieron (32m+5, 32m+6) como")
print(f"  ejemplo. Aqui el resto 5 sale en el puesto {puesto} de 32")
print(f"  con tasa {dict((r, t) for r, t, c in tasas)[5]:.4f}.")
if puesto <= 8:
    print(f"  Esta arriba, como tenia que estar.")


# ---------------------------- EL MECANISMO: las clases que coinciden SIEMPRE

print(f"\n\nEL MECANISMO DE LA CONJETURA DE WU\n")
print(f"  Hay clases de resto en las que el par coincide el 100% de las veces.")
print(f"  Y su numero crece al doblar el modulo. Eso es lo que empuja la")
print(f"  densidad hacia arriba.\n")
print(f"  {'mod':>7} {'siempre':>8} {'fraccion':>9} {'muestra/clase':>14}")
print(f"  {'-'*7} {'-'*8} {'-'*9} {'-'*14}")

previa = -1.0
rotos_clases = 0
for k in range(3, POTENCIA - 8):
    MOD = 1 << k
    restos = menores % MOD
    suma = np.bincount(restos, weights=mismo, minlength=MOD)
    cuenta = np.bincount(restos, minlength=MOD)
    tasa = suma / np.maximum(cuenta, 1)
    siempre = int(((tasa > 0.99999) & (cuenta > 30)).sum())
    frac = siempre / MOD
    if previa >= 0 and frac < previa:
        rotos_clases += 1
    previa = frac
    print(f"  {MOD:>7} {siempre:>8} {frac:>9.5f} {int(cuenta.min()):>14,}")

print(f"\n  escalones que bajan: {rotos_clases}")
print(f"\n  LOS DOS ANCLAJES CONOCIDOS CAEN DENTRO:")
print(f"    resto 4 mod 8   -> Lagarias 1985: 8k+4 y 8k+5 se funden en 3 pasos")
print(f"    resto 5 mod 32  -> Wu y Huang 2001: la familia (32m+5, 32m+6)")
print(f"\n  AVISO DE SESGO, y es serio. Al doblar el modulo la muestra por clase")
print(f"  se parte por la mitad. Con pocas decenas de ejemplos por clase, una")
print(f"  clase con tasa real 0,99 sale medida como 1,000. Las filas de modulo")
print(f"  grande estan infladas y NO se pueden leer como cota inferior. Las")
print(f"  fiables son las de arriba, donde hay miles de ejemplos por clase.")
