"""Localiza intervalos que superan el limite externo; no es un cierre Lean."""

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
    analizador.add_argument("--rachas", type=int, nargs="+", required=True)
    analizador.add_argument("--logaritmos", type=Path, required=True)
    analizador.add_argument("--limite-externo", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    datos_log = json.loads(argumentos.logaritmos.read_text(encoding="utf-8"))
    di, ds = [Fraction(datos_log["dos"][k]) for k in ("inferior", "superior")]
    ti, ts = [Fraction(datos_log["tres"][k]) for k in ("inferior", "superior")]
    resultados = []
    for R in argumentos.rachas:
        assert 1 <= R <= 100
        A = techo(Fraction(5 * (8 ** R - 5 ** R), 3 * 5 ** R))
        c, H = (R - 1).bit_length(), 0
        while 8 * A * (19 * (H + 33) ** 2 + c + 1) + 5 >= 5 * 2 ** H:
            H += 1
        intervalos = intervalos_superiores(ti / ds, ts / di, 2 ** H)
        fuera, maximo = [], 0
        for j, fila in enumerate(intervalos):
            P, Q = fila["superior"]
            p, v = fila["inferior"]
            error = P * di - Q * ts
            assert error > 0 and p * ds - v * ti < 0
            s = techo(R / error)
            _, beta = log2_encerrado(s, 96, 64)
            B = techo(256 * beta)
            cota = cota_afinada(R, Fraction(B, 256), Fraction(317, 200))
            if cota >= fila["q_inicio"]:
                maximo = max(maximo, s)
                if s > argumentos.limite_externo + 1:
                    fuera.append({"intervalo": j, **fila, "lambda_inferior": str(error),
                                  "semilla_exclusiva": s, "B": B, "cota_q": cota,
                                  "inicio_semilla": argumentos.limite_externo + 1,
                                  "limite_semilla": s - 1})
        resultado = {"R": R, "A": A, "c": c, "H": H, "numero_intervalos": len(intervalos),
                     "cola_desde_q": intervalos[-1]["q_fin"], "semilla_exclusiva": maximo,
                     "intervalos_fuera": fuera}
        resultados.append(resultado)
        print(f"R={R}: H={H}, semilla<{maximo}, {len(fuera)} intervalos fuera.")
    salida = {"estado": "exploracion exacta, no cotejada independientemente ni formalizada",
              "limite_externo": argumentos.limite_externo, "resultados": resultados,
              "sha256_script": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    argumentos.salida.write_text(json.dumps(salida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
