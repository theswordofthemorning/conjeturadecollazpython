"""Cotejo exacto de reinicios finitos y compatibilidad entre anchura y congruencia."""

import argparse
from fractions import Fraction
import hashlib
import json
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


def reinicios(nmax, pasos):
    cantidad, traslados, pisos = 0, 0, 0
    for n in range(1, nmax + 1):
        x, inversos, normalizados = recorrido(n, pasos)
        mayor = Fraction(0)
        for k in range(pasos, -1, -1):
            mayor = max(mayor, inversos[k])
            if inversos[k] != mayor:
                continue
            cantidad += 1
            y, locales, reales = recorrido(x[k], pasos - k)
            assert y == x[k:]
            assert all(valor <= 1 for valor in locales)
            assert all(valor >= x[k] for valor in y)
            for j in range(pasos - k + 1):
                assert inversos[k + j] == inversos[k] * locales[j]
                assert normalizados[k + j] == inversos[k] * reales[j]
                traslados += 1
            cola = (normalizados[-1] - normalizados[k]) / inversos[k]
            assert cola == reales[-1] - x[k]
            pisos += 1
    return dict(minimos_finitos=cantidad, identidades_traslado=traslados, colas_reiniciadas=pisos,
                alcance='Mínimos sólo hasta el corte; no certifican FugaPura ni mínimos de todo el futuro.')


def anillos(mmax):
    casos = 0
    for m in range(mmax + 1):
        presupuesto = Fraction(3 * 2 ** 100, 2 ** m)
        suma = Fraction(0)
        for d in range(33):
            assert suma * 2 ** (m + d) + 3 * 2 ** 100 == 3 * 2 ** (100 + d)
            assert suma <= presupuesto
            aporte = Fraction(3 * 2 ** (99 * (m + d + 1)), 2 ** (100 * (m + d)))
            suma += aporte
            casos += 1
    return dict(pisos=mmax + 1, cortes=casos, intervalo_cortes=[0, 32])


def compatibilidad(lmax):
    cantidad, pasos = 0, 0
    muestras = []
    for largo in range(2, lmax + 1):
        n = 2 ** largo - 1
        theta = 1 + Fraction(2, 3) ** largo
        xi = n + theta  # Parámetro de un prefijo: NO es un límite orbital demostrado.
        x, inversos, normalizados = recorrido(n, largo)
        m = (n.bit_length() - 1) // 100
        assert 2 ** (100 * m) <= n < 2 ** (100 * (m + 1))
        assert theta ** 100 <= n ** 99
        u = Fraction(2 ** 100, 2 ** m)
        # exp(u)-1>=u: esta desigualdad racional basta para satisfacer la cota mayor.
        assert theta <= n * u
        for j in range(largo + 1):
            a, modulo, b = 3 ** j, 2 ** j, 3 ** j - 2 ** j
            assert x[j] == 3 ** j * 2 ** (largo - j) - 1
            assert modulo * x[j] == a * n + b
            assert (a * n + b) % modulo == 0
            assert inversos[j] <= 1
            cola = xi / inversos[j] - x[j]
            assert cola == 1 + Fraction(2, 3) ** (largo - j)
            assert 1 < cola <= 2
            assert b + modulo <= a * theta
            if j < largo:
                assert x[j] % 2 == 1
            pasos += 1
        assert (-b * pow(a, -1, modulo)) % modulo == n
        cantidad += 1
        if largo in (2, 3, 4, 99, 100, 101, 199, 200, 201, lmax):
            muestras.append(dict(L=largo, n=str(n), m=m, theta=str(theta),
                                 cola_inicial=str(theta), cola_final='2'))
    return dict(longitudes=cantidad, pasos_comprobados=pasos, muestras=muestras,
                alcance='Semillas variables; parámetro real compatible sólo con cada prefijo finito.')


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--nmax', type=int, default=128)
    analizador.add_argument('--pasos', type=int, default=64)
    analizador.add_argument('--mmax', type=int, default=128)
    analizador.add_argument('--lmax', type=int, default=256)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    assert args.nmax >= 1 and args.pasos >= 1 and args.mmax >= 0 and args.lmax >= 2
    resultado = dict(parametros=dict(nmax=args.nmax, pasos=args.pasos, mmax=args.mmax, lmax=args.lmax),
                     reinicios=reinicios(args.nmax, args.pasos), anillos=anillos(args.mmax),
                     compatibilidad=compatibilidad(args.lmax))
    resultado['sha256_fuente_lf'] = hashlib.sha256(
        Path(__file__).read_text(encoding='utf-8').encode('utf-8')).hexdigest()
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"OK: {resultado['reinicios']['minimos_finitos']} mínimos finitos, "
          f"{resultado['reinicios']['identidades_traslado']} traslados, "
          f"{resultado['anillos']['cortes']} cortes geométricos y "
          f"{resultado['compatibilidad']['longitudes']} prefijos compatibles.")


if __name__ == '__main__':
    main()
