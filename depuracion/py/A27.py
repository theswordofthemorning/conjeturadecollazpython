# A27 - verificacion independiente (Agente 2, Python desde cero)
#
# ENUNCIADO: por cada resto r mod 2^k hay COMO MUCHO UN candidato de ciclo,
# y sale en cerrado:  m = (r - T^k(r)) / (3^{S(r)} - 2^k)
#
# MAPA: el ATAJO.  T(n) = n/2 si n par,  (3n+1)/2 si n impar.
# "ciclo de longitud k" = T^k(n) = n  con  n = 2^k*m + r,  0 <= r < 2^k.
#
# Derivacion propia (la que se pone a prueba):
#   (a) Los primeros k bits de paridad de n los decide n mod 2^k (Terras),
#       y  T^k(2^k*m + r) = 3^{S_k(r)}*m + T^k(r)  para TODO m entero
#       (tambien negativo), donde S_k(r) = impares en los k primeros pasos de r.
#   (b) T^k(n) = n  =>  3^S*m + T^k(r) = 2^k*m + r
#                  =>  m*(3^S - 2^k) = r - T^k(r)
#       El coeficiente 3^S - 2^k es impar-menos-par para k >= 1, nunca 0.
#       Ecuacion lineal con pendiente no nula => COMO MUCHO una solucion m,
#       y es la formula del enunciado. Para k = 0 la pendiente es 0 (S=0,
#       3^0 = 2^0 = 1): la formula NO esta definida y ahi el enunciado
#       necesita k >= 1.
#
# Todo con enteros exactos de Python. Ningun float decide nada.

from fractions import Fraction
import sys

def T(n):
    # mapa del atajo sobre todo Z; para n impar 3n+1 es par, la division es exacta
    if n % 2 == 0:
        return n // 2
    x = 3 * n + 1
    assert x % 2 == 0
    return x // 2

def iterar(n, k):
    """devuelve (T^k(n), impares vistos)"""
    s = 0
    for _ in range(k):
        if n % 2 != 0:
            s += 1
        n = T(n)
    return n, s

fallos = 0

# ------------------------------------------------------------------
# [1] La identidad de Terras que sostiene la formula, verificada cruda:
#     T^k(2^k*m + r) = 3^{S(r)}*m + T^k(r), con m positivos, cero y NEGATIVOS
# ------------------------------------------------------------------
ms = [-1000, -17, -3, -2, -1, 0, 1, 2, 3, 17, 1000]
casos1 = 0
for k in range(1, 11):
    for r in range(2 ** k):
        tkr, s = iterar(r, k)
        for m in ms:
            n = (2 ** k) * m + r
            lhs, s_n = iterar(n, k)
            rhs = (3 ** s) * m + tkr
            casos1 += 1
            if lhs != rhs or s_n != s:
                fallos += 1
                print("FALLO [1] k=%d r=%d m=%d: %d != %d" % (k, r, m, lhs, rhs))
print("[1] identidad de Terras (atajo, m de -1000 a 1000 incl. negativos):",
      casos1, "casos, fallos:", fallos)
if fallos:
    raise SystemExit("[1] la identidad de Terras fallo: la formula no se sostiene")

# ------------------------------------------------------------------
# [2] El denominador 3^S - 2^k: nunca cero para k >= 1; cero exacto en k = 0
# ------------------------------------------------------------------
casos2 = 0
for k in range(1, 17):
    for r in range(2 ** k):
        _, s = iterar(r, k)
        if 3 ** s == 2 ** k:
            fallos += 1
            print("FALLO [2] denominador cero en k=%d r=%d" % (k, r))
        casos2 += 1
# borde k = 0
_, s0 = iterar(7, 0)
den0 = 3 ** s0 - 2 ** 0
print("[2] denominador != 0 en", casos2, "clases (k=1..16), 0 excepciones;",
      "borde k=0: S=0 y denominador =", den0, "(la formula NO aplica en k=0)")
if den0 != 0:
    raise SystemExit("[2] el borde k=0 no da denominador cero, revisar")

# ------------------------------------------------------------------
# [3] UNICIDAD empirica: para cada (k, r), cuantos m en [-60, 60] cumplen
#     T^k(2^k*m + r) = 2^k*m + r ?  Debe ser <= 1, y si hay uno debe ser
#     exactamente el de la formula.
# ------------------------------------------------------------------
casos3 = 0
max_sols = 0
for k in range(1, 9):
    for r in range(2 ** k):
        tkr, s = iterar(r, k)
        num = r - tkr
        den = 3 ** s - 2 ** k
        m_formula = Fraction(num, den)  # exacto
        soluciones = []
        for m in range(-60, 61):
            n = (2 ** k) * m + r
            if iterar(n, k)[0] == n:
                soluciones.append(m)
        casos3 += 1
        max_sols = max(max_sols, len(soluciones))
        if len(soluciones) > 1:
            fallos += 1
            print("FALLO [3] mas de un candidato: k=%d r=%d sols=%s" % (k, r, soluciones))
        if soluciones:
            if Fraction(soluciones[0]) != m_formula:
                fallos += 1
                print("FALLO [3] la solucion no es la de la formula: k=%d r=%d" % (k, r))
        else:
            # si la formula da entero en [-60,60], tendria que haber salido
            if m_formula.denominator == 1 and -60 <= m_formula <= 60:
                fallos += 1
                print("FALLO [3] la formula da m=%s y el barrido no lo ve: k=%d r=%d"
                      % (m_formula, k, r))
