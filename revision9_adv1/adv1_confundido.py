# adv1_confundido.py -- 9a revision, adversario 1
#
# ATAQUE 5 contra medianareal.py: el disenio confunde c0 con T.
# Los tres arranques se midieron cada uno a SU T = 30 ln c0 (207/414/
# 622): c0 y T crecen JUNTOS, y el propio modelo V2 tiene un
# transitorio en T (mediana fwd 12,8 -> 17,8 entre T = 100 y 6400 en
# medianauniversal_salida.txt). La deriva medida (+0,07 decadas)
# puede ser el transitorio compartido y no "olvido de c0".
#
# El desconfundido: la MISMA c0 a T distintos y DISTINTAS c0 al mismo
# T, en malla cruzada:
#   (c0 = 997,        T = 207)   la celda publicada chica
#   (c0 = 997,        T = 622)   c0 chica al T de la grande
#   (c0 = 999999937,  T = 207)   c0 grande al T de la chica  <- AQUI
#       la prediccion adversarial: a T = 207 la contraccion forzada
#       solo mata ~e^{-15} y prod*u0 ~ 40 >> W: la ley DEBE recordar
#       c0 -- si lo hace, "la ley no recuerda el arranque" es un
#       artefacto del emparejamiento T = 30 ln c0, no una propiedad
#       de la cadena.
#   (c0 = 999999937,  T = 622)   la celda publicada grande
# Y la CALIBRACION V2b: el modelo autonomo con u0 = c0/9 en las
# mismas cuatro celdas -- si V2b reproduce la tabla real celda a
# celda, lo que medianareal.py vio es el transitorio de V2, y su
# veredicto ("olvido") es la parte tautologica del disenio.
#
# Semillas fijas y declaradas; dinamica entera exacta en la cadena.

import math
import random

SEMILLA = 20260901                     # propia del adversario
CELDAS = [(997, 207), (997, 622), (999999937, 207), (999999937, 622)]
OBJETIVO = 1200
TOPE_CORRIDAS = 3 * 10 ** 6
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
        return None
    return (0, abs(g))


def log10_abs_u(k, c):
    if c == 0:
        return float('-inf')
    ac = abs(c)
    if ac.bit_length() < 900:
        lc = math.log10(ac)
    else:
        b = ac.bit_length()
        lc = (b - 60) * math.log10(2.0) + math.log10(ac >> (b - 60))
    return lc - k * LOG3


def cuantil(datos, p):
    s = sorted(datos)
    return s[max(0, min(len(s) - 1, int(round(p / 100.0 * (len(s) - 1)))))]


def celda_real(c0, T, objetivo):
    azar = random.Random(SEMILLA + c0 + 1000 * T)
    muestra = []
    corridas = 0
    while len(muestra) < objetivo and corridas < TOPE_CORRIDAS:
        corridas += 1
        k, c = 2, c0
        tau_fin = None
        for t in range(1, 2 * T + 1):
            r = transicion(k, c, azar.getrandbits(1))
            if r is None:
                k, c = 1, 1
                tau_fin = t
                break
            k, c = r
            if k <= 1:
                tau_fin = t
                break
        if tau_fin is not None and T <= tau_fin <= 2 * T:
            muestra.append(log10_abs_u(k, c))
    return muestra, corridas


def celda_v2b(c0, T, objetivo):
    # el modelo autonomo V2b (rachas Geom(1/2)) con u0 = c0/9,
    # exito medido igual: log10|u| a la absorcion, tau en [T, 2T]
    azar = random.Random(SEMILLA + c0 + 1000 * T + 7)
    muestra = []
    corridas = 0
    while len(muestra) < objetivo and corridas < TOPE_CORRIDAS:
        corridas += 1
        k, u = 2, c0 / 9.0
        compartidos = 0
        while azar.getrandbits(1):
            compartidos += 1
        tau_fin = None
        for t in range(1, 2 * T + 1):
            bit = azar.getrandbits(1)
            if compartidos == 0:
                es_mixto = True
                j = 0
                while azar.getrandbits(1):
                    j += 1
                compartidos = j
            else:
                es_mixto = False
                compartidos -= 1
            u = u / 2.0 if bit == 0 else (3.0 * u - 1.0) / 2.0
            if es_mixto:
                k += 1 if bit == 0 else -1
                if k <= 1:
                    tau_fin = t
                    break
        if tau_fin is not None and T <= tau_fin <= 2 * T:
            if u == 0.0:
                muestra.append(float('-inf'))
            else:
                muestra.append(math.log10(abs(u)))
    return muestra, corridas


print("ADV1 -- EL DESCONFUNDIDO DE medianareal.py (malla cruzada c0 x T)")
print("cuantiles 10/25/50/75/90 de log10|u| condicionado a tau en [T,2T]")
print()
print("celda            REAL (cadena entera)          V2B (modelo, u0=c0/9)")
for c0, T in CELDAS:
    m_real, cor_r = celda_real(c0, T, OBJETIVO)
    m_v2b, cor_v = celda_v2b(c0, T, OBJETIVO)
    qr = "/".join("%+.2f" % cuantil(m_real, p) for p in CUANTILES)
    qv = "/".join("%+.2f" % cuantil(m_v2b, p) for p in CUANTILES)
    print("c0=%10d T=%3d  n=%4d %s   n=%4d %s"
          % (c0, T, len(m_real), qr, len(m_v2b), qv), flush=True)
print()
print("Lectura del adversario: si la celda (999999937, 207) esta muy")
print("por encima de (997, 207), la ley condicionada a T FIJO recuerda")
print("c0 y el 'olvido' publicado es del emparejamiento T = 30 ln c0.")
print("Si V2b reproduce la tabla real celda a celda, medianareal.py")
print("midio el transitorio del modelo, no una propiedad nueva de la")
print("cadena.")
