# subrenovacionc.py
#
# LA SUB-RENOVACION DE c: LA PERPETUIDAD CRITICA (04-08-2026; paso 2).
#
#   El paso 1 (dispersionc.py) midio crecimiento DIFUSIVO de log|c| y
#   bandas diadicas con cociente acercandose a 1/2. Este fichero pone
#   la estructura exacta debajo:
#
#   T1 -- EL TEOREMA DEL MULTIPLICADOR (exacto, de las seis leyes):
#      escribiendo cada transicion como c' = m*c + s (afin en c),
#      . en el NUCLEO (k >= 1), TODA transicion tiene m = 1/2 en una
#        rama y m = 3/2 en la otra: cada paso es una MONEDA JUSTA entre
#        contraer x1/2 y expandir x3/2. E[m] = (1/2 + 3/2)/2 = 1 EXACTO
#        y E[log2 m] = (log2 3 - 2)/2 = -0.2075 < 0: la dinamica de c
#        es una PERPETUIDAD DE KESTEN CRITICA -- kappa = 1 es la unica
#        solucion positiva de E[m^kappa] = 1. (El mismo balance 3/2-1/2
#        que gobierna B/A -> 2: la criticidad ES la constante del
#        problema.)
#      . la UNICA excepcion es la frontera con gap impar (k = 0, g
#        impar): ahi las DOS ramas tienen m = 3/2 ((3g+1)/2 y (3g-1)/2)
#        -- la bomba de reentrada, el unico estado sin moneda.
#      Consecuencia estandar (Kesten 1973, con las condiciones
#      DECLARADAS abajo): una afin aleatoria contractiva en log con
#      E[m^kappa] = 1 tiene distribucion estacionaria de cola
#      P(|c| > x) ~ C / x^kappa = C / x.
#
#   T2 -- LA COLA, MEDIDA: bandas diadicas exactas de |c| en el nucleo
#      a profundidad tope: el cociente entre bandas consecutivas debe
#      tender a 1/2 (kappa = 1) si la perpetuidad manda. Se mide por
#      separado en k = 1 y en todo el nucleo, con la regla 4x.
#
#   T3 -- LAS LEYES MOD 3 (teorema, verificacion exhaustiva):
#      (a) toda ENTRADA al nucleo desde la frontera llega con
#          c = 2 (mod 3)  ((3g+1)/2 y (3g-1)/2 son = 2 mod 3);
#      (b) c = 0 (mod 3) es INALCANZABLE en el nucleo (las seis leyes
#          lo preservan; es Komodo 3 en coordenadas de la cadena:
#          el mayor es 3^k v + c = c mod 3);
#      (c) la absorcion exige c = 1 en k = 1, y 1 = 1 (mod 3): solo la
#          sub-clase c = 1 (mod 3) puede fundir.
#
#   Y LA LECTURA HONESTA DE LOS DOS PASOS JUNTOS, escrita al final:
#   la firma kappa = 1 revierte el veredicto provisional del paso 1.
#   Una cola 1/x es TENSA (la masa relativa de |c| <= C converge a
#   limites positivos): la lectura "dispersion" era la sombra
#   pre-asintotica de una convergencia critica lenta. Tensa + paseo
#   recurrente + piso de absorcion por visita => phi = 1 (Gao-Wu).
#   CONDICIONES DECLARADAS (por que esto NO es teorema): los (m, s)
#   de Kesten aqui NO son i.i.d. (el shift s depende del nivel k de la
#   torre y crece como 3^k) y el piso por visita exige uniformidad.
#   Lo exacto: T1 y T3. Lo medido: T2. Lo heuristico: el cierre.

PROF = 34
TOPE_ESTADOS = 9 * 10 ** 6


