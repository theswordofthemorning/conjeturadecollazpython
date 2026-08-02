# A22.py - Agente 2 (independiente). Verificacion del item A22:
#   "a(32) = 1.871.137.623 clases mod 2^32 se funden: cota inferior DEMOSTRADA
#    del 43,5658% de los pares consecutivos"
#
# TODO DERIVADO DESDE CERO, sin abrir ningun fichero del repo.
#
# MAPAS (hay tres; aqui se declara cual se usa en cada sitio):
#   - clasico:  n -> n/2 si par,  n -> 3n+1 si impar
#   - atajo T:  n -> n/2 si par,  n -> (3n+1)/2 si impar
# El criterio de clases se construye sobre el ATAJO T (es donde vale la forma
# afin exacta). La "altura" (pasos hasta 1) se comprueba en LOS DOS mapas.
#
# DERIVACION PROPIA DEL CRITERIO (esbozo, verificado numericamente abajo):
#   Sea n = 2^k*m + r con 0 <= r < 2^k. Por induccion sobre j <= k:
#       T^j(n) = 3^{s_j} * 2^{k-j} * m + c_j
#   donde c_0 = r y en cada paso la paridad de T^j(n) es la de c_j (porque
#   2^{k-j}*m es par mientras j < k), y c_j evoluciona exactamente como T(c_j).
#   Luego  T^k(2^k*m + r) = 3^{S_k(r)} * m + T^k(r),  con S_k(r) = numero de
#   pasos impares entre los primeros k, y S_k, T^k dependen SOLO de r.
#   Por tanto, la clase r es "buena" (el par (n, n+1) se funde en el paso k
#   para TODO m) exactamente cuando
#       S_k(r) == S_k(r+1)   y   T^k(r) == T^k(r+1)
#   Ojo con m = 0: la derivacion de "misma altura" necesita ademas que la
#   trayectoria no toque el 1 antes del paso k; con m >= 1, n >= 2^k y
#   T^j(n) >= n/2^j >= 2 para j < k, asi que esta garantizado. Con m = 0 no.
#
# Todo lo que decide es aritmetica entera exacta (int / Fraction).

from fractions import Fraction
import sys

fallos = []

def T(n):
    # mapa del ATAJO
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2

def S_y_Tk(r, k):
    # S_k(r) y T^k(r) iterando el atajo k veces sobre el entero r
    s = 0
    c = r
    for _ in range(k):
        if c % 2 == 1:
            s += 1
            c = (3 * c + 1) // 2
        else:
            c = c // 2
    return s, c

def altura_clasica(n):
    # pasos del mapa CLASICO hasta llegar a 1
    p = 0
    while n != 1:
        n = 3 * n + 1 if n % 2 == 1 else n // 2
        p += 1
    return p

def altura_atajo(n):
    p = 0
    while n != 1:
        n = T(n)
        p += 1
    return p

# ---------------------------------------------------------------
# (0) Verificacion numerica de la derivacion afin (no darla por buena):
#     T^k(2^k*m + r) == 3^{S_k(r)}*m + T^k(r) para una rejilla de casos.
# ---------------------------------------------------------------
comprobadas = 0
for k in (1, 2, 3, 5, 8, 12):
    for r in range(2 ** k):
        s, tk = S_y_Tk(r, k)
        for m in (0, 1, 2, 7, 100):
            n = (2 ** k) * m + r
            c = n
            for _ in range(k):
                c = T(c)
            if c != (3 ** s) * m + tk:
                fallos.append(("forma afin", k, r, m))
            comprobadas += 1
print("(0) forma afin T^k(2^k*m+r) = 3^S*m + T^k(r):",
      comprobadas, "casos, fallos =",
      len([f for f in fallos if f[0] == "forma afin"]))

