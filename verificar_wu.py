# verificar_wu.py
#
# RE-DERIVACION INDEPENDIENTE DE LO QUE EL REPO IMPORTA DE WU JIA-BANG
# Y DE LA CITA "WU Y HUANG 2001".
#
# AVISO SOBRE UNA AFIRMACION PROPIA DE ESTE FICHERO QUE RESULTO FALSA
# (01-08-2026). En el BALANCE del final se decia que "Wu ya habia calculado
# d(2^N) hasta N = 24, asi que este barrido reproduce a Wu y no lo amplia".
# NO ES CIERTO: el d(2^N) de Wu es K/(2^N - 1) -la densidad de ENTEROS que
# pertenecen a alguna tupla- y el del repo es la fraccion de PARES
# consecutivos que coinciden. En 2^24 valen 0,724756 y 0,500265. Un revisor lo
# caza antes de que la "correccion" entrara en el CLAUDE.md. El texto se deja
# corregido en su sitio, no borrado.
#
# Nada de aqui se cree por estar publicado. Todo se recalcula con enteros
# exactos de Python (int nativo, precision ilimitada). Cero numpy en la cadena
# que decide algo; numpy solo aparece para construir la tabla de alturas del
# barrido masivo, y esa tabla se contrasta contra una version lenta en Python
# puro antes de usarla.
#
# ---------------------------------------------------------------------------
# DE QUIEN ES CADA COSA QUE SE COMPRUEBA
# ---------------------------------------------------------------------------
#
#   (1) Terras (1976), Teoremas 1.1 y 1.2. El mapa acelerado
#           T(n) = n/2 si n par ; (3n+1)/2 si n impar
#       cumple  T^k(2^k*m + r) = 3^{S_k(r)} * m + T^k(r), con S_k(r) = numero
#       de pasos impares entre los k primeros. Es la pieza de la que cuelga
#       TODO lo demas de este fichero, asi que se comprueba primero y a mano.
#
#   (2) Garner (1985), Discrete Math. 55(1), 57-64: los pares (8k+4, 8k+5) se
#       funden siempre. Referencia SI verificable, DOI comprobado contra la API
#       de Crossref el 01-08-2026:  10.1016/S0012-365X(85)80020-0
#       (AVISO: un borrador de este mismo fichero llevaba el DOI
#        10.1016/0012-365X(85)90031-3, que da 404 en Crossref. Era inventado.
#        Queda escrito para que se vea que el fallo se caza comprobando.)
#
#   (3) "Wu Jia-Bang y Huang (2001)": las familias que se funden son
#       progresiones aritmeticas modulo 2^k, con los ejemplos
#           (32m+5, 32m+6)   (64m+45, 64m+46)   (128m+29, 128m+30)
#
#       LA CITA APARECE, Y EL CLAUDE.md SE PUEDE ACTUALIZAR (01-08-2026).
#       Estaba marcada como NO VERIFICADA por no tener DOI ni estar en
#       Crossref. Las dos cosas son ciertas y las dos son irrelevantes: es un
#       suplemento de una revista china de 2001, y esas no tienen DOI. La
#       referencia SI existe, catalogada por Lagarias en persona:
#
#         Wu, Jia Bang and Huang, Guo Lin (2001a), "Family of consecutive
#         integer pairs of the same height in the Collatz conjecture"
#         (en chino, resumen en ingles), Mathematica Applicata (Wuhan) 14
#         (2001), suplemento, 21-25.   MR 1885838   Zbl 1002.11023
#
#       Entrada 125 de "The 3x+1 problem: An annotated bibliography, II
#       (2000-2009)", J. C. Lagarias, arXiv:math/0608208. La nota que el
#       propio Lagarias le pone da las tres familias, textualmente, y ademas
#       los vectores de paridad de la tercera: (1001101) y (0111100). Eso
#       ultimo se comprueba abajo con codigo, y cuadra.
#
#       Por que no salia: Crossref no indexa suplementos de revistas chinas
#       de 2001, y Elia-Tucker 2015 no la citan porque su bibliografia entera
#       son cuatro entradas. Buscar en Crossref y concluir "no existe" fue el
#       error de metodo; el indice correcto para Collatz es la bibliografia
#       anotada de Lagarias, que lista los 3 papers de Wu y los 4 de Wu-Huang.
#
#       Aun asi se mantiene la separacion, porque es la buena:
#           EL HECHO       -> se comprueba con codigo exacto. Es verdad
#                             independientemente de quien lo publicara.
#           LA ATRIBUCION  -> no se comprueba con codigo. Se comprueba en un
#                             indice bibliografico, y ahora esta.
#
#   (4) Wu Jia-Bang (1992/1993/1995). Las tres referencias tambien aparecen
#       en la bibliografia de Lagarias (arXiv:math/0309224, entradas 188-190),
#       con sus numeros de MathSciNet y Zentralblatt:
#
#         188. Wu (1992), "A tendency of the proportion of consecutive numbers
#              of the same height in the Collatz problem", J. Huazhong Univ.
#              Sci. Technol. 20 no.5, 171-174.  MR 94b:11024, Zbl 766.11013
#              -> "The longest tuple in [1, 2^30), which is the 176-tuple with
#                  initial number 722,067,240, has been found."
#              -> y ojo: "The number of integers K which belong to n-tuples in
#                  [1, 2^N) (N = 1, 2, ..., 24) is accurately calculated. It is
#                  found that the density d(2^N) is increased with N."
#                  O SEA QUE WU YA CALCULO LA DENSIDAD HASTA N = 24 EN 1992.
#         189. Wu (1993), Mathematica Applicata, suppl. 6, 150-153. MR 1277568
#              -> "checked all positive integers up to 1.5 x 10^8 ... and found
#                  a 120-tuple, which is the longest tuple among all checked."
#         190. Wu (1995), J. Huazhong Univ. Sci. Tech. 23, suppl. II, 170-172.
#              MR 1403509
#              -> "A 310-tuple with an initial number 6,622,073,000 has been
#                  found", prueba que la densidad CONDICIONADA crece, y
#                  conjetura que la no condicionada tambien.
#       Estos dos numeros SI son comprobables uno por uno, y salen baratos:
#       calcular la altura de 400 numeros de diez cifras cuesta milisegundos.
#       Lo que NO es comprobable a nuestra escala es la palabra "MAS LARGA":
#       eso exige barrer los 2^30 enteros. Se dice explicitamente.
#
#   (5) La conjetura de Wu (1995): la densidad de pares consecutivos con la
#       misma altura crece con N. Se remide desde cero hasta 2^24 y se cruza
#       contra la tabla que el CLAUDE.md publica.
#
# ---------------------------------------------------------------------------
# COTA O PROMEDIO
# ---------------------------------------------------------------------------
#
#   El criterio de fusion (S_k(r) == S_k(r+1) y T^k(r) == T^k(r+1)) es una
#   COTA: decide, con una comprobacion finita, sobre los INFINITOS m de la
#   clase. Es el "cuarto camino" en estado puro.
#   La densidad d(2^N) es un PROMEDIO: no dice nada de ningun n concreto.

