"""Clase sin 00: menor n >= 3 cuyas L primeras paridades del atajo evitan 00.

Mapa: atajo T(x) = x/2 si x es par y (3x+1)/2 si es impar. Para n impar, evitar 00
equivale a que todos los exponentes de Syracuse v2(3x+1) sean 1 o 2, es decir, a no
pasar por un impar congruente con 5 módulo 8. 1 y 2 siguen (10)^w y se excluyen.
Búsqueda en profundidad de las clases módulo 2^L con representante menor que 2^B;
L <= lmax_bruto se repite por fuerza bruta. Medición exacta y finita, no prueba.
"""

import argparse
import hashlib
import json
import math
from pathlib import Path
import time


def paso(x):
    return (3 * x + 1) // 2 if x % 2 else x // 2


def medir(bits_cota, lmax):
    cota = 1 << bits_cota
    minimos = {}
    nodos = 0
    pila = [(0, 0, 0, 0, 1)]   # largo, r, y = T^largo(r), impares, último bit
    potencias3 = [1]
    while pila:
        largo, r, y, impares, ultimo = pila.pop()
        nodos += 1
        if largo > 0 and r >= 3:
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
            if largo > 0 and ultimo == 0 and bit == 0:
                continue
            siguiente = (3 * yy + 1) >> 1 if bit else yy >> 1
            pila.append((largo + 1, rr, siguiente, impares + bit, bit))
    return minimos, nodos


def evita_00(n, largo):
    x, anterior = n, 1
    for _ in range(largo):
        bit = x % 2
        if anterior == 0 and bit == 0:
            return False
        anterior, x = bit, paso(x)
    return True


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--bits', type=int, required=True)
    analizador.add_argument('--lmax', type=int, default=400)
    analizador.add_argument('--lmax-bruto', type=int, default=30)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    assert 1 <= args.bits <= 60 and args.lmax >= 1
    inicio = time.time()
    minimos, nodos = medir(args.bits, args.lmax)
    largos = sorted(minimos)
    filas, peor = [], (0.0, None, None)
    for largo in largos:
        valor = minimos[largo]
        filas.append(dict(largo=largo, minimo=str(valor), bits=valor.bit_length()))
        cociente = (largo - 1) / math.log2(valor)
        if cociente > peor[0]:
            peor = (cociente, largo, valor)
    for previo, actual in zip(filas, filas[1:]):
        assert int(previo['minimo']) <= int(actual['minimo'])
    comprobados = 0
    for fila in filas:
        if fila['largo'] > args.lmax_bruto:
            break
        n = 3
        while not evita_00(n, fila['largo']):
            n += 1
        assert n == int(fila['minimo']), fila
        comprobados += 1
    resultado = dict(
        parametros=dict(bits=args.bits, lmax=args.lmax, lmax_bruto=args.lmax_bruto),
        nodos_visitados=nodos, largo_maximo_bajo_la_cota=largos[-1],
        comprobados_por_fuerza_bruta=comprobados,
        peor_cociente=dict(valor=round(peor[0], 4), largo=peor[1], semilla=str(peor[2])),
        filas=filas, segundos=round(time.time() - inicio, 1),
        alcance=f'Exacto para todo 3 <= n < 2^{args.bits}: ninguno evita 00 durante '
                f'{largos[-1] + 1} pasos. Medición finita, no prueba universal.')
    resultado['sha256_fuente_lf'] = hashlib.sha256(
        Path(__file__).read_text(encoding='utf-8').encode('utf-8')).hexdigest()
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n',
                           encoding='utf-8')
    print(f"OK: {nodos} nodos; largo máximo {largos[-1]} bajo 2^{args.bits}; "
          f"peor cociente {resultado['peor_cociente']}; {resultado['segundos']} s.")


if __name__ == '__main__':
    main()
