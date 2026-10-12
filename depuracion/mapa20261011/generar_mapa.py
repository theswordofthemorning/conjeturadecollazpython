"""Genera los dos mapas sin red ni inferencias por nombre de fichero."""

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import sqlite3
from urllib.parse import quote

RAIZ = Path(__file__).resolve().parents[2]
# cytoscape 3.30.2, dagre 0.8.5 y cytoscape-dagre 2.5.0, copiados de jsdelivr.
LIBRERIAS = ('cytoscape.min.js', 'dagre.min.js', 'cytoscape-dagre.js')


def leer(base, salida):
    conexion = sqlite3.connect(Path(base).resolve().as_uri() + '?mode=ro', uri=True)
    conexion.row_factory = sqlite3.Row

    def tabla(nombre):
        return [dict(f) for f in conexion.execute('SELECT * FROM ' + nombre + ' ORDER BY rowid')]

    try:
        datos = {r['clave']: json.loads(r['valor']) for r in tabla('mapa_config')}
        for nombre in ('ramas', 'piezas', 'relaciones', 'inventario'):
            datos[nombre] = tabla('mapa_' + nombre)
        datos['afirmaciones'] = tabla('afirmaciones')
        datos['correcciones'] = tabla('correcciones')
        datos['nodos_previos'] = tabla('nodos')
        asignaciones = tabla('mapa_afirmaciones')
        nodos = tabla('mapa_nodos')
    except sqlite3.OperationalError as error:
        raise ValueError('Regenerar primero afirmaciones.db con guardarafirmaciones.py') from error
    finally:
        conexion.close()
    for nombre in ('piezas', 'relaciones', 'inventario'):
        for fila in datos[nombre]:
            for campo in ('fuentes', 'alias', 'nodos_originales'):
                if campo in fila:
                    fila[campo] = json.loads(fila[campo])
    piezas = {p['id']: p for p in datos['piezas']}
    afirmaciones = {a['id']: a for a in datos['afirmaciones']}
    for p in piezas.values():
        p['afirmaciones'], p['nodos'] = [], []
    for fila in asignaciones:
        piezas[fila['pieza']]['afirmaciones'].append(fila['afirmacion_id'])
        afirmaciones[fila['afirmacion_id']].update(pieza=fila['pieza'], referencia=fila['referencia'])
    for fila in nodos:
        piezas[fila['pieza']]['nodos'].append(fila['nodo'])
    anteriores = {n['nombre']: n for n in datos['nodos_previos']}
    for p in piezas.values():
        p['conteo'] = dict(Counter(afirmaciones[i]['estado'] for i in p['afirmaciones']))
        p['estados_nodos'] = {n: anteriores[n]['estado'] for n in p['nodos']}
    fuentes = set(datos['fuentes_inventario'])
    for lista in ('piezas', 'relaciones', 'inventario'):
        for fila in datos[lista]:
            fuentes.update(fila['fuentes'])
    fuentes.update(a['fichero'] for a in datos['afirmaciones'] if a['fichero'])
    fuentes.update(e['fuente'] for e in datos['recorrido'])
    datos['enlaces'] = {}
    for fuente in sorted(fuentes):
        ruta, separador, ancla = fuente.partition('#')
        relativo = Path(os.path.relpath(RAIZ / ruta, salida)).as_posix()
        datos['enlaces'][fuente] = quote(relativo, safe='/') + (separador + ancla if separador else '')
    datos['conteo'] = dict(Counter(a['estado'] for a in datos['afirmaciones']))
    datos['huella_base'] = hashlib.sha256(Path(base).read_bytes()).hexdigest()
    return datos


def generar(base, salida):
    salida = Path(salida).resolve()
    salida.mkdir(parents=True, exist_ok=True)
    datos = leer(base, salida)
    plantilla = Path(__file__).with_name('plantilla_flujo.html').read_text(encoding='utf-8')
    # Las librerías de dibujo van incrustadas para que el mapa funcione sin conexión.
    librerias = '\n'.join((Path(__file__).with_name('vendor') / nombre).read_text(encoding='utf-8')
                          for nombre in LIBRERIAS)
    plantilla = plantilla.replace('__LIBRERIAS__', librerias)
    contenido = json.dumps(datos, ensure_ascii=False, separators=(',', ':'))
    contenido = contenido.replace('&', '\\u0026').replace('<', '\\u003c')
    contenido = contenido.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    for modo, nombre in (('basic', 'MapaDependenciasBasic.html'), ('complex', 'MapaDependenciasComplex.html')):
        html = plantilla.replace('__MODO__', modo).replace('__DATOS__', contenido)
        (salida / nombre).write_text(html, encoding='utf-8', newline='\n')
    print(f"Mapas: {len(datos['inventario'])} nombres, {len(datos['piezas'])} piezas, "
          f"{len(datos['afirmaciones'])} afirmaciones y {len(datos['relaciones'])} relaciones documentadas.")
    print('Todas las piezas pertenecen a una rama. Uso local sin conexión.')
    return datos


def main():
    argumentos = argparse.ArgumentParser(description=__doc__)
    argumentos.add_argument('--base', type=Path, default=RAIZ / 'afirmaciones.db')
    argumentos.add_argument('--salida', type=Path, default=Path(__file__).resolve().parent)
    opciones = argumentos.parse_args()
    generar(opciones.base, opciones.salida)


if __name__ == '__main__':
    main()
