"""Contrasta la criba con suelo por orbitas directas y Fraction.

T(n)=n/2 par; (3n+1)/2 impar. Solo se exige el suelo al comienzo de
cada bloque; se incluye el ultimo bloque aunque termine debajo del suelo.
El cotejo es finito y no sustituye los enunciados universales de Lean.
"""

import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--suelo", type=int, required=True)
    analizador.add_argument("--max-semilla", type=int, required=True)
    analizador.add_argument("--max-rachas", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    N = argumentos.suelo
    assert argumentos.max_semilla >= N >= 4095 and argumentos.max_rachas >= 1
    P, Q = 2 * N + 1, N + 1
    alfa, gamma = Fraction(317, 200), Fraction(4095, 4096)
    assert 2 ** 4095 * Q ** 4096 <= P ** 4096
    bordes = []
    for y in (N - 1, N, N + 1, 2 * N, 2 ** 64):
        margen = Q * (2 * y + 1) - P * (y + 1)
        assert margen == y - N and (margen >= 0) == (y >= N)
        bordes.append({"y": y, "margen": margen})
    conteos = {"semillas": 0, "bloques": 0, "pasos_T": 0,
               "pasos_suelo_comprobados": 0, "finales_bajo_suelo": 0,
               "igualdades_paso": 0, "igualdades_cota": 0}
    for n in range(N if N % 2 else N + 1, argumentos.max_semilla + 1, 2):
        conteos["semillas"] += 1
        x, A = n, 0
        cota, anterior, descontada = 0, 0, 0
        B = (((n + 1) ** 256) - 1).bit_length()
        beta = Fraction(B, 256)
        for i in range(argumentos.max_rachas):
            if x < N:
                break
            assert P ** i * 2 ** A * (x + 1) <= Q ** i * 3 ** A * (n + 1)
            y, a, b = x, 0, 0
            while y % 2:
                y = (3 * y + 1) // 2
                a += 1
                conteos["pasos_T"] += 1
            z = y
            while y % 2 == 0:
                assert y > 0
                y //= 2
                b += 1
                conteos["pasos_T"] += 1
            assert a >= 1 and b >= 1
            assert 2 ** a * (z + 1) == 3 ** a * (x + 1)
            assert z == 2 ** b * y
            assert 2 ** a <= x + 1
            assert P ** i * 2 ** (A + a) <= (n + 1) * Q ** i * 3 ** A
            if y >= N:
                izquierda = P * 2 ** a * (y + 1)
                derecha = Q * 3 ** a * (x + 1)
                assert izquierda <= derecha
                conteos["pasos_suelo_comprobados"] += 1
                conteos["igualdades_paso"] += izquierda == derecha
            else:
                conteos["finales_bajo_suelo"] += 1
            nueva = math.floor(beta + alfa * cota - gamma * i)
            numerador = 400 * B + 162304 * cota - 102375 * i
            assert numerador >= 0 and nueva == numerador // 102400
            assert 2 * (i + 1) <= nueva and cota <= nueva
            anterior = math.floor(beta + alfa * anterior)
            descontada = math.floor(beta - 1 + alfa * descontada)
            A, cota, x = A + a, nueva, y
            assert A <= cota <= i + 1 + descontada <= anterior
            conteos["igualdades_cota"] += A == cota
            conteos["bloques"] += 1
    salida = {
        "resultado": "sin discrepancias", "suelo": N,
        "max_semilla": argumentos.max_semilla, "max_rachas": argumentos.max_rachas,
        "gamma": str(gamma), "gamma_comprobada_por_potencia": True,
        "conteos": conteos, "bordes_razon": bordes,
        "alcance": "Cotejo finito. Incluye bloques finales que bajan del suelo; no supone llegada a 1 ni ley probabilistica.",
        "sha256_cotejador": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    argumentos.salida.write_text(json.dumps(salida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(salida, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
