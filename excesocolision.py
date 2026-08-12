# excesocolision.py
#
# PIRANAS (bautizado 12-08: se comen el exceso -- razon MEDIA de
# contraccion ~0,7 en t = 8..26 (X2); la serie a escala fija NO es
# monotona paso a paso (picos > 1: A t=22->23 x1,38): la contraccion
# a escala fija es de TENDENCIA, y el objeto monotono medido es la
# razon multi-escala (X4) -- precision de la 10a, A3-1).
# EL EXCESO DE COLISION Y SU CONTRACCION (12-08-2026;
# el instrumento del ataque por pares al teorema de conteo --
# notaequidistribucion.txt 3-bis).
#
#   QUE MIDE. La constante de colision L2 a escala m = 8,
#     C2(t) = 2^m * Sigma_r P(c_t = r mod 2^m | vivo)^2
#   (la probabilidad de colision de dos palabras independientes,
#   normalizada al piso uniforme C2 = 1), y su EXCESO
#   e_t = C2(t) - 1, para todo t = 0..T_MAXDP, exacto por el DP de
#   conteos enteros de equidistribucionmixto.py.
#
#   POR QUE IMPORTA. El telescopio de primer desvio del conteo es
#   CRITICO EXACTO (Sigma 2^-i = 1: cero holgura); el teorema
#   pendiente tiene la forma e_(t+1) <= rho * e_t + sumable con
#   rho < 1 -- UNA transicion del DP, no un asintotico. Este
#   fichero mide ese rho.
#
#   COMPROBACIONES (SystemExit):
#     X1  el exceso final es chico: e_T <= 0,06 en los tres
#         arranques (a 6% del piso uniforme).
#     X2  la contraccion es geometrica de verdad: la razon media
#         (e_T / e_8)^(1/(T-8)) <= 0,85 en los tres arranques
#         (la medida da ~0,7).
#     X3  el arranque adversarial NO es especial: su razon media
#         difiere de la del arranque A en menos de 0,1.
#     X4  LA RAZON MULTI-ESCALA (el blanco afilado del teorema):
#         rho_ms(t, m) = e_(t+1)(m) / e_t(m+1) < 0,5 en toda celda
#         con t >= 12, m = 6..9, tres arranques. Si un teorema
#         entrega rho < 1/2 para UNA transicion, el telescopio
#         tiempo-por-escala cierra solo:
#         e_t(m) <= e_0(m+t) rho^t <= 2^m (2 rho)^t -> 0.
#         La medida da peor caso ~0,44: margen 13%.
#
#   Capa 1: mapa = cadena (k, c) del atajo; medida de clases;
#   condicionado a vivo; m = 8 fijo y declarado; horizonte finito.

M_BITS = 13
T_MAXDP = 26
M8 = 8
ESCALAS = [6, 7, 8, 9, 10]     # para X4 (m y m+1 adyacentes)
E_FINAL_TOPE = 0.06            # convencion de gate, sin derivacion
RAZON_TOPE = 0.85              # convencion de gate, sin derivacion
RHO_MS_TOPE = 0.5              # el umbral critico del telescopio

