# -----------------------------------------------------------------------------
# A18 (agente 2, independiente): "los primeros k pasos de cualquier numero
# los decide n mod 2^k"
#
# Interpretacion verificada: el PATRON de los primeros k pasos (que regla se
# aplico en cada paso: par -> dividir, impar -> multiplicar) es funcion
# unicamente de n mod 2^k. Es decir, dos numeros congruentes mod 2^k aplican
# exactamente la misma secuencia de reglas durante sus primeros k pasos.
#
# Hay que decidir el MAPA. Se prueban los dos:
#   clasico : n/2 si par, 3n+1 si impar        (1 paso impar NO divide)
#   atajo   : n/2 si par, (3n+1)/2 si impar    (todo paso divide)
#
# Argumento derivado desde cero (bit a bit):
#   conocer n mod 2^j = conocer los j bits bajos. La paridad es el bit 0.
#   - paso par     n -> n/2       : de j bits conocidos quedan j-1.
#   - paso impar clasico  n -> 3n+1 : 3n+1 mod 2^j lo fija n mod 2^j -> quedan j.
#   - paso impar atajo n -> (3n+1)/2 : quedan j-1.
#   En el atajo cada paso consume exactamente un bit -> k bits deciden k pasos
#   exactos (y no mas). En el clasico solo consumen bit los pasos pares -> k
#   bits deciden AL MENOS k pasos (a veces mas).
# Todo lo de abajo verifica ese argumento con enteros exactos, sin un float.
# -----------------------------------------------------------------------------

