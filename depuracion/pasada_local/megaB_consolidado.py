# Re-medicion consolidada de los items pendientes SIN fichero propio (o con
# fichero de barrido caro que no se re-ejecuta). Un bloque por item, aritmetica
# exacta donde decide, y UNA linea "ITEM | dato" por resultado.
# Escrito desde cero: no copia implementaciones del repo.
from fractions import Fraction
import sqlite3, os

def clasico(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1

def atajo(n):
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2

def tray(n, paso, tope=10**7):
    t = [n]
    while t[-1] != 1 and len(t) < tope:
        t.append(paso(t[-1]))
    return t

def pasos_hasta_1(n):
    c = 0
    while n != 1:
        n = clasico(n); c += 1
    return c

# ---------- A76: identidad 2^B*seq[j] = 3^A*seq[i] + C en los pares del 221
# (clasico: en cada tramo A cuenta impares, B cuenta pares; C -> 3C + 2^B en los impares)
t221 = tray(221, clasico)
fallos = 0; pares = 0
for i in range(len(t221)):
    A = 0; B = 0; C = 0
    for j in range(i + 1, len(t221)):
        x = t221[j - 1]
        if x % 2 == 0:
            B += 1
        else:
            A += 1
            C = 3 * C + 2 ** B
        pares += 1
        if 2 ** B * t221[j] != 3 ** A * t221[i] + C:
            fallos += 1
print(f"A76 | {len(t221)} numeros del 221, {pares} pares, fallos={fallos}")

# ---------- A32: el arranque (patron de paridad k=6, ATAJO) lo decide n mod 64
t1276 = tray(1276, clasico)
numeros = sorted(set(t221) | set(t1276))
def patron(n, k):
    p = []
    for _ in range(k):
        p.append(n % 2); n = atajo(n)
    return tuple(p)
fallos = sum(1 for x in numeros if patron(x, 6) != patron(64 + (x % 64), 6))
print(f"A32 | numeros distintos 221+1276={len(numeros)} (221:{len(t221)}, 1276:{len(t1276)}), fallos malla k=6={fallos}")

# ---------- A38: equidistribucion exacta de los 2^k patrones (ATAJO), k=1..10
malo = None
for k in range(1, 11):
    vistos = {}
    for r in range(2 ** k):
        vistos.setdefault(patron(2 ** k + r, k), 0)
        vistos[patron(2 ** k + r, k)] += 1
    if len(vistos) != 2 ** k or set(vistos.values()) != {1}:
        malo = k; break
print(f"A38 | biyeccion resto-patron k=1..10: {'FALLA en k=' + str(malo) if malo else 'exacta (cada patron una vez)'}")

# ---------- A41: valuacion 2-adica media de 3n+1 en los impares de las trayectorias
suma = 0; cuenta = 0
for n in range(3, 100001, 2):
    m = n
    while m != 1:
        if m % 2 == 1:
            v = 0; x = 3 * m + 1
            while x % 2 == 0:
                v += 1; x //= 2
            suma += v; cuenta += 1
            m = 3 * m + 1
        else:
            m //= 2
print(f"A41 | valuacion media = {suma/cuenta:.5f} sobre {cuenta} saltos impares (impares 3..100000); esperado ~2 (medido repo: 1,99048)")

# ---------- A42: fraccion de pasos impares, clasico y atajo
def fracciones(n):
    a = b = 0; m = n
    while m != 1:
        if m % 2: a += 1
        m = clasico(m); b += 1
    return a, b
ta = tb = 0
for n in range(2, 100001):
    a, b = fracciones(n); ta += a; tb += b
fc = ta / tb                      # clasico: impares / pasos clasicos
fa = ta / (tb - ta)               # atajo: impares / pasos atajo (B = pasos clasicos - impares)
print(f"A42 | fraccion impar clasico={fc:.6f} (esp ~1/3), atajo={fa:.6f} (esp ~1/2), rango 2..100000")

# ---------- A43: la fraccion impar contra el tamano de la semilla
for lo, hi in [(10**3, 2 * 10**3), (10**4, 11 * 10**3), (10**5, 101 * 10**3), (10**6, 1001 * 10**3)]:
    ta = tb = 0
    for n in range(lo, hi):
        a, b = fracciones(n); ta += a; tb += b
    print(f"A43 | semillas {lo}..{hi - 1}: fraccion impar clasico = {ta/tb:.6f}")

# ---------- A48: racha inicial de impares (atajo) contra log2(altitud/n), impares
import math
xs = []; ys = []
for n in range(1, 100000, 2):
    r = 0; m = n
    while m % 2 == 1:
        r += 1; m = atajo(m)
    alt = max(tray(n, clasico))
    xs.append(r); ys.append(math.log2(alt / n))
mx = sum(xs) / len(xs); my = sum(ys) / len(ys)
cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
sx = math.sqrt(sum((x - mx) ** 2 for x in xs)); sy = math.sqrt(sum((y - my) ** 2 for y in ys))
print(f"A48 | corr(racha, log2(alt/n)) = {cov/(sx*sy):.4f} sobre {len(xs)} impares 1..99999 (repo: 0,59; refutada como prediccion)")

# ---------- A49: espejo base 10 — correlacion de pasos
def espejo10(n):
    return int(str(n)[::-1])
xs = []; ys = []
for n in range(2, 100001):
    e = espejo10(n)
    if e >= 2:
        xs.append(pasos_hasta_1(n)); ys.append(pasos_hasta_1(e))
mx = sum(xs) / len(xs); my = sum(ys) / len(ys)
cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
sx = math.sqrt(sum((x - mx) ** 2 for x in xs)); sy = math.sqrt(sum((y - my) ** 2 for y in ys))
print(f"A49 | corr(pasos(n), pasos(espejo10(n))) = {cov/(sx*sy):.4f} sobre {len(xs)} casos 2..100000 (repo: +0,08, nula)")

# ---------- A50: espejo base 2 — la identidad de UN paso y el ruido del segundo
def espejo2(n):
    k = n.bit_length()
    return 2 ** k - n if n != 2 ** (k - 1) else n  # potencias de 2: punto fijo del bloque
xs = []; ys = []
for n in range(2, 50001):
    e = espejo2(n)
    if e >= 2:
        xs.append(pasos_hasta_1(n)); ys.append(pasos_hasta_1(e))
mx = sum(xs) / len(xs); my = sum(ys) / len(ys)
cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
sx = math.sqrt(sum((x - mx) ** 2 for x in xs)); sy = math.sqrt(sum((y - my) ** 2 for y in ys))
print(f"A50 | corr(pasos(n), pasos(espejo2(n))) = {cov/(sx*sy):.4f} sobre {len(xs)} casos 2..50000 (repo: +0,06, ruido)")

# ---------- A53: la fila 'se escapan del rango' del A/B no discrimina
def escapan(regla, N, techo_factor=1000):
    cuenta = 0
    for n in range(1, N + 1):
        m = n; pasos = 0
        while 1 < m <= N * techo_factor and pasos < 10000:
            m = regla(m); pasos += 1
        if m > N * techo_factor:
            cuenta += 1
    return cuenta
def tresnmenos1(n):
    return n // 2 if n % 2 == 0 else 3 * n - 1
e1 = escapan(clasico, 1024); e2 = escapan(tresnmenos1, 1024)
print(f"A53 | escapan de rango N=1024: 3n+1 -> {e1}, 3n-1 -> {e2} (si son iguales, la fila no discrimina)")

# ---------- A55: los restos mod 64 que pisa el 221
restos = set(x % 64 for x in t221)
nunca = sorted(set(range(64)) - restos)
esperado = 64 * (1 - (1 - 1 / 64) ** len(t221))
print(f"A55 | el 221 pisa {len(restos)} de 64 restos (azar esperaria {esperado:.1f}); nunca pisa {nunca}")

# ---------- A65: ciclos del espejo base 10 bajo 100.000
vistos = set(); ciclos = set()
for n in range(1, 100000):
    orb = []
    m = n
    while m not in orb:
        orb.append(m); m = espejo10(m)
    inicio = orb.index(m)
    ciclos.add(frozenset(orb[inicio:]))
print(f"A65 | espejo base 10: {len(ciclos)} ciclos distintos alcanzados desde n < 100000 (repo: 44.450); Collatz positivo tiene 1")

# ---------- A80: los cruces de hilos.db por desfase
db = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'x')
repo = r'C:\Users\Home\Desktop\conjeturadecollazpython'
con = sqlite3.connect(os.path.join(repo, 'hilos.db'))
cols = [r[1] for r in con.execute('PRAGMA table_info(cruces)')]
print(f"A80-esquema | columnas de cruces: {cols}")
try:
    total = con.execute('SELECT COUNT(*) FROM cruces WHERE es_cola = 0').fetchone()[0]
    d0 = con.execute('SELECT COUNT(*) FROM cruces WHERE es_cola = 0 AND paso_a = paso_b').fetchone()[0]
    print(f"A80 | cruces no-cola: {total}, con desfase 0: {d0} (repo: 983 y 833)")
