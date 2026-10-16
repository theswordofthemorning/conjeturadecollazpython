"""Contraste orbital de ventanas interiores, incluida la ausencia de rachas A."""

import argparse
import hashlib
import itertools
import json
from pathlib import Path

from cotejar_congruencias import minimo_afin, minimo_por_bits, RESIDUOS, SOBRECOSTES


def recorrer_literal(semilla, palabra):
    actual = semilla
    longitud, impares = 0, 0
    for letra in palabra:
        for paridad in ((1,) if letra == "A" else (1, 1, 0)):
            assert actual % 2 == paridad
            if actual % 2:
                actual = (3 * actual + 1) // 2
                impares += 1
            else:
                actual //= 2
            longitud += 1
    return actual, longitud, impares


def huella(ruta):
    return hashlib.sha256(ruta.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--prefijo-max", type=int, required=True)
    analizador.add_argument("--racha-max", type=int, required=True)
    analizador.add_argument("--traslados", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    assert 0 <= args.prefijo_max <= 7 and 1 <= args.racha_max <= 4
    assert 1 <= args.traslados <= 4
    prefijos = ["".join(letras) for largo in range(args.prefijo_max + 1)
                for letras in itertools.product("AB", repeat=largo)]
    controles, vacias, interiores = 0, 0, 0
    muestras = []
    for prefijo, b, c, d in itertools.product(prefijos, range(args.racha_max + 1),
                                             range(1, args.racha_max + 1),
                                             range(args.racha_max + 1)):
        ventana = "B" + "A" * b + "B" * c + "A" * d + "B"
        # Una cola adicional prueba que la ventana no necesita terminar el camino.
        cola = "AB" if (b + c + d) % 2 else ""
        palabra = prefijo + ventana + cola
        menor, modulo = minimo_afin(palabra)
        assert (menor, modulo) == minimo_por_bits(palabra)
        for traslado in range(args.traslados):
            n = menor + traslado * modulo
            x, pasos, impares = recorrer_literal(n, prefijo)
            y, _, _ = recorrer_literal(x, "B")
            z, _, _ = recorrer_literal(y, "A" * b)
            t, _, _ = recorrer_literal(z, "B" * c)
            u, _, _ = recorrer_literal(t, "A" * d)
            recorrer_literal(u, "B" + cola)
            r, resto = divmod(y + 1, 2 ** (b + 2))
            assert resto == 0 and r > 0 and r % 2 == 1
            assert r % 72 == RESIDUOS[b % 6]
            assert 9 * (x + 5) == 32 * (2 ** b * r + 1)
            assert b + SOBRECOSTES[b % 6] <= (x + 4).bit_length()
            izquierda = 2 ** (pasos + b + SOBRECOSTES[b % 6] - 1)
            derecha = 3 ** impares * (n + 5)
            assert izquierda < derecha
            controles += 1
            vacias += b == 0 or d == 0
            interiores += bool(prefijo)
            if traslado == 0 and prefijo in ("", "ABAB") and b == d == 0:
                muestras.append(dict(prefijo=prefijo, b=b, c=c, d=d, n=n, x=x,
                                     izquierda=izquierda, derecha=derecha))
    carpeta = Path(__file__).resolve().parent
    resultado = dict(alcance="Contraste finito por composición afín, levantamiento de bits y "
                            "órbita literal. La prueba universal está en Lean; no prueba P.",
                     parametros=vars(args) | {"salida": str(args.salida)},
                     controles=controles, con_racha_a_vacia=vacias,
                     ventanas_interiores=interiores, muestras=muestras,
                     fuente_sha256_lf=huella(Path(__file__)),
                     construcciones_sha256_lf=huella(carpeta / "cotejar_congruencias.py"))
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK: {controles} ventanas, {vacias} con alguna racha A vacía.")


if __name__ == "__main__":
    main()
