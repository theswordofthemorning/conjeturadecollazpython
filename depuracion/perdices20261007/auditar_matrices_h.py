"""Audita ejecuciones SAT guardadas y controles negativos del verificador entero."""

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path

from verificar_matrices_h import comprobar_ejecucion


def huella(ruta):
    return hashlib.sha256(ruta.read_text(encoding='utf-8').encode('utf-8')).hexdigest()


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
        cantidad = comprobar_ejecucion(datos)
        if datos['parametros']['sistema'] == 'control15':
            assert datos['terminacion_relativa_certificada'] and cantidad == 3
            controles[datos['parametros']['interpretacion']] = datos
        resumen.append(dict(archivo=ruta.name, sha256_lf=huella(ruta), certificados=cantidad,
                            estados=[e['estado'] for e in datos['etapas']],
                            cierre=datos['terminacion_relativa_certificada']))
    assert set(controles) == {'natural', 'arctic'}
    corruptos = []
    for tipo, datos in controles.items():
        nulo = deepcopy(datos)
        for simbolo in nulo['etapas'][0]['certificado']['simbolos'].values():
            d = len(simbolo['vector'])
            simbolo['matriz'] = [[0] * d for _ in range(d)]
            simbolo['vector'] = [0] * d
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
    rechazados = []
    for nombre, datos in corruptos:
        try:
            comprobar_ejecucion(datos)
        except AssertionError:
            rechazados.append(nombre)
        else:
            raise AssertionError('Se aceptó un certificado alterado: ' + nombre)
    resultado = dict(ejecuciones=resumen, controles_negativos_rechazados=rechazados,
                     sha256_auditor_lf=huella(Path(__file__)),
                     alcance='Certificados SAT verificados por aritmética independiente y '
                     'cadena de reglas anclada en el sistema de entrada. No certifica UNSAT '
                     'ni interpreta un timeout como ausencia de órdenes.')
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    certificados = sum(f['certificados'] for f in resumen)
    print(f'OK: {len(resumen)} ejecuciones, {certificados} certificados y {len(rechazados)} controles negativos.')


if __name__ == '__main__':
    main()
