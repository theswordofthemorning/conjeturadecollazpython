"""Compila la cadena local de Ocelotas en un directorio temporal, sin huecos."""

import argparse
import hashlib
import os
from pathlib import Path
import re
import subprocess
import tempfile


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--salida", type=Path)
    argumentos = analizador.parse_args()
    carpeta = Path(__file__).resolve().parent
    formal = carpeta.parent / "gao20260920" / "formal"
    lineas = ["SHA256 comprobador: " + hashlib.sha256(Path(__file__).read_bytes()).hexdigest()]

    def ejecutar(comando, entorno=None):
        resultado = subprocess.run(
            comando, cwd=formal, env=entorno, capture_output=True,
            text=True, encoding="utf-8", errors="strict", check=False,
        )
        salida = resultado.stdout + resultado.stderr
        lineas.extend(["Comando: " + " ".join(comando), salida,
                       f"Codigo de salida: {resultado.returncode}"])
        print(salida, end="", flush=True)
        if resultado.returncode or re.search(r"\bsorryAx\b|declaration uses 'sorry'", salida):
            raise RuntimeError("Compilacion fallida o dependencia de sorryAx")
        return salida

    try:
        ejecutar(["lake", "env", "lean", "--version"])
        with tempfile.TemporaryDirectory(prefix="ocelotas_lean_") as temporal:
            entorno = os.environ.copy()
            entorno["LEAN_PATH"] = temporal + os.pathsep + entorno.get("LEAN_PATH", "")
            for nombre in ["Ocelotas", "OcelotasRachas", "OcelotasTrayectorias", "OcelotasFinito",
                           "OcelotasCriba", "OcelotasCertificado", "OcelotasCierre",
                           "OcelotasContador", "OcelotasRhin", "OcelotasLMN"]:
                fuente = carpeta / (nombre + ".lean")
                texto = fuente.read_text(encoding="utf-8")
                if re.search(r"\b(sorry|sorryAx|admit|axiom|native_decide)\b", texto):
                    raise RuntimeError(f"Revisar marcador no permitido en {fuente}")
                salida = ejecutar(["lake", "env", "lean", "-R", str(carpeta),
                                   "-o", str(Path(temporal) / (nombre + ".olean")),
                                   str(fuente)], entorno)
                listas = re.findall(r"depends on axioms:\s*\[(.*?)\]", salida, flags=re.DOTALL)
                if not listas:
                    raise RuntimeError(f"Falta auditoria de axiomas en {fuente}")
                for lista in listas:
                    usados = {elemento.strip() for elemento in lista.split(",") if elemento.strip()}
                    if usados - {"propext", "Classical.choice", "Quot.sound"}:
                        raise RuntimeError(f"Axiomas no admitidos en {fuente}: {usados}")
                lineas.append(f"SHA256 {nombre}.lean: {hashlib.sha256(fuente.read_bytes()).hexdigest()}")
            lineas.append("CADENA VALIDADA: solo axiomas estandar admitidos; ningun hueco.")
    finally:
        if argumentos.salida:
            argumentos.salida.write_text("\n".join(lineas) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
