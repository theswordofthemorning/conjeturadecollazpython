"""Contraste independiente de los cierres R=18,75 y sus vecinos R=19,76.

No importa el certificador. Usa series de atanh con resto racional para
logaritmos (en lugar de cuadrados binarios), reconstruye los convergentes
por matrices y comprueba la cola LMN por duplicaciones (sin derivadas).
El barrido historico de semillas no se repite.
"""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def logaritmo_reducido(numero, terminos):
    """Encierra log(numero) para 1<=numero<=2 con 2 atanh((x-1)/(x+1))."""
    if not 1 <= numero <= 2:
        raise ValueError("Argumento sin reducir")
    z = (numero - 1) / (numero + 1)
    potencia = z
    suma = Fraction(0)
    for indice in range(terminos):
        suma += 2 * potencia / (2 * indice + 1)
        potencia *= z * z
    resto = 2 * potencia / ((2 * terminos + 1) * (1 - z * z))
    return suma, suma + resto


def fraccion_continua(numero, cantidad):
    lista = []
    for _ in range(cantidad):
        parte = numero.numerator // numero.denominator
        lista.append(parte)
        resto = numero - parte
        if not resto:
            break
        numero = 1 / resto
    return lista


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--certificado", type=Path, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    datos = json.loads(argumentos.certificado.read_text(encoding="utf-8"))
    dos_inf, dos_sup = logaritmo_reducido(Fraction(2), 110)
    mitad_inf, mitad_sup = logaritmo_reducido(Fraction(3, 2), 110)
    alfa_inf = 1 + mitad_inf / dos_sup
    alfa_sup = 1 + mitad_sup / dos_inf
    assert Fraction(datos["alfa_inferior"]) < alfa_inf
    assert alfa_sup < Fraction(datos["alfa_superior"])
    assert Fraction(datos["log2_inferior"]) < dos_inf
    assert dos_sup < Fraction(datos["log2_superior"])
    # Control independiente de la constante publicada usada por LMNDebil.
    assert 1 < dos_inf + mitad_inf
    assert Fraction(2434, 100) * (dos_sup + mitad_sup) < 27
    cantidad = len(datos["cocientes"])
    assert fraccion_continua(alfa_inf, cantidad) == datos["cocientes"]
    assert fraccion_continua(alfa_sup, cantidad) == datos["cocientes"]
    matriz = (1, 0, 0, 1)
    pares = []
    for cociente in datos["cocientes"]:
        a, b, c, d = matriz
        matriz = (a * cociente + b, a, c * cociente + d, c)
        pares.append([matriz[0], matriz[2]])
    assert pares == datos["convergentes"]
    assert pares[1][1] == 1
    for indice in range(1, len(pares)):
        p, q = pares[indice]
        pa, qa = pares[indice - 1]
        assert abs(p * qa - pa * q) == 1
        if indice > 1:
            assert qa < q
        if indice % 2:
            assert Fraction(p, q) > alfa_sup
        else:
            assert Fraction(p, q) < alfa_inf

    resultados = []
    revisados = 0
    for fila in datos["resultados"]:
        rachas = fila["rachas"]
        if rachas not in {18, 19, 75, 76}:
            continue
        limites = []
        assert len(fila["intervalos"]) == len(pares) - 2
        for indice, intervalo in enumerate(fila["intervalos"], 1):
            inicio, fin = pares[indice][1], pares[indice + 1][1]
            assert intervalo["j"] == indice
            assert (intervalo["q_inicio"], intervalo["q_fin"]) == (inicio, fin)
            numerador = rachas * (inicio + fin) * 1000
            semilla = (numerador + 692) // 693
            assert semilla == intervalo["semilla_exclusiva"]
            entero = semilla.bit_length() - 1
            resto_inf, resto_sup = logaritmo_reducido(Fraction(semilla, 2 ** entero), 55)
            beta_inf = entero + resto_inf / dos_sup
            beta_sup = entero + resto_sup / dos_inf
            acumulado = 0
            for _ in range(rachas):
                inferior = beta_inf + alfa_inf * acumulado
                superior = beta_sup + alfa_sup * acumulado
                piso_inf = inferior.numerator // inferior.denominator
                piso_sup = superior.numerator // superior.denominator
                assert piso_inf == piso_sup, "Aumentar terminos de la serie"
                acumulado = piso_sup
            assert acumulado == intervalo["cota_q"]
            assert intervalo["sobrevive"] == (inicio <= acumulado)
            if inicio <= acumulado:
                limites.append((semilla, indice))
            revisados += 1
        limite, decisivo = max(limites)
        assert (limite, decisivo) == (fila["semilla_exclusiva"], fila["intervalo_decisivo"])
        # Cola independiente por intervalos [2^t Q,2^(t+1) Q), t>=0.
        # G[A+B(x+d*t)^2] crece a lo sumo por 2 si x>=3d.
        # La cota en t=0 es menor que Q; induccion frente a Q*2^t.
        inicio_cola = pares[-1][1]
        crecimiento = Fraction(5 * (8 ** rachas - 5 ** rachas), 3 * 5 ** rachas)
        d = Fraction(6932, 10000)
        x = d * ((4 * inicio_cola).bit_length() + 1) + 21
        a = rachas.bit_length() + 2
        b = Fraction(30000, 693)
        assert x >= 3 * d
        assert 2 * x * x - (x + d) ** 2 > 0
        assert crecimiento * (a + b * x * x) < inicio_cola
        resultados.append({"rachas": rachas, "semilla_exclusiva": limite,
                           "intervalo_decisivo": decisivo, "cola_diadica": True})

    assert {f["rachas"] for f in resultados} == {18, 19, 75, 76}
    por_rachas = {f["rachas"]: f["semilla_exclusiva"] for f in resultados}
    assert por_rachas[18] <= 2 ** 23 < por_rachas[19]
    assert por_rachas[75] <= 28 * 10 ** 18 + 1 < por_rachas[76]
    # Bordes de log2 para potencias exactas, sin logaritmos de biblioteca.
    assert logaritmo_reducido(Fraction(1), 55) == (0, 0)
    salida = {"resultado": "sin discrepancias", "convergentes": cantidad,
              "intervalos_revisados": revisados, "resultados": resultados,
              "metodo": "atanh racional y cola diadica; sin importar el certificador",
              "sha256_certificado": hashlib.sha256(argumentos.certificado.read_bytes()).hexdigest(),
              "sha256_cotejador": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "censo_repetido": False}
    argumentos.salida.write_text(json.dumps(salida, ensure_ascii=False, indent=2)
                                 + "\n", encoding="utf-8")
    print(json.dumps(salida, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
