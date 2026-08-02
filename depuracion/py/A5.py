# A5 - verificacion independiente (agente 2, Python, sin mirar el repo)
#
# ENUNCIADO LITERAL DE LA BASE:
#   "eps > 0 siempre, y vale 0 exactamente en las potencias de 2"
# con eps = ln(2^B / (3^A * n)) sobre la trayectoria COMPLETA hasta 1,
# mapa CLASICO: par -> n/2 ; impar -> 3n+1.
#   A = numero de pasos impares (aplicaciones de 3n+1)
#   B = numero de pasos pares  (aplicaciones de n/2)
#
# Como ln es monotona y ln(1)=0, el enunciado equivale (sin un solo float) a:
#   Res(n) = 2^B / (3^A * n)  >=  1,  con igualdad exactamente en n = 2^m.
# Todo lo que decide va en enteros y Fraction.
#
# Derivacion propia del argumento (para contrastarla, no para sustituir la medida):
#   en un paso impar   x -> 3x+1 = 3x * (1 + 1/(3x))
#   en un paso par     x -> x/2
#   luego 1 = valor final = n * 3^A * PROD(1+1/(3x)) / 2^B
#   =>  Res(n) = 2^B/(3^A n) = PROD sobre pasos impares de (1 + 1/(3x))
#   cada factor > 1 (x entero >= 1), asi que Res > 1 si A >= 1 y Res = 1 si A = 0.
#   Y A = 0 exactamente cuando la trayectoria solo divide, o sea n = 2^m.
# Esa cadena se comprueba abajo con Fraction exacto, no se da por buena.

from fractions import Fraction
import sys

LIMITE = 100000          # rango del barrido principal, declarado

def tray_clasica(n):
    """Cuenta (A, B) y devuelve la lista de valores impares visitados (antes de 3x+1)."""
    A = 0
    B = 0
    impares = []
    x = n
    while x != 1:
        if x % 2 == 0:
            x //= 2
            B += 1
        else:
            impares.append(x)
            x = 3 * x + 1
            A += 1
    return A, B, impares

def es_potencia_de_2(n):
    return n >= 1 and (n & (n - 1)) == 0

fallos_cota = 0          # Res < 1
fallos_igualdad = 0      # (Res == 1) no coincide con (n potencia de 2)
fallos_producto = 0      # Res != producto de factores (1+1/(3x))
fallos_A0 = 0            # (A == 0) no coincide con (n potencia de 2)
igualdades = []          # los n con Res == 1

# el producto exacto es caro en n grandes; se comprueba en un subrango + bordes
RANGO_PRODUCTO = 2000

for n in range(1, LIMITE + 1):
    A, B, impares = tray_clasica(n)
    # Res exacto como Fraction de enteros
    res = Fraction(2 ** B, (3 ** A) * n)
    pot2 = es_potencia_de_2(n)

    if res < 1:
        fallos_cota += 1
        if fallos_cota <= 5:
            print("FALLO COTA: n =", n, "Res =", res)
    if (res == 1) != pot2:
        fallos_igualdad += 1
        if fallos_igualdad <= 5:
            print("FALLO IGUALDAD: n =", n, "Res =", res, "pot2 =", pot2)
    if (A == 0) != pot2:
        fallos_A0 += 1
        if fallos_A0 <= 5:
            print("FALLO A=0: n =", n, "A =", A, "pot2 =", pot2)
    if res == 1:
        igualdades.append(n)

    if n <= RANGO_PRODUCTO:
        prod = Fraction(1)
        for x in impares:
            prod *= Fraction(3 * x + 1, 3 * x)
        if prod != res:
            fallos_producto += 1
            if fallos_producto <= 5:
                print("FALLO PRODUCTO: n =", n)

# --- bordes explicitos ---
# n = 1: trayectoria vacia, A = B = 0, Res = 1, y 1 = 2^0 es potencia de 2
A1, B1, _ = tray_clasica(1)
if not (A1 == 0 and B1 == 0):
    raise SystemExit("BORDE n=1 RARO: A=%d B=%d" % (A1, B1))
# n = 2: un paso par, Res = 2/2 = 1
A2, B2, _ = tray_clasica(2)
if not (A2 == 0 and B2 == 1 and Fraction(2 ** B2, 2) == 1):
    raise SystemExit("BORDE n=2 RARO")
# n = 3 (impar chico): Res = 2^B/(3^A*3), debe ser > 1 estricto
A3, B3, _ = tray_clasica(3)
r3 = Fraction(2 ** B3, (3 ** A3) * 3)
if not r3 > 1:
    raise SystemExit("BORDE n=3 RARO: Res = %s" % r3)
# potencias de 2 grandes, fuera del barrido denso: 2^40, 2^60
for m in (20, 40, 60):
    n = 2 ** m
    A_, B_, _ = tray_clasica(n)
    r_ = Fraction(2 ** B_, (3 ** A_) * n)
    if not (A_ == 0 and B_ == m and r_ == 1):
        raise SystemExit("BORDE 2^%d RARO" % m)
# un impar grande fuera del barrido: 10^6 + 1 y 10^6 + 3
for n in (1000001, 1000003):
    A_, B_, imp_ = tray_clasica(n)
    r_ = Fraction(2 ** B_, (3 ** A_) * n)
    prod_ = Fraction(1)
    for x in imp_:
        prod_ *= Fraction(3 * x + 1, 3 * x)
    if not (r_ > 1 and prod_ == r_):
        raise SystemExit("BORDE n=%d RARO" % n)

if fallos_cota or fallos_igualdad or fallos_producto or fallos_A0:
    raise SystemExit("HAY FALLOS: cota=%d igualdad=%d producto=%d A0=%d"
                     % (fallos_cota, fallos_igualdad, fallos_producto, fallos_A0))

# resumen
pot2_en_rango = [2 ** m for m in range(0, 17) if 2 ** m <= LIMITE]
print("barrido n = 1 ..", LIMITE, "(mapa clasico, Fraction exacto)")
print("fallos de la cota Res >= 1:", fallos_cota)
print("fallos de 'igualdad <-> potencia de 2':", fallos_igualdad)
print("fallos de 'A=0 <-> potencia de 2':", fallos_A0)
print("identidad Res == PROD(1+1/(3x)) comprobada en n = 1 ..", RANGO_PRODUCTO,
      "+ 2 impares de 10^6:", "0 fallos" if fallos_producto == 0 else "FALLA")
print("n con Res == 1 (eps == 0):", len(igualdades), "casos")
print("  esperados (potencias de 2 hasta el limite):", len(pot2_en_rango))
print("  coinciden como conjuntos:", igualdades == pot2_en_rango)
print("  lista:", igualdades)
print()
print("VEREDICTO ARITMETICO: eps >= 0 para todo n del rango, con eps = 0")
print("exactamente en las potencias de 2 y eps > 0 en todos los demas.")
print("El enunciado literal 'eps > 0 siempre' es contradictorio con su propia")
print("segunda mitad: lo correcto es eps >= 0 con igualdad solo en n = 2^m.")
