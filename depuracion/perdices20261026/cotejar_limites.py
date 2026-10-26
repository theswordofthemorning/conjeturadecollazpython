"""Contrasta series reales A/B, cilindros binarios y ramas literales por separado."""

import argparse
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


def paso_literal(n):
    return (3 * n + 1) // 2 if n % 2 else n // 2


def codigo(q, bloques):
    actual = q
    palabra = []
    for _ in range(bloques):
        if actual <= 3:
            palabra.append("A")
            actual = (3 * actual - 1) / 2
        else:
            palabra.append("B")
            actual = (9 * actual - 5) / 8
        assert 1 <= actual <= 4
    return "".join(palabra)


def revisar(q, bloques):
    palabra = codigo(q, bloques)
    x = -q
    suma = Fraction(0)
    largo = subidas = aditivo = 0
    representantes = []
    digitos = "".join("1" if b == "A" else "110" for b in palabra)
    for indice, bit in enumerate(digitos):
        impar = int(bit)
        if impar:
            suma -= Fraction(2 ** indice, 3 ** (subidas + 1))
            aditivo = 3 * aditivo + 2 ** indice
            subidas += 1
            x = (3 * x + 1) / 2
        else:
            x /= 2
        largo += 1
        assert 3 * subidas >= 2 * largo
        assert suma == -q - Fraction(2 ** largo, 3 ** subidas) * x
        if q.denominator == 2:
            assert x.denominator == 2 ** (largo + 1)
        if q == 2:
            assert x.denominator == 2 ** largo
        modulo = 2 ** largo
        residuo = -aditivo * pow(3 ** subidas, -1, modulo) % modulo
        assert residuo == suma.numerator * pow(suma.denominator, -1, modulo) % modulo
        if representantes:
            assert residuo % (modulo // 2) == representantes[-1]
        representantes.append(residuo)
    inverso = Fraction(2 ** largo, 3 ** subidas)
    assert 1 <= -x <= 4
    assert 0 < inverso <= Fraction(8, 9) ** bloques
    assert 0 < suma + q <= 4 * Fraction(8, 9) ** bloques
    # El representante entero REAL satisface los bits; -q sigue ramas prescritas.
    n = representantes[-1]
    assert n > 0
    actual = n
    for bit in digitos:
        assert actual % 2 == int(bit)
        actual = paso_literal(actual)
    assert 2 ** largo * actual == 3 ** subidas * n + aditivo
    assert Fraction(aditivo, 3 ** subidas) == -suma
    return dict(q=str(q), bloques=bloques, pasos_T=largo, impares=subidas,
                palabra=palabra, primeros_residuos=representantes[:16],
                semilla_entera=str(n), salida_entera=str(actual),
                suma_parcial=str(suma), error_real=str(suma + q),
                cota_error=str(4 * Fraction(8, 9) ** bloques),
                salida_prescrita=str(x), denominador_prescrito=str(x.denominator))


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--bloques", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    assert 1 <= args.bloques <= 512
    casos = [Fraction(1), Fraction(3, 2), Fraction(2), Fraction(5, 2),
             Fraction(3), Fraction(7, 2), Fraction(4)]
    resultados = [revisar(q, k) for q in casos for k in sorted({1, 2, 3, args.bloques})]
    # Testigo de perdida de paridad: -2 es par, pero el codigo comienza por A.
    assert codigo(Fraction(2), 4).startswith("AA")
    assert paso_literal(-2) == -1
    assert (3 * Fraction(-2) + 1) / 2 == Fraction(-5, 2)
    datos = dict(alcance="Contraste finito exacto; no prueba racionalidad/irracionalidad "
                 "del limite 2-adico ni una orbita entera infinita.",
                 fuente_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                 recorridos=len(resultados), pasos_T=sum(r["pasos_T"] for r in resultados),
                 casos=resultados)
    args.salida.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK: {len(resultados)} recorridos; {datos['pasos_T']} pasos prescritos y enteros cotejados.")


if __name__ == "__main__":
    main()
