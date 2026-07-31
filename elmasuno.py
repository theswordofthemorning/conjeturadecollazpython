# elmasuno.py
#
# EL «+1», CONTADO UNA SOLA VEZ.
#
# El CLAUDE.md de este repo dice que el «+1» del 3n+1 aparece TRES veces,
# como el mismo estorbo medido en tres sitios distintos, y pregunta si se
# pueden escribir como una sola cantidad. Las tres son:
#
#   (a) EL GROSOR DE LA LAMINA (collazlamina.py, mapahilos.py):
#           eps = ln( 2^B / (3^A * n) )
#       acotado por ln(Res(993)) = 0,225654. Es el logaritmo del residuo
#       de Roosendaal.
#
#   (b) EL «+2» DEL ESPEJO EN BASE 2 (mallaespejo2.py):
#           T(2^k - n) = 3*2^k + 2 - T(n)      para n impar
#
#   (c) EL SOBRANTE DE LA FRACCION IMPAR (sesion del 30-07-2026):
#           S = suma de ln(1 + 1/(3x)) sobre los valores impares x
#       que cerraba la contabilidad de la paridad
#           -ln(n) = I*ln(3/2) + P*ln(1/2) + S
#       con un residuo de 1,7e-7.
#
# ESTE FICHERO DEMUESTRA QUE (a) Y (c) NO SON DOS COSAS PARECIDAS:
# SON EXACTAMENTE LA MISMA SUMA. No aproximadamente. Identicamente.
#
# ---------------------------------------------------------------------------
# LA DERIVACION ENTERA, EN TEXTO PLANO. Son dos lineas.
# ---------------------------------------------------------------------------
#
# Mira la trayectoria clasica como un PRODUCTO de factores, no como una lista
# de numeros. Cada paso multiplica el valor actual por algo:
#
#   x PAR   ->  x/2          el factor es      1/2
#   x IMPAR ->  3x+1         el factor es      (3x+1)/x  =  3 * (1 + 1/(3x))
#
# Esa segunda igualdad es la clave y es aritmetica de primaria: se multiplica
# arriba y abajo por 3 y se parte la fraccion en dos.
#
#       3x + 1     3*(3x + 1)         3x + 1            3x       1
#       ------  =  ----------  =  3 * ------  =  3 * ( ---- + ---- )
#          x           3x               3x              3x      3x
#
#                                    =  3 * (1 + 1/(3x))
#
# O sea: un paso impar NO multiplica por 3. Multiplica por 3 y un pelin mas.
# Ese pelin es el «+1».
#
# Ahora multiplica TODOS los factores de la trayectoria. La trayectoria va de
# n a 1, asi que el producto de todos los factores vale exactamente 1/n:
#
#       1/n  =  (1/2)^B  *  producto sobre los impares de  3*(1 + 1/(3x))
#            =  (1/2)^B  *  3^A  *  producto de (1 + 1/(3x))
#
# donde A = veces que se aplico 3n+1, B = veces que se aplico n/2. Despejando
# el producto:
#
#       ****************************************************************
#       *        2^B                                                   *
#       *     ---------  =  PRODUCTO de (1 + 1/(3*x_i))  sobre los      *
#       *      3^A * n                        A valores impares         *
#       ****************************************************************
#
# y tomando logaritmos en los dos lados:
#
#       eps  =  ln( 2^B / (3^A * n) )  =  suma de ln(1 + 1/(3*x_i))  =  S
#
# El grosor de la lamina ES el sobrante de la fraccion impar. Misma suma,
# termino a termino, no dos cantidades parecidas que se acercan.
#
# Y la contabilidad de (c) estaba escrita con el mapa del ATAJO (I pasos
# impares, P pasos pares), mientras que (a) esta escrita con el mapa CLASICO
# (A y B). Los dos juegos de coordenadas se traducen solos:
#
#       I = A            (los pasos impares son los mismos en los dos mapas)
#       P = B - A        (el clasico parte cada paso del atajo en dos)
#
#       A*ln3 - B*ln2  =  I*ln(3/2) + P*ln(1/2)
#
# Por eso -ln(n) = I*ln(3/2) + P*ln(1/2) + S es la MISMA ecuacion que
# -ln(n) = A*ln3 - B*ln2 + eps. El residuo 1,7e-7 que se midio entonces no
# era el error de la identidad: era el error de sumar millones de logaritmos
# en coma flotante. Aqui se comprueba en racionales exactos y da 0.
#
# ---------------------------------------------------------------------------
# TRES COSAS QUE CAEN GRATIS DE LA IDENTIDAD
# ---------------------------------------------------------------------------
#
# 1. POR QUE LA LAMINA NO TIENE NADA POR DEBAJO DEL PLANO. Es la pregunta que
#    collazlamina.py contestaba MIDIENDO (6.555 pares, ninguno negativo). Con
#    la identidad se contesta en una linea: cada factor (1 + 1/(3x)) es
#    ESTRICTAMENTE MAYOR QUE 1 porque x es un entero positivo. Un producto de
#    cosas mayores que 1 es mayor que 1, luego su logaritmo es positivo, luego
#    eps > 0 SIEMPRE. No hay nada que medir. Y vale 0 exactamente cuando A=0,
#    o sea cuando n es una potencia de 2 y no hay ni un solo «+1».
#
# 2. DE DONDE SALE EL TAMAÑO DE eps, Y NO ES DE DONDE PARECE. Cada termino
#    ln(1 + 1/(3x)) vale casi 1/(3x): decrece con x. Luego lo que engorda eps
#    NO son los numeros grandes por los que sube la trayectoria, sino los
#    IMPARES PEQUEÑOS por los que pasa — y esos estan al FINAL del camino,
#    no al principio. Medido abajo en el 993: los cinco impares mas chicos
#    que pisa (5, 7, 11, 13, 17) se llevan el 82% del grosor, y el propio
#    993 aporta el 0,15%. Por eso eps esta acotado en la practica: todas las
#    trayectorias terminan pisando los mismos numeros chicos. Esto NO
#    demuestra el techo de Roosendaal, solo dice donde vive.
#
# 3. EL «+1» NO APARECE TRES VECES, APARECE DOS. Ver las conclusiones abajo.
#
# No dibuja nada. Solo numeros. Las comprobaciones cortan con SystemExit.

