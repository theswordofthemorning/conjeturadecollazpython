# -*- coding: utf-8 -*-
#
# VERIFICAR LA FRONTERA DE EXCLUSION DE CICLOS -- REVISION ADVERSARIAL DE
# verificar_terras.py, SECCION [6](d)
# ==============================================================================
#
# QUE SE REVISA. El fichero verificar_terras.py re-deriva la exclusion de ciclos
# de Collatz por periodo, a partir de la identidad exacta
#
#     2^k / 3^S  =  producto sobre los impares del ciclo de (1 + 1/(3 n_i))
#
# y de una cota inferior X para el minimo del ciclo (X = el limite verificado por
# fuerza bruta). Un periodo k queda EXCLUIDO si, con S = mayor S con 3^S < 2^k,
#
#     k*ln2 - S*ln3  >  S * ln(1 + 1/(3X))
#
# La identidad y el criterio son CORRECTOS -- se comprueban abajo otra vez. Lo
# que esta mal es COMO SE EXTRAE LA FRONTERA, y son dos metodos distintos
# presentados como uno:
#
#   (c) del fichero: evalua TODOS los k con enteros puros y devuelve
#       "primer k que falla" - 1.                                    <- TIGHT
#   (d) del fichero: evalua SOLO los jump values y devuelve el
#       ULTIMO JUMP VALUE QUE PASA.                                  <- FLOJO
#
# Como los jump values estan MUY espaciados (el hueco antes de la frontera de
# 2^71 es de factor 11), (d) tira a la basura un factor 10-17. El fichero pone
# (c) en la tabla de X pequenos y (d) en la tabla de X grandes, y presenta (c)
# como "CONTROL" de (d): el control solo compara k_falla, que es justo la unica
# cantidad que los dos calculan igual, asi que no podia cazar nada.
#
# CONSECUENCIA. El fichero concluye que su derivacion da 17.026.679.261 pasos
# clasicos, "el 87,4% de la cifra publicada" (19.478.780.533), y que por tanto
# "la cifra publicada queda CORROBORADA". Con la frontera bien extraida el mismo
# argumento da 186.265.759.593 pasos clasicos: 9,56 VECES esa cifra.
# O sea lo contrario de corroborarla -- la deja senalada como la cota DEBIL,
# que es exactamente el fallo que esta revision existe para cazar.
#
# ------------------------------------------------------------------------------
# ESTADO (01-08-2026): LA CORRECCION YA ESTA APLICADA
# ------------------------------------------------------------------------------
# verificar_terras.py [6](d) ya devuelve k_falla - 1, y comprueba el hueco en su
# propia seccion (e). Las constantes REPORTA_* de abajo son los numeros que ese
# fichero imprimia ANTES del arreglo, y se dejan a proposito: son el registro de
# que la revision reprodujo el error antes de corregirlo. Si algun dia dejan de
# reproducirse, este fichero corta con SystemExit y hay que mirar por que.
#
# Y un segundo hallazgo, posterior, que cambia contra QUIEN se contrasta: la
# cifra buena con X_0 = 2^71 NO es 19.478.780.533 (Laurore 2025, ya descartada)
# NI 217.976.794.617 (Barina 2025 seccion 6, que repite Wikipedia). Es
# 114.208.327.604 pasos de atajo / 186.265.759.595 clasicos -- justo lo que sale
# aqui. La cifra de Barina exige X_0 >= 2^71,884 y el record esta en 2^71,019.
# Ver verificar_ciclos.py, que lo certifica por tres caminos independientes.
#
# ------------------------------------------------------------------------------
# QUE SE COMPRUEBA AQUI, EN ESTE ORDEN, CORTANDO SI FALLA
# ------------------------------------------------------------------------------
#
#   [A] La identidad de ciclo, en los cuatro ciclos que existen sobre Z. Fraction.
#   [B] (c) y (d) NO devuelven lo mismo. Enteros exactos contra decimal.
#   [C] El hueco entre el ultimo jump que pasa y el primero que falla TAMBIEN
#       esta excluido -- se demuestra, no se supone: dentro del hueco los unicos
#       k con forma lineal pequena son los MULTIPLOS m*K_j, y para esos el
#       cociente izq/b es CONSTANTE, luego heredan el margen de K_j; cualquier
#       otro k tiene izq >= izq(K_{j-1}), que ya supera el umbral maximo.
#   [D] La tabla corregida, y el contraste con la cifra que cita el CLAUDE.md.
#
# NOTA DE ARITMETICA. [A] [B] son enteros y Fraction. [C] [D] necesitan k ~ 10^11
# (2^k no cabe en memoria) y usan decimal con PRECISION DECLARADA de 300 digitos;
# el metodo decimal se valida en [B] reproduciendo el resultado entero exacto.
#
# ==============================================================================

