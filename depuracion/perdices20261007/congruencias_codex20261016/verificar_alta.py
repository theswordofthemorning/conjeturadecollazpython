"""Valida las altas con el generador; permite integrarlas tras cotejar la conservación."""

import argparse
import copy
from contextlib import closing
import hashlib
import json
import os
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


def leer_tablas(ruta):
    with closing(sqlite3.connect(ruta.resolve().as_uri() + "?mode=ro", uri=True)) as conexion:
        nombres = [f[0] for f in conexion.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")]
        # Identificadores procedentes únicamente del esquema del catálogo local.
        return {nombre: conexion.execute('SELECT * FROM "' + nombre + '" ORDER BY rowid').fetchall()
                for nombre in nombres}


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--salida", type=Path, required=True)
    analizador.add_argument("--integrar", action="store_true",
                            help="Integra sólo después del cotejo temporal y conserva todas las filas previas.")
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
    claves = [alta["clave"] for alta in altas]
    fuentes_nuevas = [alta["fichero"] for alta in altas]
    presentes = [f for f in base["altas"] if f["clave"] in claves]
    cantidad_integrada = len(presentes)
    integrado = cantidad_integrada == len(altas)
    escrito = False
    if cantidad_integrada:
        assert presentes == altas[:cantidad_integrada]
        assert base["altas"][-cantidad_integrada:] == presentes
        base["altas"] = base["altas"][:-cantidad_integrada]
        piezas_base = [p for p in mapa_base["piezas"]
                       if propuesta["referencia_pieza"] in p["afirmaciones"]]
        assert len(piezas_base) == 1
        pieza = piezas_base[0]
        assert pieza["afirmaciones"][-cantidad_integrada:] == claves[:cantidad_integrada]
        assert pieza["fuentes"][-cantidad_integrada:] == fuentes_nuevas[:cantidad_integrada]
        pieza["afirmaciones"] = pieza["afirmaciones"][:-cantidad_integrada]
        pieza["fuentes"] = pieza["fuentes"][:-cantidad_integrada]
    nuevo = copy.deepcopy(base)
    nuevo["altas"].extend(altas)
    mapa_nuevo = copy.deepcopy(mapa_base)
    piezas = [p for p in mapa_nuevo["piezas"]
              if propuesta["referencia_pieza"] in p["afirmaciones"]]
    assert len(piezas) == 1
    piezas[0]["afirmaciones"].extend(alta["clave"] for alta in altas)
    piezas[0]["fuentes"].extend(fuentes_nuevas)
    with tempfile.TemporaryDirectory(prefix="perdices_congruencias_codex_") as carpeta:
        temporal = Path(carpeta)
        assert temporal.resolve().parent == Path(tempfile.gettempdir()).resolve()
        assert temporal.name.startswith("perdices_congruencias_codex_")
        casos = [("base", base, mapa_base), ("ampliado", nuevo, mapa_nuevo)]
        if 0 < cantidad_integrada < len(altas):
            casos.append(("actual", json.loads(registro.read_text(encoding="utf-8")),
                          json.loads(mapa.read_text(encoding="utf-8"))))
        tablas = {}
        for etiqueta, datos, mapa_datos in casos:
            datos_temporales = copy.deepcopy(datos)
            datos_temporales["mapa_investigacion"] = etiqueta + "_mapa.json"
            guardar(temporal / datos_temporales["mapa_investigacion"], mapa_datos)
            ruta_registro = temporal / (etiqueta + "_registro.json")
            guardar(ruta_registro, datos_temporales)
            destino = temporal / (etiqueta + ".db")
            proceso = subprocess.run([sys.executable, "-B", "-X", "utf8",
                                      str(RAIZ / "guardarafirmaciones.py"),
                                      "--registro", str(ruta_registro), "--salida", str(destino)],
                                     cwd=RAIZ, capture_output=True, text=True, encoding="utf-8", timeout=60)
            assert proceso.returncode == 0, proceso.stdout + proceso.stderr
            assert not proceso.stderr, proceso.stderr
            tablas[etiqueta] = leer_tablas(destino)
        anterior, posterior = tablas["base"], tablas["ampliado"]
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
        actual = tablas.get("actual", posterior if integrado else anterior)
        filas_actuales = len(actual["afirmaciones"])
        assert posterior["afirmaciones"][:filas_actuales] == actual["afirmaciones"]
        assert leer_tablas(RAIZ / "afirmaciones.db") == actual, \
            "El catálogo central difiere del generado; no integrar sobre cambios no conciliados."
        assert antes == {str(r.relative_to(RAIZ)): huella(r) for r in protegidos}
        if args.integrar and not integrado:
            originales = {ruta: ruta.read_bytes() for ruta in (registro, mapa, RAIZ / "afirmaciones.db")}
            try:
                guardar(registro, nuevo)
                guardar(mapa, mapa_nuevo)
                # El generador ya validó integridad, relaciones y lectura de todas las tablas.
                # El reemplazo se hace en el mismo directorio para que sea atómico en Windows.
                with tempfile.NamedTemporaryFile(dir=RAIZ, prefix="afirmaciones_perdices_",
                                                 suffix=".tmp", delete=False) as archivo:
                    intermedio = Path(archivo.name)
                    archivo.write((temporal / "ampliado.db").read_bytes())
                os.replace(intermedio, RAIZ / "afirmaciones.db")
                assert leer_tablas(RAIZ / "afirmaciones.db") == posterior
                integrado = True
                escrito = True
            except BaseException:
                for ruta, contenido in originales.items():
                    ruta.write_bytes(contenido)
                raise
            finally:
                if "intermedio" in locals() and intermedio.exists():
                    intermedio.unlink()
    despues = {str(r.relative_to(RAIZ)): huella(r) for r in protegidos}
    assert antes["respuestas.db"] == despues["respuestas.db"]
    if not escrito:
        assert antes == despues, "Alguna fuente compartida cambio durante la comprobacion."
    resultado = dict(alcance=("Altas integradas y cotejadas con el catálogo central." if integrado else
                             "Altas validadas en bases temporales; integración central pendiente."),
                     integrado=integrado,
                     filas_base=filas_base, filas_ampliadas_temporales=filas_ampliadas,
                     filas_centrales_antes=filas_actuales,
                     preservacion_literal_afirmaciones_previas=True,
                     unico_cambio_editorial_previo="Añadir las fuentes nuevas a la misma pieza.",
                     diferencias_por_tabla=diferencias, protegidos_sha256=despues,
                     catalogo_central_cotejado=True, historial_respuestas_sin_modificar=True,
                     alta_sha256=huella(CARPETA / "alta_registro.json"),
                     generador_sha256=huella(RAIZ / "guardarafirmaciones.py"),
                     aplicador_sha256=huella(RAIZ / "registroafirmaciones.py"),
                     verificador_sha256=huella(Path(__file__)))
    guardar(args.salida, resultado)
    print(f"OK: {filas_base} filas conservadas, {filas_ampliadas} validadas; integrado={integrado}.")


if __name__ == "__main__":
    main()
