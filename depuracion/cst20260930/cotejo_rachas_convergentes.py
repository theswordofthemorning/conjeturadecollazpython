"""Cotejo independiente de rachas_convergentes.py.

1. CST directa para 2 <= n < N: se itera el atajo con enteros, se detecta el
   primer cruce 3^S_j < 2^j y se exige T^j(n) < n. No reutiliza el código del
   barrido verificar_r_rachas.py. Por defecto N = N_17 de rachas_convergentes.
2. Mejor aproximación: para 1 <= q <= Q, la distancia de q log2(3) al entero más
   próximo es al menos 1/(q_j + q_(j+1)) si q_j <= q < q_(j+1). Se usa el
   encierro racional de log2(3); es un control numérico del teorema clásico.
3. Lambda(q) >= log 2 / (q_j + q_(j+1)) con enteros exactos para q <= Q3:
   Lambda >= Delta / 2^k (porque log(1 + x) >= x / (1 + x)), luego basta
   Delta * (q_j + q_(j+1)) * 1000 >= 2^k * 694 (694/1000 > log 2).
"""

import argparse
from fractions import Fraction
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verificar_rhin_convergentes import cocientes_certificados, convergentes  # noqa: E402


def cst_hasta(N):
    """Devuelve (comprobados, mayor primer cruce, n que lo alcanza)."""
    mayor = (0, None)
    for n in range(2, N):
        x = n
        impares = 0
        pasos = 0
        tres = 1
        dos = 1
        while True:
            if x % 2 == 1:
                x = (3 * x + 1) // 2
                impares += 1
                tres *= 3
            else:
                x = x // 2
            pasos += 1
            dos *= 2
            if tres < dos:             # primer cruce del coeficiente
                break
        if not x < n:
            raise SystemExit(f"FALLO DE CST en n = {n}, cruce {pasos}")
        if pasos > mayor[0]:
            mayor = (pasos, n)
    return N - 2, mayor


def intervalo(q, denominadores):
    for j in range(1, len(denominadores) - 1):
        if denominadores[j] <= q < denominadores[j + 1]:
            return denominadores[j], denominadores[j + 1]
    raise ValueError(q)


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--n", type=int, default=4674093,
                            help="CST directa para 2 <= n < este valor")
    analizador.add_argument("--q", type=int, default=200000,
                            help="mejor aproximación para 1 <= q <= este valor")
    analizador.add_argument("--q3", type=int, default=3000,
                            help="cota exacta de Lambda para 1 <= q <= este valor")
    argumentos = analizador.parse_args()

    cocientes, bajo, alto = cocientes_certificados(4000, 256)
    denominadores = [q for _, q in convergentes(cocientes)]

    comprobados, mayor = cst_hasta(argumentos.n)
    print(f"1. CST directa para 2 <= n < {argumentos.n}: {comprobados} enteros, sin fallos.")
    print(f"   Mayor primer cruce: {mayor[0]}, en n = {mayor[1]}.")

    peor = None
    for q in range(1, argumentos.q + 1):
        qa, qb = intervalo(q, denominadores)
        # q log2(3) está en [q*bajo, q*alto]; distancia al entero más próximo, cota inferior.
        a, b = q * bajo, q * alto
        piso = a.numerator // a.denominator
        if b.numerator // b.denominator != piso:
            raise SystemExit(f"Encierro insuficiente en q = {q}")
        distancia = min(a - piso, piso + 1 - b)
        cociente = distancia * (qa + qb)
        if cociente <= 1:
            raise SystemExit(f"Falla la mejor aproximación en q = {q}")
        if peor is None or cociente < peor[0]:
            peor = (cociente, q)
    print(f"2. Mejor aproximación para 1 <= q <= {argumentos.q}: sin fallos; menor "
          f"distancia * (q_j + q_(j+1)) = {float(peor[0]):.6f}, en q = {peor[1]}.")

    for q in range(1, argumentos.q3 + 1):
        qa, qb = intervalo(q, denominadores)
        tres = 3 ** q
        k = tres.bit_length()
        Delta = (1 << k) - tres
        if not Delta * (qa + qb) * 1000 >= (1 << k) * 694:
            raise SystemExit(f"Falla la cota exacta de Lambda en q = {q}")
    print(f"3. Cota exacta de Lambda para 1 <= q <= {argumentos.q3}: sin fallos.")


if __name__ == "__main__":
    main()
