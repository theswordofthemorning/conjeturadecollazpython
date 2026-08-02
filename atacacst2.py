# atacacst2.py
#
# LA SEGUNDA FASE DEL ATAQUE A CST: subir X0, el barrido directo sigma == sigma*.
#
#   paradacoef.py verifico sigma = sigma* en los impares hasta 2*10^7, y de ahi
#   salio el corte demostrado sigma* <= 16.294 (via la cota B(k): una clase con
#   tramo abierto exige r <= B(k), y B(k) <= 2*10^7 para todo k <= 16.294).
#
#   Este programa empuja X0 a 10^8. Cada extension corre el corte por la curva
#   B(k) sin gastar un token: la conversion X0 -> K la hace la maquinaria de
#   B(k) de paradacoef.py en la sesion siguiente.
#
#   Los pares son triviales (sigma = sigma* = 1); se barren solo los impares.
#   Si aparece UN solo n con sigma != sigma*, ES un contraejemplo de CST y
#   este programa para en el acto: seria el hallazgo del siglo, no un bug.

LIMITE = 10 ** 8    # barrer impares 3 .. LIMITE
TRAMO = 10 ** 7     # imprimir progreso cada tanto

import sys

def verificar_tramo(desde, hasta):
    # sigma(n): primer k con T^k(n) < n.  sigma*(n): primer k con 2^k > 3^S.
    # Se avanzan JUNTOS: en cuanto uno de los dos dispara, el otro tiene que
    # disparar en el mismo k, o hay contraejemplo.
    for n in range(desde | 1, hasta, 2):
        x = n
        S = 0
        k = 0
        pot2 = 1
        pot3 = 1
        while True:
            k += 1
            pot2 += pot2
            if x % 2:
                S += 1
                pot3 *= 3
                x = (3 * x + 1) // 2
            else:
                x //= 2
            cae_real = x < n
            cae_coef = pot2 > pot3
            if cae_real or cae_coef:
                if cae_real != cae_coef:
                    raise SystemExit("CONTRAEJEMPLO DE CST EN n = %d (k = %d): "
                                     "real=%r coef=%r" % (n, k, cae_real, cae_coef))
                break

# comprobacion previa: el barrido reproduce el rango ya conocido en un tramo
verificar_tramo(3, 100001)
print("COMPROBACION OK: impares 3..10^5, sigma == sigma*, 0 diferencias")

for ini in range(0, LIMITE, TRAMO):
    verificar_tramo(max(3, ini), min(ini + TRAMO, LIMITE))
    print("  ... impares hasta %d: 0 diferencias" % min(ini + TRAMO, LIMITE))
    sys.stdout.flush()

print()
print("RESULTADO: sigma(n) = sigma*(n) para TODO n hasta %d." % LIMITE)
print("X0 sube de 2*10^7 a 10^8: la conversion a un corte sigma* <= K nuevo")
print("va por la curva B(k) de paradacoef.py (siguiente sesion).")
