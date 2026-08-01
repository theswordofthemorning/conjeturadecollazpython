# cotatramos3n1.py
#
# LA COTA POR TRAMO, PERO SOBRE EL MAPA 3n-1. NO ES COLLATZ.
#
# ---------------------------------------------------------------------------
# AVISO DE MAPA, PRIMERO DE TODO
# ---------------------------------------------------------------------------
#
# Este repo ya se equivoco TRES veces confundiendo un mapa con otro (el
# 2/ln(4/3) atribuido al clasico en vez de al atajo, la traduccion de Everett,
# y la medicion en vivo del mapa clasico contra el del atajo). Asi que aqui va
# explicito y arriba del todo:
#
#     ESTE FICHERO MIDE            n par   ->  n / 2
#                                  n impar ->  3n - 1
#
#     NO mide el clasico 3n+1, NO mide el atajo (3n+1)/2.
#
# El mapa 3n-1 sobre los enteros positivos ES Collatz sobre los enteros
# NEGATIVOS (si n = -m, par -> n/2 = -(m/2); impar -> 3n+1 = -(3m-1)). Y NO
# converge: tiene TRES ciclos conocidos -- {1,2}, el de largo 5 desde el 5, y
# el de largo 18 desde el 17. Por eso todo barrido de aqui esta acotado por
# NUMERO DE PASOS y nunca por "hasta llegar al 1": un tramo puede entrar en
# ciclo y no terminar jamas.
#
# ---------------------------------------------------------------------------
# LA IDENTIDAD, DERIVADA AQUI (no copiada)
# ---------------------------------------------------------------------------
#
# Sea un tramo que arranca en x = seq[i] y llega a y = seq[j], con
#   A = veces que se aplico 3n-1     B = veces que se aplico n/2
#
# Se propone el invariante
#
#     2^B * y  =  3^A * x  +  C            con C entero, C = 0 al arrancar
#
# y se comprueba que se conserva paso a paso:
#
#   PASO PAR   y -> y/2.  B pasa a B+1, A y C no se tocan:
#              2^(B+1) * (y/2) = 2^B * y = 3^A x + C.   Invariante intacto.
#
#   PASO IMPAR y -> 3y-1. A pasa a A+1, B no se toca:
#              2^B * (3y - 1) = 3 * (2^B y) - 2^B
#                             = 3 * (3^A x + C) - 2^B
#                             = 3^(A+1) x + (3C - 2^B)
#              luego la regla de actualizacion es
#
#                         C  ->  3C - 2^B         (2^B con la B DE AHORA)
#
# Comparese con el mapa 3n+1, donde la misma cuenta da C -> 3C + 2^B. La FORMA
# de la identidad es la misma en los dos mapas; lo unico que cambia es el signo
# del termino que se suma. Eso es todo el asunto de este fichero.
#
# ---------------------------------------------------------------------------
# EL SIGNO DE C, Y LA COTA QUE SALE DE EL
# ---------------------------------------------------------------------------
#
# INDUCCION, en dos lineas: C arranca en 0. Si C <= 0 y viene un paso impar,
# el nuevo C vale 3C - 2^B <= -2^B <= -1 < 0. Los pasos pares no tocan C.
# Luego
#
#     C <= 0 SIEMPRE,  y  C = 0 exactamente cuando A = 0 (tramo sin impares).
#     Si A >= 1 entonces C <= -1, estricto.
#
# Y de ahi, directamente y sin hipotesis:
#
#   (II)  2^B * y  <=  3^A * x        para todo tramo, todo x, todo largo
#         (EN COLLATZ VA AL REVES: alli 3^A x <= 2^B y, porque alli C >= 0)
#
#   (III) COROLARIO ESPEJO: si el tramo SUBE (y > x) entonces 2^B < 3^A.
#         Demostracion: 2^B y <= 3^A x < 3^A y (porque x < y y 3^A > 0), y
#         como y > x >= 1 > 0 se puede dividir por y: 2^B < 3^A.
#         NO HACE FALTA NINGUNA HIPOTESIS EXTRA sobre n0 -- solo que sea un
#         entero positivo, que es el dominio del mapa. La unica division es
#         por y, y y > x >= 1 la garantiza. (En Collatz el corolario es "si
#         BAJA entonces 2^B > 3^A"; aqui es "si SUBE entonces 2^B < 3^A".)
#
# Todo lo de abajo se comprueba en ARITMETICA ENTERA EXACTA. Ni un float en la
# cadena que decide.

