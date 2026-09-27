"""Revision adversarial del 27-09-2026: Gao (1993), con codigo nuevo.

No importa nada del laboratorio. Recalcula desde cero, con el mapa clasico
C(n) = n/2 si n es par y 3n+1 si es impar:

1. La tabla 3 de Gao: 2^k * dbarra_k = #{n < 2^k - 1 : n y n+1 coalescen
   en algun paso j <= k}. Coalescer (Gao, pag. 264): C^j(n) = C^j(n+1), las
   mismas divisiones por 2 en los j primeros pasos, y ningun 1 en
   C^0..C^j de las dos trayectorias (la lectura mas exigente).
2. La tabla 2 de Gao: d(x) = #{n < x : n y n+1 coalescen} / x, sin tope de
   pasos. Nadie la habia cotejado antes.
3. El puente de Hienas: si n y n+1 se encuentran en k <= log2(n) pasos,
   coalescen en el sentido de Gao en ese mismo paso.

Los valores de Gao salen de su articulo (Discrete Math. 112, 1993, pags.
265-266), redondeados a tres decimales.

Uso: python -B -X utf8 revision_gao.py
Termina con SystemExit(1) si algo no coincide.
"""

import time
import numpy as np

K_TABLA3 = 24          # tabla 3 hasta k = K_TABLA3 (Gao llega a 24)
X_TABLA2 = 7           # tabla 2 hasta x = 10^X_TABLA2 (Gao llega a 10^8)
P_PUENTE = 22          # puente para todo n < 2^P_PUENTE
BLOQUE = 2 ** 21       # tamano de bloque para no gastar mucha memoria

# Tabla 3 de Gao (pag. 266): k -> dbarra_k con tres decimales
TABLA3_GAO = {4: 0.063, 5: 0.125, 6: 0.172, 7: 0.227, 8: 0.254, 9: 0.283,
              10: 0.298, 11: 0.313, 12: 0.322, 13: 0.334, 14: 0.340,
              15: 0.348, 16: 0.354, 17: 0.360, 18: 0.365, 19: 0.370,
              20: 0.374, 21: 0.378, 22: 0.382, 23: 0.386, 24: 0.389}

# Tabla 2 de Gao (pag. 265): exponente j de x = 10^j -> d(x)
TABLA2_GAO = {2: 0.310, 3: 0.365, 4: 0.416, 5: 0.450, 6: 0.477, 7: 0.496,
              8: 0.512}

GRANDE = 2 ** 62       # aviso de desborde de int64


