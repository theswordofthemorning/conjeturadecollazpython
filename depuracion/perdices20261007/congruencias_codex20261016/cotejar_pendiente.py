"""Contrasta una familia explícita y sus mínimos; no busca nuevas semillas."""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

from cotejar_congruencias import minimo_afin, minimo_por_bits, recorrer


CARPETA = Path(__file__).resolve().parent


def huella(ruta):
    return hashlib.sha256(ruta.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def comprobar(a, b, traslados):
    potencia = 2 ** (3 * b)
    q, resto = divmod(potencia - 1, 3 ** a)
    assert resto == 0 and q > 0
    semilla = 2 ** (a + 2) * q - 1
    palabra = "A" * a + "B" * b + "AA"
    largo = a + 3 * b + 2
    modulo = 2 ** largo
    assert minimo_afin(palabra) == minimo_por_bits(palabra) == (semilla, modulo)
    assert 0 < semilla < modulo
    intermedio_a = 4 * potencia - 5
    intermedio_b = 4 * 9 ** b - 5
    final = 9 ** (b + 1) - 10
    assert recorrer(semilla, "A" * a) == intermedio_a
    assert recorrer(intermedio_a, "B" * b) == intermedio_b
    assert recorrer(intermedio_b, "AA") == final
    for traslado in range(traslados):
        entrada = semilla + traslado * modulo
        # T literal se contrasta con una composición racional por bloques.
        racional = Fraction(entrada)
        for bloque in palabra:
            racional = (3 * racional + 1) / 2 if bloque == "A" else (9 * racional + 5) / 8
        assert racional.denominator == 1
        assert recorrer(entrada, palabra) == racional.numerator
        assert racional == final + traslado * 3 ** (a + 2 * b + 2)
    ell = (semilla + 4).bit_length()
    assert semilla + 5 <= 2 ** (3 * b + 2)
    assert ell + a <= largo
    sufijo = "B" * b + "AA"
    minimo_sufijo = 2 ** (3 * b + 2) - 5
    assert minimo_afin(sufijo) == minimo_por_bits(sufijo) == (minimo_sufijo, minimo_sufijo + 5)
    cociente = Fraction(semilla + 5, minimo_sufijo + 5)
    factor = Fraction(2, 3) ** a
    assert cociente == factor + (1 - factor) / potencia
    if b >= a:
        assert cociente <= 2 * factor
    return dict(a=a, b=b, pasos=largo, ell=ell, exceso=largo - ell,
                semilla_hex=hex(semilla) if largo < 100 else None,
                semilla_sha256_hex=hashlib.sha256(hex(semilla).encode()).hexdigest(),
                minimo_original_y_sufijo_cotejados=True,
                cociente_acotado_por_dos_tercios=b >= a)


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--a-max", type=int, required=True)
    analizador.add_argument("--b-borde-max", type=int, required=True)
    analizador.add_argument("--traslados", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    assert 2 <= args.a_max <= 10
    assert 1 <= args.b_borde_max <= 64 and 1 <= args.traslados <= 4
    familia = [comprobar(a, 2 * 3 ** (a - 2), args.traslados)
               for a in range(2, args.a_max + 1)]
    bordes = []
    for a in range(args.a_max + 1):
        for b in range(1, args.b_borde_max + 1):
            if (2 ** (3 * b) - 1) % (3 ** a) == 0:
                bordes.append(comprobar(a, b, args.traslados))
    assert any(f["a"] == 0 for f in bordes) and any(f["a"] == 1 for f in bordes)
    resultado = dict(
        alcance="Contraste finito de la familia y de la fórmula general. La prueba universal "
                "está en PENDIENTE_UNO.md y Lean; no prueba un reloj con pendiente mayor que uno.",
        parametros=vars(args) | {"salida": str(args.salida)},
        familia=familia, bordes= bordes,
        casos=len(familia) + len(bordes),
        recorridos_completos=(len(familia) + len(bordes)) * args.traslados,
        fuentes_sha256_lf={nombre: huella(CARPETA / nombre)
                           for nombre in (Path(__file__).name, "cotejar_congruencias.py")})
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: resultado[k] for k in ("casos", "recorridos_completos")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
