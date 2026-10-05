"""Compila y audita el plano de la casa sobre las cachés verificadas de Ocelotas.

Uso, desde la raíz del repositorio:

    python -B -X utf8 depuracion/casa20261004/comprobar_casa.py
        --compilados-base C:/Users/Home/AppData/Local/Temp/ocelotas_auditado_20261003
        --compilados-extension C:/Users/Home/AppData/Local/Temp/ocelotas_veinticuatro_paralelo_20261004
        --salida depuracion/casa20261004/evidencia_casa.json

Antes de compilar comprueba, por huellas SHA-256, que cada módulo de Ocelotas que
importan `CasaPlano` y `CasaOcelotas` coincide con su fuente actual y con el objeto
auditado de su manifiesto, y que las firmas de entorno de las dos cachés son las
esperadas. Después compila los dos módulos en una carpeta temporal, exige código 0,
cuenta las consultas `#print axioms` y rechaza `sorryAx` o cualquier axioma distinto
de propext, Classical.choice y Quot.sound. Las cachés sólo se leen.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time

CASA = Path(__file__).resolve().parent
RAIZ = CASA.parents[1]
CST = RAIZ / "depuracion" / "cst20260930"
FORMAL = RAIZ / "depuracion" / "gao20260920" / "formal"
sys.path.insert(0, str(CST))
from comprobar_rachas_lean import auditar, huella  # noqa: E402

MODULOS = ["CasaPlano", "CasaOcelotas"]
PROHIBIDAS = re.compile(r"\b(sorry|sorryAx|admit|axiom|native_decide|implemented_by|extern|"
                        r"unsafe|ofReduceBool|trustCompiler)\b")
RESPUESTA = re.compile(r"^'([^']+)' (?:depends on axioms: \[(.*?)\]|does not depend on any axioms)",
                       re.MULTILINE | re.DOTALL)


def importaciones(fuente):
    return [d for linea in re.findall(r"^import ([^\n]+)", fuente.read_text(encoding="utf-8"), re.MULTILINE)
            for d in linea.split()]


def cierre_ocelotas():
    """Módulos de Ocelotas que importan, directa o indirectamente, los de la casa."""
    vistos, pendientes = set(), []
    for modulo in MODULOS:
        pendientes += [d for d in importaciones(CASA / (modulo + ".lean")) if (CST / (d + ".lean")).is_file()]
    while pendientes:
        nombre = pendientes.pop()
        if nombre in vistos:
            continue
        vistos.add(nombre)
        pendientes += [d for d in importaciones(CST / (nombre + ".lean")) if (CST / (d + ".lean")).is_file()]
    return vistos


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--compilados-base", type=Path, required=True)
    analizador.add_argument("--compilados-extension", type=Path, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    base_dir = argumentos.compilados_base.resolve()
    ext_dir = argumentos.compilados_extension.resolve()

    fuentes = {m: CASA / (m + ".lean") for m in MODULOS}
    huellas_fuentes = {m: huella(f) for m, f in fuentes.items()}
    for m, f in fuentes.items():
        prohibida = PROHIBIDAS.search(f.read_text(encoding="utf-8"))
        assert not prohibida, f"Palabra prohibida en {m}: {prohibida.group(0)}"

    version = subprocess.run(["lake", "env", "lean", "--version"], cwd=FORMAL, check=True,
                             capture_output=True, text=True, encoding="utf-8").stdout
    firma = hashlib.sha256((version + str(CST) + huella(FORMAL / "lean-toolchain") +
        huella(FORMAL / "lake-manifest.json") + os.environ.get("LEAN_PATH", "")).encode("utf-8")).hexdigest()
    firma_extension = hashlib.sha256((firma + str(base_dir) + str(ext_dir) +
        huella(CST / "comprobar_extension_paralela.py") +
        huella(CST / "comprobar_rachas_lean.py")).encode("utf-8")).hexdigest()
    manifiesto_base = json.loads((base_dir / "manifiesto_ocelotas.json").read_text(encoding="utf-8"))
    manifiesto_ext = json.loads((ext_dir / "manifiesto_extensiones.json").read_text(encoding="utf-8"))
    assert manifiesto_base["version"] == 1 and manifiesto_base["entorno"] == firma, "Firma de la base"
    assert manifiesto_ext["version"] == 1 and manifiesto_ext["entorno"] == firma_extension, "Firma de la extension"

    cierre = cierre_ocelotas()
    verificados = {}
    for nombre in sorted(cierre):
        if nombre in manifiesto_base["modulos"]:
            entrada, carpeta, origen = manifiesto_base["modulos"][nombre], base_dir, "base"
        else:
            entrada, carpeta, origen = manifiesto_ext["modulos"][nombre], ext_dir, "extension"
        assert entrada["fuente"] == huella(CST / (nombre + ".lean")), f"Fuente cambiada: {nombre}"
        assert entrada["objeto"] == huella(carpeta / (nombre + ".olean")), f"Objeto cambiado: {nombre}"
        auditar(entrada["auditoria"], nombre)
        verificados[nombre] = {"origen": origen, "fuente": entrada["fuente"], "objeto": entrada["objeto"]}
    print(f"Prefijo verificado: {len(verificados)} modulos de Ocelotas "
          f"({sum(v['origen'] == 'base' for v in verificados.values())} de la base).", flush=True)

    compilados, salidas, consultas = {}, [], 0
    with tempfile.TemporaryDirectory(prefix="casa_") as temporal:
        entorno = os.environ.copy()
        entorno["LEAN_PATH"] = os.pathsep.join([temporal, str(ext_dir), str(base_dir),
                                                entorno.get("LEAN_PATH", "")])
        for modulo in MODULOS:
            objeto = Path(temporal) / (modulo + ".olean")
            comando = ["lake", "env", "lean", "-R", str(CASA), "-o", str(objeto), str(fuentes[modulo])]
            print(f"COMPILANDO: {modulo}", flush=True)
            inicio = time.time()
            resultado = subprocess.run(comando, cwd=FORMAL, env=entorno, capture_output=True,
                                       text=True, encoding="utf-8", check=False)
            segundos = round(time.time() - inicio, 3)
            salida = resultado.stdout + resultado.stderr
            salidas.append(f"== {modulo} ({segundos} s, codigo {resultado.returncode})\n{salida}")
            print(salida, end="", flush=True)
            assert resultado.returncode == 0, f"Compilacion fallida: {modulo}"
            assert "warning" not in salida and "error" not in salida, f"Avisos en {modulo}"
            auditar(salida, modulo)
            pedidas = re.findall(r"^#print axioms (\S+)", fuentes[modulo].read_text(encoding="utf-8"),
                                 re.MULTILINE)
            respuestas = {nombre: [a.strip() for a in (lista or "").split(",") if a.strip()]
                          for nombre, lista in RESPUESTA.findall(salida)}
            assert pedidas and sorted(pedidas) == sorted(respuestas), f"Consultas de {modulo}"
            assert huella(fuentes[modulo]) == huellas_fuentes[modulo], f"Fuente cambiada: {modulo}"
            consultas += len(pedidas)
            compilados[modulo] = {"fuente": huellas_fuentes[modulo], "objeto": huella(objeto),
                                  "segundos": segundos, "axiomas": respuestas, "comando": comando}

    for nombre, dato in verificados.items():
        carpeta = base_dir if dato["origen"] == "base" else ext_dir
        assert huella(carpeta / (nombre + ".olean")) == dato["objeto"], f"Objeto cambiado: {nombre}"
    evidencia = {
        "estado": "compilado y auditado sobre cachés verificadas por huellas",
        "version_lean": version.strip(),
        "entorno_base": firma, "entorno_extension": firma_extension,
        "sha256_comprobador": huella(Path(__file__)),
        "sha256_auxiliar": huella(CST / "comprobar_rachas_lean.py"),
        "modulos": compilados, "consultas": consultas,
        "prefijo_ocelotas": verificados,
    }
    argumentos.salida.write_text(json.dumps(evidencia, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    argumentos.salida.with_suffix(".txt").write_text(version + "".join(salidas), encoding="utf-8")
    print(f"OK: {consultas} consultas en {len(compilados)} modulos; "
          f"{len(verificados)} modulos de Ocelotas verificados por huellas.")


if __name__ == "__main__":
    main()
