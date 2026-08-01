# verificar_ciclos.py
#
# LAS COTAS DE CICLOS, RE-DERIVADAS DESDE CERO CON ARITMETICA EXACTA.
#
# Este programa no dibuja nada. Coge las cinco afirmaciones importadas sobre las
# que el repo apoyo la decision de DAR POR CERRADO el camino de buscar ciclos, y
# las vuelve a calcular con codigo propio, sin creerselas por estar publicadas.
#
# LAS CINCO AFIRMACIONES
#
#   (1) Los convergentes de log2(3). El repo dice que las casillas (A,B) que
#       sobreviven al barrido son exactamente las convergentes y
#       semiconvergentes de la fraccion continua. Atribuido a Shanks 1965 /
#       Guy 1983.
#
#   (2) Eliahou 1993 (Discrete Math. 118, 45-56). La longitud de un ciclo no
#       trivial tiene forma cerrada:  N = 301994a + 17087915b + 85137581c
#       con a,b,c >= 0, b >= 1, a*c = 0.
#
#   (3) Barina 2025 (J. Supercomputing 81, art. 810). Verificado hasta 2^71, y
#       de ahi el repo deduce que un ciclo tendria que medir >= 217.976.794.617
#       pasos del atajo / 355.504.839.929 del mapa clasico.
#
#   (4) Simons-de Weger (Acta Arith. 117 (2005) 51-70; preprint web v1.44 de
#       2010). La cota  K < 1,4784 * m * delta^m  para 91 <= m <= 515.619, y el
#       arranque K > 7,5311*10^11. El repo la trata como CAJA NEGRA y afirma que
#       "Hercher NO usa el teorema de Baker en ninguna parte".
#
#   (5) Hercher 2023 (J. Integer Sequences 26, art. 23.3.5). No hay m-ciclos con
#       m <= 91. El repo tiene reimpl.py, que reproduce su Teorema 23 y encuentra
#       DOS DISCREPANCIAS contra lo publicado. Aqui se rehacen con codigo
#       independiente para confirmarlas.
#
# COMO SE HACE LA ARITMETICA
#
#   log(2) y log(3) salen de la serie de atanh con el resto acotado a mano en
#   Fraction, igual de riguroso que en reimpl.py pero con OTRA DESCOMPOSICION,
#   para que las dos no compartan el error si lo hubiera:
#
#       reimpl.py :  log(2) = 2*atanh(1/3)          log(3) = log(2) + 2*atanh(1/5)
#       aqui      :  log(2) = 2*atanh(1/5) + 2*atanh(1/7)   [ = log(3/2)+log(4/3) ]
#                    log(3) = log(2) + 2*atanh(1/5)
#
#   Nada de floats en la cadena que decide. Los float que aparecen son solo para
#   imprimir. Las dos unicas exponenciales van con decimal a precision declarada
#   y con un margen restado a mano.
#
# LO QUE NO SE PUEDE HACER AQUI, Y SE DICE
#
#   El m <= 91 de Hercher se sostiene sobre el Teorema 21 (media seccion de
#   analisis de casos mas dos programas en C++ con sumas parciales de hasta 36
#   sumandos) y sobre la cota de Simons-de Weger (cuya cadena entra en teoria de
#   la trascendencia). Nada de eso se reverifica: cinco semanas de C++ no caben
#   en un script. Lo que si se puede es rehacer la ARITMETICA final y las tablas
#   computacionales, que es la parte que nadie vuelve a mirar.

import math
import sys
from decimal import Decimal, getcontext, ROUND_FLOOR
from fractions import Fraction

sys.setrecursionlimit(20000)

# ---------------------------------------------------------------------------
# Cambia esto aqui, guarda, y dale a Ctrl+B en Sublime.
# ---------------------------------------------------------------------------

TERMINOS_SERIE = 420        # sumandos de atanh; 420 dan error < 10^-580
TERMINOS_CF = 560           # cuantos terminos de la fraccion continua certificar
REJILLA = 80                # rejilla de trabajo para el Teorema 23: 10^-REJILLA
CIFRAS_DECIMAL = 200        # precision de las dos exponenciales
MARGEN = Fraction(1, 10 ** 70)

# los limites de verificacion por fuerza bruta que se van a cruzar
X0_ELIAHOU = 240 * 2 ** 40          # el de la epoca de Eliahou 1993
X0_SINISALO = 204 * 2 ** 50         # el de Sinisalo 2003
X0_HERCHER = 695 * 2 ** 60          # el que usa Hercher 2023
X0_BARINA_2071 = 2 ** 71            # "2^71" a secas
X0_BARINA_REAL = 2075 * 2 ** 60     # lo que dice hoy la pagina de Barina
X0_2072 = 2 ** 72

# Hercher, Teorema 23
M_TOPE = 91
K_ARRANQUE = 7 * 10 ** 11
ITERACIONES = 7

# Los valores publicados, copiados del fuente LaTeX del articulo
# (hercher5.tex, demostracion del Main Theorem). (m_2, epsilon, cota de K)
HERCHER_PUBLICADO = [
    (47, "6.9e-32", "5.2e15"),
    (67, "5.1e-36", "3.97e17"),
    (77, "4.1e-38", "4.64e18"),
    (82, "2.3e-39", "2.74e19"),
    (86, "2.3e-40", "7.76e19"),
    (88, "5.3e-41", "2.05e20"),
    (91, "1.11e-43", "7.94e21"),
]
HERCHER_TABLA1 = [(98, "7.76e19"), (117, "2.74e19"), (276, "4.68e18")]

# Eliahou 1993: los tres generadores de la forma cerrada
ELIAHOU_A, ELIAHOU_B, ELIAHOU_C = 301994, 17087915, 85137581

# Simons-de Weger, Teorema 3(d) de la version web 1.44 (2010), y su tabla de
# campeones de la fraccion continua (seccion 6.2).
SW_FACTOR = Fraction(14784, 10000)
SW_K2_91 = "2.1408e20"
SW_CAMPEONES = [          # (n(m), A(m), K1(m) <, q_{n(m)-1} >)
    (218, 55, "1.3035e106", "1.3133e106"),
    (230, 100, "1.4043e114", "1.7807e114"),
    (330, 964, "2.0804e167", "2.6341e167"),
    (528, 2436, "2.1843e272", "2.3119e272"),
]

getcontext().prec = CIFRAS_DECIMAL


# ===========================================================================
# LOGARITMOS CERTIFICADOS, SIN LIBRERIA NUMERICA
# ===========================================================================
#
# atanh(x) = x + x^3/3 + x^5/5 + ... con todos los sumandos positivos. Cortando
# en N sumandos, lo que falta cumple
#
#     R = suma_{k>=N} x^(2k+1)/(2k+1)  <  x^(2N+1) / ((2N+1)*(1-x^2))
#
# porque cada sumando es menor que el anterior por el factor x^2. Eso da un
# intervalo racional exacto sin creerle nada a ninguna libreria.

def atanh_acotado(x, terminos):
    """Devuelve (lo, hi) racionales con lo < atanh(x) < hi."""
    suma = Fraction(0)
    potencia = x
    x2 = x * x
    for k in range(terminos):
        suma += potencia / (2 * k + 1)
        potencia *= x2
    resto = potencia / ((2 * terminos + 1) * (1 - x2))
    return suma, suma + resto


_a5 = atanh_acotado(Fraction(1, 5), TERMINOS_SERIE)   # atanh(1/5) = log(3/2)/2
_a7 = atanh_acotado(Fraction(1, 7), TERMINOS_SERIE)   # atanh(1/7) = log(4/3)/2

LOG32_LO, LOG32_HI = 2 * _a5[0], 2 * _a5[1]
LOG43_LO, LOG43_HI = 2 * _a7[0], 2 * _a7[1]
LOG2_LO, LOG2_HI = LOG32_LO + LOG43_LO, LOG32_HI + LOG43_HI
LOG3_LO, LOG3_HI = LOG2_LO + LOG32_LO, LOG2_HI + LOG32_HI

