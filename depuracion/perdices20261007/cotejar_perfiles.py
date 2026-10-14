"""Contrasta cilindros construidos y perfiles; no amplía el censo de semillas."""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path


CARPETA = Path(__file__).resolve().parent
RAIZ = CARPETA.parents[1]


def valuacion(numero):
    assert numero != 0
    numero = abs(numero)
    return (numero & -numero).bit_length() - 1


def divisiones(numero):
    assert numero > 0
    exponente = 0
    while numero % 2 == 0:
        numero //= 2
        exponente += 1
    return exponente


def recorrer(numero, paridades):
    """Atajo literal: no usa los coeficientes del bloque compuesto."""
    for bit in paridades:
        assert numero % 2 == bit, (numero, bit)
        numero = (3 * numero + 1) // 2 if bit else numero // 2
    return numero


def coeficientes(a):
    assert a >= 1
    N = 2 ** (a + 3)
    D = 3 ** (a + 2)
    E = D - N // 2
    C = D - N
    assert 0 < N < D and C % 2 == 1 and E % 2 == 1
    return N, D, E, C


def construir(formas, repeticiones, trasladado):
    assert repeticiones >= 1 and trasladado >= 0
    assert all(u >= 0 and v >= 0 and u + v > 0 for u, v in formas)
    candidatos = []
    for a in range(1, len(formas) + 2):
        N, D, E, C = coeficientes(a)
        candidatos.append(Fraction(-E, C))
        defectos = [C * v - u * E for u, v in formas]
        if all(defectos):
            break
    else:
        raise AssertionError("La familia finita no puede cubrir todos los puntos fijos")
    assert len(candidatos) == len(set(candidatos))
    ordenes = [valuacion(d) for d in defectos]
    k = max(ordenes, default=0)
    precision = (a + 3) * repeticiones + k + 1
    modulo = 2 ** precision
    residuo = -E * pow(C, -1, modulo) % modulo
    semilla = residuo + trasladado * modulo
    assert semilla > 0 and (C * semilla + E) % modulo == 0
    valor = semilla
    fronteras = [valor]
    for j in range(repeticiones + 1):
        perfil = [divisiones(u * valor + v) for u, v in formas]
        assert perfil == ordenes
        assert N ** j * (C * valor + E) == D ** j * (C * semilla + E)
        assert (C * valor + E) % 2 ** (precision - (a + 3) * j) == 0
        if j == repeticiones:
            break
        siguiente = recorrer(valor, [1] * (a + 2) + [0])
        assert N * siguiente == D * valor + E
        assert siguiente > valor
        valor = siguiente
        fronteras.append(valor)
    return dict(formas=formas, r=repeticiones, trasladado=trasladado, a=a,
                N=N, D=D, E=E, C=C, precision=precision, perfil=ordenes,
                semilla=semilla, fronteras=fronteras)


def contrastar_presupuesto_guardado():
    # Esta implementación sólo necesita las paridades y las valuaciones de frontera.
    origen = CARPETA / "medicion_salida_ab.json"
    datos = json.loads(origen.read_text(encoding="utf-8"))
    semillas = sorted({int(f["minimo"]) for f in datos["filas"]})
    prefijos = 0
    minimo = None
    for n in semillas:
        pendientes = [(n, 0, None)]
        while pendientes:
            x, largo, inicial = pendientes.pop()
            for bits, constante in (([1], 1), ([1, 1, 0], 5)):
                y = x
                for bit in bits:
                    if y % 2 != bit:
                        break
                    y = (3 * y + 1) // 2 if bit else y // 2
                else:
                    nuevo_largo = largo + len(bits)
                    vin = divisiones(n + constante) if inicial is None else inicial
                    vfin = divisiones(y + constante)
                    ell = (n + 4).bit_length()
                    margen = 2 * vin + 4 * ell - nuevo_largo - 2 * vfin
                    assert margen >= 0
                    prefijos += 1
                    if minimo is None or margen < minimo[0]:
                        minimo = (margen, n, nuevo_largo, vin, vfin, ell)
                    pendientes.append((y, nuevo_largo, vin))
    return dict(semillas=len(semillas), prefijos=prefijos, fallos=0,
                margen_minimo=minimo, alcance="Sólo testigos guardados; no prueba de P.")


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--formas-max", type=int, required=True)
    analizador.add_argument("--repeticiones-max", type=int, required=True)
    analizador.add_argument("--traslados", type=int, required=True)
    analizador.add_argument("--familia-k-max", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    assert 1 <= args.formas_max <= 12
    assert 1 <= args.repeticiones_max <= 12
    assert 1 <= args.traslados <= 8 and 0 <= args.familia_k_max <= 256
    familias = [[], [(1, 1), (1, 5)], [(2, 2), (4, 20), (0, 8)]]
    for m in range(1, args.formas_max + 1):
        # Cada forma anula un punto fijo diferente: fuerza a elegir a=m+1.
        formas = [(coeficientes(a)[3], coeficientes(a)[2]) for a in range(1, m + 1)]
        familias.append(formas)
    casos = []
    for formas in familias:
        for r in range(1, args.repeticiones_max + 1):
            for trasladado in range(args.traslados):
                casos.append(construir(formas, r, trasladado))
    concretos = []
    for k in list(range(args.familia_k_max + 1)) + [2 ** 20, 2 ** 80]:
        n = 256 * k + 231
        y = recorrer(n, [1, 1, 1, 0])
        assert y == 432 * k + 391 > n
        assert (divisiones(n + 1), divisiones(n + 5)) == (3, 2)
        assert (divisiones(y + 1), divisiones(y + 5)) == (3, 2)
        concretos.append(dict(k=k, semilla=n, salida=y))
    # Borde: una unidad menos de precisión no garantiza conservar el perfil.
    assert recorrer(103, [1, 1, 1, 0]) == 175
    assert [divisiones(103 + c) for c in (1, 5)] == [3, 2]
    assert [divisiones(175 + c) for c in (1, 5)] == [4, 2]
    # La forma del propio punto fijo debe ser descartada, no evaluada en cero.
    assert construir([(11, 19)], 1, 0)["a"] == 2
    guardado = contrastar_presupuesto_guardado()
    fuentes = [Path(__file__), CARPETA / "PerdicesPerfiles.lean",
               CARPETA / "medicion_salida_ab.json"]
    huellas = {p.relative_to(RAIZ).as_posix(): hashlib.sha256(
        p.read_bytes().replace(b"\r\n", b"\n")).hexdigest() for p in fuentes}
    resultado = dict(parametros={k: v for k, v in vars(args).items() if k != "salida"},
                     alcance="Construcciones finitas contrastadas; prueba universal en PERFILES.md.",
                     casos=len(casos), fronteras=sum(len(c["fronteras"]) for c in casos),
                     familia_concreta=concretos, cilindros=casos,
                     borde_precision=dict(semilla=103, salida=175,
                                          perfil_inicial=[3, 2], perfil_final=[4, 2]),
                     plantilla_doble_guardada=guardado, sha256_lf=huellas)
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps({k: resultado[k] for k in ("casos", "fronteras", "plantilla_doble_guardada")},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
