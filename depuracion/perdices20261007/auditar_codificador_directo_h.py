"""Coteja el codificador BitVec con aritmética entera y certificados conocidos."""

import argparse
from itertools import product
import json
from pathlib import Path

import z3

from buscar_matrices_directas_h import codificar
from buscar_matrices_h import huella
from verificar_matrices_h import comprobar, interpretar


def sustituciones(codigo, simbolos):
    pares = []
    for letra, (matriz, vector) in codigo['simbolos'].items():
        dato = simbolos[letra]
        expresiones = sum(matriz, []) + vector
        valores = sum(dato['matriz'], []) + dato['vector']
        pares.extend((e, z3.BitVecVal(v, codigo['ancho'])) for e, v in zip(expresiones, valores))
    return pares


def cotejar_prefijos(codigo, simbolos, tipo):
    pares = sustituciones(codigo, simbolos)
    exactos = {letra: (s['matriz'], s['vector']) for letra, s in simbolos.items()}
    cantidad = 0
    maximo = 0
    for palabra, (matriz, vector) in codigo['prefijos'].items():
        m, v = interpretar(palabra, exactos, tipo)
        esperado = sum(m, []) + v
        calculado = [z3.simplify(z3.substitute(x, *pares)).as_long()
                     for x in sum(matriz, []) + vector]
        assert calculado == esperado, (tipo, palabra, esperado, calculado)
        assert max(esperado) <= codigo['maximo'] < 2 ** codigo['ancho']
        cantidad += 1
        maximo = max(maximo, max(esperado))
    return cantidad, maximo


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--controles', nargs='+', type=Path, required=True)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    relecturas = 0
    prefijos = 0
    decisiones = 0
    maximos = {}
    for ruta in args.controles:
        datos = json.loads(ruta.read_text(encoding='utf-8'))
        assert datos['terminacion_relativa_certificada']
        for etapa in datos['etapas']:
            certificado = etapa['certificado']
            comprobar(certificado)
            codigo = codificar(certificado['reglas'], certificado['interpretacion'],
                                certificado['dimension'], datos['parametros']['cota'])
            pares = sustituciones(codigo, certificado['simbolos'])
            assert all(z3.is_true(z3.simplify(z3.substitute(c, *pares)))
                       for c in codigo['condiciones'])
            cantidad, _ = cotejar_prefijos(codigo, certificado['simbolos'], certificado['interpretacion'])
            prefijos += cantidad
            relecturas += 1
    reglas = [dict(izquierda='ab', derecha='ba', estricta=True, en_cabeza=True),
              dict(izquierda='bbbb', derecha='a', estricta=False, en_cabeza=False)]
    for tipo in ['natural', 'arctic']:
        codigo = codificar(reglas, tipo, 1, 2)
        maximos[tipo] = 0
        for valores in product(range(3), repeat=4):
            simbolos = {'a': dict(matriz=[[valores[0]]], vector=[valores[1]]),
                        'b': dict(matriz=[[valores[2]]], vector=[valores[3]])}
            cantidad, mayor = cotejar_prefijos(codigo, simbolos, tipo)
            prefijos += cantidad
            maximos[tipo] = max(maximos[tipo], mayor)
            pares = sustituciones(codigo, simbolos)
            admisible = all(z3.is_true(z3.simplify(z3.substitute(c, *pares)))
                            for c in codigo['condiciones'])
            exactos = {letra: (s['matriz'], s['vector']) for letra, s in simbolos.items()}
            lm, lv = interpretar('ab', exactos, tipo)
            rm, rv = interpretar('ba', exactos, tipo)
            estricta = lv[0] > rv[0] if tipo == 'natural' else all(
                a > b or a == b == 0 for a, b in zip(sum(lm, []) + lv, sum(rm, []) + rv))
            certificado = dict(interpretacion=tipo, dimension=1, simbolos=simbolos,
                               reglas=reglas, eliminadas=[0] if estricta else [])
            try:
                comprobar(certificado)
                esperado = True
            except AssertionError:
                esperado = False
            assert admisible == esperado, (tipo, valores)
            decisiones += 1
    assert relecturas >= 6 and maximos['natural'] > 2 and maximos['arctic'] > 2
    rutas = [Path(__file__), Path(__file__).with_name('buscar_matrices_directas_h.py'),
             Path(__file__).with_name('buscar_matrices_h.py'),
             Path(__file__).with_name('verificar_matrices_h.py')]
    resultado = dict(version_z3=z3.get_version_string(),
                     fuentes={ruta.name: huella(ruta) for ruta in rutas},
                     controles={ruta.name: huella(ruta) for ruta in args.controles},
                     certificados_releidos=relecturas, prefijos_cotejados=prefijos,
                     decisiones_exhaustivas_dimension_1=decisiones,
                     maxima_entrada_compuesta_con_coeficientes_hasta_2=maximos,
                     alcance='Cotejo finito del codificador; la ausencia universal de '
                     'desbordamiento usa las cotas escritas de MATRICES_H.md, sin Lean.')
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'OK: {relecturas} certificados releídos, {prefijos} prefijos exactos, '
          f'{decisiones} decisiones exhaustivas.')


if __name__ == '__main__':
    main()
