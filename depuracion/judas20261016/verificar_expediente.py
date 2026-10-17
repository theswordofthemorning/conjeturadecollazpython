"""Vigencia de la evidencia Lean citada en el expediente de revisión humana (J3b).

No compila nada. Recalcula la huella sha256 de cada fuente Lean registrado en
las evidencias de Gao, Garner y Wu y de Ocelotas, con fines de línea LF y tal
cual, y la compara con la registrada. Revisa además que las auditorías
guardadas sólo nombren los axiomas estándar y ninguna sorryAx. Una huella
igual dice que el fuente no cambió desde la auditoría; no repite la auditoría.
"""

import argparse
import hashlib
import json
from pathlib import Path
import re

ESTANDAR = {'propext', 'Classical.choice', 'choice', 'Quot.sound'}


def huellas(ruta):
    datos = ruta.read_bytes()
    return {'lf': hashlib.sha256(datos.replace(b'\r\n', b'\n')).hexdigest(),
            'tal_cual': hashlib.sha256(datos).hexdigest()}


def comparar(ruta, registrada):
    if not ruta.exists():
        return 'falta el archivo'
    actual = huellas(ruta)
    if registrada == actual['lf']:
        return 'igual (LF)'
    if registrada == actual['tal_cual']:
        return 'igual (tal cual)'
    return 'distinta'


def axiomas_de_auditoria(texto):
    usados, consultas = set(), 0
    for lista in re.findall(r'depends on axioms: \[([^\]]*)\]', texto):
        consultas += 1
        usados |= {a.strip() for a in lista.split(',') if a.strip()}
    sin_axiomas = len(re.findall(r'does not depend on any axioms', texto))
    return usados, consultas, sin_axiomas


def revisar_gao(raiz):
    carpeta = raiz / 'depuracion/gao20260920/formal'
    datos = json.loads((raiz / 'depuracion/gao20260920/evidencia_gao_lean.json').read_text(encoding='utf-8'))
    filas, problemas = {}, []
    for nombre, info in datos['modulos'].items():
        estado = comparar(carpeta / f'{nombre}.lean', info['sha256'])
        axiomas = set(info['axiomas_usados'])
        filas[nombre] = {'huella': estado, 'consultas': info['consultas'],
                         'axiomas': sorted(axiomas), 'codigo': info['codigo']}
        if not estado.startswith('igual') or not axiomas <= ESTANDAR or info['codigo'] != 0 \
                or info['errores'] or not info['solo_estandar']:
            problemas.append(nombre)
    for nombre, registrada in datos['sha256'].items():
        estado = comparar(carpeta / nombre, registrada)
        filas[nombre] = {'huella': estado}
        if not estado.startswith('igual'):
            problemas.append(nombre)
    leanchecker = datos.get('leanchecker', {})
    return {
        'evidencia': 'depuracion/gao20260920/evidencia_gao_lean.json',
        'lean': datos['lean'],
        'mathlib': datos['mathlib_commit'],
        'modulos': filas,
        'leanchecker_todos_cero': all(v == 0 for v in leanchecker.values()),
        'leanchecker_revisados': len(leanchecker),
        'problemas': problemas,
    }


def fuentes_registradas(nodo, salida, nombre=None):
    if isinstance(nodo, dict):
        if nombre and isinstance(nodo.get('fuente'), str):
            salida.setdefault(nombre, set()).add(nodo['fuente'])
        for clave, valor in nodo.items():
            fuentes_registradas(valor, salida, clave)
    return salida


def revisar_ocelotas(raiz, archivo):
    carpeta = raiz / 'depuracion/cst20260930'
    datos = json.loads((carpeta / archivo).read_text(encoding='utf-8'))
    registradas = fuentes_registradas({'base': datos['prefijo_auditado'],
                                       'extensiones': datos['extensiones']}, {})
    filas, problemas = {}, []
    for nombre, valores in sorted(registradas.items()):
        estados = {comparar(carpeta / f'{nombre}.lean', v) for v in valores}
        estado = estados.pop() if len(estados) == 1 else 'registros discrepantes'
        filas[nombre] = estado
        if not estado.startswith('igual'):
            problemas.append(nombre)
    usados, consultas, sin_axiomas = axiomas_de_auditoria(datos['auditoria'])
    if not usados <= ESTANDAR or 'sorryAx' in datos['auditoria']:
        problemas.append('axiomas')
    return {
        'evidencia': f'depuracion/cst20260930/{archivo}',
        'modulo_final': datos['modulo'],
        'lean': datos['version_lean'],
        'fuentes_revisadas': len(filas),
        'huellas': filas,
        'consultas_registradas': datos['consultas'],
        'consultas_en_auditoria': consultas,
        'consultas_sin_axiomas': sin_axiomas,
        'axiomas_en_auditoria': sorted(usados),
        'problemas': problemas,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--raiz', default='.')
    parser.add_argument('--salida', default='depuracion/judas20261016/vigencia_expediente.json')
    args = parser.parse_args()
    raiz = Path(args.raiz)
    resultado = {
        'fecha': '2026-10-16',
        'gao_garner_wu': revisar_gao(raiz),
        'ocelotas_83': revisar_ocelotas(raiz, 'evidencia_rozier.json'),
        'record_roosendaal': revisar_ocelotas(raiz, 'evidencia_record_roosendaal.json'),
    }
    problemas = sum(len(v['problemas']) for v in resultado.values() if isinstance(v, dict))
    resultado['problemas_totales'] = problemas
    Path(args.salida).write_text(json.dumps(resultado, ensure_ascii=False, indent=1) + '\n',
                                 encoding='utf-8')
    g, o, r = resultado['gao_garner_wu'], resultado['ocelotas_83'], resultado['record_roosendaal']
    print('Gao/Garner/Wu:', len(g['modulos']), 'archivos;',
          {k: v['huella'] for k, v in g['modulos'].items()},
          '| leanchecker en cero:', g['leanchecker_todos_cero'], g['leanchecker_revisados'])
    for nombre, bloque in (('Ocelotas 83', o), ('Récord Roosendaal', r)):
        conteo = {}
        for estado in bloque['huellas'].values():
            conteo[estado] = conteo.get(estado, 0) + 1
        print(f"{nombre}: {bloque['fuentes_revisadas']} fuentes {conteo}; consultas "
              f"{bloque['consultas_registradas']} (auditoría: {bloque['consultas_en_auditoria']} "
              f"con axiomas, {bloque['consultas_sin_axiomas']} sin axiomas); "
              f"axiomas {bloque['axiomas_en_auditoria']}")
    print('problemas totales:', problemas, [v['problemas'] for v in resultado.values() if isinstance(v, dict)])


if __name__ == '__main__':
    main()
