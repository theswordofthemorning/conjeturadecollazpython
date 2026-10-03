"""CST por número de rachas, con los convergentes de log2(3) en lugar de una criba por q.

Mapa T(n) = n/2 (par) o (3n+1)/2 (impar); k = tau(n) el primer cruce del
coeficiente, q = S_k(n), Lambda = k log 2 - q log 3 en (0, log 2]. Si en el
cruce T^k(n) >= n (un fallo de CST) y la palabra hasta k tiene r <= R rachas
impares, entonces, con lemas ya demostrados en Lean:

  (a) n < r 3^q / (2^k - 3^q) <= R / Lambda        (fallo_producto, e^x - 1 >= x)
  (b) si n + 1 < 2^m, entonces q <= cota(R, m)       (criba_desde_trayectoria, cota_monotona)

Hecho clásico (Lagrange): si q_j <= q < q_(j+1), con q_j los denominadores de
los convergentes de log2(3) y j >= 1, entonces ||q log2 3|| >= ||q_j log2 3||
> 1/(q_j + q_(j+1)). Como Lambda = log 2 (1 - {q log2 3}) >= log 2 ||q log2 3||,
en ese intervalo

  n < s_j = R (q_j + q_(j+1)) / log 2,   y por (b)   q <= cota(R, m_j),

con m_j la longitud en bits de techo(s_j). Si cota(R, m_j) < q_j, el intervalo
no admite fallos. Si lo admite, sus semillas son n < s_j. Por tanto todo fallo
con a lo sumo R rachas tiene n < N_R = max s_j sobre los intervalos que
sobreviven. Más allá del último denominador certificado actúa Rhin:
n < R k^14 con k <= 2q, así que q <= cota(R, m) con m de unos 14 log2(2q) bits,
imposible para q tan grande (y la desigualdad sólo mejora al crecer q).

Conclusión: si CST está comprobada para 2 <= n < N_R, no hay fallos con a lo
sumo R rachas. Las comprobaciones disponibles son el barrido propio hasta 2^23
(verificar_r_rachas_23_salida.txt) y el corolario 5.4 de Rozier-Terracol
(arXiv:2502.00948v5, n <= 2,8 * 10^19, apoyado en tablas externas).

Aritmética exacta: cocientes certificados de verificar_rhin_convergentes.py,
log 2 > 693/1000 certificado y la recursión entera de cota.
"""

import argparse
from fractions import Fraction
import math
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verificar_rhin_convergentes import (cocientes_certificados, convergentes,  # noqa: E402
                                         log_dos_inferior)


def cota(R, m):
    """La recursión de OcelotasRachas.cota."""
    c = 0
    for _ in range(R):
        c = (5 * m + 8 * c - 1) // 5
    return c


