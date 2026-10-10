"""Contraste exacto de excursiones; nunca declara una fuga por un prefijo."""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def trayectoria(n, pasos):
    valores, productos, impares = [n], [Fraction(1)], [0]
    for _ in range(pasos):
        x = valores[-1]
        impar = x % 2
        valores.append((3 * x + 1) // 2 if impar else x // 2)
        productos.append(productos[-1] * Fraction(3 if impar else 1, 2))
        impares.append(impares[-1] + impar)
    return valores, productos, impares


def residuo_afin(palabra):
    a, b, m = 1, 0, 1
    for bit in palabra:
        if bit:
            a, b = 3 * a, 3 * b + m
        m *= 2
    return (-b * pow(a, -1, m)) % m


def familia(a):
    b = 0
    while 3 ** a > 3 * 2 ** (a + b):
        b += 1
    u = pow(3 ** a, -1, 2 ** b)
    n = 2 ** a * u - 1
    palabra = [1] * a + [0] * b
    assert n == residuo_afin(palabra)
    valores, productos, _ = trayectoria(n, a + b)
    assert [x % 2 for x in valores[:-1]] == palabra
    assert all(valores[j] == 3 ** j * 2 ** (a - j) * u - 1 for j in range(a + 1))
    assert all(valores[a + j] * 2 ** j == 3 ** a * u - 1 for j in range(b + 1))
    assert all(p >= 1 for p in productos)
    assert all(x > n for x in valores[1:])
    visitas = [j for j, p in enumerate(productos) if p <= 3]
    assert visitas == [0, 1, 2, a + b]
    assert Fraction(3, 2) < productos[-1] <= 3
    return dict(a=a, b=b, semilla=n, final=valores[-1],
                visitas=visitas, hueco=a + b - 2,
                producto_final=str(productos[-1]))


def controlar_rachas(valores, u, v, c):
    """Extrae rachas de la órbita directa; contrasta la criba algebraica."""
    palabra = [x % 2 for x in valores[u:v]]
    if len(palabra) <= 1:
        return False
    assert palabra[0] == 1 and palabra[-1] == 0
    longitudes = []
    j = 0
    while j < len(palabra):
        inicio = j
        while j < len(palabra) and palabra[j] == 1:
            j += 1
        a = j - inicio
        inicio = j
        while j < len(palabra) and palabra[j] == 0:
            j += 1
        b = j - inicio
        assert a >= 1 and b >= 1
        longitudes.append((a, b))
    x = valores[u]
    l = x.bit_length()  # Menor L con x+1 <= 2^L, también en potencias exactas.
    assert x + 1 <= 2 ** l
    acumulados, tiempo = 0, 0
    for i, (a, b) in enumerate(longitudes):
        assert (valores[u + tiempo] + 1) % 2 ** a == 0
        assert 2 ** (acumulados + a) <= (x + 1) * 3 ** acumulados
        acumulados += a
        tiempo += a + b
        assert acumulados + l <= 2 ** (i + 1) * l
    assert tiempo == v - u
    assert 2 ** tiempo <= 3 ** (c + acumulados)
    assert tiempo <= 2 * ((2 ** len(longitudes) - 1) * l + c)
    return True


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--a-max', type=int, required=True)
    analizador.add_argument('--n-max', type=int, required=True)
    analizador.add_argument('--pasos', type=int, required=True)
    analizador.add_argument('--nivel-max', type=int, required=True)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    assert args.a_max >= 3 and args.n_max >= 2 and args.pasos >= 1 and args.nivel_max >= 0
    familias = [familia(a) for a in range(3, args.a_max + 1)]
    segmentos, rangos, presupuestos, rachas = 0, 0, 0, 0
    for caso in familias:
        valores, _, _ = trayectoria(caso['semilla'], caso['a'] + caso['b'])
        assert controlar_rachas(valores, 2, caso['a'] + caso['b'], 1)
        rachas += 1
    for n in range(2, args.n_max + 1):
        valores, productos, impares = trayectoria(n, args.pasos)
        # Únicamente el prefijo anterior al primer cruce, incluyendo tiempo cero.
        fin = next((j for j, p in enumerate(productos) if p < 1), len(productos))
        for c in range(args.nivel_max + 1):
            techo = 3 ** c
            visitas = [j for j in range(fin) if productos[j] <= techo]
            if c == 0:
                assert visitas == [0]
            constante = 2 ** (150 * c + 894) * (techo * n) ** 144
            for r, tiempo in enumerate(visitas):
                cuenta = sum(p <= techo for p in productos[:tiempo + 1])
                assert cuenta == r + 1
                # Control de índices y álgebra: no certifica la hipótesis global.
                assert (r + 1) ** 150 <= constante * (tiempo + 1) ** 24
                rangos += 1
                d = max((v - u for u, v in zip(visitas[:r], visitas[1:r + 1])), default=0)
                assert tiempo <= visitas[0] + d * r
                assert (r + 1) ** 126 <= constante * (visitas[0] + d + 1) ** 24
                presupuestos += 1
            for u, v in zip(visitas, visitas[1:]):
                d, s = v - u, impares[v] - impares[u]
                cociente = Fraction(3 ** s, 2 ** d)
                assert cociente == productos[v] / productos[u]
                assert Fraction(1, techo) <= cociente <= techo
                incremento = sum((1 / productos[j] for j in range(u, v)
                                  if valores[j] % 2), Fraction(0)) / 3
                assert valores[v] / productos[v] - valores[u] / productos[u] == incremento
                if d > 1:
                    assert valores[u] % 2 == 1 and valores[v - 1] % 2 == 0
                    assert all(productos[j] > techo for j in range(u + 1, v))
                    assert Fraction(techo, 2) < productos[v] <= techo
                    assert controlar_rachas(valores, u, v, c)
                    rachas += 1
                segmentos += 1
    resultado = dict(estado='cotejo finito exacto; ninguna fuga pura afirmada',
                     sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                     parametros={k: v for k, v in vars(args).items() if k != 'salida'},
                     familias_verificadas=len(familias), segmentos=segmentos,
                     controles_indice=rangos, controles_presupuesto=presupuestos,
                     controles_rachas=rachas,
                     ejemplos=[familias[i] for i in sorted({0, min(2, len(familias) - 1), len(familias) - 1})])
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'OK: {len(familias)} familias, {segmentos} segmentos, {rangos} índices y presupuestos, {rachas} rachas.')


if __name__ == '__main__':
    main()
