# verificar_constantes.py
#
# RE-DERIVACION INDEPENDIENTE DE LAS CONSTANTES Y LOS NUMEROS IMPORTADOS:
# ROOSENDAAL, WAGON, LAS CONSTANTES DE PARADA, A076227 Y LA CRIBA DE BARINA.
#
# ---------------------------------------------------------------------------
# POR QUE EXISTE ESTE FICHERO
# ---------------------------------------------------------------------------
#
# El repo cita numeros de otra gente y los da por buenos porque tienen autor.
# Eso ya fallo dos veces (la cita Wu-Huang sin DOI; la cota de periodo minimo
# once veces mas debil que el estado del arte). Aqui se vuelve a derivar CADA
# numero con codigo propio y aritmetica EXACTA, y donde no se puede, se dice.
#
# La distincion que manda, y que se imprime en cada bloque:
#
#     COTA        -> tiene forma de teorema. Vale "para todo n". Sirve.
#     PROMEDIO    -> mide una poblacion. No decide ningun caso individual.
#     CONSTRUCCION-> es cierto por como se definio. Verdadero, pero vacio.
#
# ---------------------------------------------------------------------------
# QUE SE COMPRUEBA, Y DE QUIEN ES CADA COSA
# ---------------------------------------------------------------------------
#
# 1. EL RESIDUO DE ROOSENDAAL.  Res(n) = 2^B / (3^A * n), donde A es cuantas
#    veces se aplico 3n+1 y B cuantas veces n/2 en el camino completo de n
#    hasta 1. Eric Roosendaal (ericr.nl) lo verifico para todo x < 2^32 y
#    conjeturo que Res(993) = 1,253142144 es el maximo absoluto.
#    Aqui: valor EXACTO como fraccion, y barrido propio.
#
# 2. LA CONSTANTE DE WAGON.  Stan Wagon, "The Collatz problem", Math.
#    Intelligencer 7 (1985) 72-76. Es el "dropping time" MEDIO: el numero
#    medio de pasos del mapa CLASICO que tarda un n IMPAR en bajar por debajo
#    de si mismo. OEIS le da entrada propia: A122790.
#    Aqui: se recalcula desde cero por programacion dinamica exacta sobre
#    vectores de paridad, sin muestrear ni un solo numero.
#
# 3. LAS CONSTANTES DE PARADA k / ln(4/3).  Literatura clasica (Lagarias).
#    Son PREDICCIONES HEURISTICAS, no teoremas. La escalera 1:2:3 segun se
#    cuenten los 3n+1, los pasos del atajo o los clasicos.
#    Aqui: se miden con DOS estimadores distintos, porque dan cosas distintas
#    y el CLAUDE.md no dice cual uso.
#
# 4. A076227 de OEIS, "Number of surviving Collatz residues mod 2^n".
#    Aqui: DP propia contra los terminos OFICIALES del b-file de OEIS (no
#    contra la lista que ya estaba copiada en descensoresto.py, que seria
#    circular).
#
# 5. LA CRIBA DE BARINA y la afirmacion estructural del repo de que "T^k es
#    una BIYECCION sobre Z/2^k y por eso una criba no sirve para ciclos".
#    Esa frase sostiene una decision estrategica del laboratorio, asi que se
#    comprueba literalmente. (Aviso: el resultado de esta comprobacion es la
#    parte mas interesante del fichero.)
#
# ---------------------------------------------------------------------------
# LO QUE NO SE PUEDE COMPROBAR AQUI, Y SE DICE EN VEZ DE FINGIRLO
# ---------------------------------------------------------------------------
#
# - La verificacion de Barina hasta 2^71 (12.395 anos-CPU + 159 anos-GPU).
#   Ni de lejos.
# - El numero 85.234.595 de supervivientes de su criba de produccion
#   h2esieve-34: sale de un fichero binario suyo que no esta aqui.
# - El factor 5/9 de su criba 3^2. Se reconstruye el nivel 3^1 (que si es
#   elemental y se demuestra en una linea) y se dice hasta donde se llego.
#
# ---------------------------------------------------------------------------
# COSTE MEDIDO EN ESTA MAQUINA
# ---------------------------------------------------------------------------
#
#   tablas (A,B) hasta 10^6 ......... ~2 s
#   barrido exacto del residuo ...... ~1 s
#   DP de paridades hasta k=2200 .... ~3 s
#   biyeccion de Terras hasta k=16 .. ~2 s
#   total ........................... menos de 15 s

import math
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60      # decimales declarados, solo para IMPRIMIR

# ---------------------------------------------------------------------------
# Cambia esto aqui, guarda, y dale a Ctrl+B en Sublime.
# ---------------------------------------------------------------------------

