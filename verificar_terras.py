# -*- coding: utf-8 -*-
#
# VERIFICAR TERRAS 1976 -- LA COLUMNA VERTEBRAL DEL REPO, RE-DERIVADA DESDE CERO
# ==============================================================================
#
# De quién es lo que se comprueba:
#
#   Riho Terras, "A stopping time problem on the positive integers",
#   Acta Arithmetica 30 (1976), 241-252.
#
# Todo este laboratorio cuelga de ese artículo: la identidad (A,B), la lámina,
# clasesfusion.py, pinzaciclos.py, mallaresiduos.py y la tabla de convergentes
# son corolarios suyos. Si Terras falla, no queda nada. Aquí NO se cree nada por
# estar publicado: cada afirmación se re-deriva con enteros y Fraction, y si algo
# no cuadra el programa se corta con SystemExit ANTES de sacar conclusiones.
#
# ------------------------------------------------------------------------------
# EL MAPA. HAY DOS, Y CONFUNDIRLOS ROMPE TODO.
# ------------------------------------------------------------------------------
#
#   CLASICO   C(n) = n/2 si par,   3n+1     si impar
#   ATAJO     T(n) = n/2 si par,  (3n+1)/2  si impar
#
# TERRAS USA EL DEL ATAJO. En cada comprobación se dice cuál se usa.
#
# ------------------------------------------------------------------------------
# QUE SE COMPRUEBA, Y COMO
# ------------------------------------------------------------------------------
#
# [1] T1.1   T^k(n) = lambda_k(n)*n + rho_k(n), con lambda_k = 3^{S_k}/2^k.
#            Forma cerrada contra iteración cruda, Fraction exacto. ATAJO.
#
# [2] T1.1 == la forma del repo, que escribe
#            2^B * seq[j] = 3^A * seq[i] + C,  con C -> 3C + 2^B en los impares.
#            (a) la recurrencia del repo, en TODOS los pares i<j de varias
#                trayectorias del mapa CLASICO, incluidos los 6.555 del 221;
#            (b) el puente: el C del repo es EXACTAMENTE 2^k * rho_k de Terras.
#                Sin eso las dos formas serían dos cosas parecidas, no la misma.
#
# [3] T1.2   lambda_k y rho_k dependen SOLO de n mod 2^k, y de ahí la recta
#            T^k(2^k*m + r) = 3^{S(r)}*m + T^k(r). Exhaustivo sobre TODOS los
#            restos módulo 2^K_T12. ATAJO.
#
# [4] C1.4   las k primeras paridades son independientes con P = 1/2 EXACTA.
#            Se comprueba CONTANDO RESTOS, no muestreando números: el mapa
#            resto -> vector de paridad es una biyección Z/2^k -> {0,1}^k.
#            Control con el mapa CLASICO, donde debe salir F(k+2) y no 2^k.
#
# [5] TablaC los "jump values": los k donde 3^{floor(k*gamma)}/2^k bate récord
#            acercándose a 1 POR DEBAJO, gamma = 1/log2(3). Recalculada con
#            enteros exactos y comparada contra la lista que publica el repo.
#            Y aparte: que son las convergentes/semiconvergentes, con la fracción
#            continua de log2(3) calculada de forma EXACTA, sin un solo float.
#
# [6] PERIODO "Terras excluyó los bucles de periodo <= 2592". Es la afirmación de
#            la que depende que el barrido de restos esté MUERTO. No se puede
#            leer el artículo desde aquí, pero SI se puede re-derivar la
#            exclusión entera, y eso es lo que se hace:
#              (a) la identidad exacta de ciclo
#                     2^k / 3^S = producto sobre los impares de (1 + 1/(3 n_i))
#                  comprobada en los cuatro ciclos que EXISTEN sobre Z;
#              (b) fuerza bruta: todo n < LIMITE_CICLOS baja de sí mismo, luego
#                  el mínimo de un ciclo no trivial es >= LIMITE_CICLOS;
#              (c) con (a) y (b), exclusión de periodos por aritmética entera.
#              (d) lo mismo en decimal, para los X que no caben en enteros.
#              (e) el hueco entre dos jump values consecutivos, comprobado.
#            Lo que NO se puede comprobar aquí: que ése sea el argumento de
#            Terras, ni que su número fuera exactamente 2592. Eso es historia.
#
# ------------------------------------------------------------------------------
# AVISO: LA SECCIÓN [6](d) ESTUVO MAL Y SE ARREGLÓ EL 01-08-2026
# ------------------------------------------------------------------------------
# `frontera()` devolvía el ÚLTIMO JUMP VALUE QUE PASA en vez del último periodo
# `k` que pasa. Como los jump values están espaciados por factores de 1,04 /
# 16,57 / 10,94 en esa zona, las tres filas de la tabla salían cortas por esos
# mismos factores, y de ahí salía la conclusión falsa de que esta derivación
# elemental «corroboraba» la cifra que citaba el CLAUDE.md cuando en realidad la
# supera. **Lo cazó `verificar_frontera_ciclos.py`, que es la revisión
# adversarial de esta sección**, y `verificar_ciclos.py` llega al mismo número
# por otra vía. Hoy la función devuelve `k_falla - 1` y el hueco se comprueba
# en (e). El control viejo no podía cazarlo porque sólo comparaba `k_falla`,
# que es la única cantidad que los dos métodos calculaban igual.
#
# ==============================================================================

