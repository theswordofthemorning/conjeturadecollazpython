"""Contraste de Hormigas y del relevo a absorción; no prueba CF_H."""

import argparse
from collections import Counter
from fractions import Fraction as F
import json
from pathlib import Path

from verificar import por_par, longitud
from verificar_armonica import parametros


def viaje(g):
    estado = ('estado', 0, g)
    bits = []
    if g == 1:
        orden = [0, 0, 1]
    elif g % 2 == 0:
        orden = [0]
    else:
        orden = [1]
    for bit in orden:
        estado = por_par(estado[1], estado[2], bit)
        bits.append(bit)
    if g >= 3 and g % 2:
        while estado[2] % 2 == 0:
            estado = por_par(estado[1], estado[2], 0)
            bits.append(0)
        estado = por_par(estado[1], estado[2], 1)
        bits.append(1)
    return bits, estado


def contrastar_viajes(limite):
    semillas = set(range(1, limite + 1))
    for e in (16, 31, 64, 127, 512):
        semillas.update((2**e - 1, 2**e, 2**e + 1))
    viajes = bloques = 0
    for g in sorted(semillas):
        m = g.bit_length()
        d = g
        largo = 0
        for j in range(1, 5):
            bits, estado = viaje(d)
            viajes += 1
            assert len(bits) <= m + 3
            largo += len(bits)
            if estado[0] == 'fusion':
                break
            assert estado[1] == 0 and 1 <= estado[2] <= d
            assert 6 * estado[2] <= 5 * d
            d = estado[2]
            assert 6**j * d <= 5**j * g
        else:
            assert d < 2**(m - 1)
        assert largo <= 4 * (m + 3)
        bloques += 1
    offsets = set(range(-limite, limite + 1))
    offsets.update(signo * g for signo in (-1, 1) for g in semillas if g > limite)
    peor = 0
    for c in offsets:
        largo, cota = longitud(c)
        assert largo <= cota
        peor = max(peor, largo)
    return {'gaps': len(semillas), 'viajes': viajes, 'bloques': bloques,
            'offsets': len(offsets), 'mayor_palabra': peor}


def distribuciones(estado, pasos, detener=False):
    actual = Counter({estado: 1})
    resultado = [actual]
    for _ in range(pasos):
        nuevo = Counter()
        for z, peso in actual.items():
            if z[0] == 'fusion' or (detener and z[1] == 1):
                nuevo[z] += 2 * peso
            else:
                for bit in (0, 1):
                    nuevo[por_par(z[1], z[2], bit)] += peso
        actual = nuevo
        resultado.append(actual)
    return resultado


def contrastar_relevo(pasos):
    # Presupuestos pequeños obtenidos por palabras explícitas para |d|<=G.
    # No sustituyen la cota universal, mucho mayor, de Hormigas.
    radios = (1, 2, 3)
    presupuestos = {g: max(longitud(c)[0] for c in range(-g, g + 1)) for g in radios}
    casos = 0
    for c in (-17, -2, -1, 0, 1, 2, 17):
        completa = distribuciones(('estado', 2, c), pasos + max(presupuestos.values()))
        detenida = distribuciones(('estado', 2, c), pasos, detener=True)
        for h in range(pasos + 1):
            assert sum(detenida[h].values()) == 2**h
            for g, d in presupuestos.items():
                buenos = sum(p for z, p in detenida[h].items()
                             if z[0] == 'estado' and z[1] == 1 and abs(z[2]) <= g)
                fusionados = completa[h + d].get(('fusion',), 0)
                assert sum(completa[h + d].values()) == 2**(h + d)
                assert F(buenos, 2**(h + d)) <= F(fusionados, 2**(h + d))
                casos += 1
    return {'horizontes_salida': [0, pasos], 'presupuestos_explicitados': presupuestos,
            'casos': casos, 'interpretacion': 'piso de primera salida buena multiplicado por 2^-D'}


def parametros_fijos(m):
    p = parametros(m)
    w = p['H_m'] + p['D_m']
    ell = (w + 1).bit_length()
    return {'m': m, 'W_m': w, 'ell_fijo': ell, 'D_m': p['D_m'],
            'z_fijo': m - ell - 1 - p['D_m'] - p['b_m'],
            'alcance': 'aritmetica de una posible variante global; no prueba su protocolo'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--limite', type=int, default=2048)
    parser.add_argument('--pasos', type=int, default=6)
    parser.add_argument('--salida', type=Path)
    args = parser.parse_args()
    if not 1 <= args.limite <= 8192 or not 0 <= args.pasos <= 8:
        parser.error('limite en 1..8192 y pasos en 0..8')
    resultado = {'alcance': 'Contrastes finitos independientes de Lean; no prueba global.',
                 'hormigas': contrastar_viajes(args.limite),
                 'relevo': contrastar_relevo(args.pasos),
                 'horizonte_fijo': [parametros_fijos(m) for m in (10, 1000, 1000000)]}
    texto = json.dumps(resultado, ensure_ascii=False, indent=2)
    if args.salida:
        args.salida.write_text(texto + '\n', encoding='utf-8')
    print(texto)


if __name__ == '__main__':
    main()
