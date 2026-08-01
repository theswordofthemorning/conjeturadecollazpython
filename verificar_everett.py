# -*- coding: utf-8 -*-
#
# VERIFICAR EVERETT 1977 - "casi todo n tiene un iterado menor que n"
# =====================================================================
#
# De quien es el teorema:
#   C. J. Everett, "Iteration of the number-theoretic function
#   f(2n) = n, f(2n+1) = 3n+2", Advances in Mathematics 25 (1977) 42-45.
#
# OJO CON EL MAPA. La f de Everett NO es la regla clasica. Es el mapa del
# ATAJO: para m impar, f(m) = f(2n+1) = 3n+2 = (3m+1)/2, o sea que el
# 3n+1 y la division que viene detras cuentan como UN SOLO paso. Para m
# par, f(m) = m/2. Esto es exactamente el "mapa del atajo" del repo.
#
# Lo que Everett usa, y es su unico truco para no pelearse con el +1:
#
#     m impar >= 3  ->  f(m)/m = (3m+1)/(2m) = 3/2 + 1/(2m) <= 5/3
#     m par         ->  f(m)/m = 1/2
#
# Con eso, si en los primeros N pasos hubo X impares:
#
#     m_N <= (5/3)^X * (1/2)^(N-X) * m_0
#
# y el lado derecho es < m_0 cuando X*log(10/3) < N*log 2, o sea
#
#     X/N < L = log 2 / log(10/3) = 0,5757...
#
# QUE SE COMPRUEBA AQUI (y en este orden, cortando con SystemExit):
#
#   1. La cota 5/3 es exacta y donde falla exactamente si m < 3.
#   2. La constante L, y su inversa en forma cerrada.
#   3. LA TRADUCCION A LAS COORDENADAS (A,B) DEL REPO. Esta es la parte
#      donde el CLAUDE.md se equivoca, y por eso va con contraejemplo.
#   4. La desigualdad de Everett en forma ENTERA sobre trayectorias reales.
#   5. Que la condicion correcta garantiza el descenso.
#   6. Que la condicion del CLAUDE.md NO lo garantiza (contraejemplos).
#   7. Que el umbral "exacto" log2(3) tampoco garantiza el descenso.
#   8. La densidad: cuanta gente cumple, y el TAMANO EXACTO DEL CONJUNTO
#      EXCEPCIONAL a cada nivel K, por dos metodos independientes.
#
# TODO EN ARITMETICA EXACTA. La condicion X/N < L se traduce a una
# comparacion de enteros sin un solo float:
#
#     X*log(10/3) < N*log 2   <=>   (10/3)^X < 2^N   <=>   5^X < 3^X * 2^(N-X)
#
# y por factorizacion unica nunca hay empate (para N >= 1), asi que la
# traduccion entera es exacta, no aproximada.

from fractions import Fraction
from decimal import Decimal, getcontext
from math import comb

# ------------------------------ CONSTANTES ------------------------------

PRECISION = 60          # digitos de decimal para las constantes
LIMITE_COTA = 100001    # hasta donde se comprueba la cota 5/3
LIMITE_COORD = 30000    # hasta donde se cruzan las coordenadas (A,B) vs (X,N)
LIMITE_TODOS_N = 20000  # trayectorias donde se comprueba TODO N
LIMITE_CONTRA = 20000   # busqueda de contraejemplos
K_BRUTO = 16            # residuos mod 2^K por fuerza bruta
K_DP = 1000             # niveles del conteo exacto por programacion dinamica
NS_BINOMIAL = [10, 20, 50, 100, 200, 400, 800, 1600, 3200]

getcontext().prec = PRECISION

FALLOS = 0


def bueno(x, n):
    """Condicion de Everett en forma entera exacta: X/N < L."""
    return 5 ** x < 3 ** x * 2 ** (n - x)


def atajo(m):
    """El mapa f de Everett."""
    if m % 2 == 0:
        return m // 2
    return (3 * m + 1) // 2


print("=" * 72)
print("VERIFICAR EVERETT 1977 - casi todo n tiene un iterado menor que n")
print("=" * 72)

# ================== 1. LA COTA 5/3, Y DONDE SE ROMPE ==================

