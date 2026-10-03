"""Prepara un certificado pequeno para la futura extension Lean a 13 rachas.

No genera ni afirma una prueba Lean completa. Usa las cotas de log 2 y
log 3 ya demostradas en OcelotasLMN, alfa=1585/1000 y beta=B/256;
log(s)<=beta*log(2) se comprueba mediante s^256<=2^B, en enteros.
"""

import argparse
from fractions import Fraction
import json
from pathlib import Path

from rachas_afinadas import cota_afinada, log2_encerrado
from rachas_unilaterales import intervalos_superiores
from rachas_convergentes import cola_con_lmn, techo


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    inferior, superior = log2_encerrado(3, 128, 64)
    intervalos = intervalos_superiores(inferior, superior, 2 ** 27)
    dos_inf = Fraction("0.693147180559945309362")
    dos_sup = Fraction("0.693147180559945309471")
    tres_inf = Fraction("1.098612288668109691335")
    tres_sup = Fraction("1.098612288668109691454")
    alfa = Fraction(1585, 1000)
    assert tres_sup <= alfa * dos_inf
    filas = []
    limite = 0
    for j, intervalo in enumerate(intervalos):
        P, Q = intervalo["superior"]
        p, q = intervalo["inferior"]
        c = P * dos_inf - Q * tres_sup
        assert c > 0 and p * dos_sup - q * tres_inf < 0
        semilla = techo(13 / c)
        _, beta = log2_encerrado(semilla, 96, 64)
        B = techo(256 * beta)
        assert semilla ** 256 <= 2 ** B
        tope = cota_afinada(13, Fraction(B, 256), alfa)
        sobrevive = intervalo["q_inicio"] <= tope
        if sobrevive:
            limite = max(limite, semilla)
        filas.append({"intervalo": j, **intervalo, "lambda_inferior": str(c),
                      "semilla_exclusiva": semilla, "B": B,
                      "cota_q": tope, "sobrevive": sobrevive})
    cola = intervalos[-1]["q_fin"]
    assert cola_con_lmn(13, cola, Fraction(693, 1000), Fraction(6932, 10000))
    G = Fraction(5 * (8 ** 13 - 5 ** 13), 3 * 5 ** 13)
    assert G < 751
    # Base de la induccion de cola que falta trasladar a Lean.
    assert 1502 * (19 * (27 + 33) ** 2 + 5) < 2 ** 27
    salida = {"estado": "preparacion exacta; no es certificado Lean",
              "rachas": 13, "semilla_exclusiva": limite,
              "cola_desde_q": cola, "alfa": str(alfa), "denominador_beta": 256,
              "filas": filas,
              "pendiente": ["certificar las 40 filas en Lean",
                            "extender la cola LMN a 13 rachas",
                            "certificar semillas hasta 31623 en el nucleo",
                            "ensamblar CST con el contador"]}
    argumentos.salida.write_text(json.dumps(salida, ensure_ascii=False, indent=2)
                                 + "\n", encoding="utf-8")
    print(f"{len(filas)} intervalos; n<{limite}; cola desde q={cola}.")
    print("Todas las comparaciones de potencias exactas pasan; Lean completo pendiente.")


if __name__ == "__main__":
    main()
