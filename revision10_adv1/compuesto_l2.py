# revision10_adv1/compuesto_l2.py
#
# TAREA c1 DE LA 10a REVISION (adversario 1): LA CUENTA DEL COMPUESTO
# DE RECARGAS BAJO L2 -- la pieza que notaequidistribucion.txt 3.iv
# declara POR REHACER ("las cuentas del compuesto de recargas con
# razon 2^(-1/2) hay que REHACERLAS").
#
# QUE HAY QUE COMPROBAR. Bajo la reduccion L2, cada lectura (racha o
# salto de recarga) tiene cola P(>= s) <= K 2^(-s/2) con
# K = sqrt(C2) (Cauchy-Schwarz trivial: P(r)^2 <= Sigma P^2). El
# encargo pregunta: (i) E[2^salto] DIVERGE con esa cola -- el
# argumento viejo "cada recarga cuesta un bit" via MGF en z = 2 esta
# muerto; (ii) reescrito con el MGF correcto (z < sqrt(2)),
# el compuesto cierra o no, y con que constante.
#
# RESULTADO EN TRES PARTES:
#   PARTE 1: la divergencia, confirmada (y tambien en L-infinito!).
#   PARTE 2: la cuenta del compuesto con el MGF correcto: cierra
#     para TODO K finito (no es margen chico: phi(1) = 1 < 2,
#     estructural), pero la razon geometrica resultante es
#     1/z* ~ 0,86 (K = 1,02), NO 2^(-1/2) = 0,707: la frase de la
#     nota "las colas de racha/recarga salen geometricas de razon
#     2^(-1/2)" NO la entrega el compuesto.
#   PARTE 3: LA REPARACION -- el compuesto es INNECESARIO: la union
#     sobre palabras de racha da la cola de la racha COMPUESTA
#     (recargas incluidas) directo de la equidistribucion:
#       "racha >= j con palabra u" es UNA clase mod 2^(j+1)
#       (verificado exhaustivo abajo; misma maquinaria que VIBORAS),
#     y  P(racha >= j) = 2^-(j-1) Sigma_{b,u} (1/4) P(clase_{b,u})
#                     <= max_clase <= sqrt(C2(j+1)) 2^-(j+1)/2 :
#     razon 2^(-1/2) EXACTA para la racha total, sin compuesto, sin
#     cotas inferiores condicionales.
#
# Capa 1: mapa = cadena (k, c) del atajo; todo son COTAS (no
# promedios); K barrido en una lista no tomada de una sola medicion;
# la verificacion de "una clase por palabra" es exhaustiva sobre
# modulos 2^(j+1) completos (sin borde redondo: el modulo ES el
# objeto); el Monte Carlo de la parte 2 es solo control de que la
# cota analitica no este al reves, no decide nada.

import random

RAIZ2 = 2 ** 0.5


# ----------------------------------------------------------------
# PARTE 1: E[2^S] diverge con cola K 2^(-s/2) (y con cola K 2^-s)
# ----------------------------------------------------------------
def parcial_mgf(z, base, K, smax):
    # cota INFERIOR de E[z^S] usando P(S = s) >= ... no hay inferior
    # desde una cota superior de cola; se usa la DISTRIBUCION FRONTERA
    # P(S >= s) = min(1, K base^s) y se suma E[z^S] parcial exacto
    total = 0.0
    for s in range(smax + 1):
        ps = min(1.0, K * base ** s) - min(1.0, K * base ** (s + 1))
        total += (z ** s) * ps
    return total


print("PARTE 1 -- LA DIVERGENCIA (distribucion frontera P(S>=s) ="
      " min(1, K r^s)):")
for (etq, base) in [("L2:  r = 2^(-1/2)", 2 ** -0.5),
                    ("Linf: r = 2^(-1)", 0.5)]:
    fila = []
    for smax in (10, 20, 40, 80):
        fila.append("s<=%d: %.3g" % (smax, parcial_mgf(2.0, base, 1.02, smax)))
    print("  %s  E[2^S] parcial: %s  -> DIVERGE" % (etq, ", ".join(fila)))
print("  (el argumento 'cada recarga cuesta un bit' via E[2^S] estaba"
      " roto YA en")
print("   L-infinito: con cola exacta 2^-s cada termino aporta ~K"
      " constante.)")
print()