from fractions import Fraction

# ----- CONSTANTES EDITABLES ---------------------------------------------------

SEMILLAS = [27, 221, 1276, 871, 6171, 77031, 100009, 63728127]
SEMILLAS_PARES = [27, 221, 1276, 6171, 100009]   # los O(L^2) de la comprobacion 2

K_T12 = 12                 # exhaustivo sobre los 2^K_T12 restos (comprobacion 3)
M_PRUEBA = [0, 1, 2, 3, 7, 100, 12345]

K_C14 = 16                 # exhaustivo sobre los 2^K_C14 restos (comprobacion 4)
K_C14_CLASICO = 14         # control con el mapa clasico (Fibonacci)

K_TABLA = 3000             # hasta donde se buscan jump values (comprobacion 5)

LIMITE_CICLOS = 1_000_000  # fuerza bruta: todo n < esto baja de si mismo
K_PERIODO = 8000           # hasta que periodo se intenta excluir
LIMITES_X = [10**3, 10**4, 10**5, 10**6]   # cotas inferiores del minimo del ciclo

# La lista que el CLAUDE.md publica como "Tabla C de Terras".
TABLA_C_REPO_K = [1, 2, 5, 8, 27, 46, 65, 149, 233, 317, 401, 485, 1539, 2593]
TABLA_C_REPO_B = [0, 1, 3, 5, 17, 29, 41, 94, 147, 200, 253, 306, 971, 1636]

fallos = []


def atajo(n):
    """Mapa del ATAJO: T(n) = n/2 si par, (3n+1)/2 si impar. Exacto en Z."""
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def clasico(n):
    """Mapa CLASICO: C(n) = n/2 si par, 3n+1 si impar."""
    return n // 2 if n % 2 == 0 else 3 * n + 1


def trayectoria_clasica(n):
    camino = [n]
    while n != 1:
        n = clasico(n)
        camino.append(n)
    return camino


def cuantos(prefijo):
    return len([f for f in fallos if f.startswith(prefijo)])


print("=" * 78)
print("VERIFICAR TERRAS 1976 -- re-derivacion con aritmetica exacta")
print("=" * 78)


# ==============================================================================
# [1] T1.1 -- la forma cerrada, mapa del ATAJO
# ==============================================================================
#
# Un paso del atajo se escribe de un tiron:  T(n) = (3^e * n + e)/2, e = n mod 2.
# Si T^j(n) = lambda_j*n + rho_j entonces
#     lambda_{j+1} = 3^e * lambda_j / 2      rho_{j+1} = (3^e * rho_j + e)/2
# y se comprueba EN CADA PASO que lambda_j == 3^{S_j}/2^j y que la forma cerrada
# devuelve exactamente el iterado.

print("\n[1] T1.1  T^k(n) = lambda_k*n + rho_k,  lambda_k = 3^{S_k}/2^k   (ATAJO)")
print(f"    {'n':>12} {'k (atajo)':>10} {'S_k':>6} {'bits de rho_k':>14}")

pasos_1 = 0
for semilla in SEMILLAS:
    x, lam, rho, S, k = semilla, Fraction(1), Fraction(0), 0, 0
    while x != 1:
        e = x % 2
        x = atajo(x)
        k += 1
        S += e
        lam = lam * Fraction(3 ** e, 2)
        rho = (Fraction(3 ** e) * rho + e) / 2
        if lam != Fraction(3 ** S, 2 ** k):
            fallos.append(f"[1] lambda_k mal en n={semilla}, k={k}")
        if Fraction(x) != lam * semilla + rho:
            fallos.append(f"[1] forma cerrada mal en n={semilla}, k={k}")
        pasos_1 += 1
    print(f"    {semilla:>12} {k:>10} {S:>6} "
          f"{rho.numerator.bit_length():>14}")
print(f"    pasos comprobados uno a uno: {pasos_1}   fallos: {cuantos('[1]')}")


# ==============================================================================
# [2] La forma del repo es la MISMA identidad
# ==============================================================================
#
# Demostracion en dos lineas, y es lo que la comprobacion mide:
#   par:    2^{B+1} * (x/2) = 2^B * x                      -> C no cambia
#   impar:  2^B * (3x+1) = 3*(2^B x) + 2^B = 3^{A+1} s + (3C + 2^B)
#
# OJO: el 2^B del "C -> 3C + 2^B" es el B DE ESE MOMENTO, no el final. El
# CLAUDE.md no lo aclara y leido al reves la identidad no cierra.

