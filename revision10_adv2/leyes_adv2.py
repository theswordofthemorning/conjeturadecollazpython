# -*- coding: utf-8 -*-
# leyes_adv2.py -- ADVERSARIO 2, 10a revision (12-08-2026)
#
# LA CADENA (k, c) RECONSTRUIDA DESDE LOS ENUNCIADOS, no desde los .py
# del repo (regla de independencia del encargo). Fuentes usadas:
#   - cadenakc.lean (las seis leyes N1-N4 + F4 + vortice como TEOREMAS)
#   - notaequidistribucion.txt (mixto bit0: 2h = 3c+1; bit1: 2h = c - 3^(k-1))
#   - bitacora.md 10-08 (2) (hijos de la moneda: (k, c/2) y (k, (3c+1-3^k)/2);
#     el UNICO abs de la cadena en la salida k=1 impar bit1)
#   - RutaTeoremas.md ZOOLOGICO (LOBAS: unica absorcion (1,1)-bit1)
#
# Estado: (k, c) = clase de pares {v, 3^k*v + c}; el bit es la paridad
# del ANCLA v (Leonas, 6a revision). mixto <=> c impar (ley_moneda).
#
# Derivacion propia de las transiciones (verificada abajo contra los
# casos del repo caso_gatas / caso_garner / caso_P1 por fuerza bruta
# sobre pares enteros REALES, sin codigo del repo):
#   k >= 1:
#     c par,   bit0 (N1): (k,   c/2)
#     c par,   bit1 (N2): (k,   (3c + 1 - 3^k)/2)
#     c impar, bit0 (N3): (k+1, (3c + 1)/2)
#     c impar, bit1 (N4): k >= 2: (k-1, (c - 3^(k-1))/2)
#                          k == 1: (0, |c - 1| / 2); c == 1 => FUSION
#   k == 0 (par {v, v+c}, c >= 1):
#     c par,   bit0:      (0, c/2)
#     c par,   bit1:      (0, 3c/2)
#     c impar, bit0 (N3): (1, (3c + 1)/2)
#     c impar, bit1 (F4): (1, (1 - 3c)/2)
# FUSION (absorcion) <=> el hijo tiene c = 0 (solo alcanzable via
# (1,1)-bit1 -> (0,0), LOBAS).

FUSION = None  # marcador de absorcion


def hijo(k, c, bit):
    """El hijo del estado (k, c) bajo el bit (paridad del ancla).
    Devuelve (k', c') o FUSION."""
    if k == 0:
        if c % 2 == 0:
            return (0, c // 2) if bit == 0 else (0, 3 * c // 2)
        else:
            return (1, (3 * c + 1) // 2) if bit == 0 else (1, (1 - 3 * c) // 2)
    # k >= 1
    if c % 2 == 0:
        if bit == 0:
            return (k, c // 2)
        return (k, (3 * c + 1 - 3 ** k) // 2)
    # c impar: mixto
    if bit == 0:
        return (k + 1, (3 * c + 1) // 2)
    # bit 1
    if k >= 2:
        return (k - 1, (c - 3 ** (k - 1)) // 2)
    # k == 1
    if c == 1:
        return FUSION
    return (0, abs(c - 1) // 2)


def T(n):
    """El atajo de Terras sobre enteros (control independiente)."""
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def par_de(k, c, v):
    """El par entero real que representa (k, c) con ancla v."""
    return (v, 3 ** k * v + c)


if __name__ == "__main__":
    import random

    # ------ V1: las leyes contra pares enteros REALES (fuerza bruta) ------
    # Para (k, c) con k >= 1 y ancla v de la paridad del bit, el par
    # {v, 3^k v + c} evoluciona por T y debe aterrizar en la forma
    # {v', 3^k' v' + c'} con (k', c') = hijo(k, c, bit) y v' = T(v)
    # (bit 0: v' = v/2; bit 1: v' = (3v+1)/2), salvo k=1 bit1 donde el
    # ancla nueva es el MENOR de los dos valores (el abs y el reorden).
    rng = random.Random(20260812)
    fallos = 0
    pruebas = 0
    for _ in range(200000):
        k = rng.randint(0, 9)
        c = rng.randint(-3000, 3000)
        if k == 0:
            c = abs(c) + 1  # en la frontera c >= 1
        if c == 0:
            continue
        bit = rng.randint(0, 1)
        # ancla con la paridad del bit
        v = 2 * rng.randint(1, 10 ** 6) + bit
        a, b = par_de(k, c, v)
        Ta, Tb = T(a), T(b)
        h = hijo(k, c, bit)
        pruebas += 1
        if h is FUSION:
            ok = (Ta == Tb)
        else:
            k2, c2 = h
            # el ancla nueva: el que corresponda; probamos las dos
            # asignaciones (el reorden del abs) y exigimos que UNA valga
            ok = (Tb == 3 ** k2 * Ta + c2) or (Ta == 3 ** k2 * Tb + c2)
        if not ok:
            fallos += 1
            if fallos < 5:
                print("FALLO:", k, c, bit, "->", h, " par", (a, b), "->", (Ta, Tb))
    print("V1: %d pruebas de ley contra pares reales, %d fallos" % (pruebas, fallos))
    if fallos:
        raise SystemExit("V1 FALLO: las leyes reconstruidas NO son las de la cadena")

    # ------ V2: los casos con nombre del repo ------
    # caso_gatas: (0,1) -bit1-> (1,-1) -bit1-> (0,1)
    assert hijo(0, 1, 1) == (1, -1), hijo(0, 1, 1)
    assert hijo(1, -1, 1) == (0, 1), hijo(1, -1, 1)
    # caso_P1: (2,2) -bit1-> (2,-1)
    assert hijo(2, 2, 1) == (2, -1), hijo(2, 2, 1)
    # caso_garner: el par (4,5) = (0,1) con v=4 funde en 3 pasos: 0,0,1
    s = (0, 1)
    s = hijo(*s, bit=0)   # v=4 par
    assert s == (1, 2), s
    s = hijo(*s, bit=0)   # v=2 par
    assert s == (1, 1), s
    s = hijo(*s, bit=1)   # v=1 impar -> vortice
    assert s is FUSION
    # vortice_fusion: (1,1) bit1 es LA absorcion
    assert hijo(1, 1, 1) is FUSION
    print("V2: caso_gatas, caso_P1, caso_garner, vortice: OK")
    print("LEYES VALIDADAS: la reconstruccion coincide con la cadena real.")
