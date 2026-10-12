"""Perdices: retorno E^b D^a sobre C={x>0:x=15 mod 24}.

Se cotejan las valuaciones binarias hacia delante y las ternarias hacia atrás
con iteración directa de H y su inversa. Cada rama tiene denominador
M=4^a*8^b y numerador A=3^(a+2b). Los cilindros y la unión de pasado y futuro
usan sólo enteros y Fraction. No se afirma terminación universal.
"""

import argparse
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path


def valuacion(n, primo):
    assert n > 0
    exponente = 0
    while n % primo == 0:
        n //= primo
        exponente += 1
    return exponente


def retorno(x):
    assert x > 0 and x % 24 == 15
    e = valuacion(x + 1, 2)
    if e % 3:
        return None
    b = e // 3
    u = (x + 1) // 8 ** b
    z = 9 ** b * u - 1
    d = valuacion(z, 2)
    if d < 2 or d % 2:
        return None
    a = d // 2
    y = 3 ** a * (z // 4 ** a)
    return (y, a, b) if y % 24 == 15 else None


def anterior(y):
    assert y > 0 and y % 24 == 15
    a = valuacion(y, 3)
    z = 4 ** a * (y // 3 ** a) + 1
    e = valuacion(z, 3)
    if e < 2 or e % 2:
        return None
    b = e // 2
    x = 8 ** b * (z // 9 ** b) - 1
    return (x, a, b) if x > 0 and x % 24 == 15 else None


def retorno_directo(x):
    b = a = 0
    while x % 8 == 7:
        x = (9 * x + 1) // 8
        b += 1
    while x % 4 == 0:
        x = 3 * x // 4
        a += 1
    return (x, a, b) if a and b and x % 24 == 15 else None


def anterior_directo(y):
    a = b = 0
    while y % 3 == 0:
        y = 4 * y // 3
        a += 1
    while y % 9 == 8:
        y = (8 * y - 1) // 9
        b += 1
    return (y, a, b) if a and b and y % 24 == 15 else None


def rama(a, b):
    assert a >= 1 and b >= 1
    numerador = 3 ** (a + 2 * b)
    modulo = 4 ** a * 8 ** b
    constante = 3 ** a * (9 ** b - 8 ** b)
    r2 = (7 * modulo - constante) * pow(numerador, -1, 8 * modulo) % (8 * modulo)
    r = r2 + 8 * modulo * (-r2 * pow(8 * modulo, -1, 3) % 3)
    s = (numerador * r + constante) // modulo
    assert r % 24 == s % 24 == 15
    assert 0 < r < 24 * modulo and 0 < s < 24 * numerador
    return dict(a=a, b=b, A=numerador, M=modulo, B=constante, r=r, s=s)


def cilindro(historia):
    """Bijección r+24*M*t -> s+24*A*t, t>=0, de una historia completa."""
    r = s = 15
    numerador = modulo = 1
    for a, b in historia:
        nueva = rama(a, b)
        # A es impar y el nuevo módulo es potencia de 2.
        t = ((nueva['r'] - s) // 24) * pow(numerador, -1, nueva['M']) % nueva['M']
        entrada = s + 24 * numerador * t
        indice = (entrada - nueva['r']) // (24 * nueva['M'])
        assert indice >= 0
        r += 24 * modulo * t
        s = nueva['s'] + 24 * nueva['A'] * indice
        modulo *= nueva['M']
        numerador *= nueva['A']
    assert r % 24 == s % 24 == 15
    assert 0 < r < 24 * modulo and 0 < s < 24 * numerador
    return r, modulo, s, numerador


def seguir(x, historia):
    for a, b in historia:
        resultado = retorno_directo(x)
        assert resultado is not None and resultado[1:] == (a, b), (x, historia)
        x = resultado[0]
    return x


def retroceder(y, historia):
    for a, b in reversed(historia):
        resultado = anterior_directo(y)
        assert resultado is not None and resultado[1:] == (a, b), (y, historia)
        y = resultado[0]
    return y


def empalmar(pasado, futuro):
    _, _, s, numerador = cilindro(pasado)
    r, modulo, _, _ = cilindro(futuro)
    rf, rp = (r - 15) // 24, (s - 15) // 24
    t = (rp - rf) * pow(modulo, -1, numerador) % numerador if numerador > 1 else 0
    q = rf + modulo * t
    return 15 + 24 * q, 24 * modulo * numerador


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--nmax', type=int, required=True)
    analizador.add_argument('--amax', type=int, required=True)
    analizador.add_argument('--bmax', type=int, required=True)
    analizador.add_argument('--profundidad', type=int, required=True)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    assert args.nmax >= 15 and min(args.amax, args.bmax) >= 1 and args.profundidad >= 0
    assert sum((args.amax * args.bmax) ** k for k in range(args.profundidad + 1)) <= 100000
    conteo = dict(semillas=0, retornos=0, predecesores=0, crecen=0, decrecen=0)
    for x in range(15, args.nmax + 1, 24):
        adelante, atras = retorno(x), anterior(x)
        assert adelante == retorno_directo(x), x
        assert atras == anterior_directo(x), x
        conteo['semillas'] += 1
        if adelante:
            y, a, b = adelante
            assert anterior(y) == (x, a, b)
            datos = rama(a, b)
            assert x % (24 * datos['M']) == datos['r']
            assert y % (24 * datos['A']) == datos['s']
            assert y != x
            conteo['retornos'] += 1
            conteo['crecen' if y > x else 'decrecen'] += 1
        if atras:
            y, a, b = atras
            assert retorno(y) == (x, a, b)
            datos = rama(a, b)
            assert y % (24 * datos['M']) == datos['r']
            assert x % (24 * datos['A']) == datos['s']
            conteo['predecesores'] += 1
    etiquetas = list(product(range(1, args.amax + 1), range(1, args.bmax + 1)))
    masa_entrada = sum((Fraction(1, 4 ** a * 8 ** b) for a, b in etiquetas), Fraction())
    masa_salida = sum((Fraction(1, 3 ** (a + 2 * b)) for a, b in etiquetas), Fraction())
    assert masa_entrada == Fraction(1 - Fraction(1, 4 ** args.amax), 3) * Fraction(
        1 - Fraction(1, 8 ** args.bmax), 7)
    assert masa_salida == Fraction(1 - Fraction(1, 3 ** args.amax), 2) * Fraction(
        1 - Fraction(1, 9 ** args.bmax), 8)
    niveles, representantes = [], 0
    for k in range(args.profundidad + 1):
        entrada = salida = Fraction()
        cantidad = 0
        for historia in product(etiquetas, repeat=k):
            r, modulo, s, numerador = cilindro(historia)
            for t in (0, 1):
                x, y = r + 24 * modulo * t, s + 24 * numerador * t
                assert seguir(x, historia) == y
                assert retroceder(y, historia) == x
                representantes += 1
            entrada += Fraction(1, modulo)
            salida += Fraction(1, numerador)
            cantidad += 1
        assert entrada == masa_entrada ** k and salida == masa_salida ** k
        niveles.append(dict(k=k, historias=cantidad, densidad_relativa_entrada=str(entrada),
                            densidad_relativa_salida=str(salida)))
    # Pasados y futuros exhaustivos en un alfabeto pequeño, incluidos los vacíos.
    pequenas = list(product(range(1, 3), repeat=2))
    historias = [h for k in range(3) for h in product(pequenas, repeat=k)]
    empalmes = 0
    for pasado in historias:
        for futuro in historias:
            x, periodo = empalmar(pasado, futuro)
            for semilla in (x, x + periodo):
                antes = retroceder(semilla, pasado)
                assert seguir(antes, pasado) == semilla
                despues = seguir(semilla, futuro)
                assert retroceder(despues, futuro) == semilla
                empalmes += 1
    # Un período completo por pareja de ramas: verificación independiente de unicidad CRT.
    periodos, semillas_periodos = [], 0
    for pasado in [(1, 1), (1, 2), (2, 1)]:
        for futuro in [(1, 1), (1, 2), (2, 1)]:
            x, periodo = empalmar([pasado], [futuro])
            encontrados = []
            for semilla in range(15, periodo, 24):
                ida, vuelta = retorno_directo(semilla), anterior_directo(semilla)
                if ida and vuelta and ida[1:] == futuro and vuelta[1:] == pasado:
                    encontrados.append(semilla)
                semillas_periodos += 1
            assert encontrados == [x]
            periodos.append(dict(pasado=pasado, futuro=futuro,
                                 periodo=periodo, unico=str(x)))
    ejemplos = []
    for a, b in [(1, 1), (1, 2), (1, 3), (2, 5), (5, 12)]:
        datos = rama(a, b)
        ejemplos.append({k: str(v) if k in ('A', 'M', 'B', 'r', 's') else v
                         for k, v in datos.items()})
    resultado = dict(parametros=vars(args) | {'salida': str(args.salida)},
                     contraste_directo=conteo, niveles=niveles,
                     representantes=representantes, empalmes_pasado_futuro=empalmes,
                     periodos_completos=periodos, semillas_en_periodos=semillas_periodos,
                     ejemplos=ejemplos,
                     sha256_fuente_lf=hashlib.sha256(Path(__file__).read_text(
                         encoding='utf-8').encode('utf-8')).hexdigest(),
                     alcance='Cotejo finito de ramas, inversas, cilindros y empalmes. Las '
                     'densidades naturales 21^(-k) y 16^(-l) tienen prueba escrita, incluido '
                     'el paso desde uniones finitas. No excluye una semilla persistente.')
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'OK: {conteo}; {representantes} representantes; {empalmes} empalmes.')


if __name__ == '__main__':
    main()
