# -*- coding: utf-8 -*-
#
# espejoak.py -- POR QUE amas(k) == amenos(k), y si es teorema o casualidad
# =========================================================================
#
# LO QUE SE MIRA
# --------------
# El repo tenia como mejor resultado propio la sucesion a(k) = cuantas clases
# de resto modulo 2^k "se funden" bajo el mapa del ATAJO de Collatz. Al medir
# la misma sucesion con el mapa del ATAJO de 3n-1 salio IDENTICA, y eso hundio
# el envio a OEIS. La pregunta que queda no es "sale igual?" -- eso ya se
# midio -- sino:
#
#     es un TEOREMA (hay una razon estructural forzosa)
#     o es una COINCIDENCIA que se puede romper en algun k mas grande?
#
# Verificar en veinte k NO distingue esas dos cosas. Por eso este programa
# hace dos trabajos separados:
#
#   (1) mide amas(k) y amenos(k) por su cuenta, con dos implementaciones que
#       no comparten codigo, y contrasta amas(k) contra los valores ya
#       publicados en sucesiones.txt;
#   (2) EXHIBE EL MECANISMO y lo comprueba paso a paso: no solo que los
#       CONTEOS coincidan, sino que hay una biyeccion explicita que manda el
#       conjunto de restos buenos de un mapa EXACTAMENTE sobre el del otro.
#
# EL ENUNCIADO LITERAL QUE SE DECIDE
# ----------------------------------
#   Tmas(n)   = n/2 si n par,  (3n+1)/2 si n impar     (atajo de Collatz)
#   Tmenos(n) = n/2 si n par,  (3n-1)/2 si n impar     (atajo de 3n-1)
#
#   S_k(r) = numero de pasos impares entre los k primeros iterados de r.
#   r es BUENO si   S_k(r) == S_k(r+1)   y   T^k(r) == T^k(r+1),
#   con el borde r = 2^k - 1, cuyo vecino cae en la clase 0 del bloque
#   siguiente y exige  S_k(2^k-1) == S_k(0)  y  T^k(2^k-1) == 3^{S_k(0)} + T^k(0).
#
#   amas(k)   = cuantos restos son buenos para Tmas.
#   amenos(k) = cuantos restos son buenos para Tmenos.
#   AFIRMACION:  amas(k) == amenos(k)  para todo k >= 1.
#
# EL MECANISMO QUE SE PROPONE (derivado a mano, antes de medir nada)
# ------------------------------------------------------------------
# PASO 1. Los dos mapas son EL MISMO mapa conjugado por el cambio de signo.
#         Sea nu(n) = -n. Entonces, como identidad exacta sobre TODO Z:
#
#              Tmenos(n) = - Tmas(-n)          o sea   Tmenos = nu . Tmas . nu
#
#         Se ve en dos lineas: si n es par,   Tmas(-n) = -n/2;
#         si n es impar, -n es impar y  Tmas(-n) = (-3n+1)/2 = -(3n-1)/2.
#         Iterando:   Tmenos^k(n) = - Tmas^k(-n)   para todo k.
#         (Aqui esta LA razon de fondo: 3n-1 no es "otra regla", es la misma
#         regla mirada del otro lado del cero. El espejo del enunciado es
#         literalmente el espejo aritmetico.)
#
# PASO 2. Como -n tiene la misma paridad que n, el vector de paridades de la
#         orbita de r bajo Tmenos es el vector de paridades de la orbita de -r
#         bajo Tmas. Luego, con nu_k(r) = (-r) mod 2^k = (2^k - r) mod 2^k:
#
#              Smenos_k(r) = Smas_k(nu_k(r))
#
# PASO 3. Para r >= 1 se tiene -r = nu_k(r) - 2^k, o sea m = -1 en la formula
#         afin de Terras  T^k(2^k*m + s) = 3^{S(s)}*m + T^k(s). Luego
#
#              Tmenos^k(r) = 3^{Smas(nu_k(r))} - Tmas^k(nu_k(r))       (r >= 1)
#
# PASO 4. EL PUNTO CLAVE: el cambio de signo manda PAREJAS DE VECINOS en
#         PAREJAS DE VECINOS, solo que dadas la vuelta:
#              (r, r+1)  ->  (-r-1, -r)
#         Escrito con la involucion  phi(r) = 2^k - 1 - r  (el NOT bit a bit
#         sobre k bits):   nu_k(r) = phi(r) + 1   y   nu_k(r+1) = phi(r).
#         Sustituyendo en los pasos 2 y 3, la condicion de que r sea bueno
#         para Tmenos se convierte, termino a termino, en la condicion de que
#         phi(r) sea bueno para Tmas. (El 3^S de la formula del paso 3 se
#         cancela justamente porque la condicion sobre S ya obliga a que los
#         dos exponentes sean el mismo.)
#
# CONCLUSION QUE HAY QUE COMPROBAR:   BUENOS_menos(k) = phi( BUENOS_mas(k) )
# como CONJUNTOS, no solo como cardinales. Y como phi es una biyeccion de
# {0,...,2^k-1} en si mismo, de ahi sale amas(k) == amenos(k) para todo k.
#
# Los dos indices de borde (r = 0 y r = 2^k - 1) son justamente los que phi
# intercambia, y hay que tratarlos aparte: se comprueba que NINGUNO de los dos
# es bueno nunca, en ninguno de los dos mapas.
#
# AVISO DE LA REGLA CERO, aplicado a este mismo fichero
# -----------------------------------------------------
#  - QUE MAPA USO: el del ATAJO en los dos lados, que es el del enunciado y el
#    de sucesiones.txt. NO el clasico. Con el clasico los numeros serian otros.
#  - ES PROMEDIO O COTA: ninguna de las dos. Es una igualdad exacta entre dos
#    conteos, y lo que se persigue es la razon, no el numero.
#  - CUANTIFICADOR ESCONDIDO: el barrido empieza en k = 1 y llega a K_MAX, o
#    sea que POR SI SOLO no dice nada de "para todo k". Quien dice "para todo
#    k" es el mecanismo (comprobacion 6), no el barrido.
#  - EL LIMITE DEL BARRIDO ELEGIDO REDONDO: K_MAX vale 21 a proposito, no 20
#    ni 16 ni 24. Aqui casi da igual porque la conclusion no se apoya en el
#    limite, pero se deja escrito que se penso.
#  - DIVISION DE ENTEROS NEGATIVOS: en Python -7 // 2 == -4, y eso estropearia
#    la conjugacion del paso 1. NO muerde, y conviene saber por que: el floor
#    solo actua sobre pares (donde es exacto), y sobre impares se divide
#    3n+1 (o 3n-1), que es PAR por construccion, tambien exacto. Se comprueba.
#
# NO SE USA UN SOLO FLOAT EN NADA QUE DECIDA. Aritmetica entera y conjuntos.

