# A61 - verificacion independiente (agente 2, Python desde cero)
#
# ENUNCIADO: en un ciclo de 3n+1 la C de la identidad es POSITIVA, luego
#            B/A > log2(3); en uno de 3n-1 es negativa y B/A < log2(3).
#
# MAPA: la identidad se deriva aqui sobre el mapa CLASICO (par: n/2, impar: 3n+1
# o 3n-1). A = pasos impares (multiplicaciones), B = pasos pares (divisiones).
# Nota: con el mapa del atajo ((3n+-1)/2 en impares) los valores A, B, C de una
# vuelta de ciclo son LOS MISMOS, porque cada paso impar del atajo es un impar
# clasico seguido de una division. Lo compruebo tambien abajo (comprobacion 6).
#
# DERIVACION PROPIA de la identidad (no copiada de ningun fichero):
#   invariante  2^B * actual = 3^A * n0 + C,  arrancando A=B=C=0, actual=n0.
#   paso par   (actual -> actual/2, B+1):        C no cambia.
#   paso impar (actual -> 3*actual+s, A+1):      C -> 3*C + s*2^B   (s = +1 o -1)
#   (se verifica el invariante paso a paso con enteros exactos)
#
# En un ciclo de una vuelta: actual vuelve a n0, luego 2^B*n0 = 3^A*n0 + C.
#   Si C > 0:  2^B*n0 > 3^A*n0  ->  2^B > 3^A  ->  B/A > log2(3)   (si A >= 1)
#   Si C < 0:  2^B < 3^A        ->  B/A < log2(3)
# La comparacion B/A vs log2(3) se hace como ENTEROS: 2^B vs 3^A. Ni un float.

import sys

fallos = []

def paso(n, s):
    # mapa clasico con signo s: par -> n/2, impar -> 3n + s
    if n % 2 == 0:
        return n // 2
    return 3 * n + s

def abc_de_tramo(n0, num_pasos, s):
    # recorre num_pasos del mapa clasico manteniendo el invariante y
    # comprobandolo con enteros exactos en CADA paso
    A = 0
    B = 0
    C = 0
    actual = n0
    for _ in range(num_pasos):
        if actual % 2 == 0:
            actual = actual // 2
            B += 1
        else:
            C = 3 * C + s * (2 ** B)
            actual = 3 * actual + s
            A += 1
        if (2 ** B) * actual != (3 ** A) * n0 + C:
            fallos.append("invariante roto en n0=%d s=%d" % (n0, s))
            raise SystemExit("FALLO: invariante roto")
    return A, B, C, actual

def busca_ciclos(s, tope, max_pasos):
    # devuelve los ciclos (como tupla canonica empezando en su minimo)
    # que alcanzan las semillas 1..tope bajo el mapa clasico con signo s
    ciclos = {}
    for n0 in range(1, tope + 1):
        vistos = {}
        n = n0
        pasos = 0
        while n not in vistos and pasos <= max_pasos:
            vistos[n] = pasos
            n = paso(n, s)
            pasos += 1
        if n in vistos:
            # extraer el ciclo
            ciclo = []
            m = n
            while True:
                ciclo.append(m)
                m = paso(m, s)
                if m == n:
                    break
            mn = min(ciclo)
            i = ciclo.index(mn)
            canon = tuple(ciclo[i:] + ciclo[:i])
            ciclos[canon] = True
        else:
            fallos.append("semilla %d sin ciclo en %d pasos (s=%d)" % (n0, max_pasos, s))
    return sorted(ciclos.keys())

TOPE = 10000
MAXP = 100000

print("A61: signo de C en ciclos y lado de B/A respecto de log2(3)")
print("mapa: clasico (par n/2, impar 3n+s), s=+1 y s=-1; semillas 1..%d" % TOPE)
print("")

# ---- comprobacion 1: inventario de ciclos alcanzados ----
ciclos_mas = busca_ciclos(+1, TOPE, MAXP)
ciclos_menos = busca_ciclos(-1, TOPE, MAXP)

