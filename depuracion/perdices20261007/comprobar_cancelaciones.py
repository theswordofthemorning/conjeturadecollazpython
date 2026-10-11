"""Audita 26 módulos previos y compila únicamente PerdicesCancelaciones."""

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
                    '--salida', str(compilados / 'auditoria_base_cancelaciones.json')], check=True)
    base = json.loads((CARPETA / 'evidencia_cruce.json').read_text(encoding='utf-8'))
    version = subprocess.run(['lake', 'env', 'lean', '--version'], cwd=FORMAL,
                             check=True, capture_output=True, text=True, encoding='utf-8').stdout.strip()
    assert version == base['contexto']['version_lean']
    previos = {n: d['objeto'] for n, d in base['modulos'].items()}
    consultas = base['consultas']
    bibliotecas = {}
    mathlib = FORMAL / '.lake/packages/mathlib'
    manifiesto = json.loads((FORMAL / 'lake-manifest.json').read_text(encoding='utf-8'))
    revision = next(p['rev'] for p in manifiesto['packages'] if p['name'] == 'mathlib')
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=mathlib,
                                   text=True, encoding='utf-8').strip() == revision

    def dependencia(nombre):
        if nombre in previos:
            return previos[nombre]
        assert nombre.startswith('Mathlib.'), nombre
        relativa = Path(*nombre.split('.'))
        fuente = mathlib / relativa.with_suffix('.lean')
        objeto = mathlib / '.lake/build/lib/lean' / relativa.with_suffix('.olean')
        fijada = subprocess.check_output(['git', 'show', revision + ':' +
                                          relativa.with_suffix('.lean').as_posix()], cwd=mathlib)
        huella_fijada = hashlib.sha256(fijada.replace(b'\r\n', b'\n')).hexdigest()
        assert huellas(fuente)['sha256_lf'] == huella_fijada
        dato = dict(fuente=fuente.relative_to(FORMAL).as_posix(),
                    objeto=objeto.relative_to(FORMAL).as_posix(),
                    sha256_fuente_lf=huellas(fuente)['sha256_lf'],
                    sha256_objeto=hashlib.sha256(objeto.read_bytes()).hexdigest())
        if nombre in bibliotecas:
            assert bibliotecas[nombre] == dato
        bibliotecas[nombre] = dato
        return dato['sha256_objeto']

    def comprobar_bibliotecas():
        for dato in bibliotecas.values():
            assert huellas(FORMAL / dato['fuente'])['sha256_lf'] == dato['sha256_fuente_lf']
            assert hashlib.sha256((FORMAL / dato['objeto']).read_bytes()).hexdigest() == dato['sha256_objeto']

    archivos = [Path(__file__), CARPETA / 'comprobar_cruce.py', CARPETA / 'auditar_cruce.py',
                CARPETA / 'evidencia_cruce.json', CARPETA / 'auditoria_cruce.json',
                FORMAL / 'lean-toolchain', FORMAL / 'lake-manifest.json']
    for etiqueta in ('separacion', 'excursiones', 'ritmo', 'balance', 'excepciones', 'aporte', 'semilla', 'novena', 'colisiones', 'cola', 'minimos', 'repeticiones'):
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
        dependencias = {d: dependencia(d) for linea in re.findall(r'^import (.+)$',
                        fuente.read_text(encoding='utf-8'), re.MULTILINE) for d in linea.split()}
        assert dependencias == previa['dependencias']
        if 'objetos_previos' in previa:
            assert previos == previa['objetos_previos']
        consultas += len(previa['axiomas'])
        assert consultas == previa['consultas']
        previos[nombre] = previa['objeto']
        archivos += [ruta, salida, fuente, CARPETA / f'comprobar_{etiqueta}.py']
    assert len(previos) == 26 and consultas == 309

    def comprobar_objetos():
        for nombre, esperada in previos.items():
            assert hashlib.sha256((compilados / (nombre + '.olean')).read_bytes()).hexdigest() == esperada, nombre

    comprobar_objetos()
    fuente = CARPETA / 'PerdicesCancelaciones.lean'
    codigo = fuente.read_text(encoding='utf-8')
    archivos.append(fuente)
    antes = {p.relative_to(RAIZ).as_posix(): huellas(p) for p in archivos}
    dependencias = {d: dependencia(d) for linea in re.findall(r'^import (.+)$', codigo, re.MULTILINE)
                    for d in linea.split()}
    comprobar_bibliotecas()
    entorno = dict(os.environ)
    entorno['LEAN_PATH'] = str(compilados) + os.pathsep + entorno.get('LEAN_PATH', '')
    objeto = compilados / 'PerdicesCancelaciones.olean'
    resultado = subprocess.run(['lake', 'env', 'lean', '-R', str(CARPETA), '-o', str(objeto),
                                str(fuente)], cwd=FORMAL, env=entorno,
                               capture_output=True, text=True, encoding='utf-8')
    salida = resultado.stdout + resultado.stderr
    assert resultado.returncode == 0, salida
    axiomas = auditar('PerdicesCancelaciones', codigo, salida)
    assert len(axiomas) == 20
    comprobar_objetos()
    comprobar_bibliotecas()
    assert antes == {p.relative_to(RAIZ).as_posix(): huellas(p) for p in archivos}
    evidencia = dict(estado='módulo compilado; 26 módulos previos auditados sin recompilar',
                     version_lean=version, modulos=27, consultas=consultas + len(axiomas),
                     consultas_nuevas=len(axiomas), axiomas=axiomas,
                     objeto=hashlib.sha256(objeto.read_bytes()).hexdigest(),
                     dependencias=dependencias, objetos_previos=previos, archivos=antes,
                     revision_mathlib=revision, bibliotecas=bibliotecas)
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(json.dumps(evidencia, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    args.salida.with_suffix('.txt').write_text(version + '\n' + salida, encoding='utf-8')
    print(f"OK: 20 lemas nuevos, {evidencia['consultas']} consultas con el cierre previo.")


if __name__ == '__main__':
    main()
