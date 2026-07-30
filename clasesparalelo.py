# clasesparalelo.py
#
# LO MISMO QUE clasesfusion.py PERO REPARTIDO ENTRE VARIOS NUCLEOS.
#
# clasesfusion.py recorre los 2^k restos con un solo proceso. En una maquina de
# 4 nucleos fisicos eso deja tres parados. Este reparte el rango de restos entre
# varios procesos y suma. El resultado tiene que salir IDENTICO, y eso es lo
# primero que se comprueba.
#
# COMO SE REPARTE, y donde esta el cuidado. El criterio mira PARES de restos
# consecutivos (r, r+1). Si se corta el rango en trozos, el par que cae justo en
# la frontera se perderia. Se arregla haciendo que cada trozo procese un resto
# DE MAS al final: el trozo [lo, hi) evalua los restos [lo, hi] y cuenta los
# pares r = lo .. hi-1. Asi los trozos se solapan en un resto y no se pierde ni
# se duplica ninguno.
#
# El borde final (r = 2^k - 1, cuyo vecino es el resto 0 del bloque siguiente)
# se trata aparte, igual que en el original.
#
# NO SUSTITUYE a clasesfusion.py: aquel es el que explica y demuestra. Este solo
# va mas rapido cuando hace falta un k grande.

import math
import multiprocessing as mp
import os
import sys
import time

import numpy as np


# ---------------------------------------------------------------------------
K_OBJETIVO = 32       # que exponente se quiere calcular
K_CONTROL = 30        # con cual se verifica primero (su valor ya se conoce)
A_CONTROL = 462857658 # el valor conocido de a(30), medido con clasesfusion.py
PROCESOS = 6          # cuantos nucleos usar. La maquina tiene 4 fisicos, 8 logicos
BLOQUE = 1 << 22      # restos por bloque dentro de cada proceso
# ---------------------------------------------------------------------------


def salto_y_paridad(restos, k):
    """Identica a la de clasesfusion.py. Devuelve (T^k(r), S_k(r))."""
    v = np.array(restos, dtype=np.int64, copy=True)
    S = np.zeros(len(v), dtype=np.int32)
    for _ in range(k):
        impar = (v & 1).astype(bool)
        S += impar
        rama_impar = 3 * v + 1
        rama_impar >>= 1
        v >>= 1
        np.copyto(v, rama_impar, where=impar)
        del rama_impar
    return v, S


def contar_trozo(args):
    """Cuenta los pares (r, r+1) que se funden, con r en [lo, hi).

    Evalua los restos [lo, hi] -- uno de mas -- para no perder el par de la
    frontera. Devuelve tambien (v, S) del resto 0 si le toco, que hace falta
    para el borde final.
    """
    lo, hi, k = args
    cuantos = 0
    cero = None
    ultimo = None

    for a in range(lo, hi + 1, BLOQUE):
        b = min(a + BLOQUE, hi + 1)
        v, S = salto_y_paridad(np.arange(a, b, dtype=np.int64), k)

        if a == 0:
            cero = (int(v[0]), int(S[0]))

        # el par que cruza la frontera entre bloques de este mismo proceso
        if ultimo is not None:
            uv, uS = ultimo
            if uS == int(S[0]) and uv == int(v[0]):
                cuantos += 1

        dentro = (S[:-1] == S[1:]) & (v[:-1] == v[1:])
        cuantos += int(dentro.sum())

        ultimo = (int(v[-1]), int(S[-1]))
        del v, S, dentro

    return cuantos, cero


def contar_paralelo(k, procesos=PROCESOS):
    """a(k) repartido entre varios procesos."""
    MOD = 1 << k
    # los pares van de r = 0 hasta r = MOD - 2; el MOD - 1 es el borde especial
    corte = MOD - 1
    paso = math.ceil(corte / procesos)
    trozos = []
    for i in range(procesos):
        lo = i * paso
        hi = min(lo + paso, corte)
        if lo < hi:
            trozos.append((lo, hi, k))

    with mp.Pool(processes=len(trozos)) as pool:
        resultados = pool.map(contar_trozo, trozos)

    cuantos = sum(c for c, _ in resultados)
    cero = next(z for _, z in resultados if z is not None)

    # el borde final: r = MOD - 1, cuyo vecino es el resto 0 con m aumentado
    v_ult, S_ult = salto_y_paridad(np.array([MOD - 1], dtype=np.int64), k)
    v_cero, S_cero = cero
    if int(S_ult[0]) == S_cero and int(v_ult[0]) == 3 ** S_cero + v_cero:
        cuantos += 1

    return cuantos


if __name__ == "__main__":
    print(f"CLASES QUE SE FUNDEN, repartido en {PROCESOS} procesos")
    print(f"  la maquina tiene {os.cpu_count()} procesadores logicos")
    print()

    # ---- COMPROBACION 1: reproducir un valor ya conocido -------------------
    print(f"comprobacion: recalcular a({K_CONTROL}), que ya se sabe que vale {A_CONTROL:,}")
    t0 = time.perf_counter()
    control = contar_paralelo(K_CONTROL)
    t_control = time.perf_counter() - t0
    print(f"  medido: {control:,}   en {t_control:,.1f} s")
    if control != A_CONTROL:
        raise SystemExit(
            f"  FALLA: sale {control:,} y tenia que salir {A_CONTROL:,}.\n"
            "  El reparto en trozos esta perdiendo o duplicando pares. No seguir."
        )
    print("  CORRECTO: el reparto no pierde ni duplica ningun par.")
    print()

    # ---- y ahora el que interesa ------------------------------------------
    for k in range(K_CONTROL + 1, K_OBJETIVO + 1):
        t0 = time.perf_counter()
        a = contar_paralelo(k)
        seg = time.perf_counter() - t0
        print(f"a({k}) = {a:,}   fraccion {a / (1 << k):.6f}   ({seg:,.1f} s)")
        sys.stdout.flush()
