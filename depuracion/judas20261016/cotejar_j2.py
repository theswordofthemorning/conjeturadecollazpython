"""Cotejo de J2 de la Ruta de Judas Iscariote (rama de Claude), 16-10-2026.

Mapa: atajo T(x) = x/2 si x es par y (3x+1)/2 si es impar, sobre enteros
positivos. Clase AB: prefijos de {1,110}^w. lambda(n) es el largo del mayor
prefijo admitido de las paridades de n, T(n), T^2(n), ...

Secciones, todas exactas (enteros o Fraction):
1. lambda de tres maneras independientes, para todo 1 <= n < 2^bits:
   T literal; la función parcial G sobre z=(n+1)/4 en las entradas de bloque;
   y los restos módulo 16 de la órbita impar (Siracusa).
2. Los récords de diagnostico_ruta.json con las tres maneras.
3. Entre Mahler y H: la conjugación n -> (n-1)/8 de la Proposición 4.15 de
   Yolcu-Aaronson-Heule, la rama común (9z+1)/8 en z = 7 mod 8 con H y la
   rama común 3z/2 en z par con la condición de Mahler en la forma de Michel.
4. Fantasmas de G: el punto fijo racional de cada palabra periódica de
   bloques es <= 0, cumple las condiciones de resto 2-ádicas y da x en [-5,-1].
5. Complejidad: factores del lenguaje AB frente a la cota lineal
   log 2/log(3/2) de Dubickas (2009, Teorema 5), y su ley de congruencia
   sobre la órbita del mayor récord.
No repite censos: sólo lee diagnostico_ruta.json y guarda su huella.
"""

import argparse
import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
import time


def lambda_literal(n, tope):
    """Primer instante con un 0 no precedido por 11; tope si no ocurre."""
    x, previo, antes = n, None, None
    for j in range(tope):
        e = x % 2
        if e == 0 and not (previo == 1 and antes == 1):
            return j
        antes, previo = previo, e
        x = (3 * x + 1) // 2 if e else x // 2
    return tope


def lambda_por_G(n, tope):
    """lambda mediante z=(n+1)/4: G(z)=3z/2 si z par, (9z+1)/8 si z=7 mod 8."""
    if n % 2 == 0:
        return 0
    if n % 4 == 1:
        return 1
    z, largo = (n + 1) // 4, 0
    while largo < tope:
        if z % 2 == 0:
            z, largo = 3 * z // 2, largo + 1
        elif z % 8 == 7:
            z, largo = (9 * z + 1) // 8, largo + 3
        elif z % 8 == 3:
            return largo + 4
        else:
            return largo + 3
    return tope


def lambda_por_siracusa(n, tope):
    """lambda mediante la órbita impar: salir es visitar 1, 5 o 13 mod 16."""
    if n % 2 == 0:
        return 0
    if n % 4 == 1:
        return 1
    y, tiempo = n, 0
    while tiempo < tope:
        r = y % 16
        if r in (5, 13):
            return tiempo + 2
        if r == 1:
            return tiempo + 3
        nu = 1 if y % 4 == 3 else 2
        y, tiempo = (3 * y + 1) >> nu, tiempo + nu
    return tope


def seccion_tres_maneras(bits, tope):
    discrepancias, maximo, testigo = [], 0, None
    for n in range(1, 2 ** bits):
        a = lambda_literal(n, tope)
        b = lambda_por_G(n, tope)
        c = lambda_por_siracusa(n, tope)
        if not a == b == c:
            discrepancias.append([n, a, b, c])
        if a > maximo:
            maximo, testigo = a, n
    return {
        'semillas': 2 ** bits - 1,
        'discrepancias': len(discrepancias),
        'ejemplos': discrepancias[:5],
        'lambda_maximo': maximo,
        'menor_semilla_del_maximo': testigo,
    }


def huella(ruta):
    return hashlib.sha256(ruta.read_bytes().replace(b'\r\n', b'\n')).hexdigest()


