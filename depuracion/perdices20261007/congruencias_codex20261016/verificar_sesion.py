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
                   CARPETA / "RELOJ_TERMINAL.md", CARPETA / "PENDIENTE_UNO.md",
                   CARPETA / "RELOJ_RACHAS.md", CARPETA / "DEFECTO_INTERIOR.md",
                   CARPETA / "CONTEXTO_INTERIOR.md",
                   CARPETA / "COMPENSACION_RELATIVA.md",
                   CARPETA / "RUTA_CODEX.md",
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
    ponderada = leer("cotejo_ponderada.json")
    for nombre, esperada in ponderada["fuentes_sha256_lf"].items():
        assert huella(CARPETA / nombre) == esperada
    assert ponderada["controles"] == sum(ponderada["por_numero_ventanas"].values())
    assert all(ponderada["por_numero_ventanas"][str(cantidad)] > 0 for cantidad in range(4))
    assert len(barrera["aristas"]) == 13 and barrera["empalmes"] == 0
    formal = leer("evidencia_barrera.json")
    assert huella(CARPETA / "comprobar_barrera.py") == formal["verificador_sha256_lf"]
    assert huella(CARPETA / "comprobar_lean.py") == formal["apoyo_sha256_lf"]
    assert huella(CARPETA / "evidencia_barrera.txt") == formal["salida_sha256_lf"]
    assert formal["version_lean"].startswith("Lean (version 4.32.2,")
    assert formal["revision_mathlib"] == conjuntas["revision_mathlib"]
    assert conjuntas["modulos"].keys() <= formal["modulos"].keys()
    for nombre, modulo in formal["modulos"].items():
        assert huella(RAIZ / modulo["fuente"]) == modulo["fuente_sha256_lf"]
        assert modulo["resolucion_imports_directos_comprobada"]
        for dependencia, esperada in modulo["imports_locales_recompilados"].items():
            assert formal["modulos"][dependencia]["objeto_sha256"] == esperada
        for axiomas in modulo["axiomas"].values():
            assert set(axiomas) <= {"propext", "Classical.choice", "Quot.sound"}
        if nombre in conjuntas["modulos"]:
            assert modulo["fuente_sha256_lf"] == conjuntas["modulos"][nombre]["fuente_sha256_lf"]
            assert modulo["axiomas"] == conjuntas["modulos"][nombre]["axiomas"]
    consultas = sum(len(m["axiomas"]) for m in formal["modulos"].values())
    assert consultas == 70
    reloj = leer("evidencia_reloj.json")
    assert huella(CARPETA / "comprobar_reloj.py") == reloj["verificador_sha256_lf"]
    assert huella(CARPETA / "comprobar_lean.py") == reloj["apoyo_sha256_lf"]
    assert huella(CARPETA / "evidencia_reloj.txt") == reloj["salida_sha256_lf"]
    assert reloj["version_lean"] == formal["version_lean"]
    assert reloj["revision_mathlib"] == formal["revision_mathlib"]
    for nombre, modulo in reloj["modulos"].items():
        assert huella(RAIZ / modulo["fuente"]) == modulo["fuente_sha256_lf"]
        assert modulo["resolucion_imports_directos_comprobada"]
        for dependencia, esperada in modulo["imports_locales_recompilados"].items():
            assert reloj["modulos"][dependencia]["objeto_sha256"] == esperada
        for axiomas in modulo["axiomas"].values():
            assert set(axiomas) <= {"propext", "Classical.choice", "Quot.sound"}
        if nombre in formal["modulos"]:
            assert modulo["fuente_sha256_lf"] == formal["modulos"][nombre]["fuente_sha256_lf"]
            assert modulo["axiomas"] == formal["modulos"][nombre]["axiomas"]
        else:
            consultas += len(modulo["axiomas"])
    assert sum(len(m["axiomas"]) for m in reloj["modulos"].values()) == 22
    assert consultas == 84
    continuaciones = leer("cotejo_reloj.json")
    for nombre, esperada in continuaciones["fuentes_sha256_lf"].items():
        assert huella(CARPETA / nombre) == esperada
    assert continuaciones["continuaciones"] == sum(continuaciones["por_potencial"].values())
    assert continuaciones["continuaciones"] == sum(continuaciones["por_numero_bloques"].values())
    assert continuaciones["con_palabra_vacia"] > 0
    assert all(continuaciones["restos_carga_b"][str(r)] > 0 for r in range(3))
    pendiente = leer("evidencia_pendiente.json")
    assert huella(CARPETA / "comprobar_pendiente.py") == pendiente["verificador_sha256_lf"]
    assert huella(CARPETA / "comprobar_lean.py") == pendiente["apoyo_sha256_lf"]
    assert huella(CARPETA / "evidencia_pendiente.txt") == pendiente["salida_sha256_lf"]
    assert pendiente["version_lean"] == formal["version_lean"]
    assert pendiente["revision_mathlib"] == formal["revision_mathlib"]
    assert reloj["modulos"].keys() <= pendiente["modulos"].keys()
    for nombre, modulo in pendiente["modulos"].items():
        assert huella(RAIZ / modulo["fuente"]) == modulo["fuente_sha256_lf"]
        assert modulo["resolucion_imports_directos_comprobada"]
        for dependencia, esperada in modulo["imports_locales_recompilados"].items():
            assert pendiente["modulos"][dependencia]["objeto_sha256"] == esperada
        for axiomas in modulo["axiomas"].values():
            assert set(axiomas) <= {"propext", "Classical.choice", "Quot.sound"}
        if nombre in reloj["modulos"]:
            assert modulo["fuente_sha256_lf"] == reloj["modulos"][nombre]["fuente_sha256_lf"]
            assert modulo["axiomas"] == reloj["modulos"][nombre]["axiomas"]
        else:
            consultas += len(modulo["axiomas"])
    assert sum(len(m["axiomas"]) for m in pendiente["modulos"].values()) == 29
    assert consultas == 91
    familia = leer("cotejo_pendiente.json")
    for nombre, esperada in familia["fuentes_sha256_lf"].items():
        assert huella(CARPETA / nombre) == esperada
    assert familia["casos"] == len(familia["familia"]) + len(familia["bordes"])
    assert familia["recorridos_completos"] == familia["casos"] * familia["parametros"]["traslados"]
    assert {f["a"] for f in familia["familia"]} == set(range(2, familia["parametros"]["a_max"] + 1))
    assert {0, 1} <= {f["a"] for f in familia["bordes"]}
    assert all(f["exceso"] >= f["a"] for f in familia["familia"] + familia["bordes"])
    rachas = leer("evidencia_rachas.json")
    assert huella(CARPETA / "comprobar_rachas.py") == rachas["verificador_sha256_lf"]
    assert huella(CARPETA / "comprobar_lean.py") == rachas["apoyo_sha256_lf"]
    assert huella(CARPETA / "evidencia_rachas.txt") == rachas["salida_sha256_lf"]
    assert rachas["version_lean"] == formal["version_lean"]
    assert rachas["revision_mathlib"] == formal["revision_mathlib"]
    anteriores = {**formal["modulos"], **reloj["modulos"], **pendiente["modulos"]}
    for nombre, modulo in rachas["modulos"].items():
        assert huella(RAIZ / modulo["fuente"]) == modulo["fuente_sha256_lf"]
        assert modulo["resolucion_imports_directos_comprobada"]
        for dependencia, esperada in modulo["imports_locales_recompilados"].items():
            assert rachas["modulos"][dependencia]["objeto_sha256"] == esperada
        for axiomas in modulo["axiomas"].values():
            assert set(axiomas) <= {"propext", "Classical.choice", "Quot.sound"}
        if nombre in anteriores:
            assert modulo["fuente_sha256_lf"] == anteriores[nombre]["fuente_sha256_lf"]
            assert modulo["axiomas"] == anteriores[nombre]["axiomas"]
        else:
            consultas += len(modulo["axiomas"])
    assert sum(len(m["axiomas"]) for m in rachas["modulos"].values()) == 46
    assert consultas == 115
    coste_rachas = leer("cotejo_rachas.json")
    for nombre, esperada in coste_rachas["fuentes_sha256_lf"].items():
        assert huella(CARPETA / nombre) == esperada
    assert coste_rachas["recorridos"] == sum(coste_rachas["por_rachas"].values())
    assert coste_rachas["recorridos"] == coste_rachas["palabras"] * coste_rachas["parametros"]["traslados"]
    assert coste_rachas["por_rachas"]["0"] > 0
    assert len(coste_rachas["modelos"]) == 2 * coste_rachas["parametros"]["rachas_modelo_max"]
    assert coste_rachas["modelos_con_reserva"] == 4 * len(coste_rachas["modelos"])
    defecto = leer("evidencia_defecto.json")
    assert huella(CARPETA / "comprobar_defecto.py") == defecto["verificador_sha256_lf"]
    assert huella(CARPETA / "comprobar_lean.py") == defecto["apoyo_sha256_lf"]
    assert huella(CARPETA / "evidencia_defecto.txt") == defecto["salida_sha256_lf"]
    assert defecto["version_lean"] == formal["version_lean"]
    assert defecto["revision_mathlib"] == formal["revision_mathlib"]
    anteriores.update(rachas["modulos"])
    for nombre, modulo in defecto["modulos"].items():
        assert huella(RAIZ / modulo["fuente"]) == modulo["fuente_sha256_lf"]
        assert modulo["resolucion_imports_directos_comprobada"]
        for dependencia, esperada in modulo["imports_locales_recompilados"].items():
            assert defecto["modulos"][dependencia]["objeto_sha256"] == esperada
        for axiomas in modulo["axiomas"].values():
            assert set(axiomas) <= {"propext", "Classical.choice", "Quot.sound"}
        if nombre in anteriores:
            assert modulo["fuente_sha256_lf"] == anteriores[nombre]["fuente_sha256_lf"]
            assert modulo["axiomas"] == anteriores[nombre]["axiomas"]
        else:
            consultas += len(modulo["axiomas"])
    assert sum(len(m["axiomas"]) for m in defecto["modulos"].values()) == 28
    assert consultas == 121
    interiores = leer("cotejo_defecto.json")
    for nombre, esperada in interiores["fuentes_sha256_lf"].items():
        assert huella(CARPETA / nombre) == esperada
    assert interiores["prefijos"] == len(interiores["familias"])
    assert interiores["casos"] == interiores["prefijos"] * interiores["parametros"]["miembros"]
    assert interiores["bordes_cola_sin_prefijo"] == 13
    assert interiores["bordes"] >= interiores["bordes_cola_sin_prefijo"]
    for familia_interior in interiores["familias"]:
        assert familia_interior["prefijo"].endswith("B")
        assert len(familia_interior["miembros"]) == interiores["parametros"]["miembros"]
        for miembro in familia_interior["miembros"]:
            assert miembro["k"] % familia_interior["periodo"] == familia_interior["residuo_k"]
            assert miembro["exceso"] == familia_interior["pasos"] + miembro["k"] + 3 - miembro["ell"]
    contexto = leer("evidencia_contexto.json")
    assert huella(CARPETA / "comprobar_contexto.py") == contexto["verificador_sha256_lf"]
    assert huella(CARPETA / "comprobar_lean.py") == contexto["apoyo_sha256_lf"]
    assert huella(CARPETA / "evidencia_contexto.txt") == contexto["salida_sha256_lf"]
    assert contexto["version_lean"] == formal["version_lean"]
    assert contexto["revision_mathlib"] == formal["revision_mathlib"]
    anteriores.update(defecto["modulos"])
    for nombre, modulo in contexto["modulos"].items():
        assert huella(RAIZ / modulo["fuente"]) == modulo["fuente_sha256_lf"]
        assert modulo["resolucion_imports_directos_comprobada"]
        for dependencia, esperada in modulo["imports_locales_recompilados"].items():
            assert contexto["modulos"][dependencia]["objeto_sha256"] == esperada
        for axiomas in modulo["axiomas"].values():
            assert set(axiomas) <= {"propext", "Classical.choice", "Quot.sound"}
        if nombre in anteriores:
            assert modulo["fuente_sha256_lf"] == anteriores[nombre]["fuente_sha256_lf"]
            assert modulo["axiomas"] == anteriores[nombre]["axiomas"]
        else:
            consultas += len(modulo["axiomas"])
    assert sum(len(m["axiomas"]) for m in contexto["modulos"].values()) == 29
    assert consultas == 128
    bilaterales = leer("cotejo_contexto.json")
    for nombre, esperada in bilaterales["fuentes_sha256_lf"].items():
        assert huella(CARPETA / nombre) == esperada
    assert bilaterales["contextos"] == len(bilaterales["familias"])
    assert bilaterales["casos"] == bilaterales["contextos"] * bilaterales["parametros"]["miembros"]
    assert bilaterales["bordes"] == 21
    assert any(f["sufijo"] == "" for f in bilaterales["familias"])
    for familia_bilateral in bilaterales["familias"]:
        assert familia_bilateral["prefijo"].endswith("B")
        assert len(familia_bilateral["miembros"]) == bilaterales["parametros"]["miembros"]
        sufijo = sum(1 if p == "A" else 3 for p in familia_bilateral["sufijo"])
        for miembro in familia_bilateral["miembros"]:
            assert miembro["a"] % 2 == 1
            assert miembro["a"] % familia_bilateral["periodo"] == familia_bilateral["residuo"]
            assert miembro["largo"] - miembro["ell"] == sufijo + familia_bilateral["d"] - 1
    relativa = leer("evidencia_relativa.json")
    assert huella(CARPETA / "comprobar_relativa.py") == relativa["verificador_sha256_lf"]
    assert huella(CARPETA / "comprobar_lean.py") == relativa["apoyo_sha256_lf"]
    assert huella(CARPETA / "evidencia_relativa.txt") == relativa["salida_sha256_lf"]
    assert relativa["version_lean"] == formal["version_lean"]
    assert relativa["revision_mathlib"] == formal["revision_mathlib"]
    anteriores.update(contexto["modulos"])
    for nombre, modulo in relativa["modulos"].items():
        assert huella(RAIZ / modulo["fuente"]) == modulo["fuente_sha256_lf"]
        assert modulo["resolucion_imports_directos_comprobada"]
        for dependencia, esperada in modulo["imports_locales_recompilados"].items():
            assert relativa["modulos"][dependencia]["objeto_sha256"] == esperada
        for axiomas in modulo["axiomas"].values():
            assert set(axiomas) <= {"propext", "Classical.choice", "Quot.sound"}
        if nombre in anteriores:
            assert modulo["fuente_sha256_lf"] == anteriores[nombre]["fuente_sha256_lf"]
            assert modulo["axiomas"] == anteriores[nombre]["axiomas"]
        else:
            consultas += len(modulo["axiomas"])
    assert sum(len(m["axiomas"]) for m in relativa["modulos"].values()) == 57
    assert consultas == 139
    compensacion = leer("cotejo_relativa.json")
    for nombre, esperada in compensacion["fuentes_sha256_lf"].items():
        assert huella(CARPETA / nombre) == esperada
    assert len(compensacion["familias"]) == 16
    assert compensacion["modelos"] == 16 * (compensacion["parametros"]["pares_max"] + 1)
    assert compensacion["orbitas"] == (compensacion["parametros"]["periodos_max"] + 1) * compensacion["parametros"]["traslados"]
    assert all(e["largo"] <= e["ell"] + 3 for e in compensacion["extremos_orbitales"])
    testigo = compensacion["testigo_no_realizable"]
    assert testigo["largo"] > testigo["altura"] + 3
    assert testigo["ell_minima"] > testigo["altura"]
    registro = leer("evidencia_registro.json")
    for nombre, esperada in registro["protegidos_sha256"].items():
        assert huella(RAIZ / nombre, False) == esperada
    assert huella(CARPETA / "alta_registro.json", False) == registro["alta_sha256"]
    assert huella(CARPETA / "verificar_alta.py", False) == registro["verificador_sha256"]
    assert huella(RAIZ / "guardarafirmaciones.py", False) == registro["generador_sha256"]
    assert huella(RAIZ / "registroafirmaciones.py", False) == registro["aplicador_sha256"]
    resultado = dict(enlaces_locales=enlaces, axiomas_consultados=consultas,
                     controles_orbitales=cotejo["controles_orbitales"],
                     controles_bordes=cotejo["controles_bordes"],
                     familias_cotejadas=len(cotejo["optimos"]),
                     ventanas_cotejadas=ventanas["controles"],
                     cadenas_cotejadas=cadenas["controles"], parejas_cotejadas=cadenas["parejas"],
                     cadenas_barrera=ternas["controles"], ternas_barrera=ternas["triples"],
                     controles_ponderada=ponderada["controles"],
                     lean_barrera="Siete módulos recompilados desde fuente; 70 consultas, sólo axiomas estándar.",
                     continuaciones_terminales=continuaciones["continuaciones"],
                     lean_reloj="Dos módulos desde fuente; 22 consultas, 14 nuevas, sólo axiomas estándar.",
                     recorridos_pendiente=familia["recorridos_completos"],
                     lean_pendiente="Tres módulos desde fuente; 29 consultas, siete nuevas, sólo axiomas estándar.",
                     recorridos_rachas=coste_rachas["recorridos"],
                     bordes_rachas=coste_rachas["bordes_cuatro_rachas"],
                     lean_rachas="Cuatro módulos desde fuente; 46 consultas, 16 lemas nuevos y ocho previos añadidos a esta auditoría.",
                     familias_defecto=interiores["prefijos"],
                     miembros_defecto=interiores["casos"], bordes_defecto=interiores["bordes"],
                     lean_defecto="Tres módulos desde fuente; 28 consultas, seis lemas nuevos. Existencia modular del prefijo sólo escrita.",
                     contextos_bilaterales=bilaterales["contextos"],
                     miembros_contexto=bilaterales["casos"], bordes_contexto=bilaterales["bordes"],
                     lean_contexto="Tres módulos desde fuente; 29 consultas, siete lemas auxiliares nuevos. Levantamientos y CRT sólo escritos.",
                     modelos_relativa=compensacion["modelos"],
                     ventanas_relativa=compensacion["ventanas"], orbitas_relativa=compensacion["orbitas"],
                     lean_relativa="Cinco módulos desde fuente; 57 consultas, once lemas nuevos. Modelos separados de la barrera orbital AB.",
                     palabras_estado=len((RAIZ / "ESTADO_INVESTIGACION.md").read_text(encoding="utf-8").split()),
                     catalogo_central_integrado=registro["integrado"],
                     catalogo_central_cotejado=registro["catalogo_central_cotejado"],
                     historial_respuestas_sin_modificar=registro["historial_respuestas_sin_modificar"],
                     archivos_sha256_lf={f.name: huella(f) for f in sorted(CARPETA.iterdir())
                                        if f.is_file() and f.resolve() != args.salida.resolve()})
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK: {enlaces} enlaces, {consultas} consultas y evidencias vigentes; catálogo cotejado.")


if __name__ == "__main__":
    main()
