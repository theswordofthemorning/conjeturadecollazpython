"""Contrasta el balance ternario general y la ambiguedad de la clase critica."""

import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


def T(n):
    return (3 * n + 1) // 2 if n % 2 else n // 2


def valoracion(n):
    assert n > 0
    resultado = 0
    while n % 3 == 0:
        n //= 3
        resultado += 1
    return resultado


def profundidad(n, m):
    return m - min(m, valoracion(2 * n + 1))


def estacionarias(maximo):
    anterior = [Fraction(1)]
    resultados = []
    for m in range(1, maximo + 1):
        modulo, periodo = 3 ** m, 2 * 3 ** (m - 1)
        nu = [Fraction(0)] * modulo
        for x, masa in enumerate(anterior):
            for a in range(1, periodo + 1):
                destino = (3 * x + 1) * pow(2, -a, modulo) % modulo
                nu[destino] += masa * Fraction(2 ** (periodo - a), 2 ** periodo - 1)
        assert sum(nu) == 1
        assert max(nu) <= Fraction(2, 3) ** m
        resultados.append(nu)
        anterior = nu
    return resultados


def revisar_modelo(m, nu):
    modulo, critico = 3 ** m, (3 ** m - 1) // 2
    inverso = pow(2, -1, modulo)
    llegada = [Fraction(0)] * modulo
    g = [profundidad(x, m) - profundidad(2 * x % modulo, m) for x in range(modulo)]
    for x, masa in enumerate(nu):
        y = x
        for _ in range(m):
            y = (3 * y + 1) % modulo
        assert y == critico
        for bit in (0, 1):
            destino = ((3 * x + 1) if bit else x) * inverso % modulo
            llegada[destino] += masa / 2
            assert (profundidad(x, m) - profundidad(2 * destino % modulo, m)
                    == bit * int(x != critico))
    assert llegada == nu
    assert sum(nu[x] * g[x] for x in range(modulo)) == (1 - nu[critico]) / 2
    assert nu[critico] <= Fraction(2 ** (m - 1), modulo)
    superior = [g[x] + int(x == critico) for x in range(modulo)]
    assert max(g) - min(g) == 2 * m
    assert max(superior) - min(superior) == 2 * m - 1
    for extremo in (0, 1):
        llegada = [Fraction(0)] * modulo
        total_impares = Fraction(0)
        for x, masa in enumerate(nu):
            impar = masa * extremo if x == critico else masa / 2
            llegada[x * inverso % modulo] += masa - impar
            llegada[(3 * x + 1) * inverso % modulo] += impar
            total_impares += impar
        assert llegada == nu
        assert total_impares == (1 + (2 * extremo - 1) * nu[critico]) / 2
    return dict(m=m, modulo=modulo, clase_critica=critico,
                masa_critica=str(nu[critico]),
                intervalo_impares=[str((1 - nu[critico]) / 2), str((1 + nu[critico]) / 2)])


def revisar_orbita(semilla, pasos, estacionarias_):
    x = semilla
    cuentas = [Counter() for _ in estacionarias_]
    criticas = [0] * len(estacionarias_)
    sumas = [0] * len(estacionarias_)
    impares = 0
    for k in range(1, pasos + 1):
        siguiente = T(x)
        assert valoracion(4 * siguiente + 1) == valoracion(2 * x + 1) + x % 2
        impares += x % 2
        for i, nu in enumerate(estacionarias_):
            m, modulo = i + 1, len(nu)
            r, critico = x % modulo, (modulo - 1) // 2
            cuentas[i][r] += 1
            criticas[i] += (x % 2) * int(r == critico)
            sumas[i] += profundidad(x, m) - profundidad(2 * x, m)
            borde = profundidad(2 * semilla, m) - profundidad(2 * siguiente, m)
            assert impares - criticas[i] == sumas[i] + borde
        x = siguiente
    for i, nu in enumerate(estacionarias_):
        m, modulo = i + 1, len(nu)
        critico = (modulo - 1) // 2
        tv = sum(abs(Fraction(cuentas[i][r], pasos) - nu[r]) for r in range(modulo)) / 2
        inferior = (1 - nu[critico]) / 2 - 2 * m * tv - Fraction(m, pasos)
        superior = (1 + nu[critico]) / 2 + (2 * m - 1) * tv + Fraction(m, pasos)
        assert inferior <= Fraction(impares, pasos) <= superior


