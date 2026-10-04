"""Contrasta las hojas de la criba descontada desde orbitas directas.

No importa el explorador ni sus transiciones afines. Reconstruye cada
prefijo iterando T desde su menor representante y valida las hojas en
otro representante, la cota racional y la cobertura disjunta.
"""

import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path


def prefijo(n, k):
    x, q, rachas, anterior = n, 0, 0, False
    for j in range(k):
        assert 3 ** q >= 2 ** j, ("cruce anterior", n, j)
        impar = x % 2 == 1
        rachas += int(impar and not anterior)
        anterior = impar
        q += impar
        x = (3 * x + 1) // 2 if impar else x // 2
    return x, q, rachas, anterior


def cotejar(datos):
    inicio, limite, R, qmin = [datos[c] for c in ("inicio", "limite", "rachas", "q_min")]
    combustible = datos["combustible"]
    assert datos["criba"] == "descuento"
    pila = [(inicio, 0)]
    intervalos, cubiertas = [], 0
    conteos = {"nodos": 0, "descenso": 0, "exceso_rachas": 0,
               "criba": 0, "vacio": 0, "pendiente": 0,
               "semillas_cubiertas": 0, "profundidad_maxima": 0}
    huella = hashlib.sha256()
    while pila:
        r, k = pila.pop()
        conteos["nodos"] += 1
        conteos["profundidad_maxima"] = max(k, conteos["profundidad_maxima"])
        m = 2 ** k
        if r > limite:
            conteos["vacio"] += 1
            continue
        c, q, s, anterior = prefijo(r, k)
        a = 3 ** q
        cantidad = (limite - r) // m + 1
        motivo = None
        if a < m and c < r:
            motivo = "descenso"
        elif s > R:
            motivo = "exceso_rachas"
        elif not anterior:
            maximo = c + a * (cantidad - 1)
            potencia = (maximo + 1) ** 256
            inferior, superior = 0, 256 * (maximo + 1).bit_length()
            while inferior < superior:
                medio = (inferior + superior) // 2
                if potencia <= 1 << medio:
                    superior = medio
                else:
                    inferior = medio + 1
            B = inferior
            assert potencia <= 1 << B
            assert B == 0 or 1 << (B - 1) < potencia
            assert B >= 256
            C = 0
            for _ in range(R - s):
                C = math.floor(Fraction(317, 200) * C + Fraction(B, 256) - 1)
            if q + (R - s) + C < qmin:
                motivo = "criba"
        if motivo:
            conteos[motivo] += 1
            cubiertas += cantidad
            t = max(1, cantidad - 1)
            c2, q2, s2, anterior2 = prefijo(r + m * t, k)
            assert (c2, q2, s2, anterior2) == (c + a * t, q, s, anterior)
            residuo = r - inicio
            assert 0 <= residuo < m
            invertido = int(f"{residuo:0{k}b}"[::-1], 2) if k else 0
            intervalos.append((invertido << (combustible - k),
                               (invertido + 1) << (combustible - k)))
            huella.update(f"{r},{m},{a},{c},{k},{q},{s},{motivo},{cantidad}\n".encode("ascii"))
        else:
            assert a >= m and k < combustible, (r, k, "obligacion no resuelta")
            pila.extend([(r + m, k + 1), (r, k + 1)])
    conteos["semillas_cubiertas"] = cubiertas
    assert conteos == datos["conteos"]
    assert huella.hexdigest() == datos["sha256_hojas"]
    intervalos.sort()
    assert all(x[1] <= y[0] for x, y in zip(intervalos, intervalos[1:]))
    assert cubiertas == limite - inicio + 1
    return {"resultado": "sin discrepancias", "conteos": conteos,
            "hojas_no_vacias": len(intervalos), "sha256_hojas": huella.hexdigest()}


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--certificados", type=Path, nargs="+", required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    resultados = {}
    for p in argumentos.certificados:
        datos = json.loads(p.read_text(encoding="utf-8"))
        resultado = cotejar(datos)
        resultado["sha256_certificado"] = hashlib.sha256(p.read_bytes()).hexdigest()
        resultados[p.name] = resultado
    salida = {"resultados": resultados,
              "limite": "cotejo exacto finito; no sustituye la prueba de la criba por prefijos",
              "sha256_cotejador": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    argumentos.salida.write_text(json.dumps(salida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(salida, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
