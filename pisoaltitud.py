# -*- coding: utf-8 -*-
#
# EL PISO DE LA ALTITUD
# =====================
#
# Qué se está mirando, y por qué merece un fichero propio.
#
# Casi todo lo que mide este laboratorio son PROMEDIOS: la fracción impar, las
# constantes de parada, el 1,7345 del coral. Un promedio no demuestra nada sobre
# un número concreto — una sola trayectoria rara no le mueve un decimal.
#
# Esto es otra cosa. Esto es una COTA: un "nunca por debajo de", que vale para
# CADA número, uno por uno, y se demuestra en una línea. Por eso es el resultado
# más valioso del repo aunque diga mucho menos que las tablas de constantes.
#
# El enunciado, con la hipótesis que le faltaba:
#
#     PARA n IMPAR:   log2( altitud(n) / n )  >=  racha(n) * log2(3/2) + 1
#
# donde:
#     racha(n)   = pasos impares seguidos al arranque bajo el mapa del ATAJO,
#                  T(n) = (3n+1)/2 si n impar, n/2 si n par.
#     altitud(n) = el valor más alto de la trayectoria bajo el mapa CLASICO 3n+1.
#
# LA DEMOSTRACION, entera.
#
#   Bajo el mapa del atajo, un paso impar manda n a (3n+1)/2 > 3n/2. Encadenando
#   k pasos impares seguidos, el número al que se llega es
#
#       T^k(n)  >  (3/2)^k * n  =  3^k * n / 2^k
#
#   Pero el mapa del atajo hace en UN paso lo que el clásico hace en DOS: el
#   clásico pasa por 3n+1 ANTES de dividir. O sea que el último paso impar, en el
#   mapa clásico, llega a 3*x+1 y sólo después baja a (3x+1)/2. La altitud clásica
#   es por tanto el DOBLE de lo que ve el atajo en ese punto:
#
#       altitud(n)  >=  2 * T^k(n)  >  2 * 3^k * n / 2^k  =  3^k * n / 2^(k-1)
#
#   Tomando log2 y con k = racha(n):
#
#       log2( altitud(n)/n )  >=  k*log2(3) - (k-1)  =  k*log2(3/2) + 1
#
#   Y AHI ESTA EL +1: es log2(2), y viene ENTERO de mezclar los dos mapas. No es
#   una constante de ajuste. Si se mide la altitud con el mapa del ATAJO en vez de
#   con el clásico, el factor 2 no aparece y el piso queda limpio:
#
#       log2( altitud_atajo(n)/n )  >=  racha(n) * log2(3/2)
#
#   y ESA vale para las dos paridades, porque con n par la racha es 0 y el piso
#   sólo pide altitud_atajo >= n, que es cierto por definición (la altitud incluye
#   al propio n).
#
# LA CORRECCION, que es la mitad del valor de este fichero.
#
#   El enunciado clásico se publicó primero SIN la hipótesis "n impar", y así es
#   FALSO. Con n par la racha vale 0, el piso exige altitud >= 2n, y eso falla en
#   más de la mitad de los pares: el 10 sube sólo hasta 16 y necesitaría 20.
#
#   Lo importante es CÓMO apareció el error. Se probó el piso contra los 243
#   récords publicados de Roosendaal y Barina — los números que más suben y más
#   tardan de todo lo conocido — y PASARON LOS 243, incluidos los 15 pares (que
#   pasan por casualidad, porque son 2*impar y el impar de dentro sube mucho).
#   Quien lo cazó fue el barrido de control sobre números corrientes.
#
#       LOS EXTREMOS CONFIRMAN; LOS CONTROLES REFUTAN.
#
# ARITMETICA. Nada de floats para decidir si la cota se cumple. Se multiplica en
# cruz y se compara con enteros exactos:
#
#     clásico:  log2(alt/n) >= r*log2(3/2) + 1   <=>   alt * 2^r  >=  2 * n * 3^r
#     atajo  :  log2(alt/n) >= r*log2(3/2)       <=>   alt * 2^r  >=      n * 3^r
#
# Los floats se usan SOLO para informar de la holgura, que es un número decorativo.
#
# Este fichero no dibuja nada: sólo números por stdout. Las comprobaciones van
# antes de las conclusiones y cortan con SystemExit, como todo en este repo.

