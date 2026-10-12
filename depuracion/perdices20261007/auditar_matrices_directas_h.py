"""Audita ejecuciones BitVec usando sólo enteros Python y los certificados guardados."""

import argparse
from copy import deepcopy
import json
from pathlib import Path

from buscar_matrices_h import huella
from verificar_matrices_h import comprobar_ejecucion, interpretar


def comprobar_datos(datos):
    cantidad = comprobar_ejecucion(datos)
    parametros = datos['parametros']
    tipo, dimension, cota = [parametros[c] for c in ['interpretacion', 'dimension', 'cota']]
    maximos = []
    for etapa in datos['etapas']:
        if 'certificado' not in etapa:
            continue
        certificado = etapa['certificado']
        assert certificado['interpretacion'] == tipo and certificado['dimension'] == dimension
        simbolos = certificado['simbolos']
        assert all(0 <= valor <= cota for s in simbolos.values()
                   for valor in sum(s['matriz'], []) + s['vector'])
        largo = max(len(r[lado]) for r in certificado['reglas']
                     for lado in ['izquierda', 'derecha'])
        maximo = ((dimension + 1) * cota) ** largo if tipo == 'natural' else largo * (cota - 1) + 1
        assert (etapa['largo_maximo'], etapa['cota_intermedia'], etapa['ancho_bits']) == (
            largo, maximo, maximo.bit_length())
        exactos = {letra: (s['matriz'], s['vector']) for letra, s in simbolos.items()}
        mayor = 0
        for regla in certificado['reglas']:
            for lado in ['izquierda', 'derecha']:
                palabra = regla[lado]
                for longitud in range(1, len(palabra) + 1):
                    matriz, vector = interpretar(palabra[:longitud], exactos, tipo)
                    mayor = max(mayor, max(sum(matriz, []) + vector))
        assert mayor <= maximo
        maximos.append(mayor)
    return cantidad, maximos


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--entradas', nargs='+', type=Path, required=True)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    resumen, controles = [], {}
    for ruta in args.entradas:
        datos = json.loads(ruta.read_text(encoding='utf-8'))
        for nombre, esperada in datos['fuentes_locales'].items():
            assert huella(Path(__file__).with_name(nombre)) == esperada, nombre
        cantidad, maximos = comprobar_datos(datos)
        if datos['parametros']['sistema'] == 'control15':
            assert datos['terminacion_relativa_certificada'] and 1 <= cantidad <= 3
            controles[datos['parametros']['interpretacion']] = datos
        resumen.append(dict(archivo=ruta.name, sha256_lf=huella(ruta), certificados=cantidad,
                            estados=[e['estado'] for e in datos['etapas']],
                            maximos_intermedios_certificados=maximos,
                            cierre=datos['terminacion_relativa_certificada']))
    assert set(controles) == {'natural', 'arctic'}
    corruptos = []
    for tipo, datos in controles.items():
        assert len(datos['etapas']) >= 2
        nulo = deepcopy(datos)
        for simbolo in nulo['etapas'][0]['certificado']['simbolos'].values():
            dimension = len(simbolo['vector'])
            simbolo['matriz'] = [[0] * dimension for _ in range(dimension)]
            simbolo['vector'] = [0] * dimension
        corruptos.append((tipo + '_nulo', nulo))
        prematuro = deepcopy(datos)
        prematuro['etapas'] = prematuro['etapas'][:1]
        corruptos.append((tipo + '_cierre_prematuro', prematuro))
        desordenado = deepcopy(datos)
        desordenado['etapas'][0], desordenado['etapas'][1] = desordenado['etapas'][1], desordenado['etapas'][0]
        corruptos.append((tipo + '_orden_alterado', desordenado))
        otra_regla = deepcopy(datos)
        otra_regla['reglas_originales'] = otra_regla['reglas_originales'].replace('ad ->| d', 'ad ->| ad')
        corruptos.append((tipo + '_regla_alterada', otra_regla))
        otra_cota = deepcopy(datos)
        otra_cota['parametros']['cota'] = 1
        corruptos.append((tipo + '_cota_alterada', otra_cota))
    rechazados = []
    for nombre, datos in corruptos:
        try:
            comprobar_datos(datos)
        except AssertionError:
            rechazados.append(nombre)
        else:
            raise AssertionError('Se aceptó una ejecución alterada: ' + nombre)
    resultado = dict(ejecuciones=resumen, controles_negativos_rechazados=rechazados,
                     fuentes={p.name: huella(p) for p in [Path(__file__),
                         Path(__file__).with_name('buscar_matrices_h.py'),
                         Path(__file__).with_name('verificar_matrices_h.py')]},
                     alcance='Verificación entera de certificados, cadena de eliminación '
                     'y cotas. No certifica UNSAT ni timeouts; no usa Z3.')
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'OK: {len(resumen)} ejecuciones, {sum(f["certificados"] for f in resumen)} '
          f'certificados y {len(rechazados)} controles negativos.')


if __name__ == '__main__':
    main()
