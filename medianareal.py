# medianareal.py
#
# LA MEDIANA UNIVERSAL, VERSION CADENA REAL -- el ciclo de prueba de
# la TRANSFERENCIA P2 (11-08-2026 (2), tras dejar L3/V2 teorema
# autocontenido en teoremav2.txt).
#
#   V2 demostro: la excursion condicionada a tau en [T, 2T], leida
#   desde la absorcion, converge a un objeto limite FIJO (la mediana
#   universal). La transferencia P2 pide que la CADENA REAL haga lo
#   mismo. Este fichero mide exactamente eso: excursiones de la
#   cadena (k, c) real (dinamica entera exacta, bits justos de
#   Terras -- la medida de clases), desde (2, c0), hasta la primera
#   entrada al fondo k <= 1, condicionadas a tau en [T, 2T] con
#   T = 30 ln c0 (las ventanas del teorema V2). Se mide la ley
#   condicionada de log10|u| = log10(|c|/3^k) en la entrada.
#
#   VEREDICTO BUSCADO: si los cuantiles condicionados son (casi)
#   INDEPENDIENTES de c0 -- tres decadas de arranque distintas --
#   el objeto limite existe tambien en la cadena real y la
#   transferencia tiene su mecanismo medido (la version condicionada
#   del "olvido del arranque" que la mezcla del 10-08 (6d) vio sin
#   condicionar). Si los cuantiles derivan con c0, la transferencia
#   tiene un obstaculo real y hay que saberlo.
#
#   Arranques: PRIMOS no redondos (la leccion del punto 8 de la
#   lista: 2^j y 10^k caen en clases especiales; un primo no), con
#   c0 % 3 != 0 (los alcanzables de Cabras) y c0 impar.
#
#   COMPROBACIONES (SystemExit):
#     C1  la balota real: P(tau > T) * sqrt(T) en [0,3, 3] para los
#         tres arranques (el paseo real es martingala con empuje de
#         borde: la forma c/sqrt(T) debe sobrevivir).
#     C2  EL VEREDICTO: la mediana condicionada de log10|u| entre el
#         arranque chico y el grande difiere menos de 0,5 (media
#         decada) -- la escala de |u| al fondo NO recuerda c0.
#     C3  el signo de la deriva: entre chico y grande la mediana no
#         crece mas de lo que baja... (informativo: se imprime la
#         tabla entera de cuantiles; C2 es el corte duro).
#
#   Semillas fijas; dinamica entera exacta (cero floats en la
#   trayectoria; el float aparece solo al formar log10|u| final).

import random
import math

ARRANQUES = [997, 999983, 999999937]   # primos, impares, % 3 != 0
OBJETIVO = [2500, 1500, 900]
TOPE_CORRIDAS = 3 * 10 ** 6
SEMILLA = 20260813
CUANTILES = [10, 25, 50, 75, 90]
LOG3 = math.log10(3.0)


def pot3(k, _cache={0: 1}):
    if k not in _cache:
        _cache[k] = 3 ** k
    return _cache[k]


