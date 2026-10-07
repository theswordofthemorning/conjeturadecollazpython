# Cotejo del retrato del fugitivo, sin Lean.
#
# Revisa con cuentas directas los numeros que usa CasaRetrato.lean:
#   1. 3^63 < 2^100 (de ahi "al menos 63 subidas de cada 100")
#      y 3^100 <= 2^159 (de ahi el tope 2^(96m)).
#   2. Los n entre 0 y 2^k - 1 tienen patrones de k pasos todos distintos,
#      y n y n + 2^k empiezan con el mismo patron.
#   3. Contados uno por uno, los n entre 0 y 2^k - 1 que a los k pasos
#      siguen sin cruce son tantos como los patrones con esa propiedad.
#   4. Para k = 100m, esos patrones no pasan de 2^(96m).
#   5. Cuantos aguantan k pasos sin cruce, en nuestra casa (3n+1) y en
#      la del vecino (5n+1).
#
# Uso, desde la raiz del repositorio:
#   python -B -X utf8 depuracion/casa20261004/cotejo_retrato.py
# No pide nada por teclado: los valores se cambian aqui arriba.

from math import comb

PASOS_PATRONES = 12        # parte 2: k = 1, ..., 12
PASOS_UNO_POR_UNO = 18     # parte 3: k = 1, ..., 18 (2^18 numeros)
BLOQUES = [1, 2, 3]        # parte 4: k = 100, 200, 300
PASOS_TABLA = [10, 20, 50, 100, 200, 300]   # parte 5


def siguiente(n):
    # el atajo: n/2 si n es par, (3n+1)/2 si es impar
    if n % 2 == 0:
        return n // 2
    return (3 * n + 1) // 2


def patron(n, k):
    # las k primeras paridades de la orbita de n, como texto de ceros y unos
    letras = ""
    for _ in range(k):
        letras = letras + str(n % 2)
        n = siguiente(n)
    return letras


def subidas(n, k):
    # cuantas subidas (pasos impares) hay en los k primeros pasos
    return patron(n, k).count("1")


def patrones_sin_cruce_al_final(k):
    # patrones de k pasos con 2^k <= 3^(subidas): se cuentan con combinaciones
    total = 0
    for s in range(k + 1):
        if 2 ** k <= 3 ** s:
            total = total + comb(k, s)
    return total


def sobrevivientes(k, base):
    # patrones de k pasos en los que el pronostico base^s / 2^j nunca baja de 1,
    # revisando todos los pasos j = 1, ..., k
    # cuantos[s] = patrones que llevan s subidas y siguen sin cruce
    cuantos = {0: 1}
    for j in range(1, k + 1):
        nuevos = {}
        for s in cuantos:
            for subida in [0, 1]:
                s_nuevo = s + subida
                if base ** s_nuevo >= 2 ** j:
                    nuevos[s_nuevo] = nuevos.get(s_nuevo, 0) + cuantos[s]
        cuantos = nuevos
    return sum(cuantos.values())


print("1. Las dos desigualdades")
print("   3^63 < 2^100:", 3 ** 63 < 2 ** 100)
print("   3^100 <= 2^159:", 3 ** 100 <= 2 ** 159)
assert 3 ** 63 < 2 ** 100
assert 3 ** 100 <= 2 ** 159
print("   (3^64 < 2^100 seria falso:", 3 ** 64 < 2 ** 100, ")")

print()
print("2. Patrones distintos y repetidos cada 2^k")
for k in range(1, PASOS_PATRONES + 1):
    vistos = set()
    for n in range(2 ** k):
        vistos.add(patron(n, k))
        assert patron(n, k) == patron(n + 2 ** k, k)
    assert len(vistos) == 2 ** k
print("   k = 1 ..", PASOS_PATRONES, ": los 2^k patrones salen todos, una vez cada uno")

print()
print("3. Sin cruce al paso k, contando numero por numero")
for k in range(1, PASOS_UNO_POR_UNO + 1):
    uno_por_uno = 0
    for n in range(2 ** k):
        if 2 ** k <= 3 ** subidas(n, k):
            uno_por_uno = uno_por_uno + 1
    por_patrones = patrones_sin_cruce_al_final(k)
    assert uno_por_uno == por_patrones
    print("   k =", k, ":", uno_por_uno, "numeros =", por_patrones, "patrones")

print()
print("4. El tope 2^(96m) para k = 100m")
for m in BLOQUES:
    k = 100 * m
    exactos = patrones_sin_cruce_al_final(k)
    assert exactos <= 2 ** (96 * m)
    print("   m =", m, ": fraccion exacta", f"{exactos / 2 ** k:.2e}",
          " tope 1/16^m =", f"{1 / 16 ** m:.2e}")

print()
print("5. Cuantos aguantan k pasos sin cruce (fraccion de todos los numeros)")
print("   k     casa 3n+1     vecino 5n+1")
for k in PASOS_TABLA:
    nuestra = sobrevivientes(k, 3) / 2 ** k
    vecino = sobrevivientes(k, 5) / 2 ** k
    print("  ", str(k).rjust(3), "   ", f"{nuestra:.2e}", "     ", f"{vecino:.4f}")

print()
print("OK: todo coincide.")
