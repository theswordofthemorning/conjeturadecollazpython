# A20_comp.py - COMPARADOR. Tercera implementacion, no copia nada de A20.py ni A20.lean.
# Ataques:
#  1. caso comun calculado por los dos agentes: k=6, r=27, m=5 (caso_identidad de Lean;
#     dentro del barrido exhaustivo k=0..13 del agente 2). Lo calculo con una
#     implementacion distinta (recursiva, con divmod).
#  2. premisa compartida: el convenio de S. El enunciado dice "S_k(r) = pasos impares
#     entre los k primeros iterados". Los dos agentes contaron r, T(r), ..., T^{k-1}(r).
#     Pruebo el convenio ALTERNATIVO (contar T(r), ..., T^k(r)) para ver si la identidad
#     tambien saldria con el — si saliera, la coincidencia no probaria el convenio.
#  3. r >= 2^k: el agente 1 dice que la identidad vale para r arbitrario. Lo pruebo.
#  4. "dependen SOLO del resto": para r < 2^k, dos n de la misma clase deben compartir
#     pendiente y ordenada; compruebo que S de la clase se lee igual desde cualquier
#     representante chico... (en realidad la recta se parametriza con r fijo, pero
#     compruebo que S_k(r) = S_k(2^k + r), que es lo que "solo del resto" exige).

def T(n):
    q, rem = divmod(n, 2)
    return q if rem == 0 else 3 * q + 2  # (3n+1)/2 = 3q+2 cuando n = 2q+1

def iterar(n, k):
    # version recursiva distinta de las de los agentes
    if k == 0:
        return n, 0
    x, s = iterar(T(n), k - 1)
    return x, s + (n % 2)

fallos = 0

# --- 1. caso comun ---
k, r, m = 6, 27, 5
n = 2**k * m + r
izq, _ = iterar(n, k)
tkr, s = iterar(r, k)
der = 3**s * m + tkr
print("caso comun k=6 r=27 m=5: n=%d, T^6(n)=%d, S_6(27)=%d, T^6(27)=%d, der=%d -> %s"
      % (n, izq, s, tkr, der, "IGUAL" if izq == der else "DISTINTO"))
if izq != der:
    fallos += 1

# --- 2. convenio alternativo de S: contar T(r)..T^k(r) en vez de r..T^{k-1}(r) ---
def S_alt(n, k):
    s = 0
    x = T(n)
    for _ in range(k):
        s += x % 2
        x = T(x)
    return s

contra_alt = 0
primero_alt = None
for k in range(1, 11):
    for r in range(2**k):
        for m in (1, 2):
            n = 2**k * m + r
            izq, _ = iterar(n, k)
            tkr, _ = iterar(r, k)
            der = 3**S_alt(r, k) * m + tkr
            if izq != der:
                contra_alt += 1
                if primero_alt is None:
                    primero_alt = (k, r, m, izq, der)
print("convenio alternativo (T(r)..T^k(r)): %d contraejemplos, primero=%s"
      % (contra_alt, primero_alt))

# --- 3. r >= 2^k (la generalizacion del agente 1) ---
contra_grande = 0
for k in range(0, 9):
    for r in range(2**k, 2**k + 40):
        for m in (0, 1, 7):
            n = 2**k * m + r
            izq, _ = iterar(n, k)
            tkr, s = iterar(r, k)
            if izq != 3**s * m + tkr:
                contra_grande += 1
print("r >= 2^k (agente 1 dice que vale igual): fallos = %d" % contra_grande)
fallos += contra_grande

# --- 4. S depende solo del resto (r y 2^k + r comparten S_k) ---
contra_resto = 0
for k in range(1, 13):
    for r in range(2**k):
        _, s1 = iterar(r, k)
        _, s2 = iterar(2**k + r, k)
        _, s3 = iterar(2**k * 9 + r, k)
        if s1 != s2 or s1 != s3:
            contra_resto += 1
print("S_k depende solo del resto (representantes r, 2^k+r, 9*2^k+r): fallos = %d" % contra_resto)
fallos += contra_resto

# --- 5. verificacion independiente masiva corta: k=0..12 exhaustivo, m en {0,1,4} ---
total = 0
for k in range(0, 13):
    for r in range(2**k):
        for m in (0, 1, 4):
            n = 2**k * m + r
            izq, _ = iterar(n, k)
            tkr, s = iterar(r, k)
            if izq != 3**s * m + tkr:
                fallos += 1
            total += 1
print("barrido propio k=0..12 exhaustivo en r, m en {0,1,4}: %d comprobaciones" % total)

if fallos:
    raise SystemExit("FALLOS: %d" % fallos)
print("COMPARADOR: 0 fallos en todo lo anterior")