print("\n[2] La forma del repo   2^B*seq[j] = 3^A*seq[i] + C   (CLASICO)")
print(f"    {'n':>12} {'numeros':>9} {'pares i<j':>10}")

pares_totales = 0
for semilla in SEMILLAS_PARES:
    seq = trayectoria_clasica(semilla)
    L = len(seq)
    pares = 0
    for i in range(L):
        A = B = C = 0
        p2, p3 = 1, 1
        for j in range(i, L - 1):
            x = seq[j]
            if x % 2 == 0:
                B += 1
                p2 *= 2
            else:
                C = 3 * C + p2
                A += 1
                p3 *= 3
            if p2 * seq[j + 1] != p3 * seq[i] + C:
                fallos.append(f"[2] identidad rota en n={semilla}, i={i}, j={j+1}")
            pares += 1
    pares_totales += pares
    print(f"    {semilla:>12} {L:>9} {pares:>10}")
print(f"    pares comprobados: {pares_totales}   fallos: {cuantos('[2] ')}")
L221 = len(trayectoria_clasica(221))
print(f"    el 221 solo: {L221} numeros -> {L221*(L221-1)//2} pares"
      f"   (el CLAUDE.md dice 6.555)")

# --- el puente: C del repo == 2^k * rho_k de Terras ---------------------------
#
# k pasos de ATAJO desde n son, en el mapa CLASICO, exactamente S pasos de 3n+1
# y k pasos de n/2 (cada impar del atajo hace 3n+1 y su division de seguido).
# O sea A = S y B = k, y entonces
#     Terras:  2^k * T^k(n) = 3^S * n + 2^k * rho_k
#     repo:    2^B * seq[j] = 3^A * seq[i] + C
# son la misma identidad si y solo si C == 2^k * rho_k.

print("\n    puente Terras <-> repo:  C == 2^k * rho_k ?")
puentes = 0
for semilla in SEMILLAS:
    x, rho, C, B, k = semilla, Fraction(0), 0, 0, 0
    while x != 1:
        e = x % 2
        if e == 1:
            C = 3 * C + 2 ** B      # el 3n+1; la division que sigue no toca C
        B += 1
        rho = (Fraction(3 ** e) * rho + e) / 2
        x = atajo(x)
        k += 1
        if B != k:
            fallos.append(f"[2b] B != k en n={semilla}, k={k}")
        if Fraction(C) != Fraction(2 ** k) * rho:
            fallos.append(f"[2b] C != 2^k*rho_k en n={semilla}, k={k}")
        puentes += 1
print(f"    igualdades comprobadas: {puentes}   fallos: {cuantos('[2b]')}")


# ==============================================================================
# [3] T1.2 -- todo depende SOLO del resto
# ==============================================================================

print(f"\n[3] T1.2  lambda_k y rho_k dependen SOLO de n mod 2^k   (ATAJO)")
print(f"    exhaustivo sobre los {2**K_T12} restos de k = {K_T12}, "
      f"con m en {M_PRUEBA}")


def perfil_atajo(n, k):
    """(S_k, T^k(n), rho_k) del mapa del atajo."""
    x, S, rho = n, 0, Fraction(0)
    for _ in range(k):
        e = x % 2
        rho = (Fraction(3 ** e) * rho + e) / 2
        x = atajo(x)
        S += e
    return S, x, rho


casos_3 = 0
for r in range(2 ** K_T12):
    S_r, T_r, rho_r = perfil_atajo(r, K_T12)
    for m in M_PRUEBA:
        S_n, T_n, rho_n = perfil_atajo(2 ** K_T12 * m + r, K_T12)
        if S_n != S_r:
            fallos.append(f"[3] S_k depende de m: r={r}, m={m}")
        if rho_n != rho_r:
            fallos.append(f"[3] rho_k depende de m: r={r}, m={m}")
        if T_n != 3 ** S_r * m + T_r:
            fallos.append(f"[3] la recta falla: r={r}, m={m}")
        casos_3 += 1
print(f"    casos: {casos_3}, cada uno con 3 igualdades (S_k, rho_k y la recta)")
print(f"    la recta verificada es  T^k(2^k*m + r) = 3^(S(r))*m + T^k(r)")
print(f"    -- es el motor exacto de clasesfusion.py y de pinzaciclos.py --")
print(f"    fallos: {cuantos('[3]')}")


# ==============================================================================
# [4] C1.4 -- paridades independientes con P = 1/2 EXACTA
# ==============================================================================
#
# No se muestrea: se cuentan restos. Si el mapa resto -> vector de paridad es una
# BIYECCION Z/2^k -> {0,1}^k, entonces con el reparto uniforme de restos el vector
# de paridad es uniforme en {0,1}^k, y eso ES la independencia con p=1/2, exacta.

print(f"\n[4] C1.4  paridades independientes, P = 1/2 exacta   (ATAJO)")
print(f"    {'k':>3} {'restos':>9} {'vectores':>9} {'biyeccion':>10}"
      f"  unos en los primeros bits")

