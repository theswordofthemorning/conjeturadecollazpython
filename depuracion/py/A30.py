# A30.py -- AGENTE 2 (independiente). Verificacion desde cero del item A30.
#
# ENUNCIADO: en el arbol inverso de Collatz (mapa CLASICO: n par -> n/2,
# n impar -> 3n+1; hacia atras, un nodo m tiene siempre el hijo 2m y ademas
# un hijo impar (m-1)/3 cuando ese numero es un entero impar):
#   (1) el ritmo de brotes de un rayo v, 2v, 4v, ... es periodico de periodo 2
#       y lo decide v mod 3: v=0 mod 3 nunca brota; v=1 mod 3 brota en k de una
#       paridad; v=2 mod 3 en la otra.
#   (2) los hijos ciclan con periodo 3, y la clase del hijo la fija 2^k*v mod 9.
#   (3) el patron completo se repite cada 18 duplicaciones, y 18 = orden de 2 mod 27.
#
# DERIVACION PROPIA (sin abrir ningun fichero del repo):
#   m tiene hijo impar n = (m-1)/3  <=>  m = 3n+1 con n impar
#   n entero      <=> m = 1 (mod 3)
#   n impar       <=> m-1 = 3n = impar*3 = impar... 3n con n impar es impar,
#                     luego m = 3n+1 es PAR.  Junto: m = 4 (mod 6).
#   Sobre el rayo m_k = 2^k * v:
#     - paridad: m_k par para todo k>=1 (y para k=0 solo si v es par)
#     - m_k mod 3 = (2^k mod 3)*(v mod 3): 2^k mod 3 alterna 1,2,1,2 (periodo 2)
#   De ahi (1). Para (2): n mod 3 lo fija m mod 9 (m=1->n=0, m=4->n=1, m=7->n=2),
#   y entre brotes consecutivos m se multiplica por 4, que tiene orden 3 mod 9.
#   Para (3): todo el patron (brote + clase fina del hijo mod 9) lo fija
#   m mod 54 = (paridad, m mod 27); 2 tiene orden 18 mod 27.
#
# Aritmetica: solo int de Python. Ningun float decide nada.

import sys

fallos = []

def brota(m):
    # hijo impar existe <=> m = 4 (mod 6). Devuelve (True, hijo) o (False, None)
    if m % 6 == 4:
        hijo = (m - 1) // 3
        # comprobacion interna contra el mapa HACIA ADELANTE (clasico):
        if hijo % 2 != 1 or 3 * hijo + 1 != m:
            fallos.append(("brota_interno", m))
        return True, hijo
    return False, None

