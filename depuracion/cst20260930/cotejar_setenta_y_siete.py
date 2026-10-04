"""Coteja la tabla R=77 sin importar preparadores ni generadores.

Usa atanh racional con resto, potencias enteras, techos por desigualdades
y una recurrencia entera de denominador 6400. No verifica el censo externo.
"""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def log_reducido(x):
    z = (x - 1) / (x + 1)
    potencia, suma = z, Fraction(0)
    for j in range(200):
        suma += 2 * potencia / (2 * j + 1)
        potencia *= z * z
    return suma, suma + 2 * potencia / (401 * (1 - z * z))


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--certificado", type=Path, required=True)
    analizador.add_argument("--prefijos", type=Path, required=True)
    analizador.add_argument("--cotejo-prefijos", type=Path, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    datos = json.loads(argumentos.certificado.read_text(encoding="utf-8"))
    assert datos["rachas"] == 77
    d_inf, d_sup = log_reducido(Fraction(2))
    m_inf, m_sup = log_reducido(Fraction(3, 2))
    t_inf, t_sup = d_inf + m_inf, d_sup + m_sup
    Dinf, Dsup = [Fraction(datos["logaritmos"]["dos"][k]) for k in ("inferior", "superior")]
    Tinf, Tsup = [Fraction(datos["logaritmos"]["tres"][k]) for k in ("inferior", "superior")]
    assert Dinf < d_inf < d_sup < Dsup
    assert Tinf < t_inf < t_sup < Tsup
    assert Tsup < Fraction(317, 200) * Dinf
    inicio, limite, pequenas, cribadas, prefijos = 1, 0, 0, 0, 0
    certificado_prefijos = json.loads(argumentos.prefijos.read_text(encoding="utf-8"))
    cotejo_prefijos = json.loads(argumentos.cotejo_prefijos.read_text(encoding="utf-8"))["resultados"][argumentos.prefijos.name]
    assert cotejo_prefijos["resultado"] == "sin discrepancias"
    assert cotejo_prefijos["sha256_certificado"] == hashlib.sha256(argumentos.prefijos.read_bytes()).hexdigest()
    assert certificado_prefijos["rachas"] == 77 and certificado_prefijos["criba"] == "afinada"
    assert not certificado_prefijos["pendientes"]
    assert datos["intervalos_por_prefijos"] == [91]
    externo = datos["limite_externo_inclusivo"]
    assert externo == 28000000000000000000
    for j, fila in enumerate(datos["filas"]):
        P, Q = fila["superior"]
        p, v = fila["inferior"]
        assert Q > 0 and v > 0 and P * v - p * Q == 1
        assert fila["intervalo"] == j and fila["q_inicio"] == inicio
        assert fila["q_fin"] == Q + v > inicio
        assert p * d_sup - v * t_inf < 0
        c = Fraction(fila["lambda_inferior"])
        assert c == P * Dinf - Q * Tsup
        assert 0 < c < P * d_inf - Q * t_sup
        s, B = fila["semilla_exclusiva"], fila["B"]
        assert (s - 1) * c < 77 <= s * c
        assert 1 << (B - 1) < s ** 256 <= 1 << B
        acumulado = 0
        for _ in range(77):
            acumulado = (25 * B + 10144 * acumulado) // 6400
        assert acumulado == fila["cota_q"]
        assert fila["sobrevive"] == (inicio <= acumulado)
        if fila["sobrevive"]:
            limite = max(limite, s)
        if s <= externo + 1:
            pequenas += 1
        elif j == 91:
            assert (inicio, s) == (130441933147714940, 42938293471394771273)
            assert certificado_prefijos["inicio"] == externo + 1
            assert certificado_prefijos["limite"] == s - 1
            assert certificado_prefijos["q_min"] == inicio
            assert certificado_prefijos["conteos"]["semillas_cubiertas"] == s - externo - 1
            prefijos += 1
        else:
            assert acumulado < inicio
            cribadas += 1
        inicio = fila["q_fin"]
    assert inicio == datos["cola_desde_q"]
    assert limite == datos["semilla_exclusiva"] == 42938293471394771273
    assert prefijos == 1
    R, A, c, H = [datos["cola"][k] for k in ("R", "A", "c", "H")]
    assert (R, A, c, H) == (77, 8691353499027139, 7, 72)
    geometrica = Fraction(0)
    for _ in range(R):
        geometrica = 1 + Fraction(8, 5) * geometrica
    assert A - 1 < geometrica <= A and R <= 1 << c
    assert 8 * A * (19 * (H + 33) ** 2 + c + 1) + 5 < 5 * (1 << H)
    assert 1 << H <= inicio
    salida = {"resultado": "sin discrepancias", "filas": len(datos["filas"]),
              "filas_por_cota_semilla": pequenas, "filas_por_criba": cribadas,
              "filas_por_prefijos": prefijos, "cotejo_prefijos": argumentos.cotejo_prefijos.name,
              "sha256_cotejo_prefijos": hashlib.sha256(argumentos.cotejo_prefijos.read_bytes()).hexdigest(),
              "semilla_exclusiva": limite, "cola_desde_q": inicio,
              "limite_externo_inclusivo": externo,
              "alcance": "Cotejo exacto de tabla, logaritmos y cola. Rozier-Terracol 5.4 permanece externo; no es un censo nuevo.",
              "sha256_certificado": hashlib.sha256(argumentos.certificado.read_bytes()).hexdigest(),
              "sha256_cotejador": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    argumentos.salida.write_text(json.dumps(salida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(salida, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