import random

# ---------------------------------------------------------------------------
SEMILLAS_BITS = (20, 45, 200)   # tamanos de las semillas aleatorias
POR_TAMANO = 40                 # cuantas semillas de cada tamano
LARGO_PREFIJO = 55              # pasos de prefijo que se miran de cada semilla
EXHAUSTIVO_HASTA = 400          # n0 = 1..este, exhaustivo, todos los pares i<j
LARGO_EXHAUSTIVO = 22           # pasos de prefijo en el barrido exhaustivo
PRESUPUESTO_CICLO = 2000        # tope de pasos al clasificar en que ciclo cae
SEMILLA_AZAR = 20260801         # fija, para que el barrido sea reproducible
# ---------------------------------------------------------------------------


def paso_menos(n):
    """UN paso del mapa 3n-1."""
    return n // 2 if n % 2 == 0 else 3 * n - 1


def paso_mas(n):
    """UN paso del mapa clasico 3n+1. Solo se usa en el control A/B."""
    return n // 2 if n % 2 == 0 else 3 * n + 1


def pasos_de(n, cuantos, paso):
    """Exactamente `cuantos` pasos. NO para en el 1: en 3n-1 el 1 no es un
    sumidero, es parte del ciclo {1,2}, y parar ahi seria mirar otro objeto."""
    v = [n]
    for _ in range(cuantos):
        n = paso(n)
        v.append(n)
    return v


def revisa(seq, signo):
    """Recorre TODOS los pares i<j del tramo y cuenta.

    signo = -1 para el mapa 3n-1 (C -> 3C - 2^B)
    signo = +1 para el mapa 3n+1 (C -> 3C + 2^B)

    Devuelve un dict con todos los conteos, para los dos sentidos de la cota,
    de modo que la MISMA funcion sirva para el mapa y para su control."""
    L = len(seq)
    r = dict(pares=0, ident=0,
             c_pos=0, c_neg=0, c_cero=0, a_cero=0, c_cero_y_a_cero=0,
             falla_cota_menos=0, falla_cota_mas=0,
             suben=0, coro_sube=0, bajan=0, coro_baja=0)
    for i in range(L):
        A = B = C = 0
        pot2 = 1          # 2^B exacto, entero
        pot3 = 1          # 3^A exacto, entero
        x = seq[i]
        for j in range(i + 1, L):
            if seq[j - 1] % 2 == 1:
                C = 3 * C + signo * pot2
                A += 1
                pot3 *= 3
            else:
                B += 1
                pot2 *= 2
            y = seq[j]
            izq = pot2 * y          # 2^B * n_k
            der = pot3 * x          # 3^A * n0
            r["pares"] += 1
            if izq != der + C:
                r["ident"] += 1
            if C > 0:
                r["c_pos"] += 1
            elif C < 0:
                r["c_neg"] += 1
            else:
                r["c_cero"] += 1
            if A == 0:
                r["a_cero"] += 1
                if C == 0:
                    r["c_cero_y_a_cero"] += 1
            if izq > der:
                r["falla_cota_menos"] += 1     # rompe  2^B*y <= 3^A*x
            if izq < der:
                r["falla_cota_mas"] += 1       # rompe  2^B*y >= 3^A*x
            if y > x:
                r["suben"] += 1
                if pot2 >= pot3:
                    r["coro_sube"] += 1        # rompe  sube => 2^B < 3^A
            if y < x:
                r["bajan"] += 1
                if pot2 <= pot3:
                    r["coro_baja"] += 1        # rompe  baja => 2^B > 3^A
    return r


def suma(acum, r):
    for k, v in r.items():
        acum[k] = acum.get(k, 0) + v
    return acum


def ciclo_de(n, presupuesto):
    """En que ciclo cae n, con TOPE DE PASOS. Devuelve el ciclo como tupla
    ordenada, o None si no cerro dentro del presupuesto."""
    visto = {}
    v = n
    for t in range(presupuesto):
        if v in visto:
            aro = [k for k, o in visto.items() if o >= visto[v]]
            return tuple(sorted(aro))
        visto[v] = t
        v = paso_menos(v)
    return None


