"""Contraste entero del cruce entre sexta raíz y casi fugitivos.

Los controles orbitales sólo usan prefijos finitos verificados; nunca
declaran una fuga pura. No importa experimentos ni ejecuta censos antiguos.
"""

import argparse
import hashlib
import json
from math import comb
from pathlib import Path


def raiz_sexta(q):
    inferior, superior = 0, 1 << ((q.bit_length() + 5) // 6)
    while superior - inferior > 1:
        medio = (inferior + superior) // 2
        if medio ** 6 <= q:
            inferior = medio
        else:
            superior = medio
    assert inferior ** 6 <= q < (inferior + 1) ** 6
    return inferior


def cota_mixta(x, c, m):
    return ((x + 1) // 2 ** (100 * m) + 1) * 2 ** (c + 96 * m)


def mejor_cota(n, c, k):
    x = raiz_sexta((3 ** c * n) ** 6 * k)
    candidatos = [(cota_mixta(x, c, m), m)
                  for m in range((x + 1).bit_length() // 100 + 2)]
    valor, m = min(candidatos)
    return dict(radio=x, mixta=valor, m=m, combinada=min(k, x, valor))


def orbita(n, pasos):
    valores, impares = [n], [0]
    for _ in range(pasos):
        x = valores[-1]
        impares.append(impares[-1] + x % 2)
        valores.append(x // 2 if x % 2 == 0 else (3 * x + 1) // 2)
    return valores, impares


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--n-max", type=int, required=True)
    analizador.add_argument("--pasos", type=int, required=True)
    analizador.add_argument("--nivel-max", type=int, required=True)
    analizador.add_argument("--m-max", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    assert args.n_max >= 2 and args.pasos >= 1 and args.nivel_max >= 0 and args.m_max >= 0
    conteos = dict(raices=0, colas_binomiales=0, intervalos=0,
                   casi_fugas_finitas=0, cotas_mixtas=0, cotas_con_m_positivo=0,
                   potencias=0)
    for x in [0, 1, 2, 3, 63, 64, 65, 2 ** 96, 2 ** 100, 2 ** 200]:
        for q in {max(0, x ** 6 - 1), x ** 6, x ** 6 + 1}:
            r = raiz_sexta(q)
            assert r ** 6 <= q < (r + 1) ** 6
            conteos['raices'] += 1
    for m in range(args.m_max + 1):
        longitud = 100 * m
        for c in range(args.nivel_max + 1):
            cuenta = sum(comb(longitud, s) for s in range(longitud + 1)
                         if 2 ** longitud <= 3 ** (c + s))
            assert cuenta <= 2 ** (c + 96 * m)
            conteos['colas_binomiales'] += 1

    semillas = list(range(2, args.n_max + 1)) + [2 ** a - 1 for a in (16, 64, 128, 256)]
    for n in semillas:
        valores, s = orbita(n, args.pasos)
        cruce = next((j for j in range(1, args.pasos + 1) if 3 ** s[j] < 2 ** j), args.pasos + 1)
        vivo = min(args.pasos, cruce - 1)
        for k in sorted({0, 1, 2, 3, 8, 16, 32, 64, vivo}):
            if k > vivo or len(set(valores[:k])) != k:
                continue
            for c in range(args.nivel_max + 1):
                bajos = [j for j in range(k) if 3 ** s[j] <= 3 ** c * 2 ** j]
                x = raiz_sexta((3 ** c * n) ** 6 * k)
                assert all(valores[j] <= x for j in bajos)
                assert len(bajos) <= min(k, x)
                conteos['intervalos'] += 1
                for m in range(min(args.m_max, (vivo - k) // 100) + 1):
                    for j in bajos:
                        for i in range(100 * m + 1):
                            assert 2 ** i <= 3 ** (c + s[j + i] - s[j])
                            conteos['casi_fugas_finitas'] += 1
                    assert len(bajos) <= cota_mixta(x, c, m)
                    conteos['cotas_mixtas'] += 1
                    conteos['cotas_con_m_positivo'] += int(m > 0)

    tablas = []
    for n in (2, 7, 27):
        for c in range(args.nivel_max + 1):
            for k in [0, 1, 64, 2 ** 120, 2 ** 600, 2 ** 1200]:
                dato = mejor_cota(n, c, k)
                x, q = dato['radio'], dato['combinada']
                assert q ** 25 <= 2 ** (25 * c + 125) * (x + 1) ** 24
                assert q ** 150 <= 2 ** (150 * c + 894) * (3 ** c * n) ** 144 * k ** 24
                conteos['potencias'] += 1
                if n == 7 and c in (0, 1) and k in (64, 2 ** 600, 2 ** 1200):
                    tablas.append(dict(n=n, c=c, K=k, **dato))
    evidencia = dict(mapa='atajo 3n+1', ley='determinista; enteros exactos',
                     alcance='Controles finitos y cotas numéricas; no se certifica ninguna fuga pura.',
                     sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                     parametros={k: v for k, v in vars(args).items() if k != 'salida'},
                     semillas=len(semillas), conteos=conteos, tablas=tablas)
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(json.dumps(evidencia, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(conteos, ensure_ascii=False))


if __name__ == '__main__':
    main()
