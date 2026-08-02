# A61_comp - comparador: tercera derivacion, sin usar el codigo de los agentes.
# En un ciclo de una vuelta la identidad da C = n0*(2^B - 3^A) directamente,
# asi que el signo de C y el lado de 2^B vs 3^A son EL MISMO HECHO (con n0>=1).
# Compruebo los cuatro ciclos iterando el mapa crudo (sin arrastrar C) y
# recomputando C por la forma cerrada; y ataco los bordes n0=0 y A=0.

from fractions import Fraction
import math

def orbita_ciclo(n0, s):
    # itera el mapa clasico crudo hasta volver a n0; cuenta A y B
    n = n0
    A = B = 0
    pasos = 0
    while True:
        if n % 2 == 0:
            n //= 2; B += 1
        else:
            n = 3 * n + s; A += 1
        pasos += 1
        if n == n0:
            return A, B, pasos
        if pasos > 10**6:
            raise SystemExit("no cierra")

casos = [(1, +1), (1, -1), (5, -1), (17, -1)]
esperado = {(1, +1): (1, 2, 1), (1, -1): (1, 1, -1),
            (5, -1): (2, 3, -5), (17, -1): (7, 11, -2363)}
for n0, s in casos:
    A, B, k = orbita_ciclo(n0, s)
    C = n0 * (2**B - 3**A)          # forma cerrada, no arrastrada
    assert (A, B, C) == esperado[(n0, s)], (n0, s, A, B, C)
    # el "luego": signo de C <-> lado de 2^B vs 3^A (mismo hecho, C = n0*(2^B-3^A))
    assert (C > 0) == (2**B > 3**A)
    # comparacion exacta de B/A vs log2(3) sin floats: B/A > log2 3 <=> 2^B > 3^A
    lado_exacto = 2**B > 3**A
    lado_float = B / A > math.log2(3)
    assert lado_exacto == lado_float, (n0, s)
    print("n0=%d s=%+d: A=%d B=%d C=%d, signo C %s, B/A=%.4f %s log2(3)" %
          (n0, s, A, B, C, "+" if C > 0 else "-", B / A, ">" if lado_exacto else "<"))

# borde n0=0: punto fijo del mapa (0 par -> 0), A=0, C=0: la mitad 3n-1 fallaria
# si se admitiera 0 como "ciclo". Confirmo que 0 cicla con A=0.
n = 0
for _ in range(5):
    n = n // 2 if n % 2 == 0 else 3 * n - 1
assert n == 0
print("borde n0=0: punto fijo con A=0, C=0 -> queda fuera del enunciado (ciclo sobre n>=1)")

# borde A=0 en un ciclo con n0>=1: imposible (2^B*n0 = n0 con B=k>=1 no cierra)
for n0 in range(1, 50):
    for B in range(1, 20):
        assert (2**B) * n0 != n0
print("borde A=0: ningun n0>=1 cumple 2^B*n0 = n0 con B>=1 -> todo ciclo tiene A>=1")
print("A61_comp: OK")
