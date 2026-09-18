"""
REVISION 12 -- ADVERSARIO 1, TANDA 3 (Erizas), ataque propio.

La seccion 5 de Erizas refuta (E0) tomando t FIJO y haciendo crecer m
sin cota. Pregunta adversarial: cuanto de la refutacion depende de que
m sea ILIMITADA? Es decir, el cociente rho(t,m) = e_{t+1}(m)/e_t(m+1)
crece con m y solo alcanza su supremo en el limite de escala?

Si es asi, (E0) restringida a m <= M(t) con M(t) finita NO queda
refutada por la seccion 5, y conviene que la nota lo diga.

Tambien comprueba la identidad de la seccion 5:
    e_t(m) = 2^m A_t - 1  para m por encima de la escala inyectiva.
"""
from fractions import Fraction as F

def paso(k, c, bit):
    if c % 2 == 0:
        return (k, (3 * c + 1 - 3**k) // 2 if bit else c // 2)
    if bit:
        return (k - 1, (c - 3**(k - 1)) // 2) if k > 2 else None
    return (k + 1, (3 * c + 1) // 2)

def evoluciona(c0, TMAX):
    est = {(2, c0): 1}
    fotos = {0: dict(est)}
    for t in range(TMAX):
        nue = {}
        for (k, c), n in est.items():
            for bit in (False, True):
                p = paso(k, c, bit)
                if p is not None:
                    nue[p] = nue.get(p, 0) + n
        est = nue
        fotos[t + 1] = dict(est)
    return fotos

def e_de_m(est, m):
    """e_t(m) = (1/V) sum_k 2^m sum_r n(k,r)^2/n_k - 1, exacto."""
    mod = 1 << m
    porf = {}
    for (k, c), n in est.items():
        porf.setdefault(k, {})
        r = c % mod
        porf[k][r] = porf[k].get(r, 0) + n
    V = sum(n for (k, c), n in est.items())
    tot = F(0)
    for k, f in porf.items():
        nk = sum(f.values())
        tot += F(mod * sum(x * x for x in f.values()), nk)
    return tot / V - 1

def A_de(est):
    porf = {}
    for (k, c), n in est.items():
        porf.setdefault(k, []).append(n)
    V = sum(n for (k, c), n in est.items())
    tot = F(0)
    for k, lst in porf.items():
        tot += F(sum(n * n for n in lst), sum(lst))
    return tot / V

def escala_inyectiva(est):
    """menor M tal que los c de cada fibra son distintos modulo 2^M."""
    M = 1
    while True:
        mod = 1 << M
        ok = True
        for k in {k for (k, c) in est}:
            vistos = set()
            for (kk, c) in est:
                if kk == k:
                    r = c % mod
                    if r in vistos:
                        ok = False
                        break
                    vistos.add(r)
            if not ok:
                break
        if ok:
            return M
        M += 1

c0, TMAX = 1, 20
fotos = evoluciona(c0, TMAX)

print("A. IDENTIDAD DE LA SECCION 5:  e_t(m) = 2^m A_t - 1  sobre la")
print("   escala inyectiva  (c0=%d)" % c0)
for t in (12, 16, 20):
    est = fotos[t]
    M = escala_inyectiva(est)
    At = A_de(est)
    ok = all(e_de_m(est, m) == (1 << m) * At - 1 for m in (M, M + 1, M + 3))
    print("   t=%2d  escala inyectiva M=%2d   e_t(m)=2^m A_t-1 en m=M,M+1,"
          "M+3: %s" % (t, M, "ok" if ok else "FALLA"))

print()
print("B. rho(t,m) = e_{t+1}(m) / e_t(m+1)  CRECE CON m?")
print("   ultima columna: el limite de escala A_{t+1}/(2 A_t)")
print("    t |" + "".join("   m=%-2d " % m for m in (1, 2, 4, 6, 8, 10, 12,
                                                     14, 16, 18)) +
      "  limite")
crece_siempre = True
for t in range(12, TMAX):
    fila = []
    for m in (1, 2, 4, 6, 8, 10, 12, 14, 16, 18):
        r = e_de_m(fotos[t + 1], m) / e_de_m(fotos[t], m + 1)
        fila.append(float(r))
    lim = float(A_de(fotos[t + 1]) / (2 * A_de(fotos[t])))
    # monotonia en m sobre TODOS los m, no solo los impresos
    todos = [e_de_m(fotos[t + 1], m) / e_de_m(fotos[t], m + 1)
             for m in range(1, 21)]
    mono = all(todos[i] <= todos[i + 1] for i in range(len(todos) - 1))
    if not mono:
        crece_siempre = False
    print("   %2d |" % t + "".join(" %.4f" % x for x in fila) +
          "  %.6f  %s" % (lim, "creciente" if mono else "NO monotona"))

print()
print("   monotona en m para todo t probado:", crece_siempre)
print()
print("C. LECTURA")
print("   Si rho(t,m) crece con m y su supremo es el limite de escala,")
print("   entonces el supremo sobre 1<=m<=M(t) es rho(t,M(t)), que es")
print("   ESTRICTAMENTE menor que el limite usado por la seccion 5.")
print("   La refutacion necesita m ilimitada a t fijo.")
for t in (12, 16, 19):
    r6 = float(e_de_m(fotos[t + 1], 6) / e_de_m(fotos[t], 7))
    r12 = float(e_de_m(fotos[t + 1], 12) / e_de_m(fotos[t], 13))
    lim = float(A_de(fotos[t + 1]) / (2 * A_de(fotos[t])))
    print("   t=%2d:  rho(m=6)=%.6f   rho(m=12)=%.6f   limite=%.6f"
          % (t, r6, r12, lim))