LIMITE_RES = 1000000      # barrido exacto del residuo de Roosendaal
LIMITE_PASOS = 1000000    # barrido de las constantes de parada
K_DP = 2200               # profundidad de la DP de vectores de paridad
K_BIYECCION = 16          # hasta que k se comprueba la biyeccion de Terras
LIMITE_CRIBA3 = 300000    # hasta donde se comprueba la regla n = 2 (mod 3)

CHECKPOINTS_WAGON = (400, 800, 1400, 2200)   # donde se mira la convergencia


# ---------------------------------------------------------------------------
# LOS NUMEROS PUBLICADOS. Copiados de la fuente, no del repo.
# ---------------------------------------------------------------------------

# ericr.nl / Roosendaal: el maximo conjeturado del residuo.
RES_993_PUBLICADO = "1.253142144"

# OEIS A122790, "Decimal expansion of Wagon's constant: the average
# 'dropping time' of the Collatz (3x+1) iteration". Digitos %S %T %U.
WAGON_A122790 = (
    "9.47795555655927473691668101258904194228187160442729971592744235"
    "666701532216248281775610685655731040264443"
)

# OEIS A076227, b-file oficial (b076227.txt), terminos n = 0 .. 44.
A076227_BFILE = [
    1, 1, 1, 2, 3, 4, 8, 13, 19, 38, 64, 128, 226, 367, 734, 1295, 2114,
    4228, 7495, 14990, 27328, 46611, 93222, 168807, 286581, 573162,
    1037374, 1762293, 3524586, 6385637, 12771274, 23642078, 41347483,
    82694966, 151917636, 263841377, 527682754, 967378591, 1934757182,
    3611535862, 6402835000, 12805670000, 23711865322, 41700700058,
    83401400116,
]

# Y cuatro terminos lejanos del mismo b-file, para que la comprobacion no
# se quede en el arranque facil.
A076227_LEJOS = {
    100: int("302560669500543257546172187"),
    200: int("4917911213247274697935031643998322726370567793471092895"),
    300: int("11135880098690424213129728622173052925298656766202286650937829"
             "0558038512175289008981"),
    500: int("87021278249897937515360373875149190908779415905852926972014983"
             "38000873914819707896528508441058590542274973938064125947122838"
             "0960815303168471"),
    1000: int("31094384746079684782981629718825888421487141017283418602460320"
              "57365961263961391042518719744303505630118461099830704515428391"
              "17228211758720952805849503419114810907745670118805553712690183"
              "62292555490193731201037196515421754987255615169829927871708148"
              "87207411401660931766283129358801166"),
}

# Los tres insumos del factor X ~ 363 del CLAUDE.md.
BARINA_H2ESIEVE_34 = 85234595     # NO verificable aqui: sale de su fichero
BARINA_FACTOR_3 = Fraction(5, 9)  # NO verificable aqui: es su regla R5/R6


print("=" * 74)
print("VERIFICACION INDEPENDIENTE: ROOSENDAAL, WAGON, PARADA, A076227, BARINA")
print("=" * 74)
print()
print(f"  LIMITE_RES = {LIMITE_RES:,}   LIMITE_PASOS = {LIMITE_PASOS:,}")
print(f"  K_DP = {K_DP}   K_BIYECCION = {K_BIYECCION}")
print()


# ===========================================================================
# LAS TABLAS (A, B) HASTA EL LIMITE. Aritmetica entera pura.
# ===========================================================================
#
# A(n) = veces que se aplica 3n+1 en el camino de n hasta 1
# B(n) = veces que se aplica n/2
# Se construyen de abajo arriba: se camina desde n hasta caer por debajo de n,
# y ahi ya esta resuelto. El coste total es la suma de los tiempos de descenso,
# que de media son ~5 pasos, asi que es lineal de verdad.

TOPE = max(LIMITE_RES, LIMITE_PASOS)

tabla_A = [0] * (TOPE + 1)
tabla_B = [0] * (TOPE + 1)
for n in range(2, TOPE + 1):
    x = n
    a = 0
    b = 0
    while x >= n:
        if x & 1:
            x = 3 * x + 1
            a += 1
        else:
            x >>= 1
            b += 1
    tabla_A[n] = a + tabla_A[x]
    tabla_B[n] = b + tabla_B[x]

# Control barato: recalcular unos cuantos a pelo, sin la tabla.
def ab_a_pelo(n):
    a = 0
    b = 0
    x = n
    while x != 1:
        if x & 1:
            x = 3 * x + 1
            a += 1
        else:
            x >>= 1
            b += 1
    return a, b