print()
print("--- 1. La cota m_{i+1}/m_i <= 5/3 (mapa del ATAJO) ---")

peor = Fraction(0)
peor_m = None
malos = []
for m in range(3, LIMITE_COTA, 2):
    r = Fraction(3 * m + 1, 2 * m)
    if r > peor:
        peor, peor_m = r, m
    if r > Fraction(5, 3):
        malos.append(m)
if malos:
    raise SystemExit("FALLO: la cota 5/3 se rompe en impares >= 3: %s" % malos[:5])

# los pares nunca son problema
for m in range(2, 2000, 2):
    if Fraction(m // 2, m) != Fraction(1, 2):
        raise SystemExit("FALLO: un paso par no da razon 1/2 en m = %d" % m)

print("  impares 3..%d: razon maxima = %s en m = %d  (5/3 = %s)"
      % (LIMITE_COTA, peor, peor_m, Fraction(5, 3)))
print("  la cota se ALCANZA con igualdad en m = 3, y decrece a partir de ahi")
print("  pares: razon exactamente 1/2 siempre - comprobado 999 casos")

# donde falla: m = 1
r1 = Fraction(3 * 1 + 1, 2 * 1)
if r1 <= Fraction(5, 3):
    raise SystemExit("FALLO: m=1 deberia romper la cota y no la rompe")
print("  m = 1 (unico impar < 3): razon = %s > 5/3.  LA COTA FALLA SOLO AHI." % r1)

# y la version CLASICA de la misma cota, por si se quiere trabajar sin atajo
peorc = max(Fraction(3 * m + 1, m) for m in range(3, 20001, 2))
if peorc != Fraction(10, 3):
    raise SystemExit("FALLO: la cota clasica no da 10/3, da %s" % peorc)
print("  version clasica (paso 3n+1 solo): razon maxima = 10/3, tambien en m = 3")

# el fallo en m=1 tiene consecuencia real: n=1 rompe la desigualdad global
# m_0 = 1, un paso impar: m_1 = 2.  Cota: m_1 * 3^1 * 2^0 <= 5^1 * m_0 ?
if not (2 * 3 > 5 * 1):
    raise SystemExit("FALLO: n=1 deberia romper la desigualdad global")
print("  consecuencia: con n = 1 la desigualdad global se rompe (6 > 5).")
print("  El conjunto que hay que excluir por este motivo es EXACTAMENTE {1}.")

# ======================= 2. LA CONSTANTE L =======================

print()
print("--- 2. La constante L = log 2 / log(10/3) ---")

L = Decimal(2).ln() / (Decimal(10) / Decimal(3)).ln()
inv_L = 1 / L
log2_3 = Decimal(3).ln() / Decimal(2).ln()
log2_10_3 = (Decimal(10) / Decimal(3)).ln() / Decimal(2).ln()

print("  L          = %s" % str(L)[:22])
print("  1/L        = %s" % str(inv_L)[:22])
print("  log2(10/3) = %s   <- misma cosa" % str(log2_10_3)[:22])
print("  log2(3)    = %s" % str(log2_3)[:22])
print("  (1-L)/L    = %s   <- de aqui salio el 0,7369 del CLAUDE.md"
      % str((1 - L) / L)[:22])

if abs(inv_L - log2_10_3) > Decimal(10) ** -40:
    raise SystemExit("FALLO: 1/L no es log2(10/3)")
if abs(inv_L - (Decimal(10).ln() / Decimal(2).ln() - log2_3)) > Decimal(10) ** -40:
    raise SystemExit("FALLO: 1/L no es log2(10) - log2(3)")

hueco = inv_L - log2_3
log2_10_9 = (Decimal(10) / Decimal(9)).ln() / Decimal(2).ln()
if abs(hueco - log2_10_9) > Decimal(10) ** -40:
    raise SystemExit("FALLO: el hueco 1/L - log2(3) no es log2(10/9)")
print("  1/L - log2(3) = %s = log2(10/9)  <- el precio EXACTO de usar 5/3"
      % str(hueco)[:22])

# la traduccion entera de la condicion es exacta
for n in range(1, 60):
    for x in range(0, n + 1):
        dec = (Decimal(x) / Decimal(n)) < L
        ent = bueno(x, n)
        if dec != ent:
            raise SystemExit("FALLO: 5^X < 3^X*2^(N-X) no equivale a X/N < L "
                             "en X=%d N=%d" % (x, n))
print("  equivalencia  X/N < L  <=>  5^X < 3^X * 2^(N-X):")
print("    comprobada en los 1.830 pares (X,N) con N <= 59, 0 fallos, sin floats")

# ============== 3. LA TRADUCCION A LAS COORDENADAS DEL REPO ==============

print()
print("--- 3. La traduccion a (A,B): que son X y N en coordenadas del repo ---")

discrepancias = 0
for n in range(2, LIMITE_COORD):
    # clasico
    m, A, B = n, 0, 0
    while m != 1:
        if m % 2:
            m = 3 * m + 1
            A += 1
        else:
            m //= 2
            B += 1
    # atajo
    m, X, N = n, 0, 0
    while m != 1:
        if m % 2:
            X += 1
        m = atajo(m)
        N += 1
    if not (A == X and B == N):
        discrepancias += 1
        if discrepancias < 4:
            print("    n=%d A=%d X=%d B=%d N=%d" % (n, A, X, B, N))
if discrepancias:
    raise SystemExit("FALLO: %d discrepancias entre (A,B) y (X,N)" % discrepancias)

print("  n de 2 a %d: A == X y B == N en los %d casos, 0 fallos."
      % (LIMITE_COORD, LIMITE_COORD - 2))
print("  RAZON: cada paso IMPAR del atajo contiene un 3n+1 y UNA division.")
print("         Luego  X = A  y  N = B.  El total de pasos clasicos es A+B,")
print("         pero el N de Everett NO es A+B: es B solo.")
print()
print("  Por tanto  X/N = A/B, y la condicion X/N < L se traduce a:")
print("      A/B < L    <=>    B/A > 1/L = 1,73696...")
print("  El CLAUDE.md dice  A/(A+B) < L  <=>  B/A > 0,7369.  ESO ES OTRO NUMERO.")

# ¿es que la version clasica da otra L? Si, y sale la MISMA condicion en B/A.
# clasico: m_N <= (10/3)^A * (1/2)^B * m_0 < m_0  <=>  A*log(10/3) < B*log 2
# que es exactamente A/B < L otra vez. La L clasica sobre A+B seria:
L_clasico = Decimal(2).ln() / ((Decimal(10) / Decimal(3)).ln() + Decimal(2).ln())
print()
print("  Y si se insiste en usar N = A+B (pasos clasicos), la constante")
print("  correcta NO es 0,5757 sino %s," % str(L_clasico)[:20])
print("  que despejada da B/A > %s - el MISMO 1,737."
      % str((1 - L_clasico) / L_clasico)[:20])
if abs((1 - L_clasico) / L_clasico - inv_L) > Decimal(10) ** -40:
    raise SystemExit("FALLO: las dos rutas no dan el mismo umbral en B/A")

print()
print("  COMPROBACION DE COHERENCIA LOGICA (la que delata el error):")
print("    una condicion SUFICIENTE de descenso tiene que ser MAS EXIGENTE")
print("    que el umbral exacto, nunca mas floja. 1,737 > 1,585: coherente.")
print("    0,7369 < 1,585: IMPOSIBLE. Prometeria descenso donde no lo hay.")

# ============ 4. LA DESIGUALDAD DE EVERETT SOBRE NUMEROS DE VERDAD ============

print()
print("--- 4. La desigualdad  m_N * 3^X * 2^(N-X) <= 5^X * m_0  (forma entera) ---")

fallos_des = 0
pasos_totales = 0
holgura_min = None
for n in range(3, LIMITE_TODOS_N):
    m = n
    X = 0
    N = 0
    p5, p3, p2 = 1, 1, 1  # 5^X, 3^X, 2^(N-X)
    while m != 1:
        if m % 2:
            X += 1
            p5 *= 5
            p3 *= 3
        else:
            p2 *= 2
        m = atajo(m)
        N += 1
        pasos_totales += 1
        izq = m * p3 * p2
        der = p5 * n
        if izq > der:
            fallos_des += 1
            if fallos_des < 4:
                print("    FALLO n=%d N=%d X=%d m=%d" % (n, N, X, m))
        h = Fraction(der - izq, der)
        if holgura_min is None or h < holgura_min:
            holgura_min = h
if fallos_des:
    raise SystemExit("FALLO: %d violaciones de la desigualdad de Everett" % fallos_des)

print("  n de 3 a %d, TODOS los N de cada trayectoria." % LIMITE_TODOS_N)
print("  %d desigualdades comprobadas en enteros exactos, 0 fallos."
      % pasos_totales)
print("  holgura relativa minima = %s (se toca la igualdad: es el caso m=3)"
      % float(holgura_min))

# ============ 5. LA CONDICION CORRECTA GARANTIZA EL DESCENSO ============

print()
print("--- 5. X/N < L  =>  m_N < n   (condicion correcta, A/B < L) ---")

fallos_desc = 0
casos = 0
primer_N = {}
sin_descenso = []
for n in range(3, LIMITE_TODOS_N):
    m = n
    X = N = 0
    p5, p3, p2 = 1, 1, 1
    visto = None
    while m != 1:
        if m % 2:
            X += 1
            p5 *= 5
            p3 *= 3
        else:
            p2 *= 2
        m = atajo(m)
        N += 1
        if p5 < p3 * p2:          # 5^X < 3^X * 2^(N-X)
            casos += 1
            if visto is None:
                visto = N
            if not m < n:
                fallos_desc += 1
                if fallos_desc < 4:
                    print("    FALLO n=%d N=%d X=%d m=%d" % (n, N, X, m))
    if visto is None:
        sin_descenso.append(n)
    else:
        primer_N[n] = visto
if fallos_desc:
    raise SystemExit("FALLO: %d casos con X/N < L y sin descenso" % fallos_desc)

print("  n de 3 a %d: %d pares (n,N) cumplen la condicion." % (LIMITE_TODOS_N, casos))
print("  En LOS %d el iterado sale por debajo de n. 0 fallos." % casos)
print("  n para los que la condicion no se cumple NUNCA: %d %s"
      % (len(sin_descenso), sin_descenso[:10]))
maxN = max(primer_N.values())
arg = [k for k, v in primer_N.items() if v == maxN][0]
print("  primer N que la cumple: media %.2f, maximo %d (en n = %d)"
      % (sum(primer_N.values()) / len(primer_N), maxN, arg))

# --- 5b. EL CONJUNTO EXCEPCIONAL EN CARNE Y HUESO ---
# Los n de arriba SI bajan (todos llegan a 1), pero Everett no los certifica
# NUNCA, en ningun N de su trayectoria completa. Son el conjunto excepcional
# concreto, y todos caen en el hueco log2(10/9) entre 1,585 y 1,737.

print()
print("  5b. Los n que Everett NO certifica jamas (bajan, pero sin certificado):")
print("      n        A     B     B/A      log2(3)=1,58496  1/L=1,73697")
en_el_hueco = 0
for n in sorted(sin_descenso):
    m, A, B = n, 0, 0
    while m != 1:
        if m % 2:
            m = 3 * m + 1
            A += 1
        else:
            m //= 2
            B += 1
    if log2_3 < Decimal(B) / Decimal(A) < inv_L:
        en_el_hueco += 1
    if n < 100 or n > 19000:
        print("      %-8d %-5d %-5d %.6f" % (n, A, B, B / A))
print("      ... (%d en total hasta %d)" % (len(sin_descenso), LIMITE_TODOS_N))
print("      DE LOS %d, %d tienen B/A ENTRE log2(3) y 1/L." % (len(sin_descenso), en_el_hueco))
print("      O sea: el conjunto excepcional de Everett es EXACTAMENTE el hueco")
print("      log2(10/9) que se paga por usar 5/3 en vez de 3/2.")
if en_el_hueco != len(sin_descenso):
    raise SystemExit("FALLO: no todos los excepcionales caen en el hueco")

# ======= 6. LA CONDICION DEL CLAUDE.MD *NO* GARANTIZA EL DESCENSO =======

print()
print("--- 6. CONTRAEJEMPLOS a la traduccion del CLAUDE.md: A/(A+B) < 0,5757 ---")

# forma entera de A/(A+B) < L :  5^A < 3^A * 2^B   con N = A+B pasos CLASICOS
contra = []
n_con_contra = 0
for n in range(3, LIMITE_CONTRA):
    m = n
    A = B = 0
    p5, p3, p2 = 1, 1, 1
    tuvo = False
    while m != 1:
        if m % 2:
            m = 3 * m + 1
            A += 1
            p5 *= 5
            p3 *= 3
        else:
            m //= 2
            B += 1
            p2 *= 2
        if p5 < p3 * p2 and not m < n:      # cumple la condicion del repo y NO baja
            tuvo = True
            if len(contra) < 6:
                contra.append((n, A + B, A, B, m))
    if tuvo:
        n_con_contra += 1

if not contra:
    raise SystemExit("FALLO: no hay contraejemplos, la traduccion del repo seria correcta")

print("  Condicion del repo en forma entera: 5^A < 3^A * 2^B con N = A+B.")
print("  n de 3 a %d: %d numeros la cumplen en algun N SIN haber bajado."
      % (LIMITE_CONTRA, n_con_contra))
print("  Los primeros:")
for (n, N, A, B, m) in contra:
    print("    n=%-5d N=%-3d A=%-3d B=%-3d -> m_N = %-6d  (m_N >= n)" % (n, N, A, B, m))
print("  La condicion del CLAUDE.md NO es suficiente para el descenso. REFUTADA.")

# y con el umbral correcto, esos mismos casos no cumplen nada
n0, N0, A0, B0, m0 = contra[0]
print("  Ejemplo mas chico: n=%d tras %d pasos clasicos tiene B/A = %d/%d = %.4f,"
      % (n0, N0, B0, A0, B0 / A0))
print("  que pasa el 0,7369 del CLAUDE.md y no llega ni a log2(3) ni a 1,737.")

# ============ 7. EL UMBRAL "EXACTO" log2(3) TAMPOCO ES SUFICIENTE ============

print()
print("--- 7. Control: B/A > log2(3) tampoco garantiza el descenso ---")

contra3 = []
for n in range(3, 4000):
    m = n
    A = B = 0
    p3, p2 = 1, 1
    while m != 1:
        if m % 2:
            m = 3 * m + 1
            A += 1
            p3 *= 3
        else:
            m //= 2
            B += 1
            p2 *= 2
        if p2 > p3 and not m < n:       # 2^B > 3^A  y sin embargo no bajo
            if len(contra3) < 5:
                contra3.append((n, A, B, m))
if not contra3:
    raise SystemExit("FALLO: se esperaban contraejemplos a log2(3)")
print("  2^B > 3^A y aun asi m_N >= n. Primeros casos:")
for (n, A, B, m) in contra3:
    print("    n=%-5d A=%-3d B=%-3d B/A=%.4f -> m_N = %d" % (n, A, B, B / A, m))
print("  Motivo: la identidad del repo 2^B*m_N = 3^A*n + C tiene C > 0, luego")
print("  m_N > 3^A*n/2^B siempre. El +1 es justo lo que obliga al colchon 5/3.")
print("  O sea que el 1,585 NO es 'el umbral verdadero' de descenso garantizado:")
print("  es el umbral del modelo SIN el +1. El unico demostrable es el 1,737.")

# ============== 8. LA DENSIDAD Y EL CONJUNTO EXCEPCIONAL ==============

print()
print("--- 8. Densidad: cuantos cumplen, y el tamano del conjunto excepcional ---")

print()
print("  8a. Densidad exacta a un N fijo (suma binomial, Fraction):")
print("      N      X minimo malo    densidad excepcional")
for N in NS_BINOMIAL:
    x0 = None
    for x in range(N + 1):
        if not bueno(x, N):
            x0 = x
            break
    mala = sum(comb(N, x) for x in range(x0, N + 1))
    d = Fraction(mala, 2 ** N)
    print("      %-6d %-16d %.8f" % (N, x0, float(d)))

print()
print("  8b. Conjunto excepcional REAL: los n que no han bajado en NINGUN")
print("      N <= K. Conteo exacto de clases mod 2^K, por DOS metodos.")

# metodo A: fuerza bruta sobre los 2^K restos (Terras: el vector de paridad
# de los primeros K pasos lo fija n mod 2^K)
malos_bruto = 0
for r in range(2 ** K_BRUTO):
    m = r
    X = N = 0
    p5, p3, p2 = 1, 1, 1
    ok = False
    for _ in range(K_BRUTO):
        if m % 2:
            X += 1
            p5 *= 5
            p3 *= 3
        else:
            p2 *= 2
        m = atajo(m)
        N += 1
        if p5 < p3 * p2:
            ok = True
            break
    if not ok:
        malos_bruto += 1

# metodo B: programacion dinamica sobre (N, X). "no bueno en ningun paso"
# depende solo de (N, X) porque la condicion depende solo de (N, X).
dp = {0: 1}
malos_dp = {}
for N in range(1, K_DP + 1):
    nueva = {}
    for x, c in dp.items():
        for nx in (x, x + 1):          # paso par o impar
            if not bueno(nx, N):
                nueva[nx] = nueva.get(nx, 0) + c
    dp = nueva
    malos_dp[N] = sum(dp.values())

if malos_dp[K_BRUTO] != malos_bruto:
    raise SystemExit("FALLO: fuerza bruta %d != DP %d en K=%d"
                     % (malos_bruto, malos_dp[K_BRUTO], K_BRUTO))
print("      K = %d: fuerza bruta sobre %d restos = %d malos"
      % (K_BRUTO, 2 ** K_BRUTO, malos_bruto))
print("               programacion dinamica         = %d malos" % malos_dp[K_BRUTO])
print("      LOS DOS METODOS COINCIDEN. 0 discrepancias.")

print()
print("      K        clases excepcionales mod 2^K        densidad")
for K in [1, 2, 4, 8, 16, 32, 64, 128, 256, 500, 1000]:
    if K > K_DP:
        continue
    d = Fraction(malos_dp[K], 2 ** K)
    print("      %-8d %-36d %.9f" % (K, malos_dp[K] if K <= 64 else -1, float(d)))

print()
print("      (la columna del medio se pone a -1 cuando el entero no cabe;")
print("       la densidad es exacta en Fraction en todos los casos)")

# el conjunto excepcional es INFINITO y explicito
print()
print("  8c. El conjunto excepcional NO es vacio y se describe:")
for K in (4, 8, 16, 32):
    r = 2 ** K - 1
    m = r
    X = N = 0
    p5, p3, p2 = 1, 1, 1
    ok = False
    for _ in range(K):
        if m % 2:
            X += 1
            p5 *= 5
            p3 *= 3
        else:
            p2 *= 2
        m = atajo(m)
        N += 1
        if p5 < p3 * p2:
            ok = True
    if ok:
        raise SystemExit("FALLO: 2^%d-1 deberia ser excepcional a nivel %d" % (K, K))
    print("      n = 2^%d - 1 = %d : %d pasos impares seguidos, X/N = 1, "
          "excepcional a nivel K=%d" % (K, r, K, K))
print("      Toda la clase n = 2^K - 1 (mod 2^K) esta fuera de Everett a nivel K.")
print("      Son 2^(-K) de los enteros: la densidad tiende a 0 pero el conjunto")
print("      es INFINITO para cada K, y la interseccion sobre todo K es donde")
print("      viviria un contraejemplo. Everett no dice nada de ella.")

print()
print("=" * 72)
print("RESUMEN")
print("=" * 72)
print("  1. La cota 5/3 es correcta y ajustada (igualdad en m=3). Falla SOLO")
print("     en m=1, y por eso Everett pide m >= 3. Excluye exactamente {1}.")
print("  2. L = 0,57571... y 1/L = log2(10/3) = 1,73696...")
print("  3. LA TRADUCCION DEL CLAUDE.md ESTA MAL. X=A y N=B, no N=A+B.")
print("     Everett en coordenadas del repo es  B/A > 1,73696, NO 0,7369.")
print("  4. La desigualdad de Everett: 0 fallos en enteros exactos.")
print("  5. La condicion correcta garantiza el descenso: 0 fallos.")
print("  6. La condicion del CLAUDE.md NO lo garantiza: contraejemplos.")
print("  7. B/A > log2(3) TAMPOCO lo garantiza. El +1 lo impide.")
print("  8. Es COTA por trayectoria y PROMEDIO en la densidad. Solo la cota")
print("     sirve para la formula.")
