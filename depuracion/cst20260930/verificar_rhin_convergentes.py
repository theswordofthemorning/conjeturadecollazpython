"""Forma entera de Rhin: comprobación hasta k enormes por los convergentes de log2(3).

RhinEntera en (k, q): si 2^(k-1) <= 3^q < 2^k, entonces 3^q <= (2^k - 3^q) * k^14.

Reducción (Legendre). Sea Lambda = k log 2 - q log 3, que es positiva y como
mucho log 2 en esa ventana. Como 2^k / 3^q = e^Lambda >= 1 + Lambda, basta
Lambda * k^14 >= 1. Si fallara en (k, q) con k >= 2, la fracción reducida
k'/q' = (k/d)/(q/d) cumpliría Lambda' * k'^14 = Lambda * k^14 / d^15 < 1 y
|log2(3) - k'/q'| = Lambda' / (q' log 2) < 1 / (2 q'^2), así que k'/q' sería un
convergente de log2(3), y además superior (Lambda' > 0). Por tanto, si todos
los convergentes superiores con numerador <= K cumplen Lambda * p^14 >= 1,
RhinEntera vale para todo k <= K. El caso k = 1 (q = 0) se comprueba aparte.

Todo es aritmética entera o racional exacta:
- log2(3) se encierra con cuadrados sucesivos de 3/2, redondeando hacia
  abajo la cota inferior y hacia arriba la superior;
- sólo se usan los cocientes parciales comunes a las dos cotas;
- log 2 > 693/1000 se certifica con la serie de exp(693/1000) < 2.
El módulo decimal (logaritmos de la biblioteca estándar) sólo sirve de cotejo
independiente de los cocientes; no interviene en la conclusión.
"""

import argparse
import decimal
from fractions import Fraction
import math


def bits_de_log2_tres(m, guarda):
    """Devuelve B con log2(3) en [1 + B/2^m, 1 + (B+1)/2^m)."""
    P = m + guarda
    uno = 1 << P
    dos = 2 << P
    inferior = 3 << (P - 1)        # 3/2 exacto
    superior = 3 << (P - 1)
    B = 0
    for _ in range(m):
        inferior = (inferior * inferior) >> P
        superior = -((-(superior * superior)) >> P)     # techo
        if inferior >= dos:
            bit = 1
            inferior = inferior >> 1
            superior = -((-superior) >> 1)
        elif superior < dos:
            bit = 0
        else:
            raise ValueError("Bit ambiguo: aumentar la guarda")
        if inferior < uno:
            raise ValueError("Cota inferior por debajo de 1: aumentar la guarda")
        B = 2 * B + bit
    return B


def fraccion_continua(x, maximo):
    """Cocientes parciales de un racional positivo."""
    cocientes = []
    numerador, denominador = x.numerator, x.denominator
    while denominador != 0 and len(cocientes) < maximo:
        a, resto = divmod(numerador, denominador)
        cocientes.append(a)
        numerador, denominador = denominador, resto
    return cocientes


def cocientes_certificados(m, guarda):
    """Cocientes parciales de log2(3) válidos para todo número de su encierro."""
    B = bits_de_log2_tres(m, guarda)
    bajo = Fraction((1 << m) + B, 1 << m)
    alto = Fraction((1 << m) + B + 1, 1 << m)
    fb = fraccion_continua(bajo, 10 ** 9)
    fa = fraccion_continua(alto, 10 ** 9)
    comunes = []
    for x, y in zip(fb, fa):
        if x != y:
            break
        comunes.append(x)
    # El último común de un racional puede no ser definitivo: se descarta.
    return comunes[:-1], bajo, alto


def log_dos_inferior():
    """Certifica log 2 > 693/1000 mostrando exp(693/1000) < 2 con serie y resto."""
    x = Fraction(693, 1000)
    suma = Fraction(0)
    termino = Fraction(1)
    for j in range(40):
        suma += termino
        termino = termino * x / (j + 1)
    # Resto: termino * (1 + x/41 + ...) <= termino / (1 - x/41)
    resto = termino / (1 - x / 41)
    if suma + resto >= 2:
        raise ValueError("No se certificó log 2 > 0,693")
    return x


def convergentes(cocientes):
    """Pares (p_n, q_n), con p_n/q_n > log2(3) cuando n es impar."""
    p_ant, q_ant = 1, 0
    p, q = cocientes[0], 1
    lista = [(p, q)]
    for a in cocientes[1:]:
        p, p_ant = a * p + p_ant, p
        q, q_ant = a * q + q_ant, q
        lista.append((p, q))
    return lista


