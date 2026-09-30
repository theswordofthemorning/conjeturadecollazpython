"""Cotejo independiente del descenso y de la obligación aritmética de OcelotasFinito.

Mapa clásico agrupado, coeficiente Fraction; no importa otros verificadores.
El cotejo aritmético es un cálculo Python, no una prueba de esa obligación en Lean.
"""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def primer_cruce(n, max_pasos):
    if n < 2 or max_pasos < 1:
        raise ValueError("Se requiere n>=2 y max_pasos>=1")
    valor = n
    coeficiente = Fraction(1)
    impares = 0
    for paso in range(1, max_pasos + 1):
        if valor % 2:
            valor = 3 * valor + 1
            coeficiente *= 3
            impares += 1
        assert valor % 2 == 0
        valor //= 2
        coeficiente /= 2
        if coeficiente < 1:
            return paso, impares, valor
    raise RuntimeError(f"INCONCLUSO: n={n}, tope={max_pasos}")


def cotejar(certificado, max_pasos):
    datos = json.loads(certificado.read_text(encoding="utf-8"))
    assert datos["rachas_hasta"] == 10
    assert datos["n_maximo"] == 11214 and datos["q_comprobados"] == 82696
    huella = hashlib.sha256()
    maximo = 0
    testigo = None
    bordes = {}
    for n in range(2, datos["n_maximo"] + 1):
        k, q, valor = primer_cruce(n, max_pasos)
        assert valor < n
        huella.update(f"{n},{k},{q},{valor}\n".encode())
        if k > maximo:
            maximo, testigo = k, n
        if n in (2, 3, 39, datos["n_maximo"]):
            bordes[n] = {"k": k, "q": q, "valor": valor}
    assert maximo == 105
    assert huella.hexdigest() == datos["barrido"]["sha256_filas_n_k_q_valor"]
    try:
        primer_cruce(testigo, maximo - 1)
    except RuntimeError:
        pass
    else:
        raise AssertionError("Se aceptó un recorrido con tope insuficiente")
    assert primer_cruce(testigo, maximo)[0] == maximo

    # Potencias sucesivas: no se usa log2 ni bit_length para encontrar k.
    potencia_tres, potencia_dos, k = 1, 2, 1
    por_semilla, por_criba = 0, 0
    ejemplos_criba = []
    for q in range(1, datos["q_comprobados"] + 1):
        potencia_tres *= 3
        while potencia_dos <= potencia_tres:
            potencia_dos *= 2
            k += 1
        diferencia = potencia_dos - potencia_tres
        assert 0 < diferencia < potencia_tres and k < datos["k_exclusivo"]
        if 10 * potencia_tres <= 11215 * diferencia:
            por_semilla += 1
        else:
            m = (q - 1) // 182
            assert 182 * m < q
            assert 11 * potencia_tres <= 2 ** m * diferencia
            por_criba += 1
            if len(ejemplos_criba) < 3:
                ejemplos_criba.append({"q": q, "k": k, "m": m})
    potencia_tres *= 3
    while potencia_dos <= potencia_tres:
        potencia_dos *= 2
        k += 1
    assert k == datos["k_exclusivo"]
    return {
        "certificado_previo": certificado.name,
        "sha256_certificado_previo": hashlib.sha256(certificado.read_bytes()).hexdigest(),
        "mapa": "clasico agrupado: 3n+1 si impar, luego una division por 2",
        "aritmetica": "int y Fraction",
        "semillas": datos["n_maximo"] - 1,
        "intervalo_cerrado": [2, datos["n_maximo"]],
        "max_pasos": max_pasos,
        "max_primer_cruce": maximo,
        "primer_testigo_del_maximo": testigo,
        "tope_insuficiente_rechazado": True,
        "sha256_filas_n_k_q_valor": huella.hexdigest(),
        "coincide_con_certificado_previo": True,
        "bordes": bordes,
        "obligacion_aritmetica": {
            "intervalo_q_cerrado": [1, datos["q_comprobados"]],
            "por_cota_semilla": por_semilla,
            "por_criba_lineal": por_criba,
            "ejemplos_criba": ejemplos_criba,
            "primer_q_fuera": q + 1,
            "k_del_primer_q_fuera": k,
            "certificada_en_lean": False,
        },
        "fallos": 0,
        "sha256_programa": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--certificado", type=Path, required=True)
    analizador.add_argument("--max-pasos", type=int, required=True)
    analizador.add_argument("--salida", type=Path)
    argumentos = analizador.parse_args()
    if argumentos.max_pasos < 1:
        analizador.error("max-pasos debe ser positivo")
    resultado = cotejar(argumentos.certificado, argumentos.max_pasos)
    contenido = json.dumps(resultado, ensure_ascii=False, indent=2) + "\n"
    if argumentos.salida:
        argumentos.salida.write_text(contenido, encoding="utf-8")
    print(contenido, end="")


if __name__ == "__main__":
    main()
