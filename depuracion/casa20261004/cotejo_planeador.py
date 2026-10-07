"""Cotejo del planeador (paso 3, segunda ronda), sin Lean.

Uso, desde la raíz del repositorio:

    python -B -X utf8 depuracion/casa20261004/cotejo_planeador.py

Comprueba con cuentas exactas lo que dice CasaPlaneador.lean y lo que cuenta el LEEME:

1. Los patrones casi fugitivos: entre los subconjuntos de {0..100m-1}, los que cumplen
   2^(100m) <= 3^c * 3^|A| son a lo sumo 2^c * 2^(96m) (pocos_patrones_nivel).
2. Un número por patrón: entre 0 y 2^L - 1, los números con 2^L <= 3^c * 3^(subidas)
   son tantos como los patrones de largo L que lo cumplen.
3. La casa del vecino (5n+1): allí los casi fugitivos no son raros, así que la cuenta
   no pasa.
4. El fantasma que vuela siempre bajo: un baile cuyo pronóstico queda siempre entre
   1 y 3. Es el de un número con infinitas cifras binarias, no el de un entero.
5. Los momentos bajos de verdad: en los números que más pasos aguantan sin cruzar,
   qué fracción del camino pasan con el pronóstico bajo, y las cotas de Lean
   (chico_si_bajo, casi_fuga_de_bajo) en cada momento bajo.
6. Las cifras de tiempos_bajos_potencia y de techo_crece.
"""

from math import comb, log2

# Números que se pueden cambiar.
NIVELES = [0, 1, 2, 5, 10, 30]   # exponentes c del nivel 3^c
LARGO_NUMEROS = 18               # parte 2: números entre 0 y 2^LARGO_NUMEROS - 1
LIMITE_VECINO = 2 ** 16          # parte 3
PASOS_VECINO = [20, 40, 60, 80]
PASOS_FANTASMA = 2000            # parte 4
LIMITE_RECORDS = 2 ** 22         # parte 5: se buscan récords entre los n < LIMITE_RECORDS


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


def subidas_minimas(largo, c, base=3):
    """El menor s con 2^largo <= base^c * base^s."""
    s = 0
    while 2 ** largo > base ** (c + s):
        s += 1
    return s


def subidas_en(n, largo):
    s = 0
    for _ in range(largo):
        s += n % 2
        n = siguiente(n)
    return s


# 1. Patrones casi fugitivos
print("1. Patrones de largo 100m con 2^(100m) <= 3^c * 3^|A|, contra el tope 2^c * 2^(96m)")
for m in range(1, 7):
    largo = 100 * m
    for c in NIVELES:
        minimo = subidas_minimas(largo, c)
        cuenta = sum(comb(largo, s) for s in range(minimo, largo + 1))
        tope = 2 ** c * 2 ** (96 * m)
        assert cuenta <= tope, (m, c)
        if c in (0, 10):
            print(f"   m={m}, c={c:2d}: unos 2^{log2(cuenta):.2f}, tope 2^{log2(tope):.0f}")
print("   todos bajo el tope, para c en", NIVELES)

# 2. Un número por patrón
print(f"2. Números entre 0 y 2^L - 1 con 2^L <= 3^c * 3^(subidas), para L <= {LARGO_NUMEROS}")
for largo in range(1, LARGO_NUMEROS + 1):
    # cuantos[s] = números entre 0 y 2^largo - 1 con s subidas en largo pasos
    cuantos = {}
    for n in range(2 ** largo):
        s = subidas_en(n, largo)
        cuantos[s] = cuantos.get(s, 0) + 1
    for s in range(largo + 1):
        assert cuantos.get(s, 0) == comb(largo, s), (largo, s)
    for c in (0, 1, 2):
        minimo = subidas_minimas(largo, c)
        por_numeros = sum(v for s, v in cuantos.items() if s >= minimo)
        por_patrones = sum(comb(largo, s) for s in range(minimo, largo + 1))
        assert por_numeros == por_patrones
print("   coinciden: con s subidas hay justo C(L, s) números, para todo L y s")

# 3. La casa del vecino
print("3. Casa del vecino: fracción de casi fugitivos entre los n <", LIMITE_VECINO)


def es_casi_fuga(n, c, pasos, base):
    """True si en los primeros pasos el pronóstico nunca baja de 1/base^c."""
    potencia_de_2 = 1
    potencia_de_base = base ** c
    for _ in range(pasos):
        if n % 2 == 1:
            potencia_de_base *= base
        if base == 3:
            n = siguiente(n)
        else:
            n = siguiente_vecino(n)
        potencia_de_2 *= 2
        if potencia_de_2 > potencia_de_base:
            return False
    return True


for base in (3, 5):
    for c in (0, 1):
        fila = []
        for pasos in PASOS_VECINO:
            cuenta = sum(1 for n in range(LIMITE_VECINO) if es_casi_fuga(n, c, pasos, base))
            fila.append(cuenta / LIMITE_VECINO)
        texto = ", ".join(f"{f:.5f}" for f in fila)
        print(f"   {base}n+1, nivel {base}^{c}, a {PASOS_VECINO} pasos: {texto}")
        if base == 5:
            assert fila[-1] > 0.15
        else:
            assert fila[-1] < 0.01
