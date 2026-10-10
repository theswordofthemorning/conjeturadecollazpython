"""Contraste exacto de la sexta raíz, los regresos y el techo de Perdices.

Cálculo independiente de PerdicesSexta.lean, sólo con enteros: sin raíces,
sin coma flotante. Recorre prefijos finitos de órbitas reales; no busca
fugitivos infinitos. Un barrido finito no prueba el enunciado universal.

Mapa: T(x) = x/2 si x es par y (3x+1)/2 si es impar. S_k cuenta las
entradas impares de los instantes j < k; el pronóstico es P_k = 3^S_k/2^k.

Uso:
python -B -X utf8 depuracion/perdices20261007/cotejar_sexta.py
    --n-max 4096 --pasos 300 --techo-max 12 --q-max 2000 --m-max 14
    --salida depuracion/perdices20261007/cotejo_sexta.json
"""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def paso(x):
    if x % 2 == 0:
        return x // 2
    return (3 * x + 1) // 2


def lema_finito_exhaustivo(m_max):
    """Todos los subconjuntos de los impares 3, 5, ..., 2*m_max+1."""
    impares = [2 * i + 1 for i in range(1, m_max + 1)]
    casos = 0
    for mascara in range(1 << len(impares)):
        elegidos = [a for i, a in enumerate(impares) if mascara >> i & 1]
        q = len(elegidos)
        if q > 0:
            # impar_mayor: el mayor vale al menos 2q+1
            assert max(elegidos) >= 2 * q + 1
        # producto_sexta: (prod (1 + 1/(3a)))^6 <= q + 1, sin fracciones
        arriba, abajo = 1, 1
        for a in elegidos:
            arriba *= (3 * a + 1) ** 6
            abajo *= (3 * a) ** 6
        assert arriba <= (q + 1) * abajo
        casos += 1
    return casos


def cadena_extrema(q_max):
    """El caso más apretado del telescopio: los q primeros impares desde 3."""
    arriba, abajo = 1, 1
    for r in range(1, q_max + 1):
        arriba *= (6 * r + 4) ** 6
        abajo *= (6 * r + 3) ** 6
        assert arriba <= (r + 1) * abajo
    return q_max


def contraste_orbita(n, pasos, techos, cuentas):
    valores, subidas = [n], [0]
    for _ in range(pasos):
        x = valores[-1]
        valores.append(paso(x))
        subidas.append(subidas[-1] + x % 2)

    # Sexta raíz general: vale en el instante k mientras las entradas
    # impares de los instantes j < k sean distintas y al menos 3.
    impares = set()
    for k in range(pasos + 1):
        x, s = valores[k], subidas[k]
        assert (2 ** k * x) ** 6 <= 3 ** (6 * s) * n ** 6 * (s + 1)
        cuentas["sexta_general"] += 1
        if k == pasos:
            break
        if x % 2 == 1:
            if x < 3 or x in impares:
                break
            impares.add(x)

    if n < 2:
        return
    # Prefijo vivo de largo K: P_j >= 1 y valores distintos para todo j < K.
    vistos = set()
    regresos = [0] * len(techos)
    mayor = None
    for K in range(1, pasos + 2):
        j = K - 1
        x, s = valores[j], subidas[j]
        if 3 ** s < 2 ** j or x in vistos:
            break
        vistos.add(x)
        assert x >= n
        cuentas["prefijos_vivos"] += 1
        for i, c in enumerate(techos):
            if 3 ** s <= c * 2 ** j:
                # regreso_sexta y regreso_sexta_real
                assert x ** 6 <= c ** 6 * n ** 6 * (s + 1)
                cuentas["regresos"] += 1
                regresos[i] += 1
            # cuenta_regresos, cuenta_regresos_real y, por ser entera la
            # cuenta, cuenta_regresos_raiz: cuenta <= floor(c n K^(1/6))
            assert regresos[i] ** 6 <= c ** 6 * n ** 6 * K
            cuentas["cuentas_de_regresos"] += 1
        # techo_sube: algún j < K cumple K^5 2^(6j) <= n^6 3^(6 S_j);
        # basta mirar el mayor pronóstico 3^S/2^j del prefijo.
        if mayor is None or 3 ** s * mayor[1] > mayor[0] * 2 ** j:
            mayor = (3 ** s, 2 ** j)
        assert K ** 5 * mayor[1] ** 6 <= n ** 6 * mayor[0] ** 6
        cuentas["techos"] += 1
        cuentas["largo_maximo"] = max(cuentas["largo_maximo"], K)


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--n-max", type=int, required=True)
    analizador.add_argument("--pasos", type=int, required=True)
    analizador.add_argument("--techo-max", type=int, required=True)
    analizador.add_argument("--q-max", type=int, required=True)
    analizador.add_argument("--m-max", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    assert 0 <= args.n_max <= 20000
    assert 0 <= args.pasos <= 1000
    assert 0 <= args.techo_max <= 50
    assert 0 <= args.q_max <= 5000
    assert 0 <= args.m_max <= 16

    subconjuntos = lema_finito_exhaustivo(args.m_max)
    cadena = cadena_extrema(args.q_max)

    semillas = sorted(set(range(1, args.n_max + 1)) |
                      {2 ** b - 1 for b in (2, 3, 5, 10, 20, 30, 64)})
    cuentas = {"sexta_general": 0, "prefijos_vivos": 0, "regresos": 0,
               "cuentas_de_regresos": 0, "techos": 0, "largo_maximo": 0}
    # Techos naturales 0..techo_max y algunos techos racionales.
    techos = [Fraction(c) for c in range(args.techo_max + 1)]
    techos += [Fraction(1, 2), Fraction(2, 3), Fraction(5, 4), Fraction(3, 2), Fraction(7, 3)]
    for n in semillas:
        contraste_orbita(n, args.pasos, techos, cuentas)

    # Borde: con n = 1 la entrada impar 1 es menor que 3 y la cota se rompe
    # en k = 1: R_1 = 4/3 y (4/3)^6 > 2 = n^6 (S_1 + 1). La hipótesis hace falta.
    assert (2 ** 1 * paso(1)) ** 6 > 3 ** 6 * 1 ** 6 * (1 + 1)
    # Borde: n = 2 cruza en el primer paso; su único prefijo vivo es K = 1.
    assert paso(2) == 1 and 3 ** 0 < 2 ** 1

    evidencia = {
        "estado": "contraste exacto terminado",
        "sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "parametros": {"n_max": args.n_max, "pasos": args.pasos,
                       "techo_max": args.techo_max, "q_max": args.q_max,
                       "m_max": args.m_max},
        "semillas": len(semillas),
        "techos": [str(c) for c in techos],
        "subconjuntos_impares": subconjuntos,
        "cadena_extrema_hasta_q": cadena,
        "cuentas": cuentas,
        "bordes": ["n=1 rompe la cota sin la hipótesis >= 3 (R_1 = 4/3)",
                   "n=2: prefijo vivo sólo K=1", "c=0: sin regresos", "K=1"],
        "alcance": "Contraste finito de PerdicesSexta.lean; el enunciado universal "
                   "es el teorema de Lean, no este barrido.",
    }
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(json.dumps(evidencia, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps(evidencia, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
