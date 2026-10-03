"""Contrasta el certificado por residuos con orbitas directas y cobertura disjunta.

Mapa T(n)=n/2 si par y (3n+1)/2 si impar, dominio 2<=n<=limite.
Sin imports del laboratorio. El arbol propone clases; cada hoja se coteja
por iteracion directa en dos representantes y se comprueba la cobertura
mediante intervalos diadicos de bits invertidos. No demuestra CST universal.
"""

import argparse
import hashlib
import json
from pathlib import Path
import time


def orbita(n, combustible):
    x, potencia, denominador, rachas, anterior = n, 1, 1, 0, False
    for k in range(combustible):
        if potencia < denominador:
            assert x < n, (n, k, x)
            return k, potencia, denominador, x, rachas
        assert x >= n, ("descenso anterior", n, k, x)
        impar = bool(x & 1)
        rachas += int(impar and not anterior)
        anterior = impar
        if impar:
            x = (3 * x + 1) // 2
            potencia *= 3
        else:
            x //= 2
        denominador *= 2
    raise AssertionError(("combustible agotado", n, combustible))


def cotejar(limite, combustible):
    contadores = {"nodos": 0, "hojas_compartidas": 0, "hojas_individuales": 0,
                  "pasos_individuales": 0, "semillas_cubiertas": 0,
                  "orbitas_directas": 0, "mayor_cruce": 0}
    intervalos = []
    huella = hashlib.sha256()

    def hoja(r, m, a, c, k, individual):
        assert m == 2 ** k and a < m and c < r
        cantidad = (limite - r) // m + 1
        assert cantidad >= 1
        if individual:
            assert cantidad == 1
        contadores["hojas_individuales" if individual else "hojas_compartidas"] += 1
        contadores["semillas_cubiertas"] += cantidad
        contadores["mayor_cruce"] = max(k, contadores["mayor_cruce"])
        # t>=1 incluye siempre otra semilla de la clase, incluso fuera del rango.
        t = max(1, cantidad - 1)
        for n, esperado in [(r, c), (r + m * t, c + a * t)]:
            j, p, d, x, _ = orbita(n, combustible)
            assert (j, p, d, x) == (k, a, m, esperado), (r, n)
            contadores["orbitas_directas"] += 1
        residuo = r - 2
        assert 0 <= residuo < m
        invertido = int(f"{residuo:0{k}b}"[::-1], 2)
        escala = combustible - 1 - k
        intervalos.append((invertido << escala, (invertido + 1) << escala))
        huella.update(f"{r},{m},{a},{c},{k},{cantidad}\n".encode("ascii"))

    def visitar(r, m, a, c, k):
        contadores["nodos"] += 1
        assert k < combustible
        if r > limite:
            return
        if a < m:
            hoja(r, m, a, c, k, False)
        elif r + m > limite:
            while a >= m:
                if c % 2:
                    c, a = (3 * c + 1) // 2, 3 * a
                else:
                    c //= 2
                m *= 2
                k += 1
                contadores["pasos_individuales"] += 1
                assert k < combustible
            hoja(r, m, a, c, k, True)
        else:
            for b in (0, 1):
                x = a * b + c
                if x % 2:
                    visitar(r + m * b, 2 * m, 3 * a, (3 * x + 1) // 2, k + 1)
                else:
                    visitar(r + m * b, 2 * m, a, x // 2, k + 1)

    visitar(2, 1, 1, 2, 0)
    intervalos.sort()
    assert all(anterior[1] <= siguiente[0]
               for anterior, siguiente in zip(intervalos, intervalos[1:]))
    assert contadores["semillas_cubiertas"] == limite - 1
    contadores["clases_disjuntas"] = len(intervalos)
    return contadores, huella.hexdigest()


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--limite", type=int, required=True)
    analizador.add_argument("--combustible", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    assert argumentos.limite >= 2 and argumentos.combustible >= 2
    inicio = time.perf_counter()
    conteos, huella = cotejar(argumentos.limite, argumentos.combustible)
    bordes = {}
    for n in sorted({2, 31623, 31624, argumentos.limite - 1, argumentos.limite}):
        if 2 <= n <= argumentos.limite:
            k, _, _, x, r = orbita(n, argumentos.combustible)
            bordes[n] = {"k": k, "T_k": x, "rachas": r}
    salida = {"resultado": "sin discrepancias", "mapa": "atajo T",
              "dominio": [2, argumentos.limite], "combustible": argumentos.combustible,
              "conteos": conteos, "bordes": bordes, "sha256_hojas": huella,
              "sha256_cotejador": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "segundos": round(time.perf_counter() - inicio, 3)}
    argumentos.salida.write_text(json.dumps(salida, ensure_ascii=False, indent=2)
                                 + "\n", encoding="utf-8")
    print(json.dumps(salida, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
