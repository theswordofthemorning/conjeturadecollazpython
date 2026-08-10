# pumasescalera.py
#
# EL SEPTIMO ESCALON DEL ACORRALADO DE PUMAS (09-08-2026, noche).
# La escalera de truncados de retornoslambda.py C3 / matriztransferencia
# daba lambda >= 1.9754 con seis escalones anidados (el ultimo:
# K = 11, |c| <= 12288). Este fichero:
#
#   1. RE-COMPUTA los seis escalones publicados con una implementacion
#      mas rapida (tabla de sucesores precomputada, conteo ENTERO de
#      caminos de fusion -- ni un float en la cadena que decide: los
#      floats aparecen solo al formar la razon final), y exige que
#      coincidan con lo publicado y que la escalera sea MONOTONA
#      (menores anidados);
#   2. COMPUTA EL ESCALON 7, nunca corrido: K = 13, |c| <= 49152
#      (313.672 estados). Resultado (09-08-2026):
#
#          lambda_T = 1.980748   ==>   LAMBDA >= 1.9807
#
#      (antes 1.9754), con la razon PLANA de t = 240 a t = 420 y el
#      gap 2 - lambda_T pasando de 0.024553 a 0.019252 (razon de gaps
#      ~0.78: el patron x0.5-0.75 del acorralado, apenas por encima --
#      el gap se resiste, como corresponde si lambda = 2).
#
#   RECORDATORIO DE LOBAS (el techo de este metodo): ningun truncado
#   finito puede demostrar lambda < 2 (la libertad de la torre), y por
#   ZORRAS lambda < 2 implicaria phi = 1. La escalera solo puede subir:
#   cada escalon es una cota inferior DEMOSTRADA nueva.
#
#   Mapa del ATAJO via la cadena de Leonas; SystemExit antes de concluir.

import time

# (K, C, lambda publicada o None si es nuevo); los seis primeros son
# la escalera de retornoslambda.py, el septimo es el de este fichero
ESCALERA = [
    (2, 12, 1.7400),
    (3, 48, 1.8667),
    (5, 192, 1.9336),
    (7, 768, 1.9556),
    (9, 3072, 1.9675),
    (11, 12288, 1.97545),
    (13, 49152, None),
]
PASOS = 420
TOLERANCIA = 5e-4          # contra lo publicado (que se dio con 4-5 cifras)


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


def escalon(K, C, pasos=PASOS):
    # cierre alcanzable desde (0,1) dentro de la caja, tabla de
    # sucesores por indice, y conteo entero de caminos de fusion
    inicio = (0, 1)
    estados = {inicio}
    frontera = [inicio]
    while frontera:
        k, c = frontera.pop()
        for bit in (0, 1):
            s = transicion(k, c, bit)
            if s[0] == 'fusion':
                continue
            k2, c2 = s[1], s[2]
            if k2 <= K and abs(c2) <= C and (k2, c2) not in estados:
                estados.add((k2, c2))
                frontera.append((k2, c2))
    indice = {s: i for i, s in enumerate(sorted(estados))}
    n = len(indice)
    FUSION, FUERA = -1, -2
    suc = [[FUERA, FUERA] for _ in range(n)]
    for s, i in indice.items():
        for bit in (0, 1):
            t = transicion(s[0], s[1], bit)
            if t[0] == 'fusion':
                suc[i][bit] = FUSION
            elif t[1] <= K and abs(t[2]) <= C:
                suc[i][bit] = indice[(t[1], t[2])]

    v = [0] * n
    v[indice[inicio]] = 1
    fus = 0
    razones = []
    for _ in range(pasos):
        nuevo = [0] * n
        fus_nueva = 0
        for i in range(n):
            ni = v[i]
            if ni:
                a, b = suc[i]
                if a == FUSION:
                    fus_nueva += ni
                elif a >= 0:
                    nuevo[a] += ni
                if b == FUSION:
                    fus_nueva += ni
                elif b >= 0:
                    nuevo[b] += ni
        v = nuevo
        if fus and fus_nueva:
            razones.append(fus_nueva / fus)
        fus = fus_nueva
    cola = razones[-40:]
    return n, min(cola), max(cola)


print("la escalera de PUMAS, re-computada entera + el escalon 7:")
print("  K     C       estados    lambda_T      gap 2-lambda_T")
anterior = 0.0
gaps = []
resultados = []
for (K, C, publicada) in ESCALERA:
    t0 = time.time()
    n, lo, hi = escalon(K, C)
    if hi - lo > 1e-6:
        raise SystemExit("escalon (%d, %d): la razon no convergio "
                         "([%f, %f])" % (K, C, lo, hi))
    if publicada is not None and abs(lo - publicada) > TOLERANCIA:
        raise SystemExit("escalon (%d, %d): %f no coincide con lo "
                         "publicado %f" % (K, C, lo, publicada))
    if lo <= anterior:
        raise SystemExit("la escalera dejo de ser monotona en (%d, %d)"
                         % (K, C))
    anterior = lo
    gaps.append(2 - lo)
    resultados.append((K, C, n, lo))
    print("  %2d  %6d     %7d    %.6f      %.6f    (%.0f s)"
          % (K, C, n, lo, 2 - lo, time.time() - t0))

print()
print("razones de gaps consecutivos:",
      ["%.3f" % (gaps[i + 1] / gaps[i]) for i in range(len(gaps) - 1)])
print()
print("VEREDICTO: los seis escalones publicados REPRODUCIDOS (monotonia y")
print("valores), y el septimo es nuevo:")
print("  LAMBDA >= %.6f    (K = 13, |c| <= 49152, %d estados)"
      % (resultados[-1][3], resultados[-1][2]))
print("El gap sigue achicandose (~x0.78 este escalon) sin senal de piso:")
print("consistente con lambda = 2 (el paseo critico), que es lo que LOBAS")
print("dice que ningun truncado puede refutar. La cota DEMOSTRADA de PUMAS")
print("queda en lambda >= 1.9807.")