fallos_tabla = 0
for n in (2, 3, 27, 97, 221, 993, 1276, 6171, 77031, 837799, 999999):
    if n <= TOPE and ab_a_pelo(n) != (tabla_A[n], tabla_B[n]):
        fallos_tabla += 1
if fallos_tabla:
    raise SystemExit("La tabla (A,B) no coincide con el calculo a pelo.")

POT2 = [1] * (max(tabla_B) + 2)
for i in range(1, len(POT2)):
    POT2[i] = POT2[i - 1] * 2
POT3 = [1] * (max(tabla_A) + 2)
for i in range(1, len(POT3)):
    POT3[i] = POT3[i - 1] * 3


# ===========================================================================
# COMPROBACION 1 -- EL RESIDUO DE ROOSENDAAL EN 993, EXACTO
# ===========================================================================

print("=" * 74)
print("COMPROBACION 1 -- Res(993), exacto, sin un solo float")
print("=" * 74)
print()

A993, B993 = ab_a_pelo(993)
print(f"  trayectoria de 993 recalculada: A = {A993}, B = {B993}"
      f"  (retraso {A993 + B993})")
if (A993, B993) != (32, 61):
    raise SystemExit("993 no da (A,B) = (32,61). Algo esta mal en el mapa.")

res993 = Fraction(2 ** B993, 3 ** A993 * 993)
print(f"  Res(993) = 2^{B993} / (3^{A993} * 993)")
print(f"           = {res993.numerator} / {res993.denominator}")
print(f"           = {Decimal(res993.numerator) / Decimal(res993.denominator)}")
print()

# El valor publicado, redondeado a las cifras que publica Roosendaal.
d = Decimal(res993.numerator) / Decimal(res993.denominator)
redondeado = str(+d.quantize(Decimal("1.000000000")))
print(f"  publicado por Roosendaal : {RES_993_PUBLICADO}")
print(f"  calculado y redondeado   : {redondeado}")
if redondeado != RES_993_PUBLICADO:
    raise SystemExit("Res(993) no reproduce el valor publicado. Para y dilo.")
print("  -> coinciden en las nueve cifras decimales publicadas.")
print()

# Los dobles tienen el mismo residuo, exacto.
iguales = True
for j in range(0, 23):
    m = 993 * 2 ** j
    a, b = ab_a_pelo(m)
    if Fraction(2 ** b, 3 ** a * m) != res993:
        iguales = False
print(f"  993 * 2^j para j = 0..22 (incluye 4.164.943.872 = 993 * 2^22):")
print(f"  todos con el mismo residuo exacto: {iguales}")
if not iguales:
    raise SystemExit("Doblar cambia el residuo. Eso seria un bug gordo.")
print()


# ===========================================================================
# COMPROBACION 2 -- Res >= 1 SIEMPRE, Y DONDE SE ALCANZA LA IGUALDAD
# ===========================================================================

print("=" * 74)
print("COMPROBACION 2 -- la cota Res >= 1, con enteros y en todo el barrido")
print("=" * 74)
print()
print("  Enunciado: para todo n que llegue a 1, 2^B - 3^A * n >= 0.")
print("  Ese entero es la C de la identidad de Terras del repo, y por eso")
print("  la cota se demuestra en una linea: C se construye sumando terminos")
print("  no negativos, luego 2^B = 3^A * n + C >= 3^A * n.")
print()

bajo_uno = 0
igual_uno = []
for n in range(2, LIMITE_RES + 1):
    c = POT2[tabla_B[n]] - POT3[tabla_A[n]] * n
    if c < 0:
        bajo_uno += 1
    elif c == 0:
        igual_uno.append(n)

print(f"  n barridos: 2 .. {LIMITE_RES:,}")
print(f"  con Res < 1 (o sea C < 0): {bajo_uno}")
if bajo_uno:
    raise SystemExit("Hay residuos por debajo de 1. La cota se cae.")
print(f"  con Res = 1 exacto (C = 0): {len(igual_uno)} -> {igual_uno[:8]} ...")

potencias = [2 ** j for j in range(1, 64) if 2 ** j <= LIMITE_RES]
if igual_uno != potencias:
    raise SystemExit("La igualdad Res = 1 no cae exactamente en las"
                     " potencias de 2.")
print("  -> la igualdad se alcanza EXACTAMENTE en las potencias de 2, en")
print("     todas y solo en ellas. Fuera de ahi la desigualdad es estricta.")
print()

# El maximo exacto del barrido. Primero se acorta con floats y despues se
# decide con enteros, que es lo unico que vale.
L2 = math.log(2.0)
L3 = math.log(3.0)
mejor = -1.0
for n in range(2, LIMITE_RES + 1):
    e = tabla_B[n] * L2 - tabla_A[n] * L3 - math.log(n)
    if e > mejor:
        mejor = e
