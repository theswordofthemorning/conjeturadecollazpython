"""Terminos para los borradores OEIS de Gao y de Wu (27-09-2026).

Mapa clasico de Collatz: C(n) = n/2 si n es par, 3n+1 si es impar (A006370).

Gao:  a(k) = #{0 <= n < 2^k - 1 : n y n+1 coalescen en algun paso j <= k}.
      Coalescer (Gao 1993, pag. 264): C^j(n) = C^j(n+1), las mismas
      divisiones por 2 en los j primeros pasos, y ningun 1 en C^0..C^j.
      Gao (tabla 3) da a(k)/2^k con tres decimales para k = 4..24.
Wu:   b(N) = #{1 <= n < 2^N : n tiene la misma altura que n-1 o que n+1}.
      Wu (1992) calcula d(2^N) = b(N)/(2^N - 1) para N = 1..24.
      Tambien se guarda L(N): la racha mas larga de igual altura en [1, 2^N).

Escribe b-files en esta carpeta. Los parametros van aqui arriba (sin input()).
Uso: python -B -X utf8 terminos_oeis.py
"""

import time
import numpy as np

K_GAO = 28             # a(k) para k = 1..K_GAO
N_WU = 26              # b(N) para N = 1..N_WU
BLOQUE = 2 ** 22


def un_paso(x):
    par = (x % 2 == 0)
    return np.where(par, x // 2, 3 * x + 1), par


def cuenta_gao_bloque(inicio, fin, k_max):
    """Paso j de la coalescencia de Gao (con tope k_max) para n en [inicio, fin);
    -1 si no coalescen en <= k_max pasos."""
    n = np.arange(inicio, fin, dtype=np.int64)
    a = n.copy()
    b = n + 1
    mit_a = np.zeros(len(n), dtype=np.int64)
    mit_b = np.zeros(len(n), dtype=np.int64)
    j = np.full(len(n), -1, dtype=np.int64)
    vivos = np.arange(len(n))
    for paso in range(k_max + 1):
        av = a[vivos]
        bv = b[vivos]
        hay_uno = (av == 1) | (bv == 1)
        juntos = (av == bv) & ~hay_uno
        buenos = juntos & (mit_a[vivos] == mit_b[vivos])
        j[vivos[buenos]] = paso
        vivos = vivos[~(hay_uno | juntos)]
        if paso == k_max or len(vivos) == 0:
            break
        nuevo_a, par_a = un_paso(a[vivos])
        nuevo_b, par_b = un_paso(b[vivos])
        a[vivos] = nuevo_a
        b[vivos] = nuevo_b
        mit_a[vivos] += par_a
        mit_b[vivos] += par_b
    return j


def terminos_gao():
    cuentas = [0] * (K_GAO + 1)
    fin = 2 ** K_GAO - 1
    for inicio in range(0, fin, BLOQUE):
        final = min(fin, inicio + BLOQUE)
        j = cuenta_gao_bloque(inicio, final, K_GAO)
        n = np.arange(inicio, final, dtype=np.int64)
        for k in range(1, K_GAO + 1):
            dentro = (n < 2 ** k - 1) & (j >= 0) & (j <= k)
            cuentas[k] += int(dentro.sum())
    return cuentas


def alturas(tope):
    """Altura de n = 0..tope (h[0] = -1: el 0 nunca llega a 1), en int16."""
    h = np.zeros(tope + 1, dtype=np.int16)
    h[0] = -1
    h[1] = 0
    inicio = 2
    while inicio <= tope:
        final = min(tope + 1, inicio + BLOQUE)
        x = np.arange(inicio, final, dtype=np.int64)
        pasos = np.zeros(len(x), dtype=np.int64)
        vivos = np.arange(len(x))
        while len(vivos) > 0:
            nuevo, _ = un_paso(x[vivos])
            x[vivos] = nuevo
            pasos[vivos] += 1
            vivos = vivos[nuevo >= inicio]
        h[inicio:final] = (pasos + h[x]).astype(np.int16)
        inicio = final
    return h


def terminos_wu(h):
    b = [0] * (N_WU + 1)
    largo = [0] * (N_WU + 1)
    igual = (h[1:-1] == h[2:])          # igual[i]: h(i+1) == h(i+2), i >= 0
    for N in range(1, N_WU + 1):
        fin = 2 ** N                     # n = 1..fin-1
        derecha = igual[0:fin - 1]       # n con n+1, n = 1..fin-1
        izquierda = np.zeros(fin - 1, dtype=bool)
        izquierda[1:] = igual[0:fin - 2] # n con n-1, n = 2..fin-1
        b[N] = int((derecha | izquierda).sum())
        # racha mas larga dentro de [1, fin): pares iguales seguidos + 1
        pares = igual[0:fin - 2].astype(np.int8)
        mejor = 0
        actual = 0
        if len(pares) > 0:
            cambios = np.flatnonzero(np.diff(np.concatenate(([0], pares, [0]))))
            if len(cambios) > 0:
                mejor = int((cambios[1::2] - cambios[0::2]).max())
        largo[N] = mejor + 1
    return b, largo


def escribir_bfile(nombre, valores, primero):
    with open(nombre, 'w', encoding='ascii', newline='\n') as f:
        for i, v in enumerate(valores):
            f.write('%d %d\n' % (primero + i, v))


def main():
    t0 = time.time()
    gao = terminos_gao()
    print('Gao a(1..%d):' % K_GAO, ','.join(str(v) for v in gao[1:]), '(%.0f s)' % (time.time() - t0))
    escribir_bfile('bfile_gao_tabla3.txt', gao[1:], 1)
    t0 = time.time()
    h = alturas(2 ** N_WU + 1)
    wu, largo = terminos_wu(h)
    print('Wu b(1..%d):' % N_WU, ','.join(str(v) for v in wu[1:]), '(%.0f s)' % (time.time() - t0))
    print('Wu L(1..%d):' % N_WU, ','.join(str(v) for v in largo[1:]))
    escribir_bfile('bfile_wu_rachas.txt', wu[1:], 1)
    # controles contra lo ya verificado hoy (revision20260927)
    ok = gao[1:13] == [0, 0, 0, 1, 4, 11, 29, 65, 145, 305, 641, 1317]
    ok = ok and gao[24] == 6522141
    ok = ok and wu[1:11] == [0, 0, 0, 4, 13, 32, 69, 147, 303, 620]
    ok = ok and wu[22] == 3003711 and wu[24] == 12159386
    print('OK' if ok else 'FALLO')
    return ok


if __name__ == '__main__':
    raise SystemExit(0 if main() else 1)