from array import array

# ----------------------------------------------------------------------
# CONSTANTES EDITABLES
# ----------------------------------------------------------------------

K_MAX = 21              # hasta que k se barre todo (no redondo a proposito)
K_FUERZA_BRUTA = 13     # hasta que k se recalcula todo con la implementacion lenta
K_SEMANTICA = 10        # hasta que k se comprueba que "bueno" = "se funden de verdad"
TOPE_CONJUGACION = 4000 # cuantos enteros se prueban en la identidad Tmenos = -Tmas(-n)
PASOS_CONJUGACION = 60  # cuantos pasos se iteran en esa identidad
EMES_DE_PRUEBA = (1, 2, 3, 7, 13, 100, 1234, 99999, 1000003)  # los m para la semantica

# Valores YA PUBLICADOS en sucesiones.txt, para k = 3, 4, 5, ...
# Se copian aqui como oraculo externo: si mi amas(k) no los reproduce,
# mi implementacion esta mal y no hay nada que discutir.
A_PUBLICADA = [1, 3, 8, 18, 39, 82, 170, 351, 721, 1476, 3012, 6130, 12450,
               25241, 51105, 103358, 208840, 421643, 850737, 1715546, 3457791,
               6966495, 14030369, 28247507, 56854178, 114400435, 230136995,
               462857658, 930718308, 1871137623]
