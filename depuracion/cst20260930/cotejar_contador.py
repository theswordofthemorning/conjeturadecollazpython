"""Cotejo finito del contador y la extracción, independiente de los otros scripts.

Compara inicios 0->1 con agrupación maximal por itertools.groupby y con una
lectura de bloques abiertos. Incluye todas las palabras binarias hasta la
longitud indicada y prefijos del atajo de Collatz sobre naturales.
No es una prueba universal ni presupone Rhin.
"""

import argparse
from fractions import Fraction
import hashlib
from itertools import groupby, product
import json
from pathlib import Path


def cotejar_palabra(bits):
    contador = sum(bit == 1 and (j == 0 or bits[j - 1] == 0)
                   for j, bit in enumerate(bits))
    grupos = [(bit, len(list(grupo))) for bit, grupo in groupby(bits)]
    assert contador == sum(bit for bit, _ in grupos)
    if not bits or bits[0] == 0:
        return contador, None

    # Construcción de la inducción: bloques completos y un bloque abierto.
    completos = []
    impar, par = 1, 0
    for bit in bits[1:]:
        if bit == 0:
            par += 1
        elif par == 0:
            impar += 1
        else:
            completos.append((impar, par))
            impar, par = 1, 0
    bloques = completos + [(impar, par)]
    assert contador == len(bloques)
    reconstruida = []
    for i, (a, b) in enumerate(bloques):
        assert a > 0 and b >= 0
        assert i == len(bloques) - 1 or b > 0
        reconstruida.extend([1] * a + [0] * b)
    assert reconstruida == list(bits)
    assert (par > 0) == (bits[-1] == 0)
    esperados = []
    for i in range(0, len(grupos), 2):
        a = grupos[i][1]
        b = grupos[i + 1][1] if i + 1 < len(grupos) else 0
        esperados.append((a, b))
    assert bloques == esperados
    return contador, bloques


def cotejar_orbita(n, max_pasos, huella):
    x = n
    bits = []
    coeficiente = Fraction(1)
    primer_cruce = None
    cerrados = 0
    for k in range(max_pasos + 1):
        r, bloques = cotejar_palabra(bits)
        assert coeficiente == Fraction(3 ** sum(bits), 2 ** k)
        assert coeficiente * n <= x
        if coeficiente >= 1:
            assert n <= x
        huella.update(f"{n},{k},{x},{r}\n".encode("ascii"))
        if bloques is not None and bits[-1] == 0:
            cerrados += 1
            assert all(a > 0 and b > 0 for a, b in bloques)
            assert sum(a + b for a, b in bloques) == k
        if primer_cruce is None and coeficiente < 1:
            assert k > 0 and bits[-1] == 0
            if n % 2:
                assert bloques is not None and r > 0
            else:
                assert (k, r) == (1, 0)
            if n >= 2 and r <= 10:
                assert x < n
            primer_cruce = {"n": n, "k": k, "rachas": r, "valor": x}
        if k == max_pasos:
            break
        bit = x % 2
        bits.append(bit)
        if bit:
            x = 3 * x + 1
            coeficiente *= 3
        x //= 2
        coeficiente /= 2
    return primer_cruce, cerrados


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--longitud-binaria", type=int, required=True)
    analizador.add_argument("--hasta", type=int, required=True)
    analizador.add_argument("--max-pasos", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    if not 0 <= argumentos.longitud_binaria <= 16:
        analizador.error("Se requiere 0<=longitud-binaria<=16")
    if argumentos.hasta < 0 or argumentos.max_pasos < 1:
        analizador.error("Se requiere hasta>=0 y max-pasos>=1")

    huella_binaria = hashlib.sha256()
    categorias = {"vacia": 0, "inicio_par": 0, "impar_abierta": 0, "impar_cerrada": 0}
    for longitud in range(argumentos.longitud_binaria + 1):
        for bits in product((0, 1), repeat=longitud):
            r, bloques = cotejar_palabra(bits)
            categoria = ("vacia" if not bits else "inicio_par" if bits[0] == 0
                         else "impar_abierta" if bits[-1] else "impar_cerrada")
            categorias[categoria] += 1
            huella_binaria.update((str((bits, r, bloques)) + "\n").encode("ascii"))

    huella_orbitas = hashlib.sha256()
    cruces = 0
    sin_cruce = []
    cerrados = 0
    for n in range(argumentos.hasta + 1):
        cruce, cantidad = cotejar_orbita(n, argumentos.max_pasos, huella_orbitas)
        cerrados += cantidad
        if cruce is None:
            sin_cruce.append(n)
        else:
            cruces += 1

    bordes = []
    for n, k, r, x in [(0, 1, 0, 0), (1, 2, 1, 1), (2, 1, 0, 1),
                       (3, 4, 1, 2), (7, 7, 2, 5), (27, 59, 15, 23),
                       (10087, 105, 25, 7688)]:
        cruce, _ = cotejar_orbita(n, k, hashlib.sha256())
        assert cruce == {"n": n, "k": k, "rachas": r, "valor": x}
        bordes.append(cruce)

    carpeta = Path(__file__).resolve().parent
    resultado = {
        "mapa": "n/2 si par; (3n+1)/2 si impar; naturales, pasos del atajo",
        "tipo": "cotejo exacto finito; no prueba universal; sin Rhin",
        "longitud_binaria": argumentos.longitud_binaria,
        "palabras_binarias": sum(categorias.values()),
        "categorias": categorias,
        "sha256_palabras": huella_binaria.hexdigest(),
        "semillas": [0, argumentos.hasta],
        "prefijos_por_semilla": [0, argumentos.max_pasos],
        "prefijos_orbita": (argumentos.hasta + 1) * (argumentos.max_pasos + 1),
        "prefijos_impares_cerrados": cerrados,
        "primeros_cruces_encontrados": cruces,
        "sin_cruce_en_horizonte": sin_cruce,
        "sha256_orbitas": huella_orbitas.hexdigest(),
        "bordes": bordes,
        "fallos": 0,
        "sha256_fuentes": {nombre: hashlib.sha256((carpeta / nombre).read_bytes()).hexdigest()
                           for nombre in ["OcelotasContador.lean", "cotejar_contador.py"]},
    }
    argumentos.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n",
                                encoding="utf-8")
    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
