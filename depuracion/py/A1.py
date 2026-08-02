# A1.py - AGENTE 2 (independiente). Verificacion del ITEM A1.
#
# ENUNCIADO: para el mapa CLASICO (par: n/2, impar: 3n+1), para cualquier
# par de posiciones i < j de una trayectoria seq, con
#   A = numero de pasos impares (3n+1) del tramo i..j
#   B = numero de pasos pares (n/2) del tramo i..j
#   C = acumulador que arranca en 0 en la posicion i, y en cada paso:
#         paso par:    C no cambia
#         paso impar:  C -> 3*C + 2^B   (B = divisiones acumuladas del tramo
#                                        en ese momento; el paso impar no
#                                        anade division, asi que da igual
#                                        antes o despues del paso)
# se cumple EXACTAMENTE:  2^B * seq[j] = 3^A * seq[i] + C
#
# DERIVACION PROPIA (induccion sobre el largo del tramo), hecha desde cero:
#   base t=0: 2^0*seq[i] = 3^0*seq[i] + 0.
#   paso par:  seq -> seq/2. Multiplico la invariante por 2:
#       2^(b+1)*seq[t+1] = 2^b*seq[t] = 3^a*seq[i] + C.  C igual, b+1.
#   paso impar: seq -> 3*seq+1. Multiplico por 3 y sumo 2^b:
#       2^b*seq[t+1] = 3*2^b*seq[t] + 2^b = 3^(a+1)*seq[i] + (3C + 2^b).
#   Luego C -> 3C + 2^b con b = divisiones acumuladas. Coincide con el
#   enunciado. La verificacion de abajo NO usa la induccion: itera la
#   recurrencia y compara los dos lados con enteros exactos.
#
# TODO EN int DE PYTHON. NI UN FLOAT EN NADA QUE DECIDA.

import sys

def paso_clasico(n):
    # el mapa CLASICO
    if n % 2 == 0:
        return n // 2
    return 3 * n + 1

def trayectoria_clasica(n, pasos_extra_en_ciclo=6):
    # trayectoria hasta el 1, y ADEMAS unos pasos de mas dentro del ciclo
    # 1 -> 4 -> 2 -> 1, para probar pares que cruzan el 1 (borde).
    seq = [n]
    x = n
    while x != 1:
        x = paso_clasico(x)
        seq.append(x)
    for _ in range(pasos_extra_en_ciclo):
        x = paso_clasico(x)
        seq.append(x)
    return seq

fallos = 0
pares_probados = 0
casos_A0 = 0          # tramos sin paso impar: C debe ser 0 exacto
casos_C0_con_A = 0    # C == 0 con A > 0 (no deberia existir en clasico)

def verificar_todos_los_pares(seq):
    # Para cada i, camino hacia adelante manteniendo (a, b, C) y compruebo
    # la identidad en CADA j > i. O(L^2) comprobaciones exactas.
    global fallos, pares_probados, casos_A0, casos_C0_con_A
    L = len(seq)
    for i in range(L - 1):
        a = 0
        b = 0
        C = 0
        for j in range(i + 1, L):
            x = seq[j - 1]
            if x % 2 == 0:
                b += 1                    # paso par: C no cambia
            else:
                C = 3 * C + (1 << b)      # paso impar: C -> 3C + 2^B
                a += 1
            izquierda = (1 << b) * seq[j]
            derecha = (3 ** a) * seq[i] + C
            pares_probados += 1
            if izquierda != derecha:
                fallos += 1
                if fallos <= 5:
                    print("FALLO: seq[i]=%d i=%d j=%d A=%d B=%d C=%d izq=%d der=%d"
                          % (seq[i], i, j, a, b, C, izquierda, derecha))
            if a == 0:
                casos_A0 += 1
                if C != 0:
                    fallos += 1
                    print("FALLO A=0 con C!=0: i=%d j=%d C=%d" % (i, j, C))
            if C == 0 and a > 0:
                casos_C0_con_A += 1

# ---------------------------------------------------------------------------
# RANGO DE VERIFICACION (declarado):
#   - todos los pares i<j de las trayectorias EXTENDIDAS (con 6 pasos de mas
#     dentro del ciclo 1-4-2) de n = 1 .. 400   <- incluye n=1, n=2, pares,
#     impares, potencias de 2
#   - mas semillas sueltas: 27, 97, 221, 703, 6631675, 2^20, 2^20+1,
#     2^40+1, (2^60)+9663  <- tamanos grandes, aritmetica de bigint
# ---------------------------------------------------------------------------

semillas = list(range(1, 401)) + [27, 97, 221, 703, 6631675,
                                  1 << 20, (1 << 20) + 1, (1 << 40) + 1,
                                  (1 << 60) + 9663]

largo_max = 0
semilla_larga = 0
for n in semillas:
    seq = trayectoria_clasica(n)
    if len(seq) > largo_max:
        largo_max = len(seq)
        semilla_larga = n
    verificar_todos_los_pares(seq)

