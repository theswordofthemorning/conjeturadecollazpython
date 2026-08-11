# recordsincap.py
#
# EL RECORD SIN CAP, EN ARITMETICA EXACTA (P4 del paper del programa,
# 11-08-2026; la mejora "gratis" que dejo anotada la 8a revision).
#
#   El record phi >= 0,443061 de gramaticaderetornos.py se computo con
#   el cap z <= 12 (ceros maximos por bloque), que manda al descarte
#   el 25,77% de la masa de caminos -- el cap solo hacia falta para la
#   identidad C2 del triangulo, no para la cota. Este fichero repite
#   la resumacion geometrica de la renovacion SIN el cap (estados
#   (k, c) a secas) y MAS PROFUNDO (bloques de largo <= 34 en vez de
#   28), todo en enteros exactos + Fraction.
#
#   POR QUE LA COTA ES VALIDA (el mismo argumento del record, intacto):
#   todo camino que funde se descompone de forma UNICA en j >= 0
#   bloques de primer retorno a (0,1) mas una cola de absorcion que no
#   pisa (0,1). Las composiciones son eventos DISJUNTOS de la medida
#   producto (cada bit pesa 1/2), asi que
#
#     phi >= Suma_j rho^j * alfa = alfa/(1 - rho)
#
#   con rho y alfa TRUNCADOS a bloques de largo <= PROF_BLOQUES: todo
#   subconteo (truncar el largo, o el cap de ceros del fichero viejo)
#   solo puede BAJAR la cota. Quitar el cap y subir el largo la sube.
#
#   COMPROBACIONES (SystemExit):
#     C0  el control de reproduccion: el barrido VIEJO (z <= 12,
#         L <= 28) re-corrido aqui debe dar exactamente el record
#         publicado 0,443061 -- si no, este fichero no es comparable.
#     C1  conservacion EXACTA: sin cap nada se descarta, asi que
#         rho + alfa + masa_viva == 1 como IGUALDAD de racionales
#         (el fichero viejo solo podia comprobar <= 1).
#     C2  monotonia: phi_trunc(L) = alfa_L/(1-rho_L) debe ser
#         no-decreciente en L (alfa sube, 1-rho baja) -- la cota
#         mejora nivel a nivel o algo esta roto.
#     C3  EL CENSO DE PARES ENTEROS REALES (el mismo tipo de
#         verificacion que la 8a le hizo al record viejo): las 2^20
#         clases mod 2^20 caminadas como DOS enteros de verdad con el
#         mapa del atajo -- sin llamar a transicion() -- deben dar
#         R(t)*2^(20-t) retornos y A(t)*2^(20-t) absorciones, celda a
#         celda, t = 1..20.
#     C4  EL VEREDICTO: la cota nueva debe superar (a) el record
#         0,443061 del cap, (b) el 0,435658 de a(32)/2^32. Y el
#         parcial a L = 28 debe caer cerca del ~0,4503 que la 8a
#         revision midio en float sin cap (se imprime para cotejo).
#
#   Mapa del ATAJO via la cadena real (la misma transicion de
#   gramaticaderetornos.py, duplicada a proposito -- regla de la casa).

from fractions import Fraction

PROF_BLOQUES = 34      # largo maximo de los bloques sin cap (~7,6M
                       # estados vivos al final, ~4 GB pico; el fichero
                       # entero, censo incluido, corre en ~2 min)
PROF_CONTROL = 28      # los parametros EXACTOS del record viejo...
Z_MAX_CONTROL = 12     # ...para la reproduccion C0
RECORD_VIEJO = "0.443061"    # lo que imprime gramaticaderetornos.py
TOPE_ESTADOS = 20 * 10 ** 6


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


def decimales(fr, n):
    # los primeros n decimales de una Fraction, exactos, como texto
    entero = fr.numerator // fr.denominator
    resto = fr - entero
    digitos = (resto * 10 ** n).numerator // (resto * 10 ** n).denominator
    return "%d.%0*d" % (entero, n, digitos)


# ---------------------------------------------------------------------------
# COMPROBACION 0: el control -- el barrido VIEJO (con cap) re-corrido,
# debe reproducir el record publicado digito a digito.
# ---------------------------------------------------------------------------

