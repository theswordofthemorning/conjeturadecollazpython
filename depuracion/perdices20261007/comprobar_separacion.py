"""Audita el cierre previo y compila los diez lemas de separación.

Los 14 objetos previos se cotejan con fuentes, entorno y evidencia;
si faltan, ejecutar comprobar_cruce.py. Sólo el módulo nuevo se compila.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

from comprobar_cruce import ADMITIDOS, CARPETA, FORMAL, RAIZ, auditar


def huella(ruta):
    return hashlib.sha256(Path(ruta).read_bytes()).hexdigest()


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--compilados', type=Path, required=True)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    compilados = args.compilados.resolve()
    subprocess.run([sys.executable, '-B', '-X', 'utf8', str(CARPETA / 'auditar_cruce.py'),
                    '--compilados', str(compilados),
                    '--salida', str(compilados / 'auditoria_base_separacion.json')], check=True)
    base = json.loads((CARPETA / 'evidencia_cruce.json').read_text(encoding='utf-8'))
    version = subprocess.run(['lake', 'env', 'lean', '--version'], cwd=FORMAL,
                             check=True, capture_output=True, text=True, encoding='utf-8').stdout.strip()
    assert version == base['contexto']['version_lean']
    entorno = dict(os.environ)
    entorno['LEAN_PATH'] = str(compilados) + os.pathsep + entorno.get('LEAN_PATH', '')
    fuente = CARPETA / 'PerdicesSeparacion.lean'
    objeto = compilados / 'PerdicesSeparacion.olean'
    antes = huella(fuente)
    resultado = subprocess.run(['lake', 'env', 'lean', '-R', str(CARPETA), '-o', str(objeto),
                                str(fuente)], cwd=FORMAL, env=entorno,
                               capture_output=True, text=True, encoding='utf-8')
    salida = resultado.stdout + resultado.stderr
    assert resultado.returncode == 0, salida
    axiomas = auditar('PerdicesSeparacion', fuente.read_text(encoding='utf-8'), salida)
    assert len(axiomas) == 10 and huella(fuente) == antes
    assert all(set(a) <= ADMITIDOS for a in axiomas.values())
    for nombre, dato in base['modulos'].items():
        assert huella(compilados / (nombre + '.olean')) == dato['objeto'], nombre
    archivos = [Path(__file__), fuente, CARPETA / 'comprobar_cruce.py',
                CARPETA / 'auditar_cruce.py', CARPETA / 'evidencia_cruce.json',
                CARPETA / 'auditoria_cruce.json']
    evidencia = dict(estado='módulo compilado; cierre previo auditado, sin recompilar',
                     version_lean=version, modulos=15, consultas=base['consultas'] + len(axiomas),
                     consultas_nuevas=len(axiomas), objeto=huella(objeto), axiomas=axiomas,
                     dependencias={'PerdicesCruce': base['modulos']['PerdicesCruce']['objeto']},
                     archivos={p.relative_to(RAIZ).as_posix(): dict(
                         sha256_bytes=huella(p),
                         sha256_lf=hashlib.sha256(p.read_text(encoding='utf-8').encode('utf-8')).hexdigest())
                         for p in archivos})
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(json.dumps(evidencia, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    args.salida.with_suffix('.txt').write_text(version + '\n' + salida, encoding='utf-8')
    print(f"OK: 10 lemas nuevos, {evidencia['consultas']} consultas con el cierre previo.")


if __name__ == '__main__':
    main()
