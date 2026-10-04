"""Cotejo finito independiente del suelo tras cortes pares.

Atajo T(n)=n/2 si par y (3n+1)/2 si impar. El primer cruce se
detecta con potencias enteras. No importa generadores ni verificadores.
"""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--inicio", type=int, required=True)
    analizador.add_argument("--limite", type=int, required=True)
    analizador.add_argument("--max-pasos", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    assert 4095 <= argumentos.inicio <= argumentos.limite
    assert argumentos.max_pasos > 0
    alfa, gamma = Fraction(317, 200), Fraction(4095, 4096)
    assert 2 ** 4095 * 4096 ** 4096 <= 8191 ** 4096
    conteos = {"semillas": 0, "pasos_T": 0, "cortes": 0,
               "cortes_vacios": 0, "cortes_interiores": 0,
               "sufijos_iniciados_en_par": 0, "sufijos_sin_impares": 0,
               "cruces_finales_bajo_suelo": 0, "cotas_comprobadas": 0,
               "congruencias_comprobadas": 0}
    bordes = []
    for n in range(argumentos.inicio, argumentos.limite + 1):
        valores, bits, sumas, rachas = [n], [], [0], [0]
        potencia_tres, potencia_dos = 1, 1
        for _ in range(argumentos.max_pasos):
            x = valores[-1]
            impar = x % 2
            rachas.append(rachas[-1] + int(impar == 1 and (not bits or bits[-1] == 0)))
            bits.append(impar)
            sumas.append(sumas[-1] + impar)
            valores.append((3 * x + 1) // 2 if impar else x // 2)
            potencia_tres *= 3 if impar else 1
            potencia_dos *= 2
            if potencia_tres < potencia_dos:
                break
        else:
            raise AssertionError(f"Primer cruce no encontrado con el limite dado: {n}")
        k = len(bits)
        assert bits[-1] == 0 and min(valores[:-1]) >= n >= 4095
        conteos["semillas"] += 1
        conteos["pasos_T"] += k
        conteos["cruces_finales_bajo_suelo"] += valores[-1] < 4095
        for i in range(k):
            if i > 0 and bits[i - 1] != 0:
                continue
            sufijo = bits[i:]
            restantes = sum(bit == 1 and (j == 0 or sufijo[j - 1] == 0)
                            for j, bit in enumerate(sufijo))
            assert rachas[-1] == rachas[i] + restantes
            assert sumas[-1] == sumas[i] + sum(sufijo)
            assert min(valores[i:k]) >= 4095
            conteos["cortes"] += 1
            conteos["cortes_vacios"] += i == 0
            conteos["cortes_interiores"] += i > 0
            conteos["sufijos_iniciados_en_par"] += sufijo[0] == 0
            conteos["sufijos_sin_impares"] += restantes == 0
            longitudes = []
            for j, bit in enumerate(sufijo):
                if bit:
                    if j == 0 or sufijo[j - 1] == 0:
                        longitudes.append(0)
                    longitudes[-1] += 1
            acumulada = 0
            for j, longitud in enumerate(longitudes):
                # Congruencia derivada de los bloques reales del sufijo,
                # incluyendo posibles entradas pares iniciales.
                assert 8191 ** j * 2 ** (acumulada + longitud) <= (
                    (valores[i] + 1) * 4096 ** j * 3 ** acumulada)
                acumulada += longitud
                conteos["congruencias_comprobadas"] += 1
            for holgura in (0, 1):
                maximo = valores[i] + holgura
                potencia = (maximo + 1) ** 256
                B = (potencia - 1).bit_length()
                assert B >= 512 and 2 ** (B - 1) < potencia <= 2 ** B
                beta = Fraction(B, 256)
                entero, racional = 0, 0
                for j in range(restantes + 2):
                    if j >= restantes:
                        assert sumas[-1] <= sumas[i] + entero
                        conteos["cotas_comprobadas"] += 1
                    numerador = 400 * B + 162304 * entero - 102375 * j
                    assert numerador >= 0
                    nuevo_racional = beta + alfa * racional - gamma * j
                    racional = nuevo_racional.numerator // nuevo_racional.denominator
                    entero = numerador // 102400
                    assert entero == racional and entero >= 2 * (j + 1)
        if n in (argumentos.inicio, argumentos.inicio + 1, argumentos.limite):
            bordes.append({"n": n, "k": k, "impares": sumas[-1],
                           "rachas": rachas[-1], "valor_final": valores[-1]})
    salida = {
        "resultado": "sin discrepancias", "inicio": argumentos.inicio,
        "limite": argumentos.limite, "max_pasos": argumentos.max_pasos,
        "conteos": conteos, "bordes": bordes,
        "alcance": "Cotejo finito de todos los cortes admisibles; incluye pares iniciales, resto sin rachas, dos cotas de valor y dos presupuestos de rachas. No prueba existencia universal del primer cruce.",
        "sha256_cotejador": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    argumentos.salida.write_text(json.dumps(salida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(salida, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
