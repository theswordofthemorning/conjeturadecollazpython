"""Auditoría acotada de censos de paridades; no repite sus búsquedas grandes.

Atajo T sobre naturales. Un largo L cuenta las paridades de x_0,...,x_(L-1).
El contraste recorre semillas directamente, sin levantar clases residuales.
Verifica fuentes históricas, testigos, cortes truncados y dominios pequeños.
No certifica de nuevo la exhaustividad de los censos de 36, 50 y 52 bits.
"""

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile


RAIZ = Path(__file__).resolve().parent


def cargar(nombre, ruta):
    especificacion = importlib.util.spec_from_file_location(nombre, ruta)
    modulo = importlib.util.module_from_spec(especificacion)
    especificacion.loader.exec_module(modulo)
    return modulo


def huella(ruta):
    return hashlib.sha256(ruta.read_text(encoding='utf-8').encode('utf-8')).hexdigest()


def longitud(n, corte, prohibidos, ab=False):
    """Primer bit que infringe la regla; devuelve corte si no lo encuentra."""
    palabra = ''
    for k in range(corte):
        bit = str(n % 2)
        palabra += bit
        if (ab and k < 2 and bit != '1') or any(f in palabra for f in prohibidos):
            return k
        n = n // 2 if n % 2 == 0 else (3 * n + 1) // 2
    return corte


def barrido(bits, corte, prohibidos, ab=False):
    minimos = {}
    for n in range(1 if ab else 3, 1 << bits):
        largo = longitud(n, corte, prohibidos, ab)
        for k in range(1, largo + 1):
            minimos.setdefault(k, n)
    return minimos


