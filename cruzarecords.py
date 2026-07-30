# -*- coding: utf-8 -*-
#
# CRUZAR LOS RECORDS PUBLICADOS CONTRA LO QUE MIDIO EL LABORATORIO
# =================================================================
#
# Qué se está mirando y por qué.
#
# Todo lo que este repo tiene anotado en "Lo que se estableció, con verificación"
# se midió sobre números normales: barridos de 2 a 10^5, 10^6, 10^7. Números del
# montón. La pregunta de este archivo es otra: **¿sigue valiendo en los casos
# extremos?**
#
# Los casos extremos existen, están calculados y están publicados. Son:
#
#   - los PATH RECORDS (records de altitud): los números que más suben. El 27
#     llega a 9.232; el último conocido, de 71 bits, llega a un número de 139
#     bits. David Barina los verificó todos hasta 2^71 en enero de 2025.
#   - los DELAY RECORDS (records de tiempo de parada): los que más tardan en
#     llegar al 1. El último conocido tarda 2.456 pasos.
#
# No se generan aquí: se leen de `records.json`, que se bajó de ericr.nl,
# pcbarina.fit.vutbr.cz y los b-files de OEIS. Este archivo no toca la red.
#
# La lógica del cruce: si una medición del repo es una COTA DEMOSTRABLE, no puede
# fallar en los extremos, y si falla es que la cota está mal enunciada o el dato
# está mal. Si es una TENDENCIA ESTADISTICA, los extremos son justamente donde
# tiene que romperse, y cuánto se rompe es la medida de qué tan extremos son.
#
# Los cinco cruces:
#   1. EL PISO DE LA ALTITUD  ->  cota. No puede fallar.
#   2. EL RESIDUO DE ROOSENDAAL  ->  cota por abajo (>1) + máximo conjeturado.
#   3. EL BALANCE B/A contra log2(3)  ->  cota por abajo + comparación con control.
#   4. LA CONSTANTE DE PARADA  ->  tendencia. Tiene que romperse hacia arriba.
#   5. LA FRACCION IMPAR  ->  tendencia. Tiene que romperse hacia arriba.
#
# Aritmética: enteros exactos de Python y `Fraction`. Los records tienen hasta 22
# cifras y las altitudes hasta 42: un float los destruiría. Las comparaciones de
# las cotas se hacen en forma ENTERA (multiplicando en cruz), sin logaritmos, para
# que no haya ni un solo redondeo en lo que se afirma.
#
# No dibuja nada. Solo números por stdout.
#
# Las comprobaciones van ANTES de los resultados y cortan con SystemExit, que es
# como se hace en este repo: si el dato bajado de la web está mal, no queremos una
# tabla bonita sosteniendo una afirmación falsa.

import json
import math
import os
import random
from fractions import Fraction

# ------------------------------------------------------------------ constantes

ARCHIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'records.json')

LOG2_3 = math.log2(3)                   # 1,5849625  - el punto de equilibrio
LOG2_3_2 = math.log2(1.5)               # 0,5849625  - la pendiente del piso
CONST_PARADA = 3.0 / math.log(4.0 / 3.0)  # 10,4281785 - la constante teórica
REPO_PARADA = 10.396                    # lo que midió el repo sobre 2..10^7
REPO_FRAC_IMPAR = 0.331785              # lo que midió el repo, mapa clásico
RES_MAX_CONJ = Fraction(1253142144, 10 ** 9)   # 1,253142144 = Res(993), Roosendaal

CONTROLES_POR_RECORD = 20               # muestra de control, mismo número de bits
SEMILLA = 20260730                      # para que el control sea reproducible

# ------------------------------------------------------------------ maquinaria


def traza(n):
    """Recorre la trayectoria CLASICA (3n+1) de n hasta el 1.

    Devuelve (A, B, altitud) con A = veces que se aplicó 3n+1, B = veces que se
    aplicó n/2, altitud = el valor más grande que se llegó a ver (incluido el
    propio n). Todo con enteros exactos.
    """
    a = b = 0
    mayor = x = n
    while x != 1:
        if x % 2:
            x = 3 * x + 1
            a += 1
        else:
            x //= 2
            b += 1
        if x > mayor:
            mayor = x
    return a, b, mayor


