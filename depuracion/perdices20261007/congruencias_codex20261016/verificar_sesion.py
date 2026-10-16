"""Comprueba enlaces y vigencia de evidencias sin repetir los experimentos."""

import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote


CARPETA = Path(__file__).resolve().parent
RAIZ = CARPETA.parents[2]


def huella(ruta, normalizar=True):
    datos = ruta.read_bytes()
    if normalizar:
        datos = datos.replace(b"\r\n", b"\n")
    return hashlib.sha256(datos).hexdigest()


def leer(nombre):
    return json.loads((CARPETA / nombre).read_text(encoding="utf-8"))


def comprobar_enlaces(fuente):
    enlaces = 0
    texto = fuente.read_text(encoding="utf-8")
    for destino in re.findall(r"\[[^\]]+\]\(([^)]+)\)", texto):
        if re.match(r"[a-z]+://", destino):
            continue
        ruta, _, fragmento = unquote(destino).partition("#")
        archivo = (fuente.parent / ruta).resolve() if ruta else fuente
        assert archivo.is_file(), (fuente, destino)
        if fragmento:
            titulos = re.findall(r"^#+\s+(.+)$", archivo.read_text(encoding="utf-8"), re.MULTILINE)
            anclas = {re.sub(r"\s", "-", re.sub(r"[^\w\s-]", "", t.lower())) for t in titulos}
            assert fragmento in anclas, (fuente, destino)
        enlaces += 1
    return enlaces


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    for fuente in CARPETA.glob("*.py"):
        ast.parse(fuente.read_text(encoding="utf-8"))
    for fuente in CARPETA.glob("*.json"):
        json.loads(fuente.read_text(encoding="utf-8"))
    enlaces = sum(comprobar_enlaces(f) for f in
                  (RAIZ / "ESTADO_INVESTIGACION.md", CARPETA / "CONGRUENCIAS.md",
                   CARPETA / "ORBITAS.md", CARPETA / "CONJUNTAS.md", CARPETA / "BARRERA.md",
                   RAIZ / "RutaDeJudasIscariote.md"))
    lean = leer("evidencia_lean.json")
    assert huella(RAIZ / lean["fuente"]) == lean["fuente_sha256_lf"]
    assert huella(CARPETA / "comprobar_lean.py") == lean["verificador_sha256_lf"]
    orbital = leer("evidencia_orbitas.json")
    assert huella(CARPETA / "comprobar_orbitas.py") == orbital["verificador_sha256_lf"]
    assert huella(CARPETA / "comprobar_lean.py") == orbital["apoyo_sha256_lf"]
    assert huella(CARPETA / "evidencia_orbitas.txt") == orbital["salida_sha256_lf"]
    for modulo in orbital["modulos"].values():
        assert huella(RAIZ / modulo["fuente"]) == modulo["fuente_sha256_lf"]
        assert modulo["resolucion_imports_directos_comprobada"]
    consultas = sum(len(m["axiomas"]) for m in orbital["modulos"].values())
    assert consultas == 29
    conjuntas = leer("evidencia_conjuntas.json")
    assert huella(CARPETA / "comprobar_conjuntas.py") == conjuntas["verificador_sha256_lf"]
    assert huella(CARPETA / "comprobar_lean.py") == conjuntas["apoyo_sha256_lf"]
    assert huella(CARPETA / "evidencia_conjuntas.txt") == conjuntas["salida_sha256_lf"]
    assert orbital["modulos"].keys() <= conjuntas["modulos"].keys()
    for modulo in conjuntas["modulos"].values():
        assert huella(RAIZ / modulo["fuente"]) == modulo["fuente_sha256_lf"]
        assert modulo["resolucion_imports_directos_comprobada"]
    consultas = sum(len(m["axiomas"]) for m in conjuntas["modulos"].values())
    assert consultas == 44
    cotejo = leer("cotejo.json")
    assert huella(CARPETA / "cotejar_congruencias.py") == cotejo["fuente_sha256_lf"]
    ventanas = leer("cotejo_ventanas.json")
    assert huella(CARPETA / "cotejar_ventanas.py") == ventanas["fuente_sha256_lf"]
    assert huella(CARPETA / "cotejar_congruencias.py") == ventanas["construcciones_sha256_lf"]
    cadenas = leer("cotejo_conjuntas.json")
    assert huella(CARPETA / "cotejar_conjuntas.py") == cadenas["fuente_sha256_lf"]
    assert huella(CARPETA / "cotejar_congruencias.py") == cadenas["construcciones_sha256_lf"]
    barrera = leer("certificado_barrera.json")
    assert huella(CARPETA / "certificar_barrera.py") == barrera["fuente_sha256_lf"]
    assert huella(CARPETA / "PerdicesBarreraTablas.lean") == barrera["tablas_lean_sha256_lf"]
    assert huella(CARPETA / "cotejar_congruencias.py") == barrera["apoyo_sha256_lf"]
    ternas = leer("cotejo_barrera.json")
    assert huella(CARPETA / "cotejar_barrera.py") == ternas["fuente_sha256_lf"]
    assert huella(CARPETA / "cotejar_congruencias.py") == ternas["apoyo_sha256_lf"]
    assert len(barrera["aristas"]) == 13 and barrera["empalmes"] == 0
    registro = leer("evidencia_registro.json")
    for nombre, esperada in registro["protegidos_sha256"].items():
        assert huella(RAIZ / nombre, False) == esperada
    assert huella(CARPETA / "alta_registro.json", False) == registro["alta_sha256"]
    assert huella(CARPETA / "verificar_alta.py", False) == registro["verificador_sha256"]
    assert huella(RAIZ / "guardarafirmaciones.py", False) == registro["generador_sha256"]
    resultado = dict(enlaces_locales=enlaces, axiomas_consultados=consultas,
                     controles_orbitales=cotejo["controles_orbitales"],
                     controles_bordes=cotejo["controles_bordes"],
                     familias_cotejadas=len(cotejo["optimos"]),
                     ventanas_cotejadas=ventanas["controles"],
                     cadenas_cotejadas=cadenas["controles"], parejas_cotejadas=cadenas["parejas"],
                     cadenas_barrera=ternas["controles"], ternas_barrera=ternas["triples"],
                     lean_barrera="Pendiente: borrador dividido por carga; compilacion interrumpida al cierre.",
                     palabras_estado=len((RAIZ / "ESTADO_INVESTIGACION.md").read_text(encoding="utf-8").split()),
                     catalogo_central_sin_modificar=True, historial_respuestas_sin_modificar=True,
                     archivos_sha256_lf={f.name: huella(f) for f in sorted(CARPETA.iterdir())
                                        if f.is_file() and f.resolve() != args.salida.resolve()})
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK: {enlaces} enlaces, {consultas} consultas y evidencias vigentes; fuentes centrales conservadas.")


if __name__ == "__main__":
    main()
