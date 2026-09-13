# pisoporarranque.py
#
# EL TEST DECISIVO DE gamma -- el piso por arranque (lema L-A), la escalera
# de decadas con horizonte EMPAREJADO (11-08-2026; protocolo definido por
# la 7a revision y la bitacora 10-08 (16)).
#
#   EL LEMA QUE SE TANTEA (L-A de la reduccion del 10-08 (13)):
#       phi(c0) = P(la excursion desde (2, c0) aterriza en la ventana
#                   de Doeblin al volver al fondo)  >=  C * c0^(-gamma)
#   con gamma(c0) -> 0. Corrección 13-09-2026: el ajuste finito de la
#   revisión 7 no excluye una forma asintótica 1/sqrt(log). Una tendencia
#   medida de gamma no decide phi: hacen falta riesgos condicionales y
#   control de los arranques visitados. Véase ESTADO_INVESTIGACION.md.
#
#   EL PROTOCOLO (el del cierre del 10-08, ahora como fichero del repo --
#   este instrumento vivia solo en la transcripcion aa6b725d y eso era
#   exactamente la "deuda de metodo" del 30-07):
#     - cadena (k, c) MODIFICADA: el vortice (1, 1) rebota a (2, 2) con
#       las dos monedas (bit 0 es N3 y da (2,2) igual; bit 1, que en la
#       cadena real FUSIONA, se rebota) -- la formulacion phi = 1 <=>
#       recurrencia de (1,1) (retorno11.py, 4a revision).
#     - masa entera exacta (conteo de palabras) desde (2, c0); la masa
#       que baja a k <= 1 SALE del barrido: exito si aterriza con
#       |c| <= K_VENTANA (la ventana de Doeblin de liebres.py), fracaso
#       si no. phi_min acumulada = COTA INFERIOR estricta del truncado.
#     - poda: se conservan los TOPE estados de mayor masa; lo podado se
#       acumula como 'perdida'. Cota superior del truncado = phi_min +
#       perdida; horquilla del limite = phi_min + perdida + masa viva.
#     - horizonte EMPAREJADO: todos los c0 con el MISMO T, para que el
#       sesgo de horizonte no fabrique la tendencia de gamma.
#
#   CONTROL DE REPRODUCCION (SystemExit): los tres puntos publicados del
#   cierre del 10-08 (bitacora (16)) se recomputan de paso -- a T = 130
#   este codigo debe dar phi_min = 0,1182 / 0,0586 / 0,0354 para
#   c0 = 2000 / 20000 / 200000. El calculo es determinista (enteros
#   exactos, poda por orden estable), asi que se exige la igualdad a
#   4 decimales, no un "parecido".
#
#   LA DECADA NUEVA: c0 = 2.000.000 con T = 150 (la contraccion media de
#   log(2e6)/0,144 son ~100 pasos; 150 deja margen), y los tres puntos
#   viejos re-corridos al MISMO T = 150 para la gamma emparejada.
#
#   ETIQUETA HONESTA (la leccion del muro de b(k), tres veces mordida):
#   tres decadas de tendencia NO son un limite. Este fichero mide; el
#   veredicto "gamma -> 0" solo puede darlo un mecanismo demostrado.
#   Y el aviso del punto 8 de la lista adversarial: los c0 de la
#   escalera son decadas redondas (v2(c0) sube exactamente 1 por
#   decada: 2000 = 2^4*125, ..., 2*10^6 = 2^7*15625); la comparacion
#   entre decadas arrastra ese desplazamiento sistematico de v2.
#   ⇢ MEDIDO POR LA 8a REVISION (adv 1) -- la frase original "sesgo
#   comun, no fabrica" estaba SIN medir: phi varia hasta x1,8 con v2
#   a magnitud fija (0,0519..0,0938 en ~2000), SE SATURA en v2 >= 4
#   (donde vive la escalera entera), y las gamma re-emparejadas por
#   v2 NO fabrican la caida. El sesgo es real, acotado, y no produce
#   la tendencia; para el valor absoluto de phi(c0) sigue siendo un
#   parametro del protocolo.
#
#   Mapa del ATAJO via la cadena simbolica; enteros exactos; SystemExit
#   antes de concluir.

