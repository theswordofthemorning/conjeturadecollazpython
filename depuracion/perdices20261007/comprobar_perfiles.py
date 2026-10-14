"""Compila PerdicesPerfiles desde fuente y audita sus doce consultas de axiomas."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


CARPETA = Path(__file__).resolve().parent
RAIZ = CARPETA.parents[1]
FORMAL = RAIZ / "depuracion/gao20260920/formal"


def ejecutar(argumentos, carpeta):
    resultado = subprocess.run(argumentos, cwd=carpeta, check=True, capture_output=True,
                               text=True, encoding="utf-8")
    assert not resultado.stderr, resultado.stderr
    return resultado.stdout


def huella(ruta):
    return hashlib.sha256(ruta.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    fuente = CARPETA / "PerdicesPerfiles.lean"
    codigo = fuente.read_text(encoding="utf-8")
    consultas = re.findall(r"^#print axioms (\S+)$", codigo, re.MULTILINE)
    assert len(consultas) == 12
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
        original = ejecutar(["git", "show", revision + ":" +
                              relativa.with_suffix(".lean").as_posix()], mathlib)
        ruta = mathlib / relativa.with_suffix(".lean")
        assert hashlib.sha256(original.replace("\r\n", "\n").encode()).hexdigest() == huella(ruta)
        objeto = mathlib / ".lake/build/lib/lean" / relativa.with_suffix(".olean")
        dependencias[nombre] = dict(fuente_sha256_lf=huella(ruta),
                                   objeto_sha256=hashlib.sha256(objeto.read_bytes()).hexdigest())
    antes = huella(fuente)
    salida = ejecutar(["lake", "env", "lean", str(fuente)], FORMAL)
    assert antes == huella(fuente)
    assert "sorryAx" not in salida and "error:" not in salida and "warning:" not in salida
    axiomas = {}
    for linea in salida.splitlines():
        coincidencia = re.fullmatch(r"'([^']+)' depends on axioms: \[([^]]*)\]", linea)
        sin_axiomas = re.fullmatch(r"'([^']+)' does not depend on any axioms", linea)
        if coincidencia:
            nombre, lista = coincidencia.groups()
            valores = lista.split(", ") if lista else []
        else:
            assert sin_axiomas, linea
            nombre, valores = sin_axiomas.group(1), []
        assert nombre not in axiomas
        assert set(valores) <= {"propext", "Classical.choice", "Quot.sound"}
        axiomas[nombre] = valores
    assert list(axiomas) == consultas
    texto = args.salida.with_suffix(".txt")
    texto.write_text(salida, encoding="utf-8")
    resultado = dict(version_lean=version, revision_mathlib=revision,
                     alcance="Módulo nuevo desde fuente e imports directos cotejados. "
                             "Sin reconstrucción ni auditoría transitiva completa de Mathlib. "
                             "La construcción para una lista finita arbitraria conserva prueba escrita.",
                     fuente=fuente.relative_to(RAIZ).as_posix(), fuente_sha256_lf=antes,
                     verificador_sha256_lf=huella(Path(__file__)),
                     salida_sha256_lf=huella(texto), dependencias=dependencias, axiomas=axiomas)
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(f"OK: Lean 4.32.2, {len(axiomas)} consultas, sólo axiomas estándar.")


if __name__ == "__main__":
    main()
