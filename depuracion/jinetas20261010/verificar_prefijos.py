"""Cotejo exacto del intervalo de semillas que sobrevive en todos los prefijos."""

import argparse
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path


def orbita(factor, semilla, longitud):
    valores = [semilla]
    bits = []
    for _ in range(longitud):
        actual = valores[-1]
        impar = actual % 2
        bits.append(impar)
        valores.append((factor * actual + 1) // 2 if impar else actual // 2)
    return tuple(bits), valores


def estados(factor, palabra):
    modulo, potencia, aditivo, techo = 1, 1, 0, None
    salida = [dict(j=0, modulo=1, potencia=1, aditivo=0, residuo=0,
                   minimo=3, techo=None, cantidad=None)]
    for j, impar in enumerate(palabra, 1):
        if impar:
            potencia *= factor
            aditivo = factor * aditivo + modulo
        modulo *= 2
        diferencia = modulo - potencia
        if diferencia > 0:
            nuevo = aditivo // diferencia
            techo = nuevo if techo is None else min(techo, nuevo)
        residuo = (-aditivo * pow(potencia, -1, modulo)) % modulo
        minimo = residuo + modulo * max(0, (3 - residuo + modulo - 1) // modulo)
        cantidad = None if techo is None else max(0, (techo - minimo) // modulo + 1)
        salida.append(dict(j=j, modulo=modulo, potencia=potencia, aditivo=aditivo,
                           residuo=residuo, minimo=minimo, techo=techo, cantidad=cantidad))
    return salida


def cotejar_palabras(longitud_maxima):
    cuentas = dict(palabras=0, semillas=0, intervalos_finitos=0,
                   transiciones=0, primeros_cruces=0)
    for factor in (3, 5):
        for longitud in range(longitud_maxima + 1):
            modulo = 2 ** longitud
            # Camino independiente: el mapa construye la tabla, sin B ni inversas.
            tabla = {orbita(factor, r, longitud)[0]: r for r in range(modulo)}
            assert len(tabla) == modulo
            for palabra in product((0, 1), repeat=longitud):
                historia = estados(factor, palabra)
                ultimo = historia[-1]
                assert ultimo['residuo'] == tabla[palabra]
                cuentas['palabras'] += 1
                for previo, actual in zip(historia, historia[1:]):
                    assert actual['minimo'] >= previo['minimo']
                    assert actual['residuo'] % previo['modulo'] == previo['residuo']
                    if previo['techo'] is not None:
                        assert actual['techo'] <= previo['techo']
                        assert actual['cantidad'] <= previo['cantidad']
                        assert (actual['techo'] - actual['minimo'] <=
                                previo['techo'] - previo['minimo'])
                    elif actual['techo'] is not None:
                        assert actual['techo'] == actual['aditivo'] // (
                            actual['modulo'] - actual['potencia'])
                        cuentas['primeros_cruces'] += 1
                    cuentas['transiciones'] += 1
                minimo, techo = ultimo['minimo'], ultimo['techo']
                if techo is None:
                    candidatos = [minimo + q * modulo for q in range(3)]
                else:
                    # Todos los representantes hasta H y el primero por encima.
                    assert ultimo['cantidad'] <= 10000
                    candidatos = [minimo + q * modulo for q in range(ultimo['cantidad'] + 1)]
                    cuentas['intervalos_finitos'] += 1
                supervivientes = 0
                for semilla in candidatos:
                    bits, valores = orbita(factor, semilla, longitud)
                    assert bits == palabra
                    directo = min(valores) >= semilla
                    assert directo == (techo is None or semilla <= techo)
                    supervivientes += directo
                    for estado, valor in zip(historia, valores):
                        assert estado['modulo'] * valor == estado['potencia'] * semilla + estado['aditivo']
                    cuentas['semillas'] += 1
                if techo is not None:
                    assert supervivientes == ultimo['cantidad']
    return cuentas


def testigos(vueltas):
    palabra, valores = orbita(3, 7, 8)
    historia = estados(3, palabra)
    assert valores == [7, 11, 17, 26, 13, 20, 10, 5, 8]
    assert historia[7]['techo'] == historia[8]['techo'] == 1
    assert historia[8]['aditivo'] // (256 - 243) == 26
    siete = dict(semilla=7, palabra=''.join(map(str, palabra)), valores=valores,
                 prefijo_siete=historia[7], prefijo_ocho=historia[8])

    palabra, valores = orbita(5, 13, 7 * vueltas)
    historia = estados(5, palabra)
    assert min(valores) == 13
    for estado in historia[7:]:
        assert (estado['minimo'], estado['techo'], estado['cantidad']) == (13, 13, 1)
    for q in range(1, vueltas + 1):
        estado = historia[7 * q]
        assert estado['potencia'] == 125 ** q
        assert estado['modulo'] == 128 ** q
        assert estado['aditivo'] == 13 * (128 ** q - 125 ** q)
    vecino = dict(factor=5, semilla=13, vueltas=vueltas, ciclo=valores[:8],
                  primer_cruce=historia[7], ultimo=historia[-1])

    # Cada horizonte tiene una semilla distinta; no se extrapola a un entero fijo.
    unos = []
    for longitud in (2, 3, 8, 16, 32, 64):
        semilla = 2 ** longitud - 1
        palabra, valores = orbita(3, semilla, longitud)
        assert palabra == (1,) * longitud
        assert min(valores) == semilla
        assert valores == [3 ** j * 2 ** (longitud - j) - 1 for j in range(longitud + 1)]
        estado = estados(3, palabra)[-1]
        assert estado['techo'] is None and estado['minimo'] == semilla
        unos.append(dict(longitud=longitud, semilla=semilla, final=valores[-1]))

    bordes = []
    for semilla, longitud in ((0, 0), (0, 4), (1, 2), (2, 1), (3, 1), (18, 8), (27, 60)):
        palabra, valores = orbita(3, semilla, longitud)
        historia = estados(3, palabra)
        admisible = semilla >= 3 and min(valores) >= semilla
        estado = historia[-1]
        assert admisible == (semilla >= 3 and (estado['techo'] is None or semilla <= estado['techo']))
        bordes.append(dict(semilla=semilla, longitud=longitud, admisible=admisible,
                           estado_final=estado))

    # Monotonía racional no implica un descenso bien fundado.
    racionales = [Fraction(13 * k + 1, k) for k in range(1, 10)]
    assert all(a > b > 13 for a, b in zip(racionales, racionales[1:]))
    assert all(int(x) >= 13 for x in racionales)
    return dict(siete=siete, vecino=vecino, unos=unos, bordes=bordes)


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--longitud-maxima', type=int, choices=range(1, 9), required=True)
    analizador.add_argument('--vueltas-vecino', type=int, choices=range(1, 17), required=True)
    analizador.add_argument('--salida', type=Path, required=True)
    argumentos = analizador.parse_args()
    cuentas = cotejar_palabras(argumentos.longitud_maxima)
    evidencia = dict(mapa='T_a(n)=n/2 par, (a*n+1)/2 impar; a=3,5',
                     dominio='semillas enteras >=3; bordes 0,1,2 separados',
                     ley='ninguna; enumeracion determinista, enteros y Fraction',
                     longitud_maxima=argumentos.longitud_maxima,
                     sha256_verificador=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                     cuentas=cuentas, testigos=testigos(argumentos.vueltas_vecino))
    argumentos.salida.parent.mkdir(parents=True, exist_ok=True)
    argumentos.salida.write_text(json.dumps(evidencia, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(cuentas, ensure_ascii=False))
    print('OK: intervalo, anidamiento, primer cruce, ciclo vecino y bordes.')


if __name__ == '__main__':
    main()
