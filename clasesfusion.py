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

import math

import numpy as np

# ---------------------------------------------------------------------------
# Cambia esto aqui, guarda, y dale a Ctrl+B en Sublime.
# ---------------------------------------------------------------------------

K_MAX = 32       # hasta que exponente 2^k se llega. 30 tarda unos 20 minutos;
                 # 32 cuesta unas 4 veces mas (algo mas de una hora).
K_DETALLE = 5    # de que modulo se imprime la lista entera de clases
BLOQUE = 1 << 22  # de cuantos restos en cuantos se trabaja

# POR QUE EN BLOQUES. Con k = 26 el array de restos son 67 millones de int64
# (537 MB), y cada np.where del paso crea tres temporales mas: se va a 3-4 GB.
# En bloques de 4 millones el pico se queda en ~100 MB, sea cual sea k. El
# unico cuidado es el par que cruza la frontera entre bloques, que se lleva a
# mano con el ultimo resto del bloque anterior.


def salto_y_paridad(restos, k):
    """Para cada r del array, devuelve (T^k(r), S_k(r)).

    Todo en sitio para no duplicar memoria: se calcula la rama impar en un
    temporal, se aplica la rama par sobre el propio array, y se copian encima
    solo las posiciones impares.
    """
    v = np.array(restos, dtype=np.int64, copy=True)
    S = np.zeros(len(v), dtype=np.int32)
    for _ in range(k):
        impar = (v & 1).astype(bool)
        S += impar
        rama_impar = 3 * v + 1        # el unico temporal grande
        rama_impar >>= 1
        v >>= 1                        # la rama par, en sitio
        np.copyto(v, rama_impar, where=impar)
        del rama_impar
    return v, S


def recorrer_clases(k, bloque=BLOQUE, listar=False):
    """Cuenta (y opcionalmente lista) los restos r modulo 2^k que se funden
    para todo m. Devuelve (cuantos, lista_o_None).

    Criterio: S_k(r) == S_k(r+1) y T^k(r) == T^k(r+1).
    """
    MOD = 1 << k
    cuantos = 0
    lista = [] if listar else None
    v_cero = S_cero = None
    ultimo = None                      # (v, S) del ultimo resto del bloque previo

    for lo in range(0, MOD, bloque):
        hi = min(lo + bloque, MOD)
        v, S = salto_y_paridad(np.arange(lo, hi, dtype=np.int64), k)
        if lo == 0:
            v_cero, S_cero = int(v[0]), int(S[0])

        # el par que cruza la frontera con el bloque anterior
        if ultimo is not None:
            uv, uS = ultimo
            if uS == int(S[0]) and uv == int(v[0]):
                cuantos += 1
                if listar:
                    lista.append(lo - 1)

        # los pares de dentro del bloque
        dentro = (S[:-1] == S[1:]) & (v[:-1] == v[1:])
        cuantos += int(dentro.sum())
        if listar:
            lista.extend((lo + np.flatnonzero(dentro)).tolist())

        ultimo = (int(v[-1]), int(S[-1]))
        del v, S, dentro

    # el borde final: r = 2^k - 1, cuyo vecino es 2^k (m+1) + 0, o sea el
    # resto 0 con m aumentado en uno. Hace falta 3^{S_k(0)} de mas.
    uv, uS = ultimo
    if uS == S_cero and uv == int(3) ** S_cero + v_cero:
        cuantos += 1
        if listar:
            lista.append(MOD - 1)

    return cuantos, (sorted(lista) if listar else None)


def clases_que_se_funden(k):
    """La lista entera. Solo para k pequenos: con k grande no cabe en memoria."""
    return recorrer_clases(k, listar=True)[1]


def cuantas_clases(k):
    """Solo el numero. Es lo unico que hace falta para k grande."""
    return recorrer_clases(k, listar=False)[0]


# ------------------------------------- COMPROBACION 1: las dos publicadas

print("COMPROBACION 1 -- las dos familias publicadas salen del criterio\n")

v3, S3 = salto_y_paridad(np.arange(0, 9, dtype=np.int64), 3)
print(f"  Lagarias 1985: 8k+4 y 8k+5 se funden siempre.")
print(f"    r=4: T^3(4) = {v3[4]}, S_3(4) = {S3[4]}")
print(f"    r=5: T^3(5) = {v3[5]}, S_3(5) = {S3[5]}")
cumple_4 = (v3[4] == v3[5]) and (S3[4] == S3[5])
print(f"    misma pendiente y misma ordenada: {cumple_4}")

v5, S5 = salto_y_paridad(np.arange(0, 33, dtype=np.int64), 5)
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
print(f"  {'k':>3} {'mod 2^k':>12} {'se funden':>11} {'fraccion':>10}   {'crece?':>8}"
      f" {'razon':>8}")
print(f"  {'-'*3} {'-'*12} {'-'*11} {'-'*10}   {'-'*8} {'-'*8}")

