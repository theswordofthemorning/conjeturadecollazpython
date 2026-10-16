"""Recompila el módulo aislado y registra axiomas e imports directos."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


CARPETA = Path(__file__).resolve().parent
RAIZ = CARPETA.parents[2]
FORMAL = RAIZ / "depuracion/gao20260920/formal"


def huella(ruta):
    return hashlib.sha256(ruta.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def ejecutar(argumentos, carpeta):
    proceso = subprocess.run(argumentos, cwd=carpeta, capture_output=True,
                             text=True, encoding="utf-8", timeout=240)
    assert proceso.returncode == 0, proceso.stdout + proceso.stderr
    assert not proceso.stderr, proceso.stderr
    return proceso.stdout


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    fuente = CARPETA / "PerdicesCongruencias.lean"
    codigo = fuente.read_text(encoding="utf-8")
    consultas = re.findall(r"^#print axioms (\S+)$", codigo, re.MULTILINE)
    assert len(consultas) == 8
    assert not re.search(r"\b(sorry|admit|axiom|native_decide)\b", codigo)
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
        original = ejecutar(["git", "show", revision + ":" + relativa.with_suffix(".lean").as_posix()], mathlib)
        ruta = mathlib / relativa.with_suffix(".lean")
        assert hashlib.sha256(original.replace("\r\n", "\n").encode()).hexdigest() == huella(ruta)
        objeto = mathlib / ".lake/build/lib/lean" / relativa.with_suffix(".olean")
        dependencias[nombre] = dict(fuente_sha256_lf=huella(ruta),
                                   objeto_sha256=hashlib.sha256(objeto.read_bytes()).hexdigest())
    antes = huella(fuente)
    salida = ejecutar(["lake", "env", "lean", str(fuente)], FORMAL)
    assert huella(fuente) == antes
    assert all(texto not in salida for texto in ("sorryAx", "error:", "warning:"))
    axiomas = {}
    for linea in salida.splitlines():
        coincidencia = re.fullmatch(r"'([^']+)' depends on axioms: \[([^]]*)\]", linea)
        vacio = re.fullmatch(r"'([^']+)' does not depend on any axioms", linea)
        assert coincidencia or vacio, linea
        nombre = (coincidencia or vacio).group(1)
        valores = coincidencia.group(2).split(", ") if coincidencia and coincidencia.group(2) else []
        assert nombre not in axiomas
        assert set(valores) <= {"propext", "Classical.choice", "Quot.sound"}
        axiomas[nombre] = valores
    assert list(axiomas) == consultas
    texto = args.salida.with_suffix(".txt")
    texto.write_text(salida, encoding="utf-8")
    resultado = dict(version_lean=version, revision_mathlib=revision,
                     alcance="Tabla compartida y cotas aritméticas. Enlaces orbitales, cilindros y "
                             "realización de familias: prueba escrita. Imports directos cotejados; "
                             "sin auditoría transitiva completa de Mathlib.",
                     fuente=fuente.relative_to(RAIZ).as_posix(), fuente_sha256_lf=antes,
                     verificador_sha256_lf=huella(Path(__file__)),
                     salida_sha256_lf=huella(texto), dependencias=dependencias, axiomas=axiomas)
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK: {len(axiomas)} consultas Lean; sólo axiomas estándar.")


if __name__ == "__main__":
    main()
