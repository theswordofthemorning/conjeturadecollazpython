# A23.py - AGENTE 2 (PYTHON INDEPENDIENTE), escrito desde cero.
#
# ENUNCIADO A VERIFICAR (literal de la base):
#   "N(k+1) >= 2*N(k) siempre, luego la fraccion f(k) es monotona"
#   con N(k) = numero de clases r mod 2^k que "se funden": el par (r, r+1)
#   cumple  S_k(r) == S_k(r+1)  y  T^k(r) == T^k(r+1).
#
# MAPA: el del ATAJO.  T(n) = n/2 si n par,  (3n+1)/2 si n impar.
#   (El enunciado usa el atajo; yo uso el atajo. Lo declaro para no mezclar
#    con el clasico ni con 3n-1.)
#
# DEMOSTRACION DECLARADA QUE HAY QUE VERIFICAR (no solo el conteo):
#   (a) el vector de paridad de los primeros k pasos depende solo de n mod 2^k
#   (b) formula afin:  T^k(2^k*m + r) = 3^{S_k(r)}*m + T^k(r)
#   (c) si r es buena mod 2^k, entonces r y r+2^k son las dos buenas mod 2^(k+1)
#       (con eso N(k+1) >= 2*N(k), y de ahi f(k+1) >= f(k) en aritmetica exacta)
#   (d) borde r = 2^k - 1: alli el "par" (r, r+1) cruza de bloque; comprobar
#       que ese borde nunca es bueno (y por que), para que el levantamiento
#       no tenga excepciones escondidas.
#
# Todo con int exacto. Ningun float decide nada.

import sys

def T(n):
    # mapa del atajo sobre enteros no negativos
    if n % 2 == 0:
        return n // 2
    return (3 * n + 1) // 2

def iterar(n, k):
    # devuelve (T^k(n), S_k(n), vector de paridad de los k pasos)
    s = 0
    vec = []
    for _ in range(k):
        p = n & 1
        vec.append(p)
        s += p
        n = T(n)
    return n, s, tuple(vec)

def es_buena(k, r):
    # el par (r, r+1) como ENTEROS (esto incluye el caso m=0 del par:
    # la condicion es aritmetica pura sobre S y T, no presupone llegar a 1)
    t1, s1, _ = iterar(r, k)
    t2, s2, _ = iterar(r + 1, k)
    return (s1 == s2) and (t1 == t2)

fallos_totales = 0

# ----------------------------------------------------------------------
# [1] El vector de paridad depende solo de n mod 2^k (Terras, rederivado
#     aqui por comprobacion): exhaustivo en r para k = 1..12, con
#     m en {0, 1, 2, 5, 13} (incluye el borde m = 0).
# ----------------------------------------------------------------------
print("[1] vector de paridad = funcion de n mod 2^k")
fallos = 0
casos = 0
for k in range(1, 13):
    M = 1 << k
    for r in range(M):
        _, _, vec_r = iterar(r, k)
        for m in (0, 1, 2, 5, 13):
            _, _, vec_n = iterar(M * m + r, k)
            casos += 1
            if vec_n != vec_r:
                fallos += 1
                print("    FALLO: k=%d r=%d m=%d" % (k, r, m))
print("    k = 1..12 exhaustivo en r, m en {0,1,2,5,13}: %d casos, %d fallos" % (casos, fallos))
fallos_totales += fallos

# ----------------------------------------------------------------------
# [2] Formula afin: T^k(2^k*m + r) = 3^{S_k(r)}*m + T^k(r)
#     (misma malla; incluye m = 0, que la cumple trivialmente, y m >= 1)
# ----------------------------------------------------------------------
print("[2] formula afin T^k(2^k*m + r) = 3^S(r)*m + T^k(r)")
fallos = 0
casos = 0
for k in range(1, 13):
    M = 1 << k
    for r in range(M):
        t_r, s_r, _ = iterar(r, k)
        for m in (0, 1, 2, 5, 13):
            t_n, s_n, _ = iterar(M * m + r, k)
            casos += 1
            if t_n != (3 ** s_r) * m + t_r or s_n != s_r:
                fallos += 1
                print("    FALLO: k=%d r=%d m=%d" % (k, r, m))
