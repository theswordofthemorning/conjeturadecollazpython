"""Clase {1,110}^w: menor natural que sigue L pasos, por búsqueda en profundidad.

Mapa: atajo T(x) = x/2 si x es par y (3x+1)/2 si es impar. Un prefijo de
{1,110}^w empieza por 11 y evita 00 y 010. Por la biyección entre paridades y
residuos, cada prefijo de largo L es una clase módulo 2^L; su representante
mínimo no decrece al alargar el prefijo. Se recorren en profundidad todas las
clases con representante menor que 2^B y se guarda, por largo, el menor.
Implementación independiente de la búsqueda por niveles de cotejar_complejidad.py.
Es medición exacta y finita: no prueba nada para n >= 2^B.
"""

import argparse
import hashlib
import json
from pathlib import Path
import time


def permitido(penultimo, ultimo, bit, largo):
    if largo < 2:
        return bit == 1
    if ultimo == 0 and bit == 0:
        return False
    if penultimo == 0 and ultimo == 1 and bit == 0:
        return False
    return True


def medir(bits_cota, lmax):
    cota = 1 << bits_cota
    minimos = {}
    nodos = 0
    # Pila de (largo, r, y, impares, penúltimo, último); y = T^largo(r).
    pila = [(0, 0, 0, 0, 1, 1)]
    potencias3 = [1]
    while pila:
        largo, r, y, impares, a, b = pila.pop()
        nodos += 1
        if largo > 0:
            previo = minimos.get(largo)
            if previo is None or r < previo:
                minimos[largo] = r
        if largo == lmax:
            continue
        while len(potencias3) <= impares:
            potencias3.append(potencias3[-1] * 3)
        for ajuste in (1, 0):
            if ajuste:
                rr = r + (1 << largo)
                if rr >= cota:
                    continue
                yy = y + potencias3[impares]
            else:
                rr, yy = r, y
            bit = yy & 1
            if not permitido(a, b, bit, largo):
                continue
            siguiente = (3 * yy + 1) >> 1 if bit else yy >> 1
            pila.append((largo + 1, rr, siguiente, impares + bit, b, bit))
    return minimos, nodos


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--bits', type=int, required=True)
    analizador.add_argument('--lmax', type=int, default=200)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    assert 1 <= args.bits <= 60 and args.lmax >= 1
    inicio = time.time()
    minimos, nodos = medir(args.bits, args.lmax)
    largos = sorted(minimos)
    filas = []
    for largo in largos:
        valor = minimos[largo]
        assert valor ** 3 >= 2 ** (largo - 1) or valor == 0, (largo, valor)
        filas.append(dict(largo=largo, minimo=str(valor), bits=valor.bit_length()))
    # Coherencia: el mínimo no decrece con el largo.
    for previo, actual in zip(filas, filas[1:]):
        assert int(previo['minimo']) <= int(actual['minimo'])
    resultado = dict(parametros=dict(bits=args.bits, lmax=args.lmax),
                     nodos_visitados=nodos, largo_maximo_bajo_la_cota=largos[-1],
                     filas=filas, cota_tres_log2=True,
                     segundos=round(time.time() - inicio, 1),
                     alcance=f'Exacto para todo n < 2^{args.bits}: ninguno sigue la clase '
                             f'{largos[-1] + 1} pasos. Medición finita, no prueba universal.')
    resultado['sha256_fuente_lf'] = hashlib.sha256(
        Path(__file__).read_text(encoding='utf-8').encode('utf-8')).hexdigest()
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n',
                           encoding='utf-8')
    print(f"OK: {nodos} nodos; largo máximo {largos[-1]} bajo 2^{args.bits}; "
          f"{resultado['segundos']} s.")


if __name__ == '__main__':
    main()
