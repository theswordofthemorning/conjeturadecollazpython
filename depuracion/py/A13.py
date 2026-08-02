# A13 - verificacion independiente, escrita desde cero.
#
# ENUNCIADO (ficha A13): "el espejo en base 2 baja estrictamente, luego toda
# orbita cae en una potencia de 2", para todo n >= 1. Estado: demostrado.
#
# DEFINICION que uso (derivada de la nota algebraica de la ficha, que es la
# unica definicion consistente con "si 2^(k-1) < n < 2^k entonces
# 2^k - n < 2^(k-1)" y con el analogo base 10 de fijos en 5*10^m):
#
#   sea k el numero de bits de n, o sea 2^(k-1) <= n < 2^k.
#   espejo(n) = 2^k - n        (el complemento respecto de la potencia de 2
#                               inmediatamente superior o igual al techo del bloque)
#
#   - si n = 2^(k-1) (potencia de 2): espejo(n) = 2^(k-1) = n  -> punto fijo.
#   - si 2^(k-1) < n < 2^k: espejo(n) = 2^k - n, con 1 <= espejo(n) < 2^(k-1).
#
# NOTA DE MAPA: esto NO es el mapa de Collatz (ni clasico, ni atajo, ni 3n-1).
# Es un mapa auxiliar del repo ("espejo en base 2"). No hay confusion de mapas
# posible porque no interviene ninguno de los tres.
#
# Todo con enteros de Python. Ningun float decide nada.

RANGO = 500_000          # verificado exhaustivo 1 .. RANGO
fallos = []

def espejo(n):
    if n < 1:
        raise ValueError("solo n >= 1")
    k = n.bit_length()           # 2^(k-1) <= n < 2^k
    return (1 << k) - n if n != (1 << (k - 1)) else n
    # para potencia de 2 devuelve n (punto fijo). Ojo: si se usara el convenio
    # "potencia estrictamente mayor" tambien daria n: 2^k - 2^(k-1) = 2^(k-1).

def es_pot2(n):
    return n >= 1 and (n & (n - 1)) == 0

# --- COMPROBACION 0: la desigualdad de la nota, algebraica y por barrido ---
# si 2^(k-1) < n < 2^k entonces 1 <= 2^k - n < 2^(k-1)
for n in range(1, RANGO + 1):
    if not es_pot2(n):
        k = n.bit_length()
        e = (1 << k) - n
        if not (1 <= e < (1 << (k - 1))):
            fallos.append(("desigualdad", n, e))
if fallos:
    raise SystemExit("FALLO en la desigualdad base: " + repr(fallos[:5]))
print("[0] desigualdad 1 <= 2^k - n < 2^(k-1) para todo no-potencia: 0 fallos en 1..%d" % RANGO)

# --- COMPROBACION 1: descenso ESTRICTO fuera de las potencias de 2 ---
peor = None
for n in range(1, RANGO + 1):
    e = espejo(n)
    if es_pot2(n):
        if e != n:
            fallos.append(("fijo", n, e))
    else:
        if not (e < n):
            fallos.append(("no baja", n, e))
        # de hecho baja de bloque: bit_length estrictamente menor
        if e.bit_length() >= n.bit_length():
            fallos.append(("no baja de bloque", n, e))
if fallos:
    raise SystemExit("FALLO en el descenso: " + repr(fallos[:5]))
print("[1] espejo(n) < n para toda no-potencia (y baja de bloque de bits); potencias fijas: 0 fallos en 1..%d" % RANGO)

# --- COMPROBACION 2: toda orbita cae en una potencia de 2, y contar ciclos ---
largos_ciclo = {}
max_pasos = 0
for n in range(1, RANGO + 1):
    x = n
    pasos = 0
    while not es_pot2(x):
        x = espejo(x)
        pasos += 1
        if pasos > 200:
            fallos.append(("no termina", n))
            break
    else:
        # llego a una potencia de 2; comprobar que es punto fijo (ciclo de largo 1)
        if espejo(x) != x:
            fallos.append(("terminal no fijo", n, x))
        largos_ciclo[1] = largos_ciclo.get(1, 0) + 1
        if pasos > max_pasos:
            max_pasos = pasos
if fallos:
    raise SystemExit("FALLO en la caida: " + repr(fallos[:5]))
print("[2] toda orbita 1..%d cae en una potencia de 2 (punto fijo). pasos maximos hasta caer: %d" % (RANGO, max_pasos))
print("    largos de ciclo encontrados: %s (esperado: solo 1)" % repr(largos_ciclo))

# --- COMPROBACION 3: reproducir el numero de la base: 1..100.000 -> {1: 100000} ---
cuenta = 0
for n in range(1, 100_001):
    x = n
    guard = 0
    while not es_pot2(x):
        x = espejo(x)
        guard += 1
        if guard > 200:
            raise SystemExit("FALLO reproduciendo 1..100000 en n=%d" % n)
    cuenta += 1   # cada orbita termina en un ciclo de largo 1
print("[3] 1..100000: largos de ciclo {1: %d} -- la cifra de la base era {1: 100000}" % cuenta)
if cuenta != 100_000:
    raise SystemExit("FALLO: no salen 100000 ciclos de largo 1")

# --- COMPROBACION 4: bordes explicitos ---
bordes = {
    1: 1,            # n=1 es 2^0: fijo
    2: 2,            # potencia: fijo
    3: 1,            # 4-3=1
    4: 4,
    5: 3,            # 8-5=3
    7: 1,            # 8-7=1
    6: 2,            # 8-6=2
    2**20: 2**20,            # potencia grande: fija
    2**20 + 1: 2**21 - (2**20 + 1),   # justo encima de una potencia
    2**20 - 1: 1,            # justo debajo: 2^20 - (2^20-1) = 1
}
for n, esperado in bordes.items():
    got = espejo(n)
    if got != esperado:
        raise SystemExit("FALLO borde: espejo(%d) = %d, esperado %d" % (n, got, esperado))
print("[4] bordes n=1,2,3,4,5,6,7, 2^20-1, 2^20, 2^20+1: todos como se esperaba")

# --- COMPROBACION 5: el argumento de terminacion no depende del barrido ---
# espejo baja el bit_length en cada paso no fijo (comprobado en [1]), luego una
# orbita desde n tiene a lo sumo bit_length(n) pasos antes de caer. Muestreo
# con numeros grandes sueltos (no cabe barrido):
import random
random.seed(13)
for _ in range(200):
    n = random.getrandbits(600) | (1 << 599)   # numeros de 600 bits
    x, pasos = n, 0
    while not es_pot2(x):
        x = espejo(x)
        pasos += 1
        if pasos > 600:
            raise SystemExit("FALLO: orbita de mas de 600 pasos en 600 bits")
print("[5] 200 semillas de 600 bits: todas caen en una potencia de 2 en <= 600 pasos (cota = bits)")

print()
print("VEREDICTO LOCAL: 0 fallos. El enunciado se sostiene tal cual esta escrito.")