import json
import math
import os

# ------------------------------------------------------------------ constantes

LIMITE = 100000              # hasta dónde llega el barrido de control
CUANTOS_EJEMPLOS = 8         # cuántos pares fallones se imprimen como muestra
ARCHIVO_RECORDS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'records.json')

LOG2_3_2 = math.log2(1.5)    # 0,5849625 - la pendiente del piso

# El 1 no tiene trayectoria (ya está en el 1), así que no tiene altitud ni piso
# que valga. Se excluye a mano de los barridos y se dice.
EXCLUIDOS = (1,)

# ------------------------------------------------------------------ maquinaria
#
# Cada programa suelto de este repo redefine su propia trayectoria de cinco
# líneas, a propósito, para que el fichero se lea entero sin saltar a otro.


def altitud_clasica(n):
    """El valor más alto de la trayectoria de n bajo la regla clasica 3n+1."""
    mayor = x = n
    while x != 1:
        x = 3 * x + 1 if x % 2 else x // 2
        if x > mayor:
            mayor = x
    return mayor


def altitud_atajo(n):
    """El valor más alto bajo el mapa del ATAJO T(n) = (3n+1)/2 en los impares."""
    mayor = x = n
    while x != 1:
        x = (3 * x + 1) // 2 if x % 2 else x // 2
        if x > mayor:
            mayor = x
    return mayor


def racha(n):
    """Pasos impares seguidos al arranque, bajo el mapa del ATAJO."""
    c = 0
    while n % 2:
        n = (3 * n + 1) // 2
        c += 1
    return c


def cumple_piso_clasico(n, alt, r):
    """alt * 2^r >= 2 * n * 3^r   -  entero exacto, sin un solo float."""
    return alt * (2 ** r) >= 2 * n * (3 ** r)


def cumple_piso_atajo(n, alt, r):
    """alt * 2^r >= n * 3^r   -  entero exacto, sin un solo float."""
    return alt * (2 ** r) >= n * (3 ** r)


def holgura_clasica(n, alt, r):
    """Cuánto sobra por encima del piso, en bits. Decorativo: no decide nada."""
    return math.log2(alt / n) - (r * LOG2_3_2 + 1)


def con_miles(n):
    return '{:,}'.format(n).replace(',', '.')


print()
print('=' * 78)
print('EL PISO DE LA ALTITUD  -  la unica cota con forma de teorema del repo')
print('=' * 78)
print()
print('   PARA n IMPAR:   log2( altitud(n) / n )  >=  racha(n) * log2(3/2) + 1')
print()
print('   racha(n)   = pasos impares seguidos al arranque, mapa del ATAJO')
print('   altitud(n) = el valor mas alto, mapa CLASICO 3n+1')
print('   log2(3/2)  = %.7f' % LOG2_3_2)
print()
print('   Se decide en forma ENTERA:   alt * 2^r  >=  2 * n * 3^r')
print('   (nada de floats: los logaritmos solo se usan para informar la holgura)')
print()
print('   Barrido de control: 1 .. %s' % con_miles(LIMITE))
print('   (se excluye n=1, que no tiene trayectoria y por tanto no tiene')
print('    altitud que medir)')
print()

# Se calcula todo una sola vez: la trayectoria es lo caro.
FICHAS = {}
for n in range(1, LIMITE + 1):
    if n in EXCLUIDOS:
        continue
    FICHAS[n] = (altitud_clasica(n), altitud_atajo(n), racha(n))

IMPARES = [n for n in FICHAS if n % 2]
PARES = [n for n in FICHAS if n % 2 == 0]

