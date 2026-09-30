"""Cotejo independiente de los prefijos y bloques formalizados en Lean.

Atajo de Collatz sobre n>=2; un paso impar clásico se agrupa con su división
por dos. El coeficiente y el término aditivo se componen con Fraction.
No importa ninguno de los otros verificadores ni presupone Rhin.
"""

import argparse
from fractions import Fraction
import hashlib
from itertools import groupby
import json
from pathlib import Path


def trayectoria(n, max_pasos):
    if n < 2 or max_pasos < 1:
        raise ValueError("Se requiere n>=2 y max_pasos>=1")
    valores = [n]
    paridades = []
    coeficiente = Fraction(1)
    aditivo = Fraction(0)
    for _ in range(max_pasos):
        actual = valores[-1]
        impar = actual % 2
        paridades.append(impar)
        if impar:
            actual = 3 * actual + 1
            coeficiente *= 3
            aditivo = 3 * aditivo + 1
        actual //= 2
        coeficiente /= 2
        aditivo /= 2
        valores.append(actual)
        assert actual == coeficiente * n + aditivo
        if coeficiente < 1:
            return valores, paridades
    raise RuntimeError(f"INCONCLUSO: n={n}; tope={max_pasos}")


def cotejar(n, max_pasos):
    valores, paridades = trayectoria(n, max_pasos)
    k = len(paridades)
    q = sum(paridades)
    assert 3 ** q < 2 ** k <= 2 * 3 ** q
    if n % 2 == 0:
        assert (k, q, valores[-1]) == (1, 0, n // 2)
        return {"k": k, "q": q, "valor": valores[-1], "bloques": []}
    grupos = [(bit, len(list(grupo))) for bit, grupo in groupby(paridades)]
    assert len(grupos) % 2 == 0 and grupos[0][0] == 1 and grupos[-1][0] == 0
    posicion = 0
    impares = 0
    bloques = []
    m = (n + 1).bit_length()
    cota = 0
    for i in range(len(grupos) // 2):
        bit_impar, a = grupos[2 * i]
        bit_par, b = grupos[2 * i + 1]
        assert (bit_impar, bit_par) == (1, 0) and a >= 1 and b >= 1
        inicio = valores[posicion]
        cima = valores[posicion + a]
        final = valores[posicion + a + b]
        assert 2 ** posicion <= 3 ** impares
        assert 2 ** a * (cima + 1) == 3 ** a * (inicio + 1)
        assert (inicio + 1) % (2 ** a) == 0
        assert 2 ** b * final == cima
        assert 2 ** impares * (inicio + 1) <= 3 ** impares * (n + 1)
        assert 2 ** (impares + a) <= (n + 1) * 3 ** impares
        assert 2 ** (posicion + a + b) * final + 2 ** (posicion + a) == (
            3 ** a * 2 ** posicion * (inicio + 1))
        posicion += a + b
        impares += a
        assert 2 ** posicion * final < 3 ** impares * (n + i + 1)
        cota = (5 * m + 8 * cota - 1) // 5
        assert impares <= cota
        bloques.append([a, b])
    assert (posicion, impares) == (k, q)
    assert 2 ** k < 2 * 3 ** q
    return {"k": k, "q": q, "valor": valores[-1], "bloques": bloques}


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--hasta", type=int, required=True)
    analizador.add_argument("--max-pasos", type=int, required=True)
    analizador.add_argument("--salida", type=Path)
    opciones = analizador.parse_args()
    if opciones.hasta < 39 or opciones.max_pasos < 1:
        analizador.error("hasta>=39 para incluir bordes; max-pasos>=1")
    cantidad_bloques = 0
    bordes = {}
    huella = hashlib.sha256()
    for n in range(2, opciones.hasta + 1):
        fila = cotejar(n, opciones.max_pasos)
        cantidad_bloques += len(fila["bloques"])
        huella.update((str(n) + ":" + json.dumps(fila, sort_keys=True) + "\n").encode())
        if n in (2, 3, 7, 39, opciones.hasta):
            bordes[n] = fila
    assert bordes[3]["bloques"] == [[2, 2]]
    assert bordes[7]["bloques"] == [[3, 1], [1, 2]]
    assert bordes[39]["bloques"] == [[3, 1], [2, 2]]
    for n in (0, 1):
        try:
            trayectoria(n, opciones.max_pasos)
        except ValueError:
            pass
        else:
            raise AssertionError("Dominio incorrectamente admitido")
    try:
        trayectoria(3, 1)
    except RuntimeError:
        pass
    else:
        raise AssertionError("Tope agotado incorrectamente admitido")
    datos = {
        "hasta_inclusivo": opciones.hasta,
        "max_pasos": opciones.max_pasos,
        "semillas": opciones.hasta - 1,
        "bloques_cotejados": cantidad_bloques,
        "bordes": bordes,
        "dominio_y_tope_comprobados": True,
        "fallos": 0,
        "sha256_filas": huella.hexdigest(),
        "sha256_programa": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "alcance": "Cotejo finito de formulas e indices; no prueba universal ni prueba de Rhin",
    }
    salida = json.dumps(datos, ensure_ascii=False, indent=2) + "\n"
    if opciones.salida:
        opciones.salida.write_text(salida, encoding="utf-8")
    print(salida, end="")


if __name__ == "__main__":
    main()
