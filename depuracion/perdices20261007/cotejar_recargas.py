"""Contraste exacto y acotado de recargas A/B; no busca nuevas semillas récord."""

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path


CARPETA = Path(__file__).resolve().parent
RAIZ = CARPETA.parents[1]
PARAMETROS = {"A": (1, 1, 3, 2, 1), "B": (3, 5, 9, 8, 5)}


def orden2(numero):
    assert numero > 0
    return (numero & -numero).bit_length() - 1


def orden_por_divisiones(numero):
    assert numero > 0
    exponente = 0
    while numero % 2 == 0:
        numero //= 2
        exponente += 1
    return exponente


def atajo(numero):
    return numero // 2 if numero % 2 == 0 else (3 * numero + 1) // 2


def realizar_bloque(numero, bloque):
    """Implementación orbital independiente de las fórmulas afines."""
    valor = numero
    for paridad in ((1,) if bloque == "A" else (1, 1, 0)):
        if valor % 2 != paridad:
            return None
        valor = atajo(valor)
    return valor


def verificar_palabra(semilla, palabra):
    assert semilla > 0 and palabra
    valor = semilla
    largo = 0
    suma = 0
    filas = []
    for indice, bloque in enumerate(palabra):
        pasos, constante, factor, divisor, aditivo = PARAMETROS[bloque]
        siguiente = realizar_bloque(valor, bloque)
        assert siguiente is not None, (semilla, palabra, indice)
        assert divisor * siguiente == factor * valor + aditivo
        entrada = orden2(valor + constante)
        salida = orden2(siguiente + constante)
        assert entrada == pasos + salida
        assert entrada == orden_por_divisiones(valor + constante)
        assert salida == orden_por_divisiones(siguiente + constante)
        eta = 0
        if indice:
            anterior = palabra[indice - 1]
            constante_anterior = PARAMETROS[anterior][1]
            eta = entrada - orden2(valor + constante_anterior)
            if anterior == bloque:
                assert eta == 0
            elif (anterior, bloque) == ("A", "B"):
                previo = filas[-1]["entrada"]
                assert orden2(previo + 1) == 3
                impar = (previo + 1) // 8
                assert eta == orden2(3 * impar + 1) > 0
            else:
                previo = filas[-1]["entrada"]
                exponente = orden2(previo + 5)
                impar = (previo + 5) // 2 ** exponente
                assert exponente >= 4
                if exponente == 4:
                    assert eta == 0
                elif exponente == 5:
                    assert eta == orden2(9 * impar - 1) > 0
                else:
                    assert eta == 5 - exponente < 0
        suma += eta
        largo += pasos
        inicial = orden2(semilla + PARAMETROS[palabra[0]][1])
        assert largo == inicial + suma - salida
        filas.append(dict(bloque=bloque, entrada=valor, salida=siguiente,
                          valuacion_entrada=entrada, valuacion_salida=salida,
                          recarga=eta))
        valor = siguiente
    return dict(semilla=semilla, palabra=palabra, largo=largo, recarga=suma,
                valuacion_inicial=inicial, valuacion_final=salida,
                presupuesto=(semilla + 4).bit_length(), filas=filas)


