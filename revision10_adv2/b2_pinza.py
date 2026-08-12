# -*- coding: utf-8 -*-
# b2_pinza.py -- ADVERSARIO 2, 10a revision: reproduccion INDEPENDIENTE
# de la pinza de LANGOSTAS (pinzacw.py, que NO se abrio).
#
# La caja del escalon K (deducida de los datos publicados: K=13 con
# |c| <= 49152 = 3*2^14 en bitacora 09-08 (13); K=19 con |c| <= 3145728
# = 3*2^20 en el escalon 10): estados (k, c) con 0 <= k <= K y
# |c| <= 3*2^(K+1), ALCANZABLES desde la semilla (0, 1) (el par
# consecutivo (r, r+1)); transiciones = las dos leyes por bit; se
# DESCARTAN las que fusionan (absorcion) o salen de la caja.
#
# La pinza: Tarjan iterativo propio para las SCC; power iteration para
# hallar un vector positivo v sobre S*; el certificado en ENTEROS:
#   inferior: rho >= min_i (v[s0]+v[s1]) / v[i]      (CW, v > 0 entero)
#   superior: rho <= max_i (v[s0]+v[s1]) / v[i]      (max de cocientes
#             de fila de D^-1 M D, valido para TODO v > 0)
# Los cocientes se comparan en enteros (cross-multiplication exacta).

import sys, time
from fractions import Fraction
sys.setrecursionlimit(10000)
from leyes_adv2 import hijo, FUSION

K_OBJETIVO = [2, 3, 5, 7, 9, 11, 13]
PUBLICADO = {2: (20, 2, 19, 1.739963), 3: (121, 2, 120, 1.866657),
             5: (734, 7, 728, 1.933590), 7: (3717, 16, 3702, 1.955595),
             9: (16361, 947, 15415, 1.967467),
             11: (72835, 3947, 68889, 1.975447),
             13: (313672, 25486, 288187, 1.980748)}


def construir(K):
    cap = 3 * 2 ** (K + 1)
    semilla = (0, 1)
    indice = {semilla: 0}
    estados = [semilla]
    suc = []  # lista de tuplas de sucesores (indices)
    frente = [semilla]
    while frente:
        nuevo = []
        for s in frente:
            hijos = []
            for bit in (0, 1):
                h = hijo(s[0], s[1], bit)
                if h is FUSION:
                    continue
                k2, c2 = h
                if k2 > K or abs(c2) > cap:
                    continue
                if h not in indice:
                    indice[h] = len(estados)
                    estados.append(h)
                    nuevo.append(h)
                hijos.append(indice[h])
            suc.append(tuple(hijos))
        # suc se llena en orden de descubrimiento == orden de estados
        frente = nuevo
    # OJO: suc quedo alineado por orden de PROCESO del BFS, que es el
    # orden de descubrimiento; re-derivamos para garantizar alineacion
    suc = [None] * len(estados)
    for s, i in indice.items():
        hs = []
        for bit in (0, 1):
            h = hijo(s[0], s[1], bit)
            if h is FUSION:
                continue
            k2, c2 = h
            if k2 > K or abs(c2) > cap:
                continue
            hs.append(indice[h])
        suc[i] = tuple(hs)
    return estados, suc


def tarjan(suc):
    """Tarjan ITERATIVO. Devuelve (num_scc, comp[], tamanos, lazos_sueltos,
    no_triviales) donde no trivial = tamano > 1 o lazo propio."""
    n = len(suc)
    UNVISITED = -1
    index = [UNVISITED] * n
    low = [0] * n
    oncall = [False] * n
    comp = [-1] * n
    pila = []
    contador = [0]
    nscc = [0]
    tam = []
    for raiz in range(n):
        if index[raiz] != UNVISITED:
            continue
        trabajo = [(raiz, 0)]
        while trabajo:
            v, pi = trabajo[-1]
            if pi == 0:
                index[v] = low[v] = contador[0]
                contador[0] += 1
                pila.append(v)
                oncall[v] = True
            avanzado = False
            hijos_v = suc[v]
            while pi < len(hijos_v):
                w = hijos_v[pi]
                pi += 1
                if index[w] == UNVISITED:
                    trabajo[-1] = (v, pi)
                    trabajo.append((w, 0))
                    avanzado = True
                    break
                elif oncall[w]:
                    if low[w] < low[v]:
                        low[v] = low[w]
            if avanzado:
                continue
            # v terminado
            if low[v] == index[v]:
                t = 0
                while True:
                    w = pila.pop()
                    oncall[w] = False
                    comp[w] = nscc[0]
                    t += 1
                    if w == v:
                        break
                tam.append(t)
                nscc[0] += 1
            trabajo.pop()
            if trabajo:
                padre = trabajo[-1][0]
                if low[v] < low[padre]:
                    low[padre] = low[v]
    # no triviales: tamano > 1 o lazo propio
    lazo = [False] * nscc[0]
    for v in range(n):
        if v in suc[v]:
            pass
    no_triv = []
    lazos_sueltos = 0
    for v in range(n):
        for w in suc[v]:
            if w == v:
                if tam[comp[v]] == 1:
                    lazos_sueltos += 1
    for ci, t in enumerate(tam):
        if t > 1:
            no_triv.append(ci)
    return nscc[0], comp, tam, lazos_sueltos, no_triv


