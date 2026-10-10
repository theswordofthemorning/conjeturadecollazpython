"""Coteja evidencia, fuentes, objetos y conservación del cierre de sexta raíz."""

import argparse
import hashlib
import json
from pathlib import Path
import re


def huella(datos):
    return hashlib.sha256(datos).hexdigest()


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--compilados", type=Path, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    carpeta = Path(__file__).resolve().parent
    raiz = carpeta.parents[1]
    nueva = json.loads((carpeta / 'evidencia_cruce.json').read_text(encoding='utf-8'))
    previa = json.loads((carpeta / 'evidencia_sexta.json').read_text(encoding='utf-8'))
    referencia = carpeta / 'auditoria_cruce.json'
    huellas_previas = (json.loads(referencia.read_text(encoding='utf-8')).get('archivos', {})
                       if referencia.exists() else {})
    historicas = {}

    def validar_fuente(ruta, esperada, historica=False):
        nombre = ruta.relative_to(raiz).as_posix()
        cruda = huella(ruta.read_bytes())
        normalizada = huella(ruta.read_text(encoding='utf-8').encode('utf-8'))
        guardada = huellas_previas.get(nombre, {})
        assert (esperada in (cruda, normalizada) or
                esperada in (guardada.get('sha256_bytes'), guardada.get('sha256_historico'))
                and normalizada == guardada.get('sha256_lf')), nombre
        if historica:
            historicas[nombre] = esperada
    assert nueva['contexto']['version_lean'] == previa['contexto']['version_lean']
    formal = raiz / 'depuracion/gao20260920/formal'
    archivos = {}
    for clave, nombre in [('toolchain', 'lean-toolchain'), ('mathlib', 'lake-manifest.json')]:
        ruta = formal / nombre
        validar_fuente(ruta, nueva['contexto'][clave])
        validar_fuente(ruta, previa['contexto'][clave], True)
        archivos[ruta.relative_to(raiz).as_posix()] = dict(
            sha256_bytes=huella(ruta.read_bytes()),
            sha256_lf=huella(ruta.read_text(encoding='utf-8').encode('utf-8')))
    for nombre in ('comprobar_cruce.py', 'comprobar_sexta.py', 'cotejar_cruce.py', 'cotejar_sexta.py'):
        ruta = carpeta / nombre
        archivos[ruta.relative_to(raiz).as_posix()] = dict(
            sha256_bytes=huella(ruta.read_bytes()),
            sha256_lf=huella(ruta.read_text(encoding='utf-8').encode('utf-8')))
    for etiqueta, evidencia in [('cruce', nueva), ('sexta', previa)]:
        validar_fuente(carpeta / f'comprobar_{etiqueta}.py', evidencia['contexto']['comprobador'], etiqueta == 'sexta')
        cotejo = json.loads((carpeta / f'cotejo_{etiqueta}.json').read_text(encoding='utf-8'))
        validar_fuente(carpeta / f'cotejar_{etiqueta}.py', cotejo['sha256'], etiqueta == 'sexta')
    consultas = 0
    conservados = []
    for nombre, dato in nueva['modulos'].items():
        ruta = raiz / dato['fuente']
        datos = ruta.read_bytes()
        codigo = ruta.read_text(encoding='utf-8')
        validar_fuente(ruta, dato['sha256'])
        assert huella((args.compilados / (nombre + '.olean')).read_bytes()) == dato['objeto'], nombre
        pedidas = re.findall(r'^#print axioms (\S+)', codigo, re.MULTILINE)
        assert sorted(pedidas) == sorted(dato['axiomas']), nombre
        assert all(set(a) <= {'propext', 'Classical.choice', 'Quot.sound'} for a in dato['axiomas'].values())
        for dependencia, objeto in dato['dependencias'].items():
            assert nueva['modulos'][dependencia]['objeto'] == objeto
        consultas += len(pedidas)
        archivos[dato['fuente']] = dict(sha256_bytes=huella(datos),
                                        sha256_lf=huella(codigo.encode('utf-8')))
        if nombre in previa['modulos']:
            anterior = previa['modulos'][nombre]
            validar_fuente(ruta, anterior['sha256'], True)
            assert dato['objeto'] == anterior['objeto'], nombre
            assert dato['axiomas'] == anterior['axiomas'], nombre
            conservados.append(nombre)
    assert len(conservados) == 13 and len(nueva['modulos']) == 14
    assert consultas == nueva['consultas'] == 122
    for nombre, anterior in historicas.items():
        archivos[nombre]['sha256_historico'] = anterior
    resultado = dict(estado='fuentes, objetos, dependencias y consultas coinciden',
                     sha256_auditor=huella(Path(__file__).read_bytes()),
                     sha256_evidencia=huella((carpeta / 'evidencia_cruce.json').read_bytes()),
                     sha256_evidencia_lf=huella((carpeta / 'evidencia_cruce.json').read_text(encoding='utf-8').encode('utf-8')),
                     version_lean=nueva['contexto']['version_lean'],
                     consultas=consultas, modulos_previos_identicos=conservados,
                     archivos=archivos)
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'OK: 14 módulos, {consultas} consultas, 13 objetos previos idénticos; huellas LF registradas.')


if __name__ == '__main__':
    main()
