"""Cotejo del criterio temporal modulo 9, con una orbita real y control racional."""

import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


NU = tuple(Fraction(v, 63) for v in (0, 8, 16, 0, 11, 4, 0, 2, 22))
PALABRA_HISTORICA = "AABAAABBAAAAAABAAAAABABAAABAAABBB"


def T(n):
    return (3 * n + 1) // 2 if n % 2 else n // 2


def potencial(r):
    return int(r == 2) + int(r % 3 == 2)


def estacionaria_independiente():
    calculada = [Fraction(0)] * 9
    for x, masa in enumerate((Fraction(0), Fraction(1, 3), Fraction(2, 3))):
        for a in range(1, 7):
            y = (3 * x + 1) * pow(2, -a, 9) % 9
            calculada[y] += masa * Fraction(2 ** (6 - a), 63)
    assert tuple(calculada) == NU
    propagada = [Fraction(0)] * 9
    for x, masa in enumerate(NU):
        propagada[5 * x % 9] += masa / 2
        propagada[5 * (3 * x + 1) % 9] += masa / 2
    assert tuple(propagada) == NU and sum(NU) == 1


def evaluar(semilla, pasos):
    x, unos, extra, cuentas = semilla, 0, 0, Counter()
    cruces, hipotesis = 0, 0
    for k in range(1, pasos + 1):
        r = x % 9
        cuentas[r] += 1
        unos += x % 2
        extra += x % 18 == 4
        y = T(x)
        assert x % 2 + int(x % 18 == 4) + int(x % 3 == 1) == potencial(y % 9)
        x = y
        c1 = sum(cuentas[r] for r in (1, 4, 7))
        c2 = sum(cuentas[r] for r in (2, 5, 8))
        c9 = cuentas[2]
        assert unos + extra + c1 + potencial(semilla % 9) == c9 + c2 + potencial(x % 9)
        tv = sum(abs(Fraction(cuentas[r], k) - NU[r]) for r in range(9)) / 2
        assert Fraction(unos, k) <= Fraction(37, 63) + 3 * tv + Fraction(2, k)
        if 3 ** unos >= 2 ** k:
            assert tv >= Fraction(8, 567) - Fraction(2, 3 * k)
        if k >= 163 and tv <= Fraction(1, 100):
            assert 97 * k <= 300 * c1 and 300 * c2 <= 203 * k
            assert 6300 * c9 <= 1663 * k
            assert 27 * unos < 17 * k and 3 ** unos < 2 ** k
            hipotesis += 1
        cruces += 3 ** unos < 2 ** k
    return dict(semilla=str(semilla), pasos=pasos, subidas=unos,
                TV_final=str(tv), cuentas=[cuentas[r] for r in range(9)],
                prefijos_con_hipotesis=hipotesis, prefijos_con_producto_menor_uno=cruces)


def circuito_euleriano():
    restantes = {(r, bit): int(63 * NU[r]) for r in range(9) for bit in (0, 1)}
    pila, salida = [(1, None)], []
    while pila:
        r, entrada = pila[-1]
        disponibles = [bit for bit in (0, 1) if restantes[r, bit]]
        if disponibles:
            bit = disponibles[0]
            restantes[r, bit] -= 1
            siguiente = 5 * ((3 * r + 1) if bit else r) % 9
            pila.append((siguiente, bit))
        else:
            pila.pop()
            if entrada is not None:
                salida.append(entrada)
    palabra = list(reversed(salida))
    assert not any(restantes.values()) and len(palabra) == 126 and sum(palabra) == 63
    r, cuenta = 1, Counter()
    for bit in palabra:
        cuenta[r] += 1
        r = 5 * ((3 * r + 1) if bit else r) % 9
    assert r == 1 and all(Fraction(cuenta[r], 126) == NU[r] for r in range(9))
    return palabra


