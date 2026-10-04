"""Propone un piloto acotado del verificador con suelo, con tres cribas.

Conserva todas las hojas para su cotejo independiente. El nucleo de Lean
evalua posteriormente el verificador completo, sin confiar en este JSON.
"""

import argparse
import hashlib
import json
from pathlib import Path


def explorar(inicio, limite, qmin, R, combustible, max_nodos, modo):
    conteos = dict.fromkeys(("nodos", "vacio", "descenso", "exceso",
                            "criba", "pendiente", "semillas"), 0)
    hojas = []

    def visitar(r, m, a, c, q, s, anterior, k):
        conteos["nodos"] += 1
        assert conteos["nodos"] <= max_nodos, "Presupuesto de nodos agotado"
        B = None
        cantidad = 0 if r > limite else (limite - r) // m + 1
        if k == combustible:
            motivo = "pendiente"
        elif r > limite:
            motivo = "vacio"
        elif a < m:
            motivo = "descenso" if c < r else "pendiente"
        elif s > R:
            motivo = "exceso"
        else:
            motivo = None
            if not anterior:
                maximo = a * (cantidad - 1) + c
                B = ((maximo + 1) ** 256 - 1).bit_length()
                assert B >= 512
                C = 0
                for j in range(R - s):
                    if modo == "suelo":
                        numerador = 400 * B + 162304 * C - 102375 * j
                        assert numerador >= 0
                        C = numerador // 102400
                    else:
                        beta = B - 256 if modo == "descuento" else B
                        C = (25 * beta + 10144 * C) // 6400
                if modo == "descuento":
                    C += R - s
                if q + C < qmin:
                    motivo = "criba"
        if motivo is not None:
            conteos[motivo] += 1
            conteos["semillas"] += cantidad
            hojas.append({"r": r, "m": m, "a": a, "c": c, "q": q,
                          "s": s, "anterior": anterior, "k": k,
                          "B": B, "motivo": motivo, "cantidad": cantidad})
            return
        for bit in (0, 1):
            x = a * bit + c
            impar = bool(x % 2)
            visitar(r + m * bit, 2 * m, a * (3 if impar else 1),
                    (3 * x + 1) // 2 if impar else x // 2,
                    q + int(impar), s + int(impar and not anterior), impar, k + 1)

    visitar(inicio, 1, 1, inicio, 0, 0, False, 0)
    assert conteos["semillas"] == limite - inicio + 1
    assert conteos["pendiente"] == 0
    return {"conteos": conteos, "hojas": hojas}


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--inicio", type=int, required=True)
    analizador.add_argument("--limite", type=int, required=True)
    analizador.add_argument("--q-min", type=int, required=True)
    analizador.add_argument("--rachas", type=int, required=True)
    analizador.add_argument("--combustible", type=int, required=True)
    analizador.add_argument("--max-nodos", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    assert 4095 <= argumentos.inicio <= argumentos.limite
    assert argumentos.q_min > 0 and argumentos.rachas > 0
    assert 0 < argumentos.combustible < 800 and argumentos.max_nodos > 0
    modos = {modo: explorar(argumentos.inicio, argumentos.limite,
                            argumentos.q_min, argumentos.rachas,
                            argumentos.combustible, argumentos.max_nodos, modo)
             for modo in ("anterior", "descuento", "suelo")}
    salida = {"estado": "propuesta exacta; requiere cotejo y Lean",
              "inicio": argumentos.inicio, "limite": argumentos.limite,
              "q_min": argumentos.q_min, "rachas": argumentos.rachas,
              "combustible": argumentos.combustible,
              "max_nodos": argumentos.max_nodos, "modos": modos,
              "sha256_generador": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    argumentos.salida.write_text(json.dumps(salida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({modo: datos["conteos"] for modo, datos in modos.items()}, indent=2))


if __name__ == "__main__":
    main()