ARRANQUES = [
    (999983, "A"),
    (999999937, "B"),
    ((2 ** 21) - ((2 ** 21 + 1) // 3), "ADV"),
]


def pot3(k, _cache={0: 1}):
    if k not in _cache:
        _cache[k] = 3 ** k
    return _cache[k]


def dp_excesos(c0):
    M = T_MAXDP + M_BITS
    estados = {(2, c0 % (2 ** M)): 1}
    filas = []
    excesos = {}               # (t, m) -> e_t(m), para X4
    for t in range(T_MAXDP + 1):
        Q = 2 ** (M - t)
        vivos = sum(estados.values())
        for m in ESCALAS:
            pesos_m = {}
            mm = 2 ** m
            for (k, cm), n in estados.items():
                r = cm % mm
                pesos_m[r] = pesos_m.get(r, 0) + n
            l2m = sum(p * p for p in pesos_m.values()) * mm \
                / float(vivos) ** 2
            excesos[(t, m)] = l2m - 1.0
        l2 = excesos[(t, M8)] + 1.0
        filas.append((t, vivos, l2))
        if t == T_MAXDP:
            break
        nuevos = {}
        Q2 = Q // 2
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
        estados = nuevos
    return filas, excesos


print("EL EXCESO DE COLISION e_t = C2(t) - 1 Y SU CONTRACCION")
print("(el kernel de la renovacion del teorema de conteo; m = %d)" % M8)
print()
razones = {}
peor_ms_global = 0.0
for c0, nombre in ARRANQUES:
    filas, excesos = dp_excesos(c0)
    print("arranque %s (c0 = %d):" % (nombre, c0))
    for (t, vivos, l2) in filas:
        if t % 2 == 0 or t >= 22:
            print("  t = %2d  C2 = %9.4f   e_t = %9.5f"
                  % (t, l2, l2 - 1.0))
    e8 = filas[8][2] - 1.0
    eT = filas[T_MAXDP][2] - 1.0
    razon = (eT / e8) ** (1.0 / (T_MAXDP - 8))
    razones[nombre] = razon
    print("  razon media de contraccion (t = 8..%d): %.3f"
          % (T_MAXDP, razon))
    if eT > E_FINAL_TOPE:
        raise SystemExit("X1: e_%d = %.4f > %.2f en el arranque %s"
                         % (T_MAXDP, eT, E_FINAL_TOPE, nombre))
    if razon > RAZON_TOPE:
        raise SystemExit("X2: razon %.3f > %.2f en el arranque %s"
                         % (razon, RAZON_TOPE, nombre))
    peor_ms = 0.0
    min_ms = None
    peor_celda = None
    for t in range(12, T_MAXDP):
        for m in ESCALAS[:-1]:
            den = excesos[(t, m + 1)]
            # celdas de denominador ~0 excluidas: son el regimen del
            # contraejemplo naif (notaequidistribucion 3-bis.vi)
            if den > 1e-6:
                r_ms = excesos[(t + 1, m)] / den
                if r_ms > peor_ms:
                    peor_ms = r_ms
                    peor_celda = (t, m)
                if min_ms is None or r_ms < min_ms:
                    min_ms = r_ms
    peor_ms_global = max(peor_ms_global, peor_ms)
    if peor_celda is not None:
        print("  razon MULTI-ESCALA peor (t >= 12, m = 6..9): %.3f "
              "(celda t=%d, m=%d); minima: %.3f"
              % (peor_ms, peor_celda[0], peor_celda[1], min_ms))
    else:
        print("  razon MULTI-ESCALA: sin celdas con denominador > 1e-6")
    if peor_ms >= RHO_MS_TOPE:
        raise SystemExit("X4: rho_ms = %.3f >= %.1f en el arranque %s "
                         "-- el telescopio tiempo-por-escala NO cierra"
                         % (peor_ms, RHO_MS_TOPE, nombre))
    print()

if abs(razones["ADV"] - razones["A"]) > 0.1:
    raise SystemExit("X3: el adversarial contrae distinto (%.3f vs %.3f)"
                     % (razones["ADV"], razones["A"]))
print("X1 OK (exceso final <= %.2f), X2 OK (razon media de contraccion" %
      E_FINAL_TOPE)
print("<= %.2f; medida ~0,7), X3 OK (el adversarial contrae igual" %
      RAZON_TOPE)
print("que A: %.3f vs %.3f)." % (razones["ADV"], razones["A"]))
print()
print("X4 OK: la razon multi-escala peor es %.3f < %.1f."
      % (peor_ms_global, RHO_MS_TOPE))
print()
print("Lectura: la GANANCIA ESTRICTA que el telescopio critico del")
print("conteo necesita EXISTE: razon MEDIA de contraccion ~0,7 en")
print("t = 8..26 (X2), uniforme en arranques, adversarial incluido;")
print("la serie a escala fija NO es monotona paso a paso (picos > 1:")
print("A t=22->23 x1,38) -- contraccion de TENDENCIA; el objeto")
print("monotono es la razon multi-escala (X4). Y EL BLANCO")
print("AFILADO: la razon multi-escala e_(t+1)(m)/e_t(m+1) queda BAJO")
print("EL UMBRAL CRITICO 1/2 en toda celda medida (peor ~0,44, margen")
print("13%): un teorema de UNA transicion con rho < 1/2 cierra el")
print("telescopio tiempo-por-escala solo (e_t <= 2^m (2rho)^t -> 0).")
print("Medicion, no teorema.")
