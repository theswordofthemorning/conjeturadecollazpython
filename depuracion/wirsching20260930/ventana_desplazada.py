# W2: la version util de (*1) para el laboratorio, medida en enteros fijos.
#
# Para un entero a (no multiplo de 3, no ciclico) se recorren todos los caminos
# hacia atras del atajo con a lo sumo K pasos pares y L impares; cada nodo del
# arbol es un camino distinto, asi que contar nodos por (impares i, pares c) da
# exactamente e_i(c, a). No usa residuos (independiente de elka.py).
#
# Se mide r_l(k, a) = e_l(k, a) / ebar_l(k), ebar_l(k) = C(k+l, k) / (2*3^(l-1)),
# en la ventana desplazada k - l in [D, D + floor(sqrt(l))], y el minimo de r en
# ella. Si ese minimo se estabiliza lejos de 0 al crecer l, la version por entero
# y con ventana desplazada de (*1) es plausible para a; si decae, no.
#
# Calculo finito y exacto (enteros). No prueba nada para l grande.
import math
import sys

ENTEROS = [5, 7, 11, 13, 17, 34, 43, 56248]
L = 21
D = 6            # desplazamiento de la ventana, por encima del exceso maximo medido
K = L + D + int(math.isqrt(L)) + 1


def tabla_caminos(a):
    """cuenta[i][c] = e_i(c, a) para i <= L, c <= K."""
    cuenta = [[0] * (K + 1) for _ in range(L + 1)]
    pila = [(a, 0, 0)]
    while pila:
        x, i, c = pila.pop()
        cuenta[i][c] += 1
        if c < K:
            pila.append((2 * x, i, c + 1))
        if i < L and x % 3 == 2:
            pila.append(((2 * x - 1) // 3, i + 1, c))
    return cuenta


def media(l, k):
    return math.comb(k + l, k) / (2 * 3 ** (l - 1))


print(f"Ventana desplazada k - l en [{D}, {D} + isqrt(l)], L = {L}, K = {K}")
for a in ENTEROS:
    cuenta = tabla_caminos(a)
    print(f"\na = {a}")
    print("   l | exceso c_l - l | min r en ventana (k) | r en k = l+D, l+D+2, l+D+4")
    for l in range(6, L + 1):
        primero = next((c for c in range(K + 1) if cuenta[l][c] > 0), None)
        exceso = None if primero is None else primero - l
        ventana = [k for k in range(l + D, l + D + math.isqrt(l) + 1) if k <= K]
        if not ventana:
            continue
        rmin, kmin = min((cuenta[l][k] / media(l, k), k) for k in ventana)
        puntos = [f"{cuenta[l][k] / media(l, k):.3f}" if k <= K else "-"
                  for k in (l + D, l + D + 2, l + D + 4)]
        print(f"  {l:2d} | {exceso!s:>14} | {rmin:8.4f} ({kmin:2d})      | {' '.join(puntos)}")
    sys.stdout.flush()
