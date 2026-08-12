# revision10_adv1/presupuesto_bits.py
#
# TAREA d1 DE LA 10a REVISION (adversario 1): EL PRESUPUESTO DE BITS
# de notaensamblajep2.txt (P2-b.ii) -- "racha >= j consume j+1 bits" --
# atacado por la via del DOBLE CONTEO: construir un c0 que re-use
# bits, o argumentar por que no puede existir.
#
# RESULTADO EN CUATRO PARTES:
#   P1  EL ATAQUE FALLA (dentro de una palabra): para una palabra de
#       Terras FIJA, el mapa c0 mod 2^T -> traza de paridades es una
#       BIYECCION exacta en la cadena (k, c) de la excursion (cada
#       paso es afin con coeficiente impar y consume UN bit fresco;
#       las trazas muertas a tiempo t agrupan exactamente 2^(T-t)
#       residuos). Verificado exhaustivo. Consecuencia: los bits que
#       las rachas leen son tramos DISJUNTOS de la traza -- el doble
#       conteo dentro de una palabra es imposible.
#   P2  EL ATAQUE FALLA (entre ramas): forzar racha >= j en LAS DOS
#       ramas del mixto exige 3^k = -1 mod 2^(j+1), y 3^k mod 8 esta
#       en {1, 3}: imposible para j >= 2 (coteja_transiciones.py,
#       item 8). El forzado word-independent muere en racha <= 1.
#   P3  PERO LA FRASE DEL PRESUPUESTO ESTA SOBRE-AFIRMADA: el
#       "surplus determinista total <= ~log2|c_i|" solo vale bajo la
#       lectura "forzado con probabilidad 1 sobre las palabras". Las
#       rachas REALIZADAS mas alla del prefijo NO estan capadas por
#       log2|c0|: el cap por-racha de P2-b.i usa el |c| CORRIENTE, y
#       la magnitud se INYECTA por los 3^k (una racha a altura k
#       puede leer hasta ~k log2(3) bits que no vinieron de c0).
#       Demostrado con c0 = 5: rachas realizadas >> 1 + log2(5).
#   P4  LA MONEDA CORRECTA del presupuesto es DENSIDAD DE CLASE, no
#       magnitud: exigir un perfil de rachas de peso total W dentro
#       de una palabra = UNA clase mod 2^(>= W) (P1), o sea
#       probabilidad 2^(-W) bajo la medida de clases -- eso es lo
#       que el teorema de conteo debe cobrar; la magnitud |c0| solo
#       capa la PRIMERA lectura (P2-b.i, correcta).
#
# Capa 1: mapa = cadena (k, c) del atajo, excursion (absorcion k = 2
# bit 1 impar, la convencion del DP); T = 13 y 12 no redondos; los
# hallazgos P3 son EXISTENCIALES (un caso basta), no promedios.

import random


def pot3(k, _c={0: 1}):
    if k not in _c:
        _c[k] = 3 ** k
    return _c[k]