A_PUBLICADA_DESDE_K = 3

# ----------------------------------------------------------------------
# LOS DOS MAPAS, un paso cada uno. Valen tambien para enteros negativos.
# ----------------------------------------------------------------------

def paso_mas(x):
    """Un paso del atajo de Collatz: x/2 si par, (3x+1)/2 si impar."""
    if x % 2 == 0:          # en Python, (-4) % 2 == 0, o sea que esto acierta con negativos
        return x // 2       # x par: la division es exacta, el floor no hace nada
    return (3 * x + 1) // 2  # x impar: 3x+1 es PAR, la division vuelve a ser exacta


def paso_menos(x):
    """Un paso del atajo de 3n-1: x/2 si par, (3x-1)/2 si impar."""
    if x % 2 == 0:
        return x // 2
    return (3 * x - 1) // 2  # x impar: 3x-1 es PAR, division exacta


POTENCIAS_DE_3 = [3 ** i for i in range(K_MAX + 2)]

# ----------------------------------------------------------------------
# IMPLEMENTACION A -- FUERZA BRUTA. Cada resto por separado, iterando.
# Es la lenta y la tonta, y por eso es la que arbitra.
# ----------------------------------------------------------------------

def tablas_por_fuerza_bruta(k, paso):
    """Devuelve dos listas: S_k(r) y T^k(r) para r = 0 .. 2^k - 1,
    calculadas iterando el mapa r veces sin ninguna formula."""
    total = 1 << k
    ese = [0] * total
    te = [0] * total
    for r in range(total):
        x = r
        impares = 0
        for _ in range(k):
            if x % 2 == 1:
                impares += 1
            x = paso(x)
        ese[r] = impares
        te[r] = x
    return ese, te

# ----------------------------------------------------------------------
# IMPLEMENTACION B -- INCREMENTAL. Sube de nivel k a nivel k+1 usando la
# formula afin  T^k(2^k*m + r) = 3^{S_k(r)}*m + T^k(r).
# No comparte ni una linea con la de arriba, y ademas usa la formula que
# la de arriba NO usa: si las dos coinciden, la formula esta bien.
# ----------------------------------------------------------------------

def subir_un_nivel(k, ese, te, paso):
    """De las tablas del nivel k saca las del nivel k+1."""
    total = 1 << k
    nueva_ese = array('q', bytes(8 * 2 * total))
    nueva_te = array('q', bytes(8 * 2 * total))
    for r in range(total):
        base_s = ese[r]
        base_t = te[r]
        tres = POTENCIAS_DE_3[base_s]
        for m in (0, 1):
            x = tres * m + base_t          # esto es T^k(2^k*m + r), por la formula afin
            posicion = r + m * total       # el resto nuevo, modulo 2^(k+1)
            nueva_ese[posicion] = base_s + (x & 1)
            nueva_te[posicion] = paso(x)
    return nueva_ese, nueva_te


def tablas_incrementales(k_max, paso):
    """Lista de tablas (S, T) para k = 0, 1, ..., k_max."""
    ese = array('q', [0])   # nivel 0: solo el resto 0, S = 0 y T^0(0) = 0
    te = array('q', [0])
    todas = [(ese, te)]
    for k in range(k_max):
        ese, te = subir_un_nivel(k, ese, te, paso)
        todas.append((ese, te))
    return todas

# ----------------------------------------------------------------------
# EL CRITERIO: que restos son BUENOS
# ----------------------------------------------------------------------

def conjunto_de_buenos(k, ese, te):
    """El conjunto de restos r modulo 2^k que cumplen el criterio."""
    total = 1 << k
    buenos = set()
    for r in range(total - 1):
        if ese[r] == ese[r + 1] and te[r] == te[r + 1]:
            buenos.add(r)
    # El borde: el vecino de 2^k - 1 es 2^k, que es m = 1 sobre la clase 0.
    if ese[total - 1] == ese[0] and te[total - 1] == POTENCIAS_DE_3[ese[0]] + te[0]:
        buenos.add(total - 1)
    return buenos


