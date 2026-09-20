"""Contraste exacto de la ruta armónica; no prueba CF_H ni enumera horizontes grandes."""

import argparse
from collections import Counter
from fractions import Fraction as F
import json
from pathlib import Path

from verificar import por_par


def avanzar(distribucion, techo=None):
    siguiente = Counter()
    for (k, c, mixtos), peso in distribucion.items():
        if k == 1 or (techo is not None and k - 1 >= techo):
            siguiente[k, c, mixtos] += 2 * peso
            continue
        for bit in (0, 1):
            hijo = por_par(k, c, bit)
            assert hijo[0] == 'estado' and hijo[1] >= 1
            siguiente[hijo[1], hijo[2], mixtos + c % 2] += peso
    return siguiente


def contrastar_arboles(pasos):
    semillas = (-2**31 - 1, -17, -1, 0, 1, 2, 17, 2**31)
    techos = (1, 2, 3, 5, 9)
    niveles = cotas = 0
    for c in semillas:
        original = Counter({(2, c, 0): 1})
        bandas = {l: original.copy() for l in techos}
        for h in range(pasos + 1):
            total = 2**h
            assert sum(original.values()) == total
            assert sum((k - 1) * p for (k, _, _), p in original.items()) == total
            vivos = sum(p for (k, _, _), p in original.items() if k >= 2)
            assert (h + 1) * vivos >= total
            for l, banda in bandas.items():
                assert sum(banda.values()) == total
                energia = sum((k - 1) * (l - k + 1) * p for (k, _, _), p in banda.items())
                cuenta = sum(j * p for (_, _, j), p in banda.items())
                assert energia + cuenta == (l - 1) * total
                techo = sum(p for (k, _, _), p in banda.items() if k - 1 >= l)
                assert l * techo <= total
                for n in range(1, pasos + 2):
                    cola = sum(p for (_, _, j), p in original.items() if j >= n)
                    assert F(cola, total) <= F(1, l) + F(l - 1, n)
                    cotas += 1
                bandas[l] = avanzar(banda, l)
            niveles += 1
            original = avanzar(original)
    return {'semillas': len(semillas), 'pasos': pasos, 'niveles': niveles,
            'cotas_mixtos': cotas, 'techos': techos,
            'motor': 'por_par: dos enteros positivos y mapa atajo; independiente de Lean'}


def techo_log2(n):
    return (n - 1).bit_length()


def parametros(m):
    t = 768 * m + 128
    n = 256 * (t + 1)**2
    l = 16 * (t + 1)
    a = 1 + (n + 2).bit_length()
    s = 3 * techo_log2(n + 1)
    h = n * (a + s + 1)
    q = t + 1
    r = (128 * (h + 1) * q)**2
    g = 3 * (r + 1)
    d = 16 * (techo_log2(g + 2) + 1)**2
    b = techo_log2(4 * q)
    ell = techo_log2(d + 2)
    assert F(1, l) + F(l - 1, n) <= F(1, 8 * (t + 1))
    assert F(n, 2**s) <= F(1, n**2) <= F(1, 8 * (t + 1))
    assert 4 * q <= 2**b and d + 2 <= 2**ell
    return {'m': m, 'T_m': t, 'H_m': h, 'Q_m': q, 'G_m': g,
            'D_m': d, 'b_m': b, 'ell_m': ell, 'z_m': m - ell - 1 - d - b}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pasos', type=int, default=10)
    parser.add_argument('--m', nargs='+', type=int, default=[10, 1000, 1000000])
    parser.add_argument('--salida', type=Path)
    args = parser.parse_args()
    if not 0 <= args.pasos <= 14 or any(m < 10 or m > 10**9 for m in args.m):
        parser.error('pasos debe estar en 0..14 y m en 10..10^9')
    assert 4 * 1025 * 61**1024 <= 62**1024
    # El paso inductivo 61*(T+2)<=62*(T+1) equivale a T>=60.
    assert 61 * (60 + 2) == 62 * (60 + 1)
    resultado = {'alcance': 'Contraste finito exacto y aritmetica; CF_H sigue candidata.',
                 'arboles': contrastar_arboles(args.pasos),
                 'producto': 'base T=1024 y umbral exacto T>=60 del paso inductivo',
                 'parametros': [parametros(m) for m in args.m]}
    texto = json.dumps(resultado, ensure_ascii=False, indent=2)
    if args.salida:
        args.salida.write_text(texto + '\n', encoding='utf-8')
    print(texto)


if __name__ == '__main__':
    main()
