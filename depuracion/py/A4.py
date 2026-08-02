# A4.py -- Agente 2 (independiente). Verificacion del item A4.
#
# ENUNCIADO: eps = ln( 2^B / (3^A * n) ) es identicamente igual a la suma de
# ln(1 + 1/(3x)) sobre los VALORES impares x que pisa la trayectoria (sin el 1 final).
# Mapa CLASICO: par -> n/2 ; impar -> 3n+1. Trayectoria completa de n hasta 1.
# A = numero de pasos impares, B = numero de pasos pares.
#
# Como ln es inyectiva sobre positivos, el enunciado equivale EXACTAMENTE a la
# identidad multiplicativa en racionales:
#
#     2^B / (3^A * n)  ==  producto de (1 + 1/(3x))  sobre los impares x
#
# y ESA es la que se verifica aqui, con fractions.Fraction, sin un solo float
# en la cadena que decide.
#
# DERIVACION PROPIA (desde la definicion del mapa, sin mirar el repo):
#   valor final / valor inicial = 1/n  = producto de los factores de cada paso.
#   paso par:    factor 1/2                          (B veces)
#   paso impar:  factor (3x+1)/x = 3 * (1 + 1/(3x))  (A veces, uno por impar pisado)
#   =>  1/n = (1/2)^B * 3^A * PROD(1 + 1/(3x))
#   =>  PROD(1 + 1/(3x)) = 2^B / (3^A * n)
# La derivacion vale para todo n cuya trayectoria termine en 1 (todo n del rango
# barrido: la terminacion se comprueba empiricamente al iterar).

from fractions import Fraction

def pasos_y_producto(n):
    """Itera el mapa CLASICO desde n hasta 1.
    Devuelve (A, B, producto exacto de (1 + 1/(3x)) sobre los impares pisados,
    lista de impares pisados). El 1 final no recibe paso y no entra."""
    A = 0
    B = 0
    prod = Fraction(1)
    impares = []
    x = n
    while x != 1:
        if x % 2 == 0:
            B += 1
            x = x // 2
        else:
            A += 1
            impares.append(x)
            prod *= 1 + Fraction(1, 3 * x)
            x = 3 * x + 1
    return A, B, prod, impares

fallos = 0
casos = 0

def comprobar(n):
    global fallos, casos
    A, B, prod, impares = pasos_y_producto(n)
    lado_izq = Fraction(2 ** B, 3 ** A * n)
    casos += 1
    if lado_izq != prod:
        fallos += 1
        print("FALLO en n =", n, " 2^B/(3^A n) =", lado_izq, " producto =", prod)
    return A, B, prod

# ---- BORDES primero: donde se rompen los enunciados de este repo ----
print("== bordes ==")

# n = 1: trayectoria vacia, A = B = 0, producto vacio = 1, 2^0/(3^0*1) = 1
A, B, prod = comprobar(1)
print("n=1   -> A=%d B=%d producto=%s  (esperado 1, suma vacia)" % (A, B, prod))
if not (A == 0 and B == 0 and prod == 1):
    raise SystemExit("BORDE n=1 ROTO: A,B,producto = %d,%d,%s" % (A, B, prod))

# n = 2: un paso par, ningun impar
A, B, prod = comprobar(2)
print("n=2   -> A=%d B=%d producto=%s" % (A, B, prod))
if not (A == 0 and B == 1 and prod == 1):
    raise SystemExit("BORDE n=2 ROTO")

# potencias de 2: A = 0, producto vacio, 2^B/n = 1 exacto
for k in range(1, 21):
    comprobar(2 ** k)
print("potencias de 2 hasta 2^20: comprobadas (A=0, producto=1)")

# 2^k - 1 (los que mas suben al principio), k = 2..16
for k in range(2, 17):
    comprobar(2 ** k - 1)
print("2^k - 1 para k=2..16: comprobados")

# el 27 y el 703 (trayectorias largas famosas), y el 221 del repo... no:
# el 221 es dato del repo; uso 27, 703, 6171, 77031 que son estandar del mapa.
for n in (3, 5, 7, 27, 703, 6171, 77031):
    A, B, prod = comprobar(n)
print("impares de trayectoria larga (3,5,7,27,703,6171,77031): comprobados")

# un caso a mano, verificable con lapiz: n = 5
# 5 ->16 ->8 ->4 ->2 ->1 : A=1, B=4, impares = [5]
# 2^4/(3^1*5) = 16/15 ; 1 + 1/15 = 16/15. Igual.
A, B, prod, impares = pasos_y_producto(5)
if not (A == 1 and B == 4 and impares == [5] and prod == Fraction(16, 15)):
    raise SystemExit("CASO A MANO n=5 ROTO")
print("n=5 a mano: A=1 B=4 impares=[5] producto=16/15  -> exacto")

# ---- BARRIDO CENTRAL: n = 1 .. 30000, exacto ----
print("== barrido n = 1 .. 30000 ==")
eps_max = Fraction(0)
n_eps_max = 1
for n in range(1, 30001):
    A, B, prod = comprobar(n)
    # de paso: el producto siempre >= 1 (cada factor > 1), o sea eps >= 0
    if prod < 1:
        raise SystemExit("PRODUCTO < 1 en n = %d (imposible por construccion)" % n)
    if prod - 1 > eps_max - 1 and prod > eps_max:
        eps_max = prod
        n_eps_max = n

print("casos comprobados en total:", casos)
print("fallos:", fallos)

# ---- semillas grandes sueltas (bits altos), pocas y baratas ----
print("== semillas grandes ==")
grandes = [2**40 + 1, 2**60 + 1, 3**25, 10**15 + 7, 2**50 - 1]
for n in grandes:
    comprobar(n)
print("5 semillas de 40-80 bits: comprobadas")
print("casos totales:", casos, " fallos totales:", fallos)

# residuo maximo del barrido (solo informativo, en float SOLO para imprimir)
import math
print("maximo producto 2^B/(3^A n) del barrido: n=%d, valor=%.10f, eps=%.10f nats"
      % (n_eps_max, float(eps_max), math.log(float(eps_max))))

if fallos == 0:
    print("VEREDICTO: identidad multiplicativa EXACTA en todos los casos -> el")
    print("enunciado logaritmico es identicamente cierto en el rango verificado,")
    print("y la derivacion de una linea lo da para todo n que llegue a 1.")
else:
    raise SystemExit("HAY FALLOS: %d" % fallos)
