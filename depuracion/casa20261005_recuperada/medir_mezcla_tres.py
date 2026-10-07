"""Medición de la mezcla fina 3-ádica del atajo (ruta hacia Tao 2019). No es una prueba.

Uso, desde la raíz del repositorio:

    python -B -X utf8 depuracion/casa20261004/medir_mezcla_tres.py --k 22 --m 9
        --salida depuracion/casa20261004/medicion_mezcla_tres.json

Por `iter_afin` (CasaTres.lean), si r es uniforme módulo 2^k y S_k(r) >= m, el valor
T^k(r) módulo 3^m y la paridad de T^k(r) son independientes. Entonces T^k(r) mod 3^m sigue
la cadena de Markov X -> X/2 (paridad par) o X -> (3X+1)/2 (paridad impar), con divisiones
por 2 en Z/3^m y monedas justas. La ley estacionaria ν_m de esa cadena es la versión, para
el atajo, de la variable de Syracuse de Tao: sum_l 3^(l-1) 2^-(a_1+...+a_l) con huecos
geométricos.

Se mide la oscilación fina de Tao, osc(m', m) = sum_{y mod 3^m} |ν_m(y) - ν_m'(y mod 3^m')/3^(m-m')|,
que la proposición 1.14 de Tao acota por O_A(m'^-A) uniformemente en m >= m'. Se calcula
de dos maneras independientes:

1. por conteo directo de r < 2^k con S_k(r) >= m (órbitas directas, enteros);
2. por la cadena en Z/3^m, iterada en coma flotante desde la ley puntual en 1 hasta que el
   cambio total es < 1e-15. La cadena olvida el estado inicial módulo 3^m en cuanto ha dado
   m subidas, así que converge deprisa; se comprueba además que la proyección de la ley
   módulo 3^m es la ley módulo 3^(m-1).

Se mide también la proposición 1.17 de Tao, el máximo de |E e(ξ X/3^m)| sobre las
frecuencias ξ no divisibles por 3, con la transformada rápida de numpy, y se comprueba la
recurrencia φ_m(ξ) = φ_m(hξ)/2 + e(hξ/3^m) φ_(m-1)(hξ)/2, con h = 2^-1 mod 3^m.

Resultado: una medición en un horizonte finito, no un teorema.
"""

import argparse
import json
from pathlib import Path

import numpy as np


def paso(n):
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def ley_por_conteo(k, m):
    """Ley de T^k(r) mod 3^m entre los r < 2^k con S_k(r) >= m."""
    M = 3 ** m
    cuenta = [0] * M
    total = 0
    for r in range(2 ** k):
        x, s = r, 0
        for _ in range(k):
            s += x % 2
            x = paso(x)
        if s >= m:
            cuenta[x % M] += 1
            total += 1
    return [c / total for c in cuenta], total


def ley_estacionaria(m, pasos=4000):
    """Ley estacionaria de X -> X/2, (3X+1)/2 en Z/3^m con monedas justas (numpy)."""
    M = 3 ** m
    medio = pow(2, -1, M)
    x = np.arange(M, dtype=np.int64)
    destino_par = (x * medio) % M
    destino_impar = ((3 * x + 1) % M * medio) % M
    p = np.zeros(M)
    p[1] = 1.0
    for _ in range(pasos):
        q = (np.bincount(destino_par, weights=p / 2, minlength=M)
             + np.bincount(destino_impar, weights=p / 2, minlength=M))
        cambio = float(np.abs(p - q).sum())
        p = q
        if cambio < 1e-15:
            break
    return p


def oscilacion(ley_fina, ley_gruesa, m, mp):
    y = np.arange(3 ** m)
    return float(np.abs(np.asarray(ley_fina) - np.asarray(ley_gruesa)[y % 3 ** mp]
                        / 3 ** (m - mp)).sum())


def proyectar(ley, m, mp):
    return np.bincount(np.arange(3 ** m) % 3 ** mp, weights=np.asarray(ley), minlength=3 ** mp)


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--k", type=int, default=22)
    analizador.add_argument("--m", type=int, default=9)
    analizador.add_argument("--salida", type=Path, required=True)
    a = analizador.parse_args()
    informe = {"k": a.k, "m": a.m}

    estacionarias = {m: ley_estacionaria(m) for m in range(1, a.m + 1)}
    # La proyección de la ley estacionaria de 3^m a 3^(m-1) es la estacionaria de 3^(m-1).
    for m in range(2, a.m + 1):
        d = float(np.abs(proyectar(estacionarias[m], m, m - 1) - estacionarias[m - 1]).sum())
        assert d < 1e-9, (m, d)
    informe["ley_mod_3"] = [round(float(v), 6) for v in estacionarias[1]]
    tabla = {}
    for m in range(2, a.m + 1):
        tabla[m] = {mp: round(oscilacion(estacionarias[m], estacionarias[mp], m, mp), 6)
                    for mp in sorted({1, max(1, m - 3), m - 1})}
    informe["osc_estacionaria (m -> {m': osc(m', m)})"] = tabla

    mc = min(a.m, 7)
    ley, total = ley_por_conteo(a.k, mc)
    dist = float(np.abs(np.asarray(ley) - estacionarias[mc]).sum())
    informe["conteo_directo"] = {
        "k": a.k, "m": mc, "residuos_con_S>=m": total,
        "distancia_total_a_la_estacionaria": round(dist, 6),
        "osc_por_conteo": {mp: round(oscilacion(ley, proyectar(ley, mc, mp), mc, mp), 6)
                           for mp in range(1, mc)}}
    # Proposición 1.17 de Tao: max_{3 no divide a xi} |E e(xi X / 3^m)| = O_A(m^-A).
    fourier = {}
    for m in range(1, a.m + 1):
        coef = np.abs(np.fft.fft(estacionarias[m]))
        coprimos = np.arange(3 ** m) % 3 != 0
        fourier[m] = round(float(coef[coprimos].max()), 6)
    # Recurrencia de la función característica de la ley estacionaria, con h = 2^-1 mod 3^m:
    # phi_m(xi) = phi_m(h xi)/2 + e(h xi / 3^m) phi_(m-1)(h xi mod 3^(m-1)) / 2.
    peor = 0.0
    for m in range(2, min(a.m, 10) + 1):
        M = 3 ** m
        h = pow(2, -1, M)
        F, G = np.fft.fft(estacionarias[m]), np.fft.fft(estacionarias[m - 1])
        xi = np.arange(M)
        hx = (h * xi) % M
        derecha = F[hx] / 2 + np.exp(-2j * np.pi * hx / M) * G[hx % (M // 3)] / 2
        peor = max(peor, float(np.abs(F - derecha).max()))
    assert peor < 1e-9, peor
    informe["recurrencia_fourier_error_max (m <= 10)"] = peor
    informe["razones_fourier (m -> M_m / M_(m-1))"] = {
        m: round(fourier[m] / fourier[m - 1], 4) for m in range(2, a.m + 1)}
    informe["fourier_max_coprimo (m -> max |phi_m(xi)|, 3 no divide a xi)"] = fourier
    informe["nota"] = ("medición en horizonte finito; la proposición 1.14 de Tao pide "
                       "osc(m', m) = O_A(m'^-A) uniforme en m >= m', y la 1.17 pide "
                       "max |phi_m(xi)| = O_A(m^-A)")
    a.salida.write_text(json.dumps(informe, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    print(json.dumps(informe, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