print("=" * 74)
print("LA COTA POR TRAMO SOBRE EL MAPA 3n-1  (n par -> n/2, n impar -> 3n-1)")
print("NO es Collatz. Collatz es 3n+1 y su cota va AL REVES.")
print("=" * 74)

# ===========================================================================
# COMPROBACION 0 -- los tres ciclos de 3n-1, para saber con que se trata
# ===========================================================================
aros = {}
for n in range(1, 3000):
    a = ciclo_de(n, PRESUPUESTO_CICLO)
    if a is None:
        raise SystemExit("FALLO: n = %d no cerro en %d pasos. Se para." % (
            n, PRESUPUESTO_CICLO))
    aros[a] = aros.get(a, 0) + 1

print("\nCOMPROBACION 0 -- los ciclos de 3n-1 en 1..2999")
for a in sorted(aros, key=len):
    print("  largo %2d  cuenta %4d  minimo %d   %s" % (
        len(a), aros[a], min(a), list(a)[:6]))
if len(aros) != 3:
    raise SystemExit("FALLO: se esperaban 3 ciclos y salieron %d. Se para." % len(aros))
largos = sorted(len(a) for a in aros)
if largos != [2, 5, 18]:
    raise SystemExit("FALLO: los largos de ciclo son %s y no [2, 5, 18]. Se para."
                     % largos)
minimos = sorted(min(a) for a in aros)
if minimos != [1, 5, 17]:
    raise SystemExit("FALLO: los minimos de ciclo son %s y no [1, 5, 17]. Se para."
                     % minimos)
print("  Los tres ciclos son los conocidos. Por eso el barrido se acota por PASOS.")

# ===========================================================================
# COMPROBACION 1 -- exhaustiva: n0 = 1..EXHAUSTIVO_HASTA, todos los pares i<j
# ===========================================================================
acum = {}
for n in range(1, EXHAUSTIVO_HASTA + 1):
    seq = pasos_de(n, LARGO_EXHAUSTIVO, paso_menos)
    acum = suma(acum, revisa(seq, -1))

print("\nCOMPROBACION 1 -- EXHAUSTIVA, n0 = 1..%d, %d pasos, todos los pares i<j"
      % (EXHAUSTIVO_HASTA, LARGO_EXHAUSTIVO))
print("  pares i<j revisados                  : %d" % acum["pares"])
print("  fallos de la identidad               : %d" % acum["ident"])
print("  valores de C positivos (prohibidos)  : %d" % acum["c_pos"])
print("  valores de C negativos               : %d" % acum["c_neg"])
print("  valores de C = 0                     : %d" % acum["c_cero"])
print("  tramos con A = 0                     : %d" % acum["a_cero"])
print("  fallos de (II)  2^B*n_k <= 3^A*n0    : %d" % acum["falla_cota_menos"])
print("  tramos que SUBEN                     : %d" % acum["suben"])
print("  de esos, fallos de (III) 2^B < 3^A   : %d" % acum["coro_sube"])
if acum["ident"] or acum["c_pos"] or acum["falla_cota_menos"] or acum["coro_sube"]:
    raise SystemExit("FALLO: la cota de 3n-1 no se sostiene en el exhaustivo. Se para.")
if acum["c_cero"] != acum["a_cero"] or acum["c_cero"] != acum["c_cero_y_a_cero"]:
    raise SystemExit("FALLO: C = 0 y A = 0 no son el mismo conjunto. Se para.")
print("  C = 0 si y solo si A = 0 : confirmado en los %d casos." % acum["pares"])

# ===========================================================================
# COMPROBACION 2 -- semillas grandes, prefijos que NO se acercan al final del
# rango. Con 200 bits el tramo de 55 pasos no llega ni de lejos a un ciclo.
# ===========================================================================
rnd = random.Random(SEMILLA_AZAR)
grandes = {}
semillas = []
for bits in SEMILLAS_BITS:
    for _ in range(POR_TAMANO):
        n = rnd.randrange(2 ** (bits - 1), 2 ** bits) | 1
        semillas.append(n)
        grandes = suma(grandes, revisa(pasos_de(n, LARGO_PREFIJO, paso_menos), -1))

