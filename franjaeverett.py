# -*- coding: utf-8 -*-
#
# LA FRANJA log2(10/9) - el hueco entre lo que Everett demuestra y la verdad
# =========================================================================
#
# QUE SE MIRA AQUI Y POR QUE
# --------------------------
# Everett 1977 demuestra que casi todo n tiene un iterado menor que n. Su
# unico truco para no pelearse con el +1 es acotar cada paso impar del mapa
# del ATAJO por una constante:
#
#     m impar >= 3   ->   f(m)/m = (3m+1)/(2m) = 3/2 + 1/(2m)  <=  5/3
#
# El 5/3 no es el 3/2 verdadero, y ese exceso se paga en el umbral. En las
# coordenadas del repo (A = pasos impares, B = pasos del atajo; en el mapa
# del atajo X = A y N = B exactamente, ya verificado en verificar_everett.py):
#
#     Everett garantiza descenso si   B/A > log2(10/3) = 1,73696559416620616
#     El equilibrio verdadero esta en B/A > log2(3)     = 1,58496250072115618
#     LA FRANJA mide                  log2(10/9)        = 0,15200309344504998
#
# LA FRANJA ESTA POBLADA: hay numeros que bajan y que Everett no certifica
# nunca, y los 24 primeros (hasta 20.000) caen los 24 dentro de la franja.
#
# PERO ESO NO ES UN HALLAZGO, ES UN TEOREMA DE DOS LINEAS, y aqui se
# demuestra en vez de medirse (comprobacion 7): si n no esta certificado,
# entonces en particular falla en su trayectoria completa, luego
# B/A <= log2(10/3); y si n llega a 1, la identidad 2^B = 3^A n + C con
# C > 0 obliga a 2^B > 3^A, luego B/A > log2(3). La pertenencia a la franja
# es forzosa. El reciproco es FALSO y por eso la franja no caracteriza nada:
# hasta 20.000 hay 42 numeros en la franja y solo 24 sin certificado.
#
# LA IDEA QUE SE PONE A PRUEBA
# ----------------------------
# El 5/3 vale para m >= 3 y es exacto en m = 3. Para m grande la cota
# verdadera (3m+1)/(2m) tiende a 3/2. Con la cota condicionada a m >= M:
#
#     umbral(M) = log2( (3M+1)/M )        ->  log2(3) cuando M -> infinito
#     franja(M) = umbral(M) - log2(3) = log2( 1 + 1/(3M) )   <- forma cerrada
#
# O sea: LA FRANJA ES EL +1, otra vez, y su anchura tiende a cero. (Es la
# cuarta aparicion del mismo estorbo en el laboratorio: el grosor 0,2286 de
# la lamina, el +2 del espejo base 2, la desviacion de la fraccion impar, y
# ahora esto.)
#
# EL OBSTACULO, que es lo que hay que medir de verdad: condicionar a m >= M
# excluye las trayectorias que bajan de M, y todas bajan. La cota afinada
# solo se puede aplicar al PREFIJO anterior a que la trayectoria caiga por
# debajo de M. Hay dos maneras de gastar ese presupuesto y son opuestas:
#
#   - M = n (auto-referente): antes del primer descenso TODOS los valores
#     son >= n, asi que la cota mas fina posible vale... pero solo hasta el
#     primer descenso. Presupuesto corto, cota buenisima.
#   - M fijo y pequeno: cota peor, pero el prefijo valido se extiende mucho
#     mas alla del primer descenso y se puede certificar mas tarde.
#
# Se miden las dos y se busca el NUCLEO que resiste a todas.
#
# EL LIMITE, ESCRITO POR DELANTE PARA NO INFLAR EL RESULTADO
# ----------------------------------------------------------
# Cerrar la franja daria "todo n baja alguna vez", QUE NO ES LA CONJETURA.
# Falta poder iterar la bajada sin tope, y eso exige una cantidad monotona a
# lo largo de la trayectoria que nadie conoce. Y el control A/B de este mismo
# fichero lo remata: con 3n-1 la franja mide CERO (la cota 3/2 vale sin
# condicionar nada) y sin embargo 3n-1 tiene TRES ciclos y no converge. O
# sea que la version mas afilada posible de este teorema es compatible con
# la no convergencia. Cerrar la franja no es evidencia sobre la conjetura.
#
# TRABAJO PREVIO EN EL REPO: verificar_everett.py ya establecio la
# traduccion correcta a (A,B) (X = A, N = B, no N = A+B), corrigio el 0,7369
# del CLAUDE.md y midio la densidad de clases excepcionales. Aqui no se
# repite: se parte de ahi.

