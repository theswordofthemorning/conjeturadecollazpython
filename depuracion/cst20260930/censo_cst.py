"""Censo propio de CST: para 2<=n<=N, el primer descenso ocurre en el primer cruce.

T es el atajo. Para cada n se busca el primer k con 3^S_k<2^k y se exige
T^k(n)<n. Criba por residuos mod 2^K: las clases que cruzan en j<=K pasos
cumplen T^j(n)=(3^S n+b)/2^j y descienden exactamente cuando
n(2^j-3^S)>b; los miembros pequeños que no lo cumplen se comprueban uno a uno.
Las clases sin cruce en K pasos se recorren individualmente con numpy
(uint64, con desbordamiento detectado y resuelto con enteros de Python).
Cálculo, no prueba Lean.
"""

import argparse
import hashlib
import json
from pathlib import Path
import time

import numpy as np


def smax_tabla(J):
    """smax[j] = mayor S con 3^S < 2^j (o -1)."""
    t, S = [], 0
    for j in range(J + 1):
        while 3 ** (S + 1) < 2 ** j:
            S += 1
        t.append(S if 3 ** S < 2 ** j else -1)
    return t


def T(x):
    return x // 2 if x % 2 == 0 else (3 * x + 1) // 2


def cst_individual(n, f=1, g=1):
    x, S, j = n, 0, 0
    while True:
        if x % 2:
            S += 1
        x = T(x)
        j += 1
        if 3 ** S < 2 ** j:
            return f * x < g * n


def clases(K):
    """Recorre los residuos r mod 2^K (r como representante, r>=0)."""
    r = np.arange(2 ** K, dtype=np.uint64)
    x = r.copy()
    S = np.zeros(2 ** K, dtype=np.int64)
    vivo = np.ones(2 ** K, dtype=bool)
    tab = smax_tabla(K)
    cruce = np.full(2 ** K, -1, dtype=np.int64)
    S_c = np.zeros(2 ** K, dtype=np.int64)
    x_c = np.zeros(2 ** K, dtype=np.uint64)
    for j in range(1, K + 1):
        impar = (x & np.uint64(1)).astype(bool)
        x = np.where(impar, (np.uint64(3) * x + np.uint64(1)) >> np.uint64(1), x >> np.uint64(1))
        S += impar
        cruza = vivo & (S <= tab[j])
        cruce[cruza] = j
        S_c[cruza] = S[cruza]
        x_c[cruza] = x[cruza]
        vivo &= ~cruza
    return r, cruce, S_c, x_c, vivo


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--N", type=int, required=True)
    ap.add_argument("--K", type=int, default=24)
    ap.add_argument("--desde", type=int, default=2, help="primer n del tramo (inclusivo, >=2)")
    ap.add_argument("--factor", type=int, default=1, help="solo pruebas de mutacion: exige f*T^k(n)<g*n")
    ap.add_argument("--divisor", type=int, default=1)
    ap.add_argument("--salida", type=Path, required=True)
    a = ap.parse_args()
    N, K, f, gd = a.N, a.K, a.factor, a.divisor
    desde = max(2, a.desde)
    t0 = time.perf_counter()
    M = 2 ** K
    r, cruce, S_c, x_c, vivo = clases(K)
    # clases que cruzan: T^j(n) = (3^S n + b)/2^j con b = 2^j T^j(r) - 3^S r
    individuales = 0
    fallos = []
    j = cruce[cruce > 0].astype(object)
    S = S_c[cruce > 0].astype(object)
    rr = r[cruce > 0].astype(object)
    xx = x_c[cruce > 0].astype(object)
    umbrales = 0
    for jj, SS, r0, x0 in zip(j, S, rr, xx):
        D = gd * 2 ** jj - f * 3 ** SS
        b = f * (2 ** jj * x0 - 3 ** SS * r0)
        # desciende (f*T^j(n)<n) si n*D > b; si D<=0 nunca: todos individuales
        n = r0 if r0 >= 2 else r0 + M
        if n < desde:
            n += (desde - n + M - 1) // M * M
        while n <= N and (D <= 0 or n * D <= b):
            individuales += 1
            if not cst_individual(n, f, gd):
                fallos.append(int(n))
            n += M
        umbrales += 1
    # clases vivas: recorrido individual
    U = r[vivo]
    tab = smax_tabla(4000)
    tabS = np.array(tab, dtype=np.int64)
    recorridos = 0
    desbordes = 0
    tmax = N // M + 1
    huella = hashlib.sha256()
    for t in range(desde // M, tmax + 1):
        n = U + np.uint64(t) * np.uint64(M)
        n = n[(n >= np.uint64(desde)) & (n <= np.uint64(N))]
        if n.size == 0:
            continue
        recorridos += n.size
        x = n.copy()
        S = np.zeros(n.size, dtype=np.int64)
        idx = np.arange(n.size)
        jj = 0
        while idx.size:
            jj += 1
            impar = (x & np.uint64(1)).astype(bool)
            grande = impar & (x > np.uint64((2 ** 64 - 2) // 3))
            if grande.any():
                for p in np.nonzero(grande)[0]:
                    desbordes += 1
                    nn = int(n[idx[p]])
                    if not cst_individual(nn, f, gd):
                        fallos.append(nn)
                keep = ~grande
                x, S, idx, impar = x[keep], S[keep], idx[keep], impar[keep]
            x = np.where(impar, (np.uint64(3) * x + np.uint64(1)) >> np.uint64(1), x >> np.uint64(1))
            S += impar
            cruza = S <= tabS[jj]
            if cruza.any():
                malos = cruza & (np.uint64(f) * x >= np.uint64(gd) * n[idx])
                for p in np.nonzero(malos)[0]:
                    fallos.append(int(n[idx[p]]))
                keep = ~cruza
                x, S, idx = x[keep], S[keep], idx[keep]
        huella.update(f"{t},{n.size}\n".encode())
    salida = {"estado": "censo exacto en Python/numpy; no es prueba Lean",
              "desde": desde, "N": N, "K": K, "factor": f, "divisor": gd, "clases_que_cruzan": umbrales,
              "clases_sin_cruce": int(vivo.sum()),
              "comprobados_por_umbral": individuales,
              "recorridos_individuales": int(recorridos),
              "desbordes_resueltos_con_enteros": desbordes,
              "fallos": fallos[:100], "numero_fallos": len(fallos),
              "sha256_lotes": huella.hexdigest(),
              "sha256_programa": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "segundos": round(time.perf_counter() - t0, 1)}
    a.salida.write_text(json.dumps(salida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(salida, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