def transicion(k, c, bit):
    if k == 0:
        if c % 2 == 0:
            return (0, c // 2) if bit == 0 else (0, 3 * c // 2)
        return (1, (3 * c + 1) // 2) if bit == 0 else (1, (1 - 3 * c) // 2)
    if c % 2 == 0:
        return (k, c // 2) if bit == 0 else (k, (3 * c + 1 - pot3(k)) // 2)
    if bit == 0:
        return (k + 1, (3 * c + 1) // 2)
    if k >= 2:
        return (k - 1, (c - pot3(k - 1)) // 2)
    g = (c - 1) // 2
    if g == 0:
        return None                    # fusion (vortice): fondo tambien
    return (0, abs(g))


def log10_abs_u(k, c):
    if c == 0:
        return float('-inf')
    ac = abs(c)
    # log10|c| robusto para enteros grandes
    if ac.bit_length() < 900:
        lc = math.log10(ac)
    else:
        b = ac.bit_length()
        lc = (b - 60) * math.log10(2.0) + math.log10(ac >> (b - 60))
    return lc - k * LOG3


def cuantil(datos, p):
    s = sorted(datos)
    return s[max(0, min(len(s) - 1, int(round(p / 100.0 * (len(s) - 1)))))]


print("LA MEDIANA UNIVERSAL EN LA CADENA REAL (el test de P2)")
print("excursiones (2, c0) -> fondo k <= 1, condicionadas a")
print("tau en [T, 2T], T = 30 ln c0; se mide log10|u| a la entrada")
print()
print("   c0          T     muestras  corridas  P(tau>T)sqrt(T)  " +
      "cuantiles 10/25/50/75/90 de log10|u|")
resultados = {}
for c0, objetivo in zip(ARRANQUES, OBJETIVO):
    T = int(round(30 * math.log(c0)))
    azar = random.Random(SEMILLA + c0)
    muestra = []
    corridas = 0
    supera_T = 0
    while len(muestra) < objetivo and corridas < TOPE_CORRIDAS:
        corridas += 1
        k, c = 2, c0
        tau_fin = None
        for t in range(1, 2 * T + 1):
            r = transicion(k, c, azar.getrandbits(1))
            if r is None:
                k, c = 1, 1            # el vortice ES fondo (k = 1)
                tau_fin = t
                break
            k, c = r
            if k <= 1:
                tau_fin = t
                break
        if tau_fin is None:
            supera_T += 1
            continue
        if tau_fin > T:
            supera_T += 1
        if T <= tau_fin <= 2 * T:
            muestra.append(log10_abs_u(k, c))
    balota = (supera_T / float(corridas)) * math.sqrt(T)
    if not (0.3 <= balota <= 3.0):
        raise SystemExit("C1: balota real %.3f fuera de [0,3, 3] en c0 = %d"
                         % (balota, c0))
    qs = {p: cuantil(muestra, p) for p in CUANTILES}
    resultados[c0] = qs
    print("  %10d  %4d  %7d  %8d      %.3f        %s"
          % (c0, T, len(muestra), corridas, balota,
             "/".join("%+.2f" % qs[p] for p in CUANTILES)), flush=True)

print()
print("COMPROBACION 1 OK: la balota real aguanta en los tres arranques.")
med_chico = resultados[ARRANQUES[0]][50]
med_grande = resultados[ARRANQUES[-1]][50]
deriva = abs(med_grande - med_chico)
print()
print("la deriva de la mediana condicionada de log10|u|:")
for c0 in ARRANQUES:
    print("  c0 = %10d:  mediana = %+.3f" % (c0, resultados[c0][50]))
if deriva > 0.5:
    raise SystemExit("C2: la mediana deriva %.2f decadas entre arranques "
                     "(> 0,5): la ley condicionada RECUERDA c0" % deriva)
print("COMPROBACION 2 OK: la mediana condicionada deriva %.2f decadas"
      % deriva)
print("entre c0 = %d y c0 = %d (< 0,5)." % (ARRANQUES[0], ARRANQUES[-1]))
print("LECTURA HONESTA (corregida por la 9a, C-9 del adv 1): a")
print("T = 30 ln c0 el termino de memoria prod*x esta muerto DE ANTEMANO")
print("por el margen de la Pieza 2 para cualquier cadena de estos")
print("multiplicadores -- esa mitad del veredicto es del disenio, no de")
print("la cadena. El contenido discriminante es la estabilidad de la")
print("parte W, confirmada ademas a T EMPAREJADO por la malla 2x2 de la")
print("9a (real y V2b coinciden a +-0,03 en las cuatro celdas).")
print()
print("Etiqueta: medicion, no teorema; el reloj real es endogeno (v2)")
print("y la dominacion por rachas geometricas (tortolas.lean) sigue")
print("siendo el paso analitico pendiente de P2.")