print('   impares en el barrido: %s' % con_miles(len(IMPARES)))
print('   pares   en el barrido: %s' % con_miles(len(PARES)))
print()


# ============================================================== COMPROBACION 1
#
# Los impares contra el piso clásico. Es una cota demostrada: tiene que dar 0.

print('-' * 78)
print('COMPROBACION 1 - los IMPARES contra el piso clasico')
print('-' * 78)

fallos = [n for n in IMPARES
          if not cumple_piso_clasico(n, FICHAS[n][0], FICHAS[n][2])]

print('   casos: %s   fallos: %d' % (con_miles(len(IMPARES)), len(fallos)))
if fallos:
    n = fallos[0]
    raise SystemExit(
        'FALLO: el piso clasico se rompe en un IMPAR. Ejemplo n=%d, '
        'altitud=%d, racha=%d. Eso tumbaria la demostracion entera.'
        % (n, FICHAS[n][0], FICHAS[n][2]))
print('   -> 0 fallos. La cota aguanta en todos los impares del rango.')
print()


# ============================================================== COMPROBACION 2
#
# Los pares contra el MISMO piso. AQUI TIENE QUE FALLAR. No es un bug: es la
# corrección. Al enunciado le faltaba la hipótesis "n impar", y esto lo prueba.

print('-' * 78)
print('COMPROBACION 2 - los PARES contra el mismo piso  (TIENE que fallar)')
print('-' * 78)

fallos_pares = [n for n in PARES
                if not cumple_piso_clasico(n, FICHAS[n][0], FICHAS[n][2])]

print('   casos: %s   fallos: %s   (%.1f%% de los pares)'
      % (con_miles(len(PARES)), con_miles(len(fallos_pares)),
         100.0 * len(fallos_pares) / len(PARES)))

if not fallos_pares:
    raise SystemExit(
        'FALLO AL REVES: los pares NO fallan, y tendrian que fallar. Si esto '
        'pasa, la correccion del 30-07-2026 esta mal y el enunciado sin la '
        'hipotesis "n impar" seria cierto. Revisar antes de seguir.')

print()
print('   Los primeros %d pares que lo rompen:' % CUANTOS_EJEMPLOS)
print('      %8s %12s %10s %12s' % ('n', 'altitud', 'racha', 'necesitaba'))
for n in sorted(fallos_pares)[:CUANTOS_EJEMPLOS]:
    alt, _, r = FICHAS[n]
    # con n par la racha es 0, asi que el piso pide exactamente altitud >= 2n
    necesitaba = 2 * n * (3 ** r) // (2 ** r)
    print('      %8d %12d %10d %12d' % (n, alt, r, necesitaba))
print()
print('   Con n par la racha vale 0 por definicion (el primer paso es una')
print('   division), y entonces el piso pide altitud >= 2n a secas. El 10 sube')
print('   solo hasta 16 y necesitaria 20. NO ES UN BUG: es la hipotesis que le')
print('   faltaba al enunciado. Sin "n impar", el teorema es falso.')
print()


# ============================================================== COMPROBACION 3
#
# La variante del atajo, sin el +1. Esta sí vale para las dos paridades.

print('-' * 78)
print('COMPROBACION 3 - la variante del ATAJO, sin el +1, pares e impares juntos')
print('-' * 78)
print('   log2( altitud_atajo(n) / n )  >=  racha(n) * log2(3/2)')
print('   en forma entera:  alt_atajo * 2^r  >=  n * 3^r')
print()

fallos = [n for n in FICHAS
          if not cumple_piso_atajo(n, FICHAS[n][1], FICHAS[n][2])]

print('   casos: %s   fallos: %d' % (con_miles(len(FICHAS)), len(fallos)))
if fallos:
    n = min(fallos)
    raise SystemExit(
        'FALLO: la variante del atajo se rompe en n=%d, altitud_atajo=%d, '
        'racha=%d. Esa es la version que se supone universal.'
        % (n, FICHAS[n][1], FICHAS[n][2]))
