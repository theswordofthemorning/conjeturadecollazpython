"""Cotejo del tablero del choque (paso 3, primera ronda), sin Lean.

Uso, desde la raíz del repositorio:

    python -B -X utf8 depuracion/casa20261004/cotejo_tablero.py

Comprueba con cuentas exactas lo que dice CasaTablero.lean y lo que cuenta el LEEME:

1. Los fantasmas de baile periódico: todo baile periódico que nunca cruza es el de un
   número negativo (el -1, el -5, el -17...).
2. Un fantasma sin baile periódico: un baile que nunca cruza y que no es el de ningún
   número entero, porque sus cifras binarias no terminan ni en ceros ni en unos.
3. Los testigos de Lean: el -1 vuelve a sí mismo, y en la casa del vecino (5n+1) el 13
   y el 17 cruzan a los 7 pasos sin bajar nunca de sí mismos.
4. El 7 en la casa del vecino: muchos pasos sin que su pronóstico baje de 1.
5. Rasgo 6: el tamaño va pegado al pronóstico mientras éste no baje de 1.
6. Rasgo 4 afinado: cuántos números por debajo de 2^k aguantan k pasos sin cruzar,
   contra el tope de Lean.
"""

from fractions import Fraction
import math

# Números que se pueden cambiar.
LARGO_MAXIMO = 14          # largo máximo de los bailes periódicos de la parte 1
PASOS_FANTASMA = 4000      # pasos del fantasma sin baile periódico
PASOS_VECINO = 100000      # pasos del 7 en la casa del vecino
LIMITE_TAMANO = 2 ** 15    # números de la parte 5
PASOS_TABLA = [100, 200, 300]


def siguiente(x):
    """El atajo. Sirve para enteros con signo y para fracciones de denominador impar."""
    if isinstance(x, Fraction):
        if x.numerator % 2 == 0:
            return x / 2
        return (3 * x + 1) / 2
    if x % 2 == 0:
        return x // 2
    return (3 * x + 1) // 2


def siguiente_vecino(n):
    """El atajo de la casa del vecino, con 5n+1."""
    if n % 2 == 0:
        return n // 2
    return (5 * n + 1) // 2


def nunca_cruza(baile):
    """True si el pronóstico 3^subidas/2^pasos no baja de 1 en ningún prefijo."""
    subidas = 0
    for pasos, paso in enumerate(baile, 1):
        subidas += paso
        if 3 ** subidas < 2 ** pasos:
            return False
    return True


def numero_del_baile(baile):
    """El único resto módulo 2^k cuyo baile empieza con estos k pasos."""
    modulo = 2 ** len(baile)
    inverso_de_3 = pow(3, -1, modulo)
    suma = 0
    subidas = 0
    for i, paso in enumerate(baile):
        if paso == 1:
            subidas += 1
            suma += 2 ** i * pow(inverso_de_3, subidas, modulo)
    return (-suma) % modulo


def baile_de(x, pasos):
    baile = []
    for _ in range(pasos):
        if isinstance(x, Fraction):
            baile.append(x.numerator % 2)
        else:
            baile.append(x % 2)
        x = siguiente(x)
    return baile


# 1. Fantasmas de baile periódico
print("1. Bailes periódicos que nunca cruzan")
cuantos = 0
negativos = 0
for largo in range(1, LARGO_MAXIMO + 1):
    for numero in range(2 ** largo):
        baile = [(numero >> i) & 1 for i in range(largo)]
        if not nunca_cruza(baile):
            continue
        # el número que repite este baile para siempre: x = -c / (3^s - 2^p)
        c = 0
        subidas = 0
        for i, paso in enumerate(baile):
            if paso == 1:
                c = 3 * c + 2 ** i
                subidas += 1
        x = Fraction(-c, 3 ** subidas - 2 ** largo)
        assert baile_de(x, largo) == baile
        y = x
        for _ in range(largo):
            y = siguiente(y)
        assert y == x
        cuantos += 1
        if x < 0:
            negativos += 1
print(f"   largo hasta {LARGO_MAXIMO}: {cuantos} bailes, y los {negativos} son de números negativos")
assert cuantos == negativos
for x in (-1, -5, -17):
    baile = []
    y = x
    while True:
        baile.append(y % 2)
        y = siguiente(y)
        if y == x:
            break
    print(f"   {x}: vuelve en {len(baile)} pasos con baile {''.join(map(str, baile))}")
    assert nunca_cruza(baile * 3)

# 2. Un fantasma sin baile periódico
print("2. Un fantasma sin baile periódico (subidas con pendiente 1/raíz(2))")


