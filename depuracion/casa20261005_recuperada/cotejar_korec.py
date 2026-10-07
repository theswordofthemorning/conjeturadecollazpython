"""Contraste independiente de Korec (CasaKorec.lean), con enteros exactos.

Uso, desde la raíz del repositorio:

    python -B -X utf8 depuracion/casa20261004/cotejar_korec.py --hasta 18
        --salida depuracion/casa20261004/cotejo_korec.json

Mapa: atajo T(n) = n/2 (par), (3n+1)/2 (impar). S_k(n) cuenta los pasos impares entre
n, T n, ..., T^(k-1) n, calculados siempre por órbitas directas (sin la recursión de la
prueba Lean). Comprueba:

1. `momento_dos`: sum_{r < 2^K} (2 S_K(r) - K)^2 = K 2^K, para K <= --hasta;
2. `cota_chebyshev`: #{r < 2^K : K + 2t <= 2 S_K(r)} (2t)^2 <= K 2^K, para todo t <= K;
3. `muchas_por_residuos`: #{n < N : S_k(n) > s} <= (N div 2^k + 1) #muchasSubidas(k, s),
   para varios N, k <= 12 y s <= k;
4. `cota_muchas`: 2m #muchasSubidas(k, s) <= (E+1) 2^k con k = 2(E+1)m y
   k + 2m <= 2s + 2, siempre que k <= --hasta;
5. `baja_de_potencia`: barrido exhaustivo de n < --enteros, k <= 20, p <= q <= 4 y
   S_k(n) <= s <= k; si se cumplen las hipótesis, T^k(n)^q < n^p;
6. `condicion`: la implicación de potencias en el peor caso N = 2^(2(E+1)(m+1)) - 1,
   para E <= 9, m <= 16 y p <= q <= 4;
7. el umbral efectivo de la prueba para p/q = 4/5 (sólo informativo: la prueba no da
   una cota práctica).

Además, a modo de ilustración y no de evidencia, la distribución del exponente
log(min_{1<=j<=20} T^j(n)) / log n para n en [2^19, 2^20): con log2 n pasos el valor típico
ronda log 3 / log 4 ≈ 0,7925, la barrera de los métodos 2-ádicos.

Un barrido finito no prueba la densidad cero: sólo coteja las piezas exactas de la prueba.
"""

import argparse
import json
from math import log
from pathlib import Path


def paso(n):
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def subidas(n, k):
    s = 0
    for _ in range(k):
        s += n % 2
        n = paso(n)
    return s