import random

import numpy as np

# ---------------------------------------------------------------------------
# Cambia esto aqui, guarda, y dale a Ctrl+B en Sublime.
# ---------------------------------------------------------------------------

# las tres familias publicadas, como (resto, exponente): (2^k*m + r, +1)
FAMILIAS = [(5, 5, "(32m+5, 32m+6)"),
            (45, 6, "(64m+45, 64m+46)"),
            (29, 7, "(128m+29, 128m+30)")]

M_FUERZA_BRUTA = 500     # cuantos m se prueban a lo bruto por familia
K_INDEPENDIENTE = 16     # hasta que k se recuenta a(k) en Python puro
POTENCIA = 24            # hasta 2^POTENCIA llega el barrido de densidad
DESDE = 10               # primera potencia de la tabla de densidad

# las tuplas que la literatura reporta: (primer numero, largo reportado, fuente)
TUPLAS_REPORTADAS = [
    (722067240,   176, "Wu Jia-Bang 1992, la mas larga bajo 2^30"),
    (6622073000,  310, "Wu Jia-Bang 1995"),
    (136696632,   120, "el repo la da como suya; es la de Wu 1993"),
    (98041684,     98, "este repo, la mas larga bajo 2^27"),
]

# el tope hasta el que Wu 1993 dice haber barrido
TOPE_WU_1993 = 150000000


# ---------------------------------------------------------------------------
# LA ARITMETICA, TODA CON int NATIVO
# ---------------------------------------------------------------------------

def paso_atajo(n):
    """Un paso del mapa acelerado T."""
    return n >> 1 if (n & 1) == 0 else (3 * n + 1) >> 1


def salto(r, k):
    """Devuelve (T^k(r), S_k(r)) con enteros exactos."""
    S = 0
    for _ in range(k):
        if r & 1:
            S += 1
        r = paso_atajo(r)
    return r, S


def altura(n):
    """Pasos del mapa CLASICO (3n+1) hasta llegar al 1."""
    c = 0
    while n != 1:
        n = n >> 1 if (n & 1) == 0 else 3 * n + 1
        c += 1
    return c


def se_funde_la_clase(r, k):
    """El criterio finito: la clase r modulo 2^k se funde con r+1 para TODO m."""
    a, sa = salto(r, k)
    b, sb = salto(r + 1, k)
    return (a == b) and (sa == sb), (a, sa, b, sb)


# ---------------------------------------------------------------------------
# COMPROBACION 1 -- la identidad de Terras, contra iteracion cruda
# ---------------------------------------------------------------------------

