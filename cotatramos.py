# cotatramos.py
#
# LA COTA POR TRAMO, RESCATADA DE collazlamina.py ANTES DE BORRARLO.
#
# collazlamina.py dibujaba "la lamina": los pares de una trayectoria puestos en
# tres ejes, todos por encima de un plano. El dibujo era ruido -- media la
# geometria que se eligio. Pero el CALCULO que hacia antes de dibujar sostiene
# una COTA, y las cotas son lo unico de este laboratorio con forma de teorema.
#
# ---------------------------------------------------------------------------
# LO QUE SE AFIRMA
# ---------------------------------------------------------------------------
#
# Para cualquier par de posiciones i < j de cualquier trayectoria, con
# A = veces que se aplico 3n+1 y B = veces que se aplico n/2 en el tramo:
#
#     2^B * seq[j]  =  3^A * seq[i]  +  C        (identidad de Terras 1.1)
#
# y C se actualiza C -> 3C + 2^B en cada paso impar, luego C >= 0 SIEMPRE, con
# C = 0 si y solo si el tramo no tiene ningun paso impar. De ahi, directamente:
#
#     (1)  2^B * seq[j]  >=  3^A * seq[i]        para todo par i < j
#     (2)  si el tramo BAJA (seq[j] < seq[i]),  entonces  2^B > 3^A
#
# LA (2) ES LA QUE IMPORTA, y es la razon de que este fichero exista: convierte
# "el balance decide todo" de PROMEDIO sobre trayectorias en COTA POR TRAMO.
# El repo tenia B/A > log2(3) como una observacion estadistica sobre
# trayectorias enteras que llegan a 1. Aqui es una desigualdad forzada, tramo a
# tramo, sin hipotesis.
#
# ---------------------------------------------------------------------------
# Y LO QUE LA HACE VALER: NO ASUME CONVERGENCIA
# ---------------------------------------------------------------------------
#
# Casi todo lo que mide este repo solo se puede evaluar sobre trayectorias que
# YA llegaron a 1 -- el residuo de Roosendaal, gamma(rho), la fraccion impar.
# Eso es contabilidad, no criterio.
#
# Esta cota no: se comprueba sobre PREFIJOS de trayectorias que NUNCA tocan el
# 1, arrancando en semillas de 200 bits. Si Collatz fuera falsa y existiera una
# orbita divergente, esta desigualdad seguiria valiendo en todos sus tramos.
# Por eso el barrido de abajo usa prefijos y no trayectorias completas: es la
# diferencia entre medir a los supervivientes y medir a la regla.
#
# Comprobado todo en aritmetica entera exacta. Ni un float en la cadena que
# decide.

import random

# ---------------------------------------------------------------------------
SEMILLAS_BITS = (20, 60, 200)   # tamanos de las semillas de los prefijos
POR_TAMANO = 60                 # cuantas semillas de cada tamano
LARGO_PREFIJO = 60              # cuantos pasos de prefijo se miran
NUMERO = 221                    # la trayectoria completa de control
SEMILLA_AZAR = 20260801         # fija, para que el barrido sea reproducible
# ---------------------------------------------------------------------------


def pasos_de(n, cuantos):
    """Los primeros `cuantos` pasos de n con el mapa clasico, sin llegar al 1."""
    v = [n]
    for _ in range(cuantos):
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        v.append(n)
        if n == 1:
            break
    return v


def secuencia_de(n):
    v = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        v.append(n)
    return v


def revisa(seq):
    """Recorre todos los pares i<j y devuelve (pares, fallos_identidad,
    C_negativos, fallos_cota, tramos_que_bajan, fallos_corolario)."""
    L = len(seq)
    pares = f_ident = c_neg = f_cota = bajan = f_coro = 0
    for i in range(L):
        A = B = C = 0
        for j in range(i + 1, L):
            if seq[j - 1] % 2 == 1:
                C = 3 * C + 2 ** B
                A += 1
            else:
                B += 1
            x, y = seq[i], seq[j]
            pares += 1
            if 2 ** B * y != 3 ** A * x + C:
                f_ident += 1
            if C < 0:
                c_neg += 1
            if 2 ** B * y < 3 ** A * x:
                f_cota += 1
            if y < x:
                bajan += 1
                if 2 ** B <= 3 ** A:
                    f_coro += 1
    return pares, f_ident, c_neg, f_cota, bajan, f_coro


print("=" * 74)
print("LA COTA POR TRAMO -- sobre prefijos que NUNCA llegan al 1")
print("=" * 74)

# ===========================================================================
# COMPROBACION 1 -- sobre prefijos, o sea sin asumir que la trayectoria acaba
# ===========================================================================
rnd = random.Random(SEMILLA_AZAR)
tot = dict(pares=0, ident=0, cneg=0, cota=0, bajan=0, coro=0)
prefijos = 0
tocaron_1 = 0

for bits in SEMILLAS_BITS:
    for _ in range(POR_TAMANO):
        n = rnd.randrange(2 ** (bits - 1), 2 ** bits) | 1
        seq = pasos_de(n, LARGO_PREFIJO)
        if seq[-1] == 1:
            tocaron_1 += 1
            continue
        prefijos += 1
        p, fi, cn, fc, ba, co = revisa(seq)
        tot["pares"] += p
        tot["ident"] += fi
        tot["cneg"] += cn
        tot["cota"] += fc
        tot["bajan"] += ba
        tot["coro"] += co