print("=" * 70)
print("espejoak.py -- amas(k) contra amenos(k): teorema o casualidad?")
print("=" * 70)
print("K_MAX = %d   (2^%d = %d restos en el ultimo nivel)" % (K_MAX, K_MAX, 1 << K_MAX))
print()

# ======================================================================
# LAS COMPROBACIONES VAN ANTES DE CUALQUIER CONCLUSION.
# Cada una corta con SystemExit si falla.
# ======================================================================

print("COMPROBACION 1 - la identidad de conjugacion  Tmenos^j(n) = -Tmas^j(-n)")
print("                 sobre TODO Z, con enteros exactos y sin floats.")
fallos = 0
comparaciones = 0
for n in range(-TOPE_CONJUGACION, TOPE_CONJUGACION + 1):
    a = n            # ira iterando con Tmenos
    b = -n           # ira iterando con Tmas
    for _ in range(PASOS_CONJUGACION):
        a = paso_menos(a)
        b = paso_mas(b)
        comparaciones += 1
        if a != -b:
            fallos += 1
    # y de paso, la paridad tiene que ir emparejada en todo momento
if fallos:
    raise SystemExit("FALLO: la conjugacion por el signo no se cumple (%d fallos)" % fallos)
print("   %d comparaciones, %d fallos.  Tmenos = nu . Tmas . nu es EXACTA." % (comparaciones, fallos))
print()

print("COMPROBACION 2 - la trampa del floor con negativos NO muerde")
print("                 (en Python -7 // 2 == -4, y eso estropearia lo de arriba)")
fallos = 0
for n in range(-TOPE_CONJUGACION, TOPE_CONJUGACION + 1):
    if n % 2 == 1:
        # sobre impares nunca se divide un impar: se divide 3n+1 y 3n-1, que son pares
        if (3 * n + 1) % 2 != 0 or (3 * n - 1) % 2 != 0:
            fallos += 1
    else:
        if n % 2 != 0:
            fallos += 1
if fallos:
    raise SystemExit("FALLO: hay divisiones no exactas (%d)" % fallos)
print("   0 fallos: el floor solo actua sobre divisiones que ya eran exactas.")
print()

print("COMPROBACION 3 - implementacion incremental contra fuerza bruta")
print("                 (dos implementaciones que no comparten codigo), k = 1..%d" % K_FUERZA_BRUTA)
tablas_mas = tablas_incrementales(K_MAX, paso_mas)
tablas_menos = tablas_incrementales(K_MAX, paso_menos)
discrepancias = 0
casos = 0
for k in range(1, K_FUERZA_BRUTA + 1):
    for nombre, paso, tablas in (("Tmas", paso_mas, tablas_mas),
                                 ("Tmenos", paso_menos, tablas_menos)):
        ese_b, te_b = tablas_por_fuerza_bruta(k, paso)
        ese_i, te_i = tablas[k]
        for r in range(1 << k):
            casos += 1
            if ese_b[r] != ese_i[r] or te_b[r] != te_i[r]:
                discrepancias += 1
if discrepancias:
    raise SystemExit("FALLO: incremental y fuerza bruta discrepan en %d casos" % discrepancias)
print("   %d restos recalculados de las dos maneras, %d discrepancias." % (casos, discrepancias))
print("   (de paso, esto valida la formula afin de Terras para LOS DOS mapas)")
print()

print("COMPROBACION 4 - los valores caben en int64 (nada se desborda en silencio)")
tope = 0
for k in range(K_MAX + 1):
    for tablas in (tablas_mas, tablas_menos):
        ese, te = tablas[k]
        tope = max(tope, max(te))
if tope >= (1 << 62):
    raise SystemExit("FALLO: T^k(r) se sale de int64 (maximo %d)" % tope)
print("   maximo T^k(r) encontrado: %d   (tope seguro 2^62 = %d)" % (tope, 1 << 62))
print()

print("COMPROBACION 5 - amas(k) contra los valores YA PUBLICADOS en sucesiones.txt")
buenos_mas = {}
buenos_menos = {}
for k in range(1, K_MAX + 1):
    ese, te = tablas_mas[k]
    buenos_mas[k] = conjunto_de_buenos(k, ese, te)
    ese, te = tablas_menos[k]
    buenos_menos[k] = conjunto_de_buenos(k, ese, te)