def iterar(n, k):
    for _ in range(k):
        n = paso(n)
    return n


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--hasta", type=int, default=18)
    analizador.add_argument("--enteros", type=int, default=2000)
    analizador.add_argument("--salida", type=Path, required=True)
    a = analizador.parse_args()
    informe = {"hasta": a.hasta, "enteros": a.enteros}

    # 1 y 2: momento y Chebyshev, con S_K por órbitas directas.
    momentos, chebyshev = {}, 0
    tablas = {}
    for K in range(a.hasta + 1):
        valores = [subidas(r, K) for r in range(2 ** K)]
        tablas[K] = valores
        m2 = sum((2 * s - K) ** 2 for s in valores)
        assert m2 == K * 2 ** K, (K, m2)
        momentos[K] = m2
        for t in range(K + 1):
            c = sum(1 for s in valores if K + 2 * t <= 2 * s)
            assert c * (2 * t) ** 2 <= K * 2 ** K, (K, t, c)
            chebyshev += 1
    informe["momento_dos"] = {"K": list(momentos), "todos_iguales_a_K_2K": True}
    informe["chebyshev_casos"] = chebyshev

    # 3: conteo por residuos.
    casos3 = 0
    for N in (1000, 4096, 100007):
        sub = {k: [subidas(n, k) for n in range(N)] for k in range(13)}
        for k in range(13):
            for s in range(k + 1):
                izquierda = sum(1 for v in sub[k] if v > s)
                malos = sum(1 for v in tablas[k] if v > s) if k in tablas else \
                    sum(1 for r in range(2 ** k) if subidas(r, k) > s)
                assert izquierda <= (N // 2 ** k + 1) * malos, (N, k, s)
                casos3 += 1
    informe["muchas_por_residuos_casos"] = casos3

    # 4: cota de los residuos con muchas subidas.
    casos4 = []
    for E in range(4):
        m = 1
        while 2 * (E + 1) * m <= a.hasta:
            k = 2 * (E + 1) * m
            for s in range(k + 1):
                if k + 2 * m <= 2 * s + 2:
                    c = sum(1 for v in tablas[k] if v > s)
                    assert 2 * m * c <= (E + 1) * 2 ** k, (E, m, s, c)
                    casos4.append([E, m, k, s, c, (E + 1) * 2 ** k // (2 * m)])
            m += 1
    informe["cota_muchas"] = {"casos": len(casos4), "muestra [E, m, k, s, c, cota]": casos4[:12]}

    # 5: bajar por debajo de una potencia.
    casos5 = 0
    for n in range(a.enteros):
        for k in range(21):
            Sk, Tk = subidas(n, k), iterar(n, k)
            for q in range(1, 5):
                for p in range(q + 1):
                    for s in range(Sk, k + 1):
                        if 3 ** (k - s) <= n and 2 ** q * 3 ** (s * q) * n ** (q - p) <= 2 ** (k * q):
                            assert Tk ** q < n ** p, (n, k, s, p, q)
                            casos5 += 1
    informe["baja_de_potencia_casos"] = casos5

    # 6: condición de potencias, peor caso.
    casos6 = 0
    for E in range(10):
        for m in range(1, 17):
            for q in range(1, 5):
                for p in range(q + 1):
                    hC = (2 ** q * 2 ** (2 * (E + 1) * (q - p)) * (3 ** ((E + 2) * q)) ** m
                          <= (2 ** (2 * (E + 1) * p)) ** m)
                    if hC:
                        N = 2 ** (2 * (E + 1) * (m + 1)) - 1
                        assert (2 ** q * 3 ** ((E + 2) * m * q) * N ** (q - p)
                                <= 2 ** (2 * (E + 1) * m * q)), (E, m, p, q)
                        casos6 += 1
    informe["condicion_casos"] = casos6

    # 7: umbral efectivo de la prueba para p/q = 4/5 (informativo).
    p, q = 4, 5
    E0 = next(M for M in range(10 ** 4)
              if all(3 ** q * (3 ** q) ** m < (4 ** p) ** m for m in range(M, M + 200)))
    A, B = 3 ** ((E0 + 2) * q), 2 ** (2 * (E0 + 1) * p)
    C = 2 ** q * 2 ** (2 * (E0 + 1) * (q - p))
    M = next(M for M in range(10 ** 5) if C * A ** M < B ** M)
    informe["umbral_efectivo_4_5"] = {
        "E0": E0, "M": M,
        "log2_N_minimo": 2 * (E0 + 1) * (M + 1),
        "nota": "la prueba es asintótica: el primer N cubierto tiene unos "
                f"{round(2 * (E0 + 1) * (M + 1) * 0.30103)} dígitos"}

    # Ilustración: exponente de descenso con log2 n pasos.
    minimos, finales = [], []
    for n in range(2 ** 19, 2 ** 20, 7):
        x, menor = n, n
        for _ in range(20):
            x = paso(x)
            menor = min(menor, x)
        minimos.append(log(menor) / log(n))
        finales.append(log(x) / log(n))
    minimos.sort()
    finales.sort()

    def cuantiles(lista):
        return {f"{c:.2f}": round(lista[int(c * (len(lista) - 1))], 4)
                for c in (0.1, 0.25, 0.5, 0.75, 0.9)}

    informe["ilustracion_exponente_20_pasos"] = {
        "muestra": len(minimos),
        "cuantiles_del_minimo_en_20_pasos": cuantiles(minimos),
        "cuantiles_del_valor_tras_20_pasos": cuantiles(finales),
        "umbral_log3_log4": round(log(3) / log(4), 5),
        "nota": "ilustración, no evidencia"}

    informe["resultado"] = "OK"
    a.salida.write_text(json.dumps(informe, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    print(json.dumps(informe, ensure_ascii=False, indent=1)[:3000])


if __name__ == "__main__":
    main()
