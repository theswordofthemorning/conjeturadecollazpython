"""Aplica correcciones literales y escribe un catálogo SQLite de forma atómica."""

import hashlib
import json
import os
from pathlib import Path
import sqlite3
import tempfile

CAMPOS = ('enunciado', 'cuantificador', 'estado', 'fichero', 'fuente', 'notas')


def aplicar_registro(afirmaciones, correcciones, nodos, dependencias, archivo):
    registro = json.loads(Path(archivo).read_text(encoding='utf-8'))
    huella = hashlib.sha256(json.dumps(
        afirmaciones, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
    if len(afirmaciones) != registro['base_filas'] or huella != registro['huella_base']:
        raise ValueError('La fuente histórica cambió: migrar el registro antes de regenerar.')
    filas = list(afirmaciones)
    usados = set()
    for cambio in registro['correcciones_afirmaciones']:
        indice = cambio['id'] - 1
        if indice in usados or filas[indice] != tuple(cambio['antes'][c] for c in CAMPOS):
            raise ValueError('Corrección duplicada o sin coincidencia literal: %s' % cambio['id'])
        usados.add(indice)
        filas[indice] = tuple(cambio['despues'][c] for c in CAMPOS)
    claves = []
    for alta in registro['altas']:
        filas.append(tuple(alta[c] for c in CAMPOS))
        claves.append((alta['clave'], len(filas)))
    if len({c[0] for c in claves}) != len(claves):
        raise ValueError('Claves actuales duplicadas')
    mapa = {n[0]: tuple(n) for n in nodos}
    for cambio in registro['nodos']:
        antes = tuple(cambio['antes']) if cambio['antes'] is not None else None
        if mapa.get(cambio['nombre']) != antes:
            raise ValueError('Nodo histórico distinto: ' + cambio['nombre'])
        mapa[cambio['nombre']] = tuple(cambio['despues'])
    aristas = list(dependencias) + [tuple(x) for x in registro['dependencias_nuevas']]
    if len(set(aristas)) != len(aristas):
        raise ValueError('Dependencias duplicadas')
    nuevas_corr = list(correcciones) + [tuple(x) for x in registro['correcciones_nuevas']]
    return filas, nuevas_corr, list(mapa.values()), aristas, claves, registro['version']


def guardar_base(ruta, esquema, tablas):
    """Valida todas las filas y relaciones antes de reemplazar la base anterior.

    tablas: mapa de tabla a (nombres de columnas, filas). El orden de filas
    es significativo para conservar los IDs de afirmaciones y correcciones.
    Un fallo conserva intacto el archivo anterior y elimina sólo el temporal.
    """
    ruta = Path(ruta).resolve()
    descriptor, temporal = tempfile.mkstemp(prefix=ruta.stem + '_', suffix='.tmp', dir=ruta.parent)
    os.close(descriptor)
    try:
        with sqlite3.connect(temporal) as conexion:
            conexion.execute('PRAGMA foreign_keys=ON')
            conexion.executescript(esquema)
            for tabla, (columnas, filas) in tablas.items():
                nombres = ','.join(columnas)
                marcas = ','.join('?' for _ in columnas)
                conexion.executemany(f'INSERT INTO {tabla} ({nombres}) VALUES ({marcas})', filas)
            conexion.commit()
        conexion.close()
        with sqlite3.connect(temporal) as revision:
            if revision.execute('PRAGMA integrity_check').fetchall() != [('ok',)]:
                raise ValueError('SQLite no supera integrity_check')
            if revision.execute('PRAGMA foreign_key_check').fetchall():
                raise ValueError('Referencias SQLite inválidas')
            for tabla, (columnas, filas) in tablas.items():
                leidas = revision.execute(
                    f"SELECT {','.join(columnas)} FROM {tabla} ORDER BY rowid").fetchall()
                if leidas != [tuple(f) for f in filas]:
                    raise ValueError('Ida y vuelta distinta en ' + tabla)
        revision.close()
        os.replace(temporal, ruta)
    finally:
        # Las conexiones deben cerrarse también si hay excepciones en Windows.
        if 'conexion' in locals():
            conexion.close()
        if 'revision' in locals():
            revision.close()
        if os.path.exists(temporal):
            os.remove(temporal)
