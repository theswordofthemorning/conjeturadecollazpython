"""Contrasta el descuento de una entrada impar por bloque completo.

T(n)=n/2 si par y (3n+1)/2 si impar; semillas positivas impares.
Cuenta bloques maximales de impares seguidos por pares, incluso despues
del primer descenso. No usa LMN ni supone un primer cruce. El contraste
finito no sustituye el teorema universal de OcelotasDescuentoRachas.
"""

import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path


def cotas(B, R):
    anterior, descontada = 0, 0
    beta, alfa = Fraction(B, 256), Fraction(317, 200)
    for _ in range(R):
        anterior = math.floor(beta + alfa * anterior)
        descontada = max(0, math.floor(beta - 1 + alfa * descontada))
    return anterior, R + descontada


def cotejar(max_semilla, max_rachas):
    bloques, semillas, pasos, max_valor = 0, 0, 0, 1
    igualdades_locales, igualdades_globales = 0, 0
    for n in range(1, max_semilla + 1, 2):
        semillas += 1
        actual, D, q = n, 0, 0
        B = (((n + 1) ** 256) - 1).bit_length()
        for i in range(max_rachas):
            x, a, b = actual, 0, 0
            while actual % 2:
                actual = (3 * actual + 1) // 2
                a += 1
                pasos += 1
                max_valor = max(max_valor, actual)
            pico = actual
            while actual % 2 == 0:
                assert actual > 0
                actual //= 2
                b += 1
                pasos += 1
            y = actual
            assert a >= 1 and b >= 1 and y >= 1
            assert 2 ** a * (pico + 1) == 3 ** a * (x + 1)
            assert 2 ** b * y == pico
            izquierda = 2 ** (a - 1) * (y + 1)
            derecha = 3 ** (a - 1) * (x + 1)
            assert izquierda <= derecha
            igualdades_locales += izquierda == derecha
            nuevo_D = D + a - 1
            assert 2 ** (nuevo_D + 1) <= (n + 1) * 3 ** D
            D, q = nuevo_D, q + a
            assert q == D + i + 1
            izquierda = 2 ** D * (y + 1)
            derecha = 3 ** D * (n + 1)
            assert izquierda <= derecha
            igualdades_globales += izquierda == derecha
            vieja, nueva = cotas(B, i + 1)
            assert q <= nueva <= vieja
            bloques += 1
    return {
        "semillas_impares": semillas, "bloques": bloques, "pasos_T": pasos,
        "maximo_observado": max_valor, "igualdades_locales": igualdades_locales,
        "igualdades_globales": igualdades_globales,
    }


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--max-semilla", type=int, required=True)
    analizador.add_argument("--max-rachas", type=int, required=True)
    analizador.add_argument("--tablas", type=Path, nargs="+", required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    assert argumentos.max_semilla >= 1 and argumentos.max_rachas >= 1
    contrastes = cotejar(argumentos.max_semilla, argumentos.max_rachas)
    tablas = {}
    for ruta in argumentos.tablas:
        datos = json.loads(ruta.read_text(encoding="utf-8"))
        R, filas, descartadas = datos["rachas"], [], []
        for fila in datos["filas"]:
            anterior, descontada = cotas(fila["B"], R)
            assert anterior == fila["cota_q"] and descontada <= anterior
            if fila["sobrevive"] and descontada < fila["q_inicio"]:
                descartadas.append(fila["intervalo"])
            filas.append({
                "intervalo": fila["intervalo"], "q_inicio": fila["q_inicio"],
                "anterior": anterior, "descontada": descontada,
            })
        tablas[ruta.name] = {
            "sha256": hashlib.sha256(ruta.read_bytes()).hexdigest(),
            "filas": filas, "filas_adicionales_excluidas": descartadas,
        }
    salida = {
        "resultado": "sin discrepancias", "mapa": "T(n)=n/2 par; (3n+1)/2 impar",
        "dominio": "semillas impares positivas; bloques completos, sin condicion de primer cruce",
        "max_semilla": argumentos.max_semilla, "max_rachas": argumentos.max_rachas,
        "contrastes": contrastes, "tablas": tablas,
        "alcance": "Contraste finito de identidades y cotas; no prueba universal ni nuevo cierre CST.",
        "sha256_cotejador": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    argumentos.salida.write_text(json.dumps(salida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"contrastes": contrastes, "descartadas": {
        k: v["filas_adicionales_excluidas"] for k, v in tablas.items()}}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
