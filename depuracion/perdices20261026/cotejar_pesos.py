"""Construye retornos A/B con variacion binaria positiva y negativa sin censo."""

import argparse
from hashlib import sha256
import json
from pathlib import Path


def valorar(n, p):
    assert n != 0
    n, v = abs(n), 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def polinomio(coeficientes, n):
    return sum(c * n ** i for i, c in enumerate(coeficientes))


def firma(caso, n):
    return [n % caso["modulo_observado"]] + [
        valorar(polinomio(c, n), p) for p, c in caso["observaciones"]]


def afines(palabra):
    D, E, L = 1, 0, 0
    for letra in palabra:
        for bit in ("1" if letra == "A" else "110"):
            if bit == "1":
                E = 3 * E + 2 ** L
                D *= 3
            L += 1
    return D, E, 2 ** L, L


def orden_dos(modulo):
    assert modulo % 2 == 1
    if modulo == 1:
        return 1
    residuo = 2 % modulo
    for g in range(1, 50001):
        if residuo == 1:
            return g
        residuo = 2 * residuo % modulo
    raise ValueError("Orden demasiado grande para este cotejo acotado")


def resumir(n):
    datos = dict(bits=n.bit_length(), peso=n.bit_count(),
                 sha256=sha256(n.to_bytes((n.bit_length() + 7) // 8, "big")).hexdigest())
    if n.bit_length() <= 1024:
        datos["decimal"] = str(n)
    return datos


def verificar(caso, n, y):
    D, E, N, L = afines(caso["palabra"])
    M, n0 = caso["periodo"], caso["semilla"]
    assert M % N == 0 and n >= n0 and (n - n0) % M == 0
    assert N * y == D * n + E and y > n > 0
    assert firma(caso, n) == firma(caso, y) == firma(caso, n0)
    actual = n
    for letra in caso["palabra"]:
        assert actual % 2 == 1
        for bit in ("1" if letra == "A" else "110"):
            assert actual % 2 == int(bit)
            actual = (3 * actual + 1) // 2 if actual % 2 else actual // 2
        assert actual % 2 == 1
    assert actual == y
    # Una segunda cuenta por escritura de bits no usa bit_count.
    assert n.bit_count() == bin(n).count("1")
    assert y.bit_count() == bin(y).count("1")
    return dict(n=resumir(n), y=resumir(y), diferencia=y.bit_count() - n.bit_count(), pasos_T=L)


def construir(caso, repeticiones):
    D, E, N, L = afines(caso["palabra"])
    M, n0 = caso["periodo"], caso["semilla"]
    y0, resto = divmod(D * n0 + E, N)
    assert resto == 0 and M % N == 0
    H = M // N
    orden = orden_dos(M >> valorar(M, 2))
    g = orden * ((D.bit_length() + orden - 1) // orden)
    K = max(valorar(M, 2), n0.bit_length(), L + y0.bit_length()) + 1
    impar_M = M >> valorar(M, 2)
    positivas = []
    for j in range(1, repeticiones + 1):
        m = impar_M * j
        suma = ((1 << (g * m)) - 1) // ((1 << g) - 1)
        n, y = n0 + (suma << K), y0 + (D * suma << (K - L))
        dato = verificar(caso, n, y)
        assert n.bit_count() == n0.bit_count() + m
        assert y.bit_count() == y0.bit_count() + m * D.bit_count()
        assert dato["diferencia"] == y0.bit_count() - n0.bit_count() + m * (D.bit_count() - 1)
        positivas.append(dict(j=j, m=m, **dato))

    a = valorar(D * H, 2)
    d = D * H >> a
    v = y0 % (1 << a)
    if (N * v - E) % 3 == 0:
        v += 1 << a
    assert (N * v - E) % 3 != 0
    u = (y0 - v) % d
    assert u > 0 and u % 3 != 0
    g_menos = orden_dos(d)
    minimo = max(a, v.bit_length() + 1, y0.bit_length() + 1)
    K0 = g_menos * ((minimo + g_menos - 1) // g_menos)
    R = 1 << g_menos
    Q, r = divmod(N * u << K0, D)
    B = N * v - E
    C, resto = divmod(r + B, D)
    assert resto == 0 and 0 < r < D
    c, resto = divmod(r * (R - 1), D)
    assert resto == 0 and 1 <= c <= R - 2
    J, cola = 0, C
    while not 0 <= cola < R ** J:
        cola += c * R ** J
        J += 1
        assert J <= 64
    negativas = []
    for i in range(1, repeticiones + 1):
        j = J + i
        y = (u << (K0 + j * g_menos)) + v
        n, resto = divmod(N * y - E, D)
        assert resto == 0
        dato = verificar(caso, n, y)
        assert n == Q * R ** j + c * (R ** j - 1) // (R - 1) + C
        assert n.bit_count() == Q.bit_count() + (j - J) * c.bit_count() + cola.bit_count()
        assert y.bit_count() == u.bit_count() + v.bit_count()
        negativas.append(dict(j=j, **dato))
    return dict(caso=caso, D=D, E=E, N=N, y0=y0,
                parametros_mas=dict(g=g, K=K, impar_M=impar_M),
                parametros_menos=dict(a=a, d=d, v=v, u=u, g=g_menos, K0=K0,
                                       J=J, c=resumir(c), cola=resumir(cola)),
                positivas=positivas, negativas=negativas)


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--repeticiones", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    assert 1 <= args.repeticiones <= 8
    observaciones = [(2, [1, 1]), (2, [5, 1])]
    casos = [dict(nombre="dos_valoraciones", palabra="AB", semilla=231, periodo=256,
                  modulo_observado=1, observaciones=observaciones),
             dict(nombre="residuo_ternario", palabra="AB", semilla=487, periodo=768,
                  modulo_observado=3, observaciones=observaciones),
             dict(nombre="primo_cinco", palabra="AB", semilla=231, periodo=1280,
                  modulo_observado=5, observaciones=observaciones + [(5, [1, 0, 1])]),
             dict(nombre="raiz_evitable", palabra="ABB", semilla=-251 * pow(115, -1, 16384) % 16384,
                  periodo=16384, modulo_observado=1, observaciones=[(2, [19, 11])]),
             dict(nombre="lote_tres", palabra="ABABAB", semilla=-19 * pow(11, -1, 65536) % 65536,
                  periodo=65536, modulo_observado=1, observaciones=observaciones)]
    resultados = [construir(caso, args.repeticiones) for caso in casos]
    recorridos = [r for c in resultados for familia in ("positivas", "negativas") for r in c[familia]]
    datos = dict(alcance="Contraste finito exacto de familias infinitas demostradas por escrito. "
                 "No es un censo ni una prueba de terminacion AB.",
                 fuente_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                 recorridos=len(recorridos), pasos_T=sum(r["pasos_T"] for r in recorridos),
                 resultados=resultados)
    args.salida.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK: {len(recorridos)} retornos; {datos['pasos_T']} pasos T; pesos exactos de ambas familias.")


if __name__ == "__main__":
    main()
