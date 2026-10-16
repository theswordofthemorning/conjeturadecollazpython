"""Congruencias compartidas y mínimos exactos; no ejecuta censos al importar."""

import argparse
import hashlib
import itertools
import json
from pathlib import Path


RESIDUOS = (71, 13, 47, 37, 23, 61)
SOBRECOSTES = (8, 6, 8, 8, 7, 8)
BITS = {"A": (1,), "B": (1, 1, 0)}


def orden(numero):
    assert numero > 0
    return (numero & -numero).bit_length() - 1


def pasos(palabra):
    return tuple(bit for bloque in palabra for bit in BITS[bloque])


def recorrer(semilla, palabra):
    actual = semilla
    for bit in pasos(palabra):
        assert actual % 2 == bit, (semilla, palabra, actual, bit)
        actual = (3 * actual + 1) // 2 if bit else actual // 2
    return actual


def minimo_afin(palabra, valuacion=None):
    """Menor semilla positiva de una palabra, con v2 final opcional exacta."""
    factor, aporte, denominador = 1, 0, 1
    for bit in pasos(palabra):
        factor *= 3 if bit else 1
        aporte = (3 * aporte + denominador) if bit else aporte
        denominador *= 2
    modulo = denominador
    objetivo = -aporte
    if valuacion is not None:
        assert valuacion >= 0
        constante = 1 if palabra[-1] == "A" else 5
        objetivo += denominador * ((1 << valuacion) - constante)
        modulo <<= valuacion + 1
    residuo = objetivo * pow(factor, -1, modulo) % modulo
    return residuo or modulo, modulo


def minimo_por_bits(palabra, valuacion=None):
    """Construcción independiente: levanta un bit de n y recorre T."""
    semilla, actual, modulo, pendiente = 0, 0, 1, 1
    for bit in pasos(palabra):
        if actual % 2 != bit:
            semilla += modulo
            actual += pendiente
        actual = (3 * actual + 1) // 2 if bit else actual // 2
        pendiente *= 3 if bit else 1
        modulo *= 2
    if valuacion is not None:
        constante = 1 if palabra[-1] == "A" else 5
        modulo_carga = 1 << (valuacion + 1)
        traslado = (((1 << valuacion) - actual - constante)
                    * pow(pendiente, -1, modulo_carga)) % modulo_carga
        semilla += modulo * traslado
        modulo *= modulo_carga
    return semilla or modulo, modulo


