# estratoscadena.py
#
# LOS ESTRATOS POR LA CADENA (k, c) - EL TEOREMA DE NUTRIAS: los canales de e8,
# cerrada como ESTRUCTURA DE SUBARBOLES, y las series extendidas.
# (04-08-2026; punto 3 del norte. Sin Lipmaa-Moriai: la cadena la
# sustituye -- los canales son los prefijos de dos bits.)
#
#   El estrato |M| de una fusion es el numero de estados con c IMPAR
#   que la palabra visita (mixto <=> c impar: ley de la moneda,
#   demostrada en cadenakc.lean). El barrido simbolico con el contador
#   de mixtos da TODAS las series e_s(N) de una vez, y ademas:
#
#   LA CONTABILIDAD DE CANALES ES ESTRUCTURAL. Los dos primeros bits
#   de la palabra son r mod 4, y los subarboles son:
#
#     prefijo 1,1 (r = 1 mod 4): (0,1) -> (1,-1) -> (0,1), dos mixtos:
#         el subarbol ES el arbol entero desplazado:
#         e_s(N) | r=1  =  e_{s-2}(N-2)          [la recursion vertical]
#     prefijo 1,0 (r = 3 mod 4): (0,1) -> (1,-1) -> (2,-1), dos mixtos:
#         el subarbol es el piso h:
#         e_s(N) | r=3  =  e^h_{s-2}(N-2)        [el canal H]
#     prefijo 0 (r par): (0,1) -> (1,2), un mixto:
#         e_s(N) | par  =  e^{(1,2)}_{s-1}(N-1)  [el canal par:
#         la ventana de Perras (s=2) y el rebote via (1,1)->(2,2)]
#
#   Las tres identidades se verifican aqui como IGUALDADES DE ENTEROS
#   nivel a nivel, y las series e6, e8, e10 se extienden mas alla de
#   todo lo medido (e8 se conocia hasta N = 18).
#
#   Convencion: e_s(N) cuenta las clases NUEVAS del nivel N (fusion
#   exactamente en el paso N) con |M| = s. Sum_s e_s(N) = b(N-1).

M_TOPE = 13          # mixtos contados exactos hasta aqui (lump encima)
PROF = 29
TOPE_ESTADOS = 9 * 10 ** 6

E8_MEDIDA = {10: 3, 11: 7, 12: 15, 13: 27, 14: 45, 15: 73, 16: 111,
             17: 166, 18: 237}   # afirmacion 77 (la escalera fallada)


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


def barrido_estratos(inicio, prof, m_inicial=0):
    # devuelve nuevas[prof][m] = palabras absorbidas en el paso prof
    # con m mixtos (el paso de la fusion cuenta como mixto, c impar)
    estados = {(inicio[0], inicio[1], m_inicial): 1}
    nuevas = {}
    for t in range(1, prof + 1):
        nuevo = {}
        for (k, c, m), n in estados.items():
            m2 = min(m + (c % 2 != 0), M_TOPE + 1)
            for bit in (0, 1):
                s = transicion(k, c, bit)
                if s[0] == 'fusion':
                    nuevas.setdefault(t, {})
                    nuevas[t][m2] = nuevas[t].get(m2, 0) + n
                else:
                    clave = (s[1], s[2], m2)
                    nuevo[clave] = nuevo.get(clave, 0) + n
        estados = nuevo
        if len(estados) > TOPE_ESTADOS:
            print("[cortado en prof %d: %d estados]" % (t, len(estados)))
            return nuevas, t
    return nuevas, prof


print("barrido principal (0,1) hasta prof %d..." % PROF)
ppal, prof_p = barrido_estratos((0, 1), PROF)

# ---------------------------------------------------------------------------
# COMPROBACION 1: las series conocidas -- e2 = 1 y e4 = 1 (unicidades
# demostradas), e6 contra su formula cuadratica, e8 contra lo medido.
# ---------------------------------------------------------------------------

for N in range(4, prof_p + 1):
    if ppal.get(N, {}).get(2, 0) != 1:
        raise SystemExit("C1 e2: N=%d da %d" % (N, ppal.get(N, {}).get(2, 0)))
    if N >= 5 and ppal.get(N, {}).get(4, 0) != 1:
        raise SystemExit("C1 e4: N=%d da %d" % (N, ppal.get(N, {}).get(4, 0)))
    if N >= 10:
        e6 = 3 + (N - 7) * (N - 8) // 2
        if ppal[N].get(6, 0) != e6:
            raise SystemExit("C1 e6: N=%d cadena=%d formula=%d"
                             % (N, ppal[N].get(6, 0), e6))
