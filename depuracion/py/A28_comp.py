# A28_comp - comparador (agente 3). Tercera implementacion, sin mirar las otras dos
# mas que para elegir QUE contrastar. Todo int puro.

fallos = 0

def T(n):  # atajo
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2

def Tc(n):  # clasico
    return n // 2 if n % 2 == 0 else 3 * n + 1

def pv(n, k, f):
    v = []
    for _ in range(k):
        v.append(n & 1)
        n = f(n)
    return tuple(v)

# CASO COMUN 1: pv 8 27 (agente 1 lo tiene por decide; agente 2 lo cubre en su exhaustivo)
esperado = (1, 1, 0, 1, 1, 1, 1, 1)
tray = [27]
for _ in range(7):
    tray.append(T(tray[-1]))
if pv(27, 8, T) != esperado or tray != [27, 41, 62, 31, 47, 71, 107, 161]:
    fallos += 1
    print("FALLO caso 27:", pv(27, 8, T), tray)
else:
    print("caso 27 OK: pv=%s tray=%s" % (pv(27, 8, T), tray))

# CASO COMUN 2: extremos k=6
if pv(0, 6, T) != (0,) * 6 or pv(63, 6, T) != (1,) * 6:
    fallos += 1
    print("FALLO extremos")
else:
    print("extremos k=6 OK")

# CASO COMUN 3: biyeccion exhaustiva k=0..16 (lo de agente 2; agente 1 lo tiene
# demostrado para todo k y por decide en k=6)
for k in range(0, 17):
    M = 1 << k
    vistos = {pv(r, k, T) for r in range(M)}
    if len(vistos) != M:
        fallos += 1
        print("FALLO biyeccion k=%d: %d de %d" % (k, len(vistos), M))
print("biyeccion exhaustiva k=0..16: fallos=%d" % fallos)

# CASO COMUN 4: control clasico. Contraejemplo minimo de agente 1 (1 vs 3 mod 4)
# y conteo Fibonacci de agente 2.
if pv(1, 2, Tc) != pv(3, 2, Tc) or (1 % 4) == (3 % 4):
    fallos += 1
    print("FALLO contraejemplo clasico")
else:
    print("clasico: pv2(1)=pv2(3)=%s con 1!=3 mod 4 OK" % (pv(1, 2, Tc),))

def fib(j):
    a, b = 0, 1
    for _ in range(j):
        a, b = b, a + b
    return a

for k in (4, 6, 8, 10, 12):
    M = 1 << k
    n = len({pv(r, k, Tc) for r in range(M)})
    if n != fib(k + 2):
        fallos += 1
        print("FALLO fibonacci k=%d: %d != %d" % (k, n, fib(k + 2)))
print("clasico F(k+2): OK hasta k=12" if fallos == 0 else "fallos=%d" % fallos)

# ATAQUE al testigo explicito de suryectividad del agente 1:
# para bit 1 y cola s < 2^k, r = (u*(2s + 2^(k+1) - 1)) mod 2^(k+1),
# con 3u = 1 mod 2^(k+1). Debe salir r impar, r < 2^(k+1), T(r) = s mod 2^k.
for k in range(0, 11):
    P = 1 << (k + 1)
    u = pow(3, -1, P)
    for s in range(1 << k):
        r = (u * (2 * s + P - 1)) % P
        if r % 2 != 1 or r >= P or T(r) % (1 << k) != s:
            fallos += 1
            print("FALLO testigo k=%d s=%d r=%d" % (k, s, r))
print("testigo de suryectividad (agente 1) verificado k=0..10 exhaustivo en s: fallos=%d" % fallos)

# ATAQUE al borde: el enunciado con k=0 (Z/1 -> vector vacio) y n grandes
if pv(0, 0, T) != () or pv(10**30 + 1, 4, T) != pv((10**30 + 1) % 16, 4, T):
    fallos += 1
    print("FALLO bordes")
else:
    print("bordes k=0 y n de 31 cifras OK")

if fallos:
    raise SystemExit("A28_comp: %d FALLOS" % fallos)
print()
print("A28_comp: 0 fallos. Los dos agentes coinciden con una tercera implementacion.")
