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
#   TEOREMA B (GAVIOTAS-SUMA -- la correccion 50, cazada por la
#   revision de Opus 5 el mismo dia). El umbral 0,2446 del corolario
#   de URRACAS es sobre LA SUMA a_V + a_D - a_K, no sobre a_D solo --
#   comparar a_D contra el es comparar una parte contra el umbral del
#   todo. La respuesta de fondo: EL MISMO argumento acota la suma
#   entera, porque en el libro de URRACAS el paso del vortice tambien
#   es una moneda CENTRADA (bit 0 = tipo 6 contractivo, bit 1 = tipo
#   9 expansivo), igual que los mixtos (tipos 6/7/8) y las monedas
#   (1/2/4/5); el UNICO paso no centrado es el tipo 3 (frontera
#   impar: contractivo seguro), que RESTA. Con eta_s = +-1 el signo
#   expansivo del paso s:
#
#       exp - contr = Sigma_{s no tipo 3} eta_s  -  #tipo3,
#       E[eta_s | F_s] = 0 en todos los sumandos,
#
#   y como  a_V + a_D - a_K = (exp - contr)/T  (URRACAS con k0 = 0):
#
#       E[a_V + a_D - a_K | F]  <=  sqrt(N' * V') / (P(F) * T),
#
#   con N' = pasos centrados esperados (<= T) y V' = energia de
#   martingala de los pasos centrados (<= Var(1_F)). a_V NO necesita
#   cota aparte: queda absorbido en la martingala.
#
#   Y LA FORMA FINA, que es la que muerde: sin descartar el termino
#   de ayuda,
#
#       E[suma | F]  <=  ( sqrt(N' V') - E[#tipo3 * 1_F] ) / (P(F) T)
#
#   donde E[#tipo3 * 1_F] se computa EXACTO (la ocupacion condicionada
#   de la frontera impar). MEDIDO ABAJO: la cota fina da 0,198 /
#   0,196 / 0,194 / 0,192 en T = 16, 20, 24, 28 -- LA SUMA ENTERA
#   a_V + a_D - a_K queda CERTIFICADA POR DEBAJO del umbral efectivo
#   0,2446 en todos los T computados, bajando con T.
#
#   POR QUE IMPORTA, con las etiquetas honestas de la correccion 50:
#   (1) a_D solo (teorema A): <= 0,070-0,085 -- pero el umbral es de
#       LA SUMA: la parte sola no cierra nada (esa era la correccion);
#   (2) LA SUMA (teorema B fino): certificada bajo 0,2446 a todo T
#       computado, con desigualdad demostrada + aritmetica exacta;
#       a_V queda ABSORBIDO en la martingala (el vortice es moneda
#       centrada) y la frontera impar AYUDA (resta determinista);
#   (3) lo demostrado sin hueco de endogeneidad son LAS
#       DESIGUALDADES a T fijo; el cierre asintotico (suma < umbral
#       para TODO T grande) sigue dependiendo del lema local inferior
#       P(F) >= c/sqrt(T) (la cota cruda sqrt(N'V')/(P T) ~ T^(-1/4)
#       -> 0 y la ayuda t3 solo mejora). La medicion fina dice que la
#       verdad es mucho mejor (suma real ~0,019); estas cotas son las
#       DEMOSTRADAS.
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
print("   T    P(F)     cota a_D   a_D real    COTA FINA   suma real   ayuda t3")
print("                                        (de la suma)")

