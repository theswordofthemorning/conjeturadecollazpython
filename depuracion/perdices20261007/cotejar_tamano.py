"""Contraste exacto del tamaño normalizado; no busca fugitivos infinitos.

Dos cálculos independientes: iteración entera con potencias, y actualización
afín con Fraction. También se contrasta el producto multiplicativo.
"""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def trayectoria(n, pasos):
    valores, subidas = [n], [0]
    for _ in range(pasos):
        x = valores[-1]
        valores.append(x // 2 if x % 2 == 0 else (3 * x + 1) // 2)
        subidas.append(subidas[-1] + x % 2)
    return valores, subidas


def contraste(n, pasos, nivel_max):
    valores, subidas = trayectoria(n, pasos)
    pronostico = Fraction(1)
    suma_afin, suma_inversa = Fraction(n), Fraction(0)
    producto = Fraction(n)
    impares = set()
    distintos = True
    bajos = [0] * (nivel_max + 1)
    vivo = True
    cuentas = {"identidades": 0, "productos": 0, "prefijos_vivos": 0,
               "cotas_por_bajos": 0, "cotas_regreso": 0, "cotas_sexta": 0}
    for k, x in enumerate(valores):
        p = Fraction(3 ** subidas[k], 2 ** k)
        r = Fraction(x, 1) / p
        assert p == pronostico
        assert r == suma_afin
        assert r <= n + suma_inversa / 3
        cuentas["identidades"] += 1
        if n > 0:
            assert r == producto
            cuentas["productos"] += 1
            if distintos:
                assert all(a >= 2 * i + 1 for i, a in enumerate(sorted(impares), 1))
                assert r ** 6 <= n ** 6 * (len(impares) + 1)
                cuentas["cotas_sexta"] += 1
        # vivo incluye exactamente los tiempos anteriores a k.
        if vivo:
            cuentas["prefijos_vivos"] += 1
            for c in range(nivel_max + 1):
                cota = n + (Fraction(bajos[c]) + Fraction(k, 3 ** c)) / 3
                assert r <= cota
                cuentas["cotas_por_bajos"] += 1
                if p <= 3 ** c:
                    assert x <= 3 ** c * r <= 3 ** c * cota
                    cuentas["cotas_regreso"] += 1
        if k == pasos:
            break
        vivo = vivo and p >= 1
        for c in range(nivel_max + 1):
            bajos[c] += p <= 3 ** c
        suma_inversa += 1 / pronostico
        if x % 2:
            distintos = distintos and x >= 3 and x not in impares
            impares.add(x)
            suma_afin += 1 / (3 * pronostico)
            if n > 0:
                producto *= 1 + Fraction(1, 3 * x)
            pronostico *= Fraction(3, 2)
        else:
            pronostico /= 2
    return cuentas


def fraccion(x):
    return [x.numerator, x.denominator]


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--n-max", type=int, required=True)
    analizador.add_argument("--pasos", type=int, required=True)
    analizador.add_argument("--nivel-max", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    assert 0 <= args.n_max <= 10000
    assert 0 <= args.pasos <= 300
    assert 0 <= args.nivel_max <= 10
    semillas = sorted(set(range(args.n_max + 1)) |
                      {2 ** b - 1 for b in (1, 2, 3, 10, 30, 64)})
    totales = {}
    for n in semillas:
        for nombre, cantidad in contraste(n, args.pasos, args.nivel_max).items():
            totales[nombre] = totales.get(nombre, 0) + cantidad

    # El inverso puede exceder 1 tras el cruce; n=1, k=2 es el borde mínimo.
    valores, subidas = trayectoria(1, 2)
    p = Fraction(3 ** subidas[2], 4)
    assert p == Fraction(3, 4) and 1 / p > 1
    # Factor 1/3 e índice anterior al paso impar: n=3, primer paso.
    assert Fraction(5, 1) / Fraction(3, 2) == 3 + Fraction(1, 3)
    # Telescopio exacto y expansión independiente del factor de sexta raíz.
    telescopio = Fraction(1)
    for r in range(1, 501):
        factor = 1 + Fraction(1, 6 * r + 3)
        assert factor ** 6 <= Fraction(r + 1, r)
        telescopio *= factor
        assert telescopio ** 6 <= r + 1
        diferencia = (r + 1) * (6 * r + 3) ** 6 - r * (6 * r + 4) ** 6
        assert diferencia == (729 + 5381 * r + 15624 * r ** 2 + 22140 * r ** 3
                              + 15120 * r ** 4 + 3888 * r ** 5)

    evidencia = {
        "estado": "contraste exacto terminado",
        "sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "parametros": {"n_max": args.n_max, "pasos": args.pasos,
                       "nivel_max": args.nivel_max},
        "semillas": len(semillas), "cuentas": totales,
        "factores_y_telescopios_sexta": 500,
        "control_tras_cruce": {"n": 1, "k": 2, "pronostico": fraccion(p)},
        "alcance": "Contraste finito; sublinealidad en Lean, cota de sexta raíz con prueba escrita.",
    }
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(json.dumps(evidencia, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps(evidencia, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
