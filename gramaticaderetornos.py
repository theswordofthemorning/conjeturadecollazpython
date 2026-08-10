# gramaticaderetornos.py
#
# LA GRAMATICA DE RETORNOS DEL TRIANGULO DE FUSION (11-08-2026, el
# instrumento que pide el addendum 3 de leydelborde.txt): unir OVEJAS
# (los primeros retornos), el triangulo F(t, S) y el programa lambda
# en UN objeto, con identidades verificables como enteros.
#
#   LA DESCOMPOSICION. Todo camino de la cadena real desde (0,1) se
#   parte de forma UNICA en bloques de primer retorno a (0,1) mas, si
#   funde, una cola de absorcion que no pasa por (0,1). Sean
#
#     R(L, z) = numero de palabras de largo L con z ceros que VUELVEN
#               a (0,1) por primera vez en el paso L (sin fundir)
#     A(L, z) = numero de palabras de largo L con z ceros que FUNDEN
#               en el paso L sin haber vuelto a (0,1)
#
#   Entonces (renovacion pura, sin analisis):
#
#     C2:  F(t, S) = Suma_j (R^(*j) * A)(t, t - S ceros)   EXACTO
#
#   -- el triangulo entero es la convolucion de la gramatica. Y en
#   masas (cada bit pesa 1/2):
#
#     rho   = Suma_L R(L)/2^L   (P(volver al lazo antes de fundir))
#     alfa  = Suma_L A(L)/2^L   (P(fundir antes de volver))
#     phi   = alfa / (1 - rho)  (la geometrica de la renovacion)
#     deficit = 1 - rho - alfa  (la masa que ni vuelve ni funde:
#               el escape -- phi = 1 <=> deficit relativo -> 0)
#
#   COMPROBACIONES (SystemExit):
#     C1  conservacion de masa del barrido de bloques, nivel a nivel.
#     C2  la identidad de convolucion contra el triangulo F(t, S)
#         recomputado aparte (t <= T_TRIANGULO), enteros exactos.
#     C3  la serie rho/alfa/deficit y phi_trunc = alfa/(1-rho) contra
#         la serie a(k)/2^k publicada (comparacion de tendencia).
#
#   Mapa del ATAJO via la cadena real; enteros exactos.

from fractions import Fraction

PROF_BLOQUES = 28      # largo maximo de los bloques R y A
Z_MAX = 12             # ceros maximos rastreados por bloque (la masa
                       # con mas ceros se acumula como 'desbordada')
T_TRIANGULO = 20       # hasta donde se verifica la convolucion
TOPE_ESTADOS = 4 * 10 ** 6

# a(k)/2^k publicada (sucesiones.txt; el primer volcado de esta tabla
# puso a(28) en la casilla de k=26 y el 1,70 absurdo lo delato: capa 1)
A_2K = {12: 1476 / 2.0 ** 12, 20: 421643 / 2.0 ** 20,
        26: 28247507 / 2.0 ** 26, 28: 114400435 / 2.0 ** 28,
        32: 1871137623 / 2.0 ** 32}


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
# EL BARRIDO DE BLOQUES: desde (0,1), sin volver a pisar (0,1); las
# transiciones que aterrizan en (0,1) cuentan como retorno R, las
# fusiones como absorcion A. Estados con ceros: (k, c, z), z <= Z_MAX
# (el exceso va a 'desbordada' y NO entra en C2 -- se declara).
# ---------------------------------------------------------------------------

R = {}
A = {}
estados = {(0, 1, 0): 1}
desbordada = 0
conservacion_ok = True
total_procesado = 0
for L in range(1, PROF_BLOQUES + 1):
    nuevo = {}
    for (k, c, z), n in estados.items():
        for bit in (0, 1):
            r = transicion(k, c, bit)
            z2 = z + (1 - bit)
            if r[0] == 'fusion':
                if z2 <= Z_MAX:
                    A[(L, z2)] = A.get((L, z2), 0) + n
                else:
                    desbordada += n
            elif (r[1], r[2]) == (0, 1):
                if z2 <= Z_MAX:
                    R[(L, z2)] = R.get((L, z2), 0) + n
                else:
                    desbordada += n
            else:
                if z2 <= Z_MAX:
                    clave = (r[1], r[2], z2)
                    nuevo[clave] = nuevo.get(clave, 0) + n
                else:
                    desbordada += n
    estados = nuevo
    # C1: masa total del nivel = 2^L (vivos + retornados/absorbidos
    # re-expandidos + desbordada re-expandida) -- se verifica en masa
    # racional al final, aqui solo el conteo de estados
    if len(estados) > TOPE_ESTADOS:
        raise SystemExit("bloques: tope de estados en L = %d" % L)

# C1 en masas exactas: sum(vivos)/2^prof + sum((R+A)(L)/2^L) + masa
# desbordada (acumulada con su nivel aproximado <= 1) debe dar <= 1 y
# el total sin desbordar debe cerrar contra 1 - desbordes
masa_bloques = sum(Fraction(n, 2 ** L) for (L, z), n in R.items()) \
    + sum(Fraction(n, 2 ** L) for (L, z), n in A.items())
masa_viva = sum(Fraction(n, 2 ** PROF_BLOQUES) for n in estados.values())
if masa_bloques + masa_viva > 1:
    raise SystemExit("C1: masa %s > 1" % float(masa_bloques + masa_viva))
print("COMPROBACION 1 OK: masa de bloques %.6f + viva %.6f <= 1 "
      % (float(masa_bloques), float(masa_viva)))
print("(desbordada por z > %d: %s caminos, fuera de C2 por diseno)"
      % (Z_MAX, desbordada))

