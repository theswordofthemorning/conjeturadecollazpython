"""Estratos de fusi?n por la cadena (k,c), con contabilidad exacta de canales.

Correcci?n 13-09-2026: las b?squedas s?lo prueban ajustes de P(N)+C(N mod p)
sobre datos finitos; no excluyen cuasipolinomios generales ni f?rmulas futuras.
El c?lculo directo independiente est? en ../zootheorem/verify/verify_strata.py.
Importar este m?dulo no ejecuta barridos. El nivel 29 requiere pedirlo.
"""

import argparse
from fractions import Fraction

M_TOPE = 13
TOPE_ESTADOS = 2_000_000

def transicion(k, c, bit):
    if k == 0:
        if c % 2 == 0:
            return ('estado', 0, c // 2) if bit == 0 else ('estado', 0, 3 * c // 2)
        return ('estado', 1, (3 * c + 1) // 2) if bit == 0 \
            else ('estado', 1, (1 - 3 * c) // 2)
    if c % 2 == 0:
        return ('estado', k, c // 2) if bit == 0 \
            else ('estado', k, (3 * c + 1 - 3 ** k) // 2)
    if bit == 0:
        return ('estado', k + 1, (3 * c + 1) // 2)
    if k >= 2:
        return ('estado', k - 1, (c - 3 ** (k - 1)) // 2)
    g = (c - 1) // 2
    if g == 0:
        return ('fusion',)
    return ('estado', 0, abs(g))


def barrido_estratos(inicio, prof, m_inicial=0):
    # devuelve nuevas[prof][m] = palabras absorbidas en el paso prof
    # con m mixtos (el paso de la fusion cuenta como mixto, c impar)
    estados = {(inicio[0], inicio[1], m_inicial): 1}
    nuevas = {}
    for t in range(1, prof + 1):
        nuevo = {}
        for (k, c, m), n in estados.items():
            m2 = min(m + (c % 2 != 0), M_TOPE + 1)
            for bit in (0, 1):
                s = transicion(k, c, bit)
                if s[0] == 'fusion':
                    nuevas.setdefault(t, {})
                    nuevas[t][m2] = nuevas[t].get(m2, 0) + n
                else:
                    clave = (s[1], s[2], m2)
                    nuevo[clave] = nuevo.get(clave, 0) + n
        estados = nuevo
        if len(estados) > TOPE_ESTADOS:
            raise RuntimeError("Barrido incompleto: nivel %d, %d estados; limite %d"
                               % (t, len(estados), TOPE_ESTADOS))
    return nuevas, prof


def ajustar_polinomio_periodico(serie, n0, grado, periodo, arranque):
    # ajusta con los primeros nvar puntos desde 'arranque' y exige la
    # igualdad EXACTA en la cola finita; None si no ajusta.
    # Esta familia P(N)+C(N mod p) NO son todos los cuasipolinomios.
    nvar = grado + 1 + periodo - 1
    puntos = serie[arranque:]
    if len(puntos) < nvar + 6:
        raise ValueError("Datos insuficientes para ajuste y seis controles")
    A = []
    for i in range(nvar):
        N = n0 + arranque + i
        fila = [Fraction(N) ** g for g in range(grado + 1)]
        fila += [Fraction(1 if N % periodo == r else 0)
                 for r in range(1, periodo)]
        fila.append(Fraction(puntos[i]))
        A.append(fila)
    m = nvar
    fila_p = 0
    for col in range(m):
        piv = next((r for r in range(fila_p, len(A)) if A[r][col] != 0), None)
        if piv is None:
            continue
        A[fila_p], A[piv] = A[piv], A[fila_p]
        pv = A[fila_p][col]
        A[fila_p] = [x / pv for x in A[fila_p]]
        for r in range(len(A)):
            if r != fila_p and A[r][col] != 0:
                f = A[r][col]
                A[r] = [a - f * b for a, b in zip(A[r], A[fila_p])]
        fila_p += 1
    sol = [Fraction(0)] * m
    for r in range(fila_p):
        col = next((c for c in range(m) if A[r][c] == 1), None)
        if col is not None:
            sol[col] = A[r][m]
    for i, v in enumerate(puntos):
        N = n0 + arranque + i
        w = sum(sol[g] * N ** g for g in range(grado + 1))
        if N % periodo != 0:
            w += sol[grado + 1 + (N % periodo) - 1]
        if w != v:
            return None
    return sol

def buscar_forma(serie):
    probados = omitidos = 0
    halladas = []
    for grado in range(1, 9):
        for periodo in range(1, 9):
            for arranque in range(7):
                if len(serie[arranque:]) < grado + periodo + 6:
                    omitidos += 1
                    continue
                probados += 1
                sol = ajustar_polinomio_periodico(serie, 10, grado, periodo, arranque)
                if sol is not None:
                    halladas.append((grado, periodo, 10 + arranque, sol))
    return halladas, probados, omitidos


def main():
    global TOPE_ESTADOS
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prof', type=int, default=20, choices=range(3, 30), metavar='3..29')
    parser.add_argument('--tope-estados', type=int, default=TOPE_ESTADOS)
    args = parser.parse_args()
    if args.tope_estados < 1:
        parser.error('--tope-estados debe ser positivo')
    TOPE_ESTADOS = args.tope_estados
    prof = args.prof
    print('Barridos simbolicos hasta nivel', prof, flush=True)
    ppal, _ = barrido_estratos((0, 1), prof)
    piso, prof_h = barrido_estratos((2, -1), prof - 2, m_inicial=2)
    par, prof_p = barrido_estratos((1, 2), prof - 1, m_inicial=1)
    for n in range(3, prof + 1):
        datos = ppal.get(n, {})
        assert datos.get(2, 0) == 1, ('e2', n)
        if n >= 5:
            assert datos.get(4, 0) == 1, ('e4', n)
        if n >= 10:
            assert datos.get(6, 0) == 3 + (n - 7) * (n - 8) // 2, ('e6', n)
        for k in range(2, 13, 2):
            assert datos.get(k, 0) == (ppal.get(n - 2, {}).get(k - 2, 0)
                                     + piso.get(n - 2, {}).get(k, 0)
                                     + par.get(n - 1, {}).get(k, 0)), ('canales', n, k)
    print('OK: estratos inferiores y contabilidad de los tres canales en el rango calculado.')
    print('n e6 e8 e10 e12')
    for n in range(1, prof + 1):
        print(n, *(ppal.get(n, {}).get(k, 0) for k in (6, 8, 10, 12)))
    for n in range(13, prof_h + 1):
        numerador = 4*n*n - 76*n + 384 - 2*(n % 3 == 2)
        assert numerador % 3 == 0 and piso.get(n, {}).get(8, 0) == numerador // 3
    print('Formula propuesta de e8 del piso h: comprobada solo en 13..%d.' % prof_h)
    coleccion = [(f'e{k}', ppal, prof, k) for k in (6, 8, 10, 12)]
    coleccion += [(f'h_e{k}', piso, prof_h, k) for k in (10, 12)]
    coleccion += [(f'par_e{k}', par, prof_p, k) for k in (8, 10, 12)]
    for nombre, tabla, limite, k in coleccion:
        serie = [tabla.get(n, {}).get(k, 0) for n in range(10, limite + 1)]
        formas, probados, omitidos = buscar_forma(serie)
        print(f'{nombre}: {probados} modelos probados, {omitidos} omitidos por falta de datos; '
              f'{len(formas)} ajustes exactos en la cola finita.')
        if nombre == 'e6' and prof >= 18:
            assert any(g == 2 and p == 1 and n == 10 for g, p, n, _ in formas)
        if formas:
            print('  Primer ajuste (grado, periodo, inicio, coeficientes):', formas[0])
    print('La busqueda restringida no excluye cuasipolinomios generales ni leyes asintoticas.')


if __name__ == '__main__':
    main()
