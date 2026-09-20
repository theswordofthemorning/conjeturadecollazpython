"""Contraste entero de M6/H3 y de rachas; no demuestra el candidato CF_H."""

import argparse
from collections import Counter
from fractions import Fraction
import json
from pathlib import Path

from verificar import por_par


SEMILLAS = (-2**31 - 1, -17, -1, 0, 1, 2, 17, 2**31)


def avanzar(distribucion):
    siguiente = Counter()
    for (k, c, mixtos), peso in distribucion.items():
        if k == 1:
            siguiente[k, c, mixtos] += 2 * peso
            continue
        for bit in (0, 1):
            hijo = por_par(k, c, bit)
            assert hijo[0] == 'estado' and hijo[1] >= 1
            siguiente[hijo[1], hijo[2], mixtos + c % 2] += peso
    return siguiente


def contrastar_reloj(pasos):
    casos_m6 = casos_h3 = identidades = 0
    for c in SEMILLAS:
        distribucion = Counter({(2, c, 0): 1})
        for h in range(pasos + 1):
            total = 2**h
            assert sum(distribucion.values()) == total
            assert all(k - 1 <= j + 1 for (k, _, j) in distribucion)
            vivos = sum(p for (k, _, _), p in distribucion.items() if k >= 2)
            for n in range(pasos + 1):
                retraso = sum(p for (k, _, j), p in distribucion.items() if k >= 2 and j < n)
                supera = sum(p for (_, _, j), p in distribucion.items() if j >= n)
                vivos_supera = sum(p for (k, _, j), p in distribucion.items() if k >= 2 and j >= n)
                assert vivos == retraso + vivos_supera
                assert vivos <= retraso + supera
                identidades += 1
                a = 1 + (n + 2).bit_length()
                for s in range(pasos + 1):
                    if h != n * (a + s + 1):
                        continue
                    assert Fraction(retraso, total) <= Fraction(n, 2**s)
                    casos_m6 += 1
                    if n == 0:
                        continue
                    for l in (1, 2, 3, 5, 9):
                        cota = Fraction(1, l) + Fraction(l - 1, n) + Fraction(n, 2**s)
                        assert Fraction(vivos, total) <= cota
                        casos_h3 += 1
            if h < pasos:
                distribucion = avanzar(distribucion)
    return {'semillas': list(SEMILLAS), 'horizontes': [0, pasos],
            'casos_M6': casos_m6, 'casos_H3': casos_h3,
            'descomposiciones_evento': identidades}


def contrastar_rachas():
    casos = 0
    testigos_ajuste = 0
    for k in range(2, 13):
        diferencia = 3**k - 1
        a = (diferencia & -diferencia).bit_length() - 1
        assert 1 <= a <= 1 + k.bit_length()
        for c in SEMILLAS:
            r = a if c == 0 else min(a, (abs(c) & -abs(c)).bit_length() - 1)
            distribucion = Counter({c: 1})
            for h in range(a + 7):
                cuenta = sum(distribucion.values())
                # L>=h: se permite que el último paso deje un offset impar.
                esperado = (2**h if h <= r else 0) if r < a else 2**min(h, a)
                assert cuenta == esperado
                if h >= a:
                    assert Fraction(cuenta, 2**h) <= Fraction(1, 2**(h-a))
                    testigos_ajuste += cuenta == 2**a
                casos += 1
                siguiente = Counter()
                for offset, peso in distribucion.items():
                    if offset % 2:
                        continue
                    for bit in (0, 1):
                        hijo = por_par(k, offset, bit)
                        assert hijo[0] == 'estado' and hijo[1] == k
                        siguiente[hijo[2]] += peso
                distribucion = siguiente
    return {'alturas_k': [2, 12], 'casos': casos, 'igualdades_cota': testigos_ajuste,
            'evento': 'al menos h pasos compartidos; no exige offset par después de h'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pasos', type=int, default=16)
    parser.add_argument('--salida', type=Path)
    args = parser.parse_args()
    if not 0 <= args.pasos <= 18:
        parser.error('pasos debe estar en 0..18')
    resultado = {'alcance': 'Contraste finito exacto de la interpretación; no prueba CF_H.',
                 'motor': 'por_par: reconstrucción de dos enteros positivos, sin importar Lean',
                 'rachas': contrastar_rachas(), 'reloj': contrastar_reloj(args.pasos)}
    texto = json.dumps(resultado, ensure_ascii=False, indent=2)
    if args.salida:
        args.salida.write_text(texto + '\n', encoding='utf-8')
    print(texto)


if __name__ == '__main__':
    main()
