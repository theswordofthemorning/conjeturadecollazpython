"""Auditoria independiente del certificado unilateral, sin importar su codigo.

Logaritmos por atanh con resto racional. Cada pareja se comprueba por su
determinante y sus signos; no se presupone que sean convergentes.
Cobertura, cotas de semilla, pisos de la criba y cola por duplicaciones.
"""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def log_reducido(numero, terminos):
    if not 1 <= numero <= 2:
        raise ValueError("Argumento fuera de [1,2]")
    z = (numero - 1) / (numero + 1)
    potencia = z
    suma = Fraction(0)
    for j in range(terminos):
        suma += 2 * potencia / (2 * j + 1)
        potencia *= z * z
    return suma, suma + 2 * potencia / ((2 * terminos + 1) * (1 - z * z))


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--certificado", type=Path, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    datos = json.loads(argumentos.certificado.read_text(encoding="utf-8"))
    dos_inf, dos_sup = log_reducido(Fraction(2), 120)
    mitad_inf, mitad_sup = log_reducido(Fraction(3, 2), 120)
    alfa_inf, alfa_sup = 1 + mitad_inf / dos_sup, 1 + mitad_sup / dos_inf
    alfa_certificada = Fraction(datos["alfa_superior"])
    ln2_certificado = Fraction(datos["log2_inferior"])
    assert Fraction(datos["alfa_inferior"]) <= alfa_inf <= alfa_sup <= alfa_certificada
    assert ln2_certificado < dos_inf < dos_sup < Fraction(datos["log2_superior"])
    previo = 1
    fronteras = 0
    for intervalo in datos["intervalos"]:
        P, Q = intervalo["superior"]
        p, q = intervalo["inferior"]
        assert Q > 0 and q > 0
        assert P * q - p * Q == 1
        assert P - Q * alfa_sup > 0 > p - q * alfa_inf
        assert intervalo["q_inicio"] == previo
        assert intervalo["q_fin"] == Q + q > previo
        # La cota de error vale incluso si b no es coprimo con k.
        # En los dos extremos del intervalo, determinar ceil(b*alfa)
        # con ambas cotas y contrastar directamente el error por arriba.
        for b in {previo, Q + q - 1}:
            ka = (b * alfa_inf).numerator // (b * alfa_inf).denominator + 1
            kb = (b * alfa_sup).numerator // (b * alfa_sup).denominator + 1
            assert ka == kb
            coeficiente = b - Q
            error = (ka - P) - coeficiente * (alfa_sup if coeficiente >= 0 else alfa_inf)
            assert error >= 0
            fronteras += 1
        previo = intervalo["q_fin"]
    assert previo == datos["cola_desde"]

    revisados = 0
    resultados = []
    for resultado in datos["resultados"]:
        R = resultado["rachas"]
        candidatos = []
        assert len(resultado["filas"]) == len(datos["intervalos"])
        for j, (fila, intervalo) in enumerate(zip(resultado["filas"], datos["intervalos"])):
            assert fila["intervalo"] == j
            P, Q = intervalo["superior"]
            c = ln2_certificado * (P - Q * alfa_certificada)
            assert 0 < c < dos_inf * (P - Q * alfa_sup)
            cociente = R / c
            semilla = (cociente.numerator + cociente.denominator - 1) // cociente.denominator
            assert semilla == fila["semilla_exclusiva"]
            entero = semilla.bit_length() - 1
            resto_inf, resto_sup = log_reducido(Fraction(semilla, 1 << entero), 60)
            beta_inf = entero + resto_inf / dos_sup
            beta_sup = entero + resto_sup / dos_inf
            acumulado = 0
            for _ in range(R):
                valor_inf = beta_inf + alfa_inf * acumulado
                valor_sup = beta_sup + alfa_sup * acumulado
                piso_inf = valor_inf.numerator // valor_inf.denominator
                piso_sup = valor_sup.numerator // valor_sup.denominator
                assert piso_inf == piso_sup, "Precision insuficiente para decidir el piso"
                acumulado = piso_sup
            assert acumulado == fila["cota_q"]
            sobrevive = intervalo["q_inicio"] <= acumulado
            assert sobrevive == fila["sobrevive"]
            if sobrevive:
                candidatos.append((semilla, j))
            revisados += 1
        limite, decisivo = max(candidatos)
        assert (limite, decisivo) == (resultado["semilla_exclusiva"], resultado["intervalo_decisivo"])
        G = Fraction(5 * (8 ** R - 5 ** R), 3 * 5 ** R)
        d = Fraction(6932, 10000)
        x = d * ((4 * previo).bit_length() + 1) + 21
        assert x >= 3 * d
        assert G * (R.bit_length() + 2 + Fraction(30000, 693) * x * x) < previo
        resultados.append({"rachas": R, "semilla_exclusiva": limite,
                           "intervalo_decisivo": decisivo, "cola_diadica": True})
    salida = {"resultado": "sin discrepancias", "parejas_unimodulares": len(datos["intervalos"]),
              "fronteras_revisadas": fronteras, "filas_revisadas": revisados,
              "resultados": resultados, "censo_repetido": False,
              "sha256_certificado": hashlib.sha256(argumentos.certificado.read_bytes()).hexdigest(),
              "sha256_cotejador": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    argumentos.salida.write_text(json.dumps(salida, ensure_ascii=False, indent=2)
                                 + "\n", encoding="utf-8")
    print(json.dumps(salida, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