print("=" * 74)
print("COMPROBACION 1 -- Terras 1976 (1.1 y 1.2), re-derivado contra iteracion")
print("=" * 74)
print()
print("  Se afirma:  T^k(2^k*m + r) = 3^{S_k(r)} * m + T^k(r)")
print("  y ademas    S_k(2^k*m + r) = S_k(r)   (depende solo del resto).")
print("  Se contrasta contra iterar T k veces sobre el numero entero.")
print()

random.seed(20260801)
casos = 0
fallos_terras = 0
for k in range(1, 21):
    for _ in range(300):
        r = random.randrange(0, 1 << k)
        m = random.randrange(0, 10 ** 6)
        n = (1 << k) * m + r
        tk_n, s_n = salto(n, k)              # iteracion cruda sobre el numero
        tk_r, s_r = salto(r, k)              # solo el resto
        prediccion = (3 ** s_r) * m + tk_r
        casos += 1
        if tk_n != prediccion or s_n != s_r:
            fallos_terras += 1
            if fallos_terras < 4:
                print(f"    FALLO: k={k} r={r} m={m}")

print(f"  casos probados: {casos:,}    fallos: {fallos_terras}")
if fallos_terras:
    raise SystemExit("La identidad de Terras no se reproduce. Nada de lo que"
                     " sigue vale. Parar aqui.")
print("  La identidad de Terras se reproduce sin excepciones.")
print()
print("  Consecuencia inmediata, y es la que hace de criterio:")
print("    altura_clasica(n) = k + S_k(n) + altura_clasica(T^k(n))")
print("    luego si S_k(r) = S_k(r+1) y T^k(r) = T^k(r+1), los dos numeros")
print("    2^k*m+r y 2^k*m+r+1 tienen la MISMA altura.")
print("    Eso es una COTA, no un promedio: finito decide sobre infinitos.")
print()
print("  PERO LA DESCOMPOSICION TIENE UNA HIPOTESIS, y el CLAUDE.md no la")
print("  escribe: hace falta que T^j(n) != 1 para todo j < k. Si la")
print("  trayectoria toca el 1 antes del paso k, T sigue dando vueltas en")
print("  1 -> 2 -> 1 y la cuenta de pasos se pasa de largo. Se comprueba")
print("  contando los dos casos por separado.")
print()

# OJO: una muestra al azar de n grandes NO produce ni un caso sin la
# hipotesis, porque un n grande no llega al 1 en pocos pasos. Hay que meter
# los n chicos a mano, que es justo donde vive el contraejemplo.
muestra = [(random.randrange(2, 200000), random.randrange(1, 14))
           for _ in range(4000)]
muestra += [(n, k) for n in range(2, 80) for k in range(1, 13)]

fallos_alt_con = 0
fallos_alt_sin = 0
casos_sin = 0
for n, k in muestra:
    # toca el 1 antes de tiempo?
    x, toca = n, False
    for j in range(k):
        if x == 1:
            toca = True
            break
        x = paso_atajo(x)
    tk, s = salto(n, k)
    mal = altura(n) != k + s + altura(tk)
    if toca:
        casos_sin += 1
        fallos_alt_sin += mal
    else:
        fallos_alt_con += mal

print(f"  altura(n) == k + S_k(n) + altura(T^k(n)):")
print(f"    CON la hipotesis (la trayectoria no toca el 1 antes del paso k):")
print(f"      {len(muestra) - casos_sin:,} casos, {fallos_alt_con} fallos")
print(f"    SIN la hipotesis (toca el 1 antes):")
print(f"      {casos_sin:,} casos, {fallos_alt_sin} fallos"
      f"   <- {100 * fallos_alt_sin / max(casos_sin, 1):.1f}% de fallo")
if casos_sin == 0:
    raise SystemExit("La muestra no contiene ni un caso sin la hipotesis:"
                     " el control no vale. Parar aqui.")
if fallos_alt_con:
    raise SystemExit("La descomposicion falla incluso con la hipotesis."
                     " Parar aqui.")
print()
print("  Y LA HIPOTESIS ES GRATIS PARA m >= 1, con demostracion de una linea:")
print("    si n = 2^k*m + r con m >= 1, entonces n >= 2^k, y como T no baja")
print("    mas rapido que dividir entre 2, T^j(n) >= n/2^j >= 2^(k-j) >= 2")
print("    para todo j < k. Luego nunca toca el 1 antes de tiempo.")
print("    Para m = 0 (o sea n = r < 2^k) NO hay garantia, y falla de verdad.")

# la cota T^j(n) >= n / 2^j, comprobada
fallos_cota = 0
for _ in range(5000):
    n = random.randrange(2, 10 ** 7)
    k = random.randrange(1, 25)
    tk, _s = salto(n, k)
    if tk * (1 << k) < n:
        fallos_cota += 1
print(f"\n  cota T^k(n) >= n / 2^k: 5.000 casos, {fallos_cota} fallos")
if fallos_cota:
    raise SystemExit("La cota T^k(n) >= n/2^k falla. Parar aqui.")


# ---------------------------------------------------------------------------
# COMPROBACION 2 -- EL HECHO: las tres familias publicadas
# ---------------------------------------------------------------------------

