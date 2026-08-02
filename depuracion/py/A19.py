# A19 - verificacion independiente, escrita desde cero.
#
# ENUNCIADO: "biyeccion perfecta entre los 2^k restos y los 2^k patrones
# de paridad posibles" -- SOLO para el mapa del ATAJO ((3n+1)/2 en impares).
# Mitad 2 del enunciado: con la regla CLASICA (3n+1) NO hay biyeccion;
# los patrones alcanzables son F(k+2) (Fibonacci), porque tras 3n+1 el
# resultado es par y no hay dos impares seguidos.
#
# Derivo todo de la definicion de los mapas. Aritmetica entera pura.
#
# Mapas:
#   atajo   T(n) = n//2 si n par,  (3n+1)//2 si n impar
#   clasico C(n) = n//2 si n par,  3n+1      si n impar
#
# Patron de paridad de longitud k de n: la paridad de n, T(n), ..., T^{k-1}(n)
# (la paridad ANTES de aplicar cada paso), como cadena de 'P'/'I'.

import sys

def T(n):
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2

def C(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1

def patron(f, n, k):
    p = []
    for _ in range(k):
        p.append('P' if n % 2 == 0 else 'I')
        n = f(n)
    return ''.join(p)

fallos = 0

# ------------------------------------------------------------------
# PARTE 0 - buena definicion: el patron de k pasos depende SOLO de
# n mod 2^k, para LOS DOS mapas. (Sin esto "resto -> patron" ni es
# una funcion.) Representantes m = 0,1,2,3,1000 incluye el borde m=0
# (n = r, incluso n = 0) y n chicos (n=0,1,2).
# ------------------------------------------------------------------
K_MAX_ATAJO = 12
K_MAX_CLASICO = 13
REPRES = [0, 1, 2, 3, 1000]

for nombre, f, kmax in (("atajo", T, K_MAX_ATAJO), ("clasico", C, K_MAX_CLASICO)):
    for k in range(0, kmax + 1):
        M = 2 ** k
        for r in range(M):
            pats = set(patron(f, r + m * M, k) for m in REPRES)
            if len(pats) != 1:
                print("FALLO buena definicion:", nombre, "k =", k, "r =", r, pats)
                fallos += 1
print("[0] buena definicion (patron depende solo de n mod 2^k):")
print("    atajo   k = 0..%d, clasico k = 0..%d, repres m = %s -> %d fallos"
      % (K_MAX_ATAJO, K_MAX_CLASICO, REPRES, fallos))
if fallos:
    raise SystemExit("ABORTO: el patron no depende solo del resto")

# ------------------------------------------------------------------
# PARTE 1 - ATAJO: biyeccion resto <-> patron.
# 2^k restos deben dar 2^k patrones DISTINTOS (inyectiva) y como el
# codominio {P,I}^k tiene exactamente 2^k elementos, distinto = biyeccion.
# Borde k = 0 incluido (1 resto, 1 patron vacio).
# ------------------------------------------------------------------
print()
print("[1] ATAJO - biyeccion resto <-> patron de paridad:")
for k in range(0, K_MAX_ATAJO + 1):
    M = 2 ** k
    pats = [patron(T, r, k) for r in range(M)]
    distintos = len(set(pats))
    ok = (distintos == M)
    print("    k = %2d : %5d restos -> %5d patrones distintos de %5d posibles  %s"
          % (k, M, distintos, 2 ** k, "BIYECCION" if ok else "** NO **"))
    if not ok:
        fallos += 1
if fallos:
    raise SystemExit("ABORTO: la biyeccion del atajo fallo")

# extremos anotados en la base: resto 0 -> todo P, resto 2^k-1 -> todo I
for k in range(1, K_MAX_ATAJO + 1):
    M = 2 ** k
    if patron(T, 0, k) != 'P' * k:
        print("FALLO: resto 0 no es P^k en k =", k); fallos += 1
    if patron(T, M - 1, k) != 'I' * k:
        print("FALLO: resto 2^k-1 no es I^k en k =", k); fallos += 1
print("    extremos: resto 0 = P^k y resto 2^k-1 = I^k, k = 1..%d -> %d fallos"
      % (K_MAX_ATAJO, fallos))
if fallos:
    raise SystemExit("ABORTO: extremos")

# ------------------------------------------------------------------
# PARTE 2 - CLASICO: NO biyeccion; los patrones alcanzables son F(k+2).
# Razon estructural: tras un paso impar (3n+1) el resultado es PAR,
# luego 'II' es imposible. Compruebo (a) el conteo contra Fibonacci,
# (b) que ningun patron alcanzado contiene 'II', y (c) que los
# alcanzados son EXACTAMENTE todas las cadenas sin 'II' (igualdad de
# conjuntos, no solo de cardinales).
# ------------------------------------------------------------------
def fib(n):  # F(1) = F(2) = 1
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

print()
print("[2] CLASICO - patrones alcanzables = F(k+2), sin dos impares seguidos:")
for k in range(0, K_MAX_CLASICO + 1):
    M = 2 ** k
    alcanzados = set(patron(C, r, k) for r in range(M))
    esperado = fib(k + 2)
    con_II = sum(1 for p in alcanzados if 'II' in p)
    # todas las cadenas de longitud k sin 'II'
    sin_II = set()
    def gen(pref):
        if len(pref) == k:
            sin_II.add(pref); return
        gen(pref + 'P')
        if not pref.endswith('I'):
            gen(pref + 'I')
    if k <= K_MAX_CLASICO:
        gen('')
    iguales = (alcanzados == sin_II)
    ok = (len(alcanzados) == esperado) and con_II == 0 and iguales
    print("    k = %2d : %5d alcanzados, F(k+2) = %5d, con 'II': %d, "
          "= {cadenas sin II}: %s  %s"
          % (k, len(alcanzados), esperado, con_II, iguales,
             "OK" if ok else "** FALLO **"))
    if not ok:
        fallos += 1
if fallos:
    raise SystemExit("ABORTO: la mitad clasica fallo")

# demostracion aritmetica del 'no II': si n es impar, 3n+1 es par. Exacta:
for n in range(1, 200001, 2):
    if (3 * n + 1) % 2 != 0:
        print("FALLO: 3n+1 impar para n =", n); fallos += 1
print("    3n+1 par para todo n impar, n = 1..200000 impares -> %d fallos" % fallos)

# ------------------------------------------------------------------
# PARTE 3 - contraejemplo explicito de que el enunciado NO vale para
# el clasico (por si alguien quita el ambito): en k = 2 ya faltan
# patrones y sobran colisiones.
# ------------------------------------------------------------------
print()
print("[3] contraste en k = 2:")
print("    atajo  :", {r: patron(T, r, 2) for r in range(4)})
print("    clasico:", {r: patron(C, r, 2) for r in range(4)})
print("    clasico k=2: 'II' no aparece; alcanzados =",
      sorted(set(patron(C, r, 2) for r in range(4))), "= 3 = F(4)")

if fallos:
    raise SystemExit("ABORTO: hubo fallos")
print()
print("VEREDICTO: 0 fallos en todo. Biyeccion del atajo confirmada k = 0..%d;"
      % K_MAX_ATAJO)
print("Fibonacci F(k+2) del clasico confirmado k = 0..%d, con igualdad de"
      % K_MAX_CLASICO)
print("conjuntos contra las cadenas sin 'II'.")
