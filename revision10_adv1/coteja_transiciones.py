# revision10_adv1/coteja_transiciones.py
#
# TAREA a1 DE LA 10a REVISION (adversario 1): cotejar que los teoremas
# de lecturaracha.lean (mitad_lee / lectura_bit0 / lectura_bit1 /
# lectura_recarga) corresponden a las transiciones REALES de la cadena
# (k, c) -- la funcion transicion() de rachasreales.py -- caso por
# caso, con atencion a los bordes k = 2, k = 1 y k = 0 (el fondo).
#
# Lean garantiza demostracion <-> enunciado; ESTE fichero ataca el
# hueco enunciado <-> objeto.
#
# Capa 1: mapa = la cadena (k, c) del atajo de Terras (transicion()
# extraida VERBATIM de rachasreales.py con ast, sin ejecutar el
# modulo); no hay promedios (todo es cotejo exacto de identidades);
# rangos de c simetricos y no redondos (-2001..2001); sin limites
# tomados por constantes del repo.

import ast
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def extraer_funciones(fichero, nombres):
    # extrae las funciones VERBATIM del fuente sin ejecutar el modulo
    fuente = open(os.path.join(RAIZ, fichero), encoding="utf-8").read()
    arbol = ast.parse(fuente)
    espacio = {}
    for nodo in arbol.body:
        if isinstance(nodo, ast.FunctionDef) and nodo.name in nombres:
            seg = ast.get_source_segment(fuente, nodo)
            exec(compile(seg, fichero + ":" + nodo.name, "exec"), espacio)
    faltan = [n for n in nombres if n not in espacio]
    if faltan:
        raise SystemExit("no encontre %s en %s" % (faltan, fichero))
    return espacio


esp_real = extraer_funciones("rachasreales.py", ["pot3", "transicion"])
transicion = esp_real["transicion"]
esp_dp = extraer_funciones("equidistribucionmixto.py", ["pot3", "paso_entero"])
paso_entero = esp_dp["paso_entero"]


def v2_de(n):
    if n == 0:
        return 999
    v = 0
    while n % 2 == 0:
        n //= 2
        v += 1
    return v


RANGO = range(-2001, 2002)
fallos = 0

# ---------------------------------------------------------------
# 1. MIXTO BIT 0 (c impar, cualquier k >= 0): el .lean dice 2h = 3c+1
# ---------------------------------------------------------------
n1 = 0
for k in range(0, 7):
    for c in RANGO:
        if c % 2 == 0:
            continue
        r = transicion(k, c, 0)
        if r is None:
            continue
        k2, h = r
        if not (k2 == k + 1 and 2 * h == 3 * c + 1):
            print("FALLO bit0: k=%d c=%d -> %s" % (k, c, r))
            fallos += 1
        n1 += 1
print("1. mixto bit 0: 2h = 3c+1 cotejado en %d casos (k=0..6, c impar"
      " en [-2001,2001], negativos incluidos): %s"
      % (n1, "OK" if fallos == 0 else "FALLOS"))

# ---------------------------------------------------------------
# 2. MIXTO BIT 1 con k >= 2: el .lean/prosa dicen k >= 3; la cadena
#    real aplica LA MISMA formula 2h = c - 3^(k-1) ya en k = 2
# ---------------------------------------------------------------
n2 = n2_k2 = 0
for k in range(2, 7):
    for c in RANGO:
        if c % 2 == 0:
            continue
        r = transicion(k, c, 1)
        k2, h = r
        if not (k2 == k - 1 and 2 * h == c - 3 ** (k - 1)):
            print("FALLO bit1: k=%d c=%d -> %s" % (k, c, r))
            fallos += 1
        n2 += 1
        if k == 2:
            n2_k2 += 1
print("2. mixto bit 1, k >= 2: 2h = c - 3^(k-1) cotejado en %d casos: OK"
      % n2)
