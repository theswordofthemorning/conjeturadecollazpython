# A19_comp - comprobacion del COMPARADOR, tercera implementacion.
# No copia nada de A19.py ni de A19.lean: patron como ENTERO con
# aritmetica de bits (convencion del Lean: bit i = paridad del iterado i),
# y de ahi se derivan las cadenas para cruzar con la convencion de Python.

def T(n): return n // 2 if n % 2 == 0 else (3 * n + 1) // 2
def C(n): return n // 2 if n % 2 == 0 else 3 * n + 1

def pat_int(f, n, k):
    p = 0
    for i in range(k):
        p |= (n & 1) << i
        n = f(n)
    return p

fallos = 0

# caso comun 1: el ancla del agente 1. pat 6 27 = 59 y trayectoria 27,41,62,31,47,71
tray = [27]
for _ in range(5): tray.append(T(tray[-1]))
if tray != [27, 41, 62, 31, 47, 71]:
    print("FALLO trayectoria 27:", tray); fallos += 1
if pat_int(T, 27, 6) != 59:
    print("FALLO pat(6,27) =", pat_int(T, 27, 6)); fallos += 1
# cruce con la convencion de cadenas del agente 2: 59 = 0b111011 -> IIPIII
cadena = ''.join('I' if (59 >> i) & 1 else 'P' for i in range(6))
if cadena != 'IIPIII':
    print("FALLO cruce de convenciones:", cadena); fallos += 1

# caso comun 2: extremos pat(6,0)=0, pat(6,63)=63 (agente 1) = P^6, I^6 (agente 2)
if pat_int(T, 0, 6) != 0 or pat_int(T, 63, 6) != 63:
    print("FALLO extremos k=6"); fallos += 1

# caso comun 3: biyeccion exhaustiva, incluida k=6 (ancla Lean) y k=12 (tope agente 2)
for k in range(0, 13):
    M = 2 ** k
    vistos = set(pat_int(T, r, k) for r in range(M))
    if len(vistos) != M or vistos != set(range(M)):
        print("FALLO biyeccion k =", k); fallos += 1
print("biyeccion atajo k=0..12: exhaustiva, imagen = [0,2^k) exacta ->", fallos, "fallos")

# caso comun 4: clasico. colision patC(2,1)=patC(2,3) (agente 1) = 'IP','IP' (agente 2)
if pat_int(C, 1, 2) != pat_int(C, 3, 2):
    print("FALLO: no colisionan 1 y 3 en k=2"); fallos += 1

# caso comun 5: conteo Fibonacci del clasico, k=0..13 (cubre el 1..7 del Lean)
fibs = [0, 1]
while len(fibs) < 20: fibs.append(fibs[-1] + fibs[-2])
for k in range(0, 14):
    M = 2 ** k
    alcanzados = set(pat_int(C, r, k) for r in range(M))
    if len(alcanzados) != fibs[k + 2]:
        print("FALLO fib k =", k, len(alcanzados), fibs[k + 2]); fallos += 1
    # ningun alcanzado con dos impares seguidos (bits 11 adyacentes)
    for p in alcanzados:
        if p & (p >> 1):
            print("FALLO: patron con II, k =", k, bin(p)); fallos += 1; break
print("clasico k=0..13: |alcanzados| = F(k+2) y sin '11' adyacentes ->", fallos, "fallos")

# ataque propio: buena definicion con m NO redondos (el punto 8 de la lista:
# los agentes usaron m = 0,1,2,3,1000; pruebo m raros y grandes, y los dos mapas)
import random
random.seed(19)
for f in (T, C):
    for k in (5, 9, 13):
        M = 2 ** k
        for _ in range(400):
            r = random.randrange(M)
            m = random.choice([7, 13, 999983, 2**40 + 3, 3**25])
            if pat_int(f, r, k) != pat_int(f, r + m * M, k):
                print("FALLO clase_residual", f.__name__, k, r, m); fallos += 1
print("clase residual con m no redondos (7, 13, 999983, 2^40+3, 3^25) ->", fallos, "fallos")

if fallos:
    raise SystemExit("COMPARADOR: HUBO FALLOS")
print("COMPARADOR: 0 fallos en todo")
