"""Cuánto empeora la cadena de diez rachas si Rhin se cambia por una cota más débil.

Hipótesis sustituta: Lambda = k log 2 - q log 3 >= c * k^(-mu) en la ventana
2^(k-1) <= 3^q < 2^k. La cadena de OcelotasTrayectorias da, para un fallo:
  Delta = 3^q (e^Lambda - 1) >= c 3^q k^(-mu)       (e^x - 1 >= x)
  n < r 3^q / Delta <= 10 k^mu / c                 (fallo_producto, r <= 10)
  S <= cota 10 m <= 182 m, con n + 1 < 2^m         (criba_desde_trayectoria)
  k <= 2 S                                         (tiempo_por_impares)
luego k <= 364 m, con m = techo(log2(10 k^mu / c)) + 1. Se busca el mayor k
que cumple esa desigualdad: por encima, la cota sustituta excluye el fallo y
por debajo la criba finita debe cubrir q <= k / log2(3).

Estimación, no certificado: usa log2 en coma flotante y la misma estructura de
la cadena (la versión Lean redondea m a potencias de dos y da 131072).
El coste relativo de la criba se estima como (q_max / 82696)^2, porque cada
exponente q exige aritmética con números de unos 1,6 q bits.
"""

import argparse
import math


def k_maximo(mu, c):
    """Mayor k con k <= 364 * (techo(log2(10 k^mu / c)) + 1)."""
    k = 2
    ultimo = None
    # La desigualdad se cumple hasta un umbral; se busca por duplicación y bisección.
    def cumple(x):
        m = math.ceil(math.log2(10 / c) + mu * math.log2(x)) + 1
        return x <= 364 * m
    while cumple(k):
        ultimo = k
        k *= 2
    bajo, alto = ultimo, k
    while alto - bajo > 1:
        medio = (bajo + alto) // 2
        if cumple(medio):
            bajo = medio
        else:
            alto = medio
    return bajo


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--mus", type=float, nargs="+",
                            default=[13.3, 14, 20, 30, 50, 100, 200])
    analizador.add_argument("--cs", type=float, nargs="+", default=[1.0, 1e-3, 1e-10])
    argumentos = analizador.parse_args()
    log2_3 = math.log2(3)
    print("Tolerancia de la cadena de diez rachas a una cota Lambda >= c k^(-mu)")
    print("(estimación; la cadena Lean actual usa mu = 14, c = 1 y obtiene k < 131072)\n")
    print(f"{'mu':>6} {'c':>8} {'k_max':>10} {'q_max':>9} {'coste criba':>12}")
    for mu in argumentos.mus:
        for c in argumentos.cs:
            k = k_maximo(mu, c)
            q = int(k / log2_3)
            coste = (q / 82696) ** 2
            print(f"{mu:>6} {c:>8.0e} {k:>10} {q:>9} {coste:>11.1f}x")


if __name__ == "__main__":
    main()