def paso_clasico(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1

def paso_atajo(n):
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2

def vector(n, k, paso):
    # paridades de los primeros k pasos (0 = par/divide, 1 = impar/multiplica)
    v = []
    for _ in range(k):
        v.append(n % 2)
        n = paso(n)
    return tuple(v)

MAPAS = (("clasico", paso_clasico), ("atajo", paso_atajo))

# --- COMPROBACION 1: exhaustiva en r, muestreada en m, para los dos mapas ----
# k = 1..13 (2^13 = 8192 restos, exhaustivo). Representantes n = m*2^k + r,
# incluyendo m = 0 (el borde: n = r, el numero chico), m = 1, y m grandes.
K_MAX = 13
REPS_M = [0, 1, 2, 3, 7, 100, 12345, 2**30 + 1]

comparaciones = 0
fallos = 0
for nombre, paso in MAPAS:
    for k in range(1, K_MAX + 1):
        M = 2 ** k
        for r in range(M):
            base = None
            for m in REPS_M:
                n = m * M + r
                if n < 1:
                    continue  # n = 0 no es un numero de Collatz
                v = vector(n, k, paso)
                if base is None:
                    base = v
                else:
                    comparaciones += 1
                    if v != base:
                        fallos += 1
                        print("FALLO", nombre, "k=", k, "r=", r, "m=", m)
if fallos:
    raise SystemExit("COMPROBACION 1 ROTA: %d fallos" % fallos)
print("COMPROBACION 1 (enunciado, ambos mapas): k=1..%d exhaustivo en r," % K_MAX)
print("  %d representantes por clase (incluye m=0) -> %d comparaciones, 0 fallos"
      % (len(REPS_M), comparaciones))

# --- COMPROBACION 2: la replica del dato de la base: 64 restos x 12 reps -----
# La base dice "64 restos x 12 representantes = 768 numeros, 0 discrepancias".
# 64 = 2^6, o sea k = 6. Se replica con m = 1..12 (768 numeros) en ambos mapas.
for nombre, paso in MAPAS:
    total = 0
    disc = 0
    k = 6
    M = 64
    for r in range(M):
        vs = set()
        for m in range(1, 13):
            vs.add(vector(m * M + r, k, paso))
            total += 1
        if len(vs) != 1:
            disc += 1
    if disc:
        raise SystemExit("COMPROBACION 2 ROTA (%s): %d clases discrepan" % (nombre, disc))
    print("COMPROBACION 2 (%s): 64 restos x 12 reps = %d numeros, 0 discrepancias" % (nombre, total))

# --- COMPROBACION 3: bordes concretos ---------------------------------------
# n=1, n=2, n par, n impar, m=0. k=0 es vacuo (0 pasos no dicen nada) y se
# declara, no se ejecuta.
for nombre, paso in MAPAS:
    for k in (1, 2, 5, 10):
        M = 2 ** k
        for n_chico, n_grande in ((1, 1 + 3 * M), (2, 2 + 5 * M), (M - 1, 2 * M - 1 + M), (M, 3 * M)):
            va = vector(n_chico, k, paso)
            vb = vector(n_grande, k, paso)
            if va != vb:
                raise SystemExit("BORDE ROTO %s k=%d n=%d vs n=%d" % (nombre, k, n_chico, n_grande))
print("COMPROBACION 3 (bordes n=1, n=2, n=2^k-1, n=2^k, m=0): 0 fallos")

# --- COMPROBACION 4: el modulo es AJUSTADO -----------------------------------
# (a) n mod 2^(k-1) NO basta para k pasos: se busca contraejemplo.
# (b) n mod 2^k NO decide el paso k+1 en el atajo (deberia fallar en TODAS las
#     clases); en el clasico decide k+1 en algunas clases y en otras no.
for nombre, paso in MAPAS:
    k = 10
    Mm = 2 ** (k - 1)
    contra = 0
    for r in range(Mm):
        vs = set()
        for m in range(0, 8):
            n = m * Mm + r
            if n < 1:
                continue
            vs.add(vector(n, k, paso))
        if len(vs) > 1:
            contra += 1
    print("COMPROBACION 4a (%s): con mod 2^%d fallan %d de %d clases para k=%d pasos"
          % (nombre, k - 1, contra, Mm, k))
    if contra == 0:
        raise SystemExit("4a: mod 2^(k-1) parece bastar y no deberia (%s)" % nombre)

for nombre, paso in MAPAS:
    k = 10
    M = 2 ** k
    difieren = 0
    for r in range(M):
        n1 = M + r      # bit k = 1 (mod 2^(k+1): r + 2^k)
        n2 = 2 * M + r  # bit k = 0 (mod 2^(k+1): r)
        if vector(n1, k + 1, paso) != vector(n2, k + 1, paso):
            difieren += 1
    print("COMPROBACION 4b (%s): el paso k+1 difiere en %d de %d clases (k=%d)"
          % (nombre, difieren, M, k))

# --- COMPROBACION 5: en el atajo, resto -> vector es BIYECCION ---------------
# (consecuencia que hace exacto el "k bits = k pasos": 2^k restos, 2^k vectores,
# todos distintos). En el clasico NO es sobreyectiva (dos impares seguidos son
# imposibles: tras 3n+1 el resultado es par).
for k in range(1, 13):
    M = 2 ** k
    vs = set(vector(r if r >= 1 else M, k, paso_atajo) for r in range(M))
    if len(vs) != M:
        raise SystemExit("5: atajo k=%d da %d vectores distintos, no %d" % (k, len(vs), M))
k = 10
M = 2 ** k
vs_cl = set(vector(r if r >= 1 else M, k, paso_clasico) for r in range(M))
print("COMPROBACION 5: atajo biyectivo k=1..12 (2^k vectores distintos, 0 fallos);")
print("  clasico k=10: %d vectores distintos de %d clases (inyectivo NO, bien definido SI... "
      % (len(vs_cl), M))
# ojo: en el clasico dos clases distintas pueden compartir vector; eso no toca
# el enunciado (que solo pide que cada clase tenga UN vector).

print()
print("VEREDICTO: el enunciado SE SOSTIENE para los DOS mapas (clasico y atajo),")
print("leido como: el patron par/impar de los primeros k pasos es funcion de n mod 2^k.")
print("El modulo es ajustado: mod 2^(k-1) no basta, y en el atajo el paso k+1")
print("ya no queda decidido en ninguna clase.")
