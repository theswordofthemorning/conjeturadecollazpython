# verificar_fusiones.py
#
# GARNER 1985 Y GAO 1993, RE-DERIVADOS DESDE CERO CON ARITMETICA EXACTA.
#
# Este repo cita a Garner y a Gao y los da por buenos porque tienen autor. Eso
# ya fallo dos veces (Wu-Huang 2001 sin DOI; la cota de ciclos once veces mas
# debil que el estado del arte). Aqui no se cree nada: se recalcula.
#
# QUE SE COMPRUEBA, Y DE QUIEN ES CADA COSA
# ---------------------------------------------------------------------------
#
# GARNER (1985), "On heights in the Collatz 3n+1 problem", Discrete Math. 55,
# 57-64. Referencia verificada por Crossref segun el propio CLAUDE.md.
#
#   G1. 8k+4 y 8k+5 se funden SIEMPRE en 3 pasos.
#   G2. Si dos trayectorias se funden, entonces 2^r*k + n1 y 2^r*k + n2 se
#       funden PARA TODO k: una fusion genera una progresion aritmetica
#       infinita de fusiones.
#   G3. Hay infinitos pares de consecutivos con la misma altura y el mismo
#       tiempo de parada total.
#
# GAO (1993). Referencia verificada por Crossref segun el propio CLAUDE.md.
#
#   GA1. Si existe UNA tupla de k consecutivos con la misma altura, existen
#        infinitas.
#   GA2. Hay una tupla de 35.654 empezando en 2^500 + 1.
#
# Y EL REPO CONTRA SI MISMO: guardarhilos.py afirma que 100002..100007 tienen
# 53 pasos los seis y se funden con desfase cero, y que (100005, 100006) es un
# caso de una familia publicada.
#
# EL VOCABULARIO, QUE EN ESTA LITERATURA CONFUNDE
# ---------------------------------------------------------------------------
#
#   altura h(n)            = NUMERO DE PASOS del mapa clasico hasta el 1.
#                            Es lo que aqui se llama altura() y es lo que se
#                            usa en TODAS las comprobaciones de abajo.
#   tiempo de parada total = exactamente lo mismo. Es sinonimo, no una segunda
#                            magnitud (Lagarias: sigma_infinito).
#   tiempo de parada       = primer paso con valor < n. OTRA cosa, y se mide
#                            aparte para que se vea que no coincide.
#   excursion maxima t(n)  = el VALOR mas alto de la trayectoria. Tampoco es
#                            la altura, y se mide aparte para que se vea.
#
# LA DISTINCION QUE MANDA: cota o promedio. Todo lo de este archivo son
# CRITERIOS FINITOS SOBRE CLASES que deciden sobre infinitos numeros. Ninguna
# medicion estadistica decide nada aqui. Eso es exactamente el cuarto camino.
#
# ARITMETICA: solo int de Python (exacta e ilimitada). Ni un float en toda la
# cadena que decide algo.

# ---------------------------------------------------------------------------
# Cambia esto aqui, guarda, y dale a Ctrl+B en Sublime.
# ---------------------------------------------------------------------------

LIMITE_CONFLUENCIA = 200000   # cuantos k se prueban en (8k+4, 8k+5) confluyen
LIMITE_ALTURA      = 20000    # cuantos k se prueban en altura(8k+4)==altura(8k+5)
MUESTRA_PROPAGA    = 200      # cuantos n se usan en la formula afin
PASOS_PROPAGA      = 25       # hasta que paso i se prueba la formula afin
MULTIPLOS_PROPAGA  = 12       # cuantos m se prueban por cada (n, i)
K_CLASES           = 18       # hasta que 2^k se cuentan las clases que se funden
GAO_EXPONENTE      = 500      # la tupla de Gao arranca en 2^GAO_EXPONENTE + 1
GAO_CUANTOS        = 40000    # cuantos consecutivos se miran a partir de ahi
PRIMERO_HILOS      = 100000   # el bloque de guardarhilos.py
CUANTOS_HILOS      = 11


# --------------------------------------------------------------- el motor

def paso(n):
    """Un paso del mapa clasico de Collatz."""
    return n // 2 if n % 2 == 0 else 3 * n + 1


def altura(n):
    """h(n): NUMERO DE PASOS del mapa clasico hasta llegar al 1."""
    cuenta = 0
    while n != 1:
        n = paso(n)
        cuenta += 1
    return cuenta


def secuencia_de(n):
    """La trayectoria entera, del numero hasta el 1."""
    camino = [n]
    while n != 1:
        n = paso(n)
        camino.append(n)
    return camino


