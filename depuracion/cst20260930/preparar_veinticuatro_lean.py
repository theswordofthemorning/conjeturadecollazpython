"""Propone la tabla de 24 rachas usando logaritmos de 55 decimales.

El rango hasta 4912740 ya esta certificado en Lean en el repositorio.
No se usa el resultado finito externo de Rozier-Terracol.
"""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

from rachas_afinadas import cota_afinada, log2_encerrado
from rachas_unilaterales import intervalos_superiores


def techo(x):
    return (x.numerator + x.denominator - 1) // x.denominator


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--logaritmos", type=Path, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    datos_log = json.loads(argumentos.logaritmos.read_text(encoding="utf-8"))
    dos_inf, dos_sup = [Fraction(datos_log["dos"][k]) for k in ("inferior", "superior")]
    tres_inf, tres_sup = [Fraction(datos_log["tres"][k]) for k in ("inferior", "superior")]
    A = techo(Fraction(5 * (8 ** 24 - 5 ** 24), 3 * 5 ** 24))
    c, H = 5, 35
    assert 8 * A * (19 * (H + 33) ** 2 + c + 1) + 5 < 5 * 2 ** H
    cola = {"R": 24, "A": A, "c": c, "H": H}
    intervalos = intervalos_superiores(tres_inf / dos_sup, tres_sup / dos_inf, 2 ** cola["H"])
    filas, limite = [], 0
    for j, intervalo in enumerate(intervalos):
        P, Q = intervalo["superior"]
        p, q = intervalo["inferior"]
        c = P * dos_inf - Q * tres_sup
        assert c > 0 and p * dos_sup - q * tres_inf < 0
        semilla = techo(24 / c)
        _, beta = log2_encerrado(semilla, 96, 64)
        B = techo(256 * beta)
        assert semilla ** 256 <= 2 ** B
        tope = cota_afinada(24, Fraction(B, 256), Fraction(317, 200))
        sobrevive = intervalo["q_inicio"] <= tope
        if sobrevive:
            limite = max(limite, semilla)
        filas.append({"intervalo": j, **intervalo, "lambda_inferior": str(c),
                      "semilla_exclusiva": semilla, "B": B,
                      "cota_q": tope, "sobrevive": sobrevive})
    interno = 4912740
    salida = {"estado": "tabla propuesta; pendiente de cotejo y Lean", "rachas": 24,
              "cola": cola, "cola_desde_q": intervalos[-1]["q_fin"],
              "semilla_exclusiva": limite, "limite_certificado_inclusivo": interno,
              "cierra_con_limite_certificado": limite <= interno + 1,
              "intervalos_por_prefijos": [f["intervalo"] for f in filas if f["sobrevive"] and f["semilla_exclusiva"] > interno + 1],
              "logaritmos": datos_log, "filas": filas,
              "sha256_generador": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    argumentos.salida.write_text(json.dumps(salida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"R=24: {len(filas)} filas, q<{salida['cola_desde_q']}, n<{limite}.")
    print(f"Comparacion con el limite interno: {salida['cierra_con_limite_certificado']}.")


if __name__ == "__main__":
    main()