except Exception as ex:
    print(f"A80 | FALLO leyendo cruces: {ex}")
con.close()

# ---------- A60 / A69: la pinza de ciclos, re-derivada, a escala k <= 16
# candidato por resto: n = 2^k*t + r con t = (r - T^k(r)) / (3^S - 2^k).
# El atajo sobre Z divide exacto siempre (3n+1 es par si n impar, tambien en negativos).
def pinzaZ(k):
    out = set()
    for r in range(2 ** k):
        m = r; S = 0
        for _ in range(k):
            S += m % 2
            m = (3 * m + 1) // 2 if m % 2 else m // 2
        den = 3 ** S - 2 ** k
        if den == 0 or (r - m) % den:
            continue
        t = (r - m) // den
        n = 2 ** k * t + r
        x = n
        for _ in range(k):
            x = (3 * x + 1) // 2 if x % 2 else x // 2
        if x == n:
            out.add(n)
    return out
todos = set()
for k in range(1, 17):
    todos |= pinzaZ(k)
positivos = sorted(x for x in todos if x > 0)
negativos = sorted(x for x in todos if x <= 0)
print(f"A60/A69 | pinza fresca k=1..16: positivos que ciclan = {positivos}; no positivos = {negativos}")

# ---------- A45 / A70: densidad de pares consecutivos con la misma altura, tendencia
def altura_pasos(n):
    c = 0
    while n != 1:
        n = clasico(n); c += 1
    return c
for N in (10**4, 10**5):
    mismo = 0
    cuenta = 0
    a = altura_pasos(2)
    for n in range(2, N):
        b = altura_pasos(n + 1)
        if a == b:
            mismo += 1
        a = b
        cuenta += 1
    print(f"A45/A70 | pares (n, n+1) con misma altura hasta {N}: {mismo}/{cuenta} = {mismo/cuenta:.4f}")

# ---------- A51: la paridad siguiente no se predice de las k anteriores (frecuencias)
from collections import defaultdict
ctx = defaultdict(lambda: [0, 0])
for n in range(100001, 140001):
    bits = []
    m = n
    for _ in range(40):
        bits.append(m % 2); m = atajo(m)
    for i in range(8, len(bits)):
        ctx[tuple(bits[i - 8:i])][bits[i]] += 1
peor = 0.0
for c, (c0, c1) in ctx.items():
    tot = c0 + c1
    if tot >= 200:
        peor = max(peor, abs(c1 / tot - 0.5))
print(f"A51 | mejor ventaja posible prediciendo bit {8+1} de sus 8 anteriores (frecuencias, {len(ctx)} contextos): desviacion maxima de 0,5 = {peor:.4f}")
