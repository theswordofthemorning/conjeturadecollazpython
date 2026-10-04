"""Coteja por separado la evidencia final de 24 rachas. Solo lee.

No usa el codigo del comprobador. Rehace las huellas de fuentes y objetos,
el cierre de importaciones, las dependencias directas, el numero de
consultas de cada fuente, los nombres consultados y los axiomas de cada
respuesta. Al final resume tiempos y tamanos y los compara con 23.
"""

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
EVIDENCIA = CARPETA / "evidencia_veinticuatro_lean.json"
EVIDENCIA_23 = CARPETA / "evidencia_veintitres_lean.json"
PERMITIDOS = {"propext", "Classical.choice", "Quot.sound"}
PROHIBIDAS = r"\b(sorry|sorryAx|admit|axiom|native_decide|implemented_by|extern|unsafe|ofReduceBool|trustCompiler)\b"
RESPUESTA = re.compile(r"^'([^']+)' (?:depends on axioms: \[(.*?)\]|does not depend on any axioms)", re.M | re.S)

fallos = []


def huella(ruta):
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def comprobar(condicion, mensaje):
    if not condicion:
        fallos.append(mensaje)


def importaciones(nombre):
    texto = (CARPETA / (nombre + ".lean")).read_text(encoding="utf-8")
    directas = []
    for linea in re.findall(r"^import ([^\n]+)", texto, re.M):
        for dependencia in linea.split():
            if (CARPETA / (dependencia + ".lean")).is_file():
                directas.append(dependencia)
    return directas


def cierre(raiz):
    vistos, pila = set(), [raiz]
    while pila:
        nombre = pila.pop()
        if nombre not in vistos:
            vistos.add(nombre)
            pila.extend(importaciones(nombre))
    return vistos


def revisar_auditoria(nombre, auditoria, consultas, perfiles):
    texto = (CARPETA / (nombre + ".lean")).read_text(encoding="utf-8")
    pedidas = re.findall(r"^#print axioms (\S+)", texto, re.M)
    respuestas = RESPUESTA.findall(auditoria)
    comprobar(len(pedidas) == consultas, f"{nombre}: {len(pedidas)} #print axioms y {consultas} consultas")
    comprobar(len(respuestas) == consultas, f"{nombre}: {len(respuestas)} respuestas y {consultas} consultas")
    for pedida, (contestada, lista) in zip(pedidas, respuestas):
        comprobar(contestada == pedida or contestada.endswith("." + pedida),
                  f"{nombre}: se pidio {pedida} y respondio {contestada}")
        usados = frozenset(x.strip() for x in lista.split(",") if x.strip())
        comprobar(usados <= PERMITIDOS, f"{nombre}: axiomas {sorted(usados)} en {contestada}")
        perfiles[usados] += 1
    comprobar(not re.search(r"sorryAx|declaration uses 'sorry'|error", auditoria), f"{nombre}: hueco o error en la salida")
    return re.search(PROHIBIDAS, re.sub(r"^#print axioms .*$", "", texto, flags=re.M))


def grupo(nombre):
    for clave in ("PrefijosAltoParte", "PrefijosBajoParte", "TablaParte"):
        if clave in nombre:
            return clave
    return nombre


