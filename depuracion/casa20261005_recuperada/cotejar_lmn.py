"""Contraste independiente de CasaLMN.lean, con enteros exactos.

Uso, desde la raíz del repositorio:

    python -B -X utf8 depuracion/casa20261004/cotejar_lmn.py
        --salida depuracion/casa20261004/cotejo_lmn.json

Comprueba, sin el núcleo de Lean:

1. `tres_cuatro_base`: 3^(2^17) · 2^(19·50^2 + 2) < 4^(2^17), y `tres_dos_base`:
   3^(2^17) <= 2^(79380 + 2^17), con enteros de Python;
2. el paso de inducción de `tres_cuatro`: 19 (t+34)^2 + 2 <= 2 (19 (t+33)^2 + 2) para
   t <= 10^5;
3. `cruce_justo`: en el primer cruce k >= 2, 2^k <= 2 · 3^S_k(n), por órbitas directas
   para n < --enteros;
4. la holgura de `LMNEntera`: para k <= --k y q = floor(k log 2 / log 3) con 2^k <= 2·3^q,
   el mayor log2(3^q / (2^k - 3^q)) observado, frente al exponente 19 (t+33)^2 que la
   hipótesis permite (t = floor(log2 k)). Sólo informa de cuán débil es la hipótesis.
"""

import argparse
import json
from pathlib import Path


def paso(n):
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def primer_cruce(n):
    s, x = 0, n
    for k in range(1, 10 ** 6):
        s += x % 2
        x = paso(x)
        if 3 ** s < 2 ** k:
            return k, s
    raise RuntimeError(n)


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--enteros", type=int, default=200000)
    analizador.add_argument("--k", type=int, default=3000)
    analizador.add_argument("--salida", type=Path, required=True)
    a = analizador.parse_args()
    informe = {}

    A = 3 ** (2 ** 17)
    assert A * 2 ** (19 * 50 ** 2 + 2) < 4 ** (2 ** 17)
    assert A <= 2 ** (79380 + 2 ** 17)
    informe["bases"] = {
        "bits_de_3^(2^17)": A.bit_length(),
        "tres_cuatro_base_margen_bits": 2 * 2 ** 17 - (A.bit_length() + 19 * 50 ** 2 + 2),
        "tres_dos_base_margen_bits": 79380 + 2 ** 17 - A.bit_length()}

    for t in range(10 ** 5 + 1):
        assert 19 * (t + 34) ** 2 + 2 <= 2 * (19 * (t + 33) ** 2 + 2), t
    informe["paso_induccion_t<=1e5"] = True

    casos = 0
    for n in range(2, a.enteros):
        k, s = primer_cruce(n)
        if k >= 2:
            assert 2 ** k <= 2 * 3 ** s, (n, k, s)
            casos += 1
    informe["cruce_justo_casos"] = casos

    peor, donde = 0.0, None
    for k in range(2, a.k + 1):
        q = 0
        while 3 ** (q + 1) < 2 ** k:
            q += 1
        if 2 ** k <= 2 * 3 ** q:
            D = 2 ** k - 3 ** q
            exceso = (3 ** q).bit_length() - D.bit_length()
            if exceso > peor:
                peor, donde = exceso, (k, q)
    t = donde[0].bit_length() - 1
    informe["holgura_LMNEntera"] = {
        "k_max": a.k, "peor_log2(3^q/D)_aprox": peor, "en_(k,q)": donde,
        "exponente_permitido_19(t+33)^2": 19 * (t + 33) ** 2,
        "nota": "la hipótesis sólo prohíbe D < 3^q / 2^(19(t+33)^2); en este rango "
                "sobra muchísimo"}
    informe["resultado"] = "OK"
    a.salida.write_text(json.dumps(informe, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    print(json.dumps(informe, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