def rhin_entera_exacta(k, q):
    tres = 3 ** q
    dos = 1 << k
    return dos <= 2 * tres and tres < dos and tres <= (dos - tres) * k ** 14


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--bits", type=int, default=20000,
                            help="bits de log2(3) que se encierran")
    analizador.add_argument("--guarda", type=int, default=256,
                            help="bits de guarda del encierro")
    analizador.add_argument("--q-exacto", type=int, default=3000,
                            help="barrido exacto de RhinEntera para 0 <= q <= este valor")
    analizador.add_argument("--q-convergente-exacto", type=int, default=200000,
                            help="convergentes con q hasta aquí se comprueban también con enteros")
    argumentos = analizador.parse_args()

    print("Forma entera de Rhin por convergentes de log2(3)")
    print(f"Parámetros: bits = {argumentos.bits}, guarda = {argumentos.guarda}, "
          f"q exacto <= {argumentos.q_exacto}, convergentes exactos con q <= "
          f"{argumentos.q_convergente_exacto}")

    # 1. Barrido exacto de control.
    peor = None
    for q in range(argumentos.q_exacto + 1):
        tres = 3 ** q
        k = tres.bit_length()          # el único k con 2^(k-1) <= 3^q < 2^k
        if not rhin_entera_exacta(k, q):
            raise SystemExit(f"FALLO EXACTO en q = {q}, k = {k}")
        margen = Fraction((((1 << k) - tres) * k ** 14), tres)
        if q >= 1 and (peor is None or margen < peor[0]):
            peor = (margen, k, q)
    print(f"\n1. Barrido exacto 0 <= q <= {argumentos.q_exacto}: sin fallos.")
    print("   En q = 0, k = 1 la desigualdad es la igualdad 1 <= 1.")
    print(f"   Con q >= 1, menor cociente (2^k - 3^q) k^14 / 3^q = {float(peor[0]):.4g}, "
          f"en k = {peor[1]}, q = {peor[2]}.")

    # 2. Encierro entero de log2(3) y cocientes certificados.
    cocientes, bajo, alto = cocientes_certificados(argumentos.bits, argumentos.guarda)
    print(f"\n2. log2(3) encerrado con {argumentos.bits} bits; "
          f"{len(cocientes)} cocientes parciales certificados.")
    print("   Primeros cocientes:", cocientes[:24])
    mayor = max(cocientes[1:])
    print(f"   Mayor cociente parcial certificado: {mayor} "
          f"(índice {cocientes.index(mayor)}).")

    # 3. Cotejo independiente con logaritmos decimales de la biblioteca estándar.
    cifras = int(argumentos.bits * 0.30103) + 60
    contexto = decimal.Context(prec=cifras)
    x = contexto.divide(contexto.ln(decimal.Decimal(3)), contexto.ln(decimal.Decimal(2)))
    cuantos = min(len(cocientes), int(0.8 * argumentos.bits * 0.30103))
    decimales = []
    for _ in range(cuantos):
        a = int(x)
        decimales.append(a)
        x = contexto.divide(1, contexto.subtract(x, a))
    iguales = decimales == cocientes[:cuantos]
    print(f"\n3. Cotejo con decimal.ln a {cifras} cifras de los primeros {cuantos} cocientes: "
          f"{'coinciden' if iguales else 'NO COINCIDEN'}.")
    if not iguales:
        raise SystemExit("Discrepancia con el cotejo decimal")

    # 4. Convergentes superiores.
    ln2 = log_dos_inferior()
    lista = convergentes(cocientes)
    comprobados = 0
    exactos = 0
    ultimo = None
    peor_mu = (0.0, None)
    peor_mu_grande = (0.0, None)
    for n, (p, q) in enumerate(lista):
        if n % 2 == 0:
            continue                   # convergente inferior: Lambda < 0
        if q <= argumentos.q_convergente_exacto:
            if not rhin_entera_exacta(p, q):
                raise SystemExit(f"FALLO EXACTO en el convergente n = {n}")
            exactos += 1
        # Cota inferior rigurosa: Lambda >= ln2_inf * (p - q * alto).
        diferencia = p - q * alto
        if diferencia <= 0:
            break                      # el encierro ya no separa: fin de la comprobación
        Lambda_inf = ln2 * diferencia
        if Lambda_inf * p ** 14 < 1:
            raise SystemExit(f"FALLO: convergente n = {n}, p = {p}")
        comprobados += 1
        ultimo = (n, p, q)
        # Exponente aproximado mu = -log(Lambda)/log(p), informativo.
        ld = math.log10(diferencia.numerator) - math.log10(diferencia.denominator)
        mu = -(ld + math.log10(math.log(2))) / math.log10(p) if p > 1 else 0.0
        if mu > peor_mu[0]:
            peor_mu = (mu, n)
        if p >= 1000 and mu > peor_mu_grande[0]:
            peor_mu_grande = (mu, n)
    n, p, q = ultimo
    print(f"\n4. Convergentes superiores comprobados: {comprobados} "
          f"({exactos} también con enteros exactos).")
    print(f"   Último: índice {n}, numerador con {len(str(p))} cifras decimales.")
    print(f"   Mayor exponente mu (Lambda = p^-mu) entre los comprobados: "
          f"{peor_mu[0]:.4f}, en el índice {peor_mu[1]}; con p >= 1000: "
          f"{peor_mu_grande[0]:.4f}, en el índice {peor_mu_grande[1]}.")
    print("   (Rhin da mu <= 13,3; la forma entera necesita mu < 14.)")
    print(f"\nCONCLUSIÓN: RhinEntera vale para todo k <= p_{n}, "
          f"un entero de {len(str(p))} cifras (y para k = 1).")
    print("Más allá, la hipótesis sólo se apoya en Rhin (1987).")


if __name__ == "__main__":
    main()
