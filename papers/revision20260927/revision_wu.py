"""Revision adversarial del 27-09-2026: Wu (1992), con codigo nuevo.

No importa nada del laboratorio (solo revision_gao.py, de esta misma
revision, para la coalescencia de Gao). Calcula con el mapa clasico C:

1. K(2^N) = #{n en [1, 2^N) con la misma altura que n-1 o que n+1} y
   d(2^N) = K/(2^N - 1), para N = 1..N_MAX. Wu (1992) los calcula hasta
   N = 24; d(2^10) = 620/1023 es el valor que cita la IA de CNKI.
2. Lo mismo con la altura del atajo T (= sigma_inf, divisiones por 2),
   para ver si el 620 distingue las dos convenciones.
3. L(2^N): la racha mas larga de igual altura dentro de [1, 2^N).
4. Que la coalescencia de Gao da la misma altura y la misma sigma_inf
   (Condoras, racha_de_coalescencia), para n < 2^P_COAL.
5. La pregunta de Gao (pag. 266): si height(n) = height(n+1), ¿es
   sigma_inf(n) = sigma_inf(n+1)? Se cuentan los contraejemplos.

Uso: python -B -X utf8 revision_wu.py
"""

import time
import numpy as np
from revision_gao import por_bloques

N_MAX = 22
P_COAL = 20

# Tabla del laboratorio (papers/README.md), N = 4..16
LABORATORIO = {4: 4, 5: 13, 6: 32, 7: 69, 8: 147, 9: 303, 10: 620, 11: 1270,
               12: 2618, 13: 5340, 14: 10802, 15: 21925, 16: 44511}


def alturas(tope):
    """altura[n] y mitades[n] (sigma_inf) para n = 1..tope, con memoria."""
    altura = [0] * (tope + 1)
    mitades = [0] * (tope + 1)
    for n in range(2, tope + 1):
        x = n
        pasos = 0
        mit = 0
        while x >= n:
            if x % 2 == 0:
                x = x // 2
                mit += 1
            else:
                x = 3 * x + 1
            pasos += 1
        altura[n] = pasos + altura[x]
        mitades[n] = mit + mitades[x]
    return altura, mitades


def cuenta_wu(h, N):
    """K(2^N): n en [1, 2^N) con la misma h que n-1 (si n >= 2) o que n+1."""
    fin = 2 ** N
    K = 0
    for n in range(1, fin):
        izquierda = n >= 2 and h[n] == h[n - 1]
        derecha = h[n] == h[n + 1]
        if izquierda or derecha:
            K += 1
    return K


def racha_mas_larga(h, N):
    """Largo maximo de una racha de igual altura contenida en [1, 2^N)."""
    fin = 2 ** N
    mejor = 1
    actual = 1
    for n in range(2, fin):
        if h[n] == h[n - 1]:
            actual += 1
        else:
            actual = 1
        mejor = max(mejor, actual)
    return mejor


def main():
    ok = True
    t0 = time.time()
    h, s = alturas(2 ** N_MAX + 1)
    print('alturas hasta 2^%d + 1 en %.0f s' % (N_MAX, time.time() - t0))
    print(' N        K(2^N)     d(2^N)     K con sigma_inf    L(2^N)')
    anterior = 0
    creciente = True
    fila_10 = None
    for N in range(1, N_MAX + 1):
        K = cuenta_wu(h, N)
        K_T = cuenta_wu(s, N)
        d = K / (2 ** N - 1)
        L = racha_mas_larga(h, N)
        if N >= 2 and d < anterior:
            creciente = False
        anterior = d
        if N in LABORATORIO and LABORATORIO[N] != K:
            print('   DISTINTO del laboratorio en N=%d' % N)
            ok = False
        if N == 10:
            fila_10 = (K, K_T)
        print('%2d  %12d   %.6f   %12d   %6d' % (N, K, d, K_T, L))
    print('d(2^N) creciente en N = 1..%d: %s' % (N_MAX, creciente))
    print('d(2^10): K = %d con la altura clasica y %d con sigma_inf (Wu: 620)'
          % fila_10)
    ok = ok and fila_10[0] == 620

    t0 = time.time()
    fin = 2 ** P_COAL
    j = por_bloques(fin, None)
    coal = j >= 0
    malos = 0
    for n in range(1, fin):
        if coal[n] and (h[n] != h[n + 1] or s[n] != s[n + 1]):
            malos += 1
    iguales_sin_coal = sum(1 for n in range(1, fin) if h[n] == h[n + 1] and not coal[n])
    print('n < 2^%d: %d pares coalescen (Gao); %d sin la misma altura y sigma_inf'
          % (P_COAL, int(coal[1:].sum()), malos))
    print('   pares con la misma altura que NO coalescen (Gao): %d' % iguales_sin_coal)
    ok = ok and malos == 0
    contra = [n for n in range(1, 2 ** N_MAX) if h[n] == h[n + 1] and s[n] != s[n + 1]]
    print('Pregunta de Gao: height igual y sigma_inf distinta, n < 2^%d: %d casos %s'
          % (N_MAX, len(contra), contra[:10]))
    print('(%.0f s)' % (time.time() - t0))
    print('OK' if ok else 'FALLO')
    return ok


if __name__ == '__main__':
    raise SystemExit(0 if main() else 1)
