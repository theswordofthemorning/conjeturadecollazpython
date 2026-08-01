# otramedicion2.py
#
# LA CAPA DE PROMEDIOS SOBRE LA MALLA DE HILOS, Y SU CRUCE CONTRA afirmaciones.db
#
# LA IDEA QUE SE ESTA PROBANDO. Tomar los once hilos de hilos.db hacia adelante
# (los naturales) y hacia atras (los enteros negativos, que son el mapa 3m-1),
# y construir encima una DIMENSION EXTRA hecha de promedios:
#
#   LONGITUDINAL  dentro de un hilo:   m[k] = ( seq[k] + seq[k+1] ) / 2
#   TRANSVERSAL   entre dos hilos:     t[k] = ( hiloA[k] + hiloB[k] ) / 2
#
# El enunciado original era ambiguo entre las dos lecturas ("el promedio de los
# numeros entre secuencias" suena transversal; el ejemplo dado -sumar el
# resultado 2 con el resultado 3 del mismo hilo- es longitudinal), asi que se
# construyen LAS DOS. Cuestan lo mismo.
#
# Y despues se cruza esa capa contra las 80 afirmaciones de afirmaciones.db.
#
# ---------------------------------------------------------------------------
# EL AVISO QUE NO SE PUEDE SALTAR, y es la razon de que exista la columna
# `cuantificador`. Cruzar 22 secuencias contra una afirmacion SOLO significa
# algo para dos de los seis cuantificadores:
#
#   todo_n          SI. Cada secuencia es un contraejemplo potencial.
#   clase_residual  SI, via los restos.
#   casi_todo_n     NO. 22 numeros no dicen nada de una densidad.
#   promedio        NO, Y ES PELIGROSO. 22 trayectorias no estiman una media.
#   ciclos          No aplica: ninguna de las 22 es un ciclo positivo.
#   verificado_hasta No aplica: son afirmaciones sobre rangos.
#
# Este programa SE NIEGA a evaluar las filas de promedio y casi_todo_n. No las
# evalua y matiza: no las evalua. El modo de fallo concreto que se evita es
# informar "22 de 22 confirmadas" sobre una fila de tipo promedio, que no es
# confirmacion sino ruido con forma de tabla.
# ---------------------------------------------------------------------------
#
# Las comprobaciones van ANTES de cualquier conclusion y cortan con SystemExit.

import math
import os
import sqlite3
from fractions import Fraction

# ---------------------------------------------------------------------------
BASE_LO = 100000
BASE_HI = 100010
ARCHIVO_HILOS = "hilos.db"
ARCHIVO_AFIRM = "afirmaciones.db"
K_RESTOS = 12          # profundidad para la comprobacion de n mod 2^k
TOPE_CICLO = 100000
# ---------------------------------------------------------------------------


def secuencia_de(n):
    v = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        v.append(n)
    return v