def fronteras(semilla, cantidades):
    a, b, c, d, e = cantidades
    n, y = semilla, recorrer(semilla, "B" * a)
    z = recorrer(y, "A" * b)
    t = recorrer(z, "B" * c)
    u = recorrer(t, "A" * d)
    final = recorrer(u, "B" * e)
    q, r, s, v = ((n + 5) // (1 << (3 * a + 2)),
                   (y + 1) // (1 << (b + 2)),
                   (z + 5) // (1 << (3 * c + 2)),
                   (t + 1) // (1 << (d + 2)))
    assert all(x > 0 and x % 2 for x in (q, r, s, v))
    assert n + 5 == (1 << (3 * a + 2)) * q
    assert y + 1 == (1 << (b + 2)) * r
    assert 9 ** a * q == 2 ** b * r + 1
    assert 8 ** c * s == 3 ** b * r + 1
    assert 9 ** c * s == 2 ** d * v + 1
    assert r % 72 == RESIDUOS[b % 6]
    assert r >= RESIDUOS[b % 6]
    ell = (n + 4).bit_length()
    if a == 1:
        assert b + SOBRECOSTES[b % 6] <= ell
    return dict(ell=ell, r=r, vfin=orden(final + 5))


def familia_optima(b):
    """b mod 12 en 0..5: r mínimo, c=1, d determinado por la misma n."""
    assert b >= 1 and b % 12 < 6
    r = RESIDUOS[b % 6]
    q, resto = divmod(2 ** b * r + 1, 9)
    assert resto == 0
    s, resto = divmod(3 ** b * r + 1, 8)
    assert resto == 0 and s % 2 == 1
    d = orden(9 * s - 1)
    n = 32 * q - 5
    datos = fronteras(n, (1, b, 1, d, 1))
    assert datos["r"] == r and datos["ell"] == b + SOBRECOSTES[b % 6]
    return dict(b=b, d=d, n=str(n), **datos)


def resumen_minimo(palabra, valuacion=None):
    n, modulo = minimo_afin(palabra, valuacion)
    assert (n, modulo) == minimo_por_bits(palabra, valuacion)
    final = recorrer(n, palabra)
    constante = 1 if palabra[-1] == "A" else 5
    if valuacion is not None:
        assert orden(final + constante) == valuacion
    return dict(pasos=len(pasos(palabra)), valuacion_exigida=valuacion,
                ell_minimo=(n + 4).bit_length(), semilla_minima_hex=hex(n),
                modulo_bits=modulo.bit_length() - 1,
                valuacion_final=orden(final + constante))


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--racha-max", type=int, required=True)
    analizador.add_argument("--periodos-optimos", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    assert 1 <= args.racha_max <= 6 and 1 <= args.periodos_optimos <= 50
    # Tabla completa: no depende de una muestra de semillas.
    tabla = []
    for b in range(6):
        admisibles = [r for r in range(72)
                      if (2 ** b * r + 1) % 9 == 0
                      and (3 ** b * r + 1) % 8 == 0]
        assert admisibles == [RESIDUOS[b]]
        tabla.append(dict(b_mod_6=b, r_mod_72=admisibles[0],
                          sobrecoste=SOBRECOSTES[b]))
    controles = 0
    for cantidades in itertools.product(range(1, args.racha_max + 1), repeat=5):
        palabra = "".join(tipo * cantidad for tipo, cantidad in zip("BABAB", cantidades))
        for valuacion in (None, 0, 1, 2, 5):
            n, modulo = minimo_afin(palabra, valuacion)
            assert (n, modulo) == minimo_por_bits(palabra, valuacion)
            for traslado in (0, 1):
                datos = fronteras(n + traslado * modulo, cantidades)
                if valuacion is not None:
                    assert datos["vfin"] == valuacion
                controles += 1
    # Bordes ajenos a BABAB: palabra vacía, una racha, ambas orientaciones.
    bordes = 0
    for palabra in ("", "A", "B", "AA", "BB", "AB", "BA", "ABAB", "BABA"):
        for valuacion in ((None,) if not palabra else (None, 0, 1, 4)):
            datos = minimo_afin(palabra, valuacion)
            assert datos == minimo_por_bits(palabra, valuacion)
            n, modulo = datos
            for traslado in (0, 1):
                final = recorrer(n + traslado * modulo, palabra)
                if valuacion is not None:
                    assert orden(final + (1 if palabra[-1] == "A" else 5)) == valuacion
                bordes += 1
    optimos = [familia_optima(b) for b in range(1, 12 * args.periodos_optimos + 1)
               if b % 12 < 6]
    palabra = "B" + "A" * 998 + "B" * 527 + "A" * 1670 + "B"
    modelo = [resumen_minimo(palabra), resumen_minimo(palabra, 2600)]
    resultado = dict(alcance="Conteos finitos de contraste. Pruebas universales en CONGRUENCIAS.md; "
                            "sin prueba de presupuesto global ni salida.",
                     parametros=vars(args) | {"salida": str(args.salida)}, tabla=tabla,
                     controles_orbitales=controles, controles_bordes=bordes,
                     optimos=optimos, modelo_anterior=modelo,
                     fuente_sha256_lf=hashlib.sha256(Path(__file__).read_bytes()
                                                     .replace(b"\r\n", b"\n")).hexdigest())
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(controles=controles, bordes=bordes, optimos=len(optimos),
                         ell_modelo=[fila["ell_minimo"] for fila in modelo]), ensure_ascii=False))


if __name__ == "__main__":
    main()
