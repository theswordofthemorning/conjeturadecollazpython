"""Aritmética exacta de CF; no enumera clases al horizonte global.

El parámetro m representa N=2^m y h=2^(6m). Se evita construir C_m,
cuyo tamaño binario es 24m+4, usando T_m=768m+128 para m>=10.
"""

import argparse
import json
from math import isqrt
from pathlib import Path


def techo_log2(x):
    assert x >= 1
    return (x-1).bit_length()


def parametros(m):
    assert m >= 10
    t = 768*m+128
    n = 256*(t+1)**2
    a = 2+(n+2).bit_length()-1
    s = 3*techo_log2(n+1)
    h_excursion = n*(a+s+1)
    q = isqrt(2*t+3)+1
    r = (128*(h_excursion+1)*q)**2
    g = 3*(r+1)
    d = 16*(techo_log2(g+2)+1)**2
    b = techo_log2(4*q)
    ell = techo_log2(d+2)
    return {'m': m, 'T_m': t, 'H_m': h_excursion,
            'Q_m': q, 'G_m': g, 'D_m': d,
            'b_m': b, 'ell_m': ell,
            'z_m': m-ell-1-d-b,
            'log2_h_global': 6*m}


def comprobar(m):
    fila = parametros(m)
    q, d, b, ell = (fila[k] for k in ('Q_m','D_m','b_m','ell_m'))
    assert q*q >= 2*fila['T_m']+3
    assert 4*q <= 2**b
    assert d+2 <= 2**ell
    assert (24*m+5)*(48*m+7) <= 2048*(m+1)**2
    assert 10*m+3 <= 16*(m+1)
    # El chequeo directo de potencias se limita; el caso universal es inductivo.
    if m <= 4096:
        n_visitas = 2**m
        h_global = n_visitas**6
        frontera = (24*m+5)*(48*m+7)
        interior = n_visitas**4*(10*m+3)
        assert n_visitas >= 64*(m+1)
        assert 2*n_visitas*(interior+frontera) <= h_global
        # beta_m <= 4/N después de multiplicar por 4*N*h^3.
        assert 12*h_global**3+264*n_visitas*h_global**2+n_visitas <= 16*h_global**3
        j = (n_visitas-1)//(d+2)
        if m >= ell+1:
            assert j >= 2**(m-ell-1)
    return fila


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--m', nargs='+', type=int, default=[10,1000,100000,500000,1000000])
    p.add_argument('--salida', type=Path)
    args = p.parse_args()
    if any(m < 10 or m > 10**9 for m in args.m):
        p.error('m debe estar entre 10 y 10^9')
    # Bordes del reloj y salto de J=0 a J>0; no se toma como inducción.
    for m in range(10, 65):
        comprobar(m)
    resultado = {'alcance': 'Solo aritmetica de parametros; CF probabilistica es prueba escrita candidata.',
                 'controles_borde': 'm=10..64',
                 'parametros': [comprobar(m) for m in args.m]}
    texto = json.dumps(resultado, ensure_ascii=False, indent=2)
    if args.salida:
        args.salida.write_text(texto+'\n', encoding='utf-8')
    print(texto)


if __name__ == '__main__':
    main()
