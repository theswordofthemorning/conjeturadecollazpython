"""Criba de pesos por racha para CST (Ocelotas), aritmetica exacta.

Un fallo de CST con primer cruce k, q impares y rachas que empiezan en
x_0=n, x_1, ..., x_(r-1) cumple

    Lambda*n < suma_i n/x_i,   Lambda = k log 2 - q log 3 > 0,

y cada sumando es <= 1 (x_i >= n). Si l_i = log2(x_i+1) supera
log2(n+1)+d, el sumando es < 2^-d. Las rachas con l_i <= beta+d
("pesadas") reinician el crecimiento: a_i <= l_i y
l_(i+1) <= l_i + (alfa-1)(a_i-1). Ver PESOS_RACHAS.md y OcelotasPesos.lean.
"""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

from rachas_unilaterales import intervalos_superiores

ALFA = Fraction(10144, 6400)


def techo(x):
    return -((-x.numerator) // x.denominator)


def piso(x):
    return x.numerator // x.denominator


def cota_entera(B, r):
    """OcelotasPrefijosAfinados.cota: alfa=10144/6400, beta=B/256."""
    c = 0
    for _ in range(r):
        c = (25 * B + 10144 * c) // 6400
    return c


def g(m, j):
    """Segmento de j rachas que empieza con x+1<=2^m (criba de descuento)."""
    return j + cota_entera(256 * m - 256, j)


def pesadas_minimas(rachas, M, c, n_inf, n_sup):
    """Menor h con c*n_inf*M < h*M + (rachas-h)*(n_sup+rachas)."""
    for h in range(1, rachas + 1):
        if c * n_inf * M < h * M + (rachas - h) * (n_sup + rachas):
            return h
    return None


def pieza(rachas, c, q_inicio, n_inf, n_sup, dmax):
    base = (n_sup + rachas).bit_length()
    for d in range(dmax + 1):
        m = base + d
        M = 2 ** m
        assert n_sup + rachas <= M
        h = pesadas_minimas(rachas, M, c, n_inf, n_sup)
        if h is None:
            # ni con todas pesadas basta: h0 = rachas
            return {"m": m, "h0": rachas, "cota_q": 0}
        tope = g(m, rachas - h + 1) + (h - 1) * m
        if tope < q_inicio:
            # h0 = h - 1; h0 = 0 se resuelve con un solo segmento
            return {"m": m, "h0": h - 1, "cota_q": tope}
    return None


def fila(rachas, c, q_inicio, externo, dmax, ancho_min):
    semilla = techo(rachas / c)  # n < semilla
    n_max = semilla - 1
    if n_max <= externo:
        return {"remite": "externo", "n_max": n_max, "piezas": []}
    piezas, pendientes = [], [(externo + 1, n_max)]
    while pendientes:
        a, b = pendientes.pop()
        if b > 2 * a:
            pendientes += [(2 * a + 1, b), (a, 2 * a)]
            continue
        r = pieza(rachas, c, q_inicio, a, b, dmax)
        if r is not None:
            piezas.append({"n_inf": a, "n_sup": b, **r})
        elif b - a < ancho_min:
            return {"remite": "falla", "n_max": n_max, "pieza_fallida": [a, b]}
        else:
            m = (a + b) // 2
            pendientes += [(m + 1, b), (a, m)]
    piezas.sort(key=lambda p: p["n_inf"])
    return {"remite": "pesos", "n_max": n_max, "piezas": piezas}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--rachas", type=int, required=True)
    p.add_argument("--logaritmos", type=Path, required=True)
    p.add_argument("--H", type=int, default=72)
    p.add_argument("--externo", type=int, default=28000000000000000000)
    p.add_argument("--dmax", type=int, default=40)
    p.add_argument("--ancho-min", type=int, default=10 ** 15)
    p.add_argument("--salida", type=Path)
    x = p.parse_args()
    datos = json.loads(x.logaritmos.read_text(encoding="utf-8"))
    dos_inf, dos_sup = [Fraction(datos["dos"][k]) for k in ("inferior", "superior")]
    tres_inf, tres_sup = [Fraction(datos["tres"][k]) for k in ("inferior", "superior")]
    assert tres_sup / dos_inf <= ALFA
    intervalos = intervalos_superiores(tres_inf / dos_sup, tres_sup / dos_inf, 2 ** x.H)
    filas, ok = [], True
    for j, it in enumerate(intervalos):
        P, Q = it["superior"]
        c = P * dos_inf - Q * tres_sup
        assert c > 0
        r = fila(x.rachas, c, it["q_inicio"], x.externo, x.dmax, x.ancho_min)
        ok = ok and r["remite"] != "falla"
        filas.append({"intervalo": j, **it, "lambda_inferior": str(c), **r})
        if r["remite"] != "externo":
            print(j, it["q_inicio"], r["remite"], len(r.get("piezas", [])), flush=True)
    print(f"R={x.rachas}: {len(filas)} filas, q<{intervalos[-1]['q_fin']}, cierre={'si' if ok else 'no'}")
    if x.salida:
        salida = {"estado": "certificado propuesto; pendiente de cotejo y Lean",
                  "rachas": x.rachas, "externo_inclusivo": x.externo,
                  "alfa_superior": str(ALFA), "H": x.H, "cierra": ok,
                  "logaritmos": datos, "filas": filas,
                  "sha256_generador": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
        x.salida.write_text(json.dumps(salida, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