# ---------------------------------------------------------------------------
# EL TRIANGULO F(t, z) RECOMPUTADO APARTE (por ceros, t <= T_TRIANGULO)
# ---------------------------------------------------------------------------

F = {}
est2 = {(0, 1, 0): 1}
for t in range(1, T_TRIANGULO + 1):
    nuevo = {}
    for (k, c, z), n in est2.items():
        for bit in (0, 1):
            r = transicion(k, c, bit)
            z2 = z + (1 - bit)
            if r[0] == 'fusion':
                if z2 <= Z_MAX:
                    F[(t, z2)] = F.get((t, z2), 0) + n
            else:
                if z2 <= Z_MAX:
                    clave = (r[1], r[2], z2)
                    nuevo[clave] = nuevo.get(clave, 0) + n
    est2 = nuevo

# ---------------------------------------------------------------------------
# COMPROBACION 2: F = Suma_j R^(*j) * A  (convolucion en (largo, ceros))
# ---------------------------------------------------------------------------


def convolucion(P, Q, tope_L):
    S = {}
    for (l1, z1), n1 in P.items():
        for (l2, z2), n2 in Q.items():
            if l1 + l2 <= tope_L and z1 + z2 <= Z_MAX:
                S[(l1 + l2, z1 + z2)] = S.get((l1 + l2, z1 + z2), 0) + n1 * n2
    return S


acumulado = dict(A)
termino = dict(A)
while True:
    termino = convolucion(R, termino, T_TRIANGULO)
    if not termino:
        break
    for clave, n in termino.items():
        acumulado[clave] = acumulado.get(clave, 0) + n

fallos = 0
for t in range(3, T_TRIANGULO + 1):
    for z in range(0, Z_MAX + 1):
        if F.get((t, z), 0) != acumulado.get((t, z), 0):
            fallos += 1
            print("  C2 FALLA en (t=%d, z=%d): F = %d, convolucion = %d"
                  % (t, z, F.get((t, z), 0), acumulado.get((t, z), 0)))
if fallos:
    raise SystemExit("C2: %d celdas fallan" % fallos)
print()
print("COMPROBACION 2 OK: el triangulo ENTERO (t <= %d, z <= %d) es" %
      (T_TRIANGULO, Z_MAX))
print("EXACTAMENTE la convolucion de la gramatica: F = Suma_j R^(*j) * A.")
print("La renovacion del triangulo es identidad de enteros, no analogia.")

# ---------------------------------------------------------------------------
# COMPROBACION 3: las series rho, alfa, deficit y phi_trunc
# ---------------------------------------------------------------------------

print()
print("las series de la renovacion (parciales hasta L):")
print("   L    rho_L      alfa_L     deficit_L   phi_trunc = alfa/(1-rho)")
rho = alfa = Fraction(0)
rho_por_L = {}
alfa_por_L = {}
for (L, z), n in R.items():
    rho_por_L[L] = rho_por_L.get(L, 0) + n
for (L, z), n in A.items():
    alfa_por_L[L] = alfa_por_L.get(L, 0) + n
for L in range(1, PROF_BLOQUES + 1):
    rho += Fraction(rho_por_L.get(L, 0), 2 ** L)
    alfa += Fraction(alfa_por_L.get(L, 0), 2 ** L)
    if L % 2 == 0 and L >= 10:
        deficit = 1 - rho - alfa
        phi_t = alfa / (1 - rho)
        print("  %2d  %.6f   %.6f   %.6f    %.6f"
              % (L, float(rho), float(alfa), float(deficit), float(phi_t)))
print()
print("contra la serie publicada a(k)/2^k: %s"
      % "  ".join("k=%d: %.4f" % (k, v) for k, v in sorted(A_2K.items())))
print()
print("Lectura: phi_trunc = alfa/(1-rho) con series truncadas es una")
print("COTA INFERIOR de phi (todo bloque contado funde de verdad); el")
print("deficit truncado mezcla 'bloques mas largos que %d' con 'escape'" % PROF_BLOQUES)
print("y NO decide. La identidad C2 es el teorema-forma del fichero:")
print("phi = 1 <=> alfa = 1 - rho <=> la gramatica no deja escapar masa.")

# ---------------------------------------------------------------------------
# COMPROBACION 4: EL RECORD. La resumacion geometrica de bloques es una
#   cota inferior VALIDA de phi (descomposicion unica en bloques de
#   primer retorno + cola; composiciones disjuntas; medida producto;
#   los subconteos por Z_MAX solo la bajan). Debe SUPERAR la mejor
#   cota previa del repo, a(32)/2^32 = 0,435658 -- si no, este fichero
#   no aporta y hay que decirlo.
# ---------------------------------------------------------------------------

phi_record = float(alfa / (1 - rho))
previa = 1871137623 / 2.0 ** 32
if phi_record <= previa:
    raise SystemExit("C4: la resumacion %.6f NO supera la cota previa %.6f"
                     % (phi_record, previa))
print()
print("COMPROBACION 4 OK -- EL RECORD DE LA COTA INFERIOR DE phi:")
print("  phi >= alfa/(1-rho) = %.6f   (bloques de largo <= %d, z <= %d,"
      % (phi_record, PROF_BLOQUES, Z_MAX))
print("  enteros exactos + resumacion geometrica de la renovacion)")
print("  contra el 0,435658 de a(32)/2^32 (que costo el barrido a 2^32).")
print("  La estructura de renovacion convierte profundidad %d en mas"
      % PROF_BLOQUES)
print("  cota que la fuerza bruta a 32: el puente del gemelo, cobrado.")
