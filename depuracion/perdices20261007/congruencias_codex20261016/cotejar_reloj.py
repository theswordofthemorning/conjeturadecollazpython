"""Contrasta continuaciones terminales mediante cilindros independientes y T literal."""

import argparse
from collections import Counter
from fractions import Fraction
import itertools
import json
from pathlib import Path

from comprobar_lean import huella
from cotejar_congruencias import minimo_afin, minimo_por_bits, orden, pasos, recorrer


def comprobar(n, palabra, c):
    x = recorrer(n, palabra)
    v = orden(x + c)
    if c == 1:
        sufijo = "A" * v
        esperado = Fraction(3 ** v * (x + 1), 2 ** v) - 1
    else:
        q, r = divmod(v, 3)
        sufijo = "B" * q + "A" * r
        intermedio = Fraction(9 ** q * (x + 5), 8 ** q) - 5
        assert intermedio.denominator == 1
        esperado = Fraction(3 ** r, 2 ** r) * (intermedio + 1) - 1
    y = recorrer(n, palabra + sufijo)
    assert len(pasos(sufijo)) == v
    assert len(pasos(palabra + sufijo)) == len(pasos(palabra)) + v
    assert esperado.denominator == 1 and y == esperado and y > 0
    # La continuación no se obtiene sumando presupuestos de semillas distintas.
    assert recorrer(x, sufijo) == y
    return v


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--bloques-max", type=int, required=True, choices=range(1, 8))
    analizador.add_argument("--carga-max", type=int, required=True, choices=range(3, 33))
    analizador.add_argument("--carga-grande", type=int, required=True)
    analizador.add_argument("--traslados", type=int, required=True, choices=[1, 2])
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    assert args.carga_max < args.carga_grande <= 512
    cargas = list(range(args.carga_max + 1)) + [args.carga_grande]
    controles, semillas, vacias = 0, 0, 0
    restos, potenciales, largos = Counter(), Counter(), Counter()
    for cantidad in range(args.bloques_max + 1):
        for letras in itertools.product("AB", repeat=cantidad):
            palabra = "".join(letras)
            constantes = (1, 5) if not palabra else (1 if palabra[-1] == "A" else 5,)
            for c in constantes:
                for v in cargas:
                    if palabra:
                        minimo, modulo = minimo_afin(palabra, v)
                        assert (minimo, modulo) == minimo_por_bits(palabra, v)
                    else:
                        modulo = 2 ** (v + 1)
                        minimo = (2 ** v - c) % modulo or modulo
                    for traslado in range(args.traslados):
                        n = minimo + traslado * modulo
                        assert orden(recorrer(n, palabra) + c) == v
                        semillas += 1
                        for potencial in (1, 5):
                            carga = comprobar(n, palabra, potencial)
                            controles += 1
                            vacias += not palabra
                            potenciales[potencial] += 1
                            largos[cantidad] += 1
                            if potencial == 5:
                                restos[carga % 3] += 1
    assert set(restos) == {0, 1, 2}
    carpeta = Path(__file__).resolve().parent
    datos = dict(alcance="Contraste finito exacto de la continuación; no prueba un reloj uniforme ni P.",
                 parametros=vars(args) | {"salida": str(args.salida)},
                 semillas=semillas, continuaciones=controles, con_palabra_vacia=vacias,
                 por_potencial=dict(potenciales), por_numero_bloques=dict(largos),
                 restos_carga_b=dict(restos),
                 fuentes_sha256_lf={nombre: huella(carpeta / nombre) for nombre in
                                   (Path(__file__).name, "cotejar_congruencias.py", "comprobar_lean.py")})
    args.salida.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(semillas=semillas, continuaciones=controles, restos_b=dict(restos))))


if __name__ == "__main__":
    main()
