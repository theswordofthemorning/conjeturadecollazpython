# A20.py - AGENTE 2 (independiente). Escrito desde cero, sin abrir ficheros del repo.
#
# ENUNCIADO A VERIFICAR (Terras 1976, Teorema 1.2):
#
#     T^k(2^k*m + r) = 3^{S_k(r)} * m + T^k(r)
#
# con T = mapa del ATAJO:  T(n) = n/2 si n par,  (3n+1)/2 si n impar.
# S_k(r) = numero de pasos impares entre los k primeros pasos partiendo de r,
#          es decir, cuantos de r, T(r), ..., T^{k-1}(r) son impares.
# Ambito declarado: todo k >= 0, todo 0 <= r < 2^k, todo m >= 0.
#
# Todo con enteros exactos de Python. Ningun float decide nada.

FALLOS = 0

def T(n):
    # mapa del atajo sobre enteros no negativos
    if n % 2 == 0:
        return n // 2
    return (3 * n + 1) // 2

def Tk_y_S(n, k):
    # devuelve (T^k(n), numero de impares entre n, T(n), ..., T^{k-1}(n))
    s = 0
    x = n
    for _ in range(k):
        if x % 2 == 1:
            s += 1
        x = T(x)
    return x, s

def comprobar(k, r, m):
    global FALLOS
    n = (2 ** k) * m + r
    izq, _ = Tk_y_S(n, k)
    tkr, s = Tk_y_S(r, k)
    der = (3 ** s) * m + tkr
    if izq != der:
        FALLOS += 1
        print("FALLO: k=%d r=%d m=%d  izq=%d der=%d" % (k, r, m, izq, der))
        return False
    return True

# ------------------------------------------------------------------
# 1. BORDES PRIMERO: k=0, m=0, r=0, n=1, n=2, y el tope r = 2^k - 1
# ------------------------------------------------------------------
print("== 1. bordes ==")

# k = 0: el unico r valido es 0; el enunciado es T^0(m) = m. Trivial pero se prueba.
for m in [0, 1, 2, 7, 10 ** 30]:
    comprobar(0, 0, m)
print("k=0: ok (5 valores de m, incluido 10^30)")

# m = 0: la identidad se reduce a T^k(r) = T^k(r). Se prueba igual, exhaustivo abajo.
# n = 1 y n = 2 como semillas: aparecen como r=1 (k=1) con m=0, r=2 (k=2) con m=0, etc.
casos_borde = 0
for k in range(0, 15):
    tope = 2 ** k
    for r in [0, 1 % tope, 2 % tope, tope - 1]:
        for m in [0, 1]:
            comprobar(k, r, m)
            casos_borde += 1
print("bordes r en {0,1,2,2^k-1}, m en {0,1}, k=0..14: %d casos, fallos hasta ahora: %d"
      % (casos_borde, FALLOS))

# ------------------------------------------------------------------
# 2. BARRIDO EXHAUSTIVO EN r, MUESTREADO EN m
#    k = 0..13 (todos los restos, 2^0 + ... + 2^13 = 16383 clases)
#    m: incluye 0, chicos, uno grande (2^40+1) y uno gigante (10^50+7)
# ------------------------------------------------------------------
print("== 2. barrido exhaustivo en r ==")
MS = [0, 1, 2, 3, 5, 12, 97, 2 ** 40 + 1, 10 ** 50 + 7]
total = 0
for k in range(0, 14):
    for r in range(2 ** k):
        for m in MS:
            comprobar(k, r, m)
            total += 1
print("k=0..13 exhaustivo en r (16383 clases) x %d valores de m: %d comprobaciones, fallos: %d"
      % (len(MS), total, FALLOS))

# ------------------------------------------------------------------
# 3. k MAS GRANDE, r y m muestreados (k = 20, sin barrido caro)
# ------------------------------------------------------------------
print("== 3. k = 20 muestreado ==")
k = 20
total3 = 0
for r in list(range(0, 2 ** k, 7919)) + [2 ** k - 1]:
    for m in [0, 1, 6, 10 ** 60 + 3]:
        comprobar(k, r, m)
        total3 += 1
print("k=20: %d comprobaciones, fallos: %d" % (total3, FALLOS))

# ------------------------------------------------------------------
# 4. LEMA INTERMEDIO: la paridad del paso j (j < k) la decide solo r.
#    Es lo que hace S_k(r) funcion del resto. Se comprueba aparte.
# ------------------------------------------------------------------
print("== 4. lema de paridades ==")
fallos_par = 0
for k in range(1, 13):
    for r in range(2 ** k):
        base, _ = r, None
        x_r = r
        x_n = (2 ** k) * 5 + r   # m = 5 de testigo
        x_n2 = (2 ** k) * 1 + r  # m = 1 de testigo
        for j in range(k):
            if (x_r % 2) != (x_n % 2) or (x_r % 2) != (x_n2 % 2):
                fallos_par += 1
            x_r, x_n, x_n2 = T(x_r), T(x_n), T(x_n2)
print("paridades de los k primeros pasos iguales para toda la clase: fallos = %d" % fallos_par)
if fallos_par:
    FALLOS += fallos_par

# ------------------------------------------------------------------
# 5. CONTROL NEGATIVO: con el mapa CLASICO (3n+1 sin dividir) la misma
#    formula es FALSA. Si tambien saliera bien, la prueba no discrimina.
# ------------------------------------------------------------------
print("== 5. control con el mapa clasico ==")
def C(n):
    if n % 2 == 0:
        return n // 2
    return 3 * n + 1

def Ck_y_S(n, k):
    s = 0
    x = n
    for _ in range(k):
        if x % 2 == 1:
            s += 1
        x = C(x)
    return x, s

contraejemplos = 0
primero = None
for k in range(1, 8):
    for r in range(2 ** k):
        for m in [1, 2, 3]:
            n = (2 ** k) * m + r
            izq, _ = Ck_y_S(n, k)
            ckr, s = Ck_y_S(r, k)
            der = (3 ** s) * m + ckr
            if izq != der:
                contraejemplos += 1
                if primero is None:
                    primero = (k, r, m, izq, der)
if contraejemplos == 0:
    print("AVISO: el control clasico NO discrimina")
    raise SystemExit("control fallido")
print("mapa clasico: %d contraejemplos; el primero: k=%d r=%d m=%d (izq=%d, der=%d)"
      % ((contraejemplos,) + primero))
print("  -> la identidad es especifica del mapa del ATAJO, como dice el enunciado")

# ------------------------------------------------------------------
# VEREDICTO
# ------------------------------------------------------------------
if FALLOS != 0:
    raise SystemExit("HAY FALLOS: %d" % FALLOS)
print("")
print("VEREDICTO: 0 fallos en la identidad del atajo en todo lo comprobado.")
gran_total = casos_borde + 5 + total + total3
print("total de comprobaciones de la identidad: %d" % gran_total)
