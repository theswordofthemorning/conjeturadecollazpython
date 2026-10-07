"""Cotejo de la grieta (el intruso del muro A), sin Lean.

Uso, desde la raíz del repositorio:

    python -B -X utf8 depuracion/casa20261004/cotejo_grieta.py

Comprueba con cuentas exactas lo que dice CasaGrieta.lean y lo que cuenta el LEEME:

1. El descenso de Terras: para 2 <= n < 2^20, el primer descenso llega justo en el
   primer cruce (CST en ese tramo), y la condición de Lean S*3^S < 3n cubre a casi
   todos; los que quedan fuera también bajan, pero eso no lo prueba Lean.
2. Las cifras de cuenta_sin_descenso: (100m + 2)*2^(100m) frente a 2^(104m).
3. Los márgenes numéricos de margen_lmn y quince_exp, y el umbral de verdad de cada
   desigualdad.
4. El teorema E: cuántos números de cada clase podrían fallar sin LMN (los menores
   que k*2^k/3) y cuántos con LMN o Rhin (sólo el menor).
5. La casa del vecino (5n+1): allí hay grietas de verdad (el 13 y el 17), cumplen la
   versión con 5 del rasgo G1 y son el menor valor de su circuito; y una parte grande
   de los números parece escapar sin bajar nunca, así que «casi todo número baja» no
   vale allí.
6. Toda fuga y los circuitos: el margen 3001^63 <= 2^100 * 1000^63 de fuga_sube, la cota
   de crecimiento_alto en órbitas reales, y las rachas por vuelta de los circuitos que sí
   existen (5n+1 y negativos con 3n+1), que circuito_exige_25 no alcanza.
"""

from math import log2

# Números que se pueden cambiar.
LIMITE_TERRAS = 2 ** 20      # parte 1
LIMITE_VECINO = 2 ** 14      # parte 5
PASOS_VECINO = 2000
TOPE_VECINO = 2 ** 200       # si la órbita pasa de aquí sin bajar, se la da por escapada


def siguiente(n):
    """El atajo: n/2 si n es par, (3n+1)/2 si es impar."""
    if n % 2 == 0:
        return n // 2
    return (3 * n + 1) // 2


def siguiente_vecino(n):
    """El atajo de la casa del vecino, con 5n+1."""
    if n % 2 == 0:
        return n // 2
    return (5 * n + 1) // 2


def cruce_y_descenso(n, paso=siguiente, base=3):
    """Devuelve (primer cruce k, subidas S en esos k pasos, primer descenso).

    El primer cruce es el primer k con base^S < 2^k. El primer descenso es el primer
    k >= 1 con T^k(n) < n; se busca hasta 100000 pasos."""
    x = n
    s = 0
    k = 0
    cruce = None
    subidas_cruce = None
    descenso = None
    while k < 100000 and (cruce is None or descenso is None):
        s += x % 2
        x = paso(x)
        k += 1
        if cruce is None and base ** s < 2 ** k:
            cruce = k
            subidas_cruce = s
        if descenso is None and x < n:
            descenso = k
    return cruce, subidas_cruce, descenso


# 1. El descenso de Terras
print("1. Descenso de Terras: 2 <= n < 2^20")
cubiertos = 0
cubiertos_k = 0
fuera = []
for n in range(2, LIMITE_TERRAS):
    k, s, d = cruce_y_descenso(n)
    # CST en este tramo: el primer descenso es el primer cruce
    assert d == k, (n, k, d)
    # desciende_de_cruce: si S*3^S < 3n, Lean asegura el descenso en el paso k
    if s * 3 ** s < 3 * n:
        cubiertos += 1
    else:
        fuera.append((n, k))
    # desciende_si_grande: si k*2^k <= 3n, también
    if k * 2 ** k <= 3 * n:
        cubiertos_k += 1
        assert s * 3 ** s < 3 * n
