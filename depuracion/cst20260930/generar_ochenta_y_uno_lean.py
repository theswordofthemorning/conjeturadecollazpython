"""Genera la tabla Lean de un cierre por pesos (81 rachas por defecto).

Filas con n_max <= N remiten a Rozier-Terracol (pequeno_por_cota).
Filas con n_max > N se cubren con piezas de OcelotasPesos.
"""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

N_EXT = 28000000000000000000
BASE = "OcelotasOchentaYUnoTabla"


def real(fr):
    fr = Fraction(fr)
    return f"({fr.numerator} / {fr.denominator} : ℝ)"


def cabecera(importaciones):
    lineas = [f"import {m}" for m in importaciones]
    lineas += ["", "/-! Tabla generada; Lean comprueba todas las obligaciones. -/",
               f"namespace {BASE}",
               "open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica", "",
               "set_option maxRecDepth 100000", "set_option maxHeartbeats 0", ""]
    return lineas


def lambda_fila(f):
    P, Q = f["superior"]
    p, v = f["inferior"]
    c = real(f["lambda_inferior"])
    return [
        f"  have hU : {c} ≤ ({P} : ℝ) * log 2 - {Q} * log 3 := by",
        "    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas",
        "    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas",
        "    linarith [h2.1, h3.2]",
        f"  have hV : ({p} : ℝ) * log 2 - {v} * log 3 < 0 := by",
        "    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas",
        "    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas",
        "    linarith [h2.2, h3.1]",
        f"  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := {P}) (Q := {Q}) (p := {p}) (v := {v})",
        f"    (c := {c}) (by norm_num) (by norm_num) (by norm_num)",
        "    (by norm_num) (by simpa using hU) (by simpa using hV)",
        "    (by omega : 0 < S (tiempo a b r) n)",
        f"    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < {Q} + {v}) hk.2",
    ]