print("\nCOMPROBACION 2 -- semillas de %s bits, %d de cada, prefijos de %d pasos"
      % ("/".join(str(b) for b in SEMILLAS_BITS), POR_TAMANO, LARGO_PREFIJO))
print("  semillas                             : %d" % len(semillas))
print("  pares i<j revisados                  : %d" % grandes["pares"])
print("  fallos de la identidad               : %d" % grandes["ident"])
print("  valores de C positivos (prohibidos)  : %d" % grandes["c_pos"])
print("  fallos de (II)  2^B*n_k <= 3^A*n0    : %d" % grandes["falla_cota_menos"])
print("  tramos que SUBEN                     : %d" % grandes["suben"])
print("  de esos, fallos de (III) 2^B < 3^A   : %d" % grandes["coro_sube"])
if (grandes["ident"] or grandes["c_pos"] or grandes["falla_cota_menos"]
        or grandes["coro_sube"]):
    raise SystemExit("FALLO: la cota de 3n-1 se rompe en semillas grandes. Se para.")

# ===========================================================================
# COMPROBACION 3 -- una semilla que entra en CADA UNO de los tres ciclos, y el
# tramo se sigue DENTRO del ciclo, dando varias vueltas. Es el caso que en
# Collatz no existe y que aqui podria romper cualquier argumento que asumiera
# que la trayectoria termina.
# ===========================================================================
por_ciclo = {}
for n in range(1, 3000):
    a = ciclo_de(n, PRESUPUESTO_CICLO)
    if a not in por_ciclo:
        por_ciclo[a] = []
    if len(por_ciclo[a]) < 3:
        por_ciclo[a].append(n)

print("\nCOMPROBACION 3 -- tramos que ENTRAN Y DAN VUELTAS en cada ciclo")
tot_ciclo = {}
for a in sorted(por_ciclo, key=len):
    sub = {}
    for n in por_ciclo[a]:
        sub = suma(sub, revisa(pasos_de(n, 4 * len(a) + 30, paso_menos), -1))
    tot_ciclo = suma(tot_ciclo, sub)
    print("  ciclo de largo %2d (min %3d), semillas %s :" % (
        len(a), min(a), por_ciclo[a]))
    print("      pares %6d | ident %d | C>0 %d | fallos (II) %d | suben %d, fallos (III) %d"
          % (sub["pares"], sub["ident"], sub["c_pos"], sub["falla_cota_menos"],
             sub["suben"], sub["coro_sube"]))
if (tot_ciclo["ident"] or tot_ciclo["c_pos"] or tot_ciclo["falla_cota_menos"]
        or tot_ciclo["coro_sube"]):
    raise SystemExit("FALLO: un tramo dentro de un ciclo rompe la cota. Se para.")
print("  Total dentro de ciclos: %d pares, 0 fallos." % tot_ciclo["pares"])

# ===========================================================================
# COMPROBACION 4 -- LA DISCRIMINACION (el control A/B del repo).
#
# Si la cota (II) valiera tambien para 3n+1, o si la de Collatz valiera para
# 3n-1, la cota no estaria midiendo la REGLA sino el modo de contar. Hay que
# exhibir contraejemplos concretos en las dos direcciones.
# ===========================================================================
mas = {}
for n in range(1, EXHAUSTIVO_HASTA + 1):
    mas = suma(mas, revisa(pasos_de(n, LARGO_EXHAUSTIVO, paso_mas), +1))
for n in semillas:
    mas = suma(mas, revisa(pasos_de(n, LARGO_PREFIJO, paso_mas), +1))

menos = dict(acum)
for k in grandes:
    menos[k] = menos.get(k, 0) + grandes[k]

print("\nCOMPROBACION 4 -- LA DISCRIMINACION, mismos n0 por los dos mapas")
print("                         %14s %14s" % ("3n-1", "3n+1"))
print("  pares revisados        %14d %14d" % (menos["pares"], mas["pares"]))
print("  fallos de la identidad %14d %14d" % (menos["ident"], mas["ident"]))
print("  C > 0                  %14d %14d" % (menos["c_pos"], mas["c_pos"]))
print("  C < 0                  %14d %14d" % (menos["c_neg"], mas["c_neg"]))
print("  rompe 2^B*nk <= 3^A*n0 %14d %14d" % (menos["falla_cota_menos"],
                                              mas["falla_cota_menos"]))
