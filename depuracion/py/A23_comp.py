# A23_comp.py - COMPARADOR. Tercera implementacion, sin mirar la estructura
# de las otras dos: aqui S y T^k se calculan por la via del VECTOR DE PARIDAD
# LEIDO DE LOS BITS (Terras al reves), no iterando T con un if.
#
# Para el atajo: el bit de paridad del paso j es la paridad del iterado.
# Implemento el iterado de otra forma: mantengo el numero como entero y
# aplico la formula n -> (n + (n & 1) * (2*n + 1)) >> 1, que es
#   par:   n >> 1
#   impar: (3n+1)//2 = (n + 2n+1) >> 1
# sin ningun if. Codigo distinto, mismo objeto (eso se comprueba en [0]).

def paso(n):
    return (n + (n & 1) * (2 * n + 1)) >> 1

def ST(n, k):
    s = 0
    for _ in range(k):
        s += n & 1
        n = paso(n)
    return s, n

# [0] que 'paso' es el ATAJO y no otro mapa: 3->5 (clasico daria 10, 3n-1 daria 4)
assert paso(3) == 5 and paso(6) == 3 and paso(5) == 8 and paso(1) == 2

def buena(k, r):
    s1, t1 = ST(r, k)
    s2, t2 = ST(r + 1, k)
    return s1 == s2 and t1 == t2

# [1] conteo propio k = 0..15 y desigualdad
N = []
for k in range(0, 16):
    N.append(sum(1 for r in range(1 << k) if buena(k, r)))
print("N(0..15) =", N)
esperado_repo = [1, 3, 8, 18, 39, 82, 170, 351, 721]  # a(3)..a(11) publicados
assert N[3:12] == esperado_repo, "no cuadra con lo publicado"
for k in range(15):
    assert N[k + 1] >= 2 * N[k], "FALLO desigualdad en k=%d" % k
    assert N[k + 1] * (1 << k) >= N[k] * (1 << (k + 1)), "FALLO f en k=%d" % k
print("N(k+1) >= 2N(k) y f monotona: 0 fallos, k=0..14")

# [2] buenas mod 32
b32 = [r for r in range(32) if buena(5, r)]
print("buenas mod 32:", b32)
assert b32 == [2, 4, 5, 12, 18, 20, 22, 28]

# [3] ATAQUE: es la desigualdad ESTRICTA la que se afirma? No: el enunciado es
# >=. Compruebo si en algun nivel hay exactamente igualdad (nuevas = 0):
iguales = [k for k in range(15) if N[k + 1] == 2 * N[k]]
print("niveles con igualdad exacta N(k+1)=2N(k):", iguales)

# [4] ATAQUE al borde: si en vez de r+1 entero se usara (r+1) mod 2^k
# (el companero del borde seria el resto 0), cambia algun conteo?
def buena_mod(k, r):
    s1, t1 = ST(r, k)
    s2, t2 = ST((r + 1) % (1 << k), k)
    return s1 == s2 and t1 == t2
difs = []
for k in range(1, 14):
    a = sum(1 for r in range(1 << k) if buena(k, r))
    b = sum(1 for r in range(1 << k) if buena_mod(k, r))
    if a != b:
        difs.append((k, a, b))
print("convenio del borde (entero vs mod): diferencias =", difs)

# [5] ATAQUE: el levantamiento afirma ademas que NO hay colision; la inyeccion
# r -> {r, r+2^k} es disjunta por rangos. Compruebo ademas el reciproco NO
# afirmado: hay buenas en k+1 cuyo r mod 2^k NO era buena en k? (las "nuevas")
for k in (5, 8, 10):
    buen_k = set(r for r in range(1 << k) if buena(k, r))
    buen_k1 = set(r for r in range(1 << (k + 1)) if buena(k + 1, r))
    heredadas = set()
    for r in buen_k:
        assert r in buen_k1 and (r + (1 << k)) in buen_k1
        heredadas.add(r); heredadas.add(r + (1 << k))
    nuevas = buen_k1 - heredadas
    print("k=%d: heredadas=%d nuevas=%d (el enunciado solo exige >=, ok)" % (k, len(heredadas), len(nuevas)))

print("COMPARADOR: todo cuadra")
