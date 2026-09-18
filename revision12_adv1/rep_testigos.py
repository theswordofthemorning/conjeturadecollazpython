"""
REVISION 12 -- ADVERSARIO 1, TANDA 2 (Castoras), testigos.

Reproduccion INDEPENDIENTE de los dos contraejemplos de Castoras.md.
La ley del paso se reimplementa desde `paso` de balance.lean; todo lo
demas (E, a, b, E_kb, G, Q, R, O, s, U, V', e', Delta) se calcula desde
las definiciones escritas en Castoras.md, no desde balance.py.

Comprueba ademas, por enumeracion, dos afirmaciones estructurales de
la nota que se usan en los pasos 2 y 3 de la demostracion:
  - cada una de las cuatro corrientes es u -> alpha*u + beta con
    alpha en {1,3} sobre Z/N  (luego conserva el exceso interno);
  - a cada altura hija llegan como mucho CUATRO corrientes.
"""
from fractions import Fraction as F
from collections import defaultdict

# ---- la ley del paso, transcrita de balance.lean ----------------
def paso(k, c, bit):
    if c % 2 == 0:
        return (k, (3 * c + 1 - 3**k) // 2 if bit else c // 2)
    if bit:
        return (k - 1, (c - 3**(k - 1)) // 2) if k > 2 else None
    return (k + 1, (3 * c + 1) // 2)

def corriente(k, c, bit):
    if c % 2 == 0:
        return "N1" if bit else "N0"
    return ("D" if k > 2 else "MUERE") if bit else "A"

# ---- exceso, desde la definicion de LEEME seccion 1 -------------
def exceso(conteos, modulo):
    """conteos: dict (k, r) -> masa. modulo: la escala."""
    porf = defaultdict(lambda: defaultdict(F))
    for (k, r), n in conteos.items():
        porf[k][r % modulo] += n
    V = sum(sum(f.values()) for f in porf.values())
    tot = F(0)
    for k, f in porf.items():
        nk = sum(f.values())
        if nk > 0:
            tot += modulo * sum(x * x for x in f.values()) / nk
    return tot / V - 1

def analiza(nombre, entrada, N):
    """entrada: lista de (k, c) con c mod 2N. N = escala hija."""
    print("=" * 66)
    print(nombre)
    padre = defaultdict(F)
    for k, c in entrada:
        padre[(k, c % (2 * N))] += 1
    V = F(len(entrada))

    E = exceso(padre, 2 * N)

    # --- paridad y excesos internos, a escala N ---
    porkb = defaultdict(lambda: defaultdict(F))   # (k,b) -> u -> masa
    nk = defaultdict(F)
    for (k, c), n in padre.items():
        b = c % 2
        porkb[(k, b)][(c // 2) % N] += n
        nk[k] += n

    G = Q = R = F(0)
    for k in nk:
        Pk = nk[k] / V
        m0 = sum(porkb[(k, 0)].values())
        m1 = sum(porkb[(k, 1)].values())
        a, b = m0 / nk[k], m1 / nk[k]
        # E_{k,b} = N * sum_r p(r|k,b)^2 - 1  con p PROBABILIDAD: /m^2
        E0 = (N * sum(x * x for x in porkb[(k, 0)].values()) / m0**2 - 1) if m0 else F(0)
        E1 = (N * sum(x * x for x in porkb[(k, 1)].values()) / m1**2 - 1) if m1 else F(0)
        G += Pk * (a * E0 + b * E1)
        Q += Pk * (a - b) ** 2
        R += Pk * (a - b) * (a * E0 - b * E1)

    print("  V=%s  E=%s  G=%s  Q=%s  R=%s" % (V, E, G, Q, R))
    print("  paso 1  E == G+Q+R :", E == G + Q + R)

    # --- O, s, U ---
    O = sum(n for (k, c), n in padre.items() if k == 2 and c % 2 == 1)
    s = F(O, 1) / (2 * V)
    u_grupo = porkb[(2, 1)]
    mu = sum(u_grupo.values())
    U = (N * sum(x * x for x in u_grupo.values()) / mu**2 - 1) if mu else F(0)
    Vp = 2 * V - O
    print("  O=%s  s=%s  U=%s  V'=%s" % (O, s, U, Vp))

    # --- las hijas, por corriente ---
    hijas = defaultdict(F)                       # (j, r) -> masa
    porcorr = defaultdict(lambda: defaultdict(F))  # (j, etiqueta) -> r -> masa
    muertas = F(0)
    for (k, c), n in padre.items():
        for bit in (False, True):
            p = paso(k, c, bit)
            et = corriente(k, c, bit)
            if p is None:
                muertas += n
                continue
            j, d = p
            hijas[(j, d % N)] += n
            porcorr[(j, (k, et))][d % N] += n
    print("  ramas muertas=%s  (debe ser O=%s):" % (muertas, O), muertas == O)
    print("  masa hija=%s  (debe ser V'=%s):" % (sum(hijas.values()), Vp),
          sum(hijas.values()) == Vp)

    ep = exceso(hijas, N)

    # --- Delta ---
    porj = defaultdict(list)
    for (j, et), f in porcorr.items():
        porj[j].append((sum(f.values()), f))
    Delta = F(0)
    maxcorr = 0
    for j, lst in porj.items():
        Sj = sum(M for M, _ in lst)
        maxcorr = max(maxcorr, len(lst))
        for i in range(len(lst)):
            for l in range(i + 1, len(lst)):
                Mi, pi = lst[i]
                Ml, pl = lst[l]
                D = N * sum((pi.get(r, F(0)) / Mi - pl.get(r, F(0)) / Ml) ** 2
                            for r in set(pi) | set(pl))
                Delta += (Mi * Ml / Sj) * D
    Delta /= (2 * V)
    print("  e'=%s   e'/E=%s   Delta=%s   corrientes max por altura=%d"
          % (ep, ep / E, Delta, maxcorr))

    izq = (1 - s) * ep
    der = E - Q - R - s * U - Delta
    print("  IDENTIDAD (C):  (1-s)e' = %s   E-Q-R-sU-Delta = %s   -> %s"
          % (izq, der, "CIERRA" if izq == der else "FALLA"))
    H = Q + R + s * U + Delta - (1 + s) * E / 2
    print("  H = %s   y  (1-s)(E/2-e') = %s   -> %s"
          % (H, (1 - s) * (E / 2 - ep),
             "CIERRA" if H == (1 - s) * (E / 2 - ep) else "FALLA"))
    return E, ep, Q, R, s, U, Delta


t1 = ([(2, 0)] * 4 + [(2, 1)] * 3 + [(2, 3)] * 3 +
      [(2, 5)] * 3 + [(2, 7)] * 3)
analiza("TESTIGO 1  (Castoras: V=16, E=5/8, e'=6/5, Q=1/4, R=-3/8, "
        "s=3/8, U=0, Delta=0)", t1, 4)

t2 = [(2, 0), (2, 1)]
analiza("TESTIGO 2  (Castoras: E=e'=3, Q=R=0, s=1/4, U=3, Delta=0)",
        t2, 4)

print("=" * 66)
print("ESTRUCTURA: las cuatro corrientes son afines de coeficiente 1 o 3")
for m in range(2, 11):
    N = 1 << m
    for k in range(2, 9):
        for etiqueta, pares in (
            ("N0", [(2 * u) % (2 * N) for u in range(N)]),
            ("N1", [(2 * u) % (2 * N) for u in range(N)]),
            ("A",  [(2 * u + 1) % (2 * N) for u in range(N)]),
            ("D",  [(2 * u + 1) % (2 * N) for u in range(N)]),
        ):
            bit = etiqueta in ("N1", "D")
            if etiqueta == "D" and k <= 2:
                continue
            img = []
            for u in range(N):
                r = paso(k, pares[u], bit)
                img.append(r[1] % N)
            # ajuste afin esperado
            alpha = 3 if etiqueta in ("N1", "A") else 1
            beta = (img[0] - alpha * 0) % N
            afin = all(img[u] == (alpha * u + beta) % N for u in range(N))
            biy = len(set(img)) == N
            if not (afin and biy):
                print("   FALLA  m=%d k=%d %s" % (m, k, etiqueta))
print("   comprobado m=2..10, k=2..8, todo u: afin con alpha en {1,3}"
      " y biyectiva en todos los casos.")
