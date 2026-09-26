"""Compila Lagartijas, Martas, Tejonas, GaoEnunciado, Hienas, GaoLiteral, Alpacas,
GarnerEnunciado, Condoras y WuEnunciado; guarda versiones, hashes y axiomas, y repasa con
leanchecker toda la cadena de módulos propios.

Los hashes se toman con finales de línea LF, como el blob de Git, para que no cambien
con la conversión CRLF de Windows.

Uso (con la caché de Mathlib ya descargada, ver formal/README.md):
    python -B -X utf8 evidencia_gao_lean.py
"""

import hashlib
import json
from pathlib import Path
import subprocess

CARPETA = Path(__file__).resolve().parent
FORMAL = CARPETA / 'formal'
MODULOS = ('Lagartijas', 'Martas', 'Tejonas', 'GaoEnunciado', 'Hienas', 'GaoLiteral',
           'Alpacas', 'GarnerEnunciado', 'Condoras', 'WuEnunciado')
AXIOMAS_ESTANDAR = {'propext', 'Classical.choice', 'choice', 'Quot.sound'}


def sha(ruta):
    return hashlib.sha256(ruta.read_bytes().replace(b'\r\n', b'\n')).hexdigest()


def main():
    version = subprocess.run(['lean', '--version'], capture_output=True, text=True,
                             cwd=FORMAL).stdout.strip()
    build = subprocess.run(['lake', 'build', 'GaoCore', 'GaoFormal'], capture_output=True,
                           text=True, encoding='utf-8', errors='replace', cwd=FORMAL)
    manifiesto = json.loads((FORMAL / 'lake-manifest.json').read_text(encoding='utf-8'))
    mathlib = next(p['rev'] for p in manifiesto['packages'] if p['name'] == 'mathlib')
    evidencia = dict(lean=version, mathlib_commit=mathlib,
                     lake_build=dict(codigo=build.returncode,
                                     final=build.stdout.strip().splitlines()[-1:]),
                     modulos={})
    ok = build.returncode == 0
    for m in MODULOS:
        salida = subprocess.run(['lake', 'env', 'lean', f'{m}.lean'], capture_output=True,
                                text=True, encoding='utf-8', errors='replace', cwd=FORMAL)
        texto = salida.stdout + salida.stderr
        consultas = [l for l in texto.splitlines() if 'depends on axioms' in l]
        usados = set()
        for l in consultas:
            usados |= {a.strip() for a in l.split('[', 1)[1].rstrip(']').split(',')}
        errores = [l for l in texto.splitlines() if ': error' in l]
        evidencia['modulos'][m] = dict(
            codigo=salida.returncode, consultas=len(consultas), errores=errores,
            axiomas_usados=sorted(usados), solo_estandar=usados <= AXIOMAS_ESTANDAR,
            sha256=sha(FORMAL / f'{m}.lean'), axiomas=consultas)
        ok = ok and salida.returncode == 0 and not errores and usados <= AXIOMAS_ESTANDAR
    cadena = ('cadena_completa', 'rachas', 'Momentos', 'Maximos', 'Resto', 'Producto',
              'Supervivencia', 'Banda', 'RachasEnteras', 'UmbralRachas', 'Reloj', 'Palabras',
              'SalidaPalabras', 'Ventana', 'ParametrosVentana', 'Hormigas', 'Ensayo',
              'Repeticion', 'Guardias', 'ConteoEnsayos') + MODULOS
    evidencia['leanchecker'] = {}
    for m in cadena:
        r = subprocess.run(['lake', 'env', 'leanchecker', m], capture_output=True, text=True,
                           encoding='utf-8', errors='replace', cwd=FORMAL)
        evidencia['leanchecker'][m] = r.returncode
        ok = ok and r.returncode == 0
    print('leanchecker:', sum(v == 0 for v in evidencia['leanchecker'].values()), 'de',
          len(cadena), 'módulos con código 0')
    evidencia['sha256'] = {n: sha(FORMAL / n) for n in
                           ('lakefile.lean', 'lake-manifest.json', 'lean-toolchain')}
    (CARPETA / 'evidencia_gao_lean.json').write_text(
        json.dumps(evidencia, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for m, d in evidencia['modulos'].items():
        print(f"{m}: {d['consultas']} consultas, axiomas {d['axiomas_usados']}")
    print('OK' if ok else 'FALLO')
    return ok


if __name__ == '__main__':
    raise SystemExit(0 if main() else 1)
