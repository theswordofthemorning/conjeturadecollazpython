# retorno11.py
#
# EL CRITERIO DE RETORNO, AFILADO DEL TODO (09-08-2026; el "segundo
# momento" del empalme resulto innecesario):
#
#   TEOREMA (el criterio final). En la cadena MODIFICADA:
#     phi = 1  <=>  p = P_(1,1)(retornar a (1,1)) = 1
#              <=>  Sigma_t P(X_t = (1,1)) = infinito.
#   Demostracion: (i) phi = 1 <=> N = visitas a (1,1) es infinito c.s.
#   (cada visita de la cadena real sobrevive con moneda 1/2, y
#   P(no fundir) = E[2^-N]); (ii) para una cadena de Markov numerable,
#   P_y(volver a y i.o.) es 0 o 1 segun p < 1 o p = 1 (dicotomia
#   clasica, geometrica en el numero de retornos), y
#   E_y[N] = 1/(1-p) = Sigma_t P_y(X_t = y); (iii) (0,1) y (1,1) SE
#   COMUNICAN -- ida: (0,1)-0->(1,2)-0->(1,1); vuelta:
#   (1,1)->(2,2)-1->(2,-1)-1->(1,-2)-0->(1,-1)-1->(0,1) -- luego la
#   recurrencia es de la clase entera y p = 1 tambien da
#   P_(0,1)(hit (1,1)) = 1. QED.
#   (La comprobacion 0 verifica los dos caminos con la funcion real.)
#
#   EL INSTRUMENTO: los PRIMEROS RETORNOS a (0,1) (el estado
#   consecutivo, misma clase), por barrido simbolico con absorcion en
#   el retorno:
#     f(L) = masa de palabras de largo L que vuelven a (0,1) por
#            primera vez en L  =>  P_L = Sigma_{j<=L} f(j),
#     S(L) = 1 - P_L  (la masa que aun no volvio).
#   Recurrencia <=> S(L) -> 0. La firma del caso critico-justo (paseo
#   simetrico) es S(L) ~ c / sqrt(L); transitoria seria S(L) -> s > 0.
#   Ademas el mismo barrido desde (2,2) mide p directamente (retorno
#   a (1,1) tras el rebote del vortice).
#
#   Cruce con OVEJAS: los conteos f(L)*2^L del retorno a gap 1 son la
#   serie de primeros retornos que LaTourette 2007 tabulo (con su
#   errata) y retornoslambda.py extendio; se imprimen para comparar.
#
#   Mapa del ATAJO, enteros exactos, SystemExit antes de concluir.

import math

PROF = 36
TOPE_ESTADOS = 9 * 10 ** 6


