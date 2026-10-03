"""Compila la cadena local de Ocelotas en un directorio temporal, sin huecos."""

import argparse
from contextlib import nullcontext
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


def huella(ruta):
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def auditar(salida, fuente):
    if re.search(r"\bsorryAx\b|declaration uses 'sorry'", salida):
        raise RuntimeError(f"Hueco en {fuente}")
    listas = re.findall(r"depends on axioms:\s*\[(.*?)\]", salida, flags=re.DOTALL)
    libres = "does not depend on any axioms" in salida
    if not listas and not libres:
        raise RuntimeError(f"Falta auditoria de axiomas en {fuente}")
    for lista in listas:
        usados = {elemento.strip() for elemento in lista.split(",") if elemento.strip()}
        if usados - {"propext", "Classical.choice", "Quot.sound"}:
            raise RuntimeError(f"Axiomas no admitidos en {fuente}: {usados}")


def reutilizable(entrada, fuente, prefijo, objeto):
    return (entrada.get("fuente") == fuente and entrada.get("prefijo") == prefijo
            and objeto.is_file() and entrada.get("objeto") == huella(objeto)
            and isinstance(entrada.get("auditoria"), str))


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--salida", type=Path)
    analizador.add_argument("--compilados", type=Path,
                            help="Conservar .olean y manifiesto; sin --reutilizar recompila todo")
    analizador.add_argument("--reutilizar", action="store_true",
                            help="Reutilizar el prefijo auditado cuyo entorno, fuentes y .olean coincidan")
    argumentos = analizador.parse_args()
    if argumentos.reutilizar and not argumentos.compilados:
        analizador.error("--reutilizar necesita --compilados")
    carpeta = Path(__file__).resolve().parent
    formal = carpeta.parent / "gao20260920" / "formal"
    lineas = ["SHA256 comprobador: " + hashlib.sha256(Path(__file__).read_bytes()).hexdigest()]

    def ejecutar(comando, entorno=None):
        resultado = subprocess.run(
            comando, cwd=formal, env=entorno, capture_output=True,
            text=True, encoding="utf-8", errors="strict", check=False,
        )
        salida = resultado.stdout + resultado.stderr
        lineas.extend(["Comando: " + " ".join(comando), salida,
                       f"Codigo de salida: {resultado.returncode}"])
        print(salida, end="", flush=True)
        if resultado.returncode or re.search(r"\bsorryAx\b|declaration uses 'sorry'", salida):
            raise RuntimeError("Compilacion fallida o dependencia de sorryAx")
        return salida

    try:
        version = ejecutar(["lake", "env", "lean", "--version"])
        firma_entorno = hashlib.sha256((version + str(carpeta) +
            huella(formal / "lean-toolchain") + huella(formal / "lake-manifest.json") +
            os.environ.get("LEAN_PATH", "")).encode("utf-8")).hexdigest()
        lineas.append("SHA256 entorno: " + firma_entorno)
        if argumentos.compilados:
            argumentos.compilados.mkdir(parents=True, exist_ok=True)
        contexto = (nullcontext(str(argumentos.compilados.resolve())) if argumentos.compilados
                    else tempfile.TemporaryDirectory(prefix="ocelotas_lean_"))
        with contexto as temporal:
            entorno = os.environ.copy()
            entorno["LEAN_PATH"] = temporal + os.pathsep + entorno.get("LEAN_PATH", "")
            archivo_manifiesto = Path(temporal) / "manifiesto_ocelotas.json"
            anteriores = {}
            if argumentos.reutilizar and archivo_manifiesto.exists():
                datos = json.loads(archivo_manifiesto.read_text(encoding="utf-8"))
                if datos.get("version") == 1 and datos.get("entorno") == firma_entorno:
                    anteriores = datos.get("modulos", {})
            manifiesto = {"version": 1, "entorno": firma_entorno, "modulos": {}}
            prefijo = firma_entorno
            conservar = argumentos.reutilizar
            compilados, reutilizados = 0, 0
            cadena = ["Ocelotas", "OcelotasRachas", "OcelotasTrayectorias", "OcelotasFinito",
                           "OcelotasCriba", "OcelotasCertificado", "OcelotasCierre",
                           "OcelotasContador", "OcelotasRhin", "OcelotasLMN",
                           "OcelotasLMNFuente", "OcelotasAfinada",
                           "OcelotasAfinadaTrayectorias", "OcelotasTreceBase",
                           "OcelotasTreceTabla", "OcelotasTreceFinito",
                           "OcelotasTreceCola", "OcelotasTrece", "OcelotasResiduos",
                           "OcelotasResiduosBloques", "OcelotasResiduosFinito",
                           "OcelotasNumerica", "OcelotasDieciochoTabla",
                           "OcelotasDieciochoCola", "OcelotasDieciocho",
                           "OcelotasGeometrica", "OcelotasPrefijos",
                           "OcelotasCribaPrefijos", "OcelotasDiecinuevePrefijos",
                           "OcelotasDiecinueveTabla", "OcelotasDiecinueveCola",
                           "OcelotasDiecinueve", "OcelotasPrefijosBloques",
                           "OcelotasVeintePrefijos", "OcelotasVeinteTabla",
                           "OcelotasVeinteCola", "OcelotasVeinte"]
            cadena.append("OcelotasTiempoRacional")
            for j in range(1, 10):
                modulo = f"OcelotasVeintiunaPrefijosHojas{j:02d}"
                if j == 7:
                    cadena.extend(modulo + f"Parte{i:02d}" for i in range(1, 26))
                cadena.append(modulo)
            cadena.extend(["OcelotasVeintiunaPrefijos", "OcelotasVeintiunaTabla",
                           "OcelotasVeintiunaCola", "OcelotasVeintiuna"])
            for nombre in cadena:
                fuente = carpeta / (nombre + ".lean")
                texto = fuente.read_text(encoding="utf-8")
                if re.search(r"\b(sorry|sorryAx|admit|axiom|native_decide)\b", texto):
                    raise RuntimeError(f"Revisar marcador no permitido en {fuente}")
                fuente_hash = huella(fuente)
                objeto = Path(temporal) / (nombre + ".olean")
                entrada = anteriores.get(nombre, {})
                if conservar and reutilizable(entrada, fuente_hash, prefijo, objeto):
                    salida = entrada["auditoria"]
                    auditar(salida, fuente)
                    reutilizados += 1
                    aviso = f"REUTILIZADO: {nombre}; auditoria original conservada en el manifiesto."
                    lineas.append(aviso)
                    print(aviso, flush=True)
                else:
                    conservar = False
                    salida = ejecutar(["lake", "env", "lean", "-R", str(carpeta),
                                       "-o", str(objeto), str(fuente)], entorno)
                    auditar(salida, fuente)
                    compilados += 1
                if fuente_hash != huella(fuente):
                    raise RuntimeError(f"La fuente cambio durante la comprobacion: {fuente}")
                objeto_hash = huella(objeto)
                manifiesto["modulos"][nombre] = {"fuente": fuente_hash, "prefijo": prefijo,
                                                "objeto": objeto_hash, "auditoria": salida}
                provisional = archivo_manifiesto.with_suffix(".tmp")
                provisional.write_text(json.dumps(manifiesto, ensure_ascii=False, indent=2) + "\n",
                                        encoding="utf-8")
                provisional.replace(archivo_manifiesto)
                lineas.extend([f"SHA256 {nombre}.lean: {fuente_hash}",
                               f"SHA256 {nombre}.olean: {objeto_hash}"])
                prefijo = hashlib.sha256((prefijo + nombre + fuente_hash + objeto_hash).encode("ascii")).hexdigest()
            lineas.append(f"COMPILADOS: {compilados}; REUTILIZADOS: {reutilizados}.")
            lineas.append("CADENA VALIDADA: solo axiomas estandar admitidos; ningun hueco.")
    finally:
        if argumentos.salida:
            argumentos.salida.write_text("\n".join(lineas) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