print()
print("=" * 74)
print("COMPROBACION 2 -- EL HECHO: las tres familias de 'Wu-Huang 2001'")
print("=" * 74)
print()
print("  Se separa a proposito de la ATRIBUCION. Aqui solo se pregunta si el")
print("  enunciado matematico es cierto, con enteros exactos.")
print()

fallos_familia = 0
excepciones_m0 = []
for r, k, nombre in FAMILIAS + [(4, 3, "(8k+4, 8k+5)  -- Garner 1985")]:
    ok, (a, sa, b, sb) = se_funde_la_clase(r, k)
    print(f"  {nombre}")
    print(f"    r={r:>4} mod 2^{k}:  T^{k}({r}) = {a:>4}   S_{k}({r}) = {sa}")
    print(f"    r={r+1:>4} mod 2^{k}:  T^{k}({r+1}) = {b:>4}   S_{k}({r+1}) = {sb}")
    print(f"    criterio (misma pendiente 3^S y misma ordenada T^k): {ok}")

    # y ahora a lo bruto, sin usar el criterio para nada. m=0 aparte.
    malos = [m for m in range(1, M_FUERZA_BRUTA + 1)
             if altura((1 << k) * m + r) != altura((1 << k) * m + r + 1)]
    malo_cero = altura(r) != altura(r + 1)
    print(f"    fuerza bruta, m = 1..{M_FUERZA_BRUTA}: "
          f"{len(malos)} desacuerdos de {M_FUERZA_BRUTA}")
    print(f"    el caso m = 0, o sea el par ({r}, {r+1}) desnudo: "
          f"altura({r})={altura(r)}, altura({r+1})={altura(r+1)}"
          f"  ->  {'FALLA' if malo_cero else 'cumple'}")
    if malo_cero:
        excepciones_m0.append((r, k, nombre))
    if ok and malos:
        fallos_familia += 1
        print(f"      DESACUERDO GRAVE: el criterio dice que si y la fuerza"
              f" bruta dice que no en m={malos[:5]}")
    if (not ok) and not malos:
        fallos_familia += 1
        print(f"      DESACUERDO GRAVE: el criterio dice que no y la fuerza"
              f" bruta no encuentra ni un fallo")
    print()

if fallos_familia:
    raise SystemExit("El criterio y la fuerza bruta no coinciden en las"
                     " familias publicadas para m >= 1. Parar aqui.")
print("  Las tres familias publicadas SON CIERTAS para todo m >= 1, y ademas")
print("  se rederivan del criterio de Terras sin necesidad de la fuente.")
print()
print(f"  PERO {len(excepciones_m0)} de las 4 FALLAN EN m = 0:")
for r, k, nombre in excepciones_m0:
    print(f"    {nombre}: el par ({r}, {r+1}) NO tiene la misma altura.")
print("  La razon es la hipotesis de la comprobacion 1: con m = 0 el numero")
print("  es r < 2^k y su trayectoria puede tocar el 1 antes del paso k.")
print("  El enunciado correcto lleva 'para todo m >= 1'. Sin esa hipotesis")
print("  es FALSO, y el repo lo escribe sin ella.")


# --------- cuantas clases buenas fallan en m = 0, contadas para cada k

print()
print("  CUANTAS CLASES BUENAS FALLAN EN m = 0, por nivel (barrido completo):")
print()
print(f"  {'k':>3} {'clases buenas':>14} {'fallan en m=0':>14} {'los restos':>28}")
print(f"  {'-'*3} {'-'*14} {'-'*14} {'-'*28}")
for k in range(3, 13):
    MOD = 1 << k
    buenas = [r for r in range(MOD - 1) if se_funde_la_clase(r, k)[0]]
    # el resto 0 se salta: altura(0) no existe, el 0 se queda en el 0
    fallan = [r for r in buenas if r >= 1 and altura(r) != altura(r + 1)]
    muestra = str(fallan[:6]) if fallan else "-"
    print(f"  {k:>3} {len(buenas):>14,} {len(fallan):>14} {muestra:>28}")


# ---------------------------------------------------------------------------
# COMPROBACION 3 -- son MINIMAS? (lo que la cita no dice)
# ---------------------------------------------------------------------------

print()
print("=" * 74)
print("COMPROBACION 3 -- las familias publicadas, son minimas?")
print("=" * 74)
print()
print("  Las clases buenas se heredan hacia arriba: si r es buena mod 2^j,")
print("  entonces r y r+2^j son buenas mod 2^(j+1). Asi que una familia")
print("  enunciada mod 2^k podria ser el eco de otra mas gorda mod 2^j con")
print("  j < k. Si lo fuera, el enunciado publicado seria mas debil de lo")
print("  necesario. Se busca el j MINIMO para cada una.")
print()

