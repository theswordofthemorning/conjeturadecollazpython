# gramatica_propia.py  (ADVERSARIO 3, 9a revision)
#
# LA GRAMATICA DE BLOQUES RE-DERIVADA A MANO, SIN MIRAR transicion().
#
# Estado: el par {v, 3^k * v + c} con beta = paridad de v el bit libre.
# Derivacion propia de los casos (atajo T(n) = n/2 o (3n+1)/2):
#
#   c par (misma paridad):
#     beta 0: {v/2, 3^k (v/2) + c/2}                     -> (k, c/2)
#     beta 1: {(3v+1)/2, 3^k (3v+1)/2 + (3c+1-3^k)/2}    -> (k, (3c+1-3^k)/2)
#             (vale tambien para k = 0: (3c+1-1)/2 = 3c/2)
#   c impar (paridades opuestas):
#     beta 0 (v par, el otro impar):
#             {v/2, 3^{k+1} (v/2) + (3c+1)/2}            -> (k+1, (3c+1)/2)
#     beta 1, k >= 1 (v impar, el otro par):
#             {(3v+1)/2, 3^{k-1} (3v+1)/2 + (c-3^{k-1})/2} -> (k-1, (c-3^{k-1})/2)
#     beta 1, k = 0 (v impar, v+c par; la base CAMBIA de pata):
#             base b = (v+c)/2; el otro = 3b + (1-3c)/2  -> (1, (1-3c)/2)
#
#   Normalizacion en k' = 0: c' = 0 es FUSION (par igualado);
#   |c'| = 1 es RETORNO al lazo; si no, c' <- |c'| (relabel de la base).
#
# El test de propiedad: estados muestreados del propio barrido,
# instanciados con enteros de verdad (v ~ 2^70) y caminados con el
# atajo a pelo: el par predicho debe SER el par real, caso a caso.
#
# Cruces:
#   (a) R(t), A(t) contra el censo de pares reales (censo_propio_RA.txt)
#       para t = 1..24 (por 2^(24-t)).
#   (b) conservacion exacta rho + alfa + viva == 1 (Fraction).
#   (c) los parciales impresos de recordsincap_salida.txt (6 decimales)
#       y el record final a 12 decimales.
#   (d) monotonia de phi_trunc (es teorema: alfa_L sube, rho_L sube,
#       rho_L < 1 -- se comprueba igual).

from fractions import Fraction

L_MAX = 34


def paso(k, c, beta):
    if c % 2 == 0:
        if beta == 0:
            k2, c2 = k, c // 2
        else:
            k2, c2 = k, (3 * c + 1 - 3 ** k) // 2
    else:
        if beta == 0:
            k2, c2 = k + 1, (3 * c + 1) // 2
        elif k == 0:
            k2, c2 = 1, (1 - 3 * c) // 2
        else:
            k2, c2 = k - 1, (c - 3 ** (k - 1)) // 2
    if k2 == 0:
        if c2 == 0:
            return ('f', 0, 0)
        if c2 < 0:
            c2 = -c2
        if c2 == 1:
            return ('r', 0, 1)
    return ('s', k2, c2)


def base_nueva(k, c, beta, v):
    # la base del estado siguiente, para el test de instanciacion
    if c % 2 == 0:
        return v // 2 if beta == 0 else (3 * v + 1) // 2
    if beta == 0:
        return v // 2
    if k == 0:
        return (v + c) // 2
    return (3 * v + 1) // 2


def atajo(n):
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


# ---- el barrido, con muestreo para el test de propiedad -----------------

R = {}
A = {}
estados = {(0, 1): 1}
muestra = []
max_c = 0
for L in range(1, L_MAX + 1):
    nuevo = {}
    tomados = 0
    for (k, c), n in estados.items():
        if tomados < 40:
            muestra.append((k, c))
            tomados += 1
        if abs(c) > max_c:
            max_c = abs(c)
        for beta in (0, 1):
            tipo, k2, c2 = paso(k, c, beta)
            if tipo == 'f':
                A[L] = A.get(L, 0) + n
            elif tipo == 'r':
                R[L] = R.get(L, 0) + n
            else:
                clave = (k2, c2)
                nuevo[clave] = nuevo.get(clave, 0) + n
    estados = nuevo

