"""Audita un modulo nuevo sobre un prefijo ya compilado y verificado.

No modifica el manifiesto compartido: permite comprobar un argumento
general mientras otro proceso evalua certificados finitos.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

from comprobar_rachas_lean import auditar, huella, reutilizable


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--modulo", required=True)
    analizador.add_argument("--compilados", type=Path, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    assert re.fullmatch(r"Ocelotas[A-Za-z0-9]+", argumentos.modulo)
    carpeta = Path(__file__).resolve().parent
    formal = carpeta.parent / "gao20260920/formal"
    fuente = carpeta / (argumentos.modulo + ".lean")
    texto = fuente.read_text(encoding="utf-8")
    assert not re.search(r"\b(sorry|sorryAx|admit|axiom|native_decide)\b", texto)
    fuente_hash = huella(fuente)
    version = subprocess.run(
        ["lake", "env", "lean", "--version"], cwd=formal, check=True,
        capture_output=True, text=True, encoding="utf-8").stdout
    firma = hashlib.sha256((version + str(carpeta) + huella(formal / "lean-toolchain") +
        huella(formal / "lake-manifest.json") + os.environ.get("LEAN_PATH", "")).encode("utf-8")).hexdigest()
    manifiesto = json.loads((argumentos.compilados / "manifiesto_ocelotas.json").read_text(encoding="utf-8"))
    assert manifiesto["version"] == 1 and manifiesto["entorno"] == firma
    necesarias, pendientes, orden = set(), set(), []

    def dependencias(nombre):
        if nombre in pendientes:
            raise ValueError(f"Importaciones circulares en {nombre}")
        pendientes.add(nombre)
        for linea in re.findall(r"^import ([^\n]+)", (carpeta / (nombre + ".lean")).read_text(encoding="utf-8"), re.MULTILINE):
            for dependencia in linea.split():
                if dependencia in pendientes:
                    raise ValueError(f"Importaciones circulares en {dependencia}")
                if (carpeta / (dependencia + ".lean")).is_file() and dependencia not in necesarias:
                    necesarias.add(dependencia)
                    dependencias(dependencia)
        pendientes.remove(nombre)
        orden.append(nombre)

    dependencias(argumentos.modulo)
    reutilizadas = necesarias & manifiesto["modulos"].keys()
    assert reutilizadas
    prefijo, base = firma, {}
    for nombre, entrada in manifiesto["modulos"].items():
        objeto = argumentos.compilados / (nombre + ".olean")
        assert reutilizable(entrada, huella(carpeta / (nombre + ".lean")), prefijo, objeto), nombre
        auditar(entrada["auditoria"], nombre)
        base[nombre] = entrada
        prefijo = hashlib.sha256((prefijo + nombre + entrada["fuente"] + entrada["objeto"]).encode("ascii")).hexdigest()
        if reutilizadas <= base.keys():
            break
    with tempfile.TemporaryDirectory(prefix="ocelotas_extension_") as temporal:
        entorno = os.environ.copy()
        entorno["LEAN_PATH"] = os.pathsep.join([temporal, str(argumentos.compilados.resolve()), entorno.get("LEAN_PATH", "")])
        extensiones, salidas, consultas = {}, [], 0
        for nombre in orden:
            if nombre in base and nombre != argumentos.modulo:
                continue
            fuente_nueva = carpeta / (nombre + ".lean")
            texto_nuevo = fuente_nueva.read_text(encoding="utf-8")
            assert not re.search(r"\b(sorry|sorryAx|admit|axiom|native_decide)\b", texto_nuevo)
            hash_nuevo = huella(fuente_nueva)
            objeto = Path(temporal) / (nombre + ".olean")
            comando = ["lake", "env", "lean", "-R", str(carpeta), "-o", str(objeto), str(fuente_nueva)]
            print(f"COMPILANDO: {nombre}", flush=True)
            resultado = subprocess.run(comando, cwd=formal, env=entorno, capture_output=True,
                                       text=True, encoding="utf-8", check=False)
            salida_nueva = resultado.stdout + resultado.stderr
            salidas.append(salida_nueva)
            print(salida_nueva, end="", flush=True)
            argumentos.salida.with_suffix(".txt").write_text(
                version + "".join(salidas) + f"\nCodigo: {resultado.returncode}\n", encoding="utf-8")
            assert resultado.returncode == 0, "Compilacion fallida"
            auditar(salida_nueva, fuente_nueva)
            numero = len(re.findall(r"^#print axioms ", texto_nuevo, re.MULTILINE))
            respuestas = len(re.findall(r"depends on axioms:|does not depend on any axioms", salida_nueva))
            assert numero == respuestas > 0
            assert huella(fuente_nueva) == hash_nuevo
            consultas += numero
            extensiones[nombre] = {"fuente": hash_nuevo, "objeto": huella(objeto),
                                  "auditoria": salida_nueva, "consultas": numero, "comando": comando}
        salida = "".join(salidas)
        assert huella(fuente) == fuente_hash
        for nombre, entrada in extensiones.items():
            assert huella(carpeta / (nombre + ".lean")) == entrada["fuente"]
        for nombre, entrada in base.items():
            assert huella(carpeta / (nombre + ".lean")) == entrada["fuente"]
            assert huella(argumentos.compilados / (nombre + ".olean")) == entrada["objeto"]
        evidencia = {
            "estado": "compilado y auditado; prefijo reutilizado por huellas",
            "version_lean": version.strip(), "entorno": firma, "comando": comando,
            "sha256_comprobador": huella(Path(__file__)),
            "sha256_comprobador_base": huella(carpeta / "comprobar_rachas_lean.py"),
            "dependencias_directas_y_transitivas": sorted(necesarias),
            "prefijo_auditado": base,
            "extensiones": extensiones,
            "modulo": argumentos.modulo, "fuente": fuente_hash,
            "objeto": huella(objeto), "auditoria": salida, "consultas": consultas,
        }
        argumentos.salida.write_text(json.dumps(evidencia, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK: {consultas} consultas; {len(base)} modulos previos reutilizados por huellas.")


if __name__ == "__main__":
    main()
