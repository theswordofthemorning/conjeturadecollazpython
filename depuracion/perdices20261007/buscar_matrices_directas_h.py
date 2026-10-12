"""Busca órdenes matriciales limitando sólo los coeficientes de cada símbolo.

La aritmética usa vectores de bits con ancho deducido del mayor largo de
palabra. En modelos admisibles no hay desbordamiento. Cada candidato se
comprueba de nuevo con enteros Python en verificar_matrices_h.py.
"""

import argparse
import json
from pathlib import Path
import subprocess
import time

import z3

from buscar_matrices_h import REVISION, huella, preparar_sistema
from verificar_matrices_h import comprobar, comprobar_ejecucion


def invertir_reglas(texto):
    reglas = []
    for linea in texto.splitlines():
        estricta = ' ->| ' in linea
        izquierda, derecha = linea.split(' ->| ' if estricta else ' ->= ')
        reglas.append(dict(izquierda=izquierda[::-1], derecha=derecha[::-1],
                           estricta=estricta, en_cabeza=estricta))
    return reglas


def cota_intermedia(tipo, dimension, cota, largo):
    assert tipo in ('natural', 'arctic')
    assert dimension >= 1 and cota >= 1 and largo >= 1
    if tipo == 'natural':
        return ((dimension + 1) * cota) ** largo
    return largo * (cota - 1) + 1


def componer_bits(izquierda, derecha, tipo):
    matriz, vector = izquierda
    otra, constante = derecha
    dimension = len(vector)
    if tipo == 'natural':
        producto = lambda a, b: a * b
        suma = lambda valores: sum(valores[1:], valores[0])
        sumar = lambda a, b: a + b
    else:
        producto = lambda a, b: z3.If(z3.Or(a == 0, b == 0), 0, a + b - 1)
        def sumar(a, b):
            return z3.If(z3.UGE(a, b), a, b)
        def suma(valores):
            resultado = valores[0]
            for valor in valores[1:]:
                resultado = sumar(resultado, valor)
            return resultado
    nueva = [[suma([producto(matriz[i][k], otra[k][j]) for k in range(dimension)])
              for j in range(dimension)] for i in range(dimension)]
    nuevo = [sumar(suma([producto(matriz[i][k], constante[k])
                         for k in range(dimension)]), vector[i]) for i in range(dimension)]
    return nueva, nuevo