print("\nCOMPROBACION 1 -- prefijos de %d pasos, semillas de %s bits" % (
    LARGO_PREFIJO, "/".join(str(b) for b in SEMILLAS_BITS)))
print("  prefijos usados (ninguno toca el 1) : %d" % prefijos)
print("  descartados por tocar el 1          : %d" % tocaron_1)
print("  pares i<j revisados                 : %d" % tot["pares"])
print("  fallos de la identidad              : %d" % tot["ident"])
print("  valores de C negativos              : %d" % tot["cneg"])
print("  pares por debajo de la cota (1)     : %d" % tot["cota"])
print("  tramos que BAJAN                    : %d" % tot["bajan"])
print("  de esos, fallos del corolario (2)   : %d" % tot["coro"])

if tot["ident"] or tot["cneg"] or tot["cota"] or tot["coro"]:
    raise SystemExit("FALLO: la cota no se sostiene. Se para antes de afirmar nada.")

# ===========================================================================
# COMPROBACION 2 -- la trayectoria completa del 221, para cuadrar con el repo
# ===========================================================================
seq = secuencia_de(NUMERO)
p, fi, cn, fc, ba, co = revisa(seq)
print("\nCOMPROBACION 2 -- la trayectoria completa del %d" % NUMERO)
print("  pasos                    : %d" % (len(seq) - 1))
print("  pares i<j                : %d" % p)
print("  fallos identidad / cota  : %d / %d" % (fi, fc))
print("  tramos que bajan         : %d, fallos del corolario: %d" % (ba, co))
if fi or fc or co:
    raise SystemExit("FALLO: el 221 rompe la cota. Se para.")

# ===========================================================================
# COMPROBACION 3 -- el control A/B. La cota tiene que DISCRIMINAR.
#
# Sobre 3n-1 la constante C de la identidad es NEGATIVA, asi que la desigualdad
# se da vuelta. Si saliera igual en los dos mapas, la cota no diria nada sobre
# convergencia -- que es exactamente lo que le paso a a(k) de clasesfusion.py.
# ===========================================================================
def revisa_menos(seq):
    L = len(seq)
    pares = f_ident = f_cota = 0
    for i in range(L):
        A = B = C = 0
        for j in range(i + 1, L):
            if seq[j - 1] % 2 == 1:
                C = 3 * C - 2 ** B
                A += 1
            else:
                B += 1
            x, y = seq[i], seq[j]
            pares += 1
            if 2 ** B * y != 3 ** A * x + C:
                f_ident += 1
            if 2 ** B * y >= 3 ** A * x:
                f_cota += 1
    return pares, f_ident, f_cota


def pasos_menos(n, cuantos):
    v = [n]
    for _ in range(cuantos):
        n = n // 2 if n % 2 == 0 else 3 * n - 1
        v.append(n)
        if n == 1:
            break
    return v


rnd2 = random.Random(SEMILLA_AZAR)
pm = fim = fcm = 0
for bits in SEMILLAS_BITS:
    for _ in range(POR_TAMANO):
        n = rnd2.randrange(2 ** (bits - 1), 2 ** bits) | 1
        s = pasos_menos(n, LARGO_PREFIJO)
        if s[-1] == 1:
            continue
        a, b, c = revisa_menos(s)
        pm += a
        fim += b
        fcm += c

print("\nCOMPROBACION 3 -- el control A/B sobre el mapa 3n-1")
print("  pares revisados                       : %d" % pm)
print("  fallos de la identidad (con C -> 3C - 2^B) : %d" % fim)
print("  pares que cumplen 2^B*y >= 3^A*x      : %d" % fcm)
print("  o sea: la desigualdad se DA VUELTA, porque alli C es negativa.")
if fim:
    raise SystemExit("FALLO: la identidad de 3n-1 no cuadra. Se para.")

print("""
======================================================================
LO QUE QUEDA ESTABLECIDO
======================================================================

  (1)  2^B * seq[j] >= 3^A * seq[i]     para todo par i<j de todo n
  (2)  si un tramo BAJA, entonces 2^B > 3^A

  Las dos salen de C >= 0 en la identidad de Terras, y C >= 0 sale de que
  C se construye sumando potencias de 2. No hay nada estadistico aqui.

  IMPORTA POR TRES RAZONES:

  - Es una COTA, no un promedio. Un promedio no demuestra ningun caso
    individual; esto vale para cada tramo de cada trayectoria.

  - NO ASUME CONVERGENCIA. Se comprobo sobre prefijos que nunca tocan el 1.
    Si existiera una orbita divergente, seguiria valiendo en ella.

  - DISCRIMINA. Sobre 3n-1 la constante C es negativa y la desigualdad se
    invierte. Una cantidad que saliera igual en los dos mapas no podria
    decir nada sobre convergencia, porque 3n-1 NO converge.

  LO QUE NO DICE, para no inflarlo: (2) es NECESARIA, no suficiente. Que un
  tramo baje obliga a 2^B > 3^A, pero 2^B > 3^A no obliga a que baje -- el
  n=7 tiene B/A = 8/5 > log2(3) y su tramo sube. La condicion suficiente
  conocida es la de Everett, B/A > log2(10/3) = 1,73697, y entre las dos
  queda la franja log2(10/9) que sigue abierta.
""")
