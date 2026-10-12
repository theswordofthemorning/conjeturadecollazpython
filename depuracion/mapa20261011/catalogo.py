"""Valida el catálogo editorial y prepara sus tablas para la escritura atómica."""

import json
from pathlib import Path


ESQUEMA = """
CREATE TABLE mapa_config (clave TEXT PRIMARY KEY, valor TEXT NOT NULL);
CREATE TABLE mapa_ramas (
    id TEXT PRIMARY KEY, titulo TEXT NOT NULL, resumen TEXT NOT NULL,
    limite TEXT NOT NULL, siguiente TEXT NOT NULL
);
CREATE TABLE mapa_piezas (
    id TEXT PRIMARY KEY, titulo TEXT NOT NULL,
    rama TEXT NOT NULL REFERENCES mapa_ramas(id),
    padre TEXT REFERENCES mapa_piezas(id) DEFERRABLE INITIALLY DEFERRED,
    animal TEXT, alias TEXT NOT NULL, resumen TEXT NOT NULL, limite TEXT NOT NULL,
    situacion TEXT NOT NULL, fuentes TEXT NOT NULL
);
CREATE TABLE mapa_afirmaciones (
    afirmacion_id INTEGER PRIMARY KEY REFERENCES afirmaciones(id),
    pieza TEXT NOT NULL REFERENCES mapa_piezas(id), referencia TEXT UNIQUE NOT NULL
);
CREATE TABLE mapa_nodos (
    nodo TEXT PRIMARY KEY REFERENCES nodos(nombre),
    pieza TEXT NOT NULL REFERENCES mapa_piezas(id)
);
CREATE TABLE mapa_relaciones (
    id INTEGER PRIMARY KEY, desde TEXT NOT NULL REFERENCES mapa_piezas(id),
    hasta TEXT NOT NULL REFERENCES mapa_piezas(id), tipo TEXT NOT NULL CHECK
      (tipo IN ('registrada','interna','usa','antecedente','contrasta','condicional')),
    detalle TEXT NOT NULL, fuentes TEXT NOT NULL, nodos_originales TEXT NOT NULL
);
CREATE TABLE mapa_inventario (
    nombre TEXT PRIMARY KEY, pieza TEXT NOT NULL REFERENCES mapa_piezas(id),
    alias_de TEXT, tipo TEXT NOT NULL, alias TEXT NOT NULL, fuentes TEXT NOT NULL
);
"""


def serializar(valor):
    return json.dumps(valor, ensure_ascii=False, separators=(',', ':'))