for r, k, nombre in FAMILIAS + [(4, 3, "(8k+4, 8k+5)  -- Garner 1985")]:
    minimo = None
    for j in range(1, k + 1):
        rj = r % (1 << j)
        ok, _ = se_funde_la_clase(rj, j)
        if ok:
            minimo = (j, rj)
            break
    if minimo is None:
        print(f"  {nombre}: no se funde en ningun j <= {k}.  ERROR")
        raise SystemExit("Una familia publicada no cumple el criterio a su"
                         " propio nivel. Parar aqui.")
    j, rj = minimo
    marca = "MINIMA" if j == k else f"NO minima: ya vale mod 2^{j} con r={rj}"
    print(f"  {nombre:<32} j minimo = {j}   -> {marca}")


# ---------------------------------------------------------------------------
# COMPROBACION 3b -- los vectores de paridad que cita Lagarias
# ---------------------------------------------------------------------------
#
# La nota de Lagarias a la entrada 125 no solo da las familias: da los
# vectores de paridad de la tercera. Si el paper dice lo que Lagarias dice
# que dice, estos dos numeros tienen que salir clavados. Es la comprobacion
# mas fina que se puede hacer de una fuente que no se puede leer.

print()
print("=" * 74)
print("COMPROBACION 3b -- los vectores de paridad citados por Lagarias")
print("=" * 74)
print()
print("  Entrada 125 de arXiv:math/0608208, nota de Lagarias, textual:")
print("    'for (128m+29, 128m+30) the patterns are (1001101), (0111100)'")
print()

PATRONES_LAGARIAS = {29: "1001101", 30: "0111100"}
fallos_patron = 0
for n, esperado in PATRONES_LAGARIAS.items():
    x = n
    bits = ""
    for _ in range(7):
        bits += str(x & 1)
        x = paso_atajo(x)
    ok = bits == esperado
    if not ok:
        fallos_patron += 1
    print(f"    n = {n}:  calculado {bits}   citado {esperado}   "
          f"{'coincide' if ok else 'NO COINCIDE'}")

print(f"\n  fallos: {fallos_patron}")
if fallos_patron:
    raise SystemExit("Los vectores de paridad citados por Lagarias no salen."
                     " O la cita esta mal copiada o el calculo esta mal.")
print("  Los dos vectores salen clavados, bit a bit. El contenido del paper")
print("  de Wu-Huang 2001a se confirma hasta el ultimo bit citado, sin")
print("  necesidad de leer el paper (que esta en chino y sin DOI).")


# ---------------------------------------------------------------------------
# COMPROBACION 3c -- Elia-Tucker 2015: los contraejemplos a Garner
# ---------------------------------------------------------------------------
#
# arXiv:1511.09141 (INTEGERS 15 (2015) #A54) demuestra que la conjetura de
# Garner sobre QUE FORMA tienen los pares consecutivos de la misma altura es
# FALSA, con una familia infinita de contraejemplos: 2^19*m + 3067, siendo
# (3067, 3068) el menor. Se comprueba que esa clase cumple nuestro criterio.

print()
print("=" * 74)
print("COMPROBACION 3c -- Elia-Tucker 2015, la familia 2^19*m + 3067")
print("=" * 74)
print()

R_ET, K_ET = 3067, 19
ok_et, (a, sa, b, sb) = se_funde_la_clase(R_ET, K_ET)
print(f"  r = {R_ET} mod 2^{K_ET}:  T^{K_ET}({R_ET}) = {a}, S = {sa}")
print(f"  r = {R_ET+1} mod 2^{K_ET}:  T^{K_ET}({R_ET+1}) = {b}, S = {sb}")
print(f"  cumple el criterio: {ok_et}")
malos_et = [m for m in range(0, 60)
            if altura((1 << K_ET) * m + R_ET) != altura((1 << K_ET) * m + R_ET + 1)]
print(f"  fuerza bruta, m = 0..59: {len(malos_et)} desacuerdos")
if not ok_et or malos_et:
    raise SystemExit("La familia de Elia-Tucker no se reproduce.")

# el j minimo, que es lo que dice si 2^19 es el modulo justo
j_et = next(j for j in range(1, K_ET + 1)
            if se_funde_la_clase(R_ET % (1 << j), j)[0])
print(f"  j minimo para el que ya se funde: {j_et}")
print(f"  -> el par mas chico de la familia es ({R_ET}, {R_ET + 1}), y aqui")
print(f"     m = 0 SI cumple, al reves que en la familia de Wu-Huang.")
print()
print("  Nota de lectura: Elia-Tucker NO refuta que estas familias existan.")
print("  Refuta la descripcion que Garner daba de QUE FORMA tienen. El")
print("  criterio de Terras que se usa aqui no depende de esa descripcion,")
print("  asi que no le afecta.")


# ---------------------------------------------------------------------------
# COMPROBACION 4 -- recuento independiente de a(k), en Python puro
# ---------------------------------------------------------------------------

