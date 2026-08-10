# moscas.py
#
# EL TEOREMA DE MOSCAS - LA TENSION, TRANSFERIDA (04-08-2026): las
# moscas no se escapan de la telarana. La tension de la estacionaria
# del IFS de Aranas pasa a la cadena real como COTA UNIFORME EN t,
# incondicional y con constante explicita -- sin citar a Kesten:
# autocontenido con subaditividad.
#
#   TEOREMA. Sea S_t(theta) = suma sobre las palabras VIVAS de largo t
#   de 2^(-t) |u_t|^theta (u = c/3^k, la coordenada de Aranas), para
#   0 < theta < 1. Entonces:
#
#   (a) [EXACTO, por transicion] en TODO estado vivo (nucleo, frontera,
#       salida, F4 incluido):  |u'| <= m_b |u| + d  con
#       (m_0, m_1) = (1/2, 3/2) y d <= 1/2.
#       (F4, el vuelco que rompia el acople de Aranas, aqui es
#       INOFENSIVO: su pendiente es 1/2 <= 3/2.)
#
#   (b) [subaditividad, estandar] |x + y|^theta <= |x|^theta + |y|^theta
#       para 0 < theta <= 1; promediando la moneda:
#
#       S_{t+1} <= r_theta S_t + (1/2)^theta,
#       r_theta = ((1/2)^theta + (3/2)^theta) / 2  <  1.
#
#       (La absorcion solo QUITA terminos: la desigualdad sobrevive.
#       Y r_theta < 1 para todo theta en (0,1) porque E[m] = 1 es
#       exactamente la criticidad kappa = 1 de Tigresas: la ventana
#       entera de momentos fraccionarios queda abierta.)
#
#   (c) COROLARIO (LA TENSION):  S_t <= r^t S_0 + (1/2)^theta/(1-r)
#       para TODO t -- uniforme -- y por Markov, la masa viva con
#       |u| > x es <= B_theta / x^theta, con B explicita.
#       theta = 1/2:  r = 0,9659,  B <= 21,5.
#       theta = 0,9:  r = 0,9881,  B <= 46,0.
#
#   LO QUE NO DA (la honestidad por delante): (1) la tension del
#   CONDICIONAL a vivo si phi = 1 (la masa viva se iria a 0 y el
#   cociente pierde la cota); (2) el PISO de absorcion por visita.
#   El piso es la pieza abierta final del programa.
#
#   ⇢ EXTENSION DE LA 6a REVISION (09-08-2026, actarevision0908c.txt):
#   la dominacion (a) y por tanto (b), (c) y la cota uniforme B_theta
#   valen VERBATIM para la cadena MODIFICADA (el vortice rebotado a
#   (2,2), sobre la que razona el criterio de retorno): el rebote
#   multiplica |u| por 2/3 y cumple |u'| <= m_bit|u| + 1/2 en los dos
#   bits, y (2/3)^theta <= r_theta para todo theta en (0,1) (2/3 <
#   sqrt(3)/2 = GM de {1/2, 3/2} y AM >= GM): la ventana de Lyapunov
#   lo absorbe. Verificado en rondadeltronco.py PARTE 2 (84.020
#   transiciones con el rebote incluido, 0 fallos).
#
#   Verificacion: (a) exacto con Fraction en rejilla amplia; (b)-(c)
#   sobre la cadena real, midiendo S_t nivel a nivel y comprobando la
#   recursion y la cota; y el corolario de cola contra lo medido.

from fractions import Fraction
import math

PROF = 34
TOPE_ESTADOS = 9 * 10 ** 6


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
# T1: LA DOMINACION LINEAL EXACTA:  |u'| <= m_b |u| + 1/2, con
#     (m_0, m_1) = (1/2, 3/2), en todo estado vivo. Fraction, sin floats.
# ---------------------------------------------------------------------------

MEDIO = Fraction(1, 2)
TRESMEDIOS = Fraction(3, 2)
probadas = 0
for k in range(0, 10):
    for c in range(1 if k == 0 else -3 ** (k + 1), 3 ** (k + 1) + 1):
        if k == 0 and c < 1:
            continue
        u = Fraction(c, 3 ** k) if k >= 1 else Fraction(c)
        for bit, m in ((0, MEDIO), (1, TRESMEDIOS)):
            s = transicion(k, c, bit)
            if s[0] == 'fusion':
                continue
            k2, c2 = s[1], s[2]
            u2 = Fraction(c2, 3 ** k2) if k2 >= 1 else Fraction(c2)
            if abs(u2) > m * abs(u) + MEDIO:
                raise SystemExit("T1: k=%d c=%d bit=%d |u'|=%s > %s"
                                 % (k, c, bit, abs(u2), m * abs(u) + MEDIO))
            probadas += 1