import math
from fractions import Fraction


# ---------------------------------------------------------------------------
# Cambia esto aqui, guarda, y dale a Ctrl+B en Sublime.
# ---------------------------------------------------------------------------

HASTA_EXACTO = 20000       # barrido de la comprobacion exacta, 1..HASTA_EXACTO
HASTA_MAXIMO = 200000      # barrido para buscar el maximo de eps
GRANDES = [27, 703, 871, 6171, 77031, 100009, 993, 1986, 3972,
           2 ** 31 - 1, 2 ** 40 + 1]      # a mano, para salir del rango chico

RES_993 = 1.2531421442887503     # el residuo de Roosendaal, maximo conjeturado

L2, L3 = math.log(2), math.log(3)


def secuencia_de(n):
    camino = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        camino.append(n)
    return camino


def recorrido(n):
    """Camina la trayectoria clasica sin un solo float y devuelve:

       A   = veces que se aplico 3n+1
       B   = veces que se aplico n/2
       num, den  =  el producto de (3x+1)/(3x) sobre los A valores impares,
                    guardado como dos enteros (se hace un solo Fraction al
                    final: multiplicar Fraction a Fraction seria un gcd por
                    paso, y no hace falta)."""
    A = B = 0
    num = den = 1
    x = n
    while x != 1:
        if x % 2 == 1:
            num *= 3 * x + 1
            den *= 3 * x
            x = 3 * x + 1
            A += 1
        else:
            x //= 2
            B += 1
    return A, B, num, den


