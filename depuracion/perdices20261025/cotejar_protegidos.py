"""Contrastes exactos de la fraccion protegida; no enumera un nuevo censo AB.

Ley: palabras binarias uniformes de longitud K, condicionadas a
3**S_j >= 2**j en todos sus prefijos. Se compara con T sobre [0, 2**K).
Las cotas universales se demuestran en PROTEGIDOS.md; este programa las
contrasta en un dominio finito mediante implementaciones independientes.
"""

import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from math import comb
from pathlib import Path


CARPETA = Path(__file__).resolve().parent
RAIZ = CARPETA.parents[1]


def sobrevive(palabra):
    producto = Fraction(1)
    for bit in palabra:
        producto *= Fraction(3 if bit else 1, 2)
        if producto < 1:
            return False
    return True


def minimo_subidas(k):
    s, potencia = 0, 1
    while potencia < 2 ** k:
        s += 1
        potencia *= 3
    return s


def historial_cuentas(horizonte):
    filas = [Counter({0: 1})]
    for k in range(1, horizonte + 1):
        nueva = Counter()
        for s, cuenta in filas[-1].items():
            if 3 ** s >= 2 ** k:
                nueva[s] += cuenta
            if 3 ** (s + 1) >= 2 ** k:
                nueva[s + 1] += cuenta
        filas.append(nueva)
    return filas


def fraccion_protegida(filas, k, longitud):
    padres = sum(cuenta for s, cuenta in filas[k - longitud].items()
                 if 3 ** s >= 2 ** k)
    return Fraction(padres * 2 ** longitud, sum(filas[k].values()))


def contraste_directo(filas, directo):
    palabras, enteros, rotaciones, reservas = 0, 0, 0, 0
    for k in range(directo + 1):
        cuenta_palabras = Counter()
        for palabra in product((0, 1), repeat=k):
            palabras += 1
            if sobrevive(palabra):
                cuenta_palabras[sum(palabra)] += 1
            if k and 3 ** sum(palabra) >= 2 ** k:
                # Minimo de productos racionales: version independiente
                # del argumento escrito con sumas de logaritmos.
                productos = [Fraction(1)]
                for bit in palabra:
                    productos.append(productos[-1] * Fraction(3 if bit else 1, 2))
                corte = min(range(k), key=productos.__getitem__)
                girada = palabra[corte:] + palabra[:corte]
                assert sobrevive(girada), (palabra, corte)
                rotaciones += 1
        assert cuenta_palabras == filas[k]
        cuenta_enteros = Counter()
        protegidos = [0] * (k + 1)
        for n in range(2 ** k):
            x, pronostico, vivo, s = n, Fraction(1), True, 0
            productos = [pronostico]
            for _ in range(k):
                impar = x % 2
                s += impar
                pronostico *= Fraction(3 if impar else 1, 2)
                productos.append(pronostico)
                vivo = vivo and pronostico >= 1
                x = (3 * x + 1) // 2 if impar else x // 2
            enteros += 1
            if vivo:
                cuenta_enteros[s] += 1
                for longitud in range(k + 1):
                    protegidos[longitud] += productos[k - longitud] >= 2 ** longitud
        assert cuenta_enteros == filas[k]
        for longitud in range(k + 1):
            assert Fraction(protegidos[longitud], sum(filas[k].values())) == \
                fraccion_protegida(filas, k, longitud)
            reservas += 1
    return dict(palabras=palabras, enteros=enteros,
                rotaciones_con_producto_final_no_menor_que_uno=rotaciones,
                cuentas_protegidas=reservas)


