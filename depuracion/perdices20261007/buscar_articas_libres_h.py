"""Órdenes árticos sin cota de pesos, mediante aritmética lineal entera.

Internamente -1 representa menos infinito y los enteros >=0 pesos finitos.
No hay productos entre incógnitas: se usa QF_LIA con máximos y condicionales.
Los certificados exportados usan la convención anterior (0=menos infinito).
"""

import argparse
import json
from pathlib import Path
import time

import z3

from buscar_matrices_h import huella
from verificar_matrices_h import comprobar


def componer_lineal(izquierda, derecha):
    matriz, vector = izquierda
    otra, constante = derecha
    dimension = len(vector)

    def producto(a, b):
        return z3.If(z3.Or(a == -1, b == -1), -1, a + b)

    def maximo(valores):
        resultado = valores[0]
        for valor in valores[1:]:
            resultado = z3.If(resultado >= valor, resultado, valor)
        return resultado

    nueva = [[maximo([producto(matriz[i][k], otra[k][j])
                      for k in range(dimension)]) for j in range(dimension)]
             for i in range(dimension)]
    nuevo = [maximo([vector[i]] + [producto(matriz[i][k], constante[k])
                                  for k in range(dimension)])
             for i in range(dimension)]
    return nueva, nuevo


def codificar(reglas, dimension):
    alfabeto = sorted({letra for regla in reglas
                       for lado in ('izquierda', 'derecha') for letra in regla[lado]})
    simbolos = {letra: ([[z3.Int(f'm_{letra}_{i}_{j}') for j in range(dimension)]
                         for i in range(dimension)],
                        [z3.Int(f'v_{letra}_{i}') for i in range(dimension)])
                for letra in alfabeto}
    grupos = {}
    for letra, (matriz, vector) in simbolos.items():
        grupos[f'dominio_{letra}'] = z3.And(
            [valor >= -1 for valor in sum(matriz, []) + vector] +
            [z3.Or(matriz[0][0] >= 0, vector[0] >= 0)])
    prefijos = dict(simbolos)

    def interpretar(palabra):
        if palabra not in prefijos:
            prefijos[palabra] = componer_lineal(interpretar(palabra[:-1]),
                                                simbolos[palabra[-1]])
        return prefijos[palabra]

    estrictas = {}
    for indice, regla in enumerate(reglas):
        lm, lv = interpretar(regla['izquierda'])
        rm, rv = interpretar(regla['derecha'])
        pares = list(zip(sum(lm, []) + lv, sum(rm, []) + rv))
        grupos[f'regla_{indice}'] = z3.And([a >= b for a, b in pares])
        if regla['estricta']:
            assert regla['en_cabeza']
            estrictas[indice] = z3.And([z3.Or(a > b, z3.And(a == -1, b == -1))
                                       for a, b in pares])
    grupos['alguna_estricta'] = z3.Or(list(estrictas.values()))
    return dict(simbolos=simbolos, grupos=grupos, estrictas=estrictas, prefijos=prefijos)


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--sistema-guardado', type=Path, required=True)
    analizador.add_argument('--dimension', type=int, required=True)
    analizador.add_argument('--segundos', type=int, required=True)
    analizador.add_argument('--semilla', type=int, default=0)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    assert 1 <= args.dimension <= 8 and args.segundos >= 1
    origen = json.loads(args.sistema_guardado.read_text(encoding='utf-8'))
    texto = origen['reglas_originales']
    reglas = []
    for linea in texto.splitlines():
        estricta = ' ->| ' in linea
        izquierda, derecha = linea.split(' ->| ' if estricta else ' ->= ')
        reglas.append(dict(izquierda=izquierda[::-1], derecha=derecha[::-1],
                           estricta=estricta, en_cabeza=estricta))
    codigo = codificar(reglas, args.dimension)
    solver = z3.SolverFor('QF_LIA')
    solver.set(timeout=args.segundos * 1000, random_seed=args.semilla, threads=1)
    for nombre, condicion in codigo['grupos'].items():
        solver.assert_and_track(condicion, nombre)
    formula = args.salida.with_suffix('.smt2')
    formula.write_text(solver.sexpr() + '\n(check-sat-assuming (' +
                       ' '.join(codigo['grupos']) + '))\n', encoding='utf-8')
    inicio = time.monotonic()
    estado = solver.check()
    resultado = dict(parametros={k: str(v) if isinstance(v, Path) else v
                                for k, v in vars(args).items()},
                     version_z3=z3.get_version_string(), reglas_originales=texto,
                     estado=str(estado), segundos=round(time.monotonic() - inicio, 3),
                     dominio='menos infinito o entero no negativo, sin cota superior',
                     logica='QF_LIA',
                     fuentes={p.name: huella(p) for p in
                              [Path(__file__), args.sistema_guardado, formula,
                               Path(__file__).with_name('verificar_matrices_h.py')]},
                     alcance='SAT se coteja con enteros independientes. UNSAT sin '
                     'certificado formal; un núcleo no es una prueba independiente. '
                     'Sin conclusión sobre otras dimensiones ni terminación de H.')
    if estado == z3.sat:
        modelo = solver.model()
        assert all(z3.is_true(modelo.eval(c, model_completion=True))
                   for c in codigo['grupos'].values())
        valor = lambda x: modelo.eval(x, model_completion=True).as_long() + 1
        simbolos = {letra: dict(matriz=[[valor(x) for x in fila] for fila in matriz],
                                 vector=[valor(x) for x in vector])
                    for letra, (matriz, vector) in codigo['simbolos'].items()}
        eliminadas = [i for i, c in codigo['estrictas'].items() if z3.is_true(modelo.eval(c))]
        certificado = dict(interpretacion='arctic', dimension=args.dimension,
                           simbolos=simbolos, reglas=reglas, eliminadas=eliminadas)
        assert comprobar(certificado) == eliminadas
        resultado['certificado'] = certificado
    elif estado == z3.unsat:
        resultado['nucleo'] = [str(c) for c in solver.unsat_core()]
    else:
        resultado['motivo'] = solver.reason_unknown()
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{estado}: {resultado["segundos"]}s', flush=True)


if __name__ == '__main__':
    main()
