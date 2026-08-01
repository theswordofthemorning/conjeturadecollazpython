# reimpl.py
#
# EL TEOREMA 23 DE HERCHER, REPRODUCIDO DESDE CERO.
#
# Este programa no dibuja nada: solo numeros por stdout. Y es el primero del
# laboratorio que no rederiva algo por su cuenta, sino que REPRODUCE
# MATEMATICA ARBITRADA y la compara, valor a valor, contra lo publicado.
#
# LA FUENTE
#
#   M. Hercher, "There are no Collatz m-cycles with m <= 91",
#   Journal of Integer Sequences 26 (2023), articulo 23.3.5. Acceso abierto.
#   https://cs.uwaterloo.ca/journals/JIS/VOL26/Hercher/hercher5.html
#   (preprint: arXiv:2201.00406)
#
#   Los valores publicados que aparecen mas abajo en la constante PUBLICADO
#   estan copiados de la demostracion del Teorema 23 del fuente LaTeX del
#   articulo (hercher5.tex, lineas 541-563), que la revista sirve junto al PDF.
#
#   Aviso de numeracion: en el articulo los entornos comparten contador, y el
#   "Main Theorem" es el numero 23. Los otros dos que se usan aqui son el
#   Teorema 21 (la desigualdad sobre (K+L)/K) y el Lema 22 (el denominador
#   minimo). Coinciden con la numeracion del preprint.
#
# ---------------------------------------------------------------------------
# QUE SE ACEPTA COMO CAJA NEGRA Y QUE SE CALCULA AQUI
# ---------------------------------------------------------------------------
#
# Esto es lo mas importante del cabecero. Aqui NO se demuestra nada de Hercher:
# se acepta su maquinaria y se rehace su ARITMETICA.
#
# CAJA NEGRA (se cree, no se comprueba):
#
#   (a) LA COTA DIOFANTICA DE SIMONS-DE WEGER:  K < 1,4784 · m · delta^m.
#       Es el unico sitio por donde entra la aproximacion diofantica dura.
#       Arbitrada en Acta Arithmetica 117 (2005) y su version web de 2010.
#       HALLAZGO DEL ESTUDIO PREVIO, y es lo que hace viable este fichero:
#       Hercher NO INVOCA el teorema de Baker en ninguna parte. Toda la
#       maquinaria pesada entra como ESTE UNICO NUMERO importado. Aceptandolo,
#       el resto de la demostracion del Teorema 23 es elemental.
#
#       PRECISION (01-08-2026), y hay que decirla: la frase vale para EL
#       ARTICULO DE HERCHER, no para LA CADENA. Comprobado sobre hercher5.tex:
#       "Baker" 0 veces, "Matveev" 0, "Rhin" 0, "linear form" 0. Pero un
#       escalon mas abajo, Simons-de Weger tienen una seccion titulada
#       "Application of Transcendence Theory" cuyo Lema 12
#            Lambda > e^(-13,3*(0,46057 + log K))
#       sale de RHIN (1987), una medida efectiva de irracionalidad para
#       log(3)/log(2) por aproximantes de Pade. Ese lema entra en K_1(m), que
#       entra en el Lema 16, de donde sale el 1,4784. O sea: la caja negra que
#       se importa SI contiene trascendencia. Redaccion correcta: "Hercher no
#       invoca Baker; la caja negra que importa si la contiene".
#
#       Y LA CAJA NO ES TAN NEGRA (01-08-2026). verificar_ciclos.py [4]
#       re-deriva el 1,4784 en diez lineas desde la propia definicion de
#       Simons-de Weger, resolviendo su ecuacion de K_2(m) por biseccion con
#       decimal a 200 cifras: b = 0,64576012, c_m = 0,3057636284, A(91) = 55,
#       K_2(91) = 2,140701e20, k_2(91) = 1,478381. El 1,4784 es k_2(91)
#       redondeado hacia arriba. Su tabla de campeones sale clavada en las 4
#       filas que caben en el rango certificado. Lo importado de verdad es el
#       Lema 12, no el numero final.
#
#   (b) EL ARRANQUE:  K > 7·10^11  para m <= 91, del Teorema 3 de la misma
#       version web de Simons-de Weger.
#
#   (c) EL TEOREMA 21 DE HERCHER, la desigualdad
#           delta < (K+L)/K < delta + (1/(K·3·log2)) · (tres sumandos)
#       con sus tres variantes segun m_2 sea m, m-1 o menor. Se usa la formula;
#       no se rehace su demostracion (que ocupa la mitad del articulo).
#
#       OJO: ESE TEOREMA TIENE CORRIGENDUM (localizado el 01-08-2026). La misma
#       revista publico el 14-06-2026 un corrigendum que dice que la
#       demostracion del Teorema 21 "contains an error". El ENUNCIADO NO
#       CAMBIA -la reparacion aterriza en la misma desigualdad-, asi que este
#       fichero sigue valiendo tal cual. Su ultimo paso, (2^v - 1)^delta <
#       2^(delta*v) - 1, se comprueba en verificar_ciclos.py [5b] en 12
#       valores de v, incluidos los siete que salen de las iteraciones de
#       abajo: 0 fallos. Lo que NO se puede comprobar es el argumento de
#       convexidad sobre el politopo, que es el cuerpo del corrigendum.
#
#       Y EL DATO QUE IMPORTA MAS ALLA DE LA MATEMATICA: el corrigendum
#       agradece el hallazgo del error a XINJUN WANG (ORCID
#       0009-0007-5895-5984), el mismo Wang cuyo preprint el CLAUDE.md
#       descartaba por "no arbitrado, cero citas, metadatos descuidados".
#       Encontrar un error real en un articulo arbitrado y que el autor lo
#       reconozca por escrito es mejor credencial que una cita. La Fase 3 del
#       plan de la pinza estaba calibrada sobre una impresion equivocada.
#
#       Y para este fichero hay una lectura directa: la caja negra (c) que
#       aqui se acepta "por estar arbitrada" llevaba TRES ANOS con un error
#       dentro. Estar arbitrado no es estar verificado.
#
#   (d) EL LEMA 22, que dice que el denominador mas chico de todas las
#       fracciones de un intervalo abierto se encuentra por fracciones
#       continuas. Aqui SI se implementa el calculo (algoritmo de Stern-Brocot)
#       y se comprueba contra casos conocidos, pero el enunciado se acepta.
#
#   (e) X_0 = 695 · 2^60, el limite de verificacion por fuerza bruta que
#       Hercher usaba en 2023 (Barina). Es un dato externo.
#
# LO QUE SE CALCULA AQUI, Y ES TODO EL CONTENIDO DEL FICHERO:
#
#   Las SIETE ITERACIONES de la demostracion del Teorema 23. En cada una:
#     1. el mayor m_2 que cumple la premisa del Teorema 21,
#     2. el valor v de ese teorema,
#     3. la cota epsilon con (K+L)/K < delta + epsilon,
#     4. el denominador minimo del intervalo (delta, delta+epsilon), que es
#        una cota inferior NUEVA de K, con la que se vuelve a empezar.
#   Y al final, la comparacion de esa cota contra la caja negra (a): cuando la
#   supera, el m-ciclo no puede existir.
#
# ---------------------------------------------------------------------------
# EL DETALLE DE RIGOR, QUE ES LA RAZON DE QUE ESTO VALGA ALGO
# ---------------------------------------------------------------------------
#
# Con un delta puntual en coma flotante salen los mismos numeros bonitos y no
# demuestran nada, porque el paso decisivo -- el denominador minimo -- es
# hipersensible: mueve delta en la cifra 40 y el denominador cambia de orden.
#
# Asi que aqui NO hay ni un float. El intervalo se ENSANCHA siempre, y todo se
# redondea en la direccion que agranda epsilon:
#
#   - log(2) y log(3) salen de la serie de atanh con el RESTO ACOTADO A MANO,
#     en Fraction. Error garantizado por debajo de 10^-230, demostrado en tres
#     lineas dentro de la funcion, sin llamar a ninguna libreria numerica.
#   - delta = log(3)/log(2) queda encerrado entre dos racionales de una rejilla
#     de 10^-60, con el de abajo redondeado hacia abajo y el de arriba hacia
#     arriba.
#   - el intervalo que se pasa al Lema 22 no es (delta, delta+epsilon) sino
#     (delta_lo, delta_hi + epsilon_hi), que lo CONTIENE. Un intervalo mas
#     ancho solo puede dar un denominador minimo mas chico, o sea una cota de K
#     mas floja. El error cae siempre del lado seguro.
#   - lo unico que pasa por decimal son dos exponenciales (2^v y un logaritmo),
#     a 150 cifras y con un margen de seguridad de 10^-60 restado a mano. El
#     error real de decimal ahi esta 80 ordenes por debajo del margen.
#   - el tercer sumando del Teorema 21 lleva un exponente delta; aqui se acota
#     con el exponente 3/2 (que es menor que delta, o sea que agranda el
#     sumando) y raiz entera exacta. Ese sumando esta diez ordenes por debajo
#     del total, asi que la grosería no cuesta nada y ahorra una potencia
#     irracional.
#
# Es el mismo espiritu que los SystemExit antes de dibujar del resto del repo:
# comprobar antes de afirmar.
#
# ---------------------------------------------------------------------------
# QUE SALIO
# ---------------------------------------------------------------------------
#
# Los siete m_2 y las siete cotas de K salen identicos a los publicados. De los
# siete epsilon salen seis; el septimo nos da 1,23·10^-43 donde el articulo
# imprime 1,11·10^-43. La diferencia no cambia nada y el programa lo demuestra:
# el denominador minimo es PLANO en todo ese rango, asi que las dos cotas dan
# el mismo K. Queda anotado como discrepancia, no se tapa.
#
# LO QUE ESTO NO ES: no es una verificacion formal, no es un arbitraje, y no
# comprueba la parte dificil del articulo (el Teorema 21 y el analisis de casos
# que lo sostiene). Es la aritmetica de la demostracion final, rehecha por
# alguien que no es el autor, con cotas de error declaradas.

