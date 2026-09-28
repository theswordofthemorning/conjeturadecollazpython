"""Arma el zip del artefacto Lean para Zenodo (27-09-2026).

Toma los fuentes de HEAD con `git show` (bytes exactos, con LF), comprueba
sus SHA-256 contra depuracion/gao20260920/evidencia_gao_lean.json y añade
el README en inglés, la licencia Apache 2.0 (el texto de la copia de
Mathlib) y la salida de revision_wu.py con N_MAX = 24.

Conserva la estructura de carpetas del repositorio para que lakefile.lean
funcione sin cambios (GaoCore lee ../cadena_completa.lean y MangostasCore
lee ../../frente20260910/rachas.lean). No incluye formal/README.md, que
está en castellano y enlaza notas que no van en el archivo.

Uso: python -B -X utf8 papers/zenodo/armar_artefacto.py
"""

import hashlib
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
AQUI = Path(__file__).resolve().parent
NOMBRE = 'said-duran-collatz-lean-1.0.0'
SALIDA = AQUI / (NOMBRE + '.zip')
COMMIT = 'HEAD'
FECHA = (2026, 9, 27, 0, 0, 0)

FORMAL = 'depuracion/gao20260920/formal/'
MODULOS = ['Momentos', 'Maximos', 'Resto', 'Producto', 'Supervivencia', 'Banda',
           'RachasEnteras', 'UmbralRachas', 'Reloj', 'Palabras', 'SalidaPalabras',
           'Ventana', 'ParametrosVentana', 'Hormigas', 'Ensayo', 'Repeticion',
           'Guardias', 'ConteoEnsayos', 'Lagartijas', 'Martas', 'Tejonas',
           'GaoEnunciado', 'Hienas', 'GaoLiteral', 'Alpacas', 'GarnerEnunciado',
           'Condoras', 'WuEnunciado']
DESDE_GIT = ([FORMAL + m + '.lean' for m in MODULOS]
             + ['depuracion/gao20260920/cadena_completa.lean',
                'depuracion/frente20260910/rachas.lean',
                FORMAL + 'lakefile.lean', FORMAL + 'lean-toolchain',
                FORMAL + 'lake-manifest.json', FORMAL + '.gitignore',
                'depuracion/gao20260920/evidencia_gao_lean.json'])
CHECKS = {
    'revision_gao.py': 'papers/revision20260927/revision_gao.py',
    'revision_gao_salida.txt': 'papers/revision20260927/revision_gao_salida.txt',
    'tabla2_1e8_salida.txt': 'papers/revision20260927/tabla2_1e8_salida.txt',
    'revision_garner.py': 'papers/revision20260927/revision_garner.py',
    'revision_garner_salida.txt': 'papers/revision20260927/revision_garner_salida.txt',
    'revision_wu.py': 'papers/revision20260927/revision_wu.py',
    'revision_wu_salida.txt': 'papers/revision20260927/revision_wu_salida.txt',
    'terminos_oeis.py': 'papers/oeis/terminos_oeis.py',
    'terminos_oeis_salida.txt': 'papers/oeis/terminos_oeis_salida.txt',
    'verificar_alpacas.py': 'depuracion/garner20260926/verificar_alpacas.py',
    'verificar_alpacas_salida.txt': 'depuracion/garner20260926/verificar_alpacas_salida.txt',
    'verificar_lagartijas.py': 'depuracion/gao20260920/verificar_lagartijas.py',
    'verificar_lagartijas_pares.py': 'depuracion/gao20260920/verificar_lagartijas_pares.py',
    'evidencia_lagartijas_exacta.json': 'depuracion/gao20260920/evidencia_lagartijas_exacta.json',
    'evidencia_lagartijas_pares.json': 'depuracion/gao20260920/evidencia_lagartijas_pares.json',
}
FUERA_DE_GIT = {
    'README.md': AQUI / 'README_artefacto.md',
    'LICENSE': RAIZ / FORMAL / '.lake/packages/mathlib/LICENSE',
    'checks/revision_wu_n24_salida.txt': AQUI / 'revision_wu_n24_salida.txt',
}


def git_bytes(ruta):
    return subprocess.run(['git', '-C', str(RAIZ), 'show', COMMIT + ':' + ruta],
                          check=True, capture_output=True).stdout


def sha(datos):
    return hashlib.sha256(datos).hexdigest()


def main():
    contenido = {}
    for ruta in DESDE_GIT:
        contenido[ruta] = git_bytes(ruta)
    for destino, origen in CHECKS.items():
        contenido['checks/' + destino] = git_bytes(origen)
    for destino, origen in FUERA_DE_GIT.items():
        contenido[destino] = origen.read_bytes().replace(b'\r\n', b'\n')

    # hashes contra la evidencia del 26-09
    evidencia = json.loads(contenido['depuracion/gao20260920/evidencia_gao_lean.json'])
    fallos = []
    comprobados = 0
    for modulo, datos in evidencia['modulos'].items():
        ruta = FORMAL + modulo + '.lean'
        comprobados += 1
        if sha(contenido[ruta]) != datos['sha256']:
            fallos.append(ruta)
    for nombre, esperado in evidencia['sha256'].items():
        comprobados += 1
        if sha(contenido[FORMAL + nombre]) != esperado:
            fallos.append(FORMAL + nombre)
    for modulo, datos in evidencia['leanchecker'].items():
        codigo = datos.get('codigo') if isinstance(datos, dict) else datos
        if codigo != 0:
            fallos.append('leanchecker ' + modulo)
    print('hashes comprobados contra la evidencia:', comprobados,
          '| módulos con leanchecker:', len(evidencia['leanchecker']))
    for texto in ('sorry', 'admit', 'native_decide'):
        patron = re.compile(rb'\b' + texto.encode() + rb'\b')
        for ruta, datos in contenido.items():
            if ruta.endswith('.lean') and patron.search(datos):
                fallos.append(texto + ' en ' + ruta)
    if fallos:
        print('FALLO:', fallos)
        return False

    SALIDA.unlink(missing_ok=True)
    with zipfile.ZipFile(SALIDA, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for ruta in sorted(contenido):
            info = zipfile.ZipInfo(NOMBRE + '/' + ruta, FECHA)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, contenido[ruta])
    total = sum(len(d) for d in contenido.values())
    print('ficheros:', len(contenido), '| bytes sin comprimir:', total)
    print('zip:', SALIDA.name, SALIDA.stat().st_size, 'bytes')
    print('sha256 del zip:', sha(SALIDA.read_bytes()))
    print('OK')
    return True


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
