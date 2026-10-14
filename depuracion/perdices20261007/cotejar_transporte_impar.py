"""Contrasta transporte y presupuestos en palabras construidas; no es un censo."""

import argparse
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path


CARPETA = Path(__file__).resolve().parent
RAIZ = CARPETA.parents[1]
BITS = {"A": (1,), "B": (1, 1, 0)}
CONSTANTE = {"A": 1, "B": 5}


def valuacion(numero):
    assert numero > 0
    return (numero & -numero).bit_length() - 1


def descomponer(numero):
    assert numero > 0
    exponente = 0
    while numero % 2 == 0:
        exponente += 1
        numero //= 2
    return exponente, numero


def dos_firmado(exponente):
    return Fraction(2 ** exponente) if exponente >= 0 else Fraction(1, 2 ** -exponente)


def construir(palabra, traslado):
    """Residuo de la composición afín; se coteja luego con cada paridad literal."""
    multiplicador, aporte, modulo = 1, 0, 1
    for bloque in palabra:
        for bit in BITS[bloque]:
            if bit:
                multiplicador *= 3
                aporte = 3 * aporte + modulo
            modulo *= 2
    residuo = -aporte * pow(multiplicador, -1, modulo) % modulo
    assert residuo > 0
    return residuo + traslado * modulo


def contrastar(n, palabra):
    assert n > 0 and palabra
    x, largo, impares, recargas, cambios = n, 0, 0, 0, 0
    correccion = Fraction(1)
    inicial = CONSTANTE[palabra[0]]
    vin, qin = descomponer(n + inicial)
    anterior = None
    negativos = 0
    for bloque in palabra:
        c = CONSTANTE[bloque]
        if anterior is not None:
            eta = valuacion(x + c) - valuacion(x + anterior)
            recargas += eta
            negativos += eta < 0
            correccion *= Fraction(x + c, x + anterior)
            cambios += c != anterior
        entrada = x
        for bit in BITS[bloque]:
            assert x % 2 == bit, (n, palabra, x, bit)
            x = (3*x+1)//2 if bit else x//2
            largo += 1
            impares += bit
        assert x > entrada
        anterior = c
    vfin, qfin = descomponer(x + anterior)
    assert vfin == valuacion(x + anterior)
    assert largo == vin + recargas - vfin
    assert dos_firmado(recargas) * qfin == 3 ** impares * qin * correccion
    assert Fraction(n+1, n+inicial) <= correccion <= Fraction(n+5, n+inicial)
    transportado = 2 ** (largo + vfin) * qfin
    assert 3 ** impares * (n+1) <= transportado <= 3 ** impares * (n+5)
    # Contraste independiente: encaje directo, sin valuaciones ni corrección.
    assert 3 ** impares * (n+1) <= 2 ** largo * (x+1)
    assert 2 ** largo * (x+5) <= 3 ** impares * (n+5)
    ell = (n+4).bit_length()
    if cambios <= 1:
        assert recargas <= 2 * ell
        assert largo + vfin <= vin + 2 * ell
    presupuesto = largo + 2*vfin <= 2*vin + 4*ell
    necesario = 3 ** (2*impares) * (n+1)**2 <= 2 ** (2*vin+largo+4*ell) * qfin**2
    suficiente = 3 ** (2*impares) * (n+5)**2 <= 2 ** (2*vin+largo+4*ell) * qfin**2
    assert not presupuesto or necesario
    assert not suficiente or presupuesto
    return dict(n=n, palabra=palabra, largo=largo, impares=impares,
                cambios=cambios, recargas=recargas, negativas=negativos,
                vin=vin, vfin=vfin, qfin=qfin, ell=ell,
                correccion=(str(correccion) if correccion.numerator.bit_length() < 1024
                            else dict(bits_numerador=correccion.numerator.bit_length(),
                                      bits_denominador=correccion.denominator.bit_length())),
                presupuesto=presupuesto)


