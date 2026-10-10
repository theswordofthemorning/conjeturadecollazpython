"""Contraste del balance par, excursiones 110 y una familia modular exacta."""

import argparse
from fractions import Fraction
import hashlib
from itertools import groupby
import json
from pathlib import Path


def orbita(n, pasos):
    valores, potencias, s = [n], [Fraction(1)], 0
    for j in range(pasos):
        x = valores[-1]
        s += x % 2
        valores.append((3 * x + 1) // 2 if x % 2 else x // 2)
        potencias.append(Fraction(3 ** s, 2 ** (j + 1)))
    return valores, potencias


def residuo(palabra):
    multiplicador, aditivo, modulo = 1, 0, 1
    for bit in palabra:
        if bit == '1':
            multiplicador *= 3
            aditivo = 3 * aditivo + modulo
        modulo *= 2
    return (-aditivo * pow(multiplicador, -1, modulo)) % modulo, modulo


def cotejar_tramo(valores, potencias, u, v):
    bits = ''.join(str(x % 2) for x in valores[u:v])
    if v == u + 1:
        return dict(regular=True, bloques=0)
    grupos = [(bit, len(list(g))) for bit, g in groupby(bits)]
    assert grupos[0][0] == '1' and grupos[-1][0] == '0'
    impares = [a for bit, a in grupos if bit == '1']
    pares = [b for bit, b in grupos if bit == '0']
    h = len(impares)
    assert len(pares) == h
    x = valores[u]
    j, s, e, reserva = u, 0, 0, Fraction(x + 1)
    for i, (a, b) in enumerate(zip(impares, pares)):
        y = valores[j + a + b]
        assert 2 ** (a + b) * (y + 1) + 2 ** a == 3 ** a * (valores[j] + 1) + 2 ** (a + b)
        q = potencias[j] / potencias[u]
        assert Fraction(valores[j] + 1, q) == reserva
        assert reserva <= x + 1 + i
        assert 2 ** (s + a + e) <= 3 ** s * (x + 1 + i)
        assert (valores[j] + 1) % 2 ** a == 0
        j += a + b
        q_siguiente = potencias[j] / potencias[u]
        reserva += (1 - Fraction(1, 2 ** b)) / q_siguiente
        assert Fraction(y + 1, q_siguiente) == reserva
        s += a
        e += b
    assert j == v and s + e == v - u
    regular = all(a == 2 for a in impares) and all(b == 1 for b in pares[:-1])
    if regular:
        assert (x + 5) % 8 ** (h - 1) == 0
        assert h <= x + 5
        assert s == 2 * h
    return dict(regular=regular, bloques=h)


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--n-max', type=int, required=True)
    analizador.add_argument('--pasos', type=int, required=True)
    analizador.add_argument('--nivel-max', type=int, required=True)
    analizador.add_argument('--k-max', type=int, required=True)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    assert args.n_max >= 2 and args.pasos >= 1 and args.nivel_max >= 0 and args.k_max >= 10
    cuentas = dict(intervalos=0, unitarios=0, regulares_no_unitarios=0,
                   irregulares=0, bloques=0, familia=0, bloques_familia=0)
    ejemplos = []
    for n in range(2, args.n_max + 1):
        valores, potencias = orbita(n, args.pasos)
        fin = next((j for j, p in enumerate(potencias) if p < 1), len(potencias))
        for c in range(args.nivel_max + 1):
            visitas = [j for j in range(fin) if potencias[j] <= 3 ** c]
            for u, v in zip(visitas, visitas[1:]):
                dato = cotejar_tramo(valores, potencias, u, v)
                cuentas['intervalos'] += 1
                cuentas['bloques'] += dato['bloques']
                etiqueta = 'unitarios' if v == u + 1 else ('regulares_no_unitarios' if dato['regular'] else 'irregulares')
                cuentas[etiqueta] += 1
                if dato['regular']:
                    assert v - u <= (24 + 2 * c) * valores[u]
                    assert (v - u) ** 2 <= (24 + 2 * c) ** 2 * (3 ** c * n) ** 6 * (u + 1)
    for k in range(10, args.k_max + 1):
        b = 0
        while 9 ** k > 3 * 8 ** k * 2 ** b:
            b += 1
        assert b >= 1 and 3 * 8 ** k * 2 ** (b - 1) < 9 ** k
        m = (5 * pow(9 ** k, -1, 2 ** b)) % 2 ** b
        assert 1 <= m < 2 ** b and m % 2 == 1
        n = 8 ** k * m - 5
        palabra = '110' * k + '0' * b
        minimo, modulo = residuo(palabra)
        assert minimo == n and 8 ** k - 5 <= n < modulo
        valores, potencias = orbita(n, len(palabra))
        assert ''.join(str(x % 2) for x in valores[:-1]) == palabra
        assert all(p >= 1 for p in potencias)
        for j in range(k + 1):
            assert valores[3 * j] + 5 == 9 ** j * 8 ** (k - j) * m
        visitas = [j for j, p in enumerate(potencias) if p <= 3]
        u, v = visitas[-2:]
        assert u == 27 and v == 3 * k + b
        assert all(p > 3 for p in potencias[u + 1:v])
        assert Fraction(3, 2) < potencias[v] <= 3
        dato = cotejar_tramo(valores, potencias, u, v)
        assert dato['regular'] and dato['bloques'] == k - 9
        assert valores[u] + 5 == 9 ** 9 * 8 ** (k - 9) * m
        cuentas['familia'] += 1
        cuentas['bloques_familia'] += dato['bloques']
        if k in {10, 16, 32, 64, args.k_max}:
            ejemplos.append(dict(k=k, b=b, m=m, n=n, u=u, v=v, h=k - 9,
                                 pares_interiores=1, ultimo_par=b + 1, minimo_modular=True))
    resultado = dict(estado='contraste finito exacto; la familia cambia de semilla con k',
                     parametros={k: v for k, v in vars(args).items() if k != 'salida'},
                     sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                     cuentas=cuentas, ejemplos=ejemplos)
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(cuentas, ensure_ascii=False))


if __name__ == '__main__':
    main()
