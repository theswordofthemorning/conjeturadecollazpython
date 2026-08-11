# adv1_recargas.py -- 9a revision, adversario 1
#
# ATAQUES 1, 2 y 3 contra notadominacion.txt / rachasreales.py:
#   A1: la aritmetica de la recarga. La Pieza A dice
#         racha <= v2(entrada) + (A-1)*[se cruzo v=A]
#       y "solo puede dispararse una vez por pasada". Se mide:
#       (a) recargas MULTIPLES por racha (conteo exacto),
#       (b) el salto de una recarga (v2_despues - (v2_antes - 1)),
#           que la cancelacion hace ILIMITADO,
#       (c) el exceso maximo contra el techo A-1 con el A REALIZADO.
#   A2: la censura del censo. rachasreales.py descarta la racha
#       abierta al terminar el bucle. Se mide cuantas y de que largo
#       (el sesgo de inspeccion: las largas quedan fuera mas a menudo)
#       y cuanto mueve la cola C_j incluirlas.
#   A3: dependencia que C4 no ve: C_j condicional al BIT del mixto
#       que abrio la racha (en V2b el reloj es independiente del bit;
#       en la cadena real c' depende del bit -> si la ley de racha
#       depende del bit, el h-transform la cambia y el "pasa intacta"
#       de la nota 5(iii) queda tocado), y condicional a las DOS
#       rachas anteriores.
#
# MISMA dinamica, mismo arranque y misma semilla que rachasreales.py
# (reproduccion exacta del stream: un getrandbits(1) por paso).
# Solo se INSTRUMENTA; no se toca ningun fichero del repo.

import math
import random

C0 = 999983
N_EXCURSIONES = 150000
T_MAX = 600
J_MAX = 12
MINIMO_MUESTRA = 200
SEMILLA = 20260814


def pot3(k, _cache={0: 1}):
    if k not in _cache:
        _cache[k] = 3 ** k
    return _cache[k]