print("[1] ciclos alcanzados desde 1..%d:" % TOPE)
print("    3n+1: %d ciclo(s): %s" % (len(ciclos_mas), [c[:6] for c in ciclos_mas]))
print("    3n-1: %d ciclo(s), largos %s, minimos %s" %
      (len(ciclos_menos), [len(c) for c in ciclos_menos], [min(c) for c in ciclos_menos]))

if len(ciclos_mas) != 1 or ciclos_mas[0] != (1, 4, 2):
    fallos.append("inventario 3n+1 inesperado: %s" % ciclos_mas)
esperados_menos = sorted([1, 5, 17])
if len(ciclos_menos) != 3 or sorted(min(c) for c in ciclos_menos) != esperados_menos:
    fallos.append("inventario 3n-1 inesperado: %s" % ciclos_menos)

# ---- comprobacion 2: el enunciado, ciclo por ciclo, una vuelta ----
print("")
print("[2] una vuelta de cada ciclo, identidad exacta y signo de C:")
resultados = []
for s, ciclos in ((+1, ciclos_mas), (-1, ciclos_menos)):
    for ciclo in ciclos:
        n0 = ciclo[0]
        L = len(ciclo)
        A, B, C, fin = abc_de_tramo(n0, L, s)
        if fin != n0:
            fallos.append("ciclo no cierra: s=%d n0=%d" % (s, n0))
        # identidad de vuelta completa
        if (2 ** B) * n0 != (3 ** A) * n0 + C:
            fallos.append("identidad de ciclo rota: s=%d n0=%d" % (s, n0))
        # A >= 1 (sin pasos impares no hay ciclo posible salvo degenerado)
        if A < 1:
            fallos.append("ciclo con A=0: s=%d n0=%d" % (s, n0))
        # signo de C y lado de B/A, todo en enteros
        if s == +1:
            if not (C > 0):
                fallos.append("C no positiva en ciclo 3n+1: n0=%d C=%d" % (n0, C))
            if not ((2 ** B) > (3 ** A)):
                fallos.append("2^B <= 3^A en ciclo 3n+1: n0=%d" % n0)
        else:
            if not (C < 0):
                fallos.append("C no negativa en ciclo 3n-1: n0=%d C=%d" % (n0, C))
            if not ((2 ** B) < (3 ** A)):
                fallos.append("2^B >= 3^A en ciclo 3n-1: n0=%d" % n0)
        lado = ">" if (2 ** B) > (3 ** A) else "<"
        print("    s=%+d  min=%-3d largo=%-3d A=%-2d B=%-2d C=%-6d  2^B %s 3^A  (B/A=%.4f, log2 3=1.5850)"
              % (s, n0, L, A, B, C, lado, B / A))
        resultados.append((s, n0, A, B, C))

# ---- comprobacion 3: el espejo 2 = 3 - 1 y 4 = 3 + 1 ----
print("")
print("[3] los dos ciclos con minimo 1:")
for s, n0, A, B, C in resultados:
    if n0 == 1:
        print("    s=%+d: 2^%d = 3^%d %+d  ->  %d = %d %+d" %
              (s, B, A, C, 2 ** B, 3 ** A, C))
        if s == +1 and not (A == 1 and B == 2 and C == 1):
            fallos.append("el ciclo trivial de 3n+1 no da 4 = 3 + 1")
        if s == -1 and not (A == 1 and B == 1 and C == -1):
            fallos.append("el ciclo de 1 en 3n-1 no da 2 = 3 - 1")

