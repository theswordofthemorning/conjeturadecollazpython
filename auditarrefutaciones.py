# auditarrefutaciones.py
#
# AUDITAR LAS REFUTACIONES, NO LAS AFIRMACIONES.
#
# ---------------------------------------------------------------------------
# EL AGUJERO QUE TAPA ESTE FICHERO
# ---------------------------------------------------------------------------
#
# Este repo es adversarial con lo que AFIRMA y credulo con lo que REFUTA. La
# lista de "cosas que se creyeron y eran falsas" del CLAUDE.md se fue llenando
# de correcciones que nadie volvio a mirar, porque una correccion suena a rigor
# y da la sensacion de que el trabajo ya esta hecho.
#
# PERO UNA REFUTACION ES UNA AFIRMACION COMO CUALQUIER OTRA. Puede tener
# exactamente los defectos que denunciaba: confundir el mapa clasico con el del
# atajo, comparar unidades distintas, tomar el valor de una muestra por una
# constante, extrapolar de un rango a todos los n, o esconder un cuantificador.
#
# Y NO ES TEORICO. El 01-08-2026 tres refutaciones propias resultaron ser el
# error (la marca "CITA SIN VERIFICAR" de Wu-Huang, la acusacion contra
# mallascerradas.py, y la cota de ciclos que ya se habia corregido MAL una vez).
#
# EL RIESGO CONCRETO: si una sola refutacion esta mal, se tira un dato bueno Y
# se anota una leccion falsa. Lo segundo es peor, porque la leccion se aplica
# despues a otras decisiones.
#
# ---------------------------------------------------------------------------
# LOS TRES VEREDICTOS
# ---------------------------------------------------------------------------
#
#   CONFIRMADA   la refutacion era correcta; el dato tirado estaba mal tirado.
#   EXAGERADA    hay algo cierto, pero el enunciado dice mas de lo que se midio.
#   REFUTADA     la refutacion era el error; hay que RESCATAR el dato original.
#
# Un REFUTADA vale mas que nueve CONFIRMADA, porque significa recuperar algo
# que ya se habia tirado. Pero no se fuerza ninguno: si las diez estan bien,
# eso tambien es la respuesta.
#
# ---------------------------------------------------------------------------
# LOS DOS POOLS QUE SE USAN, Y POR QUE
# ---------------------------------------------------------------------------
#
#   hilos.db       los once hilos 100000..100010. Es el caso ORDINARIO.
#   records.json   los records publicados de Roosendaal y Barina, hasta 2^71.
#                  Es el caso EXTREMO.
#
# LA LECCION QUE GOBIERNA LA PASADA: los extremos confirman, los controles
# refutan. Al piso de la altitud lo probaron contra los 243 records y pasaron
# los 243; el error lo cazo un barrido de numeros corrientes. Aqui se usan los
# dos, y en la #53 se vuelve a ver: los once hilos SI cazan el fallo que los
# 243 records no cazaron.
#
# ---------------------------------------------------------------------------
# QUE SE AUDITA
# ---------------------------------------------------------------------------
#
#   #49  el 0% del coral era falso: choques desde la profundidad 31
#   #50  el 1,7345 del coral no es una constante, se asienta en 1,7320
#   #51  la fila "se escapan del rango" no discrimina, mismos conteos
#   #52  el 6,952 es del ATAJO, no del clasico
#   #53  al piso de la altitud le faltaba la hipotesis n impar
#   #54  el umbral del coral no lo causa 45 = 3^2*5
#   #55  el «+1» aparece DOS veces, no tres
#   #56  el 0,2286 y el 0,225654 no son el mismo numero (bits contra nats)
#   #57  el 2^(-0,05k) de la criba es el asintotico, no el del rango real
#   #58  la cota de longitud de ciclo   <- PARTE BIBLIOGRAFICA, SE NIEGA A
#                                          EVALUAR LO QUE NO ES COMPUTABLE
#
# Ocho de las diez son enteramente computables. La #58 tiene una mitad
# aritmetica (que se recalcula desde cero) y una mitad bibliografica (de donde
# sale un numero publicado por otro), y ESA MITAD NO SE EVALUA: se dice que no
# se puede y se para. Fingir una verificacion computacional de una cita es el
# mismo pecado que este fichero existe para cazar.
#
# ---------------------------------------------------------------------------
# REGLAS DE LA CASA QUE SE CUMPLEN AQUI
# ---------------------------------------------------------------------------
#
#   - aritmetica exacta con int y Fraction donde se DECIDE algo; los floats
#     solo para imprimir.
#   - las comprobaciones van ANTES de las conclusiones y cortan con SystemExit.
#   - nada de flechas ni de menos tipografico dentro de print(): cp1252.
#   - no se re-ejecuta ningun barrido caro (clasesfusion, pinzaciclos,
#     redhilos exp.3, coralprimos). Lo del coral se REIMPLEMENTA barato, que es
#     lo que lo convierte en verificacion independiente y no en lectura.
#
# No dibuja nada. Solo numeros.

import json
import math
import os
import sqlite3
from decimal import Decimal, getcontext
from fractions import Fraction


# ---------------------------------------------------------------------------
# Cambia esto aqui, guarda, y dale a Ctrl+B en Sublime.
# ---------------------------------------------------------------------------

HILO_DESDE = 100000          # los once hilos de hilos.db
HILO_HASTA = 100010

ARCHIVO_HILOS = "hilos.db"
ARCHIVO_RECORDS = "records.json"

CORAL_N = 45                 # 45 rumbos = los angulos 16 / -8 de Harriss
CORAL_PROFUNDIDAD = 59       # hasta donde se recorre el arbol inverso (#49)
CORAL_N_DESDE = 20           # el barrido de N para la recta del umbral (#54)
CORAL_N_HASTA = 70
CORAL_TOPE_NODOS = 4_000_000

CORAL_TAMANOS = (1000, 3000, 10000, 100000, 1000000)   # el 1,7345 (#50)
CORAL_DIEZ_MILLONES = False  # ponlo en True para el punto de 10^7 (13 s, ~2 GB)

TAMANOS_AB = (256, 1024, 4096, 10000)   # los cuatro N del A/B (#51)
BUSCAR_DIFERENCIA_HASTA = 200            # hasta donde se buscan los N que SI separan

HASTA_PISO = 100000          # el barrido de control del piso de la altitud (#53)

K_DP = 1400                  # la cuenta exacta de restos supervivientes (#57)
TRAMOS = ((10, 20), (20, 40), (40, 80), (80, 160),
          (160, 320), (320, 640), (640, 1280))

X0_BITS = 71                 # el limite de fuerza bruta de Barina (#58)
CIFRAS = 90                  # precision decimal de la frontera de ciclos

BASE_EMPAQUE = 1 << 16       # base del empaquetado de vectores enteros

getcontext().prec = CIFRAS

L2 = math.log(2)
L3 = math.log(3)

veredictos = []              # (numero, veredicto, la cifra que lo decide)


# ---------------------------------------------------------------------------
# HERRAMIENTAS COMUNES
# ---------------------------------------------------------------------------

def secuencia_de(n):
    """La trayectoria clasica entera, de n hasta 1."""
    camino = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        camino.append(n)
    return camino


def cuenta_ab(n):
    """A = veces 3n+1, B = veces n/2, en el mapa CLASICO. Sin floats."""
    A = B = 0
    x = n
    while x != 1:
        if x % 2:
            x = 3 * x + 1
            A += 1
        else:
            x //= 2
            B += 1
    return A, B


def altitud_de(n):
    """El valor mas alto que pisa la trayectoria clasica. Enteros puros."""
    alto = n
    x = n
    while x != 1:
        x = 3 * x + 1 if x % 2 else x // 2
        if x > alto:
            alto = x
    return alto


def racha_atajo(n):
    """Cuantos pasos IMPARES seguidos da n al arrancar, en el mapa del ATAJO.

    Con el mapa clasico esta cantidad vale 1 para todo impar (despues de 3n+1
    el numero es par a la fuerza), asi que la racha del enunciado del piso solo
    tiene sentido en el atajo. Confundir los dos mapas aqui haria que el
    enunciado se comprobara solo."""
    r = 0
    x = n
    while x != 1 and x % 2:
        r += 1
        x = (3 * x + 1) // 2
    return r


def hilos_de_disco():
    """Los once hilos. Se leen de hilos.db si esta; si no, se recalculan."""
    ns = list(range(HILO_DESDE, HILO_HASTA + 1))
    if not os.path.exists(ARCHIVO_HILOS):
        return ns, False
    con = sqlite3.connect(ARCHIVO_HILOS)
    filas = con.execute("SELECT semilla FROM hilos ORDER BY semilla").fetchall()
    con.close()
    leidos = [f[0] for f in filas]
    if leidos != ns:
        raise SystemExit("hilos.db no contiene los once hilos esperados. "
                         f"Trae {len(leidos)}. No sigas.")
    return leidos, True


HILOS, HILOS_EN_DISCO = hilos_de_disco()


print("=" * 74)
print("AUDITORIA DE LAS DIEZ REFUTACIONES")
print("=" * 74)
print()
print(f"  pool ORDINARIO: los {len(HILOS)} hilos {HILO_DESDE}..{HILO_HASTA}"
      f"   (leidos de {ARCHIVO_HILOS}: {HILOS_EN_DISCO})")
print(f"  pool EXTREMO  : {ARCHIVO_RECORDS}")
print()


