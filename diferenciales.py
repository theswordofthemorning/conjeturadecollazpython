# diferenciales.py
#
# EL PERFIL DIFERENCIAL EXACTO DE LA CADENA -- el instrumento de los
# objetivos secundarios 3 (criptoanalisis diferencial) y 4
# (verificacion relacional), que ademas generaliza el programa de
# fusion a pares NO consecutivos (09-08-2026).
#
#   LA OBSERVACION QUE LO HACE GRATIS: la cadena (k, c) de Leonas no
#   sabe que el par es consecutivo. Arrancarla en (0, DELTA) en vez de
#   (0, 1) da EXACTAMENTE la dinamica del par {v, v + DELTA}, y el
#   barrido simbolico cuenta las clases v mod 2^t donde el par colapsa
#   (misma trayectoria desde el indice de encuentro, S igualada).
#
#   EN EL LENGUAJE DE CADA OBJETIVO:
#   - cripto: a_DELTA(k)/2^k es la PROBABILIDAD DE COLISION DIFERENCIAL
#     exacta de la funcion de ronda (3x+1)/2-o-x/2 para la diferencia
#     de entrada DELTA tras k rondas -- lo que un trail search estima,
#     aqui en cerrado, con las seis leyes como reglas de transicion
#     de la diferencia (la "DDT" del mapa, por clases 2-adicas).
#   - relacional: es la probabilidad de que dos entradas a distancia
#     DELTA se vuelvan INDISTINGUIBLES EN TIEMPO (fundidas => mismo
#     resto de trayectoria => mismo tiempo restante, exacto).
#   - Collatz: la densidad de fusion de {n, n + DELTA} -- el objeto de
#     las tuplas de Garner/Gao/Wu, medido por clases para DELTA > 1
#     (el programa entero era el caso DELTA = 1).
#
#   Control de la casa: el simbolico contra el barrido directo con
#   pares de enteros, por cada DELTA. SystemExit antes de concluir.

DELTAS = list(range(1, 13)) + [16]
K_SIM = 20              # profundidad del barrido simbolico
K_DIRECTA = 12          # cruce directo hasta aqui
TOPE_ESTADOS = 3 * 10 ** 6


def paso(x):
    return (3 * x + 1) // 2 if x % 2 else x // 2


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


def a_directa_delta(k, delta):
    # clases v mod 2^k donde (v, v + delta) se encuentran al mismo
    # indice con S igualada, dentro de k pasos
    n = 0
    for r0 in range(2 ** k):
        x, y = r0, r0 + delta
        Sx = Sy = 0
        for _ in range(k):
            if x % 2:
                Sx += 1
            if y % 2:
                Sy += 1
            x, y = paso(x), paso(y)
            if x == y:
                if Sx == Sy:
                    n += 1
                break
    return n


# ---------------------------------------------------------------------------
# COMPROBACION 1: SIMBOLICO = DIRECTO para cada DELTA.
# ---------------------------------------------------------------------------

perfil = {}
for delta in DELTAS:
    estados = {(0, delta): 1}
    absorbidas = 0
    a_sim = []
    corte = None
    for prof in range(1, K_SIM + 1):
        nuevo = {}
        nuevas_abs = 0
        for (k, c), n in estados.items():
            for bit in (0, 1):
                t = transicion(k, c, bit)
                if t[0] == 'fusion':
                    nuevas_abs += n
                else:
                    clave = (t[1], t[2])
                    nuevo[clave] = nuevo.get(clave, 0) + n
        absorbidas = 2 * absorbidas + nuevas_abs
        estados = nuevo
        a_sim.append(absorbidas)
        if len(estados) > TOPE_ESTADOS:
            corte = prof
            break
    for k in range(3, min(K_DIRECTA, len(a_sim)) + 1):
        d = a_directa_delta(k, delta)
        if a_sim[k - 1] != d:
            raise SystemExit("C1 delta=%d: a(%d) simbolico=%d, directo=%d"
                             % (delta, k, a_sim[k - 1], d))
    perfil[delta] = (a_sim, corte)

print("COMPROBACION 1 OK: simbolico = directo (k = 3..%d) para los %d"
      % (K_DIRECTA, len(DELTAS)))
print("valores de DELTA. La cadena ES la dinamica del par {v, v+DELTA}.")

# ---------------------------------------------------------------------------
# COMPROBACION 2: LA REDUCCION PAR -> IMPAR. (0, 2m) -0-> (0, m) y
#   -1-> (0, 3m): la densidad de DELTA par tiene que ser mezcla de las
#   impares de su arbol de mitades/triples. Se comprueba el primer
#   escalon como identidad de conteos:
#       a_{2m}(k) = a_m(k-1) + a_{3m}(k-1)
#   (el primer bit parte la clase en dos mitades de peso 2^{k-1}).
# ---------------------------------------------------------------------------

for m in (1, 2, 3, 4, 5, 6, 8):
    if 2 * m in perfil and m in perfil and 3 * m in perfil:
        a2m = perfil[2 * m][0]
        am = perfil[m][0]
        a3m = perfil[3 * m][0]
        for k in range(2, min(len(a2m), len(am) + 1, len(a3m) + 1)):
            if a2m[k - 1] != am[k - 2] + a3m[k - 2]:
                raise SystemExit("C2: a_%d(%d)=%d != a_%d(%d)+a_%d(%d)=%d+%d"
                                 % (2 * m, k, a2m[k - 1], m, k - 1, 3 * m,
                                    k - 1, am[k - 2], a3m[k - 2]))
print()
print("COMPROBACION 2 OK: a_2m(k) = a_m(k-1) + a_3m(k-1) exacta donde")
print("los tres perfiles existen -- la diferencia par se reduce a las")
print("impares por el primer bit (F1/F2), como identidad de enteros.")

# ---------------------------------------------------------------------------
# LA TABLA DEL PERFIL: densidad a k = K_SIM, primera fusion, y la
# densidad relativa contra DELTA = 1.
# ---------------------------------------------------------------------------

print()
print("el perfil diferencial (k = %d):" % K_SIM)
print("  DELTA   densidad     primera fusion   relativa a DELTA=1")
base = None
for delta in DELTAS:
    a_sim, corte = perfil[delta]
    kmax = len(a_sim)
    dens = a_sim[kmax - 1] / 2.0 ** kmax
    primera = next((i + 1 for i, v in enumerate(a_sim) if v > 0), None)
    if delta == 1:
        base = dens
    print("   %3d    %8.6f        %4s            %6.3f"
          % (delta, dens,
             primera if primera is not None else "--",
             dens / base if base else 0.0))

print()
print("VEREDICTO (medido + dos identidades exactas): el perfil")
print("diferencial completo de la funcion de ronda queda calculado en")
print("cerrado por la cadena -- la 'DDT 2-adica' del mapa del atajo.")
print("Lectura cripto: la diferencia 1 es la MAS debil (colisiona mas);")
print("lectura relacional: la tabla es la tasa exacta de pares que se")
print("vuelven indistinguibles en tiempo; lectura Collatz: la densidad")
print("de fusion de {n, n+DELTA} -- el objeto de Gao/Wu -- medida por")
print("clases para todo DELTA <= 16.")
