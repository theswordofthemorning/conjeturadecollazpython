# conteoconjunto.py
#
# EL BLANCO DEL TEOREMA DE CONTEO, MEDIDO SOBRE EL OBJETO CORRECTO
# (12-08-2026, tras la 10a revision y el contraejemplo naif de
# notaequidistribucion 3-bis.vi: la desigualdad multi-escala con el
# exceso de la MARGINAL de c es FALSA para distribuciones
# arbitrarias -- el enunciado correcto lleva el funcional CONJUNTO
# (k, c). Este fichero mide EXACTAMENTE ese funcional.)
#
#   LOS DOS OBJETOS. A tiempo t la ley de clases vive en (k, x) con
#   x = c mod 2^Q; r = c mod 2^m es la clase a escala m.
#
#   (1) EL CONJUNTO ABSOLUTO (la primera calibracion -- REGISTRADA
#       COMO NEGATIVO): E_t(m) = P_col(t,m) - Sigma_k P(k)^2 2^-m
#       con P_col = Sigma_(k,r) p(k,r)^2. Su razon multi-escala NO
#       baja de 1/2 (medido: peor 0,895/0,894/0,910 en A/B/ADV, en
#       m = 10) -- y la fisica es visible: E_t carga la colision de
#       la MARGINAL de k (Sigma P(k)^2 ~ 1/K_eff), que decae solo
#       DIFUSIVA (K_eff ~ sqrt(t), Rutas 3-bis.v), nunca geometrica.
#       Un funcional que cobra la concentracion de k no puede
#       contraer a razon fija. Se mide y se reporta como negativo.
#
#   (2) EL CONDICIONAL (el blanco CORRECTO): la colision condicional
#         C2_cond(t, m) = Sigma_k P(k) * C2_k(m),
#       con C2_k(m) = 2^m Sigma_r p(r|k)^2 la colision DENTRO de la
#       fibra. Por Cauchy-Schwarz con pesos P(k):
#         C2_marg(m) <= C2_cond(m)    (LA DESIGUALDAD PUENTE:
#       p(r) = Sigma_k p(k,r) y (Sigma_k p(k,r))^2 <=
#       (Sigma_k P(k)) * (Sigma_k p(k,r)^2 / P(k)) -- una linea),
#       asi que si e_cond := C2_cond - 1 contrae multi-escala
#         rho_cond(t, m) = e_(t+1)(m) / e_t(m + 1) < 1/2,
#       el telescopio da e_t(m) <= 2^m (2 rho)^t -> 0 y con el cae
#       C2_marg: LA PIEZA B ENTERA via L2. El contraejemplo naif NO
#       aplica: con marginal uniforme y k correlacionado, e_cond > 0
#       (las fibras estan concentradas y el funcional lo ve) -- el
#       cociente queda bien planteado. Y el piso movil de k esta
#       DIVIDIDO, no restado: la difusion de k no contamina.
#
#   TODO EXACTO: con conteos n(k, r) enteros y vivos V,
#     NUM_t(m) = 2^m * Sigma n(k,r)^2 - Sigma_k n_k^2      (entero)
#     E_t(m)   = NUM_t(m) / (V^2 * 2^m)          (el absoluto, (1))
#     e_cond_t(m) = (1/V) Sigma_k (2^m S2_k - n_k^2) / n_k
#       con S2_k = Sigma_r n(k,r)^2  -- en Fraction  (el bueno, (2))
#     rho_abs  = 2 * NUM_(t+1)(m) * V_t^2
#                  / (NUM_t(m+1) * V_(t+1)^2)
#     rho_cond = e_cond_(t+1)(m) / e_cond_t(m+1)  (Fraction exacta)
#   El float aparece solo al imprimir.
#
#   EL FILTRO, DECLARADO DE NACIMIENTO (leccion M5 de la 10a): la
#   razon solo se computa si el denominador normalizado E_t(m+1)
#   supera DEN_MIN -- las celdas excluidas se CUENTAN y se informan.
#   Con el funcional conjunto no se espera denominador 0 salvo
#   colapso exacto a uniforme-por-fibra, pero el filtro existe y se
#   dice.
#
#   LA GEOGRAFIA: por cada t de la escalera se reporta la fraccion
#   del exceso NUM que aportan las fibras del zocalo (k <= 4), donde
#   la sonda de alturas del 12-08 concentro el residuo.
#
#   COMPROBACIONES (SystemExit):
#     Z1  conservacion: vivos + absorbidos = 2^t en todo t.
#     Z2  el piso es exacto: una ley sintetica uniforme-por-fibra
#         (construida a mano) debe dar NUM = 0 EXACTO; y el
#         contraejemplo naif de 3-bis.vi (k correlacionado con x,
#         marginal uniforme) debe dar NUM > 0 -- el conjunto VE lo
#         que la marginal no.
#     Z3  cruce independiente (t = T_CRUCE): la enumeracion
#         exhaustiva de las 2^t palabras con la dinamica entera
#         exacta (sin modulos) debe reproducir Sigma n(k,r)^2 y
#         Sigma n_k^2 COMO ENTEROS.
#     Z4  veredicto sobre el CONDICIONAL: rho_cond < RHO_TOPE = 0,5
#         en toda celda computada (el 1/2 es DERIVADO: el telescopio
#         pide 2 rho < 1) de la escalera t >= T_MIN, tres arranques.
#         El absoluto (1) NO entra al veredicto: es el negativo
#         registrado.
#     Z5  la desigualdad puente verificada en los numeros:
#         C2_marg(m) <= C2_cond(m) en cada punto de la escalera
#         (es teorema -- C-S --; el chequeo caza errores de
#         implementacion, no de matematica).
#
#   Capa 1: mapa = la cadena (k, c) del atajo (la de rachasreales);
#   la medida es la de clases (palabras uniformes); es MEDICION
#   EXACTA a horizonte finito t <= 25, no teorema; arranques primos
#   no redondos + el adversarial; escalera y filtro declarados.