print("T1 OK -- LA DOMINACION LINEAL: |u'| <= m_b |u| + 1/2 con")
print("(m_0, m_1) = (1/2, 3/2), en %d transiciones exactas (Fraction," % probadas)
print("k <= 9, |c| <= 3^(k+1), frontera y F4 incluidos, 0 fallos).")
print("El vuelco F4 (pendiente 1/2 en el bit expansor) queda dominado.")

# ---------------------------------------------------------------------------
# T2: LA RECURSION DE LYAPUNOV SOBRE LA CADENA REAL.
#     S_t(theta) medida nivel a nivel; se comprueba
#     S_{t+1} <= r_theta S_t + (1/2)^theta  y  S_t <= B_theta.
# ---------------------------------------------------------------------------

THETAS = (0.5, 0.9)
r = {th: (0.5 ** th + 1.5 ** th) / 2 for th in THETAS}
B = {th: 1.0 + 0.5 ** th / (1 - r[th]) for th in THETAS}

estados = {(0, 1): 1}
S_hist = {th: [] for th in THETAS}
for t in range(1, PROF + 1):
    nuevo = {}
    for (k, c), n in estados.items():
        for bit in (0, 1):
            s = transicion(k, c, bit)
            if s[0] == 'fusion':
                continue
            clave = (s[1], s[2])
            nuevo[clave] = nuevo.get(clave, 0) + n
    estados = nuevo
    if len(estados) > TOPE_ESTADOS:
        raise SystemExit("tope en t=%d" % t)
    for th in THETAS:
        S = sum(n * abs(c / 3 ** k if k >= 1 else float(c)) ** th
                for (k, c), n in estados.items()) / 2.0 ** t
        S_hist[th].append(S)

print()
print("T2: la recursion de Lyapunov sobre la cadena real:")
for th in THETAS:
    ok_rec = ok_cota = True
    for i in range(len(S_hist[th]) - 1):
        if S_hist[th][i + 1] > r[th] * S_hist[th][i] + 0.5 ** th + 1e-9:
            ok_rec = False
        if S_hist[th][i] > B[th]:
            ok_cota = False
    if not (ok_rec and ok_cota):
        raise SystemExit("T2: theta=%.1f recursion=%s cota=%s"
                         % (th, ok_rec, ok_cota))
    print("  theta = %.1f:  r = %.4f  B_teorica = %5.1f  S_t medida en "
          "[%.3f, %.3f]  (recursion y cota: OK los %d niveles)"
          % (th, r[th], B[th], min(S_hist[th]), max(S_hist[th]), PROF))

print()
print("T2 OK: S_t se queda MUY por debajo de la cota (el teorema es")
print("holgado) y la recursion S' <= r S + (1/2)^theta se cumple nivel")
print("a nivel. LA TENSION ES UNIFORME EN t: teorema con constante.")

# ---------------------------------------------------------------------------
# T3: EL COROLARIO DE COLA contra lo medido (t = PROF).
# ---------------------------------------------------------------------------

total_ini = 2 ** PROF
print()
print("T3: masa viva con |u| > x (fraccion de TODAS las palabras, t = %d):" % PROF)
print("      x     medida      cota th=0.5   cota th=0.9")
for x in (4, 16, 64, 256, 1024):
    p = sum(n for (k, c), n in estados.items()
            if abs(c / 3 ** k if k >= 1 else float(c)) > x) / 2.0 ** PROF
    print("  %5d   %.6f      %8.4f      %8.4f"
          % (x, p, min(1.0, B[0.5] / x ** 0.5), min(1.0, B[0.9] / x ** 0.9)))

print()
print("VEREDICTO DE MOSCAS: la tension de Aranas TRANSFERIDA a la cadena")
print("real -- cota uniforme en t, incondicional, con constante explicita")
print("y sin hipotesis externas (subaditividad + la moneda de Tigresas).")
print("Lo que queda abierto, dicho con todas las letras: (1) si phi = 1,")
print("el condicional a vivo pierde la cota (la masa viva se va a 0);")
print("(2) el PISO de absorcion por visita. El piso es la ultima pieza.")