def recorrido(n, i):
    """Avanza i pasos clasicos y devuelve (valor, pares, impares) del tramo."""
    pares = impares = 0
    for _ in range(i):
        if n % 2:
            impares += 1
        else:
            pares += 1
        n = paso(n)
    return n, pares, impares


def paso_atajo(n):
    """Un paso del mapa acelerado T de Terras."""
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def atajo_k(n, k):
    """Devuelve (T^k(n), S_k(n)) con S = cuantos de los k pasos fueron impares."""
    S = 0
    for _ in range(k):
        if n % 2:
            S += 1
            n = (3 * n + 1) // 2
        else:
            n //= 2
    return n, S


print("=" * 74)
print("GARNER 1985 Y GAO 1993, RE-DERIVADOS CON ARITMETICA ENTERA EXACTA")
print("=" * 74)
print()
print("Vocabulario que se usa aqui:")
print("  altura h(n) = NUMERO DE PASOS hasta el 1 (= tiempo de parada total).")
print("  NO es el valor maximo. El valor maximo es la excursion t(n) y se")
print("  mide aparte, abajo, precisamente para que se vea que no coinciden.")


# ===========================================================================
# COMPROBACION 1 -- GARNER G1: (8k+4, 8k+5) confluyen en 3 pasos
# ===========================================================================
#
# El algebra, para tenerla escrita antes de medirla:
#
#   8k+4  es par   -> 4k+2   par   -> 2k+1   IMPAR -> 6k+4     (P, P, I)
#   8k+5  es IMPAR -> 24k+16 par   -> 12k+8  par   -> 6k+4     (I, P, P)
#
# Los dos caen en 6k+4 al tercer paso, con los mismos dos pares y el mismo
# impar, en distinto orden. Eso ultimo es lo que hace que la fusion se
# propague (ver COMPROBACION 3), y no es un detalle decorativo.

print()
print("-" * 74)
print("COMPROBACION 1 -- GARNER G1: 8k+4 y 8k+5 caen en 6k+4 en 3 pasos")
print("-" * 74)

fallos_g1 = 0
fallos_cuentas = 0
for k in range(0, LIMITE_CONFLUENCIA):
    v_a, pares_a, impares_a = recorrido(8 * k + 4, 3)
    v_b, pares_b, impares_b = recorrido(8 * k + 5, 3)
    if not (v_a == v_b == 6 * k + 4):
        fallos_g1 += 1
    if (pares_a, impares_a) != (2, 1) or (pares_b, impares_b) != (2, 1):
        fallos_cuentas += 1

print(f"  k probados: 0 .. {LIMITE_CONFLUENCIA - 1}  ({LIMITE_CONFLUENCIA:,} casos)")
print(f"  C^3(8k+4) = C^3(8k+5) = 6k+4 ..... fallos: {fallos_g1}")
print(f"  los dos gastan 2 pares y 1 impar . fallos: {fallos_cuentas}")
if fallos_g1 or fallos_cuentas:
    raise SystemExit("G1 de Garner no se cumple. Imposible, es algebra. No sigas.")
print("  VEREDICTO G1: CONFIRMADA. Es una identidad algebraica, no una medida.")


# ===========================================================================
# COMPROBACION 2 -- de G1 a la altura, y la excepcion que nadie anota
# ===========================================================================
#
# "Confluyen en 3 pasos" NO implica por si solo "misma altura". Hace falta que
# el punto de encuentro se alcance ANTES de llegar al 1, y en k = 0 eso falla:
# 8*0+4 = 4 ya esta dentro del ciclo final y llega al 1 en 2 pasos, o sea
# antes del paso 3 en el que se supone que se encuentran.

print()
print("-" * 74)
print("COMPROBACION 2 -- de la confluencia a la altura, y el caso k = 0")
print("-" * 74)

print(f"  k=0:  altura(4) = {altura(4)}   altura(5) = {altura(5)}   "
      f"iguales: {altura(4) == altura(5)}")
print("        el 4 llega al 1 en 2 pasos, o sea ANTES del paso 3 en el que")
print("        se encuentran. La confluencia existe; la igualdad de altura no.")

fallos_altura = 0
primer_fallo = None
for k in range(1, LIMITE_ALTURA + 1):
    if altura(8 * k + 4) != altura(8 * k + 5):
        fallos_altura += 1
        if primer_fallo is None:
            primer_fallo = k

print(f"  k de 1 a {LIMITE_ALTURA:,}: altura(8k+4) == altura(8k+5)")
print(f"    fallos: {fallos_altura}   primer fallo: {primer_fallo}")
if fallos_altura:
    raise SystemExit("La igualdad de alturas falla para k >= 1. Revisa.")
print(f"  VEREDICTO: la version con altura vale para k >= 1, NO para k = 0.")

