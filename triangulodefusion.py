# triangulodefusion.py
#
# EL EXPERIMENTO DE PASCAL PARA b(k) (11-08-2026; el punto (ii) del
# puente de fichawinklerzarubin.txt: "si el conteo estratificado
# satisface una recursion de Pascal con dos entradas, todo el aparato
# Winkler/Zarubin se copia -- es el experimento que yo haria primero").
#
#   EL GEMELO RESUELTO. Para el tiempo de parada de coeficiente, el
#   triangulo R(k, n) de Winkler (posicion final k, orden n) cumple
#   R(k, n) = R(k-1, n) + R(k-1, n-1); las columnas suman A100982 y
#   las filas A076227. El deficit del doblado esta concentrado en los
#   niveles A020914 (Zarubin 2019).
#
#   NUESTRO LADO. b(t) = clases nuevas del nivel t+1 = palabras de
#   largo t desde (0,1) que ABSORBEN en el paso t (el vortice
#   (1,1)-bit1) sin haber absorbido antes (PALOMAS: b(t) = N_t(1,1)).
#   El analogo de la "posicion" de Winkler: estratificar la absorcion
#   por S = numero de bits 1 de la palabra (los pasos impares del
#   ancla). Este fichero construye la tabla
#
#       F(t, S) = numero de palabras de largo t que absorben en el
#                 paso t con exactamente S unos
#
#   y las tablas vivas L(t, S) (masa viva por unos) y pregunta:
#     C1  el cruce duro: Sigma_S F(t, S) reproduce b(t-1) publicada.
#     C2  el soporte: en el gemelo, cada orden vive en UN largo
#         (A020914); aqui, cuantos S soporta cada t? (concentracion)
#     C3  EL TEST DE PASCAL: existe una recursion de dos terminos
#         F(t, S) = a*F(t-1, S) + b*F(t-1, S-1) (o con L de por
#         medio)? Se mide el residuo de las cuatro formas candidatas.
#     C4  la diagonal dominante: S/t de la masa absorbida contra
#         log_2(3)/(1+log_2(3)) = 0,613 (la pendiente de Terras) y
#         contra la diagonal del gemelo.
#
#   ETIQUETA HONESTA: esto es un EXPERIMENTO de estructura (medicion
#   exacta de enteros, sin azar). Un "no cumple Pascal" con estas
#   coordenadas no cierra la via: puede pedir otra coordenada de
#   posicion (v2(Delta) de Tortolas es la siguiente candidata).
#
#   Mapa del ATAJO via la cadena simbolica; enteros exactos;
#   SystemExit antes de concluir.

PROF_MAX = 22          # niveles del barrido (los estados crecen ~2x/nivel)
TOPE_ESTADOS = 4 * 10 ** 6

# b(k) publicada, k = 3..31 (sucesiones.txt)
B_PUBLICADA = {3: 1, 4: 2, 5: 2, 6: 3, 7: 4, 8: 6, 9: 11, 10: 19, 11: 34,
               12: 60, 13: 106, 14: 190, 15: 341, 16: 623, 17: 1148,
               18: 2124, 19: 3963, 20: 7451, 21: 14072}


def transicion(k, c, bit):
    # la cadena REAL (con fusion; identica a paseodeladeuda.py)
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
# EL BARRIDO CON S: estados (k, c, S) -> numero de palabras.
#   S = unos acumulados. La absorcion en el paso t con S unos suma el
#   bit de la fusion (que es un 1): se registra con S_final = S + 1.
# ---------------------------------------------------------------------------

estados = {(0, 1, 0): 1}
F = {}          # F[(t, S)] = absorbidas en el paso t con S unos (bit final incluido)
L = {}          # L[(t, S)] = masa viva tras el paso t con S unos
for t in range(1, PROF_MAX + 1):
    nuevo = {}
    for (k, c, S), n in estados.items():
        for bit in (0, 1):
            r = transicion(k, c, bit)
            if r[0] == 'fusion':
                F[(t, S + 1)] = F.get((t, S + 1), 0) + n
            else:
                clave = (r[1], r[2], S + bit)
                nuevo[clave] = nuevo.get(clave, 0) + n
    estados = nuevo
    for (k, c, S), n in estados.items():
        L[(t, S)] = L.get((t, S), 0) + n
    if len(estados) > TOPE_ESTADOS:
        print("[cortado en t=%d: %d estados]" % (t, len(estados)))
        PROF_MAX = t
        break

# ---------------------------------------------------------------------------
# COMPROBACION 1: el cruce duro contra b publicada.
#   a(k) = absorbidas en <= k pasos y b(k) = a(k+1) - 2a(k), asi que las
#   absorciones FRESCAS del paso t son b(t-1) (indexacion verificada
#   contra paseodeladeuda.py C3; el primer intento de este fichero
#   comparaba contra b(t) y el SystemExit lo cazo -- la indexacion
#   paso/estado, la misma leccion que Perras R2).
# ---------------------------------------------------------------------------

