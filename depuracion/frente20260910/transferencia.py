"""Gacelas: cambio armonico, supervivencia futura y multiplicadores.

Fracciones y conteos enteros. Cruces locales, no revision externa ciega.
"""

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import comb

from contraccion import avanzar, control_pares, control_palabras, hijos


@lru_cache(None)
def supervivientes(k, c, t):
    if t == 0:
        return 1
    return sum(supervivientes(*z, t-1) for z in hijos(k, c) if z is not None)


def avanzar_armonica(ley):
    nueva = defaultdict(F)
    for (k, c), peso in ley.items():
        for z in hijos(k, c):
            if z is not None:
                nueva[z] += peso*F(z[0]-1, 2*(k-1))
    return dict(nueva)


def balota(t):
    return F(comb(t, t//2), 2**t)


def controles_binomiales():
    paseo = Counter({1: 1})
    for t in range(201):
        assert F(sum(paseo.values()), 2**t) == balota(t)
        assert balota(t)**2*(2*t+3) >= 1
        nuevo = Counter()
        for h, n in paseo.items():
            nuevo[h+1] += n
            if h > 1:
                nuevo[h-1] += n
        paseo = nuevo
    for t in range(401):
        # Producto > (31/32)^t equivale a 3^o * 16^t > 31^t.
        malos = sum(comb(t, o) for o in range(t+1) if 3**o*16**t > 31**t)
        assert F(malos, 2**t)**2 <= F(30, 31)**t
    assert 4*62**2*61**2048*(2*1024+3) <= 62**2048
    print("CONTROL: balota t=0..200; cola binomial t=0..400; umbral T=1024: OK.")


def control_perpetuidad():
    casos = 0
    for c0 in (-5, 0, 1, 5, 999983, 1398101):
        for palabra in product((0, 1), repeat=8):
            k, c = 2, c0
            multiplicador, w = F(1), F(0)
            for bit in palabra:
                anterior_k, anterior_c = k, c
                # Evolucion por pares positivos, sin hijos().
                v = 2*(abs(c)+1)+bit
                z = 3**k*v+c
                tv = v//2 if v % 2 == 0 else (3*v+1)//2
                tz = z//2 if z % 2 == 0 else (3*z+1)//2
                if c % 2:
                    k += 1 if bit == 0 else -1
                c = tz-3**k*tv
                a = F(1+2*bit, 2)
                if anterior_c % 2 == 0:
                    delta = F(0) if bit == 0 else (F(1, 3**anterior_k)-1)/2
                else:
                    delta = F(1, 2*3**k) if bit == 0 else F(-1, 2)
                multiplicador *= a
                w = a*w+delta
                assert F(c, 3**k) == multiplicador*F(c0, 9)+w
                if k == 1:
                    break
            casos += 1
    print(f"CONTROL: descomposicion u=producto*u0+W por pares: {casos} palabras: OK.")


def investigar(c0, pasos):
    estados = Counter({(2, c0): 1})
    armonica = {(2, c0): F(1)}
    for t in range(pasos+1):
        assert sum(n*(k-1) for (k, _), n in estados.items()) == 2**t
        assert sum(armonica.values()) == 1
        assert armonica == {z: F(n*(z[0]-1), 2**t) for z, n in estados.items()}
        assert F(sum(estados.values()), 2**t) >= balota(t)
        if t == 8:
            control_palabras(c0, 8, estados)
        if t < pasos:
            estados, _ = avanzar(estados)
            armonica = avanzar_armonica(armonica)
    # Condicionamiento al horizonte FUTURO 12, prefijo de seis pasos.
    horizonte, prefijo = 12, 6
    estados = Counter({(2, c0): 1})
    for _ in range(prefijo):
        estados, _ = avanzar(estados)
    total = supervivientes(2, c0, horizonte)
    masa = F(0)
    for (k, c), n in estados.items():
        restantes = supervivientes(k, c, horizonte-prefijo)
        condicionada = F(n*restantes, total)
        q = F(n*(k-1), 2**prefijo)
        densidad = F(restantes, 2**(horizonte-prefijo))/((k-1)*F(total, 2**horizonte))
        assert condicionada == q*densidad
        masa += condicionada
    assert masa == 1
    print(f"c0={c0}: ley P y Q hasta t={pasos}, puente r=6,T=12: OK; S12={F(total, 2**12)}")
    supervivientes.cache_clear()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--pasos", type=int, default=16)
    p.add_argument("--semillas", type=int, nargs="+", default=[-5, 0, 1, 5, 999983, 1398101])
    args = p.parse_args()
    if not 8 <= args.pasos <= 20:
        p.error("Tanda acotada: pasos 8..20")
    control_pares()
    controles_binomiales()
    control_perpetuidad()
    for c0 in args.semillas:
        investigar(c0, args.pasos)
    s4 = F(supervivientes(2, 0, 4), 16)
    bit0 = F(supervivientes(2, 0, 3), 16)/s4
    assert s4 == F(3, 4) and bit0 == F(2, 3)
    print(f"ADV (2,0), tau>4: S4={s4}, P(bit0|tau>4)={bit0}; bajo Q es 1/2.")
    print("FIN: no se identifica Q con el limite condicionado ni se acota W en la salida.")


if __name__ == "__main__":
    main()