print("   HALLAZGO: la identidad vale TAMBIEN en k = 2 (%d casos) --"
      % n2_k2)
print("   la prosa (.lean linea 14, notaequidistribucion 1.) dice"
      " 'k >= 3';")
print("   la cadena real (transicion) la aplica desde k = 2. El DP"
      " (paso_entero)")
print("   ABSORBE en k = 2 con bit 1 (convencion excursion k <= 1 ="
      " fondo).")

# ---------------------------------------------------------------
# 3. MIXTO BIT 1 con k = 1 (el abs): la premisa 2h = c - p con
#    p = 3^0 = 1 es FALSA cuando g = (c-1)/2 < 0; el teorema
#    lectura_bit1 la cubre solo EN VACUO. La lectura de
#    divisibilidad, en cambio, sobrevive al signo (v2(-x) = v2(x)).
# ---------------------------------------------------------------
n3 = n3_falla_premisa = n3_v2_ok = 0
for c in RANGO:
    if c % 2 == 0:
        continue
    r = transicion(1, c, 1)
    if r is None:
        continue                      # g = 0: absorcion
    k2, h = r
    n3 += 1
    if 2 * h != c - 1:
        n3_falla_premisa += 1
        if 2 * h != 1 - c:
            print("FALLO k=1: c=%d -> %s" % (c, r))
            fallos += 1
    # la lectura de divisibilidad con p = 1: 2^j | h <=> 2^(j+1) | c-1
    if (v2_de(h) if h != 0 else 999) == v2_de(c - 1) - 1 or c == 1:
        n3_v2_ok += 1
print("3. mixto bit 1, k = 1 (abs): %d casos; la premisa 2h = c-1 del"
      % n3)
print("   .lean FALLA en %d de ellos (los c < 1: h = |g| = (1-c)/2) --"
      % n3_falla_premisa)
print("   el teorema los cubre EN VACUO; la lectura v2 sobrevive por"
      " signo")
print("   (v2(h) = v2(c-1) - 1 en %d/%d). Ni el .lean ni la prosa"
      % (n3_v2_ok, n3), end="")
print(" reclaman k = 1.")

# ---------------------------------------------------------------
# 4. COMPARTIDO BIT 1 (c par, k >= 1): la recarga, 2h = 3c + 1 - 3^k
# ---------------------------------------------------------------
n4 = 0
for k in range(1, 7):
    for c in RANGO:
        if c % 2 == 1:
            continue
        k2, h = transicion(k, c, 1)
        if not (k2 == k and 2 * h == 3 * c + 1 - 3 ** k):
            print("FALLO recarga: k=%d c=%d" % (k, c))
            fallos += 1
        n4 += 1
print("4. compartido bit 1 (recarga): 2h = 3c + 1 - 3^k cotejado en"
      " %d casos: OK" % n4)

# ---------------------------------------------------------------
# 5. EL FONDO (k = 0): que formas tiene y cuales cubre el .lean
# ---------------------------------------------------------------
n5 = 0
for c in RANGO:
    if c % 2 == 1:
        k2, h = transicion(0, c, 0)
        if not (k2 == 1 and 2 * h == 3 * c + 1):
            fallos += 1
        k2, h = transicion(0, c, 1)
        if not (k2 == 1 and 2 * h == 1 - 3 * c):
            fallos += 1
        n5 += 2
print("5. fondo k = 0, c impar: bit 0 da 2h = 3c+1 (la forma de"
      " lectura_bit0);")
print("   bit 1 da 2h = 1 - 3c: OTRA clase (3c = +1 mod 2^(j+1), no"
      " -1) que")
print("   lecturaracha.lean NO cubre. Cotejados %d casos. Para P2 es"
      " irrelevante" % n5)
print("   (las excursiones terminan en la primera entrada al fondo),"
      " pero si")
print("   alguien aplicara la lectura bit 0 al fondo-bit-1 usaria la"
      " clase ERRONEA.")

