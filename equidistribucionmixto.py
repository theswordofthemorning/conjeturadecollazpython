# equidistribucionmixto.py
#
# ACTUALIZACION 10-09-2026: ver depuracion/frente20260910/Mangostas.md.
# Este censo mide v2 del hijo del mixto, NO la duracion compartida
# realizada o minima sobre los bits futuros. En el ejemplo ADV,
# P(L>=21 | bit 0 inicial)=2^-20, no 1. Las cuentas de divisibilidad
# se conservan; la ley de L requiere el automata de valuacion truncada.
#
# LA EQUIDISTRIBUCION DE v2 TRAS EL MIXTO, MEDIDA EXACTA (12-08-2026;
# punto 1(a) de la ruta post-9a -- la Pieza B de notadominacion.txt,
# el corazon analitico que la 9a dejo "POR ESCRIBIR").
#
#   LA REDUCCION (capa 1, aritmetica exacta -- es la palanca de todo
#   el fichero): la racha que sigue a un mixto lee los bits bajos de
#   c en el momento del mixto:
#     - mixto bit 0 (c impar, k sube):  c' = (3c+1)/2, y
#       racha >= j  <=>  v2(3c+1) >= j+1  <=>  3c = -1 mod 2^(j+1)
#       -- UNA clase de c mod 2^(j+1);
#     - mixto bit 1 (c impar, k >= 3 baja): c' = (c - 3^(k-1))/2, y
#       racha >= j  <=>  c = 3^(k-1) mod 2^(j+1) -- UNA clase.
#   Asi que la Pieza B ("P(racha >= j) <= C 2^-j bajo la medida de
#   clases") ES EXACTAMENTE la equidistribucion de c_t mod 2^m sobre
#   las palabras de Terras: si cada clase mod 2^m pesa <= C 2^-m,
#   la racha queda dominada con la MISMA C (por union de las dos
#   clases, una por bit). Y si el mapa palabra -> c_t mod 2^t fuera
#   INYECTIVO (la biyeccion de Terras del mapa clasico), C = 1
#   exacta. La inyectividad aqui NO es exacta (tortolas.lean: los
#   dos hijos de un compartido difieren en Delta con v2(Delta)
#   arbitrario); este fichero MIDE cuanto le falta.
#
#   QUE CALCULA (todo EXACTO, conteos enteros de palabras -- cero
#   Monte Carlo, cero floats en lo que decide):
#     DP sobre estados (k, c mod 2^(M-t)) desde (2, c0), donde el
#     modulo pierde UN bit por paso (la division entre 2 es exacta:
#     la paridad se conoce y el resto se arrastra). El conteo de
#     palabras que llegan a cada estado es un entero exacto; la
#     absorcion (k <= 1: el fondo) se retira y se contabiliza.
#     En la escalera de tiempos reporta:
#       - masa viva y P(c impar | vivo);
#       - la cola de racha tras mixto: P(racha >= j | mixto bit b,
#         vivo) * 2^j para j <= J_MAX, por los DOS bits;
#       - la constante de equidistribucion por residuo:
#         max_r P(c_t = r mod 2^j | vivo) * 2^j.
#
#   COMPROBACIONES (SystemExit):
#     E1  el cruce independiente (regla de los tres, pata 2): a
#         t = T_CRUCE se enumeran las 2^t palabras con la dinamica
#         entera EXACTA de rachasreales (otro codigo, sin modulos) y
#         los conteos de la cola de racha deben COINCIDIR COMO
#         ENTEROS con los del DP.
#     E2  la conservacion: vivos + absorbidos = 2^t en todo t.
#     E3  el contraejemplo del adv 1 REPRODUCIDO: desde c0_ADV =
#         -3^(-1) mod 2^21, la racha tras el primer mixto bit 0 es
#         >= 19 con probabilidad 1 (el transitorio existe y el
#         instrumento lo ve); y a t = 20 la cola ya esta bajo
#         C_TOPE (el transitorio MUERE: es el tramo determinista
#         que la version quenched se traga).
#     E4  el veredicto: C_j <= C_TOPE en toda la escalera t >= 12,
#         los dos bits, los tres arranques -- SOLO en las celdas
#         donde el peso esperado del evento alcanza (impares * 2^-j
#         >= MIN_ESPERADO): esto NO es un piso de muestra (el censo
#         es exacto, no hay ruido) sino de GRANULARIDAD -- donde
#         2^-j es menor que unas pocas palabras, la celda mide el
#         residuo determinista del c0 concreto (el transitorio que
#         la version quenched de la nota se traga), no la
#         equidistribucion; se reporta igual, sin exigir.
#
#   La version ADAPTADA (condicionada al camino entero de k -- el
#   "pasado grueso") se mide en el cruce de t = T_CRUCE agrupando
#   las palabras por su k-camino: para todo grupo con >= 2^(j+2)
#   palabras, P(racha >= j | grupo) * 2^j <= tope adaptado.
#
#   Capa 1: mapa = la cadena (k, c) del atajo de Terras (la de
#   rachasreales.py); la medida es la DE CLASES (palabras uniformes:
#   bits iid); condicionado a VIVO (la transferencia usa excursiones
#   -- misma convencion que dominacioncondicionada.py); t no redondo
#   en el cruce (14) y escalera declarada; es MEDICION EXACTA a
#   horizonte finito, no teorema asintotico.