M_BITS = 12
T_MAXDP = 25
T_MIN = 12                  # el veredicto exige desde aqui
M_ESCALAS = range(5, 11)    # m = 5..10 (m+1 <= 11 < M_BITS)
T_CRUCE = 14
RHO_TOPE = 0.5              # DERIVADO: el telescopio pide 2*rho < 1
DEN_MIN = 1e-9              # filtro del denominador, DECLARADO:
                            # convencion; las excluidas se informan

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


# ----- el DP exacto (misma dinamica que equidistribucionmixto) -----

def dp_correr(c0):
    M = T_MAXDP + M_BITS
    estados = {(2, c0 % (2 ** M)): 1}
    absorbidos = 0
    historia = {}
    for t in range(T_MAXDP + 1):
        Q = 2 ** (M - t)
        historia[t] = (estados, absorbidos)
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


from fractions import Fraction


def medir_exceso(estados, m):
    # devuelve, exactos: NUM(m) entero (el absoluto), el aporte del
    # zocalo k <= 4 a NUM, e_cond(m) en Fraction (el condicional), la
    # fraccion del e_cond que aporta el zocalo, y C2_marg(m) en
    # Fraction (para el puente Z5)
    por_celda = {}
    por_fibra = {}
    marginal = {}
    vivos = 0
    for (k, cm), n in estados.items():
        r = cm % (2 ** m)
        por_celda[(k, r)] = por_celda.get((k, r), 0) + n
        por_fibra[k] = por_fibra.get(k, 0) + n
        marginal[r] = marginal.get(r, 0) + n
        vivos += n
    s2_k = {}
    for (k, r), n in por_celda.items():
        s2_k[k] = s2_k.get(k, 0) + n * n
    num_total = 0
    num_zocalo = 0
    e_cond = Fraction(0)
    e_cond_zoc = Fraction(0)
    for k, s2 in s2_k.items():
        nk = por_fibra[k]
        aporte = (2 ** m) * s2 - nk * nk
        num_total += aporte
        parte = Fraction(aporte, nk)
        e_cond += parte
        if k <= 4:
            num_zocalo += aporte
            e_cond_zoc += parte
    e_cond = e_cond / vivos
    frac_zoc = (e_cond_zoc / vivos) / e_cond if e_cond > 0 else Fraction(0)
    c2_marg = Fraction((2 ** m) * sum(n * n for n in marginal.values()),
                       vivos * vivos)
    c2_cond = e_cond + 1
    return num_total, num_zocalo, e_cond, frac_zoc, c2_marg, c2_cond


# ----- Z2: el piso y el contraejemplo naif, sinteticos -----