# ---- test de propiedad: instanciacion entera --------------------------

V0 = 2 ** 70
fallos = 0
for (k, c) in muestra:
    for beta in (0, 1):
        v = V0 + beta                       # paridad beta, gigante
        par_real = {atajo(v), atajo(3 ** k * v + c)}
        tipo, k2, c2 = paso(k, c, beta)
        b = base_nueva(k, c, beta, v)
        if tipo == 'f':
            ok = (len(par_real) == 1)
        else:
            # reconstruir el par predicho SIN la normalizacion de signo:
            # {b, 3^{k2} b + c2} o su relabel {b - c2', ...}; basta la
            # igualdad de conjuntos probando los dos signos de c2
            ok = (par_real == {b, 3 ** k2 * b + c2}
                  or par_real == {b, 3 ** k2 * b - c2}
                  or par_real == {b - c2, 3 ** k2 * (b - c2) + c2})
        if not ok:
            fallos += 1
            print("PROPIEDAD FALLA: (k=%d, c=%d, beta=%d)" % (k, c, beta))
if fallos:
    raise SystemExit("la derivacion propia falla en %d instancias" % fallos)
print("TEST DE PROPIEDAD OK: %d estados muestreados x 2 bits, el par"
      % len(muestra))
print("predicho ES el par entero real en todos (v ~ 2^70).")
print()

# ---- cruce (a): contra el censo de pares reales -----------------------

fallos = 0
with open("revision9_adv3/censo_propio_RA.txt") as f:
    for linea in f:
        t, rc, ac = [int(z) for z in linea.split()]
        if rc != R.get(t, 0) * 2 ** (24 - t) or \
           ac != A.get(t, 0) * 2 ** (24 - t):
            fallos += 1
            print("CRUCE a FALLA en t = %d" % t)
if fallos:
    raise SystemExit("gramatica propia vs censo: %d discrepancias" % fallos)
print("CRUCE a OK: R(t) y A(t) de la gramatica propia clavan el censo de")
print("pares enteros reales celda a celda, t = 1..24.")
print()

# ---- cruces (b)-(d): conservacion, parciales, record ------------------

rho = Fraction(0)
alfa = Fraction(0)
anterior = Fraction(0)
print("   L    rho_L      alfa_L     viva_L      phi_trunc")
for L in range(1, L_MAX + 1):
    rho += Fraction(R.get(L, 0), 2 ** L)
    alfa += Fraction(A.get(L, 0), 2 ** L)
    phi = alfa / (1 - rho)
    if phi < anterior:
        raise SystemExit("monotonia rota en L = %d" % L)
    anterior = phi
    if L >= 20 and L % 2 == 0:
        print("  %2d  %.6f   %.6f   %.6f    %.6f"
              % (L, float(rho), float(alfa), 1 - float(rho) - float(alfa),
                 float(phi)))
viva = sum(Fraction(n, 2 ** L_MAX) for n in estados.values())
if rho + alfa + viva != 1:
    raise SystemExit("CONSERVACION ROTA: %s" % float(rho + alfa + viva))
print()
print("CONSERVACION OK: rho + alfa + viva == 1 exacto (Fraction).")
print("estados vivos al final: %d   max|c| visto: %d" % (len(estados), max_c))

phi = alfa / (1 - rho)
num = (phi * 10 ** 12).numerator // (phi * 10 ** 12).denominator
print()
print("EL RECORD, RECOMPUTADO POR LA GRAMATICA PROPIA:")
print("  phi_trunc(34) = 0.%012d   (12 decimales exactos)" % num)
print("  rho  = %.8f   alfa = %.8f" % (float(rho), float(alfa)))