def semilla_afin(palabra):
    d, e, m = 1, 0, 1
    for bit in palabra:
        if bit:
            d, e = 3 * d, 3 * e + m
        m *= 2
    return (-e * pow(d, -1, m)) % m, m


def semilla_por_bits(palabra):
    semilla = 0
    for i, bit in enumerate(palabra):
        x = semilla
        for _ in range(i):
            x = T(x)
        if x % 2 != bit:
            semilla += 2 ** i
    return semilla, 2 ** len(palabra)


def control_racional():
    bits = [int(bit) for letra in PALABRA_HISTORICA for bit in ("1" if letra == "A" else "110")]
    minima, modulo = semilla_afin(bits)
    assert (minima, modulo) == semilla_por_bits(bits) and minima == 6416623
    real, racional = minima, Fraction(23)
    colisiones = 0
    primeras = [racional]
    for i, bit in enumerate(bits):
        r = racional.numerator * pow(racional.denominator, -1, 9) % 9
        siguiente = (3 * racional + 1) / 2 if bit else racional / 2
        y = siguiente.numerator * pow(siguiente.denominator, -1, 9) % 9
        # Esta identidad modular tambien vale con ramas prescritas racionales.
        assert bit + int(bit == 0 and r == 4) + int(r % 3 == 1) == potencial(y)
        assert real % 2 == bit
        real, racional = T(real), siguiente
        primeras.append(racional)
        if i >= 1:
            assert real % 9 == y
            colisiones += 1
    assert primeras[2] == 53 and primeras[5] == Fraction(241, 4)
    return dict(palabra=PALABRA_HISTORICA, semilla_real=str(minima),
                semilla_racional_prescrita="23", frontera_fallida="241/4",
                coincidencias_mod_9_desde_dos_subidas=colisiones,
                conclusion="El balance modulo 9 NO detecta la falta de integridad del recorrido racional.")


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--semillas-max", type=int, required=True)
    analizador.add_argument("--pasos", type=int, required=True)
    analizador.add_argument("--periodos-euler", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    if not (1 <= args.semillas_max <= 512 and 163 <= args.pasos <= 400 and 2 <= args.periodos_euler <= 4):
        analizador.error("Presupuesto: semillas<=512, 163<=pasos<=400, 2<=periodos-euler<=4")
    estacionaria_independiente()
    ordinarias = [evaluar(n, args.pasos) for n in range(1, args.semillas_max + 1)]
    palabra = circuito_euleriano() * args.periodos_euler
    residuo, modulo = semilla_afin(palabra)
    assert (residuo, modulo) == semilla_por_bits(palabra)
    semilla = residuo + modulo * ((1 - residuo) * pow(modulo, -1, 9) % 9)
    assert semilla > 0 and semilla % 9 == 1
    x = semilla
    for bit in palabra:
        assert x % 2 == bit
        x = T(x)
    euler = evaluar(semilla, len(palabra))
    assert euler["TV_final"] == "0" and euler["prefijos_con_hipotesis"] > 0
    resultado = dict(
        alcance="Criterio condicional sobre frecuencias temporales de una misma orbita. "
                "No se demuestra la hipotesis de mezcla para excepciones. "
                "El balance modular tambien admite el control racional historico.",
        parametros={k: v for k, v in vars(args).items() if k != "salida"},
        estacionaria_mod_9=list(map(str, NU)),
        semillas_ordinarias=len(ordinarias),
        balances_orbitales=sum(f["pasos"] for f in ordinarias) + len(palabra),
        prefijos_ordinarios_con_hipotesis=sum(f["prefijos_con_hipotesis"] for f in ordinarias),
        ejemplo_real_no_vacio=euler,
        control_racional=control_racional(),
        fuente_sha256=sha256(Path(__file__).read_bytes()).hexdigest())
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(estado="correcto", balances=resultado["balances_orbitales"],
                          ejemplo_TV=euler["TV_final"],
                          hipotesis_en_ejemplo=euler["prefijos_con_hipotesis"])))


if __name__ == "__main__":
    main()