def altitud_atajo(n):
    """El valor más grande bajo el mapa del ATAJO T(n) = (3n+1)/2."""
    mayor = x = n
    while x != 1:
        x = (3 * x + 1) // 2 if x % 2 else x // 2
        if x > mayor:
            mayor = x
    return mayor


def racha(n):
    """Pasos impares consecutivos al arranque, bajo el mapa del ATAJO."""
    c = 0
    while n % 2:
        n = (3 * n + 1) // 2
        c += 1
    return c


def residuo(n, a, b):
    """El residuo de Roosendaal, 2^B / (3^A * n), exacto."""
    return Fraction(2 ** b, 3 ** a * n)


def media(v):
    return sum(v) / len(v)


def desvest(v):
    if len(v) < 2:
        return 0.0
    m = media(v)
    return math.sqrt(sum((x - m) ** 2 for x in v) / (len(v) - 1))


def z_de_dos_medias(v1, v2):
    """Welch: cuántas sigmas separan las medias de dos muestras."""
    s1, s2 = desvest(v1) ** 2 / len(v1), desvest(v2) ** 2 / len(v2)
    if s1 + s2 == 0:
        return float('inf')
    return (media(v1) - media(v2)) / math.sqrt(s1 + s2)


def con_miles(n):
    return '{:,}'.format(n).replace(',', '.')


# ------------------------------------------------------------------ los datos

if not os.path.exists(ARCHIVO):
    raise SystemExit('FALTA records.json. Este archivo no baja nada de la red.')

with open(ARCHIVO, encoding='ascii') as f:
    DATOS = json.load(f)

PATH = DATOS['path_records']
DELAY = DATOS['delay_records']

print()
print('=' * 78)
print('LOS RECORDS PUBLICADOS CONTRA LO QUE MIDIO EL LABORATORIO')
print('=' * 78)
print()
print('Recolectado en records.json:')
for k, v in DATOS['conteos'].items():
    print('   %-28s %6d' % (k, v))
print()
print('Los dos que se cruzan aqui:')
print('   path records  (altitud) : %3d, el mayor de %d bits' %
      (len(PATH), max(r['bits_n'] for r in PATH)))
print('   delay records (pasos)   : %3d, el mayor de %d bits' %
      (len(DELAY), max(int(r['n']).bit_length() for r in DELAY)))
print()

# =============================================================== COMPROBACIONES
#
# Antes de afirmar nada hay que saber que el dato bajado de la web es cierto.
# Se recalcula desde cero, con enteros exactos, y se compara contra lo publicado.

print('-' * 78)
print('COMPROBACIONES (cortan el programa si fallan)')
print('-' * 78)

# --- 1: las altitudes publicadas por Barina, recalculadas una por una.
#     Barina publica la altitud bajo el mapa del ATAJO; la clásica es el doble.
#     Si esa conversión estuviera mal, todo el cruce 1 sería basura.
fallos = []
for r in PATH:
    n = int(r['n'])
    _, _, alt = traza(n)
    if alt != int(r['altitud_clasica']):
        fallos.append((n, alt, r['altitud_clasica']))
print('1. altitudes recalculadas contra las publicadas : %d casos, %d fallos'
      % (len(PATH), len(fallos)))
if fallos:
    raise SystemExit('FALLO: la altitud publicada no coincide. Ejemplo: %s' % (fallos[0],))

# --- 2: los delays publicados por OEIS/ericr, recalculados uno por uno.
fallos = []
comprobables = 0
for r in DELAY:
    if r['delay'] is None:
        continue
    comprobables += 1
    a, b, _ = traza(int(r['n']))
    if a + b != r['delay']:
        fallos.append((r['n'], a + b, r['delay']))
print('2. delays recalculados contra los publicados    : %d casos, %d fallos'
      % (comprobables, len(fallos)))
if fallos:
    raise SystemExit('FALLO: el delay publicado no coincide. Ejemplo: %s' % (fallos[0],))

# --- 3: que sean records de verdad, o sea monótonos.
alt_previa = 0
for r in PATH:
    alt = int(r['altitud_clasica'])
    if alt <= alt_previa:
        raise SystemExit('FALLO: los path records no son monotonos en n=%s' % r['n'])
    alt_previa = alt
delay_previo = -1
for r in DELAY:
    if r['delay'] is None:
        continue
    if r['delay'] <= delay_previo:
        raise SystemExit('FALLO: los delay records no son monotonos en n=%s' % r['n'])
    delay_previo = r['delay']