print("  rompe 2^B*nk >= 3^A*n0 %14d %14d" % (menos["falla_cota_mas"],
                                              mas["falla_cota_mas"]))
print("  suben / fallan (III)   %11d/%2d %11d/%2d" % (
    menos["suben"], menos["coro_sube"], mas["suben"], mas["coro_sube"]))
print("  bajan / fallan Collatz %11d/%2d %11d/%2d" % (
    menos["bajan"], menos["coro_baja"], mas["bajan"], mas["coro_baja"]))

if mas["ident"]:
    raise SystemExit("FALLO: la identidad de 3n+1 no cuadra. Se para.")
if mas["falla_cota_menos"] == 0:
    raise SystemExit("FALLO: (II) tambien vale para 3n+1 -> NO DISCRIMINA. Se para.")
if menos["falla_cota_mas"] == 0:
    raise SystemExit("FALLO: la cota de Collatz tambien vale para 3n-1 -> NO "
                     "DISCRIMINA. Se para.")
if menos["c_pos"] or mas["c_neg"]:
    raise SystemExit("FALLO: el signo de C no separa los dos mapas. Se para.")
if menos["coro_baja"] == 0:
    raise SystemExit("FALLO: en 3n-1 'baja => 2^B > 3^A' no falla nunca; entonces "
                     "el corolario no es especifico del sentido. Se para.")

# --- los contraejemplos MINIMOS, exhibidos uno a uno -----------------------
def primer_contra(paso, signo, cual):
    """Busca el primer (n0, i, j) que rompe la cota `cual` en el mapa dado.
    cual = 'menos' -> rompe 2^B*y <= 3^A*x ; 'mas' -> rompe 2^B*y >= 3^A*x."""
    for n in range(1, 200):
        seq = pasos_de(n, 12, paso)
        for i in range(len(seq)):
            A = B = C = 0
            pot2 = pot3 = 1
            x = seq[i]
            for j in range(i + 1, len(seq)):
                if seq[j - 1] % 2 == 1:
                    C = 3 * C + signo * pot2
                    A += 1
                    pot3 *= 3
                else:
                    B += 1
                    pot2 *= 2
                y = seq[j]
                mal = (pot2 * y > pot3 * x) if cual == "menos" else (pot2 * y < pot3 * x)
                if mal:
                    return (x, y, A, B, C, pot2 * y, pot3 * x)
    return None


c1 = primer_contra(paso_mas, +1, "menos")
c2 = primer_contra(paso_menos, -1, "mas")
if c1 is None or c2 is None:
    raise SystemExit("FALLO: no se hallo contraejemplo de discriminacion. Se para.")

print("\n  CONTRAEJEMPLO 1 -- (II) es FALSA para 3n+1:")
print("    n0 = %d, n_k = %d, A = %d, B = %d, C = %+d" % (c1[0], c1[1], c1[2], c1[3], c1[4]))
print("    2^B*n_k = %d  >  3^A*n0 = %d      (rompe 2^B*n_k <= 3^A*n0)" % (c1[5], c1[6]))
print("\n  CONTRAEJEMPLO 2 -- la cota de Collatz es FALSA para 3n-1:")
print("    n0 = %d, n_k = %d, A = %d, B = %d, C = %+d" % (c2[0], c2[1], c2[2], c2[3], c2[4]))
print("    2^B*n_k = %d  <  3^A*n0 = %d      (rompe 3^A*n0 <= 2^B*n_k)" % (c2[5], c2[6]))

# --- y un contraejemplo al corolario en el sentido EQUIVOCADO --------------
def primer_baja_sin(paso, signo):
    """En 3n-1: un tramo que BAJA y sin embargo tiene 2^B <= 3^A. Muestra que
    el corolario de Collatz ('baja => 2^B > 3^A') no se hereda."""
    for n in range(1, 400):
        seq = pasos_de(n, 14, paso)
        for i in range(len(seq)):
            A = B = C = 0
            pot2 = pot3 = 1
            x = seq[i]
            for j in range(i + 1, len(seq)):
                if seq[j - 1] % 2 == 1:
                    C = 3 * C + signo * pot2
                    A += 1
                    pot3 *= 3
                else:
                    B += 1
                    pot2 *= 2
                y = seq[j]
                if y < x and pot2 <= pot3:
                    return (x, y, A, B, pot2, pot3)
    return None


