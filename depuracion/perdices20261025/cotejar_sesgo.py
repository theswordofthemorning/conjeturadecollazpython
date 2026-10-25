"""Contrasta el sesgo de frontera y la no convergencia modular de supervivientes.

No importa experimentos anteriores. DP por (subidas, residuo), palabras
literales y orbitas enteras se cotejan por separado, con enteros y Fraction.
"""

import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


CARPETA = Path(__file__).resolve().parent
RAIZ = CARPETA.parents[1]


def umbral(k):
    s = 0
    while 3 ** s < 2 ** k:
        s += 1
    return s


def recorre_palabra(palabra):
    pronostico, vivo, residuo = Fraction(1), True, 0
    for bit in palabra:
        pronostico *= Fraction(3 if bit else 1, 2)
        vivo = vivo and pronostico >= 1
        residuo = ((3 * residuo + 1) if bit else residuo) * 2 % 3
    return vivo, pronostico, residuo


def cuentas(horizonte):
    estados, filas = Counter({(0, 0): 1}), []
    for k in range(horizonte + 1):
        n = sum(estados.values())
        frontera = Counter({(s, x): c for (s, x), c in estados.items()
                            if 3 ** s < 2 ** (k + 1)})
        b = sum(frontera.values())
        r = sum(c for (s, x), c in estados.items() if x == 1)
        rb = sum(c for (s, x), c in frontera.items() if x == 1)
        filas.append(dict(N=n, B=b, R=r, RB=rb, s=umbral(k), estados=estados.copy()))
        nuevos = Counter()
        for (s, x), c in estados.items():
            if 3 ** s >= 2 ** (k + 1):
                nuevos[s, 2 * x % 3] += c
            nuevos[s + 1, 2] += c
        estados = nuevos
    return filas


def frontera_alta(k, fila):
    return 3 * 2 ** k <= 2 * 3 ** fila["s"] < 4 * 2 ** k


