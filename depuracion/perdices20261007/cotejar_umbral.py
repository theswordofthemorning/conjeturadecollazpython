"""Cuenta prefijos sin cruce, su frontera y bloques con reserva, con enteros.

La DP usa palabras y una cadena arrancada en cero. La comparación independiente
enumera enteros, itera Collatz y calcula su pronóstico como Fraction. La ley
artificial sólo se identifica con la real cuando todas las palabras han tenido
al menos m subidas. No se extraen conclusiones asintóticas del barrido finito.
"""

import argparse
from collections import defaultdict
from fractions import Fraction
import hashlib
import json
from itertools import product
from math import comb
from pathlib import Path

from cotejar_acoplamiento import estacionaria_por_geometrica


def huella(ruta):
    return hashlib.sha256(Path(ruta).read_bytes()).hexdigest()


def tv(p, q):
    return sum((abs(a - b) for a, b in zip(p, q)), Fraction(0)) / 2


def proyectar(vector, modulo):
    salida = [0] * modulo
    for x, cuenta in enumerate(vector):
        salida[x % modulo] += cuenta
    return salida


def resumir(numero):
    return {"exacto": str(numero), "aproximado": float(numero)}


def avanzar(estados, k, modulo):
    """D[k+1,s+b,f_b(x)] += D[k,s,x] si el nuevo prefijo sobrevive."""
    siguientes = defaultdict(int)
    for (s, x), cuenta in estados.items():
        for b in (0, 1):
            if 3 ** (s + b) >= 2 ** (k + 1):
                y = ((3 * x + 1) if b else x) * pow(2, -1, modulo) % modulo
                siguientes[s + b, y] += cuenta
    return dict(siguientes)


def margenes(estados, modulo):
    subidas = defaultdict(int)
    residuos = [0] * modulo
    for (s, x), cuenta in estados.items():
        subidas[s] += cuenta
        residuos[x] += cuenta
    return dict(subidas), residuos


def frontera_independiente(estados, nuevos, k, modulo):
    """Todas las ramas menos las bajadas prohibidas: identidad de vectores."""
    libre, borrado = [0] * modulo, [0] * modulo
    inverso = (modulo + 1) // 2
    n, b = sum(estados.values()), 0
    for (s, x), cuenta in estados.items():
        assert 3 ** s >= 2 ** k
        assert 3 ** (s + 1) >= 2 ** (k + 1)
        y0, y1 = x * inverso % modulo, (3 * x + 1) * inverso % modulo
        libre[y0] += cuenta
        libre[y1] += cuenta
        if 3 ** s < 2 ** (k + 1):
            b += cuenta
            borrado[y0] += cuenta
    _, vector = margenes(nuevos, modulo)
    total = sum(vector)
    assert total == 2 * n - b > 0
    assert vector == [a - e for a, e in zip(libre, borrado)]
    ley = [Fraction(c, total) for c in vector]
    sin_borrar = [Fraction(c, 2 * n) for c in libre]
    distancia = tv(ley, sin_borrar)
    epsilon = Fraction(b, 2 * n)
    if b:
        eliminada = [Fraction(c, b) for c in borrado]
        assert distancia == epsilon * tv(ley, eliminada)
    else:
        assert distancia == 0
    assert distancia <= epsilon <= Fraction(1, 2)
    return {"padres": n, "frontera": b, "supervivientes": total,
            "fraccion_borrada": resumir(epsilon), "tv_paso_libre": resumir(distancia)}


