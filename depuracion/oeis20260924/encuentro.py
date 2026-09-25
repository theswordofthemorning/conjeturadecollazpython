# encuentro.py -- cuando se encuentran las trayectorias de m y m+1
# Mapa clasico de Collatz (A006370): x/2 si x es par, 3x+1 si es impar.
# m recorre A078417: los m con la misma altura que m+1.
# a(n) = primer paso k en que las trayectorias de m y m+1 coinciden.
# Sin input(): los parametros van en estas variables.

import math

CUANTOS = 10000          # terminos de la b-file
LIMITE_GAO = 200000      # hasta donde se coteja el conjunto de Gao


def paso(x):
    if x % 2 == 0:
        return x // 2
    return 3 * x + 1


def altura(m):
    # pasos hasta llegar a 1 por primera vez (A006577)
    k = 0
    while m != 1:
        m = paso(m)
        k += 1
    return k


def encuentro(m):
    # solo se llama si m y m+1 tienen la misma altura: entonces termina
    x, y, k = m, m + 1, 0
    while x != y:
        x, y, k = paso(x), paso(y), k + 1
    return k


def gao_directo(m):
    # definicion literal de Gao: C^k(m) = C^k(m+1) para algun k <= log2(m)
    x, y, k = m, m + 1, 0
    while k <= math.log2(m):
        if x == y:
            return True
        x, y, k = paso(x), paso(y), k + 1
    return False


# 1. A078417 recalculada y cotejada con la b-file oficial
oficial = []
for linea in open("b078417_oficial.txt", encoding="utf8"):
    partes = linea.split()
    if len(partes) == 2 and not linea.startswith("#"):
        oficial.append(int(partes[1]))
propia = []
m = 1
while len(propia) < CUANTOS:
    if altura(m) == altura(m + 1):
        propia.append(m)
    m += 1
if propia != oficial[:CUANTOS]:
    raise SystemExit("A078417 recalculada NO coincide con la oficial")
print("A078417: 10000 terminos coinciden con la b-file oficial")

# 2. la secuencia nueva y su b-file
datos = [encuentro(m) for m in propia]
with open("b_encuentro.txt", "w", encoding="utf8") as salida:
    for i in range(CUANTOS):
        salida.write(str(i + 1) + " " + str(datos[i]) + "\n")
print("primeros 60:", ",".join(map(str, datos[:60])))

# 3. el conjunto de Gao coincide con {m en A078417 : a <= log2 m}, m >= 2
fallos = 0
for m in range(2, LIMITE_GAO):
    directo = gao_directo(m)
    via_tabla = altura(m) == altura(m + 1) and encuentro(m) <= math.log2(m)
    if directo != via_tabla:
        fallos += 1
print("Gao, m = 2 ..", LIMITE_GAO - 1, "discrepancias:", fallos)

# 4. a = 3 exactamente para m = 4 (mod 8), m > 4 (pares de Garner)?
tres = [propia[i] for i in range(CUANTOS) if datos[i] == 3]
garner = [m for m in propia if m % 8 == 4 and m > 4]
print("a=3 sobre m = 4 mod 8:", all(m % 8 == 4 for m in tres),
      "| todo m = 4 mod 8 (m>4) de la tabla tiene a=3:",
      all(datos[propia.index(m)] == 3 for m in garner[:500]))
print("maximo de a en la b-file:", max(datos), "| ultimo m:", propia[-1])
