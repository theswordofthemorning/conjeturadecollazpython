"""Compila desde las fuentes el retrato del fugitivo y audita sus axiomas.

Uso, desde la raíz del repositorio:

    python -B -X utf8 depuracion/casa20261004/comprobar_fugitivo.py
        --salida depuracion/casa20261004/evidencia_fugitivo.json

A diferencia de `comprobar_casa.py`, no lee cachés: compila en una carpeta temporal
nueva los ocho módulos de Ocelotas que importa `CasaPlano` (en orden de dependencias),
después `CasaPlano`, `CasaFugitivo`, `CasaCasiTodos`, `CasaChoques`, `CasaTerras`,
`CasaDomino`, `CasaKorec`, `CasaPotencia`, `CasaTres`, `CasaLMN` y `CasaCadena`.
Exige código 0 y ningún `sorry`; en los módulos de la casa, además, ningún aviso ni
palabra prohibida, y en sus consultas `#print axioms` sólo admite propext,
Classical.choice y Quot.sound. Guarda las huellas
SHA-256 de todas las fuentes compiladas. Unos cinco minutos.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time

CASA = Path(__file__).resolve().parent
RAIZ = CASA.parents[1]
CST = RAIZ / "depuracion" / "cst20260930"
FORMAL = RAIZ / "depuracion" / "gao20260920" / "formal"
CADENA = ["Ocelotas", "OcelotasRachas", "OcelotasTrayectorias", "OcelotasFinito",
          "OcelotasCriba", "OcelotasCertificado", "OcelotasCierre", "OcelotasContador"]
CASA_MODULOS = ["CasaPlano", "CasaFugitivo", "CasaCasiTodos", "CasaChoques", "CasaTerras",
                "CasaDomino", "CasaKorec", "CasaPotencia", "CasaTres", "CasaLMN",
                "CasaCadena"]
ADMITIDOS = {"propext", "Classical.choice", "Quot.sound"}
PROHIBIDAS = re.compile(r"\b(sorry|sorryAx|admit|axiom|native_decide|implemented_by|extern|"
                        r"unsafe|ofReduceBool|trustCompiler)\b")
DIAGNOSTICO = re.compile(r"\b(warning|error):")
RESPUESTA = re.compile(r"^'([^']+)' (?:depends on axioms: \[(.*?)\]|does not depend on any axioms)",
                       re.MULTILINE | re.DOTALL)


def huella(ruta):
    return hashlib.sha256(Path(ruta).read_bytes()).hexdigest()


def importaciones(fuente):
    return [d for linea in re.findall(r"^import ([^\n]+)", fuente.read_text(encoding="utf-8"),
                                      re.MULTILINE) for d in linea.split()]


def fuente_de(modulo):
    carpeta = CASA if modulo.startswith("Casa") else CST
    return carpeta / (modulo + ".lean")


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()

    orden = CADENA + CASA_MODULOS
    for i, modulo in enumerate(orden):
        for d in importaciones(fuente_de(modulo)):
            if not d.startswith("Mathlib"):
                assert d in orden[:i], f"{modulo} importa {d}, fuera de la cadena o desordenado"
    for modulo in CASA_MODULOS:
        prohibida = PROHIBIDAS.search(fuente_de(modulo).read_text(encoding="utf-8"))
        assert not prohibida, f"Palabra prohibida en {modulo}: {prohibida.group(0)}"

    version = subprocess.run(["lake", "env", "lean", "--version"], cwd=FORMAL, check=True,
                             capture_output=True, text=True, encoding="utf-8").stdout.strip()
    modulos, salidas, consultas = {}, [version + "\n"], 0
    with tempfile.TemporaryDirectory(prefix="casa_fugitivo_") as temporal:
        entorno = dict(os.environ)
        entorno["LEAN_PATH"] = temporal + os.pathsep + entorno.get("LEAN_PATH", "")
        for modulo in orden:
            fuente = fuente_de(modulo)
            inicio = time.time()
            r = subprocess.run(["lake", "env", "lean", "-R", str(fuente.parent), "-o",
                                str(Path(temporal) / (modulo + ".olean")), str(fuente)],
                               cwd=FORMAL, env=entorno, capture_output=True, text=True,
                               encoding="utf-8")
            segundos = round(time.time() - inicio, 3)
            texto = r.stdout + r.stderr
            assert r.returncode == 0, f"{modulo} no compila:\n{texto[-4000:]}"
            assert "sorry" not in texto, f"{modulo} usa sorry"
            if modulo in CASA_MODULOS:
                assert not DIAGNOSTICO.search(texto), \
                    f"Avisos en {modulo}:\n{texto[-4000:]}"
            dato = {"fuente": str(fuente.relative_to(RAIZ)).replace("\\", "/"),
                    "sha256": huella(fuente), "segundos": segundos}
            if modulo in CASA_MODULOS:
                pedidas = re.findall(r"^#print axioms (\S+)", fuente.read_text(encoding="utf-8"),
                                     re.MULTILINE)
                respuestas = {}
                for nombre, lista in RESPUESTA.findall(r.stdout):
                    axiomas = {a.strip() for a in lista.replace("\n", " ").split(",") if a.strip()}
                    assert axiomas <= ADMITIDOS, f"{nombre}: {sorted(axiomas)}"
                    respuestas[nombre] = sorted(axiomas)
                assert pedidas and sorted(pedidas) == sorted(respuestas), f"Consultas de {modulo}"
                consultas += len(pedidas)
                dato["axiomas"] = respuestas
                salidas.append(f"== {modulo} ({segundos} s, codigo 0)\n{r.stdout}")
            modulos[modulo] = dato
            print(f"{modulo}: {segundos} s", flush=True)

    evidencia = {"estado": "compilado desde las fuentes en carpeta temporal nueva, sin cachés",
                 "version_lean": version, "sha256_comprobador": huella(Path(__file__)),
                 "toolchain": huella(FORMAL / "lean-toolchain"),
                 "manifiesto": huella(FORMAL / "lake-manifest.json"),
                 "modulos": modulos, "consultas": consultas}
    argumentos.salida.write_text(json.dumps(evidencia, ensure_ascii=False, indent=2) + "\n",
                                 encoding="utf-8")
    argumentos.salida.with_suffix(".txt").write_text("".join(salidas), encoding="utf-8")
    print(f"OK: {consultas} consultas en {len(CASA_MODULOS)} módulos de la casa; "
          f"{len(CADENA)} módulos de Ocelotas compilados desde las fuentes.")


if __name__ == "__main__":
    main()
