"""Comprueba que los tramos del censo son contiguos desde --desde y que cada uno
recorrió exactamente las semillas de las clases sin cruce mod 2^24 de su rango.
Las clases que cruzan quedan decididas por la fórmula exacta de censo_cst.py."""

import argparse
import json
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from censo_cst import clases  # noqa: E402

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("--carpeta", type=Path, required=True)
ap.add_argument("--desde", type=int, required=True)
ap.add_argument("--tramos", type=int, default=6)
arg = ap.parse_args()
AQUI = arg.carpeta

r, cruce, S, x, vivo = clases(24)
U = r[vivo].astype(np.int64)
M = 1 << 24
prev = arg.desde - 1
filas = []
for i in range(1, arg.tramos + 1):
    d = json.loads((AQUI / f"tramo_{i}.json").read_text(encoding="utf-8"))
    a, b = d["desde"], d["N"]
    esperado = int(((b - U) // M - (a - 1 - U) // M).sum())
    filas.append({"tramo": i, "desde": a, "hasta": b, "contiguo": a == prev + 1,
                  "recorridos": d["recorridos_individuales"], "esperados": esperado,
                  "fallos": d["numero_fallos"], "umbral": d["comprobados_por_umbral"]})
    prev = b
ok = all(f["contiguo"] and f["recorridos"] == f["esperados"] and f["fallos"] == 0 for f in filas)
salida = {"desde": arg.desde, "hasta": prev, "clases_sin_cruce": len(U), "tramos": filas,
          "resultado": "cubre sin fallos" if ok else "FALLA"}
(AQUI / "cobertura.json").write_text(json.dumps(salida, indent=2) + "\n", encoding="utf-8")
print(salida["resultado"], salida["hasta"])