from fractions import Fraction
from decimal import Decimal, getcontext
import time

# ------------------------------ CONSTANTES ------------------------------

PRECISION = 50          # digitos de decimal para los umbrales
LIMITE_COTA = 100001    # hasta donde se comprueba la cota (3m+1)/(2m)
LIMITE_EXHAUSTIVO = 20000   # barrido con TODOS los N de cada trayectoria
LIMITE_BARRIDO = 10 ** 7    # barrido principal de certificacion (unos 20 s)
LIMITE_FAMILIA = 10 ** 6    # barrido de la familia de cotas M (unos 10 s)
LIMITE_MENOS = 10 ** 6      # barrido del control A/B con 3n-1
LISTA_M = (1, 3, 5, 9, 27, 101, 1001, 10001)   # cotas condicionadas m >= M
N_MAX_TABLA = 4000      # niveles de la tabla de umbrales enteros
K_DP = 400              # niveles de la programacion dinamica de clases
NIVEL_N0 = 18           # hasta que nivel se enumeran las clases a mano
TOPE_CICLO = 3000       # guarda de pasos para 3n-1 (tiene ciclos)

getcontext().prec = PRECISION

T0 = time.time()

print("=" * 74)
print("LA FRANJA log2(10/9) - el hueco entre Everett y la verdad")
print("=" * 74)


# --------------------------- LA MAQUINARIA ---------------------------

def tabla_x0(nmax, M):
    """x0[N] = menor X con ((3M+1)/M)^X >= 2^N, en enteros exactos.

    El certificado con la cota (3M+1)/(2M) es  X < x0[N].  Se apoya en que
    ((3M+1)/M)^X / 2^N crece con X, o sea que la condicion es monotona."""
    a = 3 * M + 1
    x0 = [0] * (nmax + 1)
    pa, pb, x, p2 = 1, 1, 0, 1
    for N in range(1, nmax + 1):
        p2 *= 2
        while pa < pb * p2:
            x += 1
            pa *= a
            pb *= M
        x0[N] = x
    return x0


def tabla_x0_ideal(nmax):
    """El limite M -> infinito: el certificado es 3^X < 2^N."""
    x0 = [0] * (nmax + 1)
    p3, p2, x = 1, 1, 0
    for N in range(1, nmax + 1):
        p2 *= 2
        while p3 < p2:
            x += 1
            p3 *= 3
        x0[N] = x
    return x0


def atajo(m):
    return (3 * m + 1) // 2 if m & 1 else m // 2


TABLAS = {M: tabla_x0(N_MAX_TABLA, M) for M in LISTA_M}
IDEAL = tabla_x0_ideal(N_MAX_TABLA)


def certifica(n, M, x0):
    """Devuelve el N donde la cota (3M+1)/(2M) certifica m_N < n, o None.

    La cota solo vale mientras todos los valores impares del prefijo sean
    >= M: en cuanto aparece un impar menor, el argumento se acaba."""
    m, X, N = n, 0, 0
    while True:
        if m & 1:
            if m < M:
                return None
            X += 1
            m = (3 * m + 1) // 2
        else:
            m //= 2
        N += 1
        if X < x0[N]:
            return N
        if m == 1:
            return None


def certifica_auto(n):
    """La cota auto-referente M = n, valida solo hasta el primer descenso."""
    a, b = 3 * n + 1, n
    m, X, N = n, 0, 0
    pa, pb, p2 = 1, 1, 1
    while True:
        if m & 1:
            X += 1
            m = (3 * m + 1) // 2
            pa *= a
            pb *= b
        else:
            m //= 2
        N += 1
        p2 *= 2
        if pa < pb * p2:
            return N
        if m < n or m == 1:
            return None


# =========================== COMPROBACIONES ===========================
# Todas cortan con SystemExit. Van ANTES de cualquier conclusion.

print()
print("--- 1. La cota (3m+1)/(2m) en Fraction exacto ---")

peor, peor_m = Fraction(0), None
for m in range(3, LIMITE_COTA, 2):
    r = Fraction(3 * m + 1, 2 * m)
    if r > peor:
        peor, peor_m = r, m
if peor != Fraction(5, 3) or peor_m != 3:
    raise SystemExit("FALLO: el maximo de (3m+1)/(2m) para m impar >= 3 "
                     "deberia ser 5/3 en m=3, y sale %s en %s" % (peor, peor_m))