def seccion_records(ruta, tope):
    datos = json.loads(ruta.read_text(encoding='utf-8'))
    filas, fallos = datos['records']['filas'], []
    for fila in filas:
        n = fila['n']
        valores = [lambda_literal(n, tope), lambda_por_G(n, tope),
                   lambda_por_siracusa(n, tope)]
        if valores != [fila['lambda']] * 3:
            fallos.append([n, fila['lambda']] + valores)
    mayor = max(filas, key=lambda f: f['n'])
    return {
        'fuente': ruta.as_posix(),
        'fuente_sha256_lf': huella(ruta),
        'records': len(filas),
        'fallos': fallos,
        'mayor_record': [mayor['n'], mayor['lambda']],
    }


def G_yah(n):
    """G de YAH, Prop. 4.15: (3n+1)/4 si n=1 mod 32, (9n+7)/8 si n=57 mod 64."""
    if n % 32 == 1:
        return (3 * n + 1) // 4
    if n % 64 == 57:
        return (9 * n + 7) // 8
    return None


def H_yah(m):
    """H de YAH, (10): 3m/4 si m=0 mod 4, (9m+1)/8 si m=7 mod 8."""
    if m % 4 == 0:
        return 3 * m // 4
    if m % 8 == 7:
        return (9 * m + 1) // 8
    return None


def M_mahler(m):
    """Condición necesaria de Mahler (1968), en la forma de Michel (1993):
    3m/2 si m es par, (3m+1)/2 si m=1 mod 4, parar si m=3 mod 4."""
    if m % 2 == 0:
        return 3 * m // 2
    if m % 4 == 1:
        return (3 * m + 1) // 2
    return None


def G_piloto(z):
    if z % 2 == 0:
        return 3 * z // 2
    if z % 8 == 7:
        return (9 * z + 1) // 8
    return None


def pasos_hasta_parar(f, z, tope):
    for paso in range(tope):
        siguiente = f(z)
        if siguiente is None:
            return paso
        z = siguiente
    return tope


def seccion_hermana(bits, tope):
    fallos_conjugacion = 0
    for m in range(1, 2 ** bits):
        g, h = G_yah(8 * m + 1), H_yah(m)
        if (g is None) != (h is None) or (h is not None and g != 8 * h + 1):
            fallos_conjugacion += 1
    rama_comun = all(G_piloto(z) == H_yah(z) for z in range(7, 2 ** bits, 8))
    rama_A_comun = all(G_piloto(z) == M_mahler(z) for z in range(2, 2 ** bits, 2))
    medidas = {}
    for nombre, f in (('G_piloto', G_piloto), ('H_yah', H_yah), ('M_mahler', M_mahler)):
        maximo, testigo, sin_parar = 0, None, 0
        for z in range(1, 2 ** bits):
            pasos = pasos_hasta_parar(f, z, tope)
            if pasos == tope:
                sin_parar += 1
            elif pasos > maximo:
                maximo, testigo = pasos, z
        medidas[nombre] = {'pasos_maximo': maximo, 'menor_testigo': testigo,
                           'sin_parar_antes_del_tope': sin_parar}
    return {
        'semillas': 2 ** bits - 1,
        'fallos_conjugacion_n_a_(n-1)/8': fallos_conjugacion,
        'rama_(9z+1)/8_identica_en_7_mod_8': rama_comun,
        'rama_3z/2_identica_a_Mahler_en_pares': rama_A_comun,
        'iteraciones_hasta_parar': medidas,
    }


def resto_2adico(q, modulo):
    """Resto módulo una potencia de 2 de un racional de denominador impar."""
    return q.numerator * pow(q.denominator, -1, modulo) % modulo


