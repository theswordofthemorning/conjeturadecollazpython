"""Compila Lagartijas.lean y guarda versiones, hashes y consultas de axiomas.

Uso (con la caché de Mathlib ya descargada, ver formal/README.md):
    python -B -X utf8 evidencia_lagartijas_lean.py
"""

import hashlib
import json
from pathlib import Path
import subprocess

CARPETA = Path(__file__).resolve().parent
FORMAL = CARPETA / 'formal'


def sha(ruta):
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def main():
    version = subprocess.run(['lean', '--version'], capture_output=True, text=True,
                             cwd=FORMAL).stdout.strip()
    salida = subprocess.run(['lake', 'env', 'lean', 'Lagartijas.lean'], capture_output=True,
                            text=True, encoding='utf-8', errors='replace', cwd=FORMAL)
    texto = salida.stdout + salida.stderr
    consultas = [l for l in texto.splitlines() if 'depends on axioms' in l]
    manifiesto = json.loads((FORMAL / 'lake-manifest.json').read_text(encoding='utf-8'))
    mathlib = next(p['rev'] for p in manifiesto['packages'] if p['name'] == 'mathlib')
    evidencia = dict(
        comando='lake env lean Lagartijas.lean', codigo=salida.returncode, lean=version,
        mathlib_commit=mathlib, consultas=len(consultas),
        admite_sorry='sorryAx' in texto or "declaration uses 'sorry'" in texto,
        errores=[l for l in texto.splitlines() if 'error' in l],
        axiomas=consultas,
        sha256={n: sha(FORMAL / n) for n in
                ('Lagartijas.lean', 'lakefile.lean', 'lake-manifest.json', 'lean-toolchain')})
    (CARPETA / 'evidencia_lagartijas_lean.json').write_text(
        json.dumps(evidencia, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    ok = salida.returncode == 0 and not evidencia['admite_sorry'] and not evidencia['errores']
    print(f"{len(consultas)} consultas de axiomas; sorry={evidencia['admite_sorry']}; "
          f"codigo={salida.returncode}")
    print('OK' if ok else 'FALLO')
    return ok


if __name__ == '__main__':
    raise SystemExit(0 if main() else 1)