print()
print("=" * 74)
print(f"COMPROBACION 4 -- a(k) recontado en Python puro, sin numpy, k = 3..{K_INDEPENDIENTE}")
print("=" * 74)
print()
print("  a(k) = cuantos restos mod 2^k se funden con su vecino para todo m.")
print("  El repo publica: 1, 3, 8, 18, 39, 82, 170, 351, 721, ...  y 25.241")
print("  en k=16. Aqui se recuenta desde cero con otra implementacion.")
print()

REPO_A = {3: 1, 4: 3, 5: 8, 6: 18, 7: 39, 8: 82, 9: 170, 10: 351, 11: 721,
          16: 25241}

print(f"  {'k':>3} {'a(k) recontado':>15} {'repo':>10} {'coincide':>10}")
print(f"  {'-'*3} {'-'*15} {'-'*10} {'-'*10}")
discrepancias = 0
for k in range(3, K_INDEPENDIENTE + 1):
    MOD = 1 << k
    # se calcula (T^k, S_k) de 0..MOD-1 una sola vez, iterando en paralelo
    v = list(range(MOD))
    S = [0] * MOD
    for _ in range(k):
        for i in range(MOD):
            x = v[i]
            if x & 1:
                S[i] += 1
                v[i] = (3 * x + 1) >> 1
            else:
                v[i] = x >> 1
    cuenta = 0
    for r in range(MOD - 1):
        if v[r] == v[r + 1] and S[r] == S[r + 1]:
            cuenta += 1
    # el borde: r = MOD-1 se empareja con 2^k*(m+1) + 0
    if S[MOD - 1] == S[0] and v[MOD - 1] == 3 ** S[0] + v[0]:
        cuenta += 1
    esperado = REPO_A.get(k)
    igual = "" if esperado is None else ("si" if esperado == cuenta else "NO")
    if esperado is not None and esperado != cuenta:
        discrepancias += 1
    print(f"  {k:>3} {cuenta:>15,} {('-' if esperado is None else f'{esperado:,}'):>10}"
          f" {igual:>10}")

if discrepancias:
    raise SystemExit("El recuento independiente NO reproduce a(k) del repo.")
print()
print("  0 discrepancias contra los valores publicados en el repo.")


# ---------------------------------------------------------------------------
# COMPROBACION 5 -- las tuplas que Wu reporta, una por una
# ---------------------------------------------------------------------------

print()
print("=" * 74)
print("COMPROBACION 5 -- las tuplas reportadas, medidas numero a numero")
print("=" * 74)
print()
print("  Se calcula la altura EXACTA de cada miembro con enteros de Python y")
print("  se mide el largo real de la racha. Tambien se comprueba que el numero")
print("  anterior y el siguiente rompan la racha (o sea, que sea maximal).")
print()
print(f"  {'empieza en':>14} {'largo repor.':>13} {'largo real':>11}"
      f" {'altura':>8} {'maximal':>9}")
print(f"  {'-'*14} {'-'*13} {'-'*11} {'-'*8} {'-'*9}")

fallos_tupla = 0
for inicio, largo_rep, fuente in TUPLAS_REPORTADAS:
    h0 = altura(inicio)
    # hacia adelante
    largo = 1
    while altura(inicio + largo) == h0:
        largo += 1
        if largo > largo_rep + 200:
            break
    # hacia atras: si el anterior tambien coincide, la racha no empieza aqui
    empieza_aqui = altura(inicio - 1) != h0
    maximal = "si" if empieza_aqui else "NO empieza ahi"
    coincide = (largo == largo_rep) and empieza_aqui
    if not coincide:
        fallos_tupla += 1
    print(f"  {inicio:>14,} {largo_rep:>13} {largo:>11} {h0:>8} {maximal:>9}"
          f"   {'' if coincide else '<-- NO CUADRA'}")
    print(f"                 ({fuente})")

print()
if fallos_tupla:
    print(f"  {fallos_tupla} tupla(s) NO cuadran con lo reportado. Eso es un")
    print(f"  hallazgo, no un error del programa: la altura se calculo con")
    print(f"  enteros exactos y se puede rehacer a mano.")
else:
    print("  Las tuplas reportadas se confirman una por una, con su largo exacto.")

print()
print("  LO QUE ESTO NO DEMUESTRA: que 176 sea la MAS LARGA bajo 2^30. Eso")
print("  exige recorrer los 2^30 enteros con su altura, o sea una tabla de")
print("  2 GB y varios minutos. Aqui se confirma que la tupla EXISTE y MIDE")
print("  lo que dicen; la maximalidad global queda sin verificar.")
print()
print("  Y LA SORPRESA, que sale de leer la ficha de Wu 1993 (entrada 189 de")
print("  la bibliografia de Lagarias):")
print()
print("    Wu 1993 dice, textual: 'checked all positive integers up to")
print("    1.5 x 10^8 ... and found a 120-tuple, which is the longest tuple")
print("    among all checked numbers.'")
print()
print(f"    La tupla de 120 que el repo presenta como suya empieza en")
print(f"    {136696632:,}, y {136696632:,} < {TOPE_WU_1993:,}.")
print(f"    Cabe DENTRO del rango que Wu barrio en 1993.")
print()
print("    O sea: el '120 en 2^28' que el CLAUDE.md apunta como medida propia")
print("    y dice que 'es compatible con la trayectoria de crecimiento de Wu")
print("    pero no la confirma' NO es una medida nueva. ES el numero de Wu,")
print("    redescubierto. Wu no solo reporta 176 bajo 2^30: reporta 120 como")
print("    record de su propio barrido de 1993, y es exactamente el mismo.")
if 136696632 >= TOPE_WU_1993:
    raise SystemExit("La aritmetica de la comparacion esta mal.")


