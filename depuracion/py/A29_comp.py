# Comparador A29: comprobaciones propias, enteros exactos, sin abrir el repo.

def T(n):  # atajo
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2

def Tc(n):  # clasico
    return n // 2 if n % 2 == 0 else 3 * n + 1

fallos = 0

# 1) caso comun de los dos agentes: 7 (k=3) sube 3 veces, impar en cada paso
x = 7
tray = [x]
for _ in range(3):
    tray.append(T(tray[-1]))
print("tray 7 (atajo):", tray)
if tray != [7, 11, 17, 26]:
    fallos += 1
for j in range(3):
    if not (tray[j] % 2 == 1 and tray[j + 1] > tray[j]):
        fallos += 1

# caso comun baja: 8 (k=3)
x = 8
tray = [x]
for _ in range(3):
    tray.append(T(tray[-1]))
print("tray 8 (atajo):", tray)
if tray != [8, 4, 2, 1]:
    fallos += 1

# 2) contraejemplo del mapa clasico: n=3, k=2 (3 = 3 mod 4)
print("tray 3 (clasico):", [3, Tc(3), Tc(Tc(3))])
if not (Tc(Tc(3)) < Tc(3)):
    fallos += 1  # si NO bajara, el clasico no seria contraejemplo

# 3) barrido propio, distinto de los rangos de los agentes (limite NO redondo):
#    k=1..11, m=0..36 para sube (n = m*2^k + 2^k - 1), m=1..37 para baja
for k in range(1, 12):
    for m in range(0, 37):
        n = m * 2**k + 2**k - 1
        x = n
        for j in range(k):
            if x % 2 != 1 or T(x) <= x:
                fallos += 1
                print("FALLO sube", k, m, j, x)
            x = T(x)
    for m in range(1, 38):
        n = m * 2**k
        x = n
        for j in range(k):
            if x % 2 != 0 or T(x) >= x:
                fallos += 1
                print("FALLO baja", k, m, j, x)
            x = T(x)

# 4) el arbitraje del off-by-one: cuantos impares seguidos da 2^K - 1
#    formula cerrada T^j(2^K-1) = 3^j * 2^(K-j) - 1 contra iteracion cruda,
#    en K chicos, y conteo directo en K = 4000.
for K in (3, 5, 10):
    x = 2**K - 1
    j = 0
    while x % 2 == 1:
        # cruce con la forma cerrada mientras j <= K
        if j <= K and x != 3**j * 2**(K - j) - 1:
            fallos += 1
            print("FALLO forma cerrada", K, j)
        x = T(x)
        j += 1
    print(f"2^{K}-1: {j} impares seguidos")
    if j != K:
        fallos += 1

x = 2**4000 - 1
j = 0
while x % 2 == 1:
    x = T(x)
    j += 1
print("2^4000-1:", j, "impares seguidos (la nota dice 3999)")
if j != 4000:
    fallos += 1

# 5) borde n=0: esta en la clase 0 mod 2^k y NO baja
print("T(0) =", T(0), "(no baja: la mitad 'baja' exige n >= 1)")
if T(0) != 0:
    fallos += 1

# 6) el reciproco NO lo afirma la ficha, pero es el Lema 8 citado como fuente:
#    k impares seguidos al arranque => n = 2^k - 1 (mod 2^k). Muestreo propio.
for n in range(1, 3001):
    x = n
    j = 0
    while x % 2 == 1 and j < 12:
        x = T(x)
        j += 1
    # j = numero de impares seguidos al arranque (tope 12)
    for k in range(1, min(j, 11) + 1):
        if n % 2**k != 2**k - 1:
            fallos += 1
            print("FALLO reciproco", n, k)

print("FALLOS TOTALES:", fallos)