previa = -1.0
bajadas = 0
fracciones = []
for k in range(3, K_MAX + 1):
    # solo el numero: con k = 26 la lista serian 28 millones de enteros
    cuantos = cuantas_clases(k)
    frac = cuantos / (1 << k)
    veredicto = "sube" if frac > previa else ("igual" if frac == previa else "BAJA")
    if previa >= 0 and frac < previa:
        bajadas += 1
    razon = f"{cuantos / fracciones[-1][1]:.4f}" if fracciones else ""
    previa = frac
    fracciones.append((k, cuantos, frac))
    print(f"  {k:>3} {1 << k:>12,} {cuantos:>11,} {frac:>10.6f}   {veredicto:>8}"
          f" {razon:>8}")

print(f"\n  escalones que bajan: {bajadas} de {len(fracciones) - 1}")


# ------------------------------------------------------- lo que significa

print(f"\nQUE SIGNIFICA ESTO PARA LA CONJETURA DE WU\n")
ultima = fracciones[-1]
print(f"  Esta fraccion es una COTA INFERIOR de la densidad de pares")
print(f"  consecutivos con la misma altura, y ahora es exacta, no muestreada:")
print(f"  al menos el {ultima[2]:.4%} de los pares se funden, demostrado,")
print(f"  con solo mirar el resto modulo 2^{ultima[0]}.")
print(f"\n  densidadfusion.py mide la densidad real en 0,5186 a 2^28.")
print(f"  La diferencia entre esa cifra y esta cota son los pares que se")
print(f"  funden pero cuya clase NO se funde entera: coincidencias que")
print(f"  dependen del m concreto, no solo del resto.")


# ------------- CORRECCION: la monotonia es TRIVIAL, no un hallazgo
#
# Una version anterior de este archivo presentaba "la fraccion crece en los
# 24 escalones" como si fuera un dato medido. No lo es: esta FORZADO, y la
# demostracion es de tres lineas. Queda escrito aqui porque el error estuvo
# publicado y conviene que se vea la correccion, no solo el resultado.

print(f"\n\nCORRECCION -- que la fraccion crezca es TRIVIAL\n")
print(f"  Si r es buena modulo 2^k, entonces r y r + 2^k son las DOS buenas")
print(f"  modulo 2^(k+1). Por que: la formula T^k(2^k m + r) = 3^S(r) m + T^k(r)")
print(f"  con m = 1 da T^k(2^k + r) = 3^S(r) + T^k(r), y lo mismo para r+1;")
print(f"  si r era buena las dos salidas coinciden, luego r + 2^k tambien.")
print(f"  Y si r es buena a nivel k, sus dos iterados ya son el MISMO numero,")
print(f"  asi que sigue siendo buena a nivel k+1.")
print(f"\n  Consecuencia:  N(k+1) >= 2*N(k)  siempre, por construccion.")
print(f"  Luego f(k+1) = N(k+1)/2^(k+1) >= N(k)/2^k = f(k).")
print(f"  LA MONOTONIA NO SE VERIFICA: SE DEMUESTRA. Y la razon > 2 tambien.")

heredadas = [2 * n for _, n, _ in fracciones[:-1]]
nuevas = [fracciones[i][1] - heredadas[i - 1] for i in range(1, len(fracciones))]

print(f"\n  Lo unico con contenido es cuantas clases se ESTRENAN en cada")
print(f"  nivel, porque")
print(f"\n      f(k+1) - f(k) = nuevas(k) / 2^(k+1)")
print(f"\n  y entonces  f(infinito) = f(k) + suma de nuevas(j)/2^(j+1).\n")
print(f"  {'k':>3} {'N(k)':>12} {'heredadas':>12} {'NUEVAS':>10} "
      f"{'razon nuevas':>13} {'nuevas/2^k':>12}")
print(f"  {'-'*3} {'-'*12} {'-'*12} {'-'*10} {'-'*13} {'-'*12}")
for i in range(1, len(fracciones)):
    k = fracciones[i][0]
    if k < 14:
        continue
    rn = f"{nuevas[i-1]/nuevas[i-2]:.4f}" if i >= 2 and nuevas[i - 2] else ""
    print(f"  {k:>3} {fracciones[i][1]:>12,} {heredadas[i-1]:>12,} "
          f"{nuevas[i-1]:>10,} {rn:>13} {nuevas[i-1]/2**k:>12.6f}")

print(f"\n  LA PREGUNTA, YA LIMPIA: converge la suma de nuevas(j)/2^(j+1)?")
print(f"  Las nuevas crecen con razon ~1,92 y subiendo. Si esa razon se")
print(f"  queda por DEBAJO de 2, la suma converge y la fraccion tiene un")
print(f"  limite < 1. Si llega a 2, diverge y la fraccion tiende a 1.")
print(f"  Con los datos de aqui la razon sube (1,84 -> 1,92) sin estabilizarse,")
print(f"  asi que NO SE PUEDE DECIDIR. Es el mismo muro que antes, pero ahora")
print(f"  formulado sobre una sucesion de enteros en vez de sobre un ajuste.")

print(f"\n  Lo que SI se puede afirmar:")
print(f"    - la cota inferior demostrada va por {fracciones[-1][2]:.4%}")
print(f"      (eso si es un resultado: no depende de muestreo ni de ajuste)")
print(f"    - que crezca no lo es: es un teorema de tres lineas")
print(f"  La conjetura de Wu sigue abierta.")