# ---------------------------------------------------------------------------
# COMPROBACION 6 -- la conjetura de densidad, remedida desde cero
# ---------------------------------------------------------------------------

print()
print("=" * 74)
print(f"COMPROBACION 6 -- la conjetura de Wu (1995), remedida hasta 2^{POTENCIA}")
print("=" * 74)
print()

TOPE = 1 << POTENCIA
BLOQUE = 1 << 20


def tabla_alturas(tope):
    """alturas[n] = pasos del mapa clasico hasta 1. Vectorizada por bloques.

    Se procesan bloques crecientes: todo lo que cae por debajo del bloque
    actual ya esta resuelto. int16 basta (las alturas no pasan de ~700 aqui).
    """
    h = np.full(tope + 1, -1, dtype=np.int16)
    h[1] = 0
    h[2] = 1
    for lo in range(3, tope + 1, BLOQUE):
        hi = min(lo + BLOQUE, tope + 1)
        origen = np.arange(lo, hi, dtype=np.int64)
        actual = origen.copy()
        cuenta = np.zeros(len(actual), dtype=np.int32)
        vivos = np.ones(len(actual), dtype=bool)
        while vivos.any():
            donde = np.flatnonzero(vivos)
            w = actual[donde]
            w = np.where((w & 1) == 0, w >> 1, 3 * w + 1)
            actual[donde] = w
            cuenta[donde] += 1
            bajos = w < lo
            if bajos.any():
                listos = donde[bajos]
                h[origen[listos]] = cuenta[listos] + h[w[bajos]]
                vivos[listos] = False
    return h


print(f"  Construyendo la tabla de alturas hasta 2^{POTENCIA} = {TOPE:,} ...")
alturas = tabla_alturas(TOPE)

# la tabla rapida contra la lenta, que es la unica que sabemos que es correcta
fallos_tabla = sum(1 for n in range(1, 20001) if int(alturas[n]) != altura(n))
print(f"  la tabla vectorizada contra altura() en Python puro, n = 1..20.000:"
      f" {fallos_tabla} fallos")
if fallos_tabla:
    raise SystemExit("La tabla vectorizada esta mal. No se puede medir nada.")

REPO_D = {21: 0.483710, 22: 0.489504, 23: 0.495086, 24: 0.500265,
          18: 0.463060, 14: 0.423305, 10: 0.364614}

print()
print(f"  {'N':>3} {'2^N':>13} {'d(altura)':>11} {'crece?':>8} {'repo':>10} {'delta':>10}")
print(f"  {'-'*3} {'-'*13} {'-'*11} {'-'*8} {'-'*10} {'-'*10}")
previa = -1.0
bajadas = 0
discrepa_repo = 0
for N in range(DESDE, POTENCIA + 1):
    hasta = 1 << N
    a = alturas[1:hasta]
    b = alturas[2:hasta + 1]
    d = float((a == b).mean())
    veredicto = "sube" if d > previa else "BAJA"
    if previa >= 0 and d <= previa:
        bajadas += 1
    previa = d
    ref = REPO_D.get(N)
    if ref is None:
        print(f"  {N:>3} {hasta:>13,} {d:>11.6f} {veredicto:>8} {'-':>10} {'-':>10}")
    else:
        delta = abs(d - ref)
        if delta > 1e-6:
            discrepa_repo += 1
        print(f"  {N:>3} {hasta:>13,} {d:>11.6f} {veredicto:>8} {ref:>10.6f}"
              f" {delta:>10.6f}")

print()
print(f"  escalones que bajan: {bajadas} de {POTENCIA - DESDE}")
print(f"  discrepancias contra la tabla del CLAUDE.md: {discrepa_repo}")
if discrepa_repo:
    raise SystemExit("Los valores de densidad del repo NO se reproducen.")


# ------------------------------- las rachas mas largas por escala, remedidas

print()
print("  LAS TUPLAS MAS LARGAS POR ESCALA, remedidas desde cero:")
print()
iguales = (alturas[1:TOPE] == alturas[2:TOPE + 1])
marca = np.zeros(len(iguales) + 2, dtype=np.int8)
marca[1:-1] = iguales
bordes = np.diff(marca)
arranques = np.flatnonzero(bordes == 1).astype(np.int64)
finales = np.flatnonzero(bordes == -1).astype(np.int64)
primeros = arranques + 1
largos = (finales - arranques) + 1

