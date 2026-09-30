# Cotejo independiente, sobre enteros: predecesores del atajo de un entero a con
# l pasos impares y a lo sumo K pasos pares.
#
# T(n) = n/2 (par), (3n+1)/2 (impar). Hacia atras desde x: el predecesor par es 2x;
# el impar es (2x-1)/3, que existe si 2x-1 es multiplo de 3 (y entonces es impar).
# Una busqueda en profundidad recorre todos los caminos hacia atras con a lo sumo K
# pasos pares y cuenta los que tienen exactamente l pasos impares. No usa residuos
# ni la recurrencia de elka.py / costo.py.
#
# Pregunta: e_l(k, a) = 0 para todo k <= l? Es decir, ningun b llega a a en 2l
# pasos del atajo con l impares (ni en menos pasos pares).
import sys

A = 34
L_MAX = 16
EXTRA = 3        # tambien se cuenta hasta K = l + EXTRA para ver cuando aparece


def contar(a, l, K):
    """Numero de caminos hacia atras desde a con l impares y exactamente k pares,
    para k = 0..K (lista)."""
    cuentas = [0] * (K + 1)
    pila = [(a, 0, 0)]          # (valor, impares hechos, pares hechos)
    while pila:
        x, i, k = pila.pop()
        if i == l:
            cuentas[k] += 1
            # tambien valen los caminos que anaden pares al final (al principio del
            # camino hacia delante); se cuentan al extender con pasos pares:
        if k < K:
            pila.append((2 * x, i, k + 1))
        if i < l and (2 * x - 1) % 3 == 0 and x > 1:
            pila.append(((2 * x - 1) // 3, i + 1, k))
    return cuentas


print(f"Predecesores de {A}: caminos con l impares y k pares (k <= l + {EXTRA})")
ok = True
for l in range(1, L_MAX + 1):
    K = l + EXTRA
    c = contar(A, l, K)
    hasta_l = sum(c[: l + 1])
    primero = next((k for k in range(K + 1) if c[k] > 0), None)
    print(f"  l={l:2d}: caminos con k <= l: {hasta_l:6d};  primer k con caminos: {primero};"
          f"  cuentas k = l..l+{EXTRA}: {c[l:]}")
    sys.stdout.flush()