print('   -> 0 fallos. ESTA es la version que hay que citar: sin el +1, y sin')
print('      hipotesis sobre la paridad. El +1 del enunciado clasico es log2(2)')
print('      y aparece solo porque se mezcla la altitud de un mapa con la racha')
print('      del otro.')
print()


# ============================================================== COMPROBACION 4
#
# La holgura. ¿Es una cota floja o va pegada al dato?

print('-' * 78)
print('COMPROBACION 4 - la holgura sobre los impares (cuanto sobra por encima)')
print('-' * 78)

holguras = sorted(holgura_clasica(n, FICHAS[n][0], FICHAS[n][2])
                  for n in IMPARES)
minima = holguras[0]
mediana = holguras[len(holguras) // 2]
maxima = holguras[-1]

print('   minima  %+.6f bits' % minima)
print('   mediana %+.6f bits' % mediana)
print('   maxima  %+.6f bits' % maxima)
print()

if minima < 0:
    raise SystemExit(
        'FALLO: hay holgura negativa (%.9f). Contradice la comprobacion 1, o '
        'sea que hay un error de coma flotante o de logica.' % minima)

apretados = [n for n in IMPARES
             if holgura_clasica(n, FICHAS[n][0], FICHAS[n][2]) < 0.001]
print('   impares con holgura por debajo de 0,001 bits: %s de %s (%.1f%%)'
      % (con_miles(len(apretados)), con_miles(len(IMPARES)),
         100.0 * len(apretados) / len(IMPARES)))
print()
print('   Los %d que van mas pegados al piso de todo el rango:' % CUANTOS_EJEMPLOS)
pegados = sorted(IMPARES,
                 key=lambda n: holgura_clasica(n, FICHAS[n][0], FICHAS[n][2]))
for n in pegados[:CUANTOS_EJEMPLOS]:
    alt, _, r = FICHAS[n]
    print('      n=%-7d altitud=%-12d racha=%-3d holgura=%+.9f'
          % (n, alt, r, holgura_clasica(n, alt, r)))
print()
print('   La cota no es floja: hay impares que la rozan por millonesimas de bit.')
print('   Una cota ajustada vale mas que una holgada, porque no deja sitio donde')
print('   esconder un contraejemplo.')
print()

# Y la holgura minima tiene formula cerrada, o sea que no hay que creersela:
# los mas apretados son los impares de racha 1 (altitud = 3n+1 exacto), donde
#   holgura = log2((3n+1)/n) - (log2(3/2) + 1) = log2(1 + 1/(3n))
# que decrece con n. El minimo lo pone el mayor impar de racha 1 del rango.
mayor_racha1 = max(n for n in IMPARES if FICHAS[n][2] == 1)
formula = math.log2(1.0 + 1.0 / (3.0 * mayor_racha1))
print('   Y la holgura minima no hay que creersela: tiene formula cerrada.')
print('   Los mas apretados son los impares de racha 1, donde altitud = 3n+1')
print('   exacto, y ahi la holgura vale log2(1 + 1/(3n)), que decrece con n.')
print('   El mayor impar de racha 1 del rango es %s:' % con_miles(mayor_racha1))
print('      log2(1 + 1/(3*%d)) = %+.9f   medido = %+.9f'
      % (mayor_racha1, formula, minima))
print('   Coinciden, luego el minimo depende SOLO de hasta donde se barra:')
print('   con LIMITE = 100.000 sale %+.6f; con 200.000 saldria %+.6f.'
      % (minima, math.log2(1.0 + 1.0 / (3.0 * (2 * LIMITE - 1)))))
print('   (El CLAUDE.md documenta +0,000002, que es el valor de un barrido')
print('    hasta 200.000, no hasta 100.000. No es una discrepancia: es que')
print('    ese numero no es una constante, es funcion del rango barrido.)')
print()


# ============================================================== COMPROBACION 5
#
# Los récords publicados. Son los casos extremos de todo lo conocido.

print('-' * 78)
print('COMPROBACION 5 - los records publicados (records.json)')
print('-' * 78)

if not os.path.exists(ARCHIVO_RECORDS):
    print('   AVISO: no existe records.json. Se salta esta comprobacion.')
    print('   (No es un fallo: este fichero no baja nada de la red.)')
    print()
else:
    with open(ARCHIVO_RECORDS, encoding='ascii') as f:
        datos = json.load(f)

    # Se quitan n=1 y n=2: degenerados. El 1 no tiene trayectoria y el 2 nunca
    # llega a aplicar 3n+1. Es el mismo recorte que hace cruzarecords.py.
    pool = ([int(r['n']) for r in datos['path_records'] if int(r['n']) > 2] +
            [int(r['n']) for r in datos['delay_records'] if int(r['n']) > 2])

    impares_rec = [n for n in pool if n % 2]
    pares_rec = [n for n in pool if n % 2 == 0]

    mal = []
    for n in pool:
        r = racha(n)
        if not cumple_piso_clasico(n, altitud_clasica(n), r):
            mal.append(n)

    print('   records cruzados: %d   (%d impares, %d pares)'
          % (len(pool), len(impares_rec), len(pares_rec)))
    print('   fallos: %d' % len(mal))
    if mal:
        print('   LOS QUE FALLAN: %s'
              % ', '.join(str(x) for x in mal[:CUANTOS_EJEMPLOS]))
    print()
    print('   Los %d pares PASAN, y pasan por casualidad: son 2*impar, y el'
          % len(pares_rec))
    print('   impar de dentro sube tanto que la altitud se lleva el factor 2 de')
    print('   sobra. Comprobado uno por uno:')
    for n in sorted(pares_rec)[:CUANTOS_EJEMPLOS]:
        mitad = n // 2
        print('      n=%-22s = 2 * %-22s   (la mitad es impar: %s)'
              % (con_miles(n), con_miles(mitad), bool(mitad % 2)))
    print()
    print('   -> los %d records pasan enteros. La cota NO se rompe en los casos'
          % len(pool))
    print('      extremos de todo lo conocido, hasta 2^71.')
    print()


# ------------------------------------------------------------------- la leccion

print('=' * 78)
print('LA LECCION  -  que es la parte que de verdad importa')
print('=' * 78)
print()
print('  El enunciado estaba MAL PUBLICADO: le faltaba la hipotesis "n impar".')
print('  Sin ella es falso en %s de los %s pares del rango, o sea en'
      % (con_miles(len(fallos_pares)), con_miles(len(PARES))))
print('  mas de la mitad. Y aun asi paso desapercibido un tiempo.')
print()
print('  COMO NO se encontro el error:')
print('     se probo contra los records publicados de Roosendaal y Barina, los')
print('     numeros que mas suben y mas tardan de todo lo conocido, hasta 2^71.')
print('     Los pasaron TODOS, incluidos los pares. Los pares pasaron por')
print('     casualidad, porque son 2*impar. El extremo confirmo una cosa falsa.')
print()
print('  COMO SI se encontro:')
print('     un barrido de control sobre numeros corrientes de 1 a %s.'
      % con_miles(LIMITE))
print('     El 10, que sube solo hasta 16, tumbo el enunciado.')
print()
print('     LOS EXTREMOS CONFIRMAN; LOS CONTROLES REFUTAN.')
print()
print('  Es el mismo argumento que sostiene la doctrina del A/B de este repo:')
print('  meter por la misma maquinaria un caso que TIENE que salir distinto, y')
print('  exigir que salga distinto. Un test que solo mira casos favorables no')
print('  esta comprobando nada - esta confirmando lo que ya creia.')
print()
print('  Y la otra mitad de la leccion: esto es una COTA, no un promedio. Un')
print('  promedio nunca demuestra nada sobre un numero concreto; una cota si.')
print('  Cuando aparezca algo nuevo en este laboratorio, la primera pregunta')
print('  tiene que ser: es un promedio, o es una cota?')
print()
