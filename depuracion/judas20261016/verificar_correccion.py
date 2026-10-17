"""Valida en copias temporales la corrección de fuentes de correccion_registro.json.

No toca el registro central. Genera con guardarafirmaciones.py una base con el
registro actual y otra con la corrección aplicada, ambas en una carpeta
temporal, y exige que la única diferencia sea el campo corregido de las filas
indicadas. Comprueba además que los archivos compartidos no cambien.
"""

import argparse
from contextlib import closing
import copy
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile

CARPETA = Path(__file__).resolve().parent
RAIZ = CARPETA.parents[1]
COLUMNAS = ('enunciado', 'cuantificador', 'estado', 'fichero', 'fuente', 'notas')


def huella(ruta):
    """sha256; los archivos de texto con fines de línea LF, las bases tal cual."""
    datos = ruta.read_bytes()
    if ruta.suffix in ('.json', '.py'):
        datos = datos.replace(b'\r\n', b'\n')
    return hashlib.sha256(datos).hexdigest()


def guardar(ruta, datos):
    ruta.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def generar(temporal, etiqueta, datos, mapa):
    datos = copy.deepcopy(datos)
    datos['mapa_investigacion'] = etiqueta + '_mapa.json'
    guardar(temporal / datos['mapa_investigacion'], mapa)
    ruta_registro = temporal / (etiqueta + '_registro.json')
    guardar(ruta_registro, datos)
    destino = temporal / (etiqueta + '.db')
    proceso = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(RAIZ / 'guardarafirmaciones.py'),
                              '--registro', str(ruta_registro), '--salida', str(destino)],
                             cwd=RAIZ, capture_output=True, text=True, encoding='utf-8', timeout=120)
    assert proceso.returncode == 0, proceso.stdout + proceso.stderr
    assert not proceso.stderr, proceso.stderr
    with closing(sqlite3.connect(destino)) as conexion:
        nombres = [f[0] for f in conexion.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")]
        return {nombre: conexion.execute('SELECT * FROM "' + nombre + '" ORDER BY rowid').fetchall()
                for nombre in nombres}


def main():
    analizador = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    analizador.add_argument('--propuesta', type=Path, default=CARPETA / 'correccion_registro.json')
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    registro = RAIZ / 'depuracion/coherencia20260913/registro.json'
    mapa = registro.with_name('mapa_investigacion.json')
    protegidos = [registro, mapa, RAIZ / 'afirmaciones.db', RAIZ / 'respuestas.db']
    antes = {str(r.relative_to(RAIZ)).replace('\\', '/'): huella(r) for r in protegidos}
    base = json.loads(registro.read_text(encoding='utf-8'))
    mapa_base = json.loads(mapa.read_text(encoding='utf-8'))
    propuesta = json.loads(args.propuesta.read_text(encoding='utf-8'))
    corregido = copy.deepcopy(base)
    por_clave = {alta['clave']: alta for alta in corregido['altas']}
    esperadas = {}
    for c in propuesta['correcciones']:
        assert c['campo'] in COLUMNAS and c['clave'] in por_clave, c['clave']
        assert c['agregar'].strip() not in por_clave[c['clave']][c['campo']], 'ya aplicada'
        por_clave[c['clave']][c['campo']] += c['agregar']
        esperadas[c['clave']] = (c['campo'], por_clave[c['clave']][c['campo']])
    with tempfile.TemporaryDirectory(prefix='judas_correccion_') as carpeta:
        temporal = Path(carpeta)
        anterior = generar(temporal, 'base', base, mapa_base)
        posterior = generar(temporal, 'corregido', corregido, mapa_base)
    assert anterior.keys() == posterior.keys()
    for nombre in anterior:
        if nombre != 'afirmaciones':
            assert anterior[nombre] == posterior[nombre], nombre
    filas_a, filas_p = anterior['afirmaciones'], posterior['afirmaciones']
    assert len(filas_a) == len(filas_p)
    cambiadas = []
    for vieja, nueva in zip(filas_a, filas_p):
        if vieja != nueva:
            diferentes = [i for i, (a, b) in enumerate(zip(vieja, nueva)) if a != b]
            cambiadas.append((nueva, diferentes))
    assert len(cambiadas) == len(esperadas)
    for fila, diferentes in cambiadas:
        coincidencias = [clave for clave, (campo, valor) in esperadas.items()
                         if valor in fila and diferentes == [1 + COLUMNAS.index(campo)]]
        assert len(coincidencias) == 1, (fila[0], diferentes)
    despues = {str(r.relative_to(RAIZ)).replace('\\', '/'): huella(r) for r in protegidos}
    assert antes == despues, 'Algún archivo compartido cambió durante la comprobación.'
    resultado = {
        'alcance': 'Corrección validada en bases temporales; no integrada en el registro central.',
        'filas': len(filas_p),
        'filas_cambiadas': len(cambiadas),
        'claves': sorted(esperadas),
        'otras_tablas_identicas': True,
        'protegidos_sha256': antes,
        'propuesta_sha256': huella(args.propuesta),
        'generador_sha256': huella(RAIZ / 'guardarafirmaciones.py'),
        'verificador_sha256': huella(Path(__file__)),
    }
    guardar(args.salida, resultado)
    print(f"OK: {len(filas_p)} filas; sólo cambian {len(cambiadas)} en el campo fuente; archivos compartidos intactos.")


if __name__ == '__main__':
    main()
