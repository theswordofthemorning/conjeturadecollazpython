# A8_comp - comprobacion del COMPARADOR (tercera implementacion, sin DP y sin residuos)
# Metodo distinto a los dos agentes:
#  - alcanzables: barrido DIRECTO n = 1..400000 (sin usar la invariancia mod 2^k)
#  - "sin dos unos seguidos": enumeracion cruda con itertools.product (no DP, no filtro Lean)
#  - Fibonacci: formula recursiva con memo, convenio F(1)=F(2)=1
import itertools, sys

def paso(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1

def patron(n, k):
    out = []
    for _ in range(k):
        out.append(n & 1)
        n = paso(n)
    return tuple(out)

memo = {1: 1, 2: 1}
def F(m):
    if m not in memo:
        memo[m] = F(m - 1) + F(m - 2)
    return memo[m]

TOPE = 400000
fallos = 0
print(" k  directos  fuerza_bruta_sin11  F(k+2)")
for k in range(1, 11):
    vistos = set()
    for n in range(1, TOPE + 1):
        vistos.add(patron(n, k))
    # enumeracion cruda de cadenas sin dos 1 adyacentes
    sin11 = [c for c in itertools.product((0, 1), repeat=k)
             if all(not (c[i] == 1 and c[i + 1] == 1) for i in range(k - 1))]
    ok = len(vistos) == len(sin11) == F(k + 2) and vistos == set(sin11)
    print("%2d  %8d  %18d  %6d   %s" % (k, len(vistos), len(sin11), F(k + 2),
                                        "OK (conjuntos identicos)" if ok else "FALLO"))
    if not ok:
        fallos += 1

# caso comun concreto de los dos agentes: patron(3, 5) y anclas de la ficha
assert patron(3, 5) == (1, 0, 1, 0, 0), "patron(3,5) discrepa del Lean"
# iter 10 27 = 214 e iter 5 5 = 1 (casos conocidos del Lean)
n = 27
for _ in range(10):
    n = paso(n)
assert n == 214, "iter 10 27 != 214"
n = 5
for _ in range(5):
    n = paso(n)
assert n == 1, "iter 5 5 != 1"

if fallos:
    raise SystemExit("FALLOS: %d" % fallos)
print("TODO OK: k=1..10, conjuntos identicos, anclas 8/21/55/144, casos 27 y 5 reproducidos")
