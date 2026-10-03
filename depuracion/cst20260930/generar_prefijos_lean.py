"""Genera un certificado por bloques para los dos intervalos de una tabla.

Las constantes y particiones son propuestas. Lean comprueba cada bloque
con decide +kernel y las condiciones del ensamblaje con acepta_rama.
"""

import argparse
import json
from pathlib import Path
import re


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--bajo", type=Path, required=True)
    analizador.add_argument("--alto", type=Path, required=True)
    analizador.add_argument("--profundidad", type=int, required=True)
    analizador.add_argument("--espacio", required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    analizador.add_argument("--hojas-por-modulo", type=int,
                            help="Separar hojas en modulos para limitar memoria de evaluacion")
    argumentos = analizador.parse_args()
    assert re.fullmatch(r"Ocelotas[A-Za-z0-9]+", argumentos.espacio)
    lineas = ["import OcelotasPrefijosBloques", "",
              "/-! Generado por generar_prefijos_lean.py; todos los bloques se comprueban en el núcleo. -/",
              f"namespace {argumentos.espacio}",
              "open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques", "",
              "set_option maxRecDepth 100000", "set_option maxHeartbeats 0", ""]
    fuentes = {}
    for nombre, archivo in [("Bajo", argumentos.bajo), ("Alto", argumentos.alto)]:
        datos = json.loads(archivo.read_text(encoding="utf-8"))
        assert datos["criba"] == "entera" and not datos["pendientes"]
        inicio, L, Q, R, F = [datos[k] for k in ("inicio", "limite", "q_min", "rachas", "combustible")]
        assert L >= inicio >= 2 and 0 <= argumentos.profundidad < F
        fuentes[nombre] = (inicio, L, Q, R, F)
        lineas.extend([f"namespace {nombre}", ""])
        nodos, bloques = 0, 0

        def visitar(r, m, a, c, q, s, anterior, k):
            nonlocal nodos, bloques
            identificador = nodos
            nodos += 1
            paridad = "true" if anterior else "false"
            cabecera = (f"theorem nodo_{identificador} : comprobar {L} {Q} {R} "
                        f"{r} {m} {a} {c} {q} {s} {paridad} {F-k} = true := by")
            termina = r > L or (a < m and c < r) or s > R
            if not termina and not anterior:
                X = a * ((L - r) // m) + c
                M = (X + 1).bit_length()
                C = 0
                for _ in range(R - s):
                    C = (5 * M + 8 * C - 1) // 5
                termina = q + C < Q
            if termina or k == argumentos.profundidad:
                bloques += not termina
                lineas.extend([cabecera, "  decide +kernel", ""])
            else:
                assert r <= L and m <= a and s <= R
                hijos = []
                for b in (0, 1):
                    x = a * b + c
                    impar = bool(x % 2)
                    hijos.append(visitar(r + m * b, 2 * m, 3 * a if impar else a,
                                         (3 * x + 1) // 2 if impar else x // 2,
                                         q + impar, s + (impar and not anterior), impar, k + 1))
                lineas.extend([cabecera,
                    "  exact acepta_rama (by decide +kernel) (by decide +kernel)",
                    "    (by decide +kernel) (by decide +kernel)",
                    f"    nodo_{hijos[0]} nodo_{hijos[1]}", ""])
            return identificador

        visitar(inicio, 1, 1, inicio, 0, 0, False, 0)
        lineas.extend([f"end {nombre}", ""])
        print(f"{nombre}: {nodos} nodos de ensamblaje, {bloques} bloques no resueltos a profundidad {argumentos.profundidad}.")
    for nombre, (inicio, L, Q, R, F) in fuentes.items():
        minuscula = nombre.lower()
        lineas.extend([f"theorem certificado_{minuscula} :",
            f"    comprobar {L} {Q} {R} {inicio} 1 1 {inicio} 0 0 false {F} = true := {nombre}.nodo_0", "",
            f"theorem descenso_{minuscula} {{n k : ℕ}} (hinicio : {inicio} ≤ n) (hmax : n ≤ {L})",
            f"    (hk : PrimerCruce n k) (hr : rachas n k ≤ {R}) (hq : {Q} ≤ S k n) :",
            f"    T^[k] n < n := certificado_descenso certificado_{minuscula} hinicio hmax hk hr hq", ""])
    lineas.extend([f"end {argumentos.espacio}", ""])
    for nombre in ["certificado_bajo", "certificado_alto", "descenso_bajo", "descenso_alto"]:
        lineas.append(f"#print axioms {argumentos.espacio}.{nombre}")
    texto = "\n".join(lineas) + "\n"
    if argumentos.hojas_por_modulo is not None:
        assert argumentos.hojas_por_modulo >= 1
        patron = r"theorem nodo_\d+ : [^\n]+ := by\n  decide \+kernel\n\n"
        hojas = []
        for nombre in ("Bajo", "Alto"):
            inicio = texto.index(f"namespace {nombre}\n")
            fin = texto.index(f"end {nombre}\n", inicio)
            tramo = texto[inicio:fin]
            hojas.extend((nombre, m.group()) for m in re.finditer(patron, tramo))
            texto = texto[:inicio] + re.sub(patron, "", tramo) + texto[fin:]
        modulos = []
        for inicio in range(0, len(hojas), argumentos.hojas_por_modulo):
            nombre_modulo = f"{argumentos.espacio}Hojas{len(modulos) + 1:02d}"
            modulos.append(nombre_modulo)
            grupo = hojas[inicio:inicio + argumentos.hojas_por_modulo]
            partes = ["import OcelotasPrefijosBloques", "",
                      "/-! Hojas generadas; evaluacion independiente en el nucleo. -/",
                      f"namespace {argumentos.espacio}",
                      "open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques",
                      "set_option maxRecDepth 100000", "set_option maxHeartbeats 0", ""]
            for nombre, prueba in grupo:
                partes.extend([f"namespace {nombre}", prueba.rstrip(), f"end {nombre}", ""])
            partes.append(f"end {argumentos.espacio}")
            for nombre, prueba in grupo:
                teorema = re.search(r"theorem (nodo_\d+)", prueba).group(1)
                partes.append(f"#print axioms {argumentos.espacio}.{nombre}.{teorema}")
            argumentos.salida.with_name(nombre_modulo + ".lean").write_text(
                "\n".join(partes) + "\n", encoding="utf-8")
        texto = "\n".join("import " + nombre for nombre in modulos) + "\n" + texto
        print(f"{len(hojas)} hojas separadas en {len(modulos)} modulos; ensamblaje sin reevaluarlas.")
    argumentos.salida.write_text(texto, encoding="utf-8")


if __name__ == "__main__":
    main()
