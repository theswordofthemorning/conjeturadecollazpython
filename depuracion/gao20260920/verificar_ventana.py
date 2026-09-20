"""Contraste exacto de la ventana conjunta; no prueba CF_H ni enumera su horizonte."""

import argparse
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

from verificar import por_par


def trayectoria(c_inicial, bits):
    k, c = 2, c_inicial
    resto, producto = F(0), F(1)
    restos, normalizados = [resto], [producto]
    tau = offset_salida = None
    prolongaciones = 0
    for t, bit in enumerate(bits, 1):
        factor = F(1 + 2 * bit, 2)
        if tau is None:
            hijo = por_par(k, c, bit)
            assert hijo[0] == 'estado' and hijo[1] >= 1
            u = F(c, 3**k)
            nuevo_u = F(hijo[2], 3**hijo[1])
            error = nuevo_u - factor * u
            assert abs(error) <= F(1, 2)
            resto = factor * resto + error
            k, c = hijo[1:]
            if k == 1:
                tau, offset_salida = t, c
        else:
            anterior = resto
            resto *= factor
            prolongaciones += resto != anterior
        producto *= factor
        if tau is None or tau == t:
            assert F(c, 3**k) == producto * F(c_inicial, 9) + resto
        restos.append(resto)
        normalizados.append(producto / F(31, 32)**t)
    return tau, offset_salida, restos, normalizados, prolongaciones


def contrastar_eventos(pasos):
    semillas = (-9, -2, -1, 0, 1, 2, 9)
    radios = (F(0), F(1, 2), F(2), F(9))
    palabras = inclusiones = salidas_borde = prolongaciones = cotas_producto = 0
    for h in range(pasos + 1):
        for c in semillas:
            cruces = [0] * (h + 1)
            for bits in product((0, 1), repeat=h):
                tau, d, restos, normalizados, cambios = trayectoria(c, bits)
                palabras += 1
                prolongaciones += cambios
                salidas_borde += tau == h and tau is not None
                for t in range(h + 1):
                    assert F(31, 32)**t * abs(F(c, 9)) <= 1
                    sobrevive_t = tau is None or tau > t
                    sobrevive_h = tau is None
                    mal_producto = max(normalizados[t:]) > 1
                    cruces[t] += mal_producto
                    for r in radios:
                        mal_resto = max(map(abs, restos)) > r
                        buena = tau is not None and t < tau <= h and abs(d) <= 3 * (r + 1)
                        assert int(sobrevive_t) <= int(buena) + int(sobrevive_h) + int(mal_producto) + int(mal_resto)
                        if sobrevive_t and not (sobrevive_h or mal_producto or mal_resto):
                            assert buena
                        inclusiones += 1
            for t, cuenta in enumerate(cruces):
                assert F(cuenta, 2**h) <= F(61, 62)**t
                cotas_producto += 1
    return {'semillas': semillas, 'horizontes': [0, pasos], 'radios': list(map(str, radios)),
            'palabras': palabras, 'inclusiones': inclusiones, 'cotas_producto': cotas_producto,
            'salidas_en_H': salidas_borde, 'cambios_W_tras_salida': prolongaciones}


def parametros(c):
    m = (1 + abs(c)).bit_length()
    t = 32 * max(32, m)
    q = t + 1
    l = 16 * q
    n = l**2
    a = 1 + (n + 2).bit_length()
    s = 3 * n.bit_length()
    h = n * (a + s + 1)
    r = (128 * (h + 1) * q)**2
    assert abs(c) * 31**t <= 9 * 32**t
    assert 4 * q * 61**t <= 62**t
    assert F(1, l) + F(l - 1, n) + F(n, 2**s) <= F(1, 4 * q)
    assert t <= h
    return {'c': c, 'T': t, 'H': h, 'G': 3 * (r + 1), 'piso': str(F(1, 4 * q))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pasos', type=int, default=8)
    parser.add_argument('--salida', type=Path)
    args = parser.parse_args()
    if not 0 <= args.pasos <= 10:
        parser.error('pasos debe estar en 0..10')
    semillas_grandes = (-2**127 - 1, -17, -1, 0, 1, 17, 2**127, 2**1024)
    resultado = {'alcance': 'Contraste finito de eventos y parametros, sin prueba de CF_H.',
                 'motor': 'por_par: dos enteros positivos; Fraction para W y producto',
                 'eventos': contrastar_eventos(args.pasos),
                 'parametros': [parametros(c) for c in semillas_grandes]}
    texto = json.dumps(resultado, ensure_ascii=False, indent=2)
    if args.salida:
        args.salida.write_text(texto + '\n', encoding='utf-8')
    print(texto)


if __name__ == '__main__':
    main()
