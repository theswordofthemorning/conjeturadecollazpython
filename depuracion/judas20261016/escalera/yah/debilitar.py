"""Escalera de G debilitadas: funciones parciales entre el peldaño 4 y el 5.

El piloto es G(2m) = 3m, G(8m+7) = 9m+8, parar en el resto. Cada versión
debilitada se detiene además en una clase fina, que se estrecha al crecer k;
en el límite k -> infinito se recupera G:

    A_k  la rama A sólo en z par con z != 0 mod 2^k   (para en 0 mod 2^k)
    B_k  la rama B sólo en z = 7 mod 8 con z != -1 mod 2^k   (para en -1 mod 2^k)

Se escriben en la base mixta de YAH igual que srs_piloto.py: las nueve
reglas X y, en vez de f R -> a0 R o t t t R -> a2 a2 R, una regla por sufijo:

    A_k  t f^i R      (z = 2^i·impar, 1 <= i <= k-1)
    B_k  f t^j R      (z termina en exactamente j unos, 3 <= j <= k-1)

más las reglas con L para los z cuyo sufijo llegaría a la L (z = 2^i en A_k,
z = 2^j - 1 en B_k). El lado derecho es c·m + d, con m el valor del prefijo,
escrito con las cifras ternarias primero y las binarias después.

Por el argumento de J2_MECANISMOS §2 (las reglas X terminan solas, toda
cifra ternaria acaba absorbida en la L y cada regla dinámica gasta cifras
binarias), cada sistema termina desde toda cadena si y sólo si su función se
detiene en todo z >= 1. El programa no prueba eso: lo comprueba por
simulación en todos los z < 2^bits, con dos estrategias de reescritura, y
mide las órbitas. Después relee cada sistema con el lector de YAH.

Uso:  python3 -I debilitar.py [--bits 12]
Escribe sistemas/G_A{k}.srs, sistemas/G_B{k}.srs y debilitadas.json.
"""
import argparse
import json
import os
import random
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
YAH = "/home/oem/herramientas/yah/rewriting-collatz"
SISTEMAS = os.path.join(AQUI, "sistemas")

FAMILIAS = [("A", k) for k in (2, 3, 4, 5)] + [("B", k) for k in (4, 5, 6, 7)]

FUNCIONES = {'f': (2, 0), 't': (2, 1), 'a0': (3, 0), 'a1': (3, 1), 'a2': (3, 2)}
X = [
    (('f', 'a0'), ('a0', 'f')), (('f', 'a1'), ('a0', 't')), (('f', 'a2'), ('a1', 'f')),
    (('t', 'a0'), ('a1', 't')), (('t', 'a1'), ('a2', 'f')), (('t', 'a2'), ('a2', 't')),
    (('L', 'a0'), ('L', 't')), (('L', 'a1'), ('L', 'f', 'f')), (('L', 'a2'), ('L', 'f', 't')),
]


def funcion(familia, k):
    def g(z):
        if familia == "A":
            if z % 2 == 0 and z % 2 ** k:
                return 3 * z // 2
            if z % 8 == 7:
                return (9 * z + 1) // 8
        else:
            if z % 2 == 0:
                return 3 * z // 2
            if z % 8 == 7 and z % 2 ** k != 2 ** k - 1:
                return (9 * z + 1) // 8
        return None
    return g


def cifras(c, d):
    """Cifras que llevan m a c·m + d (0 <= d < c, c = 3^p 2^q), ternarias primero."""
    p = q = 0
    while c % 3 == 0:
        c, p = c // 3, p + 1
    while c % 2 == 0:
        c, q = c // 2, q + 1
    assert c == 1
    bases = [3] * p + [2] * q
    resto, salida = d, []
    for i in range(len(bases) - 1, -1, -1):
        resto, cifra = divmod(resto, bases[i])
        salida.append(('a' + str(cifra)) if bases[i] == 3 else 'ft'[cifra])
    assert resto == 0
    return tuple(reversed(salida))


def binaria(z):
    return ('L',) + tuple('f' if b == '0' else 't' for b in bin(z)[3:]) + ('R',)