def seccion_fantasmas(largo_max):
    mapas = {'A': (Fraction(3, 2), Fraction(0)), 'B': (Fraction(9, 8), Fraction(1, 8))}
    revisadas, fallos, minimo, maximo = 0, [], None, None
    for largo in range(1, largo_max + 1):
        for palabra in itertools.product('AB', repeat=largo):
            alfa, beta = Fraction(1), Fraction(0)
            for letra in palabra:
                a, b = mapas[letra]
                alfa, beta = a * alfa, a * beta + b
            z = beta / (1 - alfa)
            punto, valido = z, z <= 0
            for letra in palabra:
                if letra == 'A':
                    valido = valido and resto_2adico(punto, 2) == 0
                else:
                    valido = valido and resto_2adico(punto, 8) == 7
                a, b = mapas[letra]
                punto = a * punto + b
            valido = valido and punto == z
            x = 4 * z - 1
            valido = valido and Fraction(-5) <= x <= Fraction(-1)
            revisadas += 1
            if not valido:
                fallos.append(''.join(palabra))
            minimo = x if minimo is None else min(minimo, x)
            maximo = x if maximo is None else max(maximo, x)
    return {
        'palabras_periodicas_revisadas': revisadas,
        'fallos': fallos[:5],
        'x_minimo': str(minimo),
        'x_maximo': str(maximo),
        'G(0)': G_piloto(0),
        'G(-1)': G_piloto(-1),
    }


def factores_AB(largo):
    """Factores de largo dado de las concatenaciones biinfinitas de 1 y 110."""
    palabras = {''}
    while min(len(p) for p in palabras) < largo + 3:
        palabras = {p + b for p in palabras for b in ('1', '110')
                    if len(p) < largo + 3} | {p for p in palabras if len(p) >= largo + 3}
    factores = set()
    for p in palabras:
        for i in range(3):
            if i + largo <= len(p):
                factores.add(p[i:i + largo])
    return factores


def seccion_complejidad(largo_max, record):
    constante = math.log(2) / math.log(1.5)
    filas = []
    for largo in range(1, largo_max + 1):
        p = len(factores_AB(largo))
        filas.append([largo, p, round(constante * largo, 3)])
    n, tope = record
    x, orbita = n, []
    for _ in range(tope):
        orbita.append(x)
        x = (3 * x + 1) // 2 if x % 2 else x // 2
    paridades = [v % 2 for v in orbita]
    pares, fallos = 0, 0
    for m in range(1, 41):
        for s in range(len(orbita) - m):
            for t in range(s + 1, len(orbita) - m + 1):
                if paridades[s:s + m] == paridades[t:t + m]:
                    pares += 1
                    if (orbita[t] - orbita[s]) % 2 ** m:
                        fallos += 1
    return {
        'constante_dubickas': constante,
        'complejidad_AB': filas,
        'ley_congruencia_en_record': {'semilla': n, 'pasos': tope,
                                      'pares_de_factores_iguales': pares,
                                      'fallos': fallos},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--bits', type=int, default=21)
    parser.add_argument('--bits-hermana', type=int, default=20)
    parser.add_argument('--tope', type=int, default=10_000)
    parser.add_argument('--bloques-fantasma', type=int, default=10)
    parser.add_argument('--largo-factores', type=int, default=24)
    parser.add_argument('--diagnostico', default='depuracion/judas20261016/diagnostico_ruta.json')
    parser.add_argument('--salida', default='depuracion/judas20261016/cotejo_j2.json')
    args = parser.parse_args()
    inicio = time.time()
    records = seccion_records(Path(args.diagnostico), args.tope)
    resultado = {
        'fecha': '2026-10-16',
        'parametros': vars(args),
        'tres_maneras': seccion_tres_maneras(args.bits, args.tope),
        'records': records,
        'hermana_H': seccion_hermana(args.bits_hermana, args.tope),
        'fantasmas': seccion_fantasmas(args.bloques_fantasma),
        'complejidad': seccion_complejidad(args.largo_factores, records['mayor_record']),
    }
    resultado['segundos'] = round(time.time() - inicio, 1)
    Path(args.salida).write_text(json.dumps(resultado, ensure_ascii=False, indent=1) + '\n',
                                 encoding='utf-8')
    print(json.dumps({k: v for k, v in resultado.items() if k != 'complejidad'},
                     ensure_ascii=False, indent=1))
    print('complejidad AB (largo, factores, 1.7095*largo):',
          resultado['complejidad']['complejidad_AB'][::6])
    print('ley de congruencia:', resultado['complejidad']['ley_congruencia_en_record'])


if __name__ == '__main__':
    main()
