"""Emite la tabla de R=77; los parametros no se aceptan como premisas."""

import argparse
from fractions import Fraction
import json
from pathlib import Path


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--certificado", type=Path, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    analizador.add_argument("--filas-por-modulo", type=int, required=True)
    argumentos = analizador.parse_args()
    datos = json.loads(argumentos.certificado.read_text(encoding="utf-8"))
    assert datos["rachas"] == 77 and datos["intervalos_por_prefijos"] == [91]
    assert argumentos.filas_por_modulo >= 1
    limite = datos["limite_externo_inclusivo"] + 1
    espacio = "OcelotasSetentaYSieteTabla"
    preambulo = [f"namespace {espacio}",
        "open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica", "",
        "set_option maxRecDepth 100000", "set_option maxHeartbeats 0", ""]
    partes, pruebas, inicio = [], [], 1
    for j, fila in enumerate(datos["filas"]):
        assert fila["intervalo"] == j and fila["q_inicio"] == inicio
        inicio = fila["q_fin"]
        P, Q = fila["superior"]
        p, v = fila["inferior"]
        assert P * v - p * Q == 1 and Q + v == inicio
        s, B = fila["semilla_exclusiva"], fila["B"]
        c = Fraction(fila["lambda_inferior"])
        ctexto = f"({c.numerator} / {c.denominator} : ℝ)"
        prueba = [f"theorem fila_{j} {{n r : ℕ}} {{a b : ℕ → ℕ}}",
            "    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)",
            "    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)",
        "    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)",
            f"    (hqa : {fila['q_inicio']} ≤ S (tiempo a b r) n)",
            f"    (hqb : S (tiempo a b r) n < {fila['q_fin']}) : n < {limite} := by",
            f"  have hU : {ctexto} ≤ ({P} : ℝ) * log 2 - {Q} * log 3 := by",
            "    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas",
            "    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas",
            "    linarith [h2.1, h3.2]",
            f"  have hV : ({p} : ℝ) * log 2 - {v} * log 3 < 0 := by",
            "    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas",
            "    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas",
            "    linarith [h2.2, h3.1]",
            f"  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := {P}) (Q := {Q}) (p := {p}) (v := {v})",
            f"    (c := {ctexto}) (by norm_num) (by norm_num) (by norm_num)",
            "    (by norm_num) (by simpa using hU) (by simpa using hV)",
            "    (by omega : 0 < S (tiempo a b r) n)",
            f"    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < {Q} + {v}) hk.2"]
        if s <= limite:
            prueba.extend([f"  exact pequeno_por_cota (s := {s}) hw hr hr77 hk hf (by norm_num)",
                           "    hLambda (by norm_num) (by norm_num)", ""])
        elif j == 91:
            assert (s, fila["q_inicio"]) == (42938293471394771273, 130441933147714940)
            prueba.extend([f"  by_cases hsmall : n < {limite}",
                "  · exact hsmall",
                f"  · have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := {s})",
                "      hw hr hr77 hk hf (by norm_num) hLambda (by norm_num)",
                "    have hd := OcelotasSetentaYSietePrefijos.descenso",
                f"      (by omega : {limite} ≤ n) (by omega : n ≤ {s - 1}) hk _hcontador hqa",
                "    omega", ""])
        else:
            assert fila["cota_q"] < fila["q_inicio"] and s ** 256 <= 2 ** B
            prueba.extend([f"  have hpot : ({s} : ℕ) ^ 256 ≤ 2 ^ {B} := by decide +kernel",
                f"  have hcriba : OcelotasAfinada.cota (1585 / 1000) ({B} / 256) 77 < {fila['q_inicio']} := by",
                "    norm_num [OcelotasAfinada.cota]",
                f"  exact False.elim (imposible_por_criba (s := {s}) (B := {B}) hw hr hr77 hk hf",
                "    (by norm_num) hLambda (by norm_num) hpot hcriba hqa)", ""])
        pruebas.append(prueba)
    for primero in range(0, len(pruebas), argumentos.filas_por_modulo):
        nombre = espacio + f"Parte{len(partes) + 1:02d}"
        partes.append(nombre)
        lineas = ["import OcelotasNumerica", "import OcelotasLogaritmosPrecisos", "import OcelotasSetentaYSietePrefijos", "",
                  "/-! Tabla generada; Lean comprueba todas las obligaciones. -/"] + preambulo
        ultimo = min(primero + argumentos.filas_por_modulo, len(pruebas))
        for j in range(primero, ultimo):
            lineas.extend(pruebas[j])
        lineas.extend([f"end {espacio}", ""])
        lineas.extend(f"#print axioms {espacio}.fila_{j}" for j in range(primero, ultimo))
        argumentos.salida.with_name(nombre + ".lean").write_text("\n".join(lineas) + "\n", encoding="utf-8")
    lineas = ["import " + p for p in partes] + [""] + preambulo
    lineas.extend(["theorem pequeno_de_tabla {n r : ℕ} {a b : ℕ → ℕ}",
        "    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)",
        "    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)",
        "    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)",
        f"    (hq : S (tiempo a b r) n < {inicio}) : n < {limite} := by",
        "  have hpos := impares_pos hw hr"])
    for j, fila in enumerate(datos["filas"][:-1]):
        lineas.extend([f"  by_cases h{j} : S (tiempo a b r) n < {fila['q_fin']}",
                       f"  · exact fila_{j} hw hr hr77 _hcontador hk hf (by omega) h{j}"])
    lineas.extend([f"  exact fila_{len(pruebas) - 1} hw hr hr77 _hcontador hk hf (by omega) hq", "",
                  f"end {espacio}", "", f"#print axioms {espacio}.pequeno_de_tabla"])
    argumentos.salida.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print(f"{len(pruebas)} filas en {len(partes)} partes, mas ensamblaje.")


if __name__ == "__main__":
    main()
