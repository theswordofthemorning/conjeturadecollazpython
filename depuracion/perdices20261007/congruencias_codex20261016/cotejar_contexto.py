"""Racha de parte impar 13 entre contextos prescritos; aritmetica exacta."""

import argparse
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path

from cotejar_congruencias import minimo_afin, minimo_por_bits, pasos, recorrer
from cotejar_defecto import afin, huella, inversa_literal, logaritmo_modular


CARPETA = Path(__file__).resolve().parent


def logaritmo_binario(objetivo, bits):
    """3 genera las unidades 1 o 3 mod 8; aqui se exige la rama impar."""
    assert bits >= 3 and objetivo % 8 == 3
    elegido, periodo = 1, 2
    for j in range(3, bits):
        modulo = 1 << (j + 1)
        candidatos = [elegido + t * periodo for t in (0, 1)
                      if pow(3, elegido + t * periodo, modulo) == objetivo % modulo]
        assert len(candidatos) == 1
        elegido = candidatos[0]
        periodo *= 2
    assert pow(3, elegido, 1 << bits) == objetivo % (1 << bits)
    return elegido, periodo


def combinar(residuo_tres, periodo_tres, residuo_dos, periodo_dos):
    assert residuo_tres % 2 == residuo_dos % 2 == 1
    # Tras dividir la diferencia y los periodos por 2, son coprimos.
    impar, potencia = periodo_tres // 2, periodo_dos // 2
    ajuste = (((residuo_dos - residuo_tres) // 2) * pow(impar, -1, potencia)) % potencia
    periodo = periodo_tres * potencia
    residuo = (residuo_tres + periodo_tres * ajuste) % periodo
    assert residuo % periodo_tres == residuo_tres
    assert residuo % periodo_dos == residuo_dos
    return residuo, periodo


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--prefijos-max", type=int, required=True)
    analizador.add_argument("--sufijos-max", type=int, required=True)
    analizador.add_argument("--miembros", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    assert 1 <= args.prefijos_max <= 3
    assert 0 <= args.sufijos_max <= 3
    assert 2 <= args.miembros <= 3
    prefijos = ["".join(p) + "B" for j in range(args.prefijos_max)
                for p in itertools.product("AB", repeat=j)]
    sufijos = ["".join(p) for j in range(args.sufijos_max + 1)
               for p in itertools.product("AB", repeat=j)]
    familias, total = [], 0
    for u, v in itertools.product(prefijos, sufijos):
        nbase, factor, aporte = afin(u)
        p, s = len(pasos(u)), sum(pasos(u))
        r = nbase + aporte
        correccion = 5 * factor - r
        objetivo_tres = r * pow(13, -1, factor) % factor
        exponente, periodo_tres = logaritmo_modular(objetivo_tres, s)
        residuo_tres = (exponente - p - 2) % periodo_tres
        cola = "BAA" + v
        minimo, modulo = minimo_afin(cola)
        assert (minimo, modulo) == minimo_por_bits(cola)
        assert minimo % 32 == 27
        bits = len(pasos(cola)) - 2
        objetivo_dos = ((minimo + 1) // 4) * pow(13, -1, 1 << bits) % (1 << bits)
        residuo_dos, periodo_dos = logaritmo_binario(objetivo_dos, bits)
        # Contraste independiente de ambos levantamientos por ciclos completos.
        assert [e for e in range(periodo_tres)
                if pow(2, e, factor) == objetivo_tres] == [exponente]
        assert [e for e in range(periodo_dos)
                if pow(3, e, 1 << bits) == objetivo_dos] == [residuo_dos]
        residuo, periodo = combinar(residuo_tres, periodo_tres, residuo_dos, periodo_dos)
        d = (16 * factor // 13).bit_length() - 1
        assert 13 * 2 ** d < 16 * factor < 13 * 2 ** (d + 1)
        umbral = max(1, d + (16 * correccion).bit_length() - p - 6)
        primero = residuo + max(0, (umbral - residuo + periodo - 1) // periodo) * periodo
        miembros = []
        for indice in range(args.miembros):
            a = primero + indice * periodo
            n, resto = divmod(13 * 2 ** (p + a + 2) - r, factor)
            assert resto == 0 and n > 0 and a % 2 == 1
            x = 13 * 2 ** (a + 2) - 1
            assert recorrer(n, u) == x and inversa_literal(x, u) == n
            z = recorrer(x, "A" * a)
            assert z + 1 == 52 * 3 ** a and z % modulo == minimo % modulo
            final = recorrer(z, cola)
            palabra = u + "A" * a + cola
            minimo_total, modulo_total = minimo_afin(palabra)
            assert (minimo_total, modulo_total) == minimo_por_bits(palabra)
            assert n % modulo_total == minimo_total % modulo_total
            assert n == minimo_total
            altura = (n + 4).bit_length()
            assert altura == p + a + 6 - d
            assert 16 * factor * (n + 5) == 13 * 2 ** (altura + d) + 16 * correccion
            assert 16 * correccion <= 2 ** altura * (16 * factor - 13 * 2 ** d)
            presupuesto = Fraction(altura) + Fraction(27, 17) * s - p
            defecto = presupuesto - a
            assert defecto == 6 - d + Fraction(27, 17) * s > 0
            largo = len(pasos(palabra))
            assert largo - altura == len(pasos(v)) + d - 1
            razon = Fraction(factor * (n + 5), 13 * 2 ** (p + a + 2))
            assert razon == 1 + Fraction(correccion, 13 * 2 ** (p + a + 2))
            miembros.append(dict(a=a, ell=altura, largo=largo,
                                  defecto=[defecto.numerator, defecto.denominator],
                                  proporcion=[(defecto / presupuesto).numerator,
                                              (defecto / presupuesto).denominator],
                                  semilla_sha256=hashlib.sha256(hex(n).encode()).hexdigest(),
                                  final_sha256=hashlib.sha256(hex(final).encode()).hexdigest(),
                                  semilla_decimal=str(n) if n.bit_length() < 128 else None))
            total += 1
        assert all(Fraction(*c["proporcion"]) > Fraction(*e["proporcion"])
                   for c, e in zip(miembros, miembros[1:]))
        familias.append(dict(prefijo=u, sufijo=v, residuo=residuo, periodo=periodo,
                              d=d, pasos_prefijo=p, impares_prefijo=s, miembros=miembros))
    # Bordes de la familia anterior: parte impar 1, k par y k impar.
    for k in range(21):
        z = 4 * 3 ** k - 1
        y = recorrer(z, "B")
        assert 2 * y + 1 == 3 ** (k + 2)
        if k % 2 == 0:
            assert y % 2 == 0
        else:
            assert y % 4 == 1 and recorrer(y, "A") % 2 == 0
    resultado = dict(parametros={k: v for k, v in vars(args).items() if k != "salida"},
                     familias=familias, casos=total, contextos=len(familias), bordes=21,
                     fuentes_sha256_lf={nombre: huella(CARPETA / nombre) for nombre in
                                       (Path(__file__).name, "cotejar_defecto.py", "cotejar_congruencias.py")},
                     alcance="Cotejo finito; existencia universal por prueba escrita con dos levantamientos y CRT. "
                             "No acota conjuntamente los defectos ni demuestra reloj uniforme.")
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK: {len(familias)} contextos, {total} miembros y 21 bordes.")


if __name__ == "__main__":
    main()
