"""Cotejo independiente de las constantes, mediante suma racional iterada."""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--certificado", type=Path, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    datos = json.loads(argumentos.certificado.read_text(encoding="utf-8"))
    resultados = []
    for fila in datos["filas"]:
        R, A, c, H = [fila[k] for k in ("R", "A", "c", "H")]
        suma = Fraction(0)
        for _ in range(R):
            suma = 1 + Fraction(8, 5) * suma
        assert A - 1 < suma <= A
        assert R <= 1 << c and (c == 0 or 1 << (c - 1) < R)
        for h in range(H):
            assert 5 * (1 << h) <= 8 * A * (19 * (h + 33) ** 2 + c + 1) + 5
        margen = 5 * (1 << H) - 8 * A * (19 * (H + 33) ** 2 + c + 1) - 5
        assert margen == fila["margen_base"] > 0
        assert fila["exponente_semilla"] == 19 * (H + 32) ** 2 + c
        resultados.append({"R": R, "H": H, "resultado": "sin discrepancias"})
    salida = {"resultado": "sin discrepancias", "filas": resultados,
              "alcance": "Constantes exactas; la cola universal la demuestra Lean, no esta malla.",
              "sha256_certificado": hashlib.sha256(argumentos.certificado.read_bytes()).hexdigest(),
              "sha256_cotejador": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    argumentos.salida.write_text(json.dumps(salida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK: {len(resultados)} certificados, incluida la minimalidad de H para estas constantes.")


if __name__ == "__main__":
    main()
