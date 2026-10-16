"""Valida el alta con el generador existente en copias temporales aisladas."""

import argparse
import copy
from contextlib import closing
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile


CARPETA = Path(__file__).resolve().parent
RAIZ = CARPETA.parents[2]


def huella(ruta):
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def guardar(ruta, datos):
    ruta.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    registro = RAIZ / "depuracion/coherencia20260913/registro.json"
    mapa = registro.with_name("mapa_investigacion.json")
    protegidos = [registro, mapa, RAIZ / "afirmaciones.db", RAIZ / "respuestas.db"]
    antes = {str(r.relative_to(RAIZ)): huella(r) for r in protegidos}
    base = json.loads(registro.read_text(encoding="utf-8"))
    mapa_base = json.loads(mapa.read_text(encoding="utf-8"))
    propuesta = json.loads((CARPETA / "alta_registro.json").read_text(encoding="utf-8"))
    altas = [propuesta["alta"]] + propuesta.get("altas_adicionales", [])
    assert len({alta["clave"] for alta in altas}) == len(altas)
    assert all(f["clave"] != alta["clave"] for f in base["altas"] for alta in altas)
    nuevo = copy.deepcopy(base)
    nuevo["altas"].extend(altas)
    mapa_nuevo = copy.deepcopy(mapa_base)
    piezas = [p for p in mapa_nuevo["piezas"]
              if propuesta["referencia_pieza"] in p["afirmaciones"]]
    assert len(piezas) == 1
    piezas[0]["afirmaciones"].extend(alta["clave"] for alta in altas)
    fuentes_nuevas = [alta["fichero"] for alta in altas]
    piezas[0]["fuentes"].extend(fuentes_nuevas)
    with tempfile.TemporaryDirectory(prefix="perdices_congruencias_codex_") as carpeta:
        temporal = Path(carpeta)
        assert temporal.resolve().parent == Path(tempfile.gettempdir()).resolve()
        assert temporal.name.startswith("perdices_congruencias_codex_")
        tablas = []
        for etiqueta, datos, mapa_datos in (("base", base, mapa_base), ("ampliado", nuevo, mapa_nuevo)):
            datos["mapa_investigacion"] = etiqueta + "_mapa.json"
            guardar(temporal / datos["mapa_investigacion"], mapa_datos)
            ruta_registro = temporal / (etiqueta + "_registro.json")
            guardar(ruta_registro, datos)
            destino = temporal / (etiqueta + ".db")
            proceso = subprocess.run([sys.executable, "-B", "-X", "utf8",
                                      str(RAIZ / "guardarafirmaciones.py"),
                                      "--registro", str(ruta_registro), "--salida", str(destino)],
                                     cwd=RAIZ, capture_output=True, text=True, encoding="utf-8", timeout=60)
            assert proceso.returncode == 0, proceso.stdout + proceso.stderr
            assert not proceso.stderr, proceso.stderr
            with closing(sqlite3.connect(destino)) as conexion:
                nombres = [f[0] for f in conexion.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")]
                # Identificadores provienen exclusivamente del esquema generado localmente.
                tablas.append({nombre: conexion.execute('SELECT * FROM "' + nombre + '" ORDER BY rowid').fetchall()
                               for nombre in nombres})
        anterior, posterior = tablas
        assert anterior.keys() == posterior.keys()
        for nombre in anterior:
            if nombre == "mapa_piezas":
                assert len(anterior[nombre]) == len(posterior[nombre])
                for vieja, nueva in zip(anterior[nombre], posterior[nombre]):
                    if vieja[0] == piezas[0]["id"]:
                        assert vieja[:-1] == nueva[:-1]
                        assert json.loads(nueva[-1]) == json.loads(vieja[-1]) + fuentes_nuevas
                    else:
                        assert vieja == nueva
            else:
                assert set(anterior[nombre]) <= set(posterior[nombre]), nombre
        assert posterior["afirmaciones"][:-len(altas)] == anterior["afirmaciones"]
        columnas = ("enunciado", "cuantificador", "estado", "fichero", "fuente", "notas")
        for fila, alta in zip(posterior["afirmaciones"][-len(altas):], altas):
            assert fila[1:] == tuple(alta[c] for c in columnas)
        diferencias = {nombre: len(posterior[nombre]) - len(anterior[nombre]) for nombre in anterior}
        filas_base, filas_ampliadas = len(anterior["afirmaciones"]), len(posterior["afirmaciones"])
    despues = {str(r.relative_to(RAIZ)): huella(r) for r in protegidos}
    assert antes == despues, "Alguna fuente compartida cambio durante la comprobacion; repetir con su nueva version."
    resultado = dict(alcance="Alta preparada y validada en bases temporales; no integrada en el catalogo central.",
                     filas_base=filas_base, filas_ampliadas_temporales=filas_ampliadas,
                     preservacion_literal_afirmaciones_previas=True,
                     unico_cambio_editorial_previo="Añadir las fuentes nuevas a la misma pieza, en copia temporal.",
                     diferencias_por_tabla=diferencias, protegidos_sha256=antes,
                     alta_sha256=huella(CARPETA / "alta_registro.json"),
                     generador_sha256=huella(RAIZ / "guardarafirmaciones.py"),
                     aplicador_sha256=huella(RAIZ / "registroafirmaciones.py"),
                     verificador_sha256=huella(Path(__file__)))
    guardar(args.salida, resultado)
    print(f"OK: {filas_base} filas conservadas, {filas_ampliadas} en copia temporal; fuentes compartidas intactas.")


if __name__ == "__main__":
    main()
