"""Ocelotas: cotas por el lado positivo de k log 2 - q log 3.

Mapa T(n)=n/2 si par, (3n+1)/2 si impar. n>=2, primer cruce k finito.
Si falla CST, Lambda*n<r. Pares unimodulares U=(P,Q), V=(p,q) con
L(U)>0>L(V) dan L(k,b)>=L(U) para 0<b<Q+q y L(k,b)>0.
El lema universal y la criba estan en OcelotasAfinada.lean.
Las tablas y el censo final no estan certificados en Lean.
"""

import argparse
from fractions import Fraction
import json
from pathlib import Path

from rachas_afinadas import cota_afinada, log2_encerrado
from rachas_convergentes import cola_con_lmn, log_dos_inferior, log_dos_superior, techo


def intervalos_superiores(alfa_inf, alfa_sup, objetivo):
    """Mediantes certificados; comprime pasos que no cambian el extremo superior."""
    inferior = (1, 1)
    superior = (2, 1)
    inicio = 1
    intervalos = []
    while True:
        p, q = inferior
        P, Q = superior
        fin = Q + q
        numerador = P + p
        assert P * q - p * Q == 1
        assert p < q * alfa_inf and P > Q * alfa_sup
        if fin >= objetivo or numerador > fin * alfa_sup:
            intervalos.append({"q_inicio": inicio, "q_fin": fin,
                               "superior": superior, "inferior": inferior})
            if fin >= objetivo:
                return intervalos
            superior = (numerador, fin)
            inicio = fin
        elif numerador < fin * alfa_inf:
            inferior = (numerador, fin)
        else:
            raise ValueError("Signo ambiguo: aumentar bits de alfa")


def estudiar(rachas, intervalos, alfa_sup, ln2_inf, bits, guarda):
    filas = []
    limite = 0
    decisivo = None
    for indice, intervalo in enumerate(intervalos):
        p, q = intervalo["superior"]
        c = ln2_inf * (p - q * alfa_sup)
        if c <= 0:
            raise ValueError("Cota de Lambda no positiva")
        semilla = techo(rachas / c)
        _, beta = log2_encerrado(semilla, bits, guarda)
        tope = cota_afinada(rachas, beta, alfa_sup)
        sobrevive = intervalo["q_inicio"] <= tope
        filas.append({"intervalo": indice, "semilla_exclusiva": semilla,
                      "cota_q": tope, "sobrevive": sobrevive})
        if sobrevive and semilla > limite:
            limite = semilla
            decisivo = indice
    return {"rachas": rachas, "semilla_exclusiva": limite,
            "intervalo_decisivo": decisivo, "filas": filas}


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--q-cola", type=int, default=10 ** 28)
    analizador.add_argument("--bits-alfa", type=int, default=256)
    analizador.add_argument("--bits-semilla", type=int, default=128)
    analizador.add_argument("--guarda", type=int, default=64)
    analizador.add_argument("--rachas", type=int, nargs="+", default=[10, 11, 12, 13, 17, 18, 19, 75, 76])
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    if argumentos.q_cola < 2 or min(argumentos.bits_alfa, argumentos.bits_semilla,
                                   argumentos.guarda, *argumentos.rachas) < 1:
        analizador.error("Parametros positivos; q-cola>=2")
    inferior, superior = log2_encerrado(3, argumentos.bits_alfa, argumentos.guarda)
    intervalos = intervalos_superiores(inferior, superior, argumentos.q_cola)
    cola = intervalos[-1]["q_fin"]
    ln2_inf, ln2_sup = log_dos_inferior(), log_dos_superior()
    resultados = []
    for rachas in sorted(set(argumentos.rachas)):
        if not cola_con_lmn(rachas, cola, ln2_inf, ln2_sup):
            raise ValueError(f"Cola LMN insuficiente para R={rachas}")
        resultado = estudiar(rachas, intervalos, superior, ln2_inf,
                            argumentos.bits_semilla, argumentos.guarda)
        resultados.append(resultado)
        print(f"R={rachas}: n<{resultado['semilla_exclusiva']}; "
              f"intervalo {resultado['intervalo_decisivo']}")
    certificado = {"mapa": "T(n)=n/2 si par; (3n+1)/2 si impar",
                   "condicion": "n>=2; primer cruce finito; LMN en la cola",
                   "parametros": {"bits_alfa": argumentos.bits_alfa,
                                  "bits_semilla": argumentos.bits_semilla,
                                  "guarda": argumentos.guarda,
                                  "q_cola_solicitado": argumentos.q_cola},
                   "alfa_inferior": str(inferior), "alfa_superior": str(superior),
                   "log2_inferior": str(ln2_inf), "log2_superior": str(ln2_sup),
                   "cola_desde": cola, "intervalos": intervalos,
                   "resultados": resultados}
    argumentos.salida.write_text(json.dumps(certificado, ensure_ascii=False, indent=2)
                                 + "\n", encoding="utf-8")
    print(f"{len(intervalos)} intervalos cubren 1<=q<{cola}; resto por LMN.")
    print("Reduccion de semillas; no se ha ampliado ningun censo ni el numero de rachas cerrado.")


if __name__ == "__main__":
    main()
