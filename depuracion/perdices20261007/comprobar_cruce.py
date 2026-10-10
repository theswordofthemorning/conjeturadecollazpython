"""Compila el cruce de sexta raíz y casi fugitivos (PerdicesCruce).

Las cachés se aceptan sólo con iguales fuentes, objetos, dependencias,
comprobador y entorno. No se mezclan con la casa recuperada del 05-10.
Reconstruye el cierre completo: Ocelotas, CasaPlano, CasaRetrato,
PerdicesEstela, PerdicesTamano, PerdicesSexta y PerdicesCruce.
Uso: python -B -X utf8 depuracion/perdices20261007/comprobar_cruce.py
    --compilados RUTA_TEMPORAL --salida RUTA_JSON
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

CARPETA = Path(__file__).resolve().parent
RAIZ = CARPETA.parents[1]
FORMAL = RAIZ / "depuracion/gao20260920/formal"
VIGENTE = RAIZ / "depuracion/casa20261004"
CST = RAIZ / "depuracion/cst20260930"
RESPUESTA = re.compile(
    r"^'([^']+)' (?:depends on axioms: \[(.*?)\]|does not depend on any axioms)",
    re.MULTILINE | re.DOTALL)
ADMITIDOS = {"propext", "Classical.choice", "Quot.sound"}


def huella(ruta):
    return hashlib.sha256(Path(ruta).read_bytes()).hexdigest()


def fuente_de(nombre):
    carpeta = CARPETA if nombre.startswith("Perdices") else (
        VIGENTE if nombre.startswith("Casa") else CST)
    return carpeta / (nombre + ".lean")


def cierre():
    orden, dependencias = [], {}

    def visitar(nombre):
        if nombre in dependencias:
            return
        texto = fuente_de(nombre).read_text(encoding="utf-8")
        deps = [d for linea in re.findall(r"^import (.+)$", texto, re.MULTILINE)
                for d in linea.split() if not d.startswith("Mathlib")]
        dependencias[nombre] = deps
        for dependencia in deps:
            visitar(dependencia)
        orden.append(nombre)

    visitar("PerdicesCruce")
    return orden, dependencias


def auditar(nombre, texto_fuente, salida):
    assert "sorry" not in salida, (nombre, "prueba incompleta")
    if nombre.startswith(("Casa", "Perdices")):
        assert not re.search(r"\b(?:warning|error):", salida), salida
        assert not re.search(
            r"\b(?:sorry|sorryAx|admit|axiom|native_decide|implemented_by|extern|unsafe)\b",
            texto_fuente), nombre
    pedidas = re.findall(r"^#print axioms (\S+)", texto_fuente, re.MULTILINE)
    respuestas = {n: sorted(a.strip() for a in (lista or "").split(",") if a.strip())
                  for n, lista in RESPUESTA.findall(salida)}
    assert sorted(pedidas) == sorted(respuestas), (nombre, pedidas, respuestas)
    for axiomas in respuestas.values():
        assert set(axiomas) <= ADMITIDOS, (nombre, axiomas)
    return respuestas


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--compilados", type=Path, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    compilados = argumentos.compilados.resolve()
    compilados.mkdir(parents=True, exist_ok=True)
    argumentos.salida.parent.mkdir(parents=True, exist_ok=True)
    manifiesto = compilados / "manifiesto_cruce.json"
    anterior = json.loads(manifiesto.read_text(encoding="utf-8")) if manifiesto.exists() else {}
    version = subprocess.run(["lake", "env", "lean", "--version"], cwd=FORMAL,
                             check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()
    contexto = {"version_lean": version, "comprobador": huella(__file__),
                "toolchain": huella(FORMAL / "lean-toolchain"),
                "mathlib": huella(FORMAL / "lake-manifest.json"),
                "formal": str(FORMAL), "lean_path_previo": os.environ.get("LEAN_PATH", "")}
    entorno = dict(os.environ)
    entorno["LEAN_PATH"] = str(compilados) + os.pathsep + contexto["lean_path_previo"]
    orden, dependencias = cierre()
    modulos, registros = {}, [version + "\n"]
    for nombre in orden:
        fuente = fuente_de(nombre)
        texto = fuente.read_text(encoding="utf-8")
        objeto = compilados / (nombre + ".olean")
        dato = {"fuente": fuente.relative_to(RAIZ).as_posix(), "sha256": huella(fuente),
                "dependencias": {d: modulos[d]["objeto"] for d in dependencias[nombre]}}
        previo = anterior.get("modulos", {}).get(nombre, {})
        reutilizable = (anterior.get("contexto") == contexto and objeto.exists()
                        and all(previo.get(k) == v for k, v in dato.items())
                        and previo.get("objeto") == huella(objeto))
        if reutilizable:
            salida = previo["salida"]
            segundos = previo["segundos"]
        else:
            inicio = time.monotonic()
            resultado = subprocess.run(
                ["lake", "env", "lean", "-R", str(fuente.parent), "-o", str(objeto), str(fuente)],
                cwd=FORMAL, env=entorno, capture_output=True, text=True, encoding="utf-8")
            salida = resultado.stdout + resultado.stderr
            assert resultado.returncode == 0, f"{nombre}:\n{salida}"
            segundos = round(time.monotonic() - inicio, 3)
        axiomas = auditar(nombre, texto, salida)
        assert huella(fuente) == dato["sha256"], nombre
        dato.update(objeto=huella(objeto), axiomas=axiomas, salida=salida, segundos=segundos)
        modulos[nombre] = dato
        manifiesto.write_text(json.dumps({"contexto": contexto, "modulos": modulos},
                                        ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        modo = "reutilizado por huellas" if reutilizable else "compilado"
        registros.append(f"== {nombre}: {modo}\n{salida}")
        print(f"{nombre}: {modo}, {segundos} s", flush=True)
    for nombre, dato in modulos.items():
        assert huella(fuente_de(nombre)) == dato["sha256"], nombre
        assert huella(compilados / (nombre + ".olean")) == dato["objeto"], nombre
    evidencia = {"estado": "compilado y auditado", "contexto": contexto,
                 "modulos": {n: {k: v for k, v in d.items() if k != "salida"}
                             for n, d in modulos.items()},
                 "consultas": sum(len(d["axiomas"]) for d in modulos.values())}
    argumentos.salida.write_text(json.dumps(evidencia, ensure_ascii=False, indent=2) + "\n",
                                 encoding="utf-8")
    argumentos.salida.with_suffix(".txt").write_text("".join(registros), encoding="utf-8")
    print(f"OK: {len(modulos)} módulos, {evidencia['consultas']} consultas.")


if __name__ == "__main__":
    main()
