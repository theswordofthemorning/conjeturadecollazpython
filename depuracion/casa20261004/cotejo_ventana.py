"""Cotejo de la ventana de Korec (casi toda órbita baja por debajo de n^0,8), sin Lean.

Uso, desde la raíz del repositorio:

    python -B -X utf8 depuracion/casa20261004/cotejo_ventana.py

Comprueba con cuentas exactas lo que dice CasaVentana.lean y lo que cuenta el LEEME:

1. Los cuatro márgenes numéricos (margen_pronostico, margen_viento, margen_viento_debil,
   margen_pesos) y cuánto sobra en cada uno.
2. Los patrones de largo 1000 con al menos 503 subidas: la cuenta exacta, la cota con pesos
   503 y 497, y 2^1000.
3. La cota de tamano_general en órbitas reales.
4. El umbral de Korec en números de verdad: qué fracción de los n de cada tramo [2^j, 2^(j+1))
   baja por debajo de n^0,8 en a lo sumo log2(n) pasos, y lo mismo con 0,75, que está por
   debajo del umbral log 3/log 4 = 0,7925.
"""

from math import comb, log2

# Números que se pueden cambiar.
TRAMOS = range(8, 19)        # parte 4: tramos [2^j, 2^(j+1))


def siguiente(n):
    """El atajo: n/2 si n es par, (3n+1)/2 si es impar."""
    if n % 2 == 0:
        return n // 2
    return (3 * n + 1) // 2


# 1. Los márgenes
print("1. Márgenes")
assert 8 * (3 ** 2515 * 2 ** 1010) <= 2 ** 5000
print(f"   margen_pronostico: 8*3^2515*2^1010 <= 2^5000, sobran 2^{5000 - (3 + 2515 * log2(3) + 1010):.3f}")
assert 32 * 3 ** 5000 < 2 ** 9000
assert 3 ** 5000 <= 2 ** 9000
print(f"   margen_viento: 32*3^5000 < 2^9000, sobran 2^{9000 - (5 + 5000 * log2(3)):.1f}")
assert 1000 ** 1000 < 2 ** 1000 * 503 ** 503 * 497 ** 497
sobra = 1000 + 503 * log2(503) + 497 * log2(497) - 1000 * log2(1000)
print(f"   margen_pesos: 1000^1000 < 2^1000*503^503*497^497, sobran 2^{sobra:.4f}")

# 2. Los patrones
print("2. Patrones de largo 1000 con al menos 503 subidas")
exacto = sum(comb(1000, s) for s in range(503, 1001))
cota = 1000 ** 1000 // (503 ** 503 * 497 ** 497)
assert exacto <= cota < 2 ** 1000
print(f"   exactos 2^{log2(exacto):.4f}; cota con pesos 2^{log2(cota):.4f}; total 2^1000")
print("   por bloque de 1000 pasos la cota pierde sólo 2^-0,026: la densidad cero llega muy despacio")

# 3. tamano_general
print("3. tamano_general: 2^k*T^k(n) + 2^k <= 3^S*n + 3^k")
casos = 0
for n in range(1, 20001):
    x = n
    s = 0
    for k in range(1, 61):
        s += x % 2
        x = siguiente(x)
        assert 2 ** k * x + 2 ** k <= 3 ** s * n + 3 ** k
        casos += 1
print(f"   se cumple en {casos} casos (n <= 20000, k <= 60)")

# 4. El umbral de Korec
print("4. Fracción que baja por debajo de n^theta en a lo sumo log2(n) pasos")


def baja(n, num, den):
    """¿Hay k <= log2(n) con T^k(n)^den < n^num?"""
    tope = n ** num
    x = n
    for k in range(n.bit_length()):
        if x ** den < tope:
            return True
        x = siguiente(x)
    return False


print("   tramo      theta=0,8   theta=0,75")
fracciones = {}
for j in TRAMOS:
    total = 2 ** j
    con_08 = 0
    con_075 = 0
    for n in range(2 ** j, 2 ** (j + 1)):
        if baja(n, 4, 5):
            con_08 += 1
        if baja(n, 3, 4):
            con_075 += 1
    fracciones[j] = (con_08 / total, con_075 / total)
    print(f"   2^{j:<2}       {con_08 / total:.4f}      {con_075 / total:.4f}")
# con 0,8 bajan más que con 0,75 en cada tramo (es más fácil bajar menos)
for j in TRAMOS:
    assert fracciones[j][0] >= fracciones[j][1]

print("OK: todo coincide.")
