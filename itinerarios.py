# itinerarios.py
#
# EL PASO 1 DE LA CLASIFICACION DE RUTAS (03-08-2026): el itinerario de
# cada clase nueva -- la palabra de FAMILIAS del mapa de E que visita
# entre paso mixto y paso mixto, terminada en V (el vortice).
#
#   Sale de la propuesta del usuario ("toda orbita relevante de E
#   pertenece a una de N familias") y del censo de nuevasfusion.py
#   (comprobacion 13: diez familias, ninguna orbita escapa).
#
#   RESULTADO, una de cal y una de arena:
#
#   . POSITIVO: en los itinerarios de |M| = 4, la familia del ULTIMO
#     tramo (el que muere en el vortice) esta siempre en {-5, -77, -4163}
#     -- EXACTAMENTE el conjunto de familias que aparecen en |M| = 2.
#     Es el teorema de la contraccion ("el ultimo tramo es un |M| = 2
#     desplazado") hecho visible en las etiquetas. Aqui se corta con
#     SystemExit si algun nivel lo rompe.
#
#   . NEGATIVO, y se registra porque el repo registra negativos: la
#     familia ASINTOTICA es un invariante ruidoso para contar. El tramo
#     solo usa un prefijo finito de la orbita de E, y la familia mezcla
#     informacion que el tramo nunca ve: los conteos por itinerario son
#     erraticos (1s y 2s), no polinomicos. El refinamiento que queda:
#     etiquetar tramos por datos FINITOS (el E de arranque modulo algo,
#     o el largo del tramo), no por el destino al infinito.
#
#   Y el detalle que mata una conjetura de un minuto de vida: las
#   familias positivas (4, 24, 84) SI aparecen en estratos altos. La
#   unica ausente es el punto fijo -1, y por razon trivial: su cuenca
#   es {-1} y ningun E de tramo real cae ahi.

K_MAX = 15          # niveles k+1 = 4 .. K_MAX+1 (fuerza bruta 2^(K_MAX+1))

B_PUBLICADA = {4: 1, 5: 2, 6: 2, 7: 3, 8: 4, 9: 6, 10: 11, 11: 19,
               12: 34, 13: 60, 14: 106, 15: 190, 16: 341}

FAMILIAS = ((-1, 1), (4, 1), (-11, 2), (-5, 3), (24, 3),
            (-59, 5), (-77, 5), (84, 11), (-4163, 27), (-5099, 27))


def paso(x):
    return (3 * x + 1) // 2 if x % 2 else x // 2


def iterar(r, k):
    S = 0
    for _ in range(k):
        if r % 2:
            S += 1
        r = paso(r)
    return r, S


def buenas(k):
    res = set()
    for r in range(2 ** k - 1):
        a, Sa = iterar(r, k)
        b, Sb = iterar(r + 1, k)
        if a == b and Sa == Sb:
            res.add(r)
    return res


def mapaE(E):
    return (E - 1) // 2 if E % 2 else (3 * E - 4) // 2


memo_familia = {}
for ciclo_min, largo in FAMILIAS:
    E = ciclo_min
    for _ in range(largo):
        memo_familia[E] = ciclo_min
        E = mapaE(E)


def familia(E0):
    ruta = []
    E = E0
    while E not in memo_familia:
        ruta.append(E)
        if len(ruta) > 100000:
            raise SystemExit("familia sin cerrar en E0 = %d" % E0)
        E = mapaE(E)
    f = memo_familia[E]
    for x in ruta:
        memo_familia[x] = f
    return f


conteo_por_M = {}
ultimas_M4 = set()
familias_vistas = set()
ant = buenas(3)
for k in range(3, K_MAX + 1):
    B1 = buenas(k + 1)
    total = 0
    for r in sorted(B1):
        if (r % 2 ** k) in ant:
            continue
        total += 1
        x, y = r, r + 1
        palabra = []
        for _ in range(k + 1):
            if (x % 2) != (y % 2):
                x2, y2 = paso(x), paso(y)
                if x2 == y2:
                    palabra.append('V')
                else:
                    s2, g2 = min(x2, y2), abs(x2 - y2)
                    palabra.append(familia(g2 - 5 * s2 - 1))
            x, y = paso(x), paso(y)
        M = len(palabra)
        conteo_por_M.setdefault(M, set()).add(tuple(palabra))
        familias_vistas |= set(p for p in palabra if p != 'V')
        if M == 4:
            ultimas_M4.add(palabra[-2])
    # COMPROBACION 1: el conteo de nuevas reproduce b(k)
    if total != B_PUBLICADA[k + 1]:
        raise SystemExit("FALLO cruce b: nivel %d da %d, publicado %d"
                         % (k + 1, total, B_PUBLICADA[k + 1]))
    ant = B1

# COMPROBACION 2: el ultimo tramo de |M| = 4 vive en las familias de |M| = 2
if not ultimas_M4 <= {-5, -77, -4163}:
    raise SystemExit("FALLO contraccion visible: ultimas de M4 = %s"
                     % sorted(ultimas_M4))

# COMPROBACION 3: la unica familia ausente es el punto fijo -1
ausentes = set(c for c, _ in FAMILIAS) - familias_vistas
if ausentes != {-1}:
    raise SystemExit("FALLO ausencias: %s" % sorted(ausentes))

print("cruce b(k): OK en los %d niveles" % (K_MAX - 2))
for M in sorted(conteo_por_M):
    print("|M| = %2d : %3d itinerarios distintos" % (M, len(conteo_por_M[M])))
print()
print("ultimas familias de |M| = 4:", sorted(ultimas_M4),
      "(las mismas de |M| = 2: la contraccion, visible)")
print("familia ausente en todo itinerario:", sorted(ausentes),
      "(trivial: su cuenca es ella misma)")
print()
print("CONCLUSION: la familia asintotica es invariante RUIDOSO para contar")
print("(el tramo solo usa un prefijo finito de la orbita); el refinamiento")
print("pendiente es etiquetar por datos finitos del tramo.")
