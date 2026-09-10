"""Erizas: controles exactos del argumento contra la contraccion en toda escala.

Reutiliza contraccion.py; no es una revision independiente ciega.
El barrido NO demuestra el resultado asintotico: ver Erizas.md.
"""

import argparse
from collections import Counter
from fractions import Fraction
from math import isqrt

from contraccion import (avanzar, colision_entera, control_pares,
                         control_palabras, exceso, hijos)


def techo_raiz_cuarta(n):
    r = isqrt(isqrt(n))
    return r if r**4 == n else r+1


def momentos(estados, t):
    total = 2**t
    unos = sum(n*(k-1) for (k, _), n in estados.items())
    dos = sum(n*(k-1)**2 for (k, _), n in estados.items())
    cuatro = sum(n*(k-1)**4 for (k, _), n in estados.items())
    absolutos = Counter()
    for (k, c), n in estados.items():
        absolutos[k] += n*abs(c)
    u = sum((Fraction(n, 3**k) for k, n in absolutos.items()), Fraction(0))
    return (Fraction(unos, total), Fraction(dos, total),
            Fraction(cuatro, total), u/total)


def controles_locales():
    casos = 0
    for k in range(2, 8):
        for c in range(-71, 72):
            ramas = hijos(k, c)
            x = k-1
            xs = [h[0]-1 if h else 0 for h in ramas]
            us = [Fraction(abs(h[1]), 3**h[0]) if h else 0 for h in ramas]
            assert sum(xs) == 2*x
            assert sum(y*y for y in xs) <= 2*(x*x+1)
            assert sum(y**4 for y in xs) <= 2*(x**4+6*x*x+1)
            assert sum(us)/2 <= Fraction(abs(c), 3**k)+Fraction(1, 2)
            casos += 1
    for n in range(1, 10001):
        h = techo_raiz_cuarta(n)
        assert (h-1)**4 < n <= h**4
    print(f"CONTROL: {casos} estados, cuatro cotas locales; 10000 raices enteras: OK.")


def investigar(c0, pasos):
    estados = Counter({(2, c0): 1})
    anterior = None
    anterior_a = None
    for t in range(pasos+1):
        vivos = sum(estados.values())
        s = Fraction(vivos, 2**t)
        uno, dos, cuatro, u = momentos(estados, t)
        assert uno == 1
        assert dos <= t+1
        assert cuatro <= (t+1)*(3*t+1)
        assert s*(t+1) >= 1
        assert u <= Fraction(abs(c0), 9)+Fraction(t, 2)
        if anterior is not None:
            _, dos_prev, cuatro_prev, u_prev = anterior
            assert dos <= dos_prev+1
            assert cuatro <= cuatro_prev+6*dos_prev+1
            assert u <= u_prev+Fraction(1, 2)
        if t == min(8, pasos):
            control_palabras(c0, t, estados)

        h = techo_raiz_cuarta(4*(t+1)**2*(3*t+1))
        j = 4*(t+1)*(abs(c0)+t+1)
        limite_c = j*3**(h+1)
        buenos = sum(n for (k, c), n in estados.items()
                     if k-1 <= h and abs(c) <= j*3**k)
        assert 2*buenos >= vivos
        soporte_caja = h*(2*limite_c+1)
        a, escala = colision_entera(estados)
        assert a >= Fraction(1, 4*soporte_caja)
        marginal = Counter()
        for (_, c), n in estados.items():
            marginal[c] += n
        b = Fraction(sum(n*n for n in marginal.values()), vivos*vivos)
        assert a >= b >= Fraction(1, 4*(2*limite_c+1))
        # La formula de escala inyectiva se cruza con el conteo modular.
        if t in {0, 8, pasos}:
            assert exceso(estados, escala) == 2**escala*a-1
        if t == 0 or t % 4 == 0 or t == pasos:
            razon = "-" if anterior_a is None else f"{float(a/(2*anterior_a)):.9f}"
            print(f"c0={c0} t={t} estados={len(estados)} S={float(s):.6f} "
                  f"A={float(a):.9f} rho_lim_m={razon} h={h} "
                  f"caja_masa={float(Fraction(buenos, vivos)):.6f}", flush=True)
        anterior, anterior_a = (uno, dos, cuatro, u), a
        if t < pasos:
            estados, _ = avanzar(estados)
    print(f"  OK: {pasos+1} leyes; momentos, supervivencia, caja y colision exactos.")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--pasos", type=int, default=20)
    p.add_argument("--semillas", type=int, nargs="+", default=[-5, 0, 1, 5, 999983, 1398101])
    args = p.parse_args()
    if not 0 <= args.pasos <= 28:
        p.error("Esta tanda acotada admite 0..28 pasos; revisar costo antes de ampliarla")
    control_pares()
    controles_locales()
    print("Decimales solo para presentar; todas las comparaciones usan enteros/Fraction.")
    for c0 in args.semillas:
        investigar(c0, args.pasos)
    print("FIN: controles terminados; prueba asintotica escrita en Erizas.md, no barrido universal.")


if __name__ == "__main__":
    main()