print("    mismos rangos: %d casos, %d fallos" % (casos, fallos))
fallos_totales += fallos

# ----------------------------------------------------------------------
# [3] El borde r = 2^k - 1 nunca es bueno, y la razon es exacta:
#     S_k(2^k - 1) = k (todo impares) y S_k(2^k) = 0 (todo pares),
#     asi que S nunca coincide para k >= 1.
# ----------------------------------------------------------------------
print("[3] borde r = 2^k - 1")
fallos = 0
for k in range(1, 18):
    r = (1 << k) - 1
    t1, s1, _ = iterar(r, k)
    t2, s2, _ = iterar(r + 1, k)
    if s1 != k or s2 != 0:
        fallos += 1
        print("    FALLO estructural: k=%d S(2^k-1)=%d S(2^k)=%d" % (k, s1, s2))
    if es_buena(k, r):
        fallos += 1
        print("    FALLO: el borde r=2^k-1 salio bueno en k=%d" % k)
print("    k = 1..17: el borde nunca es bueno (S=%s contra S=0), %d fallos" % ("k", fallos))
fallos_totales += fallos

# ----------------------------------------------------------------------
# [4] Exhaustivo: buenas por nivel, k = 0..17.
#     - k = 0 es un borde: mod 1 hay un solo resto (r=0), par (0,1),
#       T^0(0)=0 != 1=T^0(1)  ->  N(0) = 0. Lo compruebo, no lo supongo.
# ----------------------------------------------------------------------
print("[4] conteo exhaustivo de clases buenas, k = 0..17")
K_TOPE = 17
buenas_por_k = {}
for k in range(0, K_TOPE + 1):
    M = 1 << k
    buenas = set()
    for r in range(M):
        if es_buena(k, r):
            buenas.add(r)
    buenas_por_k[k] = buenas

if len(buenas_por_k[0]) != 0:
    print("    AVISO: N(0) != 0, revisar definicion en el borde k=0")
    fallos_totales += 1

fila = []
for k in range(0, K_TOPE + 1):
    fila.append("N(%d)=%d" % (k, len(buenas_por_k[k])))
print("    " + "  ".join(fila[:9]))
print("    " + "  ".join(fila[9:]))

# ----------------------------------------------------------------------
# [5] LA DEMOSTRACION, paso a paso, sin fiarse del conteo:
#     para CADA r buena a nivel k, comprobar que
#        (i)  r        es buena a nivel k+1
#        (ii) r + 2^k  es buena a nivel k+1
#     y que las 2*N(k) levantadas son restos distintos mod 2^(k+1)
#     (trivial: r < 2^k <= r + 2^k < 2^(k+1), pero se comprueba).
# ----------------------------------------------------------------------
print("[5] verificacion del levantamiento r -> {r, r+2^k}")
fallos = 0
casos = 0
for k in range(1, K_TOPE):
    M = 1 << k
    levantadas = set()
    for r in sorted(buenas_por_k[k]):
        casos += 2
        if r not in buenas_por_k[k + 1]:
            fallos += 1
            print("    FALLO (i): k=%d r=%d buena en k pero no en k+1" % (k, r))
        if (r + M) not in buenas_por_k[k + 1]:
            fallos += 1
            print("    FALLO (ii): k=%d r=%d -> r+2^k=%d no buena en k+1" % (k, r, r + M))
        levantadas.add(r)
        levantadas.add(r + M)
    if len(levantadas) != 2 * len(buenas_por_k[k]):
        fallos += 1
        print("    FALLO: colision de levantadas en k=%d" % k)
