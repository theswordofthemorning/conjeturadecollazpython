"""Audita el objeto de RetornoH y compila únicamente PerdicesRachasH."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

from comprobar_retorno_h import CARPETA, FORMAL, RAIZ, huella, huella_lf


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--compilados', type=Path, required=True)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    compilados = args.compilados.resolve()
    compilados.mkdir(parents=True, exist_ok=True)
    base = json.loads((CARPETA / 'evidencia_retorno_h.json').read_text(encoding='utf-8'))
    dependencia = compilados / 'PerdicesRetornoH.olean'
    if not dependencia.exists():
        subprocess.run([sys.executable, '-B', '-X', 'utf8', str(CARPETA / 'comprobar_retorno_h.py'),
                        '--compilados', str(compilados), '--salida', str(compilados / 'retorno_h.json')],
                       check=True)
    assert huella(dependencia) == base['sha256_objeto']
    for archivo, esperada in base['archivos'].items():
        assert huella_lf(RAIZ / archivo) == esperada, archivo
    version = subprocess.check_output(['lake', 'env', 'lean', '--version'], cwd=FORMAL,
                                      text=True, encoding='utf-8').strip()
    assert version == base['version_lean']
    mathlib = FORMAL / '.lake/packages/mathlib'
    revision = base['revision_mathlib']
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=mathlib,
                                   text=True, encoding='utf-8').strip() == revision
    bibliotecas = {}
    for nombre in list(base['bibliotecas_directas']) + ['Mathlib.Tactic.Ring']:
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
    fuente = CARPETA / 'PerdicesRachasH.lean'
    codigo = fuente.read_text(encoding='utf-8')
    archivos = [fuente, Path(__file__), CARPETA / 'evidencia_retorno_h.json']
    antes = {p.relative_to(RAIZ).as_posix(): huella_lf(p) for p in archivos}
    objeto = compilados / 'PerdicesRachasH.olean'
    entorno = dict(os.environ)
    entorno['LEAN_PATH'] = str(compilados) + os.pathsep + entorno.get('LEAN_PATH', '')
    proceso = subprocess.run(['lake', 'env', 'lean', '-R', str(CARPETA), '-o', str(objeto), str(fuente)],
                             cwd=FORMAL, env=entorno, capture_output=True, text=True, encoding='utf-8')
    salida = proceso.stdout + proceso.stderr
    assert proceso.returncode == 0, salida
    assert not re.search(r'sorryAx|warning:|error:', salida), salida
    axiomas = dict(re.findall(r"'(PerdicesRachasH\.\w+)' depends on axioms: \[([^]]*)\]", salida))
    teoremas = re.findall(r'^theorem (\w+)', codigo, re.MULTILINE)
    assert set(axiomas) == {'PerdicesRachasH.' + t for t in teoremas}
    for nombre, valores in list(axiomas.items()):
        axiomas[nombre] = [v.strip() for v in valores.split(',') if v.strip()]
        assert set(axiomas[nombre]) <= {'propext', 'Classical.choice', 'Quot.sound'}
    assert antes == {p.relative_to(RAIZ).as_posix(): huella_lf(p) for p in archivos}
    assert huella(dependencia) == base['sha256_objeto']
    evidencia = dict(version_lean=version, revision_mathlib=revision,
                     modulo='PerdicesRachasH', consultas_nuevas=len(axiomas),
                     consultas_con_base=base['consultas'] + len(axiomas), axiomas=axiomas,
                     archivos=antes, bibliotecas_directas=bibliotecas,
                     sha256_objeto=huella(objeto), dependencia=base['sha256_objeto'],
                     alcance='Rachas, composición, balance y unidades módulo 3. La maximalidad, '
                     'decodificación por valuaciones, cilindros y densidades tienen prueba escrita.')
    args.salida.write_text(json.dumps(evidencia, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    args.salida.with_suffix('.txt').write_text(version + '\n' + salida, encoding='utf-8')
    print(f'OK: {len(axiomas)} teoremas nuevos; {evidencia["consultas_con_base"]} con la base; axiomas estándar.')


if __name__ == '__main__':
    main()
