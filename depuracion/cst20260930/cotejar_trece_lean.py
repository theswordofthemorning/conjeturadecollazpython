"""Cotejo independiente del cierre de trece rachas y del nuevo rango Lean.

No importa generadores ni verificadores anteriores. Coteja el certificado
por atanh racional, enteros y una recurrencia con denominador 6400; recorre
directamente 2<=n<=31623, dentro del censo empirico ya conservado.
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
        s = (13 * c.denominator + c.numerator - 1) // c.numerator
        assert s == fila["semilla_exclusiva"]
        B = fila["B"]
        assert s ** 256 <= 2 ** B
        acumulado = 0
        for _ in range(13):
            acumulado = (25 * B + 10144 * acumulado) // 6400
        assert acumulado == fila["cota_q"]
        assert fila["sobrevive"] == (fila["q_inicio"] <= acumulado)
        if fila["sobrevive"]:
            limite = max(limite, s)
        else:
            descartados += 1
    assert inicio == 171928773 and limite == 31624
    assert Fraction(5 * (8 ** 13 - 5 ** 13), 3 * 5 ** 13) < 751
    assert 1502 * (19 * 60 ** 2 + 5) < 2 ** 27
    maximo = (0, 0)
    rachas_max = 0
    casos_trece = 0
    bordes = {}
    for n in range(2, 31624):
        valor, numerador, denominador = n, 1, 1
        rachas, anterior = 0, False
        for pasos in range(1, 225):
            impar = valor % 2 == 1
            rachas += impar and not anterior
            anterior = impar
            if impar:
                numerador *= 3
                valor = (3 * valor + 1) // 2
            else:
                valor //= 2
            denominador *= 2
            if numerador < denominador:
                assert valor < n, (n, pasos, valor)
                break
            assert valor >= n, (n, pasos, "descenso prematuro")
        else:
            raise AssertionError((n, "cruce no observado en 224 pasos"))
        maximo = max(maximo, (pasos, n))
        rachas_max = max(rachas_max, rachas)
        casos_trece += rachas == 13
        if n in {2, 11214, 11215, 31623}:
            bordes[str(n)] = {"k": pasos, "T_k": valor, "rachas": rachas}
    salida = {"resultado": "sin discrepancias", "filas": len(datos["filas"]),
              "intervalos_descartados": descartados, "semilla_exclusiva": limite,
              "semillas_cotejadas": 31622, "semillas_adicionales_Lean": 20409,
              "mayor_cruce": {"k": maximo[0], "n": maximo[1]},
              "rachas_maximas": rachas_max, "semillas_con_trece_rachas": casos_trece,
              "bordes": bordes,
              "sha256_certificado": hashlib.sha256(argumentos.certificado.read_bytes()).hexdigest(),
              "sha256_cotejador": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    argumentos.salida.write_text(json.dumps(salida, ensure_ascii=False, indent=2)
                                 + "\n", encoding="utf-8")
    print(json.dumps(salida, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