def codificar(reglas, tipo, dimension, cota):
    largo = max(len(r[lado]) for r in reglas for lado in ('izquierda', 'derecha'))
    maximo = cota_intermedia(tipo, dimension, cota, largo)
    ancho = maximo.bit_length()
    alfabeto = sorted({letra for r in reglas for lado in ('izquierda', 'derecha')
                       for letra in r[lado]})
    simbolos = {letra: ([[z3.BitVec(f'm_{letra}_{i}_{j}', ancho)
                         for j in range(dimension)] for i in range(dimension)],
                       [z3.BitVec(f'v_{letra}_{i}', ancho) for i in range(dimension)])
                for letra in alfabeto}
    condiciones = []
    for matriz, vector in simbolos.values():
        condiciones.extend(z3.ULE(valor, cota) for valor in sum(matriz, []) + vector)
        if tipo == 'arctic':
            condiciones.append(z3.Or(matriz[0][0] != 0, vector[0] != 0))
    prefijos = dict(simbolos)
    def interpretar(palabra):
        if palabra not in prefijos:
            prefijos[palabra] = componer_bits(interpretar(palabra[:-1]),
                                               simbolos[palabra[-1]], tipo)
        return prefijos[palabra]
    estrictas = {}
    for indice, regla in enumerate(reglas):
        lm, lv = interpretar(regla['izquierda'])
        rm, rv = interpretar(regla['derecha'])
        pares = list(zip(sum(lm, []) + lv, sum(rm, []) + rv))
        condiciones.extend(z3.UGE(a, b) for a, b in pares)
        if regla['estricta']:
            assert regla['en_cabeza']
            estrictas[indice] = (z3.UGT(lv[0], rv[0]) if tipo == 'natural' else
                z3.And([z3.Or(z3.UGT(a, b), z3.And(a == 0, b == 0)) for a, b in pares]))
    assert estrictas
    condiciones.append(z3.Or(list(estrictas.values())))
    return dict(simbolos=simbolos, condiciones=condiciones, estrictas=estrictas,
                prefijos=prefijos, largo=largo, maximo=maximo, ancho=ancho)


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--fuente-externa', type=Path, required=True)
    analizador.add_argument('--sistema', choices=['control15', 'objetivo57'], required=True)
    analizador.add_argument('--interpretacion', choices=['natural', 'arctic'], required=True)
    analizador.add_argument('--dimension', type=int, required=True)
    analizador.add_argument('--cota', type=int, required=True)
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
    texto, semantica = preparar_sistema(externa, args.sistema)
    reglas = invertir_reglas(texto)
    fuentes = [Path(__file__), Path(__file__).with_name('buscar_matrices_h.py'),
               Path(__file__).with_name('verificar_matrices_h.py')]
    resultado = dict(parametros=vars(args) | {'fuente_externa': str(externa), 'salida': str(args.salida)},
                     revision_externa=REVISION, version_z3=z3.get_version_string(),
                     reglas_originales=texto, reglas_con_semantica_afin_cotejada=semantica,
                     fuentes_locales={p.name: huella(p) for p in fuentes},
                     fuentes_externas={nombre: huella(externa / nombre) for nombre in
                         ['rules/collatz-T-odd-mod8.srs', 'relative/collatz-T-1or5mod8.srs']},
                     codificacion='BitVec sin desbordamiento; cota sólo para símbolos',
                     etapas=[], terminacion_relativa_certificada=False,
                     alcance='Modelos SAT cotejados con enteros independientes. UNSAT sin '
                     'certificado formal; timeout no decide existencia. Sin formalización Lean.')
    for numero in range(args.etapas):
        inicio = time.monotonic()
        codigo = codificar(reglas, args.interpretacion, args.dimension, args.cota)
        solver = z3.SolverFor('QF_BV')
        solver.set(timeout=args.segundos * 1000, random_seed=args.semilla, threads=1)
        solver.add(codigo['condiciones'])
        preparacion = time.monotonic() - inicio
        print(f'Etapa {numero + 1}: ancho {codigo["ancho"]}, cota intermedia '
              f'{codigo["maximo"]}, preparación {preparacion:.2f}s', flush=True)
        comienzo = time.monotonic()
        estado = solver.check()
        etapa = dict(numero=numero + 1, largo_maximo=codigo['largo'],
                     cota_intermedia=codigo['maximo'], ancho_bits=codigo['ancho'],
                     restricciones=len(codigo['condiciones']), estado=str(estado),
                     segundos_preparacion=round(preparacion, 3),
                     segundos_sat=round(time.monotonic() - comienzo, 3))
        resultado['etapas'].append(etapa)
        if estado == z3.sat:
            modelo = solver.model()
            assert all(z3.is_true(modelo.eval(c, model_completion=True)) for c in codigo['condiciones'])
            valor = lambda expresion: modelo.eval(expresion, model_completion=True).as_long()
            simbolos = {letra: dict(matriz=[[valor(x) for x in fila] for fila in matriz],
                                     vector=[valor(x) for x in vector])
                        for letra, (matriz, vector) in codigo['simbolos'].items()}
            eliminadas = [i for i, c in codigo['estrictas'].items() if z3.is_true(modelo.eval(c))]
            certificado = dict(interpretacion=args.interpretacion, dimension=args.dimension,
                               simbolos=simbolos, reglas=reglas, eliminadas=eliminadas)
            assert comprobar(certificado) == eliminadas
            etapa['certificado'] = certificado
            etapa['modelo_bitvec_verificado'] = True
            reglas = [r for i, r in enumerate(reglas) if i not in eliminadas]
            resultado['terminacion_relativa_certificada'] = not any(r['estricta'] for r in reglas)
        elif estado == z3.unknown:
            etapa['motivo'] = solver.reason_unknown()
        comprobar_ejecucion(resultado)
        args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'  {estado}: {etapa["segundos_sat"]}s; cierre={resultado["terminacion_relativa_certificada"]}',
              flush=True)
        if estado != z3.sat or resultado['terminacion_relativa_certificada']:
            break


if __name__ == '__main__':
    main()
