"""Valida enlaces, evidencias y conservacion sin repetir los experimentos."""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re


CARPETA = Path(__file__).resolve().parent
RAIZ = CARPETA.parents[1]


def huella(ruta):
    return sha256(ruta.read_bytes()).hexdigest()


def leer(nombre):
    return json.loads((CARPETA / nombre).read_text(encoding="utf-8"))


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    documentos = [RAIZ / "ESTADO_INVESTIGACION.md",
                  RAIZ / "depuracion/balance20261025/BALANCE.md",
                  RAIZ / "depuracion/perdices20261007/UMBRAL.md",
                  RAIZ / "depuracion/perdices20261007/congruencias_codex20261016/RUTA_CODEX.md",
                  *(CARPETA / nombre for nombre in
                    ("PROTEGIDOS.md", "SESGO_FRONTERA.md", "FRECUENCIAS_TEMPORALES.md",
                     "OBSERVABILIDAD_TERNARIA.md", "RETORNOS_ARITMETICOS.md"))]
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
    for nombre in ("evidencia_lean.json", "evidencia_lean_sesgo.json",
                   "evidencia_lean_frecuencias.json", "evidencia_lean_intercambio.json",
                   "evidencia_lean_valuaciones.json", "evidencia_lean_retornos.json"):
        dato = leer(nombre)
        assert huella(RAIZ / dato["fuente"]) == dato["fuente_sha256"]
        assert huella(CARPETA / "comprobar_lean.py") == dato["verificador_sha256"]
        assert huella((CARPETA / nombre).with_suffix(".txt")) == dato["salida_sha256"]
        assert all(set(a) <= {"propext", "Classical.choice", "Quot.sound"}
                   for a in dato["axiomas"].values())
        consultas += len(dato["axiomas"])
    for nombre in ("protegidos", "sesgo", "frecuencias", "valuaciones", "retornos"):
        dato = leer("cotejo_" + nombre + ".json")
        fuente = "cotejar_" + nombre + ".py"
        esperada = (dato["fuente_sha256"] if nombre in ("frecuencias", "valuaciones", "retornos") else
                    dato["fuentes_sha256"][fuente])
        assert huella(CARPETA / fuente) == esperada
    registro = leer("evidencia_registro.json")
    for ruta, esperada in registro["protegidos_sha256"].items():
        assert huella(RAIZ / ruta) == esperada, ruta
    assert huella(CARPETA / "alta_registro.json") == registro["alta_sha256"]
    assert huella(CARPETA / "verificar_alta.py") == registro["verificador_sha256"]
    assert registro["preservacion_literal_afirmaciones_previas"]
    assert registro["historial_respuestas_sin_modificar"] and registro["integrado"]
    altas = leer("alta_registro.json")
    cantidad = 361 + len(altas.get("altas_adicionales", []))
    assert registro["filas_base"] == 360 and registro["filas_ampliadas_temporales"] == cantidad
    resultado = dict(
        estado="evidencias y enlaces coherentes",
        alcance="Comprobacion de integridad documental y evidencia guardada; "
                "no recompila Lean, no repite cotejos y no sustituye revision humana.",
        documentos=resumen, consultas_lean=consultas,
        afirmaciones_previas_conservadas=registro["filas_base"],
        afirmaciones_actuales=registro["filas_ampliadas_temporales"],
        respuestas_db_sha256=registro["protegidos_sha256"]["respuestas.db"],
        fuentes_sha256={p.name: huella(p) for p in sorted(CARPETA.iterdir())
                        if p.is_file() and p.resolve() != args.salida.resolve()})
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(estado="correcto", consultas_lean=consultas,
                          afirmaciones=cantidad, enlaces=sum(d["enlaces_locales"] for d in resumen))))


if __name__ == "__main__":
    main()
