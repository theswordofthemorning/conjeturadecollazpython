"""Contrasta QF_LIA con composiciones árticas enteras, incluidos pesos grandes."""

import argparse
import itertools
import json
from pathlib import Path

import z3

from buscar_articas_libres_h import codificar, componer_lineal
from buscar_matrices_h import huella
from verificar_matrices_h import comprobar, interpretar


def valor(expresion, sustituciones):
    return z3.simplify(z3.substitute(expresion, sustituciones)).as_long() + 1


def cotejar(simbolos, prefijos, concretos):
    sustituciones = []
    for letra, (matriz, vector) in simbolos.items():
        m, v = concretos[letra]
        sustituciones.extend((x, z3.IntVal(y - 1)) for x, y in
                             zip(sum(matriz, []) + vector, sum(m, []) + v))
    for palabra, (matriz, vector) in prefijos.items():
        obtenido = ([[valor(x, sustituciones) for x in fila] for fila in matriz],
                    [valor(x, sustituciones) for x in vector])
        assert obtenido == interpretar(palabra, concretos, 'arctic'), palabra
    return sustituciones, len(prefijos)


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--controles', type=Path, nargs='+', required=True)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    certificados = prefijos = 0
    for ruta in args.controles:
        datos = json.loads(ruta.read_text(encoding='utf-8'))
        for etapa in datos['etapas']:
            original = etapa['certificado']
            assert original['interpretacion'] == 'arctic'
            codigo = codificar(original['reglas'], original['dimension'])
            for escala in [1, 10000]:
                certificado = json.loads(json.dumps(original))
                escalar = lambda n: 0 if n == 0 else 1 + escala * (n - 1)
                for dato in certificado['simbolos'].values():
                    dato['matriz'] = [[escalar(x) for x in fila] for fila in dato['matriz']]
                    dato['vector'] = [escalar(x) for x in dato['vector']]
                comprobar(certificado)
                concretos = {letra: (dato['matriz'], dato['vector'])
                             for letra, dato in certificado['simbolos'].items()}
                sustituciones, cuenta = cotejar(codigo['simbolos'], codigo['prefijos'], concretos)
                assert all(z3.is_true(z3.simplify(z3.substitute(c, sustituciones)))
                           for c in codigo['grupos'].values())
                estrictas = [i for i, c in codigo['estrictas'].items()
                             if z3.is_true(z3.simplify(z3.substitute(c, sustituciones)))]
                assert estrictas == certificado['eliminadas']
                certificados += 1
                prefijos += cuenta
    simbolos = {c: ([[z3.Int('m_' + c)]], [z3.Int('v_' + c)]) for c in 'ab'}
    expresiones = dict(simbolos)
    for palabra in ['aa', 'ab', 'ba', 'bb', 'aab', 'abb', 'baa', 'bbb']:
        expresiones[palabra] = componer_lineal(expresiones[palabra[:-1]], simbolos[palabra[-1]])
    bordes = 0
    for ma, va, mb, vb in itertools.product([0, 1, 2, 10001], repeat=4):
        _, cuenta = cotejar(simbolos, expresiones, {'a': ([[ma]], [va]), 'b': ([[mb]], [vb])})
        prefijos += cuenta
        bordes += 1
    fuentes = [Path(__file__), Path(__file__).with_name('buscar_articas_libres_h.py'),
               Path(__file__).with_name('verificar_matrices_h.py')] + args.controles
    resultado = dict(version_z3=z3.get_version_string(), certificados=certificados,
                     escalas=[1, 10000], asignaciones_borde=bordes,
                     interpretaciones_comparadas=prefijos,
                     fuentes={p.name: huella(p) for p in fuentes},
                     alcance='Cotejo finito independiente de semántica y modelos conocidos; '
                     'no decide los timeouts ni certifica universalmente el codificador.')
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in resultado.items() if k != 'fuentes'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
