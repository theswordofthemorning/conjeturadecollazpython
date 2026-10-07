"""Cotejo de la densidad exacta de Terras (CasaTerras.lean), sin Lean.

Uso, desde la raíz del repositorio:

    python -B -X utf8 depuracion/casa20261004/cotejo_terras.py

Comprueba con cuentas exactas lo que dice CasaTerras.lean y lo que cuenta el LEEME:

1. congruentes_mismo_baile: números congruentes módulo 2^k tienen las mismas k primeras
   paridades.
2. baja_iff_cruza: para k*2^k <= 3n, bajar en a lo sumo k pasos es cruzar en a lo sumo k pasos.
3. densidad_terras: F(k) = |A_k|/2^k, con A_k los restos módulo 2^k cuyo pronóstico cruza en a
   lo sumo k pasos, frente a la proporción real de los n de [2^20, 2^21) que bajan en a lo sumo
   k pasos.
4. terras_tiende_a_uno: F(k) crece hacia 1.
5. teorema_B y primer_cruce_resto: el baile de k pasos es una biyección entre los restos módulo
   2^k y los patrones de largo k, y el primer cruce depende sólo del resto.
"""

import random

# Números que se pueden cambiar.
K_MAX = 18          # parte 3: F(k) para k <= K_MAX
TRAMO = 20          # parte 3: los n de [2^TRAMO, 2^(TRAMO+1))
SEMILLA = 20261007


def siguiente(n):
    """El atajo: n/2 si n es par, (3n+1)/2 si es impar."""
    if n % 2 == 0:
        return n // 2
    return (3 * n + 1) // 2


def paridades(n, k):
    salida = []
    for _ in range(k):
        salida.append(n % 2)
        n = siguiente(n)
    return salida


def cruza_en(n, k):
    """¿Hay j <= k con 3^S_j(n) < 2^j?"""
    s = 0
    x = n
    for j in range(1, k + 1):
        s += x % 2
        x = siguiente(x)
        if 3 ** s < 2 ** j:
            return True
    return False


def baja_en(n, k):
    """¿Hay 1 <= j <= k con T^j(n) < n?"""
    x = n
    for _ in range(k):
        x = siguiente(x)
        if x < n:
            return True
    return False


# 1. Congruentes, mismo baile
print("1. congruentes_mismo_baile")
azar = random.Random(SEMILLA)
for _ in range(20000):
    k = azar.randrange(1, 40)
    n = azar.randrange(0, 2 ** 60)
    n2 = n % 2 ** k + 2 ** k * azar.randrange(0, 2 ** 40)
    assert paridades(n, k) == paridades(n2, k)
print("   20000 pares congruentes módulo 2^k (k < 40) tienen las mismas k primeras paridades")

# 2. Bajar es cruzar, para n grande
print("2. baja_iff_cruza")
casos = 0
for k in range(1, 15):
    desde = -(-k * 2 ** k // 3)
    for n in range(max(desde, 1), max(desde, 1) + 3000):
        assert baja_en(n, k) == cruza_en(n, k)
        casos += 1
print(f"   coincide en {casos} casos (k < 15, 3000 números desde k*2^k/3)")

# 3. La densidad exacta
print("3. F(k) = |A_k|/2^k frente a la proporción real en [2^20, 2^21)")
tabla = []
for k in range(1, K_MAX + 1):
    restos = sum(1 for r in range(2 ** k) if cruza_en(r, k))
    tabla.append(restos / 2 ** k)
# proporción real, con una sola pasada por número
bajan_en = [0] * (K_MAX + 1)
total = 2 ** TRAMO
for n in range(2 ** TRAMO, 2 ** (TRAMO + 1)):
    x = n
    for j in range(1, K_MAX + 1):
        x = siguiente(x)
        if x < n:
            bajan_en[j] += 1
            break
acumulado = 0
for k in range(1, K_MAX + 1):
    acumulado += bajan_en[k]
    real = acumulado / total
    if k in (1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 18):
        print(f"   k={k:<2}: F(k) = {tabla[k - 1]:.6f}; real {real:.6f}")
    # si k*2^k <= 3*2^20, baja_iff_cruza vale en todo el tramo: deben coincidir exactamente
    if k * 2 ** k <= 3 * 2 ** TRAMO:
        assert abs(real - tabla[k - 1]) < 1e-12, (k, real, tabla[k - 1])

# 4. F(k) crece hacia 1
print("4. F(k) crece")
for k in range(1, K_MAX):
    assert tabla[k] >= tabla[k - 1]
print(f"   F(1) = {tabla[0]:.4f}, F(10) = {tabla[9]:.4f}, F({K_MAX}) = {tabla[K_MAX - 1]:.4f}")

# 5. Teoremas B y C
print("5. Teoremas B y C")
for k in range(1, 15):
    patrones = set(tuple(paridades(r, k)) for r in range(2 ** k))
    assert len(patrones) == 2 ** k


def primer_cruce(n, tope=500):
    s = 0
    x = n
    for j in range(1, tope + 1):
        s += x % 2
        x = siguiente(x)
        if 3 ** s < 2 ** j:
            return j
    return None


casos = 0
for _ in range(5000):
    n = azar.randrange(2, 2 ** 50)
    k = primer_cruce(n)
    if k is not None and k <= 40:
        assert primer_cruce(n % 2 ** k) == k
        casos += 1
print(f"   para k < 15 los 2^k restos dan 2^k patrones distintos; en {casos} números el primer cruce")
print("   es el mismo que el de su resto módulo 2^k")

print("OK: todo coincide.")
