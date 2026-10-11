"""Regresiones de persistencia: fuente histórica, atomicidad y captura literal."""

import ast
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
from unittest.mock import patch

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
from registroafirmaciones import aplicar_registro, guardar_base
from guardarrespuestas import abrir, anotar


def fuente_historica():
    arbol = ast.parse((RAIZ / 'guardarafirmaciones.py').read_text(encoding='utf-8'))
    nombres = {'AFIRMACIONES', 'CORRECCIONES', 'CONSTANTES', 'NODOS', 'DEPENDENCIAS'}
    nodos = [n for n in arbol.body if
             isinstance(n, ast.FunctionDef) and n.name in ('fila', 'cte') or
             isinstance(n, ast.Assign) and len(n.targets) == 1 and
             isinstance(n.targets[0], ast.Name) and n.targets[0].id in nombres]
    espacio = {}
    exec(compile(ast.Module(body=nodos, type_ignores=[]), '<fuente literal>', 'exec'), espacio)
    return espacio


def verificar_catalogo():
    fuente = fuente_historica()
    args = [fuente[n] for n in ('AFIRMACIONES', 'CORRECCIONES', 'NODOS', 'DEPENDENCIAS')]
    archivo = RAIZ / 'depuracion/coherencia20260913/registro.json'
    filas, corr, nodos, deps, claves, version = aplicar_registro(*args, archivo)
    assert len(filas) == 312 and version == '2026-10-10'
    # Una edición accidental de la base antigua no se aplica a IDs desplazados.
    alteradas = list(args[0]); alteradas[0] = ('alterado',) + alteradas[0][1:]
    try:
        aplicar_registro(alteradas, *args[1:], archivo)
    except ValueError:
        pass
    else:
        raise AssertionError('No se detectó una fuente histórica alterada')
    ruta = RAIZ / 'afirmaciones.db'
    with sqlite3.connect(f'file:{ruta.as_posix()}?mode=ro', uri=True) as db:
        assert db.execute('SELECT enunciado,cuantificador,estado,fichero,fuente,notas FROM afirmaciones ORDER BY id').fetchall() == filas
        assert db.execute('SELECT que_se_creia,por_que_era_falsa,leccion FROM correcciones ORDER BY id').fetchall() == corr
        assert db.execute('SELECT nombre,estado,descripcion FROM nodos ORDER BY rowid').fetchall() == nodos
        assert db.execute('SELECT hijo,padre FROM dependencias ORDER BY rowid').fetchall() == deps
        assert db.execute('SELECT clave,afirmacion_id FROM claves_actuales ORDER BY rowid').fetchall() == claves
        assert db.execute('PRAGMA integrity_check').fetchall() == [('ok',)]
    db.close()
    print(f'OK: registro {version}, {len(filas)} afirmaciones, {len(nodos)} nodos, {len(deps)} dependencias.')


def verificar_atomicidad():
    esquema = 'CREATE TABLE datos (valor INTEGER NOT NULL CHECK(valor>0));'
    with tempfile.TemporaryDirectory() as carpeta:
        ruta = Path(carpeta) / 'prueba.db'
        guardar_base(ruta, esquema, {'datos': (('valor',), [(1,)])})
        anterior = ruta.read_bytes()
        for filas, simular in [([(0,)], False), ([(2,)], True)]:
            try:
                if simular:
                    with patch('registroafirmaciones.os.replace', side_effect=OSError('fallo de disco simulado')):
                        guardar_base(ruta, esquema, {'datos': (('valor',), filas)})
                else:
                    guardar_base(ruta, esquema, {'datos': (('valor',), filas)})
            except (sqlite3.IntegrityError, OSError):
                pass
            else:
                raise AssertionError('Se esperaba fallo')
            assert ruta.read_bytes() == anterior
            assert list(Path(carpeta).iterdir()) == [ruta]
        guardar_base(ruta, esquema, {'datos': (('valor',), [(2,)])})
        with sqlite3.connect(ruta) as db:
            assert db.execute('SELECT valor FROM datos').fetchall() == [(2,)]
        db.close()
    print('OK: fallos de validación y reemplazo conservan la base anterior.')


def verificar_captura():
    with tempfile.TemporaryDirectory() as carpeta:
        db = abrir(str(Path(carpeta) / 'respuestas.db'))
        uno = dict(orden=1, fecha_hora='2026-09-13', rol='usuario', texto='literal')
        with db:
            anotar(db, 'prueba', uno)
            anotar(db, 'prueba', uno)
        try:
            with db:
                anotar(db, 'prueba', dict(uno, orden=2))
                anotar(db, 'prueba', dict(uno, texto='otra versión'))
        except ValueError:
            pass
        else:
            raise AssertionError('Se esperaba conflicto literal')
        assert db.execute('SELECT orden,texto FROM respuestasclaude').fetchall() == [(1, 'literal')]
        db.close()
    print('OK: captura repetida no duplica; conflicto revierte todo el lote.')


if __name__ == '__main__':
    verificar_atomicidad()
    verificar_captura()
    verificar_catalogo()