def z2():
    # uniforme-por-fibra: dos fibras (k=2 con 8 unidades repartidas
    # uniformes mod 4, k=3 con 4 unidades uniformes mod 4): exceso 0
    # en LOS DOS funcionales
    est = {}
    for r in range(4):
        est[(2, r)] = 2
        est[(3, r)] = 1
    total, _, e_cond, _, _, _ = medir_exceso(est, 2)
    if total != 0 or e_cond != 0:
        raise SystemExit("Z2: el piso no es exacto (NUM = %d, e_cond "
                         "= %s)" % (total, e_cond))
    # el contraejemplo naif de 3-bis.vi: marginal de c UNIFORME mod 4
    # pero k correlacionado (k=2 vive en r=0,1; k=3 en r=2,3): la
    # marginal no ve nada; LOS DOS funcionales deben ver exceso > 0
    est = {(2, 0): 1, (2, 1): 1, (3, 2): 1, (3, 3): 1}
    marg = {}
    for (k, r), n in est.items():
        marg[r] = marg.get(r, 0) + n
    if len(set(marg.values())) != 1:
        raise SystemExit("Z2: el sintetico no tiene marginal uniforme")
    total, _, e_cond, _, c2m, c2c = medir_exceso(est, 2)
    if total <= 0 or e_cond <= 0:
        raise SystemExit("Z2: los funcionales NO ven el contraejemplo "
                         "naif (NUM = %d, e_cond = %s)" % (total, e_cond))
    if c2m > c2c:
        raise SystemExit("Z2: el puente C-S falla en el sintetico")
    print("Z2 OK: piso exacto en el uniforme-por-fibra (exceso 0 en los")
    print("dos funcionales) y el contraejemplo naif de 3-bis.vi VISTO")
    print("por ambos (NUM = %d, e_cond = %s > 0 con marginal de c"
          % (total, e_cond))
    print("uniforme); puente C2_marg <= C2_cond OK en el sintetico.")
    print()


# ----- Z3: la enumeracion exhaustiva, otro codigo -----