def un_paso(x):
    """Un paso del mapa clasico sobre un arreglo; devuelve (nuevo, era_par)."""
    par = (x % 2 == 0)
    return np.where(par, x // 2, 3 * x + 1), par


def primer_evento(inicio, fin, tope_pasos):
    """Para cada n en [inicio, fin) sigue n y n+1 a la vez con C.

    Devuelve un arreglo con el paso j en que coalescen (en el sentido de Gao)
    o -1 si antes aparece un 1, si se encuentran con distintas mitades, o si
    no pasa nada en tope_pasos pasos (tope_pasos = None: sin tope)."""
    n = np.arange(inicio, fin, dtype=np.int64)
    a = n.copy()
    b = n + 1
    mit_a = np.zeros(len(n), dtype=np.int64)
    mit_b = np.zeros(len(n), dtype=np.int64)
    resultado = np.full(len(n), -1, dtype=np.int64)
    vivos = np.arange(len(n))
    paso = 0
    while len(vivos) > 0:
        av = a[vivos]
        bv = b[vivos]
        # primero el 1: si aparece en C^0..C^paso, ya no pueden coalescer
        hay_uno = (av == 1) | (bv == 1)
        se_encuentran = (av == bv) & ~hay_uno
        buenos = se_encuentran & (mit_a[vivos] == mit_b[vivos])
        resultado[vivos[buenos]] = paso
        terminados = hay_uno | se_encuentran
        vivos = vivos[~terminados]
        if tope_pasos is not None and paso == tope_pasos:
            break
        if len(vivos) == 0:
            break
        nuevo_a, par_a = un_paso(a[vivos])
        nuevo_b, par_b = un_paso(b[vivos])
        a[vivos] = nuevo_a
        b[vivos] = nuevo_b
        mit_a[vivos] += par_a
        mit_b[vivos] += par_b
        if len(vivos) > 0 and max(nuevo_a.max(), nuevo_b.max()) > GRANDE:
            raise SystemExit('desborde de int64')
        paso += 1
    return resultado


def por_bloques(fin, tope_pasos):
    partes = []
    for inicio in range(0, fin, BLOQUE):
        partes.append(primer_evento(inicio, min(fin, inicio + BLOQUE), tope_pasos))
    return np.concatenate(partes)


def tabla3():
    """Cuenta 2^k * dbarra_k para k = 1..K_TABLA3 con una sola pasada."""
    fin = 2 ** K_TABLA3 - 1
    j = por_bloques(fin, K_TABLA3)
    cuentas = {}
    for k in range(1, K_TABLA3 + 1):
        tope_n = 2 ** k - 1
        cuentas[k] = int(((j[:tope_n] >= 0) & (j[:tope_n] <= k)).sum())
    return cuentas


def tabla2():
    fin = 10 ** X_TABLA2
    j = por_bloques(fin, None)
    valores = {}
    for e in range(2, X_TABLA2 + 1):
        x = 10 ** e
        valores[e] = int((j[:x] >= 0).sum()) / x
    return valores, j


def puente():
    """Encuentro de Lagarias (k <= floor(log2 n), sin mirar el 1) contra Gao."""
    fin = 2 ** P_PUENTE
    fallos = 0
    encuentros = 0
    en_2_20 = 0
    for inicio in range(1, fin, BLOQUE):
        final = min(fin, inicio + BLOQUE)
        n = np.arange(inicio, final, dtype=np.int64)
        log2n = np.floor(np.log2(n)).astype(np.int64)
        # correccion por si el redondeo de log2 falla cerca de potencias de 2
        log2n = np.where(2 ** (log2n + 1) <= n, log2n + 1, log2n)
        log2n = np.where(2 ** log2n > n, log2n - 1, log2n)
        a = n.copy()
        b = n + 1
        mit_a = np.zeros(len(n), dtype=np.int64)
        mit_b = np.zeros(len(n), dtype=np.int64)
        vio_uno = np.zeros(len(n), dtype=bool)
        paso_encuentro = np.full(len(n), -1, dtype=np.int64)
        mitades_iguales = np.zeros(len(n), dtype=bool)
        sin_uno = np.zeros(len(n), dtype=bool)
        for paso in range(0, P_PUENTE + 1):
            # vio_uno: aparecio un 1 en C^0..C^paso de alguna de las dos
            vio_uno |= (a == 1) | (b == 1)
            nuevo = (paso_encuentro < 0) & (a == b) & (paso <= log2n)
            paso_encuentro[nuevo] = paso
            mitades_iguales[nuevo] = mit_a[nuevo] == mit_b[nuevo]
            sin_uno[nuevo] = ~vio_uno[nuevo]
            a, par_a = un_paso(a)
            b, par_b = un_paso(b)
            mit_a += par_a
            mit_b += par_b
        hay = paso_encuentro >= 0
        encuentros += int(hay.sum())
        fallos += int((hay & ~(mitades_iguales & sin_uno)).sum())
        if final <= 2 ** 20:
            en_2_20 += int(hay.sum())
        elif inicio < 2 ** 20:
            en_2_20 += int(hay[: 2 ** 20 - inicio].sum())
    return encuentros, fallos, en_2_20


def main():
    ok = True
    t0 = time.time()
    cuentas = tabla3()
    print('Tabla 3 (2^k * dbarra_k), k = 1..%d:' % K_TABLA3)
    print('  ', [cuentas[k] for k in range(1, K_TABLA3 + 1)])
    for k, valor in TABLA3_GAO.items():
        if k > K_TABLA3:
            continue
        mio = cuentas[k] / 2 ** k
        # redondeo a tres decimales, mitad hacia arriba como en la tabla
        redondeado = int(mio * 1000 + 0.5) / 1000
        bien = abs(redondeado - valor) < 1e-9
        ok = ok and bien
        if not bien:
            print('   DISTINTO en k=%d: mio %.6f, Gao %.3f' % (k, mio, valor))
    print('   coincide con la tabla 3 de Gao:', ok, '(%.0f s)' % (time.time() - t0))

    t0 = time.time()
    valores, j = tabla2()
    print('Tabla 2, d(10^e):')
    ok2 = True
    for e, v in valores.items():
        redondeado = int(v * 1000 + 0.5) / 1000
        bien = abs(redondeado - TABLA2_GAO[e]) < 1e-9
        ok2 = ok2 and bien
        print('   e=%d  mio %.6f  Gao %.3f  %s' % (e, v, TABLA2_GAO[e], 'OK' if bien else 'DISTINTO'))
    print('   coincide con la tabla 2 de Gao:', ok2, '(%.0f s)' % (time.time() - t0))
    ok = ok and ok2

    t0 = time.time()
    encuentros, fallos, en_2_20 = puente()
    print('Puente, n < 2^%d: %d encuentros en <= log2 n pasos, %d fallos'
          % (P_PUENTE, encuentros, fallos))
    print('   densidad de encuentros en [1, 2^20): %.4f' % (en_2_20 / 2 ** 20))
    print('   densidad de encuentros en [1, 2^%d): %.4f  (%.0f s)'
          % (P_PUENTE, encuentros / 2 ** P_PUENTE, time.time() - t0))
    ok = ok and fallos == 0
    print('OK' if ok else 'FALLO')
    return ok


if __name__ == '__main__':
    raise SystemExit(0 if main() else 1)