total = LIMITE_TERRAS - 2
print(f"   en todos, el primer descenso es el primer cruce (CST en el tramo)")
print(f"   S*3^S < 3n (desciende_de_cruce): {cubiertos} de {total} ({cubiertos / total:.5f})")
print(f"   k*2^k <= 3n (desciende_si_grande): {cubiertos_k} de {total} ({cubiertos_k / total:.5f})")
mayor_fuera = max(fuera)
cruce_mas_largo = max(fuera, key=lambda par: par[1])
print(f"   quedan fuera {len(fuera)}; el mayor es n = {mayor_fuera[0]} (cruce {mayor_fuera[1]});")
print(f"   el cruce más largo entre ellos es el de n = {cruce_mas_largo[0]} ({cruce_mas_largo[1]} pasos)")
# Los que quedan fuera tienen un cruce largo para su tamaño: 3n <= S*3^S < k*2^k
for n, k in fuera:
    assert 3 * n < k * 2 ** k

# 2. Las cifras de cuenta_sin_descenso
print("2. cuenta_sin_descenso: por debajo de 2^(104m), a lo sumo (100m + 2)*2^(100m) no bajan")
for m in range(1, 11):
    assert (2 ** (4 * m) + 1) * 2 ** (96 * m) == 2 ** (100 * m) + 2 ** (96 * m)
    tope = (100 * m + 2) * 2 ** (100 * m)
    exponente = log2(tope) / (104 * m)
    if m in (1, 2, 5, 10):
        print(f"   m={m}: tope = x^{exponente:.4f} con x = 2^{104 * m}")
print(f"   el exponente tiende a 100/104 = {100 / 104:.4f}; Lagarias (1985) da 0,95")
no_bajan = [n for n in range(0, 2 ** 12) if cruce_y_descenso(n)[2] is None]
print(f"   entre 0 y 2^12 - 1 no bajan: {no_bajan}")
assert no_bajan == [0, 1]

# 3. Márgenes numéricos
print("3. Márgenes")
assert 99 ** 15 <= 2 * 98 ** 15
for k in range(98, 3001):
    assert k ** 15 < 3 * 2 ** k
assert not 97 ** 15 < 3 * 2 ** 97
print("   quince_exp: k^15 < 3*2^k para 98 <= k <= 3000, y falla en k = 97")
for t in range(16, 2001):
    assert 19 * (t + 33) ** 2 + t + 1 <= 2 ** t
assert not 19 * (15 + 33) ** 2 + 15 + 1 <= 2 ** 15
print("   margen_lmn: 19(t+33)^2 + t + 1 <= 2^t para 16 <= t <= 2000, y falla en t = 15")
# Umbral de verdad para LMN: el menor k con k * 2^(19(log2 k + 33)^2) < 3*2^k
k = 2
while not k * 2 ** (19 * (k.bit_length() - 1 + 33) ** 2) < 3 * 2 ** k:
    k += 1
umbral_lmn = k
print(f"   con LMN, la desigualdad k*2^(19(log2 k + 33)^2) < 3*2^k vale desde k = {umbral_lmn};")
print(f"   Lean usa k >= 2^16 = {2 ** 16}")
assert umbral_lmn <= 2 ** 16
for k in range(umbral_lmn, umbral_lmn + 2000):
    assert k * 2 ** (19 * (k.bit_length() - 1 + 33) ** 2) < 3 * 2 ** k

# 4. El teorema E
print("4. Teorema E: números de una clase módulo 2^k que podrían no bajar en su cruce k")
for k in (10, 20, 50, 98, 200):
    sin_lmn = (k * 2 ** k - 1) // 3 // 2 ** k + 1
    print(f"   k={k}: sin LMN, los menores que k*2^k/3 (hasta {sin_lmn} por clase);"
          f" con Rhin {'sólo el menor' if k >= 98 else 'todavía no'}")