print("    k = 1..%d: %d comprobaciones de levantamiento, %d fallos" % (K_TOPE - 1, casos, fallos))
fallos_totales += fallos

# ----------------------------------------------------------------------
# [6] La desigualdad y la monotonia de f, en aritmetica exacta:
#     N(k+1) >= 2*N(k)   y   f(k+1) >= f(k)  <=>  2*N(k+1) >= ... espera:
#     f(k) = N(k)/2^k;  f(k+1) >= f(k)  <=>  N(k+1)*2^k >= N(k)*2^(k+1)
#     <=>  N(k+1) >= 2*N(k).  Se comprueba con enteros, sin Fraction siquiera.
# ----------------------------------------------------------------------
print("[6] N(k+1) >= 2*N(k) y monotonia de f(k) = N(k)/2^k")
fallos = 0
for k in range(0, K_TOPE):
    n_k = len(buenas_por_k[k])
    n_k1 = len(buenas_por_k[k + 1])
    if n_k1 < 2 * n_k:
        fallos += 1
        print("    FALLO: N(%d)=%d < 2*N(%d)=%d" % (k + 1, n_k1, k, 2 * n_k))
    # monotonia de f con productos cruzados enteros
    if n_k1 * (1 << k) < n_k * (1 << (k + 1)):
        fallos += 1
        print("    FALLO monotonia f en k=%d" % k)
print("    k = 0..%d: %d fallos. Nuevas por nivel:" % (K_TOPE - 1, fallos))
nuevas = []
for k in range(2, K_TOPE):
    nuevas.append("k%d->%d: +%d" % (k, k + 1, len(buenas_por_k[k + 1]) - 2 * len(buenas_por_k[k])))
print("    " + "  ".join(nuevas))
fallos_totales += fallos

# ----------------------------------------------------------------------
# [7] Bordes sueltos que pide el encargo:
#     - n=1, n=2 como restos chicos: aparecen en el exhaustivo, pero los
#       imprimo para verlos.
#     - el paso (k -> k+1) de la demostracion en detalle sobre un caso:
#       si T^k(r) == T^k(r+1) = x, el paso k+1 aplica T al MISMO x en los
#       dos, luego la igualdad se conserva. Compruebo la mecanica en el
#       primer r bueno de cada nivel.
# ----------------------------------------------------------------------
print("[7] bordes y mecanica del paso k -> k+1")
for k in (3, 4, 5):
    for r in sorted(buenas_por_k[k])[:1]:
        t1, s1, _ = iterar(r, k)
        t2, s2, _ = iterar(r + 1, k)
        u1, z1, _ = iterar(r, k + 1)
        u2, z2, _ = iterar(r + 1, k + 1)
        ok = (t1 == t2) and (u1 == T(t1)) and (u2 == T(t2)) and (u1 == u2)
        print("    k=%d r=%d: T^k=%d=%d, T^(k+1)=%d=%d, paso extra sobre el mismo numero: %s"
              % (k, r, t1, t2, u1, u2, "ok" if ok else "FALLO"))
        if not ok:
            fallos_totales += 1
print("    r=1 buena en k=3..6? " + str([1 in buenas_por_k[k] for k in (3, 4, 5, 6)]))
print("    r=2 buena en k=3..6? " + str([2 in buenas_por_k[k] for k in (3, 4, 5, 6)]))

# ----------------------------------------------------------------------
# veredicto
# ----------------------------------------------------------------------
if fallos_totales > 0:
    raise SystemExit("VEREDICTO: %d fallos. El enunciado NO se sostiene tal cual." % fallos_totales)
print()
print("VEREDICTO: 0 fallos en todo. N(k+1) >= 2*N(k) verificado exhaustivo")
print("k = 0..%d, y la DEMOSTRACION del levantamiento verificada caso a caso" % K_TOPE)
print("(cada r buena se levanta a dos buenas, sin excepciones, borde incluido).")
