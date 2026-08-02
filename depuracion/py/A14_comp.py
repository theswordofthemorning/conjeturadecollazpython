# A14 comparador - tercera implementacion, sin compartir codigo con las otras dos.
# Cuenta digitos convirtiendo a cadena en base b (metodo distinto del bucle //).

def a_base(n, b):
    s = []
    while n > 0:
        s.append(n % b)
        n //= b
    return s[::-1]

def espejo(n, b):
    L = len(a_base(n, b))
    return b ** L - n

# caso comun de los dos agentes: base 10 -> fijos 5, 50, 500 (hasta 999)
fijos10 = [n for n in range(1, 1000) if espejo(n, 10) == n]
assert fijos10 == [5, 50, 500], fijos10
print("caso comun base 10, n<1000:", fijos10)

# las parejas del repo que fijan la definicion (unico mapa compatible)
for a, bb in [(2, 8), (20, 80), (47, 53), (332, 668), (350, 650)]:
    assert espejo(a, 10) == bb, (a, bb, espejo(a, 10))
print("parejas 2-8, 20-80, 47-53, 332-668, 350-650: cuadran con b^L - n")
# y NO cuadran con la reversa de digitos ni con el complemento por cifra b-1-d:
rev47 = int(str(47)[::-1]); comp47 = 99 - 47
assert rev47 != 53 and comp47 != 53
print("descarte: reversa(47)=%d, complemento9(47)=%d, ninguno da 53" % (rev47, comp47))

# barrido corto en las 15 bases contra la prediccion, n = 1..50000
fallos = 0
for b in range(2, 17):
    medidos = [n for n in range(1, 50001) if espejo(n, b) == n]
    if b % 2 == 0:
        pred = []
        m = 0
        while (b // 2) * b ** m <= 50000:
            pred.append((b // 2) * b ** m)
            m += 1
    else:
        pred = []
    if medidos != pred:
        fallos += 1
        print("DISCREPA base", b, medidos, pred)
if fallos:
    raise SystemExit("FALLO")
print("15 bases, n=1..50000: conjunto de fijos = prediccion, 0 fallos")

# barrido base 2 hasta 299 (para cruzar con el decide del agente 1)
f2 = [n for n in range(1, 300) if espejo(n, 2) == n]
assert f2 == [1, 2, 4, 8, 16, 32, 64, 128, 256], f2
print("base 2, n<300:", f2, "(= el barrido decide del agente 1)")

# base 6 hasta 699 (cruce con el otro decide)
f6 = [n for n in range(1, 700) if espejo(n, 6) == n]
assert f6 == [3, 18, 108, 648], f6
print("base 6, n<700:", f6, "(= el barrido decide del agente 1)")
print("COMPARADOR: 0 fallos")