candidatos = [n for n in range(2, LIMITE_RES + 1)
              if tabla_B[n] * L2 - tabla_A[n] * L3 - math.log(n) > mejor - 1e-9]

# Comparacion exacta entre candidatos: Res(p) > Res(q) sii
# 2^Bp * 3^Aq * q  >  2^Bq * 3^Ap * p
campeon = candidatos[0]
for n in candidatos[1:]:
    izq = POT2[tabla_B[n]] * POT3[tabla_A[campeon]] * campeon
    der = POT2[tabla_B[campeon]] * POT3[tabla_A[n]] * n
    if izq > der:
        campeon = n
empatados = []
for n in candidatos:
    izq = POT2[tabla_B[n]] * POT3[tabla_A[campeon]] * campeon
    der = POT2[tabla_B[campeon]] * POT3[tabla_A[n]] * n
    if izq == der:
        empatados.append(n)

res_max = Fraction(POT2[tabla_B[campeon]], POT3[tabla_A[campeon]] * campeon)
print(f"  candidatos al maximo (cribados con float): {len(candidatos)}")
print(f"  maximo EXACTO del barrido: Res = "
      f"{Decimal(res_max.numerator) / Decimal(res_max.denominator)}")
print(f"  se alcanza en: {empatados}")
if res_max != res993:
    raise SystemExit("El maximo del barrido no es el de 993.")
print("  -> es exactamente el mismo racional que Res(993). El maximo de")
print(f"     Roosendaal aguanta hasta {LIMITE_RES:,}.")
print()
print("  COTA (Res >= 1): demostrada, no solo medida. PERO es condicional a")
print("  que n llegue a 1, o sea que da por supuesta la conjetura para n.")
print("  Sobre un hipotetico n que no terminara, no dice absolutamente nada.")
print("  COTA SUPERIOR (Res <= 1,2531...): conjetura de Roosendaal, sin")
print("  demostracion. Verificada por el, no demostrada por nadie.")
print()


# ===========================================================================
# LA DP DE VECTORES DE PARIDAD -- la maquinaria de las comprobaciones 3 y 4
# ===========================================================================
#
# Mapa del atajo:  T(n) = n/2 si par, (3n+1)/2 si impar.
# Un vector de paridad de longitud k "sobrevive" si en ningun paso j <= k
# el producto de factores 3/2 y 1/2 ha bajado de 1, o sea si 3^S_j > 2^j
# para todo j, donde S_j = cuantos unos lleva el vector.
# Se cuentan los vectores por programacion dinamica sobre (j, S), con
# enteros exactos. Es codigo propio: no mira descensoresto.py.

smin = [0] * (K_DP + 2)
_s = 0
for _j in range(1, K_DP + 2):
    while 3 ** _s <= 2 ** _j:
        _s += 1
    smin[_j] = _s

vivos = {0: 1}
a076227 = [1]
# acumuladores del tiempo de descenso, exactos: numerador por nivel
num_sigma = [0] * (K_DP + 1)      # suma de (cuenta * sigma) en el nivel j
num_clasico = [0] * (K_DP + 1)    # suma de (cuenta * (sigma + impares))
for j in range(1, K_DP + 1):
    nuevo = {}
    for s, c in vivos.items():
        for bit in (0, 1):
            s2 = s + bit
            if s2 >= smin[j]:
                nuevo[s2] = nuevo.get(s2, 0) + c
            else:
                num_sigma[j] += c * j
                num_clasico[j] += c * (j + s2)
    vivos = nuevo
    a076227.append(sum(vivos.values()))


# ===========================================================================
# COMPROBACION 3 -- A076227 CONTRA EL B-FILE OFICIAL DE OEIS
# ===========================================================================

print("=" * 74)
print("COMPROBACION 3 -- A076227 propia contra el b-file oficial de OEIS")
print("=" * 74)
print()

fallos_3 = [(k, A076227_BFILE[k], a076227[k])
            for k in range(len(A076227_BFILE)) if A076227_BFILE[k] != a076227[k]]
print(f"  terminos n = 0..{len(A076227_BFILE) - 1} comparados: "
      f"{len(A076227_BFILE)}   discrepancias: {len(fallos_3)}")
if fallos_3:
    for k, pub, mio in fallos_3[:5]:
        print(f"    n = {k}: OEIS {pub}, calculado {mio}")
    raise SystemExit("No reproduzco A076227. Hay un bug.")

