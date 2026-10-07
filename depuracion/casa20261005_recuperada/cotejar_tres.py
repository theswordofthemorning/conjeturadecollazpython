"""Contraste independiente del lado 3-ádico (CasaTres.lean), con enteros exactos.

Uso, desde la raíz del repositorio:

    python -B -X utf8 depuracion/casa20261004/cotejar_tres.py
        --salida depuracion/casa20261004/cotejo_tres.json

Por órbitas directas, sin la inducción de la prueba Lean:

1. `iter_afin`: T^k(r + 2^k t) = T^k(r) + 3^S_k(r) t, para k <= 24, r < 2^min(k,10) y
   t < 40;
2. `tres_determinado`: T^k(n) ≡ T^k(n mod 2^k) (mod 3^S_k(n)), para n < 20000 y k <= 30;
3. `fibra_inyectiva` y `fibra_contenida`: en cada clase r mod 2^k con S = S_k(r) <= j, los
   t < 3^(j-S) dan 3^(j-S) valores distintos de T^k módulo 3^j, todos ≡ T^k(r) (mod 3^S),
   para k <= 12, todos los r < 2^k y j <= S + 3;
4. `paridad_independiente`: si m <= S_k(r), r y r + 2^k dan el mismo T^k módulo 3^m y
   paridades opuestas, para k <= 16 y todos los r < 2^k;
5. `sin_multiplos_de_tres`: si S_k(n) >= 1, 3 no divide a T^k(n), para n < 20000, k <= 60.

Un barrido finito no prueba las identidades universales: sólo las coteja.
"""

import argparse
import json
from pathlib import Path


def paso(n):
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def orbita(n, k):
    s = 0
    for _ in range(k):
        s += n % 2
        n = paso(n)
    return n, s


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--salida", type=Path, required=True)
    a = analizador.parse_args()
    informe = {}

    casos = 0
    for k in range(25):
        for r in range(2 ** min(k, 10)):
            Tr, S = orbita(r, k)
            for t in range(40):
                assert orbita(r + 2 ** k * t, k)[0] == Tr + 3 ** S * t, (k, r, t)
                casos += 1
    informe["iter_afin_casos"] = casos

    casos = 0
    for n in range(20000):
        for k in range(31):
            Tn, S = orbita(n, k)
            assert Tn % 3 ** S == orbita(n % 2 ** k, k)[0] % 3 ** S, (n, k)
            casos += 1
    informe["tres_determinado_casos"] = casos

    casos = 0
    for k in range(13):
        for r in range(2 ** k):
            Tr, S = orbita(r, k)
            for j in range(S, S + 4):
                valores = [orbita(r + 2 ** k * t, k)[0] % 3 ** j for t in range(3 ** (j - S))]
                assert len(set(valores)) == 3 ** (j - S), (k, r, j)
                assert all(v % 3 ** S == Tr % 3 ** S for v in valores), (k, r, j)
                casos += 1
    informe["fibra_casos"] = casos

    casos = 0
    for k in range(17):
        for r in range(2 ** k):
            Tr, S = orbita(r, k)
            Tr2 = orbita(r + 2 ** k, k)[0]
            assert Tr2 % 2 != Tr % 2, (k, r)
            for m in range(S + 1):
                assert Tr2 % 3 ** m == Tr % 3 ** m, (k, r, m)
                casos += 1
    informe["paridad_independiente_casos"] = casos

    casos = 0
    for n in range(20000):
        x, s = n, 0
        for k in range(61):
            if s >= 1:
                assert x % 3 != 0, (n, k)
                casos += 1
            s += x % 2
            x = paso(x)
    informe["sin_multiplos_de_tres_casos"] = casos
    informe["resultado"] = "OK"
    a.salida.write_text(json.dumps(informe, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    print(json.dumps(informe, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