def decimal_de(fraccion, cifras):
    """Pasa una Fraction a texto decimal con las cifras que se pidan, a mano
    y con enteros, para no perder precision por el camino."""
    escalado = fraccion.numerator * 10 ** cifras // fraccion.denominator
    texto = str(escalado)
    return texto[:-cifras] + "," + texto[-cifras:]


def cuenta(n):
    """Solo A y B, sin el producto. Es lo que se usa en el barrido largo."""
    A = B = 0
    x = n
    while x != 1:
        if x % 2 == 1:
            x = 3 * x + 1
            A += 1
        else:
            x //= 2
            B += 1
    return A, B


print("EL «+1» DEL 3n+1, CONTADO UNA SOLA VEZ")
print()
print("  Hipotesis:  ln( 2^B / (3^A * n) )  ==  suma de ln(1 + 1/(3*x_i))")
print("  o sea: el grosor de la lamina y el sobrante de la fraccion impar")
print("  no son parientes, son el mismo numero.")
print()


# ---------------------------------------------------------------------------
# COMPROBACION 1 -- la identidad, en racionales exactos, sin un solo float
# ---------------------------------------------------------------------------
#
# Se compara la fraccion 2^B / (3^A * n) contra el producto de (3x+1)/(3x),
# como objetos Fraction. Tienen que ser LA MISMA fraccion, no una cerca de
# la otra.

casos = list(range(1, HASTA_EXACTO + 1)) + GRANDES

fallos = 0
primer_fallo = None
for n in casos:
    A, B, num, den = recorrido(n)
    izquierda = Fraction(2 ** B, 3 ** A * n)
    derecha = Fraction(num, den)
    if izquierda != derecha:
        fallos += 1
        if primer_fallo is None:
            primer_fallo = n

print("COMPROBACION 1 -- la identidad es exacta, en Fraction")
print(f"  numeros probados: {len(casos):,}  "
      f"(el 1 al {HASTA_EXACTO:,}, mas {len(GRANDES)} grandes a mano)")
print(f"  el mayor de los grandes: {max(GRANDES):,}")
print(f"  fallos: {fallos}")
if fallos:
    raise SystemExit(f"La identidad falla, primero en n={primer_fallo}. "
                     "No sigas.")


# ---------------------------------------------------------------------------
# COMPROBACION 2 -- eps > 0 siempre, y por que es trivial
# ---------------------------------------------------------------------------
#
# Cada factor del producto es (1 + 1/(3x)) con x entero positivo, luego cada
# factor es > 1. El producto de cosas > 1 es > 1. Fin. Aqui se comprueba
# ademas que el unico caso de igualdad es A = 0 (las potencias de 2).

negativos = 0
ceros = []
factor_minimo_mal = 0
for n in casos:
    A, B, num, den = recorrido(n)
    res = Fraction(num, den)          # = 2^B / (3^A * n)
    if res < 1:
        negativos += 1
    if res == 1:
        ceros.append(n)
    if A > 0 and num <= den:
        factor_minimo_mal += 1

potencias_de_2 = [n for n in casos if (n & (n - 1)) == 0]

print()
print("COMPROBACION 2 -- eps nunca es negativo, y eso es una linea de algebra")
print("  cada factor es (1 + 1/(3x)) con x entero positivo -> cada factor > 1")
print("  producto de cosas > 1 es > 1 -> su logaritmo es > 0 -> eps > 0")
print(f"  casos con eps < 0 : {negativos}")
print(f"  casos con eps == 0: {len(ceros)}   y son exactamente las potencias"
      f" de 2: {sorted(set(ceros)) == sorted(set(potencias_de_2))}")
print(f"  casos con A > 0 y producto no estrictamente mayor que 1:"
      f" {factor_minimo_mal}")
if negativos or factor_minimo_mal:
    raise SystemExit("Un eps salio negativo. Eso rompe la lamina entera.")
