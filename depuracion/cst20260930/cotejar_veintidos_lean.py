"""Cotejo independiente del cierre de la tabla numerica de veintidos rachas.

No importa generadores ni verificadores anteriores. Coteja el certificado
por atanh racional, enteros y una recurrencia con denominador 6400; el rango de semillas se coteja por separado en cotejar_residuos.py.
"""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def log_reducido(numero):
    z = (numero - 1) / (numero + 1)
    potencia = z
    suma = Fraction(0)
    for j in range(110):
        suma += 2 * potencia / (2 * j + 1)
        potencia *= z * z
    return suma, suma + 2 * potencia / (221 * (1 - z * z))


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--certificado", type=Path, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    datos = json.loads(argumentos.certificado.read_text(encoding="utf-8"))
    assert datos["rachas"] == 22 and datos["semilla_exclusiva"] == 341045748
    assert datos["cola_desde_q"] == 4598951775 and len(datos["filas"]) == 42
    assert (datos["cola_bits"], datos["cola_coeficiente"], datos["cola_desplazamiento"]) == (33, 51580, 6)
    dos_inf, dos_sup = log_reducido(Fraction(2))
    mitad_inf, mitad_sup = log_reducido(Fraction(3, 2))
    tres_inf, tres_sup = dos_inf + mitad_inf, dos_sup + mitad_sup
    Dinf, Dsup = Fraction("0.693147180559945309362"), Fraction("0.693147180559945309471")
    Tinf, Tsup = Fraction("1.098612288668109691335"), Fraction("1.098612288668109691454")
    assert Dinf < dos_inf <= dos_sup < Dsup
    assert Tinf < tres_inf <= tres_sup < Tsup
    assert Tsup < Fraction(317, 200) * Dinf
    inicio = 1
    limite = 0
    descartados = 0
    for fila in datos["filas"]:
        P, Q = fila["superior"]
        p, q = fila["inferior"]
        assert P * q - p * Q == 1 and Q > 0 and q > 0
        assert fila["q_inicio"] == inicio
        assert fila["q_fin"] == Q + q > inicio
        inicio = fila["q_fin"]
        assert p * dos_sup - q * tres_inf < 0
        c = P * Dinf - Q * Tsup
        assert c == Fraction(fila["lambda_inferior"]) > 0
        assert c < P * dos_inf - Q * tres_sup
        s = (22 * c.denominator + c.numerator - 1) // c.numerator
        assert s == fila["semilla_exclusiva"]
        B = fila["B"]
        assert s ** 256 <= 2 ** B
        acumulado = 0
        for _ in range(22):
            acumulado = (25 * B + 10144 * acumulado) // 6400
        assert acumulado == fila["cota_q"]
        assert fila["sobrevive"] == (fila["q_inicio"] <= acumulado)
        if fila["sobrevive"]:
            limite = max(limite, s)
        else:
            descartados += 1
    assert inicio == 4598951775 and limite == 341045748
    assert Fraction(5 * (8 ** 22 - 5 ** 22), 3 * 5 ** 22) < 51580
    assert datos["tiempo_racional"] == [8, 5]
    assert 3 ** 5 < 2 ** 8
    assert datos["tabla_bits"] == 32
    assert datos["puente_por_q"] == {"tiempo_inferior": [3, 2], "exponentes": [32]}
    assert 2 ** 3 < 3 ** 2
    assert 2 * (8 * 51580 * (19 * 65 ** 2 + 6) + 5) < 15 * inicio
    assert 8 * 51580 * (19 * 66 ** 2 + 6) + 5 < 5 * 2 ** 33
    grandes = [(fila["intervalo"], fila["q_inicio"], fila["semilla_exclusiva"])
               for fila in datos["filas"] if fila["sobrevive"] and fila["semilla_exclusiva"] > 4912741]
    assert grandes == [(35, 79335, 6003187), (36, 190537, 341045748)]
    salida = {"resultado": "sin discrepancias", "filas": len(datos["filas"]),
              "intervalos_descartados": descartados, "semilla_exclusiva": limite,
              "cola_desde_q": inicio, "cotejo_semillas": "cotejo_residuos.json",
              "intervalos_por_prefijos": grandes, "cotejo_prefijos": "cotejo_prefijos_22.json",
              "sha256_certificado": hashlib.sha256(argumentos.certificado.read_bytes()).hexdigest(),
              "sha256_cotejador": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    argumentos.salida.write_text(json.dumps(salida, ensure_ascii=False, indent=2)
                                 + "\n", encoding="utf-8")
    print(json.dumps(salida, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
