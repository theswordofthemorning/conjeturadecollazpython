"""Comprueba JinetasPrefijos desde la fuente, sin cachés locales de la casa."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


def huella(ruta):
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    carpeta = Path(__file__).resolve().parent
    formal = carpeta.parent / "gao20260920/formal"
    fuente = carpeta / "JinetasPrefijos.lean"
    version = subprocess.run(["lake", "env", "lean", "--version"], cwd=formal,
                             check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()
    proceso = subprocess.run(["lake", "env", "lean", str(fuente)], cwd=formal,
                             capture_output=True, text=True, encoding="utf-8")
    salida = proceso.stdout + proceso.stderr
    assert proceso.returncode == 0, salida
    assert not re.search(r"\b(?:warning|error):|sorry", salida), salida
    codigo = fuente.read_text(encoding="utf-8")
    assert not re.search(r"\b(?:sorry|sorryAx|admit|axiom|native_decide|implemented_by|extern|unsafe)\b", codigo)
    pedidas = re.findall(r"^#print axioms (\S+)", codigo, re.MULTILINE)
    patron = r"^'([^']+)' (?:depends on axioms: \[(.*?)\]|does not depend on any axioms)"
    axiomas = {nombre: sorted(a.strip() for a in (lista or "").split(",") if a.strip())
               for nombre, lista in re.findall(patron, salida, re.MULTILINE | re.DOTALL)}
    assert sorted(pedidas) == sorted(axiomas) and pedidas
    assert all(set(lista) <= {"propext", "Classical.choice", "Quot.sound"}
               for lista in axiomas.values())
    evidencia = dict(version_lean=version, sha256_fuente=huella(fuente),
                     sha256_comprobador=huella(Path(__file__)),
                     sha256_toolchain=huella(formal / "lean-toolchain"),
                     sha256_mathlib_manifest=huella(formal / "lake-manifest.json"),
                     consultas=len(pedidas), axiomas=axiomas, salida=salida)
    argumentos.salida.parent.mkdir(parents=True, exist_ok=True)
    argumentos.salida.write_text(json.dumps(evidencia, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(version)
    print(f"OK: {len(pedidas)} consultas; sólo axiomas estándar; sin avisos.")


if __name__ == "__main__":
    main()