for k in range(1, K_C14 + 1):
    vistos = {}
    unos = [0] * k
    for r in range(2 ** k):
        x, v = r, 0
        for pos in range(k):
            e = x % 2
            if e:
                unos[pos] += 1
            v = (v << 1) | e
            x = atajo(x)
        vistos[v] = vistos.get(v, 0) + 1
    biy = (len(vistos) == 2 ** k) and all(c == 1 for c in vistos.values())
    if not biy:
        fallos.append(f"[4] no hay biyeccion resto->paridad en k={k}")
    if any(u != 2 ** (k - 1) for u in unos):
        fallos.append(f"[4] algun bit no sale 50/50 exacto en k={k}")
    if k <= 6 or k == K_C14:
        print(f"    {k:>3} {2**k:>9} {len(vistos):>9} {str(biy):>10}"
              f"  {' '.join(str(u) for u in unos[:8])}")

k = min(10, K_C14)
conjunta = {}
for r in range(2 ** k):
    x, bits = r, []
    for _ in range(k):
        bits.append(x % 2)
        x = atajo(x)
    for a in range(k):
        for b in range(a + 1, k):
            clave = (a, b, bits[a], bits[b])
            conjunta[clave] = conjunta.get(clave, 0) + 1
esperado = 2 ** k // 4
if [v for v in conjunta.values() if v != esperado]:
    fallos.append(f"[4] independencia por parejas rota en k={k}")
print(f"    parejas de bits (k={k}): las {len(conjunta)} casillas conjuntas valen")
print(f"    {esperado} cada una -> independencia EXACTA, no aproximada")
print(f"    fallos: {cuantos('[4]')}")

print(f"\n    CONTROL con el mapa CLASICO (debe salir F(k+2), no 2^k):")
fib = [1, 1]
while len(fib) < K_C14_CLASICO + 4:
    fib.append(fib[-1] + fib[-2])
linea = []
for k in range(2, K_C14_CLASICO + 1):
    patrones = set()
    for r in range(2 ** k):
        x, v = r, 0
        for _ in range(k):
            v = (v << 1) | (x % 2)
            x = clasico(x)
        patrones.add(v)
    fk2 = fib[k + 1]           # fib[0]=F(1), fib[1]=F(2)  ->  fib[k+1]=F(k+2)
    if len(patrones) != fk2:
        fallos.append(f"[4c] clasico k={k}: {len(patrones)} != F(k+2)={fk2}")
    if k >= K_C14_CLASICO - 3:
        linea.append(f"k={k}: {len(patrones)} = F({k+2})")
print("    " + "   ".join(linea))
print(f"    fallos: {cuantos('[4c]')}  -> los dos mapas dan cosas distintas:")
print(f"    la biyeccion (y con ella el P=1/2 exacto) es SOLO del atajo.")


# ==============================================================================
# [5] La Tabla C: los jump values
# ==============================================================================
#
# b(k) = mayor b con 3^b <= 2^k  (= floor(k*gamma), gamma = 1/log2 3), y se apunta
# k cuando 3^b/2^k bate el record de acercarse a 1 por debajo. Todo con enteros:
# comparar 3^b1/2^k1 > 3^b2/2^k2 es comparar 3^b1 * 2^k2 > 3^b2 * 2^k1.

print(f"\n[5] Tabla C -- jump values recalculados con enteros exactos, k <= {K_TABLA}")

b, pot3, pot2 = 0, 1, 1
mejor_b, mejor_k = None, None
saltos = []
for k in range(1, K_TABLA + 1):
    pot2 *= 2
    while pot3 * 3 <= pot2:
        pot3 *= 3
        b += 1
    if mejor_k is None or pot3 * (2 ** mejor_k) > (3 ** mejor_b) * pot2:
        saltos.append((k, b))
        mejor_b, mejor_k = b, k

ks = [s[0] for s in saltos]
bs = [s[1] for s in saltos]
print(f"    calculado  k = {ks[:14]}")
print(f"    el repo    k = {TABLA_C_REPO_K}")
print(f"    calculado  b = {bs[:14]}")
print(f"    el repo    b = {TABLA_C_REPO_B}")
igual_tabla = (ks[:14] == TABLA_C_REPO_K and bs[:14] == TABLA_C_REPO_B)
if not igual_tabla:
    fallos.append("[5] la Tabla C recalculada NO coincide con la del repo")
print(f"    coinciden los 14 primeros: {igual_tabla}")
print(f"    jump values hasta {K_TABLA}: {len(saltos)}.  Los que el repo NO lista:")
print(f"    k = {ks[14:]}   b = {bs[14:]}")


# --- son las convergentes/semiconvergentes? fraccion continua EXACTA ---------
#
# CF de log(u)/log(v) sin floats: a = mayor n con v^n <= u; luego (u,v)->(v,u/v^a).
# Todo Fraction, exacto. Es el algoritmo clasico de potencias.

