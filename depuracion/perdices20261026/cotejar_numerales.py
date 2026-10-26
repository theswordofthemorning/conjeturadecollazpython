"""Conversion de numerales, promedios afines y certificados lineales de factor uno."""

import argparse
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


REGLAS = (("ea", "ae"), ("fa", "be"), ("ga", "af"), ("eb", "bf"),
          ("fb", "ag"), ("gb", "bg"), ("ec", "bc"), ("fc", "aac"), ("gc", "bac"))


def binaria(n):
    assert n >= 1
    return "".join("ab"[int(x)] for x in bin(n)[3:][::-1]) + "c"


def ternaria(n):
    assert n >= 1
    cifras = []
    while n:
        n, cifra = divmod(n, 3)
        cifras.append(cifra)
    return "".join("efg"[x] for x in cifras[:-1]) + ("c" if cifras[-1] == 1 else "ac")


def convertir(palabra):
    pasos = []
    while True:
        for posicion in range(len(palabra) - 1):
            regla = next(((l, r) for l, r in REGLAS if palabra[posicion:posicion + 2] == l), None)
            if regla:
                nueva = palabra[:posicion] + regla[1] + palabra[posicion + 2:]
                pasos.append((palabra, nueva))
                palabra = nueva
                break
        else:
            assert set(palabra) <= set("abc") and palabra.endswith("c")
            return palabra, pasos
        assert len(pasos) < 100000


def aplicar(simbolo, punto):
    matriz, vector = simbolo
    return [sum(matriz[i][j] * punto[j] for j in range(2)) + vector[i] for i in range(2)]


def evaluar(palabra, simbolos, punto=(0, 0)):
    valor = list(punto)
    for letra in reversed(palabra):
        valor = aplicar(simbolos[letra], valor)
    return valor


def comprobar_estaticas(simbolos):
    for l, r in REGLAS:
        l0, r0 = evaluar(l, simbolos), evaluar(r, simbolos)
        assert all(x >= y for x, y in zip(l0, r0))
        for punto in ((1, 0), (0, 1)):
            lv, rv = evaluar(l, simbolos, punto), evaluar(r, simbolos, punto)
            assert all(lv[i] - l0[i] >= rv[i] - r0[i] for i in range(2))


