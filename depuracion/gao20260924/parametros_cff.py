# -*- coding: utf-8 -*-
"""Aritmetica exacta de los parametros de CF_F y CF_H.

Todo con enteros de precision arbitraria; ningun flotante en las
desigualdades. Comprueba las identidades declaradas en
Ventana_armonica.md seccion 4 y la condicion de contenido de
Guardias_finitas.md (que J_F >= 1).

    python -B -X utf8 depuracion/gao20260924/parametros_cff.py
"""
from fractions import Fraction


def techo_log2(x):
    """ceil(log2(x)) exacto para x >= 1."""
    return (x - 1).bit_length()


def suelo_log2(x):
    """floor(log2(x)) exacto para x >= 1."""
    return x.bit_length() - 1


def ventana(c0):
    """Parametros de la seccion 3 de Ventana_armonica.md para el arranque c0."""
    m0 = techo_log2(2 + abs(c0))
    T = 32 * max(32, m0)
    Q = T + 1
    L = 16 * Q
    n = L * L
    a = 2 + suelo_log2(n + 2)
    s = 3 * techo_log2(n + 1)
    H = n * (a + s + 1)
    R = (128 * (H + 1) * Q) ** 2
    G = 3 * (R + 1)
    D = 16 * (techo_log2(G + 2) + 1) ** 2
    return dict(m0=m0, T=T, Q=Q, L=L, n=n, a=a, s=s, H=H, R=R, G=G, D=D)


def cff(m):
    """Parametros globales de CF_F / CF_H para el nivel m."""
    N = 2 ** m
    h = N ** 6
    C = 9 * h ** 4
    v = ventana(C)
    W = v["H"] + v["D"]                      # CF_F usa bloques de H+D
    J_F = (N - 1) // (W + 2)                 # ensayos de CF_F
    J_H = (N - 1) // (v["D"] + 2)            # ensayos de CF_H
    d = N ** 4 * (10 * m + 3)                # duracion por excursion
    return dict(N=N, h=h, C=C, W=W, J_F=J_F, J_H=J_H, d=d, **v)


print("1. Identidades declaradas en Ventana_armonica.md seccion 4")
print("   r = 24m+4 ;  T_m = 768m+128 ;  Q_m = T_m+1 ;  d = N^4(10m+3)")
print()
print("   m |  r = m0  esperado |    T_m     esperado | ok")
malas = 0
for m in list(range(10, 20)) + [30, 50, 100, 1000]:
    p = cff(m)
    r_esp, T_esp = 24 * m + 4, 768 * m + 128
    ok = (p["m0"] == r_esp and p["T"] == T_esp and p["Q"] == T_esp + 1)
    malas += (not ok)
    print("%4d | %7d %9d | %8d %10d | %s"
          % (m, p["m0"], r_esp, p["T"], T_esp, "si" if ok else "NO"))
print("   identidades fallidas:", malas)

print()
print("2. El termino 3/N: union de N excursiones con coste 3/N^2")
print("   H3 con n=N^4, L=N^2, a=4m+2, s=6m da 1/L+(L-1)/n+n*2^-s")
for m in (10, 12, 20, 50):
    N = 2 ** m
    n_, L_, s_ = N ** 4, N ** 2, 6 * m
    coste = Fraction(1, L_) + Fraction(L_ - 1, n_) + Fraction(n_, 2 ** s_)
    print("   m=%-4d coste por excursion = %s  <= 3/N^2 = %s : %s"
          % (m, coste, Fraction(3, N * N), coste <= Fraction(3, N * N)))
    assert coste <= Fraction(3, N * N)
print("   union de N excursiones: N * 3/N^2 = 3/N  (exacto)")

print()
print("3. Encaje temporal: las N excursiones caben en h")
print("   N*d <= h  <=>  10m+3 <= 2^m")
for m in (5, 6, 7, 8, 9, 10, 11):
    N = 2 ** m
    print("   m=%-3d 10m+3 = %-5d  N = %-6d  cabe: %s"
          % (m, 10 * m + 3, N, 10 * m + 3 <= N))
