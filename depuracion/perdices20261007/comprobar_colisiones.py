"""Audita 22 módulos previos y compila únicamente PerdicesColisiones."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

from comprobar_cruce import CARPETA, FORMAL, RAIZ, auditar
from comprobar_ritmo import huellas


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--compilados', type=Path, required=True)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    compilados = args.compilados.resolve()
    subprocess.run([sys.executable, '-B', '-X', 'utf8', str(CARPETA / 'auditar_cruce.py'),
                    '--compilados', str(compilados),
                    '--salida', str(compilados / 'auditoria_base_colisiones.json')], check=True)
    base = json.loads((CARPETA / 'evidencia_cruce.json').read_text(encoding='utf-8'))
    version = subprocess.run(['lake', 'env', 'lean', '--version'], cwd=FORMAL,
                             check=True, capture_output=True, text=True, encoding='utf-8').stdout.strip()
    assert version == base['contexto']['version_lean']
    previos = {n: d['objeto'] for n, d in base['modulos'].items()}
    consultas = base['consultas']
    archivos = [Path(__file__), CARPETA / 'comprobar_cruce.py', CARPETA / 'auditar_cruce.py',
                CARPETA / 'evidencia_cruce.json', CARPETA / 'auditoria_cruce.json',
                FORMAL / 'lean-toolchain', FORMAL / 'lake-manifest.json']
    for etiqueta in ('separacion', 'excursiones', 'ritmo', 'balance', 'excepciones', 'aporte', 'semilla', 'novena'):
        nombre = 'Perdices' + etiqueta.capitalize()
        ruta = CARPETA / f'evidencia_{etiqueta}.json'
        previa = json.loads(ruta.read_text(encoding='utf-8'))
        assert version == previa['version_lean']
        for archivo, dato in previa['archivos'].items():
            assert huellas(RAIZ / archivo)['sha256_lf'] == dato['sha256_lf'], archivo
        fuente = CARPETA / (nombre + '.lean')
        salida = ruta.with_suffix('.txt')
        assert auditar(nombre, fuente.read_text(encoding='utf-8'),
                       salida.read_text(encoding='utf-8')) == previa['axiomas']
        dependencias = {d: previos[d] for linea in re.findall(r'^import (.+)$',
                        fuente.read_text(encoding='utf-8'), re.MULTILINE) for d in linea.split()}
        assert dependencias == previa['dependencias']
        if 'objetos_previos' in previa:
            assert previos == previa['objetos_previos']
        consultas += len(previa['axiomas'])
        assert consultas == previa['consultas']
        previos[nombre] = previa['objeto']
        archivos += [ruta, salida, fuente, CARPETA / f'comprobar_{etiqueta}.py']
    assert len(previos) == 22 and consultas == 232

    def comprobar_objetos():
        for nombre, esperada in previos.items():
            assert hashlib.sha256((compilados / (nombre + '.olean')).read_bytes()).hexdigest() == esperada, nombre

    comprobar_objetos()
    fuente = CARPETA / 'PerdicesColisiones.lean'
    codigo = fuente.read_text(encoding='utf-8')
    archivos.append(fuente)
    antes = {p.relative_to(RAIZ).as_posix(): huellas(p) for p in archivos}
    dependencias = {d: previos[d] for linea in re.findall(r'^import (.+)$', codigo, re.MULTILINE)
                    for d in linea.split()}
    entorno = dict(os.environ)
    entorno['LEAN_PATH'] = str(compilados) + os.pathsep + entorno.get('LEAN_PATH', '')
    objeto = compilados / 'PerdicesColisiones.olean'
    resultado = subprocess.run(['lake', 'env', 'lean', '-R', str(CARPETA), '-o', str(objeto),
                                str(fuente)], cwd=FORMAL, env=entorno,
                               capture_output=True, text=True, encoding='utf-8')
    salida = resultado.stdout + resultado.stderr
    assert resultado.returncode == 0, salida
    axiomas = auditar('PerdicesColisiones', codigo, salida)
    assert len(axiomas) == 20
    comprobar_objetos()
    assert antes == {p.relative_to(RAIZ).as_posix(): huellas(p) for p in archivos}
    evidencia = dict(estado='módulo compilado; 22 módulos previos auditados sin recompilar',
                     version_lean=version, modulos=23, consultas=consultas + len(axiomas),
                     consultas_nuevas=len(axiomas), axiomas=axiomas,
                     objeto=hashlib.sha256(objeto.read_bytes()).hexdigest(),
                     dependencias=dependencias, objetos_previos=previos, archivos=antes)
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(json.dumps(evidencia, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    args.salida.with_suffix('.txt').write_text(version + '\n' + salida, encoding='utf-8')
    print(f"OK: 20 lemas nuevos, {evidencia['consultas']} consultas con el cierre previo.")


if __name__ == '__main__':
    main()
