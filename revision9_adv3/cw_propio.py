# cw_propio.py  (ADVERSARIO 3, 9a revision)
#
# EL CERTIFICADO COLLATZ-WIELANDT, IMPLEMENTACION PROPIA. Sin copiar
# certificadocw.py: BFS propio (FIFO, no LIFO: otro orden de indices),
# transicion re-derivada a mano (la de gramatica_propia.py), iteracion
# propia (normaliza cada paso), escala propia (10^13, no 10^12), y el
# certificado por Fraction exacta en vez de comparacion cruzada.
#
# ADEMAS computa lo que el fichero del repo NO computa: el MAXIMO de
# (Mv)_i / v_i sobre el soporte, que es COTA SUPERIOR de lambda_T
# (para v > 0 en el soporte... el max sobre soporte con sucesores
# fuera aportando su peso real 0 sigue siendo cota superior del
# cociente de Rayleigh restringido; se usa como PINZA numerica: si el
# certificado publicado supera este max, esta ROTO).
#
# Uso: python cw_propio.py N1 N2 ...   (numeros de escalon, 1-10)

import sys
import numpy as np
from fractions import Fraction

ESCALERA = [(2, 12), (3, 48), (5, 192), (7, 768), (9, 3072), (11, 12288),
            (13, 49152), (15, 196608), (17, 786432), (19, 3145728)]
PUBLICADO = [1.739963, 1.866657, 1.933590, 1.955595, 1.967467,
             1.975447, 1.980748, 1.984415, 1.987045, 1.989042]
ITER = 700
ESCALA = 10 ** 13


def paso(k, c, beta):
    # derivacion propia (ver gramatica_propia.py)
    if c % 2 == 0:
        k2, c2 = (k, c // 2) if beta == 0 else (k, (3 * c + 1 - 3 ** k) // 2)
    elif beta == 0:
        k2, c2 = k + 1, (3 * c + 1) // 2
    elif k == 0:
        k2, c2 = 1, (1 - 3 * c) // 2
    else:
        k2, c2 = k - 1, (c - 3 ** (k - 1)) // 2
    if k2 == 0:
        if c2 == 0:
            return None                  # fusion: muere
        c2 = abs(c2)
    return (k2, c2)


def escalon(K, C):
    from collections import deque
    indice = {(0, 1): 0}
    cola = deque([(0, 1)])
    suces = []
    while cola:
        k, c = cola.popleft()
        fila = []
        for beta in (0, 1):
            s = paso(k, c, beta)
            if s is None or s[0] > K or abs(s[1]) > C:
                fila.append(-1)          # fuera: peso 0
            else:
                if s not in indice:
                    indice[s] = len(indice)
                    cola.append(s)
                fila.append(indice[s])
        suces.append(fila)
    # los estados descubiertos despues pueden tener sucesores ya
    # indexados: suces se completo al vuelo, pero las filas de estados
    # tempranos pueden apuntar a -1 por estados descubiertos DESPUES?
    # No: el indice crece monotono y fila guarda el indice al momento;
    # un sucesor dentro de caja siempre se indexa al tocarlo. Correcto.
    n = len(indice)
    s0 = np.array([f[0] for f in suces], dtype=np.int64)
    s1 = np.array([f[1] for f in suces], dtype=np.int64)
    # indice -1 -> fantasma n (peso 0)
    s0 = np.where(s0 < 0, n, s0)
    s1 = np.where(s1 < 0, n, s1)
    v = np.ones(n + 1)
    v[n] = 0.0
    for _ in range(ITER):
        v = v[s0] + v[s1]
        v = np.append(v, 0.0)
        v /= v.max()
    w = np.floor(v[:n] / v[:n].max() * ESCALA).astype(np.int64).tolist()
    l0 = s0.tolist()
    l1 = s1.tolist()
    w.append(0)                          # el fantasma
    minimo = None
    maximo = None
    soporte = 0
    for i in range(n):
        if w[i] <= 0:
            continue
        soporte += 1
        f = Fraction(w[l0[i]] + w[l1[i]], w[i])
        if minimo is None or f < minimo:
            minimo = f
        if maximo is None or f > maximo:
            maximo = f
    return n, soporte, minimo, maximo


for arg in sys.argv[1:]:
    e = int(arg)
    K, C = ESCALERA[e - 1]
    n, soporte, mn, mx = escalon(K, C)
    pub = PUBLICADO[e - 1]
    print("escalon %2d (K=%2d, C=%8d): estados %8d  soporte %8d"
          % (e, K, C, n, soporte), flush=True)
    print("   certificado propio  %.6f   maximo propio %.6f   publicado %.6f"
          % (float(mn), float(mx), pub), flush=True)
    if pub > float(mx) + 1e-9:
        print("   *** ROTO: el certificado publicado SUPERA la cota superior propia")
    elif abs(float(mn) - pub) > 2e-4:
        print("   *** DISCREPANCIA > 2e-4 con lo publicado")
    else:
        print("   OK: publicado dentro de la pinza propia [%.6f, %.6f]"
              % (float(mn), float(mx)))
