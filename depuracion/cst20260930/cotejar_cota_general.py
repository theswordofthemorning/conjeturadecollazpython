"""Contraste entero y racional de la cota general; no es una prueba orbital.

Los polinomios verifican exactamente los margenes usados en las inducciones.
La malla de recurrencias contrasta bordes; Lean certifica los cuantificadores.
"""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def producto(a, b):
    resultado = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            resultado[i + j] += x * y
    return resultado


def diferencia(a, b):
    return [x - y for x, y in zip(a, b)]


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    # Coeficientes en orden creciente, sin llamar a Lean ni a su generador.
    margen_r = diferencia([2 * x for x in producto([65, 2], [65, 2])],
                          producto([67, 2], [67, 2]))
    margen_t = diferencia([2 * x for x in producto([33, 1], [33, 1])],
                          producto([34, 1], [34, 1]))
    margen_m = diferencia(producto([33, 1], [33, 1]), [1, 1, 0])
    assert margen_r == [3961, 252, 4]
    assert margen_t == [1022, 64, 1]
    assert margen_m == [1088, 65, 1]
    assert min(margen_r + margen_t + margen_m) >= 0
    margen_base = 2 ** 32 - (40 * 65 ** 2 + 1)
    assert margen_base > 0
    casos = 0
    for m in (0, 1, 2, 3, 16, 1000):
        cota, geometrica = 0, Fraction(0)
        for r in range(101):
            assert cota <= geometrica <= (2 ** r - 1) * m
            assert 40 * 2 ** r * (2 * r + 65) ** 2 + 1 < 2 ** (2 * r + 32)
            casos += 1
            # La resta truncada coincide con el dominio natural de Lean.
            cota = max(5 * m + 8 * cota - 1, 0) // 5
            geometrica = m + Fraction(8, 5) * geometrica
    salida = {
        "resultado": "sin discrepancias",
        "margen_base": margen_base,
        "polinomios_positivos": {"paso_r": margen_r, "paso_t": margen_t, "dominio_m": margen_m},
        "casos_recurrencia": casos,
        "rango_r": [0, 100], "valores_m": [0, 1, 2, 3, 16, 1000],
        "limite": "Identidades exactas y malla de bordes; la universalidad corresponde a la derivacion escrita y a Lean. No es un censo de Collatz.",
        "sha256_cotejador": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    argumentos.salida.write_text(json.dumps(salida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(salida, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