def mostrar(perfiles):
    for usados, cuantos in sorted(perfiles.items(), key=lambda x: -x[1]):
        print(f"   {cuantos:6d}  {sorted(usados) if usados else 'sin axiomas'}")


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--compilados-base", type=Path, required=True)
    analizador.add_argument("--compilados-extension", type=Path, required=True)
    argumentos = analizador.parse_args()
    base_objetos, extension_objetos = argumentos.compilados_base, argumentos.compilados_extension

    d = json.loads(EVIDENCIA.read_text(encoding="utf-8"))
    base, ext = d["prefijo_auditado"], d["extensiones"]
    print("SHA-256 de la evidencia:", huella(EVIDENCIA))
    print("estado:", d["estado"])
    print("lean:", d["version_lean"])
    comprobar(d["modulo"] == "OcelotasVeinticuatro", "modulo")
    comprobar(d["trabajos"] == 4, "trabajos")
    comprobar(d["compilados"] + d["reutilizados"] == len(ext), "compilados + reutilizados")
    comprobar(d["compilados"] == sum(not e["reutilizado"] for e in ext.values()), "compilados")
    comprobar(d["consultas"] == sum(e["consultas"] for e in ext.values()), "suma de consultas")
    comprobar(d["auditoria"] == "".join(e["auditoria"] for e in ext.values()), "auditoria conjunta")
    comprobar(d["sha256_comprobador"] == huella(CARPETA / "comprobar_extension_paralela.py"), "huella comprobador")
    comprobar(d["sha256_comprobador_base"] == huella(CARPETA / "comprobar_rachas_lean.py"), "huella comprobador base")

    necesarias = cierre("OcelotasVeinticuatro")
    comprobar(set(ext) == necesarias - set(base), "extensiones distintas del cierre de importaciones")
    print(f"cierre de importaciones: {len(necesarias)} modulos; base usada {len(necesarias & set(base))} de {len(base)}; extensiones {len(ext)}")

    perfiles_base, perfiles_ext = Counter(), Counter()
    prohibidas = []
    for nombre, e in base.items():
        comprobar(huella(CARPETA / (nombre + ".lean")) == e["fuente"], f"fuente base {nombre}")
        comprobar(huella(base_objetos / (nombre + ".olean")) == e["objeto"], f"objeto base {nombre}")
        consultas = len(RESPUESTA.findall(e["auditoria"]))
        if revisar_auditoria(nombre, e["auditoria"], consultas, perfiles_base):
            prohibidas.append(nombre)
    todos = {**base, **ext}
    tamanos = Counter()
    for nombre, e in ext.items():
        comprobar(huella(CARPETA / (nombre + ".lean")) == e["fuente"], f"fuente {nombre}")
        objeto = extension_objetos / (nombre + ".olean")
        comprobar(huella(objeto) == e["objeto"], f"objeto {nombre}")
        tamanos[grupo(nombre)] += objeto.stat().st_size
        directas = importaciones(nombre)
        esperadas = {x: {"fuente": todos[x]["fuente"], "objeto": todos[x]["objeto"]} for x in directas}
        comprobar(e["dependencias"] == esperadas, f"dependencias {nombre}")
        if revisar_auditoria(nombre, e["auditoria"], e["consultas"], perfiles_ext):
            prohibidas.append(nombre)
    print("palabras prohibidas en fuentes (fuera de #print axioms):", prohibidas or "ninguna")

    print(f"consultas de la base: {sum(perfiles_base.values())}")
    mostrar(perfiles_base)
    print(f"consultas de las extensiones: {sum(perfiles_ext.values())} (evidencia: {d['consultas']})")
    mostrar(perfiles_ext)
    print("respuestas finales:")
    for linea in ext["OcelotasVeinticuatro"]["auditoria"].splitlines():
        print("  ", linea)

    print("tiempos de compilacion por grupo (segundos de cada modulo, sumados):")
    por_grupo = {}
    for nombre, e in ext.items():
        por_grupo.setdefault(grupo(nombre), []).append((e["segundos_compilacion"], e["reutilizado"]))
    for g, lista in por_grupo.items():
        segundos = [s for s, _ in lista]
        print(f"   {g:42s} modulos {len(lista):4d}  reutilizados {sum(r for _, r in lista):4d}  "
              f"suma {sum(segundos):9.1f}  media {sum(segundos) / len(segundos):7.1f}  max {max(segundos):7.1f}  "
              f"olean {tamanos[g] / 2**20:8.1f} MiB")
    total = sum(e["segundos_compilacion"] for e in ext.values())
    print(f"   suma total {total:.1f} s = {total / 3600:.2f} h de proceso; olean total {sum(tamanos.values()) / 2**20:.1f} MiB")
    print(f"   duracion de la ultima ejecucion: {d['segundos']} s = {d['segundos'] / 3600:.2f} h")

    v = json.loads(EVIDENCIA_23.read_text(encoding="utf-8"))
    e23 = v["extensiones"]
    t23 = sum(e.get("segundos_compilacion", 0) for e in e23.values())
    print(f"23: {len(e23)} extensiones, {v['compilados']} compilados, {v['reutilizados']} reutilizados, "
          f"{v['consultas']} consultas, suma de compilacion {t23:.1f} s = {t23 / 3600:.2f} h")
    alto23 = [e.get("segundos_compilacion", 0) for n, e in e23.items() if "PrefijosAltoParte" in n]
    print(f"23 partes altas: {len(alto23)}, suma {sum(alto23):.1f} s")

    print()
    print("FALLOS:" if fallos else "SIN FALLOS: todas las comprobaciones pasan.")
    for f in fallos[:50]:
        print("  ", f)


if __name__ == "__main__":
    main()
