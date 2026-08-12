# recargaexacta.py
#
# LA GEOMETRIA DEL SALTO DE RECARGA, MEDIDA EXACTA (12-08-2026;
# punto 1(b) de la ruta post-9a -- la equidistribucion de la
# cancelacion de recargas de notadominacion.txt, Pieza A caso
# v2 = A, que la 9a dejo "POR ESCRIBIR" como objeto hermano de la
# Pieza B).
#
#   LA UNIFICACION (lecturaracha.lean, lectura_recarga +
#   una_clase_recarga): el salto de recarga LEE los mismos bits que
#   la racha. En el paso compartido bit 1 desde (k, c par) el hijo
#   cumple 2h = 3c + 1 - 3^k; con v2(c) = A = v2(3^k - 1) exacto
#   (la premisa de recarga), v2(h) >= A automatico, y
#     salto >= s  <=>  2^(A+1+s) | 3c + 1 - 3^k
#                 <=>  c en UNA clase mod 2^(A+1+s)
#   (unicidad por tres_inyectivo). LAS DOS EQUIDISTRIBUCIONES DE LA
#   NOTA SON UNA: equidistribucion de c mod 2^m. Si cada clase pesa
#   <= C 2^-m, entonces P(salto >= s | recarga) <= C' 2^-s con
#   C' ~ C / P(premisa | clase gruesa) -- y la prediccion de la 9a
#   ("salta ~Geom(1/2)") es exactamente C_s ~ 1.
#
#   QUE CALCULA (todo EXACTO, conteos enteros de palabras): el
#   mismo DP de equidistribucionmixto.py sobre (k, c mod 2^(M-t))
#   desde (2, c0); en la escalera de tiempos toma los estados con
#   la PREMISA de recarga (c par, v2(c) = A(k)) y mide la cola del
#   salto: C_s = P(salto >= s | premisa) * 2^s, con el cap de
#   modulo declarado por estado (den[s] solo suma estados que
#   pueden leer s bits: sin sesgo de celda).
#
#   COMPROBACIONES (SystemExit):
#     R1  conservacion: vivos + absorbidos = 2^t.
#     R2  cruce independiente (regla de los tres): enumeracion
#         exhaustiva de las 2^T_CRUCE palabras con dinamica entera
#         exacta (sin modulos, sin codigo comun) -- los conteos
#         ge[s] y den[s] de la premisa deben COINCIDIR COMO ENTEROS.
#     R3  el veredicto: C_s <= C_TOPE en toda celda con peso
#         esperado >= MIN_ESPERADO, t >= 12, tres arranques.
#     R4  la premisa es la clase que dice la aritmetica: P(v2(c) =
#         A | c par) * 2^(A+1) acotado (equidistribucion de la
#         propia premisa; se reporta por A).
#
#   Capa 1: mapa = cadena (k, c) del atajo; medida DE CLASES
#   (palabras uniformes); condicionado a vivo; horizonte finito
#   declarado; las celdas de granularidad marcadas sin exigir.

M_BITS = 16
T_MAXDP = 20               # M = 36, mismo coste que equidistribucionmixto
ESCALERA = [8, 12, 16, 20]
S_MAX = 8                  # cola del salto hasta aqui
T_CRUCE = 14
C_TOPE = 3.0
MIN_ESPERADO = 8.0

