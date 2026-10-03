"""Prepara constantes exactas para una tabla Lean de R rachas, sin certificarla."""

import argparse
from fractions import Fraction
import json
from pathlib import Path

from rachas_afinadas import cota_afinada, log2_encerrado
from rachas_unilaterales import intervalos_superiores
from rachas_convergentes import techo


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--rachas", type=int, required=True)
    analizador.add_argument("--bits-cola", type=int, required=True)
    analizador.add_argument("--bits-tabla", type=int,
                            help="Objetivo menor para tabla; exige puente por 3*q<2*k")
    analizador.add_argument("--tiempo-racional", type=int, nargs=2, metavar=("NUM", "DEN"),
                            help="Usar DEN*k<=NUM*q+DEN, comprobando 3^DEN<=2^NUM")
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    R, t = argumentos.rachas, argumentos.bits_cola
    assert 1 <= R <= 75 and 1 <= t <= 60
    bits_tabla = t if argumentos.bits_tabla is None else argumentos.bits_tabla
    assert 1 <= bits_tabla <= t
    inferior, superior = log2_encerrado(3, 128, 64)
    intervalos = intervalos_superiores(inferior, superior, 2 ** bits_tabla)
    dos_inf = Fraction("0.693147180559945309362")
    dos_sup = Fraction("0.693147180559945309471")
    tres_inf = Fraction("1.098612288668109691335")
    tres_sup = Fraction("1.098612288668109691454")
    alfa = Fraction(1585, 1000)
    assert tres_sup <= alfa * dos_inf
    filas, limite = [], 0
    for j, intervalo in enumerate(intervalos):
        P, Q = intervalo["superior"]
        p, q = intervalo["inferior"]
        c = P * dos_inf - Q * tres_sup
        assert c > 0 and p * dos_sup - q * tres_inf < 0
        semilla = techo(R / c)
        _, beta = log2_encerrado(semilla, 96, 64)
        B = techo(256 * beta)
        assert semilla ** 256 <= 2 ** B
        tope = cota_afinada(R, Fraction(B, 256), alfa)
        sobrevive = intervalo["q_inicio"] <= tope
        if sobrevive:
            limite = max(limite, semilla)
        filas.append({"intervalo": j, **intervalo, "lambda_inferior": str(c),
                      "semilla_exclusiva": semilla, "B": B,
                      "cota_q": tope, "sobrevive": sobrevive})
    G = Fraction(5 * (8 ** R - 5 ** R), 3 * 5 ** R)
    A = techo(G)
    desplazamiento = (R - 1).bit_length() + 1
    polinomio = 19 * (t + 33) ** 2 + desplazamiento
    if argumentos.tiempo_racional:
        numerador, denominador = argumentos.tiempo_racional
        assert 1 <= numerador <= 10000 and 1 <= denominador <= 10000
        assert 3 ** denominador <= 2 ** numerador
        assert numerador * A * polinomio + denominador < denominador * 2 ** t
    else:
        assert 2 * A * polinomio < 2 ** t
    if bits_tabla < t:
        assert argumentos.tiempo_racional and 2 ** 3 < 3 ** 2
        for exponente in range(bits_tabla, t):
            cota_tiempo = numerador * A * (19 * (exponente + 33) ** 2 + desplazamiento) + denominador
            assert 2 * cota_tiempo <= 3 * denominador * intervalos[-1]["q_fin"]
    salida = {"estado": "constantes propuestas; comprobar el modulo Lean generado",
              "rachas": R, "semilla_exclusiva": limite,
              "cola_desde_q": intervalos[-1]["q_fin"], "alfa": str(alfa),
              "denominador_beta": 256, "cola_bits": t, "cola_coeficiente": A,
              "cola_desplazamiento": desplazamiento, "filas": filas}
    if argumentos.tiempo_racional:
        salida["tiempo_racional"] = argumentos.tiempo_racional
    if argumentos.bits_tabla is not None:
        salida["tabla_bits"] = bits_tabla
        salida["puente_por_q"] = {"tiempo_inferior": [3, 2],
                                  "exponentes": list(range(bits_tabla, t))}
    argumentos.salida.write_text(json.dumps(salida, ensure_ascii=False, indent=2)
                                 + "\n", encoding="utf-8")
    print(f"R={R}: {len(filas)} filas; n<{limite}; cola q>={intervalos[-1]['q_fin']}.")
    print(f"Cola: A={A}, t>={t}, desplazamiento={desplazamiento}; base exacta valida.")


if __name__ == "__main__":
    main()
