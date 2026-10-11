"""Contraste exacto del producto de novena raíz y de sus hipótesis finitas."""

import argparse
from fractions import Fraction
import hashlib
from itertools import combinations
import json
from math import comb
from pathlib import Path


def raiz_entera(n, grado):
    menor, mayor = 0, 1 << ((n.bit_length() + grado - 1) // grado)
    while menor + 1 < mayor:
        medio = (menor + mayor) // 2
        if medio ** grado <= n:
            menor = medio
        else:
            mayor = medio
    assert menor ** grado <= n < (menor + 1) ** grado
    return menor


def factor(x):
    return Fraction(3 * x + 1, 3 * x)


def polinomio(limite):
    # Expansión independiente por coeficientes binomiales.
    coeficientes = [0] * 11
    for a, b, c in ((2, 3, 12), (-2, -1, 13)):
        for j in range(10):
            coeficientes[j] += b * comb(9, j) * 9 ** j * c ** (9 - j)
            coeficientes[j + 1] += a * comb(9, j) * 9 ** j * c ** (9 - j)
    assert all(c >= 0 for c in coeficientes)
    for r in range(limite + 1):
        diferencia = (2 * r + 3) * (9 * r + 12) ** 9 - (2 * r + 1) * (9 * r + 13) ** 9
        assert diferencia == sum(c * r ** j for j, c in enumerate(coeficientes)) >= 0
    return coeficientes


def conjuntos(elementos):
    permitidos, x = [], 3
    while len(permitidos) < elementos:
        if x % 3:
            permitidos.append(x)
        x += 2
    cuentas = dict(conjuntos=0, excepciones=0)
    for q in range(elementos + 1):
        for conjunto in combinations(permitidos, q):
            producto = Fraction(1)
            for valor in conjunto:
                producto *= factor(valor)
            assert producto ** 9 <= 2 * q + 1
            if conjunto:
                assert 3 * q + 1 <= max(conjunto)
            cuentas['conjuntos'] += 1
            for excepcional in (3, 9):
                assert (producto * factor(excepcional)) ** 9 <= 3 * (2 * (q + 1) + 1)
                cuentas['excepciones'] += 1
    return dict(permitidos=permitidos, cuentas=cuentas)


def trayectorias(n_max, pasos):
    cuentas = dict(pasos_modulares=0, prefijos_validos=0, prefijos_con_excepcion=0,
                   cotas_novena_mejores=0)
    for n in range(1, n_max + 1):
        x, s, producto = n, 0, Fraction(1)
        vistos, validos, impares_de_tres, primer_impar = set(), True, 0, False
        for k in range(pasos + 1):
            if primer_impar:
                assert x % 3 != 0
            if validos:
                assert Fraction(2 ** k * x, 3 ** s) == n * producto
                assert (2 ** k * x) ** 9 <= 3 ** (9 * s) * 3 * n ** 9 * (2 * s + 1)
                cuentas['prefijos_validos'] += 1
                cuentas['prefijos_con_excepcion'] += impares_de_tres > 0
                cuentas['cotas_novena_mejores'] += 9 * (2 * s + 1) ** 2 < (s + 1) ** 3
            if k == pasos:
                break
            anterior = x
            if x % 2:
                validos = validos and x >= 3 and x not in vistos
                vistos.add(x)
                impares_de_tres += x % 3 == 0
                assert impares_de_tres <= 1
                producto *= factor(x)
                s += 1
                x = (3 * x + 1) // 2
                primer_impar = True
            else:
                x //= 2
            assert anterior % 3 == 0 or x % 3 != 0
            cuentas['pasos_modulares'] += 1
    return cuentas


def bordes():
    assert factor(1) ** 9 > 3 * (2 * 1 + 1)
    assert factor(5) ** (9 * 16) > 3 * (2 * 16 + 1)
    producto, q = Fraction(1), 0
    while q < 4096:
        q += 1
        producto *= factor(2 * q + 1)
        if producto ** 9 > 3 * (2 * q + 1):
            break
    else:
        raise AssertionError('No aparecio el control sin exclusion de multiplos de tres')
    assert 9 * (2 * 33 + 1) ** 2 > (33 + 1) ** 3
    assert 9 * (2 * 34 + 1) ** 2 < (34 + 1) ** 3
    return dict(entrada_uno='falla la cota en el primer paso de n=1',
                repetidos='16 copias de 5 violan la cota del producto',
                impares_sin_restriccion_tres=q, comparacion_s=34)


def radios():
    cuentas = dict(radios=0, novena_menor=0, iguales=0, sexta_menor=0)
    ejemplos = []
    for n in (3, 27, 97):
        for c in range(3):
            for k in (0, 1, 35, 36, 37, 100, 1000, 10 ** 6, 10 ** 12, 10 ** 24):
                cn = 3 ** c * n
                sexta = raiz_entera(cn ** 6 * k, 6)
                novena = raiz_entera(6 * cn ** 9 * k, 9)
                if k >= 36:
                    assert novena <= sexta
                if k <= 36:
                    assert sexta <= novena
                cuentas['radios'] += 1
                cuentas['novena_menor' if novena < sexta else 'sexta_menor' if sexta < novena else 'iguales'] += 1
                if n == 27 and c == 1 and k in (36, 1000, 10 ** 12, 10 ** 24):
                    ejemplos.append(dict(n=n, c=c, K=k, radio_sexta=sexta, radio_novena=novena))
    return dict(cuentas=cuentas, ejemplos=ejemplos,
                alcance='Evaluacion de cotas para una hipotetica fuga pura; no cuenta regresos de una fuga observada.')


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--elementos', type=int, required=True)
    analizador.add_argument('--factor-max', type=int, required=True)
    analizador.add_argument('--n-max', type=int, required=True)
    analizador.add_argument('--pasos', type=int, required=True)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    assert 0 <= args.elementos <= 16 and args.factor_max >= 0
    assert args.n_max >= 1 and args.pasos >= 1
    coeficientes = polinomio(args.factor_max)
    finitos = conjuntos(args.elementos)
    orbital = trayectorias(args.n_max, args.pasos)
    controles = bordes()
    comparaciones = radios()
    datos = Path(__file__).read_bytes()
    evidencia = dict(estado='cotejo exacto terminado', fuente=Path(__file__).name,
                     sha256_bytes=hashlib.sha256(datos).hexdigest(),
                     sha256_lf=hashlib.sha256(datos.replace(b'\r\n', b'\n')).hexdigest(),
                     parametros={k: v for k, v in vars(args).items() if k != 'salida'},
                     coeficientes=coeficientes, conjuntos=finitos, trayectorias=orbital,
                     bordes=controles, radios=comparaciones,
                     alcance='El producto general se prueba en Lean. El cotejo usa solo tramos finitos '
                             'con entradas impares distintas y >=3; no verifica FugaPura ni infinitos regresos. '
                             'Las cotas temporales y la exigencia octava son teoremas condicionales, no mediciones.')
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(json.dumps(evidencia, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(finitos['cuentas']))
    print(json.dumps(orbital))
    print(json.dumps(controles))
    print(json.dumps(comparaciones['cuentas']))


if __name__ == '__main__':
    main()