def cf_de_log(u, v, terminos):
    u, v = Fraction(u), Fraction(v)
    salida = []
    for _ in range(terminos):
        a, p = 0, Fraction(1)
        while p * v <= u:
            p *= v
            a += 1
        salida.append(a)
        u, v = v, u / p
        if v == 1:
            break
    return salida


cf = cf_de_log(3, 2, 11)
print(f"\n    fraccion continua EXACTA de log2(3): {cf}")

p_ant, q_ant = 1, 0
p, q = cf[0], 1
convergentes = [(p, q)]
semis = []
for i in range(1, len(cf)):
    a = cf[i]
    for j in range(1, a + 1):
        semis.append((p_ant + j * p, q_ant + j * q))
    p_ant, q_ant, p, q = p, q, p_ant + a * p, q_ant + a * q
    convergentes.append((p, q))

# las que se acercan a 1 por DEBAJO cumplen 2^k > 3^b, o sea k/b > log2(3)
candidatas = sorted({(kk, bb) for (kk, bb) in semis + convergentes
                     if bb > 0 and 2 ** kk > 3 ** bb and kk <= K_TABLA})
lista_semi = [(1, 0)] + candidatas
mismo = ([kk for kk, _ in lista_semi] == ks and [bb for _, bb in lista_semi] == bs)
if not mismo:
    fallos.append("[5b] los jump values NO son las semiconvergentes")
print(f"    semiconvergentes de log2(3) con k/b > log2(3), k <= {K_TABLA}:")
print(f"    k = {[kk for kk, _ in lista_semi]}")
print(f"    identicas a los jump values: {mismo}")
print(f"    fallos: {cuantos('[5')}")


# ==============================================================================
# [6] El periodo 2592
# ==============================================================================
#
# LA IDENTIDAD DE CICLO, que es lo unico que hace falta, y sale en tres lineas.
# En un ciclo del ATAJO de k pasos con S impares, el producto de las razones da
# la vuelta y vale 1:
#
#     prod_{impares} (3n_i+1)/(2 n_i)  *  prod_{pares} (1/2)  =  1
#     prod_{impares} (3 + 1/n_i)  =  2^k
#     3^S * prod_{impares} (1 + 1/(3 n_i))  =  2^k
#
#     ==>   2^k / 3^S  =  prod_{impares} (1 + 1/(3 n_i))        [EXACTA]
#
# El minimo de un ciclo es IMPAR (si fuera par su mitad tambien estaria dentro y
# seria menor). Y todos los impares del ciclo son >= ese minimo X, luego
#
#     1  <  2^k / 3^S  <=  (1 + 1/(3X))^S
#
# Si NINGUN S cumple eso, no hay ciclo de periodo k. Y basta mirar el S mayor con
# 3^S < 2^k: al bajar S el lado izquierdo se multiplica por 3 y el derecho encoge,
# o sea que si falla ahi falla para todos los S menores.

print(f"\n[6] PERIODO -- 'Terras excluyo los bucles de periodo <= 2592'")
print(f"    (a) la identidad de ciclo, en los ciclos que EXISTEN sobre Z:")

for inicio in [1, -1, -5, -17]:
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
        fallos.append(f"[6] identidad de ciclo rota en el ciclo de {inicio}")
    print(f"        ciclo de {inicio:>4}:  k={k:>3}  S={S:>3}  "
          f"2^k/3^S = {izq}   producto = {der}   iguales: {izq == der}")
print(f"    fallos: {cuantos('[6]')}")

print(f"\n    (b) fuerza bruta: todo n < {LIMITE_CICLOS:,} baja por debajo de si")
print(f"        mismo, luego ningun ciclo tiene su minimo ahi abajo...")
peor = 0
for n in range(2, LIMITE_CICLOS):
    x, pasos = n, 0
    while x >= n:
        x = x >> 1 if x % 2 == 0 else 3 * x + 1
        pasos += 1
    if pasos > peor:
        peor = pasos
print(f"        hecho: 0 excepciones en {LIMITE_CICLOS-2:,} numeros")
print(f"        (el descenso mas lento tardo {peor} pasos del mapa clasico)")

print(f"\n    (c) exclusion de periodos, aritmetica entera exacta.")
print(f"        periodo k excluido  <=>  2^k * (3X)^S > (3*(3X+1))^S")
print(f"        con S = mayor S con 3^S < 2^k, y X = cota inferior del minimo.")
print(f"\n        {'X (minimo garantizado)':>24} {'mayor periodo k excluido':>26}"
      f" {'cubre 2592?':>12}")

for X in LIMITES_X:
    U, V = 3 * X, 3 * (3 * X + 1)
    potU = potV = 1
    S, pot3, pot2 = 0, 1, 1
    primer_fallo = None
    for k in range(1, K_PERIODO + 1):
        pot2 *= 2
        while pot3 * 3 < pot2:
            pot3 *= 3
            S += 1
            potU *= U
            potV *= V
        if S < 1:
            continue                 # sin pasos impares no hay ciclo posible
        if not (pot2 * potU > potV):
            primer_fallo = k
            break
    mayor = (primer_fallo - 1) if primer_fallo else K_PERIODO
    print(f"        {X:>24,} {mayor:>26,} {str(mayor >= 2592):>12}")

