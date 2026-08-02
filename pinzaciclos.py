# pinzaciclos.py
#
# LA PINZA DE DESCARTE DE CICLOS: UN CANDIDATO POR RESTO, Y NINGUNO SOBREVIVE.
#
# Este programa no dibuja nada: solo numeros por stdout. Junta por primera vez
# cuatro piezas que el laboratorio ya tenia verificadas por separado:
#
#   1. mallaresiduos.py -- los primeros k pasos los decide n modulo 2^k
#   2. clasesfusion.py  -- la identidad de Terras escrita como una recta en m
#   3. collazmalla.py   -- las coordenadas (A, B) de un tramo
#   4. la tabla de convergentes de log2(3) (Terras tabla C, Guy 1983)
#
# Y las usa para lo que Terras las uso en 1976: descartar ciclos.
#
# ---------------------------------------------------------------------------
# LA MATEMATICA, EN CINCO LINEAS
# ---------------------------------------------------------------------------
#
# Con el mapa del ATAJO   T(n) = n/2 si par,  (3n+1)/2 si impar,
# el Teorema 1.2 de Terras dice que lambda_k y rho_k dependen SOLO del resto,
# y poniendo n = 2^k * m + r queda la recta que ya usa clasesfusion.py:
#
#     T^k(2^k * m + r)  =  3^{S_k(r)} * m  +  T^k(r)
#
# donde S_k(r) = cuantos de los k primeros pasos fueron impares.
#
# Un ciclo de longitud k es T^k(n) = n. Sustituyendo n = 2^k * m + r:
#
#     3^{S(r)} * m + T^k(r)  =  2^k * m + r
#     m * (3^{S(r)} - 2^k)   =  r - T^k(r)
#
#     m  =  ( r - T^k(r) )  /  ( 3^{S(r)} - 2^k )
#
# El denominador nunca es cero (3^S = 2^k solo con S = k = 0), asi que
#
#     POR CADA RESTO r HAY COMO MUCHO UN CANDIDATO, Y SE CALCULA EN CERRADO.
#
# Si m no sale entero >= 0, ese resto queda descartado PARA SIEMPRE, para los
# infinitos numeros de su clase. Eso es la pinza: un barrido finito de 2^k
# casillas que decide sobre todos los enteros a la vez.
#
# ---------------------------------------------------------------------------
# LA OTRA MITAD DE LA PINZA
# ---------------------------------------------------------------------------
#
# El filtro algebraico de arriba es exhaustivo pero cuesta 2^k. El filtro de
# log2(3) es gratis y dice DONDE mirar: un ciclo con A pasos impares y B = k
# pasos del atajo necesita 2^k muy cerca de 3^A, o sea k/A muy cerca de
# log2(3) = 1,5849625007. Las unicas fracciones que lo consiguen son las
# convergentes y semiconvergentes de su fraccion continua. Aqui se comprueba
# que los dos filtros dicen lo mismo, y se mide el mecanismo: la cantidad de
# restos que pasan la division es aproximadamente C(k,S) / |3^S - 2^k|, o sea
# que se dispara exactamente en las convergentes. El filtro de log2(3) no es
# una regla aparte: es el tamano del denominador de esta ecuacion.
#
# ---------------------------------------------------------------------------
# POR QUE EN BLOQUES (copiado de clasesfusion.py, que ya resolvio esto)
# ---------------------------------------------------------------------------
#
# A k = 30 el array de restos son 1.073 millones de int64: 8,6 GB, y cada
# operacion del paso crea temporales. En bloques de 4 millones el pico se
# queda en unos 150 MB, sea cual sea k.
#
# Y hay un ahorro mas: se hace UNA sola pasada de K_MAX pasos sobre todos los
# restos de [0, 2^K_MAX), y despues de cada paso k se revisa el trozo r < 2^k,
# que es justo el rango de restos que le toca a ese k. Asi el barrido entero
# de k = 1 a K_MAX cuesta lo mismo que el barrido de K_MAX solo.
#
# Ese troceado esta verificado contra una implementacion independiente en
# Python puro, sin numpy y sin bloques (o sea sin el pegado de la frontera):
# los tres conteos de k = 1 a 22 salen identicos, 0 discrepancias. Es la misma
# disciplina que uso clasesfusion.py con su troceado.
#
# ---------------------------------------------------------------------------
# LO QUE SALIO, Y QUE NO SE ESPERABA
# ---------------------------------------------------------------------------
#
# Prediccion escrita antes de medir: cero supervivientes salvo el ciclo
# trivial. Se cumple, hasta k = 30 (2.147.483.646 restos, uno a uno).
#
# Lo que NO se habia previsto: la ecuacion no mira el signo de m, asi que un
# m negativo tambien es solucion valida y da un n negativo que cicla. El
# barrido esta resolviendo el problema sobre TODO Z sin proponerselo, y por eso
# RECUPERA los tres ciclos negativos de Collatz sin que se le haya hablado
# nunca de negativos. Sale exacto: los restos que pasan la division son
#
#     dividen(k) = 2 + 2*[2|k] + 3*[3|k] + 11*[11|k]
#
# que es el conteo de los cuatro ciclos conocidos sobre Z ({0}, {1,2}, {-1},
# {-5,-7,-10} y el de once elementos {-17,...,-34}), cada uno apareciendo en
# los k multiplos de su periodo. 0 desacuerdos en los 30 valores de k, y cero
# restos sin explicar. La ultima seccion del programa lo comprueba.
#
# ---------------------------------------------------------------------------
# LO QUE ESTO NO ES
# ---------------------------------------------------------------------------
#
# No es nuevo ni de lejos. Terras lo hizo en 1976 y con la fuerza bruta que
# habia entonces llego a periodo 2592 -- y ese 2592 es una cifra HISTORICA, no
# la frontera: la frontera se mueve con lo verificado, y con X0 = 2^71 (Barina
# 2025) el mismo argumento elemental excluye ya hasta periodo 114.208.327.603.
# Hercher (2023) demostro algo mucho mas fuerte (no hay m-ciclos con m <= 91).
# Esto es rederivacion verificada. El informe del final lo dice con numeros.

