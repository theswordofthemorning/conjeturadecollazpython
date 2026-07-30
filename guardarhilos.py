# guardarhilos.py
#
# LOS ONCE HILOS, EN UNA BASE DE DATOS, Y LA MALLA QUE FORMAN AL CRUZARSE.
#
# Se toman los once numeros 100000 ... 100010, se les aplica Collatz hasta el
# 1, y se guarda TODO en sqlite (hilos.db). Despues se cruza cada paso de cada
# hilo contra cada paso de todos los demas, y ese cruce tambien se guarda.
#
# LA PREGUNTA QUE SE ESTA HACIENDO: no "que valor sale", sino "en que PASO
# sale". Paso 13 del hilo 1 contra paso 13 del hilo 2. Y contra todos los
# pasos del hilo 2. La malla completa.
#
# LO QUE SE ENCUENTRA (y esto no es opinion, esta medido abajo):
#
#   Los hilos SE FUNDEN. Cuando dos trayectorias pisan el mismo numero, a
#   partir de ahi son la misma trayectoria para siempre. Y varias de las
#   fusiones ocurren con DESFASE CERO: paso 18 contra paso 18. De ahi que
#   100002 ... 100007 tarden los seis exactamente 53 pasos.
#
# LA TRAMPA, Y HAY QUE MATARLA ANTES DE MIRAR NADA:
#
#   TODAS las trayectorias terminan en 4-2-1. Asi que TODAS "se funden" al
#   final, siempre, sin excepcion y sin significado. Esa cola comun llena la
#   malla de coincidencias espectaculares que no dicen nada. Aqui se calcula
#   la cola comun a los once y se marca cada cruce como cola o no cola. Solo
#   los cruces de fuera de la cola son informacion.
#
# ESTO YA ESTA EN LA LITERATURA, y conviene saberlo antes de entusiasmarse:
#
#   - Garner (1985) demostro que hay infinitos pares de enteros consecutivos
#     con la misma altura y el mismo tiempo de parada total, estudiando
#     exactamente como se funden las trayectorias de consecutivos.
#   - Gao (1993): si existe UNA tupla de k consecutivos con la misma altura,
#     existen infinitas. Hay una tupla de 35.654 empezando en 2^500 + 1.
#   - Wu Jia-Bang (1992,1993,1995): la tupla mas larga bajo 2^30 es de 176,
#     empezando en 722.067.240; y encontro una de 310 en 6.622.073.000.
#   - Wu y Huang (2001): las familias de pares consecutivos que se funden son
#     progresiones aritmeticas modulo 2^k. Dan ejemplos publicados:
#         (32m+5, 32m+6),  (64m+45, 64m+46),  (128m+29, 128m+30)
#     La COMPROBACION 4 de abajo usa esto: 100005 = 32*3125 + 5, o sea que
#     nuestro par (100005, 100006) es un caso de la primera familia. Si la
#     literatura tiene razon, ese par se funde para CUALQUIER m. Se comprueba.
#   - Oliveira e Silva usa la fusion de n y n-1 como optimizacion industrial
#     de su criba: le quita el 17,5% de las hojas del arbol de busqueda.
#
# El programa comprueba las cuatro cosas antes de dar la base por buena.

import os
import sqlite3

# ---------------------------------------------------------------------------
# Cambia esto aqui, guarda, y dale a Ctrl+B en Sublime.
# ---------------------------------------------------------------------------

PRIMERO = 100000      # el primer numero de la tanda
CUANTOS = 11          # cuantos numeros seguidos se toman
ARCHIVO = "hilos.db"  # la base de datos que se crea


def secuencia_de(n):
    """La trayectoria entera, del numero hasta el 1."""
    camino = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        camino.append(n)
    return camino


# ------------------------------------------------------- calcular los hilos

semillas = [PRIMERO + i for i in range(CUANTOS)]
hilos = {}
for indice, semilla in enumerate(semillas, 1):
    hilos[indice] = secuencia_de(semilla)

print(f"LOS {CUANTOS} HILOS  ({PRIMERO} ... {PRIMERO + CUANTOS - 1})\n")
print(f"  {'hilo':<5} {'semilla':>8} {'pasos':>6} {'pico':>18} {'impares':>8} {'razon':>7}")
print(f"  {'-'*5} {'-'*8} {'-'*6} {'-'*18} {'-'*8} {'-'*7}")
for indice, semilla in enumerate(semillas, 1):
    camino = hilos[indice]
    pasos = len(camino) - 1
    impares = sum(1 for v in camino[:-1] if v % 2 == 1)
    print(f"  {indice:<5} {semilla:>8} {pasos:>6} {max(camino):>18,} "
          f"{impares:>8} {impares / pasos:>7.4f}")


