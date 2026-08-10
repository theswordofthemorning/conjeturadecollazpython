# gaviotas.py
#
# LA COTA MARTINGALA DE LA MONEDA CONDICIONADA (10-08-2026; teorema
# propuesto: GAVIOTAS -- siguen al barco a cualquier horizonte; el
# bautizo es del usuario). El "ultimo paso" del acta de la 5a
# revision, ACOTADO con demostracion completa a T fijo: la
# endogeneidad del horario (el hueco declarado en maquinaria.txt,
# objetivo 6) DESAPARECE del argumento.
#
#   TEOREMA (GAVIOTAS). En la cadena modificada con la medida de
#   palabras (cada bit una moneda justa independiente), sea F
#   cualquier evento del nivel T (aqui: el fondo k <= 1), sea
#   M_s = E[1_F | F_s] la martingala cerrada de Doob, sea eps_s el
#   bit +-1 del paso s si es MONEDA (c par) y 0 si no, y sean
#
#       N_c = E[numero de pasos-moneda en 0..T-1]
#       V_c = Sigma_s E[ (M_{s+1} - M_s)^2 ; paso s moneda ]
#
#   Entonces
#
#       | E[ (Ee - E0) * 1_F ] |  <=  sqrt( N_c * V_c )
#
#   y ademas V_c <= Sigma_s E[(M_{s+1}-M_s)^2] = Var(1_F) = P(1-P)
#   (la ortogonalidad de los incrementos de martingala, EXACTA).
#
#   DEMOSTRACION (ocho lineas, sin nada de Collatz):
#   (1) "ser moneda en s" es F_s-medible y el bit es justo e
#       independiente del pasado => E[eps_s | F_s] = 0.
#   (2) E[eps_s * 1_F] = E[eps_s * M_{s+1}]  (torre sobre F_{s+1})
#       = E[eps_s * (M_{s+1} - M_s)]         (por (1), E[eps M_s]=0).
#   (3) Ee - E0 = Sigma_s eps_s, luego
#       E[(Ee-E0) 1_F] = Sigma_s E[eps_s dM_s]
#       <= Sigma_s sqrt(E[eps_s^2]) sqrt(E[dM_s^2; moneda])
#       <= sqrt(Sigma E[eps^2]) * sqrt(Sigma E[dM^2; moneda])
#       = sqrt(N_c * V_c)                     (Cauchy-Schwarz dos veces,
#                                              eps_s^2 = 1_moneda).
#   (4) Sigma_s E[dM_s^2] = Var(M_T) - Var(M_0) = Var(1_F). QED.
#
#   POR QUE IMPORTA. El "ultimo paso" pedia acotar el desbalance de
#   la moneda condicionada al fondo bajo el umbral efectivo ~0,2446
#   por paso. Este teorema lo CERTIFICA a T fijo con aritmetica
#   exacta (abajo: a_D <= 0,074 ya en T = 24, y la cota BAJA con T),
#   y SIN el hueco de la endogeneidad: no usa horario producto, no
#   usa Efron-Stein, no usa CLT local -- solo bits justos dado el
#   pasado (exacto en la medida de clases de Leonas), Doob y
#   Cauchy-Schwarz. Para el limite T -> infinito la cota da
#   a_D <= sqrt(N_c V_c)/(P(F) T): con N_c ~ 0,44 T, V_c <= P(1-P) y
#   P(F) ~ c/sqrt(T) (medido; el lema local inferior es el pendiente)
#   sale a_D = O(T^(-1/4)) -> 0. La medicion fina (GARZAS, nucleo de
#   sensibilidad) dice que la verdad es aun mejor (~log T / T); esta
#   cota es la DEMOSTRADA.
#
#   Relacion con URRACAS: alli quedo aislado "el desbalance de UNA
#   moneda justa condicionada"; aqui esa esperanza queda acotada por
#   la energia de la martingala del propio evento. Las gaviotas
#   siguen al barco: la informacion que la moneda puede cargar sobre
#   el fondo esta limitada por la varianza del fondo mismo.
#
# COMPROBACIONES (SystemExit antes de concluir):
#   C1  conservacion de masa 2^s.
#   C2  LA ORTOGONALIDAD, EXACTA EN RACIONALES: Sigma_s E[dM^2] ==
#       P(F)(1 - P(F)) como igualdad de Fraction, en cada T probado.
#   C3  el cruce con monedacondicionada.py: a_D(T = 24) = 0,009087 y
#       a_D(T = 28) = 0,008330 reproducidos (6 cifras).
#   C4  la cota se cumple con holgura: |E[(Ee-E0)1_F]| <= sqrt(N_c V_c)
#       en cada T, y en T >= 24 la cota condicionada por paso queda
#       POR DEBAJO del umbral efectivo 0,2446.
#
# Mapa del ATAJO via la cadena de Leonas modificada; enteros y
# racionales exactos.

from fractions import Fraction
import math
import time

T_MAX = 28
TES = (16, 20, 24, 28)
FONDO_K = 1
UMBRAL_EFECTIVO = 0.2446
CRUCE_GARZAS = {24: 0.009087, 28: 0.008330}   # a_D de monedacondicionada.py


