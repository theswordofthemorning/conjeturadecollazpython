"""Contraste independiente del ahorro de potencia (CasaPotencia.lean), con enteros exactos.

Uso, desde la raíz del repositorio:

    python -B -X utf8 depuracion/casa20261004/cotejar_potencia.py
        --salida depuracion/casa20261004/cotejo_potencia.json

Comprueba, sin la recursión de la prueba Lean:

1. `razon_fugitivos`: ((1+√3)/√2)^20 = (2+√3)^10 = a + b√3 < 2^19, en enteros;
2. `razon_potencia`: (3ρ)^32 = 3^32 (2+√3)^16 / 4^16 < 3^31, es decir 3 (2+√3)^16 < 4^16;
3. `razon_tres_grande`: 11/5 <= 3ρ, es decir 22√2 <= 15 (1 + √3), elevando al cuadrado;
4. la cadena de `fugitivos_potencia`: c_K^20 < 2^(19K) para K <= --hasta, con c_K contado
   por órbitas directas;
5. la cadena de `noDescienden_tres`: en cada bloque [3^J, 3^(J+1)), J <= --bloques, los
   candidatos #{n : 2^J <= 3^S_J(n)} cumplen la cota por residuos y la cota 6 (3ρ)^J;
6. por órbitas directas, para n < 3^--bloques, que los únicos que nunca bajan de sí mismos
   son 0 y 1 (el conjunto acotado por Lean no tiene más elementos en ese rango), que no
   hay fugitivos n >= 2 y que las fallas de CST (`fallasCST`: primer cruce k sin bajar en
   el paso k) son también sólo 0 y 1.

Un barrido finito no prueba la cota universal: sólo coteja las piezas exactas de la prueba.
"""

import argparse
import json
from math import sqrt
from pathlib import Path


def paso(n):
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def subidas(n, k):
    s = 0
    for _ in range(k):
        s += n % 2
        n = paso(n)
    return s


def potencia_raiz3(a, b, n):
    """(a + b√3)^n = x + y√3 con enteros."""
    x, y = 1, 0
    for _ in range(n):
        x, y = x * a + 3 * y * b, x * b + y * a
    return x, y


def menor_que(x, y, c):
    """Decide x + y√3 < c con enteros, y >= 0."""
    d = c - x
    return d > 0 and 3 * y * y < d * d


def baja(n):
    """True si la órbita de n baja alguna vez de n (n >= 2 tras verificarse llegada a 1)."""
    x = paso(n)
    for _ in range(10 ** 6):
        if x < n:
            return True
        x = paso(x)
    raise RuntimeError(n)


def primer_cruce(n):
    s, x = 0, n
    for k in range(1, 10 ** 6):
        s += x % 2
        x = paso(x)
        if 3 ** s < 2 ** k:
            return k, x
    raise RuntimeError(n)


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--hasta", type=int, default=20)
    analizador.add_argument("--bloques", type=int, default=11)
    analizador.add_argument("--salida", type=Path, required=True)
    a = analizador.parse_args()
    informe = {"hasta": a.hasta, "bloques": a.bloques}

    x, y = potencia_raiz3(2, 1, 10)
    assert menor_que(x, y, 2 ** 19)
    informe["razon_fugitivos"] = {"(2+√3)^10": f"{x} + {y}√3", "≈": x + y * sqrt(3),
                                  "2^19": 2 ** 19}
    x, y = potencia_raiz3(2, 1, 16)
    assert menor_que(3 * x, 3 * y, 4 ** 16)
    informe["razon_potencia"] = {"3(2+√3)^16": f"{3 * x} + {3 * y}√3",
                                 "≈": 3 * (x + y * sqrt(3)), "4^16": 4 ** 16}
    # 22√2 <= 15 + 15√3  <=>  968 <= 900 + 450√3  <=>  68 <= 450√3  <=>  68^2 <= 3 * 450^2
    assert 68 ** 2 <= 3 * 450 ** 2
    informe["razon_tres_grande"] = "68^2 <= 3·450^2"

    cs = {}
    for K in range(a.hasta + 1):
        c = sum(1 for r in range(2 ** K) if 2 ** K <= 3 ** subidas(r, K))
        assert c ** 20 < 2 ** (19 * K) or K == 0, (K, c)
        cs[K] = c
    informe["c_K"] = cs

    rho3 = 3 * (1 + sqrt(3)) / sqrt(2) / 2
    bloques = []
    for J in range(a.bloques):
        candidatos = sum(1 for n in range(3 ** J, 3 ** (J + 1))
                         if 2 ** J <= 3 ** subidas(n, J))
        porres = (3 ** (J + 1) // 2 ** J + 1) * cs.get(J, sum(
            1 for r in range(2 ** J) if 2 ** J <= 3 ** subidas(r, J)))
        assert candidatos <= porres <= 6 * rho3 ** J * (1 + 1e-12), (J, candidatos, porres)
        bloques.append([J, candidatos, porres, round(6 * rho3 ** J, 1)])
    informe["bloques [J, candidatos, cota por residuos, 6 (3ρ)^J]"] = bloques

    limite = 3 ** a.bloques
    nunca = [n for n in range(2)] + [n for n in range(2, limite) if not baja(n)]
    assert nunca == [0, 1], nunca[:10]
    cruces = {n: primer_cruce(n) for n in range(limite)}
    fallas = [n for n, (k, x) in cruces.items() if n <= x]
    assert fallas == [0, 1], fallas[:10]
    informe["orbitas_directas"] = {"limite": limite, "nunca_bajan": nunca,
                                   "con_primer_cruce": len(cruces),
                                   "fallas_CST": fallas,
                                   "tau_maximo": max(k for k, _ in cruces.values())}
    informe["resultado"] = "OK"
    a.salida.write_text(json.dumps(informe, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    print(json.dumps(informe, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
