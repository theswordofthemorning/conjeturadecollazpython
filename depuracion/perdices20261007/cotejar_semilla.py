"""Levantamientos y aportes exactos; ventanas finitas, sin presumir fuga infinita."""

import argparse
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path


def codigo(palabra):
    a, b, m = 1, 0, 1
    for bit in palabra:
        if bit == '1':
            a, b = 3 * a, 3 * b + m
        else:
            assert bit == '0'
        m *= 2
    residuo = (-b * pow(a, -1, m)) % m
    return a, b, m, residuo


def orbita(n, pasos):
    valores, potencias, palabra = [n], [Fraction(1)], ''
    for _ in range(pasos):
        x = valores[-1]
        impar = x % 2
        palabra += str(impar)
        valores.append((3 * x + 1) // 2 if impar else x // 2)
        potencias.append(potencias[-1] * Fraction(3 if impar else 1, 2))
    return valores, potencias, palabra


def enlace(prefijo, sufijo):
    a, b, m, r = codigo(prefijo)
    d, e, largo, _ = codigo(sufijo)
    aa, bb, mm, rr = codigo(prefijo + sufijo)
    q, resto = divmod(a * r + b, m)
    assert resto == 0 and (aa, bb, mm) == (d * a, d * b + m * e, m * largo)
    t = (-(d * q + e) * pow(d * a, -1, largo)) % largo
    assert rr == r + m * t and 0 <= t < largo
    assert ((d * q + e) % largo == 0) == (t == 0)
    aporte = Fraction(m * e, a * d)
    cambio = Fraction(m * (e + 5 * (largo - d)), a * d)
    for desplazamiento in (0, 1):
        semilla = rr + desplazamiento * mm
        xs, ps, palabra = orbita(semilla, len(prefijo) + len(sufijo))
        u = len(prefijo)
        assert palabra == prefijo + sufijo
        assert xs[u] == q + a * (t + desplazamiento * largo)
        assert Fraction(xs[-1], ps[-1]) - Fraction(xs[u], ps[u]) == aporte
        assert Fraction(xs[-1] + 5, ps[-1]) - Fraction(xs[u] + 5, ps[u]) == cambio
    assert (orbita(r, len(prefijo) + len(sufijo))[2] == prefijo + sufijo) == (t == 0)
    return dict(prefijo=prefijo, sufijo=sufijo, a=a, b=b, m=m, d=d, e=e,
                modulo_sufijo=largo, r=r, q=q, t=t, semilla=rr,
                aporte=str(aporte), cambio_cinco=str(cambio))


def parejas():
    # Mismo instante, P de entrada, techo y sufijo; distinto levantamiento.
    casos = [('11011101', '11011011', '1110100', 1, 1),
             ('1101110110', '1101110101', '110', 1, 0),
             ('1111011011', '1111010111', '111100', 2, -1)]
    resultados = []
    for buena, mala, sufijo, c, signo in casos:
        izquierda, derecha = enlace(buena, sufijo), enlace(mala, sufijo)
        assert izquierda['t'] == 0 < derecha['t']
        for clave in ('a', 'm', 'd', 'e', 'modulo_sufijo', 'aporte', 'cambio_cinco'):
            assert izquierda[clave] == derecha[clave]
        cambio = Fraction(izquierda['cambio_cinco'])
        assert (cambio > 0) - (cambio < 0) == signo
        for fila in (izquierda, derecha):
            xs, ps, _ = orbita(fila['semilla'], len(buena) + len(sufijo))
            u, v = len(buena), len(buena) + len(sufijo)
            assert all(p >= 1 for p in ps)
            assert ps[u] <= 3 ** c and ps[v] <= 3 ** c
            assert all(p > 3 ** c for p in ps[u + 1:v])
            fila.update(entrada=xs[u], salida=xs[v])
        resultados.append(dict(nivel=c, signo=signo, sin_levantamiento=izquierda,
                               con_levantamiento=derecha))
    return resultados


def excursiones(n_max, pasos, nivel_max):
    cuentas = dict(unitarias=0, no_unitarias=0, entrada_menor_modulo=0,
                   duracion_supera_quinta=0)
    maximo, testigo = Fraction(0), None
    for n in range(2, n_max + 1):
        xs, ps, palabra = orbita(n, pasos)
        fin = next((i for i, p in enumerate(ps) if p < 1), len(ps))
        for c in range(nivel_max + 1):
            visitas = [i for i in range(fin) if ps[i] <= 3 ** c]
            for u, v in zip(visitas, visitas[1:]):
                if v == u + 1:
                    cuentas['unitarias'] += 1
                    continue
                cuentas['no_unitarias'] += 1
                x, longitud = xs[u], v - u
                _, _, modulo, residuo = codigo(palabra[u:v])
                assert residuo == x % modulo
                if x < modulo:
                    assert residuo == x
                    cuentas['entrada_menor_modulo'] += 1
                cociente = Fraction(longitud, (x + 1) ** 5)
                cuentas['duracion_supera_quinta'] += cociente > 1
                if cociente > maximo:
                    maximo, testigo = cociente, dict(n=n, c=c, u=u, v=v, entrada=x)
    return dict(cuentas=cuentas, maximo_cociente=str(maximo), testigo=testigo)


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--largo-max', type=int, required=True)
    analizador.add_argument('--n-max', type=int, required=True)
    analizador.add_argument('--pasos', type=int, required=True)
    analizador.add_argument('--nivel-max', type=int, required=True)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    assert 0 <= args.largo_max <= 14 and args.n_max >= 2
    assert args.pasos >= 1 and args.nivel_max >= 0
    cuentas = dict(palabras=0, cortes=0, levantamientos_cero=0, levantamientos_positivos=0)
    for largo in range(args.largo_max + 1):
        for bits in product('01', repeat=largo):
            palabra = ''.join(bits)
            cuentas['palabras'] += 1
            for u in range(largo + 1):
                fila = enlace(palabra[:u], palabra[u:])
                cuentas['cortes'] += 1
                cuentas['levantamientos_cero' if fila['t'] == 0 else 'levantamientos_positivos'] += 1
    ejemplos = parejas()
    medicion = excursiones(args.n_max, args.pasos, args.nivel_max)
    fuente = Path(__file__).read_bytes()
    evidencia = dict(estado='cotejo exacto terminado',
                     fuente=Path(__file__).name,
                     sha256_bytes=hashlib.sha256(fuente).hexdigest(),
                     sha256_lf=hashlib.sha256(fuente.replace(b'\r\n', b'\n')).hexdigest(),
                     parametros={k: v for k, v in vars(args).items() if k != 'salida'},
                     cuentas=cuentas, parejas=ejemplos, excursiones=medicion,
                     alcance='Identidades y congruencias finitas, incluidos palabra vacia y residuo cero. '
                             'Los prefijos con P>=1 no certifican FugaPura; la cota quinta universal '
                             'es condicional y se prueba aparte en Lean. Ningun barrido prueba Collatz.')
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(json.dumps(evidencia, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(cuentas))
    print(json.dumps(medicion))
    print('OK: tres parejas con aporte identico y distinto levantamiento.')


if __name__ == '__main__':
    main()
