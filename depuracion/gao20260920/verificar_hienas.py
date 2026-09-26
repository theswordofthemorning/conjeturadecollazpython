"""Hienas, contraste numerico: tabla 3 de Gao (1993) y puente con la forma de Lagarias.

Mapa clasico C(n) = n/2 si n es par, 3n+1 si es impar.

Gao (pag. 264): n y n+1 "coalescen" en el paso j si C^j(n) = C^j(n+1),
con el mismo numero de divisiones por 2 en los j primeros pasos, y sin
que el 1 aparezca en ninguna de las dos trayectorias. Aqui se usa la
lectura mas exigente: el 1 no puede estar en C^0..C^j (como en Hienas.lean).

Gao (pag. 265): d_barra(k) = 2^-k * #{n < 2^k - 1 : coalescen en <= k pasos}.

Lagarias: G = {n : C^j(n) = C^j(n+1) para algun j <= log2 n}.

Comprueba, para todos los n < 2^K:
- los 21 valores de la tabla 3 de Gao (k = 4..24), a media milesima;
- que todo n de G coalesce en el sentido de Gao (el puente de Hienas.lean).

Basta mirar el PRIMER encuentro j0: despues del encuentro las dos
trayectorias son la misma, asi que las divisiones ya no pueden igualarse
si no lo estaban, y un 1 anterior sigue siendo anterior.

Es un control finito; el certificado universal es Hienas.lean.
Uso: python -B -X utf8 verificar_hienas.py   (unos 30 segundos, necesita numpy)
"""

import numpy as np

K = 24              # se estudian todos los n < 2^K
BLOQUE = 2**22      # tamano de cada tanda, para no llenar la memoria

# Tabla 3 de Gao, copiada del articulo (pag. 266)
TABLA3 = {4: 0.063, 5: 0.125, 6: 0.172, 7: 0.227, 8: 0.254, 9: 0.283,
          10: 0.298, 11: 0.313, 12: 0.322, 13: 0.334, 14: 0.340,
          15: 0.348, 16: 0.354, 17: 0.360, 18: 0.365, 19: 0.370,
          20: 0.374, 21: 0.378, 22: 0.382, 23: 0.386, 24: 0.389}


def main():
    cuenta_gao = {k: 0 for k in range(1, K + 1)}   # numerador de d_barra(k)
    cuenta_G = {k: 0 for k in range(1, K + 1)}     # n < 2^k en el conjunto G
    en_G = 0
    fallos_puente = 0       # n en G cuyo encuentro NO es de Gao
    for inicio in range(0, 2**K, BLOQUE):
        n = np.arange(inicio, inicio + BLOQUE, dtype=np.int64)
        x = n.copy()
        y = n + 1
        mitx = np.zeros(BLOQUE, dtype=np.int16)
        mity = np.zeros(BLOQUE, dtype=np.int16)
        unox = (x == 1)
        unoy = (y == 1)
        primer = np.full(BLOQUE, -1, dtype=np.int16)
        mit_iguales = np.zeros(BLOQUE, dtype=bool)
        sin_uno = np.zeros(BLOQUE, dtype=bool)
        for paso in range(1, K + 1):
            parx = (x % 2 == 0)
            pary = (y % 2 == 0)
            x = np.where(parx, x // 2, 3 * x + 1)
            y = np.where(pary, y // 2, 3 * y + 1)
            mitx += parx
            mity += pary
            unox |= (x == 1)          # ahora cubre C^0..C^paso
            unoy |= (y == 1)
            nuevo = (primer == -1) & (x == y)
            primer[nuevo] = paso
            mit_iguales[nuevo] = (mitx[nuevo] == mity[nuevo])
            sin_uno[nuevo] = ~(unox[nuevo] | unoy[nuevo])
        # log2 entero de n, como Nat.log 2 n (vale 0 en n = 0)
        log2n = np.zeros(BLOQUE, dtype=np.int16)
        for b in range(1, K + 1):
            log2n[n >= 2**b] = b
        gao_ok = (primer >= 1) & mit_iguales & sin_uno
        G = (primer >= 1) & (primer <= log2n)
        en_G += int(G.sum())
        fallos_puente += int((G & ~gao_ok).sum())
        for k in range(1, K + 1):
            cuenta_gao[k] += int((gao_ok & (primer <= k) & (n < 2**k - 1)).sum())
            cuenta_G[k] += int((G & (n < 2**k)).sum())
    print('k   d_barra(k) calculado   tabla 3 de Gao   densidad de G en 2^k')
    for k in range(4, K + 1):
        d = cuenta_gao[k] / 2**k
        g = cuenta_G[k] / 2**k
        # Gao redondea hacia arriba (1/16 = 0.0625 -> 0.063); se admite media milesima
        marca = 'OK' if abs(d - TABLA3[k]) <= 0.0005 + 1e-12 else 'DIFIERE'
        print(f'{k:2d}   {d:.6f}             {TABLA3[k]:.3f} {marca:8s}     {g:.6f}')
    print()
    print(f'n < 2^{K} en G (forma de Lagarias): {en_G}')
    print(f'de ellos, encuentros que NO cumplen la definicion de Gao: {fallos_puente}')
    iguales = all(abs(cuenta_gao[k] / 2**k - TABLA3[k]) <= 0.0005 + 1e-12 for k in range(4, K + 1))
    ok = iguales and fallos_puente == 0
    print('OK' if ok else 'FALLO')
    return ok


if __name__ == '__main__':
    raise SystemExit(0 if main() else 1)
