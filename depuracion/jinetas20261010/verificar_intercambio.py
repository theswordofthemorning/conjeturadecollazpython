"""Contraste exacto de Jinetas: palabras frente a órbitas, sin muestreo.

Uso: python -B -X utf8 verificar_intercambio.py --longitud-maxima 12 --salida RUTA
El límite de esta sesión es 12; no se amplía automáticamente.
"""

import argparse
import hashlib
import json
from pathlib import Path


def datos_palabra(palabra, factor=3):
    aditivo = 0
    impares = 0
    for indice, bit in enumerate(palabra):
        if bit == "1":
            aditivo = factor * aditivo + 2 ** indice
            impares += 1
    modulo = 2 ** len(palabra)
    pendiente = factor ** impares
    residuo = (-aditivo * pow(pendiente, -1, modulo)) % modulo
    minimo = residuo + modulo * max(0, (3 - residuo + modulo - 1) // modulo)
    defecto = modulo - pendiente
    margen = defecto * minimo - aditivo
    return dict(B=aditivo, s=impares, r=residuo, u=minimo,
                D=defecto, margen=margen, paradoja=defecto > 0 and margen <= 0)


def orbita(semilla, longitud, factor=3):
    """Camino independiente: decide cada paridad desde el entero actual."""
    valor = semilla
    bits = []
    trayectoria = [semilla]
    for _ in range(longitud):
        impar = valor % 2
        bits.append(str(impar))
        valor = (factor * valor + 1) // 2 if impar else valor // 2
        trayectoria.append(valor)
    return "".join(bits), valor, trayectoria


def verificar(longitud_maxima):
    totales = dict(palabras=0, intercambios=0, intercambios_con_D_positivo=0,
                   sin_acarreo=0, con_acarreo=0, controles_levantamientos=0,
                   controles_relleno=0, segmentos_paradojicos=0)
    testigos = {}
    por_longitud = []
    for longitud in range(1, longitud_maxima + 1):
        modulo = 2 ** longitud
        # La tabla se construye por semillas; no usa la inversa modular.
        directos = {}
        for residuo in range(modulo):
            palabra, final, _ = orbita(residuo, longitud)
            assert palabra not in directos
            directos[palabra] = (residuo, final)
        assert len(directos) == modulo
        segmentos = 0
        for numero in range(modulo):
            palabra = format(numero, f"0{longitud}b")
            datos = datos_palabra(palabra)
            residuo, final = directos[palabra]
            assert datos["r"] == residuo
            assert modulo * final == 3 ** datos["s"] * residuo + datos["B"]
            semillas = {datos["u"], datos["u"] + modulo}
            if datos["D"] > 0:
                cantidad = max(0, (datos["B"] // datos["D"] - datos["u"]) // modulo + 1)
                segmentos += cantidad
                if cantidad:
                    semillas.add(datos["u"] + (cantidad - 1) * modulo)
                semillas.add(datos["u"] + cantidad * modulo)
            for semilla in semillas:
                leida, termino, _ = orbita(semilla, longitud)
                assert leida == palabra
                assert modulo * termino == 3 ** datos["s"] * semilla + datos["B"]
                assert (datos["D"] > 0 and termino >= semilla) == (
                    datos["D"] > 0 and datos["D"] * semilla <= datos["B"])
                totales["controles_levantamientos"] += 1
            for relleno in range(4):
                ampliada = datos_palabra("0" * relleno + palabra)
                escala = 2 ** relleno
                assert ampliada["B"] == escala * datos["B"]
                assert ampliada["r"] == escala * datos["r"]
                _, termino, _ = orbita(escala * datos["u"], longitud + relleno)
                assert ampliada["paradoja"] == (
                    ampliada["D"] > 0 and ampliada["D"] * ampliada["u"] <= ampliada["B"])
                assert (ampliada["D"] > 0 and termino >= escala * datos["u"]) == (
                    3 ** datos["s"] < escala * modulo and
                    (escala * modulo - 3 ** datos["s"]) * datos["u"] <= datos["B"])
                totales["controles_relleno"] += 1
            for indice in range(longitud - 1):
                if palabra[indice:indice + 2] != "01":
                    continue
                cambiada = palabra[:indice] + "10" + palabra[indice + 2:]
                nueva = datos_palabra(cambiada)
                antes = palabra[:indice].count("1")
                despues = palabra[indice + 2:].count("1")
                resto_modulo = 2 ** (longitud - indice)
                inversa = pow(3 ** (antes + 1), -1, resto_modulo)
                acarreo = int(datos["r"] + 2 ** indice * inversa >= modulo)
                assert nueva["B"] == datos["B"] - 2 ** indice * 3 ** despues
                assert nueva["r"] == datos["r"] + 2 ** indice * inversa - acarreo * modulo
                cambio = 2 ** indice * (datos["D"] * (inversa - acarreo * resto_modulo) + 3 ** despues)
                assert datos["D"] * (nueva["r"] - datos["r"]) - (nueva["B"] - datos["B"]) == cambio
                correccion = (nueva["u"] - nueva["r"] - datos["u"] + datos["r"]) // modulo
                assert nueva["margen"] - datos["margen"] == cambio + datos["D"] * modulo * correccion
                if datos["D"] > 0:
                    totales["intercambios_con_D_positivo"] += 1
                    totales["con_acarreo" if acarreo else "sin_acarreo"] += 1
                    if not acarreo:
                        assert cambio > 0
                    caso = dict(palabra=palabra, cambiada=cambiada, indice=indice,
                                anterior=datos, nueva=nueva, h=inversa, H=resto_modulo,
                                acarreo=acarreo, cambio_margen_residuo=cambio,
                                trayectoria_anterior=orbita(datos["u"], longitud)[2],
                                trayectoria_nueva=orbita(nueva["u"], longitud)[2])
                    if datos["r"] > 2 and nueva["r"] > 2:
                        if datos["paradoja"] != nueva["paradoja"]:
                            clave = "crea_paradoja" if nueva["paradoja"] else "pierde_paradoja"
                            testigos.setdefault(clave, caso)
                        signo = "positivo" if cambio > 0 else "negativo" if cambio < 0 else "nulo"
                        testigos.setdefault(f"acarreo_{acarreo}_margen_{signo}", caso)
                totales["intercambios"] += 1
            totales["palabras"] += 1
        # Segundo conteo: todas las semillas hasta el mayor umbral B/D,
        # decidiendo paradoja sólo desde su órbita y número de impares.
        limite = max((datos_palabra(p)["B"] // datos_palabra(p)["D"]
                      for p in directos if datos_palabra(p)["D"] > 0), default=0)
        segmentos_directos = 0
        for semilla in range(3, limite + 1):
            palabra, final, _ = orbita(semilla, longitud)
            if 3 ** palabra.count("1") < modulo and final >= semilla:
                segmentos_directos += 1
        assert segmentos == segmentos_directos
        totales["segmentos_paradojicos"] += segmentos
        por_longitud.append(dict(L=longitud, segmentos=segmentos, limite_semilla=limite))
    bordes = []
    for semilla, longitud, factor in [(7, 8, 3), (13, 7, 5), (1, 2, 3), (2, 1, 3), (3, 1, 3), (-1, 1, 3)]:
        palabra, final, trayectoria = orbita(semilla, longitud, factor)
        datos = datos_palabra(palabra, factor)
        assert 2 ** longitud * final == factor ** datos["s"] * semilla + datos["B"]
        paradoja = semilla > 2 and datos["D"] > 0 and final >= semilla
        assert paradoja == (semilla > 2 and datos["D"] > 0 and datos["D"] * semilla <= datos["B"])
        bordes.append(dict(n=semilla, L=longitud, factor=factor, palabra=palabra,
                          B=datos["B"], D=datos["D"], final=final, paradoja=paradoja,
                          trayectoria=trayectoria))
    return dict(longitud_maxima=longitud_maxima, aritmetica="enteros exactos",
                totales=totales, por_longitud=por_longitud, testigos=testigos, bordes=bordes)


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--longitud-maxima", type=int, required=True, choices=range(1, 13))
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    resultado = verificar(argumentos.longitud_maxima)
    resultado["sha256_verificador"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    argumentos.salida.parent.mkdir(parents=True, exist_ok=True)
    argumentos.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(resultado["totales"], ensure_ascii=False))
    print(json.dumps(resultado["testigos"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
