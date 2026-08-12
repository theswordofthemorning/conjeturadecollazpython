# -*- coding: utf-8 -*-
# a2_equidistribucion.py -- ADVERSARIO 2: reproduccion del DP de la
# Pieza B (contra equidistribucionmixto_salida.txt, fichero NO abierto:
# solo su salida publicada).

from dp_adv2 import correr_dp, stats_t

ARRANQUES = [("A", 999983), ("B", 999999937), ("ADV", 1398101)]

# la tabla publicada (equidistribucionmixto_salida.txt), a mano:
#   t: (vivos, p_impar, c1b0, c1b1, c4b0, c4b1, c8b0, c8b1, c10b0, c10b1, residuo, l2)
PUB = {
 ("A", 8):  (81, 0.5556, 0.844, 1.000, 0.711, 1.333, 0.000, 0.000, 0.000, 0.000, 9.481, 4.643),
 ("A", 12): (1114, 0.4803, 1.050, 0.996, 1.077, 0.852, 1.914, 0.000, 5.742, 0.000, 3.907, 1.650),
 ("A", 16): (16057, 0.5033, 0.989, 0.968, 1.045, 1.047, 0.697, 0.699, 0.000, 0.559, 2.232, 1.167),
 ("A", 20): (235631, 0.4968, 0.997, 0.989, 0.976, 0.980, 0.682, 0.659, 0.201, 0.655, 1.803, 1.069),
 ("A", 24): (3502466, 0.4979, 1.001, 1.000, 1.079, 0.986, 1.045, 0.756, 0.614, 0.938, 1.639, 1.042),
 ("B", 8):  (95, 0.5368, 1.098, 1.158, 1.569, 0.421, 0.000, 0.000, 0.000, 0.000, 10.779, 4.453),
 ("B", 12): (1262, 0.5111, 1.014, 1.016, 1.464, 1.009, 0.397, 0.461, 0.000, 0.000, 5.274, 1.674),
 ("B", 16): (17749, 0.4991, 1.004, 1.011, 0.885, 1.007, 0.347, 0.323, 0.231, 0.516, 2.740, 1.252),
 ("B", 20): (256445, 0.4999, 0.995, 0.991, 1.097, 0.994, 0.647, 0.813, 0.383, 1.114, 2.048, 1.130),
 ("B", 24): (3769952, 0.5013, 1.003, 1.012, 0.995, 1.000, 0.871, 0.838, 1.673, 0.609, 1.516, 1.038),
 ("ADV", 8):  (93, 0.4839, 0.933, 1.027, 0.711, 1.297, 0.000, 0.000, 0.000, 0.000, 13.763, 6.245),
 ("ADV", 12): (1232, 0.4992, 1.011, 0.960, 1.171, 1.055, 0.000, 0.000, 0.000, 0.000, 6.649, 2.699),
 ("ADV", 16): (17400, 0.5030, 1.006, 0.976, 1.093, 0.918, 0.644, 2.258, 0.234, 4.974, 2.840, 1.321),
 ("ADV", 20): (251994, 0.5023, 1.000, 0.977, 0.905, 0.979, 1.715, 0.702, 0.202, 0.567, 2.622, 1.165),
 ("ADV", 24): (3719136, 0.5014, 0.999, 0.996, 0.950, 0.995, 0.669, 1.006, 0.873, 0.875, 1.560, 1.039),
}

if __name__ == "__main__":
    print("EL DP DE LA PIEZA B, REPRODUCIDO POR EL ADVERSARIO 2 (codigo propio)")
    print("M = 36; conteos enteros; absorcion = primera entrada al fondo (k <= 1)")
    print()
    peor_discrepancia = 0.0
    discrepancias_enteras = []
    for nombre, c0 in ARRANQUES:
        print("=== arranque %s (c0 = %d) ===" % (nombre, c0))
        snaps = correr_dp(c0, M=36, T=24)
        for t in (8, 12, 16, 20, 24):
            s = stats_t(snaps[t], t)
            pub = PUB[(nombre, t)]
            fila = "  t = %2d: vivos %8d (pub %8d)  P(imp) %.4f (%.4f)" % (
                t, s["vivos"], pub[0], s["p_impar"], pub[1])
            if s["vivos"] != pub[0]:
                discrepancias_enteras.append((nombre, t, "vivos", s["vivos"], pub[0]))
                fila += "  <<< ENTERO DISTINTO"
            print(fila)
            mios = [s["cj"][1][0], s["cj"][1][1], s["cj"][4][0], s["cj"][4][1],
                    s["cj"][8][0], s["cj"][8][1], s["cj"][10][0], s["cj"][10][1],
                    s["residuo"], s["l2"]]
            pubs = list(pub[2:])
            etiq = ["c1b0", "c1b1", "c4b0", "c4b1", "c8b0", "c8b1", "c10b0", "c10b1", "res", "l2"]
            difs = []
            for e, m, p in zip(etiq, mios, pubs):
                d = abs(m - p)
                if d > peor_discrepancia:
                    peor_discrepancia = d
                if d > 0.0015:
                    difs.append("%s: mio %.3f pub %.3f" % (e, m, p))
            linea = "          C_j j=1: %.3f/%.3f  j=4: %.3f/%.3f  j=8: %.3f/%.3f  j=10: %.3f/%.3f  res %.3f  L2 %.3f" % tuple(mios)
            print(linea)
            if difs:
                print("          DIFERENCIAS > 0.0015: " + "; ".join(difs))
        print()
    print("peor discrepancia en las metricas flotantes: %.4f" % peor_discrepancia)
    if discrepancias_enteras:
        print("DISCREPANCIAS DE ENTEROS (SANGRE):", discrepancias_enteras)
    else:
        print("0 discrepancias de enteros en 'vivos' (15 celdas, 3 arranques).")