def contraste_enteros(k, m_max, estados, historial):
    """No usa avanzar: enteros reales, pronóstico multiplicativo y rama natural."""
    modulo = 3 ** m_max
    artificial, real = defaultdict(int), defaultdict(int)
    reservas = [0] * (k + 1)
    for n in range(2 ** k):
        x, y, s, pronostico = n, 0, 0, Fraction(1)
        acumuladas, vivo = [0], True
        for _ in range(k):
            b = x % 2
            pronostico *= Fraction(3 if b else 1, 2)
            if pronostico < 1:
                vivo = False
            x = (3 * x + 1) // 2 if b else x // 2
            y = ((3 * y + 1) if b else y) * ((modulo + 1) // 2) % modulo
            s += b
            acumuladas.append(s)
        if vivo:
            artificial[s, y] += 1
            real[s, x % modulo] += 1
            for longitud in range(k + 1):
                reservas[longitud] += int(3 ** acumuladas[k - longitud] >= 2 ** k)
    assert dict(artificial) == estados, k
    comparaciones = 0
    for m in range(m_max + 1):
        a, r = defaultdict(int), defaultdict(int)
        for (s, x), cuenta in artificial.items():
            if s >= m:
                a[s, x % (3 ** m)] += cuenta
        for (s, x), cuenta in real.items():
            if s >= m:
                r[s, x % (3 ** m)] += cuenta
        assert dict(a) == dict(r), (k, m)
        comparaciones += sum(a.values())
    for longitud in range(k + 1):
        padres_seguros = sum(c for s, c in historial[k - longitud].items() if 3 ** s >= 2 ** k)
        assert reservas[longitud] == padres_seguros * 2 ** longitud, (k, longitud)
    return {"enteros": 2 ** k, "sincronizaciones": comparaciones,
            "fibras_con_reserva": k + 1}


def contraste_reserva():
    """Criterio universal de bloques contrastado por enumeración finita independiente."""
    triples, palabras = 0, 0
    for k in range(9):
        for s in range(9):
            inicial = Fraction(3 ** s, 2 ** k)
            for longitud in range(8):
                todas = True
                for w in product((0, 1), repeat=longitud):
                    p, viva = inicial, inicial >= 1
                    for b in w:
                        p *= Fraction(3 if b else 1, 2)
                        viva = viva and p >= 1
                    todas = todas and viva
                    palabras += 1
                assert todas == (inicial >= 2 ** longitud), (k, s, longitud)
                triples += 1
    return {"triples_k_s_L": triples, "palabras": palabras,
            "k_max": 8, "s_max": 8, "L_max": 7}


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--m-max", type=int, required=True)
    analizador.add_argument("--pasos", type=int, required=True)
    analizador.add_argument("--directo", type=int, required=True)
    analizador.add_argument("--bloque-max", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    a = analizador.parse_args()
    if not (1 <= a.m_max <= 3 and 1 <= a.pasos <= 400 and
            0 <= a.directo <= min(14, a.pasos) and 1 <= a.bloque_max <= 40):
        analizador.error("Presupuesto: 1<=m<=3, 1<=pasos<=400, directo<=min(14,pasos), bloque<=40")
    modulo = 3 ** a.m_max
    estacionarias = [[Fraction(1)]]
    for _ in range(a.m_max):
        estacionarias.append(estacionaria_por_geometrica(estacionarias[-1]))
    estados, historial = {(0, 0): 1}, [{0: 1}]
    directos = [contraste_enteros(0, a.m_max, estados, historial)]
    muestras, cotas, identidades = {}, 0, 0
    for k in range(1, a.pasos + 1):
        nuevos = avanzar(estados, k - 1, modulo)
        frontera = frontera_independiente(estados, nuevos, k - 1, modulo)
        identidades += 1
        estados = nuevos
        subidas, residuos = margenes(estados, modulo)
        historial.append(subidas)
        total = sum(residuos)
        if k <= a.directo:
            directos.append(contraste_enteros(k, a.m_max, estados, historial))
        guardar = k in {1, 2, 3, 10, 20, 50, 100, 200, a.pasos} or k >= a.pasos - 5
        dato = {"frontera": frontera, "minimo_subidas": min(subidas), "niveles": {}}
        for m in range(1, a.m_max + 1):
            ley = [Fraction(c, total) for c in proyectar(residuos, 3 ** m)]
            distancia = tv(ley, estacionarias[m])
            mejor = None
            for longitud in range(1, min(k, a.bloque_max) + 1):
                padres = sum(c for s, c in historial[k - longitud].items() if 3 ** s >= 2 ** k)
                g = Fraction(padres * 2 ** longitud, total)
                q = Fraction(sum(comb(longitud, j) for j in range(min(m, longitud + 1))),
                             2 ** longitud)
                cota = 1 - g * (1 - q)
                assert 0 <= g <= 1 and distancia <= cota <= 1, (k, m, longitud)
                cotas += 1
                if mejor is None or cota < mejor[0]:
                    mejor = (cota, longitud, g, q)
            if guardar:
                dato["niveles"][m] = {
                    "ley_igual_a_enteros_reales": min(subidas) >= m,
                    "tv_estacionaria": resumir(distancia), "mejor_cota_reserva": resumir(mejor[0]),
                    "longitud_bloque": mejor[1], "fraccion_con_reserva": resumir(mejor[2]),
                    "cola_binomial": resumir(mejor[3])}
                if m == 1:
                    dato["niveles"][m]["ley"] = list(map(str, ley))
        if guardar:
            muestras[k] = dato
            print(f"k={k}: {total.bit_length()} bits en la cuenta; "
                  f"TV módulo 3={float(tv([Fraction(c, total) for c in proyectar(residuos, 3)], estacionarias[1])):.8f}",
                  flush=True)
    if 3 in muestras:
        assert muestras[3]["niveles"][1]["ley"] == ["0", "1/2", "1/2"]
    informe = {
        "estado": "identidades, cotas y contrastes exactos correctos",
        "parametros": {"m_max": a.m_max, "pasos": a.pasos, "directo": a.directo,
                       "bloque_max": a.bloque_max},
        "fuentes": {Path(__file__).name: huella(__file__),
                    "cotejar_acoplamiento.py": huella(Path(__file__).with_name("cotejar_acoplamiento.py"))},
        "convencion": "TV=media suma absoluta; palabras uniformes condicionadas a cada prefijo sin cruce",
        "limite": "DP desde cero; coincide con enteros reales sólo si minimo_subidas>=m; sin conclusion asintotica",
        "identidades_frontera": identidades, "cotas_bloques": cotas,
        "reserva_independiente": contraste_reserva(),
        "contraste_independiente": {clave: sum(d[clave] for d in directos) for clave in directos[0]},
        "muestras": muestras}
    a.salida.parent.mkdir(parents=True, exist_ok=True)
    a.salida.write_text(json.dumps(informe, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK: {identidades} identidades, {cotas} cotas, {informe['contraste_independiente']}")


if __name__ == "__main__":
    main()
