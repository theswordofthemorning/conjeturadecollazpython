# cadenaqnr.py
#
# LA CADENA (k, c) PARA TODA LA FAMILIA (qx + r)/2 -- el objetivo
# secundario 1: la maquinaria sin Collatz (09-08-2026).
#
#   Las SEIS LEYES de Leonas valen con 3 -> q y 1 -> r (q impar, r
#   impar), derivadas igual que en paseodeladeuda.py:
#
#     nucleo k >= 1, c PAR:    N1 bit0: (k, c/2)
#                              N2 bit1: (k, (qc + r(1 - q^k))/2)
#     nucleo k >= 1, c IMPAR:  N3 bit0: (k+1, (qc + r)/2)
#                              N4 bit1: k >= 2: (k-1, (c - r q^(k-1))/2)
#                                       k = 1:  gap g' = (c - r)/2
#                                         g' = 0  -> FUSION (c = r)
#                                         g' != 0 -> (0, |g'|)
#     frontera k = 0, g PAR:   F1 bit0: (0, g/2)    F2 bit1: (0, qg/2)
#     frontera k = 0, g IMPAR: F3 bit0: (1, (qg + r)/2)
#                              F4 bit1: (1, (r - qg)/2)
#
#   Y LA LINEA QUE CARACTERIZA AL 3 -- EL TEOREMA DE AGUILAS
#   (bautizado por el usuario el 09-08-2026; rapaz porque CORTA la
#   familia entera en q = 3), que es el hallazgo del fichero:
#   el multiplicador de la perpetuidad de c es moneda justa entre 1/2
#   y q/2, o sea
#
#       E[m] = (1 + q)/4       E[log2 m] = (log2 q - 2)/2
#
#   E[m] = 1  <=>  q = 3   (la criticidad kappa = 1 de TIGRESAS)
#   E[log2 m] < 0  <=>  q < 4  (contraccion en log: SOLO q = 1, 3)
#
#   Para q >= 5 la perpetuidad es SUPERCRITICA EN LOG (E[log m] > 0)
#   y no hay ventana de momentos para Moscas.
#   ⇢ CORRECCION (REVISION EXTERNA, 09-08-2026): la lectura dinamica
#   que aqui decia "la densidad de fusion debe morir" esta REFUTADA
#   POR LA PROPIA TABLA: la densidad es monotona no decreciente (el
#   doblado vale en las seis series), phi(5x+1) >= 0,0044 y
#   phi(7x+1) >= 0,107, ambas subiendo -- y 7x+1 esta MENOS apagada
#   que 5x+1, al reves de lo que la historia supercritica predeciria.
#   LO DEFENDIBLE con los datos: las razones de b quedan por DEBAJO
#   de 2 para q >= 5 (1,65 en 7x+1 contra 1,89 en 3x+1 al mismo k) --
#   plausible phi_q < 1, como diferencia de grado MEDIDA, sin
#   mecanismo demostrado.
#
#   Control A/B doble: (1) barrido DIRECTO con pares de enteros contra
#   barrido SIMBOLICO de la cadena, por cada mapa; (2) el espejo
#   (3, -1) tiene que dar a(k) identica a (3, +1) (teorema espejoak).
#   Mapa del atajo, enteros exactos, SystemExit antes de concluir.

MAPAS = [(3, 1), (3, -1), (5, 1), (7, 1), (5, 3), (7, 3)]
K_DIRECTA = 14          # cruce directo vs simbolico hasta aqui
K_SIM = 22              # barrido simbolico hasta aqui (o el tope)
TOPE_ESTADOS = 3 * 10 ** 6

import math


def paso_q(x, q, r):
    return (q * x + r) // 2 if x % 2 else x // 2


