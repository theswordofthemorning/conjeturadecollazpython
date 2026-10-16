"""Cotejo exacto de tres rachas; sin censo de semillas ni prueba por muestreo."""

import argparse
import hashlib
import itertools
import json
from pathlib import Path


CARPETA = Path(__file__).resolve().parent
BITS = {"A": (1,), "B": (1, 1, 0)}
CONSTANTES = {"A": 1, "B": 5}


def orden(numero):
    assert numero > 0
    resultado = 0
    while numero % 2 == 0:
        resultado += 1
        numero //= 2
    return resultado


def cilindro(palabra, traslado):
    multiplicador, aporte, denominador = 1, 0, 1
    for bloque in palabra:
        for bit in BITS[bloque]:
            multiplicador *= 3 ** bit
            aporte = 3 ** bit * aporte + bit * denominador
            denominador *= 2
    residuo = -aporte * pow(multiplicador, -1, denominador) % denominador
    assert residuo > 0
    return residuo + traslado * denominador


def contrastar(n, orientacion, a, b, c):
    assert n >= 1 and min(a, b, c) >= 1
    palabra = orientacion[0]*a + orientacion[1]*b + orientacion[2]*c
    x, largo, recargas = n, 0, 0
    anterior = CONSTANTES[palabra[0]]
    fronteras = [n]
    for indice, bloque in enumerate(palabra, 1):
        constante = CONSTANTES[bloque]
        recargas += orden(x + constante) - orden(x + anterior)
        for bit in BITS[bloque]:
            assert x % 2 == bit, (n, orientacion, a, b, c, indice, x)
            x = (3*x+1)//2 if bit else x//2
            largo += 1
        anterior = constante
        if indice in (a, a+b, a+b+c):
            fronteras.append(x)
    _, y, z, w = fronteras
    vin = orden(n + CONSTANTES[palabra[0]])
    vfin = orden(w + CONSTANTES[palabra[-1]])
    assert vfin == ((w+anterior) & -(w+anterior)).bit_length()-1
    ell = (n+4).bit_length()
    assert 2**(ell-1) < n+5 <= 2**ell
    assert largo == vin + recargas - vfin
    margen = 2*vin+4*ell-largo-2*vfin
    resultado = dict(n=n, orientacion=orientacion, a=a, b=b, c=c,
                     ell=ell, vin=vin, vfin=vfin, margen= margen,
                     fronteras=fronteras)
    if orientacion == "ABA":
        assert 2**a*(y+1) == 3**a*(n+1)
        assert 2**(3*b)*(z+5) == 9**b*(y+5)
        assert 2**c*(w+1) == 3**c*(z+1)
        assert vin == a+2 and a+2 <= ell
        assert 51*b <= 17*ell+10*a
        assert 17*(c+vfin) <= 17*ell+10*a+3*b
        assert margen >= 0
    else:
        assert orientacion == "BAB" and vin == 3*a+2
        q = (n+5) // 2**vin
        r = (y+1) // 2**(b+2)
        k = orden(3**b*r+1)
        s = (3**b*r+1) // 2**k
        assert q % 2 == r % 2 == s % 2 == 1
        assert 9**a*q == 2**b*r+1
        assert 2**k*s == 3**b*r+1
        assert 3**(b+2*a)*q - 2**(b+k)*s == 3**b-2**b
        assert vfin+3*c == k+2
        assert margen == 3*a+3*c+4*ell-b-2*k
        assert 17*(3*c+vfin) <= 17*ell+3*a+10*b
        region = 37*b <= 34*ell+45*a+51*c+68
        if region:
            assert margen >= 0
        resultado.update(q=q, r=r, k=k, s=s, region_suficiente=region)
    return resultado


def desde_parametros(a, b, r, c=1):
    assert r > 0 and r % 2 == 1
    numerador = 2**b*r+1
    assert numerador % 9**a == 0
    q = numerador // 9**a
    k = orden(3**b*r+1)
    assert 1 <= 3*c <= k+2
    n = 2**(3*a+2)*q-5
    return contrastar(n, "BAB", a, b, c)


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--racha-max", type=int, required=True)
    analizador.add_argument("--traslados", type=int, required=True)
    analizador.add_argument("--b-max", type=int, required=True)
    analizador.add_argument("--r-max", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    assert 1 <= args.racha_max <= 20 and 1 <= args.traslados <= 4
    assert 1 <= args.b_max <= 1024 and 1 <= args.r_max <= 255
    assert 3**17 < 2**27
    casos = []
    for orientacion in ("ABA", "BAB"):
        for a, b, c in itertools.product(range(1, args.racha_max+1), repeat=3):
            palabra = orientacion[0]*a+orientacion[1]*b+orientacion[2]*c
            for traslado in range(args.traslados):
                casos.append(contrastar(cilindro(palabra, traslado), orientacion, a, b, c))
    cilindros = len(casos)
    for a in range(1, 5):
        for b in range(1, args.b_max+1):
            for r in range(1, args.r_max+1, 2):
                if (2**b*r+1) % 9**a == 0:
                    casos.append(desde_parametros(a, b, r))
    partes_pequenas = len(casos)-cilindros
    # CRT impone las dos congruencias simultáneamente y la valuación exacta k.
    for a, b, k in itertools.product((1, 2, 4, 8),
                                     (1, 2, 3, 6, 12, 32, 64, 128, 256, 512),
                                     (1, 2, 3, 8, 32, 128)):
        modulo_tres, modulo_dos = 9**a, 2**(k+1)
        r_tres = -pow(2**b, -1, modulo_tres) % modulo_tres
        r_dos = (2**k-1)*pow(3**b, -1, modulo_dos) % modulo_dos
        r = r_dos + modulo_dos*((r_tres-r_dos)*pow(modulo_dos, -1, modulo_tres) % modulo_tres)
        for c in sorted({1, (k+2)//3}):
            caso = desde_parametros(a, b, r, c)
            assert caso["k"] == k
            casos.append(caso)
    bab = [caso for caso in casos if caso["orientacion"] == "BAB"]
    fuera = [caso for caso in bab if not caso["region_suficiente"]]
    fallos = [caso for caso in casos if caso["margen"] < 0]
    resumen = dict(cilindros=cilindros, partes_impares_pequenas=partes_pequenas,
                   crt=len(casos)-cilindros-partes_pequenas, total=len(casos),
                   fuera_region_suficiente=len(fuera), contraejemplos_p2=len(fallos))
    testigos = [min((caso for caso in casos if caso["orientacion"] == tipo),
                   key=lambda caso: caso["margen"]) for tipo in ("ABA", "BAB")]
    if fuera:
        testigos.append(min(fuera, key=lambda caso: caso["n"]))
    fuentes = [Path(__file__), CARPETA / "PerdicesDosCambios.lean"]
    salida = dict(parametros={k:v for k,v in vars(args).items() if k != "salida"},
                  alcance="Cotejo finito independiente con T literal; no prueba universal BAB.",
                  resumen=resumen, testigos=testigos, contraejemplos=fallos,
                  sha256_lf={ruta.name: hashlib.sha256(ruta.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
                             for ruta in fuentes})
    args.salida.write_text(json.dumps(salida, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(resumen, ensure_ascii=False))
    if fallos:
        print("Se encontraron contraejemplos: revisar el JSON antes de continuar.")


if __name__ == "__main__":
    main()
