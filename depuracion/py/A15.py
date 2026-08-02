# A15 - verificacion independiente (agente 2, Python desde cero)
#
# ENUNCIADO LITERAL: T(2^k - n) = 2^(k-1) - T(n)
#   "en los pasos pares el espejo base 2 CONMUTA con Collatz"
#   Ambito declarado en la base: n par. Cuantificador: todo_n. Estado: demostrado.
#
# INTERPRETACION QUE VERIFICO (escrita antes de medir):
#   - "paso par" = el paso de Collatz sobre un numero PAR, o sea T(n) = n/2.
#     En un paso par los TRES mapas (clasico, atajo, 3n-1) hacen lo mismo:
#     dividir entre 2. La identidad, si vale, es independiente del mapa.
#   - Para que el lado izquierdo sea tambien un "paso par" hace falta que
#     2^k - n sea par, y con n par eso exige k >= 1.
#   - Enunciado interpretado:
#       para todo k >= 1 y todo n par (con el espejo 2^k - n tambien par),
#       T(2^k - n) = 2^(k-1) - T(n),  donde T(m) = m/2 en los pares.
#
# Derivacion propia (el "algebra de dos lineas"):
#   n par, k >= 1  =>  2^k - n par  =>  T(2^k - n) = (2^k - n)/2
#                                                  = 2^(k-1) - n/2
#                                                  = 2^(k-1) - T(n).
#   La verificacion numerica de abajo comprueba que esa cadena no esconde
#   ningun borde (n = 0, n = 2^k, n > 2^k, k chico...).
#
# Todo con int exacto de Python. Ningun float decide nada.

import sys

def paso_clasico(m):
    # mapa clasico sobre Z: par -> m/2, impar -> 3m+1
    if m % 2 == 0:
        return m // 2
    return 3 * m + 1

def paso_atajo(m):
    # mapa del atajo: par -> m/2, impar -> (3m+1)/2
    if m % 2 == 0:
        return m // 2
    return (3 * m + 1) // 2   # 3m+1 es par si m impar; division exacta

def paso_3n1(m):
    # mapa 3n-1: par -> m/2, impar -> 3m-1
    if m % 2 == 0:
        return m // 2
    return 3 * m - 1

fallos = 0
comprobados = 0

# ---------------------------------------------------------------
# 1) RANGO CENTRAL: k = 1..20, n par de 0 a 2^k + 400 (incluye n > 2^k,
#    o sea espejo negativo), con los tres mapas.
# ---------------------------------------------------------------
for k in range(1, 21):
    tope = 2**k + 400 if k <= 12 else 2**12 + 400  # limitar coste, ya exhaustivo hasta k=12
    for n in range(0, tope + 1, 2):
        espejo = 2**k - n
        # ambos lados son pares por construccion: comprobarlo explicitamente
        if espejo % 2 != 0:
            print("IMPOSIBLE: espejo impar con n par, k =", k, "n =", n)
            raise SystemExit(1)
        lhs = espejo // 2          # T sobre un par: los tres mapas coinciden
        rhs = 2**(k-1) - n // 2
        comprobados += 1
        if lhs != rhs:
            fallos += 1
            if fallos <= 5:
                print("FALLO en k =", k, "n =", n, ":", lhs, "!=", rhs)
        # y con los tres mapas literales, sobre el espejo (que es par):
        for paso in (paso_clasico, paso_atajo, paso_3n1):
            if paso(espejo) != rhs:
                fallos += 1
                print("FALLO de mapa", paso.__name__, "k =", k, "n =", n)

print("[1] rango central: k = 1..20, n par (exhaustivo 0..2^k+400 hasta k=12,")
print("    0..4496 despues), espejos negativos incluidos:")
print("    comprobaciones =", comprobados, "| fallos =", fallos)

