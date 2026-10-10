"""Compila el cierre orbital de excursiones y audita sus 15 módulos previos.

No recompila el cierre previo. Si faltan objetos, reproducir primero
comprobar_cruce.py y comprobar_separacion.py en la misma carpeta temporal.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

from comprobar_cruce import CARPETA, FORMAL, RAIZ, auditar


def huellas(ruta):
    return dict(sha256_bytes=hashlib.sha256(ruta.read_bytes()).hexdigest(),
                sha256_lf=hashlib.sha256(ruta.read_text(encoding='utf-8').encode('utf-8')).hexdigest())


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--compilados', type=Path, required=True)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    compilados = args.compilados.resolve()
    subprocess.run([sys.executable, '-B', '-X', 'utf8', str(CARPETA / 'auditar_cruce.py'),
                    '--compilados', str(compilados),
                    '--salida', str(compilados / 'auditoria_base_excursiones.json')], check=True)
    base = json.loads((CARPETA / 'evidencia_cruce.json').read_text(encoding='utf-8'))
    separacion = json.loads((CARPETA / 'evidencia_separacion.json').read_text(encoding='utf-8'))
    version = subprocess.run(['lake', 'env', 'lean', '--version'], cwd=FORMAL,
                             check=True, capture_output=True, text=True, encoding='utf-8').stdout.strip()
    assert version == separacion['version_lean'] == base['contexto']['version_lean']
    for nombre, dato in separacion['archivos'].items():
        assert huellas(RAIZ / nombre)['sha256_lf'] == dato['sha256_lf'], nombre
    fuente_previa = CARPETA / 'PerdicesSeparacion.lean'
    salida_previa = (CARPETA / 'evidencia_separacion.txt').read_text(encoding='utf-8')
    assert auditar('PerdicesSeparacion', fuente_previa.read_text(encoding='utf-8'),
                   salida_previa) == separacion['axiomas']
    assert separacion['consultas'] == base['consultas'] + len(separacion['axiomas']) == 132
    assert separacion['dependencias'] == {'PerdicesCruce': base['modulos']['PerdicesCruce']['objeto']}
    previos = {n: d['objeto'] for n, d in base['modulos'].items()}
    previos['PerdicesSeparacion'] = separacion['objeto']

    def comprobar_objetos():
        for nombre, esperada in previos.items():
            actual = hashlib.sha256((compilados / (nombre + '.olean')).read_bytes()).hexdigest()
            assert actual == esperada, nombre

    comprobar_objetos()
    fuente = CARPETA / 'PerdicesExcursiones.lean'
    codigo = fuente.read_text(encoding='utf-8')
    dependencias = {d: previos[d] for linea in re.findall(r'^import (.+)$', codigo, re.MULTILINE)
                    for d in linea.split()}
    archivos = [Path(__file__), fuente, fuente_previa, CARPETA / 'comprobar_separacion.py',
                CARPETA / 'evidencia_separacion.json', CARPETA / 'evidencia_separacion.txt',
                CARPETA / 'comprobar_cruce.py', CARPETA / 'auditar_cruce.py',
                CARPETA / 'evidencia_cruce.json', CARPETA / 'auditoria_cruce.json',
                FORMAL / 'lean-toolchain', FORMAL / 'lake-manifest.json']
    antes = {p.relative_to(RAIZ).as_posix(): huellas(p) for p in archivos}
    entorno = dict(os.environ)
    entorno['LEAN_PATH'] = str(compilados) + os.pathsep + entorno.get('LEAN_PATH', '')
    objeto = compilados / 'PerdicesExcursiones.olean'
    resultado = subprocess.run(['lake', 'env', 'lean', '-R', str(CARPETA), '-o', str(objeto),
                                str(fuente)], cwd=FORMAL, env=entorno,
                               capture_output=True, text=True, encoding='utf-8')
    salida = resultado.stdout + resultado.stderr
    assert resultado.returncode == 0, salida
    axiomas = auditar('PerdicesExcursiones', codigo, salida)
    assert len(axiomas) == 10
    comprobar_objetos()
    assert antes == {p.relative_to(RAIZ).as_posix(): huellas(p) for p in archivos}
    evidencia = dict(estado='módulo compilado; 15 módulos previos auditados sin recompilar',
                     version_lean=version, modulos=16, consultas=132 + len(axiomas),
                     consultas_nuevas=len(axiomas), axiomas=axiomas,
                     objeto=hashlib.sha256(objeto.read_bytes()).hexdigest(),
                     dependencias=dependencias, objetos_previos=previos, archivos=antes)
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(json.dumps(evidencia, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    args.salida.with_suffix('.txt').write_text(version + '\n' + salida, encoding='utf-8')
    print(f"OK: 10 lemas nuevos, {evidencia['consultas']} consultas con el cierre previo.")


if __name__ == '__main__':
    main()
