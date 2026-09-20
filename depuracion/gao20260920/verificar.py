"""Controles exactos del candidato: no certifican la probabilidad infinita.

No importa experimentos históricos. Todos los barridos están en main.
"""

import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import product
import json
from math import comb, isqrt
from pathlib import Path
import sys

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
from estratoscadena import transicion


def atajo(x):
    return x // 2 if x % 2 == 0 else (3 * x + 1) // 2


def por_par(k, c, bit):
    """Reconstrucción mediante dos enteros positivos y sus imágenes."""
    v = 2 * (abs(c) + 1) + bit
    w = 3**k * v + c
    a, b = atajo(v), atajo(w)
    if c % 2 == 0:
        nuevo_k = k
        nuevo_c = b - 3**nuevo_k * a
    elif k == 0:
        nuevo_k = 1
        nuevo_c = b - 3*a if bit == 0 else a - 3*b
    elif bit == 0:
        nuevo_k = k + 1
        nuevo_c = b - 3**nuevo_k * a
    elif k == 1:
        if a == b:
            return ('fusion',)
        nuevo_k, nuevo_c = 0, abs(b - a)
    else:
        nuevo_k = k - 1
        nuevo_c = b - 3**nuevo_k * a
    return ('estado', nuevo_k, nuevo_c)


def controles_transicion():
    casos = 0
    semillas = set(range(-256, 257))
    for e in (16, 31, 64, 127):
        for base in (2, 3):
            for signo in (-1, 1):
                for vecino in (-1, 0, 1):
                    semillas.add(signo * base**e + vecino)
    for k in range(13):
        for c in sorted(semillas):
            if k == 0 and c <= 0:
                continue
            for bit in (0, 1):
                hijo = transicion(k, c, bit)
                assert hijo == por_par(k, c, bit), (k, c, bit)
                u = F(c, 3**k)
                u2 = F(0) if hijo[0] == 'fusion' else F(hijo[2], 3**hijo[1])
                assert abs(u2) <= F(1 + 2*bit, 2)*abs(u) + F(1, 2)
                casos += 1
    return casos


def control_cilindros(n):
    """Cada palabra de ancla aparece una vez; cruce con las dos órbitas."""
    palabras = set()
    fusiones = 0
    for r in range(2**n):
        a = 3*2**n + r
        b = a + 1
        impares_a = impares_b = 0
        ancla_a = True
        estado = ('estado', 0, 1)
        palabra = 0
        absorbido = False
        for t in range(n):
            bit = (a if ancla_a else b) % 2
            palabra |= bit << t
            impares_a += a % 2
            impares_b += b % 2
            a, b = atajo(a), atajo(b)
            if not absorbido:
                _, k, c = estado
                hijo = transicion(k, c, bit)
                if hijo[0] == 'fusion':
                    assert a == b and impares_a == impares_b
                    absorbido = True
                else:
                    if k == 0 and c % 2 and bit == 1:
                        ancla_a = not ancla_a
                    elif k == 1 and c % 2 and bit == 1:
                        ancla_a = a <= b
                    _, k2, c2 = hijo
                    v, w = (a, b) if ancla_a else (b, a)
                    sa, sb = (impares_a, impares_b) if ancla_a else (impares_b, impares_a)
                    assert sb - sa == k2
                    assert w == 3**k2*v + c2
                estado = hijo
            assert absorbido == (a == b and impares_a == impares_b)
        assert palabra not in palabras
        palabras.add(palabra)
        fusiones += absorbido
    assert len(palabras) == 2**n
    return {'nivel': n, 'palabras': len(palabras), 'fusiones': fusiones}


def politica(k, c):
    if k == 0:
        return 0 if c == 1 or c % 2 == 0 else 1
    return 1 if c == 0 or c % 2 else 0


def longitud(c):
    m = (abs(c) + 1).bit_length()
    cota = 16*(m + 1)**2
    estado = ('estado', 1, c)
    for t in range(1, cota + 1):
        _, k, d = estado
        estado = por_par(k, d, politica(k, d))
        if estado[0] == 'fusion':
            return t, cota
    raise AssertionError(('Politica sin fusion en su cota', c, cota))


