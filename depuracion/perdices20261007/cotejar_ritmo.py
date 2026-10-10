"""Contraste exacto de la cota 8/5, los bloques pares y el reloj séxtico.

Sólo prefijos anteriores al primer cruce; no certifica una fuga infinita.
Implementación independiente de los módulos Lean, con órbitas directas.
"""

import argparse
from fractions import Fraction
import hashlib
from itertools import groupby
import json
from pathlib import Path


def raiz_entera(n, grado):
    menor, mayor = 0, 1 << ((n.bit_length() + grado - 1) // grado)
    while menor + 1 < mayor:
        medio = (menor + mayor) // 2
        if medio ** grado <= n:
            menor = medio
        else:
            mayor = medio
    return mayor if mayor ** grado <= n else menor


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--n-max', type=int, required=True)
    analizador.add_argument('--pasos', type=int, required=True)
    analizador.add_argument('--nivel-max', type=int, required=True)
    analizador.add_argument('--d-max', type=int, required=True)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    assert args.n_max >= 2 and args.pasos >= 1 and args.nivel_max >= 0 and args.d_max >= 0
    cuentas = dict(segmentos=0, unitarios=0, no_unitarios=0, bloques=0,
                   presupuestos_pares=0, saltos_de_factor=0, relojes=0)
    mejora = dict(casos=0, ejemplo=None)
    for n in range(2, args.n_max + 1):
        valores, coeficientes, s = [n], [Fraction(1)], 0
        for j in range(args.pasos):
            x = valores[-1]
            s += x % 2
            p = Fraction(3 ** s, 2 ** (j + 1))
            if p < 1:
                break
            valores.append((3 * x + 1) // 2 if x % 2 else x // 2)
            coeficientes.append(p)
        for c in range(args.nivel_max + 1):
            techo = 3 ** c
            visitas = [j for j, p in enumerate(coeficientes) if p <= techo]
            for u, v in zip(visitas, visitas[1:]):
                d, x = v - u, valores[u]
                bits = [y % 2 for y in valores[u:v]]
                h = sum(bit == 1 and (i == 0 or bits[i - 1] == 0)
                        for i, bit in enumerate(bits))
                grupos = [(bit, len(list(g))) for bit, g in groupby(bits)]
                assert h == sum(bit == 1 for bit, _ in grupos)
                # Techo logarítmico mínimo, calculado sin flotantes.
                l = x.bit_length()
                assert x + 1 <= 2 ** l and (l == 0 or 2 ** (l - 1) < x + 1)
                cuentas['segmentos'] += 1
                cuentas['unitarios' if d == 1 else 'no_unitarios'] += 1
                assert 5 ** h * d <= (3 + 2 * c) * 8 ** h * (x + 1)
                assert (x + 1) ** 6 <= 64 * (techo * n) ** 6 * (u + 1)
                if d > 1:
                    assert grupos[0][0] == 1 and grupos[-1][0] == 0 and len(grupos) == 2 * h
                    tiempo, impares, pares = u, 0, 0
                    reserva = Fraction(x + 1)
                    for i in range(h):
                        a, b = grupos[2 * i][1], grupos[2 * i + 1][1]
                        z = valores[tiempo] + 1
                        q = coeficientes[tiempo] / coeficientes[u]
                        assert Fraction(z, q) == reserva
                        assert z % 2 ** a == 0
                        assert 5 * (impares + a) <= 5 * l + 8 * impares
                        # Contabilidad que conserva TODOS los pasos pares anteriores.
                        assert reserva <= x + 1 + i
                        assert 2 ** (impares + a + pares) <= 3 ** impares * (x + 1 + i)
                        cuentas['presupuestos_pares'] += 1
                        tiempo += a + b
                        impares += a
                        pares += b
                        q_siguiente = coeficientes[tiempo] / coeficientes[u]
                        reserva += (1 - Fraction(1, 2 ** b)) / q_siguiente
                        assert Fraction(valores[tiempo] + 1, q_siguiente) == reserva
                        assert 3 * 5 ** (i + 1) * impares + 5 * 5 ** (i + 1) * l <= 5 * 8 ** (i + 1) * l
                        cuentas['bloques'] += 1
                    assert tiempo == v and d == impares + pares
                    assert 5 * d <= 8 * (c + impares)
                    assert 5 ** h * d <= (3 * l + 2 * c) * 8 ** h
                    anterior = 2 * ((2 ** h - 1) * l + c)
                    nueva = Fraction((3 * l + 2 * c) * 8 ** h, 5 ** h)
                    if nueva < anterior:
                        mejora['casos'] += 1
                        if mejora['ejemplo'] is None or h > mejora['ejemplo']['h']:
                            mejora['ejemplo'] = dict(n=n, c=c, u=u, v=v, h=h,
                                                    anterior=anterior, nueva=str(nueva))
                # Menor B entero que satisface la hipótesis del lema de salto.
                denominador = 5 ** (6 * h) * (u + 1) ** 4
                minimo = (8 ** (6 * h) + denominador - 1) // denominador
                for tope in (minimo, minimo + 1):
                    assert 8 ** (6 * h) <= tope * denominador
                    constante = 64 * (3 + 2 * c) ** 6 * (techo * n) ** 6
                    assert d ** 6 <= constante * tope * (u + 1) ** 5
                    cuentas['saltos_de_factor'] += 1
                assert (minimo - 1) * denominador < 8 ** (6 * h)
    # Trayectorias abstractas maximales; incluye D=0 y t_0>0.
    for constante in range(args.d_max + 1):
        for inicial in (0, 1, 2, 7, 64):
            t = inicial
            for i in range(args.pasos + 1):
                assert t + 1 <= (constante + inicial + 1) * (i + 1) ** 6
                derecho = constante * (t + 1) ** 5
                salto = raiz_entera(derecho, 6)
                assert salto ** 6 <= derecho < (salto + 1) ** 6
                t += salto
                cuentas['relojes'] += 1
    resultado = dict(estado='contraste finito exacto; no prueba infinitud ni FugaPura',
                     parametros={k: v for k, v in vars(args).items() if k != 'salida'},
                     sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                     cuentas=cuentas, mejora=mejora)
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(cuentas, ensure_ascii=False))


if __name__ == '__main__':
    main()