def techo_de(i):
    """El menor entero m con m >= i / raíz(2)."""
    m = math.isqrt(i * i // 2)
    while 2 * m * m < i * i:
        m += 1
    return m


baile = [techo_de(i + 1) - techo_de(i) for i in range(PASOS_FANTASMA)]
assert nunca_cruza(baile)
print(f"   no cruza en {PASOS_FANTASMA} pasos; empieza {''.join(map(str, baile[:30]))}...")
anteriores = None
for k in (50, 100, 200, 400, 800, 1600, 3200):
    resto = numero_del_baile(baile[:k])
    if k <= 400:
        assert baile_de(resto, k) == baile[:k]
    unos = bin(resto).count("1")
    ceros = k - unos
    print(f"   sus primeras {k:4d} cifras binarias: {unos:4d} unos y {ceros:4d} ceros")
    if anteriores is not None:
        assert unos > anteriores[0] and ceros > anteriores[1]
    anteriores = (unos, ceros)
print("   ni los unos ni los ceros se acaban: no es un entero positivo ni negativo")

# 3. Los testigos de Lean
print("3. Los testigos de Lean")
assert siguiente(-1) == -1
print("   el -1 vuelve a sí mismo: (3*(-1)+1)/2 = -1")
for x in (13, 17):
    y = x
    subidas = 0
    pasos = 0
    primer_cruce = None
    valores = []
    while True:
        subidas += y % 2
        y = siguiente_vecino(y)
        pasos += 1
        valores.append(y)
        if primer_cruce is None and 5 ** subidas < 2 ** pasos:
            primer_cruce = pasos
        if y == x:
            break
    print(f"   vecino: el {x} vuelve en {pasos} pasos, cruza a los {primer_cruce} y su menor valor es {min(valores)}")
    assert pasos == 7 and primer_cruce == 7 and min(valores) == x

# 4. El 7 en la casa del vecino
print("4. El 7 en la casa del vecino")
n = 7
subidas = 0
menor = None
log2_de_5 = math.log2(5)
for pasos in range(1, PASOS_VECINO + 1):
    subidas += n % 2
    n = siguiente_vecino(n)
    margen = subidas * log2_de_5 - pasos
    if menor is None or margen < menor[0]:
        menor = (margen, subidas, pasos)
margen, subidas_menor, pasos_menor = menor
assert 5 ** subidas_menor >= 2 ** pasos_menor
assert margen > 0.1
print(f"   {PASOS_VECINO} pasos sin cruzar; el pronóstico nunca bajó de 2^{margen:.3f}")
print(f"   (comprobado exacto en el paso {pasos_menor}); el valor final tiene {n.bit_length()} cifras binarias")

# 5. Rasgo 6: el tamaño va pegado al pronóstico
print("5. Rasgo 6: n*3^S/2^k <= T^k(n) <= (n + S/3)*3^S/2^k antes del cruce")
casos = 0
iguales = 0
for n in range(1, LIMITE_TAMANO):
    x = n
    subidas = 0
    pasos = 0
    while True:
        assert 3 ** subidas * n <= 2 ** pasos * x
        assert 3 * 2 ** pasos * x <= 3 ** subidas * (3 * n + subidas)
        casos += 1
        if 3 * 2 ** pasos * x == 3 ** subidas * (3 * n + subidas) and subidas > 0:
            iguales += 1
        if 3 ** subidas < 2 ** pasos:
            break
        subidas += x % 2
        x = siguiente(x)
        pasos += 1
print(f"   {casos} casos con n < {LIMITE_TAMANO}; la cota de arriba se alcanza justo en {iguales}")

# 6. Rasgo 4 afinado
print("6. Rasgo 4 afinado: números por debajo de 2^k que aguantan k pasos sin cruzar")
for k in PASOS_TABLA:
    # cuantos[s] = bailes de largo j, con s subidas, sin cruce hasta j
    cuantos = {0: 1}
    for j in range(1, k + 1):
        nuevos = {}
        for s, veces in cuantos.items():
            for paso in (0, 1):
                t = s + paso
                if 3 ** t >= 2 ** j:
                    nuevos[t] = nuevos.get(t, 0) + veces
        cuantos = nuevos
    total = sum(cuantos.values())
    m = k // 100
    tope = 2 * 2 ** (96 * m)
    assert total <= tope
    print(f"   k = {k}: unos 2^{math.log2(total):.2f}, bajo el tope de Lean 2*2^{96 * m}")

print("OK: todo coincide.")