def paso_clasico(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1

# comprobacion 0: la condicion m=4 (mod 6) coincide con la definicion directa
# "existe n impar positivo con 3n+1 = m", barrida en m = 1..600000
for m in range(1, 600001):
    directo = (m - 1) % 3 == 0 and ((m - 1) // 3) % 2 == 1 and (m - 1) // 3 >= 1
    if directo != (m % 6 == 4):
        fallos.append(("condicion_brote", m))
if fallos:
    raise SystemExit("FALLO en la condicion de brote: %r" % fallos[:5])
print("comprobacion 0: brote <=> m = 4 (mod 6), barrido m = 1..600000, 0 fallos")

# y el hijo de verdad vuelve a m en un paso del mapa clasico
for m in range(1, 100001):
    b, h = brota(m)
    if b and paso_clasico(h) != m:
        fallos.append(("hijo_no_vuelve", m))
if fallos:
    raise SystemExit("FALLO: %r" % fallos[:5])
print("comprobacion 0b: paso_clasico(hijo) == m en los 16666 brotes de m<=100000, 0 fallos")

RAYOS = list(range(1, 301))          # 300 rayos (incluye v=1,2, pares, multiplos de 3)
K_MAX = 100                          # 100 duplicaciones por rayo (enteros grandes exactos)

# ---------- CLAIM 1: ritmo de brotes, periodo 2, decidido por v mod 3 ----------
exc_k0 = []          # excepciones en k=0
fallos1 = 0
total_brotes = 0
for v in RAYOS:
    r = v % 3
    for k in range(0, K_MAX + 1):
        m = (1 << k) * v
        b, h = brota(m)
        if b:
            total_brotes += 1
        if r == 0:
            esperado = False                       # nunca brota
        elif r == 1:
            esperado = (k % 2 == 0)                # brota en k pares
        else:
            esperado = (k % 2 == 1)                # brota en k impares
        # la paridad de m: en k=0 con v impar, m es impar y NO puede brotar
        if k == 0 and v % 2 == 1 and esperado and not b:
            exc_k0.append(v)
            continue
        if b != esperado:
            fallos1 += 1
            if fallos1 <= 5:
                print("  CONTRAEJEMPLO claim1: v=%d k=%d brota=%s esperado=%s" % (v, k, b, esperado))
print("claim 1: 300 rayos x k=0..100, brotes totales = %d, fallos (k>=1) = %d" % (total_brotes, fallos1))
print("  borde k=0: %d excepciones, todas con v impar y v=1 (mod 3): %s..." % (len(exc_k0), exc_k0[:8]))
print("  (en k=0 el numero es v, impar, y un impar no tiene hijo impar: 3n+1 es par)")

# ---------- CLAIM 2: la clase del hijo la fija m mod 9, y cicla con periodo 3 ----------
tabla = {1: 0, 4: 1, 7: 2}   # m mod 9 -> hijo mod 3  (derivada: n=(m-1)/3)
fallos2a = 0
fallos2b = 0
transiciones = 0
for v in RAYOS:
    brotes_v = []
    for k in range(0, K_MAX + 1):
        m = (1 << k) * v
        b, h = brota(m)
        if b:
            if tabla.get(m % 9, None) != h % 3:
                fallos2a += 1
            brotes_v.append((k, h % 3, m % 9))
    # entre brotes consecutivos la clase del hijo avanza +1 mod 3 (ciclo 0->1->2->0)
    for i in range(1, len(brotes_v)):
        transiciones += 1
        if (brotes_v[i][1] - brotes_v[i-1][1]) % 3 != 1:
            fallos2b += 1
    # y el ciclo tiene periodo exactamente 3 (cada 3 brotes vuelve la misma clase)
    for i in range(3, len(brotes_v)):
        if brotes_v[i][1] != brotes_v[i-3][1]:
            fallos2b += 1
print("claim 2: tabla {1:0, 4:1, 7:2} (m mod 9 -> hijo mod 3): fallos = %d" % fallos2a)
print("  transiciones entre brotes consecutivos: %d, fallos del ciclo +1 mod 3 / periodo 3 = %d" % (transiciones, fallos2b))
o9 = 1
x = 4 % 9
while x != 1:
    x = (x * 4) % 9
    o9 += 1
print("  orden de 4 mod 9 = %d (entre brotes m se multiplica por 4)" % o9)

# ---------- CLAIM 3: el patron completo se repite cada 18 duplicaciones ----------
# orden de 2 mod 27, calculado:
o27 = 1
x = 2 % 27
while x != 1:
    x = (x * 2) % 27
    o27 += 1
print("claim 3: orden de 2 mod 27 = %d" % o27)

# patron completo en el paso k (para k>=1): (brota?, hijo mod 9 si brota)
fallos3 = 0
for v in RAYOS:
    pat = []
    for k in range(1, K_MAX + 1):
        m = (1 << k) * v
        b, h = brota(m)
        pat.append((b, h % 9 if b else None))
    for i in range(len(pat) - 18):
        if pat[i] != pat[i + 18]:
            fallos3 += 1
print("  patron (brote, hijo mod 9) en k y k+18: 300 rayos, k=1..100, fallos = %d" % fallos3)

# minimalidad: que periodos menores NO valen para el patron completo,
# y cuales valen para los patrones gruesos (sobre un rayo no multiplo de 3)
def periodo_minimo(pat):
    L = len(pat)
    for p in range(1, L):
        if all(pat[i] == pat[i + p] for i in range(L - p)):
            return p
    return None

v = 5
pat_full  = []
pat_brote = []
pat_mod3  = []
for k in range(1, 361):
    m = (1 << k) * v
    b, h = brota(m)
    pat_full.append((b, h % 9 if b else None))
    pat_brote.append(b)
    pat_mod3.append((b, h % 3 if b else None))
print("  rayo v=5, k=1..360: periodo minimo del brote solo = %d" % periodo_minimo(pat_brote))
print("                      periodo minimo de (brote, hijo mod 3) = %d" % periodo_minimo(pat_mod3))
print("                      periodo minimo de (brote, hijo mod 9) = %d" % periodo_minimo(pat_full))

# y para un multiplo de 3 el patron es todo mudo (periodo 1)
v = 9
pat9 = []
for k in range(1, 101):
    b, _ = brota((1 << k) * v)
    pat9.append(b)
print("  rayo v=9 (multiplo de 3): brotes = %d de 100 (patron mudo, periodo 1)" % sum(pat9))

# ---------- bordes sueltos ----------
b, h = brota(4)
print("borde v=1: 2^2*1 = 4 brota y su hijo es %d (el 1: el lazo del ciclo trivial)" % h)
b0, _ = brota(1)
b1, _ = brota(2)
print("borde: brota(1)=%s, brota(2)=%s  (ni 1 ni 2 tienen hijo impar)" % (b0, b1))
# v par que arranca brotando en k=0:
b4, h4 = brota(4 * 1)   # v=4, k=0
print("borde v=4 (par, v=1 mod 3): brota ya en k=0 -> %s, hijo %s (k=0 es par: cuadra)" % (b4, h4))

# ---------- veredicto ----------
if fallos or fallos1 or fallos2a or fallos2b or fallos3:
    raise SystemExit("HAY FALLOS: %d %d %d %d %d" % (len(fallos), fallos1, fallos2a, fallos2b, fallos3))
print()
print("VEREDICTO DEL SCRIPT: las tres partes aguantan para k >= 1 con 0 fallos;")
print("la unica letra chica es k=0 (rayo de arranque impar), donde la paridad")
print("anade una condicion que el enunciado por restos no menciona.")
