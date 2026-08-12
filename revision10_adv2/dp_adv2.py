# -*- coding: utf-8 -*-
# dp_adv2.py -- ADVERSARIO 2: el DP exacto de la Pieza B, reconstruido
# desde los enunciados (equidistribucionmixto.py y excesocolision.py NO
# se abrieron).
#
# DP sobre (k, c mod 2^(M-t)) con conteos ENTEROS de palabras, desde
# (2, c0); cada estado abre dos hijos por el bit del ancla; se ABSORBE
# la palabra cuya transicion entra al fondo (k <= 1), o sea el mixto
# bit1 desde k = 2. Leyes (las de leyes_adv2, validadas contra pares
# reales):
#   c par,   bit0: (k,   c/2)
#   c par,   bit1: (k,   (3c + 1 - 3^k)/2)
#   c impar, bit0: (k+1, (3c + 1)/2)
#   c impar, bit1: (k-1, (c - 3^(k-1))/2)   [k = 2 -> fondo: absorbida]
# Todas son afines (a*c + b)/2 con a en {1,3}: c mod 2^n determina el
# hijo mod 2^(n-1) -- el DP pierde UN bit de modulo por paso.

def correr_dp(c0, M=36, T=26):
    """Devuelve lista de snapshots: snap[t] = dict {(k, r): conteo}
    con r = c mod 2^(M-t), conteos enteros de palabras vivas."""
    snaps = []
    estado = {(2, c0 % (1 << M)): 1}
    snaps.append(dict(estado))
    for t in range(T):
        n = M - t          # modulo actual
        n2 = n - 1         # modulo del hijo
        mod2 = 1 << n2
        modn = 1 << n
        nuevo = {}
        # potencias de 3 mod 2^n cacheadas por k
        p3 = {}
        for (k, r), cnt in estado.items():
            if r % 2 == 0:
                # bit 0: c/2
                h0 = (k, (r >> 1) % mod2)
                nuevo[h0] = nuevo.get(h0, 0) + cnt
                # bit 1: (3c + 1 - 3^k)/2
                if k not in p3:
                    p3[k] = pow(3, k, modn)
                num = (3 * r + 1 - p3[k]) % modn
                h1 = (k, (num >> 1) % mod2)
                nuevo[h1] = nuevo.get(h1, 0) + cnt
            else:
                # bit 0: (k+1, (3c+1)/2)
                num = (3 * r + 1) % modn
                h0 = (k + 1, (num >> 1) % mod2)
                nuevo[h0] = nuevo.get(h0, 0) + cnt
                # bit 1: (k-1, (c - 3^(k-1))/2) -- absorbe si k == 2
                if k >= 3:
                    if (k - 1) not in p3:
                        p3[k - 1] = pow(3, k - 1, modn)
                    num = (r - p3[k - 1]) % modn
                    h1 = (k - 1, (num >> 1) % mod2)
                    nuevo[h1] = nuevo.get(h1, 0) + cnt
                # k == 2, bit 1: fondo -> absorbida (no se propaga)
        estado = nuevo
        snaps.append(dict(estado))
    return snaps


def stats_t(snap, t, M=36):
    """Las metricas publicadas en un snapshot al tiempo t."""
    total = sum(snap.values())
    if total == 0:
        return None
    imp = sum(cnt for (k, r), cnt in snap.items() if r % 2 == 1)
    res = {}

    # C_j bit0: entre c impar, clase 3c+1 == 0 mod 2^(j+1)
    # C_j bit1: entre c impar con k >= 3, clase c == 3^(k-1) mod 2^(j+1)
    def cjs(j):
        mj = 1 << (j + 1)
        m0 = 0
        m1 = 0
        tot1 = 0
        for (k, r), cnt in snap.items():
            if r % 2 == 1:
                if (3 * r + 1) % mj == 0:
                    m0 += cnt
                if k >= 3:
                    tot1 += cnt
                    if (r - pow(3, k - 1, mj)) % mj == 0:
                        m1 += cnt
        c0 = (m0 / imp) * (1 << j) if imp else 0.0
        c1 = (m1 / tot1) * (1 << j) if tot1 else 0.0
        return c0, c1

    # residuo peor y L2 a m = 8
    m8 = 1 << 8
    hist = {}
    for (k, r), cnt in snap.items():
        rr = r % m8
        hist[rr] = hist.get(rr, 0) + cnt
    peor = max(hist.values()) * m8 / total
    l2 = m8 * sum(v * v for v in hist.values()) / (total * total)
    return {"vivos": total, "p_impar": imp / total, "cj": {j: cjs(j) for j in (1, 4, 8, 10)},
            "residuo": peor, "l2": l2}


def hist_m(snap, m):
    """Histograma entero de c mod 2^m (todas las vivas) y colision L2."""
    mm = 1 << m
    hist = {}
    for (k, r), cnt in snap.items():
        rr = r % mm
        hist[rr] = hist.get(rr, 0) + cnt
    return hist


def C2_de(snap, m):
    total = sum(snap.values())
    if total == 0:
        return None
    hist = hist_m(snap, m)
    return (1 << m) * sum(v * v for v in hist.values()) / (total * total)
