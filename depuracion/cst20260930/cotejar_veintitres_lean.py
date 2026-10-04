"""Coteja la tabla de 23 rachas y sus dos ventanas por calculo independiente.

No importa el preparador ni el explorador. Usa series racionales de atanh,
potencias enteras y la recurrencia de la criba en aritmetica Fraction.
El rango hasta 4912740 se remite al certificado Lean existente.
"""

import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path


def huella(ruta):
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


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
    analizador.add_argument("--prefijos", type=Path, nargs=2, default=[])
    analizador.add_argument("--cotejos-prefijos", type=Path, nargs="+", default=[])
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    assert bool(argumentos.prefijos) == bool(argumentos.cotejos_prefijos)
    datos = json.loads(argumentos.certificado.read_text(encoding="utf-8"))
    assert datos["rachas"] == 23
    interno = datos["limite_certificado_inclusivo"]
    assert interno == 4912740 and datos["intervalos_por_prefijos"] == [35, 36]
    resultados = {}
    for ruta in argumentos.cotejos_prefijos:
        nuevos = json.loads(ruta.read_text(encoding="utf-8"))["resultados"]
        assert not resultados.keys() & nuevos.keys()
        resultados.update(nuevos)
    ventanas = {}
    for ruta in argumentos.prefijos:
        prefijo = json.loads(ruta.read_text(encoding="utf-8"))
        cotejo = resultados[ruta.name]
        assert cotejo["resultado"] == "sin discrepancias"
        assert cotejo["sha256_certificado"] == huella(ruta)
        assert cotejo["conteos"] == prefijo["conteos"]
        assert cotejo["sha256_hojas"] == prefijo["sha256_hojas"]
        assert prefijo["rachas"] == 23 and prefijo["criba"] == "afinada"
        assert prefijo["inicio"] == interno + 1
        assert not prefijo["pendientes"] and prefijo["conteos"]["pendiente"] == 0
        assert prefijo["conteos"]["semillas_cubiertas"] == prefijo["limite"] - interno
        qmin = prefijo["q_min"]
        assert qmin not in ventanas
        ventanas[qmin] = prefijo
    if ventanas:
        assert set(ventanas) == {79335, 190537}
    d_inf, d_sup = log_reducido(Fraction(2))
    m_inf, m_sup = log_reducido(Fraction(3, 2))
    t_inf, t_sup = d_inf + m_inf, d_sup + m_sup
    Dinf, Dsup = [Fraction(datos["logaritmos"]["dos"][k]) for k in ("inferior", "superior")]
    Tinf, Tsup = [Fraction(datos["logaritmos"]["tres"][k]) for k in ("inferior", "superior")]
    assert Dinf < d_inf < d_sup < Dsup
    assert Tinf < t_inf < t_sup < Tsup
    assert Tsup < Fraction(317, 200) * Dinf
    inicio, limite = 1, 0
    pequenas, cribadas, prefijos_usados = [], [], []
    for j, fila in enumerate(datos["filas"]):
        P, Q = fila["superior"]
        p, v = fila["inferior"]
        assert Q > 0 and v > 0 and P * v - p * Q == 1
        assert fila["intervalo"] == j and fila["q_inicio"] == inicio
        assert fila["q_fin"] == Q + v > inicio
        assert p * d_sup - v * t_inf < 0
        cota = Fraction(fila["lambda_inferior"])
        assert cota == P * Dinf - Q * Tsup
        assert 0 < cota < P * d_inf - Q * t_sup
        semilla, B = fila["semilla_exclusiva"], fila["B"]
        assert (semilla - 1) * cota < 23 <= semilla * cota
        assert 1 << (B - 1) < semilla ** 256 <= 1 << B
        acumulado = 0
        for _ in range(23):
            acumulado = math.floor(Fraction(B, 256) + Fraction(317, 200) * acumulado)
        assert acumulado == fila["cota_q"]
        assert fila["sobrevive"] == (inicio <= acumulado)
        if fila["sobrevive"]:
            limite = max(limite, semilla)
        if semilla <= interno + 1:
            pequenas.append(j)
        elif j in (35, 36):
            assert fila["sobrevive"]
            assert (inicio, semilla) == {35: (79335, 6276059), 36: (190537, 356547673)}[j]
            if ventanas:
                assert ventanas[inicio]["limite"] == semilla - 1
            prefijos_usados.append(j)
        else:
            assert acumulado < inicio
            cribadas.append(j)
        inicio = fila["q_fin"]
    assert inicio == datos["cola_desde_q"] == 19362882631
    assert limite == datos["semilla_exclusiva"] == 356547673
    assert not datos["cierra_con_limite_certificado"]
    assert (len(pequenas), len(cribadas), len(prefijos_usados)) == (35, 6, 2)
    R, A, c, H = [datos["cola"][k] for k in ("R", "A", "c", "H")]
    assert (R, A, c, H) == (23, 82528, 5, 34)
    geometrica = Fraction(0)
    for _ in range(R):
        geometrica = 1 + Fraction(8, 5) * geometrica
    assert A - 1 < geometrica <= A and R <= 1 << c
    assert 8 * A * (19 * (H + 33) ** 2 + c + 1) + 5 < 5 * (1 << H)
    assert 1 << H <= inicio
    salida = {
        "resultado": "sin discrepancias", "filas": len(datos["filas"]),
        "prefijos_cotejados": bool(ventanas),
        "filas_por_cota_semilla": pequenas, "filas_por_criba": cribadas,
        "filas_por_prefijos": prefijos_usados, "limite_certificado_inclusivo": interno,
        "semilla_exclusiva": limite, "cola_desde_q": inicio,
        "alcance": ("Tabla, cola y logaritmos cotejados. "
                    + ("Ventanas cotejadas por separado. " if ventanas else "Ventanas pendientes. ")
                    + "Falta la cadena Lean de 23. No usa Rozier-Terracol."),
        "sha256_certificado": huella(argumentos.certificado),
        "sha256_prefijos": {p.name: huella(p) for p in argumentos.prefijos},
        "sha256_cotejos_prefijos": {p.name: huella(p) for p in argumentos.cotejos_prefijos},
        "sha256_cotejador": huella(Path(__file__)),
    }
    argumentos.salida.write_text(json.dumps(salida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(salida, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
