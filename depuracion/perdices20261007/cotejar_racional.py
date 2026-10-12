"""Racionales p/q, q impar: cotejo exacto de las dos ramas de PerdicesRacional.

Mapa 3x+q sobre enteros: x/2 si x es par y (3x+q)/2 si es impar. Con x_t = p_t/q,
es el atajo de Collatz sobre p/q. Todo es aritmética entera; no hay ley aleatoria.
"""

import argparse
import hashlib
import json
from pathlib import Path

from cotejar_complejidad import palabra_mecanica


def paso(x, q):
    return (3 * x + q) // 2 if x % 2 else x // 2


def orbita(p, q, pasos):
    xs = [p]
    for _ in range(pasos):
        xs.append(paso(xs[-1], q))
    return xs


def factores(xs, m, posiciones):
    return [tuple(x % 2 for x in xs[t:t + m]) for t in posiciones]


def umbral_inyectivo(qmax, pmax, mmax):
    """Rama inyectiva, forma finita: valores distintos bajo el umbral, factores distintos."""
    revisados = ciclados = 0
    for q in range(1, qmax + 1, 2):
        for p in range(-pmax, pmax + 1):
            a = abs(p) + q
            for m in range(1, mmax + 1):
                k = -1
                while 3 ** (k + 1) * a <= 2 ** (m + k + 1):
                    k += 1
                if k < 0:
                    continue
                xs = orbita(p, q, k + m + 1)
                for t in range(k + 1):
                    assert abs(xs[t]) + q <= 2 ** m, (p, q, m, t)
                if len(set(xs[:k + 1])) < k + 1:
                    ciclados += 1
                    continue
                f = factores(xs, m + 1, range(k + 1))
                assert len(set(f)) == k + 1, (p, q, m)
                revisados += 1
    return dict(casos_con_valores_distintos=revisados, casos_que_ya_repiten=ciclados)


def rama_periodica(qmax, pmax):
    """Rama repetida: desde la primera repetición la palabra es periódica y la
    complejidad de largo i+d no pasa de i+d."""
    casos = 0
    ejemplos = []
    for q in range(1, qmax + 1, 2):
        for p in range(-pmax, pmax + 1):
            vistos = {}
            x, t = p, 0
            while x not in vistos:
                vistos[x] = t
                x, t = paso(x, q), t + 1
                assert t < 100000, ('corte de seguridad: no se trata como ciclo', p, q)
            i, d = vistos[x], t - vistos[x]
            largo = i + d
            xs = orbita(p, q, 3 * largo + 4 * d + largo)
            for s in range(i, len(xs) - d):
                assert xs[s + d] == xs[s]
            todos = set(factores(xs, largo, range(len(xs) - largo + 1)))
            assert len(todos) <= largo, (p, q, i, d)
            casos += 1
            if p in (1, -1, -5, -17) and q == 1 or (q, p) in ((5, 1), (7, 1), (9, 3)):
                ejemplos.append(dict(p=p, q=q, entrada=i, periodo=d, factores=len(todos)))
    return dict(semillas=casos, ejemplos=ejemplos)


def umbral_teorema(qmax, pmax):
    """El umbral m = 9(|p|+q) del teorema: 3^(m+2)(|p|+q) <= 2^(m+(m+2))."""
    for q in range(1, qmax + 1, 2):
        for p in range(-pmax, pmax + 1):
            a = abs(p) + q
            m = 9 * a
            assert 3 ** (m + 2) * a <= 2 ** (2 * m + 2)
            assert 3 ** (m + 1) * (3 + m + 1) <= 3 * 4 ** (m + 1)
    return True


