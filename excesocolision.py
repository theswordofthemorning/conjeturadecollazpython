# excesocolision.py
#
# PIRANAS (bautizado 12-08: se comen el exceso a razon ~0,7 por
# paso). EL EXCESO DE COLISION Y SU CONTRACCION GEOMETRICA (12-08-2026;
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
#
#   Capa 1: mapa = cadena (k, c) del atajo; medida de clases;
#   condicionado a vivo; m = 8 fijo y declarado; horizonte finito.

M_BITS = 12
T_MAXDP = 26
M8 = 8
E_FINAL_TOPE = 0.06
RAZON_TOPE = 0.85

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
    for t in range(T_MAXDP + 1):
        Q = 2 ** (M - t)
        vivos = sum(estados.values())
        pesos = {}
        for (k, cm), n in estados.items():
            r = cm % (2 ** M8)
            pesos[r] = pesos.get(r, 0) + n
        l2 = sum(p * p for p in pesos.values()) * (2 ** M8) \
            / float(vivos) ** 2
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
    return filas


print("EL EXCESO DE COLISION e_t = C2(t) - 1 Y SU CONTRACCION")
print("(el kernel de la renovacion del teorema de conteo; m = %d)" % M8)
print()
razones = {}
for c0, nombre in ARRANQUES:
    filas = dp_excesos(c0)
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
    print()

if abs(razones["ADV"] - razones["A"]) > 0.1:
    raise SystemExit("X3: el adversarial contrae distinto (%.3f vs %.3f)"
                     % (razones["ADV"], razones["A"]))
print("X1 OK (exceso final <= %.2f), X2 OK (contraccion geometrica" %
      E_FINAL_TOPE)
print("<= %.2f; medida ~0,7), X3 OK (el adversarial contrae igual" %
      RAZON_TOPE)
print("que A: %.3f vs %.3f)." % (razones["ADV"], razones["A"]))
print()
print("Lectura: la GANANCIA ESTRICTA que el telescopio critico del")
print("conteo necesita EXISTE y es geometrica (~0,7 por paso, uniforme")
print("en arranques, adversarial incluido). El teorema pendiente es")
print("demostrar rho < 1 para UNA transicion del DP. Medicion, no")
print("teorema.")