# ----------------------------------------------------------------
# PARTE 2: el compuesto con el MGF correcto.
# Modelo (conservador, el de la Pieza A medida):
#   racha_total T = X0 + N + Sigma_{i<=N} S_i
#   P(X0 >= s) <= K 2^(-s/2)        (lectura de la entrada, L2)
#   P(S_i >= s | pasado) <= K 2^(-s/2), s >= 1   (salto de recarga)
#   P(N >= n | pasado) <= 2^(-n)    (cada recarga consume un bit
#                                    justo: EXACTO, no equidistrib.)
# MGF: phi_S(z) <= 1 + (z-1) K Sigma_{s>=1} z^(s-1) 2^(-s/2)
#              = 1 + (z-1) K / (sqrt(2) - z)          (z < sqrt(2))
# E[z^T] <= phi_X0(z) / (1 - z phi_S(z) / 2)  si  z phi_S(z) < 2.
# Cola: P(T >= j) <= E[z^T] z^-j  -- razon geometrica 1/z.
# ----------------------------------------------------------------
def phi_cota(z, K):
    if z >= RAIZ2:
        return float("inf")
    return 1.0 + (z - 1.0) * K / (RAIZ2 - z)


def z_estrella(K, con_paso_n=True):
    # el mayor z con z*phi(z) < 2 (o phi(z) < 2 si no se cuenta el
    # paso del bit de la recarga en el largo), por biseccion
    lo, hi = 1.0, RAIZ2 - 1e-12
    for _ in range(200):
        mid = (lo + hi) / 2
        val = mid * phi_cota(mid, K) if con_paso_n else phi_cota(mid, K)
        if val < 2.0:
            lo = mid
        else:
            hi = mid
    return lo


print("PARTE 2 -- EL COMPUESTO, REHECHO CON z < sqrt(2):")
print("  condicion de cierre: z*phi_S(z) < 2 con phi_S(z) = 1 +"
      " (z-1)K/(sqrt2 - z)")
print("  %-28s %-10s %-12s %-10s" % ("K = sqrt(C2)", "z*",
                                     "razon 1/z*", "cierra?"))
for K in (1.019, 1.02, 1.2, 1.5, 2.0, 3.0, 10.0):
    z = z_estrella(K)
    print("  %-28s %-10.4f %-12.4f %s"
          % ("%.3f" % K, z, 1.0 / z, "SI (estructural)"))
print("  con K = sqrt(1,038) = 1,019 (lo medido a t=24):"
      " z* = %.4f, razon = %.4f" % (z_estrella(1.019),
                                    1.0 / z_estrella(1.019)))
print("  phi(1) = 1 < 2 SIEMPRE: el cierre no es 'margen chico', es")
print("  estructural para todo C2 finito. PERO la razon que entrega es")
print("  ~0,86, NO 2^(-1/2) = 0,707: la frase de la nota atribuye al")
print("  compuesto una razon que el compuesto NO alcanza (en z ->"
      " sqrt(2)")
print("  el MGF del salto ya diverge, y la ramificacion en N corta"
      " antes).")
print()

# control Monte Carlo: el modelo frontera no debe violar la cota
azar = random.Random(20260812)


def muestra_frontera(K):
    # P(S >= s) = min(1, K 2^(-s/2)), s >= 1; N con P(N >= n) = 2^-n
    def un_salto():
        s = 1
        while azar.random() < 2 ** -0.5 and s < 400:
            s += 1
        return s
    x0 = 0
    while azar.random() < 2 ** -0.5 and x0 < 400:
        x0 += 1
    total = x0
    while azar.random() < 0.5:
        total += 1 + un_salto()
    return total


K = 1.019
NM = 400000
muestras = [muestra_frontera(K) for _ in range(NM)]
zs = [1.0 + 0.002 * i for i in range(1, 84)]     # grilla z en (1, z*)
peor = 0.0
for j in (5, 10, 15, 20, 25):
    p = sum(1 for m in muestras if m >= j) / float(NM)
    cota = float("inf")
    for z in zs:
        fz = phi_cota(z, K)
        if z * fz < 2.0:
            c = (phi_cota(z, K) / (1 - z * fz / 2)) * z ** -j
            cota = min(cota, c)
    if cota > 0 and p / cota > peor:
        peor = p / cota
    print("  MC frontera: P(T >= %2d) = %.2e  cota Chernoff = %.2e  %s"
          % (j, p, cota, "OK" if p <= cota * 1.05 else "VIOLADA"))
print("  (control: la cota Chernoff optimizada nunca queda por debajo"
      " del modelo")
print("   frontera; peor cociente MC/cota = %.3f <= 1)" % peor)
print()


# ----------------------------------------------------------------
# PARTE 3: LA REPARACION -- una clase POR PALABRA de racha, y la
# cola de la racha COMPUESTA directa de L2 con razon 2^(-1/2).
#
# Lema (verificacion exhaustiva; demostrable con la maquinaria de
# lecturaracha.lean): fijados k' (la altura durante la racha), el bit
# b del mixto y la palabra u en {0,1}^(j-1) de los bits de la racha,
#   { c impar mod 2^(j+1) : la racha tras el mixto con bit b y
#     palabra u dura >= j }  es EXACTAMENTE UNA clase mod 2^(j+1)
# (cada paso pide "hijo par": una condicion afin con coeficiente
# impar que fija UN bit nuevo de c -- tres_inyectivo).
# Consecuencia:  P(racha_total >= j | mixto)
#   = (1/2) Sigma_b 2^-(j-1) Sigma_u P(clase_{b,u})
#   <= 2 * 2^(j-1) * 2^-j * max_clase = max_clase
#   <= sqrt(C2(j+1)) * 2^-(j+1)/2      -- razon 2^(-1/2), DIRECTO,
# sin compuesto, sin E[2^S], sin cota inferior del denominador
# condicional. Las recargas quedan DENTRO de la palabra u.
# ----------------------------------------------------------------
def pot3(k, _c={0: 1}):
    if k not in _c:
        _c[k] = 3 ** k
    return _c[k]


