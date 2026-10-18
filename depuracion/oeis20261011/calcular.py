# Cálculo y cotejo de las tres fichas OEIS del 11-10-2026.
# Uso: python -B -X utf8 calcular.py --limite-encuentro 2000000 --limite-casi 2000000
# Escribe calcular_salida.txt y b_encuentro.txt en esta carpeta.
import argparse
import math
import os
import sys

CARPETA = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(CARPETA))


def C(x):
    return x // 2 if x % 2 == 0 else 3 * x + 1


def T(x):
    return x // 2 if x % 2 == 0 else (3 * x + 1) // 2


def alturas(limite):
    # h[k] = pasos de C hasta 1, para 1 <= k <= limite (memo hacia abajo).
    h = [0] * (limite + 1)
    for k in range(2, limite + 1):
        x, pasos = k, 0
        while x >= k:
            x = C(x)
            pasos += 1
        h[k] = pasos + h[x]
    return h


def encuentro(m):
    x, y, k = m, m + 1, 0
    while x != y:
        x, y, k = C(x), C(y), k + 1
    return k


def casi_ciclo(n):
    # Devuelve el primer j >= 1 con T^j(n) = n + 1, o 0 si la órbita llega a 1 antes.
    x, j = n, 0
    while x != 1:
        x, j = T(x), j + 1
        if x == n + 1:
            return j
    return 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--limite-encuentro', type=int, required=True)
    p.add_argument('--limite-casi', type=int, required=True)
    a = p.parse_args()
    lineas = []

    def decir(texto):
        print(texto)
        lineas.append(texto)

    # ---------- Ficha 1: tiempo de encuentro de los pares de A078417 ----------
    N = a.limite_encuentro
    h = alturas(N + 1)
    a078417 = [m for m in range(1, N + 1) if h[m] == h[m + 1]]
    oficial = []
    with open(os.path.join(RAIZ, 'depuracion', 'oeis20260924', 'b078417_oficial.txt'), encoding='utf8') as f:
        for linea in f:
            partes = linea.split()
            if len(partes) == 2 and not linea.startswith('#'):
                oficial.append(int(partes[1]))
    decir('A078417 recalculada: %d términos <= %d; coincide con la b-file oficial (%d): %s'
          % (len(a078417), N, len(oficial), a078417[:len(oficial)] == oficial))
    tiempos = [encuentro(m) for m in a078417]
    decir('Ficha 1, primeros 60: ' + ','.join(map(str, tiempos[:60])))
    with open(os.path.join(CARPETA, 'b_encuentro.txt'), 'w', encoding='utf8', newline='\n') as f:
        for i, t in enumerate(tiempos[:10000], 1):
            f.write('%d %d\n' % (i, t))
    zoo = os.path.join(os.path.dirname(RAIZ), 'zootheorem', 'seqs', 'bfile_meeting_equal_height_3x1.txt')
    if os.path.exists(zoo):
        with open(zoo, encoding='utf8') as f:
            previa = [int(l.split()[1]) for l in f if l.strip() and not l.startswith('#')]
        decir('Ficha 1 coincide con la b-file preparada en zootheorem (%d): %s'
              % (len(previa), previa == tiempos[:len(previa)]))
    minimo = min(tiempos)
    tres = all((t == 3) == (m % 8 == 4) for m, t in zip(a078417, tiempos))
    decir('Mínimo %d; a = 3 sii m = 4 (mod 8): %s' % (minimo, tres))
    cota = all(t <= h[m] for m, t in zip(a078417, tiempos))
    decir('a(n) <= A006577(m) en todos: %s' % cota)
    vistos = sorted(set(tiempos))
    faltan = [v for v in range(3, 40) if v not in vistos]
    decir('Valores ausentes entre 3 y 39: %s' % faltan)
    # Forma de Lagarias de la conjetura de Gao, restringida a los m que llegan a 1.
    gao = [m for m in range(2, N + 1) if any_meet(m, int(math.log2(m)))]
    pares = set(m for m, t in zip(a078417, tiempos) if t <= math.log2(m))
    decir('Gao (k <= log2 m) = {A078417 con a <= log2 m} hasta %d: %s (%d elementos)'
          % (N, set(gao) == pares, len(gao)))
    # Ejemplos
    decir('Ejemplos: m=%d a=%d; m=%d a=%d' % (a078417[0], tiempos[0], a078417[1], tiempos[1]))

    # ---------- Ficha 2: casi ciclos T^j(n) = n + 1 ----------
    M = a.limite_casi
    casi = []
    for n in range(2, M + 1):
        j = casi_ciclo(n)
        if j:
            casi.append((n, j))
    decir('Ficha 2 (n <= %d): %s' % (M, ','.join(str(n) for n, j in casi)))
    decir('Pasos j: %s' % ','.join(str(j) for n, j in casi))
    rozier = [(3, 3), (8, 7), (8, 9), (8, 19), (8, 25), (27, 166), (27, 250), (27, 333), (27, 376),
              (46, 91), (46, 121), (46, 243), (46, 667), (46, 889), (54, 432), (73, 487), (73, 649),
              (73, 865), (73, 1153), (73, 2307), (73, 3643)]
    nuestro = sorted((j, n) for n, j in casi)
    decir('Coincide con los 21 pares (j, n) de Rozier-Terracol, apéndice B: %s' % (nuestro == sorted(rozier)))
    # Unicidad de j: ¿algún n alcanza n+1 con dos j distintos? (la órbita no puede volver a n+1 sin ciclo)
    paradojicas = all(paradojica(n, j) for n, j in casi if n > 3)
    decir('Todas con n > 3 son paradójicas (3^q < 2^j): %s' % paradojicas)

    # ---------- Ficha 3: racha más larga de alturas iguales en [1, 2^n) ----------
    tope = 22
    hh = alturas(2 ** tope + 1)
    directo = []
    for n in range(1, tope + 1):
        mejor, actual = 1, 1
        for k in range(2, 2 ** n):
            actual = actual + 1 if hh[k] == hh[k - 1] else 1
            mejor = max(mejor, actual)
        directo.append(mejor)
    b441 = {}
    with open(os.path.join(RAIZ, 'papers', 'oeis', 'b078441_oficial.txt'), encoding='utf8') as f:
        for linea in f:
            partes = linea.split()
            if len(partes) == 2 and not linea.startswith('#'):
                b441[int(partes[0])] = int(partes[1])
    kmax = max(b441)
    desde_b = []
    for n in range(1, 40):
        if b441[kmax] + kmax - 1 <= 2 ** n - 1:
            break  # la b-file no basta: podría haber rachas más largas que kmax
        desde_b.append(max(k for k in b441 if b441[k] + k - 1 <= 2 ** n - 1))
    decir('Ficha 3 directa n=1..%d: %s' % (tope, ','.join(map(str, directo))))
    decir('Ficha 3 desde b078441 n=1..%d: %s' % (len(desde_b), ','.join(map(str, desde_b))))
    tabla_wu = [1, 1, 1, 2, 3, 3, 5, 5, 6, 7, 9, 14, 17, 17, 17, 25, 25, 27, 29, 40, 40, 52, 65, 77, 96, 96]
    decir('Directa = b-file en 1..%d: %s; tabla del artículo III (N<=26) = b-file: %s; L(2^30) = %d (Wu: 176)'
          % (tope, directo == desde_b[:tope], tabla_wu == desde_b[:26], desde_b[29]))

    with open(os.path.join(CARPETA, 'calcular_salida.txt'), 'w', encoding='utf8', newline='\n') as f:
        f.write('\n'.join(lineas) + '\n')


def any_meet(m, kmax):
    x, y = m, m + 1
    for _ in range(kmax):
        x, y = C(x), C(y)
        if x == y:
            return True
    return False


def paradojica(n, j):
    x, q = n, 0
    for _ in range(j):
        q += x % 2
        x = T(x)
    return 3 ** q < 2 ** j and x >= n


if __name__ == '__main__':
    sys.exit(main())
