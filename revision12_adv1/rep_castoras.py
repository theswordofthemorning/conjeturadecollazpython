"""
REVISION 12 -- ADVERSARIO 1, TANDA 2 (Castoras).

Verifica la identidad (C) de Castoras.md celda por celda sobre las 234
celdas registradas en balance_celdas.json, en Fraction exacta:

    (1-s) e_{t+1}(m) = e_t(m+1) - Q - R - sU - Delta          (C)
    H = B - (1+s)E/2 = (1-s)(E/2 - e'),   B = Q+R+sU+Delta

No reejecuta el DP: comprueba que los numeros que el laboratorio
publico satisfacen la identidad que dice satisfacer, y luego mira la
TENDENCIA de H/E, que la nota no reporta.
"""
import json
from fractions import Fraction as F

d = json.load(open("depuracion/frente20260910/balance_celdas.json"))
celdas = d["celdas"]
print("celdas registradas =", len(celdas))

def fr(x):
    return F(x["num"], x["den"])

fallos_C = 0
fallos_H = 0
filas = []
for cel in celdas:
    E = fr(cel["ep"])          # e_t(m+1), el exceso padre
    ep = fr(cel["eh"])         # e_{t+1}(m), el exceso hija
    s = fr(cel["s"])
    Q = fr(cel["q"])
    R = fr(cel["r"])
    sU = fr(cel["salida"])     # el termino s*U
    De = fr(cel["delta"])
    H = fr(cel["margen"])
    B = Q + R + sU + De
    # (C)
    if (1 - s) * ep != E - Q - R - sU - De:
        fallos_C += 1
    # H en sus dos formas
    if H != B - (1 + s) * E / 2 or H != (1 - s) * (E / 2 - ep):
        fallos_H += 1
    filas.append((cel["c0"], cel["t"], cel["m"], H / E, ep / E, s, De,
                  fr(cel["n0n1"])))

print()
print("A. LA IDENTIDAD (C), EXACTA, EN LAS 234 CELDAS")
print("   fallos de (C)                 =", fallos_C)
print("   fallos de las dos formas de H =", fallos_H)

he = [f[3] for f in filas]
print()
print("B. RANGO DE H/E   [Castoras.md afirma 0,038917 a 0,266228]")
print("   min = %.6f   max = %.6f" % (float(min(he)), float(max(he))))
print("   H/E > 0 en todas:", all(x > 0 for x in he))

print()
print("C. TENDENCIA DE H/E EN EL TIEMPO (lo que la nota NO reporta)")
print("   t : min H/E   max H/E   media   |  min(1/2 - e'/E)")
for t in sorted({f[1] for f in filas}):
    sub = [f for f in filas if f[1] == t]
    v = [float(f[3]) for f in sub]
    w = [float(F(1, 2) - f[4]) for f in sub]
    print("  %2d :  %.6f  %.6f  %.6f  |  %.6f"
          % (t, min(v), max(v), sum(v) / len(v), min(w)))

print()
print("D. TENDENCIA POR ARRANQUE: peor H/E de cada t")
for c0 in sorted({f[0] for f in filas}):
    sub = sorted([f for f in filas if f[0] == c0], key=lambda z: z[1])
    ts = sorted({f[1] for f in sub})
    peor = [min(float(f[3]) for f in sub if f[1] == t) for t in ts]
    print("   c0=%-11d  t=12: %.6f   t=18: %.6f   t=24: %.6f   "
          "cociente 24/12 = %.3f"
          % (c0, peor[0], peor[6], peor[12], peor[12] / peor[0]))

print()
print("E. FRACCION N0-N1 DENTRO DE Delta, EN LAS CELDAS m=8")
print("   [Castoras.md afirma entre ~17,7% y ~25,6%]")
m8 = [f for f in filas if f[2] == 8]
frac = [float(f[7] / f[6]) for f in m8]
print("   celdas m=8 = %d   min = %.4f%%   max = %.4f%%"
      % (len(m8), 100 * min(frac), 100 * max(frac)))

print()
print("F. CONTROL DE SIGNOS  [la nota afirma Q,sU,Delta >= 0; R puede ser <0]")
neg = {"Q": 0, "sU": 0, "Delta": 0, "R": 0}
for cel in celdas:
    if fr(cel["q"]) < 0:
        neg["Q"] += 1
    if fr(cel["salida"]) < 0:
        neg["sU"] += 1
    if fr(cel["delta"]) < 0:
        neg["Delta"] += 1
    if fr(cel["r"]) < 0:
        neg["R"] += 1
print("   celdas con Q<0 =", neg["Q"], " sU<0 =", neg["sU"],
      " Delta<0 =", neg["Delta"], " R<0 =", neg["R"])
print("   s <= 1/2 en todas:",
      all(fr(c["s"]) <= F(1, 2) for c in celdas))
