"""Contraste exacto y acotado del protocolo; no verifica el cierre de Gao."""
from fractions import Fraction
from functools import lru_cache
from itertools import product
from pathlib import Path
import argparse
import json


def paso(estado, bit):
    base, _ = estado
    nueva = 2 if base == 2 else (bit if base == 0 else 2 * bit)
    return nueva, base == 0 and nueva == 1


def guardia(estado):
    return estado == (1, True)


def trayectoria(palabra, inicial):
    estados = [inicial]
    for bit in palabra:
        estados.append(paso(estados[-1], bit))
    return estados


def verificar(hasta):
    casos = inclusiones = comparaciones = 0
    riesgos = {}
    for ancho in (1, 2, 3):
        supervivencia = Fraction(sum(
            trayectoria(bs, (1, True))[-1][0] != 2
            for bs in product((0, 1), repeat=ancho)), 2 ** ancho)
        riesgos[str(ancho)] = str(1 - supervivencia)

        @lru_cache(None)
        def promedio(j, h, estado):
            if j == 0:
                return Fraction(1)
            if h == 0:
                return Fraction(0)
            if guardia(estado) and ancho <= h:
                total = Fraction(0)
                for bs in product((0, 1), repeat=ancho):
                    final = trayectoria(bs, estado)[-1]
                    if final[0] != 2:
                        total += promedio(j - 1, h - ancho, (final[0], False))
                return total / 2 ** ancho
            return sum((promedio(j, h - 1, paso(estado, b))
                        for b in (0, 1)), Fraction(0)) / 2

        for inicial in ((0, False), (1, True), (1, False), (2, False)):
            for h in range(hasta + 1):
                cuentas = [0] * 4
                for bs in product((0, 1), repeat=h):
                    estados = trayectoria(bs, inicial)
                    entradas = sum(map(guardia, estados))
                    vivo = estados[-1][0] != 2
                    i = fallidos = 0
                    while i < h:
                        if guardia(estados[i]) and i + ancho <= h:
                            final = i + ancho
                            if estados[final][0] == 2:
                                break
                            fallidos += 1
                            # La marca se borra al reiniciar: saltar el extremo.
                            i = final + 1
                        else:
                            i += 1
                    for j in range(4):
                        evento = fallidos >= j
                        cuentas[j] += evento
                        if vivo and entradas >= 1 + j * (ancho + 2):
                            assert evento, (ancho, inicial, bs, j)
                            inclusiones += 1
                    casos += 1
                for j, cantidad in enumerate(cuentas):
                    probabilidad = Fraction(cantidad, 2 ** h)
                    assert probabilidad == promedio(j, h, inicial)
                    assert probabilidad <= supervivencia ** j
                    comparaciones += 1
    return {'alcance': 'Cadena auxiliar finita absorbente; contraste del protocolo y conteo, no de EF ni CF_F.',
            'h_maximo': hasta, 'palabras_y_estados': casos,
            'inclusiones': inclusiones, 'comparaciones_racionales': comparaciones,
            'riesgos_por_ancho': riesgos}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--hasta', type=int, default=10)
    parser.add_argument('--salida', type=Path)
    args = parser.parse_args()
    assert 0 <= args.hasta <= 16
    resultado = json.dumps(verificar(args.hasta), ensure_ascii=False, indent=2)
    if args.salida:
        args.salida.write_text(resultado + '\n', encoding='utf-8')
    print(resultado)