filas = []
for T in TES:
    gama = dict((x, 1 if x[0] <= FONDO_K else 0) for x in niveles[T])
    F = sum(niveles[T][x] * g for x, g in gama.items())
    S_eed = 0
    S_expcontr = 0
    S_tipo3 = 0
    var_total = Fraction(0)
    var_moneda = Fraction(0)
    var_centrada = Fraction(0)
    n_moneda = 0
    n_centrada = 0
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
            tipo3 = (k == 0 and c % 2 == 1)
            if not tipo3:
                # paso CENTRADO: bit 1 = expansivo, bit 0 = contractivo
                # (monedas 1/2/4/5, mixtos 6/7/8, y el vortice 6/9)
                var_centrada += contrib
                n_centrada += a * 2 ** (T - s)
                S_expcontr += a * d
            else:
                S_expcontr -= a * (g0 + g1)
                S_tipo3 += a * (g0 + g1)
            if (not (k == 1 and c == 1)) and c % 2 == 0:
                var_moneda += contrib
                S_eed += a * d
                n_moneda += a * 2 ** (T - s)
        gama = gnuevo
    P = Fraction(F, 2 ** T)
    # C2: la ortogonalidad, exacta en racionales
    if var_total != P * (1 - P):
        raise SystemExit("C2 (T=%d): Sigma E[dM^2] != P(1-P)" % T)
    sesgo = Fraction(S_eed, 2 ** T)
    cota_eed = math.sqrt(float(Fraction(n_moneda, 2 ** T)) * float(var_moneda))
    a_d = float(sesgo / P) / T
    cota_ad = cota_eed / float(P) / T
    suma_real = float(Fraction(S_expcontr, 2 ** T) / P) / T
    cota_expcontr = math.sqrt(float(Fraction(n_centrada, 2 ** T))
                              * float(var_centrada))
    cota_suma = cota_expcontr / float(P) / T
    ayuda_t3 = float(Fraction(S_tipo3, 2 ** T) / P) / T
    # C3: el cruce con GARZAS
    if T in CRUCE_GARZAS and abs(a_d - CRUCE_GARZAS[T]) > 2e-6:
        raise SystemExit("C3 (T=%d): a_D = %.6f, GARZAS dio %.6f"
                         % (T, a_d, CRUCE_GARZAS[T]))
    cota_fina = cota_suma - ayuda_t3
    # C4: las cotas se cumplen sobre sus valores reales, y la FINA baja
    # del umbral en todo T
    if abs(float(sesgo)) > cota_eed or suma_real > cota_fina:
        raise SystemExit("C4 (T=%d): una cota no se cumple" % T)
    if cota_fina >= UMBRAL_EFECTIVO:
        raise SystemExit("C4 (T=%d): la cota fina %.4f no baja del umbral"
                         % (T, cota_fina))
    filas.append((T, cota_ad, cota_suma, suma_real, cota_fina))
    print("  %2d   %.4f    %.5f    %.6f     %.5f    %.6f    %.5f"
          % (T, float(P), cota_ad, a_d, cota_fina, suma_real, ayuda_t3))

print()
print("C2 OK: la ortogonalidad Sigma E[dM^2] = P(1-P) es IGUALDAD EXACTA")
print("de racionales en los %d valores de T." % len(TES))
print("C3 OK: a_D reproducido contra monedacondicionada.py en T = 24, 28.")
print("C4 OK: las cotas valen sobre sus valores reales en todo T probado,")
print("y LA COTA FINA DE LA SUMA baja del umbral 0,2446 en TODOS los T:")
print("%s" % "   ".join("T=%d: %.4f" % (f[0], f[4]) for f in filas))

print()
print("VEREDICTO, con las etiquetas de la correccion 50:")
print("1) El umbral 0,2446 es de LA SUMA a_V + a_D - a_K, no de a_D solo")
print("   (la correccion, cazada por la revision de Opus 5): la cota A")
print("   sobre a_D (%.4f en T = 28) por si sola no cierra nada." % filas[-1][1])
print("2) LA RESPUESTA DE FONDO (teorema B): el mismo argumento acota la")
print("   suma entera -- el vortice es moneda centrada (tipos 6/9), a_V")
print("   queda ABSORBIDO en la martingala, y la frontera impar (tipo 3,")
print("   contractiva segura) RESTA. La cota fina certifica la suma")
print("   bajo el umbral en todos los T computados (%.4f en T = 28," % filas[-1][4])
print("   contra el valor real %.4f: holgura x%.0f del umbral abajo)."
      % (filas[-1][3], (UMBRAL_EFECTIVO - filas[-1][3])
         / max(UMBRAL_EFECTIVO - filas[-1][4], 1e-9)))
print("3) Lo demostrado sin hueco de endogeneidad son LAS DESIGUALDADES")
print("   a T fijo; el cierre asintotico (para TODO T grande) depende")
print("   del lema local inferior P(F) >= c/sqrt(T): la cota cruda es")
print("   O(T^(-1/4)) -> 0 y la ayuda t3 solo mejora.")
print("%.0fs" % (time.time() - t0))