def preparar_mapa(archivo, afirmaciones, claves, nodos, dependencias, raiz):
    """No infiere pertenencias. Exige cobertura exacta y fuentes locales existentes."""
    datos = json.loads(Path(archivo).read_text(encoding='utf-8'))
    ramas = {r['id']: r for r in datos['ramas']}
    piezas = {p['id']: p for p in datos['piezas']}
    if len(ramas) != len(datos['ramas']) or len(piezas) != len(datos['piezas']):
        raise ValueError('Identificadores duplicados en el mapa')
    referencias = {f'historica:{i}': i for i in range(1, 209)}
    referencias.update(dict(claves))
    asignaciones, enlaces_nodos = [], []
    for pieza in piezas.values():
        if pieza['rama'] not in ramas:
            raise ValueError('Rama inexistente: ' + pieza['id'])
        vistos, actual = set(), pieza
        while actual.get('padre'):
            if actual['id'] in vistos:
                raise ValueError('Ciclo en la pertenencia al árbol')
            vistos.add(actual['id'])
            actual = piezas[actual['padre']]
            if actual['rama'] != pieza['rama']:
                raise ValueError('Padre editorial de otra rama')
        for referencia in pieza['afirmaciones']:
            if referencia not in referencias:
                raise ValueError('Afirmación sin identidad vigente: ' + referencia)
            asignaciones.append((referencias[referencia], pieza['id'], referencia))
        enlaces_nodos.extend((n, pieza['id']) for n in pieza['nodos'])
    if sorted(a[0] for a in asignaciones) != list(range(1, len(afirmaciones) + 1)):
        raise ValueError('Cada afirmación debe tener exactamente una pieza principal')
    if sorted(n[0] for n in enlaces_nodos) != sorted(n[0] for n in nodos):
        raise ValueError('Falta un nodo previo o se asignó dos veces')
    originales = []
    mapa_nodos = dict(enlaces_nodos)
    for relacion in datos['relaciones']:
        if relacion['desde'] not in piezas or relacion['hasta'] not in piezas:
            raise ValueError('Relación con extremo inexistente')
        if not relacion['detalle'] or not relacion['fuentes']:
            raise ValueError('Relación sin explicación o evidencia')
        if relacion.get('nodos_originales'):
            padre, hijo = relacion['nodos_originales']
            originales.append((hijo, padre))
            if (mapa_nodos[padre], mapa_nodos[hijo]) != (relacion['desde'], relacion['hasta']):
                raise ValueError('Una dependencia histórica cambió de extremos')
    if sorted(originales) != sorted(dependencias):
        raise ValueError('No se conservaron todas las dependencias del registro')
    for entrada in datos['inventario']:
        if entrada['pieza'] not in piezas or not entrada['fuentes']:
            raise ValueError('Animal sin pieza o evidencia')
    cubiertas = {e['pieza'] for e in datos['inventario']}
    if any(p['animal'] and p['id'] not in cubiertas for p in piezas.values()):
        raise ValueError('Animal fuera del inventario')
    fuentes = set(datos['fuentes_inventario'])
    for elemento in datos['piezas'] + datos['relaciones'] + datos['inventario']:
        fuentes.update(elemento['fuentes'])
    for etapa in datos['recorrido']:
        fuentes.add(etapa['fuente'])
        if not set(etapa['piezas']) <= piezas.keys():
            raise ValueError('Etapa con pieza inexistente')
    for fuente in fuentes:
        if not (Path(raiz) / fuente.split('#')[0]).is_file():
            raise ValueError('Fuente del mapa inexistente: ' + fuente)
    if datos['actual'] not in piezas:
        raise ValueError('Frente actual inexistente')
    tablas = {
        'mapa_config': (('clave', 'valor'), [(k, serializar(v)) for k, v in datos.items()
                         if k not in ('ramas', 'piezas', 'relaciones', 'inventario')]),
        'mapa_ramas': (('id', 'titulo', 'resumen', 'limite', 'siguiente'),
                       [tuple(r[k] for k in ('id', 'titulo', 'resumen', 'limite', 'siguiente'))
                        for r in datos['ramas']]),
        'mapa_piezas': (('id', 'titulo', 'rama', 'padre', 'animal', 'alias', 'resumen', 'limite', 'situacion', 'fuentes'),
                        [(p['id'], p['titulo'], p['rama'], p.get('padre'), p['animal'],
                          serializar(p['alias']), p['resumen'], p['limite'], p['situacion'],
                          serializar(p['fuentes'])) for p in datos['piezas']]),
        'mapa_afirmaciones': (('afirmacion_id', 'pieza', 'referencia'), sorted(asignaciones)),
        'mapa_nodos': (('nodo', 'pieza'), enlaces_nodos),
        'mapa_relaciones': (('desde', 'hasta', 'tipo', 'detalle', 'fuentes', 'nodos_originales'),
                            [(r['desde'], r['hasta'], r['tipo'], r['detalle'], serializar(r['fuentes']),
                              serializar(r.get('nodos_originales', []))) for r in datos['relaciones']]),
        'mapa_inventario': (('nombre', 'pieza', 'alias_de', 'tipo', 'alias', 'fuentes'),
                            [(e['nombre'], e['pieza'], e.get('alias_de'), e.get('tipo', 'animal'),
                              serializar(e['alias']), serializar(e['fuentes'])) for e in datos['inventario']])
    }
    return ESQUEMA, tablas
