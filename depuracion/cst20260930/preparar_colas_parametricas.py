"""Propone certificados enteros de colas para limites arbitrarios de rachas.

El modulo generado aplica el teorema parametrico; cada desigualdad
numerica vuelve a comprobarse en el nucleo de Lean.
"""

import argparse
import hashlib
import json
from pathlib import Path


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--rachas", type=int, nargs="+", required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    analizador.add_argument("--lean", type=Path, required=True)
    argumentos = analizador.parse_args()
    filas = []
    lineas = ["import OcelotasColaParametrica", "",
              "/-! Certificados de colas, sin afirmar descenso en los tiempos restantes. -/",
              "namespace OcelotasColasCertificadas",
              "open Ocelotas OcelotasContador OcelotasLMNFuente", "",
              "set_option maxRecDepth 100000", "set_option maxHeartbeats 1000000", ""]
    for r in sorted(set(argumentos.rachas)):
        assert 1 <= r <= 10000
        numerador, denominador = 5 * (8 ** r - 5 ** r), 3 * 5 ** r
        a = (numerador + denominador - 1) // denominador
        c = (r - 1).bit_length()
        h = 0
        while 8 * a * (19 * (h + 33) ** 2 + c + 1) + 5 >= 5 * 2 ** h:
            h += 1
        margen = 5 * 2 ** h - (8 * a * (19 * (h + 33) ** 2 + c + 1) + 5)
        filas.append({"R": r, "A": a, "c": c, "H": h,
                      "exponente_semilla": 19 * (h + 32) ** 2 + c,
                      "margen_base": margen})
        lineas.extend([f"theorem region_{r} (hL : LMN23) {{n k : ℕ}} (hn : 2 ≤ n)",
            f"    (hk : PrimerCruce n k) (hr : rachas n k ≤ {r}) (hf : n ≤ T^[k] n) :",
            f"    k < 2 ^ {h} ∧ n < 2 ^ (19 * ({h} + 32) ^ 2 + {c}) :=",
            f"  OcelotasColaParametrica.region_del_fallo_corolario (R := {r})",
            f"    (A := {a}) (c := {c}) (H := {h}) hL",
            "    (by decide +kernel) (by decide +kernel) (by decide +kernel) hn hk hr hf", ""])
    lineas.append("end OcelotasColasCertificadas")
    for fila in filas:
        lineas.append(f"#print axioms OcelotasColasCertificadas.region_{fila['R']}")
    argumentos.lean.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    datos = {"estado": "constantes propuestas; Lean comprueba las desigualdades",
             "filas": filas, "sha256_generador": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             "sha256_lean": hashlib.sha256(argumentos.lean.read_bytes()).hexdigest()}
    argumentos.salida.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for fila in filas:
        print(f"R={fila['R']}: H={fila['H']}, exponente de semilla={fila['exponente_semilla']}.")


if __name__ == "__main__":
    main()
