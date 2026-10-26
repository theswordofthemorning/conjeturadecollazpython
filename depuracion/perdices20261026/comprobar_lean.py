"""Compila los modulos del 26-10 y coteja axiomas e imports directos de Mathlib."""

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess


CARPETA = Path(__file__).resolve().parent
RAIZ = CARPETA.parents[1]
FORMAL = RAIZ / "depuracion/gao20260920/formal"


def huella(ruta):
    return sha256(ruta.read_bytes()).hexdigest()


def ejecutar(argumentos, entorno=None):
    proceso = subprocess.run(argumentos, cwd=FORMAL, env=entorno, capture_output=True,
                             text=True, encoding="utf-8", timeout=180)
    assert proceso.returncode == 0, proceso.stdout + proceso.stderr
    assert not proceso.stderr, proceso.stderr
    return proceso.stdout


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--lean", type=Path, required=True)
    analizador.add_argument("--modulo", default="PerdicesLimitesReales",
                            choices=("PerdicesLimitesReales", "PerdicesRetornoFirmaDigital",
                                     "PerdicesTrazasMatrices", "PerdicesClasificacionTriangular"))
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    fuente = CARPETA / (args.modulo + ".lean")
    codigo = fuente.read_text(encoding="utf-8")
    assert not re.search(r"\b(sorry|admit|axiom|native_decide)\b", codigo)
    consultas = re.findall(r"^#print axioms (\S+)$", codigo, re.MULTILINE)
    version = ejecutar([str(args.lean), "--version"]).strip()
    assert version.startswith("Lean (version 4.32.2,")
    manifiesto = json.loads((FORMAL / "lake-manifest.json").read_text(encoding="utf-8"))
    revision = next(p["rev"] for p in manifiesto["packages"] if p["name"] == "mathlib")
    mathlib = FORMAL / ".lake/packages/mathlib"
    assert ejecutar(["git", "-C", str(mathlib), "rev-parse", "HEAD"]).strip() == revision
    entorno = os.environ.copy()
    entorno["LEAN_PATH"] = os.pathsep.join(str(FORMAL / ".lake/packages" / p["name"] /
                                              ".lake/build/lib/lean")
                                           for p in manifiesto["packages"])
    resueltos = {Path(p).resolve() for p in
                 ejecutar([str(args.lean), "--deps", str(fuente)], entorno).splitlines()}
    dependencias = {}
    for nombre in re.findall(r"^import (\S+)$", codigo, re.MULTILINE):
        assert nombre.startswith("Mathlib.")
        relativa = Path(*nombre.split("."))
        ruta = mathlib / relativa.with_suffix(".lean")
        original = ejecutar(["git", "-C", str(mathlib), "show",
                              revision + ":" + relativa.with_suffix(".lean").as_posix()])
        assert original.replace("\r\n", "\n") == ruta.read_text(encoding="utf-8")
        objeto = mathlib / ".lake/build/lib/lean" / relativa.with_suffix(".olean")
        assert objeto.resolve() in resueltos
        dependencias[nombre] = dict(fuente_sha256=huella(ruta), objeto_sha256=huella(objeto))
    antes = huella(fuente)
    salida = ejecutar([str(args.lean), str(fuente)], entorno)
    assert huella(fuente) == antes
    assert not any(t in salida for t in ("sorryAx", "error:", "warning:")), salida
    axiomas = {}
    for linea in salida.splitlines():
        hallazgo = re.fullmatch(r"'([^']+)' depends on axioms: \[([^]]*)\]", linea)
        vacio = re.fullmatch(r"'([^']+)' does not depend on any axioms", linea)
        assert hallazgo or vacio, linea
        nombre = (hallazgo or vacio).group(1)
        valores = hallazgo.group(2).split(", ") if hallazgo and hallazgo.group(2) else []
        assert nombre not in axiomas
        assert set(valores) <= {"propext", "Classical.choice", "Quot.sound"}
        axiomas[nombre] = valores
    assert list(axiomas) == consultas
    texto = args.salida.with_suffix(".txt")
    texto.write_text(salida, encoding="utf-8")
    alcance = ("Intervalo invariante, identidad de sumas parciales, error geometrico "
                "y convergencia real para todo q en [1,4]; testigos 3/2 y 2; "
                "paridad de numeradores y obstruccion algebraica a puntos fijos diadicos. "
                "Identificacion con series de bits, aperiodicidad de las palabras y "
                "lectura critica del preprint: prueba escrita. No formaliza el limite "
                "2-adico ni decide su racionalidad. "
                if args.modulo == "PerdicesLimitesReales" else
                "Retornos enteros 231->391 y 8423->14215; firma v2(n+1),v2(n+5) "
                "y pesos binarios exactos. Imposibilidad completa de un perfil "
                "monotono en tamano y en cualquiera de los dos sentidos del peso, "
                "elegido por firma, que descienda en cada bloque A/B real. "
                "Generalizacion a observaciones arbitrarias, lotes fijos, "
                "perfiles eventuales y variaciones ilimitadas: prueba escrita."
                if args.modulo == "PerdicesRetornoFirmaDigital" else
                "Conmutador no negativo de las seis reglas de intercambio, "
                "igualdad diagonal, identidad de traza ponderada, conmutacion "
                "e igualdad de las seis reglas matriciales bajo conexion "
                "bidireccional de la suma de matrices. Nucleo escalar ponderado "
                "de la obstruccion con M_a=M_b=t I; su traduccion a las reglas "
                "matriciales conserva prueba escrita. No demuestra terminacion "
                "ni clasifica todos los vectores constantes."
                if args.modulo == "PerdicesTrazasMatrices" else
                "Igualdad de determinantes y trazas a partir de invariantes escalares; "
                "tres ramas triangulares (imagen comun, nucleo comun y resonancia 2:3); "
                "nucleo del descarte nilpotente. La triangularizacion, el paso desde "
                "las matrices naturales, integridad de parametros y enlace orbital "
                "conservan prueba escrita o permanecen abiertos segun la nota.")
    resultado = dict(
        version_lean=version, revision_mathlib=revision,
        alcance=alcance + " Imports directos cotejados; sin auditoria transitiva completa.",
        fuente=fuente.relative_to(RAIZ).as_posix(), fuente_sha256=antes,
        verificador_sha256=huella(Path(__file__)), salida_sha256=huella(texto),
        dependencias=dependencias, axiomas=axiomas)
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK: {len(axiomas)} consultas; Lean 4.32.2, solo axiomas estandar.")


if __name__ == "__main__":
    main()
