"""Cotejo exacto de lo leído en Mahler (1968) y Bernstein (1994).

Máquina de Mahler: g -> 3g/2 si g es par y (3g+1)/2 si es impar. Si a es un
número Z con parte entera g, las partes enteras de a(3/2)^n siguen esa máquina,
y las partes fraccionarias r_n cumplen r_n en [0, 1/3) si g_n es par y
r_n en [1/3, 1/2) si es impar (Mahler, p. 314), con r_n = e_n/3 + (2/3) r_(n+1).
Todo con Fraction o enteros: sin coma flotante.

Comprueba:
1. La tabla de Mahler para G_1 = 13 (p. 317), hasta el corte en H_8 = 100877.
2. Prueba fina de ventana: los r_0 compatibles con las paridades e_0..e_(L-1)
   (y r_L en [0, 1/2)) forman un intervalo [a, b) que se calcula hacia atrás.
   Si queda vacío, no hay número Z en [g, g+1). Esta prueba es más fuerte que
   «ningún g_n deja resto 3 al dividir por 4» (dos impares seguidos).
3. El 13 de Mahler: la prueba fina lo descarta con 11 paridades (153, 230, 345,
   518, 777: impar, par, impar, par, impar); la del resto 3, en g_21 = 67251.
4. Conteo por ventanas: de los 2^L restos de g módulo 2^L, cuántos pasan cada
   prueba. Los que esquivan el resto 3 son números de Fibonacci (la cuenta x^0,7
   de Mahler); los que pasan la prueba fina son menos (Flatto 1992 prueba x^0,59).
5. Bernstein (1994), con el atajo T(x) = x/2 o (3x+1)/2: si d_0 < d_1 < ... son
   los instantes impares, x + suma 2^(d_m)/3^(m+1) = 2^K T^K(x)/3^(S_K), así que
   x = -suma en sentido 2-ádico. En los fantasmas la misma serie converge
   también en los reales, al mismo valor; en el 1 diverge en los reales.

Un barrido finito no prueba nada universal.
Uso:
python -B -X utf8 depuracion/mahler20261007/cotejar_mahler.py
    --largo 28 --pasos 330 --salida depuracion/mahler20261007/cotejo_mahler.json
"""

import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path


def paso_mahler(g):
    if g % 2 == 0:
        return 3 * g // 2
    return (3 * g + 1) // 2


def orbita_mahler(g, pasos):
    valores = [g]
    for _ in range(pasos):
        valores.append(paso_mahler(valores[-1]))
    return valores


def tabla_mahler(G1, filas):
    """Algoritmo de Mahler (p. 317): H = (3G+1)/2, 2^a || H, G' = (3/2)^a H."""
    tabla = []
    G = G1
    for _ in range(filas):
        H = (3 * G + 1) // 2
        a, impar = 0, H
        while impar % 2 == 0:
            impar //= 2
            a += 1
        tabla.append([G, H, a])
        if a == 0:
            break
        G = 3 ** a * impar
    return tabla


def intervalo_fino(paridades):
    """Los r_0 compatibles con las paridades dadas: (a, b) para [a, b), o None."""
    a, b = Fraction(0), Fraction(1, 2)
    for e in reversed(paridades):
        a = Fraction(e, 3) + Fraction(2, 3) * a
        b = Fraction(e, 3) + Fraction(2, 3) * b
        if e == 0:
            a, b = max(a, Fraction(0)), min(b, Fraction(1, 3))
        else:
            a, b = max(a, Fraction(1, 3)), min(b, Fraction(1, 2))
        if a >= b:
            return None
    return a, b


def sin_dos_impares(paridades):
    return all(not (paridades[i] == 1 and paridades[i + 1] == 1)
               for i in range(len(paridades) - 1))


def contar_ventanas(largo):
    """Cuántas palabras de cada largo pasan la prueba fina (búsqueda hacia atrás)."""
    cuentas = [0] * (largo + 1)
    pila = [(0, Fraction(0), Fraction(1, 2))]
    while pila:
        profundidad, a, b = pila.pop()
        cuentas[profundidad] += 1
        if profundidad == largo:
            continue
        for e in (0, 1):
            na = Fraction(e, 3) + Fraction(2, 3) * a
            nb = Fraction(e, 3) + Fraction(2, 3) * b
            if e == 0:
                na, nb = max(na, Fraction(0)), min(nb, Fraction(1, 3))
            else:
                na, nb = max(na, Fraction(1, 3)), min(nb, Fraction(1, 2))
            if na < nb:
                pila.append((profundidad + 1, na, nb))
    return cuentas


def paso(x):
    if x % 2 == 0:
        return x // 2
    return (3 * x + 1) // 2