c3 = primer_baja_sin(paso_menos, -1)
if c3 is None:
    raise SystemExit("FALLO: no se hallo el contraejemplo del corolario. Se para.")
print("\n  CONTRAEJEMPLO 3 -- en 3n-1 'baja => 2^B > 3^A' es FALSO:")
print("    n0 = %d -> n_k = %d (BAJA), A = %d, B = %d, 2^B = %d <= 3^A = %d"
      % (c3[0], c3[1], c3[2], c3[3], c3[4], c3[5]))
print("    o sea que el corolario NO se traduce sustituyendo una palabra:")
print("    en 3n-1 el enunciado que vale es 'SUBE -> 2^B < 3^A'.")

# ===========================================================================
# COMPROBACION 5 -- (V) el signo. Que es lo que cambia exactamente.
# ===========================================================================
print("\nCOMPROBACION 5 -- (V) que cambia de signo: la diferencia o la C")
print("  La identidad tiene la MISMA forma en los dos mapas, y en los dos la")
print("  diferencia 2^B*n_k - 3^A*n0 es EXACTAMENTE C -- ni una excepcion en")
print("  %d + %d = %d pares. Luego NO son dos preguntas: es una." % (
    menos["pares"], mas["pares"], menos["pares"] + mas["pares"]))
print("  Lo que cambia es el signo de C, y la desigualdad lo arrastra:")
print("    3n+1 :  C -> 3C + 2^B  ->  C >= 0  ->  2^B*n_k >= 3^A*n0")
print("            C > 0 en %d pares, C < 0 en %d pares" % (mas["c_pos"], mas["c_neg"]))
print("    3n-1 :  C -> 3C - 2^B  ->  C <= 0  ->  2^B*n_k <= 3^A*n0")
print("            C > 0 en %d pares, C < 0 en %d pares" % (menos["c_pos"], menos["c_neg"]))
print("  Y el caso de igualdad es el mismo en los dos: C = 0 <=> A = 0.")

print("""
======================================================================
LO QUE QUEDA ESTABLECIDO PARA EL MAPA 3n-1
======================================================================

  IDENTIDAD   2^B * n_k  =  3^A * n0  +  C
              C = 0 al arrancar;  C -> 3C - 2^B en cada paso impar;
              C no cambia en los pasos pares.

  (I)   C <= 0 SIEMPRE, por induccion (3C - 2^B <= -2^B < 0 si C <= 0).
        C = 0 exactamente cuando el tramo no tiene ningun paso impar.
        La constante del enunciado que se pedia "C >= 0" NO existe con ese
        signo: aqui la que no cambia de signo es -C.

  (II)  2^B * n_k  <=  3^A * n0        para todo n0 >= 1 y todo k.
        EN COLLATZ ES AL REVES. No es la misma cota con otro nombre.

  (III) Si el tramo SUBE (n_k > n0) entonces 2^B < 3^A.
        SIN HIPOTESIS EXTRA sobre n0: la unica division del argumento es por
        n_k, y n_k > n0 >= 1 ya la garantiza. Pedir mas (n0 impar, n0 fuera
        de ciclo, k grande) debilitaria el enunciado sin comprarlo nada.

  (IV)  DISCRIMINA. (II) es falsa en 3n+1 desde el primer paso impar, y la
        cota de Collatz es falsa en 3n-1 desde el primer paso impar. Y el
        corolario tampoco se hereda: en 3n-1 hay tramos que BAJAN con
        2^B <= 3^A. La cota mide la REGLA, no el modo de contar.

  NO ASUME CONVERGENCIA, y aqui eso no es retorica: 3n-1 NO converge. Se
  comprobo sobre prefijos de 200 bits que no llegan a ningun ciclo, Y sobre
  tramos que dan varias vueltas DENTRO de los tres ciclos. La desigualdad
  aguanta en los dos sitios, porque no sabe nada de destinos.

  LO QUE NO DICE: (III) es NECESARIA, no suficiente. Que 2^B < 3^A no obliga
  al tramo a subir.
""")
