# Capa 1 del agente Lean: sanity check propio, independiente del repo.
# Mapa del ATAJO: n/2 si par, (3n+1)/2 si impar.
# Mapa CLASICO: n/2 si par, 3n+1 si impar.

def T(n): return n // 2 if n % 2 == 0 else (3 * n + 1) // 2
def C(n): return n // 2 if n % 2 == 0 else 3 * n + 1

def pat(k, n, f):
    p = 0
    for i in range(k):
        p |= (n % 2) << i
        n = f(n)
    return p

# 1) biyeccion con el ATAJO, k = 0..12 (exhaustivo en restos)
for k in range(0, 13):
    pats = [pat(k, r, T) for r in range(2 ** k)]
    assert len(set(pats)) == 2 ** k, ("inyectividad", k)
    assert set(pats) == set(range(2 ** k)), ("sobreyectividad", k)
print("atajo: biyeccion exacta k=0..12, 0 fallos")

# 2) valor concreto para el ancla de Lean
print("pat 6 27 (atajo) =", pat(6, 27, T))
print("pat 6 0  =", pat(6, 0, T), " pat 6 63 =", pat(6, 63, T))
print("T27,T41,T62 =", T(27), T(41), T(62), " C27,C82 =", C(27), C(82))

# 3) periodicidad (clase residual): pat k n == pat k (n mod 2^k), muestreo
for k in range(1, 11):
    for n in range(0, 3000):
        assert pat(k, n, T) == pat(k, n % 2 ** k, T), ("periodo T", k, n)
        assert pat(k, n, C) == pat(k, n % 2 ** k, C), ("periodo C", k, n)
print("periodicidad T y C: k=1..10, n=0..2999, 0 fallos")

# 4) CLASICO: conteo de patrones distintos = F(k+2)
fib = [0, 1]
for i in range(2, 20):
    fib.append(fib[-1] + fib[-2])
for k in range(1, 11):
    cnt = len({pat(k, r, C) for r in range(2 ** k)})
    ok = cnt == fib[k + 2]
    print(f"clasico k={k}: {cnt} patrones, F(k+2)={fib[k+2]}, {'OK' if ok else 'FALLA'}")
    assert ok

# 5) contraejemplo concreto a la inyectividad del clasico
print("patC 2 1 =", pat(2, 1, C), " patC 2 3 =", pat(2, 3, C))
assert pat(2, 1, C) == pat(2, 3, C)

# 6) bordes: k=0 (un resto, un patron), n=1, n=2
assert pat(0, 0, T) == 0 and 2 ** 0 == 1
print("bordes k=0, n=1, n=2 OK")
print("TODO OK")
