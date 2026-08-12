# union_cruce.py
#
# EL CRUCE INDEPENDIENTE de unionpalabras.lean (12-08-2026, tras la
# 10a revision): fuerza bruta sin codigo comun con el .lean ni con
# equidistribucionmixto.py. Verifica el enunciado del lema de la
# UNION POR PALABRAS sobre la dinamica entera cruda:
#
#   para cada puerta de mixto (bit 0: h = (3c+1)/2; bit 1 con
#   altura k: h = (c - 3^(k-1))/2) y cada palabra de leyes
#   compartidas (division: h -> h/2; recarga con q = 3^k:
#   h -> (3h+1-q)/2), el conjunto de c IMPARES que sobreviven la
#   palabra entera (todos los pasos enteros, o sea el valor
#   corriente PAR en cada paso) es A LO SUMO UNA clase mod 2^(j+1),
#   con j el largo de la palabra.
#
# Barrido: k = 2..6, j = 1..6, TODAS las palabras de cada largo
# (recarga con el q = 3^k de la altura, constante en la corrida --
# como en la cadena real), c sobre TODOS los impares de un periodo
# completo mod 2^(j+2). Si dos supervivientes difieren mod 2^(j+1),
# SystemExit: el lema seria falso.
#
# Y las instancias del .lean cotejadas con la dinamica.

import itertools

K_MIN, K_MAX = 2, 6
J_MAX = 6

def sobrevive(c, bit, k, palabra):
    # la puerta del mixto
    if bit == 0:
        n = 3 * c + 1
    else:
        n = c - 3 ** (k - 1)
    if n % 2 != 0:
        return None
    h = n // 2
    q = 3 ** k
    # la corrida
    for ley in palabra:
        if ley == 'd':
            if h % 2 != 0:
                return None
            h = h // 2
        else:  # recarga
            n = 3 * h + 1 - q
            if n % 2 != 0:
                return None
            h = n // 2
    return h

total = 0
con_super = 0
vacias = 0
for k in range(K_MIN, K_MAX + 1):
    for j in range(1, J_MAX + 1):
        modulo = 2 ** (j + 1)
        periodo = 2 ** (j + 2)
        for palabra in itertools.product('dr', repeat=j):
            for bit in (0, 1):
                total += 1
                clases = set()
                for c in range(1, periodo, 2):
                    if sobrevive(c, bit, k, palabra) is not None:
                        clases.add(c % modulo)
                if len(clases) > 1:
                    raise SystemExit(
                        "ROTO: bit %d k %d palabra %s: %d clases "
                        "mod 2^%d: %s"
                        % (bit, k, ''.join(palabra), len(clases),
                           j + 1, sorted(clases)))
                if len(clases) == 1:
                    con_super += 1
                else:
                    vacias += 1

print("union por palabras: %d combinaciones (k=%d..%d, j=1..%d, "
      "todas las palabras, ambos bits)" % (total, K_MIN, K_MAX, J_MAX))
print("  a lo sumo UNA clase mod 2^(j+1) en TODAS: OK")
print("  con superviviente: %d   vacias: %d" % (con_super, vacias))

# las instancias del .lean, cotejadas contra esta dinamica
# corrida_c5: c=5 bit 0 -> h=8, palabra ddd -> 1
assert sobrevive(5, 0, 2, ('d', 'd', 'd')) == 1
# corrida_c21: c=21 bit 0 -> h=32, palabra ddd -> 4
assert sobrevive(21, 0, 2, ('d', 'd', 'd')) == 4
# clase compartida: 5 y 21 congruentes mod 2^4
if (5 - 21) % 16 != 0:
    raise SystemExit("ROTO: 5 y 21 no comparten clase mod 16")
# corrida_recarga (k=2, q=9): h=8, palabra rd -> 4; companera h=16 -> 10
# (las corridas del .lean arrancan del hijo: se prueban directas)
h = 8
h = (3 * h + 1 - 9) // 2
h = h // 2
assert h == 4
h = 16
h = (3 * h + 1 - 9) // 2
h = h // 2
assert h == 10
print("  instancias del .lean cotejadas con la dinamica: OK")
print("VEREDICTO: el lema de la union por palabras AGUANTA el cruce.")