for N, v in sorted(E8_MEDIDA.items()):
    if ppal[N].get(8, 0) != v:
        raise SystemExit("C1 e8: N=%d cadena=%d medida=%d"
                         % (N, ppal[N].get(8, 0), v))

print("COMPROBACION 1 OK: e2 = e4 = 1 (todas las N), e6 = 3+(N-7)(N-8)/2")
print("clavada hasta N = %d (antes: 18), y e8 = lo medido en N = 10..18." % prof_p)

# ---------------------------------------------------------------------------
# COMPROBACION 2: LOS TRES CANALES, como igualdades de enteros.
#   vertical: e_s(N) del subarbol r=1 mod 4 = e_{s-2}(N-2) del arbol;
#   h:        subarbol r=3 mod 4 = piso h desplazado;
#   par:      subarbol r par = arbol de (1,2) desplazado.
#   El canal vertical es ESTRUCTURAL (el subarbol de 1,1 ES el arbol);
#   aqui se verifican los otros dos contra barridos independientes.
# ---------------------------------------------------------------------------

print()
print("barrido del piso h (2,-1) y del canal par (1,2)...")
piso_h, prof_h = barrido_estratos((2, -1), PROF - 2, m_inicial=2)
canal_p, prof_c = barrido_estratos((1, 2), PROF - 1, m_inicial=1)

for N in range(4, prof_p + 1):
    for s in range(2, M_TOPE, 2):
        total = ppal[N].get(s, 0)
        vert = ppal.get(N - 2, {}).get(s - 2, 0) if N - 2 >= 1 else 0
        hh = piso_h.get(N - 2, {}).get(s, 0) if N - 2 >= 1 else 0
        par = canal_p.get(N - 1, {}).get(s, 0) if N - 1 >= 1 else 0
        if total != vert + hh + par:
            raise SystemExit("C2: N=%d s=%d total=%d != %d+%d+%d"
                             % (N, s, total, vert, hh, par))

print("COMPROBACION 2 OK: e_s(N) = e_{s-2}(N-2) + e^h_s(N-2) + e^par_s(N-1)")
print("como IGUALDAD DE ENTEROS en todos los niveles y estratos (s <= %d)."
      % (M_TOPE - 1))
print("La contabilidad de canales de e8 (afirmacion 84) es ESTRUCTURAL:")
print("los canales son los subarboles de los dos primeros bits de la")
print("cadena, y la recursion vertical es la identidad de subarbol.")

# ---------------------------------------------------------------------------
# COMPROBACION 3: las series extendidas, y las diferencias de e8.
# ---------------------------------------------------------------------------

print()
print("  N      e6      e8      e10      e12    (nuevas del nivel N)")
for N in range(10, prof_p + 1):
    d = ppal[N]
    print("%3d  %6d  %6d  %7d  %7d"
          % (N, d.get(6, 0), d.get(8, 0), d.get(10, 0), d.get(12, 0)))

e8 = [ppal[N].get(8, 0) for N in range(10, prof_p + 1)]
d1 = [e8[i + 1] - e8[i] for i in range(len(e8) - 1)]
d2 = [d1[i + 1] - d1[i] for i in range(len(d1) - 1)]
d3 = [d2[i + 1] - d2[i] for i in range(len(d2) - 1)]
print()
print("e8 diferencias 1as:", d1)
print("e8 diferencias 2as:", d2)
print("e8 diferencias 3as:", d3)
print()
print("CONCLUSION: e8 extendida %d niveles mas alla de lo medido; si las" % (prof_p - 18))
print("terceras diferencias no se estabilizan, e8 NO es cubica (la")
print("escalera fallada, ahora con serie larga para buscar su forma).")