def techo(x):
    return -((-x.numerator) // x.denominator)


def estudio(R, denominadores, ln2):
    """Devuelve (N_R, intervalo decisivo, último intervalo superviviente)."""
    N = 0
    decisivo = None
    ultimo = None
    for j in range(1, len(denominadores) - 1):
        qa, qb = denominadores[j], denominadores[j + 1]
        s = techo(Fraction(R * (qa + qb)) / ln2)      # n < s, entero
        m = s.bit_length()                            # n + 1 <= s < 2^m
        tope = cota(R, m)
        if tope >= qa:
            ultimo = (j, qa, qb, tope)
            if s > N:
                N = s
                decisivo = (j, qa, qb)
    return N, decisivo, ultimo


def cola_con_rhin(R, q_inicio, ln2):
    """Ningún q >= q_inicio sobrevive usando Rhin: n < R k^14 y k <= 2q.

    De cota(r+1, m) <= m + (8/5) cota(r, m) sale cota(R, m) <= G_R m, con
    G_R = 5 (8^R - 5^R) / (3 * 5^R). Un fallo exige q <= G_R m(q), con
    m(q) <= log2(R) + 14 log2(2q) + 1 bits. La función
    f(q) = G_R (log2(R) + 14 log2(2q) + 1) - q decrece para q >= 14 G_R / ln 2,
    luego basta comprobar ese umbral y f(q_inicio) < 0 (con longitudes en bits,
    que acotan los logaritmos por arriba)."""
    G = Fraction(5 * (8 ** R - 5 ** R), 3 * 5 ** R)
    decrece = q_inicio >= 14 * G / ln2
    negativa = G * (R.bit_length() + 14 * (2 * q_inicio).bit_length() + 1) < q_inicio
    return decrece and negativa


def log_dos_superior():
    """Certifica log 2 < 6932/10000: las sumas parciales de exp(0,6932) ya pasan de 2."""
    x = Fraction(6932, 10000)
    suma = Fraction(0)
    termino = Fraction(1)
    for j in range(40):
        suma += termino
        termino = termino * x / (j + 1)
    if suma <= 2:
        raise ValueError("No se certificó log 2 < 0,6932")
    return x


def cola_con_lmn(R, q_inicio, ln2_inf, ln2_sup):
    """Ningún q >= q_inicio sobrevive con la cota de Laurent-Mignotte-Nesterenko.

    Forma débil, implicada por su corolario (1995) para 2 y 3:
    log Lambda >= -30 (log(2k) + 21)^2. Con k <= 2q, n < R e^E y
    E = 30 (log(4q) + 21)^2, basta m = bits(R) + 1 + E/log 2 + 1. Un fallo exige
    q <= G_R m(q). La función G_R m(q) - q decrece si q > (60/log 2) G_R (log(4q) + 21);
    se comprueba eso y que es negativa en q_inicio, acotando log(4q) por
    log 2 * bits(4q)."""
    G = Fraction(5 * (8 ** R - 5 ** R), 3 * 5 ** R)
    L = ln2_sup * (4 * q_inicio).bit_length()          # >= log(4 q_inicio)
    inv_ln2 = 1 / ln2_inf                               # >= 1/log 2
    decrece = q_inicio > 60 * inv_ln2 * G * (L + 21)
    m = R.bit_length() + 2 + 30 * inv_ln2 * (L + 21) ** 2
    negativa = G * m < q_inicio
    return decrece and negativa


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--bits", type=int, default=20000)
    analizador.add_argument("--rmax", type=int, default=80)
    analizador.add_argument("--barrido", type=int, default=2 ** 23,
                            help="CST comprobada para 2 <= n < barrido (propio)")
    analizador.add_argument("--rt", type=int, default=28 * 10 ** 18,
                            help="CST comprobada para 2 <= n <= rt (Rozier-Terracol)")
    argumentos = analizador.parse_args()

    cocientes, _, _ = cocientes_certificados(argumentos.bits, 256)
    denominadores = [q for _, q in convergentes(cocientes)]
    ln2 = log_dos_inferior()
    ln2_sup = log_dos_superior()
    print("CST por número de rachas mediante los convergentes de log2(3)")
    print(f"{len(cocientes)} cocientes certificados; último denominador con "
          f"{len(str(denominadores[-1]))} cifras.\n")
    print(f"{'R':>3} {'N_R (semillas n < N_R)':>24} {'intervalo decisivo':>34} "
          f"{'último superviviente':>22}")
    r_propio = 0
    r_rt = 0
    for R in range(1, argumentos.rmax + 1):
        N, decisivo, ultimo = estudio(R, denominadores, ln2)
        if not cola_con_rhin(R, denominadores[-1], ln2):
            raise SystemExit(f"La cola con Rhin no cierra para R = {R}")
        if not cola_con_lmn(R, denominadores[-1], ln2, ln2_sup):
            raise SystemExit(f"La cola con Laurent-Mignotte-Nesterenko no cierra para R = {R}")
        if N <= argumentos.barrido and r_propio == R - 1:
            r_propio = R
        if N <= argumentos.rt + 1 and r_rt == R - 1:
            r_rt = R
        texto = f"q_{decisivo[0]}={decisivo[1]}, q_{decisivo[0] + 1}={decisivo[2]}"
        print(f"{R:>3} {N:>24} {texto:>34} {'j=' + str(ultimo[0]):>22}")
    print(f"\nCola: ningún q por encima del último denominador sobrevive para "
          f"R <= {argumentos.rmax}, ni con Rhin ni con la forma débil de")
    print("Laurent-Mignotte-Nesterenko, log Lambda >= -30 (log(2k) + 21)^2; "
          "cualquiera de las dos basta.")
    print(f"\nCONCLUSIÓN 1 (barrido propio, 2 <= n < {argumentos.barrido}): ningún fallo "
          f"de CST con a lo sumo {r_propio} rachas impares.")
    print(f"CONCLUSIÓN 2 (Rozier-Terracol, n <= {argumentos.rt}): ningún fallo con a lo sumo "
          f"{r_rt} rachas impares.")
    print("Ambas usan, sólo para k mayor que el último numerador certificado, Rhin o bien")
    print("Laurent-Mignotte-Nesterenko (1995).")


if __name__ == "__main__":
    main()