fallos = 0
comprobados = 0
for k in range(A_PUBLICADA_DESDE_K, K_MAX + 1):
    publicado = A_PUBLICADA[k - A_PUBLICADA_DESDE_K]
    mio = len(buenos_mas[k])
    comprobados += 1
    if publicado != mio:
        fallos += 1
        print("   k = %d : publicado %d, mio %d  <-- DISCREPA" % (k, publicado, mio))
if fallos:
    raise SystemExit("FALLO: mi amas(k) no reproduce la sucesion publicada")
print("   k = %d..%d : %d valores, todos identicos a los publicados." % (
    A_PUBLICADA_DESDE_K, K_MAX, comprobados))
print()

print("COMPROBACION 6 - el criterio significa lo que dice: los buenos SE FUNDEN")
print("                 de verdad, y los malos NO, en los dos mapas. k = 1..%d" % K_SEMANTICA)
#
# OJO CON COMO SE ENUNCIA ESTO. "Bueno" quiere decir "se funden PARA TODO m",
# no "se funden para algun m". Un resto malo con las dos pendientes distintas
# puede fundirse en UN m suelto (dos rectas de distinta pendiente se cortan una
# vez), y eso NO es un fallo: seria un fallo exigirle que no se funda nunca.
# Lo que si tiene que pasar es que a un resto malo se le encuentre ALGUN m
# donde NO se funde. Esos cruces sueltos se cuentan aparte y se informan.
fallos_buenos = 0
fallos_malos = 0
cruces_sueltos = 0
pruebas = 0
for k in range(1, K_SEMANTICA + 1):
    total = 1 << k
    for nombre, paso, buenos in (("Tmas", paso_mas, buenos_mas),
                                 ("Tmenos", paso_menos, buenos_menos)):
        conjunto = buenos[k]
        for r in range(total):
            cuantos_se_funden = 0
            for m in EMES_DE_PRUEBA:
                uno = total * m + r
                otro = uno + 1
                for _ in range(k):
                    uno = paso(uno)
                    otro = paso(otro)
                pruebas += 1
                if uno == otro:
                    cuantos_se_funden += 1
            if r in conjunto and cuantos_se_funden != len(EMES_DE_PRUEBA):
                fallos_buenos += 1     # bueno que NO se funde en algun m: eso si es un fallo
            if r not in conjunto:
                if cuantos_se_funden == len(EMES_DE_PRUEBA):
                    fallos_malos += 1  # malo que se funde en TODOS los m probados: fallo
                elif cuantos_se_funden:
                    cruces_sueltos += 1  # malo que se funde en algun m suelto: legitimo
if fallos_buenos or fallos_malos:
    raise SystemExit("FALLO: el criterio no coincide con la fusion real (%d + %d)"
                     % (fallos_buenos, fallos_malos))
print("   %d pares (2^k*m + r, +1) iterados a mano: %d fallos." % (pruebas, fallos_buenos + fallos_malos))
print("   Ni un resto bueno deja de fundirse, ni un resto malo se funde en todos los m.")
print("   (%d restos malos se funden en ALGUN m suelto; eso es correcto y esperado:" % cruces_sueltos)
print("    dos rectas de distinta pendiente se cortan una vez.)")
print()

print("COMPROBACION 7 - los dos indices de borde NUNCA son buenos, en ningun mapa")
fallos = 0
for k in range(1, K_MAX + 1):
    total = 1 << k
    for buenos in (buenos_mas, buenos_menos):
        if 0 in buenos[k]:
            fallos += 1
        if (total - 1) in buenos[k]:
            fallos += 1
if fallos:
    raise SystemExit("FALLO: algun borde salio bueno (%d casos); el mecanismo no cierra" % fallos)
print("   k = 1..%d, los dos mapas: r = 0 y r = 2^k - 1 nunca son buenos. 0 excepciones." % K_MAX)
print("   (razon: el vecino de 0 es 1, que es IMPAR de salida, luego S no puede valer 0;")
print("    y 2^k - 1 es impar de salida, luego tampoco.)")
print()