import math
from decimal import Decimal, getcontext, ROUND_FLOOR
from fractions import Fraction

# ---------------------------------------------------------------------------
# Cambia esto aqui, guarda, y dale a Ctrl+B en Sublime.
# ---------------------------------------------------------------------------

M_TOPE = 91             # el m del enunciado: "no hay m-ciclos con m <= 91"
K_ARRANQUE = 7 * 10 ** 11   # caja negra (b): Simons-de Weger, Teorema 3
X0 = 695 * 2 ** 60      # caja negra (e): el limite de Barina que uso Hercher
ITERACIONES = 7         # cuantas vueltas da el articulo. Son siete.

TERMINOS_SERIE = 300    # sumandos de atanh. 300 dan error < 10^-230
REJILLA = 60            # delta se encierra en una rejilla de 10^-REJILLA
CIFRAS_DECIMAL = 150    # precision de las dos exponenciales
MARGEN = Fraction(1, 10 ** 60)   # lo que se resta/suma a mano por si acaso

CON_BARRIDO_M = True    # comprobar que m = 91 es el peor caso de todos
CON_TABLA = True        # reproducir tres filas de la Tabla 1 del articulo

getcontext().prec = CIFRAS_DECIMAL

# Los valores que imprime el articulo, copiados a mano del fuente LaTeX.
# Cada fila es (m_2, epsilon, cota de K), y los dos ultimos como texto porque
# es texto lo que hay en el papel: son valores redondeados.
PUBLICADO = [
    (47, "6.9e-32", "5.2e15"),
    (67, "5.1e-36", "3.97e17"),
    (77, "4.1e-38", "4.64e18"),
    (82, "2.3e-39", "2.74e19"),
    (86, "2.3e-40", "7.76e19"),
    (88, "5.3e-41", "2.05e20"),
    (91, "1.11e-43", "7.94e21"),
]