# ---- comprobacion 4: varias vueltas (el signo no depende de cuantas) ----
print("")
print("[4] dos y tres vueltas de cada ciclo:")
ok_vueltas = 0
for s, ciclos in ((+1, ciclos_mas), (-1, ciclos_menos)):
    for ciclo in ciclos:
        n0 = ciclo[0]
        L = len(ciclo)
        for vueltas in (2, 3):
            A, B, C, fin = abc_de_tramo(n0, L * vueltas, s)
            if fin != n0:
                fallos.append("multivuelta no cierra: s=%d n0=%d v=%d" % (s, n0, vueltas))
            if s == +1 and not (C > 0 and (2 ** B) > (3 ** A)):
                fallos.append("multivuelta 3n+1 falla: n0=%d v=%d" % (n0, vueltas))
            if s == -1 and not (C < 0 and (2 ** B) < (3 ** A)):
                fallos.append("multivuelta 3n-1 falla: n0=%d v=%d" % (n0, vueltas))
            ok_vueltas += 1
print("    %d casos multivuelta, signo y lado correctos en todos" % ok_vueltas)

# ---- comprobacion 5: bordes y estructura general del signo de C ----
# El argumento estructural: C arranca en 0, los pasos pares no lo tocan y un
# paso impar hace C -> 3C + s*2^B. Con s=+1, C queda >= 0 siempre y > 0 en
# cuanto A >= 1. Con s=-1, C <= 0 y < 0 en cuanto A >= 1. Lo mido sobre
# TRAMOS ARBITRARIOS (no solo ciclos), incluidos bordes n=1, n=2, k=0.
print("")
print("[5] signo de C sobre tramos arbitrarios (no solo ciclos):")
casos = 0
for s in (+1, -1):
    for n0 in list(range(1, 300)) + [2 ** 20, 2 ** 20 + 1]:
        for k in (0, 1, 2, 5, 17, 40):
            A, B, C, fin = abc_de_tramo(n0, k, s)
            if A == 0:
                if C != 0:
                    fallos.append("A=0 pero C!=0: s=%d n0=%d k=%d" % (s, n0, k))
            else:
                if s == +1 and not C > 0:
                    fallos.append("C<=0 con A>=1 en 3n+1: n0=%d k=%d" % (n0, k))
                if s == -1 and not C < 0:
                    fallos.append("C>=0 con A>=1 en 3n-1: n0=%d k=%d" % (n0, k))
            casos += 1
print("    %d tramos: C=0 exactamente cuando A=0; C>0 (s=+1) y C<0 (s=-1) cuando A>=1" % casos)
print("    borde k=0: A=B=C=0, identidad 1*n0 = 1*n0 + 0, degenerado y excluido del enunciado")
print("    (un ciclo de verdad tiene A>=1: solo con divisiones n/2 no se vuelve al inicio)")

# ---- comprobacion 6: mismos (A,B,C) con el mapa del atajo ----
print("")
print("[6] control de mapa: el atajo da los mismos (A,B,C) por vuelta de ciclo:")
def abc_atajo(n0, s):
    # una vuelta de ciclo con el mapa del atajo: par n/2, impar (3n+s)/2
    A = 0; B = 0; C = 0
    actual = n0
    while True:
        if actual % 2 == 0:
            actual //= 2
            B += 1
        else:
            C = 3 * C + s * (2 ** B)
            actual = 3 * actual + s
            A += 1
            actual //= 2
            B += 1
        if (2 ** B) * actual != (3 ** A) * n0 + C:
            fallos.append("invariante atajo roto: s=%d n0=%d" % (s, n0))
        if actual == n0:
            return A, B, C
for s, n0, A, B, C in resultados:
    Aa, Ba, Ca = abc_atajo(n0, s)
    igual = (Aa, Ba, Ca) == (A, B, C)
    if not igual:
        fallos.append("atajo difiere del clasico: s=%d n0=%d" % (s, n0))
    print("    s=%+d min=%-3d atajo (A,B,C)=(%d,%d,%d) %s clasico" %
          (s, n0, Aa, Ba, Ca, "==" if igual else "!="))

# ---- veredicto ----
print("")
if fallos:
    for f in fallos:
        print("FALLO: " + f)
    raise SystemExit("A61: FALLOS = %d" % len(fallos))
print("A61: 0 fallos. El enunciado se sostiene en todos los ciclos alcanzables")
print("desde 1..%d, en una, dos y tres vueltas, con comparacion entera exacta." % TOPE)
