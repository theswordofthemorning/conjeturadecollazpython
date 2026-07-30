# clasesfusion.py
#
# LAS CLASES QUE SE FUNDEN SIEMPRE, DEMOSTRADAS EN VEZ DE MEDIDAS.
#
# densidadfusion.py encontro midiendo que hay clases de resto modulo 2^k en
# las que el par (n, n+1) coincide en altura el 100% de las veces, y que su
# numero crece al doblar el modulo. Pero medir tiene un sesgo declarado: al
# doblar el modulo la muestra por clase se parte, y con pocas decenas de
# ejemplos una clase de tasa 0,99 se mide como 1,000.
#
# Aqui no se mide: se demuestra. Y el criterio sale de una linea de Terras.
#
# ---------------------------------------------------------------------------
# EL CRITERIO
# ---------------------------------------------------------------------------
#
# Terras (1976), Teorema 1.1, para el mapa acelerado T:
#
#     T^k(n) = lambda_k(n) * n + rho_k(n),    lambda_k = 3^{S_k} / 2^k
#
# donde S_k(n) = cuantos de los k primeros pasos fueron impares, y **tanto
# lambda_k como rho_k dependen solo del vector de paridad**, o sea solo de
# n modulo 2^k (Teorema 1.2). Poniendo n = 2^k * m + r:
#
#     T^k(2^k m + r) = (3^{S_k}/2^k)(2^k m + r) + rho_k
#                    = 3^{S_k(r)} * m  +  T^k(r)
#
# Es una recta en m, con pendiente 3^{S_k(r)} y ordenada T^k(r), y **las dos
# cosas dependen solo de r**. Entonces las trayectorias de 2^k m + r y de
# 2^k m + r+1 coinciden en el paso k **para todo m** exactamente cuando
#
#     S_k(r) == S_k(r+1)      (misma pendiente)
#     T^k(r) == T^k(r+1)      (misma ordenada)
#
# Y si coinciden en el paso k, a partir de ahi son la misma trayectoria, con
# lo cual tienen la misma altura. Ademas la primera condicion garantiza que
# hayan gastado el mismo numero de pasos del mapa clasico para llegar ahi
# (k pasos de T son k + S_k pasos de C).
#
# Es una comprobacion FINITA que vale para los INFINITOS m de la clase.
#
# ---------------------------------------------------------------------------
# LO QUE SALE
# ---------------------------------------------------------------------------
#
# Las dos familias publicadas caen dentro, y se rederivan en tres lineas:
#
#   resto 4 mod 8   -> 8k+4 y 8k+5 (Lagarias 1985)
#   resto 5 mod 32  -> (32m+5, 32m+6) (Wu y Huang 2001)
#
# Y la fraccion de clases que se funden siempre se puede calcular EXACTA
# para cada k, sin muestrear nada.

import numpy as np

# ---------------------------------------------------------------------------
# Cambia esto aqui, guarda, y dale a Ctrl+B en Sublime.
# ---------------------------------------------------------------------------

K_MAX = 22       # hasta que exponente 2^k se llega. 22 tarda ~1 min.
K_DETALLE = 5    # de que modulo se imprime la lista entera de clases


def salto_y_paridad(k):
    """Para cada r de 0 a 2^k, devuelve (T^k(r), S_k(r)).

    Vectorizado: mueve los 2^k restos a la vez, k veces.
    """
    v = np.arange(0, (1 << k) + 1, dtype=np.int64)
    S = np.zeros(len(v), dtype=np.int64)
    for _ in range(k):
        impar = (v & 1).astype(bool)
        S += impar
        v = np.where(impar, (3 * v + 1) >> 1, v >> 1)
    return v, S


def clases_que_se_funden(k):
    """Los restos r modulo 2^k tales que (2^k m + r, +1) se funden para todo m."""
    v, S = salto_y_paridad(k)
    MOD = 1 << k
    # el caso normal: r y r+1 estan en el mismo bloque
    normal = (S[:MOD - 1] == S[1:MOD]) & (v[:MOD - 1] == v[1:MOD])
    buenos = list(np.flatnonzero(normal))
    # el caso del borde: r = 2^k - 1, y n+1 = 2^k (m+1) + 0
    r = MOD - 1
    if S[r] == S[0] and v[r] == int(3 ** int(S[0])) + v[0]:
        buenos.append(r)
    return sorted(int(x) for x in buenos)


# ------------------------------------- COMPROBACION 1: las dos publicadas

print("COMPROBACION 1 -- las dos familias publicadas salen del criterio\n")

v3, S3 = salto_y_paridad(3)
print(f"  Lagarias 1985: 8k+4 y 8k+5 se funden siempre.")
print(f"    r=4: T^3(4) = {v3[4]}, S_3(4) = {S3[4]}")
print(f"    r=5: T^3(5) = {v3[5]}, S_3(5) = {S3[5]}")
cumple_4 = (v3[4] == v3[5]) and (S3[4] == S3[5])
print(f"    misma pendiente y misma ordenada: {cumple_4}")