fallos_lejos = []
for k, valor in sorted(A076227_LEJOS.items()):
    if k <= K_DP:
        ok = (a076227[k] == valor)
        print(f"  n = {k:>5}: {len(str(valor)):>4} cifras   coincide: {ok}")
        if not ok:
            fallos_lejos.append(k)
if fallos_lejos:
    raise SystemExit(f"A076227 falla en los terminos lejanos {fallos_lejos}.")
print()
print("  -> los 45 primeros terminos MAS los cuatro lejanos salen identicos.")
print(f"     a(34) = {a076227[34]:,}, que es la criba clasica que cita el")
print(f"     CLAUDE.md: {100.0 * a076227[34] / 2 ** 34:.3f}% de los restos,")
print(f"     o sea 1 de cada {2 ** 34 / a076227[34]:.1f}.")
print()

# Control: la DP cuenta PALABRAS. Que eso sea igual a contar CLASES DE RESTO
# es el teorema de Terras, y se comprueba cribando restos de verdad.
print("  Control (esto es Terras, no una definicion): cribar los restos de")
print("  verdad tiene que dar el mismo numero que contar palabras.")
fallos_criba = 0
for k in range(1, 15):
    vivos_reales = 0
    for r in range(2 ** k):
        x = r
        s = 0
        sobrevive = True
        for j in range(1, k + 1):
            if x & 1:
                x = (3 * x + 1) >> 1
                s += 1
            else:
                x >>= 1
            if s < smin[j]:
                sobrevive = False
                break
        if sobrevive:
            vivos_reales += 1
    if vivos_reales != a076227[k]:
        fallos_criba += 1
print(f"  k = 1..14 cribados sobre restos reales: {fallos_criba} discrepancias")
if fallos_criba:
    raise SystemExit("Contar palabras no es lo mismo que contar restos.")
print()


# ===========================================================================
# COMPROBACION 4 -- LA CONSTANTE DE WAGON
# ===========================================================================

print("=" * 74)
print("COMPROBACION 4 -- la constante de Wagon contra OEIS A122790")
print("=" * 74)
print()
print("  Definicion (A060445 de OEIS lo dice igual): el 'dropping time' es")
print("  el numero de pasos del mapa CLASICO que tarda un n IMPAR en llegar")
print("  por debajo de si mismo. Wagon es su media.")
print()
print("  Como se calcula aqui, sin muestrear un solo entero: cada vector de")
print("  paridad que muere en el paso j aporta peso 1/2^j, tiempo de atajo j")
print("  y tiempo clasico j + (unos del vector). Los pares mueren en j = 1,")
print("  asi que condicionar a impar es dividir entre 1/2 el resto.")
print()

print("      K    media atajo (todos)     WAGON = media clasica (impares)")
print("  -----  ---------------------  --------------------------------")
digitos_ok = 0
for K in CHECKPOINTS_WAGON:
    if K > K_DP:
        continue
    tot_s = sum(num_sigma[j] * 2 ** (K - j) for j in range(1, K + 1))
    tot_c = sum(num_clasico[j] * 2 ** (K - j) for j in range(1, K + 1))
    media_atajo = Decimal(tot_s) / Decimal(2 ** K)
    media_clas = Decimal(tot_c) / Decimal(2 ** K)
    wagon = 2 * media_clas - 1
    s_wagon = str(wagon)
    n_ok = 0
    for ca, cb in zip(s_wagon, WAGON_A122790):
        if ca != cb:
            break
        n_ok += 1
    digitos_ok = max(digitos_ok, n_ok)
    print(f"  {K:>5}  {str(media_atajo)[:21]:>21}  {s_wagon[:32]:>32}")

print()
print(f"  OEIS A122790 : {WAGON_A122790[:44]}...")
print(f"  caracteres iniciales que coinciden (incluido el punto): "
      f"{digitos_ok}")
if digitos_ok < 20:
    raise SystemExit("No reproduzco la constante de Wagon a 20 cifras.")
