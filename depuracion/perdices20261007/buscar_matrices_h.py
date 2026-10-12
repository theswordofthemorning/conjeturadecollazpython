"""Busca interpretaciones matriciales del sistema que evita 5 y 7 módulo 8.

Usa sin modificar el codificador publicado de Yolcu–Aaronson–Heule, fijado a
un commit, y Z3 como solucionador SAT. Verifica cada modelo contra todas las
cláusulas y cada matriz con un verificador entero independiente. UNSAT afecta
sólo a la codificación acotada; unknown no prueba imposibilidad.
"""

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from types import SimpleNamespace

from verificar_matrices_h import comprobar, comprobar_ejecucion, interpretar


REVISION = '8a4dfda60f97a6d33ff0a24fdfa7a172d4bec340'


def huella(ruta):
    return hashlib.sha256(ruta.read_text(encoding='utf-8').encode('utf-8')).hexdigest()


def datos_regla(regla):
    return dict(izquierda=''.join(regla.left), derecha=''.join(regla.right),
                estricta=regla.strict, en_cabeza=regla.top)


def afine(palabra):
    a, b = 1, 0
    digitos = {'a': (2, 0), 'b': (2, 1), 'e': (3, 0), 'f': (3, 1), 'g': (3, 2)}
    for c in palabra:
        if c == 'c':
            a, b = 0, 1
        elif c != 'd':
            m, v = digitos[c]
            a, b = m * a, m * b + v
    return a, b


