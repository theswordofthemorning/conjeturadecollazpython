"""Identidades finitas de la cola, familia de bloques y control de topologías."""

import argparse
from fractions import Fraction
import hashlib
import json
from math import isqrt
from pathlib import Path


def paso(x):
    return (3 * x + 1) // 2 if x % 2 else x // 2


def recorrido(n, pasos):
    valores, inversos, normalizados = [n], [Fraction(1)], [Fraction(n)]
    x, s = n, 0
    for j in range(pasos):
        s += x % 2
        x = paso(x)
        inverso = Fraction(2 ** (j + 1), 3 ** s)
        valores.append(x)
        inversos.append(inverso)
        normalizados.append(inverso * x)
    return valores, inversos, normalizados


def identidades(nmax, pasos):
    cantidad, colas = 0, 0
    for n in range(1, nmax + 1):
        x, inversos, normalizados = recorrido(n, pasos)
        pares, impares, todos = Fraction(0), Fraction(0), Fraction(0)
        for k in range(pasos + 1):
            aumentado = normalizados[k] + inversos[k]
            assert normalizados[k] == n + impares / 3
            assert aumentado == n + 1 + pares
            assert todos == 4 * (normalizados[k] - n) + inversos[k] - 1
            cantidad += 1
            if k < pasos:
                if x[k] % 2:
                    impares += inversos[k]
                else:
                    pares += inversos[k]
                todos += inversos[k]
        # Corte finito K: la cola termina en cero y no satisface la cota infinita >=1.
        cola = Fraction(0)
        for k in range(pasos - 1, -1, -1):
            cola = (2 * cola + 1) / 3 if x[k] % 2 else 2 * cola
            directa = (normalizados[-1] - normalizados[k]) / inversos[k]
            assert cola == directa
            suma_pares = sum((inversos[j] / inversos[k] for j in range(k, pasos)
                              if x[j] % 2 == 0), Fraction(0))
            assert cola == 1 + suma_pares - inversos[-1] / inversos[k]
            colas += 1
    return dict(identidades=cantidad, colas_finitas=colas,
                nota='Se incluyen ciclos; sólo se cotejan identidades finitas, no límites de fugas.')


def familia(qmax):
    ejemplos = []
    for q in range(1, qmax + 1):
        palabra = [1] * (2 * q) + [0] * q + [1, 1]
        largo = len(palabra)
        aditivo = 9 * (3 ** (2 * q) - 2 ** (2 * q)) + 5 * 2 ** (3 * q)
        multiplicador, modulo = 3 ** (2 * q + 2), 2 ** largo
        n = (-aditivo * pow(multiplicador, -1, modulo)) % modulo
        assert 0 < n < modulo
        x, inversos, normalizados = recorrido(n, largo)
        assert [a % 2 for a in x[:-1]] == palabra
        assert all(inverso <= 1 for inverso in inversos)
        assert multiplicador * n + aditivo == modulo * x[-1]
        k = 2 * q
        cola = (normalizados[-1] - normalizados[k]) / inversos[k]
        assert cola == Fraction(5 * 2 ** q, 9)
        assert Fraction(x[k], 2 ** q).denominator == 1
        ejemplos.append(dict(q=q, n=str(n), k=k, K=largo, entrada=str(x[k]),
                             cola_finita=str(cola)))
    return ejemplos


def topologias(mmax):
    ejemplos = []
    for m in range(1, mmax + 1):
        a = isqrt((2 * 3 ** (2 * m)) // (2 ** (2 * m)))
        racional = Fraction(2 ** m * a, 3 ** m)
        error = Fraction(2, 3) ** m
        assert racional ** 2 <= 2 < (racional + error) ** 2
        residuo = (racional.numerator * pow(racional.denominator, -1, 2 ** m)) % (2 ** m)
        assert residuo == 0
        if m in (1, 2, 3, mmax):
            ejemplos.append(dict(m=m, aproximante=str(racional),
                                 error_menor_que=str(error), residuo=residuo))
    return dict(comprobaciones=mmax, ejemplos=ejemplos,
                alcance='Límite real sqrt(2), límite 2-ádico 0: no son sumas de una palabra Collatz.')


def minimo_futuro(mmax):
    # Cola geométrica de la cuenta orbital, sin calcular exp ni simular fugas.
    for m in range(mmax + 1):
        presupuesto = Fraction(3 * 2 ** 100, 2 ** m)
        acumulado = Fraction(0)
        for j in range(m, m + 17):
            acumulado += Fraction(3 * 2 ** (99 * (j + 1)), 2 ** (100 * j))
            resto = Fraction(3 * 2 ** 100, 2 ** (j + 1))
            assert acumulado + resto == presupuesto
    return dict(minimos=mmax + 1, anillos_por_minimo=17,
                cota='sum 1/x_j <= 3*2^100/2^m si todos los x_j >=2^(100m)')


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--nmax', type=int, default=128)
    analizador.add_argument('--pasos', type=int, default=96)
    analizador.add_argument('--qmax', type=int, default=64)
    analizador.add_argument('--mmax', type=int, default=128)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    assert min(args.nmax, args.pasos, args.qmax, args.mmax) >= 1
    evidencia = dict(parametros=dict(nmax=args.nmax, pasos=args.pasos,
                                     qmax=args.qmax, mmax=args.mmax),
                     identidades=identidades(args.nmax, args.pasos), familia=familia(args.qmax),
                     topologias=topologias(args.mmax), minimo_futuro=minimo_futuro(args.mmax))
    # Borde: n=1, un paso, cola finita 1/3, incompatible con aplicar el límite >=1.
    x, inversos, normalizados = recorrido(1, 1)
    assert normalizados[-1] - normalizados[0] == Fraction(1, 3)
    evidencia['borde_cola_finita'] = 'n=1, k=0, K=1: cola=1/3<1'
    evidencia['sha256_fuente_lf'] = hashlib.sha256(
        Path(__file__).read_text(encoding='utf-8').encode('utf-8')).hexdigest()
    args.salida.write_text(json.dumps(evidencia, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"OK: {evidencia['identidades']['identidades']} identidades, "
          f"{evidencia['identidades']['colas_finitas']} colas, {args.qmax} bloques; "
          f"{args.mmax} aproximantes y {args.mmax + 1} presupuestos.")


if __name__ == '__main__':
    main()
