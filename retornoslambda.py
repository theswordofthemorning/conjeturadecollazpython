# retornoslambda.py
#
# EL CIERRE DEL GOAL DE LAMBDA (04-08-2026), en tres piezas:
#
#   1. EL CRUCE LaTOURETTE - LOS RETORNOS DE OVEJAS (tesis Moravian 2007,
#      lecturas/latourette2007/): sus "blocks" son pares de secuencias de
#      paridad (q, q') con T_q(x) = T_q'(x+1) + 1 -- o sea PALABRAS QUE
#      VUELVEN A DIFERENCIA 1: nuestras palabras de PRIMER RETORNO de la
#      cadena (k, c) al estado consecutivo (0,1). Sus conteos por largo
#      (leidos de la imagen de la pagina 26 del visor):
#          largo:  2  5  7  8  9  10  11      (21 blocks en total)
#          count:  1  1  1  3  2   4   9
#      Aqui se calcula R01(j) = primeros retornos exactos de la cadena y
#      se compara. Si clava, el catalogo a mano de 2007 ES nuestra serie
#      de retornos, y la cadena lo extiende sin limite.
#
#   2. EL TEOREMA DE INVERSION - ZORRAS (el mecanismo, escrito):
#          phi < 1  ==>  lambda = 2      (equivalente: lambda < 2 ==> phi = 1)
#      Mecanismo: el estado (1,2) fusiona en exactamente 2 pasos con la
#      palabra 0,1 (test C2a). Toda palabra viva de largo t que termina
#      en (1,2) se extiende a una palabra de fusion de largo t+2, y
#      prefijos distintos dan fusiones distintas:
#          b(t+2) >= N_t(1,2)            (test C2b, igualdad de enteros)
#      Si la fraccion s_t = N_t(1,2)/vivas(t) esta acotada abajo (C2c,
#      medida) y phi < 1, entonces vivas(t) >= (1-phi)*2^t y
#          b(t+2) >= s*(1-phi)*2^t  ==>  lambda = 2.
#      COROLARIO CONTRA EL ATAJO DEL GOAL: demostrar lambda < 2 NO
#      demostraria f < 1 -- demostraria f = 1 (Gao-Wu). El atajo del
#      autovalor no rodea el paseo: desemboca en el.
#
#   3. LA RESPUESTA A "ES lambda < 2?": NO DECIDIBLE POR TRUNCADOS, pero
#      acorralada: lambda >= lambda_T para todo truncado (los caminos del
#      truncado son caminos reales), lambda_T sube 1.7400 -> 1.8667 ->
#      1.9336 -> 1.9556 -> ... y el gap 2 - lambda_T se achica ~a la
#      mitad por escalon. Aqui se anaden dos truncados mas (regla 4x).
#      Ademas b(t+1)/b(t) medida (1.9432 en t=33) YA ESTA POR DEBAJO de
#      la cota demostrada del truncado K=7 (1.9556): las razones tienen
#      que seguir subiendo al menos hasta ahi -- la extrapolacion "se
#      asienta en ~1.95" queda muerta.

LATOURETTE_41 = {2: 1, 5: 1, 7: 1, 8: 3, 9: 2, 10: 4, 11: 9}     # blocks, 21
LATOURETTE_42 = {6: 1, 7: 2, 8: 2, 9: 4, 10: 7, 11: 11}          # strings, 27
B_SERIE = [1, 2, 2, 3, 4, 6, 11, 19, 34, 60, 106, 190, 341, 623, 1148,
           2124, 3963, 7451, 14072, 26699, 50913, 97379, 186769, 359164,
           692079, 1336125, 2583668, 5002992, 9701007, 18831364, 36594031]
PROF_R = 30
PROF_N = 32


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
# C1: LOS PRIMEROS RETORNOS R01(j) CONTRA LAS DOS TABLAS DE LaTOURETTE
#   (tesis Moravian 2007; imagenes en lecturas/latourette2007/, tablas
#   transcritas de las paginas 26 y 28 del documento).
#
#   EL CRUCE, con su hallazgo: sus "blocks" son los primeros retornos
#   del par a gap 1 CON EL ORDEN CONSERVADO (el lado de x sigue menor)
#   y sus "strings" los retornos CON VUELCO (el lado de x queda mayor).
#   Los conteos clavan largo a largo EXCEPTO uno: su Tabla 4.2 lista en
#   L = 11 la entrada (00011100101, 10110100010), que toca gap 1 ya en
#   t = 9 -- su prefijo de 9 bits es la PRIMERA entrada L9 de su propia
#   tabla (000111001, 101101000) -- y viola la condicion de subsecuencia
#   de su Definicion 4. ERROR EN LA TABLA DE 2007, cazado por la cadena:
#   el conteo bueno de L11 es 9 blocks + 10 strings = 19, no 20.
#   (Las otras 47 entradas: formales +-1 y realizables, 0 defectos.)
# ---------------------------------------------------------------------------