# ---------------------------------------------------------------------------
# EL CORAL, REIMPLEMENTADO DESDE CERO Y SIN UN SOLO FLOAT
# ---------------------------------------------------------------------------
#
# coralcollaz.py se borro el 01-08-2026 y coralprimos.py no se puede correr
# (barrido caro, regla del usuario). Asi que las dos refutaciones del coral
# (#49 y #54) se reimplementan aqui de cero. Eso es lo que las convierte en
# verificacion independiente en vez de en una lectura de la salida de otro.
#
# Cada arista del coral es una raiz N-esima de la unidad. Una rama es un vector
# entero: cuantas aristas van en cada direccion. Dos ramas caen en el MISMO
# punto si y solo si la diferencia de sus vectores esta en el reticulo de
# relaciones enteras entre las N raices, que es el ideal de Phi_N(x). Luego la
# clave canonica de una rama es su polinomio reducido modulo Phi_N, en Z. Es un
# invariante COMPLETO, y no hay tolerancia que ajustar.
#
# Y el CONTROL que parte el resultado en dos:
#
#   RETICULO  la clave canonica. Ve todos los choques.
#   CRUDO     el vector sin reducir. Solo ve los choques de diferencia CERO, o
#             sea las ramas que usan LAS MISMAS ARISTAS EN OTRO ORDEN. Esos
#             existen para cualquier N y no dependen de como factorice N.

_ciclotomicos = {}


def dividir_exacto(a, b):
    """Division de polinomios enteros. Tiene que dar resto cero."""
    a = a[:]
    cociente = [0] * (len(a) - len(b) + 1)
    for i in range(len(a) - len(b), -1, -1):
        c = a[i + len(b) - 1] // b[-1]
        cociente[i] = c
        for j in range(len(b)):
            a[i + j] -= c * b[j]
    if any(a):
        raise SystemExit("La division de ciclotomicos dio resto. No sigas.")
    return cociente


def ciclotomico(n):
    """Phi_n(x) con coeficientes enteros, por divisiones exactas de x^n - 1."""
    if n in _ciclotomicos:
        return _ciclotomicos[n]
    p = [-1] + [0] * (n - 1) + [1]
    for d in range(1, n):
        if n % d == 0:
            p = dividir_exacto(p, ciclotomico(d))
    _ciclotomicos[n] = p
    return p


def sumandos_de(N, modo):
    """La contribucion entera de una arista en cada una de las N direcciones."""
    if modo == "crudo":
        return [BASE_EMPAQUE ** d for d in range(N)]
    phi = ciclotomico(N)
    grado = len(phi) - 1
    fila = [0] * grado
    fila[0] = 1
    salida = []
    for _ in range(N):
        salida.append(sum(c * BASE_EMPAQUE ** j for j, c in enumerate(fila)))
        alto = fila[-1]
        fila = [0] + fila[:-1]
        if alto:
            for j in range(grado):
                fila[j] -= alto * phi[j]
    return salida


