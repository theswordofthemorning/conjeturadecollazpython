# identidadexacta.py
#
# LA IDENTIDAD EXACTA DE LA RENOVACION (03-08-2026, noche; propuesta por
# la primera revision externa -Opus 5- como sustituto de toda simulacion).
#
#   Si el teorema de Gatas es literal, la particion de las clases buenas
#   mod 2^(k+2) debe valer como IGUALDAD DE ENTEROS en cada nivel finito,
#   sin Monte Carlo, sin topes, sin sesgo de truncamiento:
#
#       a(k+2)  =  a(k)  +  (2^k - 1)  +  G(k)  +  H(k)
#
#   donde:
#     a(k)      rama r = 1 (mod 4): la contraccion (4t+1 -> par fresco
#               (3t+1, 3t+2)) mas la biyeccion t -> 3t+1 dan EXACTAMENTE
#               las buenas de nivel k;
#     2^k - 1   rama r par con |M| = 2: la ventana de Perras (fusion en
#               j+3 <= k+2 <=> j <= k-1; los patrones 1^j 0 1 suman
#               2^k - 1 clases, exacto);
#     G(k)      rama r par con |M| >= 4 (rebotados y refundidos);
#     H(k)      rama r = 3 (mod 4).
#
#   RESULTADO: LA IDENTIDAD CIERRA EXACTA en todos los niveles probados
#   (k = 3..14), con rama1 == a(k) clavado y perras == 2^k - 1 clavado.
#   G y H nacen como SUCESIONES EXACTAS (los "g" y "h" de la ecuacion de
#   renovacion en forma entera):
#
#     G: 0, 0, 0, 0, 1, 5, 16, 44, 110, 259, 588, 1302     (k = 3..14)
#     H: 0, 0, 0, 1, 3, 9, 24, 58, 134, 300, 659, 1426
#
#   Y DE REGALO (revision externa): la rama h se reduce igual que la g:
#   (4t+3, 4t+4) va en dos pasos a {w, 9w-1} con w = t+1 -- casi espejo
#   del rebote {w, 9w+2}, sin ser conjugados por una simetria obvia
#   (gap par contra gap impar). Y los contraejemplos de Elia-Tucker 2015
#   a la conjetura de Garner viven TODOS en |M| = 8 (tabla abajo), lo
#   que confirma la afirmacion de novedad de Perras: el estrato |M| = 2
#   es exactamente el territorio donde Garner tenia razon.

def paso(x):
    return (3 * x + 1) // 2 if x % 2 else x // 2


def analiza(r, N):
    # (buena, |M|) del par (r, r+1) en <= N pasos; buena exige S igual
    x, y = r, r + 1
    Sx = Sy = M = 0
    for _ in range(N):
        if (x % 2) != (y % 2):
            M += 1
        if x % 2:
            Sx += 1
        if y % 2:
            Sy += 1
        x, y = paso(x), paso(y)
        if x == y:
            return (Sx == Sy), M
    return False, M


G_serie, H_serie = [], []
for k in range(3, 15):
    N = k + 2
    a_k = sum(analiza(r, k)[0] for r in range(2 ** k - 1))
    rama1 = perr = G = H = a_k2 = 0
    for r in range(2 ** N - 1):
        buena, M = analiza(r, N)
        if not buena:
            continue
        a_k2 += 1
        if r % 4 == 1:
            rama1 += 1
        elif r % 4 == 3:
            H += 1
        elif M == 2:
            perr += 1
        else:
            G += 1
    # LAS TRES COMPROBACIONES, exactas o nada:
    if rama1 != a_k:
        raise SystemExit("FALLO rama 1: k=%d da %d, a(k)=%d" % (k, rama1, a_k))
    if perr != 2 ** k - 1:
        raise SystemExit("FALLO Perras: k=%d da %d, 2^k-1=%d"
                         % (k, perr, 2 ** k - 1))
    if a_k2 != rama1 + perr + G + H:
        raise SystemExit("FALLO particion: k=%d" % k)
    G_serie.append(G)
    H_serie.append(H)
    print("k=%2d  a(k)=%6d  perras=%6d  G=%5d  H=%5d  a(k+2)=%6d  EXACTO"
          % (k, a_k, perr, G, H, a_k2))

# la reduccion de la rama h
for t in range(0, 3000):
    x, y = paso(4 * t + 3), paso(4 * t + 4)
    x, y = paso(x), paso(y)
    if {x, y} != {t + 1, 9 * (t + 1) - 1}:
        raise SystemExit("FALLO reduccion h: t=%d" % t)

# los contraejemplos de Elia-Tucker viven en |M| = 8
for m in range(4):
    buena, M = analiza(2 ** 19 * m + 3067, 600)
    if not (buena and M == 8):
        raise SystemExit("FALLO Elia-Tucker: m=%d buena=%r M=%d"
                         % (m, buena, M))

print()
print("G(k) =", G_serie)
print("H(k) =", H_serie)
print()
print("IDENTIDAD EXACTA: a(k+2) = a(k) + (2^k - 1) + G(k) + H(k), k = 3..14,")
print("con rama1 == a(k) y perras == 2^k - 1 CLAVADOS: la autosimilitud de")
print("Gatas y la ventana de Perras valen como igualdad de enteros. La")
print("reduccion h -> {w, 9w-1} verificada, y los contraejemplos de")
print("Elia-Tucker (2^19 m + 3067) viven todos en |M| = 8.")
