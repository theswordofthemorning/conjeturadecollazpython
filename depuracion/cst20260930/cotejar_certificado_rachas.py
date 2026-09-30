"""Cotejo independiente: criba más débil q<E*m y mapa clásico agrupado.

No importa certificar_rachas.py. Recorre otra criba, con más supervivientes,
y comprueba que aun así basta el mismo intervalo de semillas (o uno menor).
"""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def cotejar(archivo):
    datos = json.loads(archivo.read_text(encoding="utf-8"))
    r = datos["rachas_hasta"]
    factor = Fraction(0)
    for _ in range(r):
        factor = 1 + Fraction(8, 5) * factor
    e = (factor.numerator + factor.denominator - 1) // factor.denominator
    assert str(factor) == datos["factor_racional"]
    assert e == datos["exponente_entero"]
    h = datos["h"]
    c = datos["c"]
    assert r + 1 <= 2 ** c and 2 ** h > 2 * e * (c + 14 * (h + 1))
    assert datos["k_exclusivo"] == 2 ** h
    potencia_tres = 1
    potencia_dos = 2
    k = 1
    mayores = []
    originales = {f["q"]: f for f in datos["supervivientes"]}
    vistos = set()
    for q in range(1, datos["q_comprobados"] + 2):
        potencia_tres *= 3
        while potencia_dos <= potencia_tres:
            potencia_dos *= 2
            k += 1
        if q == datos["q_comprobados"] + 1:
            assert k == datos["k_del_primer_q_excluido"] >= 2 ** h
            break
        assert k < 2 ** h
        diferencia = potencia_dos - potencia_tres
        m = 0
        cota = diferencia
        while cota < (r + 1) * potencia_tres:
            cota *= 2
            m += 1
        if q < e * m:
            # ceil(r P / Delta) - 1 usando Fraction.
            limite = Fraction(r * potencia_tres, diferencia)
            n_maximo = -(-limite.numerator // limite.denominator) - 1
            mayores.append((q, k, n_maximo))
        if q in originales:
            fila = originales[q]
            assert q < e * m
            assert (fila["k"], fila["m"], fila["n_maximo"]) == (k, m, n_maximo)
            vistos.add(q)
    assert vistos == set(originales)
    maximo_independiente = max(f[2] for f in mayores)
    assert maximo_independiente <= datos["n_maximo"]
    huella = hashlib.sha256()
    max_k = 0
    bordes = {}
    for n in range(2, datos["n_maximo"] + 1):
        x = n
        coeficiente = Fraction(1)
        q = 0
        for k in range(1, datos["barrido"]["max_pasos_permitidos"] + 1):
            if x % 2:
                x = 3 * x + 1  # paso impar del mapa clásico
                coeficiente *= 3
                q += 1
            assert x % 2 == 0
            x //= 2
            coeficiente /= 2
            if coeficiente < 1:
                break
        else:
            raise AssertionError(f"Primer cruce inconcluso: n={n}")
        assert x < n
        max_k = max(max_k, k)
        huella.update(f"{n},{k},{q},{x}\n".encode())
        if n in (2, 3, 39, datos["n_maximo"]):
            bordes[n] = {"k": k, "q": q, "valor": x}
    assert huella.hexdigest() == datos["barrido"]["sha256_filas_n_k_q_valor"]
    return {
        "certificado": archivo.name,
        "criba_independiente": "q < E*m; más débil que la recurrencia",
        "supervivientes_independientes": len(mayores),
        "n_maximo_independiente": maximo_independiente,
        "semillas_cotejadas": datos["n_maximo"] - 1,
        "max_primer_cruce_observado": max_k,
        "sha256_filas_coincide": True,
        "bordes": bordes,
        "fallos": 0,
    }


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("certificado", type=Path)
    analizador.add_argument("--salida", type=Path)
    opciones = analizador.parse_args()
    resultado = cotejar(opciones.certificado)
    contenido = json.dumps(resultado, ensure_ascii=False, indent=2) + "\n"
    if opciones.salida:
        opciones.salida.write_text(contenido, encoding="utf-8")
    print(contenido, end="")


if __name__ == "__main__":
    main()
