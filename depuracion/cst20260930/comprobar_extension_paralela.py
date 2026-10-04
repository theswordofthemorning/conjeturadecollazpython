"""Compila extensiones en paralelo y conserva cada modulo auditado para poder reanudar.

Copia de comprobar_extension_persistente.py con las mismas comprobaciones.
Solo cambia el reparto: compila a la vez hasta --trabajos modulos cuyas
dependencias directas ya estan compiladas y auditadas, con prioridad baja.
Solo el proceso principal escribe el manifiesto y la evidencia.
Usar un directorio de extensiones distinto del prefijo compartido y una
sola ejecucion por directorio. La reutilizacion verifica entorno, fuentes,
objetos, dependencias directas y auditoria; cada avance se guarda atomicamente.
"""

import argparse
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

from comprobar_rachas_lean import auditar, huella, reutilizable


def escribir_atomico(ruta, datos):
    temporal = ruta.with_suffix(ruta.suffix + ".tmp")
    temporal.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporal.replace(ruta)


def compilar(comando, formal, entorno):
    inicio = time.perf_counter()
    resultado = subprocess.run(comando, cwd=formal, env=entorno, capture_output=True,
        text=True, encoding="utf-8", check=False,
        creationflags=getattr(subprocess, "BELOW_NORMAL_PRIORITY_CLASS", 0))
    return resultado.returncode, resultado.stdout + resultado.stderr, time.perf_counter() - inicio


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--modulo", required=True)
    analizador.add_argument("--compilados-base", type=Path, required=True)
    analizador.add_argument("--compilados-extension", type=Path, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    analizador.add_argument("--trabajos", type=int, required=True)
    argumentos = analizador.parse_args()
    assert re.fullmatch(r"Ocelotas[A-Za-z0-9]+", argumentos.modulo)
    assert argumentos.trabajos >= 1
    carpeta = Path(__file__).resolve().parent
    formal = carpeta.parent / "gao20260920/formal"
    almacen_base = argumentos.compilados_base.resolve()
    almacen = argumentos.compilados_extension.resolve()
    assert almacen != almacen_base
    almacen.mkdir(parents=True, exist_ok=True)
    hash_comprobador = huella(Path(__file__))
    hash_base = huella(carpeta / "comprobar_rachas_lean.py")
    version = subprocess.run(["lake", "env", "lean", "--version"], cwd=formal,
        capture_output=True, text=True, encoding="utf-8", check=True).stdout
    firma = hashlib.sha256((version + str(carpeta) + huella(formal / "lean-toolchain") +
        huella(formal / "lake-manifest.json") + os.environ.get("LEAN_PATH", "")).encode("utf-8")).hexdigest()
    firma_almacen = hashlib.sha256((firma + str(almacen_base) + str(almacen) +
        hash_comprobador + hash_base).encode("utf-8")).hexdigest()
    manifiesto_base = json.loads((almacen_base / "manifiesto_ocelotas.json").read_text(encoding="utf-8"))
    assert manifiesto_base["version"] == 1 and manifiesto_base["entorno"] == firma
    orden, directas, pendientes, visitadas = [], {}, set(), set()

    def visitar(nombre):
        if nombre in pendientes:
            raise ValueError(f"Importaciones circulares en {nombre}")
        if nombre in visitadas:
            return
        pendientes.add(nombre)
        fuente = carpeta / (nombre + ".lean")
        texto = fuente.read_text(encoding="utf-8")
        dependencias = []
        for linea in re.findall(r"^import ([^\n]+)", texto, re.MULTILINE):
            for dependencia in linea.split():
                if (carpeta / (dependencia + ".lean")).is_file():
                    dependencias.append(dependencia)
                    visitar(dependencia)
        directas[nombre] = dependencias
        pendientes.remove(nombre)
        visitadas.add(nombre)
        orden.append(nombre)

    visitar(argumentos.modulo)
    necesarias_base = set(orden) & manifiesto_base["modulos"].keys()
    assert necesarias_base
    prefijo, base = firma, {}
    for nombre, entrada in manifiesto_base["modulos"].items():
        objeto = almacen_base / (nombre + ".olean")
        assert reutilizable(entrada, huella(carpeta / (nombre + ".lean")), prefijo, objeto), nombre
        auditar(entrada["auditoria"], nombre)
        base[nombre] = entrada
        prefijo = hashlib.sha256((prefijo + nombre + entrada["fuente"] + entrada["objeto"]).encode("ascii")).hexdigest()
        if necesarias_base <= base.keys():
            break
    for nombre, entrada in base.items():
        sombra = almacen / (nombre + ".olean")
        assert not sombra.exists() or huella(sombra) == entrada["objeto"], f"Objeto que oculta la base: {nombre}"
    archivo_manifiesto = almacen / "manifiesto_extensiones.json"
    datos_anteriores = {}
    if archivo_manifiesto.exists():
        previo = json.loads(archivo_manifiesto.read_text(encoding="utf-8"))
        if previo.get("version") == 1 and previo.get("entorno") == firma_almacen:
            datos_anteriores = previo["modulos"]
    manifiesto = {"version": 1, "entorno": firma_almacen, "modulos": datos_anteriores.copy()}
    entorno = os.environ.copy()
    entorno["LEAN_PATH"] = os.pathsep.join([str(almacen), str(almacen_base), entorno.get("LEAN_PATH", "")])
    extensiones, disponibles = {}, base.copy()
    lineas = [version, "SHA256 comprobador: " + hash_comprobador + "\n",
              f"Trabajos simultaneos: {argumentos.trabajos}\n"]
    compilados, reusados = 0, 0
    inicio_total = time.perf_counter()

    def guardar(nombre, entrada, reusado):
        manifiesto["modulos"][nombre] = entrada
        escribir_atomico(archivo_manifiesto, manifiesto)
        disponibles[nombre] = entrada
        extensiones[nombre] = {**entrada, "reutilizado": reusado}
        argumentos.salida.with_suffix(".txt").write_text("".join(lineas), encoding="utf-8")

    restantes = [nombre for nombre in orden if nombre not in base]
    en_curso = {}
    with ThreadPoolExecutor(max_workers=argumentos.trabajos) as ejecutor:
        while restantes or en_curso:
            for nombre in list(restantes):
                if len(en_curso) >= argumentos.trabajos:
                    break
                if not all(d in disponibles for d in directas[nombre]):
                    continue
                restantes.remove(nombre)
                fuente = carpeta / (nombre + ".lean")
                texto = fuente.read_text(encoding="utf-8")
                assert not re.search(r"\b(sorry|sorryAx|admit|axiom|native_decide)\b", texto)
                hash_fuente = huella(fuente)
                objeto = almacen / (nombre + ".olean")
                firmas_dependencias = {d: {k: disponibles[d][k] for k in ("fuente", "objeto")}
                                       for d in directas[nombre]}
                entrada = datos_anteriores.get(nombre)
                numero = len(re.findall(r"^#print axioms ", texto, re.MULTILINE))
                puede_reusar = bool(entrada and entrada.get("fuente") == hash_fuente and
                    entrada.get("dependencias") == firmas_dependencias and objeto.is_file() and
                    entrada.get("objeto") == huella(objeto) and entrada.get("consultas") == numero)
                if puede_reusar:
                    auditar(entrada["auditoria"], fuente)
                    respuestas = len(re.findall(r"depends on axioms:|does not depend on any axioms", entrada["auditoria"]))
                    assert respuestas == numero > 0
                    reusados += 1
                    print(f"REUTILIZADO: {nombre}", flush=True)
                    lineas.append(f"REUTILIZADO: {nombre}; auditoria original conservada.\n")
                    guardar(nombre, entrada.copy(), True)
                else:
                    comando = ["lake", "env", "lean", "-R", str(carpeta), "-o", str(objeto), str(fuente)]
                    print(f"COMPILANDO: {nombre}", flush=True)
                    futuro = ejecutor.submit(compilar, comando, formal, entorno)
                    en_curso[futuro] = (nombre, fuente, hash_fuente, objeto, firmas_dependencias,
                                        numero, comando)
            if not en_curso:
                assert not restantes, "Dependencias sin resolver"
                break
            listos, _ = wait(en_curso, return_when=FIRST_COMPLETED)
            for futuro in listos:
                nombre, fuente, hash_fuente, objeto, firmas_dependencias, numero, comando = en_curso.pop(futuro)
                codigo, salida, segundos = futuro.result()
                print(f"TERMINADO: {nombre}", flush=True)
                print(salida, end="", flush=True)
                lineas.extend([f"MODULO: {nombre}; segundos: {segundos:.3f}\n", salida,
                               f"Codigo: {codigo}\n"])
                argumentos.salida.with_suffix(".txt").write_text("".join(lineas), encoding="utf-8")
                assert codigo == 0, f"Compilacion fallida: {nombre}"
                auditar(salida, fuente)
                respuestas = len(re.findall(r"depends on axioms:|does not depend on any axioms", salida))
                assert respuestas == numero > 0
                assert huella(fuente) == hash_fuente
                entrada = {"fuente": hash_fuente, "objeto": huella(objeto),
                           "dependencias": firmas_dependencias, "auditoria": salida,
                           "consultas": numero, "comando": comando,
                           "segundos_compilacion": round(segundos, 3)}
                compilados += 1
                guardar(nombre, entrada, False)
    extensiones = {nombre: extensiones[nombre] for nombre in orden if nombre in extensiones}
    for nombre, entrada in base.items():
        assert huella(carpeta / (nombre + ".lean")) == entrada["fuente"]
        assert huella(almacen_base / (nombre + ".olean")) == entrada["objeto"]
    for nombre, entrada in extensiones.items():
        assert huella(carpeta / (nombre + ".lean")) == entrada["fuente"]
        assert huella(almacen / (nombre + ".olean")) == entrada["objeto"]
    assert huella(Path(__file__)) == hash_comprobador
    assert huella(carpeta / "comprobar_rachas_lean.py") == hash_base
    evidencia = {"estado": "compilado y auditado; objetos persistentes comprobados por huellas",
        "version_lean": version.strip(), "entorno_base": firma, "entorno": firma_almacen,
        "sha256_comprobador": hash_comprobador, "sha256_comprobador_base": hash_base,
        "modulo": argumentos.modulo, "prefijo_auditado": base, "extensiones": extensiones,
        "compilados": compilados, "reutilizados": reusados, "trabajos": argumentos.trabajos,
        "consultas": sum(e["consultas"] for e in extensiones.values()),
        "auditoria": "".join(e["auditoria"] for e in extensiones.values()),
        "segundos": round(time.perf_counter() - inicio_total, 3)}
    escribir_atomico(argumentos.salida, evidencia)
    print(f"OK: {compilados} compilados, {reusados} reutilizados, {evidencia['consultas']} consultas.")


if __name__ == "__main__":
    main()