def fila(f, R):
    j, qa, qb = f["intervalo"], f["q_inicio"], f["q_fin"]
    c = Fraction(f["lambda_inferior"])
    semilla = f["n_max"] + 1
    assert R <= semilla * c and f["n_max"] == semilla - 1
    L = [f"theorem fila_{j} {{n r : ℕ}} {{a b : ℕ → ℕ}}",
         f"    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ {R})",
         "    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)",
         f"    (hqa : {qa} ≤ S (tiempo a b r) n)",
         f"    (hqb : S (tiempo a b r) n < {qb}) : n < {N_EXT + 1} := by"]
    L += lambda_fila(f)
    if f["remite"] == "externo":
        assert semilla <= N_EXT + 1
        L += [f"  exact pequeno_por_cota (s := {semilla}) hw hr hrR hk hf (by norm_num)",
              "    hLambda (by norm_num) (by norm_num)", ""]
        return L
    assert f["remite"] == "pesos"
    L += [f"  by_cases hsmall : n < {N_EXT + 1}",
          "  · exact hsmall",
          "  · exfalso",
          f"    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := {semilla})",
          "      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)",
          "    have hn0 : 0 < n := by omega"]
    piezas = f["piezas"]
    assert piezas[0]["n_inf"] == N_EXT + 1 and piezas[-1]["n_sup"] == f["n_max"]
    for a, b in zip(piezas, piezas[1:]):
        assert b["n_inf"] == a["n_sup"] + 1
    for t, pz in enumerate(piezas):
        m, h0, ninf, nsup = pz["m"], pz["h0"], pz["n_inf"], pz["n_sup"]
        assert nsup + R <= 2 ** m and m >= 1
        if t < len(piezas) - 1:
            L.append(f"    by_cases hp{t} : n ≤ {nsup}")
            pre, hhi = "    · ", f"hp{t}"
        else:
            pre, hhi = "    ", "(by omega)"
        if h0 == 0:
            L.append(f"{pre}exact OcelotasPesos.pieza_cadena (m := {m}) (nsup := {nsup}) (qmin := {qa})")
            L.append(f"        hn0 hw hr hrR {hhi} (by norm_num) (by norm_num) (by decide +kernel) hqa")
        else:
            cert = h0 * 2 ** m + (R - h0) * (nsup + R)
            assert Fraction(cert) <= c * ninf * 2 ** m and h0 <= R
            if h0 < R:
                criba = "(fun _ => by decide +kernel)"
            else:
                criba = "(fun h => absurd h (lt_irrefl _))"
            L.append(f"{pre}exact OcelotasPesos.pieza_imposible (m := {m}) (h0 := {h0}) (ninf := {ninf})")
            L.append(f"        (nsup := {nsup}) (qmin := {qa}) hn0 hw hr hrR hk hf (by norm_num) hLambda")
            L.append(f"        (by omega) {hhi} (by norm_num) (by norm_num) (by norm_num) (by norm_num)")
            L.append(f"        {criba} hqa")
    L.append("")
    return L


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--certificado", type=Path, required=True)
    ap.add_argument("--carpeta", type=Path, required=True)
    ap.add_argument("--externas-por-parte", type=int, default=46)
    ap.add_argument("--pesos-por-parte", type=int, default=2)
    ap.add_argument("--base", default="OcelotasOchentaYUnoTabla")
    x = ap.parse_args()
    global BASE, N_EXT
    BASE = x.base
    d = json.loads(x.certificado.read_text(encoding="utf-8"))
    R = d["rachas"]
    assert d["cierra"]
    N_EXT = d["externo_inclusivo"]
    filas = d["filas"]
    partes, actual = [], []
    for f in filas:
        tipo = f["remite"]
        if actual:
            previo = actual[-1]["remite"]
            lleno = (len(actual) >= x.externas_por_parte if tipo == "externo"
                     else len(actual) >= x.pesos_por_parte)
            if tipo != previo or lleno:
                partes.append(actual)
                actual = []
        actual.append(f)
    partes.append(actual)
    nombres = []
    for i, parte in enumerate(partes, 1):
        nombre = f"{BASE}Parte{i:02d}"
        nombres.append(nombre)
        L = cabecera(["OcelotasNumerica", "OcelotasLogaritmosPrecisos", "OcelotasPesos"])
        for f in parte:
            L += fila(f, R)
        L.append(f"end {BASE}")
        L.append("")
        L += [f"#print axioms {BASE}.fila_{f['intervalo']}" for f in parte]
        (x.carpeta / f"{nombre}.lean").write_text("\n".join(L) + "\n", encoding="utf-8")
    Qfin = filas[-1]["q_fin"]
    L = cabecera(nombres)
    L += ["theorem pequeno_de_tabla {n r : ℕ} {a b : ℕ → ℕ}",
          f"    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ {R})",
          "    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)",
          f"    (hq : S (tiempo a b r) n < {Qfin}) : n < {N_EXT + 1} := by",
          "  have hpos := impares_pos hw hr"]
    for f in filas[:-1]:
        j, qb = f["intervalo"], f["q_fin"]
        L.append(f"  by_cases h{j} : S (tiempo a b r) n < {qb}")
        L.append(f"  · exact fila_{j} hw hr hrR hk hf (by omega) h{j}")
    j = filas[-1]["intervalo"]
    L.append(f"  exact fila_{j} hw hr hrR hk hf (by omega) hq")
    L += ["", f"end {BASE}", "",
          f"#print axioms {BASE}.pequeno_de_tabla"]
    (x.carpeta / f"{BASE}.lean").write_text("\n".join(L) + "\n", encoding="utf-8")
    meta = {"partes": nombres, "filas": len(filas), "q_fin": Qfin,
            "sha256_certificado": hashlib.sha256(x.certificado.read_bytes()).hexdigest(),
            "sha256_generador": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (x.carpeta / f"generacion_{BASE}.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(nombres), "partes;", sum(len(f.get("piezas", [])) for f in filas), "piezas")


if __name__ == "__main__":
    main()
