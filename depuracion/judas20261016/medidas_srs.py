"""Medidas de terminación de los dos fragmentos fáciles del sistema del piloto.

Ruta de Judas, 16-10-2026. En el sistema de srs_piloto.py, una inversión es un
par formado por una cifra binaria (f, t) y una ternaria (a0, a1, a2) situada
más a la derecha, no necesariamente al lado. Las dos medidas se comparan en
orden lexicográfico:

    reglas X:          (cifras ternarias, inversiones)
    fragmento sin L:   (cifras binarias, inversiones)

Si una regla cambia las cifras ternarias en dA y las binarias en dB, al
aplicarla dentro de u izq v las inversiones cambian en
inv(der) - inv(izq) + B(u)*dA + dB*A(v). Con esa cuenta se decide regla por
regla si la medida baja en todo contexto: esa es la prueba. Después se cotejan
contextos y reescrituras al azar, que son sólo una medición finita. También se
comprueba la estructura que usa J2 §2: L sólo va al principio y R sólo al final
de cada lado, ninguna regla crea ni borra L o R, y toda cifra ternaria tiene
una regla X con el símbolo que la precede.
"""

import argparse
import json
from pathlib import Path
import random

from srs_piloto import X, DINAMICAS

BINARIAS = ('f', 't')
TERNARIAS = ('a0', 'a1', 'a2')
SIMBOLOS = ('L', 'R') + BINARIAS + TERNARIAS
PESOS = (1, 2, 4, 4, 1, 1, 1)
FRAGMENTOS = {
    'X': (X, TERNARIAS),
    'sin L': ([regla for regla in X + DINAMICAS if 'L' not in regla[0]], BINARIAS),
}


def cuenta(cadena, clase):
    return sum(1 for s in cadena if s in clase)


def inversiones(cadena):
    total, binarias = 0, 0
    for s in cadena:
        if s in BINARIAS:
            binarias += 1
        elif s in TERNARIAS:
            total += binarias
    return total


def medida(cadena, clase):
    return (cuenta(cadena, clase), inversiones(cadena))


def texto(regla):
    izq, der = regla
    return ' '.join(izq) + ' -> ' + ' '.join(der)


def baja_en_todo_contexto(izq, der, clase):
    """Baja la primera componente, o sólo cambian las inversiones y bajan."""
    dA = cuenta(der, TERNARIAS) - cuenta(izq, TERNARIAS)
    dB = cuenta(der, BINARIAS) - cuenta(izq, BINARIAS)
    primera = dA if clase == TERNARIAS else dB
    if primera < 0:
        return True
    return dA == 0 and dB == 0 and inversiones(der) < inversiones(izq)


def estructura():
    reglas = X + DINAMICAS
    lados = [lado for regla in reglas for lado in regla]
    pares = {(b, a) for b in ('L',) + BINARIAS for a in TERNARIAS}
    return {
        'L_solo_al_principio': all('L' not in lado[1:] for lado in lados),
        'R_solo_al_final': all('R' not in lado[:-1] for lado in lados),
        'conservan_L_y_R': all(izq.count(s) == der.count(s) for izq, der in reglas for s in ('L', 'R')),
        'cobertura_X': pares <= {izq for izq, _ in X},
    }


def cadena_al_azar(azar, largo):
    return tuple(azar.choices(SIMBOLOS, weights=PESOS, k=azar.randint(0, largo)))


def cotejar_contextos(reglas, clase, azar, contextos, largo):
    fallos = 0
    for izq, der in reglas:
        for _ in range(contextos):
            u, v = cadena_al_azar(azar, largo), cadena_al_azar(azar, largo)
            if not medida(u + der + v, clase) < medida(u + izq + v, clase):
                fallos += 1
    return fallos


def reescribir_al_azar(cadena, reglas, clase, azar, tope, usos):
    """Reescribe en un lugar al azar hasta la forma normal; cuenta las veces que la medida no baja."""
    pasos, fallos = 0, 0
    while pasos < tope:
        opciones = [(i, regla) for i in range(len(cadena)) for regla in reglas
                    if cadena[i:i + len(regla[0])] == regla[0]]
        if not opciones:
            return pasos, fallos
        i, (izq, der) = azar.choice(opciones)
        nueva = cadena[:i] + der + cadena[i + len(izq):]
        if not medida(nueva, clase) < medida(cadena, clase):
            fallos += 1
        usos[texto((izq, der))] += 1
        cadena, pasos = nueva, pasos + 1
    raise RuntimeError('tope de pasos')


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--contextos', type=int, default=200)
    parser.add_argument('--cadenas', type=int, default=3000)
    parser.add_argument('--largo', type=int, default=24)
    parser.add_argument('--semilla', type=int, default=20261016)
    parser.add_argument('--tope', type=int, default=100_000)
    parser.add_argument('--salida', default='depuracion/judas20261016/cotejo_medidas.json')
    args = parser.parse_args()
    azar = random.Random(args.semilla)
    resultado = {'fecha': '2026-10-16', 'parametros': vars(args), 'estructura': estructura(),
                 'fragmentos': {}}
    for nombre, (reglas, clase) in FRAGMENTOS.items():
        usos = {texto(regla): 0 for regla in reglas}
        pasos, fallos = 0, 0
        for _ in range(args.cadenas):
            p, f = reescribir_al_azar(cadena_al_azar(azar, args.largo), reglas, clase, azar,
                                      args.tope, usos)
            pasos, fallos = pasos + p, fallos + f
        resultado['fragmentos'][nombre] = {
            'medida': ['cifras ternarias' if clase == TERNARIAS else 'cifras binarias', 'inversiones'],
            'reglas': len(reglas),
            'bajan_en_todo_contexto': [texto(r) for r in reglas if baja_en_todo_contexto(*r, clase)],
            'no_bajan': [texto(r) for r in reglas if not baja_en_todo_contexto(*r, clase)],
            'fallos_contextos_al_azar': cotejar_contextos(reglas, clase, azar, args.contextos,
                                                          args.largo),
            'reescrituras_al_azar': pasos,
            'fallos_reescrituras': fallos,
            'usos_por_regla': usos,
        }
    resultado['prueba_completa'] = (all(resultado['estructura'].values()) and
                                    not any(datos['no_bajan']
                                            for datos in resultado['fragmentos'].values()))
    Path(args.salida).write_text(json.dumps(resultado, ensure_ascii=False, indent=1) + '\n',
                                 encoding='utf-8')
    print(json.dumps({k: v for k, v in resultado.items() if k != 'fragmentos'}, ensure_ascii=False))
    for nombre, datos in resultado['fragmentos'].items():
        print(nombre, '| no bajan:', datos['no_bajan'], '| contextos con fallo:',
              datos['fallos_contextos_al_azar'], '| reescrituras:', datos['reescrituras_al_azar'],
              '| fallos:', datos['fallos_reescrituras'], '| regla menos usada:',
              min(datos['usos_por_regla'].values()))


if __name__ == '__main__':
    main()
