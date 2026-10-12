"""Cotejo entero, por funciones y polinomios, de soportes y rectas naturales 2x2."""

import argparse
from collections import Counter
from itertools import product
import json
from pathlib import Path
from random import Random

from comprobar_proyecciones_matrices import huella_lf
from verificar_matrices_h import componer, interpretar


VARIABLES = ['d00', 'd01', 'a00', 'a01', 'a10', 'a11',
             'b00', 'b01', 'b10', 'b11', 'va0', 'va1', 'vb0', 'vb1']
RUTAS = [('d00', 'va0'), ('d01', 'va1'), ('d00', 'vb0'), ('d01', 'vb1'),
         ('d00', 'b01', 'va1'), ('d01', 'b10', 'va0'),
         ('d00', 'b01', 'vb1'), ('d01', 'b10', 'vb0'),
         ('d00', 'b00', 'a01', 'va1'), ('d01', 'b11', 'a10', 'va0')]
REGLAS = [('da', 'd'), ('dbaa', 'dabe'), ('dbba', 'dbaf'),
          ('ea', 'ae'), ('fa', 'be'), ('ga', 'af'), ('eb', 'bf'),
          ('fb', 'ag'), ('gb', 'bg'), ('ec', 'bc'), ('fc', 'aac'), ('gc', 'bac')]


def evaluar(palabra, simbolos, punto):
    """Aplica funciones al punto, sin componer matrices."""
    x, y = punto
    for letra in reversed(palabra):
        m, v = simbolos[letra]
        x, y = m[0][0] * x + m[0][1] * y + v[0], m[1][0] * x + m[1][1] * y + v[1]
    return x, y


def sumar(*polinomios):
    resultado = Counter()
    for p in polinomios:
        resultado.update(p)
    return resultado


def multiplicar(p, q):
    resultado = Counter()
    for a, ca in p.items():
        for b, cb in q.items():
            resultado[tuple(sorted(a + b))] += ca * cb
    return resultado


def simbolico(palabra):
    """Expande la evaluación de cada letra; d tiene vector nulo."""
    punto = [Counter(), Counter()]
    for letra in reversed(palabra):
        siguiente = []
        for i in range(2):
            constante = Counter({('v' + letra + str(i),): 1}) if letra != 'd' else Counter()
            siguiente.append(sumar(constante, *[
                multiplicar(Counter({(letra + str(i) + str(j),): 1}), punto[j]) for j in range(2)]))
        punto = siguiente
    return punto[0]


def producto(valores):
    resultado = 1
    for valor in valores:
        resultado *= valor
    return resultado


def asignacion(valores):
    r = dict(zip(VARIABLES, valores))
    simbolos = {s: ([[r[s + '00'], r[s + '01']], [r[s + '10'], r[s + '11']]],
                    [r['v' + s + '0'], r['v' + s + '1']]) for s in 'ab'}
    simbolos['d'] = ([[r['d00'], r['d01']], [0, 0]], [0, 0])
    return r, simbolos


def conserva(simbolo, k, t):
    m, v = simbolo
    return (m[1][0] + m[1][1] * k == k * (m[0][0] + m[0][1] * k)
            and m[1][1] * t + v[1] == k * (m[0][1] * t + v[0]) + t)


def proyeccion(simbolo, k, t):
    m, v = simbolo
    return m[0][0] + m[0][1] * k, m[0][1] * t + v[0]