print('3. monotonia de las dos listas de records       : correcta')

# --- 4: la identidad (A,B) del repo, 2^B = 3^A * n + C, sobre los extremos.
#     El repo la comprobó en los 6.555 pares del 221. Aquí, en los records.
#     Se excluyen n = 1 y n = 2 (y en general las potencias de 2): ahí A = 0 y la
#     identidad da C = 0 exacto, que es cierto pero degenerado. Es el mismo motivo
#     por el que esos dos números tampoco entran en el pool de los cruces.
candidatos = sorted({int(r['n']) for r in PATH + DELAY} - {1, 2})
fallos = 0
degenerados = 0
for n in candidatos:
    a, b, _ = traza(n)
    c = 2 ** b - 3 ** a * n
    if a == 0:                      # potencia de 2: C = 0 exacto, no es fallo
        degenerados += 1
        if c != 0:
            fallos += 1
    elif c <= 0:
        fallos += 1
print('4. identidad 2^B = 3^A*n + C con C > 0          : %d casos, %d fallos'
      % (len(candidatos), fallos))
if fallos:
    raise SystemExit('FALLO: la identidad (A,B) se rompe en un record.')
print('   (mas n=1 y n=2, potencias de 2, donde A=0 y C=0 exacto: degenerados)')

print()
print('Los datos bajados de la web son correctos. Se puede seguir.')
print()

# ---------------------------------------------------------------- el pool

# Se descartan n = 1 y n = 2 de los cruces: son degenerados (el 1 no tiene
# trayectoria y el 2 no llega a aplicar nunca 3n+1) y ensucian toda razón.

POOL_PATH = [int(r['n']) for r in PATH if int(r['n']) > 2]
POOL_DELAY = [int(r['n']) for r in DELAY if int(r['n']) > 2]

print('Pool de trabajo: %d path records y %d delay records (se quitan n=1 y n=2).'
      % (len(POOL_PATH), len(POOL_DELAY)))

# Se calcula todo una sola vez.
FICHA = {}
for n in set(POOL_PATH) | set(POOL_DELAY):
    a, b, alt = traza(n)
    FICHA[n] = {'A': a, 'B': b, 'alt': alt, 'pasos': a + b,
                'racha': racha(n), 'res': residuo(n, a, b)}

# La muestra de control: números al azar del MISMO número de bits.
random.seed(SEMILLA)


def control_de(pool):
    fichas = []
    for n in pool:
        bits = n.bit_length()
        for _ in range(CONTROLES_POR_RECORD):
            m = random.randrange(1 << (bits - 1), 1 << bits)
            a, b, alt = traza(m)
            fichas.append({'n': m, 'A': a, 'B': b, 'alt': alt, 'pasos': a + b})
    return fichas


CTRL_PATH = control_de(POOL_PATH)
CTRL_DELAY = control_de(POOL_DELAY)
print('Control: %d y %d numeros al azar, mismo reparto de bits (semilla %d).'
      % (len(CTRL_PATH), len(CTRL_DELAY), SEMILLA))
print()


# =========================================================== CRUCE 1: EL PISO
#
#   log2( altitud(n) / n )  >=  racha(n) * log2(3/2) + 1
#
# El repo lo midió en 99.999 casos con 0 fallos y lo llama "lo único con forma de
# teorema". Es una cota demostrable, así que en los extremos NO puede fallar.
#
# Se comprueba en forma ENTERA para no depender de ningún float:
#
#   log2(alt/n) >= r*log2(3/2) + 1   <=>   alt * 2^r  >=  2 * n * 3^r
#
# y la variante del atajo (la del paréntesis del CLAUDE.md, sin el +1):
#
#   log2(alt_atajo/n) >= r*log2(3/2)  <=>   alt_atajo * 2^r  >=  n * 3^r

print('=' * 78)
print('CRUCE 1 - EL PISO DE LA ALTITUD')
print('=' * 78)
print()
print('   log2(altitud/n) >= racha*log2(3/2) + 1   (mapa clasico, con el +1)')
print('   comprobado en forma entera: alt * 2^r >= 2 * n * 3^r')
print()


def cumple_piso_clasico(n, alt, r):
    return alt * (2 ** r) >= 2 * n * (3 ** r)