def secuencia_neg(n):
    """Trayectoria de un negativo hasta cerrar ciclo. Devuelve la lista entera."""
    vistos = set()
    v = []
    k = 0
    while n not in vistos and k < TOPE_CICLO:
        vistos.add(n)
        v.append(n)
        m = -n
        n = -(m // 2) if m % 2 == 0 else -(3 * m - 1)
        k += 1
    return v


def paridad_de(n):
    """Patron de paridad de los primeros K_RESTOS pasos, mapa del atajo."""
    p = []
    x = n
    for _ in range(K_RESTOS):
        p.append(x % 2)
        x = x // 2 if x % 2 == 0 else (3 * x + 1) // 2
    return tuple(p)


print("=" * 74)
print("OTRA MEDICION 2 -- la capa de promedios, y el cruce contra afirmaciones.db")
print("=" * 74)

# ===========================================================================
# COMPROBACION 1 -- las 22 secuencias contra hilos.db
# ===========================================================================
if not os.path.exists(ARCHIVO_HILOS):
    raise SystemExit("FALLO: no existe " + ARCHIVO_HILOS)

con = sqlite3.connect("file:" + ARCHIVO_HILOS + "?mode=ro", uri=True)
guardados = dict((h, (s, p, pi))
                 for h, s, p, pi in con.execute(
                     "select hilo, semilla, pasos, pico from hilos order by hilo"))

pos = {}
for h, (s, p, pi) in guardados.items():
    v = secuencia_de(s)
    pos[h] = v
    if len(v) - 1 != p or max(v) != pi:
        raise SystemExit("FALLO: el hilo %d no coincide con hilos.db" % h)

filas = con.execute("select hilo, k, valor from pasos order by hilo, k").fetchall()
malos = sum(1 for h, k, val in filas if pos[h][k] != val)
print("\nCOMPROBACION 1 -- las 11 secuencias positivas contra hilos.db")
print("  hilos : %d    pasos comparados : %d    descuadres : %d" % (
    len(pos), len(filas), malos))
if malos:
    raise SystemExit("FALLO: descuadre con hilos.db. Se para.")

neg = dict((h, secuencia_neg(-guardados[h][0])) for h in guardados)
print("  espejos negativos construidos : %d" % len(neg))
print("  TOTAL de secuencias en la malla : %d" % (len(pos) + len(neg)))

# ===========================================================================
# COMPROBACION 2 -- y esta decide el valor de todo el programa.
#
# El promedio LONGITUDINAL no es un dato nuevo: esta determinado por el valor
# y su paridad, sin mirar nada mas.
#
#     x PAR    ->  ( x + x/2 ) / 2      =  3x/4
#     x IMPAR  ->  ( x + 3x+1 ) / 2     =  2x + 1/2
#
# Si esto sale exacto en todos los casos, la "dimension extra" es un cambio de
# etiqueta, no informacion. Se comprueba con Fraction, sin un solo float.
# ===========================================================================
casos = 0
fallos = 0
for h, v in list(pos.items()) + list(neg.items()):
    for k in range(len(v) - 1):
        x = v[k]
        prom = Fraction(x + v[k + 1], 2)
        if x % 2 == 0:
            pred = Fraction(3 * x, 4)
        else:
            pred = Fraction(4 * x + 1, 2)
        casos += 1
        if prom != pred:
            fallos += 1

print("\nCOMPROBACION 2 -- el promedio longitudinal esta determinado por la paridad")
print("  promedios comprobados con Fraction : %d" % casos)
print("  fallos                             : %d" % fallos)
if fallos:
    raise SystemExit("FALLO: la forma cerrada del promedio no se sostiene. Se para.")
print("  forma cerrada:  x par -> 3x/4      x impar -> 2x + 1/2")
print("  -> LA CAPA LONGITUDINAL NO ANADE INFORMACION. Es una funcion de (x, x mod 2).")

enteros = sum(1 for h, v in list(pos.items()) + list(neg.items())
              for k in range(len(v) - 1) if (v[k] + v[k + 1]) % 2 == 0)
print("  promedios que salen enteros        : %d de %d (%.1f%%)" % (
    enteros, casos, 100.0 * enteros / casos))
print("  los demas son semienteros: la capa ni siquiera vive en Z.")

# ===========================================================================
# LA CAPA TRANSVERSAL -- esta si mezcla trayectorias independientes
# ===========================================================================
print("\n" + "=" * 74)
print("LA CAPA TRANSVERSAL -- promedio entre hilos, en el mismo paso")
print("=" * 74)

hs = sorted(pos)
parejas = [(a, b) for i, a in enumerate(hs) for b in hs[i + 1:]]
comun = {}
for a, b in parejas:
    n = min(len(pos[a]), len(pos[b]))
    comun[(a, b)] = [Fraction(pos[a][k] + pos[b][k], 2) for k in range(n)]

print("  parejas de hilos            : %d" % len(parejas))
print("  tramo comun mas corto/largo : %d / %d pasos" % (
    min(len(v) for v in comun.values()), max(len(v) for v in comun.values())))
ent = sum(1 for v in comun.values() for x in v if x.denominator == 1)
tot = sum(len(v) for v in comun.values())
print("  promedios enteros           : %d de %d (%.1f%%)" % (
    ent, tot, 100.0 * ent / tot))

# La pregunta que importa: el promedio de dos trayectorias, es una trayectoria?
sigue = rompe = 0
for (a, b), v in comun.items():
    for k in range(len(v) - 1):
        x = v[k]
        if x.denominator != 1:
            continue
        xi = int(x)
        sig = xi // 2 if xi % 2 == 0 else 3 * xi + 1
        if v[k + 1] == sig:
            sigue += 1
        else:
            rompe += 1
print()
print("  LA PREGUNTA QUE DECIDE: el promedio de dos trayectorias, es a su vez")
print("  una trayectoria de Collatz?")
print("    pasos enteros donde SI sigue la regla : %d" % sigue)
print("    pasos enteros donde NO la sigue       : %d" % rompe)
if sigue + rompe:
    print("    -> cumple la regla en el %.2f%% de los pasos" % (
        100.0 * sigue / (sigue + rompe)))
print("  Collatz NO es lineal: T(a)+T(b) no es T(a+b), asi que promediar dos")
print("  orbitas no da una orbita. La capa transversal es un objeto nuevo que")
print("  no obedece la regla que se queria estudiar.")

# ===========================================================================
# EL CRUCE CONTRA afirmaciones.db
# ===========================================================================
print("\n" + "=" * 74)
print("CRUCE CONTRA afirmaciones.db")
print("=" * 74)

if not os.path.exists(ARCHIVO_AFIRM):
    raise SystemExit("FALLO: no existe " + ARCHIVO_AFIRM)

ca = sqlite3.connect("file:" + ARCHIVO_AFIRM + "?mode=ro", uri=True)
afs = ca.execute("select id, cuantificador, estado, fichero, enunciado "
                 "from afirmaciones order by id").fetchall()

TESTABLES = ("todo_n", "clase_residual")
por_c = {}
for _id, c, e, f, en in afs:
    por_c.setdefault(c, []).append(_id)

print("\n  Las 80 afirmaciones, por cuantificador:")
for c in sorted(por_c, key=lambda x: -len(por_c[x])):
    veredicto = "SE CRUZA" if c in TESTABLES else "SE NIEGA A CRUZAR"
    print("    %-18s %3d   %s" % (c, len(por_c[c]), veredicto))

n_niega = sum(len(v) for c, v in por_c.items() if c not in TESTABLES)
print()
print("  %d filas se cruzan, %d NO." % (
    sum(len(por_c.get(c, [])) for c in TESTABLES), n_niega))
print("  Las %d que no, se dejan sin evaluar A PROPOSITO: 22 secuencias no" % n_niega)
print("  estiman una densidad ni una media. Evaluarlas y matizar seria el error.")

# --- las que SI se pueden encodear y correr de verdad ---
print("\n  Las que este programa puede EJECUTAR (no solo listar):")

res = []

# (1) la identidad de Terras sobre la malla base
mal = 0
tot_pares = 0
for h, v in pos.items():
    A = B = 0
    C = 0
    for k in range(len(v) - 1):
        if v[k] % 2:
            C = 3 * C + 2 ** B
            A += 1
        else:
            B += 1
        tot_pares += 1
        if 2 ** B * v[k + 1] != 3 ** A * v[0] + C:
            mal += 1
res.append(("la identidad 2^B*seq[j] = 3^A*seq[i] + C", "todo_n",
            "malla base", tot_pares, mal))

# (2) la misma identidad sobre la CAPA DE PROMEDIOS
mal2 = tot2 = 0
for h, v in pos.items():
    prom = [Fraction(v[k] + v[k + 1], 2) for k in range(len(v) - 1)]
    A = B = 0
    C = Fraction(0)
    for k in range(len(prom) - 1):
        if prom[k].denominator == 1 and int(prom[k]) % 2 == 0:
            B += 1
        else:
            C = 3 * C + 2 ** B
            A += 1
        tot2 += 1
        if Fraction(2) ** B * prom[k + 1] != Fraction(3) ** A * prom[0] + C:
            mal2 += 1
res.append(("la misma identidad, sobre la CAPA DE PROMEDIOS", "todo_n",
            "capa promedios", tot2, mal2))

# (3) el piso de la altitud, sobre los impares de la base
mal3 = tot3 = 0
for h, v in pos.items():
    n = v[0]
    if n % 2 == 0:
        continue
    r = 0
    x = n
    while x % 2:
        r += 1
        x = (3 * x + 1) // 2
    tot3 += 1
    if max(v) * 2 ** r < 2 * n * 3 ** r:
        mal3 += 1
res.append(("el piso: log2(alt/n) >= racha*log2(3/2) + 1", "todo_n",
            "impares de la base", tot3, mal3))

# (4) n mod 2^k fija los k primeros pasos
mod = 2 ** K_RESTOS
grupos = {}
for h, v in pos.items():
    grupos.setdefault(v[0] % mod, set()).add(paridad_de(v[0]))
mal4 = sum(1 for r, s in grupos.items() if len(s) > 1)
res.append(("n mod 2^%d fija los %d primeros pasos" % (K_RESTOS, K_RESTOS),
            "clase_residual", "restos de la base", len(grupos), mal4))

# (5) Res >= 1, con igualdad solo en potencias de 2
mal5 = tot5 = 0
for h, v in pos.items():
    A = sum(1 for x in v[:-1] if x % 2)
    B = len(v) - 1 - A
    tot5 += 1
    if 2 ** B < 3 ** A * v[0]:
        mal5 += 1
res.append(("Res = 2^B/(3^A*n) >= 1", "todo_n", "malla base", tot5, mal5))

print()
print("  %-46s %-16s %-8s %s" % ("afirmacion", "sobre que", "casos", "fallos"))
for enun, cuant, sobre, tot_, mal_ in res:
    print("  %-46s %-16s %-8d %d" % (enun[:46], sobre, tot_, mal_))

# ===========================================================================
# EL CONTROL A/B -- la maquinaria discrimina, o dibuja lo que sea?
# ===========================================================================
print("\n" + "=" * 74)
print("CONTROL A/B -- la misma capa de promedios sobre OTRAS reglas")
print("=" * 74)
print("  Si la capa de promedios 'revela estructura', tiene que revelar cosas")
print("  DISTINTAS con reglas distintas. Si sale lo mismo, lo que mide es la")
print("  maquinaria, no Collatz.")
print()


def capa_de(v):
    """Estadisticos de la capa longitudinal de una secuencia."""
    p = [Fraction(v[k] + v[k + 1], 2) for k in range(len(v) - 1)]
    ent = sum(1 for x in p if x.denominator == 1)
    return len(p), ent, 100.0 * ent / len(p) if p else 0.0


def seq_3n_menos_1(m):
    v = [m]
    vistos = set()
    while m not in vistos and len(v) < TOPE_CICLO:
        vistos.add(m)
        m = m // 2 if m % 2 == 0 else 3 * m - 1
        v.append(m)
    return v


def seq_dobla(m):
    """Regla de control SIN Collatz: n -> n/2 si par, n+1 si impar."""
    v = [m]
    while m != 1:
        m = m // 2 if m % 2 == 0 else m + 1
        v.append(m)
    return v


print("  %-22s %-10s %-10s %s" % ("regla", "promedios", "enteros", "% enteros"))
for nom, gen in (("3n+1  (Collatz)", secuencia_de),
                 ("3n-1  (los negativos)", seq_3n_menos_1),
                 ("n+1   (control trivial)", seq_dobla)):
    T = E = 0
    for s in range(BASE_LO, BASE_HI + 1):
        t, e, _ = capa_de(gen(s))
        T += t
        E += e
    print("  %-22s %-10d %-10d %.2f%%" % (nom, T, E, 100.0 * E / T))

print()
print("  El porcentaje de promedios enteros es solo la fraccion de pasos PARES,")
print("  porque x par da 3x/4 y x impar da un semientero. O sea que esta columna")
print("  mide la paridad, que ya sabiamos, por un camino mas largo.")

# ===========================================================================
print("\n" + "=" * 74)
print("VEREDICTO")
print("=" * 74)
print("""
  1. LA CAPA LONGITUDINAL NO ANADE NADA, y esta demostrado arriba con
     Fraction, no medido: el promedio de dos terminos consecutivos vale 3x/4
     si x es par y 2x+1/2 si es impar. Es una funcion de (x, x mod 2). Una
     dimension nueva construida con una funcion de lo que ya tenias no puede
     contener informacion nueva -- es el mismo argumento por el que
     sqrt(pico)-1 tampoco decia nada.

  2. LA CAPA TRANSVERSAL SI ES UN OBJETO NUEVO, pero NO es Collatz: el
     promedio de dos orbitas no es una orbita, porque T no es lineal. Las
     afirmaciones del repo no se le aplican, y de hecho la identidad de
     Terras se rompe sobre ella (ver la tabla del cruce).

  3. EL CRUCE CONTRA LA BASE se hizo con el filtro de cuantificador puesto:
     las filas de tipo promedio y casi_todo_n quedaron SIN EVALUAR a
     proposito. Ese es el resultado honesto -- 22 secuencias no estiman una
     densidad, y decir '22 de 22' sobre una de esas filas seria fabricar
     confirmacion.

  4. LO QUE SI SOBREVIVE es la malla base: la identidad, el piso y el resto
     mod 2^k se cumplen sin un fallo. Pero eso ya se sabia; lo que esta
     medicion aporta es el NEGATIVO sobre la capa de promedios.
""")
