"""Contraste exacto de relojes por rachas; no ejecuta censos al importar."""

import argparse
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path

from cotejar_congruencias import minimo_afin, minimo_por_bits, pasos, recorrer


CARPETA = Path(__file__).resolve().parent
GAMMA = {"A": Fraction(10, 17), "B": Fraction(1, 17)}


def huella(ruta):
    return hashlib.sha256(ruta.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def fraccion(valor):
    return [valor.numerator, valor.denominator]


def rachas(palabra):
    return [(tipo, len(list(grupo))) for tipo, grupo in itertools.groupby(palabra)]


def coeficiente(tipos):
    acumulado = Fraction(0)
    for tipo in reversed(tipos):
        acumulado = 1 + (1 + GAMMA[tipo]) * acumulado
    return acumulado


def coeficiente_cerrado(inicio, cantidad):
    pares, resto = divmod(cantidad, 2)
    razon = Fraction(486, 289)
    factor = Fraction(44 if inicio == "A" else 35, 17)
    return factor * sum((razon ** j for j in range(pares)), Fraction(0)) + resto * razon ** pares


def cotejar_orbita(n, palabra):
    grupos = rachas(palabra)
    altura = (n + 4).bit_length()
    presupuesto = Fraction(altura)
    actual, longitud, impares = n, 0, 0
    carga = 0
    for tipo, cantidad in grupos:
        duracion = cantidad * (1 if tipo == "A" else 3)
        constante = 1 if tipo == "A" else 5
        entrada = actual
        for bit in pasos(tipo * cantidad):
            assert actual % 2 == bit
            actual = (3 * actual + 1) // 2 if bit else actual // 2
        carga = ((actual + constante) & -(actual + constante)).bit_length() - 1
        orden_entrada = ((entrada + constante) & -(entrada + constante)).bit_length() - 1
        assert duracion + carga == orden_entrada
        assert (1 << longitud) * (entrada + constante) <= 3 ** impares * (n + 5)
        assert 17 * (longitud + duracion + carga) <= 27 * impares + 17 * altura
        assert duracion + carga <= presupuesto
        presupuesto += GAMMA[tipo] * duracion
        longitud += duracion
        impares += cantidad * (1 if tipo == "A" else 2)
    assert actual == recorrer(n, palabra)
    tipos = [tipo for tipo, _ in grupos]
    cota = coeficiente(tipos)
    assert longitud + carga <= cota * altura
    if tipos:
        assert cota == coeficiente_cerrado(tipos[0], len(tipos))
        presupuesto, descuento = Fraction(altura), Fraction(0)
        for i, (tipo, cantidad) in enumerate(grupos):
            duracion = cantidad * (1 if tipo == "A" else 3)
            if i == len(grupos) - 1:
                duracion += carga
            defecto = presupuesto - duracion
            assert defecto >= 0
            peso = 1 + GAMMA[tipo] * coeficiente(tipos[i + 1:])
            descuento += peso * defecto
            presupuesto += GAMMA[tipo] * duracion
        assert longitud + carga + descuento == cota * altura
    return len(grupos), longitud, carga


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--bloques-max", type=int, required=True)
    analizador.add_argument("--rachas-modelo-max", type=int, required=True)
    analizador.add_argument("--vertices-max", type=int, required=True)
    analizador.add_argument("--traslados", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    assert 0 <= args.bloques_max <= 12
    assert 4 <= args.rachas_modelo_max <= 64
    assert 0 <= args.vertices_max <= min(10, args.rachas_modelo_max)
    assert 1 <= args.traslados <= 4
    por_rachas, recorridos, palabras = {}, 0, 0
    for cantidad in range(args.bloques_max + 1):
        for letras in itertools.product("AB", repeat=cantidad):
            palabra = "".join(letras)
            minimo, modulo = minimo_afin(palabra)
            assert (minimo, modulo) == minimo_por_bits(palabra)
            palabras += 1
            for traslado in range(args.traslados):
                numero, _, _ = cotejar_orbita(minimo + traslado * modulo, palabra)
                por_rachas[str(numero)] = por_rachas.get(str(numero), 0) + 1
                recorridos += 1
    # Fronteras con rachas vacías y los dos potenciales terminales, incluidos n par y W vacío.
    bordes = 0
    for inicio in "AB":
        tipos = [inicio, "B" if inicio == "A" else "A"] * 2
        constante = 5 if inicio == "A" else 1
        numerador = 34100 if inicio == "A" else 27125
        for cantidades in itertools.product(range(3), repeat=4):
            palabra = "".join(p * k for p, k in zip(tipos, cantidades))
            n, modulo = minimo_por_bits(palabra)
            assert (n, modulo) == minimo_afin(palabra)
            for traslado in range(args.traslados):
                semilla = n + traslado * modulo
                final = recorrer(semilla, palabra)
                carga = ((final + constante) & -(final + constante)).bit_length() - 1
                assert 4913 * (len(pasos(palabra)) + carga) <= numerador * (semilla + 4).bit_length()
                bordes += 1
    modelos, vertices, reservas = [], 0, 0
    for cantidad in range(1, args.rachas_modelo_max + 1):
        for inicio in "AB":
            tipos = [inicio if i % 2 == 0 else ("B" if inicio == "A" else "A") for i in range(cantidad)]
            cota = coeficiente(tipos)
            assert cota == coeficiente_cerrado(inicio, cantidad)
            assert cota >= cantidad
            # Altura común que hace enteras todas las duraciones saturadas y los bloques B.
            altura = 3 * 17 ** cantidad
            presupuesto, coste = Fraction(altura), Fraction(0)
            for tipo in tipos:
                duracion = presupuesto
                assert duracion.denominator == 1
                if tipo == "B":
                    assert duracion.numerator % 3 == 0
                coste += duracion
                presupuesto += GAMMA[tipo] * duracion
            assert coste == cota * altura
            # Mismo crecimiento con cualquier reserva constante elegida; no son órbitas.
            for reserva in (0, 1, 17, 1224):
                presupuesto, total = Fraction(altura + reserva), Fraction(0)
                for tipo in tipos:
                    duracion = presupuesto - reserva
                    assert duracion > 0 and duracion.denominator == 1
                    assert presupuesto - duracion == reserva
                    total += duracion
                    presupuesto += GAMMA[tipo] * duracion
                assert total == cota * altura
                pesos = [1 + GAMMA[tipo] * coeficiente(tipos[i + 1:])
                         for i, tipo in enumerate(tipos)]
                assert total + reserva * sum(pesos) == cota * (altura + reserva)
                reservas += 1
            if cantidad <= args.vertices_max:
                maximo = Fraction(0)
                for elecciones in itertools.product((0, 1), repeat=cantidad):
                    presupuesto, total = Fraction(1), Fraction(0)
                    for tipo, eleccion in zip(tipos, elecciones):
                        duracion = presupuesto * eleccion
                        total += duracion
                        presupuesto += GAMMA[tipo] * duracion
                    maximo = max(maximo, total)
                    vertices += 1
                assert maximo == cota
            modelos.append(dict(inicio=inicio, rachas=cantidad, coeficiente=fraccion(cota),
                                altura=str(altura), coste=str(coste.numerator)))
    resultado = dict(parametros={k: v for k, v in vars(args).items() if k != "salida"},
                     palabras=palabras, recorridos=recorridos, por_rachas=por_rachas,
                     bordes_cuatro_rachas=bordes, vertices_relajacion=vertices, modelos=modelos,
                     modelos_con_reserva=reservas,
                     alcance="Cotejo finito exacto. Los modelos saturados son restricciones lineales, no orbitas.",
                     fuentes_sha256_lf={nombre: huella(CARPETA / nombre)
                                        for nombre in (Path(__file__).name, "cotejar_congruencias.py")})
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK: {recorridos} recorridos, {bordes} bordes, {vertices} vertices; {len(modelos)} modelos racionales.")


if __name__ == "__main__":
    main()
