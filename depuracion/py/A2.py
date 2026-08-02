# -*- coding: utf-8 -*-
# AGENTE 2 (independiente) - Item A2
# Enunciado: log2( altitud(n)/n ) >= racha(n) * log2(3/2) + 1   para n IMPAR
#   racha(n)   = pasos impares seguidos al arranque bajo el mapa del ATAJO ((3n+1)/2)
#   altitud(n) = valor mas alto de la trayectoria bajo el mapa CLASICO (3n+1), incluyendo n
# Forma entera exacta (sin floats en la decision):
#   alt * 2^r >= 2 * n * 3^r
#
# Escrito desde cero, sin mirar ningun fichero del repo.

from fractions import Fraction
import sys

LIMITE = 200001          # barrido principal: impares 1..LIMITE
LIMITE_PARES = 100000    # contraejemplos con n par

def altitud_clasica(n):
    """Valor maximo de la trayectoria clasica (n/2 si par, 3n+1 si impar),
    incluyendo el propio n, deteniendose al llegar a 1."""
    m = n
    alt = n
    while m != 1:
        if m % 2 == 0:
            m //= 2
        else:
            m = 3 * m + 1
        if m > alt:
            alt = m
    return alt

def racha_atajo(n):
    """Cuantos pasos impares seguidos al arranque bajo el atajo:
    mientras el valor actual sea impar, se aplica (3x+1)/2 y se cuenta."""
    r = 0
    m = n
    while m % 2 == 1:
        m = (3 * m + 1) // 2
        r += 1
        if m == 1:      # llego al 1 siendo... 1 es impar; el bucle seguiria: 1 -> 2
            pass        # no hace falta cortar: 1 es impar, da 1->2 (par) y termina
    return r

def cumple(n, alt, r):
    """Decision entera exacta: alt * 2^r >= 2 * n * 3^r."""
    return alt * (2 ** r) >= 2 * n * (3 ** r)

fallos = []
comprobados = 0
holgura_min = None   # holgura en la desigualdad entera, como Fraction alt*2^r/(2n*3^r)
holgura_arg = None

for n in range(1, LIMITE + 1, 2):
    alt = altitud_clasica(n)
    r = racha_atajo(n)
    comprobados += 1
    if not cumple(n, alt, r):
        fallos.append((n, alt, r))
    else:
        q = Fraction(alt * 2 ** r, 2 * n * 3 ** r)   # >= 1 si cumple
        if holgura_min is None or q < holgura_min:
            holgura_min = q
            holgura_arg = (n, alt, r)

print("== BARRIDO PRINCIPAL (n impar) ==")
print("mapa de la racha: ATAJO (3n+1)/2 ; mapa de la altitud: CLASICO 3n+1")
print("rango: impares de 1 a", LIMITE, "->", comprobados, "numeros")
print("fallos:", len(fallos))
if fallos:
    print("primeros fallos:", fallos[:10])
n0, alt0, r0 = holgura_arg
print("cociente minimo alt*2^r/(2n*3^r) =", holgura_min, "~", float(holgura_min))
print("  alcanzado en n =", n0, " alt =", alt0, " racha =", r0)

# la holgura en bits: log2(cociente). Prediccion cerrada para racha 1:
# alt = 3n+1 y la cota pide 3n, asi que cociente = (3n+1)/(3n) = 1 + 1/(3n),
# minimo en el mayor impar de racha 1 del rango.
import math
print("  holgura en bits (solo para imprimir):", math.log2(float(holgura_min)))

# mayor impar de racha 1 del rango, para contrastar la formula 1 + 1/(3n)
mayor_r1 = None
for n in range(LIMITE, 0, -2):
    if racha_atajo(n) == 1:
        mayor_r1 = n
        break
print("  mayor impar de racha 1 en el rango:", mayor_r1,
      " -> 1 + 1/(3n) =", Fraction(3 * mayor_r1 + 1, 3 * mayor_r1),
      " coincide con el minimo?", Fraction(3 * mayor_r1 + 1, 3 * mayor_r1) == holgura_min)

print()
print("== BORDES ==")

# n = 1: racha y altitud a mano.
# Trayectoria clasica de 1: 1 -> 4 -> 2 -> 1, altitud = 4.
# Atajo: 1 es impar -> (3*1+1)/2 = 2 (par), racha = 1.
alt1 = altitud_clasica(1)
r1 = racha_atajo(1)
print("n=1: altitud =", alt1, " racha =", r1,
      " desigualdad 4*2 >= 2*1*3 ->", cumple(1, alt1, r1))
