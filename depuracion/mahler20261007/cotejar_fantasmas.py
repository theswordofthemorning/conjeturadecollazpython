"""Cotejo exacto del diccionario cohete <-> Mahler (idea documentada, sin desarrollar).

Mapa: T(x) = x/2 si x es par y (3x+1)/2 si es impar, sobre los enteros
(también negativos). P_k = 3^S_k / 2^k es el pronóstico y
R_k = T^k(x) / P_k el tamaño normalizado. Todo con Fraction: sin coma flotante.

Comprueba, en tramos finitos:
1. T^k(x) = P_k * R_k y R_k = x + (1/3) * suma de 1/P_j sobre los j < k impares.
2. Para x > 0, R_k nunca baja de x y nunca disminuye.
3. Fantasmas con pronóstico creciente y valor acotado: R_k tiende a 0.
   -1: R_k = -(2/3)^k exacto.  -5 -> -7 -> -10: R_3m = -5 (8/9)^m.
   -17 (11 pasos, 7 impares): R_11m = -17 (2048/2187)^m.
4. La cola: para k <= K, T^k(x) = R_K P_k - (1/3) suma_{k<=j<K, impar} P_k/P_j,
   y la cola vale al menos 1/3 si T^k(x) es impar y k < K.

Un barrido finito no prueba nada universal; las identidades son algebra.
Uso:
python -B -X utf8 depuracion/mahler20261007/cotejar_fantasmas.py
    --pasos 330 --salida depuracion/mahler20261007/cotejo_fantasmas.json
"""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def paso(x):
    if x % 2 == 0:
        return x // 2
    return (3 * x + 1) // 2


def recorrer(x0, pasos):
    """Devuelve valores x_k, pronósticos P_k y normalizados R_k para k = 0..pasos."""
    valores, pronosticos, normalizados = [x0], [Fraction(1)], [Fraction(x0)]
    for _ in range(pasos):
        x, p, r = valores[-1], pronosticos[-1], normalizados[-1]
        if x % 2 != 0:
            r = r + Fraction(1, 3) / p
            p = p * Fraction(3, 2)
        else:
            p = p / 2
        valores.append(paso(x))
        pronosticos.append(p)
        normalizados.append(r)
    return valores, pronosticos, normalizados


def cotejar_semilla(x0, pasos, cuentas):
    valores, pronosticos, normalizados = recorrer(x0, pasos)
    for k in range(pasos + 1):
        # 1. identidad multiplicativa y suma afín
        assert valores[k] == pronosticos[k] * normalizados[k]
        suma = sum((Fraction(1, 3) / pronosticos[j] for j in range(k) if valores[j] % 2 != 0),
                   Fraction(0))
        assert normalizados[k] == x0 + suma
        cuentas["identidades"] += 1
        # 2. para semillas positivas, R_k >= x0 y no disminuye
        if x0 > 0:
            assert normalizados[k] >= x0
            if k > 0:
                assert normalizados[k] >= normalizados[k - 1]
            cuentas["positivos"] += 1
    # 4. la cola, con R_K en el lugar del límite
    K = pasos
    for k in range(K + 1):
        cola = sum((Fraction(1, 3) * pronosticos[k] / pronosticos[j]
                    for j in range(k, K) if valores[j] % 2 != 0), Fraction(0))
        assert valores[k] == normalizados[K] * pronosticos[k] - cola
        if k < K and valores[k] % 2 != 0:
            assert cola >= Fraction(1, 3)
        cuentas["colas"] += 1
    return valores, pronosticos, normalizados


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--pasos", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    assert 33 <= args.pasos <= 2000

    cuentas = {"identidades": 0, "positivos": 0, "colas": 0, "fantasmas": 0}
    positivos = [3, 7, 27, 97, 871, 2 ** 20 - 1, 2 ** 64 - 1]
    negativos = [-1, -5, -7, -10, -17]
    resumen = {}
    for x0 in positivos + negativos:
        valores, pronosticos, normalizados = cotejar_semilla(x0, args.pasos, cuentas)
        # Sólo informativo: el valor aproximado de R al final del tramo.
        resumen[str(x0)] = {"R_final_aprox": "%.6g" % float(normalizados[-1]),
                            "valor_final": valores[-1]}

    # 3. Fantasmas: R_k tiende a 0 con fórmula exacta.
    valores, _, normalizados = recorrer(-1, args.pasos)
    for k in range(args.pasos + 1):
        assert valores[k] == -1 and normalizados[k] == -Fraction(2, 3) ** k
        cuentas["fantasmas"] += 1
    valores, _, normalizados = recorrer(-5, args.pasos)
    assert valores[:4] == [-5, -7, -10, -5]
    for m in range(args.pasos // 3 + 1):
        assert normalizados[3 * m] == -5 * Fraction(8, 9) ** m
        cuentas["fantasmas"] += 1
    valores, _, normalizados = recorrer(-17, args.pasos)
    vuelta = valores[:12]
    assert vuelta[0] == vuelta[11] == -17 and len(set(vuelta[:11])) == 11
    assert sum(1 for v in vuelta[:11] if v % 2 != 0) == 7
    for m in range(args.pasos // 11 + 1):
        assert normalizados[11 * m] == -17 * Fraction(2048, 2187) ** m
        cuentas["fantasmas"] += 1

    evidencia = {
        "estado": "cotejo exacto terminado",
        "sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "parametros": {"pasos": args.pasos},
        "semillas_positivas": positivos,
        "semillas_negativas": negativos,
        "cuentas": cuentas,
        "vuelta_menos_17": vuelta,
        "resumen": resumen,
        "alcance": "Identidades exactas en tramos finitos y fórmulas cerradas de los "
                   "fantasmas; no prueba que exista ni que no exista un cohete.",
    }
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(json.dumps(evidencia, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps(evidencia["cuentas"], ensure_ascii=False))
    print(json.dumps(evidencia["vuelta_menos_17"]))


if __name__ == "__main__":
    main()
