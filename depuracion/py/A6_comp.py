# Comparador A6: comprobaciones propias, sin abrir el repo.
# 1) caso comun v=16: padres bajo el mapa clasico
# 2) iff exhaustivo independiente hasta 60.000 (implementacion distinta: dict de preimagenes)
# 3) vortices de la trayectoria del 221 (la nota de la ficha dice 50; el conteo aritmetico?)

def T(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1

# 1) padres de 16 por fuerza bruta
padres16 = [u for u in range(1, 1000) if T(u) == 16]
print("padres de 16:", padres16)
assert sorted(padres16) == [5, 32]

# 2) iff independiente: preimagenes de v=1..60000 con u=1..120001
from collections import defaultdict
pre = defaultdict(list)
for u in range(1, 120002):
    pre[T(u)].append(u)
fallos = 0
for v in range(1, 60001):
    ps = pre[v]
    dos = (len(ps) == 2)
    if dos != (v % 6 == 4):
        fallos += 1
        print("FALLO iff en", v, ps)
    if v % 6 == 4:
        if sorted(ps) != sorted([2 * v, (v - 1) // 3]):
            fallos += 1
            print("FALLO conjunto en", v, ps)
        if (v - 1) % 3 != 0 or ((v - 1) // 3) % 2 != 1:
            fallos += 1
            print("FALLO forma en", v)
    else:
        if ps != [2 * v]:
            fallos += 1
            print("FALLO padre unico en", v, ps)
print("iff v=1..60000: fallos =", fallos)

# 3) trayectoria del 221, mapa clasico, y sus vortices (v % 6 == 4)
tray = [221]
n = 221
while n != 1:
    n = T(n)
    tray.append(n)
print("largo trayectoria 221:", len(tray))
vort = [v for v in tray if v % 6 == 4]
print("vortices aritmeticos (v%6==4):", len(vort))
print("el 4 esta en la trayectoria:", 4 in tray)
