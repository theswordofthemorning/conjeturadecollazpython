"""Coteja bloques y costes del corte con enteros y órbitas independientes."""

import argparse
import hashlib
import json
from pathlib import Path


def paso(n):
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def orbita(n, longitud):
    valores = [n]
    for _ in range(longitud):
        valores.append(paso(valores[-1]))
    return valores


def afin(palabra):
    a, b, m = 1, 0, 1
    for bit in palabra:
        if bit:
            a, b = 3 * a, 3 * b + m
        m *= 2
    return m, a, b


def cotejar(a_max, b_max, u_max, familia_max):
    bloques = suelos = cortes = 0
    bordes = {}
    for a in range(1, a_max + 1):
        for u in range(1, u_max + 1, 2):
            x = 2 ** a * u - 1
            impar = 3 ** a * u - 1
            b = 0
            while impar % 2 == 0:
                impar //= 2
                b += 1
            if b > b_max:
                continue
            y = impar
            valores = orbita(x, a + b)
            palabra = [v % 2 for v in valores[:-1]]
            assert palabra == [1] * a + [0] * b
            assert valores[-1] == y and y % 2 == 1 and b >= 1
            p, q, r = 2 ** a, 2 ** b, 3 ** a
            m, A, B = afin(palabra)
            assert (m, A, B) == (p * q, r, r - p)
            assert p * (q * y + 1) == r * (x + 1)
            for n in sorted({1, 2, 3, x, max(1, x - 1)}):
                assert m * (y - n) == r * (x - n) - (m - r) * n + r - p
                assert (y < n) == (x - y > x - n) == (x - y >= x - n + 1)
                assert (y < n) == ((m - A) * x - B > m * (x - n))
                cortes += 1
            for suelo in sorted({0, 1, max(0, y - 1), y, y + 1}):
                diferencia = (q * suelo + 1) * p * (y + 1) - (suelo + 1) * r * (x + 1)
                assert diferencia == p * (q - 1) * (suelo - y)
                assert (diferencia <= 0) == (suelo <= y)
                assert (diferencia == 0) == (suelo == y)
                suelos += 1
            if a == 1:
                assert x == 1 or y < x
            if (a, b) == (2, 1):
                assert x < y
            if x in (1, 3, 11):
                bordes[str(x)] = dict(a=a, b=b, salida=y, orbita=valores)
            bloques += 1

    familias = []
    for k in sorted({1, 2, 4, 8, 16, 32, familia_max}):
        if k > familia_max:
            continue
        n = 2 * 8 ** k - 5
        valores = orbita(n, 3 * k)
        palabra = [v % 2 for v in valores[:-1]]
        assert palabra == [1, 1, 0] * k
        assert valores[-1] % 2 == 1
        assert min(valores) == n
        assert [valores[3 * j] for j in range(k + 1)] == [
            2 * 9 ** j * 8 ** (k - j) - 5 for j in range(k + 1)]
        assert all(valores[3 * j] < valores[3 * (j + 1)] for j in range(k))
        m, A, B = afin(palabra)
        assert (m, A, B) == (8 ** k, 9 ** k, 5 * (9 ** k - 8 ** k))
        unos = 0
        for j, bit in enumerate(palabra, 1):
            unos += bit
            assert 3 ** unos > 2 ** j
        familias.append(dict(k=k, semilla=n, salida=valores[-1], pasos=3 * k))

    siete = orbita(7, 7)
    assert siete == [7, 11, 17, 26, 13, 20, 10, 5]
    assert 13 - 10 <= 13 - 7 < 13 - 5
    coeficientes = []
    for n, longitud in ((7, 7), (13, 2)):
        valores = orbita(n, longitud)
        unos = 0
        for j, valor in enumerate(valores[:-1], 1):
            unos += valor % 2
            assert (3 ** unos < 2 ** j) == (j == longitud)
            assert (valores[j] < n) == (j == longitud)
        coeficientes.append(dict(semilla=n, primer_cruce=longitud,
                                  primer_descenso=longitud))
    return dict(bloques=bloques, suelos=suelos, cortes=cortes, bordes=bordes,
                familias=familias, testigo_corte=siete, cruces=coeficientes)


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--a-max", type=int, required=True)
    analizador.add_argument("--b-max", type=int, required=True)
    analizador.add_argument("--u-max", type=int, required=True)
    analizador.add_argument("--familia-max", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    assert min(argumentos.a_max, argumentos.b_max, argumentos.u_max, argumentos.familia_max) >= 1
    resultado = cotejar(argumentos.a_max, argumentos.b_max, argumentos.u_max, argumentos.familia_max)
    evidencia = dict(mapa="atajo 3n+1", ley="determinista, enteros exactos",
                     parametros={k: v for k, v in vars(argumentos).items() if k != "salida"},
                     sha256_verificador=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                     resultado=resultado)
    argumentos.salida.parent.mkdir(parents=True, exist_ok=True)
    argumentos.salida.write_text(json.dumps(evidencia, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK: {resultado['bloques']} bloques, {resultado['suelos']} suelos, {resultado['cortes']} cortes.")
    print(f"Familias: {len(resultado['familias'])}; bordes y primer cruce cotejados.")


if __name__ == "__main__":
    main()
