# A14 - verificacion independiente, escrita desde cero.
#
# ENUNCIADO: el espejo en base b tiene puntos fijos exactamente (b/2)*b^m
#            si b es par, y NI UNO si b es impar.
#
# DEFINICION DEL ESPEJO (derivada de las parejas registradas en la base:
# 2<->8, 20<->80, 47<->53, 332<->668, 350<->650, fijo 5, todas en base 10):
#   espejo_b(n) = b^k - n,   donde k = numero de digitos de n en base b.
# Comprobacion de la definicion: 10-2=8, 100-20=80, 100-47=53, 1000-332=668,
# 1000-350=650, 10-5=5. Todas cuadran; no hay otra funcion "espejo" simple
# (reversa de digitos, complemento b-1) que las cuadre todas.
#
# El enunciado es un "exactamente": conjunto de puntos fijos = {(b/2)*b^m, m>=0}
# para b par, vacio para b impar. Es una afirmacion universal, no un promedio.
#
# Verificacion en dos capas:
#  (1) barrido exhaustivo n = 1..LIMITE en las 15 bases 2..16, comparando el
#      conjunto medido contra el predicho (interseccion con el rango).
#  (2) el argumento en cerrado, comprobado con enteros: para cada k, la ecuacion
#      n = b^k - n tiene solucion entera n = b^k/2 sii b es par, y esa solucion
#      tiene exactamente k digitos (b^(k-1) <= n < b^k). Comprobado k = 1..60.
# Bordes probados: n=1, n=b-1, n=b^k, b=2 (el caso minimo), el limite del rango.
# Aritmetica: solo int de Python. Ningun float decide nada.

LIMITE = 200_000
BASES = range(2, 17)

def num_digitos(n, b):
    # n >= 1
    k = 0
    while n > 0:
        n //= b
        k += 1
    return k

def espejo(n, b):
    return b ** num_digitos(n, b) - n

fallos = 0

# ---- capa 1: barrido exhaustivo ----
for b in BASES:
    medidos = [n for n in range(1, LIMITE + 1) if espejo(n, b) == n]
    if b % 2 == 0:
        predichos = []
        m = 0
        while (b // 2) * b ** m <= LIMITE:
            predichos.append((b // 2) * b ** m)
            m += 1
    else:
        predichos = []
    ok = medidos == predichos
    if not ok:
        fallos += 1
    print("base %2d : fijos medidos %-40s predichos %-40s %s"
          % (b, medidos, predichos, "OK" if ok else "FALLO"))

if fallos:
    raise SystemExit("FALLO en la capa 1: el conjunto medido no es el predicho")

# ---- capa 2: el argumento en cerrado, con enteros ----
# punto fijo con k digitos  <=>  n = b^k - n  <=>  2n = b^k
# solucion entera sii b^k par sii b par (k>=1). Unicidad: una por k.
# y hay que comprobar que n = b^k/2 tiene de verdad k digitos.
for b in BASES:
    for k in range(1, 61):
        bk = b ** k
        if b % 2 == 0:
            n = bk // 2
            assert 2 * n == bk, "b^k/2 no es entero con b par?!"
            if not (b ** (k - 1) <= n < bk):
                raise SystemExit("FALLO: b=%d k=%d, b^k/2 no tiene k digitos" % (b, k))
            if num_digitos(n, b) != k or espejo(n, b) != n:
                raise SystemExit("FALLO: b=%d k=%d, el candidato no es fijo" % (b, k))
            # y n = (b/2)*b^(k-1), o sea la forma (b/2)*b^m con m = k-1
            if n != (b // 2) * b ** (k - 1):
                raise SystemExit("FALLO: b=%d k=%d, forma (b/2)*b^m rota" % (b, k))
        else:
            if bk % 2 == 0:
                raise SystemExit("FALLO: b impar con b^k par, b=%d k=%d" % (b, k))
            # 2n = b^k impar -> sin solucion entera: ni un punto fijo con k digitos
print("capa 2: k = 1..60, 15 bases: la ecuacion 2n = b^k decide todo, 0 fallos")

# ---- bordes explicitos ----
# n = 1: espejo(1) = b - 1; fijo sii b = 2. (1 = (2/2)*2^0: es el m=0 de b=2)
for b in BASES:
    es_fijo = (espejo(1, b) == 1)
    if es_fijo != (b == 2):
        raise SystemExit("FALLO en el borde n=1, base %d" % b)
# n = b - 1 (el digito maximo): espejo = b - (b-1) = 1; fijo solo si b-1 = 1 (b=2)
for b in BASES:
    if (espejo(b - 1, b) == b - 1) != (b == 2):
        raise SystemExit("FALLO en el borde n=b-1, base %d" % b)
# n = b^k (un 1 seguido de k ceros): espejo = b^(k+1) - b^k, nunca fijo salvo b=2
# (b=2: espejo(2^k) = 2^(k+1) - 2^k = 2^k, fijo -- y ES (b/2)*b^m con m=k)
for b in BASES:
    for k in range(1, 20):
        fijo = (espejo(b ** k, b) == b ** k)
        if fijo != (b == 2):
            raise SystemExit("FALLO en el borde n=b^k, base %d k %d" % (b, k))
print("bordes n=1, n=b-1, n=b^k: consistentes (solo b=2 los tiene fijos, y son (b/2)*b^m)")

print()
print("VEREDICTO: 0 fallos. Puntos fijos de espejo_b(n) = b^k - n:")
print("  b par   -> exactamente { (b/2)*b^m : m >= 0 }  (uno por cada numero de digitos)")
print("  b impar -> ninguno (2n = b^k no tiene solucion entera)")
