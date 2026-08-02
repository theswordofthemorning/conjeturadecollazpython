# A1_comp.py - COMPARADOR (agente 3). Tercera implementacion, sin la recurrencia.
#
# Los dos agentes usan la recurrencia C -> 3C + 2^b. Yo NO: calculo C con la
# FORMA CERRADA (suma explicita sobre los pasos impares del tramo):
#
#   C(i,j) = SUMA sobre cada paso impar s del tramo de
#              3^(impares DESPUES de s en el tramo) * 2^(pares ANTES de s)
#
# y compruebo que  2^B*seq[j] - 3^A*seq[i]  ==  esa suma, con enteros exactos.
# Si la recurrencia de los dos agentes fuera una mala copia compartida, esta
# suma no coincidiria con la resta directa.

def paso(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1

def tray(n, extra=0):
    s = [n]
    while s[-1] != 1:
        s.append(paso(s[-1]))
    for _ in range(extra):
        s.append(paso(s[-1]))
    return s

def C_cerrada(seq, i, j):
    # paridades de las posiciones i..j-1 (las que ejecutan paso)
    par = [seq[t] % 2 for t in range(i, j)]  # 1 = impar
    A = sum(par)
    B = len(par) - A
    C = 0
    pares_antes = 0
    impares_vistos = 0
    for t, p in enumerate(par):
        if p == 1:
            impares_vistos += 1
            impares_despues = A - impares_vistos
            C += (3 ** impares_despues) * (2 ** pares_antes)
        else:
            pares_antes += 1
    return A, B, C

fallos = 0
probados = 0
for n in list(range(1, 120)) + [221, 27, 703, (1 << 40) + 1]:
    seq = tray(n, extra=5)
    L = len(seq)
    for i in range(L - 1):
        for j in range(i + 1, L):
            A, B, C = C_cerrada(seq, i, j)
            probados += 1
            if (2 ** B) * seq[j] != (3 ** A) * seq[i] + C:
                fallos += 1
                if fallos < 4:
                    print("FALLO", n, i, j, A, B, C)
print("forma cerrada vs identidad: %d pares, %d fallos" % (probados, fallos))

# caso comun de los dos agentes: el 221 entero
seq = tray(221)
L = len(seq)
A, B, C = C_cerrada(seq, 0, L - 1)
print("221: posiciones=%d pares=%d A=%d B=%d" % (L, L * (L - 1) // 2, A, B))
print("221: C(cerrada)=%d  y  2^73 - 3^41*221 = %d  iguales: %s"
      % (C, 2 ** 73 - 3 ** 41 * 221, C == 2 ** 73 - 3 ** 41 * 221))

# ciclo trivial como par: 1 -> 4 -> 2 -> 1
seq1 = tray(1, extra=3)
A, B, C = C_cerrada(seq1, 0, 3)
print("ciclo: A=%d B=%d C=%d  (4 = 3 + 1: %s)" % (A, B, C, 2 ** B * 1 == 3 ** A * 1 + C))

# la lectura alternativa (mala) del enunciado: "2^B" con el B TOTAL del tramo
# en vez del acumulado. Compruebo que esa lectura FALLA, o sea que la lectura
# compartida por los dos agentes no es una eleccion arbitraria: es la unica
# que hace verdadera la identidad.
def C_mala(seq, i, j):
    par = [seq[t] % 2 for t in range(i, j)]
    A = sum(par)
    B = len(par) - A
    C = 0
    for p in par:
        if p == 1:
            C = 3 * C + 2 ** B   # B total, lectura equivocada
    return A, B, C

malos = 0
tot = 0
for n in (7, 27, 221):
    seq = tray(n)
    for i in range(len(seq) - 1):
        for j in range(i + 1, len(seq)):
            A, B, C = C_mala(seq, i, j)
            tot += 1
            if (2 ** B) * seq[j] != (3 ** A) * seq[i] + C:
                malos += 1
print("lectura 'B total': falla en %d de %d pares (debe fallar en casi todos)" % (malos, tot))

if fallos:
    raise SystemExit("COMPARADOR: DISCREPANCIA")
print("COMPARADOR: la tercera via (forma cerrada) coincide. 0 fallos.")
