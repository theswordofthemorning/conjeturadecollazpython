"""Bloques expansivos: presupuesto de una semilla y modelos simbólicos finitos."""

import argparse
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path


def paso(x):
    return (3 * x + 1) // 2 if x % 2 else x // 2


def datos(palabra):
    posiciones = [i for i, bit in enumerate(palabra) if bit == '1']
    d, s = len(palabra), len(posiciones)
    # Suma cerrada; independiente de la composición iterativa de Semilla.
    e = sum(2 ** i * 3 ** (s - j - 1) for j, i in enumerate(posiciones))
    return 3 ** s, e, 2 ** d


def valuacion(dato):
    assert dato > 0
    return (dato & -dato).bit_length() - 1


def coincidencia_orbital(n, palabra):
    x = n
    for j in range(4096):
        if x % 2 != int(palabra[j % len(palabra)]):
            return j
        x = paso(x)
    raise AssertionError('Corte de seguridad alcanzado; no se acepta como terminación.')


def copias_orbitales(n, palabra):
    return coincidencia_orbital(n, palabra) // len(palabra)


def presupuestos(dmax, nmax, rmax):
    palabras, semillas, representantes, longitudes = 0, 0, 0, 0
    for d in range(1, dmax + 1):
        for bits in product('01', repeat=d):
            palabra = ''.join(bits)
            a, e, modulo = datos(palabra)
            if a <= modulo:
                continue
            c = a - modulo
            palabras += 1
            for n in range(nmax + 1):
                r = copias_orbitales(n, palabra)
                assert coincidencia_orbital(n, palabra) == valuacion(c * n + e)
                assert r == valuacion(c * n + e) // d
                assert 2 ** (d * r) <= c * n + e
                semillas += 1
            for r in range(rmax + 1):
                aa, ee, mm = datos(palabra * r)
                assert (aa, mm) == (a ** r, modulo ** r)
                assert c * ee + e * mm == e * aa
                residuo = (-ee * pow(aa, -1, mm)) % mm
                assert residuo == (-e * pow(c, -1, mm)) % mm
                for desplazamiento in (0, 1):
                    n = residuo + desplazamiento * mm
                    cantidad = copias_orbitales(n, palabra)
                    assert coincidencia_orbital(n, palabra) == valuacion(c * n + e)
                    assert cantidad >= r
                    assert cantidad == valuacion(c * n + e) // d
                    x = n
                    for _ in range(d * r):
                        x = paso(x)
                    assert mm * (c * x + e) == aa * (c * n + e)
                    representantes += 1
                longitudes += 1
    # El potencial cero de un ciclo contractivo impide extender el presupuesto.
    assert datos('10') == (3, 1, 4)
    assert (3 - 4) * 1 + 1 == 0 and paso(paso(1)) == 1
    return dict(palabras_expansivas=palabras, semillas_pequenas=semillas,
                representantes=representantes, longitudes=longitudes,
                alcance='Palabras no vacías expansivas; incluye cero copias y semilla cero. '
                        'El caso contractivo 10, n=1 tiene potencial cero y no admite esta cota.')


def relojes(nmax, pasos, dmax):
    casos = 0
    for n in range(nmax + 1):
        x = n
        for u in range(pasos + 1):
            assert 2 ** u * (x + 1) <= 3 ** u * (n + 1)
            palabra, y = '', x
            for d in range(1, dmax + 1):
                palabra += str(y % 2)
                y = paso(y)
                a, e, modulo = datos(palabra)
                if a <= modulo:
                    continue
                c = a - modulo
                r = copias_orbitales(x, palabra)
                assert r == valuacion(c * x + e) // d
                assert 2 ** (u + d * r) <= max(c, e) * 3 ** u * (n + 1)
                if u <= d * r:
                    assert 4 ** u <= max(c, e) * 3 ** u * (n + 1)
                casos += 1
            x = paso(x)
    return dict(presupuestos_desde_una_semilla=casos, corte=pasos)


