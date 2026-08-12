# corrienteszocalo.py
#
# LAS CORRIENTES DEL ZOCALO (12-08-2026, etapa 1 del ataque al
# teorema de conteo -- la descomposicion de la recursion de un paso
# de BALLENAS por corrientes de entrada, medida exacta).
#
#   LA IDEA. La fibra hija (k', t+1) recibe masa por CUATRO
#   corrientes, cada una UN mapa afin de un subconjunto de padres:
#     N0  compartido bit 0:  (k', c par)   -> c/2
#     N1  recarga (bit 1):   (k', c par)   -> (3c + 1 - 3^k')/2
#     A   ascenso (mixto 0): (k'-1, c impar) -> (3c + 1)/2
#     D   descenso (mixto 1): (k'+1, c impar) -> (c - 3^k')/2
#   Dentro de la fibra hija, a escala m, la ley es la mezcla
#   p = Sigma_i w_i p_i, y la colision se descompone EXACTA:
#     e_hija(m) = Sigma_i w_i^2 E_ii + Sigma_(i!=j) w_i w_j E_ij
#   con E_ij = 2^m Sigma_r p_i(r) p_j(r) - 1 (el exceso cruzado
#   sobre el piso). DOS mecanismos posibles de la contraccion:
#     (a) ESTRUCTURAL: si las cruzadas E_ij ~ 0 (corrientes
#         decorrelacionadas), e_hija ~ (Sigma_i w_i^2) * E_tipico,
#         y Sigma w_i^2 < 1/2 en cuanto hay dos corrientes
#         comparables -- el 1/2 del telescopio saldria del
#         BRANCHING, no de una estimacion fina;
#     (b) si las cruzadas NO son ~0, el mecanismo es otro y esto
#         es un negativo que registrar.
#   Y LA ESCALA: cada corriente es un mapa afin de coeficiente
#   impar sobre la mitad par/impar del padre -- por la biyeccion de
#   VIBORAS/LORAS, la colision de la corriente a escala m ES la del
#   subconjunto padre a escala m+1: E_ii(m) ya es el objeto padre
#   en la escala fina (comprobado exacto en S2).
#
#   COMPROBACIONES (SystemExit -- solo las identidades exactas; las
#   hipotesis (a)/(b) se MIDEN, no se exigen):
#     S1  la suma de corrientes reproduce el DP: los conteos de la
#         fibra hija reconstruidos = los del paso siguiente del DP,
#         estado a estado, en enteros.
#     S2  la biyeccion por corriente: la colision de N0 y la de N1
#         a escala m son AMBAS iguales a la colision del
#         subconjunto par del padre a escala m+1 (enteros); idem
#         A y D contra los impares de su padre.
#     S3  la identidad de mezcla: 2^m Sigma n_hija(r)^2 =
#         Sigma_ij Sigma_r n_i(r) n_j(r) * 2^m, en enteros.
#     S4  conservacion de masa por fibra.
#
#   Capa 1: mapa = la cadena (k, c) del atajo (mismas leyes que
#   equidistribucionmixto/conteoconjunto); MEDICION exacta a
#   horizonte finito, no teorema; transiciones y escalas
#   declaradas; arranques primos no redondos + adversarial; el
#   foco es el ZOCALO k' <= 5 (donde vive ~80% del exceso).

M_BITS = 12
T_MAXDP = 25
TRANSICIONES = [16, 20, 24]      # t -> t+1
M_FOCO = 8                       # la escala de la tabla
M_BARRIDO = range(6, 11)         # el barrido del veredicto
K_ZOCALO = 5                     # tabla por fibra hasta aqui

