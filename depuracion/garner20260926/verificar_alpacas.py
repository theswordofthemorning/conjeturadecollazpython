"""Contraste independiente de Alpacas (conjetura de Garner, 1985): rachas de la misma altura.

Alpacas.lean demuestra: para cada L y N hay n >= N tal que n, n+1, ..., n+L tienen la
misma altura h y el mismo tiempo total de parada s (divisiones por 2 hasta llegar a 1).
La construccion de la prueba da h = t + a + m y s = t + m. Aqui se rehace con otro
codigo y se comprueba iterando de verdad. Es un control finito, no una prueba.

Mapa clasico C(n) = n/2 si n es par, 3n+1 si es impar. Atajo T(x) = x/2 o (3x+1)/2.

1. Clases de Terras por recurrencia en t (distinta del sondeo, que itera T sobre cada r):
   T^t(2^t*u + r) = 3^a(r)*u + A(r). El par (r, r+1) esta fusionado hasta t si tiene la
   misma clase. Para t <= 10 se coteja con la iteracion directa.
2. Para cada L se busca el menor t con L pares seguidos fusionados.
3. m con 2^m = A (mod 3^a) se obtiene subiendo de 3^k a 3^(k+1), como en `dos_genera`.
   Luego u = (2^m - A)/3^a y n = 2^t*u + r.
4. Cada n+i se itera t+a pasos clasicos: no pasa por 1, llega a 2^m y hace t mitades.
   Si m <= M_DIRECTO, ademas se itera hasta 1 y se comparan altura y mitades.
   Se repite con el siguiente m del periodo, para ver que n puede crecer.
5. Cotejos: 2 es raiz primitiva modulo 3^k (k <= 9) y la tabla 1 de Gao (1993).

Uso: python -B -X utf8 verificar_alpacas.py      (unos segundos)
"""

L_MAX = 22          # rachas de L+1 consecutivos, L = 1..L_MAX (L = 22 pide t = 20)
T_MAX = 20          # tope de t en la busqueda
M_DIRECTO = 6000    # con m hasta aqui se itera tambien la cola 2^m -> 1


def clases_por_nivel(t_max):
    """Lista de (a, A) por nivel: nivel[t] = (a, A) con listas de largo 2^t."""
    niveles = [([0], [0])]
    for t in range(1, t_max + 1):
        a_prev, A_prev = niveles[-1]
        mitad = 2 ** (t - 1)
        a = [0] * (2 ** t)
        A = [0] * (2 ** t)
        for r in range(2 ** t):
            q, b = divmod(r, 2)
            if b == 0:
                x, extra = q, 0
            else:
                x, extra = 3 * q + 2, 1
            v, w = divmod(x, mitad)
            a[r] = a_prev[w] + extra
            A[r] = 3 ** a_prev[w] * v + A_prev[w]
        niveles.append((a, A))
    return niveles


def atajo(x, pasos):
    impares = 0
    for _ in range(pasos):
        if x % 2 == 0:
            x //= 2
        else:
            x = (3 * x + 1) // 2
            impares += 1
    return impares, x


def raiz_primitiva(k):
    """Orden de 2 modulo 3^k, por fuerza bruta."""
    modulo = 3 ** k
    x, orden = 2 % modulo, 1
    while x != 1:
        x = x * 2 % modulo
        orden += 1
    return orden


def exponente(a, A):
    """m con 3^a | 2^m - A, subiendo de 3^k a 3^(k+1) (a >= 1, 3 no divide a A)."""
    m = 0 if A % 3 == 1 else 1
    for k in range(1, a):
        periodo = 2 * 3 ** (k - 1)
        for s in range(3):
            if (pow(2, m + s * periodo, 3 ** (k + 1)) - A) % 3 ** (k + 1) == 0:
                m = m + s * periodo
                break
        else:
            raise AssertionError('no se pudo subir el exponente')
    return m


def prefijo(n, pasos):
    """Itera pasos clasicos: (pasa por 1 antes, valor final, mitades)."""
    mitades, uno = 0, False
    for _ in range(pasos):
        if n == 1:
            uno = True
        if n % 2 == 0:
            n //= 2
            mitades += 1
        else:
            n = 3 * n + 1
    return uno, n, mitades


