# A28 - verificacion independiente (agente 2, Python desde cero)
#
# ENUNCIADO: el mapa RESTO -> VECTOR DE PARIDAD es una biyeccion
#            Z/2^k -> {0,1}^k, luego no hay descarte EN BLOQUE de clases
#            para buscar ciclos.
#
# MAPA: el de Terras 1976 es el ATAJO:  T(n) = n/2 si n par, (3n+1)/2 si n impar.
# El vector de paridad de longitud k de n es (par(n), par(T n), ..., par(T^{k-1} n)).
#
# Derivo todo de la definicion; aritmetica entera pura.

def T(n):
    # mapa del atajo
    if n % 2 == 0:
        return n // 2
    return (3 * n + 1) // 2

def T_clasico(n):
    if n % 2 == 0:
        return n // 2
    return 3 * n + 1

def vector_paridad(n, k, mapa):
    v = []
    x = n
    for _ in range(k):
        v.append(x % 2)
        x = mapa(x)
    return tuple(v)

fallos = 0

# ------------------------------------------------------------------
# [1] BIEN DEFINIDO: el vector de paridad de longitud k depende SOLO
#     de n mod 2^k (mapa del atajo).
#     Exhaustivo en r para k = 0..12, con m en {0,1,2,3,7,1000}.
#     Muestreado en r para k = 13..16.
# ------------------------------------------------------------------
import random
random.seed(28)

comp1 = 0
for k in range(0, 13):
    M = 2 ** k
    for r in range(M):
        base = vector_paridad(r, k, T)
        for m in (0, 1, 2, 3, 7, 1000):
            if vector_paridad(r + m * M, k, T) != base:
                fallos += 1
                print("FALLO [1]: k=%d r=%d m=%d" % (k, r, m))
            comp1 += 1
for k in range(13, 17):
    M = 2 ** k
    for _ in range(2000):
        r = random.randrange(M)
        base = vector_paridad(r, k, T)
        for m in (0, 1, 5, 999):
            if vector_paridad(r + m * M, k, T) != base:
                fallos += 1
                print("FALLO [1]: k=%d r=%d m=%d" % (k, r, m))
            comp1 += 1
print("[1] bien definido (atajo): %d comprobaciones, fallos hasta aqui: %d" % (comp1, fallos))

# ------------------------------------------------------------------
# [2] BIYECCION: los 2^k restos dan 2^k vectores DISTINTOS (atajo).
#     Exhaustivo k = 0..16. Como dominio y codominio tienen el mismo
#     cardinal 2^k, inyectivo <=> biyectivo <=> 2^k vectores distintos.
# ------------------------------------------------------------------
for k in range(0, 17):
    M = 2 ** k
    vistos = set()
    for r in range(M):
        vistos.add(vector_paridad(r, k, T))
    if len(vistos) != M:
        fallos += 1
        print("FALLO [2]: k=%d -> %d vectores distintos de %d" % (k, len(vistos), M))
    else:
        if k in (0, 1, 2, 8, 12, 16):
            print("[2] k=%2d: %d restos -> %d vectores distintos (biyeccion)" % (k, M, len(vistos)))
print("[2] biyeccion exhaustiva k=0..16: fallos hasta aqui: %d" % fallos)

# ------------------------------------------------------------------
# [3] CONTROL A/B: con el mapa CLASICO (3n+1) NO hay biyeccion.
#     Los vectores alcanzables son F(k+2) (sin dos impares seguidos...
#     lo mido, no lo supongo). k = 1..12, exhaustivo en restos mod 2^k.
# ------------------------------------------------------------------
def fib(j):
    a, b = 0, 1
    for _ in range(j):
        a, b = b, a + b
    return a

for k in (4, 6, 8, 10, 12):
    M = 2 ** k
    vistos = set()
    for r in range(M):
        vistos.add(vector_paridad(r, k, T_clasico))
    esperado = fib(k + 2)
    marca = "OK" if len(vistos) == esperado else "FALLO"
    if len(vistos) == M:
        fallos += 1
        print("FALLO [3]: clasico dio biyeccion en k=%d (no debia)" % k)
    if len(vistos) != esperado:
        fallos += 1
    print("[3] clasico k=%2d: %d vectores de %d restos (F(k+2)=%d) %s" % (k, len(vistos), M, esperado, marca))

# ------------------------------------------------------------------
# [4] LA VERSION FALSA, refutada con numeros (contexto de la ficha):
#     'T^k es una biyeccion sobre Z/2^k' es falso al pie de la letra.
#     (a) T no desciende a Z/2: 0 y 2 son la misma clase mod 2 y
#         T(0) != T(2) mod 1... lo que falla es T(0)=0, T(2)=1 distintos.
#     (b) T no es inyectiva sobre Z: T(1) = T(4).
# ------------------------------------------------------------------
if not (T(0) == 0 and T(2) == 1):
    fallos += 1
    print("FALLO [4a]")
else:
    print("[4a] T(0)=0 y T(2)=1: 0 y 2 son la misma clase mod 2 con imagenes distintas -> T no desciende a Z/2^k")
if not (T(1) == 2 and T(4) == 2):
    fallos += 1
    print("FALLO [4b]")
else:
    print("[4b] T(1)=T(4)=2 -> T no es inyectiva sobre Z")

# ------------------------------------------------------------------
# [5] EL COROLARIO ESTRATEGICO: 'no hay descarte en bloque'.
#     Formalizacion comprobable: ningun par de clases distintas mod 2^k
#     comparte vector de paridad (eso es [2]); luego un criterio de
#     candidato a ciclo formulado sobre el vector de paridad decide
#     UNA clase por vector, nunca un bloque. Ademas compruebo que la
#     ecuacion de ciclo por resto da a lo sumo UN candidato por clase:
#     T^k(2^k*m + r) = 3^{S(r)}*m + T^k(r)  (Terras 1.2, la derivo yo),
#     y T^k(n) = n  =>  m = (r - T^k(r)) / (3^{S(r)} - 2^k): unico si existe.
#     Verifico la formula lineal exacta en k = 1..10, exhaustivo en r,
#     m en {0,1,2,3,50}.
# ------------------------------------------------------------------
def iterT(n, k):
    S = 0
    x = n
    for _ in range(k):
        if x % 2 == 1:
            S += 1
        x = T(x)
    return x, S

comp5 = 0
for k in range(1, 11):
    M = 2 ** k
    for r in range(M):
        tr, S = iterT(r, k)
        for m in (0, 1, 2, 3, 50):
            lhs, S2 = iterT(M * m + r, k)
            if lhs != (3 ** S) * m + tr or S2 != S:
                fallos += 1
                print("FALLO [5]: k=%d r=%d m=%d" % (k, r, m))
            comp5 += 1
print("[5] formula lineal T^k(2^k m + r) = 3^S(r) m + T^k(r): %d comprobaciones, fallos: %d" % (comp5, fallos))

# ------------------------------------------------------------------
# VEREDICTO
# ------------------------------------------------------------------
if fallos:
    raise SystemExit("A28: %d FALLOS - el enunciado NO se sostiene tal cual" % fallos)
print()
print("A28: 0 fallos. El mapa resto -> vector de paridad (mapa del ATAJO) es")
print("biyeccion Z/2^k -> {0,1}^k, exhaustivo k = 0..16; bien definido; el")
print("clasico NO es biyectivo (F(k+2) vectores); y cada clase da a lo sumo")
print("un candidato a ciclo -> sin descarte en bloque.")