R0 = {}
A0 = {}
estados = {(0, 1, 0): 1}
for L in range(1, PROF_CONTROL + 1):
    nuevo = {}
    for (k, c, z), n in estados.items():
        for bit in (0, 1):
            r = transicion(k, c, bit)
            z2 = z + (1 - bit)
            if z2 > Z_MAX_CONTROL:
                continue
            if r[0] == 'fusion':
                A0[L] = A0.get(L, 0) + n
            elif (r[1], r[2]) == (0, 1):
                R0[L] = R0.get(L, 0) + n
            else:
                clave = (r[1], r[2], z2)
                nuevo[clave] = nuevo.get(clave, 0) + n
    estados = nuevo
rho0 = sum(Fraction(n, 2 ** L) for L, n in R0.items())
alfa0 = sum(Fraction(n, 2 ** L) for L, n in A0.items())
phi_control = alfa0 / (1 - rho0)
if ("%.6f" % float(phi_control)) != RECORD_VIEJO:
    raise SystemExit("C0: el control da %.6f y el record publicado es %s"
                     % (float(phi_control), RECORD_VIEJO))
print("COMPROBACION 0 OK: el barrido viejo (z <= %d, L <= %d) reproduce"
      % (Z_MAX_CONTROL, PROF_CONTROL))
print("el record publicado phi >= %s digito a digito." % RECORD_VIEJO)
print()

# ---------------------------------------------------------------------------
# EL BARRIDO SIN CAP: estados (k, c), ningun camino descartado.
# ---------------------------------------------------------------------------

R = {}
A = {}
estados = {(0, 1): 1}
maximo_estados = 0
for L in range(1, PROF_BLOQUES + 1):
    nuevo = {}
    for (k, c), n in estados.items():
        for bit in (0, 1):
            r = transicion(k, c, bit)
            if r[0] == 'fusion':
                A[L] = A.get(L, 0) + n
            elif (r[1], r[2]) == (0, 1):
                R[L] = R.get(L, 0) + n
            else:
                clave = (r[1], r[2])
                nuevo[clave] = nuevo.get(clave, 0) + n
    estados = nuevo
    maximo_estados = max(maximo_estados, len(estados))
    if len(estados) > TOPE_ESTADOS:
        raise SystemExit("sin cap: tope de estados en L = %d" % L)

# ---------------------------------------------------------------------------
# COMPROBACION 1: conservacion EXACTA de la masa (igualdad, no <=)
# ---------------------------------------------------------------------------

rho = sum(Fraction(n, 2 ** L) for L, n in R.items())
alfa = sum(Fraction(n, 2 ** L) for L, n in A.items())
masa_viva = sum(Fraction(n, 2 ** PROF_BLOQUES) for n in estados.values())
if rho + alfa + masa_viva != 1:
    raise SystemExit("C1: rho + alfa + viva = %s, no es 1 EXACTO"
                     % float(rho + alfa + masa_viva))
print("COMPROBACION 1 OK: rho + alfa + masa_viva == 1 como IGUALDAD de")
print("racionales (sin cap nada se descarta; el fichero viejo solo")
print("podia comprobar <= 1). Estados vivos al final: %d (pico %d)."
      % (len(estados), maximo_estados))
print()

# ---------------------------------------------------------------------------
# COMPROBACION 2: la serie phi_trunc(L), monotona no-decreciente
# ---------------------------------------------------------------------------

print("la serie de la cota (parciales hasta L, sin cap):")
print("   L    rho_L      alfa_L     viva_L      phi_trunc")
rho_L = alfa_L = Fraction(0)
phi_anterior = Fraction(0)
phi_28 = None
for L in range(1, PROF_BLOQUES + 1):
    rho_L += Fraction(R.get(L, 0), 2 ** L)
    alfa_L += Fraction(A.get(L, 0), 2 ** L)
    phi_t = alfa_L / (1 - rho_L)
    if phi_t < phi_anterior:
        raise SystemExit("C2: phi_trunc BAJA en L = %d" % L)
    phi_anterior = phi_t
    if L == 28:
        phi_28 = phi_t
    if L % 2 == 0 and L >= 20:
        # phi_t impreso TRUNCADO con decimales() -- la misma convencion
        # que la escalera final (9a, adv 3: antes la serie redondeaba
        # con %.6f y la escalera truncaba: 0.462782 vs 0.462781 para el
        # mismo racional)
        print("  %2d  %.6f   %.6f   %.6f    %s"
              % (L, float(rho_L), float(alfa_L),
                 1 - float(rho_L) - float(alfa_L), decimales(phi_t, 6)))
print("COMPROBACION 2 OK: la cota mejora (no-decreciente) nivel a nivel.")
print()
print("cotejo con la 8a revision (midio ~0,4503 en float, sin cap, a 28):")
print("  phi_trunc(28) sin cap, exacto = %s" % decimales(phi_28, 6))
print()

