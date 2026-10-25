"""Construye retornos enteros A/B con la misma firma aritmetica y mayor valor."""

import argparse
from fractions import Fraction
from hashlib import sha256
import json
from math import gcd, lcm
from pathlib import Path


def T(n):
    return (3 * n + 1) // 2 if n % 2 else n // 2


def valorar(n, primo):
    n = abs(n)
    assert n != 0
    valor = 0
    while n % primo == 0:
        valor += 1
        n //= primo
    return valor


def valorar_racional(x, primo):
    return valorar(x.numerator, primo) - valorar(x.denominator, primo)


def polinomio(coeficientes, x):
    resultado = 0
    for coeficiente in reversed(coeficientes):
        resultado = resultado * x + coeficiente
    return resultado


def totiente(n):
    resultado, resto, divisor = n, n, 2
    while divisor * divisor <= resto:
        if resto % divisor == 0:
            resultado -= resultado // divisor
            while resto % divisor == 0:
                resto //= divisor
        divisor += 1
    if resto > 1:
        resultado -= resultado // resto
    return resultado


def combinar(a, modulo_a, b, modulo_b):
    if modulo_b == 1:
        return a, modulo_a
    assert gcd(modulo_a, modulo_b) == 1
    nuevo = a + modulo_a * ((b - a) * pow(modulo_a, -1, modulo_b) % modulo_b)
    return nuevo, modulo_a * modulo_b


def firma(n, modulo, observaciones):
    return [n % modulo] + [valorar(polinomio(coeficientes, n), primo)
                           for primo, coeficientes in observaciones]


def construir(modulo, observaciones, lote):
    grados = sum(len(coeficientes) - 1 for _, coeficientes in observaciones)
    for b in range(1, grados + 2):
        N, D = 2 * 8 ** b, 3 * 9 ** b
        E = 11 * 9 ** b - 10 * 8 ** b
        fijo = -Fraction(E, D - N)
        if all(polinomio(c, fijo) != 0 for _, c in observaciones):
            break
    else:
        raise AssertionError("Se agotaron mas puntos distintos que raices posibles")
    assert gcd(fijo.denominator, 6) == 1
    assert N * fijo == D * fijo + E
    auxiliar = next(n for n in range(1, grados + 2)
                   if all(polinomio(c, n) != 0 for _, c in observaciones))
    parte, niveles = modulo, {2: 1, 3: 0}
    for primo in (2, 3):
        exponente = 0
        while parte % primo == 0:
            parte //= primo
            exponente += 1
        niveles[primo] = max(niveles[primo], exponente)
    for primo, coeficientes in observaciones:
        if primo in (2, 3):
            valor = valorar_racional(polinomio(coeficientes, fijo), primo)
            assert valor >= 0
            niveles[primo] = max(niveles[primo], valor + 1)
        else:
            valor = valorar(polinomio(coeficientes, auxiliar), primo)
            parte = lcm(parte, primo ** (valor + 1))
    repeticiones = lote * parte * totiente(parte)
    longitud = (1 + 3 * b) * repeticiones
    modulo_dos, modulo_tres = 2 ** (longitud + niveles[2]), 3 ** niveles[3]
    residuo = fijo.numerator * pow(fijo.denominator, -1, modulo_dos) % modulo_dos
    semilla, periodo = combinar(residuo, modulo_dos,
                               fijo.numerator * pow(fijo.denominator, -1, modulo_tres) % modulo_tres,
                               modulo_tres)
    semilla, periodo = combinar(semilla, periodo, auxiliar % parte, parte)
    assert semilla > 0
    # Cotejo independiente de la identidad de la permutacion en los modulos ensayados.
    assert parte <= 1000
    for residuo in range(parte):
        y = residuo
        for _ in range(repeticiones):
            y = (D * y + E) * pow(N, -1, parte) % parte
        assert y == residuo
    return dict(b=b, N=N, D=D, E=E, fijo=fijo, auxiliar=auxiliar,
                repeticiones=repeticiones, longitud=longitud, semilla=semilla,
                periodo=periodo, niveles=niveles, parte_coprima=parte, lote=lote)


def revisar(caso, traslado):
    datos = construir(caso["modulo"], caso["observaciones"], caso["lote"])
    n = datos["semilla"] + traslado * datos["periodo"]
    palabra = ("A" + "B" * datos["b"]) * datos["repeticiones"]
    bits = [int(bit) for bloque in palabra for bit in ("1" if bloque == "A" else "110")]
    x, pasos = n, 0
    for bloque in palabra:
        assert x > 0 and x % 2 == 1
        for bit in ("1" if bloque == "A" else "110"):
            assert x % 2 == int(bit)
            x = T(x)
            pasos += 1
        assert x % 2 == 1
    assert pasos == len(bits) == datos["longitud"]
    assert len(palabra) % caso["lote"] == 0
    D, N, E, t = datos["D"], datos["N"], datos["E"], datos["repeticiones"]
    cociente, resto = divmod(D ** t - N ** t, D - N)
    assert resto == 0
    assert N ** t * x == D ** t * n + E * cociente
    inicial = firma(n, caso["modulo"], caso["observaciones"])
    assert inicial == firma(x, caso["modulo"], caso["observaciones"])
    assert x > n
    return dict(caso=caso["nombre"], modulo=caso["modulo"], lote=caso["lote"], traslado=traslado,
                observaciones=caso["observaciones"], b=datos["b"], repeticiones=t,
                fijo=str(datos["fijo"]), parte_coprima=datos["parte_coprima"],
                semilla=str(n), final=str(x), pasos_T=pasos, bloques=len(palabra), firma=inicial)


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--traslados", type=int, required=True)
    analizador.add_argument("--lote", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    assert 1 <= args.traslados <= 8 and 1 <= args.lote <= 16
    basicas = [(2, [1, 1]), (2, [5, 1])]
    ternarias = basicas + [(3, [1, 1]), (3, [5, 1])]
    extendidas = ternarias + [(2, [19, 11]), (5, [1, 1]), (2, [1, 0, 1])]
    casos = [dict(nombre="dos_valoraciones", modulo=1, observaciones=basicas),
             dict(nombre="residuos_y_ternarias", modulo=72, observaciones=ternarias),
             dict(nombre="raiz_a_evitar_y_primo_del_denominador", modulo=360, observaciones=extendidas)]
    resultados = []
    for caso in casos:
        for lote in sorted({1, args.lote}):
            for traslado in range(args.traslados):
                resultados.append(revisar(dict(caso, lote=lote), traslado))
    assert resultados[0]["semilla"] == "231" and resultados[0]["final"] == "391"
    assert any(r["b"] == 2 and r["parte_coprima"] == 5 for r in resultados)
    resultado = dict(
        alcance="Construcciones finitas exactas; la generalizacion CRT tiene prueba escrita. "
                "No prueba terminacion ni refuta el reloj AB.",
        recorridos=resultados, pasos_contrastados=sum(r["pasos_T"] for r in resultados),
        fuente_sha256=sha256(Path(__file__).read_bytes()).hexdigest())
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(estado="correcto", recorridos=len(resultados),
                          pasos=resultado["pasos_contrastados"])))


if __name__ == "__main__":
    main()
