# Comparador A33: tercera implementacion, estructuralmente distinta.
# - lambda_j como Fraction exacta (no comparacion de potencias enteras)
# - criba "todos los j <= k" (la de los dos agentes) CONTRA la variante
#   "solo j = k", para ver si la eleccion de formalizacion cambia el objeto.
from fractions import Fraction

def T(n):
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2

def lambdas(r, k):
    # devuelve la lista de lambda_j = 3^{S_j}/2^j, j = 1..k
    x, S, out = r, 0, []
    for j in range(1, k + 1):
        if x % 2 == 1:
            S += 1
        x = T(x)
        out.append(Fraction(3 ** S, 2 ** j))
    return out

KMAX = 16
conteos_todos = []   # sobrevive si lambda_j >= 1 para TODO j <= k
conteos_final = []   # variante: sobrevive si lambda_k >= 1 (solo el ultimo)
testigo_ok = True
for k in range(0, KMAX + 1):
    a_todos = a_final = 0
    for r in range(2 ** k):
        ls = lambdas(r, k)
        if all(l >= 1 for l in ls):
            a_todos += 1
            if r == 2 ** k - 1:
                pass
        if not ls or ls[-1] >= 1:
            a_final += 1
    conteos_todos.append(a_todos)
    conteos_final.append(a_final)
    # el testigo, comprobado aparte
    if not all(l >= 1 for l in lambdas(2 ** k - 1, k)):
        testigo_ok = False
        print("FALLO: 2^%d - 1 no sobrevive" % k)

print("criterio 'todo j<=k' :", conteos_todos)
print("criterio 'solo j=k'  :", conteos_final)
print("distinguen?          :", conteos_todos != conteos_final)
print("testigo 2^k-1 sobrevive en k=0..%d: %s" % (KMAX, testigo_ok))

# caso comun de los dos agentes: T^5(31) = 242 = 3^5 - 1, S_5 = 5
x, S = 31, 0
for _ in range(5):
    if x % 2:
        S += 1
    x = T(x)
print("T^5(31) =", x, " S_5 =", S, " esperado 242 y 5")

# A076227 (terminos que conozco de OEIS, offset a(1)): 1,1,2,3,4,8,13,19,38,64,128,226,367,734,1295,2114
oeis = [1, 1, 2, 3, 4, 8, 13, 19, 38, 64, 128, 226, 367, 734, 1295, 2114]
print("cuadra con A076227 a(1)..a(16):", conteos_todos[1:] == oeis)
