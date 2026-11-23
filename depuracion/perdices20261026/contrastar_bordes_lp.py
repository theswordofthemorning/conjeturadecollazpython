"""Contraste independiente de los bordes de factor uno de CONSTANTES_F_INVERTIBLE §5.

Para cada borde se fijan las matrices de la nota y la primera fila r de M_d.
Las incógnitas son las doce coordenadas de v_a,v_b,v_c,v_e,v_f,v_g, reales y
no negativas. Restricciones: las nueve estáticas sobre constantes, coordenada
a coordenada, y las tres dinámicas débiles en la coordenada 0. La segunda fila
de M_d se omite: sólo añadiría restricciones, de modo que omitirla es prudente.
Con un símplex exacto (Fraction, regla de Bland) se maximiza cada descenso
bajo la normalización suma <= 1. Máximo 0 equivale a descenso nulo en todo el
cono, porque las restricciones son homogéneas.
"""

import argparse
from fractions import Fraction
import json
from pathlib import Path


LETRAS = "abcefg"
ESTATICAS = [("ea", "ae"), ("fa", "be"), ("ga", "af"), ("eb", "bf"), ("fb", "ag"),
             ("gb", "bg"), ("ec", "bc"), ("fc", "aac"), ("gc", "bac")]
DINAMICAS = [("a", ""), ("baa", "abe"), ("bba", "baf")]


def producto(m, v):
    return [sum(m[i][j] * v[j] for j in range(2)) for i in range(2)]


def suma(u, v):
    return [[x + y for x, y in zip(fu, fv)] for fu, fv in zip(u, v)]


def constante(palabra, matrices):
    """Constante de la palabra como forma lineal: lista de 2 filas de 12 coeficientes."""
    nula = [[Fraction(0)] * 12 for _ in range(2)]
    resultado = nula
    for letra in reversed(palabra):
        m = matrices[letra]
        transformada = [[sum(m[i][j] * resultado[j][k] for j in range(2)) for k in range(12)]
                        for i in range(2)]
        propia = [[Fraction(0)] * 12 for _ in range(2)]
        indice = LETRAS.index(letra)
        propia[0][2 * indice] = Fraction(1)
        propia[1][2 * indice + 1] = Fraction(1)
        resultado = suma(transformada, propia)
    return resultado


def resta(u, v):
    return [[x - y for x, y in zip(fu, fv)] for fu, fv in zip(u, v)]


def maximizar(objetivo, desigualdades):
    """max objetivo·x con desigualdades·x <= 0, sum x <= 1, x >= 0; símplex exacto de Bland."""
    filas = [list(d) + [Fraction(0)] for d in desigualdades]
    filas.append([Fraction(1)] * 12 + [Fraction(1)])
    m, n = len(filas), 12
    tabla = []
    for i, fila in enumerate(filas):
        holguras = [Fraction(1) if j == i else Fraction(0) for j in range(m)]
        tabla.append(fila[:n] + holguras + [fila[n]])
    coste = [-c for c in objetivo] + [Fraction(0)] * m + [Fraction(0)]
    base = [n + i for i in range(m)]
    while True:
        entrante = next((j for j in range(n + m) if coste[j] < 0), None)
        if entrante is None:
            return coste[-1]
        candidatos = [(tabla[i][-1] / tabla[i][entrante], base[i], i)
                      for i in range(m) if tabla[i][entrante] > 0]
        assert candidatos, "no acotado"
        _, _, saliente = min(candidatos)
        pivote = tabla[saliente][entrante]
        tabla[saliente] = [x / pivote for x in tabla[saliente]]
        for i in range(m):
            if i != saliente and tabla[i][entrante] != 0:
                factor = tabla[i][entrante]
                tabla[i] = [x - factor * y for x, y in zip(tabla[i], tabla[saliente])]
        factor = coste[entrante]
        coste = [x - factor * y for x, y in zip(coste, tabla[saliente])]
        base[saliente] = entrante