def transicion_mod(k, c, bit):
    # la cadena de Leonas con el vortice rebotado (identica a
    # retorno11.py / monedacondicionada.py / firmaacoplamiento.py)
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
for s in range(T_MAX + 1):
    if sum(niveles[s].values()) != 2 ** s:
        raise SystemExit("C1: masa no conservada en s = %d" % s)
print("C1 OK: masa 2^s conservada en los %d niveles." % (T_MAX + 1))
print()
print("   T    P(F)      E[(Ee-E0)1_F]   sqrt(Nc*Vc)   holgura   "
      "cota a_D      a_D real")

filas = []
for T in TES:
    gama = dict((x, 1 if x[0] <= FONDO_K else 0) for x in niveles[T])
    F = sum(niveles[T][x] * g for x, g in gama.items())
    S_eed = 0
    var_total = Fraction(0)
    var_moneda = Fraction(0)
    n_moneda = 0
    for s in range(T - 1, -1, -1):
        gnuevo = {}
        for x, a in niveles[s].items():
            k, c = x
            h0 = transicion_mod(k, c, 0)
            h1 = transicion_mod(k, c, 1)
            g0 = gama.get(h0, 0)
            g1 = gama.get(h1, 0)
            gnuevo[x] = g0 + g1
            d = g1 - g0
            # dM = +-(g1-g0)/2^(T-s) segun el bit, cada uno prob 1/2:
            # E[dM^2] suma a/2^s * d^2/4^(T-s)
            contrib = Fraction(a * d * d, 2 ** s * 4 ** (T - s))
            var_total += contrib
            if (not (k == 1 and c == 1)) and c % 2 == 0:
                var_moneda += contrib
                S_eed += a * d
                n_moneda += a * 2 ** (T - s)
        gama = gnuevo
    P = Fraction(F, 2 ** T)
    # C2: la ortogonalidad, exacta en racionales
    if var_total != P * (1 - P):
        raise SystemExit("C2 (T=%d): Sigma E[dM^2] != P(1-P)" % T)
    Nc = Fraction(n_moneda, 2 ** T)
    sesgo = Fraction(S_eed, 2 ** T)
    cota = math.sqrt(float(Nc) * float(var_moneda))
    a_d = float(sesgo / P) / T
    cota_ad = cota / float(P) / T
    # C3: el cruce con GARZAS
    if T in CRUCE_GARZAS and abs(a_d - CRUCE_GARZAS[T]) > 2e-6:
        raise SystemExit("C3 (T=%d): a_D = %.6f, GARZAS dio %.6f"
                         % (T, a_d, CRUCE_GARZAS[T]))
    # C4: la cota se cumple
    if abs(float(sesgo)) > cota:
        raise SystemExit("C4 (T=%d): la cota no se cumple" % T)
    filas.append((T, cota_ad))
    print("  %2d   %.4f      %+.6f      %.4f      x%4.1f    %.5f      %.6f"
          % (T, float(P), float(sesgo), cota, cota / abs(float(sesgo)),
             cota_ad, a_d))

print()
print("C2 OK: la ortogonalidad Sigma E[dM^2] = P(1-P) es IGUALDAD EXACTA")
print("de racionales en los %d valores de T (el descuadre mas minimo" % len(TES))
print("delataria un error en gama o en la contabilidad de incrementos).")
print("C3 OK: a_D reproducido contra monedacondicionada.py en T = 24, 28.")
for T, cota_ad in filas:
    if T >= 24 and cota_ad >= UMBRAL_EFECTIVO:
        raise SystemExit("C4: la cota por paso no baja del umbral en T=%d" % T)
print("C4 OK: la cota vale en todo T probado, y desde T = 24 la cota")
print("condicionada POR PASO queda bajo el umbral efectivo 0,2446:")
print("a_D <= %.4f en T = 24 y a_D <= %.4f en T = 28 -- CERTIFICADO"
      % (filas[2][1], filas[3][1]))
print("con desigualdad demostrada + aritmetica exacta, sin lemas")
print("pendientes a T fijo.")

print()
print("VEREDICTO: el 'ultimo paso' (acotar el desbalance de la moneda")
print("condicionada bajo ~0,2446 por paso) tiene ahora COTA DEMOSTRADA a")
print("T fijo -- sin horario producto, sin Efron-Stein, sin CLT local:")
print("bits justos dado el pasado (exacto en la medida de clases) + Doob")
print("+ Cauchy-Schwarz. La cota baja con T (%s" % " / ".join(
    "%.4f" % c for _, c in filas))
print("en T = %s); para T -> infinito, con N_c ~ 0,44 T y" % (
    ", ".join(str(T) for T, _ in filas)))
print("P(F) ~ c/sqrt(T) (medido), da a_D = O(T^(-1/4)) -> 0. El unico")
print("pendiente asintotico es el lema local inferior P(F) >= c/sqrt(T);")
print("a T fijo no hay pendiente ninguno.")
print("%.0fs" % (time.time() - t0))