# ---------------------------------------------------------------
# 2) k GRANDE con n grande: k = 64, 200; n par al azar determinista
# ---------------------------------------------------------------
f2 = 0
c2 = 0
for k in (64, 200):
    for j in range(1, 2001):
        n = (j * j * 7919 + j * 13) % (2**k)
        if n % 2 == 1:
            n += 1
        espejo = 2**k - n
        lhs = espejo // 2
        rhs = 2**(k-1) - n // 2
        c2 += 1
        if lhs != rhs:
            f2 += 1
            print("FALLO k grande:", k, n)
print("[2] k = 64 y k = 200, 2000 n pares cada uno: comprobaciones =", c2, "| fallos =", f2)

# ---------------------------------------------------------------
# 3) BORDES donde el enunciado DEBE romperse o degenerar
# ---------------------------------------------------------------
print("[3] bordes:")

# 3a) n IMPAR: la identidad es falsa en general (el espejo es impar y entra
#     la rama 3n+1). Busco contraejemplos con el mapa clasico y con el atajo.
ce_clasico = []
ce_atajo = []
ok_impar_clasico = 0
for k in range(1, 13):
    for n in range(1, 2**k, 2):
        espejo = 2**k - n            # impar
        rhs = 2**(k-1) - paso_clasico(n)
        if paso_clasico(espejo) != rhs:
            if len(ce_clasico) < 3:
                ce_clasico.append((k, n, paso_clasico(espejo), rhs))
        else:
            ok_impar_clasico += 1
        rhs2 = 2**(k-1) - paso_atajo(n)
        if paso_atajo(espejo) != rhs2:
            if len(ce_atajo) < 3:
                ce_atajo.append((k, n, paso_atajo(espejo), rhs2))
print("    n impar, clasico: contraejemplos =", ce_clasico)
print("    n impar, clasico: casos impares que casualmente SI cumplen =", ok_impar_clasico)
print("    n impar, atajo:   contraejemplos =", ce_atajo)

# curiosidad de borde: con el ATAJO en los impares, T(2^k-n) = (3(2^k-n)+1)/2
# y 2^(k-1) - T(n) = 2^(k-1) - (3n+1)/2; diferencia = 3*2^(k-1) - 2^(k-1) = 2^k...
# lo mide el bucle: si saliera identidad tambien en impares, lo habria dicho.

# 3b) k = 0: 2^0 - n = 1 - n (impar si n par) y 2^(-1) no es entero.
n = 4
espejo = 1 - n   # -3, impar
print("    k = 0, n = 4: espejo =", espejo, "(impar, cambia de rama);",
      "2^(k-1) = 1/2 no es entero -> el enunciado exige k >= 1")

# 3c) n = 0 y n = 2^k (espejo 0): degenerados pero consistentes
for k in (1, 5, 10):
    assert (2**k - 0) // 2 == 2**(k-1) - 0
    assert (2**k - 2**k) // 2 == 2**(k-1) - 2**(k-1)
print("    n = 0 y n = 2^k: la identidad da 2^(k-1) = 2^(k-1) y 0 = 0, consistente")

# 3d) n = 2 (el par mas chico > 0), k = 1: espejo = 0, T(0) = 0, rhs = 1 - 1 = 0
print("    k = 1, n = 2: T(0) =", 0, "y 2^0 - T(2) =", 1 - 1, "-> coinciden")

# 3e) n par NEGATIVO: n = -6, k = 4 -> espejo = 22, T = 11; rhs = 8 - (-3) = 11
n = -6
k = 4
print("    n = -6, k = 4: T(2^4 - (-6)) =", (2**k - n) // 2,
      "y 2^3 - T(-6) =", 2**(k-1) - (n // 2), "-> coinciden (vale sobre todo Z par)")

if fallos == 0 and f2 == 0:
    print()
    print("VEREDICTO DEL SCRIPT: 0 fallos en el ambito declarado (n par, k >= 1);")
    print("la identidad es falsa para n impar (contraejemplos arriba) y no esta")
    print("definida en k = 0. El 'todo_n' de la base necesita el ambito 'n par'")
    print("que la propia nota ya declara.")
else:
    raise SystemExit("HAY FALLOS")
