"""Contraste independiente de CasaCadena.lean, con enteros exactos.

Uso, desde la raíz del repositorio:

    python -B -X utf8 depuracion/casa20261004/cotejar_cadena.py
        --salida depuracion/casa20261004/cotejo_cadena.json

Comprueba por órbitas directas, sin la inducción de la prueba Lean:

1. `cadena_correcta`: T^k(n) mod 3^m = cadena(palabra_k(n), n) para n < 3000, k <= 25,
   m <= 6, con la cadena escrita aparte (división por 2 con el inverso modular de Python);
2. `palabra_sobre` y `palabra_inyectiva`: c -> palabra_k(c) es una biyección de [0, 2^k)
   en {0,1}^k, para k <= 14;
3. `ley_de_la_cadena`: para k <= 8 y m <= 4, la ley de T^k(r) mod 3^m con r < 2^k 3^m
   coincide, valor por valor, con la de la cadena con palabra y punto de partida
   uniformes.
"""

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path


def paso(n):
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def palabra(k, n):
    w = []
    for _ in range(k):
        w.append(n % 2 == 1)
        n = paso(n)
    return tuple(w)


def cadena(m, w, x):
    M = 3 ** m
    inv2 = pow(2, -1, M)
    x %= M
    for b in w:
        x = ((3 * x + 1) if b else x) * inv2 % M
    return x


def iterar(n, k):
    for _ in range(k):
        n = paso(n)
    return n


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--salida", type=Path, required=True)
    a = analizador.parse_args()
    informe = {}

    casos = 0
    for n in range(3000):
        for k in range(26):
            Tk, w = iterar(n, k), palabra(k, n)
            for m in range(7):
                assert Tk % 3 ** m == cadena(m, w, n), (n, k, m)
                casos += 1
    informe["cadena_correcta_casos"] = casos

    for k in range(15):
        palabras = {palabra(k, c) for c in range(2 ** k)}
        assert len(palabras) == 2 ** k
        assert palabras == set(itertools.product((False, True), repeat=k))
    informe["biyeccion_palabras_k<=14"] = True

    casos = 0
    for k in range(9):
        for m in range(5):
            M = 3 ** m
            orbita = Counter(iterar(r, k) % M for r in range(2 ** k * M))
            teoria = Counter(cadena(m, w, x)
                             for w in itertools.product((False, True), repeat=k)
                             for x in range(M))
            assert orbita == teoria, (k, m)
            casos += 1
    informe["ley_de_la_cadena_pares_(k,m)"] = casos
    informe["resultado"] = "OK"
    a.salida.write_text(json.dumps(informe, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    print(json.dumps(informe, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