from fractions import Fraction
from decimal import Decimal, getcontext

# ----- CONSTANTES EDITABLES ---------------------------------------------------

PRECISION_DECIMAL = 300
TERMINOS_CF = 30

CICLOS_CONOCIDOS = [1, -1, -5, -17]      # los cuatro ciclos de Collatz sobre Z

X_ENTEROS = [10**3, 10**4, 10**5, 10**6, 10**8]   # donde (c) es viable con int
K_MAX_ENTEROS = 30000

LIMITES = [("Terras 1976, verificado ~10^8", 10**8),
           ("Oliveira e Silva 2008, 2^62", 2**62),
           ("Barina 2025, 2^71 (record de hoy)", 2**71)]

CITA_CLAUDEMD = 19_478_780_533    # "cualquier otro ciclo mide >= esto PASOS"
PERIODO_TERRAS = 2592             # el numero que el CLAUDE.md atribuye a 1976

# los numeros que reporta verificar_terras.py, para contrastarlos
REPORTA_TERRAS_1976 = 23_673
REPORTA_OES_2008 = 630_138_897
REPORTA_BARINA_2071 = 10_439_860_591
REPORTA_CLASICOS = 17_026_679_261

getcontext().prec = PRECISION_DECIMAL
LN2 = Decimal(2).ln()
LN3 = Decimal(3).ln()
GAMMA = LN3 / LN2                 # log2(3)

fallos = []


def atajo(n):
    """T(n) = n/2 si par, (3n+1)/2 si impar. Exacto en Z, tambien negativos."""
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


print("=" * 78)
print("REVISION ADVERSARIAL DE verificar_terras.py [6](d)")
print("=" * 78)


# ==============================================================================
# [A] La identidad de ciclo. Es correcta, y hay que dejarlo dicho.
# ==============================================================================

print("\n[A] la identidad de ciclo  2^k/3^S = prod (1 + 1/(3 n_i))   (Fraction)")
for inicio in CICLOS_CONOCIDOS:
    orbita = [inicio]
    x = atajo(inicio)
    while x != inicio:
        orbita.append(x)
        x = atajo(x)
    k = len(orbita)
    S = sum(1 for y in orbita if y % 2 != 0)
    izq = Fraction(2 ** k, 3 ** S)
    der = Fraction(1)
    for y in orbita:
        if y % 2 != 0:
            der *= (1 + Fraction(1, 3 * y))
    if izq != der:
        fallos.append(f"[A] identidad rota en el ciclo de {inicio}")
    print(f"    ciclo de {inicio:>4}:  k={k:>3} S={S:>3}  {izq} == {der}  ->  {izq == der}")
print(f"    fallos: {len(fallos)}   -- el criterio de verificar_terras.py es CORRECTO")


# ==============================================================================
# [B] (c) y (d) del fichero no devuelven lo mismo
# ==============================================================================

def tight_entero(X, kmax):
    """(c) del fichero: TODOS los k, enteros puros. Devuelve (mayor, primer_fallo).

    periodo k excluido  <=>  2^k * (3X)^S > (3*(3X+1))^S
    """
    U, V = 3 * X, 3 * (3 * X + 1)
    potU = potV = 1
    S, pot3, pot2 = 0, 1, 1
    for k in range(1, kmax + 1):
        pot2 *= 2
        while pot3 * 3 < pot2:
            pot3 *= 3
            S += 1
            potU *= U
            potV *= V
        if S < 1:
            continue
        if not (pot2 * potU > potV):
            return k - 1, k
    return kmax, None


# los jump values, desde la fraccion continua de log2(3)
x = GAMMA
CF = []
for _ in range(TERMINOS_CF):
    a = int(x)
    CF.append(a)
    f = x - a
    if f == 0:
        break
    x = 1 / f
p_ant, q_ant = 1, 0
p, q = CF[0], 1
puntos = [(p, q)]
for i in range(1, len(CF)):
    a = CF[i]
    for j in range(1, a + 1):
        puntos.append((p_ant + j * p, q_ant + j * q))
    p_ant, q_ant, p, q = p, q, p_ant + a * p, q_ant + a * q
    puntos.append((p, q))
JUMPS = [(1, 0)] + sorted({(kk, bb) for kk, bb in puntos
                           if bb > 0 and Decimal(kk) > Decimal(bb) * GAMMA})


