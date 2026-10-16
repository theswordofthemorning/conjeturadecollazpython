"""Certificado modular exhaustivo y contraste de cadenas orbitales exactas."""

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path

from cotejar_congruencias import RESIDUOS, minimo_afin, minimo_por_bits, recorrer


def huella(ruta):
    return hashlib.sha256(ruta.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def compatible(terna, modulo):
    b, c, d = terna
    return (pow(9, c, modulo) * (pow(3, b, modulo) * RESIDUOS[b % 6] + 1)
            - pow(8, c, modulo) * (pow(2, d, modulo) * RESIDUOS[d % 6] + 1)) % modulo == 0


def certificado():
    anteriores, periodo_anterior, tablas = [(0, 0, 0)], 1, []
    for periodo in (12, 36, 108, 324):
        modulo = math.gcd(2 ** periodo - 1, 3 ** periodo - 1)
        assert all(pow(base, periodo, modulo) == 1 for base in (2, 3, 8, 9))
        candidatos = [tuple(valor + periodo_anterior * salto for valor, salto in zip(terna, saltos))
                      for terna in anteriores
                      for saltos in itertools.product(range(periodo // periodo_anterior), repeat=3)]
        actuales = sorted(terna for terna in candidatos if compatible(terna, modulo))
        # Segunda construcción independiente: buscar todas las parejas b,c del
        # periodo completo, con un índice de todos los residuos posibles de d.
        indice = {}
        for d in range(periodo):
            valor = (pow(2, d, modulo) * RESIDUOS[d % 6] + 1) % modulo
            indice.setdefault(valor, []).append(d)
        independientes = []
        for b, c in itertools.product(range(periodo), repeat=2):
            valor = (pow(9, c, modulo) * pow(pow(8, c, modulo), -1, modulo)
                     * (pow(3, b, modulo) * RESIDUOS[b % 6] + 1)) % modulo
            independientes.extend((b, c, d) for d in indice.get(valor, []))
        assert actuales == sorted(independientes)
        tablas.append(dict(periodo=periodo, modulo=modulo,
                           candidatos_comprobados=len(candidatos), supervivientes=actuales))
        anteriores, periodo_anterior = actuales, periodo
    assert anteriores == [(0, 0, 0), (0, 216, 36), (108, 0, 216), (216, 0, 108), (323, 2, 1)]
    # Cuatro clases tienen b=0 mod 4 y mod 6; c>=1 implica c>=2.
    # La quinta tiene d=1 mod 54 y c>=2. Las contradicciones son mod 16 y 81.
    assert pow(3, 4, 16) == 1 and pow(9, 2, 16) == 1
    assert all(pow(9, c, 16) * (71 + 1) % 16 == 8 for c in (0, 1))
    assert 8 ** 2 % 16 == 0
    assert pow(2, 54, 81) == 1 and (2 * 13 + 1) % 81 == 27
    assert math.gcd(8, 81) == 1 and 9 ** 2 % 81 == 0
    return tablas


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--ventanas-max", type=int, required=True)
    analizador.add_argument("--racha-a-max", type=int, required=True)
    analizador.add_argument("--racha-b-max", type=int, required=True)
    analizador.add_argument("--traslados", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    assert 1 <= args.ventanas_max <= 4
    assert 0 <= args.racha_a_max <= 3 and 1 <= args.racha_b_max <= 3
    assert 1 <= args.traslados <= 3
    tablas = certificado()
    controles, parejas, minimos, con_vacias = 0, 0, 0, 0
    testigo = None
    for cantidad in range(1, args.ventanas_max + 1):
        for aes in itertools.product(range(args.racha_a_max + 1), repeat=cantidad + 1):
            for bes in itertools.product(range(1, args.racha_b_max + 1), repeat=cantidad):
                palabra = "B" + "".join("A" * a + "B" * b for a, b in zip(aes, bes)) + "A" * aes[-1] + "B"
                n, modulo = minimo_afin(palabra)
                assert (n, modulo) == minimo_por_bits(palabra)
                for traslado in range(args.traslados):
                    semilla = n + traslado * modulo
                    actual = recorrer(semilla, "B")
                    partes = []
                    for a, b in zip(aes, bes):
                        r, resto = divmod(actual + 1, 2 ** (a + 2))
                        assert resto == 0 and r > 0 and r % 2 == 1
                        assert r % 72 == RESIDUOS[a % 6]
                        partes.append(r)
                        actual = recorrer(actual, "A" * a + "B" * b)
                    assert recorrer(actual, "A" * aes[-1] + "B") == recorrer(semilla, palabra)
                    excesos = [(r - RESIDUOS[b % 6]) // 72 for r, b in zip(partes, aes)]
                    assert sum(excesos) >= cantidad // 2
                    for i in range(cantidad - 1):
                        b, c, d = aes[i], bes[i], aes[i + 1]
                        r, v = partes[i:i + 2]
                        assert 9 ** c * (3 ** b * r + 1) == 8 ** c * (2 ** d * v + 1)
                        assert excesos[i] + excesos[i + 1] >= 1
                        parejas += 1
                        if excesos[i] + excesos[i + 1] == 1 and testigo is None:
                            testigo = dict(semilla=semilla, palabra=palabra, b=b, c=c, d=d,
                                           partes=[r, v], excesos=excesos[i:i + 2])
                    minimos += excesos.count(0)
                    con_vacias += 0 in aes
                    controles += 1
    resultado = dict(alcance="Certificado modular exhaustivo con periodicidad comprobada; "
                            "contrastes orbitales finitos. No prueba el presupuesto global.",
                     parametros=vars(args) | {"salida": str(args.salida)}, tablas=tablas,
                     controles=controles, parejas=parejas, minimos_locales=minimos,
                     controles_con_a_vacia=con_vacias, testigo_exceso_72=testigo,
                     fuente_sha256_lf=huella(Path(__file__)),
                     construcciones_sha256_lf=huella(Path(__file__).with_name("cotejar_congruencias.py")))
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(controles=controles, parejas=parejas, minimos=minimos,
                         candidatos=[len(t["supervivientes"]) for t in tablas]), ensure_ascii=False))


if __name__ == "__main__":
    main()