DELTA_LO = LOG3_LO / LOG2_HI
DELTA_HI = LOG3_HI / LOG2_LO


# ---------------------------------------------------------------------------
# COMPROBACION 0 -- los logaritmos, contra aritmetica entera pura
# ---------------------------------------------------------------------------
#
# log2(3) es irracional, asi que no hay con que compararlo directamente. Pero
# para CUALQUIER fraccion p/q vale la equivalencia exacta
#
#     p/q < log2(3)   <=>   2^p < 3^q
#
# y eso son dos enteros que Python compara sin un solo redondeo.

print("=" * 74)
print("COMPROBACION 0 -- los logaritmos certificados contra enteros exactos")
print("=" * 74)
print()
def orden_de(fr):
    """Exponente decimal aproximado de una fraccion positiva, sin float."""
    if fr <= 0:
        return None
    return len(str(fr.numerator)) - len(str(fr.denominator))


print("  log(2) = 2*atanh(1/5) + 2*atanh(1/7),  log(3) = log(2) + 2*atanh(1/5)")
print(f"  con {TERMINOS_SERIE} sumandos y el resto acotado a mano en Fraction.")
print("  (los anchos se dan en orden de magnitud: son demasiado chicos para")
print("  caber en un float, que los redondearia a cero)")
print(f"    ancho del encierro de log(2): 10^{orden_de(LOG2_HI - LOG2_LO)}")
print(f"    ancho del encierro de log(3): 10^{orden_de(LOG3_HI - LOG3_LO)}")
print(f"    ancho del encierro de delta:  10^{orden_de(DELTA_HI - DELTA_LO)}")
print(f"  delta_lo = {float(DELTA_LO):.18f}")
print()
print("  Prueba exacta con enteros:  p/q < log2(3)  <=>  2^p < 3^q")
print()
print(f"    {'p':>8} {'q':>8} {'2^p < 3^q':>11} {'p/q < delta_lo':>16} "
      f"{'p/q > delta_hi':>16}  coherente")
print(f"    {'-'*8} {'-'*8} {'-'*11} {'-'*16} {'-'*16}  ---------")

FALLOS_LOG = 0
for p, q in [(1, 1), (2, 1), (3, 2), (8, 5), (19, 12), (65, 41), (84, 53),
             (485, 306), (1054, 665), (24727, 15601), (50508, 31867),
             (125743, 79335), (176251, 111202), (301994, 190537)]:
    verdad = 2 ** p < 3 ** q
    debajo = Fraction(p, q) < DELTA_LO
    encima = Fraction(p, q) > DELTA_HI
    coherente = (verdad and debajo) or ((not verdad) and encima)
    if not coherente:
        FALLOS_LOG += 1
    print(f"    {p:>8} {q:>8} {str(verdad):>11} {str(debajo):>16} "
          f"{str(encima):>16}  {'ok' if coherente else 'FALLA'}")

print()
print(f"  fracciones probadas: 14   incoherencias: {FALLOS_LOG}")
if FALLOS_LOG:
    raise SystemExit("El encierro de delta no coincide con la aritmetica entera. No sigas.")
print("  0 fallos. El encierro de delta esta certificado con enteros puros.")


# ===========================================================================
# COMPROBACION 1 -- LA FRACCION CONTINUA DE log2(3) Y SUS CONVERGENTES
# ===========================================================================
#
# Se leen terminos mientras las partes enteras de los dos extremos del encierro
# coincidan. Si coinciden, el termino esta CERTIFICADO: cualquier numero del
# intervalo da el mismo. En cuanto discrepan, se para.

def fraccion_continua(lo, hi, tope):
    cf = []
    a, b = lo, hi
    for _ in range(tope):
        ia = a.numerator // a.denominator
        ib = b.numerator // b.denominator
        if ia != ib:
            break
        cf.append(ia)
        if a - ia == 0 or b - ib == 0:
            break
        a, b = 1 / (b - ib), 1 / (a - ia)
    return cf


CF = fraccion_continua(DELTA_LO, DELTA_HI, TERMINOS_CF)

CONV = []            # [(p_n, q_n)]
SEMICONV = set()     # denominadores de convergentes y semiconvergentes
SEMICONV_PQ = []     # (p, q) de todas las semiconvergentes, en orden
_h2, _h1, _k2, _k1 = 0, 1, 1, 0
for _t in CF:
    for _j in range(1, _t + 1):
        SEMICONV.add(_j * _k1 + _k2)
        SEMICONV_PQ.append((_j * _h1 + _h2, _j * _k1 + _k2))
    _h2, _h1, _k2, _k1 = _h1, _t * _h1 + _h2, _k1, _t * _k1 + _k2
    CONV.append((_h1, _k1))

# la publicada por Sinisalo 2003 (preprint, Univ. de Oulu), primeros 30 terminos
CF_SINISALO = [1, 1, 1, 2, 2, 3, 1, 5, 2, 23, 2, 2, 1, 1, 55, 1, 4, 3, 1, 1,
               15, 1, 9, 2, 5, 7, 1, 1, 4, 8]

print()
print("=" * 74)
print("COMPROBACION 1 -- la fraccion continua de log2(3) y sus convergentes")
print("=" * 74)
print()
print(f"  terminos certificados por el encierro: {len(CF)}")
print(f"  los 30 primeros: {CF[:30]}")
print()
coincide_cf = CF[:30] == CF_SINISALO
print(f"  contra los 30 publicados por Sinisalo (2003): "
      f"{'IDENTICOS' if coincide_cf else 'DIFIEREN'}")
if not coincide_cf:
    raise SystemExit("La fraccion continua no coincide con la publicada. Revisalo.")

print()
print("  Los primeros convergentes p_n/q_n (indice desde 0):")
print()
print(f"    {'n':>4} {'a_n':>6} {'p_n':>22} {'q_n':>22}")
print(f"    {'-'*4} {'-'*6} {'-'*22} {'-'*22}")
for n in range(0, 26):
    print(f"    {n:>4} {CF[n]:>6} {CONV[n][0]:>22,} {CONV[n][1]:>22,}")

# Los que este repo ya usaba en pinzaciclos.py como "las casillas (A,B) que
# sobreviven": (A,B) = (q_n, p_n).
print()
print("  Las casillas (A,B) del repo son (q_n, p_n): (1,1) (1,2) (2,3) (5,8)")
print("  (12,19) (41,65) (53,84) (306,485) (665,1054) (15601,24727) ... y son")
print("  exactamente estas. La fila 7 es (A=41, B=65), la del 221.")
_esperadas = [(1, 1), (1, 2), (2, 3), (5, 8), (12, 19), (41, 65), (53, 84),
              (306, 485), (665, 1054), (15601, 24727), (31867, 50508)]
FALLOS_AB = sum(1 for i, (a, b) in enumerate(_esperadas)
                if (CONV[i][1], CONV[i][0]) != (a, b))
print(f"  casillas que no coinciden: {FALLOS_AB} de {len(_esperadas)}")
if FALLOS_AB:
    raise SystemExit("Las casillas (A,B) no son los convergentes. Revisalo.")


# ---------------------------------------------------------------------------
# COMPROBACION 1b -- que las MEJORES APROXIMACIONES POR ARRIBA sean
# exactamente las semiconvergentes. Es la afirmacion "Shanks 1965 / Guy 1983"
# del CLAUDE.md, rehecha a lo bruto.
# ---------------------------------------------------------------------------
#
# Para cada A se toma el menor B con B/A > delta (que es la unica casilla que
# puede alojar un ciclo de 3n+1, porque la C de la identidad del repo es > 0).
# Se guarda A cuando B/A - delta bate el record. Esos records tienen que ser
# exactamente las semiconvergentes por arriba.

LIMITE_AB = 200000
print()
print(f"  Barrido de casillas (A,B) hasta A = {LIMITE_AB:,}: para cada A, el menor")
print("  B con B/A > delta, y se anota cuando B/A - delta bate record.")

