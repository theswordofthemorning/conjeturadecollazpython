"""Mangostas: ley exacta de la duracion compartida, no solo v2 de entrada.

Controles sin filtros y mezcla tras un mixto vivo. Reutiliza el DP local;
el cruce con pares usa otro calculo, pero NO es una revision ciega.
"""

import argparse
from collections import Counter
from fractions import Fraction
from itertools import product

from contraccion import avanzar, control_pares, control_palabras, hijos


def v2(n):
    if n == 0:
        raise ValueError("v2(0) no es finita: usar nivel para incluir cero")
    n = abs(n)
    return (n & -n).bit_length()-1


def nivel(c, a):
    return a if c == 0 else min(v2(c), a)


def cola(a, r, j):
    if r < a:
        return Fraction(int(j <= r))
    return Fraction(1, 2**max(0, j-a))


def cuenta(a, r, n):
    if r < a:
        return 2**n if n < r else 0
    return 2**n if n < a else 2**(a-1)


def avanzar_compartidos(k, estados):
    nuevos = Counter()
    for c, peso in estados.items():
        assert c % 2 == 0
        for altura, hijo in hijos(k, c):
            assert altura == k
            if hijo % 2 == 0:
                nuevos[hijo] += peso
    return nuevos


def controles():
    celdas = 0
    for k in range(2, 17):
        a = v2(3**k-1)
        assert a == (1 if k % 2 else 2+v2(k))
        semillas = sorted(set(range(-63, 65)) | {3**k-1, 2**21, 2**a*(2**12+1)})
        for c in semillas:
            r = nivel(c, a)
            estados = Counter({c: 1}) if c % 2 == 0 else Counter()
            for n in range(17):
                real = sum(estados.values())
                assert real == cuenta(a, r, n), (k, c, n)
                assert Fraction(real, 2**n) == cola(a, r, n+1)
                estados = avanzar_compartidos(k, estados)
                celdas += 1
    print(f"CONTROL: {celdas} celdas (k=2..16, signos, cero, recargas y alturas grandes): OK.")

    # Cruce por pares positivos y palabras, sin hijos/avanzar_compartidos.
    casos = 0
    for k, c0 in product((2, 3, 4, 8), (0, 2, 8, 2**21)):
        siguen = 0
        for palabra in product((0, 1), repeat=10):
            c = c0
            for bit in palabra:
                if c % 2:
                    break
                v = 2*(abs(c)+1)+bit
                w = 3**k*v+c
                tv = v//2 if v % 2 == 0 else (3*v+1)//2
                tw = w//2 if w % 2 == 0 else (3*w+1)//2
                c = tw-3**k*tv
            else:
                siguen += c % 2 == 0
        a = v2(3**k-1)
        assert siguen == cuenta(a, nivel(c0, a), 10)
        casos += 1
    print(f"CONTROL: {casos} arranques x 1024 palabras, por pares positivos: OK.")
    assert hijos(2, 1398101)[0] == (3, 2**21)
    assert hijos(3, 2**21)[1][1] % 2 == 1
    assert cola(1, 1, 21) == Fraction(1, 2**20)
    print("ADV: tras bit 0, h=2^21 a k=3; P(L>=21)=1/1048576, NO 1.")


def medir_entrada(estados, j_max):
    grupos = Counter()
    entrada = Counter()
    for (k, c), peso in estados.items():
        if c % 2:
            for hijo in hijos(k, c):
                if hijo is not None:
                    entrada[hijo] += peso
    if not entrada:
        return None
    for (k, c), peso in entrada.items():
        a = v2(3**k-1)
        grupos[a, nivel(c, a)] += peso
    total = sum(grupos.values())
    a_max = max(a for a, _ in grupos)
    prefactor = Fraction(sum(n*2**a for (a, r), n in grupos.items() if r == a), total)
    peor = (Fraction(0), 0)
    for j in range(1, j_max+1):
        prob = sum((n*cola(a, r, j) for (a, r), n in grupos.items()), Fraction(0))/total
        breve = sum(n for (a, r), n in grupos.items() if a >= j and r >= j)
        largo = sum(n*2**a for (a, r), n in grupos.items() if a < j and r == a)
        normalizado = prob*2**j
        assert normalizado == Fraction(2**j*breve+largo, total)
        if j > a_max:
            assert normalizado == prefactor
        if normalizado > peor[0]:
            peor = normalizado, j
    # Reproduce la mezcla durante cinco bits futuros por la cadena entera.
    pendientes = Counter({(k, c): n for (k, c), n in entrada.items() if c % 2 == 0})
    for n in range(6):
        esperado = sum(peso*cuenta(a, r, n) for (a, r), peso in grupos.items())
        assert sum(pendientes.values()) == esperado
        nuevos = Counter()
        for (k, c), peso in pendientes.items():
            for kk, cc in hijos(k, c):
                if cc % 2 == 0:
                    nuevos[kk, cc] += peso
        pendientes = nuevos
    return total, a_max, prefactor, peor


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--pasos", type=int, default=20)
    p.add_argument("--semillas", type=int, nargs="+", default=[1, 5, 999983, 1398101])
    p.add_argument("--j-max", type=int, default=32)
    args = p.parse_args()
    if not 8 <= args.pasos <= 24 or args.j_max < 1:
        p.error("Tanda acotada: pasos 8..24; j-max positivo")
    control_pares()
    controles()
    print("MEZCLA: condicionada a c impar ahora y a la proxima rama mixta viva;")
    print("no condicionada a supervivencia futura; fracciones exactas, sin filtro de granularidad.")
    for semilla in args.semillas:
        estados = Counter({(2, semilla): 1})
        for t in range(args.pasos+1):
            if t == 8:
                control_palabras(semilla, 8, estados)
            if t >= 8 and (t % 4 == 0 or t == args.pasos):
                medido = medir_entrada(estados, args.j_max)
                if medido is not None:
                    total, a_max, prefactor, (peor, j) = medido
                    print(f"c0={semilla} t={t} entradas={total} Amax={a_max} "
                          f"C_cola={prefactor} (~{float(prefactor):.6f}) "
                          f"max_C_j={float(peor):.6f} en j={j}", flush=True)
            if t < args.pasos:
                estados, _ = avanzar(estados)
    print("FIN: ley de una racha verificada; los prefactores de mezclas son mediciones finitas.")


if __name__ == "__main__":
    main()
