"""Propone arboles con testigos para la criba descontada y los divide en modulos Lean independientes.

La generacion reproduce el certificado exacto y su cotejo independiente.
Las hojas proporcionan el exponente; Lean comprueba la potencia y la cota.
Los subarboles se evaluan con decide +kernel y se unen mediante acepta_rama.
"""

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import tempfile
import time


@dataclass
class Nodo:
    estado: tuple
    nodos: int
    texto: str | None
    nombre: str | None = None


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--certificado", type=Path, required=True)
    analizador.add_argument("--cotejo", type=Path, required=True)
    analizador.add_argument("--espacio", required=True)
    analizador.add_argument("--directorio", type=Path, required=True)
    analizador.add_argument("--nodos-subarbol", type=int, required=True)
    analizador.add_argument("--nodos-modulo", type=int, required=True)
    argumentos = analizador.parse_args()
    assert re.fullmatch(r"Ocelotas[A-Za-z0-9]+", argumentos.espacio)
    assert argumentos.directorio.is_dir()
    assert 1 <= argumentos.nodos_subarbol <= argumentos.nodos_modulo
    datos = json.loads(argumentos.certificado.read_text(encoding="utf-8"))
    cotejo = json.loads(argumentos.cotejo.read_text(encoding="utf-8"))
    cotejo = cotejo["resultados"][argumentos.certificado.name]
    huella_datos = hashlib.sha256(argumentos.certificado.read_bytes()).hexdigest()
    assert cotejo["resultado"] == "sin discrepancias"
    assert cotejo["sha256_certificado"] == huella_datos
    assert datos["criba"] == "descuento" and not datos["pendientes"]
    inicio, limite, qmin, R, combustible = [datos[k] for k in
        ("inicio", "limite", "q_min", "rachas", "combustible")]
    assert limite >= inicio >= 2 and R >= 1 and qmin >= 1 and 0 < combustible < 800
    espacio = argumentos.espacio
    preambulo = ["import OcelotasCertificadosDescuento", "",
        "/-! Propuesta generada; todas las condiciones se comprueban en Lean. -/",
        f"namespace {espacio}",
        "open Ocelotas OcelotasContador OcelotasCribaPrefijosDescuento",
        "open OcelotasPrefijosDescuentoTestigos OcelotasCertificadosDescuento", "",
        "set_option maxRecDepth 100000", "set_option maxHeartbeats 0", ""]
    conteos = {"nodos": 0, "descenso": 0, "exceso_rachas": 0,
               "criba": 0, "vacio": 0, "pendiente": 0,
               "semillas_cubiertas": 0, "profundidad_maxima": 0}
    huella_hojas = hashlib.sha256()
    partes, uniones, grupo, nombres_grupo = [], [], [], []
    serial, coste_grupo, subarboles = 0, 0, 0
    inicio_reloj = time.perf_counter()

    def cabecera(nombre, estado):
        r, m, a, c, q, s, anterior, k = estado
        paridad = "true" if anterior else "false"
        llamada = f"{limite} {qmin} {R} {r} {m} {a} {c} {q} {s} {paridad} {combustible-k}"
        return f"theorem {nombre} : comprobar {llamada} = true := by", llamada

    with tempfile.TemporaryDirectory(prefix="ocelotas_testigos_") as temporal:
        provisional = Path(temporal)

        def guardar_grupo():
            nonlocal grupo, nombres_grupo, coste_grupo
            if not grupo:
                return
            modulo = f"{espacio}Parte{len(partes)+1:03d}"
            lineas = preambulo + grupo + [f"end {espacio}", ""]
            lineas.extend(f"#print axioms {espacio}.{n}" for n in nombres_grupo)
            archivo = provisional / (modulo + ".lean")
            archivo.write_text("\n".join(lineas) + "\n", encoding="utf-8")
            partes.append({"modulo": modulo, "nodos_evaluados": coste_grupo,
                           "subarboles": len(nombres_grupo),
                           "sha256": hashlib.sha256(archivo.read_bytes()).hexdigest()})
            grupo, nombres_grupo, coste_grupo = [], [], 0

        def exportar(nodo):
            nonlocal serial, coste_grupo, subarboles
            if nodo.nombre is not None:
                return nodo.nombre
            if coste_grupo + nodo.nodos > argumentos.nodos_modulo:
                guardar_grupo()
            nombre = f"nodo_{serial}"
            serial += 1
            subarboles += 1
            titulo, llamada = cabecera(nombre, nodo.estado)
            r, m, a, c, q, s, anterior, k = nodo.estado
            paridad = "true" if anterior else "false"
            grupo.extend([f"def testigo_{nombre} : Testigo :=", f"  {nodo.texto}", "",
                titulo,
                f"  exact verificar_correcto {limite} {qmin} {R} {combustible-k}",
                f"    testigo_{nombre} {r} {m} {a} {c} {q} {s} {paridad} (by decide +kernel)", ""])
            nombres_grupo.append(nombre)
            coste_grupo += nodo.nodos
            nodo.nombre, nodo.texto = nombre, None
            return nombre

        def visitar(r, m, a, c, q, s, anterior, k):
            nonlocal serial
            assert k < combustible, "El certificado propuesto agota combustible"
            estado = (r, m, a, c, q, s, anterior, k)
            conteos["nodos"] += 1
            conteos["profundidad_maxima"] = max(conteos["profundidad_maxima"], k)
            motivo, texto = None, None
            if r > limite:
                conteos["vacio"] += 1
                return Nodo(estado, 1, ".vacio")
            cantidad = (limite - r) // m + 1
            if a < m:
                assert c < r, "Cruce sin descenso: no se puede certificar esta rama"
                motivo, texto = "descenso", ".descenso"
            elif s > R:
                motivo, texto = "exceso_rachas", ".exceso"
            elif not anterior:
                maximo = a * (cantidad - 1) + c
                B = ((maximo + 1) ** 256 - 1).bit_length()
                assert maximo >= 1 and B >= 256
                cota = 0
                for _ in range(R - s):
                    cota = (25 * (B - 256) + 10144 * cota) // 6400
                if q + (R - s) + cota < qmin:
                    motivo, texto = "criba", f"(.criba {B})"
            if motivo is not None:
                conteos[motivo] += 1
                conteos["semillas_cubiertas"] += cantidad
                huella_hojas.update(f"{r},{m},{a},{c},{k},{q},{s},{motivo},{cantidad}\n".encode("ascii"))
                return Nodo(estado, 1, texto)
            hijos = []
            for b in (0, 1):
                x = a * b + c
                impar = bool(x % 2)
                hijos.append(visitar(r + m * b, 2 * m, 3 * a if impar else a,
                    (3 * x + 1) // 2 if impar else x // 2,
                    q + impar, s + (impar and not anterior), impar, k + 1))
            izquierda, derecha = hijos
            tamano = 1 + izquierda.nodos + derecha.nodos
            if izquierda.texto is not None and derecha.texto is not None and tamano <= argumentos.nodos_subarbol:
                return Nodo(estado, tamano, f"(.rama {izquierda.texto} {derecha.texto})")
            nombres = [exportar(hijo) for hijo in hijos]
            nombre = f"nodo_{serial}"
            serial += 1
            titulo, _ = cabecera(nombre, estado)
            uniones.extend([titulo,
                f"  exact acepta_rama (by decide +kernel) {nombres[0]} {nombres[1]}", ""])
            return Nodo(estado, tamano, None, nombre)

        raiz = visitar(inicio, 1, 1, inicio, 0, 0, False, 0)
        nombre_raiz = exportar(raiz)
        guardar_grupo()
        assert sum(p["nodos_evaluados"] for p in partes) + serial - subarboles == conteos["nodos"]
        assert conteos == datos["conteos"] == cotejo["conteos"]
        assert huella_hojas.hexdigest() == datos["sha256_hojas"] == cotejo["sha256_hojas"]
        assert conteos["semillas_cubiertas"] == limite - inicio + 1
        lineas = ["import " + parte["modulo"] for parte in partes] + preambulo[1:]
        lineas.extend(uniones)
        lineas.extend(["theorem certificado :",
            f"    comprobar {limite} {qmin} {R} {inicio} 1 1 {inicio} 0 0 false {combustible} = true := {nombre_raiz}", "",
            f"theorem descenso {{n k : ℕ}} (hinicio : {inicio} ≤ n) (hmax : n ≤ {limite})",
            f"    (hk : PrimerCruce n k) (hr : rachas n k ≤ {R}) (hq : {qmin} ≤ S k n) :",
            "    T^[k] n < n := OcelotasCribaPrefijosDescuento.certificado_descenso",
            "      (by decide +kernel) certificado hinicio hmax hk hr hq", "", f"end {espacio}", "",
            f"#print axioms {espacio}.certificado", f"#print axioms {espacio}.descenso"])
        principal = provisional / (espacio + ".lean")
        principal.write_text("\n".join(lineas) + "\n", encoding="utf-8")
        registro = {"estado": "fuentes propuestas; requieren compilacion y auditoria Lean",
            "certificado": argumentos.certificado.name, "sha256_certificado": huella_datos,
            "sha256_cotejo": hashlib.sha256(argumentos.cotejo.read_bytes()).hexdigest(),
            "sha256_generador": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "espacio": espacio, "nodos_subarbol": argumentos.nodos_subarbol,
            "nodos_modulo": argumentos.nodos_modulo, "conteos": conteos,
            "sha256_hojas": huella_hojas.hexdigest(), "subarboles": subarboles,
            "uniones": serial - subarboles, "partes": partes,
            "sha256_principal": hashlib.sha256(principal.read_bytes()).hexdigest(),
            "segundos": round(time.perf_counter() - inicio_reloj, 3)}
        for archivo in provisional.glob("*.lean"):
            (argumentos.directorio / archivo.name).write_bytes(archivo.read_bytes())
        salida = argumentos.directorio / ("generacion_" + espacio + ".json")
        salida.write_text(json.dumps(registro, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{conteos['nodos']} nodos, {subarboles} subarboles, {serial-subarboles} uniones, {len(partes)} partes.")


if __name__ == "__main__":
    main()
