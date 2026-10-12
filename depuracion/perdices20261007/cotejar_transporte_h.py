"""Contrasta el tamaño del empalme con el transporte del mínimo concatenado.

Mapa F y dominio C=15 mod 24, positivos. Se comparan tres cálculos:
CRT del punto medio, cilindro de la historia concatenada e iteración de H.
Las identidades se cotejan con enteros/Fraction; no excluyen persistencia.
"""

import argparse
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path

from cotejar_rachas_h import cilindro, empalmar, seguir


def afin(historia):
    a_total, m_total, b_total = 1, 1, 0
    for a, b in historia:
        pendiente, divisor = 3 ** (a + 2 * b), 2 ** (2 * a + 3 * b)
        constante = 3 ** a * (9 ** b - 8 ** b)
        a_total, m_total, b_total = (pendiente * a_total, divisor * m_total,
                                    pendiente * b_total + constante * m_total)
    return a_total, m_total, b_total


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--profundidad', type=int, required=True)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    assert 0 <= args.profundidad <= 3
    etiquetas = [(1, 1), (1, 2), (1, 3), (2, 1)]
    historias = [h for k in range(args.profundidad + 1) for h in product(etiquetas, repeat=k)]
    parejas = cotas = trayectorias = 0
    mayor_error = Fraction()
    for pasado in historias:
        rp, mp, sp, ap = cilindro(pasado)
        aa, mm, bp = afin(pasado)
        assert aa == ap and mm == mp and mp * sp == ap * rp + bp
        for futuro in historias:
            _, mq, _, _ = cilindro(futuro)
            r, m, s, a = cilindro(pasado + futuro)
            medio, periodo = empalmar(pasado, futuro)
            assert m == mp * mq and periodo == 24 * ap * mq
            assert medio == seguir(r, pasado)
            assert mp * medio == ap * r + bp
            desplazamiento = (r - rp) // (24 * mp)
            assert r == rp + 24 * mp * desplazamiento
            assert medio == sp + 24 * ap * desplazamiento
            error = Fraction(medio, 24 * ap * mq) - Fraction(r, 24 * mp * mq)
            assert error == Fraction(bp, 24 * ap * mp * mq)
            mayor_error = max(mayor_error, error)
            # Comparar también semillas del prefijo P que no necesariamente siguen Q.
            for indice in {0, max(0, desplazamiento - 1), desplazamiento, desplazamiento + 1}:
                n = rp + 24 * mp * indice
                y = seguir(n, pasado)
                assert (n >= r) == (y >= medio)
                assert mp * (y - medio) == ap * (n - r)
                cotas += 1
            for indice in (0, 1):
                n = r + 24 * m * indice
                y = seguir(n, pasado)
                assert y == medio + periodo * indice
                assert seguir(y, futuro) == s + 24 * a * indice
                trayectorias += 1
            parejas += 1
    archivos = [Path(__file__), Path(__file__).with_name('cotejar_rachas_h.py')]
    resultado = dict(parametros=dict(profundidad=args.profundidad, etiquetas=etiquetas),
                     parejas=parejas, equivalencias_de_cotas=cotas,
                     trayectorias_completas=trayectorias,
                     mayor_diferencia_normalizada=str(mayor_error),
                     fuentes={p.name: hashlib.sha256(p.read_text(encoding='utf-8').encode('utf-8')).hexdigest()
                              for p in archivos},
                     alcance='Cotejo de la identidad escrita en RACHAS_H.md, sección 7. '
                     'La cota del punto de empalme equivale a la del mínimo concatenado; '
                     'no es una restricción de tamaño independiente. Sin Lean nuevo.')
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'OK: {parejas} parejas, {cotas} cotas y {trayectorias} trayectorias completas.')


if __name__ == '__main__':
    main()
