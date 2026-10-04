"""Revisa hojas del piloto con orbitas directas, Fraction y cobertura.

No importa el generador. Reconstruye cada prefijo en dos semillas de su
clase y enumera su cobertura; este cotejador se limita a pilotos pequenos.
"""

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def trayectoria(n, pasos):
    x, q, r, anterior = n, 0, 0, False
    for _ in range(pasos):
        impar = x % 2 == 1
        q += int(impar)
        r += int(impar and not anterior)
        anterior = impar
        x = (3 * x + 1) // 2 if impar else x // 2
    return x, q, r, anterior


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--certificado", type=Path, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    datos = json.loads(argumentos.certificado.read_text(encoding="utf-8"))
    inicio, limite = datos["inicio"], datos["limite"]
    assert 4095 <= inicio <= limite and limite - inicio < 100000
    resumen = {}
    for modo, arbol in datos["modos"].items():
        assert modo in ("anterior", "descuento", "suelo")
        cubiertas, conteos, prefijos = set(), Counter(), []
        for hoja in arbol["hojas"]:
            r, m, a, c, k, q, s = (hoja[nombre] for nombre in ("r", "m", "a", "c", "k", "q", "s"))
            motivo = hoja["motivo"]
            assert 0 <= k < datos["combustible"] and m == 2 ** k
            assert inicio <= r < inicio + m
            prefijos.append((r - inicio, m))
            conteos[motivo] += 1
            if r > limite:
                assert motivo == "vacio" and hoja["cantidad"] == 0
                continue
            semillas = set(range(r, limite + 1, m))
            assert len(semillas) == hoja["cantidad"] and not (semillas & cubiertas)
            cubiertas.update(semillas)
            # Dos evaluaciones directas reconstruyen la aplicacion afin.
            assert trayectoria(r, k) == (c, q, s, hoja["anterior"])
            assert trayectoria(r + m, k) == (c + a, q, s, hoja["anterior"])
            assert a == 3 ** q
            for n in semillas:
                assert trayectoria(n, k) == (a * ((n - r) // m) + c, q, s, hoja["anterior"])
            if motivo == "descenso":
                assert a < m and c < r
            elif motivo == "exceso":
                assert a >= m and s > datos["rachas"]
            else:
                assert motivo == "criba" and a >= m and s <= datos["rachas"]
                assert hoja["anterior"] is False
                maximo = max(trayectoria(n, k)[0] for n in semillas)
                B = hoja["B"]
                assert B >= 512 and 2 ** (B - 1) < (maximo + 1) ** 256 <= 2 ** B
                alfa = Fraction(317, 200)
                beta = Fraction(B, 256) - (1 if modo == "descuento" else 0)
                gamma = Fraction(4095, 4096) if modo == "suelo" else 0
                cota = 0
                for j in range(datos["rachas"] - s):
                    valor = beta + alfa * cota - gamma * j
                    assert valor >= 0
                    cota = valor.numerator // valor.denominator
                if modo == "descuento":
                    cota += datos["rachas"] - s
                assert q + cota < datos["q_min"]
        # Las clases terminales son disjuntas incluso fuera del intervalo.
        for j, (r, m) in enumerate(prefijos):
            for t, v in prefijos[:j]:
                assert (r - t) % min(m, v) != 0
        assert cubiertas == set(range(inicio, limite + 1))
        assert sum(Fraction(1, m) for _, m in prefijos) == 1
        assert arbol["conteos"]["nodos"] == 2 * len(prefijos) - 1
        for motivo in ("vacio", "descenso", "exceso", "criba", "pendiente"):
            assert conteos[motivo] == arbol["conteos"][motivo]
        assert conteos["pendiente"] == 0
        assert len(cubiertas) == arbol["conteos"]["semillas"]
        resumen[modo] = {"nodos": arbol["conteos"]["nodos"],
                         "hojas": len(prefijos), "semillas": len(cubiertas),
                         "motivos": dict(conteos)}
    salida = {"resultado": "sin discrepancias", "modos": resumen,
              "alcance": "Cobertura finita disjunta, prefijos por orbitas directas, cotas por Fraction. No demuestra una mejora universal de complejidad.",
              "sha256_certificado": hashlib.sha256(argumentos.certificado.read_bytes()).hexdigest(),
              "sha256_cotejador": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    argumentos.salida.write_text(json.dumps(salida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(salida, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
