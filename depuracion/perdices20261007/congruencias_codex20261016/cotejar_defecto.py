"""Familias con prefijo prescrito y defecto interior fijo; calculo exacto."""

import argparse
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path

from cotejar_congruencias import minimo_afin, minimo_por_bits, pasos, recorrer


CARPETA = Path(__file__).resolve().parent


def huella(ruta):
    return hashlib.sha256(ruta.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def afin(palabra):
    denominador, factor, aporte = 1, 1, 0
    for letra in palabra:
        base, impar, suma = (2, 3, 1) if letra == "A" else (8, 9, 5)
        aporte = impar * aporte + suma * denominador
        denominador *= base
        factor *= impar
    return denominador, factor, aporte


def logaritmo_modular(objetivo, exponente):
    """Levanta el exponente de 2 un digito ternario por vez; sin flotantes."""
    assert exponente >= 1 and objetivo % 3
    elegido = 0 if objetivo % 3 == 1 else 1
    modulo, periodo = 3, 2
    for _ in range(1, exponente):
        modulo *= 3
        candidatos = [elegido + t * periodo for t in range(3)
                      if pow(2, elegido + t * periodo, modulo) == objetivo % modulo]
        assert len(candidatos) == 1
        elegido = candidatos[0]
        periodo *= 3
    assert 0 <= elegido < periodo
    assert pow(2, elegido, modulo) == objetivo % modulo
    return elegido, periodo


def inversa_literal(final, palabra):
    actual = final
    for bit in reversed(pasos(palabra)):
        if bit:
            actual, resto = divmod(2 * actual - 1, 3)
            assert resto == 0 and actual % 2 == 1
        else:
            actual *= 2
        assert actual > 0
    return actual


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--prefijos-max", type=int, required=True)
    analizador.add_argument("--miembros", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    assert 1 <= args.prefijos_max <= 4
    assert 1 <= args.miembros <= 3
    prefijos = ["".join(letras) + "B"
                for longitud in range(args.prefijos_max)
                for letras in itertools.product("AB", repeat=longitud)]
    # Seis rachas: el fenomeno no depende de tener pocos cambios previos.
    prefijos.append("ABABAB")
    resultados, total, conteo_bordes = [], 0, 0
    for k in range(13):
        entrada = (1 << (k + 2)) - 1
        final = recorrer(entrada, "A" * k + "B")
        assert 2 * final + 1 == 3 ** (k + 2)
        assert minimo_afin("A" * k + "B") == minimo_por_bits("A" * k + "B")
        conteo_bordes += 1
    for palabra in prefijos:
        longitud, impares = len(pasos(palabra)), sum(pasos(palabra))
        denominador, factor, aporte = afin(palabra)
        assert denominador == 2 ** longitud and factor == 3 ** impares
        assert factor - denominador <= aporte <= 5 * (factor - denominador)
        objetivo = denominador + aporte
        correccion = 5 * factor - objetivo
        assert 4 * denominador <= correccion <= 4 * factor
        assert objetivo % 3 != 0
        exponente, periodo = logaritmo_modular(objetivo, impares)
        # Contraste independiente: ciclo modular completo, sin levantamiento.
        potencia, encontrados = 1, []
        for j in range(periodo):
            if potencia == objetivo % factor:
                encontrados.append(j)
            potencia = 2 * potencia % factor
        assert encontrados == [exponente] and potencia == 1
        piso = factor.bit_length() - 1
        residuo = (exponente - longitud - 2) % periodo
        minimo = max(1, piso + correccion.bit_length() - longitud - 2)
        primero = residuo + max(0, (minimo - residuo + periodo - 1) // periodo) * periodo
        casos = []
        # Bordes: cada k pequeno admisible, sin exigir la altura eventual.
        for k in range(13):
            numerador = (1 << (longitud + k + 2)) - objetivo
            if numerador > 0 and numerador % factor == 0:
                n = numerador // factor
                assert recorrer(n, palabra) == (1 << (k + 2)) - 1
                recorrer(n, palabra + "A" * k + "B")
                conteo_bordes += 1
        for indice in range(args.miembros):
            k = primero + indice * periodo
            n, resto = divmod((1 << (longitud + k + 2)) - objetivo, factor)
            assert resto == 0 and n > 0 and k >= 1
            altura = (n + 4).bit_length()
            assert altura == longitud + k + 2 - piso
            assert correccion <= (1 << altura) * (factor - (1 << piso))
            entrada = (1 << (k + 2)) - 1
            assert inversa_literal(entrada, palabra) == n
            assert recorrer(n, palabra) == entrada
            # La cola se comprueba paso a paso y por su formula independiente.
            salida_a = recorrer(entrada, "A" * k)
            assert salida_a + 1 == 4 * 3 ** k
            final = recorrer(salida_a, "B")
            assert 2 * final + 1 == 3 ** (k + 2)
            minimo_a, modulo = minimo_afin(palabra + "A" * k + "B")
            assert (minimo_a, modulo) == minimo_por_bits(palabra + "A" * k + "B")
            assert n == minimo_a  # La familia tambien da el minimo de su cilindro.
            presupuesto = Fraction(altura) + Fraction(27, 17) * impares - longitud
            defecto = presupuesto - k
            assert defecto == 2 + Fraction(27, 17) * impares - piso
            assert longitud + k + 3 - altura == piso + 1
            # Forma multiplicativa exacta del defecto con logaritmos reales:
            # 2^(delta_exacta - 2) = 1 + correccion/2^(P+k+2).
            razon = Fraction(factor * (n + 5), 1 << (longitud + k + 2))
            assert razon == 1 + Fraction(correccion, 1 << (longitud + k + 2))
            assert razon > 1
            assert defecto > 0 and defecto / presupuesto < 1
            casos.append(dict(k=k, ell=altura, exceso=piso + 1,
                              defecto=[defecto.numerator, defecto.denominator],
                              defecto_relativo=[(defecto / presupuesto).numerator,
                                                (defecto / presupuesto).denominator],
                              semilla_hex_sha256=hashlib.sha256(hex(n).encode()).hexdigest(),
                              semilla_decimal=str(n) if n.bit_length() < 128 else None))
            total += 1
        assert all(Fraction(*a["defecto_relativo"]) > Fraction(*b["defecto_relativo"])
                   for a, b in zip(casos, casos[1:]))
        resultados.append(dict(prefijo=palabra, pasos=longitud, impares=impares,
                               periodo=periodo, residuo_k=residuo, miembros=casos))
    resultado = dict(parametros={k: v for k, v in vars(args).items() if k != "salida"},
                     prefijos=len(prefijos), familias=resultados, casos=total,
                     bordes=conteo_bordes, bordes_cola_sin_prefijo=13,
                     fuentes_sha256_lf={nombre: huella(CARPETA / nombre) for nombre in
                                       (Path(__file__).name, "cotejar_congruencias.py")},
                     alcance="Cotejo finito de una familia con prueba escrita universal. "
                             "No verifica un reloj uniforme ni una perdida conjunta.")
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK: {len(prefijos)} prefijos, {total} miembros, {conteo_bordes} bordes.")


if __name__ == "__main__":
    main()
