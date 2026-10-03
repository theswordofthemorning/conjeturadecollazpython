"""CST por rachas: criba con log2(s) y log2(3) encerrados en racionales.

Mapa T(n)=n/2 (par), (3n+1)/2 (impar), n>=2. k=tau(n) es el primer
cruce finito, q=S_k(n), r<=R el numero de rachas impares. Para un fallo:
n<R/Lambda y 2^A_(i+1)<=(n+1)3^A_i. En q_j<=q<q_(j+1), Lagrange
da n<s=ceil(R(q_j+q_(j+1))/(693/1000)), luego n+1<=s. Con cotas
superiores racionales beta>log2(s), alfa>log2(3), se itera
C_0=0, C_(i+1)=floor(beta+alfa*C_i). Si C_R<q_j, no hay fallo.

La cola conserva la criba anterior, mas debil, y LMN. No recorre semillas
ni prueba CST universal. El cierre usa censos ya realizados y citados.
"""

import argparse
from fractions import Fraction
import json
from pathlib import Path

from verificar_rhin_convergentes import cocientes_certificados, convergentes
from rachas_convergentes import cola_con_lmn, log_dos_inferior, log_dos_superior, techo


def log2_encerrado(numero, bits, guarda):
    """Cuadrados con redondeo dirigido; devuelve [inferior, superior] exacto.

    La normalizacion deja numero/2^entero en [1,2). En cada paso se
    decide un bit solo cuando todo el intervalo esta al mismo lado de 2.
    La cota superior final es estricta, incluso para potencias de dos.
    """
    if numero < 1 or bits < 1 or guarda < 1:
        raise ValueError("Se requieren numero, bits y guarda positivos")
    entero = numero.bit_length() - 1
    escala = 1 << (bits + guarda)
    inferior = numero * escala // (1 << entero)
    superior = -((-numero * escala) // (1 << entero))
    codigo = 0
    for _ in range(bits):
        inferior = inferior * inferior // escala
        superior = -((-superior * superior) // escala)
        if inferior >= 2 * escala:
            bit = 1
            inferior //= 2
            superior = (superior + 1) // 2
        elif superior < 2 * escala:
            bit = 0
        else:
            raise ValueError(f"Bit ambiguo para {numero}; aumentar guarda")
        codigo = 2 * codigo + bit
    return (entero + Fraction(codigo, 1 << bits),
            entero + Fraction(codigo + 1, 1 << bits))


def cota_afinada(rachas, beta, alfa):
    acumulado = 0
    for _ in range(rachas):
        valor = beta + alfa * acumulado
        acumulado = valor.numerator // valor.denominator
    return acumulado


def estudiar(rachas, denominadores, alfa, ln2, bits, guarda):
    limite = 0
    decisivo = None
    intervalos = []
    for indice in range(1, len(denominadores) - 1):
        inicio, fin = denominadores[indice:indice + 2]
        semilla = techo(Fraction(rachas * (inicio + fin)) / ln2)
        _, beta = log2_encerrado(semilla, bits, guarda)
        cota = cota_afinada(rachas, beta, alfa)
        sobrevive = inicio <= cota
        intervalos.append({"j": indice, "q_inicio": inicio, "q_fin": fin,
                           "semilla_exclusiva": semilla, "cota_q": cota,
                           "sobrevive": sobrevive})
        if sobrevive and semilla > limite:
            limite = semilla
            decisivo = indice
    return {"rachas": rachas, "semilla_exclusiva": limite,
            "intervalo_decisivo": decisivo, "intervalos": intervalos}


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--bits-alfa", type=int, default=256)
    analizador.add_argument("--bits-semilla", type=int, default=128)
    analizador.add_argument("--guarda", type=int, default=64)
    analizador.add_argument("--rmax", type=int, default=80)
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    if min(argumentos.bits_alfa, argumentos.bits_semilla,
           argumentos.guarda, argumentos.rmax) < 1:
        analizador.error("Todos los parametros numericos deben ser positivos")
    cocientes, bajo, alto = cocientes_certificados(argumentos.bits_alfa, argumentos.guarda)
    pares = convergentes(cocientes)
    denominadores = [q for _, q in pares]
    if len(pares) < 3 or denominadores[1] != 1:
        raise ValueError("Los intervalos no cubren desde q=1")
    ln2 = log_dos_inferior()
    ln2_sup = log_dos_superior()
    resultados = []
    for rachas in range(1, argumentos.rmax + 1):
        if not cola_con_lmn(rachas, denominadores[-1], ln2, ln2_sup):
            raise ValueError(f"La cola LMN no cierra para R={rachas}")
        resultados.append(estudiar(rachas, denominadores, alto, ln2,
                                   argumentos.bits_semilla, argumentos.guarda))
    propio = max((r["rachas"] for r in resultados
                  if r["semilla_exclusiva"] <= 2 ** 23), default=0)
    externo = max((r["rachas"] for r in resultados
                   if r["semilla_exclusiva"] <= 28 * 10 ** 18 + 1), default=0)
    certificado = {
        "mapa": "T(n)=n/2 si par; (3n+1)/2 si impar",
        "condicion": "n>=2; tau(n)=k finito; rachas hasta k; cola bajo LMN",
        "parametros": {"bits_alfa": argumentos.bits_alfa,
                       "bits_semilla": argumentos.bits_semilla,
                       "guarda": argumentos.guarda, "rmax": argumentos.rmax},
        "alfa_inferior": str(bajo), "alfa_superior": str(alto),
        "cocientes": cocientes, "convergentes": pares,
        "log2_inferior": str(ln2), "log2_superior": str(ln2_sup),
        "cierre_propio": {"n_exclusivo": 2 ** 23, "rachas": propio,
                           "evidencia": "verificar_r_rachas_23_salida.txt"},
        "cierre_externo": {"n_inclusivo": 28 * 10 ** 18, "rachas": externo,
                            "hipotesis": "Rozier-Terracol v5, corolario 5.4"},
        "resultados": resultados,
    }
    argumentos.salida.write_text(json.dumps(certificado, ensure_ascii=False, indent=2)
                                 + "\n", encoding="utf-8")
    print(f"{len(pares)} convergentes certificados; cola desde q={denominadores[-1]}.")
    for resultado in resultados:
        if resultado["rachas"] in {17, 18, 19, 73, 74, 75, 76}:
            print(f"R={resultado['rachas']}: n<{resultado['semilla_exclusiva']}; "
                  f"intervalo j={resultado['intervalo_decisivo']}")
    print(f"Cierre con barrido propio existente: hasta {propio} rachas.")
    print(f"Cierre condicional a Rozier-Terracol: hasta {externo} rachas.")
    print("Calculo exacto y prueba escrita; extension no formalizada en Lean.")


if __name__ == "__main__":
    main()
