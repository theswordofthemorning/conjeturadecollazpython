"""Lagartijas con pares reales (n, n+1) bajo el mapa atajo T.

Para cada n en [2^K, 2^(K+1)) se siguen las dos trayectorias enteras y sus
conteos impares P, Q. Orientación canónica: ancla = la de menos pasos impares
y, si empatan, la menor. Entonces k=|P-Q| y c = otro - 3^k*ancla. Se coteja:

  1  en cada t<=K, el estado de la cadena alimentada con la paridad del ancla
     real coincide con (k,c); la fusión de la cadena equivale a X=Y con P=Q;
  2  las palabras de K bits de ancla recorren {0,1}^K exactamente una vez
     (transporte a clases módulo 2^K);
  3  el número de n fusionados hasta t es 2^K * P(fusión hasta t) de la cadena,
     calculada aparte por distribución exacta de estados (la cadena cuenta
     palabras de t bits: se escala por 2^(K-t));
  4  la inclusión de Lagartijas sobre pares reales: vivo en h y menos de N
     entradas guardadas implica cruce de magnitud U o hueco de edad >= G;
  5  periodicidad (canon_modulo): el estado a tiempo K de n y de n mod 2^K coincide;
  6  fusion_clasica: si la cadena fusiona en t, el mapa clásico f encuentra
     n y n+1 en k = t + P_t <= 2t pasos.

Uso: python -B -X utf8 verificar_lagartijas_pares.py [--K 18]
"""

import argparse
import json
from fractions import Fraction
from pathlib import Path

from verificar_lagartijas import FUSION, paso, tamano, guardado


def T(x):
    return x // 2 if x % 2 == 0 else (3 * x + 1) // 2


def collatz(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1


def estado_final(n, K):
    X, Y, P, Q = n, n + 1, 0, 0
    for _ in range(K):
        P, X = P + X % 2, T(X)
        Q, Y = Q + Y % 2, T(Y)
    return canonico(X, Y, P, Q)[0]


def canonico(X, Y, P, Q):
    if P == Q and X == Y:
        return FUSION, X
    if P < Q or (P == Q and X < Y):
        ancla, otro, k = X, Y, Q - P
    else:
        ancla, otro, k = Y, X, P - Q
    return (k, otro - 3 ** k * ancla), ancla


def fusion_cadena(K):
    """Pesos enteros: número de palabras de t bits que han fusionado, t=0..K."""
    dist, fusionadas = {(0, 1): 1}, [0]
    for t in range(1, K + 1):
        nueva, f = {}, 0
        for w, p in dist.items():
            for b in (False, True):
                w2 = paso(w, b)
                if w2 is FUSION:
                    f += p
                else:
                    nueva[w2] = nueva.get(w2, 0) + p
        dist = nueva
        fusionadas.append(2 * fusionadas[-1] + f)
    return fusionadas


def main(K=18):
    N, G, h, C, U = 2, 8, 16, 36, Fraction(4)
    assert h <= K
    discrepancias = 0
    vistas = bytearray(2 ** K)
    repetidas = 0
    fusion_real = [0] * (K + 1)
    vivas_pocas = sin_explicar = 0
    periodicidad_fallos = clasica_fallos = clasica_casos = 0
    for n in range(2 ** K, 2 ** (K + 1)):
        X, Y, P, Q = n, n + 1, 0, 0
        z = (0, 1)
        palabra = 0
        estados = []
        fusion_en = None
        for t in range(K + 1):
            real, ancla = canonico(X, Y, P, Q)
            if real != z:
                discrepancias += 1
                break
            estados.append(z)
            if z is FUSION and fusion_en is None:
                fusion_en = t
            if t == K:
                break
            b = ancla % 2 == 1
            palabra = 2 * palabra + b
            z = paso(z, b)
            P, X = P + X % 2, T(X)
            Q, Y = Q + Y % 2, T(Y)
        if z != estado_final(n - 2 ** K, K):
            periodicidad_fallos += 1
        if fusion_en is not None:
            clasica_casos += 1
            X2, Y2, P2, Q2 = n, n + 1, 0, 0
            for _ in range(fusion_en):
                P2, X2 = P2 + X2 % 2, T(X2)
                Q2, Y2 = Q2 + Y2 % 2, T(Y2)
            k = fusion_en + P2
            a, b = n, n + 1
            for _ in range(k):
                a, b = collatz(a), collatz(b)
            clasica_fallos += not (P2 == Q2 and k <= 2 * fusion_en and a == b)
        if vistas[palabra]:
            repetidas += 1
        vistas[palabra] = 1
        for t in range(K + 1):
            fusion_real[t] += fusion_en is not None and fusion_en <= t
        # inclusión de Lagartijas en los primeros h pasos del par real
        est = estados[:h + 1]
        if len(est) == h + 1 and est[-1] is not FUSION:
            guard = [False] + [guardado(est[t], est[t + 1], C) for t in range(h)]
            if sum(guard) < N:
                vivas_pocas += 1
                c1 = any(tamano(w) > U for w in est)
                i, a, obj = 0, 0, False
                for t in range(h + 1):
                    if t > 0:
                        i, a = (i + 1, 0) if guard[t] else (i, a + 1)
                    if i < N and a >= G and all(tamano(w) <= U for w in est[:t + 1]):
                        obj = True
                sin_explicar += not (c1 or obj)
    cadena = fusion_cadena(K)
    salida = dict(
        K=K, pares=2 ** K,
        estado_real_igual_a_cadena=discrepancias == 0, discrepancias=discrepancias,
        palabras_distintas=2 ** K - repetidas, repetidas=repetidas,
        fusion_hasta_t_real=fusion_real, fusion_hasta_t_cadena=cadena,
        transporte_exacto=all(fusion_real[t] == cadena[t] * 2 ** (K - t) for t in range(K + 1)),
        inclusion=dict(N=N, G=G, h=h, C=C, U=str(U), vivas_pocas=vivas_pocas,
                       sin_explicar=sin_explicar),
        periodicidad_fallos=periodicidad_fallos,
        encuentro_clasico=dict(casos=clasica_casos, fallos=clasica_fallos))
    print(json.dumps(salida, ensure_ascii=False, indent=1))
    ok = (discrepancias == 0 and repetidas == 0 and salida['transporte_exacto']
          and sin_explicar == 0 and periodicidad_fallos == 0 and clasica_fallos == 0)
    print('OK' if ok else 'FALLO')
    Path(__file__).with_name('evidencia_lagartijas_pares.json').write_text(
        json.dumps(salida, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    return ok


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--K', type=int, default=18)
    raise SystemExit(0 if main(p.parse_args().K) else 1)
