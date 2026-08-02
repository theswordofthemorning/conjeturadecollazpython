# A10 comparador - tercera implementacion, sin compartir codigo con A10.py
# ni con A10.lean. Ataques:
#  (1) caso comun de los dos agentes (ciclos 2/5/18, espejos m=100,101, colIter 7 27)
#  (2) identidad de un paso con una TERCERA forma (bit-ops sobre magnitud)
#  (3) intento de reproducir el 8.095.665 de la base con varios criterios de corte
#  (4) el atajo: comprobar que la identidad tambien vale ahi (por si el enunciado
#      se leyera con el otro mapa, que la ficha no especifica)

import sys

def col(n):          # Collatz clasico sobre Z, forma bit
    if n & 1:
        return 3 * n + 1
    # division exacta de par: sobre magnitud, sin floor de negativos
    return -((-n) >> 1) if n < 0 else (n >> 1)

def t31(m):          # 3m-1 clasico sobre positivos
    return 3 * m - 1 if m & 1 else m >> 1

fallos = 0

# (1a) caso comun: prefijo del 27 (Lean: colIter 7 27 = 47)
x = 27
for _ in range(7):
    x = col(x)
if x != 47:
    print("FALLO colIter 7 27 =", x); fallos += 1
else:
    print("[1a] colIter 7 27 = 47 OK (tercera implementacion)")

# (1b) ciclos: largos 2, 5, 18 desde 1, 5, 17 en 3m-1
for semilla, largo in [(1, 2), (5, 5), (17, 18)]:
    x = semilla
    vist = []
    while x not in vist:
        vist.append(x)
        x = t31(x)
    ini = vist.index(x)
    ciclo = vist[ini:]
    if len(ciclo) != largo:
        print("FALLO ciclo desde", semilla, "largo", len(ciclo)); fallos += 1
print("[1b] ciclos 3m-1 de largos 2/5/18 OK" if fallos == 0 else "[1b] hay fallos")

# (1c) espejos de 25 pasos en m=100 y m=101 (los decide de Lean)
for m in (100, 101):
    a, b = -m, m
    for _ in range(25):
        a, b = col(a), t31(b)
    if a != -b:
        print("FALLO espejo 25 pasos m =", m); fallos += 1
print("[1c] espejos 25 pasos m=100,101 OK" if fallos == 0 else "[1c] fallos")

# (2) identidad de un paso, tercera forma, m = 1..500000 (rango NO redondo a proposito: 500001 no, usamos 1..500000 mas 17 sueltos grandes y no redondos)
for m in range(1, 500001):
    if col(-m) != -t31(m):
        print("FALLO paso en m =", m); fallos += 1; break
else:
    print("[2] un paso, m = 1..500000: 0 fallos")
# bordes no redondos y grandes (limite de barrido no redondo, punto 8 de la lista)
for m in [2**31 - 1, 2**31, 10**18 + 7, 3**40 + 2, 999983]:
    if col(-m) != -t31(m):
        print("FALLO paso en m grande =", m); fallos += 1
print("[2b] casos grandes/no redondos OK" if fallos == 0 else "[2b] fallos")

# (3) reproducir el 8.095.665 de la base con distintos criterios de corte
c_sets = {}
for semilla in (1, 5, 17):
    x = semilla; vist = []
    while x not in vist:
        vist.append(x); x = t31(x)
    c_sets[semilla] = set(vist[vist.index(x):])
SUM = c_sets[1] | c_sets[5] | c_sets[17]
MINIMOS = {1, 5, 17}

def cuenta(criterio):
    total = 0
    for m in range(1, 100001):
        pos = m; pasos = 0
        if criterio == "entrada" and pos in SUM:
            total += 0; continue
        while True:
            if criterio == "entrada" and pos in SUM:
                break
            if criterio == "minimo" and pos in MINIMOS:
                break
            pos = t31(pos); pasos += 1
            if criterio == "entrada_post" and pos in SUM:
                break
            if pasos > 10**6:
                raise SystemExit("bucle")
        total += pasos
    return total

for crit in ("entrada", "entrada_post", "minimo"):
    print("[3] criterio", crit, "-> pasos totales m=1..100000:", cuenta(crit))

# (4) el atajo tambien conjuga: ((3n+1)/2 vs (3m-1)/2)
def col_a(n):
    if n & 1:
        v = 3 * n + 1
        return -((-v) >> 1) if v < 0 else (v >> 1)
    return -((-n) >> 1) if n < 0 else (n >> 1)
def t31_a(m):
    return (3 * m - 1) >> 1 if m & 1 else m >> 1
for m in range(1, 200001):
    if col_a(-m) != -t31_a(m):
        print("FALLO atajo en m =", m); fallos += 1; break
else:
    print("[4] la conjugacion vale tambien con el mapa del ATAJO, m = 1..200000: 0 fallos")

print()
print("FALLOS TOTALES:", fallos)
