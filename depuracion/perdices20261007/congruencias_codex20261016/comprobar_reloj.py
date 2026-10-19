"""Recompila siete módulos desde fuente y comprueba sus imports y axiomas."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

from comprobar_lean import CARPETA, FORMAL, RAIZ, huella


def ejecutar(argumentos, carpeta, entorno=None):
    proceso = subprocess.run(argumentos, cwd=carpeta, env=entorno,
                             capture_output=True, text=True, encoding="utf-8", timeout=480)
    assert proceso.returncode == 0, proceso.stdout + proceso.stderr
    assert not proceso.stderr, proceso.stderr
    return proceso.stdout


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    fuentes = [CARPETA.parent / "PerdicesTransporteImpar.lean",
               CARPETA / "PerdicesRelojTerminal.lean"]
    version = ejecutar(["lake", "env", "lean", "--version"], FORMAL).strip()
    assert version.startswith("Lean (version 4.32.2,")
    manifiesto = json.loads((FORMAL / "lake-manifest.json").read_text(encoding="utf-8"))
    revision = next(p["rev"] for p in manifiesto["packages"] if p["name"] == "mathlib")
    mathlib = FORMAL / ".lake/packages/mathlib"
    assert ejecutar(["git", "rev-parse", "HEAD"], mathlib).strip() == revision
    dependencias, modulos, salidas = {}, {}, []
    with tempfile.TemporaryDirectory(prefix="perdices_reloj_codex_") as carpeta:
        temporal = Path(carpeta).resolve()
        assert temporal.parent == Path(tempfile.gettempdir()).resolve()
        assert temporal.name.startswith("perdices_reloj_codex_")
        entorno = os.environ.copy()
        entorno["LEAN_PATH"] = str(temporal) + os.pathsep + entorno.get("LEAN_PATH", "")
        for fuente in fuentes:
            print("Compilando " + fuente.name, flush=True)
            codigo = fuente.read_text(encoding="utf-8")
            assert not re.search(r"\b(sorry|admit|axiom|native_decide)\b", codigo)
            consultas = re.findall(r"^#print axioms (\S+)$", codigo, re.MULTILINE)
            assert consultas or fuente.stem == "PerdicesBarreraTablas"
            esperados, locales = set(), {}
            for nombre in re.findall(r"^import (\S+)$", codigo, re.MULTILINE):
                if not nombre.startswith("Mathlib."):
                    assert nombre in modulos
                    objeto = temporal / (nombre + ".olean")
                    esperados.add(objeto.resolve())
                    locales[nombre] = hashlib.sha256(objeto.read_bytes()).hexdigest()
                    assert locales[nombre] == modulos[nombre]["objeto_sha256"]
                    continue
                relativa = Path(*nombre.split("."))
                original = ejecutar(["git", "show", revision + ":" + relativa.with_suffix(".lean").as_posix()], mathlib)
                ruta = mathlib / relativa.with_suffix(".lean")
                assert hashlib.sha256(original.replace("\r\n", "\n").encode()).hexdigest() == huella(ruta)
                objeto = mathlib / ".lake/build/lib/lean" / relativa.with_suffix(".olean")
                esperados.add(objeto.resolve())
                dependencias[nombre] = dict(fuente_sha256_lf=huella(ruta),
                                           objeto_sha256=hashlib.sha256(objeto.read_bytes()).hexdigest())
            antes = huella(fuente)
            # La copia temporal mantiene resolubles los nombres de módulo;
            # los originales y las cachés del repositorio no se escriben.
            copia = temporal / fuente.name
            copia.write_text(codigo, encoding="utf-8")
            resueltas = ejecutar(["lake", "env", "lean", "--deps", str(copia)], FORMAL, entorno)
            assert esperados <= {Path(linea).resolve() for linea in resueltas.splitlines()}
            salida = ejecutar(["lake", "env", "lean", "--root=" + str(temporal),
                               "-o", str(copia.with_suffix(".olean")), str(copia)], FORMAL, entorno)
            assert huella(fuente) == antes
            assert not any(t in salida for t in ("sorryAx", "error:", "warning:")), salida
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
            modulos[fuente.stem] = dict(fuente=fuente.relative_to(RAIZ).as_posix(),
                                        fuente_sha256_lf=antes, axiomas=axiomas,
                                        objeto_sha256=hashlib.sha256(copia.with_suffix(".olean").read_bytes()).hexdigest(),
                                        imports_locales_recompilados=locales,
                                        resolucion_imports_directos_comprobada=True)
            salidas.append(salida)
    texto = args.salida.with_suffix(".txt")
    texto.write_text("".join(salidas), encoding="utf-8")
    resultado = dict(version_lean=version, revision_mathlib=revision,
                     alcance="Continuaci?n orbital exacta de toda carga terminal y equivalencia entre "
                             "presupuesto universal y reloj logar?tmico; no afirma ninguno de ambos. "
                             "Imports directos cotejados; sin auditor?a transitiva completa de Mathlib.",
                     modulos=modulos, dependencias=dependencias,
                     verificador_sha256_lf=huella(Path(__file__)),
                     apoyo_sha256_lf=huella(CARPETA / "comprobar_lean.py"),
                     salida_sha256_lf=huella(texto))
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK: {sum(len(m['axiomas']) for m in modulos.values())} consultas desde fuente.")


if __name__ == "__main__":
    main()