# 5. La casa del vecino
print("5. La casa del vecino (5n+1)")
for g in (13, 17):
    k, s, d = cruce_y_descenso(g, siguiente_vecino, 5)
    assert k == 7 and s == 3 and d is None
    # rasgo G1 con 5: 5n <= S*5^S
    assert 5 * g <= s * 5 ** s
    # es el menor valor de su circuito
    ciclo = [g]
    x = siguiente_vecino(g)
    while x != g:
        ciclo.append(x)
        x = siguiente_vecino(x)
    assert min(ciclo) == g
    print(f"   {g}: cruza en el paso {k} (5^{s} < 2^{k}), nunca baja de sí mismo, 5*{g} <= {s}*5^{s},"
          f" y es el menor de su circuito {ciclo}")
bajan = 0
escapan = 0
otros = 0
for n in range(2, LIMITE_VECINO):
    x = n
    resultado = "otro"
    for paso in range(PASOS_VECINO):
        x = siguiente_vecino(x)
        if x < n:
            resultado = "baja"
            break
        if x > TOPE_VECINO:
            resultado = "escapa"
            break
    if resultado == "baja":
        bajan += 1
    elif resultado == "escapa":
        escapan += 1
    else:
        otros += 1
total = LIMITE_VECINO - 2
print(f"   2 <= n < 2^14: bajan {bajan / total:.3f}, pasan de 2^200 sin bajar {escapan / total:.3f},"
      f" ni lo uno ni lo otro en {PASOS_VECINO} pasos {otros / total:.3f}")
assert escapan > total // 10

# 6. Toda fuga y los circuitos
print("6. Toda fuga y los circuitos")
assert 3001 ** 63 <= 2 ** 100 * 1000 ** 63
margen = 100 - 63 * log2(3001 / 1000)
print(f"   fuga_sube: 3001^63 <= 2^100 * 1000^63, con margen de 2^{margen:.3f}")
revisados = 0
for n in range(1001, 200001, 2):
    x = n
    s_sub = 0
    for t in range(1, 401):
        if x < 1000:
            break
        s_sub += x % 2
        x = siguiente(x)
        # crecimiento_alto: 1000^S * 2^t * T^t(n) <= 3001^S * n, mientras no baje de 1000
        assert 1000 ** s_sub * 2 ** t * x <= 3001 ** s_sub * n
        revisados += 1
print(f"   crecimiento_alto se cumple en {revisados} tramos de órbitas que empiezan entre 1001 y 2*10^5")


def rachas_por_vuelta(x0, paso):
    """Rachas impares en una vuelta del circuito de x0, contadas desde su menor valor."""
    ciclo = [x0]
    x = paso(x0)
    while x != x0:
        ciclo.append(x)
        x = paso(x)
    i = ciclo.index(min(ciclo))
    ciclo = ciclo[i:] + ciclo[:i]
    rachas = 0
    for j, y in enumerate(ciclo):
        if y % 2 == 1 and (j == 0 or ciclo[j - 1] % 2 == 0):
            rachas += 1
    subidas = sum(y % 2 for y in ciclo)
    return ciclo, rachas, subidas


for g in (13, 17):
    ciclo, rachas, subidas = rachas_por_vuelta(g, siguiente_vecino)
    print(f"   5n+1, circuito del {g}: {rachas} racha(s) por vuelta; el pronóstico de una vuelta es"
          f" 5^{subidas}/2^{len(ciclo)} < 1")
    assert 5 ** subidas < 2 ** len(ciclo)


def siguiente_entero(n):
    """El atajo en los enteros con signo."""
    if n % 2 == 0:
        return n // 2
    return (3 * n + 1) // 2


for g in (-1, -5, -17):
    ciclo, rachas, subidas = rachas_por_vuelta(g, siguiente_entero)
    print(f"   3n+1 con negativos, circuito del {g}: {rachas} racha(s) por vuelta, pero el pronóstico"
          f" de una vuelta es 3^{subidas}/2^{len(ciclo)} > 1, así que su menor valor no es grieta")
    assert 3 ** subidas > 2 ** len(ciclo)

print("OK: todo coincide.")