def transicion(k, c, bit):
    if k == 0:
        if c % 2 == 0:
            return (0, c // 2) if bit == 0 else (0, 3 * c // 2)
        return (1, (3 * c + 1) // 2) if bit == 0 else (1, (1 - 3 * c) // 2)
    if c % 2 == 0:
        return (k, c // 2) if bit == 0 else (k, (3 * c + 1 - pot3(k)) // 2)
    if bit == 0:
        return (k + 1, (3 * c + 1) // 2)
    if k >= 2:
        return (k - 1, (c - pot3(k - 1)) // 2)
    g = (c - 1) // 2
    if g == 0:
        return None
    return (0, abs(g))


def v2_de(n):
    if n == 0:
        return 99
    v = 0
    while n % 2 == 0:
        n //= 2
        v += 1
    return v


def A_de(k, _cache={}):
    if k not in _cache:
        _cache[k] = v2_de(pot3(k) - 1)
    return _cache[k]


azar = random.Random(SEMILLA)

# censos
rachas_cerradas = {}                 # largo -> n (las que el repo cuenta)
rachas_censuradas = {}               # largo -> n (abiertas al cortar T_MAX)
abiertas_en_fondo = {}               # largo -> n (abiertas al pisar k <= 1)
por_bit = {0: {}, 1: {}}             # bit del mixto de apertura -> censo
por_A = {}                           # A(k_racha) -> censo
por_par_anterior = {}                # (bucket(ant2), bucket(ant1)) -> censo
recargas_por_racha = {}              # n_recargas -> n rachas
salto_max_global = 0
salto_hist = {}                      # salto de UNA recarga -> n
exceso_por_A = {}                    # A -> exceso maximo observado
max_k_visto = 0
max_A_visto = 0
detalle_exceso_max = None
exceso_max = 0
total = 0


def bucket(x):
    if x is None:
        return 9
    if x == 0:
        return 0
    if x <= 2:
        return 1
    if x <= 5:
        return 2
    return 3


for _ in range(N_EXCURSIONES):
    k, c = 2, C0
    racha = None
    k_racha = None
    v2_entrada = None
    bit_apertura = None
    n_rec = 0
    salto_tot = 0
    ant1 = ant2 = None
    fin = None
    for t in range(T_MAX):
        k0 = k
        bit = azar.getrandbits(1)
        # instrumentacion ANTES del paso: v2 y si es compartido
        v_antes = v2_de(c) if c != 0 else 99
        r = transicion(k, c, bit)
        if r is None:
            fin = 'fondo'
            break
        k, c = r
        if k == k0:
            if racha is not None:
                racha += 1
                v_desp = v2_de(c) if c != 0 else 99
                delta = v_desp - v_antes
                if delta >= 0:                     # RECARGA
                    n_rec += 1
                    salto = v_desp - (v_antes - 1)
                    salto_tot += salto
                    salto_hist[salto] = salto_hist.get(salto, 0) + 1
                    salto_max_global = max(salto_max_global, salto)
        else:
            if racha is not None:
                rachas_cerradas[racha] = rachas_cerradas.get(racha, 0) + 1
                total += 1
                A = A_de(k_racha)
                max_A_visto = max(max_A_visto, A)
                por_A.setdefault(A, {})[racha] = \
                    por_A.setdefault(A, {}).get(racha, 0) + 1
                por_bit[bit_apertura][racha] = \
                    por_bit[bit_apertura].get(racha, 0) + 1
                if ant1 is not None:
                    llave = (bucket(ant2), bucket(ant1))
                    por_par_anterior.setdefault(llave, {})[racha] = \
                        por_par_anterior.setdefault(llave, {}).get(racha, 0) + 1
                recargas_por_racha[n_rec] = \
                    recargas_por_racha.get(n_rec, 0) + 1
                if racha > v2_entrada:
                    exc = racha - v2_entrada
                    if exc > exceso_max:
                        exceso_max = exc
                        detalle_exceso_max = (v2_entrada, racha, A,
                                              k_racha, n_rec, salto_tot)
                    exceso_por_A[A] = max(exceso_por_A.get(A, 0), exc)
                ant2, ant1 = ant1, racha
            racha = 0
            k_racha = k
            v2_entrada = v2_de(c) if c != 0 else 99
            bit_apertura = bit
            n_rec = 0
            salto_tot = 0
        max_k_visto = max(max_k_visto, k)
        if k <= 1:
            fin = 'fondo'
            break
    if fin is None:
        fin = 'censura'
    # la racha abierta al terminar: donde el repo hace break sin cerrar
    if racha is not None:
        if fin == 'fondo':
            abiertas_en_fondo[racha] = abiertas_en_fondo.get(racha, 0) + 1
        else:
            rachas_censuradas[racha] = rachas_censuradas.get(racha, 0) + 1

print("ADV1 -- LA RECARGA, LA CENSURA Y EL BIT (semilla %d, %d exc.)"
      % (SEMILLA, N_EXCURSIONES))
print()
print("== ATAQUE 1: la recarga ==")
print("k maximo visitado: %d;  A maximo realizado: %d  (techo A-1 = %d)"
      % (max_k_visto, max_A_visto, max_A_visto - 1))
print("rachas por numero de recargas:")
for n in sorted(recargas_por_racha):
    print("  %d recargas: %d rachas" % (n, recargas_por_racha[n]))
multi = sum(v for n, v in recargas_por_racha.items() if n >= 2)
print("rachas con RECARGA MULTIPLE (>= 2): %d  (la nota dice 'solo una"
      % multi)
print("vez por pasada')")
print("histograma del salto de UNA recarga (v2 gana s respecto del")
print("descenso normal):")
for s in sorted(salto_hist):
    print("  salto %2d: %d veces" % (s, salto_hist[s]))
print("salto maximo de UNA sola recarga: %d  (la nota lo acota por A-1 <= %d)"
      % (salto_max_global, max_A_visto - 1))
print("exceso maximo racha - v2_entrada: %d" % exceso_max)
if detalle_exceso_max:
    v2e, ra, A, kk, nr, st = detalle_exceso_max
    print("  el evento: v2_entrada = %d, racha = %d, A = %d, k = %d,"
          % (v2e, ra, A, kk))
    print("  recargas en esa racha = %d, salto acumulado = %d" % (nr, st))
print("exceso maximo por valor de A:")
for A in sorted(exceso_por_A):
    print("  A = %2d: exceso max %d  (techo de la nota: %d)"
          % (A, exceso_por_A[A], A - 1))
print()

print("== ATAQUE 2: la censura del censo ==")
n_fondo = sum(abiertas_en_fondo.values())
n_cens = sum(rachas_censuradas.values())
print("rachas abiertas al pisar el fondo: %d (largos: %s)"
      % (n_fondo, dict(sorted(abiertas_en_fondo.items())[:8])))
print("rachas abiertas al cortar T_MAX = %d: %d" % (T_MAX, n_cens))
if n_cens:
    media_cens = sum(l * n for l, n in rachas_censuradas.items()) \
        / float(n_cens)
    media_cerr = sum(l * n for l, n in rachas_cerradas.items()) / float(total)
    print("  largo medio censurado: %.3f  contra %.3f de las cerradas"
          % (media_cens, media_cerr))
    print("  largos censurados grandes: %s"
          % sorted((l for l in rachas_censuradas for _ in
                    range(rachas_censuradas[l]) if l >= 8), reverse=True)[:20])


def cola(tabla):
    n = sum(tabla.values())
    acum = {}
    vivos = n
    for j in range(0, J_MAX + 1):
        acum[j] = vivos / float(n) if n else 0.0
        vivos -= tabla.get(j, 0)
    return n, acum


# la cola con las censuradas incluidas como cota inferior (una racha
# censurada de largo L cuenta en P(racha >= j) para j <= L)
mezcla = dict(rachas_cerradas)
for l, n in rachas_censuradas.items():
    mezcla[l] = mezcla.get(l, 0) + n
n_m, cola_m = cola(mezcla)
n_c, cola_c = cola(rachas_cerradas)
print("C_j sin censuradas / con censuradas (el sesgo de inspeccion):")
for j in range(8, J_MAX + 1):
    print("  j = %2d:  %.3f  /  %.3f" % (j, cola_c[j] * 2 ** j,
                                         cola_m[j] * 2 ** j))
print()

print("== ATAQUE 3: dependencias que C4 no mira ==")
print("(a) por BIT del mixto de apertura (V2b los supone independientes):")
for b in (0, 1):
    n_b, cola_b = cola(por_bit[b])
    media_b = sum(l * n for l, n in por_bit[b].items()) / float(n_b)
    peor = 0.0
    for j in range(1, J_MAX + 1):
        if cola_b[j] * n_b >= MINIMO_MUESTRA:
            peor = max(peor, cola_b[j] * 2 ** j)
    print("  bit %d: %8d rachas, media %.3f, C_j max %.3f, "
          "P(>=1) = %.4f, P(>=6) = %.5f"
          % (b, n_b, media_b, peor, cola_b[1], cola_b[6]))
print("(b) por valor de A = v2(3^k - 1) (la franja por k de C2 NO es esto):")
for A in sorted(por_A):
    n_A, cola_A = cola(por_A[A])
    media_A = sum(l * n for l, n in por_A[A].items()) / float(n_A)
    peor = 0.0
    for j in range(1, J_MAX + 1):
        if cola_A[j] * n_A >= MINIMO_MUESTRA:
            peor = max(peor, cola_A[j] * 2 ** j)
    print("  A = %2d: %8d rachas, media %.3f, C_j max %.3f"
          % (A, n_A, media_A, peor))
print("(c) por el PAR de rachas anteriores (bucket 0/1/2/3 = 0,1-2,3-5,>=6):")
for llave in sorted(por_par_anterior):
    tabla = por_par_anterior[llave]
    n_p, cola_p = cola(tabla)
    if n_p < 5000:
        continue
    peor = 0.0
    for j in range(1, J_MAX + 1):
        if cola_p[j] * n_p >= MINIMO_MUESTRA:
            peor = max(peor, cola_p[j] * 2 ** j)
    media_p = sum(l * n for l, n in tabla.items()) / float(n_p)
    print("  ant2 %s ant1 %s: %8d rachas, media %.3f, C_j max %.3f"
          % (llave[0], llave[1], n_p, media_p, peor))
print()
print("total de rachas cerradas: %d (el repo dijo 3860014)" % total)
