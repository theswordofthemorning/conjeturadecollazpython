# -*- coding: utf-8 -*-
# c2_condicionada.py -- ADVERSARIO 2: la dominacion condicionada a
# sobrevivir, medida con OTRAS convenciones de ventana (el ataque del
# encargo c2; dominacioncondicionada.py NO se abrio).
#
# Simulador propio de la cadena real (k, c) con dinamica entera exacta
# (leyes_adv2, validadas contra pares reales), excursiones desde
# (2, c0), bits i.i.d. justos, absorcion en la primera entrada al
# fondo (k <= 1), truncado en T_MAX = 900.
#
# Racha: tras cada paso mixto SOBREVIVIDO en el tiempo s, el numero L
# de pasos compartidos consecutivos que siguen; cierre = s + L.
# La racha en curso al final (absorcion o T_MAX) queda CENSURADA
# (marca abierta).
#
# Convenciones medidas:
#   PUB   (la publicada): rachas con cierre < T, censurando la abierta;
#         ensembles 'todas' y 'sobrevive' (tau >= T).
#   ALT1  (apertura en [0,T), SIN censura): toda racha ABIERTA antes de
#         T cuenta con su largo COMPLETO aunque cierre despues de T.
#   ALT2  (censura dura en min(tau,T)): como PUB pero la racha en curso
#         a T se INCLUYE truncada a su largo observado.
# Y las tardias por APERTURA >= 100 ademas de por cierre >= 100.

import random
from leyes_adv2 import hijo, FUSION

T_MAX = 900
HORIZONTES = [50, 100, 200, 414]


def excursion(c0, rng):
    """Devuelve (tau, rachas) con rachas = lista de
    (apertura, bit, largo, cerrada_bool); tau = T_MAX+1 si trunca."""
    k, c = 2, c0
    t = 0
    rachas = []
    abierta = None  # (apertura, bit, largo)
    while t < T_MAX:
        bit = rng.getrandbits(1)
        mixto = (c % 2 == 1)
        h = hijo(k, c, bit)
        t += 1
        if mixto:
            # cierra la racha anterior si estaba abierta
            if abierta is not None:
                a, b0, L = abierta
                rachas.append((a, b0, L, True))
                abierta = None
            if h is FUSION or h[0] <= 1:
                return t, rachas, abierta
            k, c = h
            abierta = (t, bit, 0)
        else:
            k, c = h
            if abierta is not None:
                a, b0, L = abierta
                abierta = (a, b0, L + 1)
    return T_MAX + 1, rachas, abierta


def metricas(sel):
    """sel = lista de (bit, largo). Devuelve (n, frac_bit0, media_b0,
    media_b1, media, cj_max)."""
    n = len(sel)
    if n == 0:
        return (0, 0, 0, 0, 0, 0)
    n0 = sum(1 for b, L in sel if b == 0)
    s0 = sum(L for b, L in sel if b == 0)
    s1 = sum(L for b, L in sel if b == 1)
    n1 = n - n0
    media = (s0 + s1) / n
    cj_max = 0.0
    j = 1
    while True:
        cnt = sum(1 for b, L in sel if L >= j)
        if cnt < 50:
            break
        cj = cnt / n * (1 << j)
        if cj > cj_max:
            cj_max = cj
        j += 1
        if j > 20:
            break
    return (n, n0 / n, s0 / n0 if n0 else 0, s1 / n1 if n1 else 0, media, cj_max)


def z_diferencia(sel):
    """z de media|b1 - media|b0 (varianzas empiricas)."""
    import math
    g0 = [L for b, L in sel if b == 0]
    g1 = [L for b, L in sel if b == 1]
    if len(g0) < 2 or len(g1) < 2:
        return 0.0
    m0 = sum(g0) / len(g0); m1 = sum(g1) / len(g1)
    v0 = sum((x - m0) ** 2 for x in g0) / (len(g0) - 1)
    v1 = sum((x - m1) ** 2 for x in g1) / (len(g1) - 1)
    return (m1 - m0) / ((v0 / len(g0) + v1 / len(g1)) ** 0.5)


def correr(nombre, c0, N, semilla):
    rng = random.Random(semilla)
    datos = []  # (tau, rachas, abierta)
    for _ in range(N):
        datos.append(excursion(c0, rng))
    print("=== arranque %s: c0 = %d, %d excursiones, T_MAX = %d, semilla %d ===" % (
        nombre, c0, N, T_MAX, semilla))
    # global (todas las rachas cerradas)
    todas = [(b, L) for tau, rs, ab in datos for (a, b, L, cerr) in rs]
    n, f0, m0, m1, med, cjm = metricas(todas)
    print("global: %d rachas, media %.4f, C_j max %.3f, frac bit0 %.4f" % (n, med, cjm, f0))
    print("        media|b0 %.4f  media|b1 %.4f  (z de la diferencia: %.1f)" % (m0, m1, z_diferencia(todas)))
    # tardias por cierre y por apertura
    tc = [(b, L) for tau, rs, ab in datos for (a, b, L, c_) in rs if a + L >= 100]
    ta = [(b, L) for tau, rs, ab in datos for (a, b, L, c_) in rs if a >= 100]
    for etiq, sel in (("cierre >= 100", tc), ("apertura >= 100", ta)):
        n, f0, m0, m1, med, cjm = metricas(sel)
        print("TARDIAS (%s): n %d  media|b0 %.4f  media|b1 %.4f  z %.1f  C_j max %.3f" % (
            etiq, n, m0, m1, z_diferencia(sel), cjm))
    print()
    print("  T    conv  ensemble    rachas  frac.b0   media|b0  media|b1  media    C_j max")
    for T in HORIZONTES:
        vivos = [d for d in datos if d[0] > T]  # tau > T  (tau >= T+1; con tau entero, 'sobrevive a [0,T)')
        for conv in ("PUB", "ALT1", "ALT2"):
            for etiq, grupo in (("todas", datos), ("sobrevive", vivos)):
                sel = []
                for tau, rs, ab in grupo:
                    if conv == "PUB":
                        sel += [(b, L) for (a, b, L, c_) in rs if a + L < T]
                    elif conv == "ALT1":
                        sel += [(b, L) for (a, b, L, c_) in rs if a < T]
                        if ab is not None and ab[0] < T:
                            sel.append((ab[1], ab[2]))  # abierta: largo observado (cota inferior del completo)
                    else:  # ALT2
                        for (a, b, L, c_) in rs:
                            if a + L < T:
                                sel.append((b, L))
                            elif a <= T:
                                sel.append((b, max(0, T - a)))
                        if ab is not None and ab[0] <= T:
                            sel.append((ab[1], min(ab[2], max(0, T - ab[0]))))
                n, f0, m0, m1, med, cjm = metricas(sel)
                print("  %3d  %-4s  %-9s %8d  %.4f    %.4f    %.4f   %.4f    %.3f" % (
                    T, conv, etiq, n, f0, m0, m1, med, cjm))
        print("       (sobreviven %d de %d)" % (len(vivos), N))
    print()


if __name__ == "__main__":
    print("LA DOMINACION CONDICIONADA CON OTRAS CONVENCIONES (adversario 2)")
    print("ALT1 = rachas ABIERTAS antes de T con largo completo (sin censura)")
    print("ALT2 = censura dura en T (la racha en curso entra truncada)")
    print()
    correr("A", 999983, 200000, 101208)
    correr("B", 999999937, 60000, 201208)
