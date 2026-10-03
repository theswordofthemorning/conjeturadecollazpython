"""Emite las cuarenta y dos obligaciones Lean del certificado preparado para R=21.

El JSON sólo propone constantes. Cada signo, producto, potencia, piso y
cobertura se vuelve a demostrar en Lean; el generador no es una premisa.
"""

import argparse
from fractions import Fraction
import json
from pathlib import Path


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--certificado", type=Path, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    datos = json.loads(argumentos.certificado.read_text(encoding="utf-8"))
    assert datos["rachas"] == 21 and datos["semilla_exclusiva"] == 325543669
    assert datos["cola_desde_q"] == 4598951775 and len(datos["filas"]) == 42
    lineas = ["import OcelotasNumerica", "import OcelotasVeintiunaPrefijos", "",
              "/-! # Ocelotas: tabla de veintiuna rachas",
              "", "Generada por generar_veintiuna_lean.py. Todas las obligaciones se certifican en Lean.",
              "-/", "", "namespace OcelotasVeintiunaTabla", "",
              "open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica", "",
              "set_option maxRecDepth 100000", "set_option maxHeartbeats 0", ""]
    inicio = 1
    for j, fila in enumerate(datos["filas"]):
        assert fila["intervalo"] == j and fila["q_inicio"] == inicio
        inicio = fila["q_fin"]
        P, Q = fila["superior"]
        p, v = fila["inferior"]
        assert P * v - p * Q == 1 and Q + v == inicio
        s, B = fila["semilla_exclusiva"], fila["B"]
        c = Fraction(fila["lambda_inferior"])
        ctexto = f"({c.numerator} / {c.denominator} : ℝ)"
        lineas.extend([f"theorem fila_{j} {{n r : ℕ}} {{a b : ℕ → ℕ}}",
            "    (hw : Palabra n a b r) (hr : 0 < r) (hr21 : r ≤ 21)",
            "    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 21)",
            "    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)",
            f"    (hqa : {fila['q_inicio']} ≤ S (tiempo a b r) n)",
            f"    (hqb : S (tiempo a b r) n < {fila['q_fin']}) : n < 4912741 := by",
            f"  have hU : {ctexto} ≤ ({P} : ℝ) * log 2 - {Q} * log 3 := by",
            "    have h2 := log_dos_cotas; have h3 := log_tres_cotas",
            "    linarith [h2.1, h3.2]",
            f"  have hV : ({p} : ℝ) * log 2 - {v} * log 3 < 0 := by",
            "    have h2 := log_dos_cotas; have h3 := log_tres_cotas",
            "    linarith [h2.2, h3.1]",
            f"  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := {P}) (Q := {Q}) (p := {p}) (v := {v})",
            f"    (c := {ctexto}) (by norm_num) (by norm_num) (by norm_num)",
            "    (by norm_num) (by simpa using hU) (by simpa using hV)",
            "    (by omega : 0 < S (tiempo a b r) n)",
            f"    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < {Q} + {v}) hk.2"])
        if s <= 4912741:
            lineas.extend([f"  exact pequeno_por_cota (s := {s}) hw hr hr21 hk hf (by norm_num)",
                          "    hLambda (by norm_num) (by norm_num)", ""])
        elif j in (35, 36):
            nombre = "bajo" if j == 35 else "alto"
            assert (s, fila["q_inicio"]) == ((5730314, 79335) if j == 35 else (325543669, 190537))
            lineas.extend(["  by_cases hsmall : n < 4912741",
                "  · exact hsmall",
                f"  · have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := {s})",
                "      hw hr hr21 hk hf (by norm_num) hLambda (by norm_num)",
                f"    have hd := OcelotasVeintiunaPrefijos.descenso_{nombre}",
                f"      (by omega : 4912741 ≤ n) (by omega : n ≤ {s - 1}) hk _hcontador hqa",
                "    omega", ""])
        else:
            assert fila["cota_q"] < fila["q_inicio"] and s ** 256 <= 2 ** B
            lineas.extend([f"  have hpot : ({s} : ℕ) ^ 256 ≤ 2 ^ {B} := by decide +kernel",
                f"  have hcriba : OcelotasAfinada.cota (1585 / 1000) ({B} / 256) 21 < {fila['q_inicio']} := by",
                "    norm_num [OcelotasAfinada.cota]",
                f"  exact False.elim (imposible_por_criba (s := {s}) (B := {B}) hw hr hr21 hk hf",
                "    (by norm_num) hLambda (by norm_num) hpot hcriba hqa)", ""])
    lineas.extend(["theorem pequeno_de_tabla {n r : ℕ} {a b : ℕ → ℕ}",
        "    (hw : Palabra n a b r) (hr : 0 < r) (hr21 : r ≤ 21)",
        "    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 21)",
        "    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)",
        "    (hq : S (tiempo a b r) n < 4598951775) : n < 4912741 := by",
        "  have hpos := impares_pos hw hr"])
    for j, fila in enumerate(datos["filas"][:-1]):
        lineas.extend([f"  by_cases h{j} : S (tiempo a b r) n < {fila['q_fin']}",
                       f"  · exact fila_{j} hw hr hr21 _hcontador hk hf (by omega) h{j}"])
    lineas.extend(["  exact fila_41 hw hr hr21 _hcontador hk hf (by omega) hq", "",
                   "end OcelotasVeintiunaTabla", "",
                   "#print axioms OcelotasVeintiunaTabla.pequeno_de_tabla"])
    argumentos.salida.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print(f"42 filas y cobertura emitidas en {argumentos.salida}; falta compilar.")


if __name__ == "__main__":
    main()