def flojo_decimal(X):
    """(d) del fichero, copia literal. Devuelve (k_seguro, b_seguro, k_falla)."""
    paso = (1 + Decimal(1) / (3 * Decimal(X))).ln()
    mejor, seguro = None, (None, None)
    for kk, bb in JUMPS:
        izq = kk * LN2 - bb * LN3
        mejor = izq if mejor is None else min(mejor, izq)
        if mejor > bb * paso:
            seguro = (kk, bb)
        else:
            return seguro[0], seguro[1], kk
    return seguro[0], seguro[1], None


print(f"\n[B] (c) entero exacto contra (d) decimal, para el MISMO X")
print(f"    {'X':>14} {'(c) TIGHT':>14} {'(d) k_seguro':>14} {'(d) k_falla':>14}  iguales?")
for X in X_ENTEROS:
    mayor, pf = tight_entero(X, K_MAX_ENTEROS)
    ks, bs, kf = flojo_decimal(X)
    # el decimal tiene que coincidir con el entero en el PRIMER FALLO
    if pf is not None and kf != pf:
        fallos.append(f"[B] decimal y entero discrepan en k_falla para X={X}")
    if pf is not None and mayor != pf - 1:
        fallos.append(f"[B] tight_entero incoherente para X={X}")
    print(f"    {X:>14,} {mayor:>14,} {ks:>14,} {kf:>14,}  {mayor == ks}")
print(f"    fallos: {len([f for f in fallos if f.startswith('[B]')])}")
print(f"    -> el metodo decimal reproduce el ENTERO EXACTO en k_falla siempre,")
print(f"       o sea que el decimal no miente. Lo que falla es que (d) reporta")
print(f"       el ultimo JUMP VALUE que pasa y no el ultimo k que pasa.")
if any(tight_entero(X, K_MAX_ENTEROS)[0] == flojo_decimal(X)[0] for X in X_ENTEROS):
    fallos.append("[B] (c) y (d) coinciden en algun X: la critica no se sostiene")


# ==============================================================================
# [C] El hueco tambien esta excluido. Se demuestra.
# ==============================================================================
#
# Sea K_j el ultimo jump value que pasa y K_j1 el primero que falla. Para todo
# k en (K_j, K_j1):
#   - si k = m*K_j, entonces b(k) = m*b_j y izq(k) = m*izq_j (la forma lineal es
#     aditiva mientras no se pase de ln3), luego izq(k)/b(k) = izq_j/b_j, o sea
#     el MISMO margen que K_j, que pasa;
#   - si no, por el teorema de las tres distancias izq(k) >= izq(K_{j-1}), y basta
#     comprobar que izq(K_{j-1}) supera el umbral MAXIMO del hueco, b(K_j1)*paso.

print(f"\n[C] el hueco (K_j, K_j+1) tambien esta excluido -- comprobado, no supuesto")
print(f"    {'X':>22} {'K_j':>16} {'K_j+1':>16} {'hueco':>7} {'margen mult.':>13} {'resto ok':>9}")

fronteras_tight = {}
for nombre, X in LIMITES:
    paso = (1 + Decimal(1) / (3 * Decimal(X))).ln()
    ks, bs, kf = flojo_decimal(X)
    idx = [i for i, (kk, _) in enumerate(JUMPS) if kk == ks][0]
    Kj, bj = JUMPS[idx]
    Kj_1, bj_1 = JUMPS[idx - 1]
    Kj1, bj1 = JUMPS[idx + 1]
    if Kj1 != kf:
        fallos.append(f"[C] el jump siguiente no es k_falla para X={X}")
    umbral_max = bj1 * paso
    izq_j = Kj * LN2 - bj * LN3
    izq_j_1 = Kj_1 * LN2 - bj_1 * LN3
    # margen de los multiplos (constante, pero se comprueba uno a uno)
    margen = None
    m = 1
    while m * Kj < Kj1:
        k2, b2 = m * Kj, m * bj
        iz2 = k2 * LN2 - b2 * LN3
        if iz2 >= LN3:
            fallos.append(f"[C] la aditividad se rompe en m={m}, X={X}")
        if not (iz2 > b2 * paso):
            fallos.append(f"[C] multiplo m={m} NO excluido para X={X}")
        r = iz2 / (b2 * paso)
        margen = r if margen is None else min(margen, r)
        m += 1
    resto_ok = izq_j_1 > umbral_max
    if not resto_ok:
        fallos.append(f"[C] el resto del hueco no queda cubierto para X={X}")
    fronteras_tight[X] = (Kj1 - 1, bj1 if Kj1 - 1 >= Kj1 else bj1 - 1)
    print(f"    {nombre[:22]:>22} {Kj:>16,} {Kj1:>16,} "
          f"{Decimal(Kj1)/Decimal(Kj):>6.2f}x {margen:>12.2f}x {str(resto_ok):>9}")
