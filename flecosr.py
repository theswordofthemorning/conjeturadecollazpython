# flecosr.py
#
# LOS FLECOS DE LA SERIE R - LA IDENTIDAD DE ARDILLAS (04-08-2026;
# punto 2 de la retaguardia del norte).
#
#   La afirmacion #88 dejo la deconvolucion c(m) = suma_j R(j)-a(m-j)
#   EXACTA en 8 niveles, pero el test independiente de germenes solo
#   reproducia el centro (j = 5, 6, 7) con flecos +-1 en los bordes, y
#   el pendiente decia: "la contabilidad de orientacion bajo vuelcos".
#
#   LA CADENA LO RESUELVE SIN CONTABILIDAD DE ORIENTACION: la forma h
#   es el estado (2,-1) y "reentrada consecutiva" es LLEGAR AL ESTADO
#   (0,1). Entonces:
#
#     F(j) = numero de palabras desde (2,-1) que visitan (0,1) POR
#            PRIMERA VEZ en el paso j        (el "R" estructural)
#     D(m) = fusiones desde (2,-1) SIN pasar por (0,1) (directas al
#            vortice (1,1)), acumuladas con doblado
#
#   y por descomposicion de caminos la identidad ES EXACTA POR
#   CONSTRUCCION:
#
#     c(m)  =  suma_j F(j) - a(m-j)  +  D(m)
#
#   El R publicado salio de deconvolver c contra a SIN el termino D:
#   los flecos son D repartida por el triangulo. Aqui se calcula F, D
#   y c con la cadena, se verifica la identidad como IGUALDAD DE
#   ENTEROS, y se compara F con el R publicado.
#
#   De regalo: la cadena desde (2,-1) debe reproducir la serie c
#   publicada entera (el H de identidadexacta.py mas c(15), c(16)), y
#   desde (2,2) la serie b reducida ([1,4,11,28,66,149] en m = 6..12).
#   Mapa del atajo, enteros exactos, SystemExit antes de concluir.

C_PUBLICADA = {3: 0, 4: 0, 5: 0, 6: 1, 7: 3, 8: 9, 9: 24, 10: 58, 11: 134,
               12: 300, 13: 659, 14: 1426, 15: 3053, 16: 6487}
B_RED_PUBLICADA = {6: 1, 7: 4, 8: 11, 9: 28, 10: 66, 11: 149}
R_PUBLICADA = {3: 1, 4: 0, 5: 1, 6: 3, 7: 2, 8: 4, 9: 9, 10: 14, 11: 25,
               12: 47, 13: 89}
PROF = 26


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


def barrido(inicio, prof, quitar_en_01=False):
    # devuelve (absorbidas_acum[t], primeras_visitas_01[t], estados_finales)
    estados = {inicio: 1}
    absorbidas = 0
    acum, primeras = [], []
    for t in range(1, prof + 1):
        nuevo = {}
        nuevas_abs = 0
        visitas = 0
        for (k, c), n in estados.items():
            for bit in (0, 1):
                s = transicion(k, c, bit)
                if s[0] == 'fusion':
                    nuevas_abs += n
                    continue
                clave = (s[1], s[2])
                if quitar_en_01 and clave == (0, 1):
                    visitas += n           # primera visita: sale del flujo
                    continue
                nuevo[clave] = nuevo.get(clave, 0) + n
        absorbidas = 2 * absorbidas + nuevas_abs
        estados = nuevo
        acum.append(absorbidas)
        primeras.append(visitas)
    return acum, primeras, estados


# ---------------------------------------------------------------------------
# COMPROBACION 1: la cadena reproduce las series c y b reducidas publicadas.
# ---------------------------------------------------------------------------

c_cadena, _, _ = barrido((2, -1), PROF)
b_cadena, _, _ = barrido((2, 2), PROF)
for m, v in sorted(C_PUBLICADA.items()):
    if c_cadena[m - 1] != v:
        raise SystemExit("C1 c: m=%d cadena=%d publicada=%d"
                         % (m, c_cadena[m - 1], v))
for m, v in sorted(B_RED_PUBLICADA.items()):
    if b_cadena[m - 1] != v:
        raise SystemExit("C1 b: m=%d cadena=%d publicada=%d"
                         % (m, b_cadena[m - 1], v))

print("COMPROBACION 1 OK: la cadena desde (2,-1) reproduce c(m) publicada")
print("(m = 3..16, incluidos c(15) = 3053 y c(16) = 6487) y desde (2,2)")
print("la serie b reducida (m = 6..11). Cero discrepancias.")
print()
print("extension de c(m) por la cadena (m = 17..%d):" % PROF)
print("  " + " ".join(str(c_cadena[m - 1]) for m in range(17, PROF + 1)))

# ---------------------------------------------------------------------------
# COMPROBACION 2: LA IDENTIDAD c(m) = suma F(j)-a(m-j) + D(m), EXACTA.
#   F = primeras visitas a (0,1); D = fusiones sin pasar por (0,1);
#   a = la serie del par consecutivo, calculada aqui mismo con la cadena.
# ---------------------------------------------------------------------------

a_cadena, _, _ = barrido((0, 1), PROF)
D_acum, F, _ = barrido((2, -1), PROF, quitar_en_01=True)

for m in range(3, PROF + 1):
    suma = D_acum[m - 1]
    for j in range(1, m):
        if F[j - 1] and m - j >= 1:
            suma += F[j - 1] * a_cadena[m - j - 1]
    if suma != c_cadena[m - 1]:
        raise SystemExit("C2: m=%d suma=%d c=%d" % (m, suma, c_cadena[m - 1]))

print()
print("COMPROBACION 2 OK: c(m) = suma_j F(j)-a(m-j) + D(m) como IGUALDAD DE")
print("ENTEROS en m = 3..%d. La renovacion de la forma h factoriza por la" % PROF)
print("primera visita al estado consecutivo (0,1), con termino directo D.")

# ---------------------------------------------------------------------------
# COMPROBACION 3: F contra el R publicado -- los flecos, explicados.
# ---------------------------------------------------------------------------

print()
print("  j    F(j) cadena    R publicada    D nuevas en j")
D_nuevas = [D_acum[0]] + [D_acum[i] - 2 * D_acum[i - 1] for i in range(1, PROF)]
for j in range(3, 14):
    rp = R_PUBLICADA.get(j, None)
    print("%3d  %12d  %13s  %13d"
          % (j, F[j - 1], rp if rp is not None else "-", D_nuevas[j - 1]))

print()
print("F(j) extendida (j = 14..%d):" % PROF)
print("  " + " ".join(str(F[j - 1]) for j in range(14, PROF + 1)))
print()
print("CONCLUSION: F es la serie estructural de reentradas (primeras")
print("visitas de la cadena a (0,1)); el R publicado deconvolvia c contra")
print("a SIN el termino directo D, asi que donde D_nuevas != 0 el R")
print("absorbe la diferencia -- esos son los flecos +-1 de los bordes.")
print("La contabilidad de orientacion bajo vuelcos ya no hace falta: la")
print("cadena la lleva dentro.")