print("COMPROBACION 8 - LEMA 1 del mecanismo:  Smenos_k(r) == Smas_k((-r) mod 2^k)")
fallos = 0
casos = 0
for k in range(1, K_MAX + 1):
    total = 1 << k
    ese_mas = tablas_mas[k][0]
    ese_menos = tablas_menos[k][0]
    for r in range(total):
        nu = (total - r) % total
        casos += 1
        if ese_menos[r] != ese_mas[nu]:
            fallos += 1
if fallos:
    raise SystemExit("FALLO: el lema 1 se rompe en %d casos" % fallos)
print("   %d restos comprobados (k = 1..%d, EXHAUSTIVO), %d fallos." % (casos, K_MAX, fallos))
print()

print("COMPROBACION 9 - LEMA 2 del mecanismo:")
print("                 Tmenos^k(r) == 3^{Smas(nu(r))} - Tmas^k(nu(r))   para r >= 1")
print("                 Tmenos^k(0) == 0                                 para r = 0")
fallos = 0
casos = 0
for k in range(1, K_MAX + 1):
    total = 1 << k
    ese_mas, te_mas = tablas_mas[k]
    ese_menos, te_menos = tablas_menos[k]
    if te_menos[0] != 0 or ese_menos[0] != 0:
        fallos += 1
    for r in range(1, total):
        nu = total - r
        casos += 1
        if te_menos[r] != POTENCIAS_DE_3[ese_mas[nu]] - te_mas[nu]:
            fallos += 1
if fallos:
    raise SystemExit("FALLO: el lema 2 se rompe en %d casos" % fallos)
print("   %d restos comprobados (k = 1..%d, EXHAUSTIVO), %d fallos." % (casos, K_MAX, fallos))
print()

print("COMPROBACION 10 - LA BIYECCION, que es el mecanismo entero:")
print("                  BUENOS_menos(k)  ==  { 2^k - 1 - r : r en BUENOS_mas(k) }")
print("                  COMO CONJUNTOS, no como cardinales.")
fallos = 0
for k in range(1, K_MAX + 1):
    total = 1 << k
    imagen = set(total - 1 - r for r in buenos_mas[k])
    if imagen != buenos_menos[k]:
        fallos += 1
        print("   k = %d : la imagen NO es el otro conjunto  <-- ROTO" % k)
if fallos:
    raise SystemExit("FALLO: la biyeccion propuesta no manda un conjunto sobre el otro")
print("   k = 1..%d : la imagen coincide EXACTAMENTE, elemento a elemento, en los %d niveles."
      % (K_MAX, K_MAX))
print("   phi(r) = 2^k - 1 - r es el NOT bit a bit sobre k bits, y es una involucion.")
print()

# ======================================================================
# YA SE PUEDE CONCLUIR. Todo lo de arriba paso.
# ======================================================================

print("=" * 70)
print("RESULTADO")
print("=" * 70)
print()
print("  k     amas(k)    amenos(k)   iguales?   conjuntos iguales?   interseccion")
print("  " + "-" * 68)
conteos_iguales = True
conjuntos_iguales_en = []
conjuntos_distintos_en = []
for k in range(1, K_MAX + 1):
    a_mas = len(buenos_mas[k])
    a_menos = len(buenos_menos[k])
    if a_mas != a_menos:
        conteos_iguales = False
    mismos = (buenos_mas[k] == buenos_menos[k])
    if mismos:
        conjuntos_iguales_en.append(k)
    else:
        conjuntos_distintos_en.append(k)
    comunes = len(buenos_mas[k] & buenos_menos[k])
    print("  %2d  %10d   %10d   %-8s   %-18s   %d" % (
        k, a_mas, a_menos,
        "si" if a_mas == a_menos else "NO",
        "si" if mismos else "NO",
        comunes))
print()

if not conteos_iguales:
    raise SystemExit("Los conteos NO coinciden: la afirmacion es FALSA y hay que decirlo.")

