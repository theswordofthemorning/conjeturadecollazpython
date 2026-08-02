# A12 - AGENTE 2 (independiente): verificar
#   ENUNCIADO: n + espejo(n) = 10^k, exacto y siempre  (todo n >= 1, base 10)
#
# INTERPRETACION (derivada desde cero, sin abrir ningun fichero del repo):
#   El "espejo" en base 10 es el complemento a la potencia de 10 de la decada:
#       espejo(n) = 10^d - n,   con d = numero de digitos decimales de n.
#   Con esa definicion la identidad es tautologica (cero grados de libertad).
#   Puntos fijos esperados: espejo(n) = n  <=>  2n = 10^d  <=>  n = 5*10^(d-1).
#
# MAPA: aqui NO interviene ningun mapa de Collatz (ni clasico, ni atajo, ni 3n-1).
#   Es aritmetica de base 10 pura.
#
# Todo con int exacto. Ningun float decide nada.

def digitos(n):
    # contar digitos sin str() para no depender de representaciones: division entera
    if n < 1:
        raise SystemExit("digitos() solo definido aqui para n >= 1")
    d = 0
    m = n
    while m > 0:
        m //= 10
        d += 1
    return d

def espejo(n):
    return 10 ** digitos(n) - n

fallos = 0

# ---------------------------------------------------------------
# COMPROBACION 1: exhaustiva n = 1 .. 10^6 (incluye ambos bordes de cada decada)
LIMITE = 10 ** 6
for n in range(1, LIMITE + 1):
    d = digitos(n)
    if n + espejo(n) != 10 ** d:
        print("FALLO C1: n =", n, "espejo =", espejo(n), "suma =", n + espejo(n))
        fallos += 1
        if fallos > 5:
            raise SystemExit("C1: demasiados fallos")
print("C1: n + espejo(n) == 10^digitos(n) exhaustivo n = 1 ..", LIMITE, "-> 0 fallos" if fallos == 0 else "-> FALLOS")
if fallos:
    raise SystemExit("C1 fallo")

# ---------------------------------------------------------------
# COMPROBACION 2: bordes explicitos, incluidos numeros gigantes (200 digitos)
bordes = [1, 2, 5, 9, 10, 11, 50, 99, 100, 101, 500, 999, 1000,
          10**6, 10**6 + 1, 5 * 10**5,
          10**199, 10**200 - 1, 5 * 10**199, 7 * 10**199 + 123456789]
for n in bordes:
    d = digitos(n)
    s = n + espejo(n)
    if s != 10 ** d:
        print("FALLO C2: n =", n)
        raise SystemExit("C2 fallo")
print("C2: bordes (1, 9, 10, 99, 100, ..., y 4 numeros de 200 digitos) -> 0 fallos")

# ---------------------------------------------------------------
# COMPROBACION 3: espejo(n) >= 1 siempre (el espejo queda dentro de los positivos)
#   y espejo es involucion DENTRO de la decada: espejo(espejo(n)) == n cuando
#   espejo(n) tiene los mismos digitos que n; si cambia de decada, NO (se declara).
inv_ok = 0
inv_cambia_decada = 0
for n in range(1, 100001):
    e = espejo(n)
    if e < 1:
        print("FALLO C3: espejo(", n, ") =", e, "< 1")
        raise SystemExit("C3 fallo")
    if digitos(e) == digitos(n):
        if espejo(e) != n:
            print("FALLO C3: involucion rota en n =", n)
            raise SystemExit("C3 fallo")
        inv_ok += 1
    else:
        inv_cambia_decada += 1
print("C3: espejo >= 1 siempre; involucion misma-decada:", inv_ok, "ok;",
      inv_cambia_decada, "cambian de decada (espejo(espejo(n)) != n ahi, p.ej. n=99 -> 1 -> 9)")

# ---------------------------------------------------------------
# COMPROBACION 4: puntos fijos en 1..10^6 son EXACTAMENTE 5*10^m
fijos = [n for n in range(1, 10**6 + 1) if espejo(n) == n]
esperados = [5, 50, 500, 5000, 50000, 500000]
if fijos != esperados:
    print("FALLO C4: fijos =", fijos)
    raise SystemExit("C4 fallo")
print("C4: puntos fijos en 1..10^6 =", fijos, "-> exactamente 5*10^m, como exige 2n = 10^d")

# ---------------------------------------------------------------
# COMPROBACION 5: parejas conocidas de control (derivables a mano)
parejas = [(2, 8, 10), (20, 80, 100), (47, 53, 100), (332, 668, 1000), (350, 650, 1000)]
for a, b, p in parejas:
    if espejo(a) != b or a + b != p:
        print("FALLO C5:", a, b)
        raise SystemExit("C5 fallo")
print("C5: parejas de control (2,8) (20,80) (47,53) (332,668) (350,650) -> 0 fallos")

# ---------------------------------------------------------------
# COMPROBACION 6 (adversarial): la OTRA lectura posible de "espejo" -- invertir
#   los digitos (reversal) -- NO cumple el enunciado. Si cumpliera, la ficha seria
#   ambigua; se mide cuantos n la cumplen por casualidad.
def reversal(n):
    r = 0
    m = n
    while m > 0:
        r = r * 10 + (m % 10)
        m //= 10
    return r

cumplen_rev = 0
ejemplo_falla = None
for n in range(1, 100001):
    s = n + reversal(n)
    # es potencia de 10?
    p = 1
    while p < s:
        p *= 10
    if p == s:
        cumplen_rev += 1
    elif ejemplo_falla is None:
        ejemplo_falla = (n, reversal(n), s)
print("C6: con espejo = INVERSION DE DIGITOS el enunciado falla; en 1..100000 lo cumplen",
      cumplen_rev, "de 100000; primer contraejemplo:", ejemplo_falla)
print("    -> el enunciado solo es verdadero con espejo(n) = 10^digitos(n) - n (complemento).")

# ---------------------------------------------------------------
print()
print("VEREDICTO A2: SOSTIENE. n + espejo(n) = 10^d(n) es una identidad de definicion,")
print("verificada exhaustiva 1..10^6 (0 fallos), bordes de decada y numeros de 200 digitos,")
print("puntos fijos exactamente 5*10^m. Ningun mapa de Collatz interviene.")
