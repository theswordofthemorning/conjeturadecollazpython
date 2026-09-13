"""Subrenovación de c: multiplicadores y puertas con signo; bandas finitas.

Las identidades del multiplicador son en magnitud. En el núcleo y la
frontera par las dos magnitudes son 1/2 y 3/2; en la frontera impar son
ambas 3/2. La moneda de primer momento uno no identifica una perpetuidad
iid ni establece cola estacionaria 1/x: el desplazamiento depende del estado.

Las dos puertas firmadas desde un gap impar son (3g+1)/2 y (1-3g)/2,
ambas 2 módulo 3. El invariante no divisibilidad por 3 está en cabras.lean.
La posterior absorción desde (1,1) no pertenece exclusivamente a una puerta.
Corrección 13-09-2026; las interpretaciones anteriores quedan en Git y en
el registro de afirmaciones. Esta ejecución sólo mide tiempos finitos.
"""

PROF = 20
TOPE_ESTADOS = 9 * 10 ** 6


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


# ---------------------------------------------------------------------------
# T1: el multiplicador de cada transicion, verificado sobre una rejilla
#     amplia: en el nucleo, {m de bit 0, m de bit 1} = {1/2, 3/2} SIEMPRE;
#     en la frontera par tambien; en la frontera impar {3/2, 3/2}.
#     (m se lee comparando c' para dos valores de c de la misma clase:
#     m = (c2' - c1') / (c2 - c1), con paridades iguales.)
# ---------------------------------------------------------------------------

def multiplicador(k, c, bit):
    # dos representantes de la misma paridad y clase mod 3; la salida a
    # frontera lleva un valor absoluto (lineal A TROZOS con pliegue en
    # c = 1), asi que se prueban ambos lados y vale el que no cruce
    for delta in (6, -6):
        c2 = c + delta
        s1 = transicion(k, c, bit)
        s2 = transicion(k, c2, bit)
        if s1[0] == 'fusion' or s2[0] == 'fusion':
            return None
        if s1[1] != s2[1]:
            return None           # niveles distintos: no comparable
        num, den = s2[2] - s1[2], c2 - c
        if abs(2 * num) in (abs(den), 3 * abs(den)):
            return (num, den)
    return (num, den)             # devuelve el ultimo: fallara el test