print(f"    fallos: {len([f for f in fallos if f.startswith('[C]')])}")


# ==============================================================================
# EL CORTE -- antes de cualquier conclusion
# ==============================================================================

if fallos:
    print()
    for f in fallos[:20]:
        print("  FALLO:", f)
    raise SystemExit(f"HAY {len(fallos)} FALLOS. Nada de lo de abajo vale.")


# ==============================================================================
# [D] La tabla corregida
# ==============================================================================

def b_de_k(k):
    """mayor b con 3^b < 2^k, en decimal a precision declarada."""
    b = int(Decimal(k) / GAMMA)
    while (b + 1) * LN3 < k * LN2:
        b += 1
    while b * LN3 >= k * LN2:
        b -= 1
    return b


print(f"\n[D] LA TABLA CORREGIDA (todas las comprobaciones de arriba pasan)")
print(f"    {'limite de fuerza bruta':<36} {'reporta [6](d)':>17} {'TIGHT':>17} {'factor':>8}")
reportados = [REPORTA_TERRAS_1976, REPORTA_OES_2008, REPORTA_BARINA_2071]
tights = []
for (nombre, X), rep in zip(LIMITES, reportados):
    ks, bs, kf = flojo_decimal(X)
    kt = kf - 1
    tights.append(kt)
    if ks != rep:
        fallos.append(f"[D] no reproduzco el numero reportado para {nombre}")
    print(f"    {nombre:<36} {rep:>17,} {kt:>17,} {kt/rep:>7.2f}x")

if fallos:
    raise SystemExit("no reproduzco los numeros de verificar_terras.py: " + str(fallos))

kt71 = tights[-1]
bt71 = b_de_k(kt71)
clasicos = kt71 + bt71

print(f"\n    frontera TIGHT con X = 2^71 (Barina 2025):")
print(f"      {kt71:,} pasos de atajo,  b = {bt71:,}")
print(f"      = {clasicos:,} pasos clasicos  (k + S)")

print(f"\n    Y la longitud MINIMA que le queda a un ciclo no trivial:")
print(f"      {kt71 + 1:,} pasos de atajo = {kt71 + 1 + b_de_k(kt71 + 1):,} clasicos")

print(f"\n    CONTRA LA CIFRA QUE CITABA EL CLAUDE.MD ({CITA_CLAUDEMD:,} pasos):")
print(f"      lo que reporta [6](d):  {REPORTA_CLASICOS:>18,}  = "
      f"{100*REPORTA_CLASICOS/CITA_CLAUDEMD:.1f}%  -> 'CORROBORADA'")
print(f"      la frontera TIGHT:      {clasicos:>18,}  = "
      f"{clasicos/CITA_CLAUDEMD:.2f}x  -> la cita es la cota DEBIL")

print(f"\n    'la frontera real esta N veces mas arriba que el 2.592':")
print(f"      reporta [6](d): {REPORTA_BARINA_2071/PERIODO_TERRAS:>14,.0f}x")
print(f"      TIGHT:          {kt71/PERIODO_TERRAS:>14,.0f}x")

print(f"\n" + "=" * 78)
print("VEREDICTO")
print("=" * 78)
print("""
  LO QUE AGUANTA de verificar_terras.py [6]: la identidad de ciclo, el criterio
  de exclusion, el metodo decimal, y la fuerza bruta. Todo eso se reproduce aqui.

  LO QUE NO: la extraccion de la frontera. (d) devuelve el ultimo JUMP VALUE que
  pasa, no el ultimo k que pasa, y los jump values estan espaciados por factores
  de 11 y de 17 justo en esa zona. Las tres filas de la tabla estan cortas.

  Y LA CONCLUSION SE DA VUELTA. El argumento elemental no "corrobora" los
  19.478.780.533 pasos que cita el CLAUDE.md: los supera 9,56 veces. Esa cifra
  es la cota DEBIL, no la frontera. Es el mismo fallo de citar por autor que ya
  mordio dos veces en este repo.

  QUE ES CADA COSA: la exclusion de periodos es una COTA ("no existe ningun ciclo
  con periodo <= K"), y por eso vale. Pero una cota mal extraida sigue siendo una
  cota valida -- solo que floja. Lo que NO vale es usar una cota que sabes floja
  para bendecir un numero publicado.
""")
