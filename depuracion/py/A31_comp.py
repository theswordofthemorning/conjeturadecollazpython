# Comparador A31: verificacion propia, sin mirar el repo.
# 1) aro de 2 mod 27: visitados / evitados
# 2) mudo real en el arbol inverso del mapa CLASICO: existe k con 2^k*v = 3x+1, x impar positivo
# 3) cruce en los 200 rayos impares v=1..399 + extension
# 4) el caso comun de los dos agentes: 67 mudos de 200

vis = set()
r = 1
for _ in range(200):
    vis.add(r)
    r = (2 * r) % 27
evitados = sorted(set(range(27)) - vis)
assert evitados == [0, 3, 6, 9, 12, 15, 18, 21, 24], evitados
assert len(vis) == 18
# largo del aro
r = 1
largo = 0
while True:
    r = (2 * r) % 27
    largo += 1
    if r == 1:
        break
assert largo == 18, largo

def brota_en_k(v, k):
    w = (2 ** k) * v
    # antecesor impar x: 3x+1 = w, x impar, x >= 1
    if (w - 1) % 3 != 0:
        return False
    x = (w - 1) // 3
    return x >= 1 and x % 2 == 1

def mudo(v, kmax=60):
    return not any(brota_en_k(v, k) for k in range(kmax + 1))

# cruce: prediccion de la malla (v mod 27 evitado) contra medicion
fallos = 0
mudos_medidos = 0
for v in range(1, 400, 2):
    pred = (v % 27) in evitados
    m = mudo(v)
    if m:
        mudos_medidos += 1
    if pred != m:
        fallos += 1
assert fallos == 0, fallos
assert mudos_medidos == 67, mudos_medidos

# equivalencia con 3|v en rango mas ancho, pares incluidos
for v in range(1, 3000):
    assert mudo(v, 40) == (v % 3 == 0), v
    assert ((v % 27) in evitados) == (v % 3 == 0), v

# si 3 no divide v, el primer brote llega en k <= 2 (razon estructural)
for v in range(1, 3000):
    if v % 3 != 0:
        assert brota_en_k(v, 1) or brota_en_k(v, 2), v

# validar brote hacia adelante con el mapa clasico
def paso(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1

for v in range(1, 500):
    for k in range(0, 20):
        if brota_en_k(v, k):
            w = (2 ** k) * v
            x = (w - 1) // 3
            assert x % 2 == 1 and paso(x) == w

# la condicion w = 4 (mod 6) del CLAUDE.md equivale a la derivada de la definicion
for w in range(1, 20000):
    cond_mod6 = (w % 6 == 4)
    cond_def = (w - 1) % 3 == 0 and ((w - 1) // 3) % 2 == 1 and (w - 1) // 3 >= 1
    assert cond_mod6 == cond_def, w

print("TODO OK: evitados = multiplos de 3 (9 de 27), aro 18, 67/200 mudos, 0 fallos,")
print("mudo <-> 3|v verificado hasta 3000, brote k<=2 si 3 no divide v, mod6 = derivada.")