for t in range(4, PROF_MAX + 1):
    if t - 1 in B_PUBLICADA:
        total = sum(n for (tt, S), n in F.items() if tt == t)
        if total != B_PUBLICADA[t - 1]:
            raise SystemExit("C1: Sigma_S F(%d,S) = %d, b(%d) publicada = %d"
                             % (t, total, t - 1, B_PUBLICADA[t - 1]))
print("COMPROBACION 1 OK: Sigma_S F(t, S) reproduce b(t-1) publicada,")
print("t = 4..%d. La tabla es la estratificacion de las nuevas por S." % PROF_MAX)

# ---------------------------------------------------------------------------
# COMPROBACION 2: el soporte en S de cada nivel.
# ---------------------------------------------------------------------------

print()
print("la tabla F(t, S) (absorbidas en t con S unos; Sigma = b(t-1)):")
print("   t  b(t-1)  soporte S (S: F)")
for t in range(3, PROF_MAX + 1):
    fila = sorted((S, n) for (tt, S), n in F.items() if tt == t)
    if not fila:
        continue
    total = sum(n for _, n in fila)
    print("  %2d  %6d   %s" % (t, total,
          "  ".join("%d:%d" % (S, n) for S, n in fila)))

# ---------------------------------------------------------------------------
# COMPROBACION 3: EL TEST DE PASCAL sobre F.
#   Cuatro candidatas de dos terminos (las traducciones naturales del
#   R(k,n) = R(k-1,n) + R(k-1,n-1) del gemelo):
#     (a) F(t,S) = F(t-1,S)   + F(t-1,S-1)
#     (b) F(t,S) = F(t-2,S-1) + F(t-2,S-2)   [el paso doble: los
#         estratos entran cada dos niveles]
#     (c) F(t,S) = 2*F(t-1,S-1) - (deficit)  [el molde Zarubin: se
#         imprime el deficit por si esta concentrado]
#     (d) F(t,S) = F(t-1,S-1) + F(t-2,S-2)   [escalera mixta]
#   Se mide, para cada candidata, la fraccion de celdas (t >= 8) que
#   la cumplen EXACTA.
# ---------------------------------------------------------------------------


def f(t, S):
    return F.get((t, S), 0)


celdas = [(t, S) for (t, S) in F if t >= 8]
formas = [
    ('a: F(t-1,S)+F(t-1,S-1)', lambda t, S: f(t-1, S) + f(t-1, S-1)),
    ('b: F(t-2,S-1)+F(t-2,S-2)', lambda t, S: f(t-2, S-1) + f(t-2, S-2)),
    ('d: F(t-1,S-1)+F(t-2,S-2)', lambda t, S: f(t-1, S-1) + f(t-2, S-2)),
]
print()
print("COMPROBACION 3 - el test de Pascal (celdas con t >= 8: %d):" % len(celdas))
for nombre, regla in formas:
    exactas = sum(1 for (t, S) in celdas if f(t, S) == regla(t, S))
    print("  %-26s exactas %4d de %d" % (nombre, exactas, len(celdas)))

print()
print("y el molde Zarubin (deficit del doblado sobre la diagonal S-1):")
print("   t   S    F(t,S)  2*F(t-1,S-1)   deficit")
for (t, S) in sorted(celdas):
    d = 2 * f(t - 1, S - 1) - f(t, S)
    if f(t, S) > 0 or d != 0:
        print("  %2d  %2d  %7d  %10d  %8d" % (t, S, f(t, S),
                                              2 * f(t - 1, S - 1), d))

# ---------------------------------------------------------------------------
# COMPROBACION 4: la diagonal dominante S/t contra la pendiente de
#   Terras log2(3)/(1+log2(3)) = 0,6131.
# ---------------------------------------------------------------------------

import math
print()
print("COMPROBACION 4 - la diagonal: S medio / t de las absorbidas")
objetivo = math.log(3, 2) / (1 + math.log(3, 2))
for t in range(6, PROF_MAX + 1):
    fila = [(S, n) for (tt, S), n in F.items() if tt == t]
    tot = sum(n for _, n in fila)
    if tot == 0:
        continue
    smedio = sum(S * n for S, n in fila) / tot
    print("  t=%2d  S/t = %.4f   (objetivo Terras %.4f)"
          % (t, smedio / t, objetivo))
print()
print("Lectura: si F concentra el soporte y una de las formas de dos")
print("terminos sale EXACTA (o el deficit Zarubin sale concentrado en")
print("pocas celdas por nivel), el aparato del gemelo se copia. Si no,")
print("la siguiente coordenada candidata es v2(Delta) de Tortolas.")
