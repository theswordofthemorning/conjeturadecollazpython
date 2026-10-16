"""Contrasta la barrera triple y su transporte desde una única semilla con T literal."""

import argparse
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path

from cotejar_congruencias import RESIDUOS, minimo_afin, minimo_por_bits, pasos, recorrer


def huella(ruta):
    return hashlib.sha256(ruta.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def comprobar(semilla, prefijo, aes, bes):
    palabra = prefijo + "B" + "".join("A" * a + "B" * b for a, b in zip(aes, bes)) + "A" * aes[-1] + "B"
    recorrer(semilla, palabra)
    partes, excesos, relojes, pesos = [], [], [], []
    anterior = prefijo
    for a, b in zip(aes, bes):
        entrada_b = recorrer(semilla, anterior)
        entrada_a = recorrer(entrada_b, "B")
        r, resto = divmod(entrada_a + 1, 2 ** (a + 2))
        assert resto == 0 and r % 72 == RESIDUOS[a % 6]
        k = r // 72
        p, s = len(pasos(anterior)), sum(pasos(anterior))
        assert 9 * (entrada_b + 5) == 32 * (2 ** a * r + 1)
        assert 2 ** p * (entrada_b + 5) <= 3 ** s * (semilla + 5)
        if k >= 17:
            assert r >= 1237 and 2 ** (a + 12) < entrada_b + 5
            assert a + 13 <= (entrada_b + 4).bit_length()
            assert 2 ** (p + a + 12) < 3 ** s * (semilla + 5)
        partes.append(r)
        excesos.append(k)
        relojes.append((p, s))
        pesos.append(Fraction(3 ** s, 2 ** (p + a)))
        anterior += "B" + "A" * a + "B" * (b - 1)
    for i in range(len(partes) - 1):
        assert 9 ** bes[i] * (3 ** aes[i] * partes[i] + 1) == 8 ** bes[i] * (2 ** aes[i + 1] * partes[i + 1] + 1)
    for i in range(len(partes) - 2):
        assert max(excesos[i:i + 3]) >= 17
    assert sum(excesos) >= 17 * (len(partes) // 3)
    base = sum(RESIDUOS[a % 6] for a in aes[:-1])
    correccion = sum(Fraction(1, 2 ** a) for a in aes[:-1])
    cota = Fraction(9, 32) * (semilla + 5) * sum(pesos)
    assert base + 1224 * (len(partes) // 3) + correccion <= sum(partes) + correccion <= cota
    return dict(semilla=semilla, palabra=palabra, excesos=excesos, partes=partes, relojes=relojes)


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--ventanas-max", type=int, required=True, choices=[3, 4])
    analizador.add_argument("--racha-a-max", type=int, required=True, choices=[1, 2])
    analizador.add_argument("--racha-b-max", type=int, required=True, choices=[1, 2])
    analizador.add_argument("--traslados", type=int, required=True, choices=[1, 2])
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    controles, triples, vacias, interiores = 0, 0, 0, 0
    mejor = None
    for cantidad in range(3, args.ventanas_max + 1):
        for aes in itertools.product(range(args.racha_a_max + 1), repeat=cantidad + 1):
            for bes in itertools.product(range(1, args.racha_b_max + 1), repeat=cantidad):
                for prefijo in ("", "AB"):
                    palabra = prefijo + "B" + "".join("A" * a + "B" * b for a, b in zip(aes, bes)) + "A" * aes[-1] + "B"
                    n, modulo = minimo_afin(palabra)
                    assert (n, modulo) == minimo_por_bits(palabra)
                    for traslado in range(args.traslados):
                        datos = comprobar(n + traslado * modulo, prefijo, aes, bes)
                        controles += 1
                        triples += cantidad - 2
                        vacias += 0 in aes
                        interiores += bool(prefijo)
                        for i in range(cantidad - 2):
                            maximo = max(datos["excesos"][i:i + 3])
                            if mejor is None or maximo < mejor["maximo"]:
                                mejor = dict(maximo=maximo, indice=i, **datos)
    borde = comprobar(6139, "", (0, 0, 1, 0), (1, 1, 1))
    assert borde["excesos"] == [23, 26, 15]
    diagnostico = []
    for cantidad in (3, 6, 12, 24, 48, 96):
        palabra = "B" * (cantidad + 2)
        n, modulo = minimo_afin(palabra)
        assert (n, modulo) == minimo_por_bits(palabra)
        assert n + 5 == 8 ** (cantidad + 2)
        comprobar(n, "", (0,) * (cantidad + 1), (1,) * cantidad)
        peso = sum(Fraction(9, 8) ** i for i in range(cantidad))
        assert peso == 8 * (Fraction(9, 8) ** cantidad - 1)
        inferior = Fraction(32, 9) * (72 * cantidad + 1224 * (cantidad // 3)) / peso
        diagnostico.append(dict(ventanas=cantidad, cota_n_mas_5=str(inferior),
                               bits_minimos_reales=(n + 4).bit_length(), cota_menor_que_uno=inferior < 1))
    assert diagnostico[-1]["cota_menor_que_uno"]
    resultado = dict(alcance="Contraste finito de T, dos cilindros independientes y aritmética racional exacta; "
                            "no sustituye el certificado universal. No se afirma optimalidad de 17.",
                     parametros=vars(args) | {"salida": str(args.salida)}, controles=controles,
                     triples=triples, controles_con_a_vacia=vacias, controles_interiores=interiores,
                     menor_maximo_observado=mejor, testigo_limite_superior_optimo=borde,
                     diagnostico_peso_geometrico=diagnostico,
                     fuente_sha256_lf=huella(Path(__file__)),
                     apoyo_sha256_lf=huella(Path(__file__).with_name("cotejar_congruencias.py")))
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(controles=controles, triples=triples, vacias=vacias,
                         interiores=interiores, menor_maximo=mejor["maximo"])))


if __name__ == "__main__":
    main()