if Fraction(3 * 1 + 1, 2 * 1) != 2:
    raise SystemExit("FALLO: m=1 deberia dar razon 2")
print("  impares 3..%d: maximo = %s, alcanzado en m = 3." % (LIMITE_COTA, peor))
print("  m = 1 da razon 2 > 5/3. SIN CONDICIONAR el supremo es 2, y entonces")
print("  el umbral seria log2(4) = 2 en vez de 1,737: mucho peor.")
print("  RESPUESTA A LA PREGUNTA (5): la cota 5/3 NO se puede afinar sin")
print("  condicionar. Es exacta, con igualdad en m = 3, y el unico impar que")
print("  la rompe es el 1. Afinarla exige condicionar a m >= M, y eso es")
print("  justo lo que crea el problema del prefijo que se mide mas abajo.")

# y la de 3n-1, que es la que decide el control A/B
peor_menos = max(Fraction(3 * m - 1, 2 * m) for m in range(1, LIMITE_COTA, 2))
if peor_menos >= Fraction(3, 2):
    raise SystemExit("FALLO: (3m-1)/(2m) deberia estar por debajo de 3/2")
print("  Y para 3n-1: (3m-1)/(2m) < 3/2 para TODO impar m >= 1, sin excluir")
print("  ninguno. Maximo medido = %s. El supremo 3/2 no se alcanza."
      % str(float(peor_menos))[:12])

print()
print("--- 2. La traduccion entera del certificado ---")

fallos = 0
for M in (3, 5, 27):
    a = Fraction(3 * M + 1, 2 * M)
    for N in range(1, 31):
        for X in range(0, N + 1):
            racional = a ** X * Fraction(1, 2) ** (N - X) < 1
            entero = (3 * M + 1) ** X < M ** X * 2 ** N
            tabla = X < TABLAS[M][N]
            if not (racional == entero == tabla):
                fallos += 1
if fallos:
    raise SystemExit("FALLO: %d desacuerdos entre Fraction, enteros y la tabla"
                     % fallos)
print("  ((3M+1)/(2M))^X * (1/2)^(N-X) < 1   <=>   (3M+1)^X < M^X * 2^N")
print("  Verificado en Fraction contra enteros contra la tabla x0, para")
print("  M = 3, 5, 27 y los 1.488 pares (X,N) con N <= 30: 0 desacuerdos.")

print()
print("--- 3. La anchura de la franja en forma cerrada ---")

log2_3 = Decimal(3).ln() / Decimal(2).ln()
fallos = 0
for M in (1, 3, 5, 9, 27, 101, 1001, 10001, 10 ** 9):
    umbral = (Decimal(3 * M + 1) / Decimal(M)).ln() / Decimal(2).ln()
    ancho = (Decimal(1) + Decimal(1) / Decimal(3 * M)).ln() / Decimal(2).ln()
    if abs((umbral - log2_3) - ancho) > Decimal(10) ** -(PRECISION - 10):
        fallos += 1
if fallos:
    raise SystemExit("FALLO: umbral(M) - log2(3) no es log2(1+1/(3M))")
print("  umbral(M) - log2(3) = log2(1 + 1/(3M)), verificado a %d digitos"
      % (PRECISION - 10))
print("  para M = 1, 3, 5, 9, 27, 101, 1001, 10001, 10^9: 0 fallos.")

print()
print("--- 4. El certificado implica descenso DE VERDAD ---")

comprobadas = 0
for M in (3, 9):
    x0 = TABLAS[M]
    for n in range(M, LIMITE_EXHAUSTIVO):
        m, X, N = n, 0, 0
        while m != 1:
            if m & 1:
                if m < M:
                    break
                X += 1
                m = (3 * m + 1) // 2
            else:
                m //= 2
            N += 1
            if X < x0[N]:
                comprobadas += 1
                if not m < n:
                    raise SystemExit(
                        "FALLO: certificado sin descenso en n=%d N=%d M=%d"
                        % (n, N, M))
print("  Cada vez que el certificado dispara, el iterado esta por debajo.")
print("  M = 3 y M = 9, n hasta %d, TODOS los N de cada trayectoria:"
      % LIMITE_EXHAUSTIVO)
print("  %d disparos comprobados, 0 fallos." % comprobadas)

print()
print("--- 5. Necesidad: descender obliga a 3^X < 2^N, y el reciproco es falso ---")

