"""Contrasta reservas relativas del modelo y la barrera orbital AB, con fracciones."""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

from cotejar_congruencias import minimo_afin, minimo_por_bits, recorrer


CARPETA = Path(__file__).resolve().parent
GAMMA = {"A": Fraction(10, 17), "B": Fraction(1, 17)}
DURACION = {"A": 1, "B": 3}


def huella(ruta):
    return hashlib.sha256(ruta.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def fraccion(numero):
    return [numero.numerator, numero.denominator]


def techo(numero):
    return -(-numero.numerator // numero.denominator)


def verificar_modelo(tipos, altura, eta, reserva):
    presupuesto = Fraction(altura)
    fronteras, defectos, total = [], [], 0
    for tipo in tipos:
        duracion = DURACION[tipo]
        defecto = presupuesto - duracion
        assert duracion > 0 and duracion <= presupuesto
        assert defecto >= eta * presupuesto + reserva
        fronteras.append(presupuesto)
        defectos.append(defecto)
        total += duracion
        presupuesto += GAMMA[tipo] * duracion
    # Dos formas independientes: recurrencia hacia atrás y productos hacia delante.
    coeficientes = [Fraction(0)] * (len(tipos) + 1)
    for i in range(len(tipos) - 1, -1, -1):
        coeficientes[i] = 1 + (1 + GAMMA[tipos[i]]) * coeficientes[i + 1]
    producto, suma = Fraction(1), Fraction(0)
    for tipo in tipos:
        suma += producto
        producto *= 1 + GAMMA[tipo]
    assert suma == coeficientes[0]
    descuento = sum(((1 + GAMMA[tipo] * coeficientes[i + 1]) * defectos[i]
                     for i, tipo in enumerate(tipos)), Fraction(0))
    assert total + descuento == coeficientes[0] * altura
    assert descuento >= eta * coeficientes[0] * altura
    return fronteras, descuento, coeficientes[0], total


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--pares-max", type=int, required=True)
    analizador.add_argument("--ventana-max", type=int, required=True)
    analizador.add_argument("--periodos-max", type=int, required=True)
    analizador.add_argument("--traslados", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    assert 1 <= args.pares_max <= 128
    assert 1 <= args.ventana_max <= 12
    assert 1 <= args.periodos_max <= 128
    assert 1 <= args.traslados <= 4
    razon = Fraction(486, 289)
    modelos, ventanas, familias = 0, 0, []
    for eta in (Fraction(0), Fraction(1, 2), Fraction(99, 100), Fraction(999999, 1000000)):
        for reserva in (0, 1, 17, 1224):
            altura = techo(Fraction(reserva + 3) / (1 - eta))
            residuos = []
            for pares in range(args.pares_max + 1):
                tipos = "AB" * pares
                fronteras, descuento, coeficiente, total = verificar_modelo(tipos, altura, eta, reserva)
                assert total == 4 * pares
                cerrado = Fraction(44, 17) * (razon ** pares - 1) / (razon - 1)
                assert coeficiente == cerrado
                for j in range(pares):
                    assert fronteras[2 * j] == altura + Fraction(13 * j, 17)
                    assert fronteras[2 * j + 1] == altura + Fraction(13 * j + 10, 17)
                if pares:
                    residuo = Fraction(total) / (coeficiente * altura)
                    assert 1 - descuento / (coeficiente * altura) == residuo
                    assert residuo <= Fraction(17 * pares, 11 * altura) * razon ** (1 - pares)
                    residuos.append(fraccion(residuo))
                modelos += 1
            # Todas las ventanas cortas del último modelo, incluidos inicio B y extremos.
            for inicio in range(len(tipos)):
                for largo in range(1, min(args.ventana_max, len(tipos) - inicio) + 1):
                    verificar_modelo(tipos[inicio:inicio + largo], fronteras[inicio], eta, reserva)
                    ventanas += 1
            familias.append(dict(eta=fraccion(eta), reserva=reserva, altura=altura,
                                  fracciones_residuales=residuos))
    orbitas, extremos = 0, []
    for pares in range(args.periodos_max + 1):
        palabra = "AB" * pares
        minimo, modulo = minimo_afin(palabra)
        assert (minimo, modulo) == minimo_por_bits(palabra)
        assert modulo == 16 ** pares
        assert minimo == ((-19 * pow(11, -1, modulo)) % modulo or modulo)
        for traslado in range(args.traslados):
            n = minimo + traslado * modulo
            final = recorrer(n, palabra)
            assert 16 ** pares * (11 * final + 19) == 27 ** pares * (11 * n + 19)
            assert (11 * n + 19) % (16 ** pares) == 0
            assert 16 ** pares <= 11 * n + 19
            altura = (n + 4).bit_length()
            assert 4 * pares <= altura + 3
            if traslado == 0:
                extremos.append(dict(pares=pares, n_hex=hex(n), ell=altura, largo=4 * pares))
            orbitas += 1
    # El modelo con pérdida del 99% y H=300 ya supera su propia barrera orbital.
    tipos, altura, eta = "AB" * 76, 300, Fraction(99, 100)
    _, _, _, total = verificar_modelo(tipos, altura, eta, 0)
    assert total == 304 and total > altura + 3
    minimo, modulo = minimo_por_bits(tipos)
    assert (minimo, modulo) == minimo_afin(tipos)
    assert (minimo + 4).bit_length() > altura
    resultado = dict(
        alcance="Contrastes finitos exactos. Los modelos no son orbitas; la barrera AB usa orbitas reales.",
        parametros={k: v for k, v in vars(args).items() if k != "salida"},
        modelos=modelos, ventanas=ventanas, familias=familias,
        orbitas=orbitas, extremos_orbitales=extremos,
        testigo_no_realizable=dict(eta=fraccion(eta), altura=altura, pares=76,
                                  largo=total, ell_minima=(minimo + 4).bit_length()),
        fuentes_sha256_lf={nombre: huella(CARPETA / nombre)
                           for nombre in (Path(__file__).name, "cotejar_congruencias.py")})
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK: {modelos} modelos, {ventanas} ventanas, {orbitas} orbitas y un testigo no realizable.")


if __name__ == "__main__":
    main()