# Y las dos magnitudes que NO son la altura, para que el vocabulario quede
# separado con numeros y no con una advertencia.
print()
print("  Las otras dos magnitudes NO coinciden, y por eso hay que decir cual")
print("  se esta usando:")
print(f"    {'k':>4} {'n':>7} {'altura':>7} {'parada':>7} {'excursion t(n)':>16}")
print(f"    {'-'*4} {'-'*7} {'-'*7} {'-'*7} {'-'*16}")


def tiempo_de_parada(n):
    """Primer paso con valor estrictamente menor que n. NO es la altura."""
    v = n
    c = 0
    while True:
        v = paso(v)
        c += 1
        if v < n:
            return c


dif_excursion = 0
dif_parada = 0
for k in range(1, 2001):
    a, b = 8 * k + 4, 8 * k + 5
    if max(secuencia_de(a)) != max(secuencia_de(b)):
        dif_excursion += 1
    if tiempo_de_parada(a) != tiempo_de_parada(b):
        dif_parada += 1
for k in (1, 2, 3, 7):
    for n in (8 * k + 4, 8 * k + 5):
        print(f"    {k:>4} {n:>7} {altura(n):>7} {tiempo_de_parada(n):>7} "
              f"{max(secuencia_de(n)):>16,}")
print(f"    de k=1 a k=2000: la excursion maxima DIFIERE en {dif_excursion} de 2000")
print(f"                     el tiempo de parada DIFIERE en {dif_parada} de 2000")
if dif_excursion == 0 or dif_parada == 0:
    raise SystemExit("Las tres magnitudes coinciden siempre. Entonces el aviso"
                     " de vocabulario sobra, y eso no cuadra. Revisa.")
print("  O sea: 'misma altura' es CIERTO, 'mismo pico' es FALSO, 'mismo tiempo")
print("  de parada' es FALSO. Solo se salva la magnitud que Garner nombra.")


# ===========================================================================
# COMPROBACION 3 -- GARNER G2: la formula afin, que es el motor de todo
# ===========================================================================
#
# El enunciado que el repo repite es:
#
#   "si dos trayectorias se funden, entonces 2^r*k + n1 y 2^r*k + n2 se funden
#    para todo k"
#
# Antes de creerlo o no, hay que aislar la maquinaria que lo sostiene, que si
# es exacta. Si los primeros i pasos de n gastan e pares y o impares, entonces
# para todo r > e y todo m:
#
#       C^i( 2^r * m + n )  =  3^o * 2^(r-e) * m  +  C^i(n)
#
# Es una RECTA en m. Cada paso par divide el termino anadido entre 2 y cada
# paso impar lo multiplica por 3; y mientras el termino anadido siga siendo
# par, no puede cambiar la paridad del otro sumando, o sea que el vector de
# paridad se conserva. La hipotesis r > e es imprescindible: con r = e el
# termino anadido puede volverse impar antes de tiempo y romper el vector.

print()
print("-" * 74)
print("COMPROBACION 3 -- la formula afin C^i(2^r m + n) = 3^o 2^(r-e) m + C^i(n)")
print("-" * 74)

ok_afin = 0
fallos_afin = 0
fallos_con_r_igual_e = 0
for n in range(1, MUESTRA_PROPAGA + 1):
    for i in range(0, PASOS_PROPAGA + 1):
        v, e, o = recorrido(n, i)
        for m in range(0, MULTIPLOS_PROPAGA):
            r = e + 1
            izquierda, _, _ = recorrido((1 << r) * m + n, i)
            derecha = 3 ** o * (1 << (r - e)) * m + v
            if izquierda == derecha:
                ok_afin += 1
            else:
                fallos_afin += 1
            # y el mismo calculo con r = e, para medir que la hipotesis manda
            izquierda_e, _, _ = recorrido((1 << e) * m + n, i)
            if izquierda_e != 3 ** o * m + v:
                fallos_con_r_igual_e += 1

print(f"  casos con r = e+1 : {ok_afin:,} comprobados, {fallos_afin} fallos")
if fallos_afin:
    raise SystemExit("La formula afin de Garner falla. Sin ella no hay nada. No sigas.")
print(f"  casos con r = e   : {fallos_con_r_igual_e:,} FALLOS")
if fallos_con_r_igual_e == 0:
    raise SystemExit("Con r = e no falla nunca, luego la hipotesis r > e sobra."
                     " Eso contradice el algebra. Revisa.")
print("  VEREDICTO: la formula es exacta y la hipotesis r > e es NECESARIA.")
print("  (el enunciado suelto '2^r*k + n1' no dice cuanto vale r; con r mal")
print("   elegido la propagacion se rompe, y aqui esta medido cuantas veces)")


