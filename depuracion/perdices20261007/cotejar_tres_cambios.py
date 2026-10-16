"""Cotejo orbital de cuatro rachas y testigo separado de una relajación."""

import argparse
import hashlib
import itertools
import json
from pathlib import Path

from cotejar_dos_cambios import cilindro


CARPETA = Path(__file__).resolve().parent
BITS = {"A": (1,), "B": (1, 1, 0)}
CONSTANTE = {"A": 1, "B": 5}


def orden(n):
    assert n > 0
    return (n & -n).bit_length()-1


def rachas(palabra):
    return [(bloque, len(list(grupo))) for bloque, grupo in itertools.groupby(palabra)]


def contrastar(n, palabra):
    grupos = rachas(palabra)
    assert n > 0 and len(grupos) == 4
    a, b, c, d = [cantidad for _, cantidad in grupos]
    x, largo, recargas = n, 0, 0
    anterior = CONSTANTE[palabra[0]]
    vin = orden(n+anterior)
    for bloque in palabra:
        recargas += orden(x+CONSTANTE[bloque])-orden(x+anterior)
        for bit in BITS[bloque]:
            assert x % 2 == bit
            x = (3*x+1)//2 if bit else x//2
            largo += 1
        anterior = CONSTANTE[bloque]
    vf, ell = orden(x+anterior), (n+4).bit_length()
    assert largo+vf == vin+recargas
    if palabra[0] == "A":
        assert vin == a+2 and a+2 <= ell
        assert 51*b+34 <= 17*ell+10*a
        assert 17*c+34 <= 17*ell+10*a+3*b
        assert 17*(3*d+vf) <= 17*ell+10*a+3*b+10*c
    else:
        assert vin == 3*a+2
        assert 17*b+34 <= 17*ell+3*a
        assert 51*c <= 17*ell+3*a+10*b
        assert 17*(d+vf) <= 17*ell+3*a+10*b+3*c
    margen = 13*vin+26*ell-largo-13*vf
    assert margen >= 0
    return dict(n=n, palabra=palabra, largo=largo, vin=vin, vfin=vf, ell=ell,
                margen_trece=margen, margen_siete=17*vin+34*ell-7*largo-17*vf)


def certificados_lineales():
    # Orden: a,b,c,d,ell,vf,1. Se cotejan identidades de polinomios lineales.
    def sumar(terminos):
        return [sum(peso*vector[i] for peso, vector in terminos) for i in range(7)]
    E = [-1, 0, 0, 0, 1, 0, -2]
    B = [10, -51, 0, 0, 17, 0, -34]
    C = [10, 3, -17, 0, 17, 0, -34]
    V = [10, 3, 10, -51, 17, -17, 0]
    G = [12, -3, -1, -3, 26, -13, 26]
    residuo = [0, 0, 0, 176868, 43, 0, 255390]
    assert sumar([(3757,V),(2499,C),(657,B),(10174,E),(1,residuo)]) == [4913*x for x in G]
    B = [3, -17, 0, 0, 17, 0, -34]
    C = [3, 10, -51, 0, 17, 0, 0]
    V = [3, 10, 3, -17, 17, -17, 0]
    G = [36, -1, -3, -1, 26, -13, 26]
    residuo = [155670, 0, 0, 58956, 7616, 0, 222904]
    assert sumar([(3757,V),(510,C),(2799,B),(1,residuo)]) == [4913*x for x in G]


