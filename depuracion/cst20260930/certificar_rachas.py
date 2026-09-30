"""Reducción exacta de Ocelotas para hasta R rachas; condicionada a RhinEntera.

Mapa T(n)=n/2 (par), (3n+1)/2 (impar), dominio n>=2. No usa flotantes.
La prueba universal está en REVISION_RACHAS.md; este programa certifica sus
desigualdades finitas y el descenso de las semillas restantes. No prueba Rhin.
No ejecuta barridos al importar. Todos los topes figuran en el informe.
"""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def techo_log2(numerador, denominador):
    """Menor m>=0 con numerador/denominador <= 2**m, para cociente >=1."""
    if not numerador >= denominador > 0:
        raise ValueError("Se requiere numerador >= denominador > 0")
    m = max(0, numerador.bit_length() - denominador.bit_length())
    if numerador > denominador << m:
        m += 1
    assert numerador <= denominador << m
    assert m == 0 or numerador > denominador << (m - 1)
    return m


def cota_impares(rachas, m):
    """5 A_i < 5m + 8 A_(i-1), A_0=0; cota entera inclusiva de A_r."""
    acumulado = 0
    for _ in range(rachas):
        acumulado = (5 * m + 8 * acumulado - 1) // 5
    return acumulado


def parametros(rachas):
    if rachas < 1:
        raise ValueError("El número de rachas debe ser positivo")
    assert 3 ** 5 < 2 ** 8
    factor = sum((Fraction(8, 5) ** i for i in range(rachas)), Fraction())
    exponente = -(-factor.numerator // factor.denominator)
    c = techo_log2(rachas + 1, 1)
    h = 1
    while (1 << h) <= 2 * exponente * (c + 14 * (h + 1)):
        h += 1
    # Esta desigualdad y su preservación al incrementar h dan la cola infinita.
    assert c + 14 * (h + 1) >= 14
    return {
        "rachas_hasta": rachas,
        "factor_racional": str(factor),
        "exponente_entero": exponente,
        "c": c,
        "h": h,
        "k_exclusivo": 1 << h,
    }


def cribar(rachas):
    datos = parametros(rachas)
    potencia = 1
    q = 0
    supervivientes = []
    while True:
        q += 1
        potencia *= 3
        k = potencia.bit_length()
        if k >= datos["k_exclusivo"]:
            break
        delta = (1 << k) - potencia
        assert 0 < delta < potencia
        # M=(R+1) P/Delta y un fallo implica n+1<M.
        m = techo_log2((rachas + 1) * potencia, delta)
        if q > cota_impares(rachas, m):
            continue
        # Usamos la cota más fuerte n<R P/Delta, no n+1<M.
        n_maximo = (rachas * potencia - 1) // delta
        supervivientes.append({"q": q, "k": k, "m": m, "n_maximo": n_maximo})
    datos.update({
        "q_comprobados": q - 1,
        "primer_q_excluido_por_k": q,
        "k_del_primer_q_excluido": k,
        "supervivientes": supervivientes,
        "n_maximo": max(f["n_maximo"] for f in supervivientes),
        "k_maximo_superviviente": max(f["k"] for f in supervivientes),
    })
    return datos


def primer_cruce(n, max_pasos, cotejar=False):
    """Iteración directa, sin usar las fórmulas de rachas para decidir CST."""
    if n < 2 or max_pasos < 1:
        raise ValueError("Se requiere n>=2 y max_pasos>=1")
    x = n
    potencia_tres = 1
    rachas = 0
    anterior_impar = False
    acumulado = 0
    impares_previos = 0
    inicios = []
    aditivo = 0
    for k in range(1, max_pasos + 1):
        impar = bool(x % 2)
        if impar:
            if not anterior_impar:
                rachas += 1
                inicios.append((k - 1, acumulado))
                impares_previos = acumulado
            acumulado += 1
            potencia_tres *= 3
            aditivo = 3 * aditivo + (1 << (k - 1))
            x = (3 * x + 1) // 2
        else:
            if anterior_impar and cotejar:
                assert (n + 1) * 3 ** impares_previos >= 1 << acumulado
            x //= 2
        anterior_impar = impar
        if potencia_tres < 1 << k:
            assert not impar
            if cotejar:
                assert (1 << k) * x == potencia_tres * n + aditivo
                if rachas:
                    # Fórmula independiente, agrupando por rachas.
                    suma = 0
                    for i, (posicion, previos) in enumerate(inicios):
                        fin = inicios[i + 1][1] if i + 1 < len(inicios) else acumulado
                        longitud = fin - previos
                        suma += (1 << posicion) * 3 ** (acumulado - fin) * (
                            3 ** longitud - (1 << longitud))
                    assert suma == aditivo < rachas * potencia_tres
                else:
                    assert aditivo == 0 and k == 1
            return {"k": k, "q": acumulado, "rachas": rachas, "valor": x}
    raise RuntimeError(f"INCONCLUSO: n={n}, sin primer cruce en {max_pasos} pasos")


def verificar_semillas(n_maximo, max_pasos, cotejo_hasta):
    huella = hashlib.sha256()
    maximo_k = 0
    for n in range(2, n_maximo + 1):
        cruce = primer_cruce(n, max_pasos, n <= cotejo_hasta)
        if cruce["valor"] >= n:
            raise AssertionError(f"Fallo CST: n={n}, datos={cruce}")
        maximo_k = max(maximo_k, cruce["k"])
        huella.update(f'{n},{cruce["k"]},{cruce["q"]},{cruce["valor"]}\n'.encode())
    return {
        "desde_inclusivo": 2,
        "hasta_inclusivo": n_maximo,
        "semillas": max(0, n_maximo - 1),
        "max_pasos_permitidos": max_pasos,
        "max_primer_cruce_observado": maximo_k,
        "cotejo_lemas_hasta": min(n_maximo, cotejo_hasta),
        "sha256_filas_n_k_q_valor": huella.hexdigest(),
        "fallos": 0,
        "inconclusos": 0,
    }


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--rachas", type=int, required=True)
    analizador.add_argument("--max-pasos", type=int, default=10000)
    analizador.add_argument("--cotejo-hasta", type=int, default=2000)
    analizador.add_argument("--salida", type=Path)
    opciones = analizador.parse_args()
    if opciones.rachas < 1 or opciones.max_pasos < 1 or opciones.cotejo_hasta < 0:
        analizador.error("rachas y max-pasos positivos; cotejo-hasta no negativo")
    datos = cribar(opciones.rachas)
    datos["hipotesis_externa"] = "RhinEntera; no demostrada por este cálculo"
    datos["aritmetica"] = "int y Fraction; sin logaritmos aproximados"
    datos["barrido"] = verificar_semillas(
        datos["n_maximo"], opciones.max_pasos, opciones.cotejo_hasta)
    datos["sha256_programa"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    if opciones.salida:
        opciones.salida.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    resumen = {clave: valor for clave, valor in datos.items() if clave != "supervivientes"}
    resumen["numero_supervivientes"] = len(datos["supervivientes"])
    print(json.dumps(resumen, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
