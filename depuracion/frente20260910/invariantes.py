"""Cruce finito del lema de invariantes; no es una revision ciega.

Componentes por conexiones x -- tau_k(x), no espectro ni power iteration.
Las normas SVD son MEDICIONES flotantes y no prueban un gap uniforme.
"""

from fractions import Fraction


def tau(k, x, n):
    return (3*x + (1 - 3**k)//2) % n


def componentes(alturas, n):
    padres = list(range(n))

    def raiz(x):
        while padres[x] != x:
            padres[x] = padres[padres[x]]
            x = padres[x]
        return x

    for k in alturas:
        for x in range(n):
            a, b = raiz(x), raiz(tau(k, x, n))
            padres[a] = b
    return len({raiz(x) for x in range(n)})


def chi(x):
    return (1, -1, -1, 1)[x % 4]


def promedio(k, f):
    n = len(f)
    return [Fraction(f[x] + f[tau(k, x, n)], 2) for x in range(n)]


def main():
    print("EXACTO: componentes comunes (3,5) frente a (2,3)")
    comprobaciones = 0
    for m in range(2, 13):
        n = 2**m
        a, b = componentes((3, 5), n), componentes((2, 3), n)
        if (a, b) != (2, 1):
            raise SystemExit(f"Componentes inesperadas: {m, a, b}")
        f = [chi(x) for x in range(n)]
        if sum(f) != 0:
            raise SystemExit("El testigo no esta centrado")
        for k in (3, 5):
            if promedio(k, f) != f:
                raise SystemExit("El testigo no es invariante")
        g = promedio(2, f)
        if sum(v*v for v in g) != Fraction(sum(v*v for v in f), 2):
            raise SystemExit("La energia no cae exactamente a la mitad")
        inv3 = pow(3, -1, n)
        for x in range(n):
            inversa_tres = inv3*(x + 13) % n
            if tau(2, inversa_tres, n) != (x + 9) % n:
                raise SystemExit("La composicion no es traslacion por 9")
            comprobaciones += 1
        print(f"  m={m:2d}: componentes={a},{b}; "
              "energia(M2 chi)/energia(chi)=1/2")
    print(f"CONTROL: {comprobaciones} identidades de traslacion: OK")

    import numpy as np

    print("MEDICION SVD: norma en media cero de M2 M3; no uniforme en m")
    for m in range(2, 9):
        n = 2**m
        identidad = np.eye(n)
        mats = []
        for k in (2, 3):
            permutacion = identidad[[tau(k, x, n) for x in range(n)]]
            mats.append((identidad + permutacion) / 2)
        producto = mats[0] @ mats[1]
        centrado = producto - np.ones((n, n))/n
        norma = np.linalg.svd(centrado, compute_uv=False)[0]
        if not 0 < norma < 1:
            raise SystemExit("SVD incompatible con la contraccion finita")
        print(f"  m={m}: {norma:.12f}")
    print("FIN: control exacto y SVD separados; no prueba rho_cond < 1/2.")


if __name__ == "__main__":
    main()
