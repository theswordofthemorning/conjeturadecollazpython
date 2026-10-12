"""Audita ProyeccionesMatrices y compila el bloque de soportes y rectas."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

from comprobar_proyecciones_matrices import CARPETA, FORMAL, RAIZ, huella, huella_lf


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--compilados', type=Path, required=True)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    compilados = args.compilados.resolve()
    compilados.mkdir(parents=True, exist_ok=True)
    archivo_base = CARPETA / 'evidencia_proyecciones_matrices.json'
    base = json.loads(archivo_base.read_text(encoding='utf-8'))
    dependencia = compilados / 'PerdicesProyeccionesMatrices.olean'
    if not dependencia.exists():
        subprocess.run([sys.executable, '-B', '-X', 'utf8',
                        str(CARPETA / 'comprobar_proyecciones_matrices.py'),
                        '--compilados', str(compilados),
                        '--salida', str(compilados / 'proyecciones.json')], check=True)
    assert huella(dependencia) == base['sha256_objeto']
    for archivo, esperada in base['archivos'].items():
        assert huella_lf(RAIZ / archivo) == esperada, archivo
    for valores in base['axiomas'].values():
        assert set(valores) <= {'propext', 'Classical.choice', 'Quot.sound'}
    version = subprocess.check_output(['lake', 'env', 'lean', '--version'], cwd=FORMAL,
                                      text=True, encoding='utf-8').strip()
    assert version == base['version_lean']
    revision = base['revision_mathlib']
    mathlib = FORMAL / '.lake/packages/mathlib'
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=mathlib,
                                   text=True, encoding='utf-8').strip() == revision
    bibliotecas = {}
    for nombre in list(base['bibliotecas_directas']) + ['Mathlib.Tactic.Ring', 'Mathlib.Tactic.Tauto']:
        relativa = Path(*nombre.split('.'))
        archivo = mathlib / relativa.with_suffix('.lean')
        objeto = mathlib / '.lake/build/lib/lean' / relativa.with_suffix('.olean')
        fijada = subprocess.check_output(['git', 'show', revision + ':' +
                                         relativa.with_suffix('.lean').as_posix()], cwd=mathlib)
        assert hashlib.sha256(fijada.replace(b'\r\n', b'\n')).hexdigest() == huella_lf(archivo)
        dato = dict(sha256_fuente_lf=huella_lf(archivo), sha256_objeto=huella(objeto))
        if nombre in base['bibliotecas_directas']:
            assert dato == base['bibliotecas_directas'][nombre]
        bibliotecas[nombre] = dato
    fuente = CARPETA / 'PerdicesSoportesMatrices.lean'
    codigo = fuente.read_text(encoding='utf-8')
    archivos = [fuente, Path(__file__), archivo_base]
    antes = {p.relative_to(RAIZ).as_posix(): huella_lf(p) for p in archivos}
    objeto = compilados / 'PerdicesSoportesMatrices.olean'
    entorno = dict(os.environ)
    entorno['LEAN_PATH'] = str(compilados) + os.pathsep + entorno.get('LEAN_PATH', '')
    proceso = subprocess.run(['lake', 'env', 'lean', '-R', str(CARPETA), '-o', str(objeto), str(fuente)],
                             cwd=FORMAL, env=entorno, capture_output=True, text=True, encoding='utf-8')
    salida = proceso.stdout + proceso.stderr
    assert proceso.returncode == 0, salida
    assert not re.search(r'sorryAx|warning:|error:', salida), salida
    assert not re.search(r'^\s*(?:axiom|sorry)\b', codigo, re.MULTILINE)
    axiomas = dict(re.findall(r"'(PerdicesSoportesMatrices\.\w+)' depends on axioms: \[([^]]*)\]", salida))
    axiomas.update({n: '' for n in re.findall(
        r"'(PerdicesSoportesMatrices\.\w+)' does not depend on any axioms", salida)})
    teoremas = re.findall(r'^theorem (\w+)', codigo, re.MULTILINE)
    assert set(axiomas) == {'PerdicesSoportesMatrices.' + t for t in teoremas}
    for nombre, valores in list(axiomas.items()):
        axiomas[nombre] = [v.strip() for v in valores.split(',') if v.strip()]
        assert set(axiomas[nombre]) <= {'propext', 'Classical.choice', 'Quot.sound'}
    assert antes == {p.relative_to(RAIZ).as_posix(): huella_lf(p) for p in archivos}
    assert huella(dependencia) == base['sha256_objeto']
    for archivo, esperada in base['archivos'].items():
        assert huella_lf(RAIZ / archivo) == esperada, archivo
    evidencia = dict(version_lean=version, revision_mathlib=revision,
                     modulo='PerdicesSoportesMatrices', consultas_nuevas=len(axiomas),
                     consultas_con_base=base['consultas'] + len(axiomas), axiomas=axiomas,
                     archivos=antes, bibliotecas_directas=bibliotecas,
                     sha256_objeto=huella(objeto), dependencia=base['sha256_objeto'],
                     alcance='Rectas invariantes naturales comunes de a,b,c,e,f,g: '
                     'obstrucción a la primera eliminación del objetivo 57, sin cota. '
                     'Diez soportes mínimos equivalen a un aporte izquierdo positivo; '
                     'son necesarios, no suficientes, para descenso. No prueba terminación de H.')
    args.salida.write_text(json.dumps(evidencia, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    args.salida.with_suffix('.txt').write_text(version + '\n' + salida, encoding='utf-8')
    print(f'OK: {len(axiomas)} teoremas nuevos; {evidencia["consultas_con_base"]} con base; sin sorryAx.')


if __name__ == '__main__':
    main()