def exponente_congruente(exponente_modulo, objetivo, desplazamiento, minimo):
    """Levanta sólo exponentes módulo 2*3^(k-1); nunca construye 2^m."""
    assert exponente_modulo >= 1 and objetivo % 3 != 0
    exponente = next(i for i in range(2)
                     if pow(2, i + desplazamiento, 3) == objetivo % 3)
    modulo = 3
    periodo = 2
    for _ in range(1, exponente_modulo):
        modulo *= 3
        candidatos = [exponente + j * periodo for j in range(3)
                      if pow(2, exponente + j * periodo + desplazamiento,
                             modulo) == objetivo % modulo]
        assert len(candidatos) == 1
        exponente = candidatos[0]
        periodo *= 3
    if exponente < minimo:
        exponente += ((minimo - exponente + periodo - 1) // periodo) * periodo
    assert pow(2, exponente + desplazamiento, modulo) == objetivo % modulo
    assert exponente >= minimo
    return exponente


def familia_alternante(repeticiones, minimo):
    potencia_dos = 16 ** repeticiones
    potencia_tres = 27 ** repeticiones
    aditivo, resto = divmod(19 * (potencia_tres - potencia_dos), 11)
    assert resto == 0
    objetivo, resto = divmod(aditivo + 5 * potencia_dos, 9)
    assert resto == 0 and objetivo % 3 == 2
    modulo = 3 ** (3 * repeticiones - 2)
    exponente = exponente_congruente(3 * repeticiones - 2, objetivo,
                                    4 * repeticiones, minimo)
    return dict(r=repeticiones, m=exponente, N=potencia_dos, D=potencia_tres,
                E=aditivo, H=objetivo, modulo=modulo)


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--pasos", type=int, required=True)
    analizador.add_argument("--familia-materializada", type=int, required=True)
    analizador.add_argument("--beta-max", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    assert args.pasos >= 35
    assert 1 <= args.familia_materializada <= 3
    assert 0 <= args.beta_max <= 32
    origen = CARPETA / "medicion_salida_ab.json"
    historico = json.loads(origen.read_text(encoding="utf-8"))
    testigos = {int(fila["minimo"]) for fila in historico["filas"]}
    semillas = sorted(testigos | {1, 2, 3, 7, 11, 15, 27, 31, 39, 63, 91})
    contador = Counter()
    signos = Counter()
    fallos = []
    controles_un_bloque = 0
    repeticiones_sin_recarga = 0
    for semilla in semillas:
        pendientes = [(semilla, "", 0)]
        while pendientes:
            valor, palabra, largo = pendientes.pop()
            for bloque in ("A", "B"):
                nuevo_largo = largo + PARAMETROS[bloque][0]
                if nuevo_largo > args.pasos:
                    continue
                siguiente = realizar_bloque(valor, bloque)
                if siguiente is None:
                    continue
                nueva_palabra = palabra + bloque
                dato = verificar_palabra(semilla, nueva_palabra)
                contador["prefijos"] += 1
                if len(nueva_palabra) == 1:
                    assert dato["recarga"] == 0
                    controles_un_bloque += 1
                if len(nueva_palabra) >= 2:
                    eta = dato["filas"][-1]["recarga"]
                    signos[(nueva_palabra[-2:], (eta > 0) - (eta < 0))] += 1
                    if nueva_palabra[-2] == nueva_palabra[-1]:
                        repeticiones_sin_recarga += 1
                if 2 * dato["recarga"] > nuevo_largo + 2 * dato["presupuesto"]:
                    fallos.append({k: dato[k] for k in
                                   ("semilla", "palabra", "largo", "recarga", "presupuesto")})
                pendientes.append((siguiente, nueva_palabra, nuevo_largo))
    assert controles_un_bloque and repeticiones_sin_recarga
    assert signos[("BA", -1)] and signos[("BA", 0)] and signos[("BA", 1)]
    testigo = verificar_palabra(4591, "AABABAAABAABAAB")
    assert (testigo["largo"], testigo["recarga"], testigo["presupuesto"]) == (25, 26, 13)
    simples = []
    for t in range(1, 13):
        numerador = 2 ** (2 * t + 3) - 11
        semilla, resto = divmod(numerador, 3)
        assert resto == 0
        dato = verificar_palabra(semilla, "AB")
        assert (orden2(semilla + 1), orden2(semilla + 5)) == (3, 2)
        assert dato["recarga"] == 2 * t
        simples.append(dict(t=t, semilla=semilla, recarga=2 * t))
    alternantes = []
    for r in range(1, args.familia_materializada + 1):
        datos = familia_alternante(r, r + 2)
        m = datos["m"]
        semilla, resto = divmod(2 ** (m + 4 * r) - datos["H"], datos["modulo"])
        assert resto == 0 and semilla > 0
        dato = verificar_palabra(semilla, "AB" * r)
        assert dato["filas"][-1]["salida"] == 9 * 2 ** m - 5
        assert dato["valuacion_inicial"] == 3 and dato["valuacion_final"] == m
        assert dato["recarga"] == 4 * r + m - 3
        assert semilla + 5 == Fraction(9 * datos["N"], datos["D"]) * 2 ** m + Fraction(
            36 * (datos["D"] - datos["N"]), 11 * datos["D"])
        alternantes.append(dict(**datos, semilla=str(semilla), largo=dato["largo"],
                                 recarga=dato["recarga"], presupuesto=dato["presupuesto"]))
    simbolicos = []
    for beta in range(args.beta_max + 1):
        r = 2 * beta + 18
        datos = familia_alternante(r, max(r + 2, beta + 7))
        # Sólo enteros de tamaño O(r) y exponenciación modular.
        assert 9 * datos["N"] * 2 ** (beta + 5) < datos["D"]
        assert Fraction(36 * (datos["D"] - datos["N"]), 11 * datos["D"]) < 4
        assert datos["m"] >= max(r + 2, beta + 7)
        simbolicos.append(dict(beta=beta, **datos,
                              techo_presupuesto_menos_m=-4,
                              recarga_menos_largo_menos_m=-3,
                              semilla_materializada=False))
    fuentes = [Path(__file__), origen, CARPETA / "PerdicesRecargas.lean"]
    huellas = {p.relative_to(RAIZ).as_posix(): hashlib.sha256(
        p.read_bytes().replace(b"\r\n", b"\n")).hexdigest() for p in fuentes}
    resultado = dict(
        parametros=dict(pasos=args.pasos, familia_materializada=args.familia_materializada,
                        beta_max=args.beta_max),
        alcance="Controles finitos, no prueba universal ni nuevo censo de semillas.",
        testigos_historicos=len(testigos), semillas_con_bordes=len(semillas),
        prefijos=contador["prefijos"], controles_un_bloque=controles_un_bloque,
        repeticiones_sin_recarga=repeticiones_sin_recarga,
        transiciones=[dict(cambio=c, signo=s, casos=v) for (c, s), v in sorted(signos.items())],
        fallos_plantilla=len(fallos), primer_fallo=fallos[0], testigo=testigo,
        familia_un_cambio=simples, familia_alternante=alternantes,
        certificados_simbolicos=simbolicos, sha256_lf=huellas)
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps({k: resultado[k] for k in
                      ("testigos_historicos", "semillas_con_bordes", "prefijos",
                       "fallos_plantilla", "primer_fallo")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