def transicion_mod(k, c, bit):
    if k == 0:
        if c % 2 == 0:
            return (0, c // 2) if bit == 0 else (0, 3 * c // 2)
        return (1, (3 * c + 1) // 2) if bit == 0 else (1, (1 - 3 * c) // 2)
    if c % 2 == 0:
        return (k, c // 2) if bit == 0 else (k, (3 * c + 1 - 3 ** k) // 2)
    if k == 1 and c == 1:
        return (2, 2)
    if bit == 0:
        return (k + 1, (3 * c + 1) // 2)
    if k >= 2:
        return (k - 1, (c - 3 ** (k - 1)) // 2)
    return (0, abs((c - 1) // 2))


# ---------------------------------------------------------------------------
# COMPROBACION 0: LA COMUNICACION (0,1) <-> (1,1), con la funcion real.
# ---------------------------------------------------------------------------

e = (0, 1)
for bit in (0, 0):
    e = transicion_mod(e[0], e[1], bit)
if e != (1, 1):
    raise SystemExit("C0 ida: %s" % (e,))
e = (1, 1)
for bit in (0, 1, 1, 0, 1):       # el rebote es forzado; luego 1,1,0,1
    e = transicion_mod(e[0], e[1], bit)
if e != (0, 1):
    raise SystemExit("C0 vuelta: %s" % (e,))
print("COMPROBACION 0 OK: (0,1) -00-> (1,1) y (1,1) -rebote,1,1,0,1-> (0,1).")
print("Los dos estados se comunican: la recurrencia es de la clase entera")
print("y el criterio queda: phi = 1 <=> p = 1 <=> Sigma P(X_t=(1,1)) = inf.")


def barrido_retorno(inicio, objetivo, prof_max):
    # devuelve (lista f(L) como fracciones float, estados vivos al final)
    estados = {inicio: 1}
    fs = []
    for L in range(1, prof_max + 1):
        nuevo = {}
        vueltos = 0
        for (k, c), n in estados.items():
            for bit in (0, 1):
                s = transicion_mod(k, c, bit)
                if s == objetivo:
                    vueltos += n
                else:
                    nuevo[s] = nuevo.get(s, 0) + n
        fs.append(vueltos / 2.0 ** L)
        estados = nuevo
        if len(estados) > TOPE_ESTADOS:
            print("   [cortado en L = %d por tope de estados]" % L)
            break
    return fs


# OJO con la contabilidad: el diccionario lleva CONTEOS de palabras;
# al nivel L el total de palabras es 2^L, y las absorbidas en j < L
# representan f(j)*2^j palabras que se multiplican por 2^(L-j). La
# funcion de arriba cuenta vueltos en unidades del nivel: f(L) =
# vueltos / 2^L es la probabilidad exacta del primer retorno en L.

# ---------------------------------------------------------------------------
# EL BARRIDO 1: primeros retornos a (0,1) desde (0,1).
# ---------------------------------------------------------------------------

print()
print("BARRIDO 1: primeros retornos al estado consecutivo (0,1):")
fs = barrido_retorno((0, 1), (0, 1), PROF)
print("conteos f(L)*2^L (cruce con la serie de Ovejas/LaTourette):")
print([int(round(f * 2 ** (i + 1))) for i, f in enumerate(fs[:20])])
print()
print("   L     P_L = Sigma f     S(L) = 1 - P_L    alfa local de S")
P = 0.0
Ss = {}
for i, f in enumerate(fs):
    L = i + 1
    P += f
    Ss[L] = 1.0 - P
    if L % 4 == 0 or L == len(fs):
        alfa = ""
        if L - 8 in Ss and Ss[L] > 0 and Ss[L - 8] > 0:
            alfa = "      %7.4f" % (-(math.log(Ss[L]) - math.log(Ss[L - 8]))
                                    / (math.log(L) - math.log(L - 8)))
        print("  %3d      %8.6f        %8.6f%s" % (L, P, Ss[L], alfa))

# ---------------------------------------------------------------------------
# EL BARRIDO 2: p directo -- retorno a (1,1) desde el rebote (2,2).
# ---------------------------------------------------------------------------

print()
print("BARRIDO 2: retorno al vortice (1,1) desde su rebote (2,2):")
fs2 = barrido_retorno((2, 2), (1, 1), PROF)
print()
print("   L     p_L = Sigma f     1 - p_L         alfa local")
P2 = 0.0
S2 = {}
for i, f in enumerate(fs2):
    L = i + 1
    P2 += f
    S2[L] = 1.0 - P2
    if L % 4 == 0 or L == len(fs2):
        alfa = ""
        if L - 8 in S2 and S2[L] > 0 and S2[L - 8] > 0:
            alfa = "      %7.4f" % (-(math.log(S2[L]) - math.log(S2[L - 8]))
                                    / (math.log(L) - math.log(L - 8)))
        print("  %3d      %8.6f        %8.6f%s" % (L, P2, S2[L], alfa))

print()
print("VEREDICTO (medido, orienta -- el criterio de arriba es exacto):")
print("  recurrencia (phi = 1) <=> S(L) -> 0. La firma critica-justa es")
print("  S(L) ~ c/sqrt(L) (alfa ~ 0,5); transitoria seria S(L) -> s > 0")
print("  (alfa -> 0 con S estancada). Un alfa estable cerca de 0,5 con")
print("  S bajando es la firma del paseo justo de RATAS/GOLONDRINAS;")
print("  la decision formal es el paso perturbed-IFS pendiente.")
