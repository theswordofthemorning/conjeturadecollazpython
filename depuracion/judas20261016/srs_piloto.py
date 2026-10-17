"""El piloto como sistema de reescritura de cadenas, en el formato de Yolcu-Aaronson-Heule.

Ruta de Judas, 16-10-2026. YAH (arXiv:2105.14697v3, §3.2) escriben un entero
en base mixta binaria-ternaria: f(x)=2x, t(x)=2x+1, 0(x)=3x, 1(x)=3x+1,
2(x)=3x+2; L es la cifra inicial 1 y R el final. Sus reglas X llevan las
cifras ternarias a la izquierda y las convierten en binarias junto a L. Aquí
se añaden las reglas dinámicas de la función parcial del piloto:

    f R   -> 0 R          z par: 3z/2
    t t t R -> 2 2 R      z = 7 mod 8: (9z+1)/8
    L t t R -> L f f f R  z = 7, donde el tercer 1 es L

El sistema termina desde toda cadena si y sólo si G se detiene en todo z>=1
(J2_MECANISMOS §2 y JudasPiloto.lean). El programa comprueba la simulación en
todos los z menores que 2^bits con dos estrategias de reescritura y escribe el
sistema en el formato SRS de la Termination Problem Database. No demuestra
terminación.
"""

import argparse
import json
from pathlib import Path
import random

FUNCIONES = {'f': (2, 0), 't': (2, 1), 'a0': (3, 0), 'a1': (3, 1), 'a2': (3, 2)}

X = [
    (('f', 'a0'), ('a0', 'f')), (('f', 'a1'), ('a0', 't')), (('f', 'a2'), ('a1', 'f')),
    (('t', 'a0'), ('a1', 't')), (('t', 'a1'), ('a2', 'f')), (('t', 'a2'), ('a2', 't')),
    (('L', 'a0'), ('L', 't')), (('L', 'a1'), ('L', 'f', 'f')), (('L', 'a2'), ('L', 'f', 't')),
]
DINAMICAS = [
    (('f', 'R'), ('a0', 'R')),
    (('t', 't', 't', 'R'), ('a2', 'a2', 'R')),
    (('L', 't', 't', 'R'), ('L', 'f', 'f', 'f', 'R')),
]
REGLAS = X + DINAMICAS


def valor(cadena):
    assert cadena[0] == 'L' and cadena[-1] == 'R'
    v = 1
    for s in cadena[1:-1]:
        b, d = FUNCIONES[s]
        v = b * v + d
    return v


def cadena_binaria(z):
    bits = bin(z)[3:]
    return ('L',) + tuple('f' if b == '0' else 't' for b in bits) + ('R',)


def G(z):
    if z % 2 == 0:
        return 3 * z // 2
    if z % 8 == 7:
        return (9 * z + 1) // 8
    return None


def ocurrencias(cadena):
    for i in range(len(cadena)):
        for indice, (izq, der) in enumerate(REGLAS):
            if cadena[i:i + len(izq)] == izq:
                yield i, indice


def reescribir(cadena, estrategia, azar, tope):
    """Aplica reglas hasta forma normal; devuelve los valores tras cada regla dinámica."""
    valores, pasos = [], 0
    while pasos < tope:
        opciones = list(ocurrencias(cadena))
        if not opciones:
            return cadena, valores, pasos
        i, indice = opciones[0] if estrategia == 'izquierda' else azar.choice(opciones)
        izq, der = REGLAS[indice]
        nueva = cadena[:i] + der + cadena[i + len(izq):]
        assert valor(nueva) == (valor(cadena) if indice < len(X) else G(valor(cadena)))
        if indice >= len(X):
            valores.append(valor(nueva))
        cadena, pasos = nueva, pasos + 1
    raise RuntimeError('tope de pasos')


def tpdb():
    lineas = ['(COMMENT Piloto 1/110 de la Ruta de Judas en el formato de Yolcu-Aaronson-Heule;',
              ' termina si y solo si G se detiene en todo z>=1)', '(RULES']
    for izq, der in REGLAS:
        lineas.append('  ' + ' '.join(izq) + ' -> ' + ' '.join(der))
    lineas.append(')')
    return '\n'.join(lineas) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--bits', type=int, default=14)
    parser.add_argument('--semilla', type=int, default=20261016)
    parser.add_argument('--tope', type=int, default=200_000)
    parser.add_argument('--srs', default='depuracion/judas20261016/piloto_yah.srs')
    parser.add_argument('--salida', default='depuracion/judas20261016/cotejo_srs.json')
    args = parser.parse_args()
    azar = random.Random(args.semilla)
    fallos, mas_largo = [], (0, None)
    for z in range(1, 2 ** args.bits):
        orbita, w = [], z
        while (w := G(w)) is not None:
            orbita.append(w)
        for estrategia in ('izquierda', 'azar'):
            final, valores, pasos = reescribir(cadena_binaria(z), estrategia, azar, args.tope)
            if valores != orbita or any(s.startswith('a') for s in final):
                fallos.append([z, estrategia])
            if pasos > mas_largo[0]:
                mas_largo = (pasos, z)
    Path(args.srs).write_text(tpdb(), encoding='utf-8')
    resultado = {
        'fecha': '2026-10-16',
        'parametros': vars(args),
        'reglas': len(REGLAS),
        'semillas': 2 ** args.bits - 1,
        'estrategias': ['izquierda', 'azar'],
        'fallos': fallos[:5],
        'numero_fallos': len(fallos),
        'derivacion_mas_larga': {'pasos': mas_largo[0], 'z': mas_largo[1]},
    }
    Path(args.salida).write_text(json.dumps(resultado, ensure_ascii=False, indent=1) + '\n',
                                 encoding='utf-8')
    print(json.dumps(resultado, ensure_ascii=False))


if __name__ == '__main__':
    main()