# ---------------------------------------------------------------
# (1) Recalcular a(k) para k = 3..18 y comparar con la sucesion dada.
#     Borde r = 2^k - 1: n+1 cae en la clase 0 del m siguiente; se
#     comprueba aparte que nunca puede ser buena.
# ---------------------------------------------------------------
publicada = [1, 3, 8, 18, 39, 82, 170, 351, 721, 1476, 3012, 6130,
             12450, 25241, 51105, 103358]  # k = 3..18

mias = []
for k in range(3, 19):
    N = 2 ** k
    datos = [S_y_Tk(r, k) for r in range(N + 1)]  # incluye r = 2^k
    buenas = 0
    for r in range(N - 1):
        if datos[r] == datos[r + 1]:
            buenas += 1
    # borde r = 2^k - 1: exige 3^{S(r)}*m + T^k(r) == 1*(m+1) + 0 para todo m
    # (porque S_k(0)=0, T^k(0)=0); imposible salvo S(r)=0, y r es impar => S>=1.
    s_borde, _ = datos[N - 1]
    if s_borde == 0:
        fallos.append(("borde", k))
    mias.append(buenas)

print("(1) a(k) k=3..18 propios:   ", mias)
print("    a(k) k=3..18 publicados:", publicada)
if mias != publicada:
    fallos.append(("sucesion a(k)", mias))
print("    coinciden los 16 terminos:", mias == publicada)
print("    borde r=2^k-1 nunca es clase buena (S>=1): comprobado k=3..18")

# ---------------------------------------------------------------
# (2) La aritmetica del enunciado: 1871137623 / 2^32
# ---------------------------------------------------------------
f32 = Fraction(1871137623, 2 ** 32)
# 43,5658% con 4 decimales de porcentaje -> comparar redondeo exacto
pct_por_10000 = (f32 * 1000000).numerator * 10 // (f32 * 1000000).denominator
# mejor: redondeo exacto a 4 decimales de porcentaje con enteros
num = 1871137623 * 10 ** 6  # porcentaje * 10^4 = fraccion * 10^6
den = 2 ** 32
cociente, resto = divmod(num, den)
redondeado = cociente + (1 if 2 * resto >= den else 0)  # 435658 esperado
print("(2) 1871137623/2^32 =", float(f32), " -> porcentaje x10^4 redondeado =", redondeado)
if redondeado != 435658:
    fallos.append(("aritmetica 43,5658", redondeado))
print("    43,5658% cuadra:", redondeado == 435658)
# y la monotonia estructural: a(k) buena mod 2^k implica 2 hijas buenas mod 2^{k+1},
# comprobada empiricamente: a(k+1) >= 2*a(k) en los 16 terminos
mono = all(mias[i + 1] >= 2 * mias[i] for i in range(len(mias) - 1))
print("    a(k+1) >= 2*a(k) en k=3..17:", mono)
if not mono:
    fallos.append(("monotonia",))
print("    => f(k) crece, luego f(32) >= f(18) =", float(Fraction(mias[-1], 2 ** 18)))

# ---------------------------------------------------------------
# (3) Que la fraccion es COTA INFERIOR de la densidad de pares consecutivos
#     con la misma altura:
#     (a) cada clase buena implica fusion real y misma altura para m >= 1
#     (b) la densidad medida de pares con misma altura es >= f(k)
# ---------------------------------------------------------------
# (3a) muestreo de m sobre TODAS las clases buenas de k = 3..10, y sobre una
#      muestra de clases buenas de k = 14
def clases_buenas(k):
    N = 2 ** k
    datos = [S_y_Tk(r, k) for r in range(N)]
    return [r for r in range(N - 1) if datos[r] == datos[r + 1]]