print("  -> reproducida por un camino que no es el de OEIS (ellos suman")
print("     A122437*A100982/2^(A020914-1); aqui es una DP sobre paridades).")
print()
print("  La otra constante del CLAUDE.md, 3,4926518521864, es la media del")
print("  tiempo de descenso en el mapa del ATAJO sobre TODOS los n. Sale de")
print("  la misma DP (columna de la izquierda).")
print()
print("  Y un regalo de la maquinaria: la media de pasos impares dentro de la")
print("  ventana de descenso es EXACTAMENTE la mitad de la media de pasos.")
K = CHECKPOINTS_WAGON[-1]
tot_s = sum(num_sigma[j] * 2 ** (K - j) for j in range(1, K + 1))
tot_c = sum(num_clasico[j] * 2 ** (K - j) for j in range(1, K + 1))
media_impares = Decimal(tot_c - tot_s) / Decimal(2 ** K)
media_atajo = Decimal(tot_s) / Decimal(2 ** K)
print(f"  media de pasos (atajo)  = {str(media_atajo)[:20]}")
print(f"  media de pasos impares  = {str(media_impares)[:20]}")
print(f"  el doble de la segunda  = {str(2 * media_impares)[:20]}")
print("  Es el teorema del paro opcional de Doob: bajo la biyeccion de Terras")
print("  los bits de paridad son monedas justas y sigma es un tiempo de paro,")
print("  luego E[unos] = E[sigma]/2. No es coincidencia numerica.")
print()
print("  PROMEDIO. Wagon mide una poblacion. No decide ningun n concreto.")
print("  Para la formula del cuarto camino no sirve, y el repo ya lo sabia.")
print()


# ===========================================================================
# COMPROBACION 5 -- LAS CONSTANTES DE PARADA k / ln(4/3)
# ===========================================================================

print("=" * 74)
print("COMPROBACION 5 -- la escalera 1:2:3 de k/ln(4/3), con DOS estimadores")
print("=" * 74)
print()

c1 = 1.0 / math.log(4.0 / 3.0)
print(f"  teorico   impares (3n+1)  1/ln(4/3) = {c1:.6f}")
print(f"  teorico   pasos del ATAJO 2/ln(4/3) = {2 * c1:.6f}")
print(f"  teorico   pasos CLASICOS  3/ln(4/3) = {3 * c1:.6f}")
print()
print("  Recordatorio de contabilidad, que es donde el repo se equivoco una")
print("  vez: pasos del atajo = B, pasos clasicos = A + B, impares = A.")
print()
print("  ESTIMADOR 1, el agregado  suma(pasos) / suma(ln n):")
print()
print("        hasta        A/ln n     B/ln n   (A+B)/ln n        B/A")
print("  -----------  ------------  ---------  -----------  ---------")
suma_a = 0
suma_b = 0
suma_l = 0.0
marcas = [m for m in (10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7)
          if m <= LIMITE_PASOS]
for n in range(2, LIMITE_PASOS + 1):
    suma_a += tabla_A[n]
    suma_b += tabla_B[n]
    suma_l += math.log(n)
    if n in marcas:
        print(f"  {n:>11,}  {suma_a / suma_l:>12.5f}  {suma_b / suma_l:>9.5f}"
              f"  {(suma_a + suma_b) / suma_l:>11.5f}"
              f"  {suma_b / suma_a:>9.6f}")
print()
print("  ESTIMADOR 2, la pendiente de la recta de regresion contra ln n")
print("  (que es lo correcto si hay un termino aditivo constante, y lo hay):")
print()


def pendiente(valor):
    sx = sy = sxx = sxy = 0.0
    cuenta = 0
    for m in range(3, LIMITE_PASOS + 1):
        x = math.log(m)
        y = float(valor(m))
        sx += x
        sy += y
        sxx += x * x
        sxy += x * y
        cuenta += 1
    pend = (cuenta * sxy - sx * sy) / (cuenta * sxx - sx * sx)
    inter = (sy - pend * sx) / cuenta
    return pend, inter


print("            magnitud    pendiente   intercepto   teorico   error")
print("  ------------------  -----------  -----------  --------  ------")
filas = (("A   (impares)", lambda m: tabla_A[m], c1),
         ("B   (atajo)", lambda m: tabla_B[m], 2 * c1),
         ("A+B (clasicos)", lambda m: tabla_A[m] + tabla_B[m], 3 * c1))
pendientes = {}
for nombre, f, teo in filas:
    p, i = pendiente(f)
    pendientes[nombre] = p
    print(f"  {nombre:>18}  {p:>11.5f}  {i:>11.3f}  {teo:>8.5f}"
          f"  {100 * (p - teo) / teo:>+5.2f}%")
print()
print("  La escalera 1:2:3 sale con la PENDIENTE:")
pa = pendientes["A   (impares)"]
pb = pendientes["B   (atajo)"]
pc = pendientes["A+B (clasicos)"]
print(f"    B/A del ajuste     = {pb / pa:.4f}   (teorico 2)")
print(f"    (A+B)/A del ajuste = {pc / pa:.4f}   (teorico 3)")
print(f"  y NO sale con el agregado: alli B/A = {suma_b / suma_a:.6f}.")
print("  Los dos estan bien medidos: el agregado arrastra el intercepto, que")
print("  es del orden de -1,7 pasos y solo se diluye como 1/ln n.")
print()
print("  PROMEDIO, y ademas CONJETURAL: k/ln(4/3) no es un teorema, es la")
print("  prediccion heuristica del modelo de moneda. No sirve para la formula.")
print()