def contraste_directo(filas, directo):
    total_palabras, total_enteros, inyecciones = 0, 0, 0
    for k in range(directo + 1):
        palabras, enteros, imagen = Counter(), Counter(), set()
        for palabra in product((0, 1), repeat=k):
            vivo, pronostico, residuo = recorre_palabra(palabra)
            total_palabras += 1
            if not vivo:
                continue
            s = sum(palabra)
            palabras[s, residuo] += 1
            if k and Fraction(3, 2) <= pronostico < 2 and residuo == 1:
                ceros = 0
                while palabra[k - 1 - ceros] == 0:
                    ceros += 1
                assert ceros % 2 == 1
                prefijo = palabra[:k - ceros - 1]
                transformada = prefijo + (0, 1) + (0,) * (ceros - 1)
                v, p, x = recorre_palabra(transformada)
                assert v and p == pronostico and x == 2
                assert transformada not in imagen
                imagen.add(transformada)
                inyecciones += 1
        for n in range(2 ** k):
            x, s, pronostico, vivo = n, 0, Fraction(1), True
            for _ in range(k):
                impar = x % 2
                s += impar
                pronostico *= Fraction(3 if impar else 1, 2)
                vivo = vivo and pronostico >= 1
                x = (3 * x + 1) // 2 if impar else x // 2
            total_enteros += 1
            if vivo:
                enteros[s, x % 3] += 1
        assert palabras == filas[k]["estados"] == enteros
        if frontera_alta(k, filas[k]):
            assert len(imagen) == filas[k]["RB"]
    return dict(palabras=total_palabras, enteros=total_enteros,
                pares_de_la_inyeccion=inyecciones)


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--horizonte", type=int, required=True)
    analizador.add_argument("--directo", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    if not (16 <= args.horizonte <= 400 and 0 <= args.directo <= min(14, args.horizonte)):
        analizador.error("Se exige 16<=horizonte<=400 y 0<=directo<=min(14,horizonte)")
    filas = cuentas(args.horizonte)
    directos = contraste_directo(filas, args.directo)
    fronteras_altas, identidades, pares_con_piso = 0, 0, 0
    distancias = [None] + [abs(Fraction(f["R"], f["N"]) - Fraction(1, 3)) for f in filas[1:]]
    for k in range(1, args.horizonte):
        f, g = filas[k], filas[k + 1]
        assert g["N"] == 2 * f["N"] - f["B"]
        assert g["R"] == f["N"] - f["R"] - f["B"] + f["RB"]
        d = Fraction(f["R"], f["N"]) - Fraction(1, 3)
        siguiente = Fraction(g["R"], g["N"]) - Fraction(1, 3)
        assert f["N"] * d + g["N"] * siguiente == f["RB"] - Fraction(2 * f["B"], 3)
        identidades += 1
        if frontera_alta(k, f):
            assert 2 * f["RB"] <= f["B"]
            assert max(distancias[k], distancias[k + 1]) >= Fraction(f["B"], 18 * f["N"])
            fronteras_altas += 1
        if f["B"] == 0:
            assert siguiente == -d / 2
    traslados = []
    for k in range(args.horizonte - 7):
        f = filas[k]
        assert filas[k + 8]["s"] >= f["s"] + 5
        h = next(h for h in (k + 1, k + 3, k + 5, k + 7)
                 if filas[h]["s"] == filas[h - 1]["s"] + 1 and
                 filas[h + 1]["s"] == filas[h]["s"] + 1)
        assert frontera_alta(h, filas[h])
        if 16 * f["B"] < f["N"]:
            continue
        g = filas[h]
        assert g["B"] >= f["B"] and g["N"] <= 2 ** (h - k) * f["N"]
        assert Fraction(g["B"], g["N"]) >= Fraction(1, 2048)
        elegido = h if distancias[h] >= distancias[h + 1] else h + 1
        assert distancias[elegido] >= Fraction(1, 36864)
        assert k + 1 <= elegido <= k + 8
        traslados.append(dict(padre=k, frontera_alta=h, horizonte_con_piso=elegido))
        pares_con_piso += 1
    for inicio in range(args.horizonte - 2):
        assert filas[inicio + 3]["s"] <= filas[inicio]["s"] + 2
        assert any(filas[k]["B"] == 0 for k in range(inicio, inicio + 3))
        if inicio:
            diferencias = [abs(Fraction(filas[k + 1]["R"], filas[k + 1]["N"]) -
                               Fraction(filas[k]["R"], filas[k]["N"]))
                           for k in range(inicio, inicio + 3)]
            assert distancias[inicio] <= 3 * max(diferencias)
    multiplicidades = Counter(t["horizonte_con_piso"] for t in traslados)
    assert max(multiplicidades.values(), default=0) <= 8
    anteriores = RAIZ / "depuracion/perdices20261007/cotejo_umbral.json"
    previo = json.loads(anteriores.read_text(encoding="utf-8"))
    coincidencias = 0
    for clave, dato in previo["muestras"].items():
        k = int(clave)
        if k <= args.horizonte:
            assert distancias[k] == Fraction(dato["niveles"]["1"]["tv_estacionaria"]["exacto"])
            coincidencias += 1
    resultado = dict(
        alcance="Contraste finito de la prueba escrita de no convergencia bajo H_K; "
                "no se trata de una ley temporal de una orbita fija ni resuelve Collatz.",
        parametros=dict(horizonte=args.horizonte, directo=args.directo),
        directo=directos, identidades_de_residuos=identidades,
        fronteras_altas_con_sesgo=fronteras_altas, traslados_con_piso=pares_con_piso,
        piso_TV="1/36864", traslados=traslados,
        cotejos_con_evidencia_anterior=coincidencias,
        muestras={k: dict(ley=["0", str(Fraction(filas[k]["R"], filas[k]["N"])),
                                    str(1 - Fraction(filas[k]["R"], filas[k]["N"]))],
                           TV=str(distancias[k]))
                  for k in (1, 2, 3, 10, args.horizonte)},
        fuentes_sha256={Path(__file__).name: sha256(Path(__file__).read_bytes()).hexdigest(),
                        "cotejo_umbral.json": sha256(anteriores.read_bytes()).hexdigest()})
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(estado="correcto", directo=directos,
                          fronteras_altas=fronteras_altas,
                          traslados_con_piso=pares_con_piso, cotejos_previos=coincidencias)))


if __name__ == "__main__":
    main()