casos_3a = 0
for k in list(range(3, 11)) + [14]:
    buenas = clases_buenas(k)
    if k == 14:
        buenas = buenas[::37]  # muestra
    for r in buenas:
        for m in (1, 2, 3, 10, 1000):
            n = (2 ** k) * m + r
            # fusion real en el paso k del atajo
            a, b = n, n + 1
            for _ in range(k):
                a, b = T(a), T(b)
            if a != b:
                fallos.append(("fusion m>=1", k, r, m))
            # misma altura en los dos mapas
            if altura_atajo(n) != altura_atajo(n + 1):
                fallos.append(("altura atajo", k, r, m))
            if altura_clasica(n) != altura_clasica(n + 1):
                fallos.append(("altura clasica", k, r, m))
            casos_3a += 1
print("(3a) clases buenas con m en {1,2,3,10,1000}:", casos_3a,
      "casos, fallos =", len([f for f in fallos if f[0] in
                              ("fusion m>=1", "altura atajo", "altura clasica")]))

# (3b) BORDE m = 0: el enunciado con "para todo m" seria falso; buscar
#      contraejemplos entre las clases buenas con m = 0
contra_m0 = []
for k in range(3, 12):
    for r in clases_buenas(k):
        if r >= 2:  # n = r con m = 0; alturas definidas para n >= 1
            if altura_clasica(r) != altura_clasica(r + 1):
                contra_m0.append((k, r))
resumen_m0 = {}
for k, r in contra_m0:
    resumen_m0.setdefault(k, []).append(r)
print("(3b) BORDE m=0: clases buenas donde el par (r, r+1) NO tiene la misma altura:")
for k in sorted(resumen_m0):
    print("     k =", k, "-> r en", sorted(set(resumen_m0[k]))[:8])
print("     => la cota exige m >= 1; con m = 0 hay contraejemplos reales")

# (3c) densidad medida de pares consecutivos con la misma altura (mapa clasico),
#      sobre una ventana con m >= 1 garantizado para k = 18, y comparar con f(18)
k = 18
N0 = 2 ** k  # asi todo n de la ventana tiene m >= 1 en cada clase mod 2^18
V = 60000
iguales = 0
alt_prev = altura_clasica(N0 + 1)
for n in range(N0 + 1, N0 + 1 + V):
    alt_sig = altura_clasica(n + 1)
    if alt_prev == alt_sig:
        iguales += 1
    alt_prev = alt_sig
dens = Fraction(iguales, V)
f18 = Fraction(mias[-1], 2 ** 18)
print("(3c) densidad medida de pares con misma altura (clasico),",
      "n en [2^18+1, 2^18+%d]:" % V, float(dens))
print("     f(18) =", float(f18), " f(32) declarada =", float(f32))
print("     densidad >= f(32)?", dens >= f32, "   densidad >= f(18)?", dens >= f18)
if not (dens >= f32):
    fallos.append(("cota inferior vs densidad", float(dens)))

# (3d) bordes chicos: n=1, n=2, k=0
#      k=0: el criterio es vacio (0 pasos); a(0) no esta definido en el enunciado.
#      n=1 y n=2: alturas 0 y 1 (clasico), solo relevantes via m=0, ya cubierto.
print("(3d) bordes: k=0 fuera de ambito (el enunciado empieza en clases mod 2^k,",
      "k>=3 en la sucesion); n=1,n=2 solo entran con m=0, cubierto en (3b)")

# ---------------------------------------------------------------
# veredicto del script
# ---------------------------------------------------------------
if fallos:
    raise SystemExit("FALLOS: " + repr(fallos[:10]))
print()
print("VEREDICTO DEL SCRIPT: 0 fallos.")
print(" - a(k) reproducida de forma independiente k=3..18, 16/16 identica")
print(" - 1871137623/2^32 redondea exactamente a 43,5658%")
print(" - a(k+1) >= 2*a(k) => la fraccion es monotona no decreciente")
print(" - clase buena => fusion y misma altura para m >= 1 (0 fallos)")
print(" - con m = 0 hay contraejemplos: la cota necesita m >= 1")
print(" - densidad medida de pares con misma altura > f(32) declarada")