import math
import time

# ---- las perillas ---------------------------------------------------------

C0_LISTA = [2000, 20000, 200000, 2000000]   # la escalera de decadas
T_MAX = 150                  # horizonte emparejado de esta pasada
TOPE = 2 * 10 ** 6           # estados vivos conservados por la poda
K_VENTANA = 25               # la ventana de Doeblin: k <= 1 y |c| <= 25

T_PUBLICADO = 130            # el horizonte del cierre del 10-08
PHI_PUBLICADA = {2000: 0.1182, 20000: 0.0586, 200000: 0.0354}

# ---------------------------------------------------------------------------
# la cadena modificada: las seis leyes de Leonas (paseodeladeuda.py) con el
# vortice rebotado. Duplicada a proposito (regla de la casa): se verifica
# abajo contra pares reales, no contra el otro fichero.
# ---------------------------------------------------------------------------


def transicion_mod(k, c, bit):
    if k == 0:
        if c % 2 == 0:
            return (0, c // 2) if bit == 0 else (0, 3 * c // 2)
        return (1, (3 * c + 1) // 2) if bit == 0 else (1, (1 - 3 * c) // 2)
    if c % 2 == 0:
        return (k, c // 2) if bit == 0 else (k, (3 * c + 1 - 3 ** k) // 2)
    if k == 1 and c == 1:
        return (2, 2)                      # el rebote: bit 0 es N3 y da lo
    if bit == 0:                           # mismo; bit 1 (fusion) se rebota
        return (k + 1, (3 * c + 1) // 2)
    if k >= 2:
        return (k - 1, (c - 3 ** (k - 1)) // 2)
    return (0, abs((c - 1) // 2))


def paso(x):
    return (3 * x + 1) // 2 if x % 2 else x // 2


# ---------------------------------------------------------------------------
# COMPROBACION 1: la cadena modificada contra pares reales.
#   Identica a la C1 de paseodeladeuda.py salvo el vortice: en (1, 1) el
#   bit 1 fusiona de verdad (se comprueba que fusiona) y aqui se rebota
#   POR CONSTRUCCION -- es la definicion de la cadena modificada, no una
#   ley que verificar contra pares.
# ---------------------------------------------------------------------------

probadas = 0
for k in range(0, 8):
    for c in range(1 if k == 0 else -60, 61):
        if c == 0 and k == 0:
            continue
        for v in range(200, 320):
            x, y = v, (3 ** k * v + c) if k >= 1 else v + c
            if y <= x:
                raise SystemExit("C1: forma invalida k=%d c=%d v=%d" % (k, c, v))
            nx, ny = paso(x), paso(y)
            if k == 1 and c == 1 and v % 2 == 1:
                if nx != ny:
                    raise SystemExit("C1 vortice: (1,1) bit 1 no fusiona, v=%d" % v)
                probadas += 1
                continue
            k2, c2 = transicion_mod(k, c, v % 2)
            lo, hi = min(nx, ny), max(nx, ny)
            objetivo = (3 ** k2 * lo + c2) if k2 >= 1 else lo + c2
            if hi != objetivo:
                raise SystemExit("C1 ley: (%d,%d) v=%d -> real (%d,%d), "
                                 "cadena (%d,%d)" % (k, c, v, lo, hi, k2, c2))
            probadas += 1

print("COMPROBACION 1 OK: la cadena modificada coincide con los pares")
print("reales en %d instancias (y el vortice con bit 1 fusiona de verdad" % probadas)
print("en todas las suyas: el rebote es construccion, no error).")

# ---------------------------------------------------------------------------
# EL BARRIDO PODADO, un c0 por vez.
#   vivos: estado -> numero entero de palabras (masa = n / 2^t, exacta).
#   La masa que baja a k <= 1 sale: 'ventana' si |c| <= K_VENTANA.
#   Poda por masa (orden estable de sorted): lo cortado va a 'perdida'.
# ---------------------------------------------------------------------------


def barrido(c0, t_max, tope):
    vivos = {(2, c0): 1}
    ventana = perdida = 0.0
    fotos = {}
    t0 = time.time()
    for t in range(1, t_max + 1):
        nuevo = {}
        for (k, c), n in vivos.items():
            for bit in (0, 1):
                kk, cc = transicion_mod(k, c, bit)
                if kk <= 1:
                    if abs(cc) <= K_VENTANA:
                        ventana += n / 2.0 ** t
                else:
                    nuevo[(kk, cc)] = nuevo.get((kk, cc), 0) + n
        if len(nuevo) > tope:
            pares = sorted(nuevo.items(), key=lambda kv: kv[1])
            cortar = len(nuevo) - tope
            perdida += sum(n for _, n in pares[:cortar]) / 2.0 ** t
            nuevo = dict(pares[cortar:])
        vivos = nuevo
        if t % 10 == 0 or t == t_max:
            viva = sum(vivos.values()) / 2.0 ** t if vivos else 0.0
            fotos[t] = (ventana, perdida, viva)
            print("  c0=%-8d t=%3d  phi_min=%.4f  perdida=%.3f  viva=%.3f"
                  "  [%.0f s]" % (c0, t, ventana, perdida, viva,
                                  time.time() - t0))
    return fotos


# COMPROBACION 2 (entretejida): la reproduccion de los tres puntos
# publicados (T = 130) se exige NADA MAS terminar cada barrido -- el
# calculo es determinista; si no clava los 4 decimales del cierre del
# 10-08, este fichero NO es el instrumento de la bitacora y no tiene
# derecho a seguir gastando la maquina.

resultados = {}
for c0 in C0_LISTA:
    print()
    print("--- barrido desde (2, %d), T = %d, tope %d ---" % (c0, T_MAX, TOPE))
    resultados[c0] = barrido(c0, T_MAX, TOPE)
    if c0 in PHI_PUBLICADA:
        phi_aqui = resultados[c0][T_PUBLICADO][0]
        if abs(phi_aqui - PHI_PUBLICADA[c0]) > 5e-5:
            raise SystemExit("C2 reproduccion: phi(%d) a T=%d da %.4f, "
                             "publicada %.4f"
                             % (c0, T_PUBLICADO, phi_aqui, PHI_PUBLICADA[c0]))
        print("  C2 OK: phi(%d) a T=%d reproduce el %.4f de la bitacora."
              % (c0, T_PUBLICADO, PHI_PUBLICADA[c0]))

# ---------------------------------------------------------------------------
# LA TABLA FINAL: la escalera emparejada a T_MAX y las gamma por decada.
#   gamma(decada) = log10(phi(c0) / phi(10 c0)) sobre las cotas
#   inferiores certificadas EMPAREJADAS. Horquilla del limite:
#   [phi_min, phi_min + perdida + viva].
# ---------------------------------------------------------------------------

print()
print("LA ESCALERA EMPAREJADA (T = %d, tope %d):" % (T_MAX, TOPE))
print("   c0         phi_min   horquilla del limite      perdida   viva")
for c0 in C0_LISTA:
    ven, per, viv = resultados[c0][T_MAX]
    print("  %-9d  %.4f    [%.4f, %.4f]           %.3f     %.3f"
          % (c0, ven, ven, ven + per + viv, per, viv))

print()
print("gamma por decada (cotas inferiores emparejadas a T = %d):" % T_MAX)
gammas = []
for a, b in zip(C0_LISTA, C0_LISTA[1:]):
    va, vb = resultados[a][T_MAX][0], resultados[b][T_MAX][0]
    g = math.log10(va / vb)
    gammas.append(g)
    print("  gamma(%d -> %d) = %.3f" % (a, b, g))

print()
if all(g2 < g1 for g1, g2 in zip(gammas, gammas[1:])):
    print("VEREDICTO DE LA PASADA: gamma CAE en cada escalon de la escalera")
    print("emparejada -- la direccion en la que la reduccion (13) vive.")
else:
    print("VEREDICTO DE LA PASADA: gamma NO cae monotonamente en esta")
    print("escalera -- el escalon que se resiste es el dato nuevo.")
print()
print("Etiqueta honesta: son cotas inferiores truncadas con horquillas que")
print("se solapan; tres decadas de tendencia no son un limite. El veredicto")
print("final de L-A pide mecanismo, no extrapolacion.")
