"""Cotejo racional de la suma ponderada, incluidas listas de cero, una y dos ventanas."""

import argparse
from collections import Counter
from fractions import Fraction
import itertools
import json
from pathlib import Path

from cotejar_barrera import comprobar, huella
from cotejar_congruencias import RESIDUOS, minimo_afin, minimo_por_bits, pasos, recorrer


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--ventanas-max", type=int, required=True, choices=[3, 4])
    analizador.add_argument("--racha-a-max", type=int, required=True, choices=[1, 2])
    analizador.add_argument("--racha-b-max", type=int, required=True, choices=[1, 2])
    analizador.add_argument("--traslados", type=int, required=True, choices=[1, 2])
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    cantidades = Counter()
    vacias, interiores = 0, 0
    for cantidad in range(args.ventanas_max + 1):
        for aes in itertools.product(range(args.racha_a_max + 1), repeat=cantidad + 1):
            for bes in itertools.product(range(1, args.racha_b_max + 1), repeat=cantidad):
                for prefijo in ("", "AB"):
                    palabra = prefijo + "B" + "".join("A" * a + "B" * b for a, b in zip(aes, bes)) + "A" * aes[-1] + "B"
                    minimo, modulo = minimo_afin(palabra)
                    assert (minimo, modulo) == minimo_por_bits(palabra)
                    for traslado in range(args.traslados):
                        n = minimo + traslado * modulo
                        datos = comprobar(n, prefijo, aes, bes)
                        # Evaluación independiente mediante las entradas B de T literal;
                        # no sustituye las partes por la identidad afín de la prueba Lean.
                        suma_partes, suma_pesos, correcciones = Fraction(0), Fraction(0), Fraction(0)
                        anterior = prefijo
                        for b, c in zip(aes, bes):
                            x = recorrer(n, anterior + "B")
                            suma_partes += Fraction(x + 1, 2 ** (b + 2))
                            bits = pasos(anterior)
                            suma_pesos += Fraction(3 ** sum(bits), 2 ** (len(bits) + b))
                            correcciones += Fraction(1, 2 ** b)
                            anterior += "B" + "A" * b + "B" * (c - 1)
                        inferior = sum(RESIDUOS[b % 6] for b in aes[:-1]) + 1224 * (cantidad // 3)
                        assert suma_partes == sum(datos["partes"])
                        assert inferior + correcciones <= suma_partes + correcciones
                        assert suma_partes + correcciones <= Fraction(9, 32) * (n + 5) * suma_pesos
                        cantidades[cantidad] += 1
                        vacias += 0 in aes
                        interiores += bool(prefijo)
    carpeta = Path(__file__).resolve().parent
    resultado = dict(alcance="Contraste finito exacto de la desigualdad formalizada; no prueba universal ni cota de salida.",
                     parametros=vars(args) | {"salida": str(args.salida)},
                     controles=sum(cantidades.values()), por_numero_ventanas=dict(cantidades),
                     controles_con_a_vacia=vacias, controles_interiores=interiores,
                     fuentes_sha256_lf={nombre: huella(carpeta / nombre) for nombre in
                                       (Path(__file__).name, "cotejar_barrera.py", "cotejar_congruencias.py")})
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(controles=resultado["controles"], por_numero_ventanas=dict(cantidades))))


if __name__ == "__main__":
    main()