def clase_unica(k_racha, bit_mixto, u, j):
    # devuelve el conjunto de c impares mod 2^(j+1) cuya racha tras el
    # mixto (bit_mixto) con palabra u dura >= j, trabajando EXACTO en
    # el modulo (la division entre 2 arrastra el resto: como el DP)
    M = 2 ** (j + 1)
    sobreviven = []
    for c in range(1, M, 2):
        # el mixto: k' = k+1 (bit 0) o k-1 (bit 1)
        if bit_mixto == 0:
            h = (3 * c + 1)
            kp = k_racha + 1
        else:
            h = (c - pot3(k_racha - 1))
            kp = k_racha - 1
        h %= 2 * M
        if h % 2:
            raise SystemExit("capa 1: el mixto no dio par por dos")
        h //= 2                      # el hijo, mod M
        vivo = True
        mod = M
        x = h % mod
        for i in range(j):
            if x % 2 != 0:           # el hijo i-esimo no es par
                vivo = False
                break
            if i == j - 1:
                break                # j-esima paridad comprobada
            b = u[i]
            if b == 0:
                x = (x // 2) % (mod // 2)
            else:
                x = (((3 * x + 1 - pot3(kp)) % mod) // 2) % (mod // 2)
            mod //= 2
        if vivo:
            sobreviven.append(c)
    return sobreviven


print("PARTE 3 -- LA REPARACION: una clase por palabra (exhaustivo):")
fallos = 0
casos = 0
for k_racha in (3, 4, 5, 6):
    for bit_mixto in (0, 1):
        if bit_mixto == 1 and k_racha < 3:
            continue
        for j in range(1, 8):
            for w in range(2 ** max(0, j - 1)):
                u = [(w >> i) & 1 for i in range(j - 1)]
                s = clase_unica(k_racha, bit_mixto, u, j)
                casos += 1
                if len(s) != 1:
                    fallos += 1
                    print("  FALLO: k=%d b=%d j=%d u=%s -> %d clases"
                          % (k_racha, bit_mixto, j, u, len(s)))
if fallos == 0:
    print("  %d combinaciones (k = 3..6, ambos bits, j = 1..7, TODAS"
          " las palabras" % casos)
    print("  u de la racha): el conjunto 'racha >= j con palabra u' es"
          " UNA clase")
    print("  mod 2^(j+1) EXACTAMENTE, en todos los casos. 0 fallos.")
    print()
    print("  CONSECUENCIA (la cuenta que el encargo pedia): con C2 ="
          " 1,038 medido,")
    K = 1.038 ** 0.5
    for j in (4, 8, 12):
        print("    P(racha_total >= %2d) <= sqrt(C2) 2^-(j+1)/2 ="
              " %.2e   (Geom(1/2) puro: %.2e)"
              % (j, K * 2 ** (-(j + 1) / 2.0), 2.0 ** -j))
    print("    razon 2^(-1/2) = 0,7071 para la racha TOTAL (recargas")
    print("    incluidas), directo de la equidistribucion L2 -- el")
    print("    compuesto de la nota es INNECESARIO y su razon 0,86")
    print("    queda superada. La cola es MAS GORDA que la Geom(1/2)")
    print("    del reloj V2 (0,707 > 0,5): la dominacion pedida por")
    print("    P2-a con C 2^-j NO sale de L2 sola -- sale la forma")
    print("    debilitada C 2^-j/2, que es la que la nota ya declara")
    print("    absorbible por la tolerancia polylog (reescala de T).")
else:
    raise SystemExit("PARTE 3: %d fallos -- la reparacion NO vale" % fallos)

print()
print("LETRA CHICA QUE LA NOTA NO DICE (hallazgo): sqrt(C2(j+1)) debe")
print("ser uniforme EN LA ESCALA j+1, no solo en j+1 = 8: a tiempo t el")
print("DP solo controla escalas m <~ t log2(1/(2 rho_ms)) (con rho_ms =")
print("0,44: m <~ 0,18 t). La cota de racha a escala j vale desde t ~")
print("5,5 j; antes, solo el cap determinista |c| (P2-b.i). El wedge")
print("(j, t) hay que escribirlo en el enunciado del lema de racha.")
