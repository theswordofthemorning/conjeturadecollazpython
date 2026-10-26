"""Comprueba evidencia, enlaces y conservacion respecto del commit inicial explicito."""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess


CARPETA = Path(__file__).resolve().parent
RAIZ = CARPETA.parents[1]


def huella(ruta):
    return sha256(ruta.read_bytes()).hexdigest()


def leer(nombre):
    return json.loads((CARPETA / nombre).read_text(encoding="utf-8"))


def original(base, relativa):
    proceso = subprocess.run(["git", "show", base + ":" + relativa], cwd=RAIZ,
                             capture_output=True, check=True)
    return proceso.stdout


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--base", required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    assert re.fullmatch(r"[0-9a-f]{40}", args.base)
    documentos = [RAIZ / "ESTADO_INVESTIGACION.md",
                  RAIZ / "depuracion/balance20261025/BALANCE.md",
                  RAIZ / "depuracion/perdices20261007/COLA.md",
                  RAIZ / "depuracion/perdices20261025/borradores/LEEME.md",
                  *(CARPETA / nombre for nombre in
                    ("LIMITES_REALES.md", "PESOS_BINARIOS.md", "PRECISION_CRECENTE.md",
                     "AUDITORIA_RUTA.md", "TRAZAS_MATRICES.md",
                     "CLASIFICACION_F_INVERTIBLE.md"))]
    resumen = []
    for ruta in documentos:
        texto = ruta.read_text(encoding="utf-8")
        assert "\ufffd" not in texto and texto.endswith("\n")
        assert all(linea == linea.rstrip() for linea in texto.splitlines())
        enlaces = 0
        for destino in re.findall(r"\]\(([^)]+)\)", texto):
            if "://" in destino or destino.startswith("#"):
                continue
            assert (ruta.parent / destino.split("#", 1)[0]).resolve().exists(), (ruta, destino)
            enlaces += 1
        resumen.append(dict(archivo=ruta.relative_to(RAIZ).as_posix(),
                            palabras=len(texto.split()), enlaces_locales=enlaces,
                            sha256=huella(ruta)))
    consultas = 0
    for nombre, cantidad in (("evidencia_lean", 11), ("evidencia_lean_digital", 8),
                             ("evidencia_lean_trazas", 9), ("evidencia_lean_clasificacion", 6)):
        formal = leer(nombre + ".json")
        assert huella(RAIZ / formal["fuente"]) == formal["fuente_sha256"]
        assert huella(CARPETA / "comprobar_lean.py") == formal["verificador_sha256"]
        assert huella(CARPETA / (nombre + ".txt")) == formal["salida_sha256"]
        assert len(formal["axiomas"]) == cantidad
        assert all(set(a) <= {"propext", "Classical.choice", "Quot.sound"}
                   for a in formal["axiomas"].values())
        consultas += cantidad
    pasos = 0
    for nombre in ("limites", "pesos"):
        cotejo = leer("cotejo_" + nombre + ".json")
        assert huella(CARPETA / ("cotejar_" + nombre + ".py")) == cotejo["fuente_sha256"]
        pasos += cotejo["pasos_T"]
    matrices = leer("cotejo_trazas.json")
    assert matrices["estado"] == "correcto"
    assert huella(CARPETA / "cotejar_trazas.py") == matrices["fuente_sha256"]
    assert huella(CARPETA / "buscar_constantes_libres.py") == matrices["codificador_sha256"]
    objetivo = RAIZ / "depuracion/perdices20261007/bv_objetivo57_n2_c3.json"
    control = RAIZ / "depuracion/perdices20261007/sat_control15_n2_c3.json"
    assert huella(objetivo) == matrices["objetivo_sha256"]
    assert huella(control) == matrices["control_sha256"]
    assert len(matrices["controles"]) == 6
    for nombre in ("lia_trazas_objetivo57_m1", "lia_trazas_objetivo57_m1_libre",
                   "lia_trazas_objetivo57_m3"):
        busqueda = leer(nombre + ".json")
        assert busqueda["fuente_sha256"] == matrices["codificador_sha256"]
        assert busqueda["sistema_sha256"] == matrices["objetivo_sha256"]
        assert busqueda["formula_sha256"] == huella(CARPETA / (nombre + ".smt2"))
        assert busqueda["constantes_sin_cota"] and busqueda["logica"] == "QF_LIA"
        assert busqueda["estado"] == ("unknown" if nombre.endswith("m3") else "unsat")
        assert busqueda["limite_segundos"] == 30
    clasificacion = leer("cotejo_clasificacion.json")
    assert clasificacion["estado"] == "correcto"
    assert clasificacion["fuente_sha256"] == huella(CARPETA / "cotejar_clasificacion.py")
    singulares = leer("exploracion_singulares.json")
    assert singulares["fuente_sha256"] == huella(CARPETA / "explorar_singulares.py")
    assert singulares["codificador_sha256"] == matrices["codificador_sha256"]
    assert singulares["sistema_sha256"] == matrices["objetivo_sha256"]
    assert len(singulares["casos"]) == 12
    assert all(c["estado"] == "unsat" for c in singulares["casos"])
    registro = leer("evidencia_registro.json")
    assert registro["integrado"] and registro["filas_base"] == 365
    assert registro["filas_ampliadas_temporales"] == 369
    for ruta, esperada in registro["protegidos_sha256"].items():
        assert huella(RAIZ / ruta) == esperada, ruta
    assert huella(CARPETA / "alta_registro.json") == registro["alta_sha256"]
    assert huella(CARPETA / "verificar_alta.py") == registro["verificador_sha256"]
    assert huella(RAIZ / "guardarafirmaciones.py") == registro["generador_sha256"]
    assert huella(RAIZ / "registroafirmaciones.py") == registro["aplicador_sha256"]
    relativa = "depuracion/coherencia20260913/registro.json"
    previo = json.loads(original(args.base, relativa).decode("utf-8"))
    actual = json.loads((RAIZ / relativa).read_text(encoding="utf-8"))
    propuesta = leer("alta_registro.json")
    previo["altas"].extend([propuesta["alta"]] + propuesta["altas_adicionales"])
    assert actual == previo
    conservacion_previa = json.loads(original(
        args.base, "depuracion/perdices20261025/evidencia_registro.json").decode("utf-8"))
    assert huella(RAIZ / "respuestas.db") == conservacion_previa["protegidos_sha256"]["respuestas.db"]
    assert registro["preservacion_literal_afirmaciones_previas"]
    assert registro["historial_respuestas_sin_modificar"]
    estado = (RAIZ / "ESTADO_INVESTIGACION.md").read_text(encoding="utf-8")
    assert "reactivó Perdices" in estado and "Ninguna se ha" in estado
    resultado = dict(
        estado="correcto", commit_base=args.base,
        alcance="Verifica enlaces, fuentes, evidencia de compilacion y contraste, "
                "y conservacion literal del registro inicial salvo cuatro altas. "
                "No repite censos ni sustituye revision matematica humana.",
        consultas_lean=consultas, pasos_cotejados=pasos,
        filas_previas_conservadas=365, filas_actuales=369,
        cotejo_matricial=matrices,
        cotejo_clasificacion=clasificacion,
        respuestas_db_sha256=huella(RAIZ / "respuestas.db"), documentos=resumen,
        fuentes_sha256={p.name: huella(p) for p in sorted(CARPETA.iterdir())
                        if p.is_file() and p.resolve() != args.salida.resolve()})
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(estado="correcto", consultas_lean=consultas, afirmaciones=369,
                          enlaces=sum(d["enlaces_locales"] for d in resumen),
                          palabras_estado=resumen[0]["palabras"])))


if __name__ == "__main__":
    main()