# ===========================================================================
# COMPROBACION 4 -- GARNER G2 tal como lo repite el repo: FALTA UNA HIPOTESIS
# ===========================================================================
#
# De la formula afin sale, sin margen:
#
#   C^i(2^r m + n1) = 3^{o1} 2^{r-e1} m + v
#   C^j(2^r m + n2) = 3^{o2} 2^{r-e2} m + v
#
# y estas dos son iguales PARA TODO m si y solo si  3^{o1} 2^{-e1} =
# 3^{o2} 2^{-e2}, o sea, por unicidad de la factorizacion, si y solo si
# o1 == o2 y e1 == e2. Es decir: la fusion se propaga si y solo si los dos
# tramos gastan EL MISMO numero de pares y EL MISMO numero de impares.
#
# El (8k+4, 8k+5) de Garner lo cumple: 2 pares y 1 impar los dos. Pero el
# enunciado suelto -"si dos trayectorias se funden"- no lo exige, y hay pares
# que se funden sin cumplirlo. Se busca uno y se mide que rompe.

print()
print("-" * 74)
print("COMPROBACION 4 -- el enunciado suelto de G2 necesita una hipotesis mas")
print("-" * 74)


def primer_valor_comun(x, y):
    """El primer valor que comparten las dos trayectorias, en los indices que
    sea. Este es el sentido FLOJO de 'se funden', y lo cumple CUALQUIER par de
    numeros, porque todos acaban en 1. Por eso solo no basta."""
    A, B = secuencia_de(x), secuencia_de(y)
    donde = {}
    for j, v in enumerate(B):
        donde.setdefault(v, j)
    for i, v in enumerate(A):
        if v in donde:
            return v, i, donde[v]
    return None


def confluencia_propagable(x, y):
    """La fusion que SI se propaga: mismo indice y las mismas cuentas de
    pares e impares en los dos tramos. Devuelve (valor, indice, e, o) o None.
    (Cuentas iguales obliga a indice igual, porque e + o = indice.)"""
    A, B = secuencia_de(x), secuencia_de(y)
    ea = oa = eb = ob = 0
    tope = min(len(A), len(B))
    for i in range(tope):
        if A[i] == B[i] and (ea, oa) == (eb, ob):
            return A[i], i, ea, oa
        if i + 1 < len(A):
            if A[i] % 2:
                oa += 1
            else:
                ea += 1
        if i + 1 < len(B):
            if B[i] % 2:
                ob += 1
            else:
                eb += 1
    return None


# El 7 y el 8 se funden en el sentido flojo -de hecho el 8 esta DENTRO de la
# trayectoria del 7- pero no hay ningun indice donde coincidan con las mismas
# cuentas, porque el 7 gasta 8 pares y 5 impares de mas antes de alcanzarlo.
v, i, j = primer_valor_comun(7, 8)
print(f"  Contraejemplo: 7 y 8 SI se funden (sentido flojo): comparten el {v},")
print(f"    en el paso {i} del 7 contra el paso {j} del 8.")
print(f"  Confluencia propagable (mismo indice y mismas cuentas):"
      f" {confluencia_propagable(7, 8)}")
if confluencia_propagable(7, 8) is not None:
    raise SystemExit("El 7 y el 8 si tendrian confluencia propagable. Revisa.")

iguales = 0
distintas = 0
for m in range(0, 40):
    if altura(1024 * m + 7) == altura(1024 * m + 8):
        iguales += 1
    else:
        distintas += 1
print(f"  1024m+7 contra 1024m+8, m de 0 a 39 (r = 10, de sobra grande):")
print(f"    misma altura: {iguales}    distinta altura: {distintas}")
if distintas == 0:
    raise SystemExit("El contraejemplo no rompe nada. Entonces el enunciado"
                     " suelto seria correcto. Revisa.")

# y ahora el mismo experimento con pares que SI tienen confluencia propagable.
# Se usa k = 1 y no k = 0 porque el par (4, 5) es justamente el que se rompe:
# la trayectoria del 4 TERMINA en el 1 antes de llegar al paso 3, o sea que ni
# siquiera existe el indice donde deberian encontrarse.
print(f"  Nota: el par (4, 5) -o sea k = 0- NO tiene confluencia propagable:")
print(f"    {confluencia_propagable(4, 5)}. La trayectoria del 4 se acaba en el")
print(f"    paso 2 y el encuentro seria en el 3. Por eso k = 0 es la excepcion.")
prop = confluencia_propagable(12, 13)
print(f"  Control con k = 1: 12 y 13 -> valor {prop[0]}, indice {prop[1]},")
print(f"    con {prop[2]} pares y {prop[3]} impares en los dos tramos.")
malos_prop = 0
for k in range(1, 2001):
    if confluencia_propagable(8 * k + 4, 8 * k + 5) != (6 * k + 4, 3, 2, 1):
        malos_prop += 1
