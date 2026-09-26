"""Reproduce la cuenta de Wu (1992): K = # de n en [1, 2^N) que pertenecen a una racha
de >= 2 consecutivos con la misma altura; d = K/(2^N - 1). Tambien cuenta los pares
con misma altura pero distinto sigma_inf (divisiones por 2), por curiosidad.

Alturas por bloques diadicos con numpy: para n en [2^k, 2^(k+1)) se itera el mapa
clasico hasta bajar de 2^k y se suma la altura ya conocida del valor alcanzado.
"""

import numpy as np

N_MAX = 24


def alturas(n_max_exp):
    tope = 2 ** n_max_exp + 1          # hace falta la altura de 2^N tambien
    h = np.zeros(tope, dtype=np.int64)
    s = np.zeros(tope, dtype=np.int64)  # divisiones por 2 hasta 1
    h[1], s[1] = 0, 0
    k = 0
    while 2 ** k < tope:
        lo, hi = 2 ** k, min(2 ** (k + 1), tope)
        if lo == 1:
            k += 1
            continue
        n = np.arange(lo, hi, dtype=np.int64)
        x = n.copy()
        pasos = np.zeros_like(n)
        mitades = np.zeros_like(n)
        vivos = np.ones(len(n), dtype=bool)
        while vivos.any():
            idx = np.nonzero(vivos)[0]
            v = x[idx]
            par = (v % 2 == 0)
            v = np.where(par, v // 2, 3 * v + 1)
            x[idx] = v
            pasos[idx] += 1
            mitades[idx] += par
            vivos[idx] = v >= lo
        h[lo:hi] = pasos + h[x]
        s[lo:hi] = mitades + s[x]
        k += 1
    return h, s


def main():
    h, s = alturas(N_MAX)
    print(' N   K (en rachas)   d = K/(2^N-1)   pares misma altura con sigma distinto')
    for N in range(2, N_MAX + 1):
        tope = 2 ** N
        hh = h[1:tope + 1]                # alturas de 1..2^N
        igual_sig = hh[1:] == hh[:-1]     # par (n, n+1) para n = 1..2^N - 1
        en = np.zeros(tope - 1, dtype=bool)   # n = 1..2^N-1
        # n en racha si comparte altura con n-1 o con n+1
        en[1:] |= igual_sig[:tope - 2]    # n >= 2 con n-1
        en |= igual_sig[:tope - 1]        # n con n+1 (n+1 puede ser 2^N)
        K = int(en.sum())
        ss = s[1:tope + 1]
        distinto = int((igual_sig & (ss[1:] != ss[:-1])).sum())
        print(f'{N:2d}   {K:12d}   {K / (tope - 1):.6f}      {distinto}')


if __name__ == '__main__':
    main()