# --------------------------------------------------------- la cola comun
#
# El sufijo mas largo que comparten los ONCE. Todo cruce que caiga aqui es
# la cola de siempre y no significa nada.

cola_comun = []
i = 1
while True:
    candidatos = set()
    for camino in hilos.values():
        if i > len(camino):
            candidatos.add(None)
            break
        candidatos.add(camino[-i])
    if len(candidatos) != 1 or None in candidatos:
        break
    cola_comun.append(candidatos.pop())
    i += 1
cola_comun.reverse()
valores_cola = set(cola_comun)

print(f"\nLA COLA COMUN A LOS ONCE: {len(cola_comun)} numeros")
print(f"  {cola_comun}")
print(f"  Todo cruce que caiga aqui es ruido: lo comparten por obligacion,")
print(f"  no por parecido. Se marca aparte y no se cuenta como hallazgo.")


# --------------------------------------------- el cruce: la malla completa
#
# Cada paso de cada hilo contra cada paso de todos los demas. Se guarda el
# desfase (paso_a - paso_b), que es el numero que lleva la informacion.

cruces = []
for a in range(1, CUANTOS + 1):
    for b in range(a + 1, CUANTOS + 1):
        posiciones_b = {}
        for j, v in enumerate(hilos[b]):
            posiciones_b.setdefault(v, []).append(j)
        for i, v in enumerate(hilos[a]):
            for j in posiciones_b.get(v, []):
                cruces.append((a, i, b, j, v, i - j, 1 if v in valores_cola else 0))

fuera_de_cola = [c for c in cruces if c[6] == 0]
print(f"\nLA MALLA: {len(cruces):,} cruces en total, de los cuales")
print(f"  {len(cruces) - len(fuera_de_cola):,} son cola comun (ruido)")
print(f"  {len(fuera_de_cola):,} estan fuera de la cola (esto es lo que importa)")


# --------------------------------------------- la primera fusion de cada par

fusiones = []
for a in range(1, CUANTOS + 1):
    for b in range(a + 1, CUANTOS + 1):
        propios = [c for c in cruces if c[0] == a and c[2] == b and c[6] == 0]
        if propios:
            primero = min(propios, key=lambda c: c[1])
            fusiones.append(primero)
        else:
            # solo comparten la cola obligatoria
            propios = [c for c in cruces if c[0] == a and c[2] == b]
            fusiones.append(min(propios, key=lambda c: c[1]))

print(f"\nDONDE SE FUNDE CADA PAR  (el primer numero comun)\n")
print(f"  {'par':<17} {'se funden en':>18} {'paso A':>7} {'paso B':>7} "
      f"{'desfase':>8}  que es")
print(f"  {'-'*17} {'-'*18} {'-'*7} {'-'*7} {'-'*8}  {'-'*20}")
desfase_cero = 0
for a, i, b, j, v, d, es_cola in sorted(fusiones, key=lambda f: (f[5] != 0, f[0], f[2])):
    if d == 0:
        desfase_cero += 1
    etiqueta = "COLA (no dice nada)" if es_cola else "fusion de verdad"
    print(f"  {semillas[a-1]}+{semillas[b-1]}"[:17].ljust(17)
          + f" {v:>18,} {i:>7} {j:>7} {d:>8}  {etiqueta}")

print(f"\n  Pares con DESFASE CERO (paso k contra paso k): {desfase_cero} de {len(fusiones)}")


# ---------------------------------- COMPROBACION 1: fundido es para siempre

fallos_fusion = 0
comprobados = 0
for a, i, b, j, v, d, es_cola in fusiones:
    A, B = hilos[a], hilos[b]
    largo = min(len(A) - i, len(B) - j)
    for t in range(largo):
        comprobados += 1
        if A[i + t] != B[j + t]:
            fallos_fusion += 1

print(f"\nCOMPROBACION 1 -- una vez fundidos, ya no se separan nunca")
print(f"  pares de posiciones revisados tras la fusion: {comprobados:,}")
print(f"  fallos: {fallos_fusion}")
if fallos_fusion:
    raise SystemExit("Dos hilos se despegan despues de fundirse. Imposible. No sigas.")


# ------------- COMPROBACION 2: los primeros k pasos los fija n mod 2^k
#
# Es el vector de paridad de Terras (1976). Si dos numeros son congruentes
# modulo 2^k, sus primeros k pasos tienen la MISMA forma par/impar.

