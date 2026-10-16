"""Contrasta el criterio de producto BAB con enteros y T literal."""

import argparse
import hashlib
import json
from pathlib import Path

from cotejar_dos_cambios import desde_parametros


CARPETA = Path(__file__).resolve().parent


def radical(numero):
    resultado, divisor = 1, 2
    while divisor*divisor <= numero:
        if numero % divisor == 0:
            resultado *= divisor
            while numero % divisor == 0:
                numero //= divisor
        divisor += 1
    return resultado*numero


def comprobar(caso, factorizar):
    a, b, r, s, k, ell = (caso[x] for x in ("a", "b", "r", "s", "k", "ell"))
    altura = 3**b*r+1
    assert altura == 2**k*s and r % 3 != 0 and s % 3 != 0
    assert 2**(3*a+2)*(2**b*r+1) <= 9**a*2**ell
    assert 17*b+34 <= 17*ell+3*a
    assert 17*(3*caso["c"]+caso["vfin"]) <= 17*ell+3*a+10*b
    assert 7*(3*a+b+3*caso["c"])+17*caso["vfin"] <= 17*caso["vin"]+34*ell
    fallo = b+2*k > 3*a+3+4*ell
    producto_pequeno = 1024*8**b*(r*s)**2 < 9**b
    altura_extrema = (6*r*s)**18 < 3**b
    assert not fallo or producto_pequeno
    assert not producto_pequeno or altura_extrema
    assert altura_extrema or not fallo
    if factorizar:
        # r,s son coprimos y ninguno tiene factores 2 o 3.
        rad = radical(3**b*r)*radical(altura)
        assert rad <= 6*r*s
        assert not fallo or rad**18 < altura
    return dict(a=a, b=b, r=r, k=k, s=s, n=caso["n"], ell=ell,
                margen=caso["margen"], region_anterior=caso["region_suficiente"],
                criterio_c18=not altura_extrema,
                criterio_producto=not producto_pequeno,
                fallo=fallo, radical_cotejado=factorizar)


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--a-max", type=int, required=True)
    analizador.add_argument("--b-max", type=int, required=True)
    analizador.add_argument("--r-max", type=int, required=True)
    analizador.add_argument("--factorizar-hasta-b", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    assert 1 <= args.a_max <= 8 and 1 <= args.b_max <= 1024
    assert 1 <= args.r_max <= 255 and 0 <= args.factorizar_hasta_b <= 12
    casos = []
    for a in range(1, args.a_max+1):
        for b in range(1, args.b_max+1):
            for r in range(1, args.r_max+1, 2):
                if (2**b*r+1) % 9**a == 0:
                    caso = desde_parametros(a, b, r)
                    casos.append(comprobar(caso, b <= args.factorizar_hasta_b))
    fuera = [caso for caso in casos if not caso["region_anterior"]]
    fallos = [caso for caso in casos if caso["fallo"]]
    resumen = dict(casos=len(casos), fuera_region_anterior=len(fuera),
                   cubiertos_c18=sum(c["criterio_c18"] for c in casos),
                   cubiertos_producto=sum(c["criterio_producto"] for c in casos),
                   radicales_cotejados=sum(c["radical_cotejado"] for c in casos),
                   fallos_p2=len(fallos))
    testigos = [min(casos, key=lambda c: c["margen"])]
    if fuera:
        testigos.append(min(fuera, key=lambda c: c["n"]))
    fuentes = [Path(__file__), CARPETA/"cotejar_dos_cambios.py", CARPETA/"PerdicesAlturaBAB.lean"]
    resultado = dict(parametros={k:v for k,v in vars(args).items() if k != "salida"},
                     alcance="Contraste finito del criterio suficiente y radicales pequeños. "
                             "No demuestra C18 para todo BAB ni prueba abc.",
                     resumen=resumen, testigos=testigos, fallos=fallos,
                     sha256_lf={p.name:hashlib.sha256(p.read_bytes().replace(b"\r\n",b"\n")).hexdigest()
                                for p in fuentes})
    args.salida.write_text(json.dumps(resultado,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(resumen,ensure_ascii=False))


if __name__ == "__main__":
    main()
