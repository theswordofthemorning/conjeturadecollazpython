"""Contraste entero de trazas, constantes y codificacion QF_LIA con controles positivos."""

import argparse
from copy import deepcopy
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import random

import z3

from buscar_constantes_libres import INTERCAMBIOS, codificar, evaluar, leer_reglas, verificar_modelo


def multiplicar(a, b):
    return tuple(sum(a[2 * i + k] * b[2 * k + j] for k in range(2))
                 for i in range(2) for j in range(2))


def sumar(a, b):
    return tuple(x + y for x, y in zip(a, b))


def restar(a, b):
    return tuple(x - y for x, y in zip(a, b))


def actuar(a, v):
    return tuple(sum(a[2 * i + k] * v[k] for k in range(2)) for i in range(2))


def mayor(a, b):
    return all(x >= y for x, y in zip(a, b))


def constantes(simbolos, izquierda, derecha):
    return restar(evaluar(izquierda, simbolos, (0, 0)),
                  evaluar(derecha, simbolos, (0, 0)))


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--control", type=Path, required=True)
    analizador.add_argument("--objetivo", type=Path, required=True)
    analizador.add_argument("--muestras", type=int, required=True)
    analizador.add_argument("--semilla", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    assert 1 <= args.muestras <= 10000
    matrices = list(product(range(3), repeat=4))
    pares = 0
    conectados = 0
    for u, v in product(matrices, repeat=2):
        k = restar(multiplicar(v, u), multiplicar(u, v))
        w = sumar(u, v)
        assert k[0] + k[3] == 0
        assert sum(multiplicar(k, w)[i] for i in (0, 3)) == 0
        if min(k) >= 0:
            pares += 1
            assert k[0] == k[3] == 0
            if w[1] > 0 and w[2] > 0:
                conectados += 1
                assert k == (0, 0, 0, 0)

    binarias = list(product(range(2), repeat=4))
    productos = {(a, b): multiplicar(a, b) for a, b in product(binarias, repeat=2)}
    validas = 0
    acopladas = 0
    for a, b, e in product(binarias, repeat=3):
        if not mayor(productos[e, a], productos[a, e]):
            continue
        for f in binarias:
            if not mayor(productos[f, a], productos[b, e]):
                continue
            if not mayor(productos[e, b], productos[b, f]):
                continue
            for g in binarias:
                if not mayor(productos[g, a], productos[a, f]):
                    continue
                if not mayor(productos[f, b], productos[a, g]):
                    continue
                if not mayor(productos[g, b], productos[b, g]):
                    continue
                validas += 1
                s = dict(a=a, b=b, e=e, f=f, g=g)
                w = tuple(sum(m[i] for m in s.values()) for i in range(4))
                diferencias = [restar(productos[s[l[0]], s[l[1]]],
                                     productos[s[r[0]], s[r[1]]]) for l, r in INTERCAMBIOS]
                assert all(d[0] == d[3] == 0 for d in diferencias)
                if w[1] > 0 and w[2] > 0:
                    acopladas += 1
                    assert all(d == (0, 0, 0, 0) for d in diferencias)

    azar = random.Random(args.semilla)
    for _ in range(args.muestras):
        simbolos = {s: ([[azar.randrange(5) for _ in range(2)] for _ in range(2)],
                         [azar.randrange(10001) for _ in range(2)]) for s in "abcdefg"}
        m = {s: tuple(sum(a, [])) for s, (a, _) in simbolos.items()}
        v = {s: tuple(b) for s, (_, b) in simbolos.items()}
        u = sumar(v["a"], v["b"])
        w = sumar(sumar(v["e"], v["f"]), v["g"])
        total = (0, 0)
        for l, r in INTERCAMBIOS:
            total = sumar(total, constantes(simbolos, l, r))
        prevista = restar(sumar(actuar(sumar(sumar(m["e"], m["f"]), m["g"]), u),
                               tuple(2 * x for x in w)),
                         sumar(actuar(sumar(m["a"], m["b"]), w), tuple(3 * x for x in u)))
        assert total == prevista
        a, b = m["a"], m["b"]
        va, vb, ve, vf = (v[s] for s in "abef")
        identidad = (1, 0, 0, 1)
        d2 = restar(sumar(actuar(restar(sumar(multiplicar(b, a), b), identidad), va),
                          actuar(restar(identidad, a), vb)), actuar(multiplicar(a, b), ve))
        d3 = restar(sumar(actuar(restar(multiplicar(b, b), b), va), actuar(b, vb)),
                    actuar(multiplicar(b, a), vf))
        for l, r, diferencia in (("da", "d", va), ("dbaa", "dabe", d2),
                                 ("dbba", "dbaf", d3)):
            assert constantes(simbolos, l, r)[0] == sum(
                simbolos["d"][0][0][j] * diferencia[j] for j in range(2))

    j = [[1, 1], [1, 1]]
    dos_j = [[2, 2], [2, 2]]
    testigo = {s: (deepcopy(j if s in "ab" else dos_j),
                   [1, 1] if s in "ab" else [0, 0]) for s in "abefg"}
    assert all(constantes(testigo, l, r) == (3, 3) for l, r in INTERCAMBIOS)

    casos_escalares = 0
    validos_escalares = 0
    for t, c in product(range(1, 5), range(4)):
        for p in range(t * c + 1):
            for x, y, z, w in product(range(5), repeat=4):
                casos_escalares += 1
                if (t * c + y <= p + z
                        and t * t * c + (t + 1) * x <= p + w
                        and t * t * z + t * y + x <= t * t * x + t * x + y
                        and x + t * w <= t * x + y):
                    validos_escalares += 1
                    assert x == y == z == w == 0

    # Familia debil conectada que no conserva ninguna recta natural (x,kx+t).
    fibonacci = {s: ([[2, 0], [0, 2]] if s in "ab" else [[1, 1], [1, 0]],
                     [0, 0]) for s in "abefg"}
    fibonacci.update(c=([[0, 0], [0, 0]], [0, 0]),
                     d=([[1, 1], [0, 0]], [0, 0]))
    for regla in leer_reglas(args.objetivo):
        l0 = evaluar(regla["izquierda"], fibonacci, (0, 0))
        r0 = evaluar(regla["derecha"], fibonacci, (0, 0))
        assert l0 == r0 == [0, 0]
        for punto in ((1, 0), (0, 1)):
            assert mayor(evaluar(regla["izquierda"], fibonacci, punto),
                         evaluar(regla["derecha"], fibonacci, punto))

    control = json.loads(args.control.read_text(encoding="utf-8"))
    comprobaciones = []
    productos_cotejados = 0
    for etapa in control["etapas"]:
        certificado = etapa["certificado"]
        reglas = certificado["reglas"]
        original = {s: (d["matriz"], d["vector"]) for s, d in certificado["simbolos"].items()}
        estrictas = verificar_modelo(reglas, original)
        for escala in (1, 10000):
            simbolos = deepcopy(original)
            for s, (matriz, vector) in simbolos.items():
                simbolos[s] = matriz, [x * escala for x in vector]
            simbolos["c"] = [[0, 0], [0, 0]], simbolos["c"][1]
            simbolos["d"] = [simbolos["d"][0][0], [0, 0]], [0, 0]
            assert verificar_modelo(reglas, simbolos) == estrictas
            solver, variables, interpretar = codificar(reglas, 3, "libre", 5)
            for s, (matriz, vector) in variables.items():
                for i, fila in enumerate(matriz):
                    for k, x in enumerate(fila):
                        solver.add(x == simbolos[s][0][i][k])
                for i, x in enumerate(vector):
                    solver.add(x == simbolos[s][1][i])
            assert solver.check() == z3.sat
            modelo = solver.model()
            for palabra in {r[lado] for r in reglas for lado in ("izquierda", "derecha")}:
                matriz, vector = interpretar(palabra)
                en_cero = evaluar(palabra, simbolos, (0, 0))
                assert [modelo.eval(x).as_long() for x in vector] == en_cero
                for k in range(2):
                    punto = [int(i == k) for i in range(2)]
                    en_base = evaluar(palabra, simbolos, punto)
                    assert all(modelo.eval(matriz[i][k]).as_long() == en_base[i] - en_cero[i]
                               for i in range(2))
                productos_cotejados += 1
            comprobaciones.append(dict(etapa=etapa["numero"], escala_constantes=escala,
                                        estrictas=estrictas, estado="sat"))
    resultado = dict(
        estado="correcto", fuente_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        codificador_sha256=sha256(Path(__file__).with_name("buscar_constantes_libres.py").read_bytes()).hexdigest(),
        control_sha256=sha256(args.control.read_bytes()).hexdigest(), version_z3=z3.get_version_string(),
        objetivo_sha256=sha256(args.objetivo.read_bytes()).hexdigest(),
        pares_matrices=len(matrices) ** 2, pares_con_conmutador_no_negativo=pares,
        pares_conectados=conectados, quintetos_binarios=len(binarias) ** 5,
        quintetos_con_intercambios_debiles=validas, quintetos_conectados=acopladas,
        muestras_constantes=args.muestras, semilla=args.semilla,
        holgura_constante_testigo=[3, 3], controles=comprobaciones,
        casos_nucleo_binario_escalar=casos_escalares,
        casos_debiles_nucleo_binario_escalar=validos_escalares,
        ejemplo_fibonacci_debil_cotejado=True,
        composiciones_simbolicas_cotejadas=productos_cotejados,
        alcance="Cotejo finito independiente y controles positivos del codificador, "
                "incluidas constantes de magnitud 10000. No es una prueba universal "
                "de imposibilidad ni una comprobacion de UNSAT mediante certificados.")
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