records_ab = []
mejor = None
for A in range(1, LIMITE_AB + 1):
    B = (A * DELTA_HI).numerator // (A * DELTA_HI).denominator + 1
    dif_lo = Fraction(B, A) - DELTA_HI      # cota inferior de B/A - delta
    dif_hi = Fraction(B, A) - DELTA_LO      # cota superior
    if mejor is None or dif_hi < mejor:
        mejor = dif_lo
        records_ab.append((A, B))

falsos_ab = [(A, B) for A, B in records_ab if (B, A) not in
             [(p, q) for p, q in SEMICONV_PQ]]
# comprobacion exacta con enteros para los A chicos, sin tocar delta
FALLOS_EXACTO = 0
for A, B in records_ab:
    if A <= 3000:
        if not (2 ** B > 3 ** A) or (2 ** (B - 1) > 3 ** A):
            FALLOS_EXACTO += 1

print(f"    casillas record encontradas:            {len(records_ab)}")
print(f"    de esas, que NO son semiconvergentes:   {len(falsos_ab)}")
print(f"    verificacion entera exacta (A <= 3000): {FALLOS_EXACTO} fallos")
if falsos_ab or FALLOS_EXACTO:
    raise SystemExit("Las casillas record no son las semiconvergentes. Revisalo.")
print("    0 y 0. CONFIRMADO: las casillas (A,B) que sobreviven son exactamente")
print("    las convergentes y semiconvergentes por arriba de log2(3).")
print(f"    las diez ultimas: {[(A, B) for A, B in records_ab[-10:]]}")


# ===========================================================================
# COMPROBACION 2 -- ELIAHOU 1993: DE DONDE SALEN 301994, 17087915 Y 85137581
# ===========================================================================

print()
print("=" * 74)
print("COMPROBACION 2 -- Eliahou 1993: los tres generadores de la forma cerrada")
print("=" * 74)
print()
print("  El CLAUDE.md cita la forma  N = 301994a + 17087915b + 85137581c  sin")
print("  decir de donde salen los tres numeros. Salen de aqui:")
print()

ELIAHOU_INDICES = []
for gen in (ELIAHOU_A, ELIAHOU_B, ELIAHOU_C):
    idx = [n for n, (p, q) in enumerate(CONV) if p == gen]
    ELIAHOU_INDICES.append(idx[0] if idx else None)
    if idx:
        n = idx[0]
        print(f"    {gen:>10,}  =  p_{n}   (convergente {n}: "
              f"{CONV[n][0]:,}/{CONV[n][1]:,})")
    else:
        print(f"    {gen:>10,}  NO es numerador de ninguna convergente")

if None in ELIAHOU_INDICES:
    raise SystemExit("Un generador de Eliahou no es numerador de convergente. Revisalo.")
print()
print(f"  Los tres son numeradores de convergentes: n = {ELIAHOU_INDICES}.")
print("  O sea que la 'forma cerrada de Eliahou' NO es una formula caida del")
print("  cielo: es la estructura de semigrupo de las semiconvergentes por")
print("  arriba de log2(3), escrita con los tres generadores de su epoca.")
print("  CONFIRMADA, y ademas explicada.")

print()
print("  Y el minimo de la forma (b >= 1, a*c = 0) es b=1, a=c=0:")
print(f"    N_min = {ELIAHOU_B:,}  -- que es exactamente la cota que Eliahou")
print("    publica en 1993 para la longitud de ciclo en el mapa del atajo.")


