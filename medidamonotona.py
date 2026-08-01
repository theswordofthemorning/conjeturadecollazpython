# medidamonotona.py
#
# LA BUSQUEDA DE UNA CANTIDAD MONOTONA, Y LA MEDIDA DE COMO FALLA.
#
# ---------------------------------------------------------------------------
# POR QUE ESTA VIA Y NO OTRA
# ---------------------------------------------------------------------------
#
# Todo lo que este laboratorio ha medido es de dos tipos: promedios (la
# fraccion impar, las constantes de parada, la razon B/A) o identidades
# exactas (Terras, el espejo base 2, gamma(rho)). Ninguno de los dos puede
# demostrar nada sobre un numero individual.
#
# Hay un tercer tipo de objeto que si tendria forma de demostracion: una
# funcion Q sobre los enteros positivos tal que
#
#     Q(T(n)) < Q(n)   para todo n > 1
#
# con Q tomando valores en un conjunto BIEN ORDENADO. Eso es una induccion
# bien fundada, o sea la conjetura demostrada en dos lineas.
#
# EL SEGUNDO REQUISITO ES EL QUE SE OLVIDA SIEMPRE. Si Q toma valores reales,
# "decrece siempre" no basta: 1, 1/2, 1/4, ... decrece para siempre y no llega
# a ningun sitio. Los reales positivos NO estan bien ordenados. Solo sirven
# codominios sin cadenas descendentes infinitas: los enteros no negativos, los
# ordinales, o cualquier real con un salto minimo garantizado.
#
# Y HAY UN TERCER REQUISITO, que este fichero anota porque descalifica de
# entrada a la mitad de las candidatas del encargo: Q TIENE QUE SER FUNCION DE
# n SOLO. El "residuo parcial 2^B/(3^A n)" y la "S parcial" son funciones del
# PAR (semilla, numero de pasos), no del numero en el que estas. No definen una
# funcion sobre los enteros y por tanto no pueden fundar ninguna induccion.
# Se miden igual, abajo, y sale algo util: van en el sentido contrario.
#
# ---------------------------------------------------------------------------
# EL OBJETIVO NO ES ENCONTRARLA. ES MEDIR COMO FALLA
# ---------------------------------------------------------------------------
#
# No se conoce ninguna Q asi (Blazewicz-Pettorossi 1983 lo intentaron sobre las
# cadenas binarias). Lo que si se puede hacer, y es lo que hace este programa,
# es medir DONDE falla cada candidata. Una Q que decrece salvo en un conjunto
# DESCRIBIBLE de clases de resto es una demostracion con un agujero localizado,
# y eso vale mas que otra medicion de promedios.
#
# ---------------------------------------------------------------------------
# EL CONTROL A/B, OBLIGATORIO EN ESTE REPO
# ---------------------------------------------------------------------------
#
# Toda cantidad se mide tambien sobre 3n-1. El mapa 3n-1 NO converge a un solo
# sumidero: tiene tres ciclos. Una Q que decrezca igual en los dos mapas no
# puede demostrar convergencia, porque estaria demostrando algo falso. Ya paso
# hoy con la sucesion a(k) de clasesfusion.py, que salio identica en los dos.
#
# ---------------------------------------------------------------------------
# ARITMETICA
# ---------------------------------------------------------------------------
#
# Ni un float en la cadena que decide. Las candidatas con logaritmos se
# codifican como enteros que preservan el orden:
#
#     log2(n) + (p/q)*racha(n)   ordena igual que   n^q * 2^(p*racha(n))
#     log2(n) - c*v2(n)          ordena igual que   n * 2^(c*(64-v2(n)))
#
# Los unicos floats del fichero estan en los porcentajes que se imprimen.

import math
from fractions import Fraction

# ---------------------------------------------------------------------------
LIMITE = 100000          # barrido paso a paso: n de 2 a LIMITE
LIMITE_TRAMOS = 40000    # barrido de tramos de k pasos (mas caro)
KS_TRAMO = (2, 3, 5, 8)  # los k del punto (3) del encargo
K_CLASES = 16            # clases mod 2^k analizadas a fuerza bruta
K_DP = 60                # hasta donde llega el conteo combinatorio exacto
PV_K = 6                 # bits del vector de paridad leido como entero
TOPE_RACHA = 200         # corte de seguridad (el 1 es fijo en el atajo 3n-1)
MUESTRA_CHEQUEO = 3000   # tamano de las comprobaciones previas
# ---------------------------------------------------------------------------


def paso_clasico(n, s):
    """n/2 si par, 3n+s si impar. s = +1 (Collatz) o s = -1 (el control)."""
    return n // 2 if n % 2 == 0 else 3 * n + s


def paso_atajo(n, s):
    """n/2 si par, (3n+s)/2 si impar."""
    return n // 2 if n % 2 == 0 else (3 * n + s) // 2


