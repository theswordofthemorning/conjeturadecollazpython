# -*- coding: utf-8 -*-
# b2_bump.py -- ADVERSARIO 2: auditoria del argumento del bump del
# escalon 10 ("w[i] <= 0 -> 1 en S* solo ensancha el lado superior").
#
# EL ARGUMENTO ANALITICO (que este script somete a tortura numerica):
#   Para TODA matriz no negativa A y TODO vector w estrictamente
#   positivo:   rho(A) <= max_i (A w)_i / w_i.
#   Prueba: con D = diag(w), rho(A) = rho(D^-1 A D) <= max fila de
#   D^-1 A D = max_i (A w)_i / w_i  (la norma infinito domina el radio
#   espectral). NO pide irreducibilidad ni que w sea autovector.
#   => bumpear w[i] <= 0 a 1 PRESERVA w > 0, luego el maximo de
#   cocientes recomputado con el w bumpeado es una cota superior
#   VALIDA: puede ser mas ancha, nunca falsa.
#
#   EL UNICO MODO DE FALLO: computar el maximo con productos VIEJOS
#   (pre-bump) o saltarse filas. Eso se testea aqui: bumpeamos
#   subconjuntos crecientes (hasta el 50% de S*) del vector de power
#   iteration en K=9 y verificamos que el maximo recomputado NUNCA
#   cae debajo de la cota inferior certificada con el vector bueno
#   (si cayera, el 'solo ensancha' seria falso).

import random
from fractions import Fraction
from b2_pinza import construir, tarjan

K = 9
PISO_CERT = Fraction(1967467, 1000000)  # la cota inferior certificada


def scc_grande(suc, comp, tam):
    ci = max(range(len(tam)), key=lambda c: tam[c])
    nodos = [v for v in range(len(suc)) if comp[v] == ci]
    pos = {v: i for i, v in enumerate(nodos)}
    sucl = [[pos[w] for w in suc[v] if comp[w] == ci] for v in nodos]
    return sucl


def power(sucl, iters=3000):
    n = len(sucl)
    x = [1.0] * n
    for it in range(iters):
        y = [sum(x[j] for j in sucl[i]) for i in range(n)]
        m = max(y)
        x = [v / m for v in y]
    return x


def cota_sup_entera(sucl, w):
    hi = Fraction(0)
    for i in range(len(sucl)):
        s = sum(w[j] for j in sucl[i])
        q = Fraction(s, w[i])
        if q > hi:
            hi = q
    return hi


def cota_inf_entera(sucl, w):
    lo = None
    for i in range(len(sucl)):
        s = sum(w[j] for j in sucl[i])
        q = Fraction(s, w[i])
        if lo is None or q < lo:
            lo = q
    return lo


if __name__ == "__main__":
    estados, suc = construir(K)
    nscc, comp, tam, lazos, nt = tarjan(suc)
    sucl = scc_grande(suc, comp, tam)
    n = len(sucl)
    x = power(sucl)
    ESC = 10 ** 12
    v_bueno = [max(1, int(round(t * ESC))) for t in x]
    lo = cota_inf_entera(sucl, v_bueno)
    hi = cota_sup_entera(sucl, v_bueno)
    print("K=%d, |S*|=%d, pinza con v bueno: [%.7f, %.7f]" % (K, n, float(lo), float(hi)))

    rng = random.Random(1208)
    ok = True
    for frac in (0.001, 0.01, 0.05, 0.2, 0.5):
        m = max(1, int(frac * n))
        idx = rng.sample(range(n), m)
        w = list(v_bueno)
        for i in idx:
            w[i] = 1  # el bump: entradas 'rotas' -> 1
        hib = cota_sup_entera(sucl, w)
        lob = cota_inf_entera(sucl, w)
        estado = "OK (ensancha)" if hib >= lo else "<<< FALSEA EL LADO SUPERIOR"
        if hib < lo:
            ok = False
        print("bump %5.1f%% (%6d entradas): sup_bump = %12.4f  inf_bump = %.6f  %s" % (
            100 * frac, m, float(hib), float(lob), estado))
    # el caso extremo: TODO el vector a 1 (bump total)
    w = [1] * n
    hib = cota_sup_entera(sucl, w)
    print("bump 100%%: sup = %.4f (= grado maximo de salida, la cota trivial)" % float(hib))
    print()
    if ok:
        print("VEREDICTO: el bump NUNCA baja el lado superior por debajo del")
        print("verdadero rho -- consistente con el teorema rho <= max_i (Aw)_i/w_i")
        print("para todo w > 0. El argumento 'solo ensancha' es CORRECTO,")
        print("CONDICIONADO a que los cocientes se recomputen con el w bumpeado")
        print("en TODAS las filas de S* (incluidas las vecinas de las bumpeadas).")
    else:
        raise SystemExit("EL BUMP PUEDE FALSEAR: hay contraejemplo arriba")
