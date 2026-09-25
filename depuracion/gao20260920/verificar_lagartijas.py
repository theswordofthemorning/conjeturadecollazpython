"""Contraste independiente de Lagartijas en parámetros pequeños.

Reimplementa la transición absorbente de `cadena_completa.lean` y calcula
por enumeración directa de palabras (no con las recursiones de la prueba):

  A  inclusión: vivo en h y menos de N entradas guardadas implica cruce de
     magnitud U o un hueco de edad >= G (con i < N), para todas las palabras;
  B  P(A) <= P(C1) + (N-1)(eps+beta) + beta con eps = max surv(d, c);
  C  frontera: riesgo de hueco r pasos <= peso(z)/theta^r;
  D  excursión: riesgo desde (2,c) en d+B+1 pasos <= surv(d,c) + 2/theta^B.

Todo con Fraction. Los parámetros cumplen las hipótesis del teorema
abstracto `pocas_entradas_abstracta`, no las de m>=10 (horizontes enormes).
Uso: python -B -X utf8 verificar_lagartijas.py [--h 16]
"""

import argparse
import json
from fractions import Fraction
from itertools import product
from pathlib import Path

FUSION = None


def paso(z, b):
    if z is FUSION:
        return FUSION
    k, c = z
    if k == 0:
        if c % 2 == 0:
            return (0, 3 * c // 2 if b else c // 2)
        return (1, (1 - 3 * c) // 2 if b else (3 * c + 1) // 2)
    if c % 2 == 0:
        return (k, (3 * c + 1 - 3 ** k) // 2 if b else c // 2)
    if b:
        if k == 1:
            return FUSION if c == 1 else (0, abs((c - 1) // 2))
        return (k - 1, (c - 3 ** (k - 1)) // 2)
    return (k + 1, (3 * c + 1) // 2)


def tamano(z):
    return Fraction(0) if z is FUSION else Fraction(abs(z[1]), 3 ** z[0])


def entrada(z, w):
    return z is not FUSION and w is not FUSION and z[0] == 1 and w[0] == 2


def guardado(z, w, C):
    """La posición de w, alcanzada desde z, es admisible."""
    return entrada(z, w) and abs(w[1]) <= C


def recorrido(z, bs):
    estados = [z]
    for b in bs:
        z = paso(z, b)
        estados.append(z)
    return estados


def palabras(n):
    return product((False, True), repeat=n)


def riesgo_bruto(z, n, C, U):
    """Fracción de palabras de n bits sin entrada guardada, vivas y con tamano<=U."""
    if z is FUSION or tamano(z) > U:
        return Fraction(0)
    buenas = 0
    for bs in palabras(n):
        w, ok = z, True
        for b in bs:
            w2 = paso(w, b)
            if guardado(w, w2, C) or w2 is FUSION or tamano(w2) > U:
                ok = False
                break
            w = w2
        buenas += ok
    return Fraction(buenas, 2 ** n)


def surv_bruto(c, d):
    """Fracción de palabras de d bits en que la excursión desde (2,c) sigue en k>=2."""
    buenas = 0
    for bs in palabras(d):
        w = (2, c)
        for b in bs:
            w = paso(w, b)
            if w[0] < 2:
                break
        buenas += w[0] >= 2
    return Fraction(buenas, 2 ** d)


def riesgo_dp(z, n, C, U):
    """Lo mismo que riesgo_bruto, propagando la distribución de estados."""
    if z is FUSION or tamano(z) > U:
        return Fraction(0)
    dist = {z: 1}
    for _ in range(n):
        nueva = {}
        for w, p in dist.items():
            for b in (False, True):
                w2 = paso(w, b)
                if guardado(w, w2, C) or w2 is FUSION or tamano(w2) > U:
                    continue
                nueva[w2] = nueva.get(w2, 0) + p
        dist = nueva
    return Fraction(sum(dist.values()), 2 ** n)


def surv_dp(c, d):
    dist = {(2, c): 1}
    for _ in range(d):
        nueva = {}
        for w, p in dist.items():
            for b in (False, True):
                w2 = paso(w, b)
                if w2[0] >= 2:
                    nueva[w2] = nueva.get(w2, 0) + p
        dist = nueva
    return Fraction(sum(dist.values()), 2 ** d)


def v2(c):
    c, v = abs(c), 0
    while c and c % 2 == 0:
        c //= 2
        v += 1
    return v


def peso(z, theta, V):
    k, c = z
    if k == 0:
        return 2 * theta ** (v2(c) + 1)
    return Fraction(2) if c % 2 == 0 else theta ** (V + 2)


def main(h=16):
    V, N, d, B = 2, 2, 4, 3
    U = Fraction(2 ** V)
    C = 9 * 2 ** V
    theta = 1 + Fraction(1, 4 * (V + 3))
    G = d + B + 1
    assert N * G <= h and theta ** (V + 3) <= 4 - 2 * theta and 9 * U <= C
    beta = 2 / theta ** B
    salida = {'parametros': dict(V=V, N=N, d=d, B=B, G=G, h=h, U=str(U), C=C,
                                 theta=str(theta))}

    # A y B: enumeración de todas las palabras de longitud h
    malas = cruces = objetivos = violaciones = 0
    for bs in palabras(h):
        est = recorrido((0, 1), bs)
        vivo = est[-1] is not FUSION
        guard = [False] + [guardado(est[t], est[t + 1], C) for t in range(h)]
        K = sum(guard)
        c1 = any(tamano(z) > U for z in est)
        i, a, obj = 0, 0, False
        for t in range(h + 1):
            if t > 0:
                if guard[t]:
                    i, a = i + 1, 0
                else:
                    a += 1
            if est[t] is not FUSION and i < N and a >= G and \
                    all(tamano(z) <= U for z in est[:t + 1]):
                obj = True
        if vivo and K < N:
            malas += 1
            violaciones += not (c1 or obj)
        cruces += c1
        objetivos += obj and not c1
    total = 2 ** h
    eps = max(surv_bruto(c, d) for c in range(-C, C + 1))
    cota = Fraction(cruces, total) + Fraction(objetivos, total)
    potencial = (N - 1) * (eps + beta) + beta
    salida['A'] = dict(palabras=total, vivas_pocas=malas, sin_explicar=violaciones)
    salida['B'] = dict(P_A=str(Fraction(malas, total)), P_C1=str(Fraction(cruces, total)),
                       P_obj_sin_C1=str(Fraction(objetivos, total)),
                       eps=str(eps), beta=str(beta),
                       cota=str(Fraction(cruces, total) + potencial),
                       ok=Fraction(malas, total) <= cota <= Fraction(cruces, total) + potencial)

    # C: frontera en estados k=1 y k=0 con c != 0 y tamano <= U
    comparaciones = fallos = 0
    for z in [(1, c) for c in range(-12, 13)] + [(0, c) for c in range(-8, 9) if c]:
        if tamano(z) > U:
            continue
        for r in range(0, 11):
            comparaciones += 1
            fallos += riesgo_bruto(z, r, C, U) > peso(z, theta, V) / theta ** r
    salida['C'] = dict(comparaciones=comparaciones, fallos=fallos)

    # D: excursión desde (2,c), |c| <= C
    comp_d = fallos_d = 0
    for c in range(-C, C + 1):
        if tamano((2, c)) > U:
            continue
        comp_d += 1
        fallos_d += riesgo_bruto((2, c), d + B + 1, C, U) > surv_bruto(c, d) + beta
    salida['D'] = dict(comparaciones=comp_d, fallos=fallos_d)

    # A2: otro juego para la inclusión (N=3, G=5)
    N2, G2, h2 = 3, 5, 15
    malas2 = sin2 = 0
    for bs in palabras(h2):
        est = recorrido((0, 1), bs)
        guard = [False] + [guardado(est[t], est[t + 1], C) for t in range(h2)]
        if est[-1] is FUSION or sum(guard) >= N2:
            continue
        malas2 += 1
        c1 = any(tamano(z) > U for z in est)
        i, a, obj = 0, 0, False
        for t in range(h2 + 1):
            if t > 0:
                i, a = (i + 1, 0) if guard[t] else (i, a + 1)
            if i < N2 and a >= G2 and all(tamano(z) <= U for z in est[:t + 1]):
                obj = True
        sin2 += not (c1 or obj)
    salida['A2'] = dict(N=N2, G=G2, h=h2, vivas_pocas=malas2, sin_explicar=sin2)

    # C2 y D2: régimen no trivial (cota < 1), V=0, por distribución exacta
    V1 = 0
    U1, C1b, th1 = Fraction(1), 9, 1 + Fraction(1, 4 * (V1 + 3))
    assert th1 ** (V1 + 3) <= 4 - 2 * th1
    comp2 = fallos2 = no_triv2 = 0
    for z in [(1, c) for c in range(-3, 4)] + [(0, 1), (0, -1)]:
        for r in range(0, 121, 8):
            cota = peso(z, th1, V1) / th1 ** r
            comp2 += 1
            no_triv2 += cota < 1
            fallos2 += riesgo_dp(z, r, C1b, U1) > cota
    salida['C2'] = dict(V=V1, comparaciones=comp2, no_triviales=no_triv2, fallos=fallos2)
    d1, B1 = 8, 20
    beta1 = 2 / th1 ** B1
    comp3 = fallos3 = no_triv3 = 0
    peor = Fraction(0)
    for c in range(-C1b, C1b + 1):
        if tamano((2, c)) > U1:
            continue
        izq = riesgo_dp((2, c), d1 + B1 + 1, C1b, U1)
        der = surv_dp(c, d1) + beta1
        comp3 += 1
        no_triv3 += der < 1
        fallos3 += izq > der
        peor = max(peor, izq / der)
    salida['D2'] = dict(d=d1, B=B1, beta=float(beta1), comparaciones=comp3,
                        no_triviales=no_triv3, fallos=fallos3, max_cociente=float(peor))
    print(json.dumps(salida, ensure_ascii=False, indent=2))
    ok = (violaciones == 0 and sin2 == 0 and salida['B']['ok'] and fallos == 0 and fallos_d == 0
          and fallos2 == 0 and fallos3 == 0)
    print('OK' if ok else 'FALLO')
    Path(__file__).with_name('evidencia_lagartijas_exacta.json').write_text(
        json.dumps(salida, ensure_ascii=False, indent=2, default=str) + '\n', encoding='utf-8')
    return ok


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--h', type=int, default=16)
    raise SystemExit(0 if main(p.parse_args().h) else 1)
