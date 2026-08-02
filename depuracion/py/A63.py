# A63 - verificacion independiente (agente 2, Python desde cero)
#
# ENUNCIADO: el unico ciclo positivo, escrito con la identidad del repo,
#            es 2^2 = 3^1 + 1, o sea 4 = 3 + 1.
# NOTAS BASE: A=1, B=2, C=1. De los 95 candidatos enteros positivos que
#            aparecieron (pares de la trayectoria del 221), los 95 ciclan
#            de verdad y son n en {1,2,4} dando 1, 2 o 3 vueltas.
#
# MAPA: CLASICO (par -> n/2, impar -> 3n+1). La identidad con A y B contados
#       por separado solo tiene sentido en el clasico. Lo derivo yo:
#
#   Invariante: 2^B * s_actual = 3^A * s_inicial + C
#   arranque: A=B=C=0.
#   paso par  (s -> s/2):    s = 2*s'  =>  2^(B+1)*s' = 3^A*s0 + C
#                            => B += 1, C igual.
#   paso impar (s -> 3s+1):  s = (s'-1)/3 => 2^B*(s'-1)/3 = 3^A*s0 + C
#                            => 2^B*s' = 3^(A+1)*s0 + 3C + 2^B
#                            => A += 1, C -> 3C + 2^B.
#
#   Ciclo: si s vuelve a si mismo tras el tramo, 2^B*x = 3^A*x + C, o sea
#          x = C / (2^B - 3^A). Con C >= 0 siempre, un ciclo positivo exige
#          2^B > 3^A.
#
# Todo con int exacto. Ningun float decide nada.

import sys

def paso(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1

fallos = 0

# ---------- 1. trayectoria del 221 y la identidad en TODOS los pares ----------
tray = [221]
while tray[-1] != 1:
    tray.append(paso(tray[-1]))

print("largo de la trayectoria del 221 (numeros):", len(tray))
n_pares = len(tray) * (len(tray) - 1) // 2
print("pares (i<j):", n_pares)

# prefijos incrementales desde cada i seria O(L^2); hacemos exactamente eso.
identidad_fallos = 0
candidatos_pos = []   # (i, j, A, B, C, x)
candidatos_neg = 0
for i in range(len(tray)):
    A = B = C = 0
    for j in range(i + 1, len(tray)):
        s = tray[j - 1]
        if s % 2 == 0:
            B += 1
        else:
            C = 3 * C + 2 ** B
            A += 1
        # identidad exacta
        if 2 ** B * tray[j] != 3 ** A * tray[i] + C:
            identidad_fallos += 1
        # candidato a ciclo: x = C / (2^B - 3^A)
        den = 2 ** B - 3 ** A
        if den != 0:
            if C % abs(den) == 0:
                x = C // den
                if x > 0:
                    candidatos_pos.append((i, j, A, B, C, x))
                elif x < 0:
                    candidatos_neg += 1
        else:
            # den = 0 solo si A=B=0, imposible con j>i
            pass

print("identidad 2^B*s[j] = 3^A*s[i] + C en los", n_pares, "pares: fallos =", identidad_fallos)
if identidad_fallos:
    raise SystemExit("FALLO: la identidad no se cumple")

# ---------- 2. los candidatos positivos: cuantos son y si ciclan ----------
print("candidatos enteros POSITIVOS:", len(candidatos_pos))
valores = sorted(set(x for (_, _, _, _, _, x) in candidatos_pos))
print("valores distintos de los candidatos:", valores)

impostores = 0
vueltas_vistas = set()
for (i, j, A, B, C, x) in candidatos_pos:
    largo = j - i
    v = x
    for _ in range(largo):
        v = paso(v)
    if v != x:
        impostores += 1
    else:
        vueltas_vistas.add((x, largo))

print("impostores (candidato que NO cicla):", impostores)
print("pares (x, largo_del_tramo) que ciclan:", sorted(vueltas_vistas))
largos = sorted(set(l for (_, l) in vueltas_vistas))
print("largos de tramo vistos:", largos, "-> vueltas:", [l // 3 for l in largos])
if impostores:
    raise SystemExit("FALLO: hay impostores")
if not set(valores) <= {1, 2, 4}:
    raise SystemExit("FALLO: candidato fuera de {1,2,4}")

# ---------- 3. la escritura canonica del ciclo: empezar en 1 ----------
# 1 -> 4 -> 2 -> 1
A = B = C = 0
s = 1
for _ in range(3):
    if s % 2 == 0:
        B += 1
    else:
        C = 3 * C + 2 ** B
        A += 1
    s = paso(s)
print("ciclo desde 1: vuelve a", s, "con A =", A, ", B =", B, ", C =", C)
if not (s == 1 and A == 1 and B == 2 and C == 1):
    raise SystemExit("FALLO: el ciclo trivial no da (A,B,C) = (1,2,1)")
print("identidad del ciclo: 2^2 =", 2 ** 2, " y 3^1 + 1 =", 3 ** 1 + 1,
      "-> 4 = 3 + 1:", 2 ** 2 == 3 ** 1 + 1)

# borde: la (A,B,C) depende del punto de arranque del ciclo
for arranque in (4, 2):
    A = B = C = 0
    s = arranque
    for _ in range(3):
        if s % 2 == 0:
            B += 1
        else:
            C = 3 * C + 2 ** B
            A += 1
        s = paso(s)
    print("mismo ciclo desde", arranque, "-> (A,B,C) =", (A, B, C),
          "; identidad:", 2 ** B, "*", arranque, "=", 3 ** A, "*", arranque, "+", C,
          "->", 2 ** B * arranque == 3 ** A * arranque + C)

# ---------- 4. unicidad EN RANGO: ningun otro ciclo con minimo <= LIMITE ----------
LIMITE = 10 ** 6
# induccion ascendente: si todo m < n llega a 1, basta iterar n hasta bajar de n.
# un ciclo nuevo con minimo x <= LIMITE haria que x nunca bajara de si mismo
# ni llegara a 1: lo detectariamos por no terminar. Ponemos tope de pasos alto
# y si se alcanza, se declara.
TOPE = 100000
sin_clasificar = 0
for n in range(2, LIMITE + 1):
    v = n
    pasos = 0
    while True:
        v = paso(v)
        pasos += 1
        if v < n:
            break              # bajo de n: por induccion ascendente, llega a 1
        if v == n:
            # volvio a n sin haber bajado nunca: ciclo con minimo n
            print("CICLO detectado con minimo", n)
            sin_clasificar += 1
            break
        if pasos > TOPE:
            print("SIN CLASIFICAR:", n)
            sin_clasificar += 1
            break

print("barrido de unicidad 2 ..", LIMITE, ": numeros que no bajan =", sin_clasificar)
if sin_clasificar:
    raise SystemExit("FALLO: aparecio un ciclo o un no-clasificado en el rango")

# ---------- 5. bordes de la ecuacion de ciclo ----------
# A=0 (tramo solo de divisiones): C=0 y x = 0/(2^B-1) = 0, nunca positivo.
# 2^B < 3^A: denominador negativo, C>0 => x negativo (lado 3n-1 / negativos).
print("candidatos con x negativo (lado 2^B < 3^A):", candidatos_neg)
# n=1: es el propio ciclo. n=2, n=4: mismos. n par corriente (n=6): no cicla.
v = 6
for _ in range(20):
    v = paso(v)
print("n = 6 tras 20 pasos:", v, "(no vuelve a 6: correcto, llego al ciclo trivial)")

print()
print("TODO OK")
