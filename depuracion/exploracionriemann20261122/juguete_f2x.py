"""Modelo de juguete: Collatz sin acarreos en F2[x].

Un polinomio de F2[x] se guarda como entero: el bit i es el coeficiente
de x^i. Multiplicar por x+1 es f ^ (f << 1), es decir 3n sin acarreos.
Mapa (Hicks-Mullen-Yucas-Zavislak 2008): f/x si x divide a f; si no,
m*f + 1. Con m = x+1 el teorema publicado dice que toda órbita llega a 1;
con m = x^2+x+1 Nichols (arXiv:1610.02545) da un ciclo que evita 1.

Esto es un barrido finito por grado, no una prueba.
"""

import argparse


def producto_sin_acarreo(a, b):
    resultado = 0
    while b:
        if b & 1:
            resultado ^= a
        a <<= 1
        b >>= 1
    return resultado


def paso(f, multiplicador):
    if f & 1 == 0:
        return f >> 1
    return producto_sin_acarreo(f, multiplicador) ^ 1


def grado(f):
    return f.bit_length() - 1


def orbita_hasta_uno(f, multiplicador, tope_pasos, tope_grado):
    """Devuelve ("uno", pasos), ("ciclo", elementos) o ("crece", grado alcanzado).

    "crece" sólo dice que se superó tope_grado: no prueba divergencia.
    """
    vistos = {}
    pasos = 0
    while f != 1:
        if f in vistos:
            inicio = vistos[f]
            return "ciclo", sorted(g for g, t in vistos.items() if t >= inicio)
        if grado(f) > tope_grado:
            return "crece", grado(f)
        vistos[f] = pasos
        f = paso(f, multiplicador)
        pasos += 1
        if pasos > tope_pasos:
            raise RuntimeError("tope de pasos superado")
    return "uno", pasos


def barrido(multiplicador, grado_maximo, tope_pasos, tope_grado):
    maximo_por_grado = {}
    ciclos = set()
    crecen = 0
    for f in range(1, 1 << (grado_maximo + 1)):
        estado, dato = orbita_hasta_uno(f, multiplicador, tope_pasos, tope_grado)
        if estado == "ciclo":
            ciclos.add(min(dato))
        elif estado == "crece":
            crecen += 1
        else:
            d = grado(f)
            maximo_por_grado[d] = max(maximo_por_grado.get(d, 0), dato)
    return maximo_por_grado, ciclos, crecen


def acarreos_de_paso_impar(n):
    """Bits en que 3n+1 difiere de su versión sin acarreos n ^ 2n ^ 1."""
    return bin((3 * n + 1) ^ (n ^ (n << 1) ^ 1)).count("1")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--grado-maximo", type=int, default=16)
    parser.add_argument("--tope-pasos", type=int, default=100000)
    parser.add_argument("--tope-grado", type=int, default=200)
    args = parser.parse_args()

    print("m = x+1 (análogo de 3n+1)")
    maximos, ciclos, crecen = barrido(0b11, args.grado_maximo, args.tope_pasos,
                                      args.tope_grado)
    print("  ciclos sin 1:", len(ciclos), " superan el tope de grado:", crecen)
    for d in sorted(maximos):
        if d >= 1:
            print("  grado %2d: máximo de pasos %4d  (d^1.5 = %6.1f, d^2 = %4d)"
                  % (d, maximos[d], d ** 1.5, d * d))

    print("m = x^2+x+1 (análogo de 7n+1 sin acarreos)")
    grado_siete = min(args.grado_maximo, 12)
    _, ciclos, crecen = barrido(0b111, grado_siete, args.tope_pasos, args.tope_grado)
    print("  grado <= %d: ciclos sin 1 %d, superan el tope de grado %d de %d"
          % (grado_siete, len(ciclos), crecen, (1 << (grado_siete + 1)) - 1))
    print("  menores representantes de ciclos:", [bin(c) for c in sorted(ciclos)][:5])

    print("Acarreos en pasos impares de la órbita entera de 27:")
    n, total, impares = 27, 0, 0
    while n != 1:
        if n & 1:
            total += acarreos_de_paso_impar(n)
            impares += 1
            n = (3 * n + 1) // 2
        else:
            n //= 2
    print("  pasos impares %d, bits corregidos por acarreo %d" % (impares, total))


if __name__ == "__main__":
    main()