def paso_entero(k, c, bit):
    if c % 2 == 0:
        return (k, c // 2) if bit == 0 else (k, (3 * c + 1 - pot3(k)) // 2)
    if bit == 0:
        return (k + 1, (3 * c + 1) // 2)
    if k >= 3:
        return (k - 1, (c - pot3(k - 1)) // 2)
    return None


def z3(c0, historia, m):
    grupos = {}
    fibras = {}
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
        if vivo:
            vivas += 1
            clave = (k, c % (2 ** m))
            grupos[clave] = grupos.get(clave, 0) + 1
            fibras[k] = fibras.get(k, 0) + 1
    s2_enum = sum(n * n for n in grupos.values())
    f2_enum = sum(n * n for n in fibras.values())
    estados, _ = historia[T_CRUCE]
    por_celda = {}
    por_fibra = {}
    for (k, cm), n in estados.items():
        clave = (k, cm % (2 ** m))
        por_celda[clave] = por_celda.get(clave, 0) + n
        por_fibra[k] = por_fibra.get(k, 0) + n
    s2_dp = sum(n * n for n in por_celda.values())
    f2_dp = sum(n * n for n in por_fibra.values())
    if s2_enum != s2_dp or f2_enum != f2_dp:
        raise SystemExit("Z3: DP y enumeracion difieren en c0 = %d "
                         "(%d/%d vs %d/%d)"
                         % (c0, s2_enum, f2_enum, s2_dp, f2_dp))
    return vivas


print("EL EXCESO CONJUNTO (k, c) Y SU RAZON MULTI-ESCALA -- el blanco")
print("del teorema de conteo sobre el objeto CORRECTO (post 3-bis.vi)")
print("DP exacto, M = %d bits; escalas m = %d..%d; filtro declarado:"
      % (T_MAXDP + M_BITS, min(M_ESCALAS), max(M_ESCALAS)))
print("rho solo si E_t(m+1) > %g (excluidas contadas)" % DEN_MIN)
print()

z2()

peor_cond = 0.0
peor_cond_celda = ""
peor_abs = 0.0
peor_abs_celda = ""
for c0, nombre in ARRANQUES:
    print("=== arranque %s ===" % nombre)
    historia = dp_correr(c0)
    # conservacion Z1, geografia y puente Z5 por escalera
    for t in (8, 12, 16, 20, 24):
        estados, absorbidos = historia[t]
        vivos = sum(estados.values())
        if vivos + absorbidos != 2 ** t:
            raise SystemExit("Z1: %d + %d != 2^%d" % (vivos, absorbidos, t))
        num8, zoc8, e_cond8, frac_zoc8, c2m8, c2c8 = medir_exceso(
            estados, 8)
        if c2m8 > c2c8:
            raise SystemExit("Z5: C2_marg = %s > C2_cond = %s en t = %d"
                             % (float(c2m8), float(c2c8), t))
        frac = (zoc8 / float(num8)) if num8 > 0 else 0.0
        print("  t = %2d: vivos %7d  e_cond(8) = %.4f (zocalo %.0f%%)  "
              "C2_marg %.4f <= C2_cond %.4f  E_abs %.2e (zocalo %.0f%%)"
              % (t, vivos, float(e_cond8), 100.0 * float(frac_zoc8),
                 float(c2m8), float(c2c8), num8 / float(vivos) ** 2
                 / 2 ** 8, 100.0 * frac))
    # las razones multi-escala, exactas
    vivos_t = {t: sum(historia[t][0].values())
               for t in range(T_MAXDP + 1)}
    medidas = {}
    for t in range(T_MIN, T_MAXDP + 1):
        for m in list(M_ESCALAS) + [max(M_ESCALAS) + 1]:
            medidas[(t, m)] = medir_exceso(historia[t][0], m)
    comp_c = exc_c = comp_a = exc_a = 0
    p_c = p_a = 0.0
    p_c_celda = p_a_celda = ""
    for t in range(T_MIN, T_MAXDP):
        for m in M_ESCALAS:
            # el condicional (Fraction exacta)
            den_c = medidas[(t, m + 1)][2]
            if float(den_c) <= DEN_MIN:
                exc_c += 1
            else:
                comp_c += 1
                rho_c = float(medidas[(t + 1, m)][2] / den_c)
                if rho_c > p_c:
                    p_c = rho_c
                    p_c_celda = "t=%d, m=%d" % (t, m)
            # el absoluto (negativo registrado; enteros)
            den_num = medidas[(t, m + 1)][0]
            den_a = den_num / float(vivos_t[t]) ** 2 / 2 ** (m + 1)
            if den_a <= DEN_MIN:
                exc_a += 1
            else:
                comp_a += 1
                rho_a = (2.0 * medidas[(t + 1, m)][0] * vivos_t[t] ** 2
                         / (den_num * float(vivos_t[t + 1]) ** 2))
                if rho_a > p_a:
                    p_a = rho_a
                    p_a_celda = "t=%d, m=%d" % (t, m)
    print("  rho_COND: peor %.3f (%s) en %d celdas (%d excluidas)"
          % (p_c, p_c_celda, comp_c, exc_c))
    print("  rho_abs (negativo registrado): peor %.3f (%s) en %d "
          "celdas (%d excl.)" % (p_a, p_a_celda, comp_a, exc_a))
    vivas = z3(c0, historia, 8)
    print("  Z3 OK: cruce exhaustivo 2^%d identico en enteros "
          "(%d vivas)" % (T_CRUCE, vivas))
    if p_c > peor_cond:
        peor_cond = p_c
        peor_cond_celda = "%s en %s" % (p_c_celda, nombre)
    if p_a > peor_abs:
        peor_abs = p_a
        peor_abs_celda = "%s en %s" % (p_a_celda, nombre)
    print()

if peor_cond >= RHO_TOPE:
    raise SystemExit("Z4: rho_cond = %.3f >= %.2f (%s) -- el blanco "
                     "condicional NO contrae bajo 1/2"
                     % (peor_cond, RHO_TOPE, peor_cond_celda))
print("Z4 OK: rho_COND <= %.3f < %.2f en toda celda computada" %
      (peor_cond, RHO_TOPE))
print("(peor: %s), escalera t = %d..%d, tres arranques." %
      (peor_cond_celda, T_MIN, T_MAXDP - 1))
print()
print("Lectura, en tres lineas:")
print("(1) EL NEGATIVO, REGISTRADO: el exceso conjunto ABSOLUTO no")
print("    contrae bajo 1/2 (peor %.3f, %s) -- carga la colision de"
      % (peor_abs, peor_abs_celda))
print("    la marginal de k, que decae difusiva (K_eff ~ sqrt(t)),")
print("    nunca geometrica: ese funcional queda descartado.")
print("(2) EL BLANCO BUENO: el exceso CONDICIONAL e_cond = ")
print("    Sigma_k P(k) (C2_k - 1) contrae multi-escala bajo 1/2 en")
print("    toda la ventana, y domina a la marginal por el puente C-S")
print("    (Z5, verificado): si un teorema entrega rho_cond < 1/2")
print("    para la transicion del DP sobre su orbita, la Pieza B")
print("    entera cae via L2. Inmune al contraejemplo naif (Z2).")
print("(3) MEDICION EXACTA a horizonte finito (t <= %d), no teorema;"
      % (T_MAXDP - 1,))
print("    filtro del denominador declarado y contado.")