def v2(n):
    if n == 0:
        return 0
    return (n & -n).bit_length() - 1


def primitivas(n, paso, s):
    """Todo lo que necesitan las candidatas, calculado una sola vez."""
    bl = n.bit_length()
    b = bin(n)[2:]
    pop = b.count("1")
    blq = sum(1 for g in b.split("0") if g)
    vv = v2(n)
    v31 = v2(3 * n + s)
    r = 0
    x = n
    while x % 2 == 1 and r < TOPE_RACHA:
        x = paso(x, s)
        r += 1
    imp = n >> vv
    pv = 0
    x = n
    for _ in range(PV_K):
        pv = pv * 2 + (x & 1)
        x = paso(x, s)
    return (n, bl, pop, blq, vv, v31, r, imp, pv)


# (nombre, valor a partir de las primitivas, codominio, es_entero_directo)
CANDIDATAS = [
    ("n",                      lambda P: P[0],                      "Z>0  bien ordenado",  True),
    ("long_binaria",           lambda P: P[1],                      "Z>0  bien ordenado",  True),
    ("bits_a_uno",             lambda P: P[2],                      "Z>0  bien ordenado",  True),
    ("bloques_de_unos",        lambda P: P[3],                      "Z>=0 bien ordenado",  True),
    ("v2(n)",                  lambda P: P[4],                      "Z>=0 ACOTADA",        True),
    ("v2(3n+s)",               lambda P: P[5],                      "Z>=0 ACOTADA",        True),
    ("racha_impares",          lambda P: P[6],                      "Z>=0 ACOTADA",        True),
    ("parte_impar = n/2^v2",   lambda P: P[7],                      "Z>0  bien ordenado",  True),
    ("vec_paridad_%dbits" % PV_K, lambda P: P[8],                   "Z>=0 ACOTADA",        True),
    ("long_bin + racha",       lambda P: P[1] + P[6],               "Z>0  bien ordenado",  True),
    ("long_bin + 2*racha",     lambda P: P[1] + 2 * P[6],           "Z>0  bien ordenado",  True),
    ("log2(n) + (3/5)racha",   lambda P: P[0] ** 5 * 2 ** (3 * P[6]), "R  NO bien ordenado", False),
    ("log2(n) - 2*v2(n)",      lambda P: P[0] * 2 ** (2 * (64 - P[4])), "R  NO bien ordenado", False),
]

MAPAS = [
    ("atajo   3n+1", paso_atajo, 1),
    ("clasico 3n+1", paso_clasico, 1),
    ("atajo   3n-1", paso_atajo, -1),
    ("clasico 3n-1", paso_clasico, -1),
]

print()
print("=" * 78)
print("medidamonotona.py - la busqueda de una cantidad monotona, y como falla")
print("=" * 78)
print("barrido paso a paso : n de 2 a %d" % LIMITE)
print("barrido de tramos   : n de 2 a %d, k en %s" % (LIMITE_TRAMOS, str(KS_TRAMO)))
print("clases a fuerza bruta: mod 2^k hasta k = %d" % K_CLASES)


# ===========================================================================
# COMPROBACIONES. CORTAN CON SystemExit ANTES DE CUALQUIER CONCLUSION
# ===========================================================================
print()
print("-" * 78)
print("COMPROBACIONES PREVIAS")
print("-" * 78)