if sorted(set(ceros)) != sorted(set(potencias_de_2)):
    raise SystemExit("El caso de igualdad no son las potencias de 2. Mira eso.")


# ---------------------------------------------------------------------------
# COMPROBACION 3 -- las dos contabilidades son la misma, traducidas
# ---------------------------------------------------------------------------
#
# (a) esta escrita en el mapa clasico (A, B); (c) en el mapa del atajo (I, P).
# Se comprueba que I == A y P == B - A contando de verdad los pasos del atajo,
# y que las dos formas de escribir la ecuacion dan el mismo numero.

fallos_traduccion = 0
peor_desvio = 0.0
for n in casos:
    A, B, num, den = recorrido(n)

    # el mapa del atajo, contado a mano: impar -> (3x+1)/2, par -> x/2
    I = P = 0
    x = n
    while x != 1:
        if x % 2 == 1:
            x = (3 * x + 1) // 2
            I += 1
        else:
            x //= 2
            P += 1

    if I != A or P != B - A:
        fallos_traduccion += 1

    # las dos escrituras de la misma ecuacion, en float, solo para verlas
    eps = B * L2 - A * L3 - math.log(n)
    izquierda = -math.log(n)
    derecha = I * math.log(1.5) + P * math.log(0.5) + eps
    peor_desvio = max(peor_desvio, abs(izquierda - derecha))

print()
print("COMPROBACION 3 -- las dos contabilidades son la misma, traducidas")
print("  I = A   y   P = B - A     (atajo contra clasico)")
print(f"  fallos de traduccion: {fallos_traduccion}")
print("  la ecuacion de (c),  -ln(n) = I*ln(3/2) + P*ln(1/2) + eps,")
print("  con el eps de (a),  eps = B*ln2 - A*ln3 - ln(n)  metido dentro")
print(f"  peor desvio de los dos lados: {peor_desvio:.3e}"
      f"   (es ruido de float; la identidad de la comprobacion 1 es exacta)")
if fallos_traduccion:
    raise SystemExit("La traduccion entre mapas falla. No sigas.")


# ---------------------------------------------------------------------------
# COMPROBACION 4 -- reproduce los numeros ya publicados en el CLAUDE.md
# ---------------------------------------------------------------------------
#
# El maximo de eps hasta 200.000 tiene que estar en n = 993 (y en sus dobles),
# y valer ln(1,253142144) = 0,225654. La comparacion se hace ENTERA, cruzando
# multiplicaciones, para no fiarse de la coma flotante:
#
#     2^B / (3^A n)  >  2^Bm / (3^Am m)   <=>   2^B * 3^Am * m  >  2^Bm * 3^A * n

mejor = None
empates = []
for n in range(2, HASTA_MAXIMO + 1):
    A, B = cuenta(n)
    if mejor is None:
        mejor = (A, B, n)
        empates = [n]
        continue
    Am, Bm, m = mejor
    izquierda = 2 ** B * (3 ** Am * m)
    derecha = 2 ** Bm * (3 ** A * n)
    if izquierda > derecha:
        mejor = (A, B, n)
        empates = [n]
    elif izquierda == derecha:
        empates.append(n)

Am, Bm, m = mejor
res_exacto = Fraction(2 ** Bm, 3 ** Am * m)
eps_maximo = math.log(float(res_exacto))
techo = math.log(RES_993)

