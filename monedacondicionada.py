# monedacondicionada.py
#
# EL SESGO DE LA MONEDA CONDICIONADA, DESCOMPUESTO POR ALTURA
# (10-08-2026; hallazgo propuesto: GARZAS -- la garza espera inmovil
# en el fondo y lee el agua; el bautizo es del usuario). El "ultimo
# paso" del acta de la 5a revision, atacado con el instrumento que
# faltaba: en la cadena MODIFICADA, forward-backward EXACTO en
# enteros --
#
#   alfa_s(x) = numero de palabras de largo s de (0,1) a x
#   gama_s(x) = numero de palabras de largo T-s de x al objetivo
#               (objetivo = fondo k <= 1 en T, o el estado (1,1) en T)
#
# y el sesgo condicionado de la moneda de un paso PAR (c par: bit 1 =
# Ee = expansiva, bit 0 = E0 = contractiva) en el estado x al nivel s:
#
#   E[bit1 - bit0 | objetivo] en (s,x)  =  alfa_s(x) * (gama_{s+1}(hijo1)
#                                          - gama_{s+1}(hijo0)) / F
#
# con F = masa de palabras que cumplen el objetivo. Se agrega POR
# ALTURA k (donde vive el sesgo?) y POR MITAD de la trayectoria (es
# efecto de borde final o vive en el grueso?). Y LA LECTURA NUEVA QUE
# ESTE INSTRUMENTO PERMITE: el desbalance TOTAL por trayectoria
# a_D * T = E[Ee - E0 | objetivo] -- si es O(1) en T, el sesgo por
# paso se desvanece solo.
#
# COMPROBACIONES (capa 1 + adversarial propia, antes de imprimir):
#   C1  conservacion: sum alfa_s = 2^s en todo nivel (no hay absorcion).
#   C2  URRACAS agregada: exp-contr = 2V + (Ee-E0) + k0 - k_t vale
#       palabra a palabra, luego la suma ponderada por gama debe dar
#       IGUALDAD DE ENTEROS: S_expcontr = 2*S_V + S_eed - S_kt (k0=0).
#       (OJO: C2 NO distingue la convencion del vortice -- ver C4.)
#   C3  objetivo trivial (todos los estados): gama es uniforme por
#       nivel y TODOS los sesgos deben ser CERO entero (la moneda justa
#       sin condicionar de urracas.py, aqui como control del backward).
#   C4  EL CRUCE INDEPENDIENTE: la fila t = 28 de urracas.py (corrida
#       10-08-2026: q1 0.509540, a_V 0.036662, a_D 0.008330, a_K
#       0.025911) debe reproducirse con este algoritmo distinto
#       (forward-backward contra acumulacion forward). Este cruce ya
#       cazo un bug real: la primera version contaba V en LOS DOS bits
#       del vortice (a_V daba el doble) y la identidad C2 cerraba
#       igual, porque exp<->contr y V se compensan (+2-2=0).
#   C5  LA FUERZA BRUTA: a T = 12, las 4096 palabras enumeradas UNA A
#       UNA con sus contadores, agregadas con el indicador del
#       objetivo; todos los acumuladores (F, S_eed, S_V, S_expcontr,
#       S_kt y el perfil num[k]) deben COINCIDIR COMO ENTEROS con el
#       forward-backward, para los dos objetivos.
#
# LOS TRES HALLAZGOS (medidos, ORIENTAN -- el veredicto es del
# mecanismo; detalles en el VEREDICTO impreso al final):
#   1) el sesgo de la moneda condicionada al fondo vive en k <= 3
#      (el 95,8% de las monedas y el 98,0% del sesgo total; el 99%
#      de las monedas recien en k <= 5 -- cifra corregida por la 7a
#      revision), es <= ~0,03 por moneda, decae de k=1 a k=3 (k=4
#      repunta a +0,009 con poca masa) y esta en LAS DOS mitades de
#      la trayectoria: no es efecto de borde final; el TOTAL por
#      trayectoria crece ~0,003-0,004/paso (aun el peor caso lineal
#      da a_D -> ~0,004, sesenta veces bajo el umbral efectivo);
#   2) condicionado a estar EN (1,1) -- el evento cuya serie ES el
#      criterio de retorno11.py -- el balance a_V + a_D - a_K es
#      NEGATIVO (~-0,05) EN LA VENTANA MEDIDA; la serie sube
#      +0,0016/paso (extrapolada cruzaria 0 hacia T ~ 60 -- 7a
#      revision): es un enunciado de ventana, no de limite;
#   3) de regalo del forward: el exponente local de P(X_t = (1,1))
#      -- la ventana de UN estado de LIEBRES, la que el acta dejo
#      INDECIDIDA -- esta bajo 1 y baja monotono desde t = 18 (1,14
#      a 0,76 en t=30; hubo cruces previos en la serie corta
#      ruidosa: t=14 -- 7a revision); la divergencia de la serie de
#      Green pide mas lento que 1/t: la direccion medida es la de la
#      recurrencia (phi = 1). Etiqueta honesta: P_t ~ 1/(t log^2 t)
#      tambien tendria alfa -> 1 por abajo y su serie CONVERGE -- la
#      serie corta orienta y no decide.
#
# Mapa del ATAJO via la cadena de Leonas modificada; enteros exactos;
# SystemExit antes de concluir.

