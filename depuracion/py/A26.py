# A26 - verificacion independiente (agente 2, Python desde cero)
#
# ENUNCIADO: si dos trayectorias se funden gastando los MISMOS pares y los
# MISMOS impares, entonces 2^r*k + n1 y 2^r*k + n2 se funden para todo k,
# siempre que r sea MAYOR que el numero de pasos pares del tramo.
#
# MAPA: clasico (n par -> n/2, n impar -> 3n+1). "Pares" = divisiones,
# "impares" = pasos 3n+1. Todo con enteros exactos de Python.
#
# Definicion usada de "fundirse": existe un indice j tal que
# T^j(n1) == T^j(n2) (mismo indice, mismo valor). El tramo es 0..j con j
# minimo. "Mismos pares y mismos impares": los conteos (e, o) de pasos
# pares e impares en el tramo coinciden entre n1 y n2.

MAX_PASOS = 400          # tope de pasos para buscar la fusion
TOPE_PAR  = 300          # pares (n1, n2) con 1 <= n1 < n2 <= TOPE_PAR
KS        = list(range(0, 31)) + [1000, 10**6 + 7]   # bordes: k=0 y k grandes

def paso(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1

def tray(n, N):
    t = [n]
    for _ in range(N):
        n = paso(n)
        t.append(n)
    return t

def cuentas(t, j):
    # pasos pares e impares en los primeros j pasos de la trayectoria t
    e = sum(1 for i in range(j) if t[i] % 2 == 0)
    o = j - e
    return e, o

def fusion(n1, n2, maxp=MAX_PASOS):
    # primer j con T^j(n1) == T^j(n2); None si no aparece
    t1 = tray(n1, maxp)
    t2 = tray(n2, maxp)
    for j in range(maxp + 1):
        if t1[j] == t2[j]:
            return j, t1, t2
    return None, t1, t2

# ---------------------------------------------------------------------------
# 1. recolectar pares que se funden con las MISMAS cuentas (hipotesis del
#    enunciado) y pares que se funden con cuentas DISTINTAS (control)
# ---------------------------------------------------------------------------
con_hipotesis = []   # (n1, n2, j, e, o)
sin_hipotesis = []   # (n1, n2, j, e1, o1, e2, o2)

for n1 in range(1, TOPE_PAR + 1):
    for n2 in range(n1 + 1, TOPE_PAR + 1):
        j, t1, t2 = fusion(n1, n2)
        if j is None or j == 0:
            continue
        e1, o1 = cuentas(t1, j)
        e2, o2 = cuentas(t2, j)
        if (e1, o1) == (e2, o2):
            con_hipotesis.append((n1, n2, j, e1, o1))
        else:
            sin_hipotesis.append((n1, n2, j, e1, o1, e2, o2))

print("pares que se funden con mismas cuentas :", len(con_hipotesis))
print("pares que se funden con cuentas distintas:", len(sin_hipotesis))
if not con_hipotesis:
    raise SystemExit("FALLO: no hay pares con la hipotesis, no se puede verificar")

# ---------------------------------------------------------------------------
# 2. el teorema, atacado: para cada par con hipotesis, r > e (r = e+1, e+2,
#    e+5) y todos los k de KS, comprobar que 2^r*k+n1 y 2^r*k+n2 se funden
#    EN EL MISMO INDICE j con el MISMO valor, y ademas contra la forma
#    cerrada  T^j(2^r*k + n) = 3^o * 2^(r-e) * k + T^j(n)  (exacta, enteros)
# ---------------------------------------------------------------------------
fallos_teorema = 0
comprobaciones = 0
muestra = con_hipotesis[:800]   # limitar el coste; sigue siendo miles de casos

for (n1, n2, j, e, o) in muestra:
    v = tray(n1, j)[j]           # valor de fusion
    for dr in (1, 2, 5):
        r = e + dr
        for k in KS:
            a = (1 << r) * k + n1
            b = (1 << r) * k + n2
            ta = tray(a, j)
            tb = tray(b, j)
            comprobaciones += 1
            esperado = 3**o * (1 << (r - e)) * k + v
            if ta[j] != tb[j] or ta[j] != esperado:
                fallos_teorema += 1
                if fallos_teorema <= 5:
                    print("FALLO teorema:", n1, n2, "r=", r, "k=", k,
                          ta[j], tb[j], esperado)

print("teorema con r > e:", comprobaciones, "comprobaciones,",
      fallos_teorema, "fallos")

# ---------------------------------------------------------------------------
# 3. el borde r = e (r NO mayor que los pares): debe romperse en una
#    fraccion de los casos -> la hipotesis 'r > e' es necesaria
# ---------------------------------------------------------------------------
fallos_re = 0
casos_re = 0
for (n1, n2, j, e, o) in muestra:
    if e == 0:
        continue
    r = e
    v = tray(n1, j)[j]
    for k in range(1, 21):       # k impares incluidos, que son los que rompen
        a = (1 << r) * k + n1
        b = (1 << r) * k + n2
        casos_re += 1
        if tray(a, j)[j] != tray(b, j)[j]:
            fallos_re += 1

print("borde r = e:", casos_re, "casos,", fallos_re,
      "fallos (se espera > 0: la hipotesis r > e es necesaria)")

# ---------------------------------------------------------------------------
# 4. el borde de la OTRA hipotesis: par (3, 20). Se 'funden' en el sentido
#    flojo (los dos pasan por 10 en el indice 1) pero con cuentas distintas
#    (3 gasta 1 impar, 20 gasta 1 par). La propagacion debe fallar casi
#    siempre -> 'mismas cuentas' es necesaria
# ---------------------------------------------------------------------------
t3 = tray(3, 1); t20 = tray(20, 1)
print("control (3,20): T(3) =", t3[1], " T(20) =", t20[1],
      " cuentas:", cuentas(t3, 1), "vs", cuentas(t20, 1))

for r in (8, 10, 12):
    exitos = 0
    for k in range(1, 41):
        a = (1 << r) * k + 3
        b = (1 << r) * k + 20
        if tray(a, 1)[1] == tray(b, 1)[1]:
            exitos += 1
    print("  (3,20) r =", r, ": fusion en el indice 1 en", exitos, "de 40 k")

# ---------------------------------------------------------------------------
# 5. bordes sueltos: k = 0 (trivial), el par de Garner (4,5), y k enorme
# ---------------------------------------------------------------------------
j45, t4, t5 = fusion(4, 5)
e45, o45 = cuentas(t4, j45)
assert (e45, o45) == cuentas(t5, j45), "las cuentas de (4,5) deberian coincidir"
print("par (4,5): j =", j45, " e =", e45, " o =", o45,
      " valor de fusion =", t4[j45])
fallos45 = 0
for k in range(0, 41):
    a = (1 << (e45 + 1)) * k + 4
    b = (1 << (e45 + 1)) * k + 5
    if tray(a, j45)[j45] != tray(b, j45)[j45]:
        fallos45 += 1
print("par (4,5) con r = e+1 =", e45 + 1, ", k = 0..40:", fallos45, "fallos")

# k gigantesco, un caso puntual con enteros exactos
n1, n2, j, e, o = con_hipotesis[0]
r = e + 1
K = 10**50 + 12345
a = (1 << r) * K + n1
b = (1 << r) * K + n2
v = tray(n1, j)[j]
esperado = 3**o * (1 << (r - e)) * K + v
assert tray(a, j)[j] == tray(b, j)[j] == esperado, "fallo con k = 10^50"
print("k = 10^50 + 12345 sobre el par", (n1, n2), ": fusion exacta, 0 fallos")

if fallos_teorema != 0:
    raise SystemExit("VEREDICTO: el enunciado FALLA en el rango probado")
if fallos_re == 0:
    print("AVISO: r = e no fallo nunca en la muestra; la necesidad de r > e"
          " no quedo exhibida aqui (no refuta el enunciado)")
print("VEREDICTO: 0 fallos del enunciado en todo el rango probado")
