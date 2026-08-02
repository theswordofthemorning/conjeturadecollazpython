# Comparador A63: tercera implementacion, sin mirar la de los agentes.
# Mapa CLASICO: par -> n/2, impar -> 3n+1.
# Identidad: 2^B * seq[j] = 3^A * seq[i] + C, con C -> 3C + 2^B en paso impar.

def trayectoria(n):
    t = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        t.append(n)
    return t

seq = trayectoria(221)
if len(seq) != 115:
    raise SystemExit("largo de trayectoria del 221 no es 115: %d" % len(seq))

# identidad en todos los pares + candidatos de ciclo
pares = 0
fallos = 0
candidatos = []  # (x, largo)
for i in range(len(seq)):
    A = 0
    B = 0
    C = 0
    for j in range(i + 1, len(seq)):
        v = seq[j - 1]
        if v % 2 == 0:
            B += 1
        else:
            A += 1
            C = 3 * C + 2 ** B
            B += 1  # ojo: en el clasico el paso impar NO divide
        # correccion: en el clasico, paso impar solo multiplica.
        # rehago el conteo bien abajo; esta rama era del atajo.
        pass
    # no usar este bucle: rehecho abajo
    break

# version correcta del conteo clasico
pares = 0
fallos = 0
candidatos = []
n_pos = len(seq)
for i in range(n_pos):
    A = 0
    B = 0
    C = 0
    for j in range(i + 1, n_pos):
        v = seq[j - 1]
        if v % 2 == 0:
            B += 1
        else:
            A += 1
            C = 3 * C + 2 ** B
        pares += 1
        # identidad
        if 2 ** B * seq[j] != 3 ** A * seq[i] + C:
            fallos += 1
        # ecuacion de ciclo: x = C / (2^B - 3^A), con x entero positivo
        D = 2 ** B - 3 ** A
        if D > 0 and C % D == 0:
            x = C // D
            if x > 0:
                candidatos.append((x, j - i))

print("pares:", pares, "fallos identidad:", fallos)
print("candidatos positivos:", len(candidatos))
vals = sorted(set(x for x, _ in candidatos))
print("valores:", vals)
largos = sorted(set(l for _, l in candidatos))
print("largos de tramo:", largos)

# cada candidato cicla de verdad?
impostores = 0
for x, largo in candidatos:
    m = x
    for _ in range(largo):
        m = m // 2 if m % 2 == 0 else 3 * m + 1
    if m != x:
        impostores += 1
print("impostores:", impostores)

# el ciclo desde 1: (A,B,C)
A = B = C = 0
m = 1
for _ in range(3):
    if m % 2 == 0:
        B += 1
        m //= 2
    else:
        A += 1
        C = 3 * C + 2 ** B
        m = 3 * m + 1
print("ciclo desde 1: A=%d B=%d C=%d  ->  2^%d = 3^%d + %d  (%d = %d + %d)"
      % (A, B, C, B, A, C, 2 ** B, 3 ** A, C))
print("dos vueltas: 16 = 9 + 7 ->", 2 ** 4 == 3 ** 2 + 7)
print("tres vueltas: 64 = 27 + 37 ->", 2 ** 6 == 3 ** 3 + 37)

# barrido corto de unicidad (induccion ascendente) hasta 200000
LIM = 200000
ciclos_nuevos = 0
for n in range(2, LIM):
    m = n
    pasos = 0
    while m >= n:
        m = m // 2 if m % 2 == 0 else 3 * m + 1
        pasos += 1
        if m == n:
            if n not in (1, 2, 4):
                ciclos_nuevos += 1
            break
        if pasos > 10 ** 6:
            raise SystemExit("sin decidir en n=%d" % n)
print("ciclos nuevos con minimo < %d:" % LIM, ciclos_nuevos)