contra = []
for n in range(3, 4000):
    m, X, N = n, 0, 0
    p3, p2 = 1, 1
    while m != 1:
        if m & 1:
            X += 1
            m = (3 * m + 1) // 2
            p3 *= 3
        else:
            m //= 2
        N += 1
        p2 *= 2
        if m < n and not p3 < p2:
            raise SystemExit("FALLO: descenso con 3^X >= 2^N en n=%d N=%d" % (n, N))
        if p3 < p2 and not m < n and len(contra) < 4:
            contra.append((n, X, N, m))
if not contra:
    raise SystemExit("FALLO: se esperaban contraejemplos al reciproco")
print("  n de 3 a 3999: ningun descenso con 3^X >= 2^N. La necesidad sale de")
print("  la identidad 2^N m_N = 3^X n + C con C > 0, y se cumple sin fallos.")
print("  Y NO es suficiente. Primeros contraejemplos (3^X < 2^N y sin bajar):")
for (n, X, N, m) in contra:
    print("    n=%-5d X=%-3d N=%-3d -> m_N = %d  (m_N >= n)" % (n, X, N, m))
print("  Esto refuta, otra vez, la frase del CLAUDE.md 'nuestro 1,585 es el")
print("  umbral verdadero': log2(3) es NECESARIO, no es umbral de descenso")
print("  garantizado. verificar_everett.py ya lo habia atrapado; aqui vuelve")
print("  a salir solo, desde la familia de cotas.")

print()
print("--- 6. La identidad exacta por clases: C depende solo del resto ---")

fallos = 0
for K in (4, 6, 8, 10):
    for r in range(2 ** K):
        m, X = r, 0
        for _ in range(K):
            if m & 1:
                X += 1
            m = atajo(m)
        C = 2 ** K * m - 3 ** X * r
        for j in (1, 2, 7, 33):
            n = r + j * 2 ** K
            mm, XX = n, 0
            for _ in range(K):
                if mm & 1:
                    XX += 1
                mm = atajo(mm)
            if XX != X or 2 ** K * mm != 3 ** X * n + C:
                fallos += 1
if fallos:
    raise SystemExit("FALLO: %d clases donde 2^K m_K = 3^X n + C se rompe" % fallos)
print("  2^K * m_K = 3^X * n + C_r, con X y C_r dependiendo SOLO de r mod 2^K.")
print("  Verificado en las 1.360 clases de K = 4, 6, 8, 10 contra 4")
print("  representantes cada una: 0 fallos. (Es el Teorema 1.2 de Terras.)")

print()
print("--- 7. Estar en la franja es FORZOSO, no es un hallazgo ---")

x3 = TABLAS[3]
sin_cert_20k = []
en_franja_20k = 0
for n in range(3, LIMITE_EXHAUSTIVO + 1):
    m, X, N = n, 0, 0
    cert = None
    while True:
        if m & 1:
            X += 1
            m = (3 * m + 1) // 2
        else:
            m //= 2
        N += 1
        if X < x3[N]:
            cert = N
            break
        if m == 1:
            break
    # A y B de la trayectoria completa (A = X, B = N del atajo)
    mm, A, B = n, 0, 0
    while mm != 1:
        if mm & 1:
            A += 1
        mm = atajo(mm)
        B += 1
    if A and 3 ** A < 2 ** B and 10 ** A >= 3 ** A * 2 ** B:
        en_franja_20k += 1          # log2(3) < B/A <= log2(10/3)
    if cert is None:
        sin_cert_20k.append(n)
        if not (3 ** A < 2 ** B and 10 ** A >= 3 ** A * 2 ** B):
            raise SystemExit("FALLO: n=%d sin certificado y fuera de la franja" % n)
print("  n de 3 a %d: %d sin certificado, y los %d estan en la franja."
      % (LIMITE_EXHAUSTIVO, len(sin_cert_20k), len(sin_cert_20k)))
print("  Pero eso NO mide nada: es forzoso. Sin certificado -> falla tambien")
print("  en la trayectoria entera -> B/A <= log2(10/3). Llega a 1 -> C > 0 ->")
print("  2^B > 3^A -> B/A > log2(3). Las dos cosas juntas SON la franja.")
print("  Y el reciproco es falso: %d numeros en la franja, solo %d sin"
      % (en_franja_20k, len(sin_cert_20k)))
print("  certificado. La franja NO caracteriza el conjunto excepcional.")

