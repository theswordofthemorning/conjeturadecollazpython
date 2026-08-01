# otramedicion.py
#
# LA MALLA DE LOS ONCE HILOS, EXTENDIDA A LOS DOS LADOS, Y CUATRO PREGUNTAS.
#
# guardarhilos.py metio en hilos.db los once numeros 100000..100010 y cruzo cada
# paso contra cada paso. Aquello preguntaba EN QUE PASO coinciden. Esto pregunta
# otras cuatro cosas, y extiende la malla:
#
#   - hacia el lado POSITIVO y hacia el NEGATIVO alrededor de los once, o sea
#     100000-VENTANA .. 100010+VENTANA
#   - y a los ENTEROS NEGATIVOS, que por el resultado ya establecido del repo son
#     el mapa 3m-1 sobre los positivos, y no terminan en 1 sino en uno de los
#     tres ciclos conocidos
#
# LAS CUATRO PREGUNTAS, tal como se plantearon:
#
#   P1. Entre el hilo 7 y el hilo 8, en los pasos 20 y 21: que distancia hay
#       entre los dos numeros?
#   P2. En que cantidad de pares e impares estan todas las secuencias de la malla?
#   P3. La relacion de pares e impares genera un patron que indique COMO se
#       generan los numeros?
#   P4. Cual es la raiz cuadrada menos 1 del mayor numero de cada sucesion?
#
# AVISO DE METODO, que este repo se exige: una pregunta no se contesta con un
# numero, se contesta con un numero Y UN CONTROL. Si una relacion aparece en la
# malla hay que comprobar que NO aparece igual en un conjunto de control; si
# aparece en los dos, la relacion la pone la maquinaria, no Collatz. Las cuatro
# respuestas de abajo llevan su control, y dos de ellas salen NEGATIVAS.
#
# Las comprobaciones van ANTES de las respuestas y cortan con SystemExit.

import math
import os
import sqlite3
from fractions import Fraction

# ---------------------------------------------------------------------------
VENTANA = 20          # cuantos numeros a cada lado de los once originales
BASE_LO = 100000      # el primer hilo de hilos.db
BASE_HI = 100010      # el ultimo
HILO_A = 7            # para la pregunta 1 (la base indexa desde 1: hilo 7 = 100006)
HILO_B = 8
PASOS_MIRA = (20, 21)
ARCHIVO = "hilos.db"
TOPE_CICLO = 100000   # corte de seguridad al buscar ciclos en los negativos
# ---------------------------------------------------------------------------


def secuencia_de(n):
    """Trayectoria clasica de un entero POSITIVO hasta el 1, incluido."""
    v = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        v.append(n)
    return v