def mezcla(qmax):
    palabras, colas, cortes, transiciones = 0, 0, 0, 0
    for q in range(qmax + 1):
        for eleccion in product(('1', '110'), repeat=q):
            palabra = ''.join(eleccion)
            a, e, modulo = datos(palabra)
            n = (-e * pow(a, -1, modulo)) % modulo + 8 * modulo
            valores, potencias = [n], [Fraction(1)]
            for bit in palabra:
                x = valores[-1]
                assert x % 2 == int(bit)
                valores.append(paso(x))
                potencias.append(potencias[-1] * Fraction(3 if bit == '1' else 1, 2))
            limites, u = [0], 0
            for bloque in eleccion:
                u += len(bloque)
                limites.append(u)
            for u in limites:
                assert all(p >= potencias[u] for p in potencias[u:])
            indices = [i for i, bloque in enumerate(eleccion) if bloque == '110']
            for i, j in zip(indices, indices[1:]):
                x, y = valores[limites[i]], valores[limites[j]]
                z, resto = divmod(x + 1, 4)
                zz, resto_siguiente = divmod(y + 1, 4)
                assert resto == resto_siguiente == 0 and z % 2 == zz % 2 == 1
                a = j - i - 1
                assert 2 ** (a + 3) * zz == 3 ** a * (9 * z + 1)
                assert valuacion(9 * z + 1) == a + 3 and z % 8 == 7
                transiciones += 1
            for terminal in (Fraction(1), Fraction(5)):
                theta = terminal
                for bloque in reversed(eleccion):
                    theta = (1 + 2 * theta) / 3 if bloque == '1' else (5 + 8 * theta) / 9
                    assert 1 <= theta <= 5
                xi = n + theta  # Parámetro finito; NO es estatura(n).
                assert theta ** 100 <= n ** 99
                for j, (x, p) in enumerate(zip(valores, potencias)):
                    t = xi * p - x
                    assert 1 <= t <= 10
                    if j in limites:
                        assert t <= 5
                    cortes += 1
                assert xi * potencias[-1] - valores[-1] == terminal
                colas += 1
            palabras += 1
    return dict(palabras=palabras, intervalos_extremos=colas, cortes=cortes,
                transiciones_entre_110=transiciones,
                alcance='Cada palabra conserva una semilla durante todos sus cortes; '
                        'la semilla varía entre palabras. No certifica integridad infinita.')


def familia_cientodiez(rmax):
    ejemplos = []
    for r in range(1, rmax + 1):
        n = 8 ** r - 5
        assert copias_orbitales(n, '110') == r
        x = n
        for j in range(r + 1):
            assert x == 9 ** j * 8 ** (r - j) - 5
            if j < r:
                for bit in '110':
                    assert x % 2 == int(bit)
                    x = paso(x)
        assert x % 2 == 0  # La siguiente copia exige impar: falla inmediatamente.
        assert 8 ** (r + 1) - 5 == n + 8 ** r * 7
        if r in (1, 2, rmax):
            ejemplos.append(dict(copias=r, semilla=str(n), salida=str(x), siguiente_levantamiento=7))
    return ejemplos


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--dmax', type=int, default=7)
    analizador.add_argument('--nmax', type=int, default=96)
    analizador.add_argument('--rmax', type=int, default=12)
    analizador.add_argument('--qmax', type=int, default=8)
    analizador.add_argument('--pasos', type=int, default=64)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    assert 1 <= args.dmax <= 10 and args.nmax >= 0
    assert 0 <= args.rmax <= 128 and 0 <= args.qmax <= 12 and args.pasos >= 0
    resultado = dict(parametros={k: v for k, v in vars(args).items() if k != 'salida'},
                     presupuestos=presupuestos(args.dmax, args.nmax, args.rmax),
                     relojes=relojes(args.nmax, args.pasos, args.dmax),
                     mezcla=mezcla(args.qmax), familia_110=familia_cientodiez(args.rmax))
    resultado['sha256_fuente_lf'] = hashlib.sha256(
        Path(__file__).read_text(encoding='utf-8').encode('utf-8')).hexdigest()
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"OK: {resultado['presupuestos']['palabras_expansivas']} palabras expansivas, "
          f"{resultado['presupuestos']['semillas_pequenas']} semillas, "
          f"{resultado['relojes']['presupuestos_desde_una_semilla']} presupuestos orbitales y "
          f"{resultado['mezcla']['palabras']} mezclas finitas.")


if __name__ == '__main__':
    main()