# --- (d) hasta donde llega la exclusion con el limite verificado de HOY -------
#
# La misma desigualdad, pero con X = 2^71 (Barina 2025, el record mundial de
# verificacion por fuerza bruta). Aqui 2^k y 3^S ya no caben en memoria (k llega
# a 10^11), asi que se pasa a logaritmos con decimal a PRECISION DECLARADA, y se
# valida el metodo reproduciendo con el el resultado exacto de (c).
#
# Solo hace falta EVALUAR los jump values: el minimo de k*ln2 - S*ln3 sobre los
# k' <= k se alcanza siempre en un jump value. Pero la FRONTERA no es el ultimo
# jump value que pasa, sino el ULTIMO PERIODO k que pasa, que es "el primer jump
# value que falla" menos uno. El hueco entre los dos se cubre en (e).
#
# ------------------------------------------------------------------------------
# AVISO GRANDE: ESTE BLOQUE ESTUVO MAL, Y LO CAZO UN REVISOR ADVERSARIAL
# ------------------------------------------------------------------------------
# Hasta el 01-08-2026 frontera() devolvia el ULTIMO JUMP VALUE QUE PASA, no el
# ultimo periodo k que pasa. Como los jump values estan espaciados por factores
# de 1,04 / 16,57 / 10,94 justo en esa zona, las tres filas de la tabla salian
# CORTAS por esos mismos factores, y de ahi salio una conclusion falsa: que la
# derivacion elemental "corroboraba" la cifra que citaba el CLAUDE.md, cuando en
# realidad la SUPERA con creces.
#
# Y el control contra (c) NO podia cazarlo: solo comparaba k_falla, que es
# justamente la unica cantidad que los dos metodos calculan igual. Un control
# que compara lo que no esta en discusion no controla nada.
#
# Quien lo cazo fue verificar_frontera_ciclos.py, que es la revision adversarial
# de esta seccion y hay que leerla al lado. Aqui queda arreglado, y ademas el
# hueco entre jump values se COMPRUEBA en (e) en vez de suponerse.
# ------------------------------------------------------------------------------

from decimal import Decimal, getcontext

PRECISION_DECIMAL = 200
TERMINOS_CF = 26
getcontext().prec = PRECISION_DECIMAL

ln2 = Decimal(2).ln()
ln3 = Decimal(3).ln()
log2_3 = ln3 / ln2

x = log2_3
cf_dec = []
for _ in range(TERMINOS_CF):
    a = int(x)
    cf_dec.append(a)
    frac = x - a
    if frac == 0:
        break
    x = 1 / frac
if cf_dec[:len(cf)] != cf:
    fallos.append("[6d] la CF por decimal no coincide con la CF exacta")

p_ant, q_ant = 1, 0
p, q = cf_dec[0], 1
puntos = [(p, q)]
for i in range(1, len(cf_dec)):
    a = cf_dec[i]
    for j in range(1, a + 1):
        puntos.append((p_ant + j * p, q_ant + j * q))
    p_ant, q_ant, p, q = p, q, p_ant + a * p, q_ant + a * q
    puntos.append((p, q))
# los jump values son los que se acercan a 1 por debajo: k/b > log2(3)
jumps = sorted({(kk, bb) for (kk, bb) in puntos
                if bb > 0 and Decimal(kk) > Decimal(bb) * log2_3})
jumps = [(1, 0)] + jumps


def b_de_k(k):
    """Mayor b con 3^b < 2^k, en decimal a la precision declarada."""
    b = int(Decimal(k) / log2_3)
    while (b + 1) * ln3 < k * ln2:
        b += 1
    while b * ln3 >= k * ln2:
        b -= 1
    return b


def frontera(X):
    """Devuelve (k_excluido, b_excluido, k_falla), con k_excluido = k_falla - 1.

    k_excluido es RIGUROSO Y AJUSTADO: todo periodo k <= k_excluido queda
    excluido si el minimo del ciclo esta garantizado >= X. k_falla es el primer
    jump value que ya no se excluye, o sea la longitud minima que le queda
    disponible a un ciclo no trivial.

    El hueco entre el ultimo jump value que pasa y k_falla se cubre en (e).
    """
    paso = (1 + Decimal(1) / (3 * Decimal(X))).ln()
    mejor = None
    for kk, bb in jumps:
        izq = kk * ln2 - bb * ln3
        mejor = izq if mejor is None else min(mejor, izq)
        if not (mejor > bb * paso):
            return kk - 1, b_de_k(kk - 1), kk
    return None, None, None


k_exc, b_exc, k_falla = frontera(10 ** 6)
print(f"\n    (d) el mismo argumento con logaritmos (decimal, precision "
      f"{PRECISION_DECIMAL})")