v5, S5 = salto_y_paridad(5)
print(f"\n  Wu y Huang 2001: (32m+5, 32m+6) se funden siempre.")
print(f"    r=5: T^5(5) = {v5[5]}, S_5(5) = {S5[5]}")
print(f"    r=6: T^5(6) = {v5[6]}, S_5(6) = {S5[6]}")
cumple_5 = (v5[5] == v5[6]) and (S5[5] == S5[6])
print(f"    misma pendiente y misma ordenada: {cumple_5}")

if not (cumple_4 and cumple_5):
    raise SystemExit("El criterio no reproduce las familias publicadas. Esta mal.")
print(f"\n  Las dos, rederivadas en tres lineas. El criterio funciona.")


# --------------- COMPROBACION 2: el criterio contra la fuerza bruta

print(f"\n\nCOMPROBACION 2 -- el criterio contra la fuerza bruta\n")


def altura(n):
    """Pasos del mapa clasico hasta el 1."""
    c = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        c += 1
    return c


fallos = 0
probados = 0
for k in (3, 4, 5, 6, 7):
    MOD = 1 << k
    buenos = set(clases_que_se_funden(k))
    for r in range(MOD):
        # se prueban varios m: si el criterio dice que se funde para TODO m,
        # ninguno puede fallar; y si dice que no, alguno tiene que fallar.
        iguales = [altura(MOD * m + r) == altura(MOD * m + r + 1)
                   for m in range(1, 40)]
        probados += len(iguales)
        if r in buenos and not all(iguales):
            fallos += 1
            print(f"    FALLO: el criterio dice que {r} mod {MOD} se funde"
                  f" siempre, y no.")
        if r not in buenos and all(iguales):
            print(f"    aviso: {r} mod {MOD} no cumple el criterio pero"
                  f" coincidio en los 39 casos probados (puede ser casualidad)")

print(f"  pares comprobados a mano: {probados:,}   fallos del criterio: {fallos}")
if fallos:
    raise SystemExit("El criterio falla contra la fuerza bruta. No sigas.")


# ------------------------------------- la lista para un modulo concreto

MOD = 1 << K_DETALLE
buenos = clases_que_se_funden(K_DETALLE)
print(f"\n\nLAS CLASES QUE SE FUNDEN SIEMPRE, modulo {MOD}\n")
print(f"  {buenos}")
print(f"  o sea {len(buenos)} de {MOD}")
for r in buenos:
    marca = ""
    if K_DETALLE == 5 and r == 5:
        marca = "   <- la familia de Wu y Huang"
    if K_DETALLE == 3 and r == 4:
        marca = "   <- la familia de Lagarias"
    print(f"    {r:>4} = {r:0{K_DETALLE}b}{marca}")


# ------------------------ la fraccion exacta, sin muestrear, para cada k

print(f"\n\nLA FRACCION EXACTA DE CLASES QUE SE FUNDEN SIEMPRE\n")
print(f"  (esto ya no es una medida con muestra: es una cuenta cerrada)\n")
print(f"  {'k':>3} {'mod 2^k':>12} {'se funden':>11} {'fraccion':>10}   {'crece?':>8}")
print(f"  {'-'*3} {'-'*12} {'-'*11} {'-'*10}   {'-'*8}")

previa = -1.0
bajadas = 0
fracciones = []
for k in range(3, K_MAX + 1):
    buenos = clases_que_se_funden(k)
    frac = len(buenos) / (1 << k)
    veredicto = "sube" if frac > previa else ("igual" if frac == previa else "BAJA")
    if previa >= 0 and frac < previa:
        bajadas += 1
    previa = frac
    fracciones.append((k, len(buenos), frac))
    print(f"  {k:>3} {1 << k:>12,} {len(buenos):>11,} {frac:>10.6f}   {veredicto:>8}")

print(f"\n  escalones que bajan: {bajadas} de {len(fracciones) - 1}")


# ------------------------------------------------------- lo que significa

print(f"\nQUE SIGNIFICA ESTO PARA LA CONJETURA DE WU\n")
ultima = fracciones[-1]
print(f"  Esta fraccion es una COTA INFERIOR de la densidad de pares")
print(f"  consecutivos con la misma altura, y ahora es exacta, no muestreada:")
print(f"  al menos el {ultima[2]:.4%} de los pares se funden, demostrado,")
print(f"  con solo mirar el resto modulo 2^{ultima[0]}.")
print(f"\n  densidadfusion.py mide la densidad real en {0.5099:.4f} a 2^26.")
print(f"  La diferencia entre esa cifra y esta cota son los pares que se")
print(f"  funden pero cuya clase NO se funde entera: coincidencias que")
print(f"  dependen del m concreto, no solo del resto.")
print(f"\n  Y LO QUE ESTO NO DICE: que la fraccion crezca en {K_MAX - 2} escalones")
print(f"  no demuestra que crezca siempre, ni que tienda a 1. La conjetura de")
print(f"  Wu sigue abierta. Lo que si hace es quitarle el sesgo de muestreo")
print(f"  que tenia la version medida, y dar una cota inferior de verdad.")
