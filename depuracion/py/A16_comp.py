# Comparador A16: arbitraje independiente con enteros exactos.
# No abre ningun fichero del repo.

def T(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1

fallos = 0

# 1) La identidad de UN paso, exhaustiva k=1..14, n impar, 1 <= n < 2^k
total1 = 0
for k in range(1, 15):
    for n in range(1, 2**k, 2):
        total1 += 1
        if T(2**k - n) != 3 * 2**k + 2 - T(n):
            fallos += 1
print("paso 1 exhaustivo:", total1, "casos,", fallos, "fallos")

# 2) Caso comun de los dos agentes: k=5, n=13
k, n = 5, 13
print("caso comun k=5,n=13:", T(2**k - n), "==", 3 * 2**k + 2 - T(n))

# 3) k=8, n=221 (caso del agente 1)
k, n = 8, 221
print("caso k=8,n=221:", T(2**k - n), "==", 3 * 2**k + 2 - T(n))

# 4) n par: contraejemplo del agente 1 (n=2, k=2)
print("n par k=2,n=2:", T(4 - 2), "vs", 3 * 4 + 2 - T(2), "-> distinto:", T(2) != 3 * 4 + 2 - T(2))

# 5) k=0, n=1: T(2^0-1)=T(0)=0 vs 3+2-T(1)=1
print("k=0,n=1:", T(0), "vs", 3 * 1 + 2 - T(1))

# 6) EL ARBITRAJE: segundo paso CLASICO. Agente 1 dice que no itera;
#    agente 2 dice que si, con constante 3*2^(k-1)+1.
def Tj(n, j):
    for _ in range(j):
        n = T(n)
    return n

f2 = 0
tot2 = 0
for k in range(2, 13):
    c2 = 3 * 2**(k - 1) + 1
    for n in range(1, 2**k, 2):
        tot2 += 1
        if Tj(2**k - n, 2) != c2 - Tj(n, 2):
            f2 += 1
print("segundo paso clasico con c=3*2^(k-1)+1:", tot2, "casos,", f2, "fallos")

# 6b) El contraejemplo del agente 1 al "segundo paso", releido:
k, n = 5, 13
print("agente1 n=13,k=5: T^2(19) =", Tj(19, 2), "; 98 - T^2(13) =", 98 - Tj(13, 2),
      "; con c2=49: 49 - T^2(13) =", 49 - Tj(13, 2))

# 7) tercer paso clasico: cuantos valores toma T^3(esp)+T^3(n)?
for k in (6, 8, 10):
    vals = set()
    for n in range(1, 2**k, 2):
        vals.add(Tj(2**k - n, 3) + Tj(n, 3))
    print(f"k={k}: T^3(esp)+T^3(n) toma {len(vals)} valores (2^(k-2) = {2**(k-2)})")

# 8) atajo: la constante 3*2^k+2 NO debe cuadrar; 3*2^(k-1)+1 si
def U(n):
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2

fa_mal = 0
fa_bien = 0
tota = 0
for k in range(2, 12):
    for n in range(1, 2**k, 2):
        tota += 1
        if U(2**k - n) != 3 * 2**k + 2 - U(n):
            fa_mal += 1
        if U(2**k - n) != 3 * 2**(k - 1) + 1 - U(n):
            fa_bien += 1
print("atajo con 3*2^k+2:", fa_mal, "fallos de", tota, "| atajo con 3*2^(k-1)+1:", fa_bien, "fallos")

# 9) algebra del segundo paso, simbolica a mano:
#    n impar -> T(n)=3n+1 par -> T^2(n)=(3n+1)/2
#    esp=2^k-n impar (k>=1, n impar, n<2^k) -> T^2(esp)=(3(2^k-n)+1)/2
#    suma = (3*2^k+2)/2 = 3*2^(k-1)+1. Exacto siempre que k>=1... pero /2 exige 3n+1 par: siempre.
# comprobacion del borde k=1: n=1, esp=1: T^2(1)+T^2(1) = 2+2 = 4 = 3*1+1 OK
print("k=1,n=1: T^2(1)+T^2(1) =", Tj(1, 2) + Tj(1, 2), "= 3*2^0+1 =", 3 * 1 + 1)
