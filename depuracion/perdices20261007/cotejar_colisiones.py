"""Cotejo entero de imágenes, patrones y sumas; no busca órbitas infinitas."""

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from math import comb
from pathlib import Path


def paso(x):
    return (3 * x + 1) // 2 if x % 2 else x // 2


def iterar(x, k):
    for _ in range(k):
        x = paso(x)
    return x


def imagenes(largo):
    tablas = []
    prefijos = 0
    for k in range(largo + 1):
        patrones = Counter()
        salidas = set()
        buenas = set()
        malas = 0
        umbral = (3 * k) // 5
        # Independiente de Lean: reconstruir el aditivo desde la palabra real.
        for n in range(2 ** k):
            x, aditivo, subidas, palabra = n, 0, 0, 0
            for j in range(k):
                bit = x % 2
                palabra += bit * 2 ** j
                if bit:
                    aditivo = 3 * aditivo + 2 ** j
                    subidas += 1
                x = paso(x)
                assert 2 ** (j + 1) * x == 3 ** subidas * n + aditivo
                assert aditivo + 2 ** (j + 1) <= 3 ** (j + 1)
                prefijos += 1
            assert palabra not in patrones
            patrones[palabra] = subidas
            salidas.add(x)
            if subidas >= umbral:
                malas += 1
            else:
                buenas.add(x)
                assert x < 3 ** umbral + (3 ** k) // (2 ** k)
        cuenta = Counter(patrones.values())
        assert cuenta == Counter({s: comb(k, s) for s in range(k + 1)})
        assert sum(2 ** s for s in patrones.values()) == 3 ** k
        assert malas == sum(comb(k, s) for s in range(umbral, k + 1))
        assert malas * 2 ** umbral <= 3 ** k
        assert len(salidas) <= len(buenas) + malas
        tablas.append(dict(k=k, entradas=2 ** k, imagen=len(salidas),
                           umbral=umbral, entradas_malas=malas,
                           imagen_buena=len(buenas)))
    return dict(tablas=tablas, identidades_prefijos=prefijos)


def bloques(limite):
    tablas = []
    for m in range(limite + 1):
        k, h = 100 * m, 60 * m
        # Se cuentan palabras con el binomio, sin recorrer 2^(100m) entradas.
        malas = sum(comb(k, s) for s in range(h, k + 1))
        assert malas * 2 ** h <= 3 ** k <= 2 ** (159 * m)
        assert malas <= 2 ** (99 * m)
        assert 3 ** (60 * m) <= 2 ** (96 * m)
        assert 3 ** k <= 2 ** (100 * m) * 2 ** (59 * m)
        assert 2 * 2 ** (96 * m) + malas <= 3 * 2 ** (99 * m)
        tablas.append(dict(m=m, malas=str(malas), cota_malas=str(2 ** (99 * m))))
    return tablas


def anillos(limite):
    constante = 3 * 2 ** 99
    suma = Fraction(0)
    for m in range(limite + 1):
        aporte = Fraction(3 * 2 ** (99 * (m + 1)), 2 ** (100 * m))
        assert aporte == Fraction(constante, 2 ** m)
        suma += aporte
        assert suma + Fraction(2 * constante, 2 ** (m + 1)) == 2 * constante
    return dict(anillos=limite + 1, cota_total=str(2 * constante),
                suma_cotas=str(suma), cola_cotas=str(Fraction(2 * constante, 2 ** (limite + 1))))


def identidades(nmax, pasos):
    verificadas, distintos = 0, 0
    for n in range(1, nmax + 1):
        x, s = n, 0
        producto, aditivo, reciprocos = Fraction(n), Fraction(n), Fraction(0)
        vistos = set()
        for j in range(pasos):
            if x in vistos:
                break
            vistos.add(x)
            distintos += 1
            reciprocos += Fraction(1, x)
            assert reciprocos == sum((Fraction(1, a) for a in vistos), Fraction(0))
            if x % 2:
                producto *= Fraction(3 * x + 1, 3 * x)
                aditivo += Fraction(2 ** j, 3 ** (s + 1))
                s += 1
            x = paso(x)
            normalizado = Fraction(2 ** (j + 1) * x, 3 ** s)
            assert normalizado == producto == aditivo
            verificadas += 1
    return dict(identidades=verificadas, valores_sin_repetir=distintos,
                alcance='Sólo prefijos finitos, detenidos al repetir; no certifican inyectividad infinita.')


def bordes():
    # Un prefijo sin repeticiones no basta: puede coalescer después.
    prefijo = [4, 2, 1]
    assert len(set(prefijo)) == 3
    imagen = [iterar(x, 2) for x in prefijo]
    assert imagen == [1, 2, 1]
    # En el ciclo 1,2 la suma temporal crece y la suma sobre valores no.
    suma_temporal = sum((Fraction(1, iterar(1, j)) for j in range(12)), Fraction(0))
    assert suma_temporal == 9 > Fraction(3, 2)
    assert Fraction(2 ** 12 * iterar(1, 12), 3 ** 6) == Fraction(4, 3) ** 6
    # Progresiones de paso r en [2^r,2^(r+1)): densidad de Banach cero no basta.
    cuentas, cotas = [], []
    for r in range(2, 65):
        cantidad = 2 ** r // r
        assert cantidad * r >= 2 ** (r - 1)
        ultimo = 2 ** r + (cantidad - 1) * r
        assert 2 ** (r + 1) - ultimo >= r
        cota = Fraction(cantidad, 2 ** (r + 1))
        assert cota >= Fraction(1, 4 * r)
        cuentas.append(cantidad)
        cotas.append(str(cota))
    return dict(prefijo_distinto=prefijo, imagen_dos_pasos=imagen,
                suma_temporal_ciclo=str(suma_temporal), suma_valores_ciclo='3/2',
                bloques_densidad_cero=len(cuentas), primera_cota=cotas[0], ultima_cota=cotas[-1],
                nota='El contraejemplo de densidad cero tiene prueba infinita escrita en COLISIONES.md.')


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--largo', type=int, default=14)
    analizador.add_argument('--bloques', type=int, default=16)
    analizador.add_argument('--nmax', type=int, default=256)
    analizador.add_argument('--pasos', type=int, default=128)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    assert args.largo >= 0 and args.bloques >= 0 and args.nmax >= 1 and args.pasos >= 1
    evidencia = dict(parametros=dict(largo=args.largo, bloques=args.bloques,
                                     nmax=args.nmax, pasos=args.pasos),
                     imagenes=imagenes(args.largo), bloques=bloques(args.bloques),
                     anillos=anillos(args.bloques), identidades=identidades(args.nmax, args.pasos),
                     bordes=bordes())
    evidencia['sha256_fuente_lf'] = hashlib.sha256(
        Path(__file__).read_text(encoding='utf-8').encode('utf-8')).hexdigest()
    args.salida.write_text(json.dumps(evidencia, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"OK: {evidencia['imagenes']['identidades_prefijos']} prefijos; "
          f"{len(evidencia['bloques'])} cuentas binomiales; "
          f"{evidencia['identidades']['identidades']} identidades orbitales; bordes comprobados.")


if __name__ == '__main__':
    main()