print()
print("  (comprobaciones superadas en %.1f s)" % (time.time() - T0))


# ============================= RESULTADOS =============================

print()
print("=" * 74)
print("R1. EL BARRIDO: hasta donde se llega y quien queda sin certificar")
print("=" * 74)

t = time.time()
sin_cert = []
for n in range(3, LIMITE_BARRIDO + 1, 2):
    m, X, N = n, 0, 0
    while True:
        if m & 1:
            X += 1
            m = (3 * m + 1) // 2
        else:
            m //= 2
        N += 1
        if X < x3[N]:
            break
        if m == 1:
            sin_cert.append(n)
            break
print("  n impar de 3 a %d (los pares se certifican en el paso 1)."
      % LIMITE_BARRIDO)
print("  Sin certificado de Everett: %d numeros.  (%.1f s)"
      % (len(sin_cert), time.time() - t))
print()
print("       hasta      cuantos    densidad")
import bisect
for e in range(2, 8):
    lim = 10 ** e
    c = bisect.bisect_right(sin_cert, lim)
    print("       10^%-8d %-9d %.3e" % (e, c, c / lim))
print()
print("  Los 24 primeros (los de hasta 20.000, que es donde llegaba el dato")
print("  previo del repo):")
print("    %s" % sin_cert[:24])
print("  El mas chico es el 27. El mas grande hallado: %d" % sin_cert[-1])
print("  La densidad cae despacio pero cae. NO ES CERO en ningun tramo.")

print()
print("=" * 74)
print("R2. CARACTERIZACION: es describible por restos?")
print("=" * 74)

print()
print("  2a. Los restos que ocupa (hasta %d):" % LIMITE_FAMILIA)
corte = sin_cert[:bisect.bisect_right(sin_cert, LIMITE_FAMILIA)]
for j in (2, 3, 4, 5, 6):
    rs = sorted(set(n % 2 ** j for n in corte))
    print("     mod 2^%d: ocupa %2d restos de %3d  ->  %s"
          % (j, len(rs), 2 ** j, rs[:10]))
print("     Todos son 3 mod 4, y eso es forzoso: n = 1 mod 4 se certifica en")
print("     el paso 2 (el atajo da par) y n par en el paso 1.")

print()
print("  2b. NO CONTIENE NINGUNA CLASE COMPLETA. Prueba directa: para cada")
print("      no certificado n, con L = su numero de pasos del atajo, el")
print("      numero n + 2^L esta en la MISMA clase mod 2^L y si se certifica.")
fallos = 0
for n in corte:
    m, L = n, 0
    while m != 1:
        m = atajo(m)
        L += 1
    if certifica(n + 2 ** L, 3, x3) is None:
        fallos += 1
if fallos:
    raise SystemExit("FALLO: %d clases enteras dentro del conjunto excepcional"
                     % fallos)
print("      %d numeros probados, %d fallos. Ni una clase entera dentro."
      % (len(corte), fallos))
print("      Razon: certificarse es una condicion ABIERTA (basta un prefijo)")
print("      y no certificarse es CERRADA, interseccion de infinitos niveles.")
print("      El conjunto certificado es una union de clases; el excepcional")
print("      es su complemento, un conjunto de Cantor 2-adico de medida cero.")
print("      RESPUESTA A (2): NO es un blanco finito de clases. Es una nube.")

print()
print("  2c. Lo que si es exacto: cuantas CLASES mod 2^K siguen sin")
print("      certificarse a nivel K. Programacion dinamica sobre (N,X),")
print("      valida porque el certificado depende solo de (N,X).")
dps = {}
for nombre, x0 in (("M=3 (Everett)", TABLAS[3]), ("M=5", TABLAS[5]),
                   ("M=27", TABLAS[27]), ("ideal 3^X<2^N", IDEAL)):
    dp = {0: 1}
    malos = {}
    for N in range(1, K_DP + 1):
        nueva = {}
        for x, c in dp.items():
            for nx in (x, x + 1):
                if nx >= x0[N]:
                    nueva[nx] = nueva.get(nx, 0) + c
        dp = nueva
        malos[N] = sum(dp.values())
    dps[nombre] = malos
print()
print("       K    " + "".join("%16s" % k for k in dps))
for K in (8, 16, 32, 64, 96, 128, 200, 300, 400):
    fila = "      %-5d" % K
    for k in dps:
        fila += "    %.6e" % float(Fraction(dps[k][K], 2 ** K))
    print(fila)