def paso(k, c, bit):
    # la dinamica entera exacta de la excursion (forma de paso_entero
    # de equidistribucionmixto.py, re-escrita)
    if c % 2 == 0:
        return (k, c // 2) if bit == 0 else (k, (3 * c + 1 - pot3(k)) // 2)
    if bit == 0:
        return (k + 1, (3 * c + 1) // 2)
    if k >= 3:
        return (k - 1, (c - pot3(k - 1)) // 2)
    return None


# ----------------------------------------------------------------
# P1: biyeccion por palabra -- exhaustivo sobre c0 mod 2^T
# ----------------------------------------------------------------
def traza(c0, palabra, T):
    k, c = 2, c0
    bits = []
    for i in range(T):
        bits.append(c % 2)
        r = paso(k, c, palabra[i])
        if r is None:
            return tuple(bits), i          # muerta en el paso i
        k, c = r
    return tuple(bits), None


T = 13
azar = random.Random(20260812)
palabras = [tuple(azar.getrandbits(1) for _ in range(T)) for _ in range(12)]
fallos = 0
for w in palabras:
    vivas = {}
    muertas = {}
    for c0 in range(2 ** T):
        tr, muerte = traza(c0, w, T)
        if muerte is None:
            vivas.setdefault(tr, []).append(c0)
        else:
            muertas.setdefault((tr[:muerte + 1], muerte), []).append(c0)
    for tr, lista in vivas.items():
        if len(lista) != 1:
            fallos += 1
            print("P1 FALLO: palabra %s traza viva con %d residuos"
                  % (w, len(lista)))
    for (tr, t), lista in muertas.items():
        if len(lista) != 2 ** (T - 1 - t):
            fallos += 1
            print("P1 FALLO: traza muerta en t=%d con %d residuos"
                  " (esperados %d)" % (t, len(lista), 2 ** (T - 1 - t)))
if fallos == 0:
    print("P1. biyeccion por palabra: %d palabras aleatorias, T = %d,"
          % (len(palabras), T))
    print("    los 2^%d residuos c0: cada traza viva tiene EXACTAMENTE"
          " 1 residuo" % T)
    print("    y cada traza muerta en t exactamente 2^(T-1-t). Un paso"
          " = un bit")
    print("    fresco, sin excepciones: EL DOBLE CONTEO DENTRO DE UNA"
          " PALABRA ES")
    print("    IMPOSIBLE (las rachas leen tramos disjuntos de la"
          " traza).")
else:
    raise SystemExit("P1: %d fallos" % fallos)

# control de estabilidad: la traza depende solo de c0 mod 2^T
for w in palabras[:4]:
    for c0 in (5, 999983, 1398101):
        t1, m1 = traza(c0, w, T)
        t2, m2 = traza(c0 + 2 ** T * 7919, w, T)
        if (t1, m1) != (t2, m2):
            raise SystemExit("P1b FALLO: la traza no es funcion de"
                             " c0 mod 2^T")
print("    (control: traza(c0) = traza(c0 + 7919*2^T) en los tres"
      " arranques, 4 palabras)")
print()

# ----------------------------------------------------------------
# P2: referencia (verificado en coteja_transiciones.py item 8)
# ----------------------------------------------------------------
for k in range(0, 30):
    if pow(3, k, 8) not in (1, 3):
        raise SystemExit("P2 FALLO: 3^%d mod 8 = %d" % (k, pow(3, k, 8)))
print("P2. entre ramas: 3^k mod 8 en {1,3} para k = 0..29 (re-check);")
print("    forzar racha >= 2 en AMBAS ramas del mixto pide 3^k = -1"
      " mod 8 = 7:")
print("    IMPOSIBLE. El surplus forzado word-independent muere en"
      " racha <= 1.")
print()

# ----------------------------------------------------------------
# P3: las rachas realizadas NO estan capadas por log2|c0|
# ----------------------------------------------------------------
import math

for c0 in (5, 27):
    tope = 1 + math.log2(abs(c0))
    mejor = (0, None, None)          # (racha, |c| al mixto, k)
    total_max = 0
    for _ in range(30000):
        k, c = 2, c0
        racha = None
        c_mixto = None
        k_mixto = None
        total = 0
        for t in range(400):
            k0 = k
            r = paso(k, c, azar.getrandbits(1))
            if r is None:
                break
            k, c = r
            if k == k0:
                if racha is not None:
                    racha += 1
            else:
                if racha is not None:
                    total += racha
                    if racha > mejor[0]:
                        mejor = (racha, c_mixto, k_mixto)
                racha = 0
                c_mixto = abs(c)     # |hijo| al abrir la racha
                k_mixto = k
        total_max = max(total_max, total)
    print("P3. c0 = %d (cap naif 1 + log2|c0| = %.1f): racha realizada"
          " maxima = %d" % (c0, tope, mejor[0]))
    print("    (a altura k = %s, con |c| ~ 2^%.1f al abrirla: los bits"
          " leidos NO son" % (mejor[2], math.log2(max(1, mejor[1]))))
    print("    los de c0 -- la magnitud la inyectan los 3^k);"
          " suma de rachas de una")
    print("    excursion hasta %d. La frase 'surplus determinista"
          " total <= ~log2|c_i|'" % total_max)
    print("    solo puede leerse como FORZADO CON PROB 1; como cota de"
          " lo realizado es FALSA.")
print()

# ----------------------------------------------------------------
# P3-bis: la identidad de P2-b.i ("racha_1 tras bit 0 ES
# v2((3c+1)/2)") contra la racha REALIZADA -- la recarga puede caer
# DENTRO de la primera racha y alargarla mas alla de v2(h); y el
# reverso del presupuesto: la racha FORZADA (para TODAS las
# palabras) nunca supera v2(h), porque la palabra 0...0 la corta
# exactamente en v2(h).
# ----------------------------------------------------------------
def v2_de(n):
    v = 0
    while n and n % 2 == 0:
        n //= 2
        v += 1
    return v


exceden = total1 = 0
peor_exceso = 0
for _ in range(20000):
    k, c = 2, 999983
    vh = None
    largo = None
    for t in range(400):
        k0 = k
        r = paso(k, c, azar.getrandbits(1))
        if r is None:
            break
        k, c = r
        if k != k0:
            # mixto: cierra la racha anterior y abre la nueva
            if largo is not None:
                total1 += 1
                if largo > vh:
                    exceden += 1
                    peor_exceso = max(peor_exceso, largo - vh)
            vh = v2_de(abs(c)) if c != 0 else 0
            largo = 0
        elif largo is not None:
            largo += 1
print("P3-bis. la identidad 'racha = v2(h)' de P2-b.i contra la racha")
print("    REALIZADA (todas las rachas de 20000 excursiones, c0 ="
      " 999983):")
print("    la racha supera v2(h) en %d / %d casos (%.2f%%), exceso"
      " maximo %d" % (exceden, total1, 100.0 * exceden / total1,
                      peor_exceso))
print("    -- P2-b.i solo es" )
print("    exacta para la racha FORZADA (la palabra 0...0 corta en"
      " v2(h)); como")
print("    identidad de lo realizado es FALSA (recargas dentro de la"
      " racha 1).")
print("    El cap del presupuesto vale para lo FORZADO; lo realizado"
      " es del conteo.")
print()
print("P4. veredicto d1: el ataque del doble conteo FALLA (P1 dentro de")
print("    palabra, P2 entre ramas) -- la biyeccion de Terras si lo")
print("    impide y ahora esta verificada para la cadena (k, c) de la")
print("    excursion, absorcion incluida. PERO el presupuesto tal como")
print("    esta escrito mezcla dos monedas: la MAGNITUD log2|c0| solo")
print("    capa la primera lectura (P2-b.i); el gasto correcto de las")
print("    rachas siguientes es DENSIDAD DE CLASE 2^-W (una clase mod")
print("    2^W por palabra, P1). Reescribir P2-b.ii con esa moneda; el")
print("    hueco analitico sigue siendo el mismo (el conteo).")