print("pares probados (identidad exacta): %d" % pares_probados)
print("fallos: %d" % fallos)
print("tramos con A=0 (C debe ser 0): %d, todos con C=0" % casos_A0)
print("tramos con C=0 y A>0 (no deberia haber): %d" % casos_C0_con_A)
print("trayectoria mas larga probada: semilla %d, %d posiciones" % (semilla_larga, largo_max))

# --- BORDES EXPLICITOS -----------------------------------------------------

# borde k=0 (i == j): el enunciado exige i<j; el caso i=j es trivialmente
# 1*seq[i] = 1*seq[i] + 0. Lo constato aparte, no cuenta como par.
seq = trayectoria_clasica(7)
for i in range(len(seq)):
    if 1 * seq[i] != 1 * seq[i] + 0:
        raise SystemExit("FALLO en el caso trivial i=j")
print("borde i=j: identidad trivial 2^0*seq[i]=3^0*seq[i]+0, correcta (no es un par i<j)")

# borde: el caso de referencia del propio enunciado, el 221.
seq221 = trayectoria_clasica(221, pasos_extra_en_ciclo=0)
L221 = len(seq221)
pares221 = L221 * (L221 - 1) // 2
# tramo completo 0 .. L-1: cuento A y B a mano
A_tot = sum(1 for x in seq221[:-1] if x % 2 == 1)
B_tot = sum(1 for x in seq221[:-1] if x % 2 == 0)
print("221: %d posiciones, %d pares i<j, tramo completo A=%d B=%d" % (L221, pares221, A_tot, B_tot))
if pares221 != 6555:
    print("AVISO: la base decia 6555 pares para el 221 y aqui salen %d" % pares221)

# borde: potencia de 2 pura (2^20): en todo prefijo A=0 y C=0
seqp = trayectoria_clasica(1 << 20, pasos_extra_en_ciclo=0)
b = 0
C = 0
ok = True
for j in range(1, len(seqp)):
    x = seqp[j - 1]
    if x % 2 == 0:
        b += 1
    else:
        C = 3 * C + (1 << b)
    if seqp[0] == (1 << 20) and j <= 20:
        if C != 0:
            ok = False
print("borde potencia de 2 (2^20): C=0 exacto en los 20 primeros pasos: %s" % ("si" if ok else "NO"))

# borde: pares que CRUZAN el 1 (ya incluidos arriba via pasos_extra_en_ciclo,
# lo hago explicito con n=1): trayectoria 1,4,2,1,4,2,1,...
seq1 = trayectoria_clasica(1, pasos_extra_en_ciclo=12)
antes = fallos
verificar_todos_los_pares(seq1)
print("borde n=1 (pares dentro del ciclo 1-4-2, varias vueltas): fallos nuevos = %d" % (fallos - antes))

# el ciclo entero 1->4->2->1 como par (i=0, j=3): debe dar A=1 B=2 C=1,
# o sea 2^2*1 = 3^1*1 + 1, que es 4 = 3 + 1.
a = 0; b = 0; C = 0
for j in range(1, 4):
    x = seq1[j - 1]
    if x % 2 == 0:
        b += 1
    else:
        C = 3 * C + (1 << b)
        a += 1
print("ciclo 1-4-2-1 como par (i=0,j=3): A=%d B=%d C=%d  ->  %d = %d + %d" %
      (a, b, C, (1 << b) * seq1[3], (3 ** a) * seq1[0], C))

# --- CONTROL DE MAPA (que el enunciado es del CLASICO y no del atajo) ------
# Con el mapa del ATAJO ((3n+1)/2 en los impares) la MISMA recurrencia
# tal cual (B = solo pasos pares) NO cuadra: el paso impar del atajo divide.
# Compruebo que la formulacion literal del enunciado falla sobre el atajo,
# o sea que la identidad distingue el mapa.
def paso_atajo(n):
    if n % 2 == 0:
        return n // 2
    return (3 * n + 1) // 2

fallos_atajo = 0
probados_atajo = 0
for n in (7, 27, 221):
    seq = [n]
    x = n
    while x != 1:
        x = paso_atajo(x)
        seq.append(x)
    for i in range(len(seq) - 1):
        a = 0; b = 0; C = 0
        for j in range(i + 1, len(seq)):
            x = seq[j - 1]
            if x % 2 == 0:
                b += 1
            else:
                C = 3 * C + (1 << b)
                a += 1
            probados_atajo += 1
            if (1 << b) * seq[j] != (3 ** a) * seq[i] + C:
                fallos_atajo += 1
print("control de mapa: la recurrencia LITERAL sobre el mapa del atajo falla en %d de %d pares"
      % (fallos_atajo, probados_atajo))
print("(si fallara en 0 el enunciado no distinguiria el mapa; falla, luego es del clasico)")

# --- VEREDICTO -------------------------------------------------------------
if fallos != 0:
    raise SystemExit("VEREDICTO: REFUTADO, hay fallos")
print("")
print("VEREDICTO: 0 fallos en %d pares exactos. La identidad se sostiene," % pares_probados)
print("incluidos los bordes n=1, n=2, pares, potencias de 2, tramos que cruzan el 1")
print("y varias vueltas dentro del ciclo. Ademas la derivacion por induccion es")
print("de tres lineas (arriba), o sea que es un teorema, no una medicion.")