def vector_de_paridad(n, k):
    """Los primeros k pasos, como cadena de P y I."""
    patron = []
    for _ in range(k):
        patron.append("I" if n % 2 else "P")
        n = n // 2 if n % 2 == 0 else 3 * n + 1
    return "".join(patron)


fallos_terras = 0
casos_terras = 0
for k in range(1, 13):
    modulo = 2 ** k
    for semilla in semillas:
        for salto in range(1, 6):
            otro = semilla + salto * modulo
            casos_terras += 1
            if vector_de_paridad(semilla, k) != vector_de_paridad(otro, k):
                fallos_terras += 1

print(f"\nCOMPROBACION 2 -- los primeros k pasos los fija n mod 2^k (Terras 1976)")
print(f"  casos probados: {casos_terras:,} (k de 1 a 12, cinco saltos por semilla)")
print(f"  fallos: {fallos_terras}")
if fallos_terras:
    raise SystemExit("El vector de paridad no depende del resto. Imposible. No sigas.")

print(f"\n  los once vectores de paridad de los 12 primeros pasos:")
for indice, semilla in enumerate(semillas, 1):
    print(f"    {semilla}  {vector_de_paridad(semilla, 12)}  (resto mod 4096: "
          f"{semilla % 4096})")


# ------------------------------------------------ escribir la base de datos

if os.path.exists(ARCHIVO):
    os.remove(ARCHIVO)

conexion = sqlite3.connect(ARCHIVO)
cursor = conexion.cursor()

cursor.executescript("""
CREATE TABLE hilos (
    hilo       INTEGER PRIMARY KEY,
    semilla    INTEGER NOT NULL,
    pasos      INTEGER NOT NULL,
    pico       INTEGER NOT NULL,
    impares    INTEGER NOT NULL,
    pares      INTEGER NOT NULL,
    razon      REAL    NOT NULL,
    paridad12  TEXT    NOT NULL
);

CREATE TABLE pasos (
    hilo   INTEGER NOT NULL,
    k      INTEGER NOT NULL,
    valor  INTEGER NOT NULL,
    impar  INTEGER NOT NULL,
    PRIMARY KEY (hilo, k)
);

CREATE TABLE cruces (
    hilo_a  INTEGER NOT NULL,
    paso_a  INTEGER NOT NULL,
    hilo_b  INTEGER NOT NULL,
    paso_b  INTEGER NOT NULL,
    valor   INTEGER NOT NULL,
    desfase INTEGER NOT NULL,
    es_cola INTEGER NOT NULL
);

CREATE TABLE fusiones (
    hilo_a  INTEGER NOT NULL,
    paso_a  INTEGER NOT NULL,
    hilo_b  INTEGER NOT NULL,
    paso_b  INTEGER NOT NULL,
    valor   INTEGER NOT NULL,
    desfase INTEGER NOT NULL,
    es_cola INTEGER NOT NULL
);

CREATE TABLE cola_comun (
    posicion INTEGER PRIMARY KEY,
    valor    INTEGER NOT NULL
);

CREATE INDEX idx_pasos_valor  ON pasos  (valor);
CREATE INDEX idx_cruces_valor ON cruces (valor);
CREATE INDEX idx_cruces_desf  ON cruces (desfase);
""")

for indice, semilla in enumerate(semillas, 1):
    camino = hilos[indice]
    pasos = len(camino) - 1
    impares = sum(1 for v in camino[:-1] if v % 2 == 1)
    cursor.execute(
        "INSERT INTO hilos VALUES (?,?,?,?,?,?,?,?)",
        (indice, semilla, pasos, max(camino), impares, pasos - impares,
         impares / pasos, vector_de_paridad(semilla, 12)))
    cursor.executemany(
        "INSERT INTO pasos VALUES (?,?,?,?)",
        [(indice, k, v, v % 2) for k, v in enumerate(camino)])

cursor.executemany("INSERT INTO cruces VALUES (?,?,?,?,?,?,?)", cruces)
cursor.executemany("INSERT INTO fusiones VALUES (?,?,?,?,?,?,?)", fusiones)
cursor.executemany("INSERT INTO cola_comun VALUES (?,?)",
                   list(enumerate(cola_comun)))
conexion.commit()

filas_pasos = cursor.execute("SELECT COUNT(*) FROM pasos").fetchone()[0]
print(f"\nBASE DE DATOS ESCRITA: {ARCHIVO}")
print(f"  hilos {CUANTOS} · pasos {filas_pasos:,} · cruces {len(cruces):,}"
      f" · fusiones {len(fusiones)} · cola comun {len(cola_comun)}")