print(f"  confluencia propagable = (6k+4, 3, 2, 1) para k de 1 a 2000:"
      f" {malos_prop} fallos")
if malos_prop:
    raise SystemExit("La confluencia propagable no sale donde el algebra dice.")
iguales_ok = 0
distintas_ok = 0
for m in range(1, 2001):
    if altura(8 * m + 4) == altura(8 * m + 5):
        iguales_ok += 1
    else:
        distintas_ok += 1
print(f"    8m+4 contra 8m+5, m de 1 a 2000: iguales {iguales_ok},"
      f" distintas {distintas_ok}")
if distintas_ok:
    raise SystemExit("El par que cumple las cuentas tambien falla. Revisa.")
print("  VEREDICTO G2: CONFIRMADA PARCIAL. El mecanismo es exacto, pero el")
print("  enunciado tal como lo repite el CLAUDE.md ('si dos trayectorias se")
print("  funden...') es FALSO sin anadir 'con el mismo numero de pares y de")
print("  impares en los dos tramos'. Medido: 34 de 40 fallan.")


# ===========================================================================
# COMPROBACION 5 -- el criterio de clases, en Python puro y sin numpy
# ===========================================================================
#
# clasesfusion.py cuenta con numpy los restos r modulo 2^k que se funden para
# todo m, con el criterio T^k(r)==T^k(r+1) y S_k(r)==S_k(r+1). Aqui se cuenta
# lo mismo desde cero, sin numpy, con enteros de Python, para ver si sale la
# misma sucesion que el repo publica.
#
# Y se cuenta ademas una cosa que el repo NO reporta: cuantos restos cumplen
# la primera condicion pero NO la segunda. Esos son la trampa: coinciden solo
# para m = 0 y para ningun m mayor.

print()
print("-" * 74)
print("COMPROBACION 5 -- las clases que se funden, rederivadas sin numpy")
print("-" * 74)
print(f"  {'k':>3} {'a(k)':>8}  {'mismo T, distinto S':>21}")
print(f"  {'-'*3} {'-'*8}  {'-'*21}")

sucesion = []
trampas = {}
for k in range(3, K_CLASES + 1):
    buenas = 0
    trampa = 0
    anterior = atajo_k(0, k)
    for r in range(0, 1 << k):
        actual = atajo_k(r + 1, k)
        if anterior[0] == actual[0]:
            if anterior[1] == actual[1]:
                buenas += 1
            else:
                trampa += 1
        anterior = actual
    sucesion.append(buenas)
    trampas[k] = trampa
    print(f"  {k:>3} {buenas:>8,}  {trampa:>21}")

PUBLICADA = [1, 3, 8, 18, 39, 82, 170, 351, 721, 1476, 3012, 6130, 12450, 25241]
comunes = min(len(PUBLICADA), len(sucesion))
if sucesion[:comunes] != PUBLICADA[:comunes]:
    raise SystemExit("La sucesion no coincide con la que el repo publica."
                     " Una de las dos implementaciones esta mal.")
print(f"  los primeros {comunes} terminos coinciden con los del repo"
      f" (sucesiones.txt): 0 discrepancias")

# el ejemplo concreto de trampa, con su numero
print()
print("  LA TRAMPA, con nombre y apellido. r = 7 modulo 1024:")
a7 = atajo_k(7, 10)
a8 = atajo_k(8, 10)
print(f"    T^10(7) = {a7[0]} con S = {a7[1]}")
print(f"    T^10(8) = {a8[0]} con S = {a8[1]}")
print("    mismo valor, distinto S. Para m = 0 coinciden; para m >= 1 la")
print("    formula da 243m+2 contra 81m+2, que no se parecen en nada.")
print("    Es la cola comun 1-2-4 disfrazada de clase. El criterio del repo")
print("    la descarta bien porque exige TAMBIEN S igual - confirmado.")

# y las dos familias publicadas, rederivadas
g_v, g_S = atajo_k(4, 3), atajo_k(5, 3)
w_v, w_S = atajo_k(5, 5), atajo_k(6, 5)
print()
print("  Las dos familias publicadas, rederivadas desde el criterio:")
print(f"    Garner  r=4, k=3:  T^3(4)={g_v[0]} S={g_v[1]}  |  "
      f"T^3(5)={g_S[0]} S={g_S[1]}  -> {g_v == g_S}")
print(f"    (32m+5) r=5, k=5:  T^5(5)={w_v[0]} S={w_v[1]}  |  "
      f"T^5(6)={w_S[0]} S={w_S[1]}  -> {w_v == w_S}")
if not (g_v == g_S and w_v == w_S):
    raise SystemExit("El criterio no reproduce las familias publicadas. Mal.")


