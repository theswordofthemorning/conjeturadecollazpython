# A29 - verificacion independiente, escrita desde cero.
#
# ENUNCIADO: n = 2^k - 1 (mod 2^k) sube k veces seguidas;
#            n = 0     (mod 2^k) baja k veces seguidas.
#
# MAPA: el enunciado solo puede ser del ATAJO  T(n) = n/2 si par, (3n+1)/2 si impar,
# porque en el mapa clasico un paso impar (3n+1) va seguido de un n/2 que BAJA,
# asi que "sube k veces seguidas" con k >= 2 seria falso alli. Se comprueba abajo.
#
# Todo con int exacto. Ningun float decide nada.

fallos = 0

def T(n):
    # mapa del atajo sobre enteros no negativos
    if n % 2 == 0:
        return n // 2
    return (3 * n + 1) // 2   # 3n+1 es par si n impar; division exacta

def run_impar_inicial(n):
    # cuantos pasos impares seguidos da n desde el principio (mapa atajo)
    c = 0
    while n % 2 == 1:
        n = T(n)
        c += 1
    return c

# ---------------------------------------------------------------
# 1) DIRECCION DEL ENUNCIADO, parte "sube":
#    n = 2^k - 1 (mod 2^k), o sea n = m*2^k + (2^k - 1), m >= 0:
#    los primeros k pasos son impares y cada uno SUBE estrictamente.
#    Bordes incluidos: m = 0 (n = 2^k - 1), k = 1 (n = 1).
# ---------------------------------------------------------------
casos_sube = 0
for k in range(1, 13):
    for m in range(0, 50):
        n = m * (1 << k) + ((1 << k) - 1)
        x = n
        for paso in range(k):
            if x % 2 != 1:
                print("FALLO sube/paridad: k=%d m=%d n=%d paso %d es par (x=%d)" % (k, m, n, paso, x))
                fallos += 1
                break
            y = T(x)
            if not (y > x):
                print("FALLO sube/monotonia: k=%d m=%d n=%d paso %d: %d -> %d no sube" % (k, m, n, paso, x, y))
                fallos += 1
                break
            x = y
        else:
            casos_sube += 1
print("parte SUBE: k=1..12, m=0..49 -> %d casos, %d fallos" % (casos_sube, fallos))

# ---------------------------------------------------------------
# 2) DIRECCION DEL ENUNCIADO, parte "baja":
#    n = 0 (mod 2^k), n = m*2^k con m >= 1:
#    los primeros k pasos son pares y cada uno BAJA estrictamente.
#    Borde m = 0 -> n = 0: fuera de dominio (0/2 = 0 no baja); se declara.
# ---------------------------------------------------------------
f0 = fallos
casos_baja = 0
for k in range(1, 13):
    for m in range(1, 51):
        n = m * (1 << k)
        x = n
        for paso in range(k):
            if x % 2 != 0:
                print("FALLO baja/paridad: k=%d m=%d n=%d paso %d es impar (x=%d)" % (k, m, n, paso, x))
                fallos += 1
                break
            y = T(x)
            if not (y < x):
                print("FALLO baja/monotonia: k=%d m=%d n=%d paso %d: %d -> %d no baja" % (k, m, n, paso, x, y))
                fallos += 1
                break
            x = y
        else:
            casos_baja += 1
print("parte BAJA: k=1..12, m=1..50 -> %d casos, %d fallos" % (casos_baja, fallos - f0))

# borde n = 0 explicito
print("borde n=0: T(0)=%d, no baja (0 no esta en el dominio n>=1); el enunciado exige m>=1 en la parte 'baja'" % T(0))

# ---------------------------------------------------------------
# 3) EL RECIPROCO (Lema 8 de Hercher, la fuente declarada):
#    k impares seguidos ==> n = 2^k - 1 (mod 2^k).
#    Exhaustivo: n = 1..2^14, k = 1..10.
# ---------------------------------------------------------------
f0 = fallos
LIM = 1 << 14
for k in range(1, 11):
    resto = (1 << k) - 1
    mod = 1 << k
    for n in range(1, LIM + 1):
        tiene_k_impares = run_impar_inicial(n) >= k
        clase = (n % mod == resto)
        if tiene_k_impares != clase:
            print("FALLO reciproco: k=%d n=%d run>=%d es %s pero clase es %s" % (k, n, k, tiene_k_impares, clase))
            fallos += 1
print("reciproco (iff): n=1..%d, k=1..10 -> %d fallos" % (LIM, fallos - f0))

# lo mismo para la parte par: k pares seguidos <=> n = 0 (mod 2^k)
f0 = fallos
for k in range(1, 11):
    mod = 1 << k
    for n in range(1, LIM + 1):
        x = n
        c = 0
        while x % 2 == 0:
            x //= 2
            c += 1
        if (c >= k) != (n % mod == 0):
            print("FALLO reciproco par: k=%d n=%d" % (k, n))
            fallos += 1
print("reciproco par (iff): n=1..%d, k=1..10 -> %d fallos" % (LIM, fallos - f0))

# ---------------------------------------------------------------
# 4) Identidad de llegada: T^k(2^k - 1) = 3^k - 1 (consecuencia de Terras),
#    y el caso grande de la nota: 2^4000 - 1.
# ---------------------------------------------------------------
f0 = fallos
for k in range(1, 30):
    x = (1 << k) - 1
    for _ in range(k):
        x = T(x)
    if x != 3 ** k - 1:
        print("FALLO identidad: k=%d T^k(2^k-1)=%d != 3^k-1" % (k, x))
        fallos += 1
print("identidad T^k(2^k-1) = 3^k - 1: k=1..29 -> %d fallos" % (fallos - f0))

r4000 = run_impar_inicial((1 << 4000) - 1)
print("run de pasos impares seguidos de 2^4000 - 1 (mapa atajo): %d" % r4000)
r4000c = None
# en el mapa CLASICO los "pasos impares" no van seguidos (tras 3n+1 viene un par);
# alli lo que se cuenta es otra cosa. Lo anotamos sin decidir con ello.

# ---------------------------------------------------------------
# 5) CONTROL DE MAPA: en el mapa clasico "sube k veces seguidas" es FALSO ya con k=2.
# ---------------------------------------------------------------
n = 3  # 3 = 3 (mod 4), k=2
sec = [3, 10, 5]
ok_clasico = (10 > 3) and (5 > 10)
print("control mapa clasico: n=3 (=3 mod 4): 3 -> 10 -> 5; 'sube 2 veces' es %s -> el enunciado es del ATAJO" % ok_clasico)

# ---------------------------------------------------------------
# 6) BORDES SUELTOS
# ---------------------------------------------------------------
# k=0: "sube 0 veces" / "baja 0 veces" es vacuo, se cumple trivialmente.
# n=1: 1 = 1 (mod 2), k=1: T(1)=2 > 1, sube. n=2: 2 = 0 (mod 2): T(2)=1 < 2, baja.
assert T(1) == 2 and T(1) > 1
assert T(2) == 1 and T(2) < 2
print("bordes: k=0 vacuo; n=1 sube (T(1)=2); n=2 baja (T(2)=1)")

print()
if fallos == 0:
    print("VEREDICTO DEL SCRIPT: 0 fallos en todo")
else:
    raise SystemExit("HUBO %d FALLOS" % fallos)