def puente_racional(qmax, pmax, pasos):
    """Atajo sobre Q con Fraction reducida: paridad del numerador y TQ^t(a/q)=(Tq^t a)/q."""
    from fractions import Fraction
    comprobados = 0
    for q in range(1, qmax + 1, 2):
        for a in range(-pmax, pmax + 1):
            x = Fraction(a, q)
            y = a
            for _ in range(pasos):
                assert x == Fraction(y, q) and x.denominator % 2 == 1
                assert x.numerator % 2 == y % 2
                x = x / 2 if x.numerator % 2 == 0 else (3 * x + 1) / 2
                y = paso(y, q)
                comprobados += 1
    return comprobados


def representantes_racionales(bits, q):
    """Representante simétrico de cada prefijo bajo 3x+q, por la biyección."""
    r, y, impares = 0, 0, 0
    salida = [0]
    for k, bit in enumerate(bits):
        if y % 2 != bit:
            r += 2 ** k
            y += 3 ** impares
        y = (3 * y + q) // 2 if bit else y // 2
        impares += bit
        largo = k + 1
        simetrico = r - 2 ** largo if r >= 2 ** (largo - 1) else r
        salida.append(simetrico)
    return salida


def sturmianas_racionales(largo, qmax):
    pendientes = {
        'sqrt2-1/2': (-1, 2, 2, 2),
        '(sqrt5-4/5)/2': (-4, 5, 5, 10),
        'sqrt3-1': (-1, 1, 3, 1),
        '(sqrt5+1)/4': (1, 1, 5, 4),
        '(sqrt5-1)/2': (-1, 1, 5, 2),
    }
    interceptos = {'0': (0, 1), '1/3': (1, 3)}
    filas = []
    for nombre, pendiente in pendientes.items():
        for nombre_i, intercepto in interceptos.items():
            bits = palabra_mecanica(pendiente, intercepto, largo)
            for q in range(1, qmax + 1, 2):
                reps = representantes_racionales(bits, q)
                for l in (64, 128, 256, largo):
                    p = reps[l]
                    xs = orbita(p, q, l)
                    assert [x % 2 for x in xs[:l]] == bits[:l]
                    # Con m = 9(|p|+q): seguir 2m+3 pasos de una palabra sturmiana obliga
                    # a repetir un valor entre los m+3 primeros (rama periódica).
                    m = 9 * (abs(p) + q)
                    if l >= 2 * m + 3:
                        assert len(set(xs[:m + 3])) < m + 3, (nombre, q, l)
                filas.append(dict(pendiente=nombre, intercepto=nombre_i, q=q,
                                  bits_representante=[abs(reps[l]).bit_length()
                                                      for l in (64, 128, 256, largo)]))
    return filas


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--qmax', type=int, default=15)
    analizador.add_argument('--pmax', type=int, default=64)
    analizador.add_argument('--mmax', type=int, default=24)
    analizador.add_argument('--largo', type=int, default=400)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    assert args.qmax >= 1 and args.pmax >= 0 and args.mmax >= 1 and args.largo >= 256
    resultado = dict(
        parametros={k: v for k, v in vars(args).items() if k != 'salida'},
        rama_inyectiva=umbral_inyectivo(args.qmax, args.pmax, args.mmax),
        rama_periodica=rama_periodica(args.qmax, args.pmax),
        umbral_del_teorema=umbral_teorema(args.qmax, args.pmax),
        pasos_del_puente_sobre_Q=puente_racional(args.qmax, args.pmax, 64),
        sturmianas=sturmianas_racionales(args.largo, min(args.qmax, 9)),
        alcance='Comprobación finita de las dos ramas y del umbral; no sustituye la prueba Lean.')
    resultado['sha256_fuente_lf'] = hashlib.sha256(
        Path(__file__).read_text(encoding='utf-8').encode('utf-8')).hexdigest()
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n',
                           encoding='utf-8')
    print(f"OK: {resultado['rama_inyectiva']['casos_con_valores_distintos']} casos inyectivos, "
          f"{resultado['rama_periodica']['semillas']} órbitas periódicas, "
          f"{len(resultado['sturmianas'])} prefijos sturmianos racionales.")


if __name__ == '__main__':
    main()