def cli(nombre, bits, corte, prohibidos=None):
    with tempfile.TemporaryDirectory(prefix='perdices_salidas_') as carpeta:
        salida = Path(carpeta) / 'resultado.json'
        comando = [sys.executable, '-B', '-X', 'utf8', str(RAIZ / nombre),
                   '--bits', str(bits), '--lmax', str(corte), '--salida', str(salida)]
        if nombre != 'medir_salida_ab.py':
            comando += ['--lmax-bruto', '8']
        if prohibidos is not None:
            comando += ['--prohibidos', ','.join(prohibidos)]
        subprocess.run(comando, check=True, capture_output=True, text=True, encoding='utf-8')
        return json.loads(salida.read_text(encoding='utf-8'))


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--bits', type=int, required=True,
                            help='cota del contraste directo, entre 2 y 20')
    analizador.add_argument('--corte', type=int, default=160)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    assert 2 <= args.bits <= 20 and args.corte >= 113
    fuentes = ['medir_salida_ab.py', 'medir_salida_sin00.py', 'medir_prohibidos.py']
    modulos = [cargar(f'actual_{i}', RAIZ / f) for i, f in enumerate(fuentes)]
    casos = [(['00', '010'], True, 0), (['00'], False, 1),
             (['00', '111'], False, 2), (['0', '1'], False, 2),
             (['11'], False, 2), (['1'], False, 2)]
    cotejos = 0
    for prohibidos, ab, indice in casos:
        for bits in range(1, min(args.bits, 10) + 1):
            referencia = barrido(bits, args.corte, prohibidos, ab)
            for corte in (0, 1, 2, 3, 8, 32, args.corte):
                parametros = (bits, corte, prohibidos) if indice == 2 else (bits, corte)
                calculado, _ = modulos[indice].medir(*parametros)
                esperado = {k: n for k, n in referencia.items() if k <= corte}
                assert calculado == esperado, (fuentes[indice], prohibidos, bits, corte)
                cotejos += 1
    informes_cli = []
    for indice, prohibidos, ab in [(0, ['00', '010'], True),
                                  (1, ['00'], False), (2, ['00', '111'], False),
                                  (2, ['11'], False), (2, ['0', '1'], False)]:
        for bits, corte in [(1, 0), (2, 1), (8, 0), (8, 1), (8, args.corte)]:
            datos = cli(fuentes[indice], bits, corte, prohibidos if indice == 2 else None)
            vacio = not ab and (1 << bits) <= 3
            referencia = barrido(bits, corte, prohibidos, ab)
            maximo = max(referencia, default=0)
            truncado = not vacio and maximo == corte
            assert datos['truncado'] == truncado
            assert datos['largo_maximo_bajo_la_cota'] == (
                None if truncado or vacio else maximo)
            assert datos['primer_largo_sin_supervivientes'] == (
                None if truncado else (0 if vacio else maximo + 1))
            if truncado:
                assert 'no se certifica' in datos['alcance']
            if ab:
                assert datos['cota_tres_log2'] == (None if truncado else True)
            informes_cli.append(dict(fuente=fuentes[indice], prohibidos=prohibidos,
                                     bits=bits, corte=corte, truncado=truncado,
                                     dominio_vacio=vacio))
    censos = []
    archivos = ['medicion_salida_ab.json', 'medicion_salida_sin00.json',
                'medicion_yah_5_7.json']
    for indice, archivo in enumerate(archivos):
        datos = json.loads((RAIZ / archivo).read_text(encoding='utf-8'))
        fuente = RAIZ / 'fuentes_salidas_20261011' / fuentes[indice]
        assert huella(fuente) == datos['sha256_fuente_lf']
        prohibidos, ab, _ = casos[indice]
        filas = {f['largo']: int(f['minimo']) for f in datos['filas']}
        assert max(filas) == datos['largo_maximo_bajo_la_cota'] < datos['parametros']['lmax']
        assert all(a <= b for a, b in zip(filas.values(), list(filas.values())[1:]))
        for largo, n in filas.items():
            assert (1 if ab else 3) <= n < 1 << datos['parametros']['bits']
            assert longitud(n, largo, prohibidos, ab) == largo, (archivo, largo, n)
            if ab:
                assert n ** 3 >= 1 << (largo - 1)
        maximo = max(filas)
        assert longitud(filas[maximo], maximo + 1, prohibidos, ab) == maximo
        referencia = barrido(args.bits, args.corte, prohibidos, ab)
        faltantes = {k: n for k, n in referencia.items() if k not in filas}
        # Los originales sin00 y prohibidos omitían el prefijo de un paso.
        assert faltantes == ({} if ab else {1: 3}), (archivo, faltantes)
        assert all(filas[k] == n for k, n in referencia.items() if k in filas)
        assert {k: n for k, n in filas.items() if n < 1 << args.bits} == {
            k: n for k, n in referencia.items() if k in filas}
        original = cargar(f'historico_{indice}', fuente)
        parametros = (args.bits, args.corte, prohibidos) if indice == 2 else (args.bits, args.corte)
        antigua, _ = original.medir(*parametros)
        nueva, _ = modulos[indice].medir(*parametros)
        assert nueva == referencia
        assert antigua == {k: n for k, n in referencia.items() if k not in faltantes}
        censos.append(dict(archivo=archivo, sha256_json=huella(RAIZ / archivo),
                           fuente_historica=str(fuente.relative_to(RAIZ)).replace('\\', '/'),
                           sha256_fuente_lf=huella(fuente), testigos=len(filas),
                           filas_omitidas_en_original=faltantes,
                           contraste_directo_hasta_exclusivo=1 << args.bits,
                           largo_maximo=maximo, semilla_record=str(filas[maximo]),
                           nodos_historicos=datos['nodos_visitados']))
    # La búsqueda por niveles de 36 bits debe coincidir con la de profundidad de 50.
    anterior = json.loads((RAIZ / 'cotejo_complejidad.json').read_text(encoding='utf-8'))
    tablas = []
    def recoger(objeto):
        if isinstance(objeto, dict):
            if 'filas' in objeto and objeto['filas'] and 'clases_bajo_la_cota' in objeto['filas'][0]:
                tablas.append(objeto['filas'])
            for valor in objeto.values():
                recoger(valor)
        elif isinstance(objeto, list):
            for valor in objeto:
                recoger(valor)
    recoger(anterior)
    assert len(tablas) == 1
    filas_ab = json.loads((RAIZ / archivos[0]).read_text(encoding='utf-8'))['filas']
    extendida = {f['largo']: int(f['minimo']) for f in filas_ab}
    for fila in tablas[0]:
        if fila['minimo'] is None:
            assert extendida[fila['largo']] >= 1 << anterior['parametros']['cota_bits_ab']
        else:
            assert extendida[fila['largo']] == int(fila['minimo'])
    resultado = dict(parametros=vars(args) | {'salida': str(args.salida)},
                     cotejos_dominio_y_horizonte=cotejos, controles_cli=informes_cli,
                     censos=censos, filas_solapadas_bfs_dfs=len(tablas[0]),
                     fuentes_actuales={f: huella(RAIZ / f) for f in fuentes},
                     sha256_auditor_lf=huella(Path(__file__)),
                     alcance='Contraste independiente acotado, huellas y testigos. '
                     'Los censos grandes se conservan; no se vuelven a enumerar.')
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'OK: {cotejos} cotejos, {len(informes_cli)} controles CLI y tres censos auditados.')


if __name__ == '__main__':
    main()