# La cota de Simons-de Weger, tal como la cita Hercher al cerrar la
# demostracion: K < 1,4784 · m · delta^m < 2,2·10^20 para m <= 91.
SW_FACTOR = Fraction(14784, 10000)
SW_PUBLICADO = "2.2e20"

# Las tres primeras filas de la Tabla 1 del articulo (Corolario 24), que segun
# el propio articulo salen del Teorema 21, o sea de esta misma maquinaria.
TABLA_PUBLICADA = [(98, "7.76e19"), (117, "2.74e19"), (276, "4.68e18")]


# ---------------------------------------------------------------------------
# LOGARITMOS CERTIFICADOS, SIN LIBRERIA NUMERICA
# ---------------------------------------------------------------------------
#
# atanh(x) = x + x^3/3 + x^5/5 + ... , todos los sumandos positivos.
# Cortando en N sumandos, lo que falta es
#
#     R = suma_{k>=N} x^(2k+1)/(2k+1)  <  x^(2N+1)/((2N+1)·(1-x^2))
#
# porque a partir de ahi cada sumando es menor que el anterior por x^2. Eso da
# un intervalo racional exacto, sin creerle nada a nadie. Y con
#
#     log(2)   = 2·atanh(1/3)          (porque (1+1/3)/(1-1/3) = 2)
#     log(3/2) = 2·atanh(1/5)          (porque (1+1/5)/(1-1/5) = 3/2)
#     log(3)   = log(2) + log(3/2)
#
# quedan los dos logaritmos que hacen falta.

def atanh_acotado(x, terminos):
    """Devuelve (lo, hi) racionales con lo < atanh(x) < hi."""
    suma = Fraction(0)
    potencia = x
    x2 = x * x
    for k in range(terminos):
        suma += potencia / (2 * k + 1)
        potencia *= x2
    # 'potencia' vale ahora x^(2N+1); el resto que falta es menor que
    # x^(2N+1) / ((2N+1)·(1-x^2))
    resto = potencia / ((2 * terminos + 1) * (1 - x2))
    return suma, suma + resto


_a3_lo, _a3_hi = atanh_acotado(Fraction(1, 3), TERMINOS_SERIE)
_a5_lo, _a5_hi = atanh_acotado(Fraction(1, 5), TERMINOS_SERIE)

LOG2_LO, LOG2_HI = 2 * _a3_lo, 2 * _a3_hi
LOG3_LO = LOG2_LO + 2 * _a5_lo
LOG3_HI = LOG2_HI + 2 * _a5_hi

# el error garantizado de los logaritmos, para poder imprimirlo
ERROR_LOG = max(LOG2_HI - LOG2_LO, LOG3_HI - LOG3_LO)