def matriz(filas):
    return [[Fraction(x) for x in fila] for fila in filas]


BORDES = {
    "imagen_comun_lambda_1": dict(
        matrices=dict(a=matriz([[1, 0], [1, 0]]), e=matriz([[1, 0], [1, 0]]),
                      b=matriz([[0, 1], [0, 1]]), g=matriz([[0, 1], [0, 1]]),
                      f=matriz([[1, 0], [0, 1]]), c=matriz([[0, 0], [0, 0]])),
        fila_d=[Fraction(1), Fraction(0)]),
    "nucleo_comun_lambda_1": dict(
        matrices=dict(a=matriz([[1, 1], [0, 0]]), b=matriz([[0, 0], [1, 1]]),
                      e=matriz([[1, 0], [0, 1]]), g=matriz([[1, 0], [0, 1]]),
                      f=matriz([[0, 1], [1, 0]]), c=matriz([[0, 0], [0, 0]])),
        fila_d=[Fraction(1), Fraction(1)]),
}


def comprobar_matrices(matrices, fila_d):
    """Partes matriciales: estáticas débiles y filas r de las dinámicas."""
    def mat(palabra):
        resultado = matriz([[1, 0], [0, 1]])
        for letra in palabra:
            m = matrices[letra]
            resultado = [[sum(resultado[i][k] * m[k][j] for k in range(2)) for j in range(2)]
                         for i in range(2)]
        return resultado
    for izquierda, derecha in ESTATICAS:
        if "c" in izquierda:
            continue
        mi, md = mat(izquierda), mat(derecha)
        assert all(mi[i][j] >= md[i][j] for i in range(2) for j in range(2)), izquierda
    for izquierda, derecha in DINAMICAS:
        ri = [sum(fila_d[k] * mat(izquierda)[k][j] for k in range(2)) for j in range(2)]
        rd = [sum(fila_d[k] * mat(derecha)[k][j] for k in range(2)) for j in range(2)]
        assert all(x >= y for x, y in zip(ri, rd)), izquierda


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    resultado = {}
    for nombre, borde in BORDES.items():
        matrices, fila_d = borde["matrices"], borde["fila_d"]
        comprobar_matrices(matrices, fila_d)
        desigualdades = []
        for izquierda, derecha in ESTATICAS:
            diferencia = resta(constante(izquierda, matrices), constante(derecha, matrices))
            desigualdades += [[-x for x in diferencia[i]] for i in range(2)]
        descensos = []
        for izquierda, derecha in DINAMICAS:
            diferencia = resta(constante(izquierda, matrices), constante(derecha, matrices))
            descensos.append([fila_d[0] * x + fila_d[1] * y
                              for x, y in zip(diferencia[0], diferencia[1])])
        desigualdades += [[-x for x in d] for d in descensos]
        maximos = [maximizar(d, desigualdades) for d in descensos]
        assert all(maximo == 0 for maximo in maximos), (nombre, maximos)
        # Control: sin las estáticas, algún descenso debe poder ser positivo.
        dinamicas = [[-x for x in d] for d in descensos]
        sin_estaticas = [maximizar(d, dinamicas) for d in descensos]
        assert max(sin_estaticas) > 0, (nombre, sin_estaticas)
        resultado[nombre] = dict(restricciones=len(desigualdades),
                                 maximos_descensos=[str(m) for m in maximos],
                                 control_sin_estaticas=[str(m) for m in sin_estaticas])
    datos = dict(estado="correcto", bordes=resultado,
                 alcance=("Los tres descensos dinamicos tienen maximo exacto 0 en ambos bordes, "
                          "sobre el cono real de constantes no negativas. Contraste independiente "
                          "de la prueba escrita de §5; no sustituye la reduccion a esas formas."))
    args.salida.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("OK:", {n: r["maximos_descensos"] for n, r in resultado.items()})


if __name__ == "__main__":
    main()