print("[3] unicidad: %d clases (k=1..8) x 121 valores de m; maximo de soluciones"
      " por clase = %d (debe ser <= 1); fallos: %d" % (casos3, max_sols, fallos))
if fallos:
    raise SystemExit("[3] unicidad rota")

# ------------------------------------------------------------------
# [4] Barrido k = 1..16: candidato en cerrado por clase, y verificacion de
#     que cada candidato entero cicla de verdad. Sin mirar el signo de m.
# ------------------------------------------------------------------
supervivientes = {}   # k -> lista de n que ciclan
for k in range(1, 17):
    vivos = []
    for r in range(2 ** k):
        tkr, s = iterar(r, k)
        num = r - tkr
        den = 3 ** s - 2 ** k
        if num % den == 0:
            m = num // den
            n = (2 ** k) * m + r
            # el candidato tiene que ciclar de verdad
            if iterar(n, k)[0] != n:
                fallos += 1
                print("FALLO [4] candidato que no cicla: k=%d r=%d n=%d" % (k, r, n))
            else:
                vivos.append(n)
    supervivientes[k] = sorted(set(vivos))

# valores que ciclan segun el barrido, con el periodo minimo en el ATAJO:
#   0 (periodo 1), 1<->2 (periodo 2), -1 (periodo 1),
#   -5 -> -7 -> -10 (periodo 3), y el ciclo de -17 (periodo 11)
ciclo_17 = []
x = -17
for _ in range(11):
    ciclo_17.append(x)
    x = T(x)
assert x == -17, "el ciclo de -17 no cierra en 11 pasos del atajo"

esperado_por_k = {}
for k in range(1, 17):
    es = {0, -1}                    # periodos 1: dividen a todo k
    if k % 2 == 0:
        es |= {1, 2}                # periodo 2
    if k % 3 == 0:
        es |= {-5, -7, -10}         # periodo 3
    if k % 11 == 0:
        es |= set(ciclo_17)         # periodo 11
    esperado_por_k[k] = sorted(es)

ok4 = True
for k in range(1, 17):
    if supervivientes[k] != esperado_por_k[k]:
        ok4 = False
        fallos += 1
        print("FALLO [4] k=%d: supervivientes %s, esperados %s"
              % (k, supervivientes[k], esperado_por_k[k]))
print("[4] barrido k=1..16 (%d clases en total): cada clase da a lo sumo 1"
      " candidato, todos los candidatos enteros ciclan, y los supervivientes"
      " son exactamente {0}, {-1}, {1,2} si 2|k, {-5,-7,-10} si 3|k,"
      " {-17..} si 11|k. Coincide: %s"
      % (sum(2 ** k for k in range(1, 17)), ok4))
print("    positivos supervivientes en todo el barrido:",
      sorted(set(n for k in supervivientes for n in supervivientes[k] if n >= 1)))
if fallos:
    raise SystemExit("[4] barrido con fallos")

# ------------------------------------------------------------------
# [5] BORDES pedidos explicitamente
# ------------------------------------------------------------------
# m = 0: n = r < 2^k. La formula debe recuperarlos: n=1 (k=2), n=2 (k=2)
tk1, s1 = iterar(1, 2)
m1 = Fraction(1 - tk1, 3 ** s1 - 4)
tk2, s2 = iterar(2, 2)
m2 = Fraction(2 - tk2, 3 ** s2 - 4)
print("[5] borde m=0: r=1,k=2 -> T^2(1)=%d, S=%d, m=%s (n=1 cicla: %s);"
      % (tk1, s1, m1, iterar(1, 2)[0] == 1),
      "r=2,k=2 -> m=%s (n=2 cicla: %s)" % (m2, iterar(2, 2)[0] == 2))
if m1 != 0 or m2 != 0:
    raise SystemExit("[5] la formula no recupera n=1, n=2 con m=0")

# n par / impar dentro de la clase: la clase decide, no la paridad del n grande
# (ya cubierto por [1] con m negativos y positivos; aqui un caso concreto)
n_par, n_impar = 8, 7
print("[5] borde paridades: T(8)=%d (par->n/2), T(7)=%d (impar->(3n+1)/2)"
      % (T(8), T(7)))
if T(8) != 4 or T(7) != 11:
    raise SystemExit("[5] el mapa del atajo esta mal implementado")

# k = 0: mod 1 hay UNA clase y TODO n cumple T^0(n)=n: infinitos candidatos.
# El enunciado con "como mucho uno" es FALSO en k=0 y la formula divide por 0.
print("[5] borde k=0: T^0(n)=n para todo n -> infinitos candidatos en la unica")
print("    clase mod 1, y el denominador es 0. El enunciado exige k >= 1.")

# limite del rango: la clase r = 2^k - 1 (todo impares) y r = 0
for k in (8, 16):
    r = 2 ** k - 1
    tkr, s = iterar(r, k)
    if s != k:
        raise SystemExit("[5] la clase 2^k-1 no da k impares seguidos")
print("[5] borde r=2^k-1: S=k exacto (k impares seguidos) en k=8 y k=16;"
      " r=0: candidato n=0 (m=0), cicla:", iterar(0, 5)[0] == 0)

print()
print("RESULTADO: 0 fallos en todo. El enunciado se sostiene para k >= 1;")
print("en k = 0 la formula no esta definida (denominador 0) y ahi 'como mucho")
print("un candidato' es ademas falso (todo n es un 0-ciclo).")
