"""Contraste independiente del retrato del fugitivo (CasaFugitivo.lean).

Uso, desde la raíz del repositorio:

    python -B -X utf8 depuracion/casa20261004/cotejar_fugitivo.py --hasta 22
        --salida depuracion/casa20261004/cotejo_fugitivo.json

Mapa: atajo T(n) = n/2 (par), (3n+1)/2 (impar). S_K(n) cuenta los pasos impares entre
n, T n, ..., T^(K-1) n. Dominio: residuos r < 2^K, cada uno con peso 1 (ley uniforme).

Comprueba con enteros exactos, para cada K <= --hasta:

1. la generatriz de Lean `suma_pesos`: el número de residuos con S_K = i es C(K, i);
2. `S_congr`: S_K(r + 2^K) = S_K(r) en todos los residuos;
3. `cota_sinCruce`: c_K = #{r < 2^K : 2^K <= 3^S_K(r)} cumple c_K^2 2^K <= (1+√3)^(2K),
   comparado en enteros como c_K^2 2^K <= a_K + b_K √3, con (4 + 2√3)^K = a_K + b_K √3;
4. `fugitivo_tres_mod_cuatro`: los residuos sin cruce hasta el paso 2 son 3 mod 4;
5. el conteo más fino d_K = #{r < 2^K : 2^j <= 3^S_j(r) para todo j <= K}, que no usa Lean,
   para mostrar cuánto más fuerte es la condición completa que la del último paso;
6. `cota_superior` de CasaCasiTodos: 2^k T^k(n) + 2^k <= 3^S_k(n) n + 3^k, y
   `desciende_de_cruce_grande`: si 3^S_k(n) < 2^k y n >= 3^k, entonces T^k(n) < n,
   para n < --enteros y k <= 40;
7. `terras_error` de CasaTerras, por órbitas directas: para N = 2^--exponente y K <= 16,
   |#{n < N : T^j(n) >= n para 1 <= j <= K} - N d_K / 2^K| <= d_K + 3^K, y para n >= 3^K
   «no baja en K pasos» equivale a «sobrevive K pasos» (`noBaja_iff_sobrevive`).

Un barrido finito no prueba la densidad cero: sólo coteja las piezas exactas de la prueba.
"""

import argparse
import json
from math import comb
from pathlib import Path


def paso(n):
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def subidas(n, k):
    s = 0
    for _ in range(k):
        s += n % 2
        n = paso(n)
    return s


def prefijos_sin_cruce(n, k):
    """True si 2^j <= 3^S_j(n) para todo j <= k."""
    s = 0
    for j in range(1, k + 1):
        s += n % 2
        n = paso(n)
        if 3 ** s < 2 ** j:
            return False
    return True


def raiz3_menor(a, b, c):
    """Decide c <= a + b*sqrt(3) con enteros, a, b >= 0."""
    if c <= a:
        return True
    d = c - a
    return d * d <= 3 * b * b


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--hasta", type=int, required=True)
    analizador.add_argument("--enteros", type=int, default=20000)
    analizador.add_argument("--exponente", type=int, default=18)
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()

    filas = []
    a, b = 1, 0  # (4 + 2√3)^K = a + b√3
    for K in range(argumentos.hasta + 1):
        modulo = 2 ** K
        cuenta = [0] * (K + 1)
        c = 0
        d = 0
        for r in range(modulo):
            s = subidas(r, K)
            cuenta[s] += 1
            assert subidas(r + modulo, K) == s, (K, r)
            if 2 ** K <= 3 ** s:
                c += 1
            if prefijos_sin_cruce(r, K):
                d += 1
                if K >= 2:
                    assert r % 4 == 3, (K, r)
        assert cuenta == [comb(K, i) for i in range(K + 1)], K
        assert raiz3_menor(a, b, c * c * modulo), K
        filas.append({"K": K, "c_K": c, "d_K": d, "proporcion_c": c / modulo,
                      "proporcion_d": d / modulo,
                      "cota_rho_K": ((1 + 3 ** 0.5) / (2 * 2 ** 0.5)) ** K})
        a, b = 4 * a + 6 * b, 2 * a + 4 * b

    casos_cruce = 0
    for n in range(argumentos.enteros):
        x, s = n, 0
        for k in range(41):
            assert 2 ** k * x + 2 ** k <= 3 ** s * n + 3 ** k, (n, k)
            if 3 ** s < 2 ** k and n >= 3 ** k:
                assert x < n, (n, k)
                casos_cruce += 1
            s += x % 2
            x = paso(x)

    N = 2 ** argumentos.exponente
    terras = []
    for K in range(min(16, argumentos.hasta) + 1):
        cuenta = 0
        for n in range(N):
            x, baja = n, False
            for _ in range(K):
                x = paso(x)
                if x < n:
                    baja = True
                    break
            if not baja:
                cuenta += 1
            if n >= 3 ** K:
                assert (not baja) == prefijos_sin_cruce(n, K), (n, K)
        d = filas[K]["d_K"]
        assert abs(cuenta * 2 ** K - N * d) <= (d + 3 ** K) * 2 ** K, K
        terras.append({"K": K, "N": N, "no_bajan": cuenta, "N_d_K_sobre_2K": N * d / 2 ** K,
                       "cota_error": d + 3 ** K})

    resultado = {"mapa": "T(n)=n/2 si par, (3n+1)/2 si impar", "hasta": argumentos.hasta,
                 "comprobado": ["generatriz binomial", "S_K periódica mod 2^K",
                                "c_K^2 2^K <= (1+√3)^(2K)", "sin cruce hasta 2 => 3 mod 4",
                                "cota superior del término aditivo",
                                "cruce con n >= 3^k es descenso",
                                "error de Terras por órbitas directas"],
                 "terras": terras,
                 "enteros": argumentos.enteros, "casos_cruce_grande": casos_cruce,
                 "filas": filas}
    argumentos.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n",
                                 encoding="utf-8")
    for f in filas:
        print(f"K={f['K']:2d}  c_K={f['c_K']:8d}  d_K={f['d_K']:7d}  "
              f"c/2^K={f['proporcion_c']:.4f}  d/2^K={f['proporcion_d']:.4f}  "
              f"rho^K={f['cota_rho_K']:.4f}")
    print(f"cota superior y {casos_cruce} cruces grandes comprobados para n < {argumentos.enteros}")
    for f in terras:
        print(f"Terras K={f['K']:2d}: #sigma>K = {f['no_bajan']:7d}, N d_K/2^K = "
              f"{f['N_d_K_sobre_2K']:10.1f}, cota {f['cota_error']}")
    print("OK")


if __name__ == "__main__":
    main()
