# Pandas y la pregunta de Gao (1993, pag. 266): conteo exacto para 1 <= n < 2^M.
#
# Mapa clasico C(n) = n/2 si n es par, 3n+1 si es impar. Hasta la primera
# llegada a 1 se cuentan:
#   S(n)   = pasos impares;
#   TAU(n) = divisiones por 2, que es el sigma_inf de Gao y el tiempo del atajo T;
#   H(n)   = S(n) + TAU(n), la altura clasica.
# El residuo de Roosendaal es Res(n) = 2^TAU / (3^S * n).
#
# Comprueba, con enteros y Fraction:
#   1. que todo residuo es menor que 3, es decir 2^TAU < 3^(S+1) * n;
#   2. el residuo maximo y los n donde se alcanza;
#   3. que ningun par (n, n+1) tiene igual altura y distinto TAU (pregunta de Gao);
#   4. la identidad de Pandas 6^d = (n/(n+1)) * Res(n) / Res(n+1), con
#      d = TAU(n) - TAU(n+1), en los pares de la racha 943..949 de Gao.
#
# Es un barrido finito: no prueba nada para todo n.
from fractions import Fraction

M = 20
N = 2 ** M

S = [0] * N
TAU = [0] * N
for n in range(2, N):
    x = n
    s = 0
    t = 0
    while x >= n:
        if x % 2 == 1:
            x = 3 * x + 1
            s = s + 1
        else:
            x = x // 2
            t = t + 1
    S[n] = s + S[x]
    TAU[n] = t + TAU[x]


def residuo(n):
    return Fraction(2 ** TAU[n], 3 ** S[n] * n)


# 1 y 2: residuos menores que 3 y el maximo, comparando a/b con c/d por a*d y c*b
menores_que_3 = 0
max_num = 0
max_den = 1
donde = []
for n in range(1, N):
    num = 2 ** TAU[n]
    den = 3 ** S[n] * n
    if num < 3 * den:
        menores_que_3 = menores_que_3 + 1
    if num * max_den > max_num * den:
        max_num = num
        max_den = den
        donde = [n]
    elif num * max_den == max_num * den:
        donde.append(n)

print(f"Rango: 1 <= n < 2^{M}")
print(f"Residuos menores que 3: {menores_que_3} de {N - 1}")
maximo = Fraction(max_num, max_den)
print(f"Residuo maximo: {float(maximo):.9f}  (fraccion exacta {maximo})")
print(f"Se alcanza en: {donde}")

# 3: la pregunta de Gao
iguales = 0
contraejemplos = 0
for n in range(1, N - 1):
    if S[n] + TAU[n] == S[n + 1] + TAU[n + 1]:
        iguales = iguales + 1
        if TAU[n] != TAU[n + 1]:
            contraejemplos = contraejemplos + 1
print(f"Pares (n, n+1) con igual altura: {iguales}")
print(f"De ellos, con distinto sigma_inf: {contraejemplos}")

# 4: la identidad de Pandas en la racha de Gao
print("Identidad de Pandas en la racha 943..949:")
for n in range(943, 949):
    d = TAU[n] - TAU[n + 1]
    lado = Fraction(n, n + 1) * residuo(n) / residuo(n + 1)
    print(f"  n={n}  H={S[n] + TAU[n]}  sigma_inf={TAU[n]}  d={d}  "
          f"(n/(n+1))*Res(n)/Res(n+1) = {lado}  6^d = {Fraction(6) ** d}  "
          f"{'coincide' if lado == Fraction(6) ** d else 'NO COINCIDE'}")