print()
print("COMPROBACION 4 -- reproduce el residuo de Roosendaal publicado")
print(f"  barrido exacto de 2 a {HASTA_MAXIMO:,}, comparando enteros")
print(f"  el maximo de eps se alcanza en n = {m}   (A={Am}, B={Bm})")
print(f"  y lo empatan {len(empates)}: {empates}")
print(f"  o sea el 993 y sus dobles, que es lo que dice el CLAUDE.md")
print(f"  la fraccion exacta: 2^{Bm} / (3^{Am} * {m}) =")
print(f"     {res_exacto.numerator} / {res_exacto.denominator}")
print(f"  en decimal, con veinte cifras: {decimal_de(res_exacto, 20)}")
print(f"  eps maximo = ln(Res) = {eps_maximo:.9f}")
print(f"  publicado    ln(Res(993)) = {techo:.9f}   (CLAUDE.md: 0,225654)")
print(f"  diferencia: {abs(eps_maximo - techo):.3e}")
print()
print("  DE PROPINA, UNA ERRATA EN UNA CONSTANTE DEL REPO. mapahilos.py")
print("  guarda RES_993 = 1.2531421442887503, y el valor exacto es")
print(f"     {decimal_de(res_exacto, 16)}")
print("  Coinciden en las nueve cifras publicadas (1,253142144) y se separan")
print("  en la decima: ...4428875 contra ...4439507. No cambia nada de lo")
print("  medido -el techo en logaritmos sigue siendo 0,225654- pero la")
print("  constante literal esta mal a partir de la decima cifra.")
if m != 993:
    raise SystemExit(f"El maximo no cae en 993 sino en {m}. Mira eso primero.")
if abs(eps_maximo - techo) > 1e-9:
    raise SystemExit("El maximo no coincide con el valor publicado.")
if empates != [993 * 2 ** k for k in range(len(empates))]:
    raise SystemExit("Los empates no son los dobles de 993. Mira eso.")


# ---------------------------------------------------------------------------
# COMPROBACION 5 -- de donde sale el grosor, y no es de donde parece
# ---------------------------------------------------------------------------
#
# Cada termino vale casi 1/(3x), asi que manda el impar MAS PEQUEÑO que pisa
# la trayectoria, no el mas grande. Y los impares chicos estan al FINAL del
# camino. Se mide en el 993, que es el campeon.

seq = secuencia_de(993)
impares = [x for x in seq[:-1] if x % 2 == 1]
terminos = [math.log(1 + 1 / (3 * x)) for x in impares]
suma = sum(terminos)
ordenados = sorted(zip(terminos, impares), reverse=True)

print()
print("COMPROBACION 5 -- el reparto del grosor en el campeon, n = 993")
print(f"  pasos impares: {len(impares)}   suma de sus ln(1+1/(3x)):"
      f" {suma:.9f}")
print(f"  eps calculado como ln(2^B/(3^A n)):        {eps_maximo:.9f}")
print(f"  diferencia (ruido de float): {abs(suma - eps_maximo):.3e}")
print(f"  el arranque, {impares[0]}, aporta {terminos[0]:.9f}"
      f"  ->  solo el {100*terminos[0]/suma:.2f}% del total")
print("  los que mandan son los impares MAS CHICOS, o sea el final del camino:")
for t, x in ordenados[:5]:
    print(f"     x = {x:>3}   aporta {t:.9f}   el {100*t/suma:>5.2f}%")
print(f"  esos cinco juntos: el {100*sum(t for t,_ in ordenados[:5])/suma:.2f}%"
      f" del grosor entero")
if abs(suma - eps_maximo) > 1e-9:
    raise SystemExit("La suma de terminos no reconstruye eps. No sigas.")


# ---------------------------------------------------------------------------
# LAS CONCLUSIONES. Van despues de las comprobaciones, nunca antes.
# ---------------------------------------------------------------------------