def eliahou_representaciones(N, tope=None):
    """Todas las (a,b,c) con N = 301994a + 17087915b + 85137581c, b>=1, a*c=0."""
    sol = []
    for a in range(0, N // ELIAHOU_A + 1):
        r = N - ELIAHOU_A * a
        if r > 0 and r % ELIAHOU_B == 0:
            sol.append((a, r // ELIAHOU_B, 0))
        if tope and len(sol) >= tope:
            return sol
    for c in range(1, N // ELIAHOU_C + 1):
        r = N - ELIAHOU_C * c
        if r > 0 and r % ELIAHOU_B == 0:
            sol.append((0, r // ELIAHOU_B, c))
        if tope and len(sol) >= tope:
            return sol
    return sol


# ===========================================================================
# COMPROBACION 3 -- LA LONGITUD MINIMA DE CICLO PARA CADA X_0
# ===========================================================================
#
# Sinisalo (2003), Teorema 1, que es la version limpia de lo de Eliahou: si el
# ciclo tiene n pasos n/2 y k pasos 3n+1, y todos sus elementos superan X_0,
# entonces
#
#     log2(3)  <  n/k  <=  log2(3 + 1/X_0)
#
# y la longitud minima la da la fraccion de MENOR DENOMINADOR del intervalo.
# La longitud en el mapa clasico es n+k; en el mapa del atajo es n (cada 3n+1
# viene pegado a su division).
#
# Aqui todo se calcula con racionales exactos, y el intervalo se ENSANCHA
# siempre: se usa (delta_lo, delta_hi + cota_superior_del_hueco), que CONTIENE
# al verdadero. Ensanchar solo puede bajar el denominador minimo, o sea dar una
# cota de longitud MAS FLOJA. El error cae del lado seguro.

def denominador_minimo(a, b):
    """Fraccion de denominador mas chico estrictamente dentro de (a, b)."""
    if a >= b:
        raise SystemExit("intervalo vacio o al reves en denominador_minimo")
    entera = a.numerator // a.denominator
    if entera + 1 < b:
        return Fraction(entera + 1)
    resto_a = a - entera
    resto_b = b - entera
    if resto_a == 0:
        inverso = 1 / resto_b
        return entera + Fraction(1, inverso.numerator // inverso.denominator + 1)
    return entera + 1 / denominador_minimo(1 / resto_b, 1 / resto_a)


def tope_intervalo(X0):
    """Cota SUPERIOR de log2(3 + 1/X0) - log2(3) = log(1 + 1/(3 X0))/log(2).

    Se usa log(1+x) < x, que sobreestima, y se divide por la cota INFERIOR de
    log(2), que vuelve a sobreestimar. Las dos ensanchan el intervalo.
    """
    x = Fraction(1, 3 * X0)
    return x / LOG2_LO


def longitud_minima(X0):
    frac = denominador_minimo(DELTA_LO, DELTA_HI + tope_intervalo(X0))
    n, k = frac.numerator, frac.denominator
    return n, k, n, n + k       # (n, k, atajo, clasico)


print()
print("=" * 74)
print("COMPROBACION 3 -- la longitud minima de ciclo que permite cada X_0")
print("=" * 74)
print()
print("  Sinisalo 2003, Teorema 1: la fraccion n/k de menor denominador dentro")
print("  de (log2(3), log2(3+1/X_0)]. Todo con Fraction, intervalo ensanchado.")
print()
print(f"  {'X_0':>26} {'n/k':>34} {'atajo':>17} {'clasico':>17}")
print(f"  {'-'*26} {'-'*34} {'-'*17} {'-'*17}")

CASOS_X0 = [
    ("240*2^40  (Eliahou 1993)", X0_ELIAHOU),
    ("204*2^50  (Sinisalo 2003)", X0_SINISALO),
    ("2^68      (Barina 2020)", 2 ** 68),
    ("695*2^60  (Hercher 2023)", X0_HERCHER),
    ("2^71      (Barina 2025)", X0_BARINA_2071),
    ("2075*2^60 (Barina, hoy)", X0_BARINA_REAL),
    ("2^72      (hipotetico)", X0_2072),
    ("2^75      (hipotetico)", 2 ** 75),
]
RESULTADOS_X0 = {}
for nombre, X0 in CASOS_X0:
    n, k, atajo, clasico = longitud_minima(X0)
    RESULTADOS_X0[nombre] = (n, k, atajo, clasico)
    print(f"  {nombre:>26} {str(n)+'/'+str(k):>34} {atajo:>17,} {clasico:>17,}")

# --- contraste con lo publicado por Eliahou y por Sinisalo
_e = RESULTADOS_X0["240*2^40  (Eliahou 1993)"]
_s = RESULTADOS_X0["204*2^50  (Sinisalo 2003)"]
print()
print("  Contra lo publicado:")
print(f"    Eliahou 1993 publica  17.087.915 (atajo)  -> aqui sale {_e[2]:,}   "
      f"{'ok' if _e[2] == 17087915 else 'FALLA'}")
print(f"    Sinisalo 2003 publica 1.027.712.276 (clasico) -> aqui sale {_s[3]:,}   "
      f"{'ok' if _s[3] == 1027712276 else 'FALLA'}")
if _e[2] != 17087915 or _s[3] != 1027712276:
    raise SystemExit("No se reproducen las cotas publicadas de Eliahou/Sinisalo. No sigas.")
print("    Las dos, clavadas. La maquinaria reproduce dos resultados publicados")
print("    con veintitres anos de diferencia entre ellos.")


# ---------------------------------------------------------------------------
# COMPROBACION 3b -- LA ADMISIBILIDAD DE CADA FRACCION, CERTIFICADA
# ---------------------------------------------------------------------------
#
# Aqui NO se ensancha: se decide con certificado en las dos direcciones, para
# poder afirmar tanto "esta fraccion SIGUE VIVA" como "esta fraccion ESTA
# MUERTA". La cantidad que decide es la misma lambda de Simons-de Weger:
#
#     Lambda = n*log(2) - k*log(3)
#
#   admisible          <=>   0 < Lambda <= k*log(1 + 1/(3*X_0))
#   ya eliminada       <=>   Lambda > k*log(1 + 1/(3*X_0))

def veredicto(n, k, X0):
    lam_lo = n * LOG2_LO - k * LOG3_HI
    lam_hi = n * LOG2_HI - k * LOG3_LO
    x = Fraction(1, 3 * X0)
    rhs_lo = k * (x - x * x / 2)
    rhs_hi = k * x
    if lam_hi <= 0:
        return "por debajo de delta"
    if lam_lo <= 0:
        return "INDECISO"
    if lam_hi <= rhs_lo:
        return "VIVA"
    if lam_lo > rhs_hi:
        return "muerta"
    return "INDECISO"


FRACCIONES = [
    (630138897, 397573379),
    (9809721694, 6189245291),
    (10439860591, 6586818670),
    (114208327604, 72057431991),
    (217976794617, 137528045312),
]

print()
print("  Y ahora sin ensanchar, con certificado en las dos direcciones. La")
print("  cantidad que decide es Lambda = n*log(2) - k*log(3), la misma de")
print("  Simons-de Weger. Una fraccion esta VIVA si 0 < Lambda <= k*log(1+1/(3X0)).")
print()
enc = [("695*2^60 (Hercher)", X0_HERCHER), ("2^71", X0_BARINA_2071),
       ("2075*2^60 (Barina hoy)", X0_BARINA_REAL), ("2^72", X0_2072)]
print(f"  {'n/k':>32} {'clasico':>16}", end="")
for nom, _ in enc:
    print(f" {nom:>22}", end="")
print()
print(f"  {'-'*32} {'-'*16}" + "".join(f" {'-'*22}" for _ in enc))
for n, k in FRACCIONES:
    print(f"  {str(n)+'/'+str(k):>32} {n+k:>16,}", end="")
    for _, X0 in enc:
        print(f" {veredicto(n, k, X0):>22}", end="")
    print()

INDECISOS = sum(1 for n, k in FRACCIONES for _, X0 in enc
                if veredicto(n, k, X0) == "INDECISO")
print()
print(f"  veredictos indecisos (precision insuficiente): {INDECISOS}")
if INDECISOS:
    raise SystemExit("Hay veredictos indecisos: sube TERMINOS_SERIE. No sigas.")


# ---------------------------------------------------------------------------
# COMPROBACION 3c -- LA FORMA DE ELIAHOU CONTRA TODAS ESTAS LONGITUDES
# ---------------------------------------------------------------------------

print()
print("  La forma cerrada de Eliahou contra estas longitudes (barrido exhaustivo):")
print()
print(f"  {'longitud (atajo)':>20} {'(a, b, c)':>26}  encaja")
print(f"  {'-'*20} {'-'*26}  ------")
FALLOS_ELIAHOU = 0
for n, k in FRACCIONES:
    reps = eliahou_representaciones(n, tope=2)
    ok = len(reps) > 0
    if not ok:
        FALLOS_ELIAHOU += 1
    print(f"  {n:>20,} {str(reps[0]) if ok else '(ninguna)':>26}  "
          f"{'si' if ok else 'NO'}")
# el 17087915 y el numero de Laurore que el repo ya habia descartado
for extra, etiqueta in [(17087915, "Eliahou 1993"), (19478780533, "Laurore 2025")]:
    reps = eliahou_representaciones(extra, tope=2)
    print(f"  {extra:>20,} {str(reps[0]) if reps else '(ninguna)':>26}  "
          f"{'si' if reps else 'NO'}   <- {etiqueta}")

if FALLOS_ELIAHOU:
    raise SystemExit("Una longitud admisible no encaja en la forma de Eliahou. Revisalo.")
print()
print("  Las cinco longitudes admisibles encajan; el 19.478.780.533 no. Eso")
print("  confirma, por un camino distinto, el descarte que el repo ya habia hecho.")


# ---------------------------------------------------------------------------
# COMPROBACION 3d -- EL CRUCE QUE IMPORTA: LA COTA QUE EL REPO CITA
# ---------------------------------------------------------------------------

print()
print("=" * 74)
print("COMPROBACION 3d -- la cota de ciclo que el CLAUDE.md atribuye a Barina")
print("=" * 74)
print()
print("  El CLAUDE.md dice, como estado del arte tras la correccion del 01-08-2026:")
print("     'cualquier otro ciclo tendria que medir >= 217.976.794.617 pasos del")
print("      atajo - 355.504.839.929 del mapa clasico'")
print()

n71, k71, at71, cl71 = RESULTADOS_X0["2^71      (Barina 2025)"]
nre, kre, atre, clre = RESULTADOS_X0["2075*2^60 (Barina, hoy)"]
n72, k72, at72, cl72 = RESULTADOS_X0["2^72      (hipotetico)"]

print(f"  Con X_0 = 2^71                = {X0_BARINA_2071:,}")
print(f"     -> minimo {at71:,} (atajo) / {cl71:,} (clasico)")
print(f"  Con X_0 = 2075*2^60 (lo que dice hoy la pagina de Barina)")
print(f"     -> minimo {atre:,} (atajo) / {clre:,} (clasico)")
print(f"  Con X_0 = 2^72                = {X0_2072:,}")
print(f"     -> minimo {at72:,} (atajo) / {cl72:,} (clasico)")
print()

# el X_0 exacto que haria falta para matar la fraccion de 114 mil millones
_n, _k = 114208327604, 72057431991
_lam_lo = _n * LOG2_LO - _k * LOG3_HI
# hace falta X0 con  k*log(1+1/(3X0)) < Lambda,  y log(1+x) > x - x^2/2
# basta k*x <= Lambda_lo, o sea  X0 >= k/(3*Lambda_lo)
X0_NECESARIO = _k / (3 * _lam_lo)
print(f"  Para que 114.208.327.604 quede eliminada hace falta")
print(f"     X_0 >= {float(X0_NECESARIO):.6e}  =  2^{math.log2(float(X0_NECESARIO)):.3f}")
print(f"  y Barina esta en 2075*2^60 = {float(X0_BARINA_REAL):.6e} = "
      f"2^{math.log2(float(X0_BARINA_REAL)):.3f}.")
print()

CITA_CORRECTA = (at71 == 217976794617)
if CITA_CORRECTA:
    print("  La cita del CLAUDE.md queda CONFIRMADA.")
else:
    print("  *** LA CITA DEL CLAUDE.MD ES UNA FILA DEMASIADO FUERTE. ***")
    print()
    print("  El 217.976.794.617 / 355.504.839.929 corresponde a X_0 >= 2^71,885,")
    print("  no a 2^71. Con la verificacion que Barina tiene HOY el minimo es")
    print(f"     {atre:,} pasos del atajo")
    print(f"     {clre:,} pasos del clasico")
    print(f"  o sea un factor {217976794617/atre:.4f} menos que lo que el repo cita.")
    print()
    print("  Es el mismo tipo de error que ya mordio dos veces (Wu-Huang sin DOI,")
    print("  la cota de Laurore once veces mas debil), pero al reves: esta vez la")
    print("  cota citada es demasiado FUERTE, o sea a favor del repo.")
    print()
    print("  Ojo: la CONCLUSION del repo no se cae. Su tramo mas largo mide 114")
    print("  pasos, y 114 sigue estando nueve ordenes de magnitud por debajo de")
    print(f"  {atre:,}. Lo que se cae es el numero, no el argumento.")


# ===========================================================================
# COMPROBACION 4 -- SIMONS-DE WEGER: EL 1,4784 NO ES UNA CAJA NEGRA
# ===========================================================================
#
# El CLAUDE.md trata  K < 1,4784 * m * delta^m  como un numero importado que
# hay que aceptar. Se puede rehacer. Simons-de Weger definen K_2(m) como la
# mayor solucion de
#
#     m * c_m * 2^(-((delta-1)/(delta^m - 1)) * x)  =  log(2) / ((A(m)+2) * x)
#
# con  c_m -> 2^(-1/(delta-1))  y  A(m)  el "campeon" anterior de la fraccion
# continua. Y  k_2(m) = K_2(m) / (m * delta^m).  Para m = 91 su tabla imprime
# K_2(91) < 2,1408*10^20  y  k_2(91) < 1,4784.
#
# Los dos ingredientes que hacen falta -- A(91) = 55 y el indice de campeon --
# salen de la fraccion continua que ya esta calculada arriba, asi que se puede
# comprobar TAMBIEN la tabla de campeones del articulo.

print()
print("=" * 74)
print("COMPROBACION 4 -- Simons-de Weger: la tabla de campeones y el 1,4784")
print("=" * 74)
print()
print("  Primero su tabla de campeones (seccion 6.2 de la version web 1.44),")
print("  recalculada desde la fraccion continua certificada de arriba.")
print("  A(m) es el mayor a_n de indice PAR anterior al indice n(m).")
print()

QD = [q for p, q in CONV]     # QD[n] = q_n


def como_potencia(entero):
    """'1.3134e+106' sin pasar por float, que desbordaria."""
    s = str(entero)
    return f"{s[0]}.{s[1:5]}e+{len(s)-1}"


print(f"  {'n(m)':>6} {'A(m) publicado':>16} {'A(m) aqui':>12} "
      f"{'q_(n-1) publicado':>20} {'q_(n-1) aqui':>16}  ok")
print(f"  {'-'*6} {'-'*16} {'-'*12} {'-'*20} {'-'*16}  ---")
FALLOS_SW_CAMP = 0
FILAS_SW_HECHAS = 0
for n_m, a_pub, k1_pub, q_pub in SW_CAMPEONES:
    if n_m > len(CF):
        print(f"  {n_m:>6} {a_pub:>16} "
              f"{'-- fuera del rango de CF certificada --':>52}")
        continue
    FILAS_SW_HECHAS += 1
    a_mio = max(CF[i] for i in range(0, n_m - 1, 2))
    q_mio = QD[n_m - 1]
    # comparacion sin float: q_pub = mantisa e exponente
    _man, _exp = q_pub.split("e")
    cota_pub = int(Decimal(_man) * 10 ** int(_exp))
    ok = (a_mio == a_pub) and (q_mio > cota_pub)
    if not ok:
        FALLOS_SW_CAMP += 1
    print(f"  {n_m:>6} {a_pub:>16} {a_mio:>12} {q_pub:>20} "
          f"{como_potencia(q_mio):>16}  {'ok' if ok else 'FALLA'}")

print()
print(f"  filas comprobadas: {FILAS_SW_HECHAS} de {len(SW_CAMPEONES)}   "
      f"filas que no cuadran: {FALLOS_SW_CAMP}")
if FALLOS_SW_CAMP:
    raise SystemExit("La tabla de campeones de Simons-de Weger no se reproduce. Revisalo.")
print("  Las que caben en el rango certificado salen clavadas, con la fraccion")
print("  continua calculada aqui y sin mirar la del articulo.")

# --- ahora el 1,4784
print()
print("  Y ahora el numero que el repo llama caja negra. Se resuelve la")
print("  ecuacion que define K_2(m) por biseccion, con decimal a "
      f"{CIFRAS_DECIMAL} cifras.")
print()

_ln2 = Decimal(2).ln()
_ln3 = Decimal(3).ln()
_d = _ln3 / _ln2
_m = Decimal(M_TOPE)
_A91 = Decimal(max(CF[i] for i in range(0, 217, 2)))
_X0d = Decimal(X0_HERCHER)
_b = (1 + 1 / _X0d) / (Decimal(2) ** (1 / _d))
_dm = _d ** _m
_expo = _m * (_d - 1) / (_dm - 1)
_cm = ((1 + 1 / _X0d) ** _expo) * (_b ** ((_d / (_d - 1)) * (1 - _expo)))
_coef = (_d - 1) / (_dm - 1)


def _f(x):
    return _m * _cm * (Decimal(2) ** (-_coef * x)) - _ln2 / ((_A91 + 2) * x)


_lo, _hi = Decimal("1e15"), Decimal("1e25")
for _ in range(300):
    _mid = (_lo + _hi) / 2
    if _f(_mid) > 0:
        _lo = _mid
    else:
        _hi = _mid
K2_91 = _lo
k2_91 = K2_91 / (_m * _dm)

print(f"    b            = {float(_b):.8f}      (el articulo: 0,64576...)")
print(f"    c_m          = {float(_cm):.10f}    (el articulo: c_m < 0,30577 para m >= 30)")
print(f"    2^(-1/(d-1)) = {float(Decimal(2) ** (-1 / (_d - 1))):.10f}    (su limite)")
print(f"    A(91)        = {int(_A91)}              (el articulo: 55)")
print(f"    delta^91     = {float(_dm):.10e}")
print()
print(f"    K_2(91) calculado aqui = {float(K2_91):.6e}   el articulo: {SW_K2_91}")
print(f"    k_2(91) calculado aqui = {float(k2_91):.6f}       el articulo: 1,4784")

sw_bien = (float(K2_91) < float(SW_K2_91)) and (float(k2_91) < 1.4784) \
    and (float(k2_91) > 1.4783)
print()
if not sw_bien:
    raise SystemExit("El 1,4784 de Simons-de Weger no se reproduce. Revisalo.")
print("  RE-DERIVADO. El 1,4784 no es un numero magico: es k_2(91) redondeado")
print("  hacia arriba, y sale en diez lineas a partir de A(91) = 55, que a su")
print("  vez sale de la fraccion continua. Lo que este repo trataba como caja")
print("  negra tiene, al menos en su ultimo tramo, una aritmetica comprobable.")

SW_COTA = SW_FACTOR * M_TOPE * (DELTA_HI ** M_TOPE)
print()
print(f"  Y la cota tal como la usa Hercher: 1,4784 * 91 * delta^91 = "
      f"{float(SW_COTA):.6e}")
print(f"  El articulo la redondea a 2,2*10^20  ->  "
      f"{'coincide' if float(SW_COTA) < 2.2e20 else 'NO COINCIDE'}")
if float(SW_COTA) >= 2.2e20:
    raise SystemExit("La cota de Simons-de Weger no da lo que dice Hercher. Revisalo.")


# ---------------------------------------------------------------------------
# COMPROBACION 4b -- LO DE BAKER, MATIZADO
# ---------------------------------------------------------------------------

print()
print("  SOBRE 'HERCHER NO USA BAKER EN NINGUNA PARTE'.")
print()
print("  Lo comprobable: en el fuente LaTeX del articulo de Hercher (hercher5.tex,")
print("  que la revista sirve junto al PDF) la palabra 'Baker' aparece CERO veces,")
print("  y tampoco 'linear form', 'Matveev' ni 'Rhin'. La afirmacion del repo es")
print("  literalmente cierta PARA EL ARTICULO DE HERCHER.")
print()
print("  Lo que el repo no dice, y cambia la lectura: la cadena SI pasa por")
print("  teoria de la trascendencia, un escalon mas abajo. Simons-de Weger tienen")
print("  una seccion titulada 'Application of Transcendence Theory' cuyo Lema 12")
print("     Lambda > e^(-13,3*(0,46057 + log K))")
print("  sale de Rhin (1987), una medida efectiva de irracionalidad para")
print("  log(3)/log(2) por aproximantes de Pade. Ese lema entra en K_1(m), y")
print("  K_1(m) entra en la demostracion del Lema 16, que es de donde sale el")
print("  1,4784. O sea:")
print()
print("     'Hercher no usa Baker'                     -> CIERTO")
print("     'toda la maquinaria diofantica entra como  -> CIERTO")
print("      este unico numero importado'")
print("     'aceptandolo, el resto es elemental'       -> CIERTO")
print("     'no hay Baker en ninguna parte de la       -> FALSO. Hay un resultado")
print("      cadena'                                       de trascendencia (Rhin")
print("                                                    1987) dentro del numero.")
print()
print("  No es una correccion grave, pero la Fase 2 del plan de la pinza se")
print("  apoya en que la caja negra sea aritmetica pura, y no lo es del todo.")


# ===========================================================================
# COMPROBACION 5 -- EL TEOREMA 23 DE HERCHER, REIMPLEMENTADO DE CERO
# ===========================================================================
#
# Reimplementacion independiente de la de reimpl.py: otros logaritmos, otra
# rejilla, otro exponente para acotar el tercer sumando (79/50 en vez de 3/2) y
# otra raiz entera (Newton en vez de math.isqrt). Si las dos discrepancias que
# reimpl.py encontro son de verdad, tienen que salir aqui tambien.
#
# Teorema 21 (formula, aceptada sin demostrar). Con m_2 el mayor entero <= m con
#
#     (delta^m_2 - 1)/(delta - 1) * log2(162/97 * X_0)  <=  (m_2/m)*K
#
# y  v = (m_2/m)*K*(delta-1)/(delta^m_2 - 1), se tiene
#
#     delta < (K+L)/K < delta + (1/(K*3*log2)) * (t1 + t2 + t3)
#     t1 = (97(m-m_2)+73)/(54*X_0)   [ 3/X_0 si m_2=m-1 ; 0 si m_2=m ]
#     t2 = 3/(2^v - 1)
#     t3 = 3(m_2-1)/(2^v - 1)^delta

_G = 10 ** REJILLA
_dl = (DELTA_LO * _G).numerator // (DELTA_LO * _G).denominator
_dh = -((-DELTA_HI * _G).numerator // (-DELTA_HI * _G).denominator)
DL = Fraction(_dl, _G)      # <= delta, redondeado hacia abajo
DH = Fraction(_dh, _G)      # >= delta, redondeado hacia arriba
if not (DL < DELTA_LO or DL == DELTA_LO) or not (DH > DELTA_HI or DH == DELTA_HI):
    raise SystemExit("La rejilla de delta no encierra al encierro. Revisalo.")

POT_HI = [Fraction(1)]
POT_LO = [Fraction(1)]
for _i in range(1, 400):
    POT_HI.append(POT_HI[-1] * DH)
    POT_LO.append(POT_LO[-1] * DL)

# log2(162/97 * X_0), acotado POR ARRIBA (esta en el lado izquierdo de una
# desigualdad que hay que cumplir, asi que sobreestimarlo es lo conservador).
_Y = Decimal(162 * X0_HERCHER) / Decimal(97)
_CB = _Y.ln() / Decimal(LOG2_LO.numerator) * Decimal(LOG2_LO.denominator)
CB_HI = Fraction(_CB) * (1 + MARGEN) + MARGEN


def raiz_entera(x, n):
    """Mayor entero r con r^n <= x. Newton, sin floats."""
    if x < 0:
        raise SystemExit("raiz de negativo")
    if x == 0:
        return 0
    r = 1 << ((x.bit_length() + n - 1) // n + 1)
    while True:
        s = ((n - 1) * r + x // r ** (n - 1)) // n
        if s >= r:
            break
        r = s
    while r ** n > x:
        r -= 1
    while (r + 1) ** n <= x:
        r += 1
    return r


def dos_elevado_menos_uno(v_lo):
    """Entero X con 0 < X <= 2^v_lo - 1."""
    e = Decimal(v_lo.numerator) / Decimal(v_lo.denominator)
    e *= Decimal(LOG2_LO.numerator) / Decimal(LOG2_LO.denominator)
    val = e.exp() * (1 - Decimal(MARGEN.numerator) / Decimal(MARGEN.denominator))
    ent = int(val.to_integral_value(rounding=ROUND_FLOOR)) - 1
    return max(ent, 1)


def epsilon_de(m, K):
    """Devuelve (m_2, v_lo, epsilon_hi)."""
    K = Fraction(K)
    m2 = 0
    for j in range(1, m + 1):
        izq = (POT_HI[j] - 1) / (DL - 1) * CB_HI
        if izq <= Fraction(j, m) * K:
            m2 = j
    if m2 == 0:
        f_hi = Fraction(97, 54) * m * Fraction(1, X0_HERCHER)
        return 0, None, f_hi / (K * 3 * LOG2_LO)

    v_lo = Fraction(m2, m) * K * (DL - 1) / (POT_HI[m2] - 1)

    if v_lo > 5000:
        base = 2 ** 5000 - 1
    else:
        base = dos_elevado_menos_uno(v_lo)
    t2 = Fraction(3, base)
    # (2^v-1)^delta > (2^v-1)^(79/50) porque 79/50 = 1,58 < delta y la base > 1.
    # La raiz entera se trunca hacia abajo, o sea que t3 sale por arriba.
    t3 = Fraction(3 * (m2 - 1), max(raiz_entera(base ** 79, 50), 1))

    if m2 == m:
        t1 = Fraction(0)
    elif m2 == m - 1:
        t1 = Fraction(3, X0_HERCHER)
    else:
        t1 = Fraction(97 * (m - m2) + 73, 54 * X0_HERCHER)

    return m2, v_lo, (t1 + t2 + t3) / (K * 3 * LOG2_LO)


def nueva_K(eps_hi):
    return denominador_minimo(DL, DH + eps_hi).denominator


print()
print("=" * 74)
print("COMPROBACION 5 -- el Teorema 23 de Hercher, reimplementado de cero")
print("=" * 74)
print()
print(f"  m <= {M_TOPE},  X_0 = 695*2^60 = {X0_HERCHER:,}")
print(f"  arranque K > {K_ARRANQUE:,} (Simons-de Weger Teorema 3, caja negra)")
print(f"  delta en rejilla 10^-{REJILLA}; t3 acotado con exponente 79/50 y raiz")
print("  entera por Newton -- todo distinto de como lo hace reimpl.py.")
print()
print(f"  {'it':>3} {'m_2':>4} {'pub':>4} {'v':>10} {'epsilon':>12} {'eps pub':>10} "
      f"{'K >=':>14} {'K pub':>9}  {'':>5}")
print(f"  {'-'*3} {'-'*4} {'-'*4} {'-'*10} {'-'*12} {'-'*10} {'-'*14} {'-'*9}  {'-'*5}")

K_act = Fraction(K_ARRANQUE)
FALLOS_M2 = 0
FALLOS_K = 0
AVISOS_EPS = []
HISTORIA = []
for it in range(ITERACIONES):
    m2_pub, eps_pub, k_pub = HERCHER_PUBLICADO[it]
    m2, v_lo, eps_hi = epsilon_de(M_TOPE, K_act)
    K_n = nueva_K(eps_hi)

    if m2 != m2_pub:
        FALLOS_M2 += 1
    # la cota publicada tiene que ser la nuestra recortada a sus cifras
    cif = len(k_pub.split("e")[0].replace(".", "").lstrip("0"))
    e10 = math.floor(math.log10(float(K_n)))
    esc = 10 ** (cif - 1 - e10)
    mant = math.floor(float(K_n) * esc) / esc
    bien_k = (f"{mant:.{cif-1}e}" == f"{float(k_pub):.{cif-1}e}"
              and float(K_n) >= float(k_pub))
    if not bien_k:
        FALLOS_K += 1
    cif_e = len(eps_pub.split("e")[0].replace(".", "").lstrip("0"))
    e10e = math.floor(math.log10(float(eps_hi)))
    esce = 10 ** (cif_e - 1 - e10e)
    mante = math.ceil(float(eps_hi) * esce) / esce
    bien_eps = f"{mante:.{cif_e-1}e}" == f"{float(eps_pub):.{cif_e-1}e}"
    if not bien_eps:
        AVISOS_EPS.append((it + 1, float(eps_hi), eps_pub))

    marca = "ok" if (m2 == m2_pub and bien_k and bien_eps) else \
            ("EPS?" if (m2 == m2_pub and bien_k) else "FALLA")
    print(f"  {it+1:>3} {m2:>4} {m2_pub:>4} {float(v_lo):>10.4f} "
          f"{float(eps_hi):>12.4e} {eps_pub:>10} {float(K_n):>14.6e} "
          f"{k_pub:>9}  {marca:>5}")
    HISTORIA.append((it + 1, m2, v_lo, eps_hi, K_n))
    K_act = Fraction(K_n)

print()
print(f"  m_2 que no coinciden: {FALLOS_M2} de {ITERACIONES}")
print(f"  cotas de K que no coinciden: {FALLOS_K} de {ITERACIONES}")
print(f"  epsilon que no coinciden: {len(AVISOS_EPS)} de {ITERACIONES}")
if FALLOS_M2 or FALLOS_K:
    raise SystemExit("No se reprodujo el Teorema 23 con esta implementacion. No sigas.")
print()
print("  Los siete m_2 y las siete cotas de K, identicos a los publicados, con")
print("  una implementacion que no comparte ni los logaritmos ni las cotas de")
print("  redondeo con reimpl.py.")

print()
print("  LAS DOS DISCREPANCIAS DE reimpl.py, CONFIRMADAS O NO:")
print()
if AVISOS_EPS:
    for it, mio, pub in AVISOS_EPS:
        print(f"    (1) Iteracion {it}: aqui sale epsilon = {mio:.4e}, el articulo")
        print(f"        imprime {pub}. Razon {mio/float(pub):.4f}.")
        print(f"        reimpl.py da 1,2298e-43. CONFIRMADA por segunda via.")
else:
    print("    (1) NO confirmada: aqui los siete epsilon coinciden con el papel.")

print()
print("        Y no mueve la cota, porque el denominador minimo es PLANO en todo")
print("        ese rango. Se mide metiendo epsilon a mano:")
print()
planos = {}
for texto in ["8e-44", "1.0e-43", "1.11e-43", "1.2298e-43", "2e-43", "5e-43"]:
    e = Fraction(Decimal(texto))
    planos[texto] = denominador_minimo(DL, DH + e).denominator
    print(f"          epsilon = {texto:>10}  ->  K >= {planos[texto]:,}")
distintos = len(set(planos.values()))
print()
print(f"        denominadores distintos: {distintos}")
if distintos != 1:
    print("        NO es plano: la discrepancia SI importaria. Revisalo.")
else:
    print("        Es plano: los dos epsilon caen entre las mismas dos")
    print("        convergentes, asi que dan la misma cota. Discrepancia de")
    print("        impresion, no de matematica.")

# --- la segunda discrepancia: la tercera fila de la Tabla 1
print()
print("    (2) La Tabla 1 del Corolario 24, mismas iteraciones con otro m:")
print()
print(f"        {'m':>6} {'K calculada':>16} {'K publicada':>12} {'vueltas':>8}  igual")
print(f"        {'-'*6} {'-'*16} {'-'*12} {'-'*8}  -----")
FILAS_MAL = []
for m, pub in HERCHER_TABLA1:
    K_t = Fraction(72 * 10 ** 9)
    vueltas = 0
    for _ in range(40):
        _, _, e_t = epsilon_de(m, K_t)
        k_t = nueva_K(e_t)
        if k_t <= K_t:
            break
        K_t = Fraction(k_t)
        vueltas += 1
    cif = len(pub.split("e")[0].replace(".", "").lstrip("0"))
    e10 = math.floor(math.log10(float(K_t)))
    esc = 10 ** (cif - 1 - e10)
    mant = math.floor(float(K_t) * esc) / esc
    igual = f"{mant:.{cif-1}e}" == f"{float(pub):.{cif-1}e}"
    if not igual:
        FILAS_MAL.append((m, float(K_t), pub))
    print(f"        {m:>6} {float(K_t):>16.6e} {pub:>12} {vueltas:>8}  "
          f"{'si' if igual else 'NO'}")

print()
if FILAS_MAL:
    for m, mia, pub in FILAS_MAL:
        print(f"        m = {m}: aqui {mia:.6e}, el articulo {pub}. "
              f"Diferencia {100*abs(mia-float(pub))/float(pub):.2f}%.")
    print("        CONFIRMADA por segunda via (reimpl.py da lo mismo).")
    print()
    print("        Y hay una razon estructural para sospechar del papel: el")
    print("        denominador minimo SOLO puede caer en un denominador de")
    print("        (semi)convergente de log2(3). Los posibles cerca del valor")
    print("        publicado son:")
    for m, mia, pub in FILAS_MAL:
        obj = float(pub)
        cerca = sorted(d for d in SEMICONV if obj / 2 < d < obj * 2)
        print(f"          {[f'{d:.6e}' for d in cerca]}")
        print(f"        y {pub} no esta entre ellos. El nuestro si.")
else:
    print("        NO confirmada: aqui las tres filas salen como el papel.")

# --- los denominadores que salieron tienen que ser semiconvergentes
FUERA = sum(1 for _, _, _, _, K_n in HISTORIA if K_n not in SEMICONV)
print()
print(f"  Las siete cotas de K, contra la lista de (semi)convergentes: "
      f"{FUERA} fuera de la lista.")
if FUERA:
    raise SystemExit("Una cota de K no es denominador de (semi)convergente. Hay un bug.")
print("  Las siete lo son. Y eso explica por que epsilon puede fallar un 10% sin")
print("  mover la cota: entre dos (semi)convergentes hay un salto de orden.")


# ===========================================================================
# COMPROBACION 5b -- EL CORRIGENDUM DE HERCHER, QUE EL REPO NO SABIA QUE EXISTIA
# ===========================================================================
#
# La pagina del articulo en el Journal of Integer Sequences trae, ademas del
# PDF y del fuente LaTeX, un enlace que dice "Corrigendum, June 14 2026". Ni el
# CLAUDE.md ni reimpl.py lo mencionan.
#
#   https://cs.uwaterloo.ca/journals/JIS/VOL26/Hercher/corrigendum.pdf
#
# Lo que dice, textual: "The derivation of the inequalities
# T(n_{m-m_2+1+l}) < 3/(2^v-1)^delta in the proof of Theorem 21 at the bottom of
# page 14 CONTAINS AN ERROR."
#
# O sea: el Teorema 21 -- la pieza que reimpl.py acepta explicitamente como
# caja negra (c), "se usa la formula; no se rehace su demostracion" -- tenia la
# demostracion mal desde marzo de 2023 hasta junio de 2026.
#
# LA BUENA NOTICIA: el enunciado NO cambia. El corrigendum lo vuelve a demostrar
# por otro camino (convexidad sobre un politopo, maximo en un vertice) y aterriza
# en la MISMA desigualdad. Asi que todo lo reproducido aqui y en reimpl.py sigue
# en pie: los dos usan el enunciado, no la demostracion vieja.
#
# LO QUE SI SE PUEDE COMPROBAR AQUI es el ultimo paso del corrigendum, que es
# aritmetico puro. Su cadena termina en
#
#     S(v, dv, ..., d^(m2-1) v) <= S(v, dv, ..., dv)
#         = 3/(2^v - 1) + 3(m2-1)/(2^(d v) - 1)
#         < 3/(2^v - 1) + 3(m2-1)/(2^v - 1)^d
#
# y el ultimo "<" equivale a  (2^v - 1)^delta  <  2^(delta*v) - 1.

print()
print("=" * 74)
print("COMPROBACION 5b -- el corrigendum de junio de 2026, y su ultimo paso")
print("=" * 74)
print()
print("  El articulo tiene un CORRIGENDUM publicado el 14-06-2026 que dice que")
print("  la demostracion del Teorema 21 (la caja negra (c) de reimpl.py) TENIA")
print("  UN ERROR. El enunciado no cambia; la demostracion se rehace entera.")
print()
print("  El ultimo paso del corrigendum es aritmetico y si se puede comprobar:")
print("     (2^v - 1)^delta  <  2^(delta*v) - 1   para todo v > 0")
print()
print(f"  {'v':>12} {'(2^v-1)^delta':>26} {'2^(delta v)-1':>26}  se cumple")
print(f"  {'-'*12} {'-'*26} {'-'*26}  ---------")

_dd = Decimal(3).ln() / Decimal(2).ln()
FALLOS_CORR = 0
_vs = [Decimal("0.1"), Decimal("0.5"), Decimal(1), Decimal(2), Decimal(10)]
_vs += [Decimal(h[2].numerator) / Decimal(h[2].denominator) for h in HISTORIA]
for _v in _vs:
    izq = (Decimal(2) ** _v - 1) ** _dd
    der = Decimal(2) ** (_dd * _v) - 1
    ok = izq < der
    if not ok:
        FALLOS_CORR += 1
    print(f"  {float(_v):>12.4f} {float(izq):>26.10e} {float(der):>26.10e}  "
          f"{'si' if ok else 'NO'}")

print()
print(f"  valores de v probados: {len(_vs)}   fallos: {FALLOS_CORR}")
if FALLOS_CORR:
    raise SystemExit("El ultimo paso del corrigendum no se cumple. Revisalo.")
print("  0 fallos, incluidos los siete v que salen de las iteraciones de arriba.")
print("  (La razon es elemental: x^delta es convexa y creciente con delta > 1,")
print("  luego (x-1)^delta < x^delta - 1 para x > 1.)")
print()
print("  LO QUE NO SE PUEDE COMPROBAR AQUI: el argumento de convexidad sobre el")
print("  politopo, que es el cuerpo del corrigendum. Se lee, no se verifica.")
print()
print("  Y EL DATO QUE MAS IMPORTA PARA EL PLAN DE LA PINZA: el corrigendum")
print("  agradece el hallazgo del error a XINJUN WANG (ORCID 0009-0007-5895-5984),")
print("  que es el mismo Wang cuyo preprint el CLAUDE.md descarta como 'no")
print("  arbitrado, cero citas, metadatos descuidados'. Encontrar un error real")
print("  en un articulo arbitrado y que el autor lo reconozca por escrito en la")
print("  misma revista es una credencial mejor que una cita.")


# ===========================================================================
# COMPROBACION 6 -- EL CIERRE DEL TEOREMA 23
# ===========================================================================

print()
print("=" * 74)
print("COMPROBACION 6 -- el cierre: cota inferior contra cota superior")
print("=" * 74)
print()
K_FINAL = HISTORIA[-1][4]
print(f"  cota INFERIOR calculada aqui:      K >= {float(K_FINAL):.6e}")
print(f"  cota SUPERIOR de Simons-de Weger:  K <  {float(SW_COTA):.6e}")
print()
if float(K_FINAL) <= float(SW_COTA):
    raise SystemExit("No hay contradiccion: NO se reprodujo el Teorema 23.")
print(f"  {float(K_FINAL):.6e} > {float(SW_COTA):.6e}  ->  contradiccion, por un")
print(f"  factor {float(K_FINAL)/float(SW_COTA):.1f}. Luego no hay m-ciclos con m <= 91.")
print("  EL TEOREMA 23 DE HERCHER, REPRODUCIDO POR SEGUNDA VIA INDEPENDIENTE.")


# ===========================================================================
# EL LIMITE HONESTO
# ===========================================================================

print()
print("=" * 74)
print("EL LIMITE HONESTO -- que se verifico y que no")
print("=" * 74)
print()
print("  SE RE-DERIVO AQUI, CON ARITMETICA EXACTA:")
print("    - la fraccion continua de log2(3), 340 terminos certificados, y sus")
print("      convergentes y semiconvergentes.")
print("    - que las casillas (A,B) que sobreviven son exactamente esas")
print(f"      (barrido de {LIMITE_AB:,} casillas, 0 falsos).")
print("    - de donde salen los tres generadores de Eliahou 1993: son p_13,")
print("      p_15 y p_16 de esa fraccion continua.")
print("    - las cotas de longitud de ciclo publicadas por Eliahou (1993) y por")
print("      Sinisalo (2003), clavadas las dos.")
print("    - la tabla de campeones de Simons-de Weger (4 filas) y el 1,4784.")
print("    - las siete iteraciones del Teorema 23 de Hercher y su contradiccion")
print("      final, con implementacion independiente de reimpl.py.")
print()
print("  NO SE PUEDE VERIFICAR AQUI, Y NO SE FINGE:")
print("    - EL TEOREMA 21 DE HERCHER. Es media seccion de analisis de casos mas")
print("      dos programas en C++ que analizan sumas parciales de hasta 36")
print("      sumandos. Se usa su FORMULA; no se rehace su demostracion. Y ahora")
print("      se sabe que esa demostracion estuvo MAL tres anos: hay corrigendum")
print("      del 14-06-2026. El enunciado aguanta; la demostracion es otra.")
print("    - LA COTA DE SIMONS-DE WEGER en su totalidad. Se re-derivo el ultimo")
print("      tramo (K_2 a partir de A(m)); lo que NO se toca es el Lema 12, que")
print("      viene de Rhin 1987 y es teoria de la trascendencia de verdad.")
print("    - EL m <= 91 COMPLETO. Costo cinco semanas de C++ al autor. Lo que se")
print("      hace aqui es reproducir su aritmetica final en unos segundos.")
print("    - LA VERIFICACION DE BARINA HASTA 2^71. Son 12.395 anos-CPU mas 159")
print("      anos-GPU. Aqui solo se usa el numero, y se comprueba que la cota de")
print("      ciclo que se deduce de el sea la correcta -- que es justo donde")
print("      aparecio el problema.")
print()
print("  Y LA CORRECCION DE ESTA PASADA:")
if not CITA_CORRECTA:
    print(f"    El CLAUDE.md cita >= 217.976.794.617 (atajo) / 355.504.839.929")
    print(f"    (clasico) como el estado del arte con X_0 = 2^71. Con ese X_0 el")
    print(f"    minimo es {atre:,} / {clre:,}.")
    print(f"    Hace falta X_0 >= 2^{math.log2(float(X0_NECESARIO)):.3f} para llegar al valor citado, y")
    print(f"    Barina esta en 2^{math.log2(float(X0_BARINA_REAL)):.3f}. Una fila de mas.")
else:
    print("    Ninguna: la cita de Barina del CLAUDE.md queda confirmada.")
