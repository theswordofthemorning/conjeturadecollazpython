"""Explora la criba descontada por prefijos; no constituye prueba Lean.

T es el atajo. Las clases n=r+m*t comparten k pasos, con T^k(n)=a*t+c.
Tras una entrada par, se acotan las rachas restantes desde el mayor valor
actual de la clase. Usa beta=B/256 comprobada por potencia y descuenta
un paso por racha. Conserva por separado el explorador
anterior. El combustible agotado deja una obligacion pendiente.
"""

import argparse
import hashlib
import json
from pathlib import Path
import time


def cota_restante(valor, rachas, criba):
    assert criba == "descuento"
    potencia = (valor + 1) ** 256
    B = (potencia - 1).bit_length()
    assert B >= 256
    cota = 0
    for _ in range(rachas):
        cota = (25 * (B - 256) + 10144 * cota) // 6400
    return rachas + cota, B


def explorar(limite, qmin, rachas, combustible, inicio=2, criba="descuento", max_nodos=None):
    conteos = {"nodos": 0, "descenso": 0, "exceso_rachas": 0,
               "criba": 0, "vacio": 0, "pendiente": 0,
               "semillas_cubiertas": 0, "profundidad_maxima": 0}
    pendientes = []
    huella = hashlib.sha256()

    class PresupuestoAgotado(Exception):
        pass

    def visitar(r, m, a, c, k, q, s, anterior):
        if max_nodos is not None and conteos["nodos"] >= max_nodos:
            conteos["pendiente"] += 1
            pendientes.append({"motivo": "presupuesto de nodos agotado", "r": r, "k": k})
            raise PresupuestoAgotado
        conteos["nodos"] += 1
        conteos["profundidad_maxima"] = max(k, conteos["profundidad_maxima"])
        if r > limite:
            conteos["vacio"] += 1
            return
        cantidad = (limite - r) // m + 1
        motivo = None
        if a < m and c < r:
            motivo = "descenso"
        elif s > rachas:
            motivo = "exceso_rachas"
        elif not anterior:
            maximo = a * (cantidad - 1) + c
            C, B = cota_restante(maximo, rachas - s, criba)
            if q + C < qmin:
                motivo = "criba"
        if motivo:
            conteos[motivo] += 1
            conteos["semillas_cubiertas"] += cantidad
            huella.update(f"{r},{m},{a},{c},{k},{q},{s},{motivo},{cantidad}\n".encode("ascii"))
            return
        if k >= combustible or a < m:
            conteos["pendiente"] += 1
            pendientes.append({"r": r, "m": m, "a": a, "c": c,
                               "k": k, "q": q, "rachas": s, "anterior": anterior})
            return
        for b in (0, 1):
            x = a * b + c
            impar = bool(x % 2)
            visitar(r + m * b, 2 * m, 3 * a if impar else a,
                    (3 * x + 1) // 2 if impar else x // 2,
                    k + 1, q + impar, s + (impar and not anterior), impar)

    try:
        visitar(inicio, 1, 1, inicio, 0, 0, 0, False)
    except PresupuestoAgotado:
        pass
    assert conteos["pendiente"] or conteos["semillas_cubiertas"] == limite - inicio + 1
    return conteos, pendientes, huella.hexdigest()


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--inicio", type=int, default=2)
    analizador.add_argument("--criba", choices=["descuento"], default="descuento")
    analizador.add_argument("--max-nodos", type=int)
    analizador.add_argument("--limite", type=int, required=True)
    analizador.add_argument("--q-min", type=int, required=True)
    analizador.add_argument("--rachas", type=int, required=True)
    analizador.add_argument("--combustible", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    assert argumentos.limite >= argumentos.inicio >= 2 and argumentos.q_min >= 1
    assert argumentos.rachas >= 1 and 0 < argumentos.combustible < 800
    assert argumentos.max_nodos is None or argumentos.max_nodos > 0
    inicio = time.perf_counter()
    conteos, pendientes, huella = explorar(argumentos.limite, argumentos.q_min,
                                          argumentos.rachas, argumentos.combustible,
                                          argumentos.inicio, argumentos.criba, argumentos.max_nodos)
    salida = {"estado": "exploracion exacta; comprobar por separado la aceptacion del caso en Lean",
              "inicio": argumentos.inicio, "limite": argumentos.limite,
              "q_min": argumentos.q_min, "criba": argumentos.criba,
              "max_nodos": argumentos.max_nodos,
              "rachas": argumentos.rachas, "combustible": argumentos.combustible,
              "conteos": conteos, "pendientes": pendientes,
              "sha256_hojas": huella,
              "sha256_explorador": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "segundos": round(time.perf_counter() - inicio, 3)}
    argumentos.salida.write_text(json.dumps(salida, ensure_ascii=False, indent=2)
                                 + "\n", encoding="utf-8")
    print(json.dumps(salida, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