def suma_bernstein(x, pasos):
    """Suma de 2^(d_m)/3^(m+1) sobre los instantes impares d_m < pasos, y T^pasos(x)."""
    suma, m = Fraction(0), 0
    for d in range(pasos):
        if x % 2 != 0:
            suma += Fraction(2 ** d, 3 ** (m + 1))
            m += 1
        x = paso(x)
    return suma, m, x


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--largo", type=int, required=True)
    analizador.add_argument("--pasos", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    assert 16 <= args.largo <= 34 and 33 <= args.pasos <= 2000

    # 1. La tabla de Mahler para G_1 = 13.
    tabla = tabla_mahler(13, 20)
    assert tabla == [[13, 20, 2], [45, 68, 2], [153, 230, 1], [345, 518, 1],
                     [777, 1166, 1], [1749, 2624, 6], [29889, 44834, 1],
                     [67251, 100877, 0]]

    # 2. La prueba fina implica la del resto 3, y la máquina reparte bien
    #    las paridades: cada palabra de largo L sale de un solo resto módulo 2^L.
    for L in range(1, 17):
        palabras = set()
        for g in range(2 ** L):
            paridades = tuple(v % 2 for v in orbita_mahler(g, L - 1))
            palabras.add(paridades)
            if intervalo_fino(paridades) is not None:
                assert sin_dos_impares(paridades)
        assert len(palabras) == 2 ** L
    patron = [1, 0, 1, 0, 1]
    assert sin_dos_impares(patron) and intervalo_fino(patron) is None
    assert 1 + Fraction(4, 9) + Fraction(16, 81) == Fraction(133, 81) > Fraction(3, 2)

    # 3. El 13 de Mahler, con las dos pruebas.
    orbita = orbita_mahler(13, 30)
    paridades = [v % 2 for v in orbita]
    corte_fino = next(L for L in range(1, 31) if intervalo_fino(paridades[:L]) is None)
    corte_resto3 = next(n for n in range(31) if orbita[n] % 4 == 3)
    assert corte_fino == 11 and orbita[6:11] == [153, 230, 345, 518, 777]
    assert corte_resto3 == 21 and orbita[21] == 67251

    # 4. Conteo por ventanas.
    finos = contar_ventanas(args.largo)
    fibonacci = [1, 2]
    while len(fibonacci) <= args.largo:
        fibonacci.append(fibonacci[-1] + fibonacci[-2])
    sin_resto3 = []
    for L in range(args.largo + 1):
        a, b = 1, 0  # palabras de largo L sin «11», según terminen en 0 o en 1
        for _ in range(L):
            a, b = a + b, a
        sin_resto3.append(a + b)
        assert sin_resto3[L] == fibonacci[L]
        assert finos[L] <= sin_resto3[L]
    for L in range(1, 17):
        directos = sum(1 for g in range(2 ** L)
                       if intervalo_fino([v % 2 for v in orbita_mahler(g, L - 1)]) is not None)
        assert directos == finos[L]
    L = args.largo
    crecimiento = {
        "largo": L,
        "fino": finos[L],
        "sin_resto3": sin_resto3[L],
        "exponente_fino_aprox": "%.4f" % (math.log2(finos[L]) / L),
        "exponente_sin_resto3_aprox": "%.4f" % (math.log2(sin_resto3[L]) / L),
        "referencias": {"log2(3/2)": "%.4f" % math.log2(1.5),
                        "log2(razon_aurea)": "%.4f" % math.log2((1 + 5 ** 0.5) / 2)},
    }

    # 5. Bernstein: x + suma = 2^K T^K(x) / 3^(S_K), en semillas positivas y negativas.
    semillas = [1, 3, 7, 27, 97, 871, 2 ** 20 - 1, -1, -5, -7, -10, -17]
    cuentas_bernstein = 0
    for x in semillas:
        suma, impares, actual = Fraction(0), 0, x
        for K in range(args.pasos + 1):
            assert x + suma == Fraction(2 ** K * actual, 3 ** impares)
            assert (x + suma).numerator % (2 ** K) == 0
            cuentas_bernstein += 1
            if actual % 2 != 0:
                suma += Fraction(2 ** K, 3 ** (impares + 1))
                impares += 1
            actual = paso(actual)
        assert (suma, impares, actual) == suma_bernstein(x, args.pasos + 1)
    # Fantasmas: la cola es |x| r^m con r = 2^p/3^q; r < 1 en los reales y
    # 2 divide a su numerador, así que la serie tiende a |x| con las dos reglas.
    circuitos = {-1: (1, 1), -5: (3, 2), -17: (11, 7)}
    cuentas_fantasmas = 0
    for x, (p, q) in circuitos.items():
        r = Fraction(2 ** p, 3 ** q)
        assert r < 1 and r.numerator % 2 == 0
        for m in range(args.pasos // p + 1):
            suma, _, _ = suma_bernstein(x, p * m)
            assert suma == -x * (1 - r ** m)
            cuentas_fantasmas += 1
    # El 1 (circuito 1 -> 2 -> 1): la suma es (4/3)^m - 1; diverge en los reales
    # y tiende a -1 en sentido 2-ádico, de modo que x = -(-1) = 1.
    for m in range(args.pasos // 2 + 1):
        suma, _, _ = suma_bernstein(1, 2 * m)
        assert suma == Fraction(4, 3) ** m - 1
        cuentas_fantasmas += 1

    evidencia = {
        "estado": "cotejo exacto terminado",
        "sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "parametros": {"largo": args.largo, "pasos": args.pasos},
        "tabla_mahler_13": tabla,
        "trece": {"orbita_hasta_21": orbita[:22], "corte_prueba_fina": corte_fino,
                  "corte_resto_3": corte_resto3},
        "ventanas": {"fino": finos, "sin_resto3": sin_resto3},
        "crecimiento": crecimiento,
        "cuentas": {"identidades_bernstein": cuentas_bernstein,
                    "valores_fantasmas": cuentas_fantasmas},
        "alcance": "Cotejo exacto en ventanas finitas. Confirma la tabla de Mahler, que la "
                   "prueba del resto 3 es necesaria pero no suficiente en cada ventana, y la "
                   "formula de Bernstein en tramos finitos. Los exponentes son medidas de "
                   "ventana, no teoremas; el de Flatto (1992) es un teorema suyo.",
    }
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(json.dumps(evidencia, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps(evidencia["trece"], ensure_ascii=False))
    print(json.dumps(crecimiento, ensure_ascii=False))
    print(json.dumps(evidencia["cuentas"], ensure_ascii=False))


if __name__ == "__main__":
    main()
