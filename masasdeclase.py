# masasdeclase.py
#
# LAS MASAS DE CLASE DEL SISTEMA DE RENOVACION (03-08-2026, noche).
#
#   Tras el teorema de Gatas (la ecuacion f = 1/4 + f/4 + g/4 + h/4) y el
#   de Jirafas (solo los eventos DE CLASE pesan, y llegan balanceados),
#   las incognitas g (familia rebote {w, 9w+2}) y h (pares con r = 3 mod
#   4) se descomponen en masas de clase:
#
#       g = mF + mC*f + mB*g          h = nF + nC*f + nB*g
#
#   donde mF/mC/mB son las medidas de las clases cuyo PRIMER evento es
#   fusion / reentrada consecutiva / reentrada rebote. Un evento de clase
#   en el paso t esta determinado por el residuo mod 2^t (Terras), asi
#   que enumerar clases mod 2^p con tope t <= p da las masas EXACTAS
#   hasta nivel p, y la masa indecisa da una HORQUILLA rigurosa para f.
#
#   RESULTADO (el muro, dicho con todas las letras): las masas convergen
#   DESPACIO -- la indecisa baja ~2% por nivel y en p = 16 sigue en
#   ~0,65 --, la cota inferior de f sube hacia ~0,43 (consistente con
#   a(32)/2^32 = 0,4357, que sigue siendo mejor) y el techo se queda en
#   1. ES EL MISMO MURO DE CONVERGENCIA LENTA QUE LA RAZON DE b(k),
#   porque es la misma pregunta escrita como sistema. Lo que este
#   fichero deja: el marco exacto, las masas por nivel, y la horquilla.
#   La via que queda para cerrar: tratar la cola indecisa de forma
#   estructural (la cola es "tramos largos antes de reentrar", que
#   deberia tener su propia renovacion), no subir p.

def paso(x):
    return (3 * x + 1) // 2 if x % 2 else x // 2


K = 999999                  # separador de testigos (impar, grande)
NIVELES = (8, 10, 12, 14, 16)


def evento(xa, ya, xb, yb, tope):
    # primer evento comun a los DOS testigos en el mismo paso
    for t in range(1, tope + 1):
        xa, ya = paso(xa), paso(ya)
        xb, yb = paso(xb), paso(yb)
        if xa == ya and xb == yb:
            return 'F'
        if abs(xa - ya) == 1 and abs(xb - yb) == 1:
            return 'C'
        la, ha = min(xa, ya), max(xa, ya)
        lb, hb = min(xb, yb), max(xb, yb)
        if ha == 9 * la + 2 and hb == 9 * lb + 2:
            return 'B'
    return '?'


def masas(familia, p):
    n = 2 ** p
    cnt = {'F': 0, 'C': 0, 'B': 0, '?': 0}
    for c in range(n):
        w1, w2 = c, c + n * K
        if familia == 'g':
            if w1 == 0:
                w1 = n * 2 * K
            e = evento(w1, 9 * w1 + 2, w2, 9 * w2 + 2, p)
        else:
            r1, r2 = 4 * w1 + 3, 4 * w2 + 3
            e = evento(r1, r1 + 1, r2, r2 + 1, p)
        cnt[e] += 1
    if sum(cnt.values()) != n:
        raise SystemExit("FALLO conteo: familia %s p=%d" % (familia, p))
    return {k: v / n for k, v in cnt.items()}


def resolver(mg, nh, i):
    # i = fraccion de la masa indecisa que se supone fundida (0 o 1)
    A = (mg['F'] + mg['?'] * i) / (1 - mg['B'])
    B = mg['C'] / (1 - mg['B'])
    A2 = nh['F'] + nh['?'] * i + nh['B'] * A
    B2 = nh['C'] + nh['B'] * B
    return (0.25 + A / 4 + A2 / 4) / (1 - 0.25 - B / 4 - B2 / 4)


anterior_lo, anterior_mu = 0.0, 1.0
for p in NIVELES:
    mg = masas('g', p)
    nh = masas('h', p)
    lo, hi = resolver(mg, nh, 0.0), resolver(mg, nh, 1.0)
    # COMPROBACION 1: la cota inferior sube y la masa indecisa baja
    if lo < anterior_lo or mg['?'] > anterior_mu:
        raise SystemExit("FALLO monotonia: p=%d lo=%.4f mu=%.4f"
                         % (p, lo, mg['?']))
    anterior_lo, anterior_mu = lo, mg['?']
    # COMPROBACION 2: la horquilla contiene el valor medido por valores
    if not (lo <= 0.4453 <= hi):
        raise SystemExit("FALLO horquilla: p=%d [%.4f, %.4f] no contiene "
                         "el f medido 0,4453" % (p, lo, hi))
    print("p=%2d  g:{F %.4f C %.4f B %.4f ? %.4f}  "
          "h:{F %.4f C %.4f B %.4f ? %.4f}  f en [%.4f, %.4f]"
          % (p, mg['F'], mg['C'], mg['B'], mg['?'],
             nh['F'], nh['C'], nh['B'], nh['?'], lo, hi))

print()
print("CONCLUSION: el sistema es exacto y las horquillas son rigurosas,")
print("pero la masa indecisa decae ~2% por nivel: el mismo muro de")
print("convergencia lenta que la razon de b(k), porque es la misma")
print("pregunta. NO subir p: la via es tratar la cola estructuralmente")
print("(la cola es 'tramos largos antes de reentrar' y deberia tener su")
print("propia renovacion). f sigue acotada mejor por a(32)/2^32 = 0,4357.")