import math
import random
from decimal import Decimal, getcontext

import numpy as np

# ---------------------------------------------------------------------------
# Cambia esto aqui, guarda, y dale a Ctrl+B en Sublime.
# ---------------------------------------------------------------------------

K_MAX = 30          # longitud maxima de ciclo, en pasos del ATAJO. 30 tarda ~15 min
BLOQUE = 1 << 22    # de cuantos restos en cuantos se trabaja
K_FUERZA = 20       # hasta que k se compara contra la fuerza bruta
N_FUERZA = 100000   # hasta que n llega la fuerza bruta
MUESTRAS = 10000    # cuantos casos al azar para probar la formula de Terras
SEMILLA = 20260730  # para que el muestreo sea repetible

# int64 aguanta hasta 3*3^k < 2^63, o sea k <= 38. Mas arriba haria falta
# aritmetica de Python y el barrido dejaria de ser vectorizado.
if K_MAX > 38:
    raise SystemExit("K_MAX > 38 desbordaria int64 en 3*T^k(r). No sigas.")


# ---------------------------------------------------------------------------
# El mapa del atajo, en Python puro y con enteros exactos
# ---------------------------------------------------------------------------

def T(n):
    """Un paso del mapa del atajo."""
    return n >> 1 if n % 2 == 0 else (3 * n + 1) >> 1


def T_iterado(n, k):
    """T aplicado k veces."""
    for _ in range(k):
        n = n >> 1 if n % 2 == 0 else (3 * n + 1) >> 1
    return n


def T_y_S(n, k):
    """(T^k(n), S_k(n)): donde cae y cuantos pasos impares gasto."""
    S = 0
    for _ in range(k):
        if n & 1:
            S += 1
            n = (3 * n + 1) >> 1
        else:
            n >>= 1
    return n, S


def periodo_minimo(n, tope):
    """El periodo mas chico p <= tope con T^p(n) = n, o 0 si no cicla."""
    v = n
    for p in range(1, tope + 1):
        v = v >> 1 if v % 2 == 0 else (3 * v + 1) >> 1
        if v == n:
            return p
    return 0


# ---------------------------------------------------------------------------
# El barrido vectorizado, en bloques
# ---------------------------------------------------------------------------

def _revisa(k, r, v, S, pot3, conteos, candidatos, divis_por_S, enteros):
    """Resuelve m = (r - T^k(r)) / (3^S(r) - 2^k) para un trozo de restos.

    Va contando cuantos sobreviven a cada condicion por separado, que es lo
    que interesa: primero que m sea entero, luego que sea >= 0, y luego que
    n = 2^k*m + r sea >= 1.
    """
    den = pot3[S] - np.int64(1 << k)
    if not den.all():
        raise SystemExit("denominador 3^S - 2^k nulo: eso es imposible, hay un bug")
    num = r - v

    divide = (num % den) == 0
    cuantos_dividen = int(divide.sum())
    conteos[k][0] += cuantos_dividen
    # los que dividen porque el numerador es 0, o sea los r que YA son un
    # punto del ciclo (T^k(r) = r con r < 2^k). Esos no son azar y hay que
    # descontarlos antes de comparar con la heuristica de divisibilidad.
    conteos[k][3] += int((num == 0).sum())

    if cuantos_dividen:
        valores, cuentas = np.unique(S[divide], return_counts=True)
        for s_val, c in zip(valores, cuentas):
            s_val = int(s_val)
            divis_por_S[k][s_val] = divis_por_S[k].get(s_val, 0) + int(c)

    m = np.zeros_like(num)
    np.floor_divide(num, den, out=m, where=divide)
    positivo = divide & (m >= 0)
    conteos[k][1] += int(positivo.sum())

    # los que dividen son POQUISIMOS (nunca mas de 15 en todo el barrido), asi
    # que se pueden recorrer en Python y quedarse con el n exacto de cada uno,
    # incluidos los de m < 0. Esos no son basura: son los ciclos de T sobre los
    # enteros NEGATIVOS, y conviene verlos.
    for i in np.flatnonzero(divide):
        mm = int(m[i])
        rr = int(r[i])
        ss = int(S[i])
        n = (1 << k) * mm + rr        # en enteros de Python: aqui no se desborda
        enteros[k].append(n)
        if mm >= 0 and n >= 1:
            conteos[k][2] += 1
            candidatos[k].append((rr, ss, mm, n))