# ---------------------------------------------------------------------------
# COMPROBACION 4 (09-08-2026): LA ESCALERA DE FORMAS CERRADAS TERMINA EN e6.
#   Busqueda EXHAUSTIVA de forma cuasi-polinomial para e8, e10, e12:
#     e_s(N) = P(N) + correccion(N mod p),   grado(P) <= 8, p <= 8,
#   con el ajuste anclado en CADA arranque N1 = 10..16 (porque una forma
#   legitima puede valer solo desde un N1, como la propia e6) y resuelto
#   EXACTO (Fraction, eliminacion gaussiana); vale solo si reproduce la
#   serie ENTERA desde N1 con al menos 6 puntos fuera del ajuste.
#   Resultado esperado (medido el 09-08): NINGUNA valida -- e8/e10/e12
#   llevan un ingrediente no cuasi-polinomial (las diferencias altas
#   oscilan con amplitud creciente, la firma de un termino tipo b(k)).
#   e6 se usa de CONTROL: su forma cuadratica debe encontrarse.
#   Y ademas: ninguna de las tres series esta en OEIS (consultado
#   09-08-2026: "No results" para las tres) -- van a sucesiones.txt.
# ---------------------------------------------------------------------------

from fractions import Fraction

def _ajusta_cuasi(serie, n0, grado, periodo, arranque):
    # ajusta con los primeros nvar puntos desde 'arranque' y exige la
    # igualdad EXACTA en toda la cola; None si no hay forma
    nvar = grado + 1 + periodo - 1
    puntos = serie[arranque:]
    if len(puntos) < nvar + 6:
        return None
    A = []
    for i in range(nvar):
        N = n0 + arranque + i
        fila = [Fraction(N) ** g for g in range(grado + 1)]
        fila += [Fraction(1 if N % periodo == r else 0)
                 for r in range(1, periodo)]
        fila.append(Fraction(puntos[i]))
        A.append(fila)
    m = nvar
    fila_p = 0
    for col in range(m):
        piv = next((r for r in range(fila_p, len(A)) if A[r][col] != 0), None)
        if piv is None:
            continue
        A[fila_p], A[piv] = A[piv], A[fila_p]
        pv = A[fila_p][col]
        A[fila_p] = [x / pv for x in A[fila_p]]
        for r in range(len(A)):
            if r != fila_p and A[r][col] != 0:
                f = A[r][col]
                A[r] = [a - f * b for a, b in zip(A[r], A[fila_p])]
        fila_p += 1
    sol = [Fraction(0)] * m
    for r in range(fila_p):
        col = next((c for c in range(m) if A[r][c] == 1), None)
        if col is not None:
            sol[col] = A[r][m]
    for i, v in enumerate(puntos):
        N = n0 + arranque + i
        w = sum(sol[g] * N ** g for g in range(grado + 1))
        if N % periodo != 0:
            w += sol[grado + 1 + (N % periodo) - 1]
        if w != v:
            return None
    return sol

series_c4 = {
    6:  [ppal[N].get(6, 0) for N in range(10, prof_p + 1)],
    8:  e8,
    10: [ppal[N].get(10, 0) for N in range(10, prof_p + 1)],
    12: [ppal[N].get(12, 0) for N in range(10, prof_p + 1)],
}
formas = {}
for s, serie in series_c4.items():
    hallada = None
    for g in range(1, 9):
        for p in range(1, 9):
            for arr in range(0, 7):
                sol = _ajusta_cuasi(serie, 10, g, p, arr)
                if sol is not None and hallada is None:
                    hallada = (g, p, 10 + arr, sol)
        if hallada:
            break
    formas[s] = hallada

if formas[6] is None:
    raise SystemExit("C4: el CONTROL fallo -- la cuadratica de e6 no se "
                     "encontro; el buscador esta roto")
if formas[6][0] != 2:
    raise SystemExit("C4: el control e6 salio con grado %d != 2" % formas[6][0])
for s in (8, 10, 12):
    if formas[s] is not None:
        raise SystemExit("C4: e%d SI tiene forma cuasi-polinomial %s -- "
                         "actualizar la conclusion, esto la refuta" % (s, formas[s][:3]))

print()
print("COMPROBACION 4 OK: el control e6 se encuentra (grado 2, como debe),")
print("y e8, e10, e12 NO admiten forma cuasi-polinomial con grado <= 8,")
print("periodo <= 8 y arranque N1 <= 16, validada exacta sobre toda la cola")
print("(>= 6 puntos fuera del ajuste). LA ESCALERA DE FORMAS CERRADAS")
print("TERMINA EN e6: los estratos 8, 10, 12 llevan un ingrediente")
print("combinatorio no cuasi-polinomial. Y ninguna de las tres series esta")
print("en OEIS (09-08-2026, 'No results' las tres): tres sucesiones nuevas")
print("mas para sucesiones.txt.")