print("   primer m con encaje:",
      next(m for m in range(1, 100) if 10 * m + 3 <= 2 ** m))

print()
print("4. Condiciones aritmeticas de la seccion 3")
for m in (10, 50, 1000):
    p = cff(m)
    c1 = p["n"] ** 2 >= 8 * p["Q"]            # para n*2^-s <= 1/(8Q)
    c2 = p["T"] >= 1024                        # hipotesis del producto
    c3 = 4 * (p["T"] + 1) * 61 ** p["T"] <= 62 ** p["T"]
    print("   m=%-5d n^2>=8Q: %-5s  T>=1024: %-5s  4(T+1)61^T<=62^T: %s"
          % (m, c1, c2, c3))
    assert c1 and c2 and c3

print()
print("5. CONTENIDO DE LA COTA: hace falta J_F >= 1, es decir W_m+2 <= N-1")
print("   W_m = H_m + D_m, con H_m de la ventana aplicada a c0 = C_m.")
print()
print("     m |            W_m |              N=2^m | J_F | J_H (CF_H)")
for m in (10, 20, 30, 40, 45, 46, 47, 48, 50, 60, 100):
    p = cff(m)
    print("  %5d | %14d | %18d | %3d | %s"
          % (m, p["W"], p["N"], p["J_F"],
             ("%d" % p["J_H"]) if p["J_H"] < 10 ** 12 else "%.3e" % p["J_H"]))

primero = next(m for m in range(1, 400) if cff(m)["J_F"] >= 1)
print()
print("   primer m con J_F >= 1 :", primero)
print("   con m = 10 declarado  : J_F =", cff(10)["J_F"], "-> la cota CF_F")
print("   no tiene contenido ahi (el termino (1-p)^J_F vale 1).")
print("   CF_H no sufre esto: usa D_m+2, no W_m+2, y D_m es diminuto.")
print("   D_m para m=10:", cff(10)["D"], " H_m para m=10:", cff(10)["H"])


print()
print("6. El mismo problema en CF_H, y el umbral de utilidad real")
primero_H = next(m for m in range(1, 400) if cff(m)["J_H"] >= 1)
print("   primer m con J_H >= 1 :", primero_H, " (CF_H tambien falla en m=10)")
print()
print("   Para que la cota sirva no basta J >= 1: hace falta J*p -> infinito,")
print("   con p_m = 2^(-D_m)/(4Q_m). En log2:")
print("       log2(J_F * p_m) = log2(J_F) - D_m - log2(4*Q_m)")
print()
print("     m |    D_m | log2(J_F) | log2(J_F*p_m) | util")
for m in (46, 100, 1000, 10000, 100000, 250000, 260000, 262500, 300000):
    p = cff(m)
    if p["J_F"] < 1:
        continue
    lj = p["J_F"].bit_length() - 1
    l4q = (4 * p["Q"]).bit_length() - 1
    tot = lj - p["D"] - l4q
    print("  %6d | %6d | %9d | %13d | %s"
          % (m, p["D"], lj, tot, "si" if tot > 0 else "no"))

lo, hi = 46, 2 ** 22
while lo < hi:
    mid = (lo + hi) // 2
    p = cff(mid)
    lj = (p["J_F"].bit_length() - 1) if p["J_F"] >= 1 else -10 ** 9
    if lj - p["D"] - ((4 * p["Q"]).bit_length() - 1) > 0:
        hi = mid
    else:
        lo = mid + 1
print()
print("   primer m con J_F * p_m > 1 (busqueda binaria, cota inferior en log2):", lo)
print("   D_m en ese punto:", cff(lo)["D"])
print()
print("   Esto no rompe el limite: D_m crece como log^2(m) y m acaba")
print("   superandolo, luego J_F*p_m -> infinito. Pero el umbral declarado")
print("   m>=10 no describe donde la cota empieza a decir algo.")