print("LOS CONTEOS: identicos en los %d niveles barridos (k = 1..%d)." % (K_MAX, K_MAX))
if conjuntos_distintos_en:
    print("LOS CONJUNTOS: DISTINTOS. Primer k en que difieren: %d." % conjuntos_distintos_en[0])
    print("               Difieren en %d de los %d niveles barridos."
          % (len(conjuntos_distintos_en), K_MAX))
    k_ejemplo = conjuntos_distintos_en[0]
    print("               Ejemplo, k = %d:" % k_ejemplo)
    print("                 BUENOS_mas   = %s" % sorted(buenos_mas[k_ejemplo]))
    print("                 BUENOS_menos = %s" % sorted(buenos_menos[k_ejemplo]))
    print("                 y la imagen por phi de los primeros es exactamente los segundos.")
else:
    print("LOS CONJUNTOS: iguales en todos los niveles barridos.")
print("Niveles donde los conjuntos coinciden: %s" % (conjuntos_iguales_en if conjuntos_iguales_en else "ninguno"))
print()

# Una ultima cosa que separa "teorema" de "casualidad numerica": si la igualdad
# viniera de una simetria del propio conjunto BUENOS_mas (o sea, si ese conjunto
# fuera invariante por phi), entonces no habria nada que explicar y la biyeccion
# seria trivial. Se mide que NO lo es.
invariantes = []
for k in range(1, K_MAX + 1):
    if buenos_mas[k] and set((1 << k) - 1 - r for r in buenos_mas[k]) == buenos_mas[k]:
        invariantes.append(k)
print("Control: en que niveles BUENOS_mas es invariante por phi (o sea, en cuantos")
print("la biyeccion seria trivial porque manda el conjunto sobre si mismo)?")
print("   niveles no vacios e invariantes: %s" % (invariantes if invariantes else "NINGUNO"))
print("   O sea que phi mueve el conjunto de verdad: no es la identidad disfrazada.")
print()

print("=" * 70)
print("VEREDICTO: TEOREMA, no casualidad.")
print("=" * 70)
print("""
La razon es estructural y no depende de k:

  1. Tmenos(n) = -Tmas(-n) como identidad EXACTA sobre Z (comprobacion 1).
     El mapa 3n-1 no es otra regla: es Collatz visto del otro lado del cero.

  2. Cambiar el signo respeta la paridad, luego respeta S_k (comprobacion 8),
     y por la formula afin de Terras traduce T^k con un 3^S y un signo
     (comprobacion 9).

  3. El cambio de signo manda la pareja de vecinos (r, r+1) en la pareja de
     vecinos (-r-1, -r). Escrito modulo 2^k eso es la involucion
     phi(r) = 2^k - 1 - r, el NOT bit a bit.

  4. En la condicion de ser bueno, el factor 3^S se cancela porque la propia
     condicion obliga a que los dos exponentes coincidan. Lo que queda es,
     literalmente, la condicion de bondad del otro mapa en phi(r).

  5. Los dos unicos indices que phi no puede emparejar dentro del rango
     -- el 0 y el 2^k - 1 -- no son buenos NUNCA en ninguno de los dos mapas
     (comprobacion 7), asi que no hay resto suelto que estropee el conteo.

Luego BUENOS_menos(k) = phi(BUENOS_mas(k)) con phi biyectiva, y por tanto
amas(k) = amenos(k) PARA TODO k >= 1. No hay ningun k grande donde pueda
romperse, porque el argumento no mira el tamano de k en ningun sitio.

CONSECUENCIA PARA EL REPO: que amenos(k) saliera identica NO era una segunda
medicion independiente que "confirmara" nada, ni tampoco una casualidad
sospechosa. Era la MISMA sucesion escrita al reves bit a bit. El pendiente de
la bitacora -- "llegar a k >= 20 y decidir si es teorema o se rompe" -- queda
cerrado sin gastar la maquina: es teorema, y ninguna k lo va a romper.

LO QUE ESTO NO DICE: no dice nada sobre si a(k) merece o no estar en OEIS,
ni sobre la conjetura de Wu, ni sobre Collatz. Solo dice por que los dos
conteos son forzosamente el mismo numero.
""")