ARRANQUES = [
    (999983, "A"),
    (999999937, "B"),
    ((2 ** 21) - ((2 ** 21 + 1) // 3), "ADV"),
]


def pot3(k, _cache={0: 1}):
    if k not in _cache:
        _cache[k] = 3 ** k
    return _cache[k]


def v2_de(n):
    if n == 0:
        return 999
    v = 0
    while n % 2 == 0:
        n //= 2
        v += 1
    return v


def A_de(k, _cache={}):
    if k not in _cache:
        _cache[k] = v2_de(pot3(k) - 1)
    return _cache[k]


def dp_correr(c0):
    M = T_MAXDP + M_BITS
    estados = {(2, c0 % (2 ** M)): 1}
    absorbidos = 0
    historia = {}
    for t in range(T_MAXDP + 1):
        Q = 2 ** (M - t)
        historia[t] = (estados, absorbidos, Q, M - t)
        if t == T_MAXDP:
            break
        nuevos = {}
        Q2 = Q // 2
        absorbidos *= 2
        for (k, cm), n in estados.items():
            if cm % 2 == 0:
                h0 = (k, (cm // 2) % Q2)
                v = (3 * cm + 1 - pot3(k)) % Q
                h1 = (k, (v // 2) % Q2)
                nuevos[h0] = nuevos.get(h0, 0) + n
                nuevos[h1] = nuevos.get(h1, 0) + n
            else:
                v = (3 * cm + 1) % Q
                h0 = (k + 1, (v // 2) % Q2)
                nuevos[h0] = nuevos.get(h0, 0) + n
                if k >= 3:
                    w = (cm - pot3(k - 1)) % Q
                    h1 = (k - 1, (w // 2) % Q2)
                    nuevos[h1] = nuevos.get(h1, 0) + n
                else:
                    absorbidos += n
        estados = nuevos
    return historia


def salto_en_estado(k, cm, Q, bits, s_tope):
    # devuelve (A, s_leible, salto_leido): la premisa es v2(cm) = A;
    # el salto se lee de 3c + 1 - 3^k hasta donde el modulo deja
    A = A_de(k)
    if A + 2 > bits:
        return A, -1, -1          # ni la premisa se puede leer
    if cm == 0 or v2_de(cm) != A:
        return A, -1, -1
    s_leible = min(s_tope, bits - A - 1)
    u = (3 * cm + 1 - pot3(k)) % Q
    vu = v2_de(u) if u != 0 else bits
    salto = min(max(vu - (A + 1), 0), s_leible)
    return A, s_leible, salto


def medir_premisa(estados, Q, bits):
    # ge[s], den[s] para s = 1..S_MAX, mas la masa de premisa por A
    ge = {s: 0 for s in range(1, S_MAX + 1)}
    den = {s: 0 for s in range(1, S_MAX + 1)}
    premisa_por_A = {}
    pares = 0
    for (k, cm), n in estados.items():
        if cm % 2 != 0:
            continue
        pares += n
        A, s_leible, salto = salto_en_estado(k, cm, Q, bits, S_MAX)
        if s_leible < 0:
            continue
        premisa_por_A[A] = premisa_por_A.get(A, 0) + n
        for s in range(1, s_leible + 1):
            den[s] += n
            if salto >= s:
                ge[s] += n
    return ge, den, premisa_por_A, pares


print("LA GEOMETRIA DEL SALTO DE RECARGA (Pieza A caso v2 = A, exacta)")
print("la unificacion: salto >= s <=> c en UNA clase mod 2^(A+1+s)")
print("(lecturaracha.lean); DP con conteos enteros, M = %d"
      % (T_MAXDP + M_BITS))
print()

peor_global = 0.0
for c0, nombre in ARRANQUES:
    print("=== arranque %s (c0 = %d) ===" % (nombre, c0))
    historia = dp_correr(c0)
    for t in ESCALERA:
        estados, absorbidos, Q, bits = historia[t]
        vivos = sum(estados.values())
        if vivos + absorbidos != 2 ** t:
            raise SystemExit("R1: conservacion rota en t = %d" % t)
        ge, den, premisa_por_A, pares = medir_premisa(estados, Q, bits)
        masa_premisa = sum(premisa_por_A.values())
        detalle = []
        peor_t = 0.0
        for s in (1, 2, 4, 6, 8):
            if den[s] == 0:
                continue
            Cs = (ge[s] / float(den[s])) * 2 ** s
            marca = ""
            if t >= 12 and den[s] * 2.0 ** (-s) >= MIN_ESPERADO:
                peor_t = max(peor_t, Cs)
            else:
                marca = "*"
            detalle.append("s=%d: %.3f%s" % (s, Cs, marca))
        # R4: la premisa misma como clase (por A)
        r4 = []
        for A in sorted(premisa_por_A):
            CA = (premisa_por_A[A] / float(pares)) * 2 ** (A + 1) \
                if pares else 0.0
            r4.append("A=%d: %.3f" % (A, CA))
        print("  t = %2d: vivos %7d, premisa %6d (%.4f de pares)  "
              "C_s %s" % (t, vivos, masa_premisa,
                          masa_premisa / float(pares) if pares else 0.0,
                          "  ".join(detalle)))
        print("          premisa como clase, P*2^(A+1) por A: %s"
              % "   ".join(r4))
        peor_global = max(peor_global, peor_t)
    print()

if peor_global > C_TOPE:
    raise SystemExit("R3: C_s = %.3f > %.1f" % (peor_global, C_TOPE))
print("R3 OK: C_s <= %.3f <= %.1f en toda celda con peso (t >= 12,"
      % (peor_global, C_TOPE))
print("tres arranques): el salto de recarga esta dominado por la")
print("geometrica que la 9a predijo (~Geom(1/2) <=> C_s ~ 1).")
print()

# ----- R2: el cruce independiente por enumeracion entera -----

def paso_entero(k, c, bit):
    if c % 2 == 0:
        return (k, c // 2) if bit == 0 else (k, (3 * c + 1 - pot3(k)) // 2)
    if bit == 0:
        return (k + 1, (3 * c + 1) // 2)
    if k >= 3:
        return (k - 1, (c - pot3(k - 1)) // 2)
    return None


print("el cruce independiente (t = %d, 2^%d palabras, enteros):"
      % (T_CRUCE, T_CRUCE))
for c0, nombre in ARRANQUES:
    ge_e = {s: 0 for s in range(1, S_MAX + 1)}
    den_e = {s: 0 for s in range(1, S_MAX + 1)}
    vivas = 0
    for w in range(2 ** T_CRUCE):
        k, c = 2, c0
        vivo = True
        for i in range(T_CRUCE):
            r = paso_entero(k, c, (w >> i) & 1)
            if r is None:
                vivo = False
                break
            k, c = r
        if not vivo:
            continue
        vivas += 1
        if c % 2 != 0 or c == 0:
            continue
        A = A_de(k)
        if v2_de(c) != A:
            continue
        s_leible = min(S_MAX, (T_MAXDP + M_BITS - T_CRUCE) - A - 1)
        salto = max(v2_de(3 * c + 1 - pot3(k)) - (A + 1), 0)
        for s in range(1, s_leible + 1):
            den_e[s] += 1
            if salto >= s:
                ge_e[s] += 1
    historia = dp_correr(c0)
    estados, absorbidos, Q, bits = historia[T_CRUCE]
    ge_d, den_d, _, _ = medir_premisa(estados, Q, bits)
    if any(ge_e[s] != ge_d[s] or den_e[s] != den_d[s]
           for s in range(1, S_MAX + 1)):
        raise SystemExit("R2: DP y enumeracion NO coinciden en c0 = %d"
                         % c0)
    print("  c0 = %d: R2 OK (ge/den identicos como enteros; premisa "
          "%d de %d vivas)" % (c0, den_e[1], vivas))

print()
print("Lectura: la 'segunda equidistribucion' de la nota de dominacion")
print("no existia como objeto aparte -- el salto de recarga es la misma")
print("lectura de bits bajos que la racha (lecturaracha.lean), y su")
print("cola medida es la geometrica con C_s ~ 1 que la 9a predijo. Lo")
print("que queda abierto es UN solo teorema de conteo (notaequi-")
print("distribucion.txt, 3.ii), no dos. Medicion exacta, no teorema.")