def pinza_scc(suc, comp, ci, iters=6000, tol=1e-13):
    """Power iteration sobre la SCC ci + certificado entero de dos lados."""
    nodos = [v for v in range(len(suc)) if comp[v] == ci]
    pos = {v: i for i, v in enumerate(nodos)}
    sucl = [[pos[w] for w in suc[v] if comp[w] == ci] for v in nodos]
    n = len(nodos)
    x = [1.0] * n
    lam = 0.0
    for it in range(iters):
        y = [0.0] * n
        # y = M x  (y[i] = suma de x en sucesores de i)
        for i in range(n):
            s = 0.0
            for j in sucl[i]:
                s += x[j]
            y[i] = s
        m = max(y)
        y = [v / m for v in y]
        if it % 25 == 24:
            # cociente de Rayleigh burdo: razon de normas L1
            s1 = sum(y)
            lamn = m * s1 / sum(x) if sum(x) else m
            if abs(lamn - lam) < tol:
                x = y
                lam = lamn
                break
            lam = lamn
        x = y
    # vector entero: escalar y redondear con piso 1
    ESC = 10 ** 12
    vi = [max(1, int(round(v * ESC))) for v in x]
    # certificado exacto en enteros
    lo_num, lo_den = None, None
    hi_num, hi_den = None, None
    for i in range(n):
        s = 0
        for j in sucl[i]:
            s += vi[j]
        # cociente s / vi[i]
        if lo_num is None or s * lo_den < lo_num * vi[i]:
            lo_num, lo_den = s, vi[i]
        if hi_num is None or s * hi_den > hi_num * vi[i]:
            hi_num, hi_den = s, vi[i]
    return Fraction(lo_num, lo_den), Fraction(hi_num, hi_den), n


if __name__ == "__main__":
    print("LA PINZA, REPRODUCIDA POR EL ADVERSARIO 2 (codigo propio)")
    print("caja: 0 <= k <= K, |c| <= 3*2^(K+1), alcanzable desde (0,1)")
    print()
    todo_ok = True
    for K in K_OBJETIVO:
        t0 = time.time()
        estados, suc = construir(K)
        nscc, comp, tam, lazos, no_triv = tarjan(suc)
        ne, ns, nS, pub = PUBLICADO[K]
        linea = "K=%2d estados %7d (pub %7d)  SCCs %7d  no-triv %d  lazos-sueltos %d" % (
            K, len(estados), ne, nscc, len(no_triv), lazos)
        if len(no_triv) == 1:
            lo, hi, n_scc = pinza_scc(suc, comp, no_triv[0])
            linea += "  |S*| %7d (pub %7d)  pinza [%.6f, %.6f] (pub %.6f)" % (
                n_scc, nS, float(lo), float(hi), pub)
            if n_scc != nS or not (lo <= Fraction(pub).limit_denominator(10**7) or True):
                pass
            if len(estados) != ne or n_scc != nS or abs(float(lo) - pub) > 2e-5:
                todo_ok = False
                linea += "   <<< DISCREPANCIA"
        else:
            todo_ok = False
            linea += "   <<< no-triv != 1"
        print(linea, " (%.0f s)" % (time.time() - t0))
    print()
    print("VEREDICTO PRELIMINAR:", "REPRODUCIDO" if todo_ok else "HAY DISCREPANCIAS")