def controles_politica():
    semillas = set(range(-4096, 4097))
    for e in (16, 32, 64, 128, 512, 1024):
        for base in (2, 3):
            for signo in (-1, 1):
                for vecino in (-1, 0, 1):
                    semillas.add(signo * base**e + vecino)
    peor = (0, 0)
    for c in semillas:
        largo, cota = longitud(c)
        assert largo <= cota
        if largo > peor[1]:
            peor = (c, largo)
    return {'casos': len(semillas), 'max_longitud': peor[1],
            'bits_semilla_maxima': abs(peor[0]).bit_length()}


def control_rachas(pasos):
    casos = 0
    for c0 in (-2**64, -32, -2, 0, 2, 32, 2**64):
        vivos = Counter({c0: 1})
        for n in range(pasos + 1):
            # Para c0 par en k=1, P(L>n)=2^-n.
            assert sum(vivos.values()) == 1
            nuevo = Counter()
            for c, peso in vivos.items():
                for bit in (0, 1):
                    hijo = por_par(1, c, bit)
                    assert hijo[1] == 1
                    if hijo[2] % 2 == 0:
                        nuevo[hijo[2]] += peso
                    casos += 1
            vivos = nuevo
    return casos


def control_w(pasos):
    casos = 0
    for c0 in (-3**32-1, -17, -1, 0, 1, 2, 17, 2**64+1):
        for palabra in product((0, 1), repeat=pasos):
            k, c = 2, c0
            pi, w = F(1), F(0)
            fuera = False
            for bit in palabra:
                a = F(1+2*bit, 2)
                if fuera:
                    w *= a
                    continue
                antes = F(c, 3**k)
                hijo = por_par(k, c, bit)
                _, k, c = hijo
                despues = F(c, 3**k)
                delta = despues - a*antes
                assert abs(delta) <= F(1, 2)
                pi *= a
                w = a*w + delta
                assert despues == pi*F(c0, 9)+w
                fuera = k == 1
            casos += 1
    return casos


def parametros(c):
    t = 32*max(32, (abs(c)+1).bit_length())
    n = 256*(t+1)**2
    a = 1+(n+2).bit_length()
    s = 3*n.bit_length()
    h = n*(a+s+1)
    q = isqrt(2*t+3)+1
    r = (128*(h+1)*q)**2
    return t, n, s, h, q, r


def controles_constantes():
    assert 2*31**32 < 32**32
    assert 16*62**2*61**2048*2051 <= 62**2048
    assert 2*5**4 < 6**4
    for m in range(500):
        q = F(comb(2*m, m), 4**m)
        assert q*q*(m+1) <= 1
    filas = []
    for c in (0, 1, -1, 2**32, -3**128, 2**4096):
        t, n, s, h, q, r = parametros(c)
        assert n+1 >= 128*(2*t+3)
        assert n**4 >= 64*(2*t+3)
        assert 2**s >= (n+1)**3
        assert F(31, 32)**t * max(F(1), F(abs(c), 9)) <= 1
        assert q*q >= 2*t+3
        assert 4*32*(h+1)*q == isqrt(r)
        filas.append({'bits_c': abs(c).bit_length(), 'T': t, 'H': h,
                      'bits_G': (3*(r+1)).bit_length()})
    return filas


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--nivel', type=int, default=12)
    p.add_argument('--salida', type=Path)
    args = p.parse_args()
    if not 3 <= args.nivel <= 16:
        p.error('nivel permitido: 3..16')
    resultado = {'transiciones': controles_transicion(),
                 'cilindros': [control_cilindros(n) for n in range(3, args.nivel+1)],
                 'politica': controles_politica(),
                 'rachas_k1': control_rachas(64),
                 'palabras_w': control_w(9),
                 'parametros': controles_constantes(),
                 'alcance': 'Controles finitos exactos; no prueba universal del ensamblaje.'}
    texto = json.dumps(resultado, ensure_ascii=False, indent=2)
    if args.salida:
        args.salida.write_text(texto+'\n', encoding='utf-8')
    print(texto)


if __name__ == '__main__':
    main()