# --- 1. La identidad afin de Terras, para los dos mapas. Es el motor de todo
#        el analisis por clases: T^k(2^k m + r) = 3^{S(r)} m + T^k(r).
fallos = 0
for s in (1, -1):
    for k in (1, 3, 5, 8, 11):
        for r in range(0, 2 ** k, max(1, 2 ** k // 40)):
            x = r
            S = 0
            for _ in range(k):
                if x % 2 == 1:
                    S += 1
                x = paso_atajo(x, s)
            tkr = x
            for m in (0, 1, 2, 7, 33, 1000):
                n = 2 ** k * m + r
                if n == 0:
                    continue
                y = n
                for _ in range(k):
                    y = paso_atajo(y, s)
                if y != 3 ** S * m + tkr:
                    fallos += 1
if fallos:
    raise SystemExit("COMPROBACION 1 FALLIDA: la identidad afin de Terras falla %d veces" % fallos)
print("1. identidad afin T^k(2^k m + r) = 3^S(r) m + T^k(r), mapas 3n+1 y 3n-1 : 0 fallos")

# --- 2. El salto de la longitud binaria esta acotado, y es exacto.
#        Paso impar del mapa clasico: +1 o +2. Paso par: -1. Siempre.
peor_bl = 0
fallos = 0
for s in (1, -1):
    for n in range(2, MUESTRA_CHEQUEO):
        d = paso_clasico(n, s).bit_length() - n.bit_length()
        if n % 2 == 0:
            if d != -1:
                fallos += 1
        else:
            if d not in (1, 2):
                fallos += 1
        peor_bl = max(peor_bl, d)
if fallos:
    raise SystemExit("COMPROBACION 2 FALLIDA: la longitud binaria salta fuera de {-1,+1,+2}")
print("2. salto de la longitud binaria: -1 en los pares, +1 o +2 en los impares : 0 fallos")

# --- 3. La racha de impares baja EXACTAMENTE 1 en cada paso impar del atajo.
#        Vale para los dos mapas, y es la razon de que 'long_bin + c*racha'
#        sea la familia interesante.
fallos = 0
for s in (1, -1):
    for n in range(3, MUESTRA_CHEQUEO, 2):
        if n == 1:
            continue
        r0 = primitivas(n, paso_atajo, s)[6]
        r1 = primitivas(paso_atajo(n, s), paso_atajo, s)[6]
        if r0 - r1 != 1:
            fallos += 1
if fallos:
    raise SystemExit("COMPROBACION 3 FALLIDA: la racha no baja exactamente 1 (%d fallos)" % fallos)
print("3. la racha de impares baja exactamente 1 por paso impar del atajo       : 0 fallos")

# --- 4. CONTROL DE QUE EL MEDIDOR PUEDE DAR 100%. La Q perfecta existe y es
#        el numero de pasos hasta 1: decrece exactamente 1 en cada paso, toma
#        valores en Z>=0 y por tanto CIERRA la induccion. Es inutil porque
#        solo se puede evaluar sobre trayectorias que YA llegaron a 1 - el
#        detector de contabilidad de este repo, aplicado a si mismo.
memo = {1: 0}


def pasos_hasta_1(n):
    pila = []
    x = n
    while x not in memo:
        pila.append(x)
        x = paso_clasico(x, 1)
    v = memo[x]
    while pila:
        v += 1
        memo[pila.pop()] = v
    return memo[n]


fallos = 0
for n in range(2, MUESTRA_CHEQUEO):
    if pasos_hasta_1(paso_clasico(n, 1)) != pasos_hasta_1(n) - 1:
        fallos += 1
if fallos:
    raise SystemExit("COMPROBACION 4 FALLIDA: el control de 100% no da 100%")
print("4. control: Q = pasos hasta 1 decrece exactamente 1, en el 100% de los n : 0 fallos")

# --- 5. r -> vector de paridad es BIYECCION mod 2^k. Para los DOS mapas.
#        Esto es lo que hace que el conteo por clases sea el mismo conteo
#        combinatorio en 3n+1 y en 3n-1, y es la clave del A/B de abajo.
for s in (1, -1):
    for k in range(1, 13):
        vistos = set()
        for r in range(2 ** k):
            x = r
            v = 0
            for _ in range(k):
                v = v * 2 + (x & 1)
                x = paso_atajo(x, s)
            vistos.add(v)
        if len(vistos) != 2 ** k:
            raise SystemExit("COMPROBACION 5 FALLIDA: no hay biyeccion resto-vector con s = %d, k = %d" % (s, k))
print("5. resto mod 2^k <-> vector de paridad es biyeccion, k = 1..12, 3n+1 y 3n-1: 0 fallos")

# --- 6. El residuo parcial de la identidad de Terras NUNCA baja. Se calcula
#        con Fraction exacto sobre prefijos que no llegan al 1.
bajadas = 0
subidas = 0
iguales = 0
for n0 in range(3, 400, 2):
    n = n0
    A = 0
    B = 0
    R = Fraction(1, 1)
    for _ in range(40):
        Rant = R
        if n % 2 == 0:
            n //= 2
            B += 1
        else:
            n = 3 * n + 1
            A += 1
        R = Fraction(2 ** B * n, 3 ** A * n0)
        if R < Rant:
            bajadas += 1
        elif R > Rant:
            subidas += 1
        else:
            iguales += 1
if bajadas:
    raise SystemExit("COMPROBACION 6 FALLIDA: el residuo parcial bajo %d veces" % bajadas)
print("6. residuo parcial 2^B n / (3^A n0): 0 bajadas, %d subidas, %d empates" % (subidas, iguales))
print("   (o sea que es monotono AL REVES: crece. Y ademas no es funcion de n)")

print()
print("Las seis comprobaciones pasan. A partir de aqui, mediciones.")


# ===========================================================================
# MEDICION 1 - PASO A PASO, LAS TRECE CANDIDATAS, LOS CUATRO MAPAS
# ===========================================================================
print()
print("-" * 78)
print("MEDICION 1 - fraccion de n con Q(T(n)) < Q(n), paso a paso, n = 2..%d" % LIMITE)
print("-" * 78)

nc = len(CANDIDATAS)
buenos = [[0] * nc for _ in MAPAS]
peor = [[0] * nc for _ in MAPAS]
# fallos por clase de resto, solo para el mapa del atajo 3n+1 (indice 0)
MOD_FALLO = 32
fallo_clase = [[0] * MOD_FALLO for _ in range(nc)]
total_clase = [0] * MOD_FALLO

for n in range(2, LIMITE + 1):
    total_clase[n % MOD_FALLO] += 1
    for im, (_, paso, s) in enumerate(MAPAS):
        tn = paso(n, s)
        if tn <= 0:
            continue
        Pn = primitivas(n, paso, s)
        Pt = primitivas(tn, paso, s)
        for ic in range(nc):
            f = CANDIDATAS[ic][1]
            a = f(Pn)
            b = f(Pt)
            if b < a:
                buenos[im][ic] += 1
            else:
                if im == 0:
                    fallo_clase[ic][n % MOD_FALLO] += 1
            if CANDIDATAS[ic][3]:
                d = b - a
                if d > peor[im][ic]:
                    peor[im][ic] = d

total = LIMITE - 1
print()
print("%-24s %9s %9s %9s %9s  %6s" % ("Q", "atajo+1", "clas+1", "atajo-1", "clas-1", "peor"))
print("-" * 78)
for ic in range(nc):
    nombre = CANDIDATAS[ic][0]
    pe = ("%+6d" % peor[0][ic]) if CANDIDATAS[ic][3] else "     -"
    print("%-24s %8.2f%% %8.2f%% %8.2f%% %8.2f%%  %6s" % (
        nombre,
        100.0 * buenos[0][ic] / total,
        100.0 * buenos[1][ic] / total,
        100.0 * buenos[2][ic] / total,
        100.0 * buenos[3][ic] / total,
        pe))
print()
print("'peor' = mayor incremento Q(T(n)) - Q(n) observado en el atajo 3n+1")
print("(solo para las candidatas de valor entero directo)")

print()
print("EL A/B, columna a columna: |atajo+1 - atajo-1| y |clas+1 - clas-1|")
print()
print("%-24s %12s %12s   %s" % ("Q", "dif atajo", "dif clasico", "veredicto"))
print("-" * 78)
for ic in range(nc):
    d1 = abs(buenos[0][ic] - buenos[2][ic]) * 100.0 / total
    d2 = abs(buenos[1][ic] - buenos[3][ic]) * 100.0 / total
    ver = "CIEGA AL SIGNO" if (d1 < 0.5 and d2 < 0.5) else "distingue"
    print("%-24s %11.3f%% %11.3f%%   %s" % (CANDIDATAS[ic][0], d1, d2, ver))
print()
print("Una Q ciega al signo no puede demostrar convergencia: 3n-1 tiene TRES")
print("ciclos, asi que lo que valga igual en los dos mapas no distingue un")
print("sumidero de tres.")


# ===========================================================================
# MEDICION 2 - DONDE FALLAN. LAS CLASES DE RESTO
# ===========================================================================
print()
print("-" * 78)
print("MEDICION 2 - donde fallan exactamente (mapa del atajo, 3n+1)")
print("-" * 78)
print()
print("Para cada Q, las clases mod 32 donde falla SIEMPRE y donde no falla NUNCA.")
print()
for ic in range(nc):
    siempre = [c for c in range(MOD_FALLO) if total_clase[c] and fallo_clase[ic][c] == total_clase[c]]
    nunca = [c for c in range(MOD_FALLO) if total_clase[c] and fallo_clase[ic][c] == 0]
    # comprimir a mod 8 si el patron es periodico de periodo 8
    def resumen(lista):
        if not lista:
            return "ninguna"
        m8 = sorted(set(x % 8 for x in lista))
        if all((c % 8) in m8 for c in range(32) if (c in lista)) and \
           len(lista) == sum(1 for c in range(32) if c % 8 in m8):
            return "n = %s (mod 8)" % ",".join(str(x) for x in m8)
        if len(lista) > 8:
            return "%d clases de 32" % len(lista)
        return "n = %s (mod 32)" % ",".join(str(x) for x in lista)
    print("%-24s falla SIEMPRE en: %-24s  nunca falla en: %s" % (
        CANDIDATAS[ic][0], resumen(siempre), resumen(nunca)))

print()
print("LA CANDIDATA CON EL AGUJERO MAS PEQUENO ES 'long_bin + racha', y su")
print("agujero es una sola clase mod 8. Se detalla abajo.")

# el detalle de long_bin + racha en el atajo 3n+1
ic_lbr = [i for i in range(nc) if CANDIDATAS[i][0] == "long_bin + racha"][0]
f = CANDIDATAS[ic_lbr][1]
sube = [0] * 8
empata = [0] * 8
baja = [0] * 8
peor_sube = 0
for n in range(2, LIMITE + 1):
    tn = paso_atajo(n, 1)
    a = f(primitivas(n, paso_atajo, 1))
    b = f(primitivas(tn, paso_atajo, 1))
    if b < a:
        baja[n % 8] += 1
    elif b == a:
        empata[n % 8] += 1
    else:
        sube[n % 8] += 1
        peor_sube = max(peor_sube, b - a)
print()
print("Q = long_bin(n) + racha(n), atajo 3n+1, repartido por n mod 8:")
print()
print("%6s %10s %10s %10s" % ("n mod 8", "baja", "empata", "SUBE"))
for c in range(8):
    print("%6d %10d %10d %10d" % (c, baja[c], empata[c], sube[c]))
print()
print("Total: baja %d, empata %d, sube %d.  Mayor subida: +%d" % (
    sum(baja), sum(empata), sum(sube), peor_sube))
print()
print("El agujero es EXACTAMENTE n = 6 (mod 8), y esta demostrado en dos lineas:")
print("un paso impar del atajo sube la longitud binaria 0 o 1 y baja la racha 1,")
print("luego nunca sube; un paso par baja la longitud 1 y sube la racha en los")
print("unos finales de n/2, que son >= 2 si y solo si n/2 = 3 (mod 4), o sea")
print("n = 6 (mod 8). Pero los EMPATES son masivos, y un empate ya rompe la")
print("induccion igual que una subida. Q no sirve, y se sabe por que.")


# ===========================================================================
# MEDICION 3 - TRAMOS DE k PASOS
# ===========================================================================
print()
print("-" * 78)
print("MEDICION 3 - Q(T^k(n)) < Q(n) para k fijo, n = 2..%d" % LIMITE_TRAMOS)
print("-" * 78)
print()
print("Basta con que Q decrezca cada k pasos: la induccion sigue cerrando.")
print("Es mucho mas debil que decrecer paso a paso. Se prueba con k = %s." % str(KS_TRAMO))
print()

SUB = ["n", "long_binaria", "bits_a_uno", "long_bin + racha"]
idx = [i for i in range(nc) if CANDIDATAS[i][0] in SUB]

tramos = {}   # (ic, k) -> lista de 4 porcentajes
for k in KS_TRAMO:
    for im, (_, paso, s) in enumerate(MAPAS):
        b = [0] * len(idx)
        tot = 0
        for n in range(2, LIMITE_TRAMOS + 1):
            x = n
            for _ in range(k):
                x = paso(x, s)
            if x <= 0:
                continue
            tot += 1
            Pn = primitivas(n, paso, s)
            Px = primitivas(x, paso, s)
            for j, ic in enumerate(idx):
                fc = CANDIDATAS[ic][1]
                if fc(Px) < fc(Pn):
                    b[j] += 1
        for j, ic in enumerate(idx):
            tramos.setdefault((ic, k), []).append(100.0 * b[j] / tot)

print("%-20s %3s %9s %9s %9s %9s" % ("Q", "k", "atajo+1", "clas+1", "atajo-1", "clas-1"))
print("-" * 78)
for ic in idx:
    for k in KS_TRAMO:
        fila = tramos[(ic, k)]
        print("%-20s %3d %8.2f%% %8.2f%% %8.2f%% %8.2f%%" % (
            CANDIDATAS[ic][0], k, fila[0], fila[1], fila[2], fila[3]))


# ===========================================================================
# MEDICION 4 - EL CRITERIO POR CLASES, EXACTO, Y EL A/B QUE LO MATA
# ===========================================================================
print()
print("-" * 78)
print("MEDICION 4 - el criterio por clases mod 2^k, exacto, y el A/B")
print("-" * 78)
print()
print("De la identidad afin: T^k(2^k m + r) = 3^S(r) m + T^k(r). Luego")
print("T^k(n) < n para TODO m salvo un conjunto FINITO si y solo si 3^S(r) < 2^k.")
print("Eso es un criterio finito que decide sobre infinitos numeros - el cuarto")
print("camino, aplicado a la unica pregunta que importa aqui.")
print()
print("%3s %14s %14s %8s %12s %12s %8s" % (
    "k", "bajan(3n+1)", "bajan(3n-1)", "igual?", "sobrev(+1)", "sobrev(-1)", "igual?"))
print("-" * 78)

POT3 = [3 ** i for i in range(K_CLASES + 2)]
POT2 = [2 ** i for i in range(K_CLASES + 2)]

resumen_clases = {}
for k in range(1, K_CLASES + 1):
    datos = {}
    for s in (1, -1):
        bajan = set()
        sobrev = set()
        for r in range(POT2[k]):
            x = r
            S = 0
            vivo = True
            for j in range(1, k + 1):
                if x & 1:
                    S += 1
                    x = (3 * x + s) >> 1
                else:
                    x >>= 1
                if POT3[S] < POT2[j]:
                    vivo = False
            if POT3[S] < POT2[k]:
                bajan.add(r)
            if vivo:
                sobrev.add(r)
        datos[s] = (bajan, sobrev)
    b1, v1 = datos[1]
    b2, v2s = datos[-1]
    resumen_clases[k] = (len(b1), len(v1))
    print("%3d %14d %14d %8s %12d %12d %8s" % (
        k, len(b1), len(b2), "SI" if len(b1) == len(b2) else "NO",
        len(v1), len(v2s), "SI" if len(v1) == len(v2s) else "NO"))
    if k == 8:
        mismos_b = (b1 == b2)
        mismos_v = (v1 == v2s)

print()
print("A k = 8: los CONJUNTOS de clases coinciden entre 3n+1 y 3n-1? bajan: %s, sobreviven: %s" % (
    "SI" if mismos_b else "NO", "SI" if mismos_v else "NO"))
print()
print("EL RESULTADO DEL A/B: los CONTEOS son identicos en todos los k, y los")
print("CONJUNTOS son distintos. La razon es la comprobacion 5: resto -> vector de")
print("paridad es biyeccion en los dos mapas, asi que el conteo es el mismo conteo")
print("combinatorio sobre {0,1}^k, y el signo del +1 solo permuta que resto lleva")
print("que vector. UN CRITERIO DE DESCENSO POR CLASES NO PUEDE VER EL SIGNO.")

# verificacion contra enteros de verdad: la clase predice, salvo conjunto finito
K_V = 8
pred_baja = set()
umbral_max = 0
for r in range(2 ** K_V):
    x = r
    S = 0
    for _ in range(K_V):
        if x % 2 == 1:
            S += 1
        x = paso_atajo(x, 1)
    if 3 ** S < 2 ** K_V:
        pred_baja.add(r)
fallos = 0
peor_n = 0
for n in range(2, 30000):
    x = n
    for _ in range(K_V):
        x = paso_atajo(x, 1)
    real = (x < n)
    if real != (n % 2 ** K_V in pred_baja):
        fallos += 1
        peor_n = max(peor_n, n)
print()
print("Verificacion contra enteros de verdad, k = %d, n = 2..29999:" % K_V)
print("  la clase acierta salvo en %d numeros, y el mayor de ellos es n = %d." % (fallos, peor_n))
print("  O sea: el conjunto excepcional es FINITO y esta acotado, como dice la")
print("  formula. Por encima de ese n la clase decide sola.")


# ===========================================================================
# MEDICION 5 - EL PRECIO DE LA DEMOSTRACION (EVERETT)
# ===========================================================================
print()
print("-" * 78)
print("MEDICION 5 - el precio de la demostracion: Everett contra el criterio exacto")
print("-" * 78)
print()
print("El criterio EXACTO es 3^S < 2^k, pero para demostrarlo hace falta el")
print("factor exacto (3n+1)/2n, que depende de n. Everett 1977 usa la cota")
print("pesimista 5/3 >= (3n+1)/2n, valida si todos los intermedios son >= 3, y")
print("su criterio DEMOSTRADO es (10/3)^S < 2^k, o sea 10^S < 2^k 3^S.")
print()
print("Las dos cuentas son combinatoria pura: S sobre los restos mod 2^k se")
print("reparte como C(k,S), por la biyeccion de la comprobacion 5.")
print()
print("%3s %14s %10s %14s %10s %10s" % ("k", "exacto", "%", "Everett", "%", "precio"))
print("-" * 78)
for k in (4, 8, 12, 16, 20, 30, 40, 60):
    ex = sum(math.comb(k, S) for S in range(k + 1) if 3 ** S < 2 ** k)
    ev = sum(math.comb(k, S) for S in range(k + 1) if 10 ** S < 2 ** k * 3 ** S)
    print("%3d %14d %9.3f%% %14d %9.3f%% %9.3f%%" % (
        k, ex, 100.0 * ex / 2 ** k, ev, 100.0 * ev / 2 ** k,
        100.0 * (ex - ev) / 2 ** k))
print()
print("El precio de tener demostracion, medido: son los puntos de la ultima")
print("columna. Y crece con k, no se encoge.")


# ===========================================================================
# MEDICION 6 - EL CONTEO EXACTO DE LOS QUE NO BAJAN, Y SU DENSIDAD
# ===========================================================================
print()
print("-" * 78)
print("MEDICION 6 - cuantas clases NO han bajado en ningun paso j <= k")
print("-" * 78)
print()
print("Conteo combinatorio exacto sobre los vectores de paridad (DP, sin barrer")
print("los 2^k restos). Es el mismo numero para 3n+1 y para 3n-1, por la misma")
print("razon de antes.")
print()

f = {0: 1}
serie = []
for j in range(1, K_DP + 1):
    g = {}
    for S, c in f.items():
        for b in (0, 1):
            S2 = S + b
            if 3 ** S2 > 2 ** j:
                g[S2] = g.get(S2, 0) + c
    f = g
    serie.append(sum(f.values()))

# comprobacion cruzada contra el barrido por restos de la medicion 4
malos = [k for k in range(1, K_CLASES + 1) if serie[k - 1] != resumen_clases[k][1]]
if malos:
    raise SystemExit("COMPROBACION FALLIDA: el DP no coincide con el barrido de restos en k = %s" % malos)
print("El DP coincide con el barrido por restos de la medicion 4 en k = 1..%d: 0 fallos" % K_CLASES)
print()
print("%3s %20s %12s %12s %14s" % ("k", "no han bajado", "densidad", "razon", "quita por bit"))
print("-" * 78)
for k in (1, 2, 4, 8, 12, 16, 20, 24, 30, 33, 34, 36, 40, 50, 60):
    if k >= 2:
        razon = serie[k - 1] / serie[k - 2]
        quita = 100.0 * (1.0 - razon / 2.0)
    else:
        razon = 0.0
        quita = 0.0
    print("%3d %20d %12.8f %12.5f %13.2f%%" % (
        k, serie[k - 1], serie[k - 1] / 2.0 ** k, razon, quita))

print()
print("ESTA SUCESION ES A076227, IDENTIFICADA: el termino k = 34 sale %d," % serie[33])
print("que es exactamente el valor que el repo tiene anotado en la seccion de las")
print("cribas industriales, y la densidad sale %.4f%% (1 de cada %.0f), tambien el" % (
    100.0 * serie[33] / 2.0 ** 34, 2.0 ** 34 / serie[33]))
print("valor anotado. Aqui se ha recalculado desde cero, por combinatoria pura y")
print("sin tocar ningun entero: es un conteo sobre {0,1}^k.")
print()
print("Y POR ESO A076227 ES CIEGA AL SIGNO. La medicion 4 la calculo tambien a")
print("fuerza bruta sobre los restos de 3n-1 y salio el MISMO numero en k = 1..%d." % K_CLASES)
print("La criba que certifica que todo n < 2^71 baja funciona igual de bien para")
print("3n-1, que tiene TRES ciclos. La criba compra la cota inferior del minimo de")
print("un ciclo; no puede decir cuantos sumideros hay.")
print()
dobles = [k for k in range(2, K_DP + 1) if serie[k - 1] == 2 * serie[k - 2]]
print("DETALLE QUE NO CUADRA CON 'cada bit extra quita un 3,4%': hay k donde el bit")
print("extra NO QUITA NADA, y el conteo se dobla exacto. En k = 2..%d pasa en:" % K_DP)
print("  k = %s" % ", ".join(str(x) for x in dobles))
print("La caida no es uniforme: alterna bits que quitan 0% con bits que quitan un")
print("8% o un 13%, porque el criterio 3^S > 2^j solo cambia de lado cuando el")
print("entero S cruza k/log2(3), y eso pasa cada dos o tres bits, no en todos.")
d20 = serie[19] / 2.0 ** 20
d40 = serie[39] / 2.0 ** 40
print()
print("Promediado de k = 20 a k = 40, la densidad cae un %.2f%% por bit, no un 3,4%%." % (
    100.0 * (1.0 - (d40 / d20) ** 0.05)))
exp_final = math.log2(serie[K_DP - 1]) / K_DP
print("Y el exponente medido log2(N(k))/k a k = %d vale %.5f, no 0,94996." % (K_DP, exp_final))
print("El 0,94996 = H(log3(2)) es el limite asintotico y es correcto, pero el")
print("factor polinomico que le falta vale %.0f a k = %d: usar 2^(-0,05 k) como" % (
    2.0 ** (0.94996 * K_DP) / serie[K_DP - 1], K_DP))
print("estimacion de la densidad en el rango alcanzable se equivoca por ese factor.")
print()
print("LA DENSIDAD BAJA A CERO PERO EL CONTEO NO: siempre quedan clases que no")
print("bajan en k pasos, para todo k. La clase r = 2^k - 1 esta ahi siempre.")
print("Por eso NINGUNA Q basada en el tamano decrece en todo tramo de k pasos,")
print("para ningun k fijo. La respuesta al punto (3) del encargo es NO, y no es")
print("una medicion: es la clase de los k impares seguidos, que existe siempre.")


# ===========================================================================
# MEDICION 7 - LA COTA DE C >= 0 VA EN EL SENTIDO CONTRARIO
# ===========================================================================
print()
print("-" * 78)
print("MEDICION 7 - por que cotatramos.py NO puede alimentar esta via")
print("-" * 78)
print()
print("cotatramos.py deja verificado que 2^B seq[j] >= 3^A seq[i] sobre prefijos.")
print("Tomando logaritmos:  log2(n_j) - log2(n_i)  >=  A log2(3) - B.")
print()
print("Eso es una cota POR ABAJO del cambio de log2(n). Una medida monotona")
print("necesita una cota POR ARRIBA. Son lados opuestos de la desigualdad.")
print()
sube_y_cumple = 0
totalseg = 0
for n0 in range(3, 6000, 2):
    n = n0
    A = 0
    B = 0
    for _ in range(25):
        if n % 2 == 0:
            n //= 2
            B += 1
        else:
            n = 3 * n + 1
            A += 1
        totalseg += 1
        if 2 ** B * n < 3 ** A * n0:
            raise SystemExit("COMPROBACION FALLIDA: 2^B n_j < 3^A n_i, la cota de Terras se rompe")
        if n > n0:
            sube_y_cumple += 1
print("Verificado en %d tramos: la cota se cumple en el 100%%, y en %d de ellos" % (totalseg, sube_y_cumple))
print("(%.1f%%) el tramo SUBE. Una desigualdad que se cumple igual cuando el numero" % (
    100.0 * sube_y_cumple / totalseg))
print("sube no certifica ningun descenso. La cota por arriba que haria falta es")
print("exactamente el residuo de Roosendaal acotado, y eso solo se sabe medir")
print("sobre trayectorias que ya llegaron al 1: contabilidad, no criterio.")


# ===========================================================================
# CONCLUSIONES
# ===========================================================================
print()
print("=" * 78)
print("CONCLUSIONES")
print("=" * 78)
print()
print("1. NINGUNA de las trece candidatas decrece siempre. La mejor con codominio")
print("   bien ordenado es long_bin + 2*racha, con el 75% en el atajo; la mejor de")
print("   todas es log2(n) + (3/5)racha con el 87%, y esa toma valores reales.")
print()
print("2. LOS CODOMINIOS. v2, v2(3n+s), la racha y el vector de paridad estan")
print("   ACOTADOS, y por eso estan muertos de antemano: si una Q acotada por M")
print("   decreciera estrictamente, toda trayectoria mediria <= M pasos, y los")
print("   tiempos de parada no estan acotados. Las dos con logaritmo toman")
print("   valores reales y NO cierran la induccion aunque decrecieran: los")
print("   reales positivos admiten cadenas descendentes infinitas. Solo cinco")
print("   candidatas tienen codominio bien ordenado, y ninguna decrece.")
print()
print("3. EL AGUJERO MAS PEQUENO MEDIDO es el de long_bin + racha: sube solo en")
print("   n = 6 (mod 8), una clase de ocho, y esta demostrado por que. Pero")
print("   empata en la mayoria de los impares, y un empate rompe la induccion")
print("   igual que una subida. Localizar el agujero no lo cierra.")
print()
print("4. TRAMOS DE k PASOS: no hay k que salve nada, y la razon no es")
print("   estadistica. La clase r = 2^k - 1 (mod 2^k) hace k pasos impares")
print("   seguidos y multiplica por (3/2)^k. Existe para todo k. Cualquier Q que")
print("   crezca con el tamano sube ahi.")
print()
print("5. EL A/B, QUE ES EL RESULTADO: el criterio por clases 3^S(r) < 2^k tiene")
print("   CONTEOS IDENTICOS en 3n+1 y en 3n-1, en todos los k medidos. Como 3n-1")
print("   tiene tres ciclos, ningun criterio de descenso por clases puede")
print("   demostrar convergencia a UN sumidero. Eso incluye el teorema de Terras")
print("   de densidad y el de Everett: los dos valen palabra por palabra para")
print("   3n-1. Demuestran que casi todo baja; no distinguen un sumidero de tres.")
print()
print("6. LA COTA QUE EL REPO YA TENIA (C >= 0) acota el descenso POR ABAJO, y")
print("   una medida monotona necesita cota POR ARRIBA. No sirve, y saberlo")
print("   ahorra el intento.")
print()
print("7. LA SORPRESA: el conteo de clases que no bajan ES A076227 (k = 34 da")
print("   151.917.636, el valor que el repo tiene anotado), y sale IDENTICO para")
print("   3n-1. La criba de Barina es ciega al signo del +1. Y de paso, su ley de")
print("   densidad tal como esta escrita en el repo -2^(-0,05 k), 'cada bit quita")
print("   un 3,4%'- se queda corta por mas del doble en el rango alcanzable: la")
print("   caida medida es del 7% por bit, y hay bits que no quitan absolutamente")
print("   nada.")