def secuencia_neg(n):
    """Trayectoria de un entero NEGATIVO hasta cerrar ciclo.

    Devuelve (cola, ciclo). No divide nunca un negativo con //, que redondearia
    hacia abajo: se separa el signo y se opera con la magnitud.
    """
    vistos = {}
    v = []
    k = 0
    while n not in vistos and k < TOPE_CICLO:
        vistos[n] = k
        v.append(n)
        m = -n                       # magnitud, siempre positiva
        if m % 2 == 0:
            n = -(m // 2)
        else:
            n = -(3 * m - 1)         # 3n+1 con n negativo es -(3m-1)
        k += 1
    if n not in vistos:
        raise SystemExit("FALLO: no cerro ciclo dentro de TOPE_CICLO")
    corte = vistos[n]
    return v[:corte], v[corte:]


def cuenta(v):
    """(impares, pares) de una trayectoria, sin contar el ultimo valor."""
    impares = sum(1 for x in v[:-1] if x % 2)
    return impares, len(v) - 1 - impares


# ===========================================================================
# COMPROBACION 1 -- los once hilos calculados aqui tienen que salir IDENTICOS
# a lo que ya esta guardado en hilos.db. Si no, todo lo de abajo sobra.
# ===========================================================================
print("=" * 74)
print("OTRA MEDICION -- la malla de los once hilos, extendida")
print("=" * 74)

if not os.path.exists(ARCHIVO):
    raise SystemExit("FALLO: no existe " + ARCHIVO)

con = sqlite3.connect(ARCHIVO)
guardados = {}
for hilo, semilla, pasos, pico, impares, pares in con.execute(
        "select hilo, semilla, pasos, pico, impares, pares from hilos order by hilo"):
    guardados[hilo] = (semilla, pasos, pico, impares, pares)

fallos = 0
for hilo, (semilla, pasos, pico, impares, pares) in guardados.items():
    v = secuencia_de(semilla)
    i, p = cuenta(v)
    if (len(v) - 1, max(v), i, p) != (pasos, pico, impares, pares):
        fallos += 1
        print("  DESCUADRE en el hilo %d (%d)" % (hilo, semilla))

# y el paso a paso, no solo los totales
filas = con.execute("select hilo, k, valor from pasos order by hilo, k").fetchall()
cache = {h: secuencia_de(s) for h, (s, _, _, _, _) in guardados.items()}
for hilo, k, valor in filas:
    if cache[hilo][k] != valor:
        fallos += 1

print("\nCOMPROBACION 1 -- los once hilos contra hilos.db")
print("  hilos comparados : %d" % len(guardados))
print("  pasos comparados : %d" % len(filas))
print("  descuadres       : %d" % fallos)
if fallos:
    raise SystemExit("FALLO: lo calculado aqui no coincide con hilos.db. Se para.")

# ===========================================================================
# COMPROBACION 2 -- Collatz sobre los negativos ES el mapa 3m-1 sobre los
# positivos. El repo lo da por establecido; aqui se vuelve a comprobar porque
# la malla extendida se apoya en ello.
# ===========================================================================
def paso_3m_menos_1(m):
    return m // 2 if m % 2 == 0 else 3 * m - 1


fallos2 = 0
comparados = 0
for m in range(1, 3001):
    cola, ciclo = secuencia_neg(-m)
    x = m
    for n in cola + ciclo:
        if n != -x:
            fallos2 += 1
            break
        x = paso_3m_menos_1(x)
        comparados += 1

print("\nCOMPROBACION 2 -- los negativos son el mapa 3m-1")
print("  magnitudes probadas : 1..3000")
print("  pasos comparados    : %d" % comparados)
print("  fallos              : %d" % fallos2)
if fallos2:
    raise SystemExit("FALLO: la equivalencia con 3m-1 no se sostiene. Se para.")

# ===========================================================================
# LA MALLA EXTENDIDA
# ===========================================================================
positivos = list(range(BASE_LO - VENTANA, BASE_HI + VENTANA + 1))
malla = {}
for n in positivos:
    v = secuencia_de(n)
    i, p = cuenta(v)
    malla[n] = {"seq": v, "pasos": len(v) - 1, "pico": max(v), "I": i, "P": p}

negativos = {}
for n in positivos:
    cola, ciclo = secuencia_neg(-n)
    v = cola + ciclo
    i, p = cuenta(v + [v[0]])
    negativos[n] = {"cola": len(cola), "ciclo": len(ciclo),
                    "min": min(v), "I": i, "P": p}

print("\nLA MALLA")
print("  numeros positivos : %d   (de %d a %d)" % (
    len(positivos), positivos[0], positivos[-1]))
print("  los once de la base estan dentro : %s" % (
    all(n in malla for n in range(BASE_LO, BASE_HI + 1))))
print("  espejo negativo   : %d numeros, con sus tres ciclos" % len(negativos))

largos = {}
for n in negativos:
    largos.setdefault(negativos[n]["ciclo"], 0)
    largos[negativos[n]["ciclo"]] += 1
print("  ciclos de destino en el lado negativo (largo: cuantos) : %s" % (
    dict(sorted(largos.items()))))

# ===========================================================================
# PREGUNTA 1 -- hilo 7 contra hilo 8, en los pasos 20 y 21
# ===========================================================================
na = BASE_LO + (HILO_A - 1)
nb = BASE_LO + (HILO_B - 1)
sa, sb = malla[na]["seq"], malla[nb]["seq"]

print("\n" + "=" * 74)
print("PREGUNTA 1 -- hilo %d (%d) contra hilo %d (%d)" % (HILO_A, na, HILO_B, nb))
print("=" * 74)
print("  (la base indexa desde 1, asi que el hilo 7 es el %d)" % na)
print()
print("  %-6s %-14s %-14s %-14s %s" % ("paso", "hilo " + str(HILO_A),
                                       "hilo " + str(HILO_B), "distancia", "cociente"))
for k in range(17, 25):
    if k >= len(sa) or k >= len(sb):
        break
    d = abs(sa[k] - sb[k])
    q = "%.6f" % (sa[k] / sb[k]) if sb[k] else "-"
    marca = "  <--" if k in PASOS_MIRA else ""
    print("  %-6d %-14d %-14d %-14d %s%s" % (k, sa[k], sb[k], d, q, marca))

d20 = abs(sa[20] - sb[20])
d21 = abs(sa[21] - sb[21])
print()
print("  RESPUESTA. La distancia en el paso 20 (el anterior al 21) es %d," % d20)
print("             y en el paso 21 es %d." % d21)
print("             Arrancaron separados por %d." % abs(na - nb))

# el perfil entero, que es lo que da sentido al numero suelto
perfil = [abs(sa[k] - sb[k]) for k in range(min(len(sa), len(sb)))]
print()
print("  EL PERFIL ENTERO, que es lo que explica ese numero:")
print("    distancia inicial            : %d" % perfil[0])
print("    distancia maxima             : %d  (en el paso %d)" % (
    max(perfil), perfil.index(max(perfil))))
print("    primer paso con distancia 0  : %s" % (
    perfil.index(0) if 0 in perfil else "nunca dentro del tramo comun"))
print("    pasos totales de cada uno    : %d y %d" % (
    malla[na]["pasos"], malla[nb]["pasos"]))

# CONTROL: la distancia se multiplica por 3 en los impares y se parte en los
# pares, o sea que NO es informacion sobre Collatz: es la propia regla.
esperado = []
d = perfil[0]
ok = 0
for k in range(len(perfil) - 1):
    par_a = sa[k] % 2 == 0
    par_b = sb[k] % 2 == 0
    if par_a and par_b:
        pred = perfil[k] // 2 if perfil[k] % 2 == 0 else None
    elif (not par_a) and (not par_b):
        pred = 3 * perfil[k]
    else:
        pred = None
    if pred is not None and pred == perfil[k + 1]:
        ok += 1
    esperado.append(pred)
util = sum(1 for e in esperado if e is not None)
print()
print("  CONTROL. Mientras los dos hilos tienen la MISMA paridad, la distancia")
print("  no es un dato nuevo: se parte por 2 o se multiplica por 3, por la regla.")
print("    pasos con la misma paridad en los dos : %d de %d" % (util, len(esperado)))
print("    de esos, la distancia sale predicha   : %d" % ok)
print("    -> la distancia solo informa cuando las paridades SE SEPARAN.")

# ===========================================================================
# PREGUNTA 2 -- cuantos pares e impares tiene cada secuencia de la malla
# ===========================================================================
print("\n" + "=" * 74)
print("PREGUNTA 2 -- pares e impares de toda la malla")
print("=" * 74)

II = [malla[n]["I"] for n in positivos]
PP = [malla[n]["P"] for n in positivos]
SS = [malla[n]["pasos"] for n in positivos]

print("  %-10s %-8s %-8s %-8s %-10s %s" % (
    "", "minimo", "maximo", "media", "distintos", "rango"))
for nom, xs in (("impares (A)", II), ("pares  (B)", PP), ("pasos  (A+B)", SS)):
    print("  %-12s %-8d %-8d %-8.2f %-10d %d" % (
        nom, min(xs), max(xs), sum(xs) / len(xs), len(set(xs)),
        max(xs) - min(xs)))

tot_i, tot_p = sum(II), sum(PP)
print()
print("  AGREGADO de la malla entera (el estimador bueno, no la media de razones):")
print("    total impares      : %d" % tot_i)
print("    total pares        : %d" % tot_p)
print("    B/A agregado       : %.6f" % (tot_p / tot_i))
print("    fraccion impar     : %.6f   (el modelo clasico predice 1/3)" % (
    tot_i / (tot_i + tot_p)))
media_razones = sum(PP[j] / II[j] for j in range(len(II))) / len(II)
print("    B/A media de razones: %.6f   <- SESGADO por Jensen, no usar" % media_razones)

print()
print("  El lado NEGATIVO de la misma malla (mapa 3m-1):")
ti = sum(negativos[n]["I"] for n in positivos)
tp = sum(negativos[n]["P"] for n in positivos)
print("    total impares      : %d" % ti)
print("    total pares        : %d" % tp)
print("    B/A agregado       : %.6f" % (tp / ti))
print()
print("    CUIDADO CON ESTE NUMERO, que es facil de leer mal. El B/A de ~2 es")
print("    el valor TIPICO sobre trayectorias, y sale ~2 en los dos mapas: la")
print("    valuacion 2-adica media de 3n+-1 vale 2 en ambos casos.")
print("    NO es la condicion de ciclo. Esa es otra cantidad: en un CICLO de")
print("    3n+1 hace falta B/A > log2(3) = %.6f, y en uno de 3n-1, B/A por" % math.log2(3))
print("    DEBAJO. Los tres ciclos negativos dan B/A = 1/1, 3/2 y 11/7, los")
print("    tres por debajo de log2(3). Confundir el B/A tipico con el B/A de")
print("    ciclo es mezclar un promedio con una cota.")

# ===========================================================================
# PREGUNTA 3 -- la relacion pares/impares, genera un patron?
# ===========================================================================
print("\n" + "=" * 74)
print("PREGUNTA 3 -- la relacion pares/impares genera un patron?")
print("=" * 74)

print("\n  (a) LA PARTE QUE SI, Y ES EXACTA. No es estadistica: es una identidad.")
print()
print("      B*(ln2 - rho*ln3) = ln n + S     con rho = A/B")
print("      y S = suma de ln(1 + 1/(3x)) sobre los valores impares x")
print()
peor = 0.0
for n in positivos:
    v = malla[n]["seq"]
    A, B = malla[n]["I"], malla[n]["P"]
    S = sum(math.log(1 + 1.0 / (3 * x)) for x in v[:-1] if x % 2)
    izq = B * (math.log(2) - (A / B) * math.log(3))
    der = math.log(n) + S
    peor = max(peor, abs(izq - der) / der)
print("      comprobado en los %d numeros de la malla" % len(positivos))
print("      error relativo peor : %.2e   (ruido de coma flotante)" % peor)
print("      -> la cantidad de pares e impares DETERMINA los pasos, dado n.")

print("\n  (b) PERO NO DICE COMO SE GENERAN LOS NUMEROS. El control:")
grupos = {}
for n in positivos:
    grupos.setdefault(round(malla[n]["I"] / malla[n]["P"], 6), []).append(n)
repes = {r: v for r, v in grupos.items() if len(v) > 1}
print("      numeros con la MISMA razon rho : %d grupos" % len(repes))
igual = dist = 0
for r, ns in repes.items():
    pasos = {malla[n]["pasos"] for n in ns}
    if len(pasos) == 1:
        igual += 1
    else:
        dist += 1
print("        grupos donde ademas coinciden los pasos : %d" % igual)
print("        grupos donde NO coinciden               : %d" % dist)
print("      Dentro de esta malla todos los n valen ~100000, o sea que ln n es")
print("      casi constante y rho parece decidirlo todo. ES UN ESPEJISMO DE RANGO.")

print("\n  (c) EL MISMO ENSAYO CON UN CONTROL DE RANGO ANCHO:")
control = [27, 703, 9663, 100009, 626331, 837799, 8400511, 63728127]
print("      %-12s %-6s %-6s %-10s %-8s %s" % ("n", "A", "B", "rho", "pasos", "pasos/ln n"))
for n in control:
    v = secuencia_de(n)
    A, B = cuenta(v)
    print("      %-12d %-6d %-6d %-10.6f %-8d %.4f" % (
        n, A, B, A / B, len(v) - 1, (len(v) - 1) / math.log(n)))
print()
print("      Fijate en rho: entre el 27 y el 63728127 apenas se mueve (0,559 a")
print("      0,603), y sin embargo pasos/ln n va de 20 a 53. Lo que gobierna rho")
print("      es pasos/ln n MAS la correccion S/ln n, que en numeros chicos pesa")
print("      mucho (ln 27 = 3,3). Los PASOS crudos no los gobierna: dependen")
print("      tambien de ln n. Dos numeros con la misma rho y distinto tamano")
print("      tienen distintos pasos.")

print("\n  (d) Y LA RAZON POR LA QUE ESTO NO SIRVE PARA LA FORMULA:")
print("      para conocer rho hay que HABER TERMINADO la trayectoria. Es")
print("      contabilidad, no criterio. Un criterio se evalua sobre n mod 2^k,")
print("      en un espacio finito, sin correr nada -- como clasesfusion.py.")

# ===========================================================================
# PREGUNTA 4 -- la raiz cuadrada menos 1 del mayor numero
# ===========================================================================
print("\n" + "=" * 74)
print("PREGUNTA 4 -- raiz cuadrada del pico, menos 1")
print("=" * 74)
print()
print("  %-8s %-12s %-18s %-14s %s" % ("hilo", "n", "pico", "sqrt(pico)-1", "entera?"))
for h in range(1, 12):
    n = BASE_LO + h - 1
    pico = malla[n]["pico"]
    r = math.isqrt(pico)
    exacta = (r * r == pico)
    print("  %-8d %-12d %-18d %-14.4f %s" % (
        h, n, pico, math.sqrt(pico) - 1, "SI" if exacta else "no"))

cuadrados = [n for n in positivos
             if math.isqrt(malla[n]["pico"]) ** 2 == malla[n]["pico"]]
print()
print("  picos que son cuadrado perfecto en toda la malla : %d de %d" % (
    len(cuadrados), len(positivos)))
esperados = sum(1.0 / (2 * math.sqrt(malla[n]["pico"])) for n in positivos)
print("  esperados por puro azar                          : %.4f" % esperados)

print()
print("  VEREDICTO, y es negativo. sqrt(x)-1 es una biyeccion creciente sobre")
print("  los positivos: no puede contener NINGUNA informacion que el pico no")
print("  tenga ya. Cambiar de escala no crea estructura. Lo unico que podria")
print("  decir algo es que el pico tuviera forma especial -- y no la tiene:")
print("  %d cuadrados perfectos contra %.2f esperados por azar." % (
    len(cuadrados), esperados))
print()
print("  Lo que SI acota el pico es una cota demostrada, no una raiz:")
print("      n impar:  log2(pico/n) >= racha(n)*log2(3/2) + 1")
peor_h = None
for h in range(1, 12):
    n = BASE_LO + h - 1
    if n % 2 == 0:
        continue
    v = malla[n]["seq"]
    racha = 0
    x = n
    while x % 2:
        racha += 1
        x = (3 * x + 1) // 2
    izq = Fraction(malla[n]["pico"]) * Fraction(2) ** racha
    der = Fraction(2 * n) * Fraction(3) ** racha
    if izq < der:
        peor_h = n
print("      comprobada en forma entera exacta sobre los impares de la base:")
print("      fallos: %s" % ("0" if peor_h is None else "FALLA en " + str(peor_h)))
if peor_h is not None:
    raise SystemExit("FALLO: el piso de la altitud no se cumple. Se para.")

print("\n" + "=" * 74)
print("RESUMEN")
print("=" * 74)
print("  P1. La distancia entre el hilo 7 y el 8 en el paso 20 es %d y en el 21" % d20)
print("      es %d. Pero mientras comparten paridad la distancia la fija la" % d21)
print("      regla (x3 o /2), no Collatz: solo informa cuando se separan.")
print("  P2. La malla entera tiene %d impares y %d pares, B/A = %.6f." % (
    tot_i, tot_p, tot_p / tot_i))
print("  P3. SI hay patron y es exacto, pero es una IDENTIDAD, no una ley del")
print("      proceso, y solo se puede evaluar cuando la trayectoria ya termino.")
print("      El 'todo depende de rho' es un espejismo del rango estrecho.")
print("  P4. NEGATIVO. sqrt(pico)-1 es un cambio de escala biyectivo y no puede")
print("      crear informacion. Los picos no son cuadrados mas de lo que dicta")
print("      el azar.")
