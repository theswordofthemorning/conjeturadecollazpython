"""Sondeo: rachas largas de consecutivos con la misma altura, desde la fusion por clases.

Ruta de Garner (1985); plan en LEEME.md de esta carpeta. Nada de esto es una prueba.

Atajo T(x) = x/2 si es par, (3x+1)/2 si es impar. Para n = 2^t*u + r, tras t pasos
T^t(n) = 3^a*u + A, con a y A que solo dependen de r (Terras). El par (r, r+1) esta
"fusionado por clases hasta t" si los dos dan el mismo (a, A): entonces n y n+1
coinciden para TODO u.

Idea: si r, r+1, ..., r+L estan fusionados de dos en dos, todos los n = 2^t*u + r + i
comparten 3^a*u + A tras t pasos. Eligiendo u con 3^a*u + A = 2^m, todos llegan a 2^m
a la vez y luego a 1: misma altura y mismo numero de divisiones por 2.

Para cada t se toma la racha mas larga de pares fusionados, se construye u y se
calcula la altura de cada numero iterando de verdad (enteros de Python, sin limite).

Uso: python -B -X utf8 sondeo_rachas.py   (unos segundos)
"""

import numpy as np

T_MAX = 20          # se prueban t = 2..T_MAX (con t=20 salen rachas de 23)
TOPE_M = 4000       # se busca m < TOPE_M con 2^m == A (mod 3^a); si no hay, se omite


def clases(t):
    """(a, A) de cada residuo r mod 2^t, en vectores."""
    r = np.arange(2**t, dtype=np.int64)
    d = r.copy()          # parte constante (valores exactos: caben en int64 para t<=22)
    a = np.zeros(2**t, dtype=np.int64)
    for _ in range(t):
        impar = (d % 2 == 1)
        d = np.where(impar, (3 * d + 1) // 2, d // 2)
        a += impar
    return a, d


def racha_mas_larga(fusion):
    """Longitud y comienzo de la racha mas larga de True seguidos."""
    mejor, inicio, actual = 0, 0, 0
    for i, v in enumerate(fusion):
        actual = actual + 1 if v else 0
        if actual > mejor:
            mejor, inicio = actual, i - actual + 1
    return mejor, inicio


def altura(n):
    """Pasos del mapa clasico hasta 1, y cuantos de ellos dividen por 2."""
    pasos, mitades = 0, 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
            mitades += 1
        else:
            n = 3 * n + 1
        pasos += 1
    return pasos, mitades


def main():
    ok = True
    print(' t   pares fusionados   racha de pares   numeros en la racha')
    for t in range(2, T_MAX + 1):
        a, A = clases(t)
        fusion = (a[:-1] == a[1:]) & (A[:-1] == A[1:])     # par (r, r+1), r < 2^t - 1
        L, r0 = racha_mas_larga(fusion)
        print(f'{t:2d}   {fusion.mean():.4f}             {L:3d}              {L + 1 if L else 0}')
        if L == 0:
            continue
        # construir u con 3^a*u + A = 2^m, m >= 3
        aa, AA = int(a[r0]), int(A[r0])
        modulo = 3**aa
        candidatos = [m for m in range(3, TOPE_M)
                      if pow(2, m, modulo) == AA % modulo and 2**m >= AA]
        if not candidatos:
            print(f'      sin m < {TOPE_M} con 2^m = A (mod 3^{aa}); se omite')
            continue
        m = candidatos[0]
        u = (2**m - AA) // modulo
        base = 2**t * u + r0
        datos = [altura(base + i) for i in range(L + 1)]
        iguales = len(set(datos)) == 1
        # control: el numero justo antes y justo despues de la racha
        fuera = [altura(base - 1), altura(base + L + 1)]
        print(f'      n = 2^{t}*u + {r0}, u con {len(str(u))} cifras; {L + 1} consecutivos'
              f' con (altura, mitades) = {datos[0]}: {"IGUALES" if iguales else "DISTINTOS"};'
              f' vecinos {fuera}')
        ok = ok and iguales
    print('OK' if ok else 'FALLO')
    return ok


if __name__ == '__main__':
    raise SystemExit(0 if main() else 1)
