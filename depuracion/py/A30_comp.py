# A30_comp.py -- COMPARADOR (agente 3). Tercera implementacion, sin mirar
# el codigo de los otros dos al escribir la logica: brote definido SOLO por
# busqueda directa del padre impar (sin usar m % 6 == 4), y patrones por
# comparacion de tuplas completas.

def hijo_impar(m):
    # busca c impar con 3c+1 = m, por division directa (no por congruencia)
    if m >= 4 and (m - 1) % 3 == 0:
        c = (m - 1) // 3
        if c % 2 == 1:
            return c
    return None

fallos = []

# caso comun de los dos agentes: rayo v=5 -> brota en k=1,3,5 con hijos 3,13,53
esperado = {1: 3, 3: 13, 5: 53}
for k in range(0, 6):
    c = hijo_impar((1 << k) * 5)
    if (k in esperado) != (c is not None) or (c is not None and c != esperado[k]):
        fallos.append(("caso_v5", k, c))
print("caso comun v=5: brota k=1,3,5 hijos 3,13,53 ->", "OK" if not fallos else fallos)

# rayo v=1: brota en k=2 (hijo 1) y k=4 (hijo 5), no en 0,1,3
for k, esp in [(0, None), (1, None), (2, 1), (3, None), (4, 5)]:
    c = hijo_impar((1 << k) * 1)
    if c != esp:
        fallos.append(("caso_v1", k, c, esp))
print("caso comun v=1: k=2->1, k=4->5, mudo en 0,1,3 ->", "OK" if not fallos else fallos)

# claim 1 con rayos NO redondos y grandes (limite no elegido redondo: 173 rayos
# impares desde v=101 hasta v=1000003, salteados con paso primo 5779)
rayos = [101 + 5779 * i for i in range(0, 173) if (101 + 5779 * i) % 2 == 1]
KMAX = 97   # tampoco redondo
f1 = f2 = f3 = 0
tabla = {1: 0, 4: 1, 7: 2}
for v in rayos:
    pat = []
    for k in range(1, KMAX + 1):
        m = (1 << k) * v
        c = hijo_impar(m)
        b = c is not None
        # claim 1
        r = v % 3
        esp = False if r == 0 else (k % 2 == 0 if r == 1 else k % 2 == 1)
        if b != esp:
            f1 += 1
        # claim 2: tabla mod 9
        if b and tabla.get(m % 9) != c % 3:
            f2 += 1
        pat.append((b, c % 9 if b else None))
    # claim 3: repeticion cada 18
    for i in range(len(pat) - 18):
        if pat[i] != pat[i + 18]:
            f3 += 1
    # borde k=0: v impar nunca brota en k=0
    if hijo_impar(v) is not None:
        fallos.append(("k0_brota", v))
print("claims 1/2/3 sobre %d rayos impares hasta v=%d, k=1..%d: fallos = %d %d %d"
      % (len(rayos), rayos[-1], KMAX, f1, f2, f3))

# minimalidad del periodo, medida en VARIOS rayos (no solo v=5)
def permin(pat):
    for p in range(1, len(pat)):
        if all(pat[i] == pat[i + p] for i in range(len(pat) - p)):
            return p
    return None

for v in [1, 5, 7, 11, 25, 101, 335, 1001]:
    pb, p3, p9 = [], [], []
    for k in range(1, 217):
        m = (1 << k) * v
        c = hijo_impar(m)
        b = c is not None
        pb.append(b)
        p3.append((b, c % 3 if b else None))
        p9.append((b, c % 9 if b else None))
    print("  v=%4d (v%%3=%d): permin brote=%s, (brote,hijo%%3)=%s, (brote,hijo%%9)=%s"
          % (v, v % 3, permin(pb), permin(p3), permin(p9)))

# ordenes, recalculados
o = 1; x = 2 % 27
while x != 1: x = 2 * x % 27; o += 1
print("orden de 2 mod 27 =", o)
o9 = 1; x = 4 % 9
while x != 1: x = 4 * x % 9; o9 += 1
print("orden de 4 mod 9  =", o9)

if fallos:
    raise SystemExit("FALLOS: %r" % fallos[:10])
print("COMPARADOR: 0 fallos")
