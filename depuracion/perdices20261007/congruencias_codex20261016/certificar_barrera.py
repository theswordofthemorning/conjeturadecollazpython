"""Construye un grafo modular necesario y coteja su cobertura independientemente."""

import argparse
import hashlib
import itertools
import json
import math
from collections import defaultdict
from pathlib import Path

from cotejar_congruencias import RESIDUOS


def huella(ruta):
    return hashlib.sha256(ruta.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def compatible(terna, modulo):
    b, c, d, k, j = terna
    r, v = RESIDUOS[b % 6] + 72 * k, RESIDUOS[d % 6] + 72 * j
    return (pow(9, c, modulo) * (pow(3, b, modulo) * r + 1)
            - pow(8, c, modulo) * (pow(2, d, modulo) * v + 1)) % modulo == 0


def independientes(periodo, modulo, limite):
    indice = defaultdict(list)
    for d, j in itertools.product(range(periodo), range(limite + 1)):
        v = RESIDUOS[d % 6] + 72 * j
        indice[(pow(2, d, modulo) * v + 1) % modulo].append((d, j))
    factores = [pow(9, c, modulo) * pow(pow(8, c, modulo), -1, modulo) % modulo
                for c in range(periodo)]
    resultado = []
    for b, k in itertools.product(range(periodo), range(limite + 1)):
        entrada = (pow(3, b, modulo) * (RESIDUOS[b % 6] + 72 * k) + 1) % modulo
        for c, factor in enumerate(factores):
            resultado.extend((b, c, d, k, j) for d, j in indice.get(factor * entrada % modulo, []))
    return sorted(resultado)


def filtro(arista):
    b, c, d, k, j = arista
    if c == 1:
        return True
    r, v = RESIDUOS[b % 6] + 72 * k, RESIDUOS[d % 6] + 72 * j
    return (pow(3, b, 16) * r + 1) % 16 == 0 and (pow(2, d, 81) * v + 1) % 81 == 0


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--limite", type=int, required=True, choices=[16])
    analizador.add_argument("--salida", type=Path, required=True)
    analizador.add_argument("--lean", type=Path, required=True)
    args = analizador.parse_args()
    tablas, anteriores, previo = [], None, None
    for periodo in (6, 12, 36, 108, 324):
        modulo = math.gcd(2 ** periodo - 1, 3 ** periodo - 1)
        assert all(pow(base, periodo, modulo) == 1 for base in (2, 3, 8, 9))
        if anteriores is None:
            candidatos = itertools.product(range(periodo), range(periodo), range(periodo),
                                            range(args.limite + 1), range(args.limite + 1))
            cantidad = periodo ** 3 * (args.limite + 1) ** 2
        else:
            factor = periodo // previo
            candidatos = ((b + previo * i, c + previo * j, d + previo * h, k, l)
                          for b, c, d, k, l in anteriores
                          for i, j, h in itertools.product(range(factor), repeat=3))
            cantidad = len(anteriores) * factor ** 3
        actuales = sorted(t for t in candidatos if compatible(t, modulo))
        assert actuales == independientes(periodo, modulo, args.limite)
        tablas.append(dict(periodo=periodo, modulo=modulo, candidatos=cantidad, supervivientes=actuales))
        anteriores, previo = actuales, periodo
    aristas = [t for t in anteriores if filtro(t)]
    assert len(aristas) == 13
    assert not any(a[2] == b[0] and a[4] == b[3] for a in aristas for b in aristas)
    # Contraste del filtro mediante sus dos divisibilidades directas.
    assert aristas == [t for t in anteriores if t[1] == 1 or
                       ((3 ** t[0] * (RESIDUOS[t[0] % 6] + 72 * t[3]) + 1) % 16 == 0
                        and (2 ** t[2] * (RESIDUOS[t[2] % 6] + 72 * t[4]) + 1) % 81 == 0)]
    codigo = ["import PerdicesCongruenciasOrbitales", "", "/-! Tablas generadas por certificar_barrera.py; verificadas en el núcleo. -/",
              "set_option maxRecDepth 100000", "set_option maxHeartbeats 1600000",
              "set_option Elab.async false", "", "namespace PerdicesBarreraTablas", "",
              "open PerdicesCongruencias", "abbrev Arista := ℕ × ℕ × ℕ × ℕ × ℕ", "",
              "def parte (b k : ℕ) : ℕ := minimoResiduo (b % 6) + 72 * k", "",
              "def compatible (m b c d k j : ℕ) : Prop :=",
              "  (9 ^ c * (3 ^ b * parte b k + 1)) % m =",
              "    (8 ^ c * (2 ^ d * parte d j + 1)) % m", "",
              "instance (m b c d k j : ℕ) : Decidable (compatible m b c d k j) := by",
              "  unfold compatible; infer_instance", ""]
    codigo.extend([
        "def inicialCarga (p m limite k : ℕ) : List Arista :=",
        "  (List.range p).flatMap fun b => (List.range p).flatMap fun c =>",
        "    (List.range p).flatMap fun d =>",
        "      ((List.range limite).filter fun j => decide (compatible m b c d k j)).map",
        "        fun j => (b, c, d, k, j)", "",
        "def inicial (p m limite : ℕ) : List Arista :=",
        "  (List.range limite).flatMap (inicialCarga p m limite)", "",
        "def levantarTabla (p factor m : ℕ) (antes : List Arista) : List Arista :=",
        "  (antes.flatMap fun t => (List.range factor).flatMap fun i =>",
        "    (List.range factor).flatMap fun j => (List.range factor).map fun h =>",
        "      (t.1 + p * i, t.2.1 + p * j, t.2.2.1 + p * h, t.2.2.2.1, t.2.2.2.2)).filter",
        "        fun t => decide (compatible m t.1 t.2.1 t.2.2.1 t.2.2.2.1 t.2.2.2.2)", "",
        "def tabla6Carga (k : ℕ) : List Arista := inicialCarga 6 7 17 k",
        "def tabla6 : List Arista := (List.range 17).flatMap tabla6Carga", ""])
    # Conservar el orden de los levantamientos, para certificar igualdad de listas
    # mediante reducción lineal, sin búsquedas cuadráticas de pertenencia.
    ordenadas = list(itertools.product(range(6), range(6), range(6), range(17), range(17)))
    ordenadas = [t for t in ordenadas if compatible(t, 7)]
    previo = 6
    for tabla in tablas[1:]:
        p = tabla["periodo"]
        ordenadas = [(b + previo * i, c + previo * j, d + previo * h, k, l)
                     for b, c, d, k, l in ordenadas
                     for i, j, h in itertools.product(range(p // previo), repeat=3)
                     if compatible((b + previo * i, c + previo * j, d + previo * h, k, l), tabla["modulo"])]
        assert sorted(ordenadas) == tabla["supervivientes"]
        codigo.append(f"def tabla{p}Carga (k : ℕ) : List Arista := match k with")
        for carga in range(17):
            grupo = [t for t in ordenadas if t[3] == carga]
            codigo.append(f"  | {carga} => [" + ",\n      ".join("(" + ", ".join(map(str, t)) + ")" for t in grupo) + "]")
        codigo.extend(["  | _ => []", f"def tabla{p} : List Arista := (List.range 17).flatMap tabla{p}Carga", ""])
        for carga in range(17):
            codigo.extend([f"theorem paso{p}_{carga} : levantarTabla {previo} {p // previo} {tabla['modulo']}",
                           f"    (tabla{previo}Carga {carga}) = tabla{p}Carga {carga} := by decide +kernel"])
        codigo.extend([f"theorem paso{p} (k : ℕ) (hk : k < 17) :",
                       f"    levantarTabla {previo} {p // previo} {tabla['modulo']} (tabla{previo}Carga k) = tabla{p}Carga k := by",
                       "  interval_cases k"])
        codigo.extend(f"  · exact paso{p}_{carga}" for carga in range(17))
        codigo.append("")
        previo = p
    codigo.extend(["def aristas : List Arista := [",
                   ",\n".join("  (" + ", ".join(map(str, t)) + ")" for t in aristas) + "]", "",
                   "end PerdicesBarreraTablas", ""])
    args.lean.write_text("\n".join(codigo), encoding="utf-8")
    resumen = [dict(periodo=t["periodo"], modulo=t["modulo"], candidatos=t["candidatos"],
                    supervivientes=len(t["supervivientes"]),
                    tabla_ordenada_sha256=hashlib.sha256(json.dumps(t["supervivientes"]).encode()).hexdigest())
               for t in tablas]
    resultado = dict(limite=args.limite, tablas=resumen, aristas=aristas, empalmes=0,
                     alcance="Cobertura finita modular con periodos, pendiente de leer junto a la prueba universal; "
                             "no acota los exponentes originales ni prueba el presupuesto global.",
                     fuente_sha256_lf=huella(Path(__file__)), tablas_lean_sha256_lf=huella(args.lean),
                     apoyo_sha256_lf=huella(Path(__file__).with_name("cotejar_congruencias.py")))
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(tablas=[(t["periodo"], t["candidatos"], len(t["supervivientes"])) for t in tablas],
                         aristas=aristas), ensure_ascii=False))


if __name__ == "__main__":
    main()
