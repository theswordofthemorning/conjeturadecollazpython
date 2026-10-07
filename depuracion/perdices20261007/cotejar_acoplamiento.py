"""Contrastes exactos de Perdices: sincronización, ley condicionada y estacionaria.

No importa experimentos antiguos. Usa Fraction para probabilidades, errores y
oscilaciones. Los valores decimales del informe son sólo representaciones.
Uso: python -B -X utf8 depuracion/perdices20261007/cotejar_acoplamiento.py
    --m-max 6 --k-max 10 --pasos 60 --salida RUTA_JSON
"""

import argparse
from fractions import Fraction
import hashlib
from itertools import product
import json
from math import comb
from pathlib import Path


def atajo(n):
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def cadena(palabra, x, modulo):
    medio = pow(2, -1, modulo)
    for bit in palabra:
        x = ((3 * x + 1 if bit else x) * medio) % modulo
    return x % modulo


def estacionaria_por_ciclos(anterior):
    """Resuelve p(x)=(p(2x)+b(x))/2 en cada ciclo de la duplicación.

    b(x) es anterior((2x-1)/3) si x=2 mod 3, y cero en otro caso.
    No aproxima un punto fijo por iteraciones.
    """
    modulo = 3 * len(anterior)
    ley = [Fraction(0)] * modulo
    pendientes = set(range(modulo))
    while pendientes:
        inicio = min(pendientes)
        ciclo, x = [], inicio
        while x in pendientes:
            ciclo.append(x)
            pendientes.remove(x)
            x = 2 * x % modulo
        assert x == inicio
        termino = [anterior[((2 * x - 1) // 3) % len(anterior)]
                   if x % 3 == 2 else Fraction(0) for x in ciclo]
        largo = len(ciclo)
        valor = sum((2 ** (largo - 1 - i) * b for i, b in enumerate(termino)),
                    Fraction(0)) / (2 ** largo - 1)
        inicial = valor
        for x, b in zip(ciclo, termino):
            ley[x] = valor
            valor = 2 * valor - b
        assert valor == inicial
    return ley


def estacionaria_por_geometrica(anterior):
    """Segundo cálculo: suma exactamente A~Geom(2) por clases de su período.

    Fórmula (1.26) y lema 1.12 de Tao: X_m=(3 X_(m-1)+1)/2^A.
    """
    modulo = 3 * len(anterior)
    periodo = 2 * len(anterior)
    denominador = 2 ** periodo - 1
    ley = [Fraction(0)] * modulo
    medio = pow(2, -1, modulo)
    for x, masa in enumerate(anterior):
        y = 3 * x + 1
        for a in range(1, periodo + 1):
            y = y * medio % modulo
            ley[y] += masa * Fraction(2 ** (periodo - a), denominador)
    return ley


def propagar(cuenta):
    modulo = len(cuenta)
    medio = pow(2, -1, modulo)
    nueva = [0] * modulo
    for x, masa in enumerate(cuenta):
        nueva[x * medio % modulo] += masa
        nueva[(3 * x + 1) * medio % modulo] += masa
    return nueva


def variacion(ley, otra):
    """Convención sup_A |mu(A)-nu(A)| = (1/2) suma |mu-nu|."""
    return sum((abs(a - b) for a, b in zip(ley, otra)), Fraction(0)) / 2


def cola_binomial(k, m):
    return Fraction(sum(comb(k, j) for j in range(min(m, k + 1))), 2 ** k)


def resumen(valor):
    return {"exacto": str(valor), "decimal": float(valor)}


def contrastar_palabras(k_max, m_max, leyes):
    casos, sincronizaciones, pares, cotas = 0, 0, 0, 0
    for k in range(k_max + 1):
        for m in range(min(m_max, 4) + 1):
            modulo = 3 ** m
            desde_enteros, desde_palabras, todos = [0] * modulo, [0] * modulo, [0] * modulo
            for n in range(2 ** k):
                x, subidas = n, 0
                for _ in range(k):
                    subidas += x % 2
                    x = atajo(x)
                if subidas >= m:
                    desde_enteros[x % modulo] += 1
                todos[x % modulo] += 1
                casos += 1
            for palabra in product((0, 1), repeat=k):
                if sum(palabra) >= m:
                    y = cadena(palabra, 0, modulo)
                    desde_palabras[y] += 1
                    # Bordes y dos puntos interiores; la prueba universal está en Lean.
                    for x in {0, 1, modulo // 2, modulo - 1, modulo + 1}:
                        assert cadena(palabra, x, modulo) == y
                        sincronizaciones += 1
            assert desde_enteros == desde_palabras, (k, m)
            total = sum(desde_enteros)
            assert total == sum(comb(k, j) for j in range(m, k + 1))
            assert variacion([Fraction(c, 2 ** k) for c in todos], leyes[m]) <= cola_binomial(k, m)
            cotas += 1
            if total:
                assert variacion([Fraction(c, total) for c in desde_enteros], leyes[m]) <= cola_binomial(k, m)
                cotas += 1
            pares += 1
    return {"orbitas": casos, "sincronizaciones": sincronizaciones,
            "pares_k_m": pares, "cotas_desde_enteros": cotas}


def contrastar_sesgo(leyes):
    casos = 0
    for k in range(65):
        x = 2 ** k - 1
        for j in range(k + 1):
            assert x == 3 ** j * 2 ** (k - j) - 1
            if j < k:
                assert x % 2 == 1
            x = atajo(x)
            casos += 1
        for m in range(min(k, len(leyes) - 1) + 1):
            assert cadena((1,) * k, 0, 3 ** m) == 3 ** m - 1
    resultado = {"casos_formula_enteros": casos, "k_max": 64}
    if len(leyes) > 2:
        distancia = variacion([Fraction(int(x == 8)) for x in range(9)], leyes[2])
        assert distancia == Fraction(41, 63)
        resultado["tv_palabra_solo_unos_mod_9"] = resumen(distancia)
    return resultado


def contrastar_no_cruce():
    """Prueba finita independiente: pronóstico como producto de Fraction."""
    supervivientes, salidas = [], []
    for n in range(8):
        x, pronostico, sobrevive = n, Fraction(1), True
        for _ in range(3):
            pronostico *= Fraction(3 if x % 2 else 1, 2)
            sobrevive = sobrevive and pronostico >= 1
            x = atajo(x)
        if sobrevive:
            supervivientes.append(n)
            salidas.append(x)
    assert supervivientes == [3, 7] and salidas == [4, 26]
    ley = [Fraction(sum(x % 3 == r for x in salidas), len(salidas)) for r in range(3)]
    distancia = variacion(ley, [Fraction(0), Fraction(1, 3), Fraction(2, 3)])
    cota = cola_binomial(3, 1)
    assert distancia == Fraction(1, 6) > cota == Fraction(1, 8)
    return {"k": 3, "m": 1, "supervivientes": supervivientes, "salidas": salidas,
            "ley_condicionada": list(map(str, ley)), "tv": str(distancia),
            "cota_sin_condicionar": str(cota), "conclusion": "la cota no se hereda"}


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--m-max", type=int, required=True)
    analizador.add_argument("--k-max", type=int, required=True)
    analizador.add_argument("--pasos", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    a = analizador.parse_args()
    if not (0 <= a.m_max <= 7 and 0 <= a.k_max <= 16 and 0 <= a.pasos <= 200):
        analizador.error("Presupuesto: m<=7, k<=16 y pasos<=200, todos no negativos")
    leyes = [[Fraction(1)]]
    informe = {"parametros": {"m_max": a.m_max, "k_max": a.k_max, "pasos": a.pasos},
               "sha256_comprobador": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "convencion": "TV=1/2 suma absoluta; oscilacion=suma absoluta",
               "estacionarias": {}, "cotas": {}}
    cotas = 0
    for m in range(a.m_max + 1):
        if m:
            p = estacionaria_por_ciclos(leyes[-1])
            assert p == estacionaria_por_geometrica(leyes[-1]), m
            leyes.append(p)
        else:
            p = leyes[0]
        assert sum(p) == 1 and min(p) >= 0
        assert [x / 2 for x in propagar(p)] == p
        if m:
            assert all(sum(p[y::3 ** (m - 1)]) == leyes[m - 1][y]
                       for y in range(3 ** (m - 1)))
            assert all(p[y] == 0 for y in range(0, 3 ** m, 3))
        informe["estacionarias"][m] = {
            "estados": len(p),
            "sha256_vector_racional": hashlib.sha256("\n".join(map(str, p)).encode()).hexdigest(),
            "oscilacion": {mp: resumen(sum(
                (abs(p[y] - leyes[mp][y % (3 ** mp)] / 3 ** (m - mp)) for y in range(len(p))),
                Fraction(0))) for mp in sorted({0, max(0, m - 1), m})}}
        if m <= 2:
            informe["estacionarias"][m]["vector"] = list(map(str, p))
        # Se prueban todos los arranques hasta m=2 y cinco arranques para los otros niveles.
        arranques = range(len(p)) if m <= 2 else sorted({0, 1, 2, len(p) // 2, len(p) - 1})
        for x in arranques:
            cuenta = [int(y == x) for y in range(len(p))]
            for k in range(a.pasos + 1):
                distancia = variacion([Fraction(c, 2 ** k) for c in cuenta], p)
                cota = cola_binomial(k, m)
                assert distancia <= cota, (m, k, x, distancia, cota)
                if x == 0 and k in {0, m, 2 * m, 4 * m, 8 * m, a.pasos}:
                    informe["cotas"][f"m={m},k={k}"] = {
                        "tv_desde_cero": resumen(distancia), "cola_binomial": resumen(cota)}
                cuenta = propagar(cuenta)
                cotas += 1
        print(f"m={m}: {len(p)} estados, estacionaria exacta por dos métodos", flush=True)
    if a.m_max >= 2:
        assert leyes[2] == [Fraction(v, 63) for v in (0, 8, 16, 0, 11, 4, 0, 2, 22)]
    informe["contraste_palabras"] = contrastar_palabras(a.k_max, a.m_max, leyes)
    informe["sesgo"] = contrastar_sesgo(leyes)
    informe["condicionamiento_no_cruce"] = contrastar_no_cruce()
    informe["cotas_verificadas"] = cotas
    informe["estado"] = "todos los contrastes exactos correctos"
    a.salida.parent.mkdir(parents=True, exist_ok=True)
    a.salida.write_text(json.dumps(informe, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK: {cotas} cotas; {informe['contraste_palabras']}")


if __name__ == "__main__":
    main()
