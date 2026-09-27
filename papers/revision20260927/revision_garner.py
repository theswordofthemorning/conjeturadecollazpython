"""Revision adversarial del 27-09-2026: Garner (1985), con codigo nuevo.

No importa nada del laboratorio. Construye rachas de L+1 consecutivos con la
misma altura por un camino distinto al de verificar_alpacas.py:

1. Busca, iterando el atajo T(x) = x/2 o (3x+1)/2 sobre todos los residuos
   r < 2^t, un bloque de L pares (r+i, r+i+1) que tras t pasos de T tienen
   el mismo valor y el mismo numero de pasos impares.
2. Toma a (pasos impares) y A = T^t(r). Comprueba que 3 no divide a A.
3. Busca m con 2^m = A (mod 3^a) por fuerza bruta, sin usar que 2 sea raiz
   primitiva, y lo repite con dos periodos mas.
4. Con u = (2^m - A)/3^a y n = 2^t*u + r, calcula de verdad, iterando el
   mapa clasico C con enteros grandes, la altura y las divisiones por 2
   (sigma_inf) de n, ..., n+L.

Ademas coteja la definicion de altura con OEIS A078441 (primer comienzo de
n consecutivos con la misma altura) y con la tabla 1 de Gao.

Uso: python -B -X utf8 revision_garner.py
"""

import numpy as np

L_MAX = 16             # rachas de L+1 consecutivos para L = 1..L_MAX
T_MAX = 22             # se prueban t = 1..T_MAX
TOPE_A078441 = 2 ** 20

# OEIS A078441, a(1)..a(40), leido el 27-09-2026
A078441 = [1, 12, 28, 98, 98, 386, 943, 1494, 1680, 2987, 2987, 2987, 2987,
           2987, 7083, 7083, 7083, 57346, 57346, 57346, 57346, 57346, 57346,
           57346, 57346, 252548, 252548, 331778, 331778, 524289, 596310,
           596310, 596310, 596310, 596310, 596310, 596310, 596310, 596310,
           596310]

# Tabla 1 de Gao (pag. 263): (largo, comienzo, altura, sigma_inf)
TABLA1_GAO = [(7, 943, 36, 26), (17, 7083, 57, 40), (25, 57346, 78, 54),
              (40, 596310, 97, 67), (65, 5772712, 214, 140),
              (98, 98041684, 169, 114), (176, 722067240, 190, 128),
              (349, 9749626154, 248, 165)]


def altura_y_mitades(n):
    """Pasos del mapa clasico hasta llegar a 1, y cuantos fueron n/2."""
    pasos = 0
    mitades = 0
    while n != 1:
        if n % 2 == 0:
            n = n // 2
            mitades += 1
        else:
            n = 3 * n + 1
        pasos += 1
    return pasos, mitades


def atajo_t_pasos(t, cuantos):
    """T^t(r) y cuantos pasos impares, para r = 0..cuantos-1."""
    x = np.arange(cuantos, dtype=np.int64)
    impares = np.zeros(cuantos, dtype=np.int64)
    for _ in range(t):
        impar = (x % 2 == 1)
        x = np.where(impar, (3 * x + 1) // 2, x // 2)
        impares += impar
    return x, impares


def buscar_bloque(L):
    """Menor t y menor r con L pares fusionados seguidos y r + L < 2^t."""
    for t in range(1, T_MAX + 1):
        cuantos = 2 ** t + 1
        valor, impares = atajo_t_pasos(t, cuantos)
        fusion = ((valor[:-1] == valor[1:]) & (impares[:-1] == impares[1:])).tolist()
        # largo[r] = cuantos pares seguidos, desde (r, r+1), estan fusionados
        largo = [0] * (2 ** t + 1)
        for r in range(2 ** t - 1, -1, -1):
            largo[r] = largo[r + 1] + 1 if fusion[r] else 0
        for r in range(0, 2 ** t - L):
            if largo[r] >= L:
                return t, r, int(valor[r]), int(impares[r])
    return None


def construir(L):
    hallado = buscar_bloque(L)
    if hallado is None:
        print('L=%d: sin bloque hasta t=%d' % (L, T_MAX))
        return False
    t, r, A, a = hallado
    if A % 3 == 0:
        print('L=%d: A=%d es multiplo de 3' % (L, A))
        return False
    modulo = 3 ** a
    # m minimo >= 3 con 2^m = A (mod 3^a), por fuerza bruta
    m = 3
    while pow(2, m, modulo) != A % modulo:
        m += 1
        if m > 3 + 2 * modulo:
            print('L=%d: no hay m' % L)
            return False
    periodo = 1
    while pow(2, periodo, modulo) != 1:
        periodo += 1
    todo_bien = True
    for extra in range(3):
        mm = m + extra * periodo
        u = (2 ** mm - A) // modulo
        if u * modulo != 2 ** mm - A or u < 0:
            print('L=%d: u no entero' % L)
            return False
        n = 2 ** t * u + r
        datos = [altura_y_mitades(n + i) for i in range(L + 1)]
        esperado = (t + a + mm, t + mm)
        bien = all(d == esperado for d in datos)
        todo_bien = todo_bien and bien
        if extra == 0:
            print('L=%2d  t=%2d  r=%-7d a=%d  A=%-8d m=%-5d periodo=%-5d cifras de n=%-5d'
                  ' altura=%-5d sigma=%-5d %s'
                  % (L, t, r, a, A, mm, periodo, len(str(n)), esperado[0], esperado[1],
                     'OK' if bien else 'FALLO'))
    return todo_bien


def cotejar_a078441():
    # alturas con memoria: se itera hasta bajar de n y se suma lo ya sabido
    alturas = [None, 0]
    for n in range(2, TOPE_A078441 + 2):
        x = n
        pasos = 0
        while x >= n:
            x = x // 2 if x % 2 == 0 else 3 * x + 1
            pasos += 1
        alturas.append(pasos + alturas[x])
    primero = {}
    n = 1
    while n <= TOPE_A078441:
        largo = 1
        while n + largo < len(alturas) and alturas[n + largo] == alturas[n]:
            largo += 1
        for k in range(1, largo + 1):
            # la racha que empieza en n contiene rachas de largo k desde n
            if k not in primero:
                primero[k] = n
        n += 1
    mio = [primero.get(k) for k in range(1, len(A078441) + 1)]
    return mio == A078441, mio


def main():
    ok = True
    print('Rachas construidas (altura y sigma_inf calculadas iterando C):')
    for L in range(1, L_MAX + 1):
        ok = construir(L) and ok
    bien, mio = cotejar_a078441()
    print('A078441, a(1)..a(%d) desde cero: %s' % (len(A078441), 'coincide' if bien else 'DISTINTO'))
    if not bien:
        print('   mio:', mio)
    ok = ok and bien
    for largo, inicio, altura, sigma in TABLA1_GAO:
        datos = [altura_y_mitades(inicio + i) for i in range(largo)]
        antes = altura_y_mitades(inicio - 1)
        despues = altura_y_mitades(inicio + largo)
        bien = (all(d == (altura, sigma) for d in datos) and antes[0] != altura
                and despues[0] != altura)
        ok = ok and bien
        print('Tabla 1 de Gao: %3d desde %-11d altura %d sigma %d: %s'
              % (largo, inicio, altura, sigma, 'OK' if bien else 'FALLO'))
    print('OK' if ok else 'FALLO')
    return ok


if __name__ == '__main__':
    raise SystemExit(0 if main() else 1)
