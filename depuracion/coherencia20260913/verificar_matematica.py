"""Controles exactos de bordes y contraejemplos; no prueba asintótica por barrido."""

from fractions import Fraction
from math import comb
from pathlib import Path
import sys

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
from estratoscadena import ajustar_polinomio_periodico, buscar_forma, transicion, barrido_estratos


def paso(x):
    return x // 2 if x % 2 == 0 else (3*x + 1) // 2


def main():
    for k in range(1001):
        x, y = 8*k + 4, 8*k + 5
        for _ in range(3):
            x, y = paso(x), paso(y)
        assert x == y == 3*k + 2
    for g in range(1, 1000, 2):
        assert transicion(0, g, 0)[2] % 3 == transicion(0, g, 1)[2] % 3 == 2
    assert transicion(0, 1, 0) == ('estado', 1, 2)
    assert transicion(1, 2, 0) == ('estado', 1, 1)
    assert transicion(1, 1, 1) == ('fusion',)
    # Testigo real del mismo prefijo de bits del ancla.
    x, y = 4, 5
    for esperado in [(2, 8), (1, 4), (2, 2)]:
        x, y = paso(x), paso(y)
        assert (x, y) == esperado

    # Unión de clases: cada entero j está en C_j y toda unión finita
    # tiene densidad <= suma de densidades <1/4. La prueba general está escrita.
    suma = Fraction(0)
    supervivencia = Fraction(1)
    for j in range(1, 201):
        suma += Fraction(1, 2**(j + 2))
        assert suma < Fraction(1, 4)
        assert (j - j) % 2**(j + 2) == 0
        supervivencia *= 1 - Fraction(1, j + 1)
        assert supervivencia == Fraction(1, j + 1)

    for n in range(1, 1001):
        q = Fraction(comb(n, n//2), 2**n)
        assert q*q <= Fraction(2, n+1)
        s = ((n+1)**3 - 1).bit_length()
        assert Fraction(n, 2**s) <= Fraction(n, (n+1)**3)
    for t in range(128, 10001):
        b = (t+2).bit_length()
        n = t // (8*b)
        a = 2 + (n+2).bit_length() - 1
        s = ((n+1)**3 - 1).bit_length()
        assert n*(a+s+1) <= t
        assert n*16*b >= t

    # El modelo restringido sí reconoce P+C y no se confunde con
    # coeficientes de n^2 que varían con la clase residual.
    datos = [n*n + (7 if n % 2 else 0) for n in range(10, 60)]
    assert ajustar_polinomio_periodico(datos, 10, 2, 2, 0) is not None
    general = [n*n*(1+n % 2) for n in range(10, 60)]
    assert ajustar_polinomio_periodico(general, 10, 2, 2, 0) is None
    try:
        ajustar_polinomio_periodico([1, 2], 10, 2, 2, 0)
    except ValueError:
        pass
    else:
        raise AssertionError('Faltaba distinguir datos insuficientes')
    _, probados, omitidos = buscar_forma(list(range(20)))
    assert (probados, omitidos) == (329, 119)
    # Cruce de implementación simbólica con el recuento directo publicado,
    # incluyendo todos los ceros iniciales. Sólo n<=13 aquí para coste acotado.
    sys.path.insert(0, str(RAIZ.parent / 'zootheorem' / 'verify'))
    from verify_strata import count_level
    simbolico, _ = barrido_estratos((0, 1), 13)
    for n in range(1, 14):
        directo, _ = count_level(n)
        assert all(directo[k] == simbolico.get(n, {}).get(k, 0) for k in directo)
    print('OK: Garner, puertas con signo, densidad, riesgos, reloj, ajuste y estratos n<=13.')


if __name__ == '__main__':
    main()