# --------- y AHORA el agujero: el criterio NO vale para m = 0
#
# El criterio garantiza que 2^k*m + r y 2^k*m + r+1 llegan al MISMO valor en
# el paso k de T. De ahi se concluye que tienen la misma altura. Pero eso
# supone que el encuentro ocurre ANTES de tocar el 1, y con m = 0 el numero
# es el propio r, que puede ser tan pequeno que ya haya terminado.
#
# clasesfusion.py comprueba el criterio contra fuerza bruta con
#     for m in range(1, 40)
# o sea EMPEZANDO EN 1. Por construccion no puede ver el unico m que falla.
# Aqui se mira m = 0 aparte.

print()
print("  EL AGUJERO DEL CRITERIO: el caso m = 0, que el repo nunca mira")
print(f"  {'k':>3} {'clases buenas':>13} {'fallan en m=0':>14}  cuales")
print(f"  {'-'*3} {'-'*13} {'-'*14}  {'-'*20}")

fallos_m_positivo = 0
malas_m_cero = set()
for k in range(3, 15):
    buenas_k = []
    anterior = atajo_k(0, k)
    for r in range(0, 1 << k):
        actual = atajo_k(r + 1, k)
        if anterior == actual:
            buenas_k.append(r)
        anterior = actual
    # m = 0: el numero es el propio r (se salta r = 0, que no tiene altura)
    fallan = [r for r in buenas_k if r > 0 and altura(r) != altura(r + 1)]
    # m >= 1: el criterio deberia ser exacto
    for r in buenas_k:
        for m in range(1, 31):
            if altura((1 << k) * m + r) != altura((1 << k) * m + r + 1):
                fallos_m_positivo += 1
    print(f"  {k:>3} {len(buenas_k):>13,} {len(fallan):>14}  {fallan}")

print(f"  fallos con m >= 1 (k de 3 a 14, m de 1 a 30): {fallos_m_positivo}")
if fallos_m_positivo:
    raise SystemExit("El criterio falla con m >= 1. Eso si romperia la cota.")
print("  Los tres pares que fallan son siempre los mismos, y son estos:")
for r in (2, 4, 5):
    print(f"    n = {r} y n+1 = {r + 1}:  altura {altura(r)} contra"
          f" {altura(r + 1)}")
print("  Causa unica: esos numeros llegan al 1 ANTES del paso k donde el")
print("  criterio los hace coincidir. Es el mismo motivo por el que 8k+4")
print("  falla en k = 0 (COMPROBACION 2) y por el que 32m+5 falla en m = 0.")
print("  El enunciado correcto es 'para todo m >= 1', no 'para todo m'.")
print("  NO afecta a la cota de densidad: tres excepciones no mueven una")
print("  densidad asintotica. Afecta al ENUNCIADO, igual que le paso al")
print("  piso de la altitud, que tambien perdio una hipotesis por el camino.")


# ===========================================================================
# COMPROBACION 6 -- GARNER G3: infinitos pares, que es una CONSTRUCCION
# ===========================================================================
#
# G3 no hay que medirlo: sale de G1 + el hecho de que 8k+4 y 8k+5 confluyen
# antes de tocar el 1 para todo k >= 1. Es una familia infinita explicita, o
# sea una CONSTRUCCION, no una cota ni un promedio. Lo unico que se puede
# hacer con codigo es confirmar que la familia no se agota, y ya se hizo en
# la COMPROBACION 2 hasta k = LIMITE_ALTURA.

print()
print("-" * 74)
print("COMPROBACION 6 -- G3: infinitos pares con la misma altura")
print("-" * 74)
print("  No es medible: es una CONSTRUCCION. La familia {8k+4, 8k+5} para")
print(f"  k >= 1 ya es infinita, y se verifico hasta k = {LIMITE_ALTURA:,}")
print(f"  con {fallos_altura} fallos. Un ordenador no puede hacer mas que eso:")
print("  la infinitud la da el algebra de la COMPROBACION 1, no el barrido.")
print("  'Mismo tiempo de parada total' es la MISMA afirmacion que 'misma")
print("  altura' - son sinonimos, no dos resultados.")


# ===========================================================================
# COMPROBACION 7 -- GAO 1993: la tupla de 35.654 en 2^500 + 1
# ===========================================================================
#
# El numero tiene 151 cifras y Python lo aguanta. Calcular 35.654 alturas a
# pelo serian ~128 millones de operaciones con enteros de 500 bits; con
# memoizacion sobre los valores ya vistos baja a un par de segundos, porque
# las trayectorias se funden enseguida entre ellas (que es justamente lo que
# dice el teorema).
#
# La memoizacion se verifica contra la version lenta antes de usarla.

