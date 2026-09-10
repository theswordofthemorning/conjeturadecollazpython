"""Capa 1: ataque exacto al exceso condicional de una excursion.

El estado sale del nucleo al bajar de k=2 a k=1. No se declara fusion.
No importa scripts del repo: muchos ejecutan barridos al importarse.
Esta implementacion fue escrita DESPUES de leer conteoconjunto.py;
el cruce es de implementaciones, no una revision independiente ciega.
"""

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product


def hijos(k, c):
    if c % 2 == 0:
        return ((k, c // 2), (k, (3 * c + 1 - 3**k) // 2))
    return ((k + 1, (3 * c + 1) // 2),
            (k - 1, (c - 3**(k - 1)) // 2) if k > 2 else None)


def avanzar(estados):
    nuevos = Counter()
    salidas = 0
    for (k, c), peso in estados.items():
        for hijo in hijos(k, c):
            if hijo is None:
                salidas += peso
            else:
                nuevos[hijo] += peso
    return nuevos, salidas


def exceso(estados, m):
    modulo = 2**m
    fibras = defaultdict(Counter)
    for (k, c), peso in estados.items():
        fibras[k][c % modulo] += peso
    vivos = sum(estados.values())
    if not vivos:
        raise ValueError("No hay ley condicionada: masa viva cero")
    suma = Fraction(0)
    for residuos in fibras.values():
        masa = sum(residuos.values())
        suma += Fraction(modulo * sum(n*n for n in residuos.values()), masa)
    resultado = suma / vivos - 1
    if resultado < 0:
        raise SystemExit("El exceso condicional no puede ser negativo")
    return resultado


def clasico_atajo(n):
    return n // 2 if n % 2 == 0 else (3*n + 1) // 2


def colision_entera(estados):
    masas = Counter()
    cuadrados = Counter()
    extremos = {}
    for (k, c), n in estados.items():
        masas[k] += n
        cuadrados[k] += n*n
        bajo, alto = extremos.get(k, (c, c))
        extremos[k] = min(bajo, c), max(alto, c)
    coeficiente = sum((Fraction(cuadrados[k], masas[k]) for k in masas),
                      Fraction(0)) / sum(masas.values())
    bits = max((alto-bajo).bit_length() for bajo, alto in extremos.values())
    return coeficiente, max(1, bits)


def control_pares():
    casos = 0
    for k, c, v in product(range(2, 7), range(-35, 36), range(50, 66)):
        rama = hijos(k, c)[v % 2]
        if rama is None:
            rama = (1, (c - 3) // 2)
        siguiente_k, siguiente_c = rama
        izquierda = clasico_atajo(3**k * v + c)
        derecha = 3**siguiente_k * clasico_atajo(v) + siguiente_c
        if izquierda != derecha:
            raise SystemExit(f"Fallo contra el par real: {(k, c, v)}")
        casos += 1
    print(f"CONTROL: {casos} pasos contra pares enteros positivos: OK", flush=True)


def control_palabras(c0, pasos, estados):
    # Reproduce el par real y recupera c; no llama a hijos/avanzar.
    conteo = Counter()
    for palabra in product((0, 1), repeat=pasos):
        k, c = 2, c0
        for bit in palabra:
            v = 2 * (abs(c) + 1) + bit
            x, y = clasico_atajo(v), clasico_atajo(3**k*v + c)
            if c % 2:
                k += 1 if bit == 0 else -1
            if k == 1:
                break
            c = y - 3**k*x
        else:
            conteo[(k, c)] += 1
    if conteo != estados:
        raise SystemExit("El conteo de palabras y el DP discrepan")


def investigar(c0, pasos, escalas, desde, bloque):
    estados = Counter({(2, c0): 1})
    salidas = 0
    medidas = {}
    peor = None
    fallos = []
    ceros = 0
    anterior_coef = None
    for t in range(pasos + 1):
        if sum(estados.values()) + salidas != 2**t:
            raise SystemExit("No se conserva vivos + salidas = 2^t")
        if t == min(8, pasos):
            control_palabras(c0, t, estados)
        coef, bits = colision_entera(estados)
        if exceso(estados, bits) != 2**bits * coef - 1:
            raise SystemExit("Falla la formula exacta en escala sin colisiones modulares")
        if t >= desde + 1 and (t % 4 == 0 or t == pasos):
            print(f"  t={t} estados={len(estados)} "
                  f"rho_lim_m={float(coef / (2*anterior_coef)):.9f} "
                  f"escala_inyectiva={bits}", flush=True)
        anterior_coef = coef
        for m in range(min(escalas), max(escalas) + bloque + 1):
            medidas[t, m] = exceso(estados, m)
        if t >= desde + bloque:
            for m in escalas:
                num, den = medidas[t, m], medidas[t-bloque, m+bloque]
                if den == 0:
                    ceros += 1
                    if num:
                        raise SystemExit(f"Piso no preservado: {c0, t, m}")
                    continue
                razon = num / den
                celda = (razon, t-bloque, m, num, den)
                if peor is None or razon > peor[0]:
                    peor = celda
                if 2**bloque * num >= den:
                    fallos.append(celda)
        if t < pasos:
            estados, nuevas_salidas = avanzar(estados)
            salidas = 2*salidas + nuevas_salidas
    razon, t, m, num, den = peor
    print(f"c0={c0} bloque={bloque} peor={float(razon):.9f} "
          f"t={t} m={m} fallos={len(fallos)} ceros={ceros}", flush=True)
    if fallos:
        print(f"  TESTIGO: e_hija={num}; e_padre={den}; rho={razon}", flush=True)
    return peor, fallos


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pasos", type=int, default=16)
    parser.add_argument("--desde", type=int, default=12)
    parser.add_argument("--m-min", type=int, default=1)
    parser.add_argument("--m-max", type=int, default=12)
    parser.add_argument("--bloque", type=int, default=1)
    parser.add_argument("--semillas", type=int, nargs="+", default=[
        1, 3, 5, 7, 9, 17, 27, 31, 63, 127, 255, 999983, 999999937,
        2**21 - (2**21 + 1)//3])
    args = parser.parse_args()
    if not (args.bloque >= 1 and 0 <= args.desde < args.pasos
            and args.desde + args.bloque <= args.pasos
            and 1 <= args.m_min <= args.m_max):
        parser.error("Rangos incompatibles")
    control_pares()
    print(f"VENTANA t={args.desde}..{args.pasos-args.bloque}, "
          f"m={args.m_min}..{args.m_max}; sin filtro numerico; "
          f"umbral exacto=1/{2**args.bloque}", flush=True)
    total = 0
    for c0 in args.semillas:
        _, fallos = investigar(c0, args.pasos,
                              range(args.m_min, args.m_max + 1),
                              args.desde, args.bloque)
        total += len(fallos)
    print(f"FIN: {total} celdas incumplen la contraccion estricta. "
          "Barrido finito, no prueba universal.", flush=True)


if __name__ == "__main__":
    main()