def transicion_q(k, c, bit, q, r):
    if k == 0:
        if c % 2 == 0:
            return ('estado', 0, c // 2) if bit == 0 else ('estado', 0, q * c // 2)
        return ('estado', 1, (q * c + r) // 2) if bit == 0 \
            else ('estado', 1, (r - q * c) // 2)
    if c % 2 == 0:
        return ('estado', k, c // 2) if bit == 0 \
            else ('estado', k, (q * c + r * (1 - q ** k)) // 2)
    if bit == 0:
        return ('estado', k + 1, (q * c + r) // 2)
    if k >= 2:
        return ('estado', k - 1, (c - r * q ** (k - 1)) // 2)
    g = (c - r) // 2
    if g == 0:
        return ('fusion',)
    return ('estado', 0, abs(g))


# ---------------------------------------------------------------------------
# COMPROBACION 1: LAS LEYES CONTRA PARES REALES, por mapa.
#   Igual que la C1 de paseodeladeuda.py, con (q, r) generales.
# ---------------------------------------------------------------------------

for (q, r) in MAPAS:
    probadas = 0
    for k in range(0, 6):
        for c in range(1 if k == 0 else -40, 41):
            if k == 0 and c < 1:
                continue
            for v in range(200, 320):
                x = v
                y = (q ** k * v + c) if k >= 1 else v + c
                if y <= x:
                    continue
                nx, ny = paso_q(x, q, r), paso_q(y, q, r)
                t = transicion_q(k, c, v % 2, q, r)
                if t[0] == 'fusion':
                    if nx != ny:
                        raise SystemExit("C1 (%d,%d): fusion falsa k=%d c=%d v=%d"
                                         % (q, r, k, c, v))
                else:
                    _, k2, c2 = t
                    lo, hi = min(nx, ny), max(nx, ny)
                    objetivo = (q ** k2 * lo + c2) if k2 >= 1 else lo + c2
                    if hi != objetivo:
                        raise SystemExit("C1 (%d,%d): ley k=%d c=%d v=%d"
                                         % (q, r, k, c, v))
                probadas += 1
    print("COMPROBACION 1 OK (%dx%+d): las seis leyes exactas en %d instancias."
          % (q, r, probadas))

# ---------------------------------------------------------------------------
# COMPROBACION 2: DIRECTO CONTRA SIMBOLICO, y las series por mapa.
#   a_q(k) = clases r0 mod 2^k donde (r0, r0+1) se encuentran al mismo
#   indice con S igualada (el criterio de la casa). El simbolico tiene
#   que clavarlo nivel a nivel.
# ---------------------------------------------------------------------------

def a_directa_q(k, q, r):
    n = 0
    for r0 in range(2 ** k - 1):
        x, y = r0, r0 + 1
        Sx = Sy = 0
        for _ in range(k):
            if x % 2:
                Sx += 1
            if y % 2:
                Sy += 1
            x, y = paso_q(x, q, r), paso_q(y, q, r)
            if x == y:
                if Sx == Sy:
                    n += 1
                break
    return n


resultados = {}
for (q, r) in MAPAS:
    estados = {(0, 1): 1}
    absorbidas = 0
    a_sim = []
    corte = None
    for prof in range(1, K_SIM + 1):
        nuevo = {}
        nuevas_abs = 0
        for (k, c), n in estados.items():
            for bit in (0, 1):
                t = transicion_q(k, c, bit, q, r)
                if t[0] == 'fusion':
                    nuevas_abs += n
                else:
                    clave = (t[1], t[2])
                    nuevo[clave] = nuevo.get(clave, 0) + n
        absorbidas = 2 * absorbidas + nuevas_abs
        estados = nuevo
        a_sim.append(absorbidas)
        if len(estados) > TOPE_ESTADOS:
            corte = prof
            break
    for k in range(3, min(K_DIRECTA, len(a_sim)) + 1):
        d = a_directa_q(k, q, r)
        if a_sim[k - 1] != d:
            raise SystemExit("C2 (%d,%+d): a(%d) simbolico=%d, directo=%d"
                             % (q, r, k, a_sim[k - 1], d))
    resultados[(q, r)] = (a_sim, corte)
    print("COMPROBACION 2 OK (%dx%+d): simbolico = directo, k = 3..%d%s."
          % (q, r, min(K_DIRECTA, len(a_sim)),
             " (cortado en prof %d por tope de estados)" % corte if corte else ""))

# ---------------------------------------------------------------------------
# COMPROBACION 3: EL ESPEJO. a(k) de (3,-1) identica a la de (3,+1)
#   hasta donde los dos llegan (teorema espejoak, ahora por la cadena).
# ---------------------------------------------------------------------------

a_mas, _ = resultados[(3, 1)]
a_menos, _ = resultados[(3, -1)]
tope = min(len(a_mas), len(a_menos))
for i in range(tope):
    if a_mas[i] != a_menos[i]:
        raise SystemExit("C3 espejo: a(%d) difiere: %d vs %d"
                         % (i + 1, a_mas[i], a_menos[i]))
print("COMPROBACION 3 OK: el espejo 3x-1 clava a(k) identica, k = 1..%d"
      % tope)
print("(el teorema de espejoak, reproducido por la cadena generalizada).")

# ---------------------------------------------------------------------------
# LA TABLA: las densidades de fusion de la familia, POR PRIMERA VEZ.
# ---------------------------------------------------------------------------

print()
print("la criticidad, por mapa:")
print("   q    E[m] = (1+q)/4    E[log2 m] = (log2 q - 2)/2")
for q in (3, 5, 7):
    print("   %d       %6.4f            %+7.4f" % (q, (1 + q) / 4.0,
                                                   (math.log(q, 2) - 2) / 2))
print("E[m] = 1 EXACTO solo en q = 3: la criticidad de Tigresas")
print("caracteriza al 3 dentro de la familia (qx+r)/2.")

print()
print("las series a_q(k) y sus densidades:")
for (q, r) in MAPAS:
    a_sim, corte = resultados[(q, r)]
    kmax = len(a_sim)
    print()
    print("  mapa %dx%+d (hasta k = %d):" % (q, r, kmax))
    fila_a = [a_sim[k - 1] for k in range(3, min(kmax, 15) + 1)]
    print("    a(3..%d) = %s" % (min(kmax, 15), fila_a))
    print("    k    a(k)         b(k-1)     razon b    densidad a(k)/2^k")
    prev_a = prev_b = None
    for k in range(3, kmax + 1):
        a = a_sim[k - 1]
        b = a - 2 * prev_a if prev_a is not None else None
        razon = ("%7.4f" % (b / prev_b)) if b and prev_b else "       "
        if k >= kmax - 6 or k <= 6:
            print("   %2d  %11d  %10s  %s     %8.6f"
                  % (k, a, b if b is not None else "", razon, a / 2.0 ** k))
        prev_a, prev_b = a, (b if b else prev_b)

# ---------------------------------------------------------------------------
# COMPROBACION 4 -- EL TEOREMA DE LECHUZAS (rapaz: ve en la oscuridad
# que no hay nada; bautizado el 09-08-2026): si 3 | r, los pares
# consecutivos NO funden JAMAS **con S igualada** bajo (qx+r)/2
# (la fusion de la cadena; calificador exigido por la revision
# externa: el encuentro DESBALANCEADO cerca de los ciclos no queda
# excluido por esta prueba -- buscado hasta 20.000 sin hallazgos,
# pero no demostrado).
#   Demostracion de una linea: la fusion exige c = r, o sea c = 0
#   (mod 3); pero en las seis leyes el termino aditivo es multiplo de
#   r (luego de 3) y el multiplicativo es una unidad mod 3 (2 o su
#   inverso), asi que c mod 3 solo se multiplica por unidades: desde
#   c0 = 1 la clase 0 es INALCANZABLE. El barrido lo confirma:
#   a(k) = 0 identico, k = 3..22, en 5x+3 y 7x+3.
# ---------------------------------------------------------------------------

for (q, r) in MAPAS:
    if r % 3 == 0:
        a_sim, _ = resultados[(q, r)]
        if any(a_sim):
            raise SystemExit("C4 LECHUZAS: %dx%+d tiene fusion y 3 | r" % (q, r))
print()
print("COMPROBACION 4 OK -- LECHUZAS: con 3 | r la fusion de consecutivos")
print("es imposible (c = 0 mod 3 inalcanzable desde c = 1: las leyes solo")
print("multiplican c por unidades mod 3). El barrido da a(k) = 0 clavado.")

print()
print("VEREDICTO (medido + la linea exacta): la maquinaria entera de la")
print("fusion de consecutivos corre igual para todo (q, r) impar -- las")
print("seis leyes son las mismas con 3 -> q --, el espejo sale de la")
print("cadena, y las densidades de 5x+1 y 7x+1 quedan medidas por")
print("primera vez. La linea dura -- AGUILAS --: E[m] = (1+q)/4, o sea")
print("kappa = 1 (Tigresas) es EXCLUSIVO de q = 3. CORREGIDO POR LA")
print("REVISION EXTERNA: las densidades de q >= 5 NO mueren (son")
print("monotonas y positivas: 0,107 el 7x+1); lo que los datos orientan")
print("es que sus razones de b quedan bajo 2 (phi_q < 1 plausible), como")
print("diferencia de grado medida, sin mecanismo demostrado.")