print(f"        CONTROL contra (c): con X = 1.000.000 el metodo decimal senala")
print(f"        k = {k_falla} como el primer periodo que ya no se excluye, y el")
print(f"        metodo entero exacto de (c) fallo justo en k = 4.701. Es el mismo")
print(f"        numero, o sea que el paso a logaritmos no ha roto nada.")
print(f"        Y la frontera que devuelve, {k_exc:,}, coincide EXACTAMENTE con el")
print(f"        4.700 que da (c) por fuerza bruta entera. Ese es el control que")
print(f"        antes faltaba: hasta el 01-08-2026 esta funcion devolvia 3.647.")
if k_falla != 4701:
    fallos.append(f"[6d] el control decimal da {k_falla}, se esperaba 4701")
if k_exc != 4700:
    fallos.append(f"[6d] la frontera decimal da {k_exc}, se esperaba 4700")

# --- (e) el hueco entre dos jump values consecutivos TAMBIEN esta excluido ----
#
# Sea K_j el ultimo jump value que pasa y K_j1 = k_falla el primero que falla.
# Para todo k con K_j < k < K_j1 hay que ver que sigue excluido. Se parte en dos:
#
#   - k = m*K_j : mientras m*izq(K_j) < ln3 la forma lineal es aditiva, luego
#     izq(k)/b(k) = izq(K_j)/b(K_j), o sea el MISMO margen que K_j, que pasa.
#     Se comprueban uno a uno, no se supone.
#   - cualquier otro k : por el teorema de las tres distancias izq(k) es al menos
#     izq(K_{j-1}), y basta ver que izq(K_{j-1}) supera el umbral MAXIMO de todo
#     el hueco, que es b(K_j1)*paso.
#
# Este es el argumento de verificar_frontera_ciclos.py [C], repetido aqui para
# que esta seccion no dependa de otro fichero.
#
# ES SUFICIENTE, NO NECESARIO, y el control lo enseña: con X = 1.000.000 la
# segunda mitad sale False -- el argumento no alcanza -- y sin embargo la
# frontera 4.700 es correcta, porque ahi (c) recorre TODOS los k con enteros
# exactos. Los dos metodos se cubren: (c) donde 2^k cabe en memoria, (e) donde
# no. Solo cuenta como FALLO que (e) no alcance en un X fuera del alcance de (c).

print(f"\n    (e) el hueco: los MULTIPLOS comprobados, el resto APOYADO en el")
print(f"        teorema de las tres distancias -- que este fichero NO verifica")
print(f"        AVISO (adversario, 01-08-2026): la mitad de (e) es un supuesto,")
print(f"        no una comprobacion, y el titulo decia lo contrario. Peor: en")
print(f"        X = 10^6 y 10^8 se cumple 2*Kj > Kj1, asi que el bucle de")
print(f"        multiplos solo llega a m = 1 -- que es K_j mismo, y ya se sabia")
print(f"        que pasa. Ahi TODO el hueco cuelga de la premisa. Comprobada a")
print(f"        mano en los cuatro huecos que caben en memoria (401-485,")
print(f"        1539-2593, 2593-3647, 3647-4701): se cumple en los cuatro con")
print(f"        holgura ~2x. En 2^62 y 2^71 el hueco mide 10^11 y no es")
print(f"        enumerable. La cota no cambia; cambia su ESTATUS.")
print(f"        {'X':>22} {'ultimo jump que pasa':>22} {'k_falla':>16} "
      f"{'margen mult.':>13} {'resto':>7}")
for nombre, X, cubre_c in [("X = 1.000.000 (control)", 10 ** 6, True),
                           ("Terras 1976, ~10^8", 10 ** 8, False),
                           ("Oliveira e Silva, 2^62", 2 ** 62, False),
                           ("Barina 2025, 2^71", 2 ** 71, False)]:
    paso = (1 + Decimal(1) / (3 * Decimal(X))).ln()
    _, _, kf = frontera(X)
    idx = [i for i, (kk, _) in enumerate(jumps) if kk == kf][0]
    Kj, bj = jumps[idx - 1]
    Kjm1, bjm1 = jumps[idx - 2]
    Kj1, bj1 = jumps[idx]
    umbral_max = bj1 * paso
    margen = None
    m = 1
    while m * Kj < Kj1:
        k2, b2 = m * Kj, m * bj
        iz2 = k2 * ln2 - b2 * ln3
        if iz2 >= ln3:
            fallos.append(f"[6e] la aditividad se rompe en m={m}, X={X}")
        if not (iz2 > b2 * paso):
            fallos.append(f"[6e] el multiplo m={m} NO queda excluido, X={X}")
        r = iz2 / (b2 * paso)
        margen = r if margen is None else min(margen, r)
        m += 1
    resto_ok = (Kjm1 * ln2 - bjm1 * ln3) > umbral_max
    if not resto_ok and not cubre_c:
        fallos.append(f"[6e] el resto del hueco no queda cubierto, X={X}")
    marca = str(resto_ok) + ("*" if (not resto_ok and cubre_c) else "")
    print(f"        {nombre:>22} {Kj:>22,} {Kj1:>16,} {margen:>12.2f}x "
          f"{marca:>7}")
