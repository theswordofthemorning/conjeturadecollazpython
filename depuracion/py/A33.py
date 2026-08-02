# -----------------------------------------------------------------------------
# A33 (agente 2, independiente): verificar
#
#   ENUNCIADO: a(k) >= 1 para todo k: el resto 2^k - 1 sobrevive siempre a la
#   criba de Brown/Terras, luego la criba NUNCA se vacia.
#
# MAPA USADO: el ATAJO  T(n) = n/2 si n par, (3n+1)/2 si n impar.
#   (La criba de Brown/Terras se define sobre este mapa: los primeros k pasos
#   de n los decide n mod 2^k, y una clase se descarta cuando el coeficiente
#   lambda_j = 3^{S_j}/2^j baja de 1, porque entonces el descenso queda
#   garantizado para los n grandes de la clase.)
#
# CRITERIO DE LA CRIBA (derivado desde la definicion, no copiado):
#   r mod 2^k se ELIMINA si existe j con 1 <= j <= k tal que 3^{S_j(r)} < 2^j,
#   donde S_j(r) = numero de pasos impares entre los primeros j pasos de r.
#   a(k) = cuantos restos de 0..2^k-1 NO se eliminan.
#
# Todo lo que decide es aritmetica entera exacta. Ningun float decide nada.
# -----------------------------------------------------------------------------

import random

def T(n):
    # mapa del atajo, valido tambien para negativos porque el paso impar
    # produce 3n+1 par y el par divide un par: la division nunca redondea
    if n % 2 == 0:
        return n // 2
    else:
        return (3 * n + 1) // 2

def vector_paridad(x, k):
    v = []
    for _ in range(k):
        v.append(x & 1)
        x = T(x)
    return v

fallos = 0

# --- COMPROBACION 0: la base de la criba (Terras): el vector de paridad de los
#     primeros k pasos depende solo de n mod 2^k. Muestreo con m aleatorios.
random.seed(33)
casos0 = 0
for k in (1, 2, 3, 5, 8, 10, 12):
    for _ in range(60):
        r = random.randrange(2 ** k)
        m = random.randrange(0, 10 ** 6)   # incluye m = 0 (el borde)
        if vector_paridad(r, k) != vector_paridad((2 ** k) * m + r, k):
            print("FALLO comprobacion 0: k=%d r=%d m=%d" % (k, r, m))
            fallos += 1
        casos0 += 1
print("comprobacion 0 (vector de paridad depende solo del resto): %d casos, %d fallos" % (casos0, fallos))
if fallos:
    raise SystemExit("la base de la criba no se sostiene; no sigo")

# --- COMPROBACION 1: criba exhaustiva para k = 0..KMAX.
#     Para cada k: contar supervivientes, comprobar a(k) >= 1, y comprobar que
#     el resto 2^k - 1 esta entre ellos. De paso: que el resto 0 NO sobrevive
#     para k >= 1 (control de que la criba muerde algo).
KMAX = 18
pow3 = [3 ** i for i in range(KMAX + 2)]
pow2 = [2 ** i for i in range(KMAX + 2)]

print("")
print(" k      a(k)   sobrevive 2^k-1?   sobrevive 0?")
conteos = []
for k in range(0, KMAX + 1):
    supervivientes = 0
    objetivo_vivo = False
    cero_vivo = False
    objetivo = pow2[k] - 1
    for r in range(pow2[k]):
        x = r
        S = 0
        vivo = True
        for j in range(1, k + 1):
            if x & 1:
                S += 1
            x = T(x)
            if pow3[S] < pow2[j]:
                vivo = False
                break
        if vivo:
            supervivientes += 1
            if r == objetivo:
                objetivo_vivo = True
            if r == 0:
                cero_vivo = True
    conteos.append(supervivientes)
    print("%2d  %8d   %s   %s" % (k, supervivientes,
                                  "SI " if objetivo_vivo else "NO!",
                                  "si (mal si k>=1)" if cero_vivo else "no"))
    if supervivientes < 1:
        print("FALLO: a(%d) = 0, la criba se vacio" % k)
        fallos += 1
    if not objetivo_vivo:
        print("FALLO: el resto 2^%d - 1 = %d NO sobrevive" % (k, objetivo))
        fallos += 1
    if k >= 1 and cero_vivo:
        print("FALLO DE CONTROL: el resto 0 sobrevive con k = %d y no deberia" % k)
        fallos += 1

print("")
print("a(k) para k = 0..%d: %s" % (KMAX, conteos))

# --- COMPROBACION 2: la estructura que hace que 2^k - 1 sobreviva PARA TODO k,
#     comprobada numericamente a k grande (mas alla de lo exhaustivo):
#     T^j(2^k - 1) = 3^j * 2^(k-j) - 1 para j = 0..k, todos los iterados
#     intermedios son impares (S_j = j), la trayectoria SUBE k veces seguidas,
#     y 3^j > 2^j para todo j >= 1 (luego el criterio de descarte nunca salta).
print("")
for k in (1, 2, 63, 64, 500, 4000):
    x = (1 << k) - 1
    ok = True
    prev = x
    for j in range(1, k + 1):
        if x % 2 != 1:          # antes del paso j el valor debe ser impar
            ok = False
            print("FALLO: k=%d, iterado %d es par" % (k, j - 1))
            break
        x = T(x)
        if x != pow(3, j) * (1 << (k - j)) - 1:   # forma cerrada
            ok = False
            print("FALLO: k=%d, forma cerrada rota en j=%d" % (k, j))
            break
        if j < k and x <= prev:  # sube en cada uno de los k primeros pasos
            ok = False
            print("FALLO: k=%d, no sube en el paso %d" % (k, j))
            break
        prev = x
        if not (pow(3, j) > pow(2, j)):
            ok = False
            print("FALLO: 3^%d <= 2^%d ???" % (j, j))
            break
    if not ok:
        fallos += 1
    print("k = %4d: 2^k-1 da S_j = j en los k pasos, forma cerrada exacta, sube las %d veces -> %s"
          % (k, k, "OK" if ok else "FALLO"))

# --- COMPROBACION 3 (la nota del circulo): el unico objeto con 'todo unos' en
#     binario para TODO k es -1, y es punto fijo impar del atajo: T(-1) = -1.
print("")
print("T(-1) = %d  (punto fijo impar del atajo: %s)" % (T(-1), "OK" if T(-1) == -1 else "FALLO"))
if T(-1) != -1:
    fallos += 1

# --- BORDES declarados:
#     k = 0: mod 1 hay un solo resto (0), sin pasos que criben -> a(0) = 1 por
#            convencion vacia; el enunciado vive en k >= 1.
#     k = 1: el resto 1 = 2^1 - 1 sobrevive (3 > 2) y el 0 muere (3^0 < 2).
#     n = 1: OJO, 1 = 2^1 - 1 sobrevive a la criba aunque este en el ciclo
#            trivial; la criba mide 'descenso garantizado', no convergencia.

print("")
if fallos == 0:
    print("VEREDICTO LOCAL: 0 fallos. a(k) >= 1 con testigo 2^k - 1, exhaustivo k = 0..%d," % KMAX)
    print("y la estructura (S_j = j, 3^j > 2^j) comprobada exacta hasta k = 4000.")
else:
    raise SystemExit("HUBO %d FALLOS" % fallos)