minimo = subidas_minimas(100, 0, base=5)
cuenta = sum(comb(100, s) for s in range(minimo, 101))
print(f"   con 5n+1, los patrones de largo 100 que no cruzan al final son unos 2^{log2(cuenta):.2f},")
print(f"   más que el tope 2^96: la cuenta de patrones no da rareza allí")
assert cuenta > 2 ** 96

# 4. El fantasma que vuela siempre bajo
print("4. El fantasma que vuela siempre bajo")
# subidas del fantasma en los primeros j pasos: el menor s con 3^s >= 2^j
subidas_fantasma = [subidas_minimas(j, 0) for j in range(PASOS_FANTASMA + 1)]
baile = [subidas_fantasma[j + 1] - subidas_fantasma[j] for j in range(PASOS_FANTASMA)]
assert all(paso in (0, 1) for paso in baile)
for j in range(PASOS_FANTASMA + 1):
    s = subidas_fantasma[j]
    assert 2 ** j <= 3 ** s < 3 * 2 ** j
print(f"   en {PASOS_FANTASMA} pasos su pronóstico queda entre 1 y 3: empieza {''.join(map(str, baile[:30]))}...")


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


anterior = None
for largo in (50, 100, 200, 400, 800, 1600):
    resto = numero_del_baile(baile[:largo])
    if largo <= 400:
        x = resto
        for paso in baile[:largo]:
            assert x % 2 == paso
            x = siguiente(x)
    if anterior is not None:
        assert resto % 2 ** anterior[0] == anterior[1]
    unos = bin(resto).count("1")
    print(f"   sus primeras {largo:4d} cifras binarias: {unos:4d} unos y {largo - unos:4d} ceros")
    anterior = (largo, resto)
# el baile no se vuelve periódico: ningún periodo p <= 300 desde ningún paso a <= 300
for a in range(301):
    for p in range(1, 301):
        assert any(baile[i] != baile[i + p] for i in range(a, PASOS_FANTASMA - p))
print("   ni los unos ni los ceros se acaban, y su baile no es periódico (periodos <= 300):")
print("   su órbita no repite valores, pero no es un entero: el tamaño no existe para él")

# 5. Los momentos bajos de verdad
print(f"5. Récords de pasos sin cruzar entre los n < {LIMITE_RECORDS}")


def primer_cruce(n, tope):
    """Primer j con 3^S_j < 2^j, o None si no cruza antes de tope."""
    potencia_de_3 = 1
    potencia_de_2 = 1
    x = n
    for j in range(1, tope + 1):
        if x % 2 == 1:
            potencia_de_3 *= 3
        x = siguiente(x)
        potencia_de_2 *= 2
        if potencia_de_3 < potencia_de_2:
            return j
    return None


records = []
mejor = 0
for n in range(3, LIMITE_RECORDS, 4):  # los demás cruzan en uno o dos pasos
    t = primer_cruce(n, 10000)
    if t > mejor:
        mejor = t
        records.append((n, t))
print("   récords (n, primer cruce):", ", ".join(f"({n}, {t})" for n, t in records[-8:]))
for n, t in records[-6:]:
    x = n
    s = 0
    vistos = set()
    bajos = {0: 0, 1: 0, 2: 0}
    for j in range(t):
        assert x not in vistos
        vistos.add(x)
        for c in bajos:
            if 3 ** s <= 3 ** c * 2 ** j:
                bajos[c] += 1
                # chico_si_bajo: T^j(n) <= 3^c (n + j)
                assert x <= 3 ** c * (n + j)
                # casi_fuga_de_bajo, mientras dura el camino sin cruce
                y = x
                sy = 0
                for i in range(1, t - j):
                    sy += y % 2
                    y = siguiente(y)
                    assert 2 ** i <= 3 ** c * 3 ** sy
        s += x % 2
        x = siguiente(x)
    texto = ", ".join(f"nivel 3^{c}: {bajos[c] / t:.3f}" for c in bajos)
    print(f"   n = {n}: {t} pasos sin cruzar; fracción de momentos bajos: {texto}")

# 6. Las cifras de tiempos_bajos_potencia
print("6. tiempos_bajos_potencia: en los primeros k = 2^(100m) pasos, pronóstico > 3^m salvo en")
print("   una fracción 3*(3/8)^m; como 3^m = k^0,01585, el nivel es una potencia del tiempo")
for m in range(1, 6):
    fraccion = 3 * (3 / 8) ** m
    nivel = log2(3) / 100
    print(f"   m={m}: fracción {fraccion:.4f}, nivel 3^{m} = k^{nivel:.5f}")
    assert 3 * 6 ** m * 2 ** (96 * m) * 8 ** m == 3 * 3 ** m * 2 ** (100 * m)
# techo_crece: desde m = 2 los momentos bajos no alcanzan para todos los pasos
assert 3 * 6 ** 1 >= 16 ** 1
for m in range(2, 40):
    assert 3 * 6 ** m * 2 ** (96 * m) < 2 ** (100 * m)
print("   techo_crece: desde m = 2, 3*6^m*2^(96m) < 2^(100m), así que algún paso pasa de 3^m")

print("OK: todo coincide.")