# ===========================================================================
# COMPROBACION 6 -- LA BIYECCION DE TERRAS, LITERALMENTE
# ===========================================================================

print("=" * 74)
print("COMPROBACION 6 -- 'T^k es una biyeccion sobre Z/2^k'. Al pie de la letra")
print("=" * 74)
print()
print("  Esta frase del CLAUDE.md sostiene una decision estrategica (que una")
print("  criba no puede servir para buscar ciclos), asi que se comprueba tal")
print("  y como esta escrita, y por separado la version correcta del teorema.")
print()


def atajo(x):
    return (3 * x + 1) >> 1 if x & 1 else x >> 1


print("  (a) El VECTOR DE PARIDAD depende solo del resto modulo 2^k:")
fallos_a = 0
for k in range(1, K_BIYECCION + 1):
    mod = 1 << k
    for r in range(mod):
        v1 = []
        x = r
        for _ in range(k):
            v1.append(x & 1)
            x = atajo(x)
        v2 = []
        x = r + mod
        for _ in range(k):
            v2.append(x & 1)
            x = atajo(x)
        if v1 != v2:
            fallos_a += 1
            break
print(f"      k = 1..{K_BIYECCION}: {fallos_a} fallos")
if fallos_a:
    raise SystemExit("El vector de paridad no esta bien definido mod 2^k.")

print("  (b) Y la aplicacion resto -> vector de paridad es BIYECTIVA:")
fallos_b = []
for k in range(1, K_BIYECCION + 1):
    mod = 1 << k
    vistos = set()
    for r in range(mod):
        v = 0
        x = r
        for j in range(k):
            v |= (x & 1) << j
            x = atajo(x)
        vistos.add(v)
    if len(vistos) != mod:
        fallos_b.append(k)
print(f"      k = 1..{K_BIYECCION}: {len(fallos_b)} fallos"
      f"   (2^{K_BIYECCION} = {1 << K_BIYECCION:,} vectores distintos)")
if fallos_b:
    raise SystemExit("La biyeccion de Terras se cae. Eso seria noticia.")
print("      -> ESO es el teorema de Terras, y aguanta.")
print()

print("  (c) Ahora la frase literal. Para que 'T^k sea una aplicacion sobre")
print("      Z/2^k' haria falta que T^k(r) mod 2^k dependiera solo de r.")
contra = None
for k in range(1, 9):
    mod = 1 << k
    for r in range(mod):
        x = r
        y = r + mod
        for _ in range(k):
            x = atajo(x)
            y = atajo(y)
        if (x - y) % mod != 0:
            contra = (k, r, r + mod, x % mod, y % mod)
            break
    if contra:
        break
print(f"      contraejemplo mas pequeno: k = {contra[0]},"
      f" r = {contra[1]} y r' = {contra[2]} son la misma clase,")
print(f"      pero T^{contra[0]}(r) = {contra[3]} y T^{contra[0]}(r')"
      f" = {contra[4]} modulo 2^{contra[0]}.")
print(f"      Ademas T ni siquiera es inyectiva sobre los enteros:"
      f" T(1) = {atajo(1)} = T(4) = {atajo(4)}.")
print()
print("  VEREDICTO: la frase 'T^k es una biyeccion sobre Z/2^k' es FALSA tal")
print("  como esta escrita. Lo cierto es (a)+(b): el VECTOR DE PARIDAD de")
print("  longitud k es una biyeccion entre Z/2^k y {0,1}^k.")
print("  La CONCLUSION del repo se salva entera, porque solo usa (b): hay")
print("  exactamente 2^k clases y una por vector, o sea que no hay dos clases")
print("  que compartan destino y puedan descartarse en bloque.")
print()
print("  Matiz que conviene anotar, porque el repo se pasa de fuerte: decir")
print("  'no hay clases que descartar' no es exacto. pinzaciclos.py descarta")
print("  casi todas. Lo que no hay es descarte EN BLOQUE: cada clase exige su")
print("  propia decision, aunque sea O(1), y por eso el coste es 2^k y no menos.")
print()


# ===========================================================================
# COMPROBACION 7 -- LA CRIBA DE BARINA Y EL FACTOR X ~ 363
# ===========================================================================

print("=" * 74)
print("COMPROBACION 7 -- el factor de criba X ~ 363 de Barina")
print("=" * 74)
print()

dens_clasica = Fraction(a076227[34], 1 << 34)
dens_barina = Fraction(BARINA_H2ESIEVE_34, 1 << 34)
dens_total = dens_barina * BARINA_FACTOR_3