def main():
    global PROF, TOPE_ESTADOS
    import argparse
    parser = argparse.ArgumentParser(description='Subrenovación: controles y bandas finitas')
    parser.add_argument('--prof', type=int, default=20)
    parser.add_argument('--tope-estados', type=int, default=2_000_000)
    args = parser.parse_args()
    if not 3 <= args.prof <= 34 or args.tope_estados < 1:
        parser.error('Se exige 3<=prof<=34 y tope positivo')
    PROF, TOPE_ESTADOS = args.prof, args.tope_estados
    probadas = 0
    for k in range(0, 9):
        for c in range(1 if k == 0 else -80, 81):
            if k == 0 and c < 1:
                continue
            ms = set()
            for bit in (0, 1):
                m = multiplicador(k, c, bit)
                if m is not None:
                    ms.add(abs((2 * m[0]) // m[1]))   # |2m|: 1 <-> 1/2, 3 <-> 3/2
            if k == 0 and c % 2 == 1:
                # la bomba de reentrada: ambas ramas |m| = 3/2 (el bit 1 con
                # signo negativo -- el vuelco -- pero magnitud 3/2)
                if ms and ms != {3}:
                    raise SystemExit("T1 frontera impar: k=%d c=%d ms=%s"
                                     % (k, c, ms))
            elif len(ms) == 2 and ms != {1, 3}:
                raise SystemExit("T1: k=%d c=%d ms=%s" % (k, c, ms))
            probadas += 1

    print("T1 OK -- EL TEOREMA DEL MULTIPLICADOR: en el nucleo y la frontera")
    print("par, cada paso es moneda justa entre m = 1/2 y m = 3/2 (E[m] = 1")
    print("EXACTO, E[log2 m] = %.4f < 0): identidad del multiplicador"
          % ((3).bit_length() and __import__('math').log2(3) / 2 - 1))
    print("en magnitud; no identifica una perpetuidad iid. La frontera impar")
    print("(ambas ramas m = 3/2): la bomba de reentrada. %d estados probados."
          % probadas)

    # ---------------------------------------------------------------------------
    # T2: la cola de |c|, en bandas diadicas exactas (t = PROF y t = PROF-2,
    #     regla 4x: dos profundidades, dos poblaciones)
    # ---------------------------------------------------------------------------

    import math

    estados = {(0, 1): 1}
    fotos = {}
    for t in range(1, PROF + 1):
        nuevo = {}
        for (k, c), n in estados.items():
            for bit in (0, 1):
                s = transicion(k, c, bit)
                if s[0] == 'fusion':
                    continue
                clave = (s[1], s[2])
                nuevo[clave] = nuevo.get(clave, 0) + n
        estados = nuevo
        if len(estados) > TOPE_ESTADOS:
            raise RuntimeError("Barrido incompleto en t=%d: límite de estados" % t)
        if t in (PROF - 2, PROF):
            fotos[t] = dict(estados)

    for t, foto in sorted(fotos.items()):
        print()
        print("T2: bandas diadicas de |c| a t = %d (masa; cociente banda/banda):" % t)
        for etiqueta, filtro in (("k = 1 solo", lambda k: k == 1),
                                 ("nucleo entero (k >= 1)", lambda k: k >= 1)):
            bandas = {}
            for (k, c), n in foto.items():
                if filtro(k) and c != 0:
                    j = max(0, int(math.log2(abs(c))))
                    bandas[j] = bandas.get(j, 0) + n
            total = sum(bandas.values())
            print("  %s:" % etiqueta)
            prev = None
            for j in sorted(bandas):
                if j > 14:
                    break
                frac = bandas[j] / total
                coc = ("%.4f" % (bandas[j] / prev)) if prev else "      "
                print("    2^%2d <= |c| < 2^%2d :  %.6f   %s"
                      % (j, j + 1, frac, coc))
                prev = bandas[j]

    print()
    print("T2: cocientes de bandas a tiempos finitos, sin conclusión asintótica.")

    # ---------------------------------------------------------------------------
    # T3: las leyes mod 3, exhaustivas sobre la foto final + algebraicas
    # ---------------------------------------------------------------------------

    # (a) conservar el signo del hijo de cada puerta, incluido g=1.
    for g in range(1, 4001, 2):
        for bit in (0, 1):
            hijo = transicion(0, g, bit)
            esperado = (3*g+1)//2 if bit == 0 else (1-3*g)//2
            assert hijo == ('estado', 1, esperado) and esperado % 3 == 2
    # (b) c = 0 (mod 3) inalcanzable en el nucleo: sobre la foto final
    malos = [(k, c) for (k, c) in fotos[PROF] if k >= 1 and c % 3 == 0]
    if malos:
        raise SystemExit("T3b: estados del nucleo con 3 | c: %s" % malos[:5])
    # (c) la absorcion es (1,1) y 1 = 1 (mod 3)
    if transicion(1, 1, 1)[0] != 'fusion':
        raise SystemExit("T3c")

    print()
    print("T3 OK: ambas puertas dan c firmado = 2 mod 3; c divisible por 3")
    print("no aparece en el núcleo a t=%d. La absorción requiere (1,1)." % PROF)
    assert transicion(0, 1, 0) == ('estado', 1, 2)
    assert transicion(1, 2, 0) == ('estado', 1, 1)
    assert transicion(1, 1, 1) == ('fusion',)
    print("La puerta directa también puede fundir: bits 0,0,1 desde (0,1).")
    print()
    print("ALCANCE: T1 y T3 son controles exactos finitos de identidades escritas.")
    print("T2 son bandas a tiempos finitos; no establecen una cola estacionaria.")
    print("No se concluyen tensión condicionada, piso de absorción ni phi=1.")


if __name__ == "__main__":
    main()
