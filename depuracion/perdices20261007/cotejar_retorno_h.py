"""Perdices: mapa parcial H de Yolcu–Aaronson–Heule, proposición 4.15.

H(x)=3x/4 si x=0 mod 4; (9x+1)/8 si x=7 mod 8; indefinido en otro caso.
Dominio objetivo: enteros positivos. Se permite cero para residuos mínimos.
Verifica el retorno del atajo T a 1 mod 8, la inversa, cilindros finitos y
su densidad exacta. Los pasos de H duran dos o tres pasos T, respectivamente.
Sin ley aleatoria ni hipótesis de independencia.
"""

import argparse
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path


def paso_t(n):
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def paso_h(n):
    if n % 4 == 0:
        return 3 * n // 4
    if n % 8 == 7:
        return (9 * n + 1) // 8
    return None


def inversa_h(n):
    if n % 3 == 0:
        return 4 * n // 3
    if n % 9 == 8:
        return (8 * n - 1) // 9
    return None


def cilindro(historia):
    """r módulo M; identidad M H^k(x) = A*x+B para esa historia."""
    r, modulo, a, b = 0, 1, 1, 0
    for rama in historia:
        divisor, pendiente, constante, residuo = (4, 3, 0, 0) if rama == 'D' else (8, 9, 1, 7)
        y = (a * r + b) // modulo
        t = (residuo - y) * pow(a, -1, divisor) % divisor
        r += modulo * t
        a, b = pendiente * a, pendiente * b + constante * modulo
        modulo *= divisor
    return r, modulo, a, b


def recorrer(n, historia):
    for rama in historia:
        assert (n % 4 == 0) if rama == 'D' else (n % 8 == 7)
        n = paso_h(n)
        assert n is not None
    return n


def valuacion2(n):
    assert n > 0
    return (n & -n).bit_length() - 1


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--nmax', type=int, required=True)
    analizador.add_argument('--profundidad', type=int, required=True)
    analizador.add_argument('--corte', type=int, default=128)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    assert args.nmax >= 1 and 0 <= args.profundidad <= 16 and args.corte >= 1
    puentes = inversas = rachas = pasos = 0
    truncadas, ciclos = [], []
    record = (0, 1)
    for x in range(1, args.nmax + 1):
        y = paso_h(x)
        if y is not None:
            assert inversa_h(y) == x
            inversas += 1
            n = 8 * x + 1
            duracion = 2 if x % 4 == 0 else 3
            bits = ''
            for _ in range(duracion):
                bits += str(n % 2)
                n = paso_t(n)
            assert n == 8 * y + 1
            assert bits == ('10' if duracion == 2 else '101')
            puentes += 1
        z = inversa_h(x)
        if z is not None:
            assert z >= 1 and paso_h(z) == x
            inversas += 1
        # Derivación independiente de los retornos: iterar T y observar 1 mod 8.
        n = 8 * x + 1
        retorno = None
        for _ in range(3):
            if n % 8 in (5, 7):
                break
            n = paso_t(n)
            if n % 8 == 1:
                retorno = (n - 1) // 8
                break
        assert retorno == y, x
        for rama, cantidad in [('D', valuacion2(x) // 2),
                               ('E', valuacion2(x + 1) // 3)]:
            if cantidad:
                final = recorrer(x, rama * cantidad)
                esperado = (3 ** cantidad * x // 4 ** cantidad if rama == 'D' else
                            9 ** cantidad * (x + 1) // 8 ** cantidad - 1)
                assert final == esperado
                assert (final % 4 != 0) if rama == 'D' else (final % 8 != 7)
                rachas += 1
        actual, vistos, largo = x, set(), 0
        while actual is not None and actual not in vistos and largo < args.corte:
            vistos.add(actual)
            siguiente = paso_h(actual)
            if siguiente is None:
                actual = None
            else:
                actual = siguiente
                largo += 1
                pasos += 1
        if actual is not None:
            (ciclos if actual in vistos else truncadas).append(x)
        if largo > record[0]:
            record = (largo, x)
    expansiones = 0
    for modulo in range(1, 33):
        for t in range(1, 4):
            for k in range(1, 17):
                x = 8 ** k * modulo * t - 1
                y = recorrer(x, 'E' * k)
                assert y == 9 ** k * modulo * t - 1 and y > x
                assert x % modulo == y % modulo == modulo - 1
                expansiones += 1
    niveles, representantes = [], 0
    for k in range(args.profundidad + 1):
        masa = Fraction(0)
        clases = []
        for historia in product('DE', repeat=k):
            r, modulo, a, b = cilindro(historia)
            assert 0 <= r < modulo
            assert modulo == 4 ** historia.count('D') * 8 ** historia.count('E')
            masa += Fraction(1, modulo)
            # Dos representantes positivos; no confundir el residuo cero con la semilla cero.
            primero = r if r else modulo
            for x in (primero, primero + modulo):
                assert modulo * recorrer(x, historia) == a * x + b
                representantes += 1
            clases.append((r, modulo))
        assert masa == Fraction(3, 8) ** k
        # Verificación por congruencia directa en niveles pequeños, independiente de la suma.
        if k <= 7:
            for i, (r, modulo) in enumerate(clases):
                for s, otro_modulo in clases[:i]:
                    assert (r - s) % min(modulo, otro_modulo) != 0
        niveles.append(dict(k=k, historias=len(clases), densidad=str(masa)))
    datos = dict(parametros=vars(args) | {'salida': str(args.salida)},
                 puentes_t_h=puentes, identidades_inversas=inversas, rachas_exactas=rachas,
                 pasos_h_observados=pasos, semillas_truncadas=truncadas,
                 semillas_con_repeticion=ciclos,
                 record_finito=dict(pasos_h=record[0], semilla=record[1]),
                 expansiones_residuales=expansiones,
                 representantes_positivos=representantes, niveles=niveles,
                 sha256_fuente_lf=hashlib.sha256(Path(__file__).read_text(
                     encoding='utf-8').encode('utf-8')).hexdigest(),
                 alcance='Cotejo finito de identidades y testigos. La densidad tiene prueba '
                 'escrita en SALIDAS.md; las identidades básicas están en PerdicesRetornoH.lean. '
                 'No excluye una órbita infinita positiva de H.')
    args.salida.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'OK: {puentes} puentes, {inversas} inversas, {representantes} representantes; '
          f'truncadas={len(truncadas)}, ciclos={len(ciclos)}; récord H {record}.')


if __name__ == '__main__':
    main()