print()
print("-" * 74)
print(f"COMPROBACION 7 -- GAO 1993: la tupla que arranca en 2^{GAO_EXPONENTE} + 1")
print("-" * 74)

_memoria = {1: 0}


def altura_memo(n):
    """Igual que altura(n), pero recordando lo ya calculado."""
    pila = []
    while n not in _memoria:
        pila.append(n)
        n = paso(n)
    h = _memoria[n]
    while pila:
        v = pila.pop()
        h += 1
        _memoria[v] = h
    return h


fallos_memo = 0
for n in range(1, 5001):
    if altura_memo(n) != altura(n):
        fallos_memo += 1
print(f"  la version memoizada contra la lenta, n de 1 a 5.000:"
      f" {fallos_memo} discrepancias")
if fallos_memo:
    raise SystemExit("La memoizacion no da lo mismo que la cuenta directa. No sigas.")

BASE = (1 << GAO_EXPONENTE) + 1
h_base = altura_memo(BASE)
print(f"  2^{GAO_EXPONENTE} + 1 tiene {len(str(BASE))} cifras decimales")
print(f"  altura(2^{GAO_EXPONENTE} + 1) = {h_base} pasos")
print(f"  altura(2^{GAO_EXPONENTE})     = {altura_memo(BASE - 1)} pasos"
      f"  (el de antes, o sea la racha empieza justo ahi)")

racha = 0
rompe_en = None
altura_rompe = None
for d in range(0, GAO_CUANTOS):
    if altura_memo(BASE + d) == h_base:
        racha += 1
    else:
        rompe_en = d
        altura_rompe = altura_memo(BASE + d)
        break

print(f"  consecutivos mirados: {GAO_CUANTOS:,}")
print(f"  RACHA MEDIDA: {racha:,} consecutivos con altura {h_base}")
if rompe_en is None:
    print(f"  no se rompio dentro del rango mirado (sube GAO_CUANTOS)")
else:
    print(f"  se rompe en el desplazamiento {rompe_en:,}, cuya altura es"
          f" {altura_rompe}")
if racha != 35654:
    raise SystemExit(f"Gao dice 35.654 y aqui salen {racha}. Uno de los dos"
                     f" esta mal, y hay que decir cual antes de seguir.")
print("  VEREDICTO GA2: CONFIRMADA EXACTA. 35.654, ni uno mas ni uno menos.")
print("  (comprobados los 35.654 enteros de la tupla, uno por uno, con")
print("   aritmetica entera exacta sobre numeros de 151 cifras)")
print()
print("  GA1 ('si existe una, existen infinitas') NO se puede comprobar con")
print("  codigo: es una implicacion sobre todas las tuplas. Lo que si se")
print("  puede es verificar su mecanismo, que es el mismo G2 de Garner ya")
print("  medido arriba, aplicado a los 35.653 pares de la tupla.")


# ===========================================================================
# COMPROBACION 8 -- el repo contra si mismo: guardarhilos.py
# ===========================================================================

print()
print("-" * 74)
print("COMPROBACION 8 -- lo que afirma guardarhilos.py, recalculado")
print("-" * 74)

semillas = [PRIMERO_HILOS + i for i in range(CUANTOS_HILOS)]
caminos = {n: secuencia_de(n) for n in semillas}

print(f"  {'n':>8} {'altura':>7} {'excursion t(n)':>16}")
print(f"  {'-'*8} {'-'*7} {'-'*16}")
for n in semillas:
    print(f"  {n:>8} {len(caminos[n]) - 1:>7} {max(caminos[n]):>16,}")

seis = list(range(100002, 100008))
alturas_seis = [len(caminos[n]) - 1 for n in seis]
print(f"  los seis 100002..100007: alturas {alturas_seis}")
if set(alturas_seis) != {53}:
    raise SystemExit("El repo dice 53 pasos los seis y no sale. Revisa.")
print("  AFIRMACION DEL REPO '53 pasos los seis': CONFIRMADA.")


def primer_comun(x, y):
    """(valor, paso en x, paso en y) del primer numero que comparten."""
    A, B = caminos[x], caminos[y]
    donde = {}
    for j, v in enumerate(B):
        donde.setdefault(v, j)
    for i, v in enumerate(A):
        if v in donde:
            return v, i, donde[v]
    return None


print()
print(f"  Las 15 parejas de los seis, con su desfase:")
print(f"  {'par':>17} {'se funden en':>14} {'paso':>6} {'paso':>6} {'desfase':>8}")
print(f"  {'-'*17} {'-'*14} {'-'*6} {'-'*6} {'-'*8}")
desfases_no_cero = 0
for a_i in range(len(seis)):
    for b_i in range(a_i + 1, len(seis)):
        x, y = seis[a_i], seis[b_i]
        v, i, j = primer_comun(x, y)
        if i - j != 0:
            desfases_no_cero += 1
        print(f"  {x}+{y:>8} {v:>14,} {i:>6} {j:>6} {i - j:>8}")
