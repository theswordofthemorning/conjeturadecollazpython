# Prueba por casos de que ningún par m, m+1 (m >= 1) se encuentra por primera vez
# tras exactamente 4 pasos de C (x/2 si par, 3x+1 si impar).
# En la clase m = 64*t + r, cada iterado es una función afín A*t + B de t mientras
# A sea par (la paridad queda fijada por B). Igualar dos funciones afines da o una
# identidad en toda la clase o a lo sumo un t; se resuelven todos los casos.
# Uso: python -B -X utf8 sin_cuatro.py --modulo 64
import argparse
from fractions import Fraction


def C(x):
    return x // 2 if x % 2 == 0 else 3 * x + 1


def pasos_afines(A, B, k):
    # Devuelve la lista de (A, B) de los iterados 0..k; falla si la paridad no queda fijada.
    lista = [(A, B)]
    for _ in range(k):
        if A % 2:
            raise ValueError('paridad no determinada')
        if B % 2 == 0:
            A, B = A // 2, B // 2
        else:
            A, B = 3 * A, 3 * B + 1
        lista.append((A, B))
    return lista


def primer_encuentro(m):
    x, y, k = m, m + 1, 0
    while x != y:
        x, y, k = C(x), C(y), k + 1
    return k


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--modulo', type=int, required=True)
    q = p.parse_args().modulo
    candidatos = set()
    clases_enteras = []
    for r in range(q):
        u = pasos_afines(q, r, 4)
        v = pasos_afines(q, r + 1, 4)
        (a1, b1), (a2, b2) = u[4], v[4]
        if a1 == a2:
            if b1 == b2:
                clases_enteras.append(r)
            continue
        t = Fraction(b2 - b1, a1 - a2)
        if t.denominator == 1 and t >= 0:
            candidatos.add(q * int(t) + r)
    print('clases con C^4(m) = C^4(m+1) idénticamente:', clases_enteras)
    print('soluciones aisladas:', sorted(candidatos))
    malos = [r for r in clases_enteras if primer_encuentro(q * 1000 + r) == 4]
    malos += [m for m in candidatos if m >= 1 and primer_encuentro(m) == 4]
    # En una clase entera, si C^3 no coincide idénticamente, el primer encuentro es 4 salvo en un t a lo sumo:
    # basta mirar un representante genérico (t = 1000).
    print('m con primer encuentro exactamente 4:', malos)
    print('OK' if not malos else 'FALLO')


if __name__ == '__main__':
    main()