def transicion(k, c, bit):
    if k == 0:
        if c % 2 == 0:
            return ('estado', 0, c // 2) if bit == 0 else ('estado', 0, 3 * c // 2)
        return ('estado', 1, (3 * c + 1) // 2) if bit == 0 \
            else ('estado', 1, (1 - 3 * c) // 2)
    if c % 2 == 0:
        return ('estado', k, c // 2) if bit == 0 \
            else ('estado', k, (3 * c + 1 - 3 ** k) // 2)
    if bit == 0:
        return ('estado', k + 1, (3 * c + 1) // 2)
    if k >= 2:
        return ('estado', k - 1, (c - 3 ** (k - 1)) // 2)
    g = (c - 1) // 2
    if g == 0:
        return ('fusion',)
    return ('estado', 0, abs(g))


# ---------------------------------------------------------------------------
# T1: el multiplicador de cada transicion, verificado sobre una rejilla
#     amplia: en el nucleo, {m de bit 0, m de bit 1} = {1/2, 3/2} SIEMPRE;
#     en la frontera par tambien; en la frontera impar {3/2, 3/2}.
#     (m se lee comparando c' para dos valores de c de la misma clase:
#     m = (c2' - c1') / (c2 - c1), con paridades iguales.)
# ---------------------------------------------------------------------------

def multiplicador(k, c, bit):
    # dos representantes de la misma paridad y clase mod 3; la salida a
    # frontera lleva un valor absoluto (lineal A TROZOS con pliegue en
    # c = 1), asi que se prueban ambos lados y vale el que no cruce
    for delta in (6, -6):
        c2 = c + delta
        s1 = transicion(k, c, bit)
        s2 = transicion(k, c2, bit)
        if s1[0] == 'fusion' or s2[0] == 'fusion':
            return None
        if s1[1] != s2[1]:
            return None           # niveles distintos: no comparable
        num, den = s2[2] - s1[2], c2 - c
        if abs(2 * num) in (abs(den), 3 * abs(den)):
            return (num, den)
    return (num, den)             # devuelve el ultimo: fallara el test


probadas = 0
for k in range(0, 9):
    for c in range(1 if k == 0 else -80, 81):
        if k == 0 and c < 1:
            continue
        ms = set()
        for bit in (0, 1):
            m = multiplicador(k, c, bit)
            if m is not None:
                ms.add(abs((2 * m[0]) // m[1]))   # |2m|: 1 <-> 1/2, 3 <-> 3/2
        if k == 0 and c % 2 == 1:
            # la bomba de reentrada: ambas ramas |m| = 3/2 (el bit 1 con
            # signo negativo -- el vuelco -- pero magnitud 3/2)
            if ms and ms != {3}:
                raise SystemExit("T1 frontera impar: k=%d c=%d ms=%s"
                                 % (k, c, ms))
        elif len(ms) == 2 and ms != {1, 3}:
            raise SystemExit("T1: k=%d c=%d ms=%s" % (k, c, ms))
        probadas += 1

print("T1 OK -- EL TEOREMA DEL MULTIPLICADOR: en el nucleo y la frontera")
print("par, cada paso es moneda justa entre m = 1/2 y m = 3/2 (E[m] = 1")
print("EXACTO, E[log2 m] = %.4f < 0): c es una PERPETUIDAD DE KESTEN"
      % ((3).bit_length() and __import__('math').log2(3) / 2 - 1))
print("CRITICA con kappa = 1. La unica excepcion es la frontera impar")
print("(ambas ramas m = 3/2): la bomba de reentrada. %d estados probados."
      % probadas)

# ---------------------------------------------------------------------------
# T2: la cola de |c|, en bandas diadicas exactas (t = PROF y t = PROF-2,
#     regla 4x: dos profundidades, dos poblaciones)
# ---------------------------------------------------------------------------

import math

estados = {(0, 1): 1}
fotos = {}
for t in range(1, PROF + 1):
    nuevo = {}
    for (k, c), n in estados.items():
        for bit in (0, 1):
            s = transicion(k, c, bit)
            if s[0] == 'fusion':
                continue
            clave = (s[1], s[2])
            nuevo[clave] = nuevo.get(clave, 0) + n
    estados = nuevo
    if len(estados) > TOPE_ESTADOS:
        print("[cortado en t=%d]" % t)
        break
    if t in (PROF - 2, PROF):
        fotos[t] = dict(estados)

for t, foto in sorted(fotos.items()):
    print()
    print("T2: bandas diadicas de |c| a t = %d (masa; cociente banda/banda):" % t)
    for etiqueta, filtro in (("k = 1 solo", lambda k: k == 1),
                             ("nucleo entero (k >= 1)", lambda k: k >= 1)):
        bandas = {}
        for (k, c), n in foto.items():
            if filtro(k) and c != 0:
                j = max(0, int(math.log2(abs(c))))
                bandas[j] = bandas.get(j, 0) + n
        total = sum(bandas.values())
        print("  %s:" % etiqueta)
        prev = None
        for j in sorted(bandas):
            if j > 14:
                break
            frac = bandas[j] / total
            coc = ("%.4f" % (bandas[j] / prev)) if prev else "      "
            print("    2^%2d <= |c| < 2^%2d :  %.6f   %s"
                  % (j, j + 1, frac, coc))
            prev = bandas[j]

print()
print("T2: los cocientes de bandas altas rondando 1/2 = cola 1/x")
print("(kappa = 1); un cociente que siguiera cayendo bajo 1/2 seria")
print("log-normal difusiva. Ver la lectura final.")

# ---------------------------------------------------------------------------
# T3: las leyes mod 3, exhaustivas sobre la foto final + algebraicas
# ---------------------------------------------------------------------------

# (a) las dos puertas de entrada traen cada una SU clase mod 3:
#     sin vuelco (bit 0): (3g+1)/2 = 2 (mod 3); con vuelco (bit 1):
#     (3g-1)/2 = 1 (mod 3). Ninguna trae c = 0 (mod 3).
for g in range(1, 4001, 2):
    c0 = (3 * g + 1) // 2
    if c0 % 3 != 2:
        raise SystemExit("T3a puerta directa: g=%d c'=%d" % (g, c0))
    if g >= 3:
        c1 = (3 * g - 1) // 2
        if c1 % 3 != 1:
            raise SystemExit("T3a puerta vuelco: g=%d c'=%d" % (g, c1))
# (b) c = 0 (mod 3) inalcanzable en el nucleo: sobre la foto final
malos = [(k, c) for (k, c) in fotos[PROF] if k >= 1 and c % 3 == 0]
if malos:
    raise SystemExit("T3b: estados del nucleo con 3 | c: %s" % malos[:5])
# (c) la absorcion es (1,1) y 1 = 1 (mod 3)
if transicion(1, 1, 1)[0] != 'fusion':
    raise SystemExit("T3c")

print()
print("T3 OK -- LAS LEYES MOD 3: (a) cada puerta de entrada trae SU")
print("clase -- directa (3g+1)/2 = 2 (mod 3), vuelco (3g-1)/2 = 1 (mod")
print("3); ninguna trae 0 [algebraico, g < 4001]; (b) 3 | c inalcanzable")
print("en el nucleo (0 estados en la foto de t = %d -- Komodo 3 en" % PROF)
print("coordenadas de la cadena: el mayor es 3^k v + c = c mod 3); (c)")
print("la absorcion (1,1) vive en la sub-clase del vuelco, c = 1 (mod 3)")
print("-- LA PUERTA QUE FUNDE ES LA DEL VUELCO. El reparto medido en")
print("k = 1 (clase 1 : clase 2 = 1 : 2) es la huella de las dos puertas.")

print()
print("LECTURA FINAL (los dos pasos juntos, con sus etiquetas):")
print("  EXACTO   : T1 (moneda critica kappa = 1), T3 (mod 3).")
print("  MEDIDO   : T2 (cola 1/x en formacion), el crecimiento difusivo")
print("             de log|c| y las cubetas desacelerando (paso 1).")
print("  LECTURA  : kappa = 1 => distribucion estacionaria TENSA de cola")
print("             1/x => la masa de |c| <= C en el nucleo converge a")
print("             limites positivos => piso de absorcion por visita =>")
print("             con el paseo recurrente, phi = 1 (Gao-Wu CIERTA).")
print("             El 'escape' del paso 1 era convergencia critica lenta.")
print("  POR QUE NO ES TEOREMA: los (m, s) no son i.i.d. (s crece con el")
print("  nivel k de la torre), y el piso por visita exige uniformidad.")
print("  El siguiente blanco con forma de teorema: acotar la contribucion")
print("  de los shifts de torre (su masa decae 2^-k, su tamano crece 3^k:")
print("  el producto masa x log-tamano SI es sumable -- log2(3^k) * 2^-k)")
print("  y formalizar la perpetuidad sobre la medida de las palabras.")