import time

T_MAX = 30                      # profundidad maxima del barrido
TES_FONDO = (16, 20, 24, 28, 30)
TES_11 = (20, 24, 28, 30)
FONDO_K = 1                     # el fondo es k <= 1
T_BRUTA = 12                    # largo de la fuerza bruta (2^T palabras)

# la fila t=28 de urracas.py (corrida 10-08-2026, algoritmo independiente)
URRACAS_T28 = {'q1': 0.509540, 'a_V': 0.036662, 'a_D': 0.008330,
               'a_K': 0.025911}


def transicion_mod(k, c, bit):
    # la cadena de Leonas con el vortice rebotado (identica a
    # retorno11.py / lamperti.py)
    if k == 0:
        if c % 2 == 0:
            return (0, c // 2) if bit == 0 else (0, 3 * c // 2)
        return (1, (3 * c + 1) // 2) if bit == 0 else (1, (1 - 3 * c) // 2)
    if c % 2 == 0:
        return (k, c // 2) if bit == 0 else (k, (3 * c + 1 - 3 ** k) // 2)
    if k == 1 and c == 1:
        return (2, 2)
    if bit == 0:
        return (k + 1, (3 * c + 1) // 2)
    if k >= 2:
        return (k - 1, (c - 3 ** (k - 1)) // 2)
    return (0, abs((c - 1) // 2))


def clasifica(k, c, bit):
    # devuelve (d_expcontr, d_V, es_moneda) segun el libro de URRACAS
    # (tipo_de_paso de urracas.py): vortice bit 0 = tipo 6 (contr, sin
    # V); vortice bit 1 = tipo 9 (exp + V); moneda = c par.
    if k == 1 and c == 1:
        return (1, 1, False) if bit == 1 else (-1, 0, False)
    if c % 2 == 0:
        return (1, 0, True) if bit == 1 else (-1, 0, True)
    if k == 0:
        return (-1, 0, False)
    return (1, 0, False) if bit == 1 else (-1, 0, False)


# ---------------------------------------------------------------------------
# FORWARD: niveles[s] = { (k,c): conteo de palabras }, s = 0..T_MAX
# ---------------------------------------------------------------------------

t0 = time.time()
niveles = [None] * (T_MAX + 1)
niveles[0] = {(0, 1): 1}
for s in range(T_MAX):
    nuevo = {}
    for (k, c), n in niveles[s].items():
        for bit in (0, 1):
            clave = transicion_mod(k, c, bit)
            nuevo[clave] = nuevo.get(clave, 0) + n
    niveles[s + 1] = nuevo

# C1: conservacion de masa (la modificada no absorbe)
for s in range(T_MAX + 1):
    if sum(niveles[s].values()) != 2 ** s:
        raise SystemExit("C1: masa no conservada en s = %d" % s)
print("C1 OK: masa conservada (2^s) en los %d niveles. forward %.1fs, "
      "estados en T: %d" % (T_MAX + 1, time.time() - t0, len(niveles[T_MAX])))


# ---------------------------------------------------------------------------
# BACKWARD: acumula en ENTEROS, ponderando por alfa * gama.
# ---------------------------------------------------------------------------

def backward(es_objetivo, TT):
    gama = dict((x, 1 if es_objetivo(x) else 0) for x in niveles[TT])
    F = sum(niveles[TT][x] * g for x, g in gama.items())
    if F == 0:
        raise SystemExit("backward: F = 0 en T = %d" % TT)
    S = {'F': F, 'expcontr': 0, 'V': 0, 'eed': 0,
         'kt': sum(niveles[TT][x] * g * x[0] for x, g in gama.items())}
    num = {}
    den = {}
    num2 = {}
    den2 = {}
    for s in range(TT - 1, -1, -1):
        mitad = 0 if s < TT // 2 else 1
        gnuevo = {}
        for x, a in niveles[s].items():
            k, c = x
            h0 = transicion_mod(k, c, 0)
            h1 = transicion_mod(k, c, 1)
            g0 = gama.get(h0, 0)
            g1 = gama.get(h1, 0)
            gnuevo[x] = g0 + g1
            if g0 == 0 and g1 == 0:
                continue
            e0, v0, m0 = clasifica(k, c, 0)
            e1, v1, m1 = clasifica(k, c, 1)
            S['expcontr'] += a * (e0 * g0 + e1 * g1)
            S['V'] += a * (v0 * g0 + v1 * g1)
            if m0:
                d = a * (g1 - g0)
                o = a * (g0 + g1)
                S['eed'] += d
                num[k] = num.get(k, 0) + d
                den[k] = den.get(k, 0) + o
                num2[(k, mitad)] = num2.get((k, mitad), 0) + d
                den2[(k, mitad)] = den2.get((k, mitad), 0) + o
        gama = gnuevo
    # C2: URRACAS agregada, igualdad de enteros (k0 = 0)
    if S['expcontr'] != 2 * S['V'] + S['eed'] - S['kt']:
        raise SystemExit("C2 (T=%d): URRACAS no cierra: %d != %d"
                         % (TT, S['expcontr'], 2 * S['V'] + S['eed'] - S['kt']))
    return S, num, den, num2, den2


def informa(nombre, TT, S, num, den, num2, den2, perfil):
    F = float(S['F'])
    q1 = 0.5 + S['expcontr'] / (2.0 * TT * F)
    a_V = 2.0 * S['V'] / (TT * F)
    a_D = S['eed'] / (TT * F)
    a_K = S['kt'] / (TT * F)
    print()
    print("=== objetivo %s, T = %d ===" % (nombre, TT))
    print("C2 OK (identidad entera). masa del objetivo F/2^T = %.6f"
          % (S['F'] / 2.0 ** TT))
    print("q1 = %.6f   a_V = %.6f   a_D = %.6f   a_K = %.6f   suma = %.6f"
          % (q1, a_V, a_D, a_K, a_V + a_D - a_K))
    print("TOTALES por trayectoria: E[2V] = %.4f   E[Ee-E0] = %.4f   "
          "E[k_T] = %.4f" % (2 * S['V'] / F, S['eed'] / F, S['kt'] / F))
    if perfil:
        print()
        print("el perfil por altura: sesgo por MONEDA a altura k")
        print("   k    monedas/palabra   sesgo por moneda   1a mitad    2a mitad")
        for k in sorted(den):
            if den[k] == 0:
                continue
            b = num[k] / float(den[k])
            b1 = num2.get((k, 0), 0) / float(den2[(k, 0)]) \
                if den2.get((k, 0)) else float('nan')
            b2 = num2.get((k, 1), 0) / float(den2[(k, 1)]) \
                if den2.get((k, 1)) else float('nan')
            print("  %2d      %8.4f         %+9.6f     %+9.6f  %+9.6f"
                  % (k, den[k] / F, b, b1, b2))
    return {'q1': q1, 'a_V': a_V, 'a_D': a_D, 'a_K': a_K,
            'tot_eed': S['eed'] / F, 'tot_2V': 2 * S['V'] / F}


# ---------------------------------------------------------------------------
# C3: objetivo trivial -- todos los sesgos deben ser CERO entero.
# ---------------------------------------------------------------------------

S3, num3, _, _, _ = backward(lambda x: True, 14)
if S3['eed'] != 0 or any(v != 0 for v in num3.values()):
    raise SystemExit("C3: el objetivo trivial no da sesgo cero")
print("C3 OK: con objetivo trivial (sin condicionar) el sesgo de la moneda")
print("es CERO entero en total y en cada altura (la moneda justa).")

# ---------------------------------------------------------------------------
# C5: LA FUERZA BRUTA a T = %d: las 2^T palabras una a una.
# ---------------------------------------------------------------------------

def bruta(es_objetivo, TT):
    S = {'F': 0, 'expcontr': 0, 'V': 0, 'eed': 0, 'kt': 0}
    num = {}
    for palabra in range(2 ** TT):
        estado = (0, 1)
        expcontr = V = eed = 0
        por_k = {}
        for s in range(TT):
            bit = (palabra >> s) & 1
            k, c = estado
            e, v, m = clasifica(k, c, bit)
            expcontr += e
            V += v
            if m:
                eed += (1 if bit == 1 else -1)
                por_k[k] = por_k.get(k, 0) + (1 if bit == 1 else -1)
            estado = transicion_mod(k, c, bit)
        if es_objetivo(estado):
            S['F'] += 1
            S['expcontr'] += expcontr
            S['V'] += V
            S['eed'] += eed
            S['kt'] += estado[0]
            for k, d in por_k.items():
                num[k] = num.get(k, 0) + d
    return S, num


for nombre, objetivo in (("FONDO", lambda x: x[0] <= FONDO_K),
                         ("(1,1)", lambda x: x == (1, 1))):
    Sb, numb = bruta(objetivo, T_BRUTA)
    Sf, numf, _, _, _ = backward(objetivo, T_BRUTA)
    for clave in ('F', 'expcontr', 'V', 'eed', 'kt'):
        if Sb[clave] != Sf[clave]:
            raise SystemExit("C5 (%s): %s bruta=%d, backward=%d"
                             % (nombre, clave, Sb[clave], Sf[clave]))
    for k in set(numb) | set(numf):
        if numb.get(k, 0) != numf.get(k, 0):
            raise SystemExit("C5 (%s): num[%d] bruta=%d, backward=%d"
                             % (nombre, k, numb.get(k, 0), numf.get(k, 0)))
print("C5 OK: la fuerza bruta (2^%d palabras una a una) coincide COMO" % T_BRUTA)
print("ENTEROS con el forward-backward en F, exp-contr, V, Ee-E0, k_T y")
print("el perfil por altura, para los dos objetivos.")

# ---------------------------------------------------------------------------
# LA MEDICION: el fondo y el (1,1), las series en T.
# ---------------------------------------------------------------------------

fondo = {}
for TT in TES_FONDO:
    S, num, den, num2, den2 = backward(lambda x: x[0] <= FONDO_K, TT)
    fondo[TT] = informa("FONDO (k <= 1)", TT, S, num, den, num2, den2,
                        perfil=(TT == T_MAX))

# C4: el cruce contra urracas.py t = 28 (algoritmo independiente)
r = fondo[28]
for clave in ('q1', 'a_V', 'a_D', 'a_K'):
    if abs(r[clave] - URRACAS_T28[clave]) > 2e-6:
        raise SystemExit("C4: %s = %.6f, urracas.py dio %.6f"
                         % (clave, r[clave], URRACAS_T28[clave]))
print()
print("C4 OK: la fila t = 28 de urracas.py reproducida por el algoritmo")
print("independiente (forward-backward): q1, a_V, a_D, a_K a 6 cifras.")

once = {}
for TT in TES_11:
    S, num, den, num2, den2 = backward(lambda x: x == (1, 1), TT)
    once[TT] = informa("EL ESTADO (1,1)", TT, S, num, den, num2, den2,
                       perfil=(TT == T_MAX))

# ---------------------------------------------------------------------------
# LAS SERIES EN T DE LOS TOTALES (la lectura del h-transform).
# ---------------------------------------------------------------------------

print()
print("las series de los TOTALES por trayectoria:")
print("            FONDO                    (1,1)")
print("   T    E[Ee-E0]   E[2V]        E[Ee-E0]   E[2V]")
for TT in TES_FONDO:
    o = once.get(TT)
    cola = "      %8.4f  %7.4f" % (o['tot_eed'], o['tot_2V']) if o else ""
    print("  %2d    %7.4f   %7.4f%s" % (TT, fondo[TT]['tot_eed'],
                                        fondo[TT]['tot_2V'], cola))

# ---------------------------------------------------------------------------
# DE REGALO DEL FORWARD (la ventana mas fina de LIEBRES, la de UN
# estado): la serie P(X_t = (1,1)) con su exponente local. La serie de
# Green Sigma_t P(X_t = (1,1)) diverge (= recurrencia = phi 1) sii el
# decaimiento es mas lento que 1/t; el exponente local se estima entre
# t-6 y t. (Las ventanas grandes de liebres.py no muerden -- acta de
# la 5a; esta es la que el acta dejo INDECIDIDA.)
# ---------------------------------------------------------------------------

import math

print()
print("la serie del criterio: P_t = P(X_t = (1,1)) y exponente local")
print("   t       P_t        alfa_t (entre t-6 y t)")
pes = {}
for t in range(2, T_MAX + 1, 2):
    pes[t] = niveles[t].get((1, 1), 0) / 2.0 ** t
    alfa = ""
    if t - 6 in pes and pes[t - 6] > 0 and pes[t] > 0:
        alfa = "   %8.4f" % (-(math.log(pes[t]) - math.log(pes[t - 6]))
                             / (math.log(t) - math.log(t - 6)))
    print("  %2d   %10.6f%s" % (t, pes[t], alfa))

print()
print("VEREDICTO (medido, ORIENTA -- el veredicto final es del mecanismo):")
print("1) el desbalance de la moneda condicionada al fondo vive en k <= 3")
print("   (el 95,8% de las monedas, el 98% del sesgo), con sesgo por moneda")
print("   <= ~0,03, decayendo de k=1 a k=3, y presente en LAS DOS mitades")
print("   de la trayectoria (no es efecto de borde final);")
print("2) el TOTAL por trayectoria E[Ee-E0 | fondo] crece ~0,003-0,004")
print("   por paso en la ventana medida (0,187 en T=16 a 0,239 en T=30);")
print("   la serie corta NO distingue sublineal de lineal-chico (leccion")
print("   de la casa), pero AUN el peor caso lineal da a_D -> ~0,004:")
print("   sesenta veces bajo el umbral efectivo 0,2446;")
print("3) condicionado a estar EN (1,1) -- el evento cuya serie ES el")
print("   criterio -- el balance a_V + a_D - a_K es NEGATIVO (~-0,05):")
print("   las palabras que vuelven al pre-vortice son del lado")
print("   contractivo, a mas de 0,29 del umbral. La obstruccion de")
print("   CEBRAS (multiplicadores supercriticos en las historias que")
print("   vuelven) NO aparece en ninguna de las dos condicionadas.")
print()
print("total %.1fs" % (time.time() - t0))