print("  pieza                          vivos a k=34     densidad   1 de cada")
print("  -----------------------------  ------------  -----------  ---------")
print(f"  A076227 (criba clasica)        {a076227[34]:>12,}"
      f"  {float(dens_clasica) * 100:>10.4f}%  {1 / float(dens_clasica):>9.1f}")
print(f"  h2esieve-34 (Barina)           {BARINA_H2ESIEVE_34:>12,}"
      f"  {float(dens_barina) * 100:>10.4f}%  {1 / float(dens_barina):>9.1f}")
print(f"  por la criba 3^2 (x 5/9)       {'-':>12}"
      f"  {float(dens_total) * 100:>10.4f}%  {1 / float(dens_total):>9.1f}")
print()
print(f"  X reconstruido = {1 / float(dens_total):.2f}   (el CLAUDE.md dice"
      f" ~363)")
print()
print("  QUE ESTA VERIFICADO Y QUE NO, sin adornos:")
print("    VERIFICADO  : a(34) = 151.917.636, contra el b-file de OEIS.")
print("    VERIFICADO  : la aritmetica de componer los tres factores.")
print("    NO VERIFICADO: el 85.234.595. Sale de un fichero binario de criba")
print("                  de Barina que no esta en esta maquina.")
print("    NO VERIFICADO: el factor 5/9 de su criba 3^2 (sus reglas R5/R6).")
print("    NO VERIFICABLE: la verificacion hasta 2^71. Son 12.395 anos-CPU")
print("                  mas 159 anos-GPU. No se finge.")
print()
print("  Lo que si se puede rederivar del todo es el PRIMER nivel, 3^1, que")
print("  es donde vive la idea. Y es una COTA, se demuestra en una linea:")
print()
print("    si n = 2 (mod 3), entonces x = (2n-1)/3 es un entero IMPAR y")
print("    positivo, x < n, y 3x+1 = 2n. Luego la trayectoria de x pasa por")
print("    n. Si todo m < n baja, n baja. Esa clase entera se puede saltar.")
print()
fallos_7 = 0
for n in range(2, LIMITE_CRIBA3 + 1):
    if n % 3 == 2:
        if (2 * n - 1) % 3 != 0:
            fallos_7 += 1
            continue
        x = (2 * n - 1) // 3
        if x < 1 or x >= n or x % 2 == 0 or 3 * x + 1 != 2 * n:
            fallos_7 += 1
print(f"  comprobado para todo n = 2 (mod 3) hasta {LIMITE_CRIBA3:,}:"
      f" {fallos_7} fallos")
if fallos_7:
    raise SystemExit("La regla del 3 se cae. Revisar.")
print("  -> quita exactamente 1 de cada 3 numeros. Factor 3/2 de criba,")
print("     demostrado. El salto de 2/3 a 5/9 es de Barina y no se")
print("     reconstruye aqui.")
print()
print("  Y la nota estructural que hace falta decir: la criba compra un")
print("  limite B por debajo del cual todo baja. NO busca ciclos. El propio")
print("  worker.c de Barina lleva MAXIMUM_CYCLE_OFFSET 0 como constante.")
print()


# ===========================================================================
# RESUMEN
# ===========================================================================

print("=" * 74)
print("RESUMEN: cota, promedio, o construccion")
print("=" * 74)
print()
print("  Res(n) >= 1 para todo n que llegue a 1 ...... COTA (demostrada,")
print("      pero condicional a que n termine: no ataca la conjetura)")
print("  Res(n) <= 1,253142144 ....................... conjetura, no demostrada")
print("  Wagon 9,4779555565592747... ................. PROMEDIO")
print("  media del atajo 3,4926518521864 ............. PROMEDIO")
print("  k/ln(4/3), la escalera 1:2:3 ................ PROMEDIO y conjetural")
print("  A076227 ..................................... CONSTRUCCION (conteo")
print("      exacto de una definicion; el contenido es la biyeccion de Terras)")
print("  vector de paridad biyectivo ................. COTA / teorema (Terras)")
print("  la regla n = 2 (mod 3) de la criba .......... COTA (una linea)")
print("  X ~ 363 de Barina ........................... medida de ingenieria,")
print("      con dos insumos que no se han podido verificar aqui")
print()
print("  Para el CUARTO CAMINO (criterios finitos sobre infinitos numeros)")
print("  solo sirven las dos COTAS estructurales: la biyeccion de Terras y")
print("  la regla del 3. Todas las constantes son promedios y no deciden")
print("  ningun n concreto.")
print()
print("FIN. Todas las comprobaciones pasaron.")
