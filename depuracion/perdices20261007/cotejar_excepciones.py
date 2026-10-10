"""Contraste entero de cadenas 110, excepciones y cotas orbitales.

Genera también palabras modulares para variar la posición y longitud de
una excepción. Los controles finitos no certifican FugaPura ni infinitud.
"""

import argparse
import hashlib
from itertools import groupby, product
import json
from pathlib import Path


def orbita(n, pasos):
    valores, impares = [n], [0]
    for _ in range(pasos):
        x = valores[-1]
        valores.append((3 * x + 1) // 2 if x % 2 else x // 2)
        impares.append(impares[-1] + x % 2)
    return valores, impares


def representante(palabra):
    a, b, modulo = 1, 0, 1
    for bit in palabra:
        if bit == '1':
            a, b = 3 * a, 3 * b + modulo
        modulo *= 2
    return (-b * pow(a, -1, modulo)) % modulo


def verificar_palabra(valores):
    x, d = valores[0], len(valores) - 1
    assert x > 0
    l = (x + 4).bit_length()
    assert 2 ** (l - 1) < x + 5 <= 2 ** l
    bits = ''.join(str(y % 2) for y in valores[:-1])
    grupos = [(bit, len(list(g))) for bit, g in groupby(bits)]
    assert not bits or bits.startswith('1') and bits.endswith('0')
    bloques = [(grupos[i][1], grupos[i + 1][1]) for i in range(0, len(grupos), 2)]
    tiempos, excepciones, ultima = [0], 0, 0
    for a, b in bloques:
        t = tiempos[-1]
        assert (valores[t] + 1) % 2 ** a == 0
        assert 2 ** b * valores[t + a + b] == valores[t + a]
        assert a <= l + t and b <= l + t + a
        assert t + a + b + l <= 4 * (t + l)
        tiempos.append(t + a + b)
        if (a, b) != (2, 1):
            excepciones += 1
            ultima = len(tiempos) - 1
        assert tiempos[ultima] + l <= 8 ** excepciones * l
        assert all(par == (2, 1) for par in bloques[ultima:len(tiempos) - 1])
        assert tiempos[-1] + l <= 2 * (tiempos[ultima] + l)
        assert tiempos[-1] + l <= 2 * 8 ** excepciones * l
    assert tiempos[-1] == d
    assert excepciones == sum(par != (2, 1) for par in bloques)
    cadenas = 0
    for bueno, grupo in groupby(enumerate(bloques), key=lambda z: z[1] == (2, 1)):
        indices = [i for i, _ in grupo]
        if bueno:
            j, k = tiempos[indices[0]], len(indices)
            final = tiempos[indices[-1] + 1]
            assert final - j == 3 * k
            assert (valores[j] + 5) % 8 ** k == 0
            assert 8 ** k * (valores[final] + 5) == 9 ** k * (valores[j] + 5)
            assert 3 * k <= l + j and final + l <= 2 * (j + l)
            cadenas += 1
    assert all(y + 5 <= 2 ** j * (x + 5) <= 2 ** (l + j)
               for j, y in enumerate(valores))
    assert d + l <= 2 * 8 ** excepciones * l
    return dict(excepciones=excepciones, bloques=len(bloques), cadenas=cadenas, l=l)


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--n-max', type=int, required=True)
    analizador.add_argument('--pasos', type=int, required=True)
    analizador.add_argument('--nivel-max', type=int, required=True)
    analizador.add_argument('--cadena-max', type=int, required=True)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    assert args.n_max >= 2 and args.pasos >= 1 and args.nivel_max >= 0 and args.cadena_max >= 0
    cuentas = dict(intervalos=0, unitarios=0, bloques_orbitales=0, cadenas_orbitales=0,
                   cotas_cuadradas=0, configuraciones_modulares=0, palabras_distintas=0,
                   bloques_modulares=0, cadenas_modulares=0, familia_anterior=0)
    ejemplos, maximo = [], -1
    for n in range(2, args.n_max + 1):
        valores, impares = orbita(n, args.pasos)
        fin = next((j for j, s in enumerate(impares) if 3 ** s < 2 ** j), len(valores))
        for c in range(args.nivel_max + 1):
            visitas = [j for j in range(fin) if 3 ** impares[j] <= 3 ** c * 2 ** j]
            for u, v in zip(visitas, visitas[1:]):
                if v == u + 1:
                    dato = dict(excepciones=0, bloques=0, cadenas=0)
                    cuentas['unitarios'] += 1
                else:
                    dato = verificar_palabra(valores[u:v + 1])
                e = dato['excepciones']
                for h in (e, e + 1):
                    constante = (12 * 8 ** h) ** 2 * (3 ** c * n) ** 6 + 1
                    assert (v - u) ** 2 <= constante * (u + 1)
                    cuentas['cotas_cuadradas'] += 1
                cuentas['intervalos'] += 1
                cuentas['bloques_orbitales'] += dato['bloques']
                cuentas['cadenas_orbitales'] += dato['cadenas']
                if e > maximo:
                    maximo = e
                    ejemplos.append(dict(n=n, c=c, u=u, v=v, h=dato['bloques'], excepciones=e))
    # Una excepción al principio, al final o entre dos cadenas; incluye
    # también (2,1), que no debe incrementar el contador.
    longitudes = sorted({0, min(1, args.cadena_max), min(2, args.cadena_max),
                         min(8, args.cadena_max), args.cadena_max})
    palabras = set()
    for p, q, (a, b) in product(longitudes, longitudes, [(1, 1), (2, 2), (3, 1), (1, 4), (8, 1), (2, 1)]):
        palabra = '110' * p + '1' * a + '0' * b + '110' * q
        palabras.add(palabra)
        n = representante(palabra)
        valores, _ = orbita(n, len(palabra))
        assert ''.join(str(x % 2) for x in valores[:-1]) == palabra
        dato = verificar_palabra(valores)
        assert dato['excepciones'] == int((a, b) != (2, 1))
        cuentas['configuraciones_modulares'] += 1
        cuentas['bloques_modulares'] += dato['bloques']
        cuentas['cadenas_modulares'] += dato['cadenas']
    cuentas['palabras_distintas'] = len(palabras)
    # Reutiliza sólo los cinco ejemplos publicados; no repite su censo.
    anterior = json.loads(Path(__file__).with_name('cotejo_balance.json').read_text(encoding='utf-8'))
    for ejemplo in anterior['ejemplos']:
        valores, _ = orbita(ejemplo['n'], ejemplo['v'])
        dato = verificar_palabra(valores[ejemplo['u']:])
        assert dato['excepciones'] == 1 and dato['bloques'] == ejemplo['h']
        assert ejemplo['v'] - ejemplo['u'] <= 15 * dato['l']
        cuentas['familia_anterior'] += 1
    # Bordes del lema general: palabra vacía y órbita positiva periódica.
    assert verificar_palabra([1])['excepciones'] == 0
    valores, impares = orbita(1, 32)
    dato = verificar_palabra(valores)
    assert dato['excepciones'] == 16
    assert 32 + dato['l'] > 2 * dato['l']  # Ignorar excepciones da una cota falsa.
    assert 3 ** impares[2] < 2 ** 2  # No confundir este borde con FugaPura.
    resultado = dict(estado='contraste finito exacto; no certifica FugaPura ni infinitos regresos',
                     parametros={k: v for k, v in vars(args).items() if k != 'salida'},
                     sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                     cuentas=cuentas, maximo_excepciones=maximo, ejemplos=ejemplos,
                     fuente_ejemplos_sha256_lf=hashlib.sha256(Path(__file__).with_name('cotejo_balance.json').read_text(encoding='utf-8').encode('utf-8')).hexdigest())
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(cuentas, ensure_ascii=False))


if __name__ == '__main__':
    main()
