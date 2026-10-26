"""Contraste exacto de la clasificacion con F invertible y A distinta de B."""

import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


IDENTIDAD = (1, 0, 0, 1)
CERO = (0, 0, 0, 0)
REGLAS = (("e", "a", "a", "e"), ("f", "a", "b", "e"),
          ("g", "a", "a", "f"), ("e", "b", "b", "f"),
          ("f", "b", "a", "g"), ("g", "b", "b", "g"))


def producto_matriz(a, b):
    return tuple(sum(a[2 * i + k] * b[2 * k + j] for k in range(2))
                 for i in range(2) for j in range(2))


def escalar(k, a):
    return tuple(k * x for x in a)


def sumar(a, b):
    return tuple(x + y for x, y in zip(a, b))


def restar(a, b):
    return tuple(x - y for x, y in zip(a, b))


def determinante(a):
    return a[0] * a[3] - a[1] * a[2]


def traza(a):
    return a[0] + a[3]


def clasificar(s):
    a, b, e, f, g = (s[x] for x in "abefg")
    assert determinante(f) != 0 and a != b
    assert all(min(m) >= 0 and all(isinstance(x, int) for x in m) for m in s.values())
    assert all(producto_matriz(s[x], s[y]) == producto_matriz(s[z], s[w])
               for x, y, z, w in REGLAS)
    assert traza(a) == traza(b) and determinante(a) == determinante(b)
    diferencia = restar(a, b)
    assert producto_matriz(diferencia, diferencia) == CERO
    if determinante(a) == 0:
        l = traza(a)
        assert l > 0
        assert producto_matriz(a, a) == escalar(l, a)
        assert producto_matriz(b, b) == escalar(l, b)
        if f == escalar(f[0], IDENTIDAD):
            t = f[0]
            assert t > 0
            assert escalar(l, e) == escalar(t, a)
            assert escalar(l, g) == escalar(t, b)
            assert producto_matriz(a, b) == escalar(l, b)
            assert producto_matriz(b, a) == escalar(l, a)
            return "imagen_comun"
        t = e[0]
        assert t > 0 and e == g == escalar(t, IDENTIDAD)
        assert escalar(l, f) == restar(escalar(t, sumar(a, b)), escalar(t * l, IDENTIDAD))
        assert producto_matriz(f, f) == escalar(t * t, IDENTIDAD)
        assert producto_matriz(a, b) == escalar(l, a)
        assert producto_matriz(b, a) == escalar(l, b)
        return "nucleo_comun"
    assert traza(a) % 3 == 0 and traza(f) % 4 == 0
    m, n = traza(a) // 3, traza(f) // 4
    assert m > 0 and n > 0
    assert determinante(a) == 2 * m * m and determinante(f) == 3 * n * n
    assert producto_matriz(a, diferencia) == escalar(2 * m, diferencia)
    assert producto_matriz(diferencia, a) == escalar(m, diferencia)
    assert escalar(m, e) == restar(escalar(2 * n, a), escalar(m * n, IDENTIDAD))
    assert escalar(m, f) == restar(escalar(n, sumar(a, b)), escalar(m * n, IDENTIDAD))
    assert escalar(m, g) == restar(escalar(2 * n, b), escalar(m * n, IDENTIDAD))
    return "resonancia_2_3"


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    binarias = list(product(range(2), repeat=4))
    productos = {(a, b): producto_matriz(a, b) for a, b in product(binarias, repeat=2)}
    iguales = 0
    conectadas = 0
    clases = Counter()
    testigos = {}
    for a, b, e in product(binarias, repeat=3):
        if a == b or productos[e, a] != productos[a, e]:
            continue
        for f in binarias:
            if determinante(f) == 0:
                continue
            if productos[f, a] != productos[b, e] or productos[e, b] != productos[b, f]:
                continue
            for g in binarias:
                if (productos[g, a] != productos[a, f] or productos[f, b] != productos[a, g]
                        or productos[g, b] != productos[b, g]):
                    continue
                iguales += 1
                s = dict(a=a, b=b, e=e, f=f, g=g)
                conectada = all(sum(m[i] for m in s.values()) > 0 for i in (1, 2))
                conectadas += int(conectada)
                clase = clasificar(s)
                clases[clase] += 1
                testigos.setdefault(clase, s)
    construidos = Counter()
    for u, v, k, q in product(range(1, 4), repeat=4):
        l, t = k * u * v, q * k * u * v
        a = (k * u * v, 0, k * v * v, 0)
        b = (0, k * u * u, 0, k * u * v)
        s = dict(a=a, b=b, e=escalar(q, a), f=escalar(t, IDENTIDAD), g=escalar(q, b))
        construidos[clasificar(s)] += 1
        a = (k * u * v, k * v * v, 0, 0)
        b = (0, 0, k * u * u, k * u * v)
        s = dict(a=a, b=b, e=escalar(t, IDENTIDAD),
                 f=restar(escalar(q, sumar(a, b)), escalar(t, IDENTIDAD)),
                 g=escalar(t, IDENTIDAD))
        construidos[clasificar(s)] += 1
    resonancias = 0
    for m, n, k, l in product(range(2, 13, 2), range(2, 13, 2), (-1, 0, 1), (-1, 0, 1)):
        if k == l:
            continue
        a = escalar(m // 2, (3 + k, 1 - k, 1 + k, 3 - k))
        b = escalar(m // 2, (3 + l, 1 - l, 1 + l, 3 - l))
        e = escalar(n, (2 + k, 1 - k, 1 + k, 2 - k))
        f = escalar(n // 2, (4 + k + l, 2 - k - l, 2 + k + l, 4 - k - l))
        g = escalar(n, (2 + l, 1 - l, 1 + l, 2 - l))
        s = dict(a=a, b=b, e=e, f=f, g=g)
        clase = clasificar(s)
        construidos[clase] += 1
        testigos.setdefault(clase, s)
        resonancias += int(2 * m >= 3 * n)
    resonantes_c3 = []
    for a in product(range(4), repeat=4):
        if traza(a) % 3 == 0:
            m = traza(a) // 3
            if m >= 2 and determinante(a) == 2 * m * m:
                resonantes_c3.append(a)
    assert resonantes_c3 == [(3, 1, 1, 3)]
    datos = dict(estado="correcto", fuente_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                 quintetos_binarios=16 ** 5, iguales_con_f_invertible_y_a_distinta_b=iguales,
                 de_ellos_conectados=conectadas, clasificacion_binaria=dict(clases),
                 casos_construidos=dict(construidos), resonancias_con_2m_mayor_igual_3n=resonancias,
                 matrices_c3_cotejadas=4 ** 4, resonantes_c3_con_mu_mayor_igual_2=resonantes_c3,
                 testigos=testigos,
                 alcance="Cotejo entero independiente de la clasificacion, no prueba universal. "
                         "No se exige orientacion dinamica ni se asignan vectores constantes.")
    args.salida.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(datos, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
