"""Compila el criterio de altura BAB y el presupuesto de dos cambios."""

import argparse
import hashlib
import json
from pathlib import Path
import re

from comprobar_transporte_impar import CARPETA, FORMAL, RAIZ, ejecutar, huella


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    fuente = CARPETA / "PerdicesAlturaBAB.lean"
    codigo = fuente.read_text(encoding="utf-8")
    consultas = re.findall(r"^#print axioms (\S+)$", codigo, re.MULTILINE)
    assert len(consultas) == 8
    version = ejecutar(["lake", "env", "lean", "--version"], FORMAL).strip()
    assert version.startswith("Lean (version 4.32.2,")
    manifiesto = json.loads((FORMAL / "lake-manifest.json").read_text(encoding="utf-8"))
    revision = next(p["rev"] for p in manifiesto["packages"] if p["name"] == "mathlib")
    mathlib = FORMAL / ".lake/packages/mathlib"
    assert ejecutar(["git", "rev-parse", "HEAD"], mathlib).strip() == revision
    dependencias = {}
    for nombre in re.findall(r"^import (\S+)$", codigo, re.MULTILINE):
        assert nombre.startswith("Mathlib.")
        relativa = Path(*nombre.split("."))
        original = ejecutar(["git", "show", revision+":"+relativa.with_suffix(".lean").as_posix()], mathlib)
        ruta = mathlib / relativa.with_suffix(".lean")
        assert hashlib.sha256(original.replace("\r\n", "\n").encode()).hexdigest() == huella(ruta)
        objeto = mathlib / ".lake/build/lib/lean" / relativa.with_suffix(".olean")
        dependencias[nombre] = dict(fuente_sha256_lf=huella(ruta),
                                   objeto_sha256=hashlib.sha256(objeto.read_bytes()).hexdigest())
    antes = huella(fuente)
    salida = ejecutar(["lake", "env", "lean", str(fuente)], FORMAL)
    assert antes == huella(fuente)
    assert all(texto not in salida for texto in ("sorryAx", "error:", "warning:"))
    axiomas = {}
    for linea in salida.splitlines():
        coincidencia = re.fullmatch(r"'([^']+)' depends on axioms: \[([^]]*)\]", linea)
        assert coincidencia, linea
        nombre, lista = coincidencia.groups()
        valores = lista.split(", ") if lista else []
        assert nombre not in axiomas and set(valores) <= {"propext", "Classical.choice", "Quot.sound"}
        axiomas[nombre] = valores
    assert list(axiomas) == consultas
    texto = args.salida.with_suffix(".txt")
    texto.write_text(salida, encoding="utf-8")
    resultado = dict(version_lean=version, revision_mathlib=revision,
                     alcance="Producto impar desde identidades BAB, criterio C18 y cierre lineal epsilon=7/17. "
                             "El enlace orbital de las rachas y la parametrización BAB conservan prueba escrita. "
                             "Imports directos cotejados, sin auditoría transitiva completa de Mathlib.",
                     fuente=fuente.relative_to(RAIZ).as_posix(), fuente_sha256_lf=antes,
                     verificador_sha256_lf=huella(Path(__file__)),
                     utilidades_sha256_lf=huella(CARPETA / "comprobar_transporte_impar.py"),
                     salida_sha256_lf=huella(texto), dependencias=dependencias, axiomas=axiomas)
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(f"OK: Lean 4.32.2, {len(axiomas)} consultas, sólo axiomas estándar.")


if __name__ == "__main__":
    main()