INV3_NEG_2_21 = (2 ** 21) - ((2 ** 21 + 1) // 3)
ARRANQUES = [
    (999983, "A (el de rachasreales)"),
    (999999937, "B (el de medianareal)"),
    (INV3_NEG_2_21, "ADV (-3^(-1) mod 2^21)"),
]


def pot3(k, _cache={0: 1}):
    if k not in _cache:
        _cache[k] = 3 ** k
    return _cache[k]


def dp_correr(c0):
    M = T_MAXDP + M_BITS
    estados = {(2, c0 % (2 ** M)): 1}
    absorbidos = 0
    historia = {}
    for t in range(T_MAXDP + 1):
        historia[t] = (estados, absorbidos)
        if t == T_MAXDP:
            break
        Q = 2 ** (M - t)
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


def descomponer(estados_t, t):
    # un paso del DP, con cada conteo etiquetado por corriente:
    # devuelve dict[(k_hija, corriente)][x_hija] = conteo entero
    M = T_MAXDP + M_BITS
    Q = 2 ** (M - t)
    Q2 = Q // 2
    llegadas = {}
    for (k, cm), n in estados_t.items():
        if cm % 2 == 0:
            destinos = [((k, 'N0'), (cm // 2) % Q2),
                        ((k, 'N1'), (((3 * cm + 1 - pot3(k)) % Q) // 2)
                         % Q2)]
        else:
            destinos = [((k + 1, 'A'), (((3 * cm + 1) % Q) // 2) % Q2)]
            if k >= 3:
                destinos.append(
                    ((k - 1, 'D'), (((cm - pot3(k - 1)) % Q) // 2) % Q2))
        for (clave, x) in destinos:
            d = llegadas.setdefault(clave, {})
            d[x] = d.get(x, 0) + n
    return llegadas


def colision_subconjunto(estados, k, paridad, escala):
    # colision entera del subconjunto de la fibra k con esa paridad,
    # a la escala dada: Sigma_clase n(clase)^2 (para S2)
    pesos = {}
    for (kk, cm), n in estados.items():
        if kk == k and cm % 2 == paridad:
            r = cm % (2 ** escala)
            pesos[r] = pesos.get(r, 0) + n
    return sum(v * v for v in pesos.values()), sum(pesos.values())


print("LAS CORRIENTES DEL ZOCALO -- la recursion de BALLENAS abierta")
print("por corrientes de entrada (N0/N1/A/D), exacta en enteros")
print("transiciones t -> t+1 en %s; tabla a m = %d; barrido m = %d..%d"
      % (TRANSICIONES, M_FOCO, min(M_BARRIDO), max(M_BARRIDO)))
print()

CORRIENTES = ['N0', 'N1', 'A', 'D']
peor_cruce_global = 0.0
peor_sw2_global = 0.0
for c0, nombre in ARRANQUES:
    print("=== arranque %s ===" % nombre)
    historia = dp_correr(c0)
    for t in TRANSICIONES:
        estados_t, _ = historia[t]
        estados_t1, _ = historia[t + 1]
        llegadas = descomponer(estados_t, t)
        # S1: reconstruir el DP del paso siguiente
        reconstruido = {}
        for (k, cor), d in llegadas.items():
            for x, n in d.items():
                clave = (k, x)
                reconstruido[clave] = reconstruido.get(clave, 0) + n
        if reconstruido != dict(estados_t1):
            raise SystemExit("S1: la suma de corrientes NO reproduce "
                             "el DP en t = %d" % t)
        # las fibras hijas del zocalo, a escala M_FOCO
        fibras = sorted(set(k for (k, _c) in llegadas.keys()))
        print("  t = %d -> %d   (m = %d)" % (t, t + 1, M_FOCO))
        print("   k'   masa    w:N0/N1/A/D          Sw2    "
              "E_ii(max)  E_cruz(max)  e_hija   rho_efec")
        for k in fibras:
            if k > K_ZOCALO:
                continue
            m = M_FOCO
            # conteos por corriente a escala m
            porcor = {}
            masas = {}
            for cor in CORRIENTES:
                d = llegadas.get((k, cor), {})
                red = {}
                for x, n in d.items():
                    r = x % (2 ** m)
                    red[r] = red.get(r, 0) + n
                porcor[cor] = red
                masas[cor] = sum(red.values())
            masa = sum(masas.values())
            if masa == 0:
                continue
            # S4 + S2 (biyeccion): N0 y N1 contra el padre par de k;
            # A contra el impar de k-1; D contra el impar de k+1
            col_par, masa_par = colision_subconjunto(
                estados_t, k, 0, m + 1)
            for cor in ('N0', 'N1'):
                col_c = sum(v * v for v in porcor[cor].values())
                if masas[cor] != masa_par or col_c != col_par:
                    raise SystemExit(
                        "S2: corriente %s de k'=%d no biyecta con el "
                        "padre par (t=%d): %d/%d vs %d/%d"
                        % (cor, k, t, masas[cor], col_c, masa_par,
                           col_par))
            col_A, masa_A = colision_subconjunto(
                estados_t, k - 1, 1, m + 1)
            col_c = sum(v * v for v in porcor['A'].values())
            if masas['A'] != masa_A or col_c != col_A:
                raise SystemExit("S2: corriente A de k'=%d (t=%d)"
                                 % (k, t))
            col_D, masa_D = colision_subconjunto(
                estados_t, k + 1, 1, m + 1)
            col_c = sum(v * v for v in porcor['D'].values())
            if masas['D'] != masa_D or col_c != col_D:
                raise SystemExit("S2: corriente D de k'=%d (t=%d)"
                                 % (k, t))
            # la identidad de mezcla S3 y la descomposicion
            hija = {}
            for cor in CORRIENTES:
                for r, n in porcor[cor].items():
                    hija[r] = hija.get(r, 0) + n
            col_hija = sum(v * v for v in hija.values())
            suma_ij = 0
            E = {}
            for i in CORRIENTES:
                for j in CORRIENTES:
                    s = 0
                    pi, pj = porcor[i], porcor[j]
                    if len(pj) < len(pi):
                        pi, pj = pj, pi
                    for r, n in pi.items():
                        if r in pj:
                            s += n * pj[r]
                    suma_ij += s
                    if masas[i] and masas[j]:
                        E[(i, j)] = ((2 ** m) * s
                                     / float(masas[i] * masas[j]) - 1)
            if suma_ij != col_hija:
                raise SystemExit("S3: la mezcla no cierra en k'=%d "
                                 "t=%d" % (k, t))
            w = {c: masas[c] / float(masa) for c in CORRIENTES}
            sw2 = sum(v * v for v in w.values())
            e_hija = (2 ** m) * col_hija / float(masa) ** 2 - 1
            e_ii_max = max((E.get((c, c), 0.0) for c in CORRIENTES
                            if masas[c]), default=0.0)
            e_cruz_max = max((abs(E[(i, j)]) for i in CORRIENTES
                              for j in CORRIENTES if i != j
                              and (i, j) in E), default=0.0)
            rho_efec = (e_hija / e_ii_max) if e_ii_max > 1e-9 else 0.0
            print("   %2d %7d  %.2f/%.2f/%.2f/%.2f   %.3f   "
                  "%8.3f   %8.3f   %6.3f   %6.3f"
                  % (k, masa, w['N0'], w['N1'], w['A'], w['D'], sw2,
                     e_ii_max, e_cruz_max, e_hija, rho_efec))
            if t == TRANSICIONES[-1]:
                peor_sw2_global = max(peor_sw2_global, sw2)
        print()
    # el barrido del veredicto: cruzadas relativas en el zocalo
    t = TRANSICIONES[-1]
    estados_t, _ = historia[t]
    llegadas = descomponer(estados_t, t)
    peor_rel = 0.0
    peor_txt = ""
    for k in range(2, K_ZOCALO + 1):
        for m in M_BARRIDO:
            porcor = {}
            masas = {}
            for cor in CORRIENTES:
                d = llegadas.get((k, cor), {})
                red = {}
                for x, n in d.items():
                    r = x % (2 ** m)
                    red[r] = red.get(r, 0) + n
                porcor[cor] = red
                masas[cor] = sum(red.values())
            e_ii = {}
            for cor in CORRIENTES:
                if masas[cor]:
                    col = sum(v * v for v in porcor[cor].values())
                    e_ii[cor] = (2 ** m) * col / float(
                        masas[cor]) ** 2 - 1
            tope = max(e_ii.values()) if e_ii else 0.0
            if tope <= 1e-6:
                continue
            for i in CORRIENTES:
                for j in CORRIENTES:
                    if i >= j or not masas[i] or not masas[j]:
                        continue
                    s = 0
                    pi, pj = porcor[i], porcor[j]
                    if len(pj) < len(pi):
                        pi, pj = pj, pi
                    for r, n in pi.items():
                        if r in pj:
                            s += n * pj[r]
                    e_ij = (2 ** m) * s / float(
                        masas[i] * masas[j]) - 1
                    rel = abs(e_ij) / tope
                    if rel > peor_rel:
                        peor_rel = rel
                        peor_txt = "k'=%d m=%d %s-%s" % (k, m, i, j)
    print("  cruzadas del zocalo (t = %d, m = %d..%d): peor "
          "|E_cruz|/E_ii = %.3f (%s)"
          % (t, min(M_BARRIDO), max(M_BARRIDO), peor_rel, peor_txt))
    peor_cruce_global = max(peor_cruce_global, peor_rel)
    print()

print("Lectura:")
print("S1-S4 OK: la descomposicion es exacta (enteros), la biyeccion")
print("VIBORAS/LORAS por corriente COMPROBADA (E_ii a escala m ES el")
print("padre a escala m+1), y la mezcla cierra.")
print("El dato del mecanismo: peor cruzada relativa del zocalo =")
print("%.3f; peor Sigma w^2 en t = %d: %.3f."
      % (peor_cruce_global, TRANSICIONES[-1], peor_sw2_global))
print("Si la cruzada es chica y Sigma w^2 < 1/2, el mecanismo del")
print("teorema es BRANCHING + DECORRELACION ENTRE CORRIENTES; si no,")
print("es un negativo que registrar. MEDICION, no teorema.")
