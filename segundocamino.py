# segundocamino.py
#
# EL SEGUNDO CAMINO PARA a(33) Y a(34) (04-08-2026): la identidad
# demostrada  a(k+2) = a(k) + (2^k - 1) + G(k) + H(k)  con G(k) =
# suma B(m) (piso g, {w,9w+2}) y H(k) = c(k) (piso h, {w,9w-1}),
# evaluada en k = 31 y 32 con TRES barridos de la cadena que arrancan
# en estados distintos. Si los tres cuadran, los dos niveles nuevos de
# paseodeladeuda.py quedan sostenidos por la identidad-teorema de
# identidadexacta.py, no por un unico barrido.
#
#   (No es independencia total -- los tres barridos comparten la
#   funcion de transicion -- pero la identidad cruza tres recorridos
#   distintos del espacio de estados, con arranques y profundidades
#   distintas: un error de contabilidad en cualquiera la rompe.)

A33 = 3761106610
A34 = 7558807251
TOPE_ESTADOS = 10 * 10 ** 6


def transicion(k, c, bit):
    if k == 0:
        if c % 2 == 0:
            return ('estado', 0, c // 2) if bit == 0 else ('estado', 0, 3 * c // 2)
        return ('estado', 1, (3 * c + 1) // 2) if bit == 0 \
            else ('estado', 1, (1 - 3 * c) // 2)
    if c % 2 == 0:
        return ('estado', k, c // 2) if bit == 0 \
            else ('estado', k, (3 * c + 1 - 3 ** k) // 2)
    if bit == 0:
        return ('estado', k + 1, (3 * c + 1) // 2)
    if k >= 2:
        return ('estado', k - 1, (c - 3 ** (k - 1)) // 2)
    g = (c - 1) // 2
    if g == 0:
        return ('fusion',)
    return ('estado', 0, abs(g))


def barrido(inicio, prof):
    estados = {inicio: 1}
    absorbidas = 0
    acum = []
    for t in range(1, prof + 1):
        nuevo = {}
        nuevas = 0
        for (k, c), n in estados.items():
            for bit in (0, 1):
                s = transicion(k, c, bit)
                if s[0] == 'fusion':
                    nuevas += n
                else:
                    clave = (s[1], s[2])
                    nuevo[clave] = nuevo.get(clave, 0) + n
        absorbidas = 2 * absorbidas + nuevas
        estados = nuevo
        acum.append(absorbidas)
        if len(estados) > TOPE_ESTADOS:
            raise SystemExit("tope de estados en prof %d" % t)
    return acum


print("barrido principal (0,1) a 34...")
a = barrido((0, 1), 34)
print("barrido piso g (2,2) a 31...")
B = barrido((2, 2), 31)
print("barrido piso h (2,-1) a 32...")
c = barrido((2, -1), 32)

# G(k) = suma_{m=0}^{k-1} B(m); B(m) = absorbidas de (2,2) en <= m
for k in (31, 32):
    # G(k) = suma de los B(m) tal cual (no doblados), m = 1..k-1
    G = sum(B[m - 1] for m in range(1, k))
    H = c[k - 1]
    esperado = a[k - 1] + (2 ** k - 1) + G + H
    obtenido = a[k + 1]
    print("k=%d: a(k)=%d  2^k-1=%d  G=%d  H=%d  ->  a(k+2)=%d  %s"
          % (k, a[k - 1], 2 ** k - 1, G, H, obtenido,
             "OK" if esperado == obtenido else "FALLO (esp %d)" % esperado))
    if esperado != obtenido:
        raise SystemExit("IDENTIDAD ROTA en k=%d" % k)

if a[32] != A33 or a[33] != A34:
    raise SystemExit("los niveles nuevos no reproducen paseodeladeuda.py")

print()
print("SEGUNDO CAMINO OK: a(33) = %d y a(34) = %d cumplen la identidad" % (A33, A34))
print("a(k+2) = a(k) + (2^k - 1) + G(k) + H(k) en k = 31 y 32, con G y H")
print("calculadas por barridos separados de los pisos g y h. Los dos")
print("niveles nuevos quedan sostenidos por la identidad-teorema.")