# convenio alternativo: si la 'trayectoria' de 1 fuera solo [1] (alt=1), fallaria:
print("n=1 con convenio alt(1)=1 (trayectoria vacia):", cumple(1, 1, r1),
      " <- el enunciado DEPENDE de que la altitud de 1 incluya el 4")

# n par: el enunciado sin la hipotesis 'n impar' es falso. Contar fallos pares.
fallos_pares = 0
primer_fallo_par = None
for n in range(2, LIMITE_PARES + 1, 2):
    alt = altitud_clasica(n)
    r = racha_atajo(n)   # n par -> racha 0
    if r != 0:
        raise SystemExit("un par con racha != 0: imposible")
    if not cumple(n, alt, r):
        fallos_pares += 1
        if primer_fallo_par is None:
            primer_fallo_par = (n, alt)
print("n par, rango 2..", LIMITE_PARES, ": fallos =", fallos_pares, "de", LIMITE_PARES // 2)
print("  primer fallo par:", primer_fallo_par, " (n=10 sube solo a 16 < 20 = 2n?",
      altitud_clasica(10), ")")

# racha alta: n = 2^k - 1 tiene racha >= k (todo unos en binario).
print()
print("== RACHA ALTA: n = 2^k - 1, k = 2..40 ==")
fallos_altos = 0
for k in range(2, 41):
    n = 2 ** k - 1
    r = racha_atajo(n)
    alt = altitud_clasica(n)
    ok = cumple(n, alt, r)
    if not ok:
        fallos_altos += 1
        print("  FALLO en k =", k)
    if k in (2, 3, 10, 20, 30, 40):
        print("  k=%2d  n=2^%d-1  racha=%d  ok=%s" % (k, k, r, ok))
print("fallos con racha alta:", fallos_altos, "de 39")

# comprobacion de la racha por 2-adicos: racha(n) = r  <=>  n = 2^r - 1 (mod 2^(r+1))
# (verificacion muestral del propio instrumento)
malos_racha = 0
for n in range(1, 20000, 2):
    r = racha_atajo(n)
    if n % (2 ** (r + 1)) != (2 ** r - 1):
        malos_racha += 1
if malos_racha:
    raise SystemExit("la definicion de racha no cuadra con la caracterizacion 2-adica")
print()
print("control del instrumento: racha(n)=r <=> n = 2^r-1 (mod 2^(r+1)), 10000 impares, 0 fallos")

print()
print("== LA DEMOSTRACION, paso a paso, con Fraction ==")
# Argumento: sea n impar con racha r. Bajo el atajo, r pasos impares seguidos:
#   x -> (3x+1)/2 > (3/2) x   (estricto, por el +1)
# luego el valor v_r tras r pasos cumple v_r > (3/2)^r * n.
# El mapa clasico, en el paso impar r-esimo, pasa por 3*v_{r-1} + 1 = 2 * v_r
# ANTES de dividir; ese valor esta en la trayectoria clasica, luego
#   altitud(n) >= 2 * v_r > 2 * (3/2)^r * n
# que es exactamente alt * 2^r > 2 * n * 3^r (estricta; la >= del enunciado es mas debil).
# Verifico las dos piezas por separado en muestra:
piezas_mal = 0
for n in range(1, 20001, 2):
    r = racha_atajo(n)
    # iterar el atajo r pasos y comprobar v_r > (3/2)^r n exacto
    v = n
    for _ in range(r):
        if v % 2 != 1:
            raise SystemExit("contradiccion: paso impar sobre un par")
        v = (3 * v + 1) // 2
    if not Fraction(v, 1) > Fraction(3 ** r, 2 ** r) * n:
        piezas_mal += 1
    # y que 2*v esta de verdad en la trayectoria clasica (es el pico intermedio 3x+1)
    if r >= 1:
        alt = altitud_clasica(n)
        if alt < 2 * v:
            piezas_mal += 1
print("piezas del argumento (v_r > (3/2)^r n  y  altitud >= 2*v_r): 10000 impares, fallos =", piezas_mal)

print()
print("== VEREDICTO PREVIO ==")
if not fallos and piezas_mal == 0 and fallos_altos == 0:
    print("0 fallos en impares; el argumento cierra; los pares refutan la version sin hipotesis.")
else:
    print("REVISAR: hay fallos")
