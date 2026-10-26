"""Primera eliminacion: matrices finitas y constantes naturales sin cota, QF_LIA."""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import time

import z3


INTERCAMBIOS = [("ea", "ae"), ("fa", "be"), ("ga", "af"),
                ("eb", "bf"), ("fb", "ag"), ("gb", "bg")]


def leer_reglas(ruta):
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    reglas = []
    for linea in datos["reglas_originales"].splitlines():
        estricta = " ->| " in linea
        izquierda, derecha = linea.split(" ->| " if estricta else " ->= ")
        reglas.append(dict(izquierda=izquierda[::-1], derecha=derecha[::-1], estricta=estricta))
    assert len(reglas) == 12 and sum(r["estricta"] for r in reglas) == 3
    assert {(r["izquierda"], r["derecha"]) for r in reglas if not r["estricta"]} == set(
        INTERCAMBIOS + [("ec", "bc"), ("fc", "aac"), ("gc", "bac")])
    assert all(r["izquierda"].startswith("d") and r["derecha"].startswith("d")
               for r in reglas if r["estricta"])
    return reglas


def evaluar(palabra, simbolos, punto):
    actual = list(punto)
    for letra in reversed(palabra):
        matriz, vector = simbolos[letra]
        actual = [sum(matriz[i][j] * actual[j] for j in range(2)) + vector[i] for i in range(2)]
    return actual


def verificar_modelo(reglas, simbolos):
    estrictas = []
    for k, regla in enumerate(reglas):
        l0 = evaluar(regla["izquierda"], simbolos, [0, 0])
        r0 = evaluar(regla["derecha"], simbolos, [0, 0])
        assert all(a >= b for a, b in zip(l0, r0))
        for j in range(2):
            punto = [int(i == j) for i in range(2)]
            ly = evaluar(regla["izquierda"], simbolos, punto)
            ry = evaluar(regla["derecha"], simbolos, punto)
            assert all(ly[i] - l0[i] >= ry[i] - r0[i] for i in range(2))
        if regla["estricta"] and l0[0] > r0[0]:
            estrictas.append(k)
    assert estrictas
    return estrictas


def codificar(reglas, cota_matrices, conexion_pedida, segundos):
    """Devuelve formula y variables para buscar o fijar un certificado de control."""
    assert 1 <= cota_matrices <= 3 and 1 <= segundos <= 60
    assert conexion_pedida in ("ambas", "libre")
    assert all(r["izquierda"].startswith("d") and r["derecha"].startswith("d")
               for r in reglas if r["estricta"])
    solver = z3.SolverFor("QF_LIA")
    solver.set(timeout=segundos * 1000, random_seed=0, threads=1)
    cero = z3.IntVal(0)
    simbolos = {}
    for letra in "abcdefg":
        matriz = [[z3.Int(f"m_{letra}_{i}_{j}") for j in range(2)] for i in range(2)]
        vector = [z3.Int(f"v_{letra}_{i}") for i in range(2)]
        # Sin perdida para una primera eliminacion: C solo aparece como sufijo;
        # D solo encabeza las dinamicas, cuya estrictitud usa la coordenada 0.
        if letra == "c":
            matriz = [[cero, cero], [cero, cero]]
        if letra == "d":
            matriz[1] = [cero, cero]
            vector = [cero, cero]
        simbolos[letra] = matriz, vector
        for fila in matriz:
            for x in fila:
                solver.add(x >= 0, x <= cota_matrices)
        for x in vector:
            solver.add(x >= 0)

    def multiplicar_coeficiente(coeficiente, termino):
        # Cada multiplicador es un literal entero: no se multiplica una
        # incognita matricial por una constante libre. Todo sigue en QF_LIA.
        return sum(z3.If(coeficiente == j, j * termino, cero)
                   for j in range(1, cota_matrices + 1))

    cache = {"": ([[z3.IntVal(int(i == j)) for j in range(2)] for i in range(2)], [cero, cero])}

    def interpretar(palabra):
        if palabra not in cache:
            matriz, vector = simbolos[palabra[0]]
            otra, constante = interpretar(palabra[1:])
            nueva = [[z3.simplify(sum(multiplicar_coeficiente(matriz[i][k], otra[k][j])
                                      for k in range(2))) for j in range(2)] for i in range(2)]
            nuevo = [z3.simplify(sum(multiplicar_coeficiente(matriz[i][k], constante[k])
                                     for k in range(2)) + vector[i]) for i in range(2)]
            cache[palabra] = nueva, nuevo
        return cache[palabra]

    comparaciones = []
    for regla in reglas:
        lm, lv = interpretar(regla["izquierda"])
        rm, rv = interpretar(regla["derecha"])
        solver.add([a >= b for a, b in zip(sum(lm, []) + lv, sum(rm, []) + rv)])
        if regla["estricta"]:
            comparaciones.append(lv[0] > rv[0])
    solver.add(z3.Or(comparaciones))
    conexion = z3.And(sum(simbolos[x][0][0][1] for x in "abefg") > 0,
                      sum(simbolos[x][0][1][0] for x in "abefg") > 0)
    if conexion_pedida == "ambas":
        solver.add(conexion)
    for izquierda, derecha in INTERCAMBIOS:
        lm, _ = interpretar(izquierda)
        rm, _ = interpretar(derecha)
        solver.add(z3.Implies(conexion, z3.And([a == b for a, b in zip(sum(lm, []), sum(rm, []))])))
    return solver, simbolos, interpretar


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--sistema-guardado", type=Path, required=True)
    analizador.add_argument("--cota-matrices", type=int, required=True)
    analizador.add_argument("--conexion", choices=("ambas", "libre"), required=True)
    analizador.add_argument("--segundos", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    reglas = leer_reglas(args.sistema_guardado)
    solver, simbolos, _ = codificar(reglas, args.cota_matrices, args.conexion, args.segundos)
    formula = args.salida.with_suffix(".smt2")
    formula.write_text(solver.to_smt2(), encoding="utf-8")
    print(f"QF_LIA: matrices <= {args.cota_matrices}, constantes libres, conexion {args.conexion}.", flush=True)
    inicio = time.monotonic()
    estado = solver.check()
    datos = dict(estado=str(estado), segundos=round(time.monotonic() - inicio, 3),
                 version_z3=z3.get_version_string(), cota_matrices=args.cota_matrices,
                 conexion=args.conexion, limite_segundos=args.segundos, semilla=0, hilos=1,
                 constantes_sin_cota=True, logica="QF_LIA", reglas=reglas,
                 fuente_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                 sistema_sha256=sha256(args.sistema_guardado.read_bytes()).hexdigest(),
                 formula_sha256=sha256(formula.read_bytes()).hexdigest(),
                 alcance="Primera eliminacion en una familia de matrices finita y vectores "
                 "sin cota. SAT se coteja con enteros independientes; UNSAT no tiene "
                 "certificado Lean; unknown no decide existencia. No prueba terminacion H.")
    if estado == z3.sat:
        modelo = solver.model()
        valor = lambda x: modelo.eval(x, model_completion=True).as_long()
        concretos = {s: ([[valor(x) for x in fila] for fila in m], [valor(x) for x in v])
                     for s, (m, v) in simbolos.items()}
        datos["estrictas"] = verificar_modelo(reglas, concretos)
        datos["simbolos"] = concretos
        datos["modelo_cotejado"] = True
    elif estado == z3.unknown:
        datos["motivo"] = solver.reason_unknown()
    args.salida.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{estado}: {datos['segundos']} segundos.", flush=True)


if __name__ == "__main__":
    main()