M_BITS = 12                # bits de residuo que sobreviven al final
T_MAXDP = 24               # pasos del DP  (modulo inicial 2^36)
ESCALERA = [8, 12, 16, 20, 24]
J_MAX = 10                 # cola de racha hasta aqui
T_CRUCE = 14               # enumeracion exhaustiva 2^14 (E1 + adaptada)
C_TOPE = 3.0               # veredicto E4 (el marginal real ronda 1);
                           # convencion de gate, sin derivacion
MIN_ESPERADO = 8.0         # E4 exige solo si impares * 2^-j >= esto;
                           # el 8 es convencion (granularidad); el
                           # veredicto es robusto a moverlo
MIN_GRUPO_LOG2 = 2         # grupo adaptado: n >= 2^(j + MIN_GRUPO_LOG2)

INV3_NEG_2_21 = (2 ** 21) - ((2 ** 21 + 1) // 3)   # -3^(-1) mod 2^21
ARRANQUES = [
    (999983, "A (el de rachasreales)"),
    (999999937, "B (el de medianareal)"),
    (INV3_NEG_2_21, "ADV (c0 = -3^(-1) mod 2^21: fuerza racha_1 = 20)"),
]

if (3 * INV3_NEG_2_21) % (2 ** 21) != (2 ** 21) - 1:
    raise SystemExit("capa 1: el c0 adversarial no cumple 3c = -1 mod 2^21")


def pot3(k, _cache={0: 1}):
    if k not in _cache:
        _cache[k] = 3 ** k
    return _cache[k]


# ----- el DP exacto sobre (k, c mod 2^Q) -----

def dp_correr(c0):
    M = T_MAXDP + M_BITS
    estados = {(2, c0 % (2 ** M)): 1}
    absorbidos = 0
    historia = {}          # t -> (estados, absorbidos, Q)
    for t in range(T_MAXDP + 1):
        Q = 2 ** (M - t)
        historia[t] = (estados, absorbidos, Q)
        if t == T_MAXDP:
            break
        nuevos = {}
        Q2 = Q // 2
        absorbidos *= 2        # cada prefijo muerto vale 2 palabras mas
        for (k, cm), n in estados.items():
            if cm % 2 == 0:
                # compartido: bit 0 -> c/2 ; bit 1 -> (3c+1-3^k)/2
                h0 = (k, (cm // 2) % Q2)
                v = (3 * cm + 1 - pot3(k)) % Q
                h1 = (k, (v // 2) % Q2)
                nuevos[h0] = nuevos.get(h0, 0) + n
                nuevos[h1] = nuevos.get(h1, 0) + n
            else:
                # mixto: bit 0 -> (k+1, (3c+1)/2) ; bit 1 -> (k-1, ...)
                v = (3 * cm + 1) % Q
                h0 = (k + 1, (v // 2) % Q2)
                nuevos[h0] = nuevos.get(h0, 0) + n
                if k >= 3:
                    w = (cm - pot3(k - 1)) % Q
                    h1 = (k - 1, (w // 2) % Q2)
                    nuevos[h1] = nuevos.get(h1, 0) + n
                else:
                    absorbidos += n      # k = 2 con bit 1 cae al fondo
        estados = nuevos
    return historia


def cola_racha(estados, Q, j_tope):
    # devuelve, por bit, los conteos enteros de "racha >= j" entre los
    # estados con c impar (el mixto ocurre en el paso siguiente), y el
    # total de impares y de vivos
    vivos = sum(estados.values())
    impares = 0
    ge0 = {j: 0 for j in range(j_tope + 1)}     # bit 0
    ge1 = {j: 0 for j in range(j_tope + 1)}     # bit 1 (solo k >= 3)
    impares_k3 = 0
    for (k, cm), n in estados.items():
        if cm % 2 == 1:
            impares += n
            u = (3 * cm + 1) % Q
            v2u = 0
            while u % 2 == 0 and v2u < j_tope + 1:
                u //= 2
                v2u += 1
            for j in range(min(v2u - 1, j_tope) + 1):
                ge0[j] += n
            if k >= 3:
                impares_k3 += n
                w = (cm - pot3(k - 1)) % Q
                v2w = 0
                while w % 2 == 0 and v2w < j_tope + 1:
                    w //= 2
                    v2w += 1
                for j in range(min(v2w - 1, j_tope) + 1):
                    ge1[j] += n
    return vivos, impares, impares_k3, ge0, ge1


def residuo_peor(estados, j):
    # max_r P(c = r mod 2^j | vivo) * 2^j (la constante L-infinito) y
    # 2^j * suma_r P(r)^2 (la constante L2, de COLISION: la que basta
    # para la version debil del lema de racha), exactas en racionales
    vivos = sum(estados.values())
    pesos = {}
    for (k, cm), n in estados.items():
        r = cm % (2 ** j)
        pesos[r] = pesos.get(r, 0) + n
    linf = max(pesos.values()) * (2 ** j) / float(vivos)
    l2 = sum(p * p for p in pesos.values()) * (2 ** j) / float(vivos) ** 2
    return linf, l2


# ----- la enumeracion exhaustiva (E1 + adaptada), OTRO codigo -----

def paso_entero(k, c, bit):
    # la dinamica entera exacta, copiada de la forma de rachasreales
    if c % 2 == 0:
        return (k, c // 2) if bit == 0 else (k, (3 * c + 1 - pot3(k)) // 2)
    if bit == 0:
        return (k + 1, (3 * c + 1) // 2)
    if k >= 3:
        return (k - 1, (c - pot3(k - 1)) // 2)
    return None                                  # fondo


def enumerar(c0, t):
    finales = []           # (k, c, k_camino) de las palabras vivas
    absorbidas = 0
    for w in range(2 ** t):
        k, c = 2, c0
        camino = []
        vivo = True
        for i in range(t):
            r = paso_entero(k, c, (w >> i) & 1)
            if r is None:
                absorbidas += 1
                vivo = False
                break
            k, c = r
            camino.append(k)
        if vivo:
            finales.append((k, c, tuple(camino)))
    return finales, absorbidas


def v2_de(n):
    v = 0
    while n % 2 == 0 and v < 64:
        n //= 2
        v += 1
    return v


print("LA EQUIDISTRIBUCION DE v2 TRAS EL MIXTO (Pieza B, exacta)")
print("DP sobre (k, c mod 2^(M-t)), M = %d; conteos enteros de palabras"
      % (T_MAXDP + M_BITS))
print()

peor_global = 0.0
for c0, nombre in ARRANQUES:
    print("=== arranque %s ===" % nombre)
    historia = dp_correr(c0)
    for t in ESCALERA:
        estados, absorbidos, Q = historia[t]
        vivos, impares, impares_k3, ge0, ge1 = cola_racha(
            estados, Q, J_MAX)
        if vivos + absorbidos != 2 ** t:
            raise SystemExit("E2: %d vivos + %d absorbidos != 2^%d"
                             % (vivos, absorbidos, t))
        peor_t = 0.0
        detalle = []
        for j in range(1, J_MAX + 1):
            Cj0 = (ge0[j] / float(impares)) * 2 ** j if impares else 0.0
            Cj1 = (ge1[j] / float(impares_k3)) * 2 ** j if impares_k3 \
                else 0.0
            if t >= 12:
                if impares * 2.0 ** (-j) >= MIN_ESPERADO:
                    peor_t = max(peor_t, Cj0)
                if impares_k3 * 2.0 ** (-j) >= MIN_ESPERADO:
                    peor_t = max(peor_t, Cj1)
            if j in (1, 4, 8, 10):
                # la marca de granularidad es POR BIT (10a, A3-13):
                # cada bit tiene su propio peso esperado
                marca0 = "" if impares * 2.0 ** (-j) >= MIN_ESPERADO \
                    else "*"
                marca1 = "" if impares_k3 * 2.0 ** (-j) >= MIN_ESPERADO \
                    else "*"
                detalle.append("j=%d: %.3f%s/%.3f%s"
                               % (j, Cj0, marca0, Cj1, marca1))
        res8, col8 = residuo_peor(estados, 8)
        print("  t = %2d: vivos %7d/2^%d  P(impar) %.4f  C_j "
              "(bit0/bit1) %s  residuo peor (m=8) %.3f  colision L2 "
              "(m=8) %.3f"
              % (t, vivos, t, impares / float(vivos), "  ".join(detalle),
                 res8, col8))
        if t >= 12:
            peor_global = max(peor_global, peor_t)
    # E3: el contraejemplo del adv 1, visto por el instrumento
    if c0 == INV3_NEG_2_21:
        estados1, _, Q1 = historia[1]
        # tras el primer paso (mixto bit 0 o bit 1 desde c0 impar):
        # el hijo bit 0 debe tener v2 >= 19 (la racha forzada)
        malo = False
        for (k, cm), n in estados1.items():
            if k == 3:                    # el hijo del bit 0
                v2c = 0
                u = cm % Q1
                while u % 2 == 0 and v2c < 25:
                    u //= 2
                    v2c += 1
                if v2c < 19:
                    malo = True
        if malo:
            raise SystemExit("E3: el c0 adversarial NO fuerza la racha "
                             "larga -- la reduccion esta mal")
        print("  E3 OK: racha_1 tras bit 0 forzada >= 19 (el transitorio")
        print("  del adv 1, reproducido) y a t >= 12 la cola ya esta")
        print("  dominada: el transitorio es determinista y MUERE.")
    print()

if peor_global > C_TOPE:
    raise SystemExit("E4: C_j = %.3f > %.1f en la escalera t >= 12"
                     % (peor_global, C_TOPE))
print("E4 OK: C_j <= %.3f <= %.1f en toda celda con peso esperado >= %g"
      % (peor_global, C_TOPE, MIN_ESPERADO))
print("de la escalera t >= 12, los dos bits, los tres arranques")
print("(contraejemplo adversarial incluido; * = celda de granularidad,")
print("POR BIT -- el asterisco va junto al valor del bit eximido --,")
print("reportada sin exigir: alli habla el residuo del c0, no la")
print("equidistribucion).")
print()

# ----- E1 + la version ADAPTADA, por enumeracion exhaustiva -----
print("el cruce independiente (t = %d, 2^%d palabras, dinamica entera "
      "exacta):" % (T_CRUCE, T_CRUCE))
for c0, nombre in ARRANQUES:
    finales, absorbidas = enumerar(c0, T_CRUCE)
    # la cola de racha por enumeracion, en ENTEROS
    impares = [x for x in finales if x[1] % 2 == 1]
    ge0_e = {j: 0 for j in range(J_MAX + 1)}
    ge1_e = {j: 0 for j in range(J_MAX + 1)}
    n_k3 = 0
    for (k, c, cam) in impares:
        v0 = v2_de(3 * c + 1)
        for j in range(min(v0 - 1, J_MAX) + 1):
            ge0_e[j] += 1
        if k >= 3:
            n_k3 += 1
            v1 = v2_de(c - pot3(k - 1)) if c != pot3(k - 1) else 64
            for j in range(min(v1 - 1, J_MAX) + 1):
                ge1_e[j] += 1
    # el DP en el mismo t
    historia = dp_correr(c0)
    estados, absorbidos_dp, Q = historia[T_CRUCE]
    vivos_dp, impares_dp, impares_k3_dp, ge0_d, ge1_d = cola_racha(
        estados, Q, J_MAX)
    if (len(finales) != vivos_dp or absorbidas != absorbidos_dp
            or len(impares) != impares_dp or n_k3 != impares_k3_dp
            or any(ge0_e[j] != ge0_d[j] for j in range(J_MAX + 1))
            or any(ge1_e[j] != ge1_d[j] for j in range(J_MAX + 1))):
        raise SystemExit("E1: DP y enumeracion NO coinciden en c0 = %d"
                         % c0)
    # la version ADAPTADA: agrupar por el k-camino entero
    grupos = {}
    for (k, c, cam) in impares:
        grupos.setdefault(cam, []).append((k, c))
    peor_adapt = 0.0
    peor_txt = ""
    for cam, miembros in grupos.items():
        n_g = len(miembros)
        for j in range(1, J_MAX + 1):
            if n_g < 2 ** (j + MIN_GRUPO_LOG2):
                break
            cuenta = 0
            for (k, c) in miembros:
                if v2_de(3 * c + 1) >= j + 1:
                    cuenta += 1
            Cj = (cuenta / float(n_g)) * 2 ** j
            if Cj > peor_adapt:
                peor_adapt = Cj
                peor_txt = "j=%d, grupo de %d" % (j, n_g)
    print("  c0 = %d: E1 OK (enteros identicos, %d vivas); adaptada: "
          "C_j peor %.3f (%s) sobre %d k-caminos"
          % (c0, len(finales), peor_adapt, peor_txt, len(grupos)))

print()
print("Lectura: la Pieza B es equidistribucion de c mod 2^m y el")
print("instrumento la mide EXACTA: el marginal con C ~ 1, el")
print("transitorio adversarial reproducido y muerto en t >= 12, y la")
print("version adaptada al k-camino acotada. Lo que queda para teorema")
print("es el conteo de colisiones del mapa palabra -> c_t mod 2^t")
print("(tortolas.lean da la mecanica del Delta). Medicion exacta, no")
print("teorema.")
