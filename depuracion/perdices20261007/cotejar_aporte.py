"""Aportes racionales exactos y familia con muchas excepciones de poco efecto."""

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


def representante(palabra):
    a, b, modulo = 1, 0, 1
    for bit in palabra:
        if bit == '1':
            a, b = 3 * a, 3 * b + modulo
        modulo *= 2
    return (-b * pow(a, -1, modulo)) % modulo


def verificar(valores, potencias, u, v):
    assert u + 1 < v
    grupos = [(bit, len(list(g))) for bit, g in groupby(x % 2 for x in valores[u:v])]
    assert grupos[0][0] == 1 and grupos[-1][0] == 0
    bloques = [(grupos[i][1], grupos[i + 1][1]) for i in range(0, len(grupos), 2)]
    tiempos, suma, firmada, e = [u], Fraction(0), Fraction(0), 0
    masa_excepciones = Fraction(0)
    for a, b in bloques:
        t = tiempos[-1]
        fin = t + a + b
        p = potencias[t]
        assert p >= potencias[u]
        aporte = (1 - Fraction(2, 3) ** a) / p
        assert Fraction(valores[fin], potencias[fin]) - Fraction(valores[t], p) == aporte
        assert 0 < aporte < 1 / p
        suma += aporte
        for desplazamiento in (0, 1, 3, 5, 7):
            correccion = Fraction(3 ** a - 2 ** a + desplazamiento * (2 ** (a + b) - 3 ** a), 3 ** a)
            cambio = Fraction(valores[fin] + desplazamiento, potencias[fin]) - Fraction(valores[t] + desplazamiento, p)
            assert cambio == correccion / p
            if desplazamiento == 5:
                if (a, b) == (2, 1):
                    assert cambio == 0
                else:
                    firmada += cambio
                    masa_excepciones += 1 / p
                    e += 1
        tiempos.append(fin)
    assert tiempos[-1] == v
    diferencia = Fraction(valores[v], potencias[v]) - Fraction(valores[u], potencias[u])
    assert suma == diferencia
    assert firmada == Fraction(valores[v] + 5, potencias[v]) - Fraction(valores[u] + 5, potencias[u])
    cadenas, masa_cadenas, comprimida = 0, Fraction(0), Fraction(0)
    for buena, grupo in groupby(enumerate(bloques), key=lambda z: z[1] == (2, 1)):
        indices = [i for i, _ in grupo]
        if buena:
            inicio, fin, k = tiempos[indices[0]], tiempos[indices[-1] + 1], len(indices)
            p = potencias[inicio]
            delta = Fraction(valores[fin], potencias[fin]) - Fraction(valores[inicio], p)
            assert delta == 5 * (1 - Fraction(8, 9) ** k) / p
            assert 0 < delta < 5 / p
            comprimida += delta
            masa_cadenas += 1 / p
            cadenas += 1
        else:
            comprimida += sum((1 - Fraction(2, 3) ** bloques[i][0]) / potencias[tiempos[i]] for i in indices)
    assert cadenas <= e + 1
    assert comprimida == diferencia < masa_excepciones + 5 * masa_cadenas
    assert diferencia < Fraction(6 * e + 5, potencias[u])
    return dict(bloques=len(bloques), excepciones=e, cadenas=cadenas,
                cambio_r=diferencia, cambio_cinco=firmada, masa_excepciones=masa_excepciones)


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--n-max', type=int, required=True)
    analizador.add_argument('--pasos', type=int, required=True)
    analizador.add_argument('--nivel-max', type=int, required=True)
    analizador.add_argument('--k-max', type=int, required=True)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    assert args.n_max >= 2 and args.pasos >= 1 and args.nivel_max >= 0 and args.k_max >= 3
    cuentas = dict(excursiones=0, bloques=0, cadenas=0, signo_positivo=0, signo_cero=0,
                   signo_negativo=0, familia=0, bloques_familia=0)
    for n in range(2, args.n_max + 1):
        valores, potencias = orbita(n, args.pasos)
        fin = next((j for j, p in enumerate(potencias) if p < 1), len(potencias))
        for c in range(args.nivel_max + 1):
            visitas = [j for j in range(fin) if potencias[j] <= 3 ** c]
            for u, v in zip(visitas, visitas[1:]):
                if v == u + 1:
                    continue
                dato = verificar(valores, potencias, u, v)
                cuentas['excursiones'] += 1
                cuentas['bloques'] += dato['bloques']
                cuentas['cadenas'] += dato['cadenas']
                signo = 'positivo' if dato['cambio_cinco'] > 0 else ('negativo' if dato['cambio_cinco'] < 0 else 'cero')
                cuentas['signo_' + signo] += 1
    signos = []
    for n, u, v, esperado in [(7, 2, 4, Fraction(8, 9)), (15, 2, 5, Fraction(0)), (63, 2, 8, Fraction(-80, 729))]:
        valores, potencias = orbita(n, v)
        assert all(p >= 1 for p in potencias)
        assert potencias[u] <= 3 and potencias[v] <= 3 and all(p > 3 for p in potencias[u + 1:v])
        dato = verificar(valores, potencias, u, v)
        assert dato['cambio_cinco'] == esperado
        signos.append(dict(n=n, u=u, v=v, cambio_r=str(dato['cambio_r']), cambio_cinco=str(esperado)))
    ejemplos = []
    for k in range(3, args.k_max + 1):
        b = 0
        while 27 ** k > 3 * 16 ** k * 2 ** b:
            b += 1
        assert b >= 1 and 3 * 16 ** k * 2 ** (b - 1) < 27 ** k
        m = (19 * pow(27 ** k, -1, 11 * 2 ** b)) % (11 * 2 ** b)
        assert m % 2 == 1 and m > 0
        assert (16 ** k * m - 19) % 11 == 0
        n = (16 ** k * m - 19) // 11
        palabra = '1110' * k + '0' * b
        assert representante(palabra) == n and 0 < n < 2 ** len(palabra)
        valores, potencias = orbita(n, len(palabra))
        assert ''.join(str(x % 2) for x in valores[:-1]) == palabra
        assert all(p >= 1 for p in potencias)
        for j in range(k + 1):
            assert 11 * valores[4 * j] + 19 == 27 ** j * 16 ** (k - j) * m
        visitas = [j for j, p in enumerate(potencias) if p <= 3]
        u, v = visitas[-2:]
        assert (u, v) == (8, 4 * k + b)
        dato = verificar(valores, potencias, u, v)
        assert dato['excepciones'] == dato['bloques'] == k - 2
        exacta = Fraction(19, 11) * (Fraction(16, 27) ** 2 - Fraction(16, 27) ** k)
        assert dato['cambio_r'] == exacta < Fraction(4864, 8019)
        assert exacta == Fraction(19, 27) * dato['masa_excepciones']
        cuentas['familia'] += 1
        cuentas['bloques_familia'] += dato['bloques']
        if k in {3, 8, 16, 64, args.k_max}:
            ejemplos.append(dict(k=k, b=b, m=m, n=n, u=u, v=v, excepciones=k - 2,
                                 cambio_r=str(exacta), cambio_por_excepcion=str(exacta / (k - 2))))
    resultado = dict(estado='contraste exacto finito; la familia cambia de semilla',
                     parametros={k: v for k, v in vars(args).items() if k != 'salida'},
                     sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                     cuentas=cuentas, signos=signos, ejemplos=ejemplos)
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(cuentas, ensure_ascii=False))


if __name__ == '__main__':
    main()
