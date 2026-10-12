"""Comprueba certificados matriciales con enteros Python, sin SAT ni NumPy.

Órdenes relativos en la cabeza de la palabra, tras la inversión del sistema.
Natural: matrices y vectores no negativos; descenso en la primera coordenada.
Ártico: 0 codifica menos infinito, n>=1 codifica n-1; suma=max, producto=suma.
Sólo se acepta el dominio ártico no negativo. No prueba UNSAT ni timeouts.
"""

import argparse
import json
from pathlib import Path


def componer(izquierda, derecha, tipo):
    m, v = izquierda
    n, w = derecha
    d = len(v)
    if tipo == 'natural':
        producto = lambda a, b: a * b
        suma = sum
        sumar = lambda a, b: a + b
    else:
        producto = lambda a, b: 0 if not a or not b else a + b - 1
        suma = max
        sumar = max
    matriz = [[suma([producto(m[i][k], n[k][j]) for k in range(d)])
               for j in range(d)] for i in range(d)]
    vector = [sumar(suma([producto(m[i][k], w[k]) for k in range(d)]), v[i])
              for i in range(d)]
    return matriz, vector


def interpretar(palabra, simbolos, tipo):
    assert palabra
    resultado = simbolos[palabra[0]]
    for letra in palabra[1:]:
        resultado = componer(resultado, simbolos[letra], tipo)
    return resultado


def comprobar(certificado):
    tipo = certificado['interpretacion']
    assert tipo in ('natural', 'arctic')
    d = certificado['dimension']
    assert d >= 1
    simbolos = {}
    alfabeto = {c for r in certificado['reglas'] for c in r['izquierda'] + r['derecha']}
    assert set(certificado['simbolos']) == alfabeto
    for c, dato in certificado['simbolos'].items():
        m, v = dato['matriz'], dato['vector']
        assert len(m) == len(v) == d and all(len(f) == d for f in m)
        assert all(type(x) is int and x >= 0 for x in sum(m, []) + v)
        if tipo == 'arctic':
            assert m[0][0] > 0 or v[0] > 0, (c, 'primera coordenada no finita')
        simbolos[c] = m, v
    eliminadas = []
    for indice, regla in enumerate(certificado['reglas']):
        assert not regla['estricta'] or regla['en_cabeza']
        lm, lv = interpretar(regla['izquierda'], simbolos, tipo)
        rm, rv = interpretar(regla['derecha'], simbolos, tipo)
        pares = list(zip(sum(lm, []) + lv, sum(rm, []) + rv))
        assert all(a >= b for a, b in pares), (indice, 'regla no orientada')
        estricta = lv[0] > rv[0] if tipo == 'natural' else all(
            a > b or a == b == 0 for a, b in pares)
        if estricta and regla['estricta']:
            eliminadas.append(indice)
    assert eliminadas and eliminadas == certificado['eliminadas']
    return eliminadas


def comprobar_ejecucion(datos):
    restantes = []
    for linea in datos['reglas_originales'].splitlines():
        if ' ->| ' in linea:
            izquierda, derecha = linea.split(' ->| ')
            estricta = True
        else:
            izquierda, derecha = linea.split(' ->= ')
            estricta = False
        restantes.append(dict(izquierda=izquierda[::-1], derecha=derecha[::-1],
                               estricta=estricta, en_cabeza=estricta))
    cantidad = 0
    for etapa in datos['etapas']:
        if 'certificado' not in etapa:
            continue
        certificado = etapa['certificado']
        assert certificado['reglas'] == restantes
        eliminadas = comprobar(certificado)
        restantes = [r for i, r in enumerate(certificado['reglas']) if i not in eliminadas]
        cantidad += 1
    if datos['terminacion_relativa_certificada']:
        assert cantidad and not any(r['estricta'] for r in restantes)
    return cantidad


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--entrada', type=Path, required=True)
    args = analizador.parse_args()
    datos = json.loads(args.entrada.read_text(encoding='utf-8'))
    cantidad = comprobar_ejecucion(datos)
    print(f'OK: {cantidad} certificados matriciales cotejados con enteros independientes.')


if __name__ == '__main__':
    main()
