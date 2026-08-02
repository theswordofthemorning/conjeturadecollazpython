# A5_comp - comprobacion del COMPARADOR, tercera implementacion.
# No comparte codigo con A5.py (cuenta A y B desde el vector de paridad y
# reconstruye Res por la identidad 2^B * 1 = 3^A * n + C, no por Fraction del
# cociente). Limite NO redondo a proposito: 131075 (incluye 2^17 y no acaba
# en potencia de 10 ni de 2).

LIMITE = 131075

def vector_paridad(n):
    # devuelve la lista de bits de paridad de la trayectoria clasica hasta el 1
    bits = []
    x = n
    while x != 1:
        b = x & 1
        bits.append(b)
        x = 3 * x + 1 if b else x >> 1
    return bits

fallos = []
iguales = []
for n in range(1, LIMITE + 1):
    bits = vector_paridad(n)
    A = sum(bits)
    B = len(bits) - A
    # identidad entera: 2^B = 3^A * n + C con C >= 0, y C = 0 sii A = 0
    # reconstruyo C paso a paso: C -> 3C + 2^(pares vistos hasta aqui) en impar
    C = 0
    pares = 0
    for b in bits:
        if b:
            C = 3 * C + 2 ** pares
        else:
            pares += 1
    lhs = 2 ** B
    rhs = 3 ** A * n + C
    if lhs != rhs:
        fallos.append(("identidad", n)); continue
    if C < 0 or lhs < 3 ** A * n:          # Res >= 1
        fallos.append(("cota", n))
    es_pot2 = (n & (n - 1)) == 0
    if (lhs == 3 ** A * n) != es_pot2:     # igualdad sii potencia de 2
        fallos.append(("igualdad", n))
    if (A == 0) != es_pot2:
        fallos.append(("A0", n))
    if lhs == 3 ** A * n:
        iguales.append(n)

print("barrido 1..%d: %d fallos" % (LIMITE, len(fallos)))
print("primeros fallos:", fallos[:5])
esperado = [2 ** m for m in range(18) if 2 ** m <= LIMITE]
print("eps=0 en:", iguales)
print("esperado :", esperado)
print("conjuntos iguales:", iguales == esperado, "(incluye 2^17 =", 2**17, ")")

# casos concretos que citan los dos agentes, recomprobados aqui
def AB(n):
    b = vector_paridad(n); return sum(b), len(b) - sum(b), len(b)

print("n=3  ->", AB(3),  "espera (2,5,7);  3^2*3=27 < 32=2^5:", 3**2*3 < 2**5)
print("n=7  ->", AB(7),  "espera (5,11,16); 3^5*7=1701 < 2048:", 3**5*7 < 2**11)
print("n=27 ->", AB(27), "espera (A,B,111)")
A27, B27, k27 = AB(27)
print("   3^A*27 < 2^B:", 3**A27*27 < 2**B27)
print("n=4  ->", AB(4),  "espera (0,2,2); 3^0*4 == 2^2:", 3**0*4 == 2**2)

# el matiz del agente 1: seguir MAS ALLA del primer 1 (n=4, k=5)
x = 4; A = B = 0
for _ in range(5):
    if x % 2 == 0: x //= 2; B += 1
    else: x = 3*x+1; A += 1
print("n=4 con k=5 -> llega a", x, "A =", A, "B =", B,
      "; 3^A*4 =", 3**A*4, "< 2^B =", 2**B, ":", 3**A*4 < 2**B)