def debil(izquierda, derecha):
    m, v = izquierda
    n, w = derecha
    return all(x >= y for x, y in zip(sum(m, []) + v, sum(n, []) + w))


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--cota-rectas', type=int, required=True)
    analizador.add_argument('--muestras-grandes', type=int, required=True)
    analizador.add_argument('--semilla', type=int, required=True)
    analizador.add_argument('--sistema-guardado', type=Path, required=True)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    assert 0 <= args.cota_rectas <= 3 and 0 <= args.muestras_grandes <= 100000
    sistema = json.loads(args.sistema_guardado.read_text(encoding='utf-8'))
    leidas = []
    for linea in sistema['reglas_originales'].splitlines():
        i, j = linea.split(' ->| ' if ' ->| ' in linea else ' ->= ')
        leidas.append((i[::-1], j[::-1]))
    assert leidas == REGLAS
    polinomio = sumar(*(simbolico(p) for p in ['da', 'dbaa', 'dbba']))
    soportes = {frozenset(m) for m in polinomio}
    minimos = {s for s in soportes if not any(t < s for t in soportes)}
    assert minimos == {frozenset(r) for r in RUTAS}
    assert len(minimos) == 10
    # Cada ruta tiene un testigo con exactamente sus factores positivos.
    testigos = []
    for ruta in RUTAS:
        r, simbolos = asignacion([int(v in ruta) for v in VARIABLES])
        assert sum(evaluar(p, simbolos, (0, 0))[0] for p in ['da', 'dbaa', 'dbba']) > 0
        for variable in ruta:
            _, sin_factor = asignacion([int(v in ruta and v != variable) for v in VARIABLES])
            assert sum(evaluar(p, sin_factor, (0, 0))[0] for p in ['da', 'dbaa', 'dbba']) == 0
        testigos.append(dict(factores=list(ruta), valores=r))
    activos = 0
    por_geometria = Counter()
    for valores in product(range(2), repeat=len(VARIABLES)):
        r, simbolos = asignacion(valores)
        funciones = sum(evaluar(p, simbolos, (0, 0))[0] for p in ['da', 'dbaa', 'dbba'])
        algebra = sum(c * producto(r[v] for v in m) for m, c in polinomio.items())
        assert funciones == algebra
        rutas = any(all(r[v] for v in ruta) for ruta in RUTAS)
        assert (funciones > 0) == rutas
        for palabra in ['da', 'dbaa', 'dbba']:
            assert evaluar(palabra, simbolos, (0, 0)) == tuple(interpretar(palabra, simbolos, 'natural')[1])
        activos += rutas
        superior = bool(r['d01'] or r['a01'] or r['b01'])
        retorno = bool(r['a10'] or r['b10'])
        por_geometria[f'superior={int(superior)},retorno={int(retorno)},aporte={int(rutas)}'] += 1
    azar = Random(args.semilla)
    for _ in range(args.muestras_grandes):
        r, simbolos = asignacion([azar.choice([0, 1, 2, 17, 10000]) for _ in VARIABLES])
        funciones = sum(evaluar(p, simbolos, (0, 0))[0] for p in ['da', 'dbaa', 'dbba'])
        assert funciones == sum(c * producto(r[v] for v in m) for m, c in polinomio.items())
        assert (funciones > 0) == any(all(r[v] for v in ruta) for ruta in RUTAS)
    # Rectas: B conserva el rayo; A es arbitraria. La prueba sólo pide esto.
    def afin(valores):
        a, b, c, d, e, f = valores
        return [[a, b], [c, d]], [e, f]
    izquierdas = [afin(v) for v in product(range(2), repeat=6)]
    candidatas = [afin(v) for v in product(range(args.cota_rectas + 1), repeat=6)]
    productos = cierres = 0
    rectas = []
    for k, t in product(range(args.cota_rectas + 1), repeat=2):
        conservan = [b for b in candidatas if conserva(b, k, t)]
        rectas.append(dict(k=k, t=t, simbolos=len(conservan)))
        for b in conservan:
            q, w = proyeccion(b, k, t)
            for a in izquierdas:
                p, v = proyeccion(a, k, t)
                compuesto = componer(a, b, 'natural')
                assert proyeccion(compuesto, k, t) == (p * q, p * w + v)
                productos += 1
            for a in conservan:
                compuesto = componer(a, b, 'natural')
                assert conserva(compuesto, k, t)
                # Contraste en puntos grandes, sin inferir universalidad del muestreo.
                p, v = proyeccion(a, k, t)
                for x in (0, 1, 17):
                    salida = evaluar('ab', {'a': a, 'b': b}, (x, k * x + t))
                    esperado = p * (q * x + w) + v
                    assert salida == (esperado, k * esperado + t)
                cierres += 1
    # Soporte d01*va1: aporte real sin entrada inversa. No orienta todo el sistema.
    _, abierto = asignacion([int(v in ('d01', 'va1')) for v in VARIABLES])
    assert evaluar('da', abierto, (0, 0))[0] == 1
    assert not debil(interpretar('da', abierto, 'natural'), abierto['d'])
    # Un grafo muy conectado puede conservar la diagonal y carecer de descenso.
    lleno = {s: ([[1, 1], [1, 1]], [0, 0]) for s in 'abdefg'}
    lleno['c'] = ([[0, 0], [0, 0]], [0, 0])
    assert all(conserva(lleno[s], 1, 0) for s in 'abcefg')
    assert all(debil(interpretar(i, lleno, 'natural'), interpretar(j, lleno, 'natural')) for i, j in REGLAS)
    assert all(evaluar(i, lleno, (0, 0))[0] == evaluar(j, lleno, (0, 0))[0] for i, j in REGLAS[:3])
    fuentes = [Path(__file__), Path(__file__).with_name('verificar_matrices_h.py'),
               Path(__file__).with_name('comprobar_proyecciones_matrices.py'),
               Path(__file__).with_name('PerdicesSoportesMatrices.lean'), args.sistema_guardado]
    resultado = dict(parametros=vars(args) | {'sistema_guardado': str(args.sistema_guardado), 'salida': str(args.salida)},
                     variables=VARIABLES, monomios=len(polinomio), soportes_distintos=len(soportes),
                     rutas_minimas=[list(r) for r in RUTAS], testigos_minimalidad=testigos,
                     soportes_binarios=2 ** len(VARIABLES), con_aporte=activos,
                     sin_aporte=2 ** len(VARIABLES) - activos,
                     geometria_local=dict(sorted(por_geometria.items())),
                     rectas=rectas, productos_proyectados=productos, cierres_rectas=cierres,
                     ejemplo_sin_retorno={'aporte_da': 1, 'orienta_sistema': False},
                     ejemplo_conectado={'conserva_diagonal': True, 'reglas_debiles': 12, 'estrictas': 0},
                     fuentes_lf={p.name: huella_lf(p) for p in fuentes},
                     alcance='Clasifica exactamente soportes de aportes izquierdos, no soportes '
                     'que orienten todo el sistema. Cotejos finitos de identidades; las pruebas '
                     'sin cota de soporte y obstrucción por rectas están en Lean. Persistencia abierta.')
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'OK: {2 ** len(VARIABLES)} soportes; {activos} activos; 10 mínimos; '
          f'{productos} productos proyectados; {cierres} cierres de rectas.')


if __name__ == '__main__':
    main()