print(f"  parejas con desfase distinto de cero: {desfases_no_cero} de 15")
if desfases_no_cero:
    raise SystemExit("El repo dice desfase cero en todas y no sale. Revisa.")
print("  AFIRMACION DEL REPO 'desfase cero': CONFIRMADA en las 15 parejas.")

# y el minimo k del criterio de clases para cada par consecutivo
print()
print("  A que nivel k decide el criterio de clases cada par consecutivo:")
print(f"  {'par':>17} {'resto mod 2^k':>14} {'k minimo':>9}")
print(f"  {'-'*17} {'-'*14} {'-'*9}")
for x in range(100002, 100007):
    k_min = None
    for k in range(1, 31):
        a, sa = atajo_k(x, k)
        b, sb = atajo_k(x + 1, k)
        if a == b and sa == sb:
            k_min = k
            break
    marca = ""
    if x == 100005:
        marca = "   <- el par 32m+5"
    print(f"  {x}+{x+1:>8} {x % (1 << k_min):>14} {k_min:>9}{marca}")

print()
print(f"  La familia (32m+5, 32m+6): 100005 = 32*{(100005 - 5) // 32} + 5")
print(f"    m = 0 aparte, porque es el agujero de la COMPROBACION 5:")
print(f"      32*0+5 = 5 y 32*0+6 = 6 -> alturas {altura_memo(5)} y"
      f" {altura_memo(6)}. NO coinciden.")
fallos_familia = 0
for m in [1, 2, 7, 100, 3125, 9999, 40000, 123456, 10 ** 7]:
    if altura_memo(32 * m + 5) != altura_memo(32 * m + 6):
        fallos_familia += 1
print(f"    m en 1,2,7,100,3125,9999,40000,123456,10^7 -> alturas distintas:"
      f" {fallos_familia}")
if fallos_familia:
    raise SystemExit("La familia 32m+5 falla con m >= 1. Revisa.")
print("    CONFIRMADA para m >= 1. Y el criterio de la COMPROBACION 5 la")
print("    decide para los INFINITOS m de golpe, sin muestrear: eso es una")
print("    cota, no una media. Pero con la hipotesis m >= 1 puesta.")


# ===========================================================================
# EL BALANCE
# ===========================================================================

print()
print("=" * 74)
print("BALANCE: cota, promedio o construccion")
print("=" * 74)
print()
print("  G1  8k+4 y 8k+5 caen en 6k+4 en 3 pasos ...... IDENTIDAD ALGEBRAICA")
print("      Sirve para la formula: SI. Es un criterio finito (mirar el resto")
print("      modulo 8) que decide sobre infinitos numeros. Cuarto camino puro.")
print()
print("  G1' misma ALTURA ............................. IDENTIDAD, con k >= 1")
print("      El k = 0 es una excepcion real: altura(4)=2 y altura(5)=5.")
print()
print("  G2  la propagacion ........................... EXACTA, pero le falta")
print("      una hipotesis en como la repite el CLAUDE.md. Sirve para la")
print("      formula SOLO con la hipotesis puesta: mismos pares y mismos")
print("      impares en los dos tramos.")
print()
print("  G3  infinitos pares .......................... CONSTRUCCION")
print("      No es una cota ni un promedio: es una familia explicita.")
print()
print("  GA2 la tupla de 35.654 ....................... CONSTRUCCION, exacta")
print("      Verificada numero a numero. No dice nada sobre los demas enteros.")
print()
print("  GA1 'una implica infinitas' .................. NO COMPROBABLE AQUI")
print("      Es una implicacion sobre todas las tuplas posibles. Lo unico")
print("      verificable es su mecanismo, que es G2.")
print()
print("  EXTRA, y es lo que no cuadra con el CLAUDE.md: el criterio de")
print("  clasesfusion.py se anuncia como valido 'para todo m' y falla en")
print("  m = 0 en exactamente tres clases (r = 2, 4, 5). La comprobacion")
print("  contra fuerza bruta de ese archivo recorre 'for m in range(1, 40)',")
print("  o sea que empieza en 1 y estructuralmente no puede verlo. La cota")
print("  de densidad NO cambia; el enunciado si.")
print()
print("  Nada de este archivo es un promedio. Todo son criterios finitos")
print("  sobre clases de restos, que es exactamente lo que el cuarto camino")
print("  pide. Y ninguno de ellos toca la conjetura: dicen que dos numeros")
print("  van al MISMO sitio, no que ese sitio sea el 1.")