print()
print("=" * 74)
print("CONCLUSIONES")
print("=" * 74)
print()
print("1. (a) Y (c) SON EL MISMO NUMERO, NO DOS PARECIDOS.")
print("   El grosor de la lamina eps = ln(2^B/(3^A n)) y el sobrante de la")
print("   fraccion impar S = suma de ln(1+1/(3x)) son identicos, termino a")
print(f"   termino, en los {len(casos):,} casos probados en racionales exactos,")
print("   0 fallos. Y la razon es de dos lineas: un paso impar multiplica por")
print("   3*(1 + 1/(3x)), no por 3; el producto de toda la trayectoria vale")
print("   1/n; se despeja. El residuo 1,7e-7 que se habia medido era error de")
print("   coma flotante, no del enunciado.")
print()
print("2. EL «+1» NO APARECE TRES VECES. APARECE DOS.")
print("   El conteo del CLAUDE.md hay que corregirlo: el grosor 0,2286 de la")
print("   lamina y la desviacion -0,0035 de la fraccion impar eran la misma")
print("   aparicion contada dos veces, en dos sistemas de coordenadas. Quedan:")
print("     - eps, la suma acumulada sobre la trayectoria (a == c)")
print("     - el «+2» del espejo en base 2 (b)")
print()
print("3. Y (b) ES PARIENTE, PERO NO ES LO MISMO. El argumento:")
print("   el «+2» del espejo sale de 3(2^k - n) + 1 = 3*2^k + 2 - (3n+1), o")
print("   sea de aplicar el «+1» a los DOS lados de una reflexion; es exacto")
print("   para UN paso y no esta sumado sobre nada. eps, en cambio, es la")
print("   ACUMULACION del mismo estorbo a lo largo de A pasos. Uno es el «+1»")
print("   visto una vez y en aritmetica entera; el otro es su integral y vive")
print("   en los logaritmos. Meterlos en el mismo saco seria justo el tipo de")
print("   union por parecido que este repo se ha propuesto no hacer.")
print("   La prueba de que no son intercambiables ya estaba medida: el puente")
print("   del espejo2 se rompe al segundo paso (correlacion +0,06), mientras")
print("   que eps es exacto sobre la trayectoria entera.")
print()
print("4. ESTO NO ES UN PROMEDIO NI UNA COTA: ES UNA IDENTIDAD.")
print("   La pregunta que se hace siempre el repo -«es un promedio o es una")
print("   cota?»- tiene aqui una tercera respuesta, y es la mas fuerte de las")
print("   tres. Un promedio no demuestra ningun caso. Una cota vale para todos")
print("   los casos pero solo por un lado. Una identidad vale para todos los")
print("   casos por los dos lados: es una IGUALDAD, cierta para cada n, no una")
print("   tendencia. Se demuestra en dos lineas y se ha verificado en")
print("   racionales exactos.")
print()
print("5. Y LO QUE REGALA: la lamina no tiene nada por debajo del plano PORQUE")
print("   cada factor es mayor que 1. collazlamina.py lo habia MEDIDO en 6.555")
print("   pares; ahora esta DEMOSTRADO en una linea, para todos los n a la vez.")
print("   Eso es lo que gana el repo con esto: un negativo medido se convierte")
print("   en un teorema pequeño.")
print()
print("   Y de paso corrige la intuicion de donde vive el grosor: no lo ponen")
print("   los numeros grandes por los que sube la trayectoria, sino los")
print("   impares CHICOS del final. En el 993 los cinco menores se llevan el")
print("   82%; el propio 993 aporta el 0,15%. El «+1» pesa donde el numero es")
print("   pequeño, que es justo donde la trayectoria ya esta acabando.")
print()
print("6. HONESTIDAD SOBRE SI ESTO «UNIFICA»: unifica de verdad DOS de las")
print("   tres apariciones, y las unifica hacia abajo. No es que dos fenomenos")
print("   distintos resulten tener una causa comun: es que eran el mismo")
print("   fenomeno escrito en dos coordenadas, y nadie lo habia notado porque")
print("   uno se medio sobre pares de una trayectoria y el otro sobre millones")
print("   de trayectorias a la vez. Es contabilidad, no descubrimiento. Pero")
print("   es contabilidad que CORRIGE UN CONTEO PUBLICADO en el CLAUDE.md, y")
print("   convierte una medicion en una demostracion. Y no toca la conjetura:")
print("   que eps > 0 siempre es trivial; que eps este ACOTADO por 0,225654")
print("   sigue siendo la conjetura de Roosendaal, y no se ha movido un milimetro.")
