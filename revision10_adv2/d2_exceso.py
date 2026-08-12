# -*- coding: utf-8 -*-
# d2_exceso.py -- ADVERSARIO 2: el exceso de colision e_t = C2(t) - 1
# y el ataque a la ventana de X4 (excesocolision.py NO se abrio).
#
# Publicado (excesocolision_salida.txt): rho_ms peor con t >= 12,
# m = 6..9, den > 1e-6: 0.428 / 0.425 / 0.436 (A / B / ADV) < 1/2.
# EL ATAQUE: esos umbrales son elecciones. Barremos t >= 8, m = 5..11,
# umbrales de denominador mas finos, y arranques estructurados nuevos,
# buscando celdas con masa real donde rho_ms cruce 1/2.

from dp_adv2 import correr_dp, C2_de

T_FIN = 26
M_GRANDE = 36


def analizar(nombre, c0, con_serie=True):
    snaps = correr_dp(c0, M=M_GRANDE, T=T_FIN)
    # e_t(m) para m = 5..11, t = 0..26  (a t alto el modulo disponible
    # es 2^(36-t): a t = 26 quedan 2^10 -> m <= 10; m = 11 solo t <= 25)
    e = {}
    for t in range(T_FIN + 1):
        disp = M_GRANDE - t
        for m in range(5, 12):
            if m <= disp:
                c2 = C2_de(snaps[t], m)
                if c2 is not None:
                    e[(t, m)] = c2 - 1.0
    if con_serie:
        print("arranque %s (c0 = %d):" % (nombre, c0))
        for t in [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 23, 24, 25, 26]:
            print("  t = %2d  C2 = %9.4f   e_t = %9.5f" % (t, e[(t, 8)] + 1, e[(t, 8)]))
        razon = (e[(26, 8)] / e[(8, 8)]) ** (1.0 / 18)
        print("  razon media de contraccion (t = 8..26): %.3f" % razon)
    return e


def barrer_rho(e, t_min, m_lo, m_hi, den_min, etiqueta):
    peor = None
    celdas = 0
    sospechosas = []
    for (t, m), val in sorted(e.items()):
        if t < t_min or not (m_lo <= m <= m_hi):
            continue
        den = e.get((t, m + 1))
        num = e.get((t + 1, m))
        if den is None or num is None or den <= den_min:
            continue
        rho = num / den
        celdas += 1
        if peor is None or rho > peor[0]:
            peor = (rho, t, m, num, den)
        if rho > 0.5:
            sospechosas.append((rho, t, m, num, den))
    print("  %s: %d celdas, peor rho_ms = %.3f en (t=%d, m=%d) [num %.2e den %.2e]" % (
        etiqueta, celdas, peor[0], peor[1], peor[2], peor[3], peor[4]))
    for rho, t, m, num, den in sorted(sospechosas, reverse=True):
        print("      > 1/2: rho = %.3f en (t=%d, m=%d)  num %.3e  den %.3e" % (rho, t, m, num, den))
    return peor, sospechosas


if __name__ == "__main__":
    print("EL EXCESO DE COLISION, REPRODUCIDO + EL ATAQUE A LA VENTANA DE X4")
    print()
    arranques = [("A", 999983), ("B", 999999937), ("ADV", 1398101)]
    # EL CUARTO ARRANQUE ESTRUCTURADO (eleccion del adversario 2):
    # c0 tal que el hijo del primer mixto bit0, c1 = (3 c0 + 1)/2 en k=3,
    # cae en la clase c == 3^2 mod 2^21 => la racha del bit 1 del SEGUNDO
    # mixto queda forzada >= 20 (el ataque simetrico al del adv 1, que
    # forzaba el bit 0 del primero). c0 = (2*9 - 1)*inv3 mod 2^22, impar.
    inv3 = pow(3, -1, 1 << 22)
    c4 = (17 * inv3) % (1 << 22)
    if c4 % 2 == 0:
        c4 += 1 << 22
    # verificacion de la estructura: c1 == 9 mod 2^21
    c1 = (3 * c4 + 1) // 2
    assert c1 % (1 << 21) == 9 % (1 << 21), (c4, c1 % (1 << 21))
    # y un QUINTO: el adversarial RETRASADO -- c0 tal que c1 (k=3) cae en
    # la clase del adv 1 (3c == -1 mod 2^20): fuerza racha bit0 >= 19 en
    # el segundo mixto.
    inv3b = pow(3, -1, 1 << 21)
    objetivo = (-inv3b) % (1 << 21)          # c1 == -3^{-1} mod 2^21
    # c1 = (3 c0 + 1)/2  =>  c0 = (2*c1 - 1)/3 mod 2^22
    c5 = ((2 * objetivo - 1) * inv3) % (1 << 22)
    if c5 % 2 == 0:
        c5 += 1 << 22
    arranques_extra = [("ADV2-bit1for", c4), ("ADV2-retras", c5)]

    resultados = {}
    for nombre, c0 in arranques + arranques_extra:
        e = analizar(nombre, c0, con_serie=(nombre in ("A", "B", "ADV")))
        resultados[nombre] = e
        print("  ventanas de rho_ms multi-escala:")
        barrer_rho(e, 12, 6, 9, 1e-6, "publicada  (t>=12, m=6..9,  den>1e-6)")
        barrer_rho(e, 8, 6, 9, 1e-6, "temprana   (t>=8,  m=6..9,  den>1e-6)")
        barrer_rho(e, 12, 5, 11, 1e-6, "anchas     (t>=12, m=5..11, den>1e-6)")
        barrer_rho(e, 8, 5, 11, 1e-6, "todo       (t>=8,  m=5..11, den>1e-6)")
        barrer_rho(e, 12, 6, 9, 1e-9, "den fino   (t>=12, m=6..9,  den>1e-9)")
        print()