def identidad_borde(nombre):
    letras = "abcefg"
    variables = [s + str(i) for s in letras for i in range(2)]
    cero = [0] * len(variables)
    unidad = lambda nombre: [int(x == nombre) for x in variables]
    if nombre == "imagen":
        a, b = [[1, 0], [1, 0]], [[0, 1], [0, 1]]
        matrices = dict(a=a, b=b, c=[[0, 0], [0, 0]], d=[[1, 0], [0, 0]],
                        e=a, f=[[1, 0], [0, 1]], g=b)
    else:
        a, b = [[1, 1], [0, 0]], [[0, 0], [1, 1]]
        matrices = dict(a=a, b=b, c=[[0, 0], [0, 0]], d=[[1, 1], [0, 0]],
                        e=[[1, 0], [0, 1]], f=[[0, 1], [1, 0]], g=[[1, 0], [0, 1]])

    def coeficientes(palabra):
        valor = [cero[:], cero[:]]
        for s in reversed(palabra):
            vector = [unidad(s + str(i)) if s in letras else cero for i in range(2)]
            valor = [[sum(matrices[s][i][j] * valor[j][k] for j in range(2)) + vector[i][k]
                      for k in range(len(variables))] for i in range(2)]
        return valor

    def diferencia(l, r, i):
        return [x - y for x, y in zip(coeficientes(l)[i], coeficientes(r)[i])]

    if nombre == "imagen":
        sumandos = [diferencia("fb", "ag", 1), diferencia("eb", "bf", 1),
                    diferencia("gc", "bac", 0), diferencia("ec", "bc", 1),
                    [2 * x for x in diferencia("dbaa", "dabe", 0)]]
        esperado = [-x for x in unidad("b1")]
    else:
        sumandos = [diferencia(l, r, i) for l, r in (("ec", "bc"), ("fc", "aac"))
                    for i in range(2)]
        sumandos += [diferencia("dbaa", "dabe", 0), diferencia("dbba", "dbaf", 0)]
        esperado = [-x - y for x, y in zip(unidad("a0"), unidad("a1"))]
    total = [sum(s[k] for s in sumandos) for k in range(len(variables))]
    assert total == esperado
    # Evaluacion numerica independiente en cero y en las doce bases constantes.
    for activada in [None] + variables:
        simbolos = {s: (m, [int(activada == s + str(i)) for i in range(2)])
                    for s, m in matrices.items()}
        for palabra in ("fb", "ag", "eb", "bf", "gc", "bac", "ec", "bc",
                        "fc", "aac", "dbaa", "dabe", "dbba", "dbaf"):
            literal = evaluar(palabra, simbolos)
            formal = coeficientes(palabra)
            assert literal == [0 if activada is None else formal[i][variables.index(activada)]
                               for i in range(2)]
    return dict(variables=variables, suma_coeficientes=total, bases_cotejadas=13)


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--control", type=Path, required=True)
    analizador.add_argument("--maximo", type=int, required=True)
    analizador.add_argument("--altura-promedio", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    assert 1 <= args.maximo <= 4095 and 0 <= args.altura_promedio <= 10
    control = json.loads(args.control.read_text(encoding="utf-8"))
    modelos = []
    for etapa in control["etapas"]:
        modelos.append({s: (d["matriz"], d["vector"])
                        for s, d in etapa["certificado"]["simbolos"].items()})
    modelos.append(dict(a=([[2, 0], [0, 2]], [0, 0]), b=([[2, 0], [0, 2]], [1, 1]),
                        c=([[0, 0], [0, 0]], [1, 1]), e=([[3, 0], [0, 3]], [0, 0]),
                        f=([[3, 0], [0, 3]], [1, 1]), g=([[3, 0], [0, 3]], [2, 2])))
    for modelo in modelos:
        comprobar_estaticas(modelo)
    pasos = 0
    maximos_pasos = 0
    comparaciones = 0
    for n in range(1, args.maximo + 1):
        inicial = ternaria(n)
        final, cambios = convertir(inicial)
        assert final == binaria(n)
        assert evaluar(inicial, modelos[-1]) == evaluar(final, modelos[-1]) == [n, n]
        pasos += len(cambios)
        maximos_pasos = max(maximos_pasos, len(cambios))
        for modelo in modelos:
            for antes, despues in cambios:
                assert all(x >= y for x, y in zip(evaluar(antes, modelo), evaluar(despues, modelo)))
                comparaciones += 1
            assert all(x >= y for x, y in zip(evaluar(inicial, modelo), evaluar(final, modelo)))
    promedios = 0
    palabras = 0
    for modelo in modelos:
        puntos = [modelo["c"][1]]
        promedio = [Fraction(x) for x in puntos[0]]
        matriz = [[Fraction(modelo["a"][0][i][j] + modelo["b"][0][i][j], 2)
                   for j in range(2)] for i in range(2)]
        vector = [Fraction(modelo["a"][1][i] + modelo["b"][1][i], 2) for i in range(2)]
        for h in range(args.altura_promedio + 1):
            esperado = [Fraction(sum(x[i] for x in puntos), len(puntos)) for i in range(2)]
            assert promedio == esperado and len(puntos) == 2 ** h
            palabras += len(puntos)
            promedios += 1
            puntos = [aplicar(modelo[s], punto) for punto in puntos for s in "ab"]
            promedio = aplicar((matriz, vector), promedio)
    for k in range(1, 33):
        assert 2 ** (5 * k + 1) <= 3 ** (4 * k)
    resultado = dict(
        estado="correcto", fuente_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        control_sha256=sha256(args.control.read_bytes()).hexdigest(), maximo=args.maximo,
        altura_promedio=args.altura_promedio, modelos=len(modelos), conversiones=args.maximo,
        pasos_reescritura=pasos, maximo_pasos=maximos_pasos, comparaciones_en_contexto=comparaciones,
        promedios_exactos=promedios, palabras_en_promedios=palabras,
        identidades_borde={nombre: identidad_borde(nombre) for nombre in ("imagen", "nucleo")},
        alcance="Conversion y promedios cotejados finitamente con enteros y Fraction. "
                "Dos identidades lineales exactas por coeficientes. No se interpreta "
                "el promedio como una ley orbital ni se demuestra terminacion H.")
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
