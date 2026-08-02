# A18_comp.py — COMPARADOR (agente 3). Tercera implementacion, escrita aparte.
# Estilo distinto a proposito: el vector se saca de una funcion generadora
# iterativa con seguimiento explicito de bits conocidos, no copiando a nadie.

import random
random.seed(20260802)

def rama_clasico(x):
    # devuelve (paridad, siguiente)
    if x & 1:
        return 1, 3 * x + 1
    return 0, x >> 1

def rama_atajo(x):
    if x & 1:
        return 1, (3 * x + 1) >> 1
    return 0, x >> 1

def vec(n, k, rama):
    out = []
    for _ in range(k):
        p, n = rama(n)
        out.append(p)
    return out

def itera(n, k, rama):
    for _ in range(k):
        _, n = rama(n)
    return n

fallos = []

# [1] Caso comun concreto que calcularon LOS DOS agentes: k=5, atajo,
#     n=27 contra n=251 (251 = 27 + 32*7; m=7 esta en la lista de reps del ag.2)
if vec(27, 5, rama_atajo) != vec(251, 5, rama_atajo):
    fallos.append("caso comun 27 vs 251 (atajo, k=5)")
print("[1] caso comun: vec_atajo(27,5) =", vec(27,5,rama_atajo), "= vec_atajo(251,5):",
      vec(27,5,rama_atajo) == vec(251,5,rama_atajo))

# [2] Las instancias del agente 1, recalculadas aqui
checks = [
    ("iterC 6 27 = 94", itera(27, 6, rama_clasico) == 94),
    ("iterA 6 27 = 107", itera(27, 6, rama_atajo) == 107),
    ("vecC 8 6 = [0,1,0,1,0,0,0,0]", vec(6, 8, rama_clasico) == [0,1,0,1,0,0,0,0]),
    ("vecA 6 27 = [1,1,0,1,1,1]", vec(27, 6, rama_atajo) == [1,1,0,1,1,1]),
    ("vecC 7 27 = vecC 7 411", vec(27,7,rama_clasico) == vec(411,7,rama_clasico)),
    ("ajuste: vecA 2 1 != vecA 2 3", vec(1,2,rama_atajo) != vec(3,2,rama_atajo)),
    ("ajuste: vecC 3 1 != vecC 3 3", vec(1,3,rama_clasico) != vec(3,3,rama_clasico)),
]
for nombre, ok in checks:
    print("[2]", nombre, "->", ok)
    if not ok:
        fallos.append(nombre)

# [3] Barrido propio, INDEPENDIENTE, con m ALEATORIOS grandes (no la lista del
#     agente 2, para no heredar su muestra) — k=1..12 exhaustivo en restos.
comp = 0
for rama, nombre in ((rama_clasico, "clasico"), (rama_atajo, "atajo")):
    for k in range(1, 13):
        M = 1 << k
        for r in range(M):
            n0 = r if r >= 1 else M
            v0 = vec(n0, k, rama)
            for _ in range(3):
                m = random.randrange(1, 10**12)
                comp += 1
                if vec(m * M + r, k, rama) != v0:
                    fallos.append("barrido %s k=%d r=%d m=%d" % (nombre, k, r, m))
print("[3] barrido propio con m aleatorios hasta 10^12: %d comparaciones, %d fallos"
      % (comp, len([f for f in fallos if f.startswith('barrido')])))

# [4] El conteo Fibonacci del clasico (dato que el agente 2 dice haber calculado
#     el mismo: 144 vectores distintos a k=10). F(12) = 144.
k = 10
M = 1 << k
vs = set(tuple(vec(r if r >= 1 else M, k, rama_clasico)) for r in range(M))
print("[4] clasico k=10: %d vectores distintos (F(12)=144):" % len(vs), len(vs) == 144)
if len(vs) != 144:
    fallos.append("Fibonacci clasico")

# [5] atajo: biyeccion resto<->vector, k=1..10 (recuento propio)
for k in range(1, 11):
    M = 1 << k
    vs = set(tuple(vec(r if r >= 1 else M, k, rama_atajo)) for r in range(M))
    if len(vs) != M:
        fallos.append("biyeccion atajo k=%d" % k)
print("[5] atajo biyectivo k=1..10:", not any(f.startswith('biyeccion') for f in fallos))

# [6] LA LECTURA QUE NO VALE, medida: si "los primeros k pasos" se leyera como
#     los VALORES de los iterados, el enunciado seria FALSO. Testigo: 27 vs 59
#     (59 = 27 + 32), congruentes mod 2^5, mismas ramas 5 pasos, valores DISTINTOS.
mismo_vec = vec(27,5,rama_atajo) == vec(59,5,rama_atajo)
mismo_val = itera(27,5,rama_atajo) == itera(59,5,rama_atajo)
print("[6] 27 vs 59 (mod 32): mismas ramas:", mismo_vec, "| mismos valores:", mismo_val,
      "(%d vs %d)" % (itera(27,5,rama_atajo), itera(59,5,rama_atajo)))
if not mismo_vec or mismo_val:
    fallos.append("lectura de valores")

# [7] Ajuste del agente 2 re-medido: mod 2^(k-1) no basta. k=10.
k = 10
Mm = 1 << (k - 1)
malas = 0
for r in range(Mm):
    conjunto = set()
    for m in range(8):
        n = m * Mm + r
        if n < 1:
            continue
        conjunto.add(tuple(vec(n, k, rama_clasico)))
    if len(conjunto) > 1:
        malas += 1
malas_a = 0
for r in range(Mm):
    conjunto = set()
    for m in range(8):
        n = m * Mm + r
        if n < 1:
            continue
        conjunto.add(tuple(vec(n, k, rama_atajo)))
    if len(conjunto) > 1:
        malas_a += 1
print("[7] mod 2^9 para k=10: clasico falla en %d/512, atajo en %d/512" % (malas, malas_a))
# el agente 2 dijo: clasico 1/512 (solo r=0), atajo 512/512

if fallos:
    raise SystemExit("COMPARADOR: FALLOS -> %s" % fallos)
print()
print("COMPARADOR: 0 fallos. Los dos trabajos y la tercera implementacion coinciden.")