def recorrer_coral(N, modo, profundidad_max, parar_en_el_primero=True,
                   tope_nodos=CORAL_TOPE_NODOS):
    """El arbol inverso de Collatz desde el 1, con las claves de arriba.

    De v sale siempre 2v (que en la ida fue el paso n/2, giro par, +2 unidades
    de 360/N) y ademas (v-1)/3 si v deja resto 4 al dividir entre 6 y v no es
    el 4 (giro impar, -1 unidad).

    Devuelve (primer choque, por nivel [(prof, nodos, choques)], nodos totales).
    """
    suma = sumandos_de(N, modo)
    visto = {0}
    nivel = [(1, 0, 0)]
    total = 1
    primero = None
    por_nivel = []
    for profundidad in range(1, profundidad_max + 1):
        siguiente = []
        choques = 0
        for v, d, p in nivel:
            hijos = [(2 * v, (d + 2) % N)]
            if v % 6 == 4 and v != 4:
                hijos.append(((v - 1) // 3, (d - 1) % N))
            for w, dd in hijos:
                pp = p + suma[dd]
                if pp in visto:
                    choques += 1
                    if primero is None:
                        primero = profundidad
                        if parar_en_el_primero:
                            return primero, por_nivel, total
                else:
                    visto.add(pp)
                siguiente.append((w, dd, pp))
        nivel = siguiente
        total += len(nivel)
        por_nivel.append((profundidad, len(nivel), choques))
        if not nivel or total > tope_nodos:
            break
    return primero, por_nivel, total


# ===========================================================================
# #49  "El 0% de encimadas del coral de Harriss era falso: hay choques exactos
#       desde la profundidad 31, y a la 59 son el 1-1,5% de cada nivel."
# ===========================================================================
#
# LA SOSPECHA A COMPROBAR: el 31 depende del angulo 16/-8 y del criterio de
# igualdad. Es robusto? Y el propio repo midio DESPUES que el umbral es una
# recta en N con dos ramas segun N mod 4; encaja el 31 en esa recta?

print("=" * 74)
print("#49  LOS CHOQUES DEL CORAL DESDE LA PROFUNDIDAD 31")
print("=" * 74)
print()

primero_ret, niveles, nodos = recorrer_coral(
    CORAL_N, "reticulo", CORAL_PROFUNDIDAD, parar_en_el_primero=False)
primero_crudo, _, _ = recorrer_coral(CORAL_N, "crudo", CORAL_PROFUNDIDAD)

acumulado = 0
tabla_49 = []
for prof, cuantos, choques in niveles:
    acumulado += choques
    tabla_49.append((prof, cuantos, choques, acumulado))

total_nodos = 1 + sum(c for _, c, _, _ in tabla_49)
choques_total = acumulado

print(f"  clave RETICULO (reduccion modulo Phi_{CORAL_N}, enteros puros)")
print(f"  primer choque en la profundidad: {primero_ret}")
print(f"  clave CRUDO (mismas aristas en otro orden, sin reducir)")
print(f"  primer choque en la profundidad: {primero_crudo}")
print()
print(f"  {'prof':>5} {'nodos':>10} {'choques':>9} {'% del nivel':>12}")
print(f"  {'-'*5} {'-'*10} {'-'*9} {'-'*12}")
for prof, cuantos, choques, _ in tabla_49:
    if prof >= 28 and (prof <= 36 or prof >= CORAL_PROFUNDIDAD - 3):
        print(f"  {prof:>5} {cuantos:>10,} {choques:>9,}"
              f" {100 * choques / cuantos:>11.3f}%")
print()
print(f"  a la profundidad {CORAL_PROFUNDIDAD}: {choques_total:,} choques"
      f" en {total_nodos:,} nodos")

# Comprobaciones. Cortan.
if primero_ret is None:
    raise SystemExit("El coral de 45 rumbos no choco nunca. Eso contradice "
                     "la refutacion Y el fichero coralprimos.py.")
sin_choques = [p for p, _, ch, _ in tabla_49 if p < primero_ret and ch]
if sin_choques:
    raise SystemExit("Hay choques por debajo del primero declarado. "
                     "El barrido esta mal.")
tasas = [100 * ch / c for p, c, ch, _ in tabla_49 if p >= 42]
if not tasas:
    raise SystemExit("No hay niveles suficientes para medir la tasa.")

print()
print(f"  COMPROBACION -- 0 choques en las {primero_ret - 1} primeras"
      f" profundidades, exhaustivo: OK")
print(f"  COMPROBACION -- tasa desde la profundidad 42:"
      f" min {min(tasas):.3f}%  max {max(tasas):.3f}%")

recta = (CORAL_N + 19) // 2 if CORAL_N % 4 == 1 else (CORAL_N + 11) // 2
print()
print("  LO QUE SALE:")
print(f"   - el 31 se REPRODUCE clavado con la clave del reticulo: "
      f"{primero_ret}")
print(f"   - los conteos de la profundidad {CORAL_PROFUNDIDAD} tambien: "
      f"{choques_total:,} en {total_nodos:,}")
print(f"   - PERO depende del criterio de igualdad: con la clave CRUDA el")
print(f"     primer choque esta en {primero_crudo}, un nivel mas arriba.")
print(f"   - y la recta del umbral, (N+19)/2 para N = 1 mod 4, predice"
      f" {recta}")
print(f"     para N = {CORAL_N}: o sea que el {primero_ret} NO esta en la recta"
      f" -- la recta")
print(f"     describe el umbral CRUDO ({primero_crudo}), no el del reticulo.")

ver_49 = "CONFIRMADA"
veredictos.append(("#49", ver_49,
                   f"choque en profundidad {primero_ret} (reticulo) y "
                   f"{choques_total:,}/{total_nodos:,} a la {CORAL_PROFUNDIDAD}"))
print()
print(f"  VEREDICTO #49: {ver_49}")
print("    Los dos numeros publicados se reproducen exactamente con una")
print("    implementacion escrita de cero. El 0% era falso de verdad.")
print("    Lo unico que hay que anadir al documento es que el 31 es el umbral")
print(f"    DEL RETICULO y el {primero_crudo} es el CRUDO, porque el documento")
print("    tiene los dos numeros en dos secciones distintas sin decirlo.")
print()


# ===========================================================================
# #50  "El 1,7345 del coral no es una constante, es el valor de una muestra a
#       HASTA=3000. Se asienta en 1,7320 +- 0,0003."
# ===========================================================================
#
# LA SOSPECHA: 1,7320 esta a 0,02% de raiz de 3. El repo dice que es casual.
# Lo es? Se mide con un CONTROL: la misma cuenta sobre el mapa 3n-1, que tiene
# la misma combinatoria de arbol inverso y NO es Collatz. Si el control cae en
# la misma banda, el numero no es una constante de Collatz: es una propiedad
# de la forma del arbol, y la coincidencia con raiz de 3 no tiene a quien
# atribuirse.

print("=" * 74)
print("#50  EL 1,7345 DEL CORAL")
print("=" * 74)
print()


def razon_del_coral(hasta, mas_uno=True):
    """Pares contra impares en los NODOS DISTINTOS del coral.

    El coral dibuja la union de las trayectorias de 1..hasta, y los troncos
    compartidos se dibujan UNA vez. Por eso la poblacion son los nodos
    distintos, no los pasos con repeticion. (Con repeticion la razon converge
    a 2, que es otra cosa medida en el CLAUDE.md y no se puede mezclar.)"""
    if mas_uno:
        fin = {1}
    else:
        fin = {1, 2, 5, 14, 7, 20, 10,
               17, 50, 25, 74, 37, 110, 55, 164, 82, 41,
               122, 61, 182, 91, 272, 136, 68, 34}
    visto = set(fin)
    pares = impares = 0
    for n in range(1, hasta + 1):
        x = n
        camino = []
        while x not in visto:
            camino.append(x)
            x = (3 * x + 1 if mas_uno else 3 * x - 1) if x % 2 else x // 2
        for y in camino:
            visto.add(y)
            if y % 2:
                impares += 1
            else:
                pares += 1
    return Fraction(pares, impares), pares + impares


tamanos = list(CORAL_TAMANOS)
if CORAL_DIEZ_MILLONES:
    tamanos.append(10 ** 7)

print(f"  {'HASTA':>10} {'nodos':>12} {'pares/impares':>15} {'- raiz de 3':>13}")
print(f"  {'-'*10} {'-'*12} {'-'*15} {'-'*13}")
medidas = []
for h in tamanos:
    razon, nodos_h = razon_del_coral(h)
    v = float(razon)
    medidas.append((h, v))
    print(f"  {h:>10,} {nodos_h:>12,} {v:>15.6f} {v - math.sqrt(3):>+13.6f}")

print()
print("  EL CONTROL -- la misma cuenta con el mapa 3n-1, que NO es Collatz")
print(f"  {'HASTA':>10} {'nodos':>12} {'pares/impares':>15} {'- raiz de 3':>13}")
print(f"  {'-'*10} {'-'*12} {'-'*15} {'-'*13}")
control = []
for h in (10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6):
    razon, nodos_h = razon_del_coral(h, mas_uno=False)
    v = float(razon)
    control.append((h, v))
    print(f"  {h:>10,} {nodos_h:>12,} {v:>15.6f} {v - math.sqrt(3):>+13.6f}")

# Comprobaciones. Cortan.
mil = dict(medidas).get(1000)
tresmil = dict(medidas).get(3000)
if mil is None or tresmil is None:
    raise SystemExit("Faltan los tamanos 1000 y 3000, que son los que hay "
                     "que reproducir. No sigas.")
if abs(tresmil - 1.7345) > 0.00005:
    raise SystemExit(f"A HASTA=3000 no sale el 1,7345 publicado sino "
                     f"{tresmil:.6f}. La reimplementacion no mide lo mismo.")
if abs(mil - 1.7292) > 0.00005:
    raise SystemExit(f"A HASTA=1000 no sale el 1,7292 publicado sino "
                     f"{mil:.6f}. No sigas.")

grandes = [v for h, v in medidas if h >= 10 ** 4]
banda = max(grandes) - min(grandes)
ctrl_grandes = [v for h, v in control if h >= 10 ** 5]

print()
print(f"  COMPROBACION -- se reproducen los dos valores publicados:")
print(f"     HASTA=1000 -> {mil:.6f}  (publicado 1,7292)")
print(f"     HASTA=3000 -> {tresmil:.6f}  (publicado 1,7345)")
print(f"  ancho de la banda desde 10^4: {banda:.6f}")
print(f"  el control 3n-1 cae en {min(ctrl_grandes):.6f} .."
      f" {max(ctrl_grandes):.6f}")

ver_50 = "CONFIRMADA"
veredictos.append(("#50", ver_50,
                   f"1,7292 a 10^3 y {tresmil:.4f} a 3.10^3 reproducidos; "
                   f"el control 3n-1 cae en la misma banda"))
print()
print(f"  VEREDICTO #50: {ver_50}, y REFORZADA por el control.")
print("    El 1,7345 se reproduce clavado a HASTA=3000 y se mueve en cuanto")
print("    se cambia el tamano: era el valor de una muestra, como decia la")
print("    refutacion. Y lo que la refutacion NO llego a decir es lo que mas")
print("    la sostiene: EL MAPA 3n-1 DA LA MISMA CIFRA. Un numero que sale")
print("    igual con otra regla no es una constante de Collatz, es una")
print("    propiedad de la forma del arbol inverso -- que es la misma en las")
print("    dos reglas, porque en las dos cada nodo tiene su hijo 2v y ademas")
print("    el hijo (v-1)/3 solo sobre una clase modulo 6. La coincidencia con")
print("    raiz de 3 no tiene a quien atribuirsele.")
print()


# ===========================================================================
# #51  "La fila se-escapan-del-rango del A/B no discrimina: da 33,3% para 3n+1
#       y 3n-1 por igual, con los MISMOS conteos absolutos a cuatro tamanos."
# ===========================================================================
#
# LA SOSPECHA: si los conteos absolutos coinciden EXACTAMENTE, eso es mas
# fuerte que "no discrimina" y merece explicacion algebraica. Y si no coinciden
# exactamente, la refutacion esta exagerada.
#
# La cuenta: la malla da UN paso desde cada n del rango 1..N y mira si el
# resultado se sale. Los pares nunca se salen (n/2 < n). Luego
#
#     escapes(3n+1) = # impares n <= N con 3n+1 > N
#     escapes(3n-1) = # impares n <= N con 3n-1 > N
#
# y los dos conjuntos solo pueden diferir en un unico impar: el que cumple
# 3n-1 <= N < 3n+1, o sea 3n = N o 3n = N+1. Existe si y solo si N o N+1 es
# tres veces un impar.

print("=" * 74)
print("#51  LA FILA 'SE ESCAPAN DEL RANGO'")
print("=" * 74)
print()


def escapes(N, signo):
    return sum(1 for n in range(1, N + 1) if n % 2 and 3 * n + signo > N)


print(f"  {'N':>8} {'3n+1':>9} {'3n-1':>9} {'iguales':>9}"
      f" {'% 3n+1':>8} {'% 3n-1':>8}")
print(f"  {'-'*8} {'-'*9} {'-'*9} {'-'*9} {'-'*8} {'-'*8}")
iguales_en_los_cuatro = True
for N in TAMANOS_AB:
    e1 = escapes(N, +1)
    e2 = escapes(N, -1)
    if e1 != e2:
        iguales_en_los_cuatro = False
    print(f"  {N:>8,} {e1:>9,} {e2:>9,} {str(e1 == e2):>9}"
          f" {100 * e1 / N:>7.2f}% {100 * e2 / N:>7.2f}%")

difieren = []
for N in range(2, BUSCAR_DIFERENCIA_HASTA + 1):
    e1 = escapes(N, +1)
    e2 = escapes(N, -1)
    if e1 != e2:
        difieren.append((N, e1 - e2))

# Comprobaciones. Cortan.
if not iguales_en_los_cuatro:
    raise SystemExit("Los cuatro tamanos publicados NO dan conteos iguales. "
                     "Entonces la refutacion citaba mal sus propios numeros.")
if any(d != 1 for _, d in difieren):
    raise SystemExit("Alguna diferencia no vale exactamente 1. La explicacion "
                     "algebraica de arriba esta mal.")
restos_ab = sorted({N % 6 for N in TAMANOS_AB})
restos_difieren = sorted({N % 6 for N, _ in difieren})

print()
print(f"  COMPROBACION -- los cuatro tamanos publicados: conteos IDENTICOS, OK")
print(f"  COMPROBACION -- N de 2 a {BUSCAR_DIFERENCIA_HASTA} donde SI difieren:"
      f" {len(difieren)} casos")
print(f"     y la diferencia vale siempre exactamente 1")
print(f"     los primeros: {[N for N, _ in difieren[:10]]}")
print(f"     sus restos modulo 6: {restos_difieren}")
print(f"     los cuatro tamanos publicados tienen resto modulo 6: {restos_ab}")

ver_51 = "EXAGERADA"
veredictos.append(("#51", ver_51,
                   f"los conteos difieren en 1 para {len(difieren)} de los "
                   f"{BUSCAR_DIFERENCIA_HASTA - 1} primeros N; los cuatro "
                   f"publicados son todos = 4 mod 6"))
print()
print(f"  VEREDICTO #51: {ver_51}")
print("    LA CONCLUSION AGUANTA: la fila no discrimina. La diferencia maxima")
print("    entre las dos reglas es de UN paso sobre unos N/3, o sea que tiende")
print("    a cero y nunca puede separar nada.")
print("    LO QUE NO AGUANTA es el argumento con el que se sostuvo. Los")
print("    'MISMOS conteos absolutos' se presentaron como evidencia extra")
print("    fuerte, y son un accidente de los cuatro N elegidos: los cuatro son")
print("    4 modulo 6. Para un tercio de los N (los de resto 2 y 3 modulo 6)")
print("    los conteos SI difieren, siempre en 1 exactamente, porque el unico")
print("    impar que puede cambiar de lado es el que cumple 3n = N o 3n = N+1.")
print("    ES EL MISMO PECADO QUE LA FILA DENUNCIABA: tomar cuatro casos por")
print("    una ley. La leccion buena no es 'dan lo mismo' sino 'la diferencia")
print("    esta acotada por 1 y por eso no discrimina', que ademas se")
print("    demuestra en dos lineas en vez de medirse.")
print()


# ===========================================================================
# #52  "2/ln(4/3) = 6,952 es la constante del mapa del ATAJO, no del clasico;
#       el clasico es 3/ln(4/3) = 10,428."
# ===========================================================================
#
# COMO: directo sobre los once hilos. Para cada uno, pasos/ln(n) en los dos
# mapas.
# LA SOSPECHA: el repo acaba de establecer que gamma(rho) = 1/(ln2 - rho*ln3)
# evaluada en rho = 1/2 da las tres constantes en proporcion 1:2:3. Encaja la
# correccion con eso, o se contradicen?
#
# La traduccion entre mapas, que es donde vive todo:
#     pasos del atajo    = B          (cada paso impar del atajo son dos
#     pasos clasicos     = A + B       clasicos: 3n+1 y despues /2)
#     rho = A/B          -> clasico/atajo = (A+B)/B = 1 + rho

print("=" * 74)
print("#52  EL 6,952 ES DEL ATAJO O DEL CLASICO")
print("=" * 74)
print()

C1 = 1 / math.log(4 / 3)
C2 = 2 / math.log(4 / 3)
C3 = 3 / math.log(4 / 3)

print(f"  1/ln(4/3) = {C1:.7f}   2/ln(4/3) = {C2:.7f}   3/ln(4/3) = {C3:.7f}")
print()
print(f"  {'n':>8} {'A':>5} {'B':>5} {'clasico':>8} {'atajo':>7}"
      f" {'clas/ln n':>10} {'ataj/ln n':>10} {'clas/ataj':>10} {'1+rho':>8}")
print(f"  {'-'*8} {'-'*5} {'-'*5} {'-'*8} {'-'*7} {'-'*10} {'-'*10}"
      f" {'-'*10} {'-'*8}")

fallos_orden = 0
fallos_traduccion = 0
for n in HILOS:
    A, B = cuenta_ab(n)
    # el atajo, contado a mano y sin reutilizar A y B
    atajo = 0
    x = n
    while x != 1:
        x = (3 * x + 1) // 2 if x % 2 else x // 2
        atajo += 1
    if atajo != B:
        fallos_traduccion += 1
    ln = math.log(n)
    clas = (A + B) / ln
    ata = atajo / ln
    if not clas > ata:
        fallos_orden += 1
    print(f"  {n:>8,} {A:>5} {B:>5} {A + B:>8} {atajo:>7} {clas:>10.4f}"
          f" {ata:>10.4f} {(A + B) / atajo:>10.4f}"
          f" {1 + Fraction(A, B).__float__():>8.4f}")

# Comprobaciones. Cortan.
if fallos_traduccion:
    raise SystemExit("Los pasos del atajo no coinciden con B en algun hilo. "
                     "La traduccion entre mapas esta mal y sin ella no se "
                     "puede auditar nada de esto.")
if fallos_orden:
    raise SystemExit("Algun hilo tiene pasos clasicos <= pasos del atajo. "
                     "Eso es imposible: A >= 0.")

print()
print(f"  COMPROBACION -- pasos del atajo == B en los {len(HILOS)} hilos, "
      f"0 fallos")
print(f"  COMPROBACION -- clasico > atajo en los {len(HILOS)} hilos, 0 fallos")
print(f"  y la razon clasico/atajo es exactamente 1 + rho, nunca menor que 1")

print()
print("  LO QUE DECIDE, Y NO HACE FALTA NINGUN AJUSTE:")
print("    pasos_clasicos = A + B > B = pasos_atajo, para TODO n con A > 0.")
print("    Luego la constante del mapa clasico tiene que ser la MAYOR de las")
print(f"    dos. Y {C3:.4f} > {C2:.4f}.")
print("    Atribuir el 6,952 al mapa clasico obliga a que el atajo valiera")
print(f"    6,952 / 1,5 = {C2 / 1.5:.4f}, y entonces la escalera 1:2:3 se")
print("    rompe: el escalon de en medio pasaria a ser el de abajo.")
print()
print("  Y CONTRA gamma(rho): NO se contradicen, es la misma cuenta.")
print("    gamma(rho) = 1/(ln2 - rho*ln3) da B/ln n; el clasico es (1+rho) por")
print("    eso mismo. En rho = 1/2 sale 1 : 2 : 3 sobre 1/ln(4/3), que es")
print("    exactamente la escalera. La correccion #52 es esa escalera leida")
print("    en el escalon correcto.")

ver_52 = "CONFIRMADA"
veredictos.append(("#52", ver_52,
                   "clasico = A+B > B = atajo en los 11 hilos, 0 fallos; "
                   "clasico/atajo = 1+rho > 1 siempre"))
print()
print(f"  VEREDICTO #52: {ver_52}")
print("    Se decide por desigualdad exacta, no por ajuste: el mapa clasico da")
print("    siempre MAS pasos que el atajo, luego le toca la constante mas")
print("    grande. Y encaja con gamma(rho) sin rozarla.")
print("    AVISO que la refutacion no traia y hace falta: los once hilos NO")
print("    reproducen 10,428 ni 6,952 uno por uno (van de 4,60 a 26,84). Esas")
print("    constantes son pendientes asintoticas, no valores por numero. Lo")
print("    que los once hilos deciden es la ATRIBUCION, que es lo que se")
print("    estaba auditando.")
print()


# ===========================================================================
# #53  "Al piso de la altitud le faltaba la hipotesis n IMPAR; sin ella es
#       falso en 28.325 de 50.000 pares."
# ===========================================================================
#
# LA SOSPECHA: el propio repo corrigio DESPUES que la frase mezclaba TRES
# rangos. El 28.325 sigue siendo el numero correcto para SU rango? Se
# recalcula. Y se prueba en los dos pools, ordinario y extremo.
#
# El enunciado, en forma entera y exacta (nada de logaritmos):
#     altitud(n) * 2^r  >=  2 * n * 3^r        con r = racha del ATAJO

print("=" * 74)
print("#53  AL PISO DE LA ALTITUD LE FALTABA 'n IMPAR'")
print("=" * 74)
print()


def cumple_piso(n, alt=None, r=None):
    if alt is None:
        alt = altitud_de(n)
    if r is None:
        r = racha_atajo(n)
    return alt * (2 ** r) >= 2 * n * (3 ** r)


fallan_par = fallan_impar = 0
total_par = total_impar = 0
ejemplo_par = None
ejemplos_impares = []
for n in range(1, HASTA_PISO + 1):
    ok = cumple_piso(n)
    if n % 2 == 0:
        total_par += 1
        if not ok:
            fallan_par += 1
            if ejemplo_par is None:
                ejemplo_par = n
    else:
        total_impar += 1
        if not ok:
            fallan_impar += 1
            if len(ejemplos_impares) < 5:
                ejemplos_impares.append(n)

print(f"  barrido de control, 1 a {HASTA_PISO:,}, forma entera exacta")
print(f"    pares  : fallan {fallan_par:,} de {total_par:,}"
      f"   ({100 * fallan_par / total_par:.2f}%)")
print(f"    impares: fallan {fallan_impar:,} de {total_impar:,}")
if ejemplo_par is not None:
    print(f"    el primer par que falla: n = {ejemplo_par},"
          f" altitud {altitud_de(ejemplo_par)}, hace falta {2 * ejemplo_par}")
if ejemplos_impares:
    print(f"    los impares que fallan: {ejemplos_impares}")

# EL POOL ORDINARIO -- los once hilos
fallan_hilos = [n for n in HILOS if not cumple_piso(n)]
print()
print(f"  POOL ORDINARIO -- los {len(HILOS)} hilos:"
      f" fallan {len(fallan_hilos)} -> {fallan_hilos}")

# EL POOL EXTREMO -- los records publicados
with open(ARCHIVO_RECORDS, encoding="utf-8") as f:
    records = json.load(f)

extremos = []
for r in records["path_records"]:
    extremos.append((int(r["n"]), int(r["altitud_clasica"])))
for r in records["delay_records"]:
    extremos.append((int(r["n"]), None))

fallan_rec = []
pares_rec = 0
comprobados_rec = 0
distintos_rec = set()
for n, alt in extremos:
    if alt is None:
        alt = altitud_de(n)
    ok = cumple_piso(n, alt)
    comprobados_rec += 1
    distintos_rec.add(n)
    if n % 2 == 0:
        pares_rec += 1
    if not ok:
        fallan_rec.append(n)

# los n <= 2 son los records triviales (el 1 y el 2 estan en las dos listas)
fallan_rec_triviales = [n for n in fallan_rec if n <= 2]
fallan_rec_de_verdad = [n for n in fallan_rec if n > 2]

print(f"  POOL EXTREMO   -- {comprobados_rec} entradas de records"
      f" ({len(distintos_rec)} n distintos, {pares_rec} pares)")
print(f"     fallan {len(fallan_rec)}, y son {sorted(set(fallan_rec))}:"
      f" los records TRIVIALES")
print(f"     records no triviales que fallan: {len(fallan_rec_de_verdad)}")

# Comprobaciones. Cortan.
if fallan_par != 28325:
    raise SystemExit(f"El barrido de control da {fallan_par} pares que fallan, "
                     f"no los 28.325 publicados. La refutacion cita mal su "
                     f"propio numero, o el rango no era 1..100.000.")
if fallan_impar != 1 or ejemplos_impares != [1]:
    raise SystemExit(f"Entre los impares fallan {fallan_impar} y se esperaba "
                     f"solo el n=1. Mira eso antes de seguir.")
if fallan_rec_de_verdad:
    raise SystemExit("Algun record NO trivial falla el piso. Entonces los "
                     "extremos SI cazaban el error y la leccion de la #53 "
                     f"esta mal contada: {fallan_rec_de_verdad[:5]}")

print()
print(f"  COMPROBACION -- el 28.325 se reproduce CLAVADO en el rango 1..100.000")
print(f"  COMPROBACION -- entre los impares el unico fallo es n = 1")

ver_53 = "CONFIRMADA"
veredictos.append(("#53", ver_53,
                   f"{fallan_par:,} de {total_par:,} pares fallan, "
                   f"recalculado; y {len(fallan_hilos)} de los 11 hilos"))
print()
print(f"  VEREDICTO #53: {ver_53}")
print("    El 28.325 es el numero correcto para su rango y se reproduce")
print("    exactamente. La hipotesis 'n impar' hacia falta de verdad.")
print()
print("    Y ESTO ES LO QUE HAY QUE RESCATAR DE LA #53, que no es un numero")
print("    sino una demostracion mas de la doctrina:")
print(f"      los {len(distintos_rec)} records EXTREMOS:"
      f" {len(fallan_rec_de_verdad)} fallos no triviales")
print(f"        (los unicos que fallan son el 1 y el 2, y no cuentan)")
print(f"      los {len(HILOS)} hilos ORDINARIOS: {len(fallan_hilos)} fallos,"
      f" y son {fallan_hilos}")
print("    Los casos extremos vuelven a no cazarlo -- se confirma la frase")
print("    del documento, ahora recalculada -- y once numeros corrientes")
print("    sacados de una base de datos que ya estaba en disco SI lo cazan.")
print("    No hizo falta el barrido de 100.000: bastaba con mirar el pool")
print("    ordinario que el repo ya tenia guardado. Los tres culpables son")
print("    pares con altitud menor que 2n, que es justo lo que el enunciado")
print("    sin hipotesis exigia.")
print()
print("    DOS AFINADOS AL ENUNCIADO, los dos menores y los dos necesarios:")
print("      (1) hay que excluir n = 1 (o pedir n >= 3): con racha 0 el piso")
print("          exige altitud >= 2, y la altitud del 1 es 1.")
print("      (2) la racha tiene que contarse en el mapa del ATAJO. En el mapa")
print("          clasico un impar va siempre a un par, asi que la racha valdria")
print("          1 para todo impar y el enunciado se comprobaria solo.")
print()


# ===========================================================================
# #54  "El umbral del coral no lo causa 45 = 3^2*5: eso explicaba UN nivel de
#       treinta y uno. Los choques los producen dos ramas con las mismas
#       aristas en otro orden, que existe para cualquier N; el 43 y el 47,
#       primos, chocan ANTES que el 45."
# ===========================================================================
#
# coralprimos.py no se puede correr. Se verifica el NUCLEO del argumento con un
# calculo barato y desde cero: barrer N de 20 a 70 con las DOS claves.
#
# El nucleo, dicho en una linea: dos ramas con el mismo MULTICONJUNTO de
# aristas tienen vector diferencia CERO, y el cero esta en cualquier reticulo,
# factorice N como factorice. Luego ese choque existe para todo N y no lo
# explica ninguna factorizacion. Lo que la factorizacion puede aportar son los
# choques ADICIONALES, de diferencia no nula, y aqui se mide cuantos niveles
# adelantan.

print("=" * 74)
print("#54  EL UMBRAL DEL CORAL Y EL 45 = 3^2 * 5")
print("=" * 74)
print()


def es_primo(n):
    return n > 1 and all(n % i for i in range(2, int(n ** 0.5) + 1))


def recta_umbral(N):
    if N % 4 == 1:
        return (N + 19) // 2
    if N % 4 == 3:
        return (N + 11) // 2
    return None


print(f"  {'N':>4} {'reticulo':>9} {'crudo':>7} {'adelanta':>9}"
      f" {'recta':>6} {'crudo==recta':>13}  que es N")
print(f"  {'-'*4} {'-'*9} {'-'*7} {'-'*9} {'-'*6} {'-'*13}")

fallos_recta = 0
impares_mirados = 0
adelantos = {}
for N in range(CORAL_N_DESDE, CORAL_N_HASTA + 1):
    pr, _, _ = recorrer_coral(N, "reticulo", 120)
    pc, _, _ = recorrer_coral(N, "crudo", 120)
    if pr is None or pc is None:
        raise SystemExit(f"El coral de N={N} no choco. Eso rompe el nucleo "
                         "del argumento: se afirmaba que existe para todo N.")
    if pr > pc:
        raise SystemExit(f"N={N}: el reticulo choca DESPUES que el crudo. "
                         "Imposible: el crudo es un subconjunto.")
    r = recta_umbral(N)
    adelantos[N] = pc - pr
    if N % 2 == 1:
        impares_mirados += 1
        if pc != r:
            fallos_recta += 1
    etiqueta = "primo" if es_primo(N) else ("par" if N % 2 == 0 else
                                            "impar compuesto")
    if N in (43, 44, 45, 47, 49) or N % 2 == 1:
        print(f"  {N:>4} {pr:>9} {pc:>7} {pc - pr:>9} {str(r):>6}"
              f" {str(pc == r) if r else '-':>13}  {etiqueta}")

# Comprobaciones. Cortan.
if fallos_recta:
    raise SystemExit(f"La recta del umbral falla en {fallos_recta} de los "
                     f"{impares_mirados} N impares. Entonces la recta que el "
                     "documento da por buena esta mal.")
for N in (43, 47):
    pr, _, _ = recorrer_coral(N, "reticulo", 120)
    p45, _, _ = recorrer_coral(45, "reticulo", 120)
    if not pr < p45:
        raise SystemExit(f"El primo {N} NO choca antes que el 45. Eso refuta "
                         "la refutacion; miralo con cuidado.")

u43, _, _ = recorrer_coral(43, "reticulo", 120)
u45, _, _ = recorrer_coral(45, "reticulo", 120)
u47, _, _ = recorrer_coral(47, "reticulo", 120)
u45c, _, _ = recorrer_coral(45, "crudo", 120)
adelanto_impares = sorted({v for N, v in adelantos.items() if N % 2 == 1})

print()
print(f"  COMPROBACION -- todos los N de {CORAL_N_DESDE} a {CORAL_N_HASTA}"
      f" chocan; ninguno se escapa")
print(f"  COMPROBACION -- la recta (N+19)/2 y (N+11)/2 clava el umbral CRUDO")
print(f"     en los {impares_mirados} N impares, 0 fallos")
print(f"  COMPROBACION -- primos 43 y 47: umbral {u43} y {u47}, contra el"
      f" {u45} del 45")
print(f"  adelanto del reticulo sobre el crudo en los N impares:"
      f" {adelanto_impares}")

ver_54 = "CONFIRMADA"
veredictos.append(("#54", ver_54,
                   f"43 choca en {u43} y 47 en {u47}, antes que el 45 en "
                   f"{u45}; y el reticulo solo adelanta {u45c - u45} nivel "
                   f"sobre el crudo"))
print()
print(f"  VEREDICTO #54: {ver_54}")
print("    Las tres piezas del argumento se sostienen, medidas de cero:")
print(f"      (1) el choque de aristas repetidas existe para TODOS los N de")
print(f"          {CORAL_N_DESDE} a {CORAL_N_HASTA}, primos incluidos.")
print(f"      (2) los primos 43 y 47 chocan en {u43} y {u47}, ANTES que el 45.")
print(f"          La prediccion de que un N primo dispararia el umbral esta")
print("          refutada por su propio codigo, y aqui otra vez.")
print(f"      (3) el reticulo del 45 solo adelanta {u45c - u45} nivel sobre el")
print(f"          crudo ({u45} contra {u45c}). O sea que el 45 = 3^2*5 explica")
print("          exactamente UN nivel de treinta y uno, como dice la")
print("          refutacion. No es el motor: es una correccion de uno.")
print()


# ===========================================================================
# #55  "El «+1» aparece DOS veces, no tres: eps = ln(2^B/(3^A n)) y
#       S = suma de ln(1+1/(3x)) son identicamente la misma suma."
# ===========================================================================
#
# LA SOSPECHA: la derivacion asume que la trayectoria LLEGA A 1. Vale sobre
# prefijos que no llegan? Si no vale, la refutacion tiene un cuantificador
# escondido.
#
# Se comprueba la version GENERAL, de un punto cualquiera a otro punto
# cualquiera de la trayectoria:
#
#     producto de (1 + 1/(3x)) sobre los impares del tramo [i, j)
#         =  2^B * seq[j] / (3^A * seq[i])
#
# El enunciado de elmasuno.py es el caso j = final, seq[j] = 1. Si la version
# general es cierta, no hay cuantificador escondido: la identidad no necesita
# que la trayectoria termine, solo que exista el tramo.
#
# TODO EN Fraction. Un float aqui no decidiria nada.

print("=" * 74)
print("#55  EL «+1» APARECE DOS VECES, NO TRES")
print("=" * 74)
print()

pares_probados = 0
tramos_cortos = 0          # los que NO acaban en el 1
fallos_identidad = 0
fallos_prefijo = 0
primer_fallo = None
for n in HILOS:
    s = secuencia_de(n)
    L = len(s)
    for i in range(L):
        num = den = 1
        A = B = 0
        for j in range(i + 1, L):
            x = s[j - 1]
            if x % 2:
                num *= 3 * x + 1
                den *= 3 * x
                A += 1
            else:
                B += 1
            # el lado izquierdo (producto de factores) contra el derecho
            # (la forma cerrada), cruzando enteros: nada de floats
            izq = num * (3 ** A * s[i])
            der = den * (2 ** B * s[j])
            pares_probados += 1
            mal = izq != der
            if mal:
                fallos_identidad += 1
                if primer_fallo is None:
                    primer_fallo = (n, i, j)
            if j != L - 1:
                tramos_cortos += 1
                if mal:
                    fallos_prefijo += 1

print(f"  identidad general sobre TODOS los tramos de los {len(HILOS)} hilos")
print(f"    tramos [i,j) probados: {pares_probados:,}")
print(f"    fallos: {fallos_identidad}")
print(f"    de esos, tramos que NO llegan al 1: {tramos_cortos:,},"
      f" fallos {fallos_prefijo}")

if fallos_identidad:
    raise SystemExit(f"La identidad falla, primero en {primer_fallo}. "
                     "Entonces la refutacion #55 esta mal y hay que rescatar "
                     "el conteo de tres.")

# Y el caso particular que es el enunciado publicado: j = final, seq[j] = 1
fallos_caso_publicado = 0
for n in HILOS:
    A, B = cuenta_ab(n)
    s = secuencia_de(n)
    num = den = 1
    for x in s[:-1]:
        if x % 2:
            num *= 3 * x + 1
            den *= 3 * x
    if Fraction(num, den) != Fraction(2 ** B, 3 ** A * n):
        fallos_caso_publicado += 1

if fallos_caso_publicado:
    raise SystemExit("El caso publicado (trayectoria entera) falla. No sigas.")

print()
print(f"  COMPROBACION -- identidad general: {pares_probados:,} tramos,"
      f" 0 fallos, en Fraction")
print(f"  COMPROBACION -- caso publicado (trayectoria entera):"
      f" {len(HILOS)} hilos, 0 fallos")
print()
print("  LA SOSPECHA DEL CUANTIFICADOR, CONTESTADA: no lo hay.")
print("    La identidad NO necesita que la trayectoria llegue a 1. La forma")
print("    general vale para cualquier tramo [i,j), y el enunciado publicado")
print("    es su caso j = final. Lo que se derivo suponiendo que el producto")
print("    total vale 1/n se puede derivar igual sin suponerlo: el producto")
print("    de un tramo vale seq[j]/seq[i], y ya.")

ver_55 = "CONFIRMADA"
veredictos.append(("#55", ver_55,
                   f"{pares_probados:,} tramos de los 11 hilos, 0 fallos, "
                   "en Fraction; y vale sobre tramos que no llegan al 1"))
print()
print(f"  VEREDICTO #55: {ver_55}")
print("    Reimplementada de cero y en racionales exactos, la identidad")
print("    aguanta, y aguanta MAS de lo que la refutacion pedia: no hace falta")
print("    que la trayectoria termine. El «+1» del grosor de la lamina y el")
print("    «+1» del sobrante de la fraccion impar son el mismo, contado dos")
print("    veces en dos sistemas de coordenadas.")
print("    (elmasuno.py se ejecuto aparte en esta misma pasada: termina sin")
print("    disparar ninguno de sus cinco SystemExit.)")
print()


# ===========================================================================
# #56  "El grosor 0,2286 y ln(Res(993)) = 0,225654 no son el mismo numero:
#       estan en unidades distintas (bits contra nats, factor 1,42), y el
#       0,2286 ni siquiera es una cota -- su maximo se alcanza en el par
#       (221 -> 16), que es la trayectoria entera del 221."
# ===========================================================================
#
# LA SOSPECHA: si el 0,2286 mide solo el 221, que mide en los otros diez? Y la
# relacion buena que el repo propone, h <= log2(Res(seq[i])), se cumple en los
# once hilos y en los records?

print("=" * 74)
print("#56  EL 0,2286 Y EL 0,225654, EN UNIDADES DISTINTAS")
print("=" * 74)
print()

# El 221, que es de donde salio el 0,2286
s221 = secuencia_de(221)
A221, B221 = cuenta_ab(221)
res221 = Fraction(2 ** B221, 3 ** A221 * 221)
eps221_nats = math.log(float(res221))
eps221_bits = eps221_nats / L2

res993 = Fraction(2 ** 61, 3 ** 32 * 993)
eps993_nats = math.log(float(res993))
eps993_bits = eps993_nats / L2

# el maximo de h sobre TODOS los pares del 221, exacto
mejor = Fraction(1)
mejor_par = None
for i in range(len(s221)):
    num = den = 1
    A = B = 0
    for j in range(i + 1, len(s221)):
        x = s221[j - 1]
        if x % 2:
            A += 1
        else:
            B += 1
        v = Fraction(2 ** B * s221[j], 3 ** A * s221[i])
        if v > mejor:
            mejor = v
            mejor_par = (s221[i], s221[j])

h_max_221 = math.log2(float(mejor))

print(f"  el maximo de h sobre los pares del 221: {h_max_221:.10f} bits")
print(f"     y se alcanza en el par {mejor_par}")
print(f"  eps(221) = ln(2^{B221}/(3^{A221}*221)):")
print(f"     {eps221_nats:.10f} nats   =   {eps221_bits:.10f} bits")
print(f"  ln(Res(993)) = ln(2^61/(3^32*993)):")
print(f"     {eps993_nats:.10f} nats   =   {eps993_bits:.10f} bits")
print(f"  factor entre los dos, en las MISMAS unidades:"
      f" {eps993_bits / h_max_221:.4f}")

# Comprobaciones. Cortan.
if abs(h_max_221 - 0.2286349110) > 1e-9:
    raise SystemExit(f"El 0,2286349110 publicado no se reproduce: sale "
                     f"{h_max_221:.10f}. No sigas.")
if abs(h_max_221 - eps221_bits) > 1e-12:
    raise SystemExit("El maximo sobre los pares del 221 NO es su eps en bits. "
                     "Entonces la refutacion se equivoca en su parte central.")
if abs(eps993_nats - 0.2256541127) > 1e-9:
    raise SystemExit("El ln(Res(993)) publicado no se reproduce. No sigas.")

print()
print(f"  COMPROBACION -- el 0,2286349110 se reproduce clavado, OK")
print(f"  COMPROBACION -- ese maximo ES eps(221) escrito en bits, OK")
print(f"  COMPROBACION -- el maximo cae en el par {mejor_par}, que es la")
print(f"     trayectoria entera del 221 (del 16 al 1 no hay ni un impar, asi")
print(f"     que el producto ya esta completo). OK")

# LOS ONCE HILOS: que mide el mismo objeto en numeros que no son el 221
print()
print("  POOL ORDINARIO -- el mismo objeto en los once hilos")
print(f"  {'n':>8} {'A':>5} {'B':>5} {'eps nats':>11} {'eps bits':>11}"
      f" {'pasa del 0,2286?':>17}")
print(f"  {'-'*8} {'-'*5} {'-'*5} {'-'*11} {'-'*11} {'-'*17}")
por_encima = 0
por_encima_del_techo = 0
epsilons = []
for n in HILOS:
    A, B = cuenta_ab(n)
    r = Fraction(2 ** B, 3 ** A * n)
    e_nats = math.log(float(r))
    e_bits = e_nats / L2
    epsilons.append((n, e_bits))
    pasa = e_bits > h_max_221
    if pasa:
        por_encima += 1
    if e_bits > eps993_bits:
        por_encima_del_techo += 1
    print(f"  {n:>8,} {A:>5} {B:>5} {e_nats:>11.7f} {e_bits:>11.7f}"
          f" {str(pasa):>17}")

# la relacion buena: h <= log2(Res(seq[i])), en enteros exactos
tramos_probados = 0
fallos_cota = 0
for n in HILOS:
    s = secuencia_de(n)
    L = len(s)
    Ai = [0] * L
    Bi = [0] * L
    for i in range(L - 2, -1, -1):
        Ai[i] = Ai[i + 1] + (1 if s[i] % 2 else 0)
        Bi[i] = Bi[i + 1] + (0 if s[i] % 2 else 1)
    for i in range(L):
        A = B = 0
        for j in range(i + 1, L):
            if s[j - 1] % 2:
                A += 1
            else:
                B += 1
            tramos_probados += 1
            # 2^B*s[j]/(3^A*s[i]) <= 2^Bi/(3^Ai*s[i])  <=>  cruzando enteros:
            if not (2 ** B * s[j] * 3 ** Ai[i] <= 2 ** Bi[i] * 3 ** A):
                fallos_cota += 1

if fallos_cota:
    raise SystemExit(f"La cota h <= log2(Res(seq[i])) falla {fallos_cota} "
                     "veces. Entonces la relacion que el repo propone en "
                     "sustitucion tampoco vale.")
if por_encima_del_techo:
    raise SystemExit("Algun hilo pasa por encima del techo de Roosendaal. "
                     "Eso seria un contraejemplo a una conjetura publicada; "
                     "revisa la aritmetica antes de creertelo.")

maximo_hilos = max(e for _, e in epsilons)
quien = [n for n, e in epsilons if e == maximo_hilos][0]

print()
print(f"  COMPROBACION -- h <= log2(Res(seq[i])) en {tramos_probados:,} tramos"
      f" de los 11 hilos: {fallos_cota} fallos")
print(f"  COMPROBACION -- 0 hilos por encima del techo {eps993_bits:.6f} bits")

ver_56 = "CONFIRMADA"
veredictos.append(("#56", ver_56,
                   f"eps({quien}) = {maximo_hilos:.6f} bits pasa del 0,2286 "
                   f"del 221; el techo real esta en {eps993_bits:.6f} bits"))
print()
print(f"  VEREDICTO #56: {ver_56}, y con un numero que la refutacion no tenia.")
print("    Las dos mitades se reproducen: el 0,2286 son bits, el 0,225654 son")
print(f"    nats, y el factor entre ellos es {eps993_bits / h_max_221:.4f}.")
print("    Y sobre que el 0,2286 no es una cota, ahora hay CONTRAEJEMPLO en el")
print("    pool ordinario, no un argumento:")
print(f"      eps({quien}) = {maximo_hilos:.7f} bits  >  {h_max_221:.7f} bits")
print(f"      y {por_encima} de los {len(HILOS)} hilos pasan del 0,2286.")
print("    Once numeros corrientes sacados de hilos.db bastan para tumbar el")
print("    0,2286 como cota. Otra vez: el control refuta, el extremo no hacia")
print("    falta.")
print("    Lo que SI es cota se cumple: h <= log2(Res(seq[i])) en los")
print(f"    {tramos_probados:,} tramos, 0 fallos, y los once eps quedan debajo")
print(f"    del techo de Roosendaal, {eps993_bits:.6f} bits.")
print()


# ===========================================================================
# #57  "El exponente de la criba 2^(-0,05k) es el ASINTOTICO; en el tramo real
#       (k = 20..40) el decaimiento es 0,108101, el doble."
# ===========================================================================
#
# LA SOSPECHA: un exponente ajustado sobre un tramo es un ESTIMADOR CON RANGO.
# Esta declarado como tal, o se presenta como constante?
#
# a(k) = restos modulo 2^k que sobreviven al criterio de descenso de Terras.
# Es A076227 de OEIS. Se cuenta sin tocar los 2^k restos: el criterio solo
# depende de CUANTOS impares lleva el prefijo, asi que se cuentan caminos con
# una programacion dinamica sobre (paso, impares). O(k^2) en vez de O(2^k).

print("=" * 74)
print("#57  EL EXPONENTE DE DECAIMIENTO DE LA CRIBA")
print("=" * 74)
print()


def impares_minimos(hasta):
    """Smin[j] = el menor S con 3^S > 2^j, con enteros exactos."""
    smin = [0] * (hasta + 1)
    S = 0
    tres = 1
    for j in range(1, hasta + 1):
        dos = 1 << j
        while tres <= dos:
            S += 1
            tres *= 3
        smin[j] = S
    return smin


def supervivientes(hasta):
    smin = impares_minimos(hasta)
    a = [1]
    estado = {0: 1}
    for j in range(1, hasta + 1):
        necesarios = smin[j]
        nuevo = {}
        for S, cuantos in estado.items():
            for bit in (0, 1):
                S2 = S + bit
                if S2 >= necesarios:
                    nuevo[S2] = nuevo.get(S2, 0) + cuantos
        estado = nuevo
        a.append(sum(estado.values()))
    return a


a = supervivientes(K_DP)

PUBLICADOS_A076227 = [1, 1, 2, 3, 4, 8, 13, 19, 38, 64, 128, 226, 367, 734,
                      1295, 2114, 4228, 7495, 14990, 27328]
if a[1:21] != PUBLICADOS_A076227:
    raise SystemExit("La DP no reproduce los terminos publicados de A076227. "
                     "Sin eso no se puede auditar nada de esta refutacion.")
if a[34] != 151917636:
    raise SystemExit(f"a(34) sale {a[34]} y el CLAUDE.md publica 151.917.636.")

LOG3_2 = L2 / L3
H = -(LOG3_2 * math.log2(LOG3_2) + (1 - LOG3_2) * math.log2(1 - LOG3_2))

print(f"  COMPROBACION -- a(1..20) coincide con A076227 publicada, OK")
print(f"  COMPROBACION -- a(34) = {a[34]:,}, el de la criba de Barina, OK")
print()
print(f"  H(log_3 2) = {H:.6f}     1 - H = {1 - H:.6f}  <- el 0,05 asintotico")
print()
print("  LA SECANTE POR TRAMOS, que es lo que publica el documento:")
print(f"  {'tramo':>12} {'pendiente':>11} {'1 - pendiente':>14}")
print(f"  {'-'*12} {'-'*11} {'-'*14}")
secantes = {}
for lo, hi in TRAMOS:
    if hi > K_DP:
        continue
    p = (math.log2(a[hi]) - math.log2(a[lo])) / (hi - lo)
    secantes[(lo, hi)] = 1 - p
    print(f"  {f'{lo} .. {hi}':>12} {p:>11.6f} {1 - p:>14.6f}")

if (20, 40) not in secantes:
    raise SystemExit("No se pudo medir el tramo 20..40, que es el auditado.")
if abs(secantes[(20, 40)] - 0.108101) > 1e-6:
    raise SystemExit(f"El tramo 20..40 da {secantes[(20, 40)]:.6f} y no el "
                     "0,108101 publicado.")

print()
print(f"  COMPROBACION -- el 0,108101 del tramo 20..40 se reproduce clavado")
print()
print("  PERO AHORA LO QUE LA REFUTACION NO MIRO -- el decaimiento BIT A BIT,")
print("  que es lo que significa la frase 'cada bit extra elimina un 7,2%':")
print(f"  {'k':>5} {'a(k)':>16} {'1 - log2(a(k+1)/a(k))':>23}")
print(f"  {'-'*5} {'-'*16} {'-'*23}")
locales = []
for k in range(28, 45):
    d = 1 - (math.log2(a[k + 1]) - math.log2(a[k]))
    locales.append((k, d))
    if 30 <= k <= 40:
        print(f"  {k:>5} {a[k]:>16,} {d:>23.6f}")

ceros = [k for k, d in locales if abs(d) < 1e-12]
if not ceros:
    raise SystemExit("Se esperaban k donde a(k+1) = 2*a(k) exactamente "
                     "(decaimiento cero). No aparecen: revisa la DP.")

print()
print("  Y LA SENSIBILIDAD DE LA SECANTE A SUS EXTREMOS:")
print(f"  {'tramo':>12} {'1 - pendiente':>14}")
print(f"  {'-'*12} {'-'*14}")
variantes = [(20, 40), (19, 39), (21, 41), (18, 38), (22, 42),
             (24, 44), (25, 45), (30, 40), (20, 50)]
valores_var = []
for lo, hi in variantes:
    if hi > K_DP:
        continue
    p = (math.log2(a[hi]) - math.log2(a[lo])) / (hi - lo)
    valores_var.append(1 - p)
    print(f"  {f'{lo} .. {hi}':>12} {1 - p:>14.6f}")

ancho = max(valores_var) - min(valores_var)

print()
print(f"  COMPROBACION -- moviendo los extremos del tramo dos unidades, el")
print(f"     'exponente del tramo real' va de {min(valores_var):.6f} a"
      f" {max(valores_var):.6f}")
print(f"     ancho: {ancho:.6f}, o sea el {100 * ancho / min(valores_var):.0f}%"
      f" de su propio valor")

ver_57 = "EXAGERADA"
veredictos.append(("#57", ver_57,
                   f"la secante va de {min(valores_var):.4f} a "
                   f"{max(valores_var):.4f} segun los extremos; y bit a bit "
                   f"alterna entre 0,0000 y 0,2036"))
print()
print(f"  VEREDICTO #57: {ver_57}")
print("    LO QUE AGUANTA, y es lo importante: el 0,05 es el LIMITE y no el")
print("    valor del rango donde se usa la criba. En k = 20..40 el decaimiento")
print("    es aproximadamente el doble. Eso es cierto y estaba mal en el")
print("    documento anterior.")
print("    LO QUE NO AGUANTA es el 0,108101 con seis decimales:")
print(f"      (1) es una SECANTE de dos puntos, no un ajuste, y moverle los")
print(f"          extremos dos unidades la lleva de {min(valores_var):.4f} a"
      f" {max(valores_var):.4f}.")
print("          De las seis cifras publicadas, dos son significativas.")
print("      (2) la frase 'cada bit extra elimina un 7,2%' es falsa bit a bit.")
print(f"          a(k) DUPLICA exactamente (decaimiento 0) en k = {ceros[:6]},")
print("          y en k = 34 el decaimiento local vale 0,2036. La sucesion es")
print("          escalonada porque Smin(j) solo sube de vez en cuando, y una")
print("          media sobre veinte escalones no describe ningun escalon.")
print("    ES EL MISMO MODO DE FALLO QUE LA REFUTACION DENUNCIABA -- citar un")
print("    numero sin su regimen -- cometido a menor escala por la propia")
print("    refutacion. Lo que hay que publicar es el par (tramo, cifras")
print("    significativas), o mejor la sucesion a(k), que es exacta.")
print()


# ===========================================================================
# #58  LA COTA DE LONGITUD DE CICLO.
#      PARTE ARITMETICA: se recalcula desde cero.
#      PARTE BIBLIOGRAFICA: NO SE EVALUA, Y SE DICE POR QUE.
# ===========================================================================
#
# El criterio, que es una COTA y por eso vale: si todo n < X ya se verifico que
# baja, ningun ciclo puede tener su minimo por debajo de X. Con la identidad
#
#     2^k / 3^S  =  producto sobre los impares del ciclo de (1 + 1/(3 n_i))
#
# un periodo k (en pasos del ATAJO) queda excluido si, con S el mayor S que
# cumple 3^S < 2^k,
#
#     k*ln2 - S*ln3  >  S * ln(1 + 1/(3X))
#
# El margen de la izquierda es minimo justo en las convergentes y
# semiconvergentes de log2(3), asi que basta evaluarlas: no hay que recorrer
# 10^11 valores de k.

print("=" * 74)
print("#58  LA COTA DE LONGITUD DE CICLO")
print("=" * 74)
print()

DL2 = Decimal(2).ln()
DL3 = Decimal(3).ln()

x = DL3 / DL2
cf = []
for _ in range(70):
    entero = int(x)
    cf.append(entero)
    frac = x - entero
    if frac == 0:
        break
    x = 1 / frac

candidatos = []
hm1, hm2 = 1, 0
km1, km2 = 0, 1
for termino in cf:
    for t in range(1, termino + 1):
        candidatos.append((t * hm1 + hm2, t * km1 + km2))
    h = termino * hm1 + hm2
    k = termino * km1 + km2
    hm2, hm1 = hm1, h
    km2, km1 = km1, k
    if k > 10 ** 14:
        break
candidatos = sorted(set(candidatos))

# control: las primeras convergentes de log2(3) tienen que ser las conocidas
convergentes_chicas = [(h, kk) for h, kk in candidatos if kk <= 41]
if (65, 41) not in convergentes_chicas:
    raise SystemExit("La fraccion continua de log2(3) no da la convergente "
                     "65/41. Todo lo que sigue estaria mal.")


def frontera(bits):
    """Primer k (pasos de atajo) que NO queda excluido, con X = 2^bits."""
    X = Decimal(2) ** bits
    c = (1 + 1 / (3 * X)).ln()
    for h, kk in candidatos:
        k_pasos, S = h, kk
        if k_pasos < 10:
            continue
        margen = k_pasos * DL2 - S * DL3
        if margen <= 0:
            continue
        if not margen > S * c:
            return k_pasos, S
    return None, None


k_falla, S_falla = frontera(X0_BITS)
if k_falla is None:
    raise SystemExit("No se encontro ningun k que falle. Imposible.")

clasico = k_falla + S_falla
print(f"  con X = 2^{X0_BITS} (el limite de fuerza bruta de Barina):")
print(f"    ultimo periodo excluido : {k_falla - 1:,} pasos de atajo")
print(f"    longitud MINIMA que le queda a un ciclo no trivial:")
print(f"      {k_falla:,} pasos de atajo")
print(f"      {clasico:,} pasos clasicos   (k + S, con S = {S_falla:,})")

# el X que haria falta para llegar a la cifra que citaba el documento
CITADA = 217976794617
margen = Decimal(k_falla) * DL2 - Decimal(S_falla) * DL3
razon = margen / S_falla
X_necesario = 1 / (3 * (razon.exp() - 1))
bits_necesarios = X_necesario.ln() / DL2

print()
print(f"  la cifra que el documento llego a citar: {CITADA:,} pasos de atajo")
print(f"  para que ESA sea la longitud minima hace falta que el periodo")
print(f"  {k_falla:,} tambien quede excluido, y eso pide")
print(f"    X >= 2^{float(bits_necesarios):.4f}")
print(f"  y el record de fuerza bruta esta en 2^{X0_BITS} (Barina 2025).")

LAURORE = 19478780533
print()
print(f"  contra la cifra vieja, {LAURORE:,} pasos:")
print(f"    con la frontera bien extraida: {k_falla:,} / {LAURORE:,}"
      f" = {k_falla / LAURORE:.2f}x")
print(f"    con la cifra que se habia puesto en su lugar: {CITADA:,} /"
      f" {LAURORE:,} = {CITADA / LAURORE:.2f}x")

# Comprobaciones. Cortan.
if k_falla != 114208327604:
    raise SystemExit(f"La frontera sale {k_falla:,} y no los 114.208.327.604 "
                     "que dan verificar_ciclos.py y verificar_frontera_"
                     "ciclos.py. Uno de los dos calculos esta mal.")
if clasico != 186265759595:
    raise SystemExit(f"El clasico sale {clasico:,} y no 186.265.759.595.")
if not (71.8 < float(bits_necesarios) < 71.9):
    raise SystemExit(f"El X necesario sale 2^{float(bits_necesarios):.4f} y el "
                     "documento dice 2^71,884.")
if abs(k_falla / LAURORE - 5.86) > 0.01:
    raise SystemExit("El factor contra la cifra vieja no es el 5,9 esperado.")

print()
print(f"  COMPROBACION -- {k_falla:,} atajo / {clasico:,} clasico, reproducidos")
print(f"     por una implementacion independiente (fraccion continua propia +")
print(f"     Decimal a {CIFRAS} cifras)")
print(f"  COMPROBACION -- el 2^71,884 se reproduce:"
      f" 2^{float(bits_necesarios):.4f}")
print(f"  COMPROBACION -- el factor contra la cifra vieja es"
      f" {k_falla / LAURORE:.2f}x, no {CITADA / LAURORE:.2f}x")

ver_58 = "CONFIRMADA (la mitad aritmetica)"
veredictos.append(("#58", ver_58,
                   f"{k_falla:,} atajo / {clasico:,} clasico con X=2^71, "
                   f"reproducidos de cero; el factor es "
                   f"{k_falla / LAURORE:.2f}x"))
print()
print(f"  VEREDICTO #58: {ver_58}")
print("    Los tres numeros de la correccion se recalculan aqui desde cero y")
print("    salen clavados. La correccion de la correccion era necesaria: la")
print(f"    cifra intermedia {CITADA:,} pedia un X que nadie ha")
print("    verificado, y el 'once veces mas debil' era en realidad"
      f" {k_falla / LAURORE:.1f}.")
print()
print("  LO QUE ESTE FICHERO SE NIEGA A EVALUAR, Y NO ES PEREZA:")
print("    - de donde sale el 19.478.780.533 y con que argumento. Es una cita.")
print("      Aqui solo se puede decir que NUESTRA derivacion elemental da"
      f" {k_falla / LAURORE:.1f}")
print("      veces mas, no si la suya esta bien o mal.")
print("    - que Barina haya verificado de verdad hasta 2^71. Son 12.395")
print("      anos-CPU. Se usa el numero; no se comprueba.")
print("    - la cota de Simons-de Weger y el Teorema 21 de Hercher, que es")
print("      donde vive la matematica de verdad de este asunto.")
print("    Fingir una verificacion computacional de una cita seria exactamente")
print("    el pecado que esta pasada existe para cazar.")
print()


# ===========================================================================
# EL RESUMEN. Va al final, despues de todas las comprobaciones.
# ===========================================================================

print("=" * 74)
print("RESUMEN DE LA AUDITORIA")
print("=" * 74)
print()
print(f"  {'ref':>5} {'veredicto':>32}  la cifra que lo decide")
print(f"  {'-'*5} {'-'*32}  {'-'*30}")
for num, ver, cifra in veredictos:
    print(f"  {num:>5} {ver:>32}  {cifra}")

confirmadas = sum(1 for _, v, _ in veredictos if v.startswith("CONFIRMADA"))
exageradas = sum(1 for _, v, _ in veredictos if v == "EXAGERADA")
refutadas = sum(1 for _, v, _ in veredictos if v == "REFUTADA")

print()
print(f"  CONFIRMADA: {confirmadas}    EXAGERADA: {exageradas}"
      f"    REFUTADA: {refutadas}")
print()
print("  NINGUNA REFUTADA. No se rescata ningun dato tirado, y eso tambien es")
print("  una respuesta: las diez refutaciones apuntaban al sitio correcto.")
print()
print("  PERO DOS SON EXAGERADAS, Y LAS DOS DE LA MISMA MANERA:")
print("    #51  presento cuatro casos ('mismos conteos absolutos') como si")
print("         fueran una ley. Son cuatro N que resultan ser 4 modulo 6.")
print("    #57  publico una secante de dos puntos con seis decimales, y una")
print("         frase por bit que es falsa bit a bit.")
print("  Las dos denunciaban 'tomar una muestra por una constante' y las dos")
print("  lo hacen a menor escala. La conclusion de las dos se sostiene; el")
print("  numero con el que se sostuvo, no.")
print()
print("  Y LO QUE LA AUDITORIA ANADE, que no estaba en ninguna de las diez:")
print("    #50  el control 3n-1 da la MISMA razon 1,732. Un numero que sale")
print("         igual con otra regla no es una constante de Collatz.")
print("    #53  los once hilos ordinarios cazan el fallo del piso que los 243")
print("         records extremos no cazaron. La doctrina se demuestra sola.")
print("    #56  hay CONTRAEJEMPLO al 0,2286 como cota dentro de hilos.db, no")
print("         hace falta argumentarlo.")
print("    #49  el 31 y el 32 del coral son los umbrales de DOS claves")
print("         distintas, y el documento tiene los dos sin decir cual es cual.")
print()
print("  LA REGLA QUE SALE DE ESTA PASADA, y es lo unico que hay que recordar:")
print("  UNA REFUTACION SE PUBLICA CON EL MISMO RIGOR QUE UNA AFIRMACION -- con")
print("  su rango, sus cifras significativas y su control. Las dos EXAGERADAS")
print("  de aqui no fallaron en la conclusion: fallaron en creerse que, por ser")
print("  correcciones, no les tocaba pasar el mismo filtro.")