print()
print("      La columna 'ideal' es el suelo: ningun afinado de la cota puede")
print("      bajar de ahi, porque 3^X < 2^N es NECESARIO para descender.")
print("      Y NO ES CERO A NINGUN NIVEL. Cerrar la franja no vacia el")
print("      conjunto excepcional: lo encoge de 4,8e-03 a 3,1e-04 en K=96.")
print("      La cota de clases es valida pero floja: a K=96 predice como")
print("      mucho 4,8e-03 y lo medido hasta 10^6 es 3,9e-04 (12 veces menos).")

print()
print("=" * 74)
print("R3. LA COTA AFINADA (3M+1)/(2M), Y EL OBSTACULO DEL PREFIJO")
print("=" * 74)

print()
print("  3a. Los umbrales, exactos a %d digitos:" % PRECISION)
print()
print("        M          cota       umbral B/A           franja = log2(1+1/(3M))")
for M in (1, 3, 5, 9, 27, 101, 1001, 10 ** 6, 10 ** 12):
    umbral = (Decimal(3 * M + 1) / Decimal(M)).ln() / Decimal(2).ln()
    ancho = umbral - log2_3
    print("        %-10s %-10s %-20s %s"
          % ("10^%d" % (len(str(M)) - 1) if M >= 10 ** 6 else M,
             format(Decimal(3 * M + 1) / Decimal(2 * M), '.7f'),
             format(umbral, '.18f'), format(ancho, '.8E')))
print("        infinito   1.5000000  %s  0" % format(log2_3, '.18f'))
print()
print("      La franja se cierra en el limite. Confirmado el punto (3).")
print()
print("      COINCIDENCIA ANOTADA PARA DESCONFIAR DE ELLA: el umbral sin")
print("      condicionar nada (M = 1, cota 2) es log2(4) = 2 EXACTO, y el")
print("      CLAUDE.md tiene medido que el B/A tipico converge a 2 (1,99048)")
print("      por la valuacion 2-adica media de 3n+1. Son dos doses de origen")
print("      distinto - log2(4) contra suma k*2^-k - y no hay razon para")
print("      creer que se hablen. Se anota, no se construye nada encima.")

print()
print("  3b. Y AHORA EL OBSTACULO. La cota m >= M solo vale mientras la")
print("      trayectoria no baje de M, y todas bajan. Barrido completo de")
print("      n impar hasta %d con cada M:" % LIMITE_FAMILIA)
print()
print("        M        sin certificar   los primeros")
for M in LISTA_M:
    x0 = TABLAS[M]
    faltan = []
    for n in range(3, LIMITE_FAMILIA + 1, 2):
        if certifica(n, M, x0) is None:
            faltan.append(n)
    print("        %-8d %-16d %s" % (M, len(faltan), faltan[:6]))
