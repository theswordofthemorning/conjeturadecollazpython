"""Cotejo escalar por evaluación de funciones y proyecciones naturales 2x2."""

import argparse
import hashlib
import itertools
import json
from pathlib import Path

from verificar_matrices_h import componer, interpretar


REGLAS = [('da', 'd'), ('dbaa', 'dabe'), ('dbba', 'dbaf'),
          ('ea', 'ae'), ('fa', 'be'), ('ga', 'af'), ('eb', 'bf'),
          ('fb', 'ag'), ('gb', 'bg'), ('ec', 'bc'), ('fc', 'aac'), ('gc', 'bac')]


def evaluar(palabra, simbolos, x):
    for letra in reversed(palabra):
        pendiente, constante = simbolos[letra]
        x = pendiente * x + constante
    return x


def coeficientes(palabra, simbolos):
    cero = evaluar(palabra, simbolos, 0)
    return evaluar(palabra, simbolos, 1) - cero, cero


def orienta(izquierda, derecha, simbolos):
    p, v = coeficientes(izquierda, simbolos)
    q, w = coeficientes(derecha, simbolos)
    return p >= q and v >= w


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--cota', type=int, required=True)
    analizador.add_argument('--sistema-guardado', type=Path, required=True)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    assert 0 <= args.cota <= 3
    origen = json.loads(args.sistema_guardado.read_text(encoding='utf-8'))
    reglas_guardadas = []
    for linea in origen['reglas_originales'].splitlines():
        izquierda, derecha = linea.split(' ->| ' if ' ->| ' in linea else ' ->= ')
        reglas_guardadas.append((izquierda[::-1], derecha[::-1]))
    assert reglas_guardadas == REGLAS
    opciones = list(itertools.product(range(args.cota + 1), repeat=2))
    validas = comparaciones = 0
    casos = dict(b_constante=0, pendiente_ternaria_cero=0, pendiente_comun=0)
    # d.m>0 permite cancelar d en cada desigualdad dinámica; su constante se cancela.
    # d.m=0 vuelve idénticos los tres pares de constantes, sin hipótesis adicional.
    for valores in itertools.product(opciones, repeat=5):
        simbolos = dict(zip('abefg', valores)) | {'d': (1, 0)}
        if not all(orienta(i, j, simbolos) for i, j in REGLAS[:9]):
            continue
        for c in opciones:
            simbolos['c'] = c
            if not all(orienta(i, j, simbolos) for i, j in REGLAS[9:]):
                continue
            validas += 1
            casos['b_constante' if simbolos['b'][0] == 0 else
                  'pendiente_ternaria_cero' if simbolos['f'][0] == 0 else
                  'pendiente_comun'] += 1
            matrices = {letra: ([[m]], [v]) for letra, (m, v) in simbolos.items()}
            for izquierda, derecha in REGLAS:
                for palabra in [izquierda, derecha]:
                    m, v = interpretar(palabra, matrices, 'natural')
                    assert (m[0][0], v[0]) == coeficientes(palabra, simbolos)
                    comparaciones += 1
            assert all(evaluar(i, simbolos, 0) == evaluar(j, simbolos, 0)
                       for i, j in REGLAS[:3])
    proyecciones = 0
    for a in itertools.product(range(2), repeat=5):
        izquierda = ([[a[0], 0], [a[1], a[2]]], [a[3], a[4]])
        for b in itertools.product(range(2), repeat=6):
            derecha = ([[b[0], b[1]], [b[2], b[3]]], [b[4], b[5]])
            matriz, vector = componer(izquierda, derecha, 'natural')
            assert (matriz[0][0], vector[0]) == (a[0] * b[0], a[0] * b[4] + a[3])
            proyecciones += 1
    # Una entrada superior derecha no nula puede alterar la proyección.
    acoplada = ([[0, 1], [0, 0]], [0, 0])
    aporte = ([[0, 0], [1, 0]], [0, 1])
    matriz, vector = componer(acoplada, aporte, 'natural')
    assert (matriz[0][0], vector[0]) == (1, 1)
    fuentes = [Path(__file__), Path(__file__).with_name('verificar_matrices_h.py'),
               Path(__file__).with_name('PerdicesProyeccionesMatrices.lean'), args.sistema_guardado]
    resultado = dict(cota=args.cota, asignaciones_escalares=len(opciones) ** 6,
                     asignaciones_debiles=validas, casos=casos,
                     interpretaciones_comparadas=comparaciones, proyecciones_2x2=proyecciones,
                     testigo_acoplamiento=dict(m00=matriz[0][0], v0=vector[0]),
                     fuentes={p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in fuentes},
                     alcance='Cotejo finito; la obstrucción sin cota tiene prueba escrita y Lean. '
                     'No excluye matrices con acoplamiento ni demuestra terminación de H.')
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in resultado.items() if k != 'fuentes'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