# ---------------------------------------------------------------
# 6. DP (paso_entero) contra cadena real (transicion): el diff exacto
# ---------------------------------------------------------------
difs = {}
for k in range(0, 7):
    for c in range(-999, 1000):
        for b in (0, 1):
            try:
                ra = transicion(k, c, b)
            except Exception:
                ra = "EXC"
            try:
                rb = paso_entero(k, c, b)
            except Exception:
                rb = "EXC"
            if ra != rb:
                clave = (k, c % 2, b)
                difs[clave] = difs.get(clave, 0) + 1
print("6. paso_entero (DP) vs transicion (real): celdas (k, paridad,"
      " bit) con")
print("   discrepancia: %s" % sorted(difs))
print("   -- la unica clase de diferencia debe ser k <= 2 impar bit 1"
      " (absorcion")
print("   del DP donde la cadena sigue a k-1) y los estados k <= 1 que"
      " el DP")
print("   nunca visita. Si aparece otra celda, es sangre.")
esperadas = all(k <= 2 and par == 1 and b == 1 or k <= 1
                for (k, par, b) in difs)
if not esperadas:
    fallos += 1
    print("   FALLO: hay discrepancias fuera del borde declarado")

# ---------------------------------------------------------------
# 7. Las instancias del .lean, contra la cadena real
# ---------------------------------------------------------------
ok7 = (transicion(2, 1398101, 0) == (3, 2097152)
       and 3 * 1398101 + 1 == 2 ** 22
       and transicion(2, 5, 0) == (3, 8)
       and transicion(3, 11, 1) == (2, 1)
       and transicion(2, 8, 1) == (2, 8))
print("7. instancias del .lean (caso_adversarial, caso_chico,"
      " caso_bit1,")
print("   caso_recarga) contra transicion(): %s"
      % ("OK las 4" if ok7 else "FALLO"))
if not ok7:
    fallos += 1

# ---------------------------------------------------------------
# 8. LA OBSTRUCCION MOD 8 (regalo para d1): forzar racha >= j en LOS
#    DOS bits del mixto a la vez exige 3^k = -1 mod 2^(j+1); como
#    3^k mod 8 pertenece a {1, 3}, es IMPOSIBLE para j >= 2.
# ---------------------------------------------------------------
for k in range(0, 25):
    if pow(3, k, 8) not in (1, 3):
        fallos += 1
        print("FALLO: 3^%d mod 8 = %d" % (k, pow(3, k, 8)))
cuenta = {}
for j in range(1, 9):
    m = 2 ** (j + 1)
    for k in range(3, 10):
        sol = 0
        for c in range(m):
            if (3 * c + 1) % m == 0 and (c - 3 ** (k - 1)) % m == 0:
                sol += 1
        cuenta[(j, k)] = sol
maximo_j = max(j for (j, k), s in cuenta.items() if s > 0)
print("8. obstruccion mod 8: clases c que fuerzan racha >= j en AMBOS"
      " bits:")
print("   existen solo hasta j = %d (j >= 2: cero soluciones, k ="
      " 3..9," % maximo_j)
print("   verificado exhaustivo). El forzado word-independent esta"
      " capado en")
print("   racha <= 1: nadie puede re-usar bits ENTRE ramas del primer"
      " mixto.")

print()
if fallos == 0:
    print("VEREDICTO a1: 0 fallos de identidad. Los teoremas del .lean")
    print("corresponden a las transiciones reales donde la prosa los")
    print("reclama (bit 0 todo k; bit 1 k >= 2 -- la prosa dice k >= 3,")
    print("ver hallazgo 2); k = 1 (abs) cubierto solo en vacuo y el")
    print("fondo bit 1 NO cubierto (clase opuesta) -- ninguno reclamado.")
else:
    raise SystemExit("VEREDICTO a1: %d FALLOS -- sangre" % fallos)