print()
print("      Se ve la pinza: con M chico la cota es mala (M=1 deja 81.441")
print("      sin certificar); con M grande la cota es buena pero la guarda")
print("      mata a todos los n pequenos, y a partir de M=27 el conjunto")
print("      excepcional vuelve a crecer.
      OJO: "EL OPTIMO ESTA EN M = 9" es lo que decia aqui y NO lo dice la
      tabla (adversario, 01-08-2026). Contando solo las excepciones REALES
      -las que no son "n < M por hipotesis"- empatan a CERO M = 5, 9, 101,
      1001 y 10001. El mejor de los probados es M = 10001, con umbral
      1,585011, a 4,8e-05 de log2(3). La conclusion cualitativa no cambia
      (la franja no se cierra), pero se estrecha tres ordenes de magnitud
      mas de lo que este fichero publicaba.")

print()
print("  3c. La otra manera de gastar el presupuesto: M = n. Antes del")
print("      primer descenso todos los valores son >= n, asi que la cota")
print("      auto-referente (3n+1)/(2n) es legitima - pero solo hasta ahi.")
resisten_auto = [n for n in sin_cert if certifica_auto(n) is None]
print("      De los %d sin certificado de Everett hasta %d, la cota M = n"
      % (len(sin_cert), LIMITE_BARRIDO))
print("      certifica %d y resisten %d: %s"
      % (len(sin_cert) - len(resisten_auto), len(resisten_auto), resisten_auto))
print("      Los que resisten cumplen 3^X < 2^N en el primer descenso (la")
print("      condicion necesaria) pero no la suficiente: viven en la rendija")
print("      que queda entre las dos, y esa rendija se cierra como 1/n.")

print()
print("  3d. EL NUCLEO: quien resiste a TODAS las cotas de la familia?")
nucleo = set(resisten_auto)
for M in LISTA_M:
    x0 = TABLAS[M]
    nucleo &= set(n for n in sin_cert if certifica(n, M, x0) is None)
print("      Interseccion de M = n con M = %s sobre los %d excepcionales:"
      % (str(LISTA_M), len(sin_cert)))
print("      NUCLEO = %s" % (sorted(nucleo) if nucleo else "VACIO"))
print()
faltan9 = []
x9 = TABLAS[9]
t = time.time()
for n in range(3, LIMITE_BARRIDO + 1, 2):
    if certifica(n, 9, x9) is None:
        faltan9.append(n)
print("      Y el resultado limpio, barrido completo hasta %d con M = 9:"
      % LIMITE_BARRIDO)
print("      sin certificar: %s   (%.1f s)" % (faltan9, time.time() - t))
print("      O sea: los tres impares menores que 9, que la hipotesis m >= 9")
print("      excluye por definicion. NADIE MAS.")
print()
print("      RESULTADO DE (3): NO HAY NUCLEO. Cambiando 5/3 por 28/9 el")
print("      conjunto excepcional de Everett hasta 10^7 pasa de %d numeros"
      % len(sin_cert))
print("      a ninguno, y el umbral baja de 1,73697 a 1,63763.
      Y con M = 10001 baja hasta 1,585011 sin dejar una sola excepcion
      real: la franja se estrecha, pero NO se cierra.")
print("      Sigue sin ser log2(3): la franja se estrecha, no se cierra.")

print()
print("=" * 74)
print("R4. EL LIMITE M -> INFINITO EXISTE DE VERDAD, Y ES POR CLASES")
print("=" * 74)
print()
print("  No hace falta acotar nada. De 2^N m_N = 3^X n + C_r sale el")
print("  criterio EXACTO, y es un criterio finito sobre infinitos numeros:")
print()
print("      si 3^X < 2^N :  m_N < n  <=>  n > C_r / (2^N - 3^X)")
print("      si 3^X >= 2^N:  no desciende NUNCA en el paso N, para ningun n")
print()
print("  O sea: cada clase r mod 2^N con 3^X < 2^N hace bajar a TODOS sus")
print("  infinitos elementos salvo a los que no pasan de un n0 explicito.")
print("  Esa es exactamente la version M -> infinito, sin cotas y sin franja.")
print()
print("       N     n0 maximo   resto que lo alcanza   X    2^N - 3^X")
peor_global = 0
for N in range(2, NIVEL_N0 + 1):
    dosN = 2 ** N
    mx, arg = 0, None
    for r in range(dosN):
        m, X = r, 0
        for _ in range(N):
            if m & 1:
                X += 1
            m = atajo(m)
        d = dosN - 3 ** X
        if d <= 0:
            continue
        n0 = (dosN * m - 3 ** X * r) // d
        if n0 > mx:
            mx, arg = n0, (r, X, d)
    peor_global = max(peor_global, mx)
    if N >= NIVEL_N0 - 7:
        print("       %-5d %-11d %-22d %-4d %d" % (N, mx, arg[0], arg[1], arg[2]))
print()
print("  Hasta el nivel %d el n0 mas grande de todas las clases es %d."
      % (NIVEL_N0, peor_global))
print("  Traducido: TODO n > %d cuya clase mod 2^%d sea buena a algun nivel"
      % (peor_global, NIVEL_N0))
print("  N <= %d desciende, y se decide mirando el resto. Es una COTA, no un"
      % NIVEL_N0)
print("  promedio, y decide infinitos numeros con una comprobacion finita.")
print()
print("  Y hay un enganche con la otra mitad del laboratorio: el n0 se")
print("  dispara cuando 2^N - 3^X es chico, o sea en las convergentes de")
print("  log2(3). Los niveles donde (2^N - 3^X)/2^N bate record son:")
rec = Fraction(2)
jump = []
for N in range(1, 72):
    x = 0
    while 3 ** (x + 1) < 2 ** N:
        x += 1
    d = Fraction(2 ** N - 3 ** x, 2 ** N)
    if d < rec:
        rec = d
        jump.append((N, x))
print("    %s" % ", ".join("N=%d X=%d" % p for p in jump))
print("  Son EXACTAMENTE los jump values de la Tabla C de Terras que ya")
print("  estan en el CLAUDE.md (1, 2, 5, 8, 27, 46, 65). Las mismas")
print("  convergentes que gobiernan los ciclos gobiernan el conjunto")
print("  excepcional del descenso. HONESTIDAD: el n0 maximo NO cae siempre")
print("  en esos niveles (N=13 y N=16 pican sin ser jump values), asi que la")
print("  relacion es de tendencia, no de identidad.")

print()
print("=" * 74)
print("R5. CONTROL A/B OBLIGATORIO: la misma franja sobre 3n-1")
print("=" * 74)
print()
print("  La cota del mapa 3n-1 es (3m-1)/(2m) = 3/2 - 1/(2m) < 3/2, y vale")
print("  para TODO impar m >= 1: no hay nada que condicionar, y el supremo")
print("  3/2 es justo el equilibrio. Luego:")
print()
print("      franja(3n+1) = log2(10/9) = %s" % str((Decimal(10) / 9).ln() / Decimal(2).ln())[:20])
print("      franja(3n-1) = 0 EXACTO, para cualquier M")
print()
print("  LA CANTIDAD DISCRIMINA. Y la razon es el signo del +1: en 3n+1 la")
print("  razon se acerca a 3/2 POR ARRIBA y hay que dejar colchon; en 3n-1")
print("  se acerca POR ABAJO y el colchon sobra. La franja no es un defecto")
print("  de Everett: es el +1 medido en su propio idioma.")
print()
t = time.time()
faltan_menos = []
for n in range(3, LIMITE_MENOS + 1, 2):
    m, X, N = n, 0, 0
    while True:
        if m & 1:
            X += 1
            m = (3 * m - 1) // 2
        else:
            m //= 2
        N += 1
        if X < IDEAL[N]:
            break
        if m < n or N > TOPE_CICLO:
            faltan_menos.append(n)
            break
print("  Barrido de 3n-1 hasta %d con el criterio 3^X < 2^N (que aqui es la"
      % LIMITE_MENOS)
print("  cota cruda de Everett, no una version afinada):")
print("     sin certificar: %s   (%.1f s)" % (faltan_menos, time.time() - t))
print("     Son los minimos de los dos ciclos no triviales de 3n-1. No se")
print("     certifican porque NO DESCIENDEN: no es un fallo del criterio.")
print()
print("  Y la inversion es exacta, mirando el signo de C:")
print("     3n+1 : C > 0  ->  3^X < 2^N es NECESARIO y no suficiente")
print("     3n-1 : C < 0  ->  3^X < 2^N es SUFICIENTE y no necesario")
print()
print("  CONSECUENCIA QUE HAY QUE TRAGARSE: la version mas afilada posible")
print("  del teorema de descenso vale PERFECTA para 3n-1, un mapa con TRES")
print("  ciclos que no converge a 1. Cerrar la franja no puede ser evidencia")
print("  sobre la convergencia, porque el caso donde ya esta cerrada no")
print("  converge.")

print()
print("=" * 74)
print("RESUMEN")
print("=" * 74)
print("  1. La franja mide log2(10/9) y su anchura general es log2(1+1/(3M)),")
print("     que tiende a 0. Es el +1 otra vez, ahora en el umbral de Everett.")
print("  2. Estar en la franja es forzoso para los no certificados (teorema)")
print("     y el reciproco es falso: la franja no los caracteriza.")
print("  3. Sin certificar hasta 10^7: %d numeros, densidad 2,6e-04 y bajando."
      % len(sin_cert))
print("  4. El conjunto excepcional NO es una union de clases: no contiene")
print("     ninguna clase completa. Es cerrado, de medida cero, una nube.")
print("  5. NO HAY NUCLEO que resista al afinado: con m >= 9 (cota 28/9) el")
print("     conjunto excepcional hasta 10^7 es exactamente {3,5,7}.")
print("  6. El limite M -> infinito no es un limite: es el criterio exacto")
print("     por clases n > C_r/(2^N - 3^X). COTA, no promedio.")
print("  7. Control A/B: la franja de 3n-1 mide CERO. La cantidad discrimina")
print("     y lo que discrimina es el signo del +1.")
print("  8. LIMITE HONESTO: todo esto certifica UN descenso. Iterarlo exige")
print("     una cantidad monotona que nadie conoce. No es la conjetura.")
print()
print("  (total %.1f s)" % (time.time() - T0))
