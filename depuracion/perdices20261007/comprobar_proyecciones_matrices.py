"""Compila el módulo independiente PerdicesProyeccionesMatrices y registra sus axiomas."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


CARPETA = Path(__file__).resolve().parent
RAIZ = CARPETA.parents[1]
FORMAL = CARPETA.parent / 'gao20260920/formal'


def huella(ruta):
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def huella_lf(ruta):
    return hashlib.sha256(ruta.read_text(encoding='utf-8').encode('utf-8')).hexdigest()


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--compilados', type=Path, required=True)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    compilados = args.compilados.resolve()
    compilados.mkdir(parents=True, exist_ok=True)
    fuente = CARPETA / 'PerdicesProyeccionesMatrices.lean'
    codigo = fuente.read_text(encoding='utf-8')
    version = subprocess.check_output(['lake', 'env', 'lean', '--version'], cwd=FORMAL,
                                      text=True, encoding='utf-8').strip()
    assert 'version 4.32.2,' in version, version
    manifiesto = json.loads((FORMAL / 'lake-manifest.json').read_text(encoding='utf-8'))
    revision = next(p['rev'] for p in manifiesto['packages'] if p['name'] == 'mathlib')
    mathlib = FORMAL / '.lake/packages/mathlib'
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=mathlib,
                                   text=True, encoding='utf-8').strip() == revision
    bibliotecas = {}
    for nombre in re.findall(r'^import (\S+)$', codigo, re.MULTILINE):
        relativa = Path(*nombre.split('.'))
        archivo = mathlib / relativa.with_suffix('.lean')
        objeto = mathlib / '.lake/build/lib/lean' / relativa.with_suffix('.olean')
        fijada = subprocess.check_output(['git', 'show', revision + ':' +
                                         relativa.with_suffix('.lean').as_posix()], cwd=mathlib)
        assert hashlib.sha256(fijada.replace(b'\r\n', b'\n')).hexdigest() == huella_lf(archivo)
        bibliotecas[nombre] = dict(sha256_fuente_lf=huella_lf(archivo), sha256_objeto=huella(objeto))
    archivos = [fuente, Path(__file__), FORMAL / 'lean-toolchain', FORMAL / 'lake-manifest.json']
    antes = {p.relative_to(RAIZ).as_posix(): huella_lf(p) for p in archivos}
    objeto = compilados / 'PerdicesProyeccionesMatrices.olean'
    comando = ['lake', 'env', 'lean', '-R', str(CARPETA), '-o', str(objeto), str(fuente)]
    proceso = subprocess.run(comando, cwd=FORMAL, capture_output=True, text=True, encoding='utf-8')
    salida = proceso.stdout + proceso.stderr
    assert proceso.returncode == 0, salida
    assert not re.search(r'sorryAx|warning:|error:', salida), salida
    assert not re.search(r'^\s*(?:axiom|sorry)\b', codigo, re.MULTILINE)
    axiomas = dict(re.findall(r"'(PerdicesProyeccionesMatrices\.\w+)' depends on axioms: \[([^]]*)\]", salida))
    axiomas.update({nombre: '' for nombre in re.findall(
        r"'(PerdicesProyeccionesMatrices\.\w+)' does not depend on any axioms", salida)})
    teoremas = re.findall(r'^theorem (\w+)', codigo, re.MULTILINE)
    assert set(axiomas) == {'PerdicesProyeccionesMatrices.' + t for t in teoremas}
    for nombre, valores in list(axiomas.items()):
        axiomas[nombre] = [v.strip() for v in valores.split(',') if v.strip()]
        assert set(axiomas[nombre]) <= {'propext', 'Classical.choice', 'Quot.sound'}
    assert antes == {p.relative_to(RAIZ).as_posix(): huella_lf(p) for p in archivos}
    evidencia = dict(version_lean=version, revision_mathlib=revision,
                     modulo='PerdicesProyeccionesMatrices', consultas=len(axiomas), axiomas=axiomas,
                     archivos=antes, bibliotecas_directas=bibliotecas,
                     sha256_objeto=huella(objeto),
                     alcance='Diez lemas: obstrucción escalar natural, proyección 2x2 y acoplamiento '
                     'necesario en la primera etapa del objetivo 57. No excluye matrices '
                     'acopladas, otras familias ni prueba la terminación de H.')
    args.salida.write_text(json.dumps(evidencia, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    args.salida.with_suffix('.txt').write_text(version + '\n' + salida, encoding='utf-8')
    print(f'OK: {len(axiomas)} teoremas; sólo axiomas estándar, sin sorryAx.')


if __name__ == '__main__':
    main()
