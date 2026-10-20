"""Contrasta el denominador global; no vuelve a censar semillas."""

import argparse
from fractions import Fraction
import hashlib
import itertools
import json
from math import gcd
from pathlib import Path

from cotejar_congruencias import minimo_afin, minimo_por_bits, pasos, recorrer


CARPETA = Path(__file__).resolve().parent


def huella(ruta):
    return hashlib.sha256(ruta.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def afin(palabra):
    """Composicion por bloques, independiente del calculo bit a bit importado."""
    multiplicador, aporte, modulo = 1, 0, 1
    for letra in palabra:
        divisor, factor, constante = (2, 3, 1) if letra == "A" else (8, 9, 5)
        multiplicador, aporte, modulo = (factor * multiplicador,
                                         factor * aporte + constante * modulo,
                                         divisor * modulo)
    return multiplicador, aporte, modulo


def comprobar(palabra):
    d, e, m = afin(palabra)
    assert d > m and e > 0
    g = gcd(d - m, e)
    q, r = (d - m) // g, e // g
    assert g % 2 == 1 and q <= r <= 5 * q
    assert Fraction(e, d - m) == Fraction(r, q)
    minimo, modulo = minimo_afin(palabra)
    assert (minimo, modulo) == minimo_por_bits(palabra)
    assert modulo == m
    assert minimo == ((-r * pow(q, -1, m)) % m or m)
    for n in (minimo, minimo + m):
        y = recorrer(n, palabra)
        assert m * y == d * n + e
        assert (q * n + r) % m == 0
        assert m <= q * n + r <= q * (n + 5)
    return dict(palabra=palabra, L=len(pasos(palabra)), minimo=str(minimo),
                ell=(minimo + 4).bit_length(), g=str(g), q=str(q), r=str(r),
                modulo=str(m), cota_util=q < m)


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--bloques-max", type=int, required=True)
    analizador.add_argument("--familia-max", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    assert 1 <= args.bloques_max <= 14 and 3 <= args.familia_max <= 256
    niveles = []
    for largo in range(1, args.bloques_max + 1):
        filas = [comprobar("".join(w)) for w in itertools.product("AB", repeat=largo)]
        niveles.append(dict(bloques=largo, palabras=len(filas),
                            sin_cancelacion=sum(f["g"] == "1" for f in filas),
                            cota_util=sum(f["cota_util"] for f in filas)))
    familias = []
    for b in range(args.familia_max + 1):
        f = comprobar("A" + "B" * b)
        d, e, m = afin(f["palabra"])
        assert d == 3 * 9 ** b and m == 2 * 8 ** b
        assert e == 11 * 9 ** b - 10 * 8 ** b
        assert f["g"] == "1"
        assert 3 * e + 8 * 8 ** b == 11 * (d - m)
        if b >= 3:
            assert int(f["q"]) > m
        familias.append({k: v for k, v in f.items() if k != "palabra"} | {"b": b})
    # El contraste positivo conserva el mecanismo de repeticion conocido.
    for b in range(1, args.familia_max + 1):
        f = comprobar("B" * b)
        assert f["q"] == "1" and f["r"] == "5"
        f = comprobar("AB" * b)
        assert f["q"] == "11" and f["r"] == "19"
    # Solo leer testigos ya guardados; no rehacer sus 719 millones de nodos.
    fuente = CARPETA.parent / "medicion_salida_ab.json"
    historico = json.loads(fuente.read_text(encoding="utf-8"))
    por_semilla = {}
    for fila in historico["filas"]:
        n = int(fila["minimo"])
        por_semilla[n] = max(por_semilla.get(n, 0), fila["largo"])
    testigos = []
    for n, longitud in por_semilla.items():
        x, bits = n, []
        for _ in range(longitud):
            bits.append(x % 2)
            x = (3 * x + 1) // 2 if x % 2 else x // 2
        # Decodificacion retrospectiva unica: cada cero cierra un B=110.
        palabra, i = [], len(bits)
        while i:
            if bits[i - 1] == 0:
                assert i >= 3 and bits[i - 3:i] == [1, 1, 0]
                palabra.append("B")
                i -= 3
            else:
                palabra.append("A")
                i -= 1
        f = comprobar("".join(reversed(palabra)))
        assert f["minimo"] == str(n)
        testigos.append(f)
    resultado = dict(
        alcance="Contraste finito exacto, no prueba por barrido ni nueva auditoria del censo.",
        parametros={k: v for k, v in vars(args).items() if k != "salida"},
        niveles=niveles, familias=familias, testigos_historicos=testigos,
        resumen_testigos=dict(total=len(testigos),
                             sin_cancelacion=sum(f["g"] == "1" for f in testigos),
                             cota_util=sum(f["cota_util"] for f in testigos)),
        fuentes_sha256_lf={p.name: huella(p) for p in
                           (Path(__file__), CARPETA / "cotejar_congruencias.py", fuente)})
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(palabras=sum(f["palabras"] for f in niveles),
                          familias=len(familias), testigos=resultado["resumen_testigos"])))


if __name__ == "__main__":
    main()
