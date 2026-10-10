"""Contraste entero de extracción, cotas y reloj; sólo prefijos finitos."""

import argparse
import hashlib
from itertools import groupby
import json
from math import isqrt
from pathlib import Path


def orbita(n, pasos):
    valores, impares = [n], [0]
    for _ in range(pasos):
        x = valores[-1]
        valores.append((3 * x + 1) // 2 if x % 2 else x // 2)
        impares.append(impares[-1] + x % 2)
    return valores, impares


def extraer(valores, u, v):
    palabra = ''.join(str(x % 2) for x in valores[u:v])
    canonico = int(palabra.startswith('1')) + palabra.count('01')
    grupos = [(bit, len(list(g))) for bit, g in groupby(palabra)]
    assert canonico == sum(bit == '1' for bit, _ in grupos)
    if v - u > 1:
        assert palabra.startswith('1') and palabra.endswith('0')
        assert len(grupos) == 2 * canonico and canonico > 0
        j = u
        for i in range(canonico):
            bit_a, a = grupos[2 * i]
            bit_b, b = grupos[2 * i + 1]
            assert (bit_a, bit_b) == ('1', '0') and a > 0 and b > 0
            assert 2 ** a * (valores[j + a] + 1) == 3 ** a * (valores[j] + 1)
            assert 2 ** (a + b) * valores[j + a + b] == 3 ** a * (valores[j] + 1) - 2 ** a
            j += a + b
        assert j == v
    return canonico


def constante(n, c, h):
    return 4 * (2 * (2 ** h + c) + 1) ** 2 * (3 ** c * n) ** 6 + 1


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--n-max', type=int, required=True)
    analizador.add_argument('--pasos', type=int, required=True)
    analizador.add_argument('--nivel-max', type=int, required=True)
    analizador.add_argument('--d-max', type=int, required=True)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    assert args.n_max >= 2 and args.pasos >= 1 and args.nivel_max >= 0 and args.d_max >= 0
    cuentas = dict(entradas=0, segmentos=0, unitarios=0, no_unitarios=0,
                   rachas_maximas=0, colas=0, relojes_orbitales=0,
                   relojes_abstractos=0, pares_omitidos_rechazados=0)
    ejemplos = []
    for n in range(2, args.n_max + 1):
        valores, impares = orbita(n, args.pasos)
        fin = next((j for j in range(args.pasos + 1) if 3 ** impares[j] < 2 ** j), args.pasos + 1)
        for c in range(args.nivel_max + 1):
            techo = 3 ** c
            visitas = [j for j in range(fin) if 3 ** impares[j] <= techo * 2 ** j]
            if c == 0:
                assert visitas == [0]
            for u in visitas:
                x = valores[u]
                assert x >= n >= 2
                assert x ** 6 <= (techo * n) ** 6 * (impares[u] + 1)
                assert (x + 1) ** 2 <= 4 * (techo * n) ** 6 * (u + 1)
                cuentas['entradas'] += 1
            cantidades = []
            for u, v in zip(visitas, visitas[1:]):
                # Mínimo siguiente por búsqueda independiente de la lista.
                siguiente = next(j for j in range(u + 1, fin)
                                 if 3 ** impares[j] <= techo * 2 ** j)
                assert siguiente == v
                h = extraer(valores, u, v)
                cantidades.append(h)
                for tope in (h, h + 1):
                    d = constante(n, c, tope)
                    assert (v - u) ** 2 <= d * (u + 1)
                cuentas['segmentos'] += 1
                cuentas['unitarios' if v - u == 1 else 'no_unitarios'] += 1
                if h > cuentas['rachas_maximas']:
                    cuentas['rachas_maximas'] = h
                    ejemplos.append(dict(n=n, c=c, u=u, v=v, rachas=h))
            # Un par que omite un regreso no satisface Consecutivos.
            for u, j, v in zip(visitas, visitas[1:], visitas[2:]):
                assert u < j < v and 3 ** impares[j] <= techo * 2 ** j
                cuentas['pares_omitidos_rechazados'] += 1
            # Se conserva la semilla original también al tomar una cola.
            for inicio in sorted({0, len(visitas) // 2}):
                cola = visitas[inicio:]
                tope = max(cantidades[inicio:], default=0)
                d = constante(n, c, tope)
                for i, u in enumerate(cola):
                    assert u + 1 <= (d + cola[0] + 1) * (i + 1) ** 2
                    cuentas['relojes_orbitales'] += 1
                cuentas['colas'] += 1
    # Recurrencia abstracta maximal: isqrt elige el mayor salto permitido.
    # Incluye D=0, t_0=0 y colas que parten después de cero.
    for d in range(args.d_max + 1):
        for inicial in (0, 1, 2, 7, 64):
            t = inicial
            for i in range(args.pasos + 1):
                assert t + 1 <= (d + inicial + 1) * (i + 1) ** 2
                salto = isqrt(d * (t + 1))
                assert salto ** 2 <= d * (t + 1) < (salto + 1) ** 2
                t += salto
                cuentas['relojes_abstractos'] += 1
    resultado = dict(estado='contraste finito exacto; no certifica FugaPura ni infinitos regresos',
                     sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                     parametros={k: v for k, v in vars(args).items() if k != 'salida'},
                     cuentas=cuentas, ejemplos=ejemplos)
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(cuentas, ensure_ascii=False))


if __name__ == '__main__':
    main()