def preparar_sistema(externa, sistema):
    lineas = (externa / 'rules/collatz-T-odd-mod8.srs').read_text(encoding='utf-8').splitlines()
    residuos = {'aabd': 1, 'abbd': 3, 'babd': 5, 'bbbd': 7}
    excluidos = {1, 5} if sistema == 'control15' else {5, 7}
    seleccionadas = []
    verificadas = 0
    for linea in lineas:
        izquierda, derecha = linea.split(' -> ')
        l, r = afine(izquierda), afine(derecha)
        dinamica = izquierda == 'ad' or izquierda in residuos
        if dinamica:
            if izquierda == 'ad':
                assert l == (2, 0) and r == (1, 0)
            else:
                assert l == (8, residuos[izquierda])
                assert r == (12, (3 * residuos[izquierda] + 1) // 2)
        else:
            assert l == r
        verificadas += 1
        if izquierda in residuos and residuos[izquierda] in excluidos:
            continue
        seleccionadas.append(izquierda + (' ->| ' if dinamica else ' ->= ') + derecha)
    texto = '\n'.join(seleccionadas) + '\n'
    if sistema == 'control15':
        assert texto == (externa / 'relative/collatz-T-1or5mod8.srs').read_text(encoding='utf-8')
    return texto, verificadas


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--fuente-externa', type=Path, required=True)
    analizador.add_argument('--sistema', choices=['control15', 'objetivo57'], required=True)
    analizador.add_argument('--interpretacion', choices=['natural', 'arctic'], required=True)
    analizador.add_argument('--dimension', type=int, required=True)
    analizador.add_argument('--cota', type=int, required=True,
                            help='máximo codificado: natural 0..cota; ártico -infinito y 0..cota-1')
    analizador.add_argument('--segundos', type=int, required=True)
    analizador.add_argument('--semilla', type=int, default=0)
    analizador.add_argument('--etapas', type=int, default=3)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    assert 1 <= args.dimension <= 8 and 1 <= args.cota <= 32
    assert args.segundos >= 1 and 1 <= args.etapas <= 3
    externa = args.fuente_externa.resolve()
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=externa,
                                   text=True, encoding='utf-8').strip() == REVISION
    subprocess.run(['git', 'diff', '--exit-code', 'HEAD', '--', 'prover', 'rules', 'relative'],
                   cwd=externa, check=True, capture_output=True)
    fuentes = {p.relative_to(externa).as_posix(): huella(p) for p in sorted((externa / 'prover').glob('*.py'))}
    fuentes['rules/collatz-T-odd-mod8.srs'] = huella(externa / 'rules/collatz-T-odd-mod8.srs')
    texto, semantica = preparar_sistema(externa, args.sistema)
    sys.path.insert(0, str(externa / 'prover'))
    especificacion = importlib.util.spec_from_file_location('codificador_publicado', externa / 'prover/main.py')
    publicado = importlib.util.module_from_spec(especificacion)
    especificacion.loader.exec_module(publicado)
    import z3
    parametros = SimpleNamespace(interpretation=args.interpretacion, dimension=args.dimension,
                                 resultwidth=args.cota, inputwidth=None, negwidth=0,
                                 removeany=True, marktop=None, markbot=None)
    resultado = dict(parametros=vars(args) | {'fuente_externa': str(externa), 'salida': str(args.salida)},
                     revision_externa=REVISION, fuentes_externas=fuentes,
                     version_z3=z3.get_version_string(), reglas_originales=texto,
                     reglas_con_semantica_afin_cotejada=semantica,
                     fuentes_locales={p.name: huella(p) for p in [Path(__file__),
                         Path(__file__).with_name('verificar_matrices_h.py')]},
                     etapas=[], terminacion_relativa_certificada=False,
                     alcance='Búsqueda finita de órdenes sobre palabras. Sólo los certificados SAT '
                     'se cotejan exactamente. No hay Lean de la búsqueda ni certificado UNSAT.')
    with tempfile.TemporaryDirectory(prefix='perdices_srs_') as temporal:
        ruta = Path(temporal) / 'sistema.srs'
        ruta.write_text(texto, encoding='utf-8')
        sistema = publicado.rules.parserules(str(ruta), False)
        assert not sistema.full and sistema.rev
        for numero in range(args.etapas):
            # Orden estable del alfabeto: no depender de PYTHONHASHSEED.
            sistema.symbols = sorted({(x,) for r in sistema.rules for x in r.left + r.right})
            inicio = time.monotonic()
            codificador = publicado.encode(sistema, parametros)
            nv, nc = len(codificador.variables), len(codificador.clauses)
            solver = z3.Tactic('sat').solver()
            solver.set(timeout=args.segundos * 1000, random_seed=args.semilla,
                       phase='always_false', threads=1)
            variables = [None] + [z3.Bool(f'v{i}') for i in range(1, nv + 1)]
            for clausula in codificador.clauses:
                solver.add(z3.Or([variables[l] if l > 0 else z3.Not(variables[-l]) for l in clausula]))
            preparacion = time.monotonic() - inicio
            print(f'Etapa {numero + 1}: {nv} variables, {nc} cláusulas, preparación {preparacion:.2f}s', flush=True)
            comienzo = time.monotonic()
            estado = solver.check()
            etapa = dict(numero=numero + 1, variables=nv, clausulas=nc, estado=str(estado),
                         segundos_preparacion=round(preparacion, 3),
                         segundos_sat=round(time.monotonic() - comienzo, 3))
            resultado['etapas'].append(etapa)
            if estado == z3.sat:
                modelo = solver.model()
                valores = [None] + [z3.is_true(modelo.eval(v, model_completion=True)) for v in variables[1:]]
                assert all(any(valores[abs(l)] == (l > 0) for l in c) for c in codificador.clauses)
                def coeficiente(tipo, simbolo, i, j=None):
                    clave = (tipo, simbolo, i) if j is None else (tipo, simbolo, i, j)
                    bits = [valores[codificador.variables[(*clave, k)]] for k in range(args.cota)]
                    assert bits == sorted(bits, reverse=True)
                    return sum(bits)
                simbolos = {s[0]: dict(matriz=[[coeficiente('M', s, i, j) for j in range(args.dimension)]
                                               for i in range(args.dimension)],
                                         vector=[coeficiente('v', s, i) for i in range(args.dimension)])
                            for s in sistema.symbols}
                certificado = dict(interpretacion=args.interpretacion, dimension=args.dimension,
                                   simbolos=simbolos, reglas=[datos_regla(r) for r in sistema.rules],
                                   eliminadas=[])
                # Selección mediante comparación exacta de interpretaciones completas.
                valores_simbolos = {s: (d['matriz'], d['vector']) for s, d in simbolos.items()}
                for indice, regla in enumerate(certificado['reglas']):
                    lm, lv = interpretar(regla['izquierda'], valores_simbolos, args.interpretacion)
                    rm, rv = interpretar(regla['derecha'], valores_simbolos, args.interpretacion)
                    estricta = lv[0] > rv[0] if args.interpretacion == 'natural' else all(
                        a > b or a == b == 0 for a, b in zip(sum(lm, []) + lv, sum(rm, []) + rv))
                    if estricta and regla['estricta']:
                        certificado['eliminadas'].append(indice)
                eliminadas = comprobar(certificado)
                etapa['certificado'] = certificado
                etapa['modelo_cnf_verificado'] = True
                sistema.rules = [r for i, r in enumerate(sistema.rules) if i not in eliminadas]
                resultado['terminacion_relativa_certificada'] = not any(r.strict for r in sistema.rules)
            elif estado == z3.unknown:
                etapa['motivo'] = solver.reason_unknown()
            comprobar_ejecucion(resultado)
            args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            print(f'  {estado}: {etapa["segundos_sat"]}s; cierre={resultado["terminacion_relativa_certificada"]}', flush=True)
            if estado != z3.sat or resultado['terminacion_relativa_certificada']:
                break


if __name__ == '__main__':
    main()