def control_condicionamiento():
    salidas = Counter()
    semillas = []
    for n in range(8):
        x, pronostico, vivo = n, Fraction(1), True
        for _ in range(3):
            impar = x % 2
            pronostico *= Fraction(3 if impar else 1, 2)
            vivo = vivo and pronostico >= 1
            x = (3 * x + 1) // 2 if impar else x // 2
        if vivo:
            semillas.append(n)
            salidas[x % 3] += 1
    ley = [Fraction(salidas[r], len(semillas)) for r in range(3)]
    estacionaria = [Fraction(0), Fraction(1, 3), Fraction(2, 3)]
    distancia = sum(abs(a - b) for a, b in zip(ley, estacionaria)) / 2
    assert semillas == [3, 7] and distancia == Fraction(1, 6) > Fraction(1, 8)
    return dict(semillas=semillas, ley=list(map(str, ley)),
                tv=str(distancia), cota_no_condicionada_invalida="1/8")


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--horizonte", type=int, required=True)
    analizador.add_argument("--directo", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    if not (1 <= args.horizonte <= 400 and 0 <= args.directo <= min(12, args.horizonte)):
        analizador.error("Se exige 1<=horizonte<=400 y 0<=directo<=min(12,horizonte)")
    assert 3 ** 5 < 2 ** 8 and 3 ** 17 < 2 ** 27
    assert 8 ** 27 * 16 ** 27 < 31 ** 27 * 5 ** 17 * 3 ** 10
    filas = historial_cuentas(args.horizonte)
    directo = contraste_directo(filas, args.directo)
    muestras, horizontes_barrera = {}, []
    cotas, comparaciones_modo, ventanas_largas = 0, 0, 0
    for k in range(1, args.horizonte + 1):
        n, anterior = sum(filas[k].values()), sum(filas[k - 1].values())
        s = minimo_subidas(k)
        assert k * n >= comb(k, s)
        assert 8 * s >= 5 * k and 27 * s >= 17 * k
        assert n ** 27 * (5 ** 17 * 3 ** 10) ** k <= 8 ** (27 * k)
        frontera = sum(cuenta for j, cuenta in filas[k - 1].items()
                       if 3 ** j < 2 ** k)
        assert n == 2 * anterior - frontera
        g1 = fraccion_protegida(filas, k, 1)
        assert 1 - g1 == Fraction(frontera, n) == Fraction(2 * anterior, n) - 1
        barrera = 16 * n <= 31 * anterior
        if barrera:
            horizontes_barrera.append(k)
            assert 1 - g1 >= Fraction(1, 31)
        if s < k:
            maximo = comb(k, s) * s ** s * (k - s) ** (k - s)
            for j in range(k + 1):
                assert comb(k, j) * s ** j * (k - s) ** (k - j) <= maximo
                comparaciones_modo += 1
            assert k ** k <= (k + 1) * maximo
        anterior_g = Fraction(1)
        for longitud in range(1, k + 1):
            g = fraccion_protegida(filas, k, longitud)
            assert 0 <= g <= anterior_g <= 1
            anterior_g = g
            assert g * k ** longitud <= k * (k + 1) * (2 * (k - s)) ** longitud
            assert g <= k * (k + 1) * Fraction(3, 4) ** longitud
            if longitud >= 8 * k.bit_length():
                assert g <= Fraction(1, k + 1)
                ventanas_largas += 1
            for m in (1, 2, 3):
                q = Fraction(sum(comb(longitud, j) for j in range(min(m, longitud + 1))),
                             2 ** longitud)
                cota_mezcla = 1 - g * (1 - q)
                assert cota_mezcla >= 1 - g1
                if barrera:
                    assert cota_mezcla >= Fraction(1, 31)
            cotas += 1
        if k in {1, 2, 3, 10, 20, 50, 100, args.horizonte}:
            longitud = min(k, 8 * k.bit_length())
            muestras[k] = dict(N=str(n), s=s, G_un_paso=str(g1),
                               piso_certificado=str(1 - g1),
                               cumple_barrera_1_31=barrera,
                               longitud_muestra=longitud,
                               G_muestra=str(fraccion_protegida(filas, k, longitud)))
    anteriores = RAIZ / "depuracion/perdices20261007/cotejo_umbral.json"
    datos_anteriores = json.loads(anteriores.read_text(encoding="utf-8"))
    coincidencias = 0
    for clave, dato in datos_anteriores["muestras"].items():
        k = int(clave)
        if k <= args.horizonte:
            assert sum(filas[k].values()) == dato["frontera"]["supervivientes"]
            coincidencias += 1
    resultado = dict(
        alcance="Contrastes finitos exactos de cotas demostradas por escrito; "
                "la barrera es para el certificado de mezcla, no para la TV real "
                "ni para una orbita fija. No demuestra Collatz ni el reloj AB.",
        parametros=dict(horizonte=args.horizonte, directo=args.directo),
        contraste_directo=directo, cotas_G=cotas, comparaciones_modo=comparaciones_modo,
        ventanas_con_G_menor_igual_inverso_K_mas_uno=ventanas_largas,
        cotejos_con_evidencia_anterior=coincidencias,
        horizontes_barrera_1_31=horizontes_barrera,
        control_condicionamiento=control_condicionamiento(), muestras=muestras,
        fuentes_sha256={Path(__file__).name: sha256(Path(__file__).read_bytes()).hexdigest(),
                        "cotejo_umbral.json": sha256(anteriores.read_bytes()).hexdigest()})
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(estado="correcto", cotas_G=cotas, directo=directo,
                          cotejos_anteriores=coincidencias,
                          horizontes_barrera=len(horizontes_barrera)), ensure_ascii=False))


if __name__ == "__main__":
    main()