print(f"        fallos: {cuantos('[6e]')}")
print(f"        (*) el argumento del hueco no alcanza ahi, pero ese X lo cubre")
print(f"            (c) recorriendo TODOS los k con enteros exactos. Los dos")
print(f"            metodos se tapan el agujero el uno al otro.")

print()
print(f"        {'limite verificado por fuerza bruta':<36} {'k excluido (riguroso)':>22}"
      f" {'en pasos clasicos':>19}")
for nombre, X in [("Terras 1976, verificado ~10^8", 10 ** 8),
                  ("Oliveira e Silva 2008, 2^62", 2 ** 62),
                  ("Barina 2025, 2^71 (record de hoy)", 2 ** 71)]:
    ke, be, kf = frontera(X)
    print(f"        {nombre:<36} {ke:>22,} {ke + be:>19,}")

ke71, be71, kf71 = frontera(2 ** 71)
bf71 = b_de_k(kf71)
print(f"\n        LA COTA, ESCRITA COMO SE PUBLICA. Todo periodo k <= "
      f"{ke71:,} esta")
print(f"        excluido, luego cualquier ciclo no trivial mide AL MENOS")
print(f"        {kf71:,} pasos del atajo = {kf71 + bf71:,} pasos clasicos")
print(f"        (un ciclo de k pasos de atajo con S impares mide k + S clasicos).")

CITA_BARINA = 217_976_794_617
print(f"\n        CONTRASTE CON LA CIFRA QUE PUBLICA BARINA 2025 (seccion 6) Y")
print(f"        QUE REPITE WIKIPEDIA: {CITA_BARINA:,} pasos del atajo.")
print(f"        Esa cifra es {CITA_BARINA/kf71:.2f} veces la que sale de aqui con")
print(f"        el MISMO X_0 = 2^71. Para alcanzarla haria falta X_0 >= 2^71,884,")
print(f"        y Barina esta en 2075*2^60 = 2^71,019. Es una fila de mas.")
print(f"        Ver verificar_ciclos.py, que lo certifica por tres caminos.")

print(f"\n        LECTURA PARA LA ESTRATEGIA DEL REPO: el barrido de restos de")
print(f"        pinzaciclos.py llega a k = 30 y cuesta 12,5 minutos. Esta")
print(f"        desigualdad, en un segundo y con la verificacion que YA existe,")
print(f"        excluye hasta k = {ke71:,}. El 2.592 del CLAUDE.md")
print(f"        NO es la frontera de hoy: es una foto de 1976. La frontera real")
print(f"        esta {ke71/2592:,.0f} veces mas arriba. La conclusion no cambia")
print(f"        (el barrido sigue muerto), pero el documento subestima por cuanto")
print(f"        lo esta, y ese es exactamente el error que ya mordio dos veces.")

print(f"\n        HONESTIDAD: esto es una re-derivacion INDEPENDIENTE de la")
print(f"        exclusion, no una lectura del articulo. Queda comprobado que la")
print(f"        exclusion de periodo <= 2592 esta al alcance con una verificacion")
print(f"        por fuerza bruta modestisima, y que el argumento cierra. Lo que")
print(f"        NO se puede comprobar desde aqui es que Terras usara ESTE")
print(f"        argumento ni que su numero fuera exactamente 2592.")


# ==============================================================================
# EL CORTE
# ==============================================================================

print("\n" + "=" * 78)
if fallos:
    for f in fallos[:20]:
        print("  FALLO:", f)
    raise SystemExit(f"HAY {len(fallos)} FALLOS. Nada de lo de abajo vale.")
print("TODAS LAS COMPROBACIONES PASAN. 0 fallos.")
print("=" * 78)

print("""
RESUMEN, separando COTA de PROMEDIO:

  [1] T1.1 forma cerrada      CONSTRUCCION (identidad algebraica exacta).
                              Sirve para la formula: es el motor de todo.
  [2] T1.1 == forma del repo  CONSTRUCCION. Son la misma identidad, con
                              C = 2^k * rho_k. Verificado, no supuesto.
  [3] T1.2 solo el resto      CONSTRUCCION + criterio FINITO sobre INFINITOS
                              numeros. Es literalmente el cuarto camino.
  [4] C1.4 paridades 50/50    BIYECCION exacta (construccion). Su lectura
                              probabilistica es un PROMEDIO y no decide ningun
                              numero concreto. Las dos cosas a la vez, y por eso
                              la red neuronal de redhilos.py no puede ganar.
  [5] Tabla C                 CONSTRUCCION aritmetica. Dice DONDE mirar; por si
                              sola no excluye nada.
  [6] periodo excluido        COTA de verdad: un "no existe ningun ciclo con".
                              Es lo unico del bloque con forma de teorema util.
""")