REPO_T = {10: 7, 13: 17, 16: 25, 18: 27, 20: 40, 22: 52, 23: 65, 24: 77}
print(f"  {'N':>3} {'2^N':>13} {'mas larga':>10} {'empieza en':>13} {'repo':>7}")
print(f"  {'-'*3} {'-'*13} {'-'*10} {'-'*13} {'-'*7}")
discrepa_t = 0
for N in range(DESDE, POTENCIA + 1):
    hasta = 1 << N
    dentro = primeros <= hasta
    if not dentro.any():
        continue
    l = np.minimum(largos[dentro], hasta - primeros[dentro] + 1)
    i = int(l.argmax())
    ref = REPO_T.get(N)
    if ref is not None and int(l[i]) != ref:
        discrepa_t += 1
    print(f"  {N:>3} {hasta:>13,} {int(l[i]):>10} {int(primeros[dentro][i]):>13,}"
          f" {('-' if ref is None else str(ref)):>7}")

print()
print(f"  discrepancias contra las tuplas del CLAUDE.md: {discrepa_t}")
if discrepa_t:
    raise SystemExit("Las tuplas maximas del repo NO se reproducen.")


# ---------------------------------------------------------------------------
# EL BALANCE
# ---------------------------------------------------------------------------

print()
print("=" * 74)
print("BALANCE")
print("=" * 74)
print()
print("  COTA (sirve para la formula):")
print("    - el criterio S_k(r)=S_k(r+1) y T^k(r)=T^k(r+1) decide sobre los")
print("      infinitos m de una clase con una cuenta finita. Verificado contra")
print("      fuerza bruta en las cinco familias y en el recuento de a(k).")
print("    - las tres familias publicadas son ciertas PARA m >= 1, y son")
print("      consecuencia del criterio: no hacen falta como axioma importado.")
print()
print("  CORRECCION AL ENUNCIADO, y es del mismo tipo que la del piso de la")
print("  altitud (a la que le faltaba 'n impar'):")
print("    - el criterio vale para m >= 1, no para todo m. Con m = 0 el numero")
print("      es r < 2^k y su trayectoria puede tocar el 1 antes del paso k.")
print("    - (5, 6) y (4, 5) son contraejemplos reales al enunciado sin la")
print("      hipotesis: alturas 5 contra 8, y 2 contra 5.")
print("    - la nota de Lagarias a la entrada 125 escribe la familia como")
print("      '{(2^k m + r, 2^k m + r + 1) : m >= 0}', con m >= 0. Con la")
print("      primera de sus tres familias, (32m+5, 32m+6), eso es falso en")
print("      m = 0. El repo copio el 'para todo m' de ahi y nadie lo probo,")
print("      porque clasesfusion.py empieza su fuerza bruta en m = 1.")
print()
print("  PROMEDIO (no sirve para la formula):")
print("    - la densidad d(2^N). Crece en todo el rango medido, pero medir que")
print("      una sucesion sube en catorce escalones no demuestra que suba")
print("      siempre. La conjetura de Wu sigue abierta.")
print("    - ESTE FICHERO AFIRMABA AQUI que 'Wu ya habia calculado d(2^N)")
print("      hasta N = 24 en 1992, asi que el barrido reproduce a Wu y no lo")
print("      amplia'. ESO ES FALSO y lo cazo un revisor el 01-08-2026 antes")
print("      de que entrara en el CLAUDE.md: son DOS cantidades distintas.")
print("      El d(2^N) de Wu es K/(2^N - 1), la densidad de ENTEROS que")
print("      pertenecen a alguna tupla; el de este repo es la fraccion de")
print("      PARES consecutivos que coinciden. En 2^24 valen 0,724756 y")
print("      0,500265. La tabla de densidad del repo mide algo suyo.")
print("      (Se deja escrito en vez de borrarlo: es el mismo error de")
print("       magnitud que el hito de Garner, y los dos aparecieron juntos.")
print("       La diferencia es que uno entro y el otro no.)")
print()
print("  NO VERIFICABLE CON ESTOS MEDIOS, y hay que decirlo:")
print("    - que 176 sea la tupla MAS LARGA bajo 2^30 (haria falta la tabla")
print("      entera de 2^30, ~2 GB). Se confirma que existe y que mide 176.")
print("    - lo mismo para el 120 bajo 1,5 x 10^8 de Wu 1993 y para el 310.")
print("      Las tres tuplas se confirman una por una; la maximalidad no.")
print("    - el contenido del paper de Wu-Huang 2001a: esta en chino y no hay")
print("      copia accesible. Lo que SI se verifico es (a) que la referencia")
print("      existe y esta catalogada, y (b) que los datos que Lagarias cita")
print("      de el -- las tres familias y los dos vectores de paridad -- son")
print("      exactos. Es lo mas lejos que se llega sin el papel en la mano.")