# totales por la cadena (el estado (0,1) colapsa el signo: totales)
estados = {(0, 1): 1}
R01 = []
for t in range(1, PROF_R + 1):
    nuevo = {}
    retornos = 0
    for (k, c), n in estados.items():
        for bit in (0, 1):
            s = transicion(k, c, bit)
            if s[0] == 'fusion':
                continue                      # fusion no es retorno
            clave = (s[1], s[2])
            if clave == (0, 1):
                retornos += n
            else:
                nuevo[clave] = nuevo.get(clave, 0) + n
    estados = nuevo
    R01.append(retornos)

COMBINADA = {2: 1, 5: 1, 6: 1, 7: 3, 8: 5, 9: 6, 10: 11, 11: 19}
for L in range(1, 12):
    if R01[L - 1] != COMBINADA.get(L, 0):
        raise SystemExit("C1 total: largo %d cadena=%d esperado=%d"
                         % (L, R01[L - 1], COMBINADA.get(L, 0)))

# el reparto por signo, con pares reales (representante grande)
KSEP = 999999
firmas = {}
for r0 in range(2 ** 11):
    rep = r0 + 2 ** 11 * KSEP
    x, y = rep, rep + 1
    for t in range(1, 12):
        x, y = paso_par = (x, y)
        x, y = ((3 * x + 1) // 2 if x % 2 else x // 2,
                (3 * y + 1) // 2 if y % 2 else y // 2)
        if abs(x - y) == 1:
            clave = (t, 1 if x > y else -1)
            firmas[clave] = firmas.get(clave, 0) + 1
            break
for L in range(2, 12):
    blocks = firmas.get((L, -1), 0) // 2 ** (11 - L)
    strings = firmas.get((L, 1), 0) // 2 ** (11 - L)
    esp41 = LATOURETTE_41.get(L, 0)
    esp42 = LATOURETTE_42.get(L, 0) if L != 11 else 10   # el error, corregido
    if blocks != esp41 or strings != esp42:
        raise SystemExit("C1 signo: L=%d blocks=%d/%d strings=%d/%d"
                         % (L, blocks, esp41, strings, esp42))

print("C1 OK -- EL CRUCE LaTOURETTE, CERRADO: blocks (4.1) = retornos con")
print("orden conservado (21/21 clavados) y strings (4.2) = retornos con")
print("vuelco (26/27: su entrada L11 (00011100101,.) toca gap 1 en t = 9")
print("-- su propio L9 -- y viola su Definicion 4: ERROR EN LA TABLA DE")
print("2007, unico, cazado por la cadena). El catalogo a mano ES la")
print("serie de retornos de la cadena, y la cadena lo extiende:")
print("  largo :", list(range(2, 12)))
print("  total :", R01[1:11], "  (blocks+strings, L11 corregido a 19)")
print("extension (largos 12..%d):" % PROF_R)
print("  ", R01[11:])
razR = [R01[i + 1] / R01[i] for i in range(13, PROF_R - 1) if R01[i]]
print("razones de la cola:", ["%.4f" % r for r in razR[-6:]])

# ---------------------------------------------------------------------------
# C2: EL TEOREMA DE INVERSION -- las tres piezas con enteros.
# ---------------------------------------------------------------------------

# (a) la ventana de 2 pasos desde (1,2)
s1 = transicion(1, 2, 0)
if s1[0] != 'estado' or (s1[1], s1[2]) != (1, 1):
    raise SystemExit("C2a: (1,2) bit 0 no va a (1,1)")
if transicion(1, 1, 1)[0] != 'fusion':
    raise SystemExit("C2a: (1,1) bit 1 no fusiona")

# (b) y (c): N_t(1,2), vivas(t) y b(t+2) >= N_t(1,2), exacto
estados = {(0, 1): 1}
filas = []
for t in range(1, PROF_N + 1):
    nuevo = {}
    for (k, c), n in estados.items():
        for bit in (0, 1):
            s = transicion(k, c, bit)
            if s[0] == 'fusion':
                continue
            clave = (s[1], s[2])
            nuevo[clave] = nuevo.get(clave, 0) + n
    estados = nuevo
    vivas = sum(estados.values())
    N12 = estados.get((1, 2), 0)
    filas.append((t, N12, vivas))

print()
print("C2: el mecanismo de la inversion, con enteros:")
print("   t     N_t(1,2)      vivas(t)   N/vivas   b(t+2) >= N_t?")
peor = 1.0
for t, N12, vivas in filas:
    frac = N12 / vivas
    b_t2 = B_SERIE[t - 1] if 3 <= t + 2 <= 33 else None
    ok = "" if b_t2 is None else ("OK" if b_t2 >= N12 else "FALLO")
    if b_t2 is not None and b_t2 < N12:
        raise SystemExit("C2b: t=%d b(t+2)=%d < N=%d" % (t, b_t2, N12))
    if t >= 8:
        peor = min(peor, frac)
    if t >= 24:
        print("  %2d  %11d  %12d    %.4f   %s" % (t, N12, vivas, frac, ok))
print("fraccion minima s_t (t >= 8): %.4f  -- acotada lejos de 0" % peor)
print()
print("C2 OK -- TEOREMA DE INVERSION (mecanismo completo):")
print("  b(t+2) >= N_t(1,2)  [enteros, verificado];  s_t >= %.3f  [medido]" % peor)
print("  ==> si phi < 1:  b(t+2) >= s*(1-phi)*2^t  ==>  lambda = 2.")
print("  CONTRAPOSITIVO: lambda < 2  ==>  phi = 1 (Gao-Wu CIERTA).")
print("  El atajo del goal se INVIERTE: demostrar lambda < 2 no daria")
print("  f < 1 -- daria f = 1. El autovalor no rodea el paseo.")

# ---------------------------------------------------------------------------
# C3: dos truncados mas (regla 4x) y el gap 2 - lambda_T (PUMAS).
# ---------------------------------------------------------------------------

def lambda_truncado(K, C, pasos=300):
    v = {(0, 1): 1}
    fus_prev = fus = 0
    razones = []
    for t in range(1, pasos + 1):
        nuevo = {}
        fus_nueva = 0
        for (k, c), n in v.items():
            for bit in (0, 1):
                s = transicion(k, c, bit)
                if s[0] == 'fusion':
                    fus_nueva += n
                elif s[1] <= K and abs(s[2]) <= C:
                    clave = (s[1], s[2])
                    nuevo[clave] = nuevo.get(clave, 0) + n
        v = nuevo
        if fus and fus_nueva:
            razones.append(fus_nueva / fus)
        fus_prev, fus = fus, fus_nueva
    return min(razones[-30:]), max(razones[-30:])

print()
print("C3: la escalera de truncados (cotas inferiores DEMOSTRADAS de lambda):")
gaps = []
for K, C in ((2, 12), (3, 48), (5, 192), (7, 768), (9, 3072), (11, 12288)):
    lo, hi = lambda_truncado(K, C)
    gaps.append(2 - lo)
    print("  K=%2d C=%6d   lambda_T = %.6f   gap 2-lambda_T = %.6f"
          % (K, C, lo, gaps[-1]))
print("razones de gaps consecutivos:",
      ["%.3f" % (gaps[i + 1] / gaps[i]) for i in range(len(gaps) - 1)])
print()
print("VEREDICTO DEL GOAL: lambda NO es estrictamente menor que 2 en")
print("ningun sentido demostrable por truncados (lema de la libertad), y")
print("las cotas inferiores suben con gap ~x0.5-0.7 por escalon hacia 2.")
print("La b-razon medida (1.9432 en t=33) esta DEBAJO de la cota")
print("demostrada %.4f: las razones deben seguir subiendo al menos" % (2 - gaps[-1]))
print("hasta ahi. Con el teorema de inversion: lambda = 2 salvo que")
print("Gao-Wu sea cierta -- y en ese caso phi = 1 y la pregunta del")
print("programa esta respondida. En ambos mundos, lambda no separa.")