def reglas_dinamicas(familia, k, g):
    reglas = []
    if familia == "A":
        # z = 2^(i+1) m + 2^i  ->  3·2^i m + 3·2^(i-1); el último f de f^i R es z par
        for i in range(1, k):
            izq = ('t',) + ('f',) * i + ('R',)
            reglas.append((izq, cifras(3 * 2 ** i, 3 * 2 ** (i - 1)) + ('R',)))
        reglas.append((('t', 't', 't', 'R'), ('a2', 'a2', 'R')))
        pequenos = [2 ** i for i in range(1, k)] + [7]
    else:
        reglas.append((('f', 'R'), ('a0', 'R')))
        # z = 2^(j+1) m + 2^j - 1  ->  9·2^(j-2) m + 9·2^(j-3) - 1
        for j in range(3, k):
            izq = ('f',) + ('t',) * j + ('R',)
            reglas.append((izq, cifras(9 * 2 ** (j - 2), 9 * 2 ** (j - 3) - 1) + ('R',)))
        pequenos = [2 ** j - 1 for j in range(3, k)]
    for z in pequenos:
        reglas.append((binaria(z), binaria(g(z))))
    return reglas


def valor(cadena):
    v = 1
    for s in cadena[1:-1]:
        b, d = FUNCIONES[s]
        v = b * v + d
    return v


def reescribir(cadena, reglas, g, estrategia, azar, tope):
    valores, pasos = [], 0
    while pasos < tope:
        opciones = [(i, n) for i in range(len(cadena)) for n, (izq, _) in enumerate(reglas)
                    if cadena[i:i + len(izq)] == izq]
        if not opciones:
            return cadena, valores, pasos
        i, n = opciones[0] if estrategia == 'izquierda' else azar.choice(opciones)
        izq, der = reglas[n]
        nueva = cadena[:i] + der + cadena[i + len(izq):]
        if n >= len(X):
            assert valor(nueva) == g(valor(cadena)), (cadena, nueva)
            valores.append(valor(nueva))
        else:
            assert valor(nueva) == valor(cadena)
        cadena, pasos = nueva, pasos + 1
    raise RuntimeError('tope de pasos')


def leer_con_yah(ruta):
    sys.path.insert(0, os.path.join(YAH, "prover"))
    import rules
    sistema = rules.parserules(ruta, True)
    if not sistema.full or sistema.rev or not all(r.strict and not r.top
                                                  for r in sistema.rules):
        sys.exit(f"ERROR: YAH no lee {ruta} como terminación completa estricta")
    return [(tuple(r.left), tuple(r.right)) for r in sistema.rules]


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--bits', type=int, default=12)
    parser.add_argument('--semilla', type=int, default=20261019)
    parser.add_argument('--tope', type=int, default=200_000)
    args = parser.parse_args()
    azar = random.Random(args.semilla)
    os.makedirs(SISTEMAS, exist_ok=True)
    informe = {"fecha": "2026-10-19", "parametros": vars(args), "sistemas": {}}
    for familia, k in FAMILIAS:
        nombre = f"G_{familia}{k}"
        g = funcion(familia, k)
        dinamicas = reglas_dinamicas(familia, k, g)
        reglas = X + dinamicas
        fallos, orbita_max = [], (0, None)
        for z in range(1, 2 ** args.bits):
            orbita, w = [], z
            while (w := g(w)) is not None:
                orbita.append(w)
                if len(orbita) > 10_000:
                    sys.exit(f"ERROR: {nombre} no se detiene desde z={z} en 10000 pasos")
            if len(orbita) > orbita_max[0]:
                orbita_max = (len(orbita), z)
            for estrategia in ('izquierda', 'azar'):
                final, valores, _ = reescribir(binaria(z), reglas, g, estrategia, azar,
                                               args.tope)
                if valores != orbita or any(s.startswith('a') for s in final):
                    fallos.append([z, estrategia])
        ruta = os.path.join(SISTEMAS, nombre + ".srs")
        with open(ruta, "w", encoding="utf-8") as f:
            for izq, der in reglas:
                f.write(" ".join(izq) + " -> " + " ".join(der) + "\n")
        if leer_con_yah(ruta) != reglas:
            sys.exit(f"ERROR: la ida y vuelta de {nombre} no coincide")
        informe["sistemas"][nombre] = {
            "reglas": len(reglas), "dinamicas": [" ".join(i) + " -> " + " ".join(d)
                                                 for i, d in dinamicas],
            "fallos": fallos[:5], "numero_fallos": len(fallos),
            "orbita_mas_larga": {"pasos": orbita_max[0], "z": orbita_max[1]},
        }
        print(f"{nombre}: {len(reglas):2d} reglas, fallos {len(fallos)}, "
              f"órbita más larga {orbita_max[0]} pasos (z={orbita_max[1]})")
        if fallos:
            sys.exit(f"ERROR: la simulación de {nombre} no coincide con su función")
    with open(os.path.join(AQUI, "debilitadas.json"), "w", encoding="utf-8") as f:
        json.dump(informe, f, ensure_ascii=False, indent=1)
    print("Escalera de G debilitadas comprobada.")


if __name__ == "__main__":
    main()
