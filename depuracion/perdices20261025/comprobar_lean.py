"""Recompila el modulo local y registra axiomas e imports directos fijados."""

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
    analizador.add_argument("--modulo", default="PerdicesProtegidos",
                            choices=("PerdicesProtegidos", "PerdicesSesgoFrontera",
                                     "PerdicesFrecuencias", "PerdicesIntercambio",
                                     "PerdicesValuaciones", "PerdicesRetornoFirma"))
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
    alcance = (
        "Maximo binomial ponderado, transferencia algebraica de cuentas, "
        "identidad de frontera, pisos del certificado y constantes exactas. "
        "Conteo de rotaciones, realizacion por orbitas, extraccion de las "
        "cuentas y densidad de horizontes: prueba escrita, no formalizados aqui. "
        if args.modulo == "PerdicesProtegidos" else
        "Seguridad del intercambio, identidad de desviacion, piso real de dos "
        "horizontes, traslado cuantitativo, paso libre e incrementos del umbral. "
        "Inyeccion completa de palabras, extraccion de cuentas, densidad y "
        "no convergencia de la medida: prueba escrita, no formalizados aqui. "
        if args.modulo == "PerdicesSesgoFrontera" else
        "Identidad local universal y balance de una trayectoria natural arbitraria; "
        "criterio completo desde tres cotas marginales hasta 3^S<2^K. "
        "Conversion de TV a eventos, discrepancia, ejemplo euleriano y control "
        "racional: prueba escrita y cotejo, no formalizados aqui. "
        if args.modulo == "PerdicesFrecuencias" else
        "Supervivencia de todos los prefijos, intercambio completo de listas, "
        "conservacion de longitud/subidas/producto, cambio de residuo, inyectividad "
        "y desigualdad 2*card(clase 1)<=card(frontera alta). "
        "Identificacion con cuentas orbitales, densidad de horizontes y "
        "no convergencia de la medida: prueba escrita, no formalizados aqui. "
        if args.modulo == "PerdicesIntercambio" else
        "Identidad universal de valoracion ternaria, profundidad acotada, "
        "separacion de paridades, identidad truncada y balance de una "
        "trayectoria natural para todos m,K. Marca critica definida por "
        "valoracion; identificacion por congruencias, medidas/TV y flujos "
        "estacionarios: prueba escrita, no formalizados aqui. "
        if args.modulo == "PerdicesValuaciones" else
        "Recorrido entero 231->391, igualdad de las dos valoraciones binarias "
        "y obstruccion completa a cualquier rango no decreciente en tamano "
        "dentro de esa firma, con valores en cualquier preorden. "
        "Construccion CRT para listas arbitrarias de observaciones y lotes "
        "fijos: prueba escrita, no formalizada aqui. ")
    resultado = dict(
        version_lean=version, revision_mathlib=revision,
        alcance=alcance + "Imports directos cotejados; sin auditoria transitiva completa.",
        fuente=fuente.relative_to(RAIZ).as_posix(), fuente_sha256=antes,
        verificador_sha256=huella(Path(__file__)), salida_sha256=huella(texto),
        dependencias=dependencias, axiomas=axiomas)
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK: {len(axiomas)} consultas; Lean 4.32.2, solo axiomas estandar.")


if __name__ == "__main__":
    main()