# delta = log(3)/log(2), encerrado y despues redondeado a la rejilla EN LA
# DIRECCION QUE ENSANCHA: el de abajo hacia abajo, el de arriba hacia arriba.
_G = 10 ** REJILLA
_d_lo_exacto = LOG3_LO / LOG2_HI
_d_hi_exacto = LOG3_HI / LOG2_LO
DELTA_LO = Fraction((_d_lo_exacto * _G).numerator // (_d_lo_exacto * _G).denominator, _G)
DELTA_HI = Fraction(-((-_d_hi_exacto * _G).numerator // (-_d_hi_exacto * _G).denominator), _G)

# potencias de delta, precalculadas. Para acotar por arriba una expresion que
# crece con delta se usa DELTA_HI, y al reves.
POT_HI = [Fraction(1)]
POT_LO = [Fraction(1)]
for _i in range(1, 400):
    POT_HI.append(POT_HI[-1] * DELTA_HI)
    POT_LO.append(POT_LO[-1] * DELTA_LO)

# El logaritmo grande de la premisa del Teorema 21: log2(162/97 · X_0). Aqui
# hace falta una cota POR ARRIBA, porque esta en el lado izquierdo de una
# desigualdad que hay que cumplir. Se calcula con decimal y se le suma el
# margen a mano.
_Y = Decimal(162 * X0) / Decimal(97)
_CB_dec = _Y.ln() / Decimal(LOG2_LO.numerator) * Decimal(LOG2_LO.denominator)
CB_HI = Fraction(_CB_dec) * (1 + MARGEN) + MARGEN


# ---------------------------------------------------------------------------
# COMPROBACION 1 -- el intervalo de delta, contra enteros exactos
# ---------------------------------------------------------------------------
#
# log2(3) es irracional, asi que no se puede comprobar directamente. Pero para
# CUALQUIER fraccion p/q vale la equivalencia exacta, sin un solo redondeo:
#
#     p/q < log2(3)   <=>   2^p < 3^q
#
# y eso son dos enteros que Python compara sin error. Con q pequeño se puede
# hacer de verdad, y sirve para atrapar un delta que estuviera mal de raiz.

print("COMPROBACION 1 -- el intervalo de delta contra enteros exactos\n")
print("  delta = log2(3), acotado por dos racionales de la rejilla 10^-%d." % REJILLA)
print("  Los logaritmos salen de la serie de atanh con el resto acotado a mano:")
print(f"    log(2) en un intervalo de ancho {float(LOG2_HI - LOG2_LO):.3e}")
print(f"    log(3) en un intervalo de ancho {float(LOG3_HI - LOG3_LO):.3e}")
print(f"    o sea error garantizado < {float(ERROR_LOG):.3e}, sin usar libreria.")
print(f"  delta_lo = {float(DELTA_LO):.20f}")
print(f"  delta_hi = {float(DELTA_HI):.20f}")
print(f"  ancho del encierro: {float(DELTA_HI - DELTA_LO):.3e}\n")

print("  Prueba exacta con enteros:  p/q < log2(3)  <=>  2^p < 3^q\n")
print(f"    {'p':>6} {'q':>5} {'2^p < 3^q':>11} {'p/q < delta_lo':>16} "
      f"{'p/q > delta_hi':>16}  coherente?")
print(f"    {'-'*6} {'-'*5} {'-'*11} {'-'*16} {'-'*16}  ---------")

FALLOS_DELTA = 0
for p, q in [(1, 1), (2, 1), (3, 2), (8, 5), (19, 12), (65, 41), (84, 53),
             (485, 306), (1054, 665), (24727, 15601), (50508, 31867)]:
    verdad = 2 ** p < 3 ** q          # o sea: p/q < log2(3), exacto
    debajo = Fraction(p, q) < DELTA_LO
    encima = Fraction(p, q) > DELTA_HI
    # si la fraccion cae fuera del encierro, el encierro tiene que estar del
    # lado correcto; si cae dentro, no se puede exigir nada (y no pasa aqui)
    coherente = (verdad and debajo) or ((not verdad) and encima)
    if not coherente:
        FALLOS_DELTA += 1
    print(f"    {p:>6} {q:>5} {str(verdad):>11} {str(debajo):>16} "
          f"{str(encima):>16}  {'ok' if coherente else 'FALLA'}")

print(f"\n  fracciones probadas: 11   incoherencias: {FALLOS_DELTA}")
if FALLOS_DELTA:
    raise SystemExit("El encierro de delta no coincide con la aritmetica entera. No sigas.")
print("  0 fallos. El encierro de delta es correcto en las once, con enteros puros.")
print("  (son las convergentes de log2(3), las mismas que ya usa pinzaciclos.py)")


# ---------------------------------------------------------------------------
# EL LEMA 22 -- el denominador mas chico de un intervalo abierto
# ---------------------------------------------------------------------------
#
# Hercher lo enuncia con fracciones continuas; el algoritmo equivalente y mas
# corto es el descenso de Stern-Brocot: si hay un entero dentro, ese gana
# (denominador 1); si no, se le quita la parte entera al intervalo, se le da la
# vuelta (que intercambia los extremos) y se repite.

def denominador_minimo(a, b):
    """Fraccion de denominador mas chico ESTRICTAMENTE dentro de (a, b)."""
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


# ---------------------------------------------------------------------------
# COMPROBACION 2 -- el denominador minimo, contra casos que se ven a mano
# ---------------------------------------------------------------------------

print("\n\nCOMPROBACION 2 -- el denominador minimo contra casos conocidos\n")
print("  El Lema 22 se acepta como enunciado, pero el calculo se comprueba.")
print("  Los casos de abajo se pueden verificar a ojo con la serie de Farey.\n")

CASOS = [
    ((Fraction(1, 3), Fraction(1, 2)), Fraction(2, 5)),
    ((Fraction(7, 10), Fraction(8, 10)), Fraction(3, 4)),
    ((Fraction(0), Fraction(1)), Fraction(1, 2)),
    ((Fraction(1), Fraction(3)), Fraction(2)),
    ((Fraction(3, 7), Fraction(4, 7)), Fraction(1, 2)),
    ((Fraction(31, 100), Fraction(32, 100)), Fraction(5, 16)),
    ((Fraction(1, 1000), Fraction(2, 1000)), Fraction(1, 501)),
]
FALLOS_LEMA = 0
for (lo, hi), esperado in CASOS:
    sale = denominador_minimo(lo, hi)
    # ademas de coincidir, tiene que estar DENTRO y ser el minimo de verdad:
    # se comprueba a lo bruto que ningun denominador menor cabe
    dentro = lo < sale < hi
    minimo_real = None
    for q in range(1, sale.denominator + 1):
        p = lo.numerator * q // lo.denominator + 1
        if lo < Fraction(p, q) < hi:
            minimo_real = Fraction(p, q)
            break
    bien = (sale == esperado) and dentro and minimo_real.denominator == sale.denominator
    if not bien:
        FALLOS_LEMA += 1
    print(f"    ({str(lo):>10}, {str(hi):>10})  ->  {str(sale):>10}   "
          f"esperado {str(esperado):>10}   fuerza bruta {str(minimo_real):>10}   "
          f"{'ok' if bien else 'FALLA'}")

print(f"\n  casos probados: {len(CASOS)}   fallos: {FALLOS_LEMA}")
if FALLOS_LEMA:
    raise SystemExit("El calculo del denominador minimo esta mal. No sigas.")
print("  0 fallos, y ademas coincide con la busqueda a lo bruto en los siete.")


# ---------------------------------------------------------------------------
# EL TEOREMA 21 -- una vuelta de la iteracion
# ---------------------------------------------------------------------------
#
# Premisa: el mayor m_2 <= m con
#
#     (delta^m_2 - 1)/(delta - 1) · log2(162/97 · X_0)  <=  (m_2/m)·K
#
# Y entonces, con v = (m_2/m)·K·(delta-1)/(delta^m_2 - 1):
#
#     (K+L)/K  <  delta + (1/(K·3·log2)) · ( t1 + t2 + t3 )
#     t1 = (97(m - m_2) + 73)/(54·X_0)     [ = 3/X_0 si m_2 = m-1; 0 si m_2 = m ]
#     t2 = 3/(2^v - 1)
#     t3 = 3(m_2 - 1)/(2^v - 1)^delta
#
# Todo se acota POR ARRIBA. Como epsilon baja cuando v sube, hace falta una
# cota INFERIOR de v, y para eso delta_lo arriba y delta_hi abajo.

def dos_elevado_a_menos(v_lo):
    """Entero X con 0 < X <= 2^v_lo - 1. La unica exponencial del programa.

    Se calcula exp(v·log2) con decimal a CIFRAS_DECIMAL cifras -- que esta
    correctamente redondeado -- se le quita el MARGEN a mano, se trunca hacia
    abajo y se le resta 1. Cualquiera de esos tres pasos ya bastaria para
    quedarse corto; los tres juntos son un exceso deliberado.
    """
    expo = Decimal(v_lo.numerator) / Decimal(v_lo.denominator)
    expo *= Decimal(LOG2_LO.numerator) / Decimal(LOG2_LO.denominator)
    valor = expo.exp() * (1 - Decimal(MARGEN.numerator) / Decimal(MARGEN.denominator))
    entero = int(valor.to_integral_value(rounding=ROUND_FLOOR)) - 1
    return max(entero, 1)


def una_vuelta(m, K):
    """Devuelve (m_2, v_lo, epsilon_hi, holgura) para un m y una cota K."""
    K = Fraction(K)

    # el mayor m_2 que cumple la premisa. Se sobreestima el lado izquierdo.
    m2 = 0
    holgura = None
    for j in range(1, m + 1):
        izq = (POT_HI[j] - 1) / (DELTA_LO - 1) * CB_HI
        der = Fraction(j, m) * K
        if izq <= der:
            m2 = j
            holgura = float(der / izq)

    if m2 == 0:
        # ningun m_2 sirve: se cae al Corolario 17, que no depende de v
        f_hi = Fraction(97, 54) * m * Fraction(1, X0)
        return 0, None, f_hi / (K * 3 * LOG2_LO), None

    # cota INFERIOR de v: delta_lo arriba, delta_hi abajo
    v_lo = Fraction(m2, m) * K * (DELTA_LO - 1) / (POT_HI[m2] - 1)

    if v_lo > 5000:
        # 2^v es astronomico; se acota a lo bestia y sobra
        base = 2 ** 5000 - 1
        t2 = Fraction(3, base)
        t3 = Fraction(3 * (m2 - 1), base)
    else:
        base = dos_elevado_a_menos(v_lo)
        t2 = Fraction(3, base)
        # (2^v-1)^delta > (2^v-1)^(3/2) porque delta > 3/2 y la base es > 1.
        # Y isqrt(base^3) <= base^(3/2). Los dos redondeos agrandan t3.
        t3 = Fraction(3 * (m2 - 1), math.isqrt(base ** 3))

    if m2 == m:
        t1 = Fraction(0)
    elif m2 == m - 1:
        t1 = Fraction(3, X0)
    else:
        t1 = Fraction(97 * (m - m2) + 73, 54 * X0)

    return m2, v_lo, (t1 + t2 + t3) / (K * 3 * LOG2_LO), holgura


def nueva_cota_de_K(epsilon_hi):
    """El Lema 22 sobre el intervalo ENSANCHADO. Devuelve (fraccion, K)."""
    q = denominador_minimo(DELTA_LO, DELTA_HI + epsilon_hi)
    return q, q.denominator


# ---------------------------------------------------------------------------
# helpers de comparacion contra el papel
# ---------------------------------------------------------------------------

def truncado(x, cifras):
    """El numero x recortado a 'cifras' cifras significativas, hacia abajo."""
    if x == 0:
        return "0"
    e = math.floor(math.log10(x))
    escala = 10 ** (cifras - 1 - e)
    mant = math.floor(x * escala) / escala
    return f"{mant:.{cifras - 1}e}"


def redondeado_arriba(x, cifras):
    """El numero x subido a 'cifras' cifras significativas."""
    e = math.floor(math.log10(x))
    escala = 10 ** (cifras - 1 - e)
    mant = math.ceil(x * escala) / escala
    return f"{mant:.{cifras - 1}e}"


def como_papel(texto):
    """'5.2e15' -> float, para comparar de verdad y no por cadenas."""
    return float(texto)


def cifras_de(texto):
    """Cuantas cifras significativas trae el numero impreso en el papel."""
    return len(texto.split("e")[0].replace(".", "").lstrip("0"))


# ===========================================================================
# LAS SIETE ITERACIONES DEL TEOREMA 23
# ===========================================================================

print("\n\nLAS SIETE ITERACIONES DEL TEOREMA 23, CONTRA LO PUBLICADO\n")
print(f"  m <= {M_TOPE}, X_0 = 695·2^60 = {X0:,}")
print(f"  arranque: K > {K_ARRANQUE:,}  (Simons-de Weger, Teorema 3 -- caja negra)")
print("  Cada vuelta: m_2 -> v -> epsilon -> denominador minimo -> nueva K.\n")

print(f"  {'it':>3} {'m_2':>5} {'m_2 pub':>8} {'v':>10} {'epsilon':>12} "
      f"{'eps pub':>10} {'K >=':>14} {'K pub':>10} {'':>6}")
print(f"  {'-'*3} {'-'*5} {'-'*8} {'-'*10} {'-'*12} {'-'*10} {'-'*14} {'-'*10} {'-'*6}")

K_actual = Fraction(K_ARRANQUE)
FALLOS_M2 = 0
FALLOS_K = 0
AVISOS_EPS = []
HISTORIA = []

for it in range(ITERACIONES):
    m2_pub, eps_pub, k_pub = PUBLICADO[it]
    m2, v_lo, eps_hi, holgura = una_vuelta(M_TOPE, K_actual)
    frac, K_nueva = nueva_cota_de_K(eps_hi)

    # el m_2 tiene que salir clavado
    if m2 != m2_pub:
        FALLOS_M2 += 1
    # la cota de K: la publicada es la nuestra recortada a sus cifras
    mia = float(K_nueva)
    bien_k = (truncado(mia, cifras_de(k_pub)) == f"{como_papel(k_pub):.{cifras_de(k_pub)-1}e}"
              and mia >= como_papel(k_pub))
    if not bien_k:
        FALLOS_K += 1
    # el epsilon: la publicada deberia ser la nuestra subida a sus cifras
    e = float(eps_hi)
    bien_eps = redondeado_arriba(e, cifras_de(eps_pub)) == \
        f"{como_papel(eps_pub):.{cifras_de(eps_pub)-1}e}"
    if not bien_eps:
        AVISOS_EPS.append((it + 1, e, eps_pub))

    marca = "ok" if (m2 == m2_pub and bien_k and bien_eps) else \
            ("EPS?" if (m2 == m2_pub and bien_k) else "FALLA")
    vt = "-" if v_lo is None else f"{float(v_lo):.4f}"
    print(f"  {it+1:>3} {m2:>5} {m2_pub:>8} {vt:>10} {e:>12.4e} {eps_pub:>10} "
          f"{mia:>14.6e} {k_pub:>10} {marca:>6}")

    HISTORIA.append((it + 1, m2, v_lo, eps_hi, K_nueva, holgura))
    K_actual = Fraction(K_nueva)

print(f"\n  m_2 que no coinciden con el articulo: {FALLOS_M2} de {ITERACIONES}")
print(f"  cotas de K que no coinciden:          {FALLOS_K} de {ITERACIONES}")
print(f"  epsilon que no coinciden:             {len(AVISOS_EPS)} de {ITERACIONES}")

if FALLOS_M2:
    raise SystemExit("Los m_2 no reproducen los del articulo. No se reprodujo el Teorema 23.")
if FALLOS_K:
    raise SystemExit("Las cotas de K no reproducen las del articulo. No sigas.")

print("\n  LOS SIETE m_2 Y LAS SIETE COTAS DE K SALEN IDENTICOS A LOS PUBLICADOS.")
print("  Cada cota publicada es exactamente la nuestra recortada a sus cifras:")
for it, m2, v_lo, eps_hi, K_n, _ in HISTORIA:
    print(f"    it {it}:  {float(K_n):.10e}   ->  el articulo imprime {PUBLICADO[it-1][2]}")

# --- la holgura de la decision de m_2, que es un entero y conviene mirar

print("\n  Cuanto margen tiene la eleccion de m_2 (es una decision entera, y si")
print("  el margen fuera del tamano del error de redondeo no valdria nada):\n")
print(f"    {'it':>3} {'m_2':>5} {'derecha/izquierda en la premisa':>34}")
for it, m2, v_lo, eps_hi, K_n, holgura in HISTORIA:
    h = "-" if holgura is None else f"{holgura:.6f}"
    print(f"    {it:>3} {m2:>5} {h:>34}")
print("\n    Todas por encima de 1 con margen de varias cifras, contra un error")
print(f"    de redondeo de {float(MARGEN):.0e}. La decision no esta en el filo.")


# ===========================================================================
# LA DISCREPANCIA DEL SEPTIMO EPSILON, SIN TAPARLA
# ===========================================================================

print("\n\nLA DISCREPANCIA, Y POR QUE NO CAMBIA NADA\n")

if AVISOS_EPS:
    for it, mio, pub in AVISOS_EPS:
        print(f"  Iteracion {it}: aqui sale epsilon = {mio:.4e} y el articulo")
        print(f"  imprime {pub}. La razon es {mio/como_papel(pub):.4f}.")
    print("\n  El nuestro es MAS GRANDE, o sea mas conservador: da un intervalo mas")
    print("  ancho y por tanto una cota de K mas floja o igual. Aun asi la cota")
    print("  sale identica, y la razon es que el denominador minimo es PLANO en")
    print("  todo ese rango. Se comprueba metiendo epsilon a mano:\n")
    print(f"    {'epsilon metido':>18} {'denominador minimo':>24}")
    print(f"    {'-'*18} {'-'*24}")
    planos = set()
    for texto in ["8e-44", "1.0e-43", "1.11e-43", "1.2298e-43", "2e-43", "5e-43"]:
        e = Fraction(Decimal(texto))
        d = denominador_minimo(DELTA_LO, DELTA_HI + e).denominator
        planos.add(d)
        print(f"    {texto:>18} {d:>24,}")
    print(f"\n  denominadores distintos que salen: {len(planos)}")
    if len(planos) != 1:
        print("  NO es plano: entonces la discrepancia SI importaria. Revisalo.")
    else:
        print("  Es plano: los dos epsilon caen entre las mismas dos convergentes")
        print("  de log2(3), asi que dan la misma cota. La discrepancia es de")
        print("  impresion, no de matematica. (Y el 1,11 del articulo trae tres")
        print("  cifras cuando los otros seis traen dos, lo que apunta a un desliz")
        print("  de transcripcion mas que a otro calculo.)")
else:
    print("  No hubo ninguna: los siete epsilon coinciden.")


# ===========================================================================
# EL BARRIDO DE m -- el enunciado es "para TODO m <= 91"
# ===========================================================================
#
# La demostracion del articulo se escribe para el caso peor, pero la cota tiene
# que valer para todos los m a la vez. Aqui se rehace la cadena entera tomando
# en cada vuelta el m que da la cota MAS FLOJA de los 91.

if CON_BARRIDO_M:
    print("\n\nEL BARRIDO DE m -- que la cadena valga para los 91 a la vez\n")
    print("  En cada vuelta se prueban los 91 valores de m y se toma el peor,")
    print("  o sea el que da el denominador minimo mas chico.\n")
    print(f"  {'it':>3} {'peor m':>8} {'K del peor':>16} {'K con m=91':>16}  igual?")
    print(f"  {'-'*3} {'-'*8} {'-'*16} {'-'*16}  ------")

    K_b = Fraction(K_ARRANQUE)
    DESACUERDOS = 0
    for it in range(ITERACIONES):
        peor = None
        for m in range(1, M_TOPE + 1):
            _, _, e_m, _ = una_vuelta(m, K_b)
            _, k_m = nueva_cota_de_K(e_m)
            if peor is None or k_m < peor[1]:
                peor = (m, k_m)
        _, _, e91, _ = una_vuelta(M_TOPE, K_b)
        _, k91 = nueva_cota_de_K(e91)
        igual = peor[1] == k91
        if not igual:
            DESACUERDOS += 1
        print(f"  {it+1:>3} {peor[0]:>8} {float(peor[1]):>16.6e} "
              f"{float(k91):>16.6e}  {'si' if igual else 'NO'}")
        K_b = Fraction(peor[1])

    print(f"\n  vueltas en que el peor m da una cota distinta de la de m=91: "
          f"{DESACUERDOS}")
    if DESACUERDOS:
        raise SystemExit("La cadena de m=91 no cubre a todos los m <= 91. Cuidado.")
    print("  La cadena de m = 91 vale para los 91 valores a la vez: aunque el m")
    print("  que maximiza epsilon cambia de vuelta en vuelta, el denominador")
    print("  minimo cae siempre en la misma convergente. El enunciado 'para todo")
    print("  m <= 91' queda cubierto.")


# ===========================================================================
# EL CIERRE: LA CAJA NEGRA DE SIMONS-DE WEGER
# ===========================================================================

print("\n\nEL CIERRE -- contra la cota importada de Simons-de Weger\n")

K_FINAL = HISTORIA[-1][4]
SW = SW_FACTOR * M_TOPE * POT_HI[M_TOPE]     # cota superior, con delta_hi
sw_ok = float(SW) < como_papel(SW_PUBLICADO)

print(f"  CAJA NEGRA (a):  K < 1,4784 · m · delta^m")
print(f"    con m = {M_TOPE} y delta acotado por arriba:  K < {float(SW):.6e}")
print(f"    el articulo lo redondea a  K < {SW_PUBLICADO}   ->  "
      f"{'coincide' if sw_ok else 'NO COINCIDE'}")
if not sw_ok:
    raise SystemExit("La cota de Simons-de Weger no da lo que dice el articulo. Revisalo.")

print(f"\n  CALCULADO AQUI:  K >= {float(K_FINAL):.6e}   (el articulo: 7.94e21)")
print(f"\n  {float(K_FINAL):.6e}  >  {float(SW):.6e}   ->  contradiccion.")

if float(K_FINAL) <= float(SW):
    raise SystemExit("No hay contradiccion: NO se reprodujo el Teorema 23.")

print(f"\n  La cota inferior supera a la superior por un factor "
      f"{float(K_FINAL) / float(SW):.1f}.")
print("  Luego no existe ningun m-ciclo de Collatz con m <= 91.")
print("  QUE ES EXACTAMENTE EL TEOREMA 23 DE HERCHER (2023), REPRODUCIDO.")


# ===========================================================================
# LAS FILAS DE LA TABLA 1 (Corolario 24)
# ===========================================================================
#
# El articulo dice que las tres primeras filas de su Tabla 1 salen del
# Teorema 21, o sea de esta misma maquinaria pero con otro m y sin tope. Se
# itera hasta que la cota deja de mejorar.

if CON_TABLA:
    print("\n\nLAS TRES PRIMERAS FILAS DE LA TABLA 1 (Corolario 24)\n")
    print("  Misma maquinaria, otro m, iterando hasta que la cota se estanca.\n")
    print(f"  {'m':>6} {'K calculada':>16} {'K publicada':>12} {'vueltas':>8}  igual?")
    print(f"  {'-'*6} {'-'*16} {'-'*12} {'-'*8}  ------")

    FILAS_OK = 0
    FILAS_MAL = []
    for m, pub in TABLA_PUBLICADA:
        K_t = Fraction(72 * 10 ** 9)      # la cota general K > 7,2·10^10
        vueltas = 0
        for _ in range(40):
            _, _, e_t, _ = una_vuelta(m, K_t)
            _, k_t = nueva_cota_de_K(e_t)
            if k_t <= K_t:
                break
            K_t = Fraction(k_t)
            vueltas += 1
        mia = float(K_t)
        igual = truncado(mia, cifras_de(pub)) == f"{como_papel(pub):.{cifras_de(pub)-1}e}"
        if igual:
            FILAS_OK += 1
        else:
            FILAS_MAL.append((m, mia, pub))
        print(f"  {m:>6} {mia:>16.6e} {pub:>12} {vueltas:>8}  "
              f"{'si' if igual else 'NO'}")

    print(f"\n  filas reproducidas: {FILAS_OK} de {len(TABLA_PUBLICADA)}")
    for m, mia, pub in FILAS_MAL:
        print(f"\n  NO REPRODUCIDA: m = {m}. Aqui sale {mia:.6e}, el articulo")
        print(f"  imprime {pub}. La diferencia es del "
              f"{100*abs(mia-como_papel(pub))/como_papel(pub):.2f}%.")
        print("  Y hay una razon para sospechar del papel y no del calculo: el")
        print("  denominador minimo solo puede caer en un denominador de")
        print("  convergente o semiconvergente de log2(3), y ese valor no lo es.")


# --- los denominadores que salieron, contra las convergentes de log2(3)

print("\n\nLOS DENOMINADORES QUE SALEN SON CONVERGENTES DE log2(3)\n")
print("  El denominador minimo de un intervalo pegado a delta tiene que ser")
print("  denominador de una convergente o semiconvergente de delta. Si no lo")
print("  fuera, habria un error en el descenso. Se comprueba con la fraccion")
print("  continua calculada aparte, a partir del encierro racional de delta.\n")

# fraccion continua de delta, solo mientras los dos extremos coincidan
cf = []
a, b = DELTA_LO, DELTA_HI
for _ in range(200):
    ia = a.numerator // a.denominator
    ib = b.numerator // b.denominator
    if ia != ib:
        break
    cf.append(ia)
    if a - ia == 0 or b - ib == 0:
        break
    a, b = 1 / (b - ib), 1 / (a - ia)

DENOM = set()
h2, h1, k2, k1 = 0, 1, 1, 0
for termino in cf:
    for j in range(1, termino + 1):
        DENOM.add(j * k1 + k2)
    h2, h1, k2, k1 = h1, termino * h1 + h2, k1, termino * k1 + k2

print(f"  terminos de la fraccion continua que el encierro determina: {len(cf)}")
print(f"  {cf[:24]} ...")
print(f"  denominadores de convergente/semiconvergente listados: {len(DENOM):,}\n")

FUERA = 0
for it, m2, v_lo, eps_hi, K_n, _ in HISTORIA:
    esta = K_n in DENOM
    if not esta:
        FUERA += 1
    print(f"    it {it}:  K = {K_n:>24,}   "
          f"{'es semiconvergente' if esta else 'NO ESTA EN LA LISTA'}")

print(f"\n  cotas que no son denominador de una (semi)convergente: {FUERA}")
if FUERA:
    raise SystemExit("Una cota no cae en una convergente de log2(3). Hay un bug.")
print("  Las siete lo son. Y de paso: eso explica por que epsilon puede fallar")
print("  un 10% sin mover la cota -- entre dos convergentes consecutivas hay un")
print("  salto de orden de magnitud, y epsilon solo decide en cual de las dos")
print("  se cae.")

if CON_TABLA and FILAS_MAL:
    print("\n  Y con la misma lista se puede contestar a la fila que no cuadra:")
    for m, mia, pub in FILAS_MAL:
        objetivo = como_papel(pub)
        cercanos = sorted(d for d in DENOM
                          if objetivo / 2 < d < objetivo * 2)
        print(f"    m = {m}: los denominadores posibles cerca de {pub} son")
        print(f"      {[f'{d:.6e}' for d in cercanos]}")
        print(f"    y {pub} no esta entre ellos, asi que ese valor NO es")
        print("    alcanzable por este metodo. El nuestro si lo es.")


# ===========================================================================
# LA COTA DE ERROR QUE SE GARANTIZA
# ===========================================================================

print("\n\nLA COTA DE ERROR QUE SE GARANTIZA\n")
print("  Esto es lo que separa un numero bonito de una comprobacion:\n")
print(f"  1. log(2) y log(3) salen de la serie de atanh con {TERMINOS_SERIE} sumandos y")
print(f"     el resto acotado a mano en Fraction. Error < {float(ERROR_LOG):.3e}.")
print("     No interviene ninguna libreria numerica: es una suma de racionales.")
print(f"  2. delta queda encerrado entre dos racionales de la rejilla 10^-{REJILLA},")
print(f"     con ancho {float(DELTA_HI - DELTA_LO):.3e}, y el encierro se comprueba contra")
print("     aritmetica entera pura (comprobacion 1).")
print("  3. El intervalo que va al Lema 22 no es (delta, delta+eps) sino")
print("     (delta_lo, delta_hi + eps_hi), que lo CONTIENE. Ensanchar solo puede")
print("     bajar el denominador minimo, o sea debilitar la cota de K. Nunca")
print("     inflarla.")
print(f"  4. Las dos exponenciales van con decimal a {CIFRAS_DECIMAL} cifras y se les resta")
print(f"     un margen de {float(MARGEN):.0e} a mano. El error real de decimal ahi esta")
print("     unas 80 potencias de diez por debajo de ese margen.")
print("  5. El sumando t3 se acota con exponente 3/2 en vez de delta y con raiz")
print("     entera exacta, o sea por arriba y sin potencias irracionales.")
print("\n  Consecuencia: la cota final K >= " + f"{float(K_FINAL):.6e}" + " es valida aunque")
print("  todos los redondeos hubieran salido en contra a la vez.")


# ===========================================================================
# EL LIMITE HONESTO
# ===========================================================================

print("\n\nEL LIMITE HONESTO -- que se reprodujo y que no\n")
print("  SE REPRODUJO:")
print("    - los siete m_2 de la demostracion del Teorema 23: 47, 67, 77, 82,")
print("      86, 88, 91. Identicos.")
print("    - las siete cotas inferiores de K. Identicas hasta las cifras que")
print("      el articulo imprime.")
print("    - la cota de Simons-de Weger evaluada en m = 91, y la contradiccion")
print("      final que cierra el teorema.")
print("    - dos de las tres primeras filas de la Tabla 1.")
print("\n  NO SE REPRODUJO:")
print("    - el septimo epsilon (sale 1,23e-43 contra el 1,11e-43 impreso). No")
print("      mueve la cota, y el programa lo demuestra midiendo que el")
print("      denominador minimo es plano en ese rango.")
print("    - la tercera fila de la Tabla 1 (sale 4,64e18 contra 4,68e18). El")
print("      4,68e18 no es denominador de ninguna semiconvergente de log2(3),")
print("      asi que no es alcanzable por este metodo.")
print("\n  LAS DOS, CONFIRMADAS POR SEGUNDA VIA (01-08-2026). verificar_ciclos.py")
print("  rehace las siete iteraciones sin compartir ni los logaritmos ni las")
print("  cotas de redondeo con este fichero -rejilla 10^-80, t3 con exponente")
print("  79/50, raiz entera por Newton- y da NUMEROS IDENTICOS: eps_7 =")
print("  1,2298e-43 y m=276 -> 4,640282e18. Los siete m_2 y las siete cotas de")
print("  K coinciden con lo publicado, 0 de 7 fuera. Cuando una segunda")
print("  implementacion independiente da tu numero, y el del papel no puede")
print("  salir del metodo del papel, la carga de la prueba cambia de lado.")
print("  Ninguna de las dos mueve la conclusion del articulo.")
print("\n  Y LO QUE NO SE INTENTO SIQUIERA, que es la mitad dificil del articulo:")
print("    - el Teorema 21 y toda la cadena de cotas sobre las sumas de T(n_i)")
print("      que lo sostienen (Seccion 3 entera, mas un programa en C++ que")
print("      analiza sumas parciales de hasta 36 sumandos).")
print("    - la cota de Simons-de Weger, que es donde vive la aproximacion")
print("      diofantica de verdad.")
print("  Sin esas dos piezas esto no es una verificacion del articulo: es la")
print("  reproduccion de su aritmetica final, que es la parte que se puede")
print("  comprobar en cinco segundos y la que nadie suele volver a mirar.")
print("\n  Aun asi, es lo primero que hace este repo que no es rederivacion")
print("  propia: los numeros de la izquierda salen de aqui y los de la derecha")
print("  de una revista arbitrada, y hay que decidir si coinciden.")