def altura(n):
    pasos, mitades = 0, 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
            mitades += 1
        else:
            n = 3 * n + 1
        pasos += 1
    return pasos, mitades


def comprobar_racha(t, r, L, a, A, m):
    """Construye n y comprueba los L+1 consecutivos. Devuelve (ok, n, directo)."""
    modulo = 3 ** a
    assert (2 ** m - A) % modulo == 0
    u = (2 ** m - A) // modulo
    n = 2 ** t * u + r
    ok, directo = True, m <= M_DIRECTO
    for i in range(L + 1):
        uno, valor, mitades = prefijo(n + i, t + a)
        ok = ok and not uno and valor == 2 ** m and mitades == t
        if directo:
            ok = ok and altura(n + i) == (t + a + m, t + m)
    return ok, n, directo


def main():
    ok = True

    # 5a. 2 es raiz primitiva modulo 3^k
    for k in range(1, 10):
        ok = ok and raiz_primitiva(k) == 2 * 3 ** (k - 1)
    print('orden de 2 modulo 3^k igual a 2*3^(k-1) para k = 1..9:', ok)

    # 1. clases por recurrencia, cotejadas con la iteracion directa
    niveles = clases_por_nivel(T_MAX)
    for t in range(0, 11):
        a, A = niveles[t]
        for r in range(2 ** t):
            ok = ok and (a[r], A[r]) == atajo(r, t)
    print('clases de Terras cotejadas con la iteracion directa, t <= 10:', ok)

    # 2-4. una racha para cada L
    print(' L    t   r          a   m       cifras de n   altura   mitades   cola directa')
    for L in range(1, L_MAX + 1):
        hallada = None
        for t in range(1, T_MAX + 1):
            a, A = niveles[t]
            seguidos = 0
            for r in range(2 ** t - 1):
                if a[r] == a[r + 1] and A[r] == A[r + 1]:
                    seguidos += 1
                    if seguidos == L:
                        hallada = (t, r - L + 1)
                        break
                else:
                    seguidos = 0
            if hallada:
                break
        if not hallada:
            print(f'{L:2d}   sin racha con t <= {T_MAX}')
            ok = False
            continue
        t, r = hallada
        a, A = niveles[t]
        clase = (a[r], A[r])
        ok = ok and all((a[r + i], A[r + i]) == clase for i in range(L + 1))
        aa, AA = clase
        ok = ok and aa >= 1 and AA % 3 != 0
        periodo = 2 * 3 ** (aa - 1)
        m = exponente(aa, AA) % periodo
        while m < 3 or 2 ** m < AA:
            m += periodo
        bien, n, directo = comprobar_racha(t, r, L, aa, AA, m)
        # el siguiente m del periodo: una racha mas arriba
        bien2, n2, _ = comprobar_racha(t, r, L, aa, AA, m + periodo)
        ok = ok and bien and bien2 and n2 > n
        print(f'{L:2d}   {t:2d}  {r:<9d}  {aa:2d}  {m:<6d}  {len(str(n)):>10d}   {t + aa + m:6d}'
              f'   {t + m:6d}    {"si" if directo else "no"}   {"OK" if bien and bien2 else "FALLO"}')

    # 5b. tabla 1 de Gao (1993, pag. 263): comienzo, largo, altura, sigma_inf
    tabla = [(943, 7, 36, 26), (7083, 17, 57, 40), (57346, 25, 78, 54),
             (596310, 40, 97, 67), (5772712, 65, 214, 140), (98041684, 98, 169, 114),
             (722067240, 176, 190, 128), (9749626154, 349, 248, 165)]
    bien_tabla = all(altura(n0 + i) == (h, s) for n0, largo, h, s in tabla for i in range(largo))
    print('tabla 1 de Gao, las 8 filas enteras:', bien_tabla)
    # la 35654-upla de Gao desde 2^500 + 1 (altura 3279, sigma 2204), por muestras
    muestra = [2 ** 500 + j for j in list(range(1, 35655, 1000)) + [35654]]
    bien_gran = all(altura(x) == (3279, 2204) for x in muestra)
    print('35654-upla de Gao desde 2^500+1, muestra de', len(muestra), 'numeros:', bien_gran)
    ok = ok and bien_tabla and bien_gran

    print('OK' if ok else 'FALLO')
    return ok


if __name__ == '__main__':
    raise SystemExit(0 if main() else 1)