def modelo_cuatro():
    a,b,c,d,e,ell,vin,vf = 1,998,527,1670,1,1000,5,2600
    assert vin == 3*a+2 <= ell
    assert 17*b+34 <= 17*ell+3*a
    assert 51*c+34 <= 17*ell+3*a+10*b
    assert 17*d+34 <= 17*ell+3*a+10*b+3*c
    assert 17*(3*e+vf) <= 17*ell+3*a+10*b+3*c+10*d
    consumos = [3*a,b,3*c,d,3*e]
    entradas = [vin,b+2,3*c+2,d+2,3*e+vf]
    salidas = [entrada-consumo for entrada,consumo in zip(entradas,consumos)]
    assert salidas == [2,2,2,2,vf]
    recargas = [entradas[i+1]-salidas[i] for i in range(4)]
    largo = sum(consumos)
    assert largo+vf == vin+sum(recargas)
    assert vf > vin+2*ell
    assert pow(2,b,9) == 4
    # En una realización, 32q<=2^1000 y 9q=2^998*r+1 forzarían r=1;
    # pero 2^998+1 no es divisible por 9. No es un contraejemplo orbital.
    assert (pow(2,b,9)+1) % 9 != 0
    # También respeta los encajes superiores exactos tras cada racha.
    tiempo, impares = 0, 0
    for i, (consumo, unos) in enumerate(zip(consumos,[2*a,b,2*c,d,2*e])):
        tiempo += consumo
        impares += unos
        orden_extremo = entradas[i+1] if i < 4 else vf
        assert 2**(tiempo+orden_extremo) <= 3**impares*2**ell
    return dict(tipo="Modelo de cotas sin semilla ni órbita construida",
                ell=ell, rachas=[a,b,c,d,e], orientacion="BABAB", vin=vin,
                vfin=vf, largo=largo, recargas=recargas,
                exceso_epsilon_cero=vf-vin-2*ell,
                encajes_superiores_exactos=True, imposible_por_congruencia_mod9=True)


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--racha-max", type=int, required=True)
    analizador.add_argument("--traslados", type=int, required=True)
    analizador.add_argument("--historicos", type=Path, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    assert 1 <= args.racha_max <= 10 and 1 <= args.traslados <= 4
    certificados_lineales()
    modelo = modelo_cuatro()
    casos = []
    largos = set(itertools.product(range(1,args.racha_max+1),repeat=4))
    largos.update(((1,128,64,1),(64,1,128,2),(80,2,40,1)))
    for tipo in ("ABAB","BABA"):
        for cantidades in sorted(largos):
            palabra = "".join(bloque*cantidad for bloque,cantidad in zip(tipo,cantidades))
            for traslado in range(args.traslados):
                casos.append(contrastar(cilindro(palabra,traslado),palabra))
    construidos = len(casos)
    datos = json.loads(args.historicos.read_text(encoding="utf-8"))
    semillas = sorted({int(fila["minimo"]) for fila in datos["filas"]})
    for n in semillas:
        pendientes = [(n, "")]
        while pendientes:
            x, palabra = pendientes.pop()
            for bloque, bits in BITS.items():
                nueva = palabra+bloque
                grupos = rachas(nueva)
                if len(grupos) > 4:
                    continue
                y = x
                for bit in bits:
                    if y % 2 != bit:
                        break
                    y = (3*y+1)//2 if bit else y//2
                else:
                    if len(grupos) == 4:
                        casos.append(contrastar(n,nueva))
                    pendientes.append((y,nueva))
    resumen = dict(construidos=construidos, semillas_historicas=len(semillas),
                   prefijos_historicos=len(casos)-construidos, total=len(casos),
                   fallos_siete_observados=sum(c["margen_siete"]<0 for c in casos),
                   certificados_lineales=2, modelos_sin_semilla=1)
    fuentes = [Path(__file__),CARPETA/"cotejar_dos_cambios.py",
               CARPETA/"PerdicesTresCambios.lean",args.historicos]
    resultado = dict(parametros={k:str(v) if isinstance(v,Path) else v for k,v in vars(args).items() if k != "salida"},
                     alcance="Cotejo finito orbital y dos identidades exactas. El modelo de cotas no es una órbita.",
                     resumen=resumen,modelo=modelo,
                     testigos=[min(casos,key=lambda c:c["margen_trece"]),min(casos,key=lambda c:c["margen_siete"])],
                     sha256_lf={p.name:hashlib.sha256(p.read_bytes().replace(b"\r\n",b"\n")).hexdigest() for p in fuentes})
    args.salida.write_text(json.dumps(resultado,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(resumen,ensure_ascii=False))


if __name__ == "__main__":
    main()
