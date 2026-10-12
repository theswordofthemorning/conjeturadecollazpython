"""Auditoría acotada de cobertura, persistencia, fuentes y mapas HTML."""

import argparse
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import sys
import unicodedata
from urllib.parse import unquote

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
from depuracion.coherencia20260913.verificar_registro import fuente_historica
from depuracion.mapa20261011.catalogo import preparar_mapa
from registroafirmaciones import aplicar_registro


def plano(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', texto)
                   if unicodedata.category(c) != 'Mn').lower()


def huella(valor):
    return hashlib.sha256(json.dumps(valor, ensure_ascii=False,
                                    separators=(',', ':')).encode('utf-8')).hexdigest()


def auditar(respaldo=None):
    fuente = fuente_historica()
    registro = RAIZ / 'depuracion/coherencia20260913/registro.json'
    filas, correcciones, nodos, deps, claves, version = aplicar_registro(
        *(fuente[n] for n in ('AFIRMACIONES', 'CORRECCIONES', 'NODOS', 'DEPENDENCIAS')), registro)
    archivo = registro.with_name('mapa_investigacion.json')
    datos = json.loads(archivo.read_text(encoding='utf-8'))
    _, tablas = preparar_mapa(archivo, filas, claves, nodos, deps, RAIZ)
    with sqlite3.connect((RAIZ / 'afirmaciones.db').as_uri() + '?mode=ro', uri=True) as db:
        for tabla, (columnas, esperadas) in tablas.items():
            leidas = db.execute('SELECT ' + ','.join(columnas) + ' FROM ' + tabla + ' ORDER BY rowid').fetchall()
            assert leidas == esperadas, tabla
        assert db.execute('PRAGMA foreign_key_check').fetchall() == []
        assert db.execute('PRAGMA integrity_check').fetchone() == ('ok',)
        assert db.execute('SELECT count(*) FROM mapa_afirmaciones').fetchone()[0] == len(filas)
        conservacion = {}
        if respaldo:
            with sqlite3.connect((Path(respaldo) / 'afirmaciones.db').as_uri() + '?mode=ro', uri=True) as antes:
                for tabla in ('afirmaciones', 'correcciones', 'constantes', 'claves_actuales', 'dependencias'):
                    viejas = antes.execute('SELECT * FROM ' + tabla + ' ORDER BY rowid').fetchall()
                    nuevas = db.execute('SELECT * FROM ' + tabla + ' ORDER BY rowid').fetchall()
                    assert viejas == nuevas, 'Cambió el contenido de ' + tabla
                    conservacion[tabla] = {'filas': len(nuevas), 'sha256_filas': huella(nuevas)}
                previos = dict((n, (e, d)) for n, e, d in antes.execute('SELECT * FROM nodos'))
                actuales = dict((n, (e, d)) for n, e, d in db.execute('SELECT * FROM nodos'))
                cambios = sorted(n for n in actuales if previos[n] != actuales[n])
                assert cambios == ['aranas_sombra', 'cebras_lyapunov', 'ocelotas'], cambios
                conservacion['nodos_corregidos'] = cambios
    # Inventario independiente: la tabla conservada y las 68 revisiones en Git.
    historico = (RAIZ / 'archivo/contexto_20260913/RutaTeoremas.md.txt').read_text(encoding='utf-8').splitlines()
    nombres_historicos = []
    for linea in historico[954:1013]:
        encontrado = re.match(r'\| \*\*(.*?)\*\*', linea)
        if encontrado:
            nombres_historicos.append(encontrado.group(1))
    historia_git = json.loads((Path(__file__).with_name('inventario_git.json')).read_text(encoding='utf-8'))
    nombres = {plano(e['nombre']) for e in datos['inventario']}
    for esperado in nombres_historicos + list(historia_git['nombres']):
        assert plano(esperado) in nombres, 'Animal histórico fuera del arca: ' + esperado
    for esperado in ('Ocelotas', 'Perdices', 'Corzas', 'Chinchillas', 'Jinetas', 'Focas', 'Lurrus', 'Libélulas'):
        assert plano(esperado) in nombres, esperado
    assert len(nombres) == len(datos['inventario'])
    # Toda pieza tiene un camino único de pertenencia hasta una rama y la raíz.
    piezas = {p['id']: p for p in datos['piezas']}
    conectadas = set()
    for pieza in piezas.values():
        actual, vistos = pieza, set()
        while actual.get('padre'):
            assert actual['id'] not in vistos
            vistos.add(actual['id'])
            actual = piezas[actual['padre']]
        assert actual['rama'] in {r['id'] for r in datos['ramas']}
        conectadas.add(pieza['id'])
    # Grafo de usos documentados, sin mezclar procedencia ni condicionamiento.
    padres = {p: set() for p in piezas}
    for r in datos['relaciones']:
        if r['tipo'] in ('usa', 'registrada'):
            padres[r['hasta']].add(r['desde'])
    pendientes = set(piezas)
    while pendientes:
        libres = {p for p in pendientes if not padres[p] & pendientes}
        assert libres, 'Ciclo entre usos: ' + str(sorted(pendientes))
        pendientes -= libres
    paginas = []
    enlaces = set()
    for modo in ('Basic', 'Complex'):
        pagina = Path(__file__).with_name('MapaDependencias' + modo + '.html')
        contenido = pagina.read_text(encoding='utf-8')
        incrustado = re.search(r'<script id="datos-mapa" type="application/json">(.*?)</script>', contenido, re.S)
        assert incrustado
        d = json.loads(incrustado.group(1))
        assert {p['id'] for p in d['piezas']} == set(piezas)
        assert len(d['afirmaciones']) == len(filas)
        assert len(d['inventario']) == len(datos['inventario'])
        assert len(d['correcciones']) == len(correcciones)
        assert d['huella_base'] == hashlib.sha256((RAIZ / 'afirmaciones.db').read_bytes()).hexdigest()
        assert not re.search(r'<script[^>]+src=', contenido), 'Dependencia de red'
        assert '__DATOS__' not in contenido and '__MODO__' not in contenido
        for origen, enlace in d['enlaces'].items():
            assert (pagina.parent / unquote(enlace.split('#')[0])).is_file(), origen
            enlaces.add(origen)
        paginas.append(pagina.name)
    for programa in ('catalogo.py', 'generar_mapa.py', 'verificar_mapa.py', 'verificar_navegacion.py'):
        ast.parse(Path(__file__).with_name(programa).read_text(encoding='utf-8'))
    return {
        'version': version, 'afirmaciones': len(filas), 'correcciones': len(correcciones),
        'nombres': len(nombres), 'animales': sum(bool(p['animal']) for p in piezas.values()),
        'piezas': len(piezas), 'conectadas_a_la_raiz': len(conectadas),
        'ramas': len(datos['ramas']), 'nombres_tabla_historica': len(nombres_historicos),
        'revisiones_git': len(historia_git['revisiones_consultadas']),
        'relaciones': dict(Counter(r['tipo'] for r in datos['relaciones'])),
        'enlaces_locales': len(enlaces), 'paginas': paginas, 'conservacion': conservacion,
        'fuentes': {str(p.relative_to(RAIZ)).replace('\\', '/'): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in (archivo, registro, Path(__file__), Path(__file__).with_name('generar_mapa.py'),
                              Path(__file__).with_name('catalogo.py'), Path(__file__).with_name('plantilla_flujo.html'))},
        'alcance': 'Auditoría de documentación, cobertura y persistencia. No recompila ni vuelve a certificar teoremas; no ejecuta censos históricos.'
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--respaldo', type=Path)
    parser.add_argument('--salida', type=Path, required=True)
    argumentos = parser.parse_args()
    resultado = auditar(argumentos.respaldo)
    argumentos.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('OK:', resultado['nombres'], 'nombres;', resultado['piezas'], 'piezas conectadas;',
          resultado['afirmaciones'], 'afirmaciones;', resultado['enlaces_locales'], 'enlaces.')


if __name__ == '__main__':
    main()