# ---------------------------------------------------------------------------
# COMPROBACION 3: EL CENSO DE PARES ENTEROS REALES. Sin transicion():
# los dos enteros del par caminados con el mapa del atajo a pelo.
# Representante x0 = 2^LC_CENSO * M_CENSO + r con M_CENSO = 2^10:
# ningun valor baja de M_CENSO en LC_CENSO pasos (x_t >= x0/2^t), asi
# que el ciclo terminal {1, 2} es inalcanzable y toda igualdad x == y
# es fusion de coeficientes (S igualada), no coalescencia del ciclo.
# (9a revision, adv 3: el margen NO excluye por si solo que
# |y - x| == 1 detecte un estado distinto de (0,1) -- la
# identificacion no se supone: la VALIDA el empate celda a celda
# contra la gramatica, que es exactamente lo que C3 comprueba.)
# ---------------------------------------------------------------------------

LC_CENSO = 20
M_CENSO = 2 ** 10


def paso_atajo(n):
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


R_censo = {}
A_censo = {}
base = 2 ** LC_CENSO * M_CENSO
for r in range(2 ** LC_CENSO):
    x = base + r
    y = x + 1
    for t in range(1, LC_CENSO + 1):
        x = paso_atajo(x)
        y = paso_atajo(y)
        if x == y:
            A_censo[t] = A_censo.get(t, 0) + 1
            break
        if abs(y - x) == 1:
            R_censo[t] = R_censo.get(t, 0) + 1
            break

fallos = 0
for t in range(1, LC_CENSO + 1):
    if R_censo.get(t, 0) != R.get(t, 0) * 2 ** (LC_CENSO - t) \
            or A_censo.get(t, 0) != A.get(t, 0) * 2 ** (LC_CENSO - t):
        fallos += 1
        print("  C3 FALLA en t = %d: censo (R %d, A %d), gramatica (R %d, A %d)"
              % (t, R_censo.get(t, 0), A_censo.get(t, 0),
                 R.get(t, 0) * 2 ** (LC_CENSO - t),
                 A.get(t, 0) * 2 ** (LC_CENSO - t)))
if fallos:
    raise SystemExit("C3: el censo de pares reales discrepa en %d niveles" % fallos)
print("COMPROBACION 3 OK: el censo de pares enteros REALES (2^%d clases,"
      % LC_CENSO)
print("dos orbitas caminadas a pelo, sin transicion()) clava R(t) y A(t)")
print("celda a celda, t = 1..%d -- la gramatica sin cap cuenta lo real."
      % LC_CENSO)
print()

# ---------------------------------------------------------------------------
# COMPROBACION 4: EL VEREDICTO
# ---------------------------------------------------------------------------

phi_nuevo = alfa / (1 - rho)
previa_barrido = Fraction(1871137623, 2 ** 32)
if phi_nuevo <= phi_control:
    raise SystemExit("C4: la cota sin cap %.6f NO supera el record con cap %.6f"
                     % (float(phi_nuevo), float(phi_control)))
if phi_nuevo <= previa_barrido:
    raise SystemExit("C4: la cota sin cap %.6f NO supera a(32)/2^32 = %.6f"
                     % (float(phi_nuevo), float(previa_barrido)))
print("COMPROBACION 4 OK -- EL RECORD NUEVO DE LA COTA INFERIOR DE phi:")
print()
print("  phi >= alfa/(1 - rho) = %s..." % decimales(phi_nuevo, 12))
print()
print("  (bloques de largo <= %d, SIN cap de ceros, enteros exactos +" % PROF_BLOQUES)
print("  resumacion geometrica; rho = %s..., alfa = %s...)"
      % (decimales(rho, 8), decimales(alfa, 8)))
print()
print("  la escalera de records del repo:")
print("    a(32)/2^32 (fuerza bruta a 2^32)          0.435658")
print("    renovacion, cap z <= 12, L <= 28 (8a)     %s" % RECORD_VIEJO)
print("    renovacion, sin cap, L <= 28              %s" % decimales(phi_28, 6))
print("    renovacion, sin cap, L <= %d  ESTE        %s"
      % (PROF_BLOQUES, decimales(phi_nuevo, 6)))
print()
print("  El cap z <= 12 descartaba el 25,77% de la masa (hallazgo de la")
print("  8a); quitarlo cobra esa masa y la profundidad extra hace el")
print("  resto. La cota sigue siendo cota: todo subconteo solo baja.")