def circuito_extremo(extremo, vueltas):
    numeradores = (0, 8, 16, 0, 11, 4, 0, 2, 22)
    aristas = {}
    for r, masa in enumerate(numeradores):
        impares = 2 * masa * extremo if r == 4 else masa
        aristas[r] = [(0, 5 * r % 9)] * (2 * masa - impares)
        aristas[r] += [(1, 5 * (3 * r + 1) % 9)] * impares
    pila, camino = [(1, None)], []
    while pila:
        r, bit = pila[-1]
        if aristas[r]:
            siguiente, destino = aristas[r].pop()
            pila.append((destino, siguiente))
        else:
            pila.pop()
            if bit is not None:
                camino.append(bit)
    bits = list(reversed(camino))
    assert len(bits) == 126 and not any(aristas.values())
    bits *= vueltas
    semilla, x, subidas = 0, 0, 0
    for k, bit in enumerate(bits):
        if x % 2 != bit:
            semilla += 2 ** k
            x += 3 ** subidas
        assert x % 2 == bit
        x = T(x)
        subidas += bit
    modulo = 2 ** len(bits)
    semilla += ((1 - semilla) * pow(modulo, -1, 9) % 9) * modulo
    assert semilla > 0
    x, cuentas, unos = semilla, Counter(), 0
    for bit in bits:
        assert x % 2 == bit
        cuentas[x % 9] += 1
        unos += bit
        x = T(x)
    assert x % 9 == 1
    assert [Fraction(cuentas[r], len(bits)) for r in range(9)] == [Fraction(v, 63) for v in numeradores]
    assert Fraction(unos, len(bits)) == Fraction(26 + 11 * extremo, 63)
    return dict(extremo=extremo, semilla=str(semilla), pasos=len(bits), impares=unos,
                proporcion_impares=str(Fraction(unos, len(bits))), tv_modulo_9="0")


def revisar_racional(maximo):
    palabra = "AABAAABBAAAAAABAAAAABABAAABAAABBB"
    bits = [int(bit) for bloque in palabra for bit in ("1" if bloque == "A" else "110")]
    real, racional, subidas, comparaciones = 6416623, Fraction(23), 0, 0
    for bit in bits:
        assert real % 2 == bit
        for m in range(1, maximo + 1):
            modulo = 3 ** m
            r = racional.numerator * pow(racional.denominator, -1, modulo) % modulo
            if subidas >= m:
                assert r == real % modulo
                comparaciones += 1
        real = T(real)
        racional = (3 * racional + 1) / 2 if bit else racional / 2
        subidas += bit
    assert racional.denominator > 1
    return comparaciones


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--modulo-max", type=int, required=True)
    analizador.add_argument("--semillas-max", type=int, required=True)
    analizador.add_argument("--pasos", type=int, required=True)
    analizador.add_argument("--vueltas-extremos", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    assert 1 <= args.modulo_max <= 5
    assert min(args.semillas_max, args.pasos, args.vueltas_extremos) >= 1
    distribuciones = estacionarias(args.modulo_max)
    modelos = [revisar_modelo(m, nu) for m, nu in enumerate(distribuciones, 1)]
    if args.modulo_max >= 3:
        cota = (1 + distribuciones[2][13]) / 2 + Fraction(1, 20) + Fraction(3, 86)
        assert Fraction(17, 27) - cota == Fraction(75101, 225442980)
    for semilla in range(1, args.semillas_max + 1):
        revisar_orbita(semilla, args.pasos, distribuciones)
    if args.modulo_max >= 2:
        for r in range(9):
            g = profundidad(r, 2) - profundidad(2 * r % 9, 2) + int(r == 4)
            assert g == int(r == 2) + int(r % 3 == 2) - int(r % 3 == 1)
    extremos = [circuito_extremo(e, args.vueltas_extremos) for e in (0, 1)]
    comparaciones = revisar_racional(args.modulo_max)
    resultado = dict(
        alcance="Contraste finito exacto; no sustituye la prueba general ni demuestra mezcla excepcional.",
        modelos=modelos, balances_orbitales=args.modulo_max * args.semillas_max * args.pasos,
        semillas=args.semillas_max, pasos=args.pasos, extremos_enteros=extremos,
        comparaciones_racionales=comparaciones,
        fuente_sha256=sha256(Path(__file__).read_bytes()).hexdigest())
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(estado="correcto", balances=resultado["balances_orbitales"],
                          modelos=args.modulo_max, extremos=len(extremos))))


if __name__ == "__main__":
    main()