def barrido(K, bloque=BLOQUE):
    """Barre los 2^k restos de cada k = 1..K y devuelve cuatro cosas.

    conteos[k]      = [m entero, y m >= 0, y n >= 1, y de los primeros
                       cuantos tenian numerador 0]
    candidatos[k]   = lista de (r, S_k(r), m, n) de los que sobreviven todo
    divis_por_S[k]  = {S: cuantos restos con ese S pasaron la division}
    enteros[k]      = TODOS los n de Z con T^k(n) = n que aparecieron,
                      negativos incluidos
    """
    pot3 = np.array([3 ** i for i in range(K + 1)], dtype=np.int64)
    conteos = {k: [0, 0, 0, 0] for k in range(1, K + 1)}
    candidatos = {k: [] for k in range(1, K + 1)}
    divis_por_S = {k: {} for k in range(1, K + 1)}
    enteros = {k: [] for k in range(1, K + 1)}

    total = 1 << K
    for lo in range(0, total, bloque):
        hi = min(lo + bloque, total)
        r = np.arange(lo, hi, dtype=np.int64)
        v = r.copy()
        S = np.zeros(hi - lo, dtype=np.int8)

        for k in range(1, K + 1):
            # un paso de T sobre el bloque entero, todo en sitio
            impar = (v & 1).astype(bool)
            S += impar
            rama_impar = 3 * v + 1
            rama_impar >>= 1
            v >>= 1
            np.copyto(v, rama_impar, where=impar)
            del rama_impar, impar

            # a este k le tocan los restos r < 2^k, y nada mas
            if lo >= (1 << k):
                continue
            fin = min(hi, 1 << k) - lo
            _revisa(k, r[:fin], v[:fin], S[:fin],
                    pot3, conteos, candidatos, divis_por_S, enteros)

        del r, v, S

    return conteos, candidatos, divis_por_S, enteros


# ---------------------------------------------------------------------------
# Las convergentes y semiconvergentes de log2(3), exactas
# ---------------------------------------------------------------------------

getcontext().prec = 60
ALFA = Decimal(3).ln() / Decimal(2).ln()       # log2(3) a 60 cifras


def fraccion_continua(x, cuantos):
    """Los primeros terminos de la fraccion continua de x."""
    terminos = []
    for _ in range(cuantos):
        a = int(x)                              # x > 0, o sea que int() es floor
        terminos.append(a)
        x = x - a
        if x == 0:
            break
        x = 1 / x
    return terminos


def convergentes_y_semi(cf):
    """Todas las (p, q) con p/q convergente o semiconvergente de la fraccion.

    Devuelve lista de (p, q, es_convergente).
    """
    salida = []
    hm2, hm1 = 0, 1
    km2, km1 = 1, 0
    for a in cf:
        for j in range(1, a + 1):
            salida.append((j * hm1 + hm2, j * km1 + km2, j == a))
        hi, ki = a * hm1 + hm2, a * km1 + km2
        hm2, hm1 = hm1, hi
        km2, km1 = km1, ki
    return salida


CF = fraccion_continua(ALFA, 12)
SEMI = convergentes_y_semi(CF)
SEMI_PARES = {(p, q) for p, q, _ in SEMI}