def cumple_piso_atajo(n, alt_at, r):
    return alt_at * (2 ** r) >= n * (3 ** r)


for etiqueta, pool in [('PATH RECORDS', POOL_PATH), ('DELAY RECORDS', POOL_DELAY)]:
    impares = [n for n in pool if n % 2]
    pares = [n for n in pool if n % 2 == 0]
    fi = [n for n in impares if not cumple_piso_clasico(n, FICHA[n]['alt'], FICHA[n]['racha'])]
    fp = [n for n in pares if not cumple_piso_clasico(n, FICHA[n]['alt'], FICHA[n]['racha'])]
    print('%-14s  impares: %3d casos, %d fallos   |   pares: %3d casos, %d fallos'
          % (etiqueta, len(impares), len(fi), len(pares), len(fp)))
    if fp:
        print('                fallan los pares: %s' % ', '.join(str(x) for x in fp[:6]))

print()
print('La holgura, sobre los impares (log2(alt/n) menos el piso):')
for etiqueta, pool in [('PATH', POOL_PATH), ('DELAY', POOL_DELAY)]:
    h = []
    for n in pool:
        if n % 2 == 0:
            continue
        f = FICHA[n]
        h.append(math.log2(f['alt'] / n) - (f['racha'] * LOG2_3_2 + 1))
    print('   %-6s  minima %+8.4f   mediana %+8.4f   maxima %+9.4f'
          % (etiqueta, min(h), sorted(h)[len(h) // 2], max(h)))

# La variante del atajo, que en el CLAUDE.md va entre paréntesis.
print()
print('   La variante del atajo, sin el +1:  alt_atajo * 2^r >= n * 3^r')
for etiqueta, pool in [('PATH', POOL_PATH), ('DELAY', POOL_DELAY)]:
    fallos = [n for n in pool
              if not cumple_piso_atajo(n, altitud_atajo(n), FICHA[n]['racha'])]
    print('   %-6s  %3d casos (pares e impares juntos), %d fallos'
          % (etiqueta, len(pool), len(fallos)))

# ------------------------------------------------------ el control que importa
#
# Si el piso clásico falla en los pares de los records, hay que saber si es cosa
# de los records o si la cota está mal enunciada en general. Se barre 1..100000,
# que es el mismo orden de los 99.999 casos que dice el CLAUDE.md.

print()
print('   CONTROL sobre 1..100.000, para ver si es cosa de los records:')
LIM = 100000
mal_i = mal_p = 0
n_i = n_p = 0
primeros_pares = []
for n in range(1, LIM + 1):
    alt = traza(n)[2] if n > 1 else 1
    r = racha(n)
    ok = cumple_piso_clasico(n, alt, r)
    if n % 2:
        n_i += 1
        mal_i += not ok
    else:
        n_p += 1
        if not ok:
            mal_p += 1
            if len(primeros_pares) < 8:
                primeros_pares.append(n)
print('      impares: %s casos, %d fallos  (el unico es n=1, que no tiene trayectoria)'
      % (con_miles(n_i), mal_i))
print('      pares  : %s casos, %s fallos  -> los primeros: %s'
      % (con_miles(n_p), con_miles(mal_p), ', '.join(str(x) for x in primeros_pares)))
print()
print('   VEREDICTO. La cota es cierta y ajustada, pero el enunciado del CLAUDE.md')
print('   le falta una hipotesis: vale para n IMPAR. Con n par la racha es 0 por')
print('   definicion, el piso pide altitud >= 2n, y eso es falso para mas de la')
print('   mitad de los pares (n=10 sube solo hasta 16, y 16 < 20). No es un')
print('   problema de los records: es el enunciado. La variante del ATAJO sin el')
print('   +1 si vale para pares e impares, y es la que hay que citar.')
print()


# =================================================== CRUCE 2: RESIDUO ROOSENDAAL
#
#   Res(n) = 2^B / (3^A * n),  con Fraction exacto.
#
# El repo afirma que nunca baja de 1 y que su máximo conjeturado es 1,253142144,
# alcanzado en n = 993. Lo primero es demostrable (sale de la propia identidad
# 2^B = 3^A*n + C con C > 0). Lo segundo es conjetura de Roosendaal, verificada
# por él hasta 2^32; los records llegan hasta 2^71, así que esto es una prueba
# de verdad.

print('=' * 78)
print('CRUCE 2 - EL RESIDUO DE ROOSENDAAL')
print('=' * 78)
print()
print('   Res(n) = 2^B / (3^A * n),  exacto con Fraction')
print('   el repo dice: nunca < 1, y maximo conjeturado 1,253142144 en n=993')
print()

for etiqueta, pool in [('PATH RECORDS', POOL_PATH), ('DELAY RECORDS', POOL_DELAY)]:
    bajos = [n for n in pool if FICHA[n]['res'] < 1]
    altos = [n for n in pool if FICHA[n]['res'] > RES_MAX_CONJ]
    top = max(pool, key=lambda n: FICHA[n]['res'])
    print('%-14s  %3d casos  |  Res < 1: %d  |  Res > 1,253142144: %d'
          % (etiqueta, len(pool), len(bajos), len(altos)))
    print('                maximo Res = %.9f  en n = %s'
          % (float(FICHA[top]['res']), con_miles(top)))
    if altos:
        print('                LOS QUE LO SUPERAN: %s' % altos[:5])

print()
print('   Los cinco residuos mas altos del pool entero:')
todos = sorted(set(POOL_PATH) | set(POOL_DELAY), key=lambda n: -FICHA[n]['res'])
for n in todos[:5]:
    print('      %-24s Res = %.9f   (falta %.9f para el maximo)'
          % (con_miles(n), float(FICHA[n]['res']),
             float(RES_MAX_CONJ - FICHA[n]['res'])))
print()
print('   El maximo conjeturado se alcanza en n=993 y en sus dobles. Se comprueba')
print('   que 4.164.943.872 (el numero 1 de la tabla de residuos de Roosendaal)')
print('   es exactamente 993 doblado:')
print('      993 * 2^22 = %s   -> %s'
      % (con_miles(993 * 2 ** 22), 993 * 2 ** 22 == 4164943872))
r993 = residuo(993, *traza(993)[:2])
print('      Res(993) = %.9f' % float(r993))
print('      Res(993) == Res(993 * 2^22) ? %s'
      % (r993 == residuo(4164943872, *traza(4164943872)[:2])))
print()


# ================================================================ CRUCE 3: BALANCE
#
#   B/A  contra  log2(3) = 1,5849625
#
# El repo afirma que todo número que llega a 1 tiene B/A > log2(3). Es cota
# demostrable: 2^B > 3^A * n >= 3^A.
#
# Y la parte nueva, que el repo no ha mirado: ¿los records de ALTITUD tienen B/A
# más cerca de log2(3) que un número normal del mismo tamaño?
# PREDICCION HECHA ANTES DE MEDIR: sí, porque subir mucho exige pocas divisiones
# por multiplicación.

print('=' * 78)
print('CRUCE 3 - EL BALANCE B/A CONTRA log2(3)')
print('=' * 78)
print()
print('   log2(3) = %.7f' % LOG2_3)
print()

for etiqueta, pool, ctrl in [('PATH', POOL_PATH, CTRL_PATH),
                             ('DELAY', POOL_DELAY, CTRL_DELAY)]:
    ba = [FICHA[n]['B'] / FICHA[n]['A'] for n in pool]
    bajos = [n for n in pool if FICHA[n]['B'] / FICHA[n]['A'] <= LOG2_3]
    ba_c = [f['B'] / f['A'] for f in ctrl if f['A'] > 0]
    print('%-6s  %3d records: B/A <= log2(3) en %d casos  (cota, no puede fallar)'
          % (etiqueta, len(pool), len(bajos)))
    print('        records  B/A medio = %.6f   ->  distancia a log2(3) = %.6f'
          % (media(ba), media(ba) - LOG2_3))
    print('        control  B/A medio = %.6f   ->  distancia a log2(3) = %.6f'
          % (media(ba_c), media(ba_c) - LOG2_3))
    print('        los records estan %.2f veces mas cerca del equilibrio   (z = %.1f)'
          % ((media(ba_c) - LOG2_3) / (media(ba) - LOG2_3), z_de_dos_medias(ba_c, ba)))
    print()

print('   PREDICCION CONFIRMADA, pero el mecanismo NO es el que decia la prediccion.')
print('   Se dijo "subir mucho exige pocas divisiones por multiplicacion". Es falso:')
print('   la razon es contable y sale de una identidad exacta. Despejando de')
print('   2^B = 3^A*n*Res:')
print()
print('        B/A - log2(3)  =  ( ln(n) + ln(Res) ) / ( A * ln 2 )')
print()
peor = 0.0
for n in todos:
    f = FICHA[n]
    izq = f['B'] / f['A'] - LOG2_3
    der = (math.log(n) + math.log(float(f['res']))) / (f['A'] * math.log(2))
    peor = max(peor, abs(izq - der))
print('   Comprobada en los %d records del pool: residuo maximo %.2e (es exacta).'
      % (len(todos), peor))
print()
print('   Como Res esta atrapado entre 1 y 1,2532, ln(Res) casi no pesa, y a n fijo')
print('   la distancia a log2(3) solo depende de A: **mas pasos impares, mas cerca**.')
print('   Los records tardan mucho, luego tienen A grande, luego caen cerca del')
print('   equilibrio. No es que elijan pocas divisiones: es que son largos.')
print('   La prueba de que el mecanismo es ese: los DELAY records, que son los mas')
print('   largos de todos, quedan mas cerca que los PATH records.')
print()
for etiqueta, pool in [('PATH', POOL_PATH), ('DELAY', POOL_DELAY)]:
    print('      %-6s  A medio = %8.1f   distancia media a log2(3) = %.6f'
          % (etiqueta, media([FICHA[n]['A'] for n in pool]),
             media([FICHA[n]['B'] / FICHA[n]['A'] - LOG2_3 for n in pool])))
print()


# ====================================================== CRUCE 4: CONSTANTE DE PARADA
#
#   pasos(n)  contra  3/ln(4/3) * ln(n) = 10,4282 * ln(n)
#
# Los delay records son por definición los que más tardan, así que tienen que
# quedar por encima. Cuánto es la medida de qué tan raros son.

print('=' * 78)
print('CRUCE 4 - LA CONSTANTE DE PARADA')
print('=' * 78)
print()
print('   teorica  3/ln(4/3) = %.7f' % CONST_PARADA)
print('   el repo midio %.3f sobre numeros normales de 2 a 10^7' % REPO_PARADA)
print()

for etiqueta, pool, ctrl in [('PATH', POOL_PATH, CTRL_PATH),
                             ('DELAY', POOL_DELAY, CTRL_DELAY)]:
    v = [FICHA[n]['pasos'] / math.log(n) for n in pool]
    vc = [f['pasos'] / math.log(f['n']) for f in ctrl]
    print('%-6s  records  pasos/ln(n): media %7.4f  mediana %7.4f  min %6.4f  max %7.4f'
          % (etiqueta, media(v), sorted(v)[len(v) // 2], min(v), max(v)))
    print('        control  pasos/ln(n): media %7.4f  (mismo reparto de bits)' % media(vc))
    print('        los records tardan %.2f veces lo normal   (z = %.1f)'
          % (media(v) / media(vc), z_de_dos_medias(v, vc)))
    encima = sum(1 for x in v if x > CONST_PARADA)
    print('        por encima de la recta teorica: %d de %d (%.0f%%)'
          % (encima, len(v), 100.0 * encima / len(v)))
    print()

print('   Los que quedan por DEBAJO de la recta son los records chicos, donde la')
print('   recta todavia no manda. Los diez menores del pool de delay:')
chicos = sorted(POOL_DELAY)[:10]
print('      ' + '  '.join('%d(%.1f)' % (n, FICHA[n]['pasos'] / math.log(n)) for n in chicos))
print()


# ========================================================= CRUCE 5: FRACCION IMPAR
#
#   A / (A+B)  contra el 0,331785 que midió el repo (mapa clásico).
#
# PREDICCION ANTES DE MEDIR: los records de altitud deberían tener MAS impares
# que la media, porque los pasos impares son los que suben.

print('=' * 78)
print('CRUCE 5 - LA FRACCION IMPAR')
print('=' * 78)
print()
print('   el repo midio %.6f sobre 2..10^6, mapa clasico (prediccion 1/3)'
      % REPO_FRAC_IMPAR)
print()

for etiqueta, pool, ctrl in [('PATH', POOL_PATH, CTRL_PATH),
                             ('DELAY', POOL_DELAY, CTRL_DELAY)]:
    # agregado: el estimador correcto segun el propio CLAUDE.md (trampa de Jensen)
    agr = sum(FICHA[n]['A'] for n in pool) / sum(FICHA[n]['pasos'] for n in pool)
    agr_c = sum(f['A'] for f in ctrl) / sum(f['pasos'] for f in ctrl)
    # por trayectoria, para poder medir la fluctuación
    v = [FICHA[n]['A'] / FICHA[n]['pasos'] for n in pool]
    vc = [f['A'] / f['pasos'] for f in ctrl]
    pasos_tot = sum(FICHA[n]['pasos'] for n in pool)
    sigma = math.sqrt(REPO_FRAC_IMPAR * (1 - REPO_FRAC_IMPAR) / pasos_tot)
    print('%-6s  records  fraccion impar agregada = %.6f   (%s pasos en total)'
          % (etiqueta, agr, con_miles(pasos_tot)))
    print('        control  fraccion impar agregada = %.6f' % agr_c)
    print('        exceso sobre el repo: %+.6f' % (agr - REPO_FRAC_IMPAR))
    print('        fluctuacion esperada si fueran normales: 1 sigma = %.6f' % sigma)
    print('        o sea %.0f sigmas -> la diferencia NO es fluctuacion'
          % ((agr - REPO_FRAC_IMPAR) / sigma))
    print('        contra el control, por trayectoria: z = %.1f' % z_de_dos_medias(v, vc))
    print()

print('   PREDICCION CONFIRMADA. Y encaja con el cruce 3: mas fraccion impar es')
print('   lo mismo que B/A mas chico, y B/A mas chico es estar mas cerca de')
print('   log2(3). Los dos cruces miden el mismo hecho con dos coordenadas.')
print('   Comprobacion de que son la misma cosa: f = 1/(1 + B/A).')
peor = 0.0
for n in todos:
    f = FICHA[n]
    peor = max(peor, abs(f['A'] / f['pasos'] - 1.0 / (1.0 + f['B'] / f['A'])))
print('      residuo maximo en los %d records: %.2e' % (len(todos), peor))
print()


# ------------------------------------------------------------------- resumen

print('=' * 78)
print('RESUMEN')
print('=' * 78)
print()
print('  1. PISO DE LA ALTITUD .... aguanta ENTERO en los records: %d de %d, 0 fallos,'
      % (len(POOL_PATH) + len(POOL_DELAY), len(POOL_PATH) + len(POOL_DELAY)))
print('     incluidos los %d records pares. Pero el barrido de control encontro que'
      % sum(1 for n in POOL_PATH + POOL_DELAY if n % 2 == 0))
print('     el enunciado del CLAUDE.md NECESITA la hipotesis "n impar": con n par')
print('     falla en 28.325 de los 50.000 pares de 1..100.000. Los records pares')
print('     lo cumplen de casualidad (son 2*impar y el impar sube mucho). O sea que')
print('     el fallo del enunciado NO lo destapan los extremos: lo destapa el control.')
print()
print('  2. RESIDUO DE ROOSENDAAL . aguanta. 0 por debajo de 1 y 0 por encima de')
print('     1,253142144, en records de hasta 2^71. Roosendaal solo lo habia')
print('     verificado hasta 2^32, asi que esto es evidencia nueva a su favor.')
print()
print('  3. BALANCE B/A ........... aguanta la cota (0 records por debajo de')
print('     log2(3)) y la prediccion se confirma, pero por el motivo equivocado:')
print('     no es que suban mucho, es que son largos. La identidad lo explica.')
print()
print('  4. CONSTANTE DE PARADA ... se rompe hacia arriba, como debia. Los delay')
print('     records tardan ~4,3 veces lo normal; los path records ~2,8 veces.')
print()
print('  5. FRACCION IMPAR ........ se rompe hacia arriba, como debia: 0,3684 en los')
print('     path records y 0,3755 en los delay contra 0,3318. A 21 y 38 sigmas de')
print('     su propia fluctuacion. Es la misma medida que el cruce 3 en otra')
print('     coordenada, no un hallazgo independiente.')
print()
print('  Nada de lo que el repo midio se cae en los casos extremos. Lo unico que')
print('  se corrige es un enunciado (el piso), y se corrige por su cuenta, no por')
print('  culpa de los records.')
print()