# ---------------------------- COMPROBACION 3: ida y vuelta contra el disco

conexion.close()
revision = sqlite3.connect(ARCHIVO)
c2 = revision.cursor()

fallos_vuelta = 0
for indice, semilla in enumerate(semillas, 1):
    leidos = [f[0] for f in c2.execute(
        "SELECT valor FROM pasos WHERE hilo=? ORDER BY k", (indice,)).fetchall()]
    if leidos != hilos[indice]:
        fallos_vuelta += 1
if c2.execute("SELECT COUNT(*) FROM cruces").fetchone()[0] != len(cruces):
    fallos_vuelta += 1

print(f"\nCOMPROBACION 3 -- ida y vuelta: los {CUANTOS} hilos releidos del disco,"
      f" {fallos_vuelta} fallos")
if fallos_vuelta:
    revision.close()
    raise SystemExit("Lo guardado no coincide con lo calculado. No sirve.")


# ------------- COMPROBACION 4: la familia publicada (32m+5, 32m+6)
#
# Wu y Huang (2001) publicaron que los pares (32m+5, 32m+6) se funden para
# todo m. Nuestro par (100005, 100006) es el caso m = 3125. Si la literatura
# tiene razon, debe cumplirse para cualquier m que probemos.

def se_funden(x, y):
    """Devuelve (valor, paso_x, paso_y) del primer numero comun, o None."""
    A, B = secuencia_de(x), secuencia_de(y)
    posiciones = {}
    for j, v in enumerate(B):
        posiciones.setdefault(v, j)
    for i, v in enumerate(A):
        if v in posiciones:
            return v, i, posiciones[v]
    return None


print(f"\nCOMPROBACION 4 -- la familia publicada (32m+5, 32m+6), Wu y Huang 2001")
print(f"  nuestro par 100005 / 100006 es el caso m = {(100005 - 5) // 32}")
fallos_familia = 0
desfases = []
for m in [0, 1, 2, 7, 100, 3125, 9999, 40000]:
    x, y = 32 * m + 5, 32 * m + 6
    r = se_funden(x, y)
    if r is None:
        fallos_familia += 1
        continue
    v, i, j = r
    desfases.append(i - j)
    marca = " <- el nuestro" if m == 3125 else ""
    print(f"    m={m:<6} {x:>8} y {y:>8} se funden en {v:>12,}"
          f"  paso {i} contra paso {j}, desfase {i - j}{marca}")
if fallos_familia:
    revision.close()
    raise SystemExit("Un par de la familia publicada no se funde. Revisa.")
print(f"  fallos: {fallos_familia}   desfases distintos: {sorted(set(desfases))}")


# ------------------------------------- lo que la base de datos ya responde

print(f"\nLO QUE LA BASE YA CONTESTA CON SQL\n")

print(f"  Cuantos cruces hay por desfase, fuera de la cola (los 8 mayores):")
for desfase, cuantos in c2.execute(
        "SELECT desfase, COUNT(*) FROM cruces WHERE es_cola=0"
        " GROUP BY desfase ORDER BY COUNT(*) DESC LIMIT 8").fetchall():
    print(f"    desfase {desfase:>5} : {cuantos:>6,} cruces")

print(f"\n  Los pasos donde MAS hilos coinciden a la vez, fuera de la cola:")
for valor, cuantos in c2.execute(
        "SELECT valor, COUNT(DISTINCT hilo) FROM pasos WHERE valor NOT IN"
        " (SELECT valor FROM cola_comun) GROUP BY valor"
        " HAVING COUNT(DISTINCT hilo) > 1 ORDER BY valor DESC LIMIT 6").fetchall():
    print(f"    el {valor:>12,} lo pisan {cuantos} hilos")

print(f"\n  Los grupos de hilos con el MISMO numero de pasos:")
for pasos, cuantos, cuales in c2.execute(
        "SELECT pasos, COUNT(*), GROUP_CONCAT(semilla) FROM hilos"
        " GROUP BY pasos ORDER BY COUNT(*) DESC").fetchall():
    print(f"    {pasos:>4} pasos : {cuantos} hilos  ({cuales})")

revision.close()

print(f"\nLa base esta en {ARCHIVO}. Se abre con sqlite3 y se consulta sin")
print(f"recalcular nada. Las tablas son: hilos, pasos, cruces, fusiones,")
print(f"cola_comun.")
