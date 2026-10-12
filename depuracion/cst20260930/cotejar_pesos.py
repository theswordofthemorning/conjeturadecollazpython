"""Cotejo independiente del certificado de pesos por racha.

No importa el certificador. Recalcula logaritmos por series de atanh,
determinantes, signos, cobertura de semillas y la criba de segmentos con
la recursión real floor(beta + alfa*C) en racionales exactos.
"""

import argparse
from fractions import Fraction
import json
from pathlib import Path


def ln_encierro(x, terminos):
    """log x = 2 atanh((x-1)/(x+1)); devuelve [inferior, superior]."""
    y = Fraction(x - 1, x + 1)
    suma, potencia = Fraction(0), y
    for i in range(terminos):
        suma += potencia / (2 * i + 1)
        potencia *= y * y
    # cola: sum_{i>=terminos} y^(2i+1)/(2i+1) <= potencia/(1-y^2)
    cola = potencia / (1 - y * y)
    return 2 * suma, 2 * (suma + cola)


def cota_real(beta, R):
    """OcelotasAfinada.cota con alfa=1585/1000."""
    c = 0
    for _ in range(R):
        v = beta + Fraction(1585, 1000) * c
        c = v.numerator // v.denominator
    return c


def g(m, j):
    return j + cota_real(Fraction(256 * m - 256, 256), j)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--certificado", type=Path, required=True)
    ap.add_argument("--salida", type=Path, required=True)
    x = ap.parse_args()
    d = json.loads(x.certificado.read_text(encoding="utf-8"))
    R, N, H = d["rachas"], d["externo_inclusivo"], d["H"]
    l2 = ln_encierro(2, 120)
    l3 = ln_encierro(3, 120)
    dos = [Fraction(d["logaritmos"]["dos"][k]) for k in ("inferior", "superior")]
    tres = [Fraction(d["logaritmos"]["tres"][k]) for k in ("inferior", "superior")]
    assert dos[0] <= l2[0] and l2[1] <= dos[1], "encierro de log 2"
    assert tres[0] <= l3[0] and l3[1] <= tres[1], "encierro de log 3"
    filas = d["filas"]
    assert filas[0]["q_inicio"] == 1
    piezas_total, externas, por_pesos = 0, 0, 0
    for a, b in zip(filas, filas[1:]):
        assert b["q_inicio"] == a["q_fin"], "filas contiguas"
    assert filas[-1]["q_fin"] >= 2 ** H
    for f in filas:
        P, Q = f["superior"]
        p, v = f["inferior"]
        assert P * v - p * Q == 1 and Q > 0 and v > 0
        assert f["q_fin"] == Q + v
        # signos con logaritmos recalculados
        assert P * l2[0] - Q * l3[1] > 0
        assert p * l2[1] - v * l3[0] < 0
        c = Fraction(f["lambda_inferior"])
        assert c == P * dos[0] - Q * tres[1] and c > 0
        assert c <= P * l2[1] - Q * l3[0]
        semilla = f["n_max"] + 1
        assert R <= semilla * c
        if f["remite"] == "externo":
            assert semilla <= N + 1
            externas += 1
            continue
        assert f["remite"] == "pesos"
        por_pesos += 1
        esperado = N + 1
        for pz in f["piezas"]:
            m, h0, ninf, nsup = pz["m"], pz["h0"], pz["n_inf"], pz["n_sup"]
            assert ninf == esperado and ninf <= nsup
            esperado = nsup + 1
            assert m >= 1 and nsup + R <= 2 ** m and 0 <= h0 <= R
            if h0 == 0:
                assert g(m, R) < f["q_inicio"]
            else:
                assert h0 * 2 ** m + (R - h0) * (nsup + R) <= c * ninf * 2 ** m
                if h0 < R:
                    assert g(m, R - h0) + h0 * m < f["q_inicio"]
            piezas_total += 1
        assert esperado == semilla, "cobertura hasta n_max"
    # parámetros de la cola
    A = -((-5 * (8 ** R - 5 ** R)) // (3 * 5 ** R))
    cc = 7
    assert R <= 2 ** cc and 5 * 8 ** R <= (3 * A + 5) * 5 ** R
    assert 8 * A * (19 * (H + 33) ** 2 + cc + 1) + 5 < 5 * 2 ** H
    salida = {"certificado": str(x.certificado.name), "rachas": R, "filas": len(filas),
              "externas": externas, "por_pesos": por_pesos, "piezas": piezas_total,
              "cola": {"A": A, "c": cc, "H": H}, "q_fin": filas[-1]["q_fin"],
              "resultado": "coincide"}
    x.salida.write_text(json.dumps(salida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(salida)


if __name__ == "__main__":
    main()