def familia(a):
    """Una sola alternancia puede dejar parte impar terminal igual a nueve."""
    assert a >= 1
    k = 2 * 3 ** (a-1)
    numerador = 2 ** k - 1
    assert numerador % 3 ** a == 0
    q = numerador // 3 ** a
    assert q % 2 == 1
    n = 2 ** (a+2) * q - 1
    caso = contrastar(n, "A" * a + "B")
    assert caso["vin"] == a+2 and caso["vfin"] == k-1
    assert caso["qfin"] == 9 and caso["recargas"] == k
    return dict(a=a, k=k, bits_semilla=n.bit_length(), ell=caso["ell"],
                recargas=k, exceso_sobre_ell=k-caso["ell"],
                qfin=9, presupuesto_doble=caso["presupuesto"])


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--bloques-max", type=int, required=True)
    analizador.add_argument("--racha-max", type=int, required=True)
    analizador.add_argument("--traslados", type=int, required=True)
    analizador.add_argument("--familia-a-max", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    assert 1 <= args.bloques_max <= 9
    assert 1 <= args.racha_max <= 20 and 1 <= args.traslados <= 4
    assert 1 <= args.familia_a_max <= 10
    palabras = set()
    for longitud in range(1, args.bloques_max+1):
        palabras.update("".join(p) for p in itertools.product("AB", repeat=longitud))
    for a in range(1, args.racha_max+1):
        palabras.update(("A"*a, "B"*a))
        for b in range(1, args.racha_max+1):
            palabras.update(("A"*a+"B"*b, "B"*b+"A"*a))
    casos = [contrastar(construir(p, t), p)
             for p in sorted(palabras, key=lambda p: (len(p), p))
             for t in range(args.traslados)]
    # Bordes: ambas igualdades, las dos orientaciones y recarga negativa.
    bordes = [contrastar(1, "A"), contrastar(3, "B"),
              contrastar(59, "BA"), contrastar(4591, "AABABAAABAABAAB")]
    assert bordes[2]["recargas"] == -1
    familias = [familia(a) for a in range(1, args.familia_a_max+1)]
    # Testigos históricos conservados: sólo se recomputan sus prefijos completos.
    origen = CARPETA / "medicion_salida_ab.json"
    datos = json.loads(origen.read_text(encoding="utf-8"))
    semillas = sorted({int(f["minimo"]) for f in datos["filas"]})
    historicos = 0
    for n in semillas:
        pendientes = [(n, "")]
        while pendientes:
            x, palabra = pendientes.pop()
            for bloque, bits in BITS.items():
                y = x
                for bit in bits:
                    if y % 2 != bit:
                        break
                    y = (3*y+1)//2 if bit else y//2
                else:
                    contrastar(n, palabra+bloque)
                    historicos += 1
                    pendientes.append((y, palabra+bloque))
    fuentes = [Path(__file__), CARPETA / "PerdicesTransporteImpar.lean", origen]
    huellas = {p.relative_to(RAIZ).as_posix(): hashlib.sha256(
        p.read_bytes().replace(b"\r\n", b"\n")).hexdigest() for p in fuentes}
    resumen = dict(palabras=len(palabras), casos=len(casos),
                   casos_hasta_un_cambio=sum(c["cambios"] <= 1 for c in casos),
                   casos_con_recargas_negativas=sum(c["negativas"] > 0 for c in casos),
                   testigos_historicos=len(semillas), prefijos_historicos=historicos)
    resultado = dict(parametros={k:v for k,v in vars(args).items() if k != "salida"},
                     alcance="Cotejo finito de las pruebas de TRANSPORTE_IMPAR.md; no prueba de salida.",
                     resumen=resumen, bordes=bordes, familias=familias, casos=casos,
                     sha256_lf=huellas)
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(resumen, ensure_ascii=False))


if __name__ == "__main__":
    main()