def es_semiconvergente(B, A):
    """B/A (que es k/S) cae en la lista de convergentes y semiconvergentes?"""
    if A == 0:
        return False
    g = math.gcd(A, B)
    return (B // g, A // g) in SEMI_PARES


# ===========================================================================
# COMPROBACION 1 -- la formula de Terras contra la iteracion cruda
# ===========================================================================
#
# Todo lo demas cuelga de esta formula. Si falla, no hay nada que barrer.

print("COMPROBACION 1 -- la formula de Terras contra la iteracion cruda\n")
print("  Se exige:  T^k(2^k*m + r)  ==  3^{S_k(r)} * m  +  T^k(r)")
print(f"  {MUESTRAS:,} casos al azar, enteros exactos de Python, sin numpy.\n")

azar = random.Random(SEMILLA)
K_MUESTRA = [1, 2, 3, 5, 8, 12, 17, 20, 25, min(30, K_MAX)]
fallos_formula = 0
probados_formula = 0
peor_ejemplo = None

for _ in range(MUESTRAS):
    k = azar.choice(K_MUESTRA)
    r = azar.randrange(0, 1 << k)
    m = azar.randrange(0, 1000)
    Tk_r, S_r = T_y_S(r, k)
    por_formula = 3 ** S_r * m + Tk_r
    por_iteracion = T_iterado((1 << k) * m + r, k)
    probados_formula += 1
    if por_formula != por_iteracion:
        fallos_formula += 1
        if peor_ejemplo is None:
            peor_ejemplo = (k, r, m, por_formula, por_iteracion)

print(f"  casos probados: {probados_formula:,}   fallos: {fallos_formula}")
if fallos_formula:
    print(f"  ejemplo: {peor_ejemplo}")
    raise SystemExit("La formula de Terras no coincide con la iteracion. No sigas.")
print("  0 fallos. La recta en m es exacta, y con ella la ecuacion del ciclo.")


# ===========================================================================
# COMPROBACION 2 -- el ciclo trivial TIENE que aparecer
# ===========================================================================
#
# Con el atajo el ciclo 1 -> 2 -> 1 mide 2 pasos, asi que tiene que salir en
# k = 2 y en todos sus multiplos (como vueltas repetidas), y en ningun k impar.

print("\n\nCOMPROBACION 2 -- el ciclo trivial tiene que salir en k = 2, 4, 6, ...\n")

conteos_chico, candidatos_chico, _, _ = barrido(K_FUERZA)

fallos_trivial = 0
extras_chico = []
for k in range(1, K_FUERZA + 1):
    salieron = sorted({n for _, _, _, n in candidatos_chico[k]})
    esperado = [1, 2] if k % 2 == 0 else []
    # lo que se EXIGE: que el trivial este en los k pares. Que aparezca algo
    # mas no se trata como fallo del codigo (seria un hallazgo), se avisa.
    falta = (k % 2 == 0) and not {1, 2} <= set(salieron)
    sobra = [n for n in salieron if n not in (1, 2)]
    if falta:
        fallos_trivial += 1
    if sobra:
        extras_chico.append((k, sobra))
    marca = "FALTA EL TRIVIAL" if falta else ("ok" if not sobra else "hay extras")
    if k <= 8 or k % 4 == 0:
        print(f"  k = {k:>2}   candidatos con n >= 1: {str(salieron):<12} "
              f"esperado: {str(esperado):<12} {marca}")

print(f"\n  k revisados: {K_FUERZA}   k pares sin el ciclo trivial: {fallos_trivial}")
if fallos_trivial:
    raise SystemExit("El barrido no encuentra el ciclo trivial donde debe. Esta mal.")
if extras_chico:
    print(f"  AVISO: aparecieron candidatos que no son 1 ni 2: {extras_chico}")
print("  El 1 y el 2 aparecen en los diez k pares y en ninguno de los impares.")
print("  (son el mismo ciclo dando 1, 2, 3, ... vueltas: n = 2^k*0 + r con m = 0)")


# ===========================================================================
# COMPROBACION 3 -- contra la fuerza bruta, hasta 100.000
# ===========================================================================
#
# Los dos sentidos: todo n <= N_FUERZA que cicle con periodo k tiene que estar
# en la lista de candidatos, y todo candidato con n <= N_FUERZA tiene que
# ciclar de verdad.

print(f"\n\nCOMPROBACION 3 -- fuerza bruta: todo n <= {N_FUERZA:,}, todo k <= {K_FUERZA}\n")

bruto = {k: set() for k in range(1, K_FUERZA + 1)}
for n in range(1, N_FUERZA + 1):
    v = n
    for k in range(1, K_FUERZA + 1):
        v = v >> 1 if v % 2 == 0 else (3 * v + 1) >> 1
        if v == n:
            bruto[k].add(n)

fallos_bruta = 0
faltan_total = 0
sobran_total = 0
for k in range(1, K_FUERZA + 1):
    mios = {n for _, _, _, n in candidatos_chico[k] if n <= N_FUERZA}
    faltan = bruto[k] - mios
    sobran = mios - bruto[k]
    faltan_total += len(faltan)
    sobran_total += len(sobran)
    if faltan or sobran:
        fallos_bruta += 1
        print(f"  k = {k}: faltan {sorted(faltan)}   sobran {sorted(sobran)}")

comparados = sum(len(b) for b in bruto.values())
print(f"  numeros ciclantes encontrados a mano: {comparados} "
      f"(en los {K_FUERZA} valores de k)")
print(f"  el barrido no encontro: {faltan_total}    invento: {sobran_total}")
if fallos_bruta:
    raise SystemExit("El barrido no coincide con la fuerza bruta. No sigas.")
print(f"  0 discrepancias en los {K_FUERZA} k, contra {N_FUERZA:,} numeros cada uno.")


# ===========================================================================
# EL BARRIDO
# ===========================================================================

print(f"\n\nEL BARRIDO -- los 2^k restos de cada k, hasta k = {K_MAX}\n")
print("  Cada resto da como mucho un candidato. Las tres columnas son las tres")
print("  condiciones, en orden: que m salga entero, que ademas sea >= 0, y que")
print("  ademas n = 2^k*m + r sea >= 1 (o sea, que no sea el 0).\n")

conteos, candidatos, divis_por_S, enteros = barrido(K_MAX)

print(f"  {'k':>3} {'restos 2^k':>15} {'m entero':>12} {'y m >= 0':>10} "
      f"{'y n >= 1':>10} {'supervivientes':>16}")
print(f"  {'-'*3} {'-'*15} {'-'*12} {'-'*10} {'-'*10} {'-'*16}")

for k in range(1, K_MAX + 1):
    a, b, c, _ = conteos[k]
    ns = sorted({n for _, _, _, n in candidatos[k]})
    texto = ", ".join(str(n) for n in ns) if ns else "-"
    print(f"  {k:>3} {1 << k:>15,} {a:>12,} {b:>10,} {c:>10,} {texto:>16}")

total_supervivientes = sum(conteos[k][2] for k in range(1, K_MAX + 1))
todos_los_n = sorted({n for k in range(1, K_MAX + 1)
                      for _, _, _, n in candidatos[k]})
print(f"\n  restos barridos en total: {sum(1 << k for k in range(1, K_MAX + 1)):,}")
print(f"  candidatos que sobreviven las tres condiciones: {total_supervivientes}")
print(f"  numeros distintos entre ellos: {todos_los_n}")


# ===========================================================================
# LOS SUPERVIVIENTES, UNO POR UNO
# ===========================================================================

print("\n\nLOS SUPERVIVIENTES, VERIFICADOS POR ITERACION\n")
print("  Cada uno se vuelve a iterar con enteros de Python, sin usar la formula.\n")
print(f"  {'k':>3} {'resto r':>10} {'A = S_k(r)':>11} {'m':>4} {'n':>8} "
      f"{'T^k(n) = n?':>12} {'periodo':>8} {'B/A':>8} {'semiconv?':>10}")
print(f"  {'-'*3} {'-'*10} {'-'*11} {'-'*4} {'-'*8} {'-'*12} {'-'*8} {'-'*8} {'-'*10}")

fallos_supervivientes = 0
fuera_de_convergentes = []
for k in range(1, K_MAX + 1):
    for r, S, m, n in sorted(candidatos[k], key=lambda t: t[3]):
        cierra = T_iterado(n, k) == n
        p = periodo_minimo(n, k)
        A, B = S, k
        g = math.gcd(A, B)
        razon = f"{B // g}/{A // g}" if A else "-"
        semi = es_semiconvergente(B, A)
        if not cierra:
            fallos_supervivientes += 1
        if not semi:
            fuera_de_convergentes.append((k, r, A, B, n))
        print(f"  {k:>3} {r:>10} {S:>11} {m:>4} {n:>8} {str(cierra):>12} "
              f"{p:>8} {razon:>8} {str(semi):>10}")

print(f"\n  supervivientes que NO ciclan al iterarlos: {fallos_supervivientes}")
if fallos_supervivientes:
    raise SystemExit("Un superviviente no cicla. La ecuacion o el codigo estan mal.")

print("\n  PREDICCION ESCRITA ANTES DE MEDIR: cero supervivientes salvo el ciclo")
print("  trivial 1-2 y sus repeticiones.")
if set(todos_los_n) <= {1, 2}:
    print("  RESULTADO: se cumple. Los unicos n que sobreviven son el 1 y el 2,")
    print("  y su periodo minimo es 2 en todos los k donde aparecen.")
else:
    print("  RESULTADO: NO se cumple. Aparecio algo mas. Verificalo tres veces")
    print(f"  antes de contarselo a nadie: {todos_los_n}")


# ===========================================================================
# EL CRUCE CON EL FILTRO DE log2(3)
# ===========================================================================

print("\n\nEL CRUCE CON EL FILTRO DE log2(3)\n")
print(f"  log2(3) = {str(ALFA)[:22]}")
print(f"  fraccion continua: {CF}")
print("\n  Convergentes (marcadas *) y semiconvergentes, escritas como B/A")
print("  o sea k/S, que es la razon de divisiones por multiplicacion:\n")
linea = []
for p, q, es_conv in SEMI:
    if q <= 200:
        linea.append(f"{p}/{q}{'*' if es_conv else ''}")
print("    " + "  ".join(linea))

print("\n  Los A que caben en este barrido (A = S <= k <= K_MAX):")
utiles = [(p, q, c) for p, q, c in SEMI if q <= K_MAX and p <= K_MAX]
for p, q, c in utiles:
    print(f"    A = {q:>3}  B = {p:>3}   B/A = {p/q:.7f}   "
          f"error contra log2(3): {abs(Decimal(p)/q - ALFA):.2e}   "
          f"{'convergente' if c else 'semiconvergente'}")

print("\n  LOS SUPERVIVIENTES CONTRA EL FILTRO:")
print(f"    supervivientes cuyo (A,B) NO es convergente ni semiconvergente: "
      f"{len(fuera_de_convergentes)}")
if fuera_de_convergentes:
    print("    ESO SERIA UNA CORRECCION AL REPO. Los casos:")
    for k, r, A, B, n in fuera_de_convergentes:
        print(f"      k={k} r={r} (A,B)=({A},{B}) n={n}")
else:
    print("    0 casos fuera. Los dos filtros dicen lo mismo.")
    print("    HONESTIDAD: con un solo ciclo superviviente esta comprobacion")
    print("    tiene casi cero poder. Es consistencia, no evidencia.")

# --- el mecanismo: por que el filtro de log2(3) es el tamano del denominador

print("\n  LAS CASILLAS PELIGROSAS DE CADA k. 'S del menor |den|' es el S que")
print("  hace 3^S mas parecido a 2^k, o sea donde el filtro de log2(3) dice que")
print("  habria que mirar. 'dividen' son los restos que pasan la division.\n")
print(f"  {'k':>3} {'S menor |den|':>14} {'|3^S - 2^k|':>16} {'k/S':>9} "
      f"{'semi?':>6} {'dividen':>8} {'de ese S':>9}")
print(f"  {'-'*3} {'-'*14} {'-'*16} {'-'*9} {'-'*6} {'-'*8} {'-'*9}")

for k in range(2, K_MAX + 1):
    mejor_S = min(range(0, k + 1), key=lambda s: abs(3 ** s - (1 << k)))
    den = abs(3 ** mejor_S - (1 << k))
    razon = k / mejor_S if mejor_S else float("inf")
    semi = es_semiconvergente(k, mejor_S)
    print(f"  {k:>3} {mejor_S:>14} {den:>16,} {razon:>9.5f} {str(semi):>6} "
          f"{conteos[k][0]:>8,} {divis_por_S[k].get(mejor_S, 0):>9,}")


# ===========================================================================
# LO QUE PASA LA DIVISION NO ES AZAR: SON LOS CICLOS DE COLLATZ SOBRE Z
# ===========================================================================
#
# CORRECCION A UNA VERSION ANTERIOR DE ESTE ARCHIVO, escrita despues de mirar
# la columna 'dividen' de arriba. Decia que esos restos eran coincidencias de
# divisibilidad y que su numero seguia la heuristica C(k,S)/|3^S - 2^k|. ES
# FALSO, y la columna lo delataba sola: no se parece a ruido, tiene periodo 3
# y dos picos exactos en k = 11 y k = 22.
#
# La razon es que la ecuacion m = (r - T^k(r)) / (3^S(r) - 2^k) no distingue
# el signo de m. Un m negativo tambien es una solucion entera, y da un n
# NEGATIVO con T^k(n) = n. O sea que este barrido, sin proponerselo, esta
# resolviendo el problema sobre TODO Z, no solo sobre los positivos.
#
# Y sobre Z los ciclos de T conocidos son cuatro, que el repo ya tenia
# medidos en la seccion de los negativos (Collatz sobre Z<0 es el mapa 3n-1):
#
#     {0}                              periodo 1
#     {1, 2}                           periodo 2
#     {-1}                             periodo 1
#     {-5, -7, -10}                    periodo 3
#     {-17, ... , -34}                 periodo 11
#
# Un n con T^k(n) = n aparece exactamente en los k multiplos de su periodo, y
# aporta un resto por cada elemento del ciclo. Luego, sin ajustar nada:
#
#     dividen(k)  =  2  +  2*[2 divide a k]  +  3*[3|k]  +  11*[11|k]
#
# (el 2 fijo son el 0 y el -1, que son puntos fijos y salen en todo k).

print("\n\nLO QUE PASA LA DIVISION NO ES AZAR: SON LOS CICLOS SOBRE Z\n")
print("  La ecuacion no mira el signo de m. Un m negativo tambien es solucion,")
print("  y da un n NEGATIVO que cicla. O sea que este barrido, sin buscarlo,")
print("  resuelve el problema sobre TODO Z. Y sobre Z los ciclos conocidos son")
print("  cuatro, los mismos que el repo ya tenia medidos en 3n-1:\n")

CICLOS_Z = []
for arranque in (0, 1, -1, -5, -17):
    c = [arranque]
    x = T(arranque)
    while x != arranque:
        c.append(x)
        x = T(x)
    CICLOS_Z.append(c)
    print(f"    periodo {len(c):>2}   {c}")

print("\n  Cada uno aporta un resto por elemento, en los k multiplos de su")
print("  periodo. Sin ajustar nada eso predice la columna 'dividen':\n")
print(f"    dividen(k) = 2 + 2*[2|k] + 3*[3|k] + 11*[11|k]\n")
print(f"  {'k':>3} {'dividen medido':>15} {'predicho':>10} {'los n que salieron':>60}")
print(f"  {'-'*3} {'-'*15} {'-'*10} {'-'*60}")

fallos_z = 0
conocidos = {n for c in CICLOS_Z for n in c}
inesperados = set()
for k in range(1, K_MAX + 1):
    predicho = sum(len(c) for c in CICLOS_Z if k % len(c) == 0)
    medido = conteos[k][0]
    salieron = sorted(enteros[k])
    if predicho != medido or len(salieron) != medido:
        fallos_z += 1
    inesperados |= set(salieron) - conocidos
    if k <= 12 or k % 6 == 0 or k in (11, 22):
        texto = str(salieron)
        print(f"  {k:>3} {medido:>15,} {predicho:>10,} {texto[:60]:>60}")

print(f"\n  k comprobados: {K_MAX}   desacuerdos entre medido y predicho: {fallos_z}")
print(f"  n encontrados que NO estan en los cuatro ciclos conocidos: "
      f"{sorted(inesperados) if inesperados else 0}")
if fallos_z or inesperados:
    print("  ATENCION: eso seria un ciclo nuevo sobre Z. Verificalo tres veces.")
else:
    print(f"  O sea: de los {sum(1 << k for k in range(1, K_MAX + 1)):,} restos barridos,")
    print("  TODOS los que pasan la division estan explicados, uno a uno, por los")
    print("  cuatro ciclos conocidos de Collatz sobre Z. Cero restos sin explicar.")
    print("\n  Y eso es un resultado mejor que el que se buscaba: el barrido no solo")
    print("  descarta ciclos positivos hasta k = " + str(K_MAX) + ", tambien RECUPERA los tres")
    print("  ciclos negativos sin que se le haya hablado nunca de los negativos.")
    print("  El de periodo 11 es el [-17, ..., -34], que en coordenadas (A,B) es")
    print("  (7, 11) -- una de las casillas de la tabla de arriba, la del lado")
    print("  2^B < 3^A. La tabla de convergentes predijo donde estaba antes de")
    print("  encontrarlo, y el barrido lo encontro ahi.")

# --- y donde podrian esconderse, si K_MAX fuera mas grande

print("\n  DONDE HABRIA QUE MIRAR SI SE SUBIERA K_MAX (las casillas peligrosas,")
print("  o sea las que tienen el denominador mas chico):\n")
print(f"    {'B = k':>6} {'A = S':>6} {'|3^A - 2^B|':>28} {'lado':>10}  tipo")
peligrosas = sorted(((abs(3 ** q - (1 << p)), p, q, c) for p, q, c in SEMI
                     if p <= 200 and q <= 200))[:10]
utiles_para_3n1 = []
for den, B, A, c in peligrosas:
    arriba = (1 << B) > 3 ** A
    if arriba:
        utiles_para_3n1.append((A, B))
    print(f"    {B:>6} {A:>6} {den:>28,} {'2^B > 3^A' if arriba else '2^B < 3^A':>10}"
          f"  {'convergente' if c else 'semiconvergente'}")

print("\n  Y AQUI SE CRUZAN DOS COSAS QUE EL REPO YA TENIA POR SEPARADO.")
print("  Solo la mitad de esas casillas puede alojar un ciclo de 3n+1: en un")
print("  ciclo la constante C de la identidad (A,B) es positiva, luego 2^B > 3^A")
print("  (y las de 2^B < 3^A son las que alojan los ciclos de 3n-1, que existen).")
print("  Filtrando por eso quedan, en orden:")
print(f"    {utiles_para_3n1}")
print("  Escritas como B: " + ", ".join(str(B) for _, B in utiles_para_3n1))
print("\n  Esa es exactamente la tabla C de Terras (1976), que CLAUDE.md ya tenia")
print("  copiada:  k = 1, 2, 5, 8, 27, 46, 65, 149, 233, ...")
print("            b = 0, 1, 3, 5, 17, 29, 41,  94, 147, ...")
print("  Recalculada aqui por un camino distinto (fraccion continua de log2(3)")
print("  con Decimal a 60 cifras, no records de 3^b/2^k), y sale la misma lista.")
print("  La fila (A,B) = (41,65) es la misma que el repo ya tenia anotada para")
print("  el 221, que falla por ocho divisiones.")

otro_lado = [f"{B}/{A}" for _, B, A, _ in peligrosas if (1 << B) < 3 ** A][:3]
print("\n  Y el descarte de arriba tampoco es gratis: las tres primeras casillas")
print(f"  del OTRO lado son B/A = {', '.join(otro_lado)}, que son exactamente los tres")
print("  ciclos de 3n-1 que el repo ya tenia medidos (los negativos de Collatz).")
print("  O sea que la mitad que este barrido descarta no esta vacia: esta llena,")
print("  pero de la otra regla. Es la mejor comprobacion de que el corte por el")
print("  signo de C esta bien puesto y no es una excusa para tirar filas.")


# ===========================================================================
# EL LIMITE HONESTO
# ===========================================================================

print("\n\nEL LIMITE HONESTO -- que se descarto exactamente, y que falta\n")
print(f"  LO QUE ESTE BARRIDO DESCARTA, con demostracion y sin muestreo:")
print(f"    no existe ningun entero n >= 1, por grande que sea, cuya orbita en")
print(f"    el mapa del ATAJO sea un ciclo de longitud k <= {K_MAX},")
print(f"    salvo el ciclo trivial 1 -> 2 -> 1.")
print(f"    Restos examinados: {sum(1 << k for k in range(1, K_MAX + 1)):,}, uno a uno,")
print(f"    con aritmetica entera exacta. Cada resto cubre infinitos numeros.")

print(f"\n  TRADUCIDO AL MAPA CLASICO (3n+1 sin dividir), Y CON CUIDADO:")
print(f"    un paso del atajo es una division, asi que k es exactamente B, el")
print(f"    numero de veces que se aplica n/2. Entonces lo descartado es:")
print(f"      todo ciclo clasico con B <= {K_MAX} divisiones, sea cual sea su largo.")
print(f"    Y como el largo total es A + B >= B, de ahi sale sin condiciones:")
print(f"      no hay ningun ciclo clasico de largo total <= {K_MAX}.")
print(f"    NO se puede decir '<= {2*K_MAX} pasos clasicos': un ciclo de largo {2*K_MAX} con")
print(f"    pocos pasos impares tendria B > {K_MAX} y se queda fuera del barrido.")
print(f"    (Terras cuenta en las mismas unidades que k, asi que las")
print(f"    comparaciones de abajo son de manzanas con manzanas.)")

print(f"\n  LO QUE YA HABIA, y con cuanta ventaja:")
print(f"    Terras 1976        descarto ciclos hasta periodo 2.592 (mismo tipo")
print(f"                       de argumento, con la tabla de convergentes), CON")
print(f"                       LA FUERZA BRUTA QUE HABIA EN 1976. Ese 2.592 es")
print(f"                       cifra historica, NO la frontera: la frontera se")
print(f"                       mueve con X0, y con el X0 = 2^71 de Barina 2025")
print(f"                       el mismo argumento llega a 114.208.327.603")
print(f"                       (186.265.759.593 pasos clasicos). Con X = 10^6,")
print(f"                       un minuto de CPU, ya alcanza 4.700.")
print(f"                       Nuestro {K_MAX} no es el 1,2% de nada: esta NUEVE")
print(f"                       ORDENES DE MAGNITUD por debajo de la frontera de")
print(f"                       hoy, y cada escalon cuesta el doble que el")
print(f"                       anterior. No es cuestion de correr mas tiempo.")
print(f"    Simons-de Weger    todo m-ciclo tiene m >= 76, o sea que descartan")
print(f"                       m <= 75 (2005). El '68' que decia aqui es la")
print(f"                       cifra que imprime el libro de 2010, no la suya.")
print(f"    Hercher 2023       no hay m-ciclos con m <= 91, donde m es el numero")
print(f"                       de minimos locales del ciclo. Eso es MUCHISIMO mas")
print(f"                       fuerte: no acota la longitud, acota la forma, y")
print(f"                       vale para ciclos de longitud infinita.")
print(f"    Barina 2025        verificacion por fuerza bruta hasta 2^71.")

print(f"\n  ESTO NO APORTA NADA A LA LITERATURA. Es rederivacion.")
print(f"  Lo unico que tiene de propio es que junta cuatro piezas del repo que")
print(f"  hasta ahora estaban sueltas -- la identidad de Terras de clasesfusion,")
print(f"  la malla de restos de mallaresiduos, las coordenadas (A,B) de")
print(f"  collazmalla y la tabla de convergentes -- y comprueba que encajan.")
print(f"  El techo del repo sigue siendo el que dice CLAUDE.md: rederivacion")
print(f"  independiente bien verificada. Esto es exactamente eso, ni mas ni menos.")

print(f"\n  Y EL LIMITE DE FONDO, que no lo arregla ningun K_MAX:")
print(f"  este metodo cuesta 2^k y descarta longitud k. Para pisar territorio")
print(f"  virgen habria que barrer 2^114208327603 casillas -- no 2^2592, que era")
print(f"  la cifra de 1976. La via buena no es barrer mas")
print(f"  restos: es acotar la FORMA del ciclo (cuantos minimos locales), que es")
print(f"  lo que hacen Simons-de Weger y Hercher, y ahi este barrido no llega.")
