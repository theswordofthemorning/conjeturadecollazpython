# A3_comp.py - COMPARADOR. Tercera implementacion, sin mirar la de los agentes
# al escribir las definiciones (las escribo desde el enunciado). Ataques:
#  (a) caso comun 27 y 31 calculados por los dos agentes -> los recalculo yo
#  (b) barrido corto propio con limite NO redondo (61 237)
#  (c) la premisa compartida: racha = racha INICIAL. El enunciado literal no
#      define racha. Pruebo la lectura alternativa (racha maxima de impares en
#      cualquier punto de la trayectoria) a ver si el piso sobrevive con ella.
#  (d) borde n = 1 con las dos convenciones.

def T(n):
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2

def racha_inicial(n):
    r = 0
    while n % 2 == 1:
        r += 1
        n = T(n)
    return r

def tray(n):
    xs = [n]
    while n != 1:
        n = T(n)
        xs.append(n)
    return xs

def alt(n):
    return max(tray(n))

# (a) casos comunes
t27 = tray(27)
assert t27[:4] == [27, 41, 62, 31], t27[:4]
r27 = racha_inicial(27)
assert r27 == 2
assert alt(27) * 2**2 >= 27 * 3**2  # alt(27)>=62 -> >=248 vs 243
print("[a] 27: racha 2, iter2 = 62, 3^2*27 = 243 <= 2^2*62 = 248: OK (los dos agentes)")
r31 = racha_inicial(31)
v = 31
for _ in range(r31):
    v = T(v)
assert r31 == 5 and v == 242
assert 3**5 * 31 == 7533 and 2**5 * 242 == 7744 and 7533 <= 7744
print("[a] 31: racha 5, v_5 = 242, 7533 <= 7744: OK (los dos agentes)")

# (b) barrido propio con limite no redondo
fallos = 0
igualdades_r0 = 0
igualdades_rpos = 0
for n in range(2, 61238):
    r = racha_inicial(n)
    a = alt(n)
    if a * 2**r < n * 3**r:
        fallos += 1
        print("CONTRAEJEMPLO", n)
    elif a * 2**r == n * 3**r:
        if r == 0:
            igualdades_r0 += 1
        else:
            igualdades_rpos += 1
print("[b] barrido n = 2..61237 (limite no redondo): fallos =", fallos,
      "| igualdades r=0:", igualdades_r0, "| igualdades r>=1:", igualdades_rpos)

# (c) lectura alternativa de racha: la racha MAXIMA de impares en toda la
# trayectoria (no solo al arranque). Si el piso tambien valiera con ella, la
# ambiguedad no importaria; si falla, la premisa compartida ES sustancial.
def racha_maxima(n):
    mejor = 0
    cur = 0
    for x in tray(n):
        if x % 2 == 1 and x != 1:
            cur += 1
            if cur > mejor:
                mejor = cur
        else:
            cur = 0
    return mejor

contra = []
for n in range(2, 20001):
    r = racha_maxima(n)
    a = alt(n)
    if a * 2**r < n * 3**r:
        contra.append(n)
print("[c] con racha = MAXIMA en la trayectoria: contraejemplos hasta 20000:",
      len(contra), "primeros:", contra[:5])

# (d) borde n = 1
print("[d] n=1 convencion parar-en-1: alt=1, racha=1 ->", 1 * 2 >= 1 * 3)
print("[d] n=1 convencion con vuelta:  alt=2, racha=1 ->", 2 * 2 >= 1 * 3)

# (e) el conteo declarado del repo: 99.999 casos en n=2..100000
print("[e] n=2..100000 son", 100000 - 2 + 1, "casos")
