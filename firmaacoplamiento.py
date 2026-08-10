# firmaacoplamiento.py
#
# EL LEMA DEL ACOPLAMIENTO DE LA MONEDA (10-08-2026; propuesto:
# TORTOLAS -- las dos copias van juntas, inseparables, exactamente
# v2(Delta) pasos; el bautizo es del usuario). El paso estructural
# despues de monedacondicionada.py (GARZAS): el sesgo de la moneda
# condicionada NO es un misterio -- es un efecto de TIMING controlado
# por un acoplamiento exacto.
#
#   LEMA (verificado abajo; la demostracion es un caso por ley).
#   En la cadena modificada, los dos hijos de una moneda en (k, c par)
#   son (k, c/2) y (k, (3c+1-3^k)/2): MISMO k, diferencia
#
#       Delta = c + (1 - 3^k)/2.
#
#   Si Delta = 0 (c = (3^k-1)/2, que exige k par), los dos hijos son
#   EL MISMO estado: la moneda sin efecto. Si Delta != 0, bajo la
#   MISMA palabra de bits las dos copias:
#     - comparten trayectoria de k y paridad de c paso a paso,
#     - la diferencia evoluciona EXACTO Delta -> +-Delta/2 o
#       +-3*Delta/2 (las seis leyes son afines con parte lineal
#       +-1/2 o +-3/2, y las partes afines se cancelan porque el k
#       es comun), o sea v2(Delta) baja EXACTAMENTE 1 por paso,
#     - y las paridades divergen EXACTAMENTE en el paso
#       j* = v2(Delta) (paridades distintas <=> Delta impar),
#   SALVO dos eventos exceptuados, ambos raros y nombrados:
#     (E1) el vortice asimetrico: exactamente UNA copia pisa (1,1)
#          (alli la ley difiere: rebote contra paso normal);
#     (E2) el signo mixto: la salida k=1, c impar, bit 1 usa abs(g)
#          -- el UNICO valor absoluto de la cadena -- y si las dos
#          copias llegan con g de signos opuestos, la diferencia
#          salta (puede incluso coalescer Delta -> 0). En la
#          frontera no puede pasar: alli el gap es positivo siempre.
#
#   COROLARIO (la mitad del "ultimo paso" del acta de la 5a).
#   Si j* >= m (el horizonte restante hasta T), las trayectorias de
#   k de los dos hijos coinciden HASTA T, y el sesgo de esa moneda
#   respecto del objetivo fondo (k <= 1 en T) es EXACTAMENTE CERO --
#   salvo que E1/E2 ocurra antes. El sesgo entero de la moneda
#   condicionada es sensibilidad al TIMING del paseo critico de k, y
#   la pieza analitica que queda (acotarla a priori) queda DESACOPLADA
#   de la dinamica de c.
#
#   LA FIRMA MEDIDA (T = 28, objetivo fondo, corrida 10-08-2026):
#     sesgo por moneda contra j*: 0,0216 (j*=0) / 0,0171 (1) /
#     0,0075 (2) / ~0 (3+) -- cae con la vida del acoplamiento;
#     ceros exactos: 1315 de 1317 monedas-estado con j* >= horizonte
#     (99,85%), y las 2 violaciones (eventos E1/E2) cargan fraccion
#     de masa 2,2e-5.
#
# COMPROBACIONES (SystemExit antes de concluir):
#   C0  el lema contra la cadena real: rejilla k = 1..8, c par en
#       [-2000, 2000], 3 palabras pseudoaleatorias reproducibles por
#       estado (semilla 1): la divergencia ocurre EXACTAMENTE en j*
#       o un evento E1/E2 la interrumpe ANTES; cero fallos exigidos.
#   C1  conservacion de masa 2^s en el barrido.
#   C2  Delta = 0 => hijos identicos (en el barrido entero).
#   C3  la prediccion de ceros: al menos 99% de las monedas-estado
#       con j* >= horizonte con sesgo exactamente 0, y masa de
#       violaciones < 1e-4 de F.
#
# Mapa del ATAJO via la cadena de Leonas modificada; enteros exactos.

import random
import time

T = 28
FONDO_K = 1
K_REJILLA = 8
C_REJILLA = 2000
PALABRAS_POR_ESTADO = 3


def transicion_mod(k, c, bit):
    # la cadena de Leonas con el vortice rebotado (identica a
    # retorno11.py / lamperti.py / monedacondicionada.py)
    if k == 0:
        if c % 2 == 0:
            return (0, c // 2) if bit == 0 else (0, 3 * c // 2)
        return (1, (3 * c + 1) // 2) if bit == 0 else (1, (1 - 3 * c) // 2)
    if c % 2 == 0:
        return (k, c // 2) if bit == 0 else (k, (3 * c + 1 - 3 ** k) // 2)
    if k == 1 and c == 1:
        return (2, 2)
    if bit == 0:
        return (k + 1, (3 * c + 1) // 2)
    if k >= 2:
        return (k - 1, (c - 3 ** (k - 1)) // 2)
    return (0, abs((c - 1) // 2))


def v2(n):
    n = abs(n)
    j = 0
    while n % 2 == 0:
        n //= 2
        j += 1
    return j


# ---------------------------------------------------------------------------
# C0: EL LEMA CONTRA LA CADENA REAL.
# ---------------------------------------------------------------------------

random.seed(1)
t0 = time.time()
probados = 0
excepciones = {}
for k in range(1, K_REJILLA + 1):
    for c in range(-C_REJILLA, C_REJILLA + 1, 2):
        delta = c + (1 - 3 ** k) // 2
        if delta == 0:
            if transicion_mod(k, c, 0) != transicion_mod(k, c, 1):
                raise SystemExit("C0: Delta=0 con hijos distintos en (%d,%d)"
                                 % (k, c))
            continue
        js = v2(delta)
        for rep in range(PALABRAS_POR_ESTADO):
            bits = [random.randint(0, 1) for _ in range(js + 12)]
            e0 = transicion_mod(k, c, 0)
            e1 = transicion_mod(k, c, 1)
            if e0[0] != e1[0]:
                raise SystemExit("C0: hijos con k distinto en (%d,%d)" % (k, c))
            resultado = None
            for j, b in enumerate(bits):
                if e0 == e1:
                    resultado = ('coalescencia', j)
                    break
                if e0[1] % 2 != e1[1] % 2:
                    resultado = ('divergencia', j)
                    break
                v0 = (e0[0] == 1 and e0[1] == 1)
                v1 = (e1[0] == 1 and e1[1] == 1)
                if v0 != v1:
                    resultado = ('E1 vortice asimetrico', j)
                    break
                if e0[0] == 1 and e0[1] % 2 == 1 and b == 1 and not v0:
                    g0, g1 = (e0[1] - 1) // 2, (e1[1] - 1) // 2
                    if g0 * g1 < 0:
                        resultado = ('E2 signo mixto', j)
                        break
                e0 = transicion_mod(e0[0], e0[1], b)
                e1 = transicion_mod(e1[0], e1[1], b)
            probados += 1
            if resultado is None:
                raise SystemExit("C0: ni divergencia ni excepcion en (%d,%d), "
                                 "js=%d" % (k, c, js))
            tipo, j = resultado
            if tipo == 'divergencia':
                if j != js:
                    raise SystemExit("C0: (%d,%d) js=%d divergio en %d"
                                     % (k, c, js, j))
            else:
                excepciones[tipo] = excepciones.get(tipo, 0) + 1
                if j >= js:
                    raise SystemExit("C0: excepcion %s DESPUES de js en (%d,%d)"
                                     % (tipo, k, c))

print("COMPROBACION 0 OK: el lema del acoplamiento clavado en %d pruebas"
      % probados)
print("(k = 1..%d, c par en [-%d, %d], %d palabras por estado): la"
      % (K_REJILLA, C_REJILLA, C_REJILLA, PALABRAS_POR_ESTADO))
print("divergencia de paridades ocurre EXACTAMENTE en j* = v2(Delta), y las")
print("unicas interrupciones son los eventos exceptuados: %s" % (excepciones,))

# ---------------------------------------------------------------------------
# EL BARRIDO Y LA FIRMA: forward, backward del fondo, sesgo por j*.
# ---------------------------------------------------------------------------

niveles = [None] * (T + 1)
niveles[0] = {(0, 1): 1}
for s in range(T):
    nuevo = {}
    for (k, c), n in niveles[s].items():
        for bit in (0, 1):
            clave = transicion_mod(k, c, bit)
            nuevo[clave] = nuevo.get(clave, 0) + n
    niveles[s + 1] = nuevo
for s in range(T + 1):
    if sum(niveles[s].values()) != 2 ** s:
        raise SystemExit("C1: masa no conservada en s = %d" % s)
print()
print("COMPROBACION 1 OK: masa 2^s conservada en los %d niveles." % (T + 1))

gama = dict((x, 1 if x[0] <= FONDO_K else 0) for x in niveles[T])
F = sum(niveles[T][x] * g for x, g in gama.items())

num = {}
den = {}
ceros_pred = 0
ceros_ok = 0
ceros_masa_mal = 0

for s in range(T - 1, -1, -1):
    m = T - s - 1
    gnuevo = {}
    for x, a in niveles[s].items():
        k, c = x
        h0 = transicion_mod(k, c, 0)
        h1 = transicion_mod(k, c, 1)
        g0 = gama.get(h0, 0)
        g1 = gama.get(h1, 0)
        gnuevo[x] = g0 + g1
        if g0 == 0 and g1 == 0:
            continue
        if not (k == 1 and c == 1) and c % 2 == 0:
            delta = c + (1 - 3 ** k) // 2
            if delta == 0:
                cub = 'inf'
                if g0 != g1:
                    raise SystemExit("C2: Delta=0 con gama distinta en (%d,%d)"
                                     % (k, c))
            else:
                js = v2(delta)
                cub = js if js < 8 else '8+'
                if js >= m:
                    ceros_pred += 1
                    if g1 == g0:
                        ceros_ok += 1
                    else:
                        ceros_masa_mal += abs(a * (g1 - g0))
            num[cub] = num.get(cub, 0) + a * (g1 - g0)
            den[cub] = den.get(cub, 0) + a * (g0 + g1)
    gama = gnuevo

print("COMPROBACION 2 OK: Delta = 0 => los dos hijos con la misma gama, en")
print("todo el barrido (la moneda sin efecto es sin efecto).")

if ceros_ok < 0.99 * ceros_pred or ceros_masa_mal > 1e-4 * F:
    raise SystemExit("C3: la prediccion de ceros falla: %d/%d, masa %.3e/F"
                     % (ceros_ok, ceros_pred, ceros_masa_mal / (1.0 * F)))
print("COMPROBACION 3 OK: %d de %d monedas-estado con j* >= horizonte tienen"
      % (ceros_ok, ceros_pred))
print("sesgo EXACTAMENTE cero (%.2f%%); la masa de las violaciones (eventos"
      % (100.0 * ceros_ok / max(1, ceros_pred)))
print("E1/E2) es %.2e de F." % (ceros_masa_mal / (1.0 * F)))

print()
print("LA FIRMA (objetivo fondo, T = %d): sesgo por moneda contra j*" % T)
print("  j*    monedas/palabra   sesgo por moneda")
for cub in list(range(8)) + ['8+', 'inf']:
    if cub not in den or den[cub] == 0:
        continue
    print(" %3s       %9.4f        %+9.6f"
          % (str(cub), den[cub] / (1.0 * F), num[cub] / (1.0 * den[cub])))

print()
print("VEREDICTO: el sesgo de la moneda condicionada al fondo es un efecto")
print("de TIMING controlado por el acoplamiento: cae con j* en las cubetas")
print("con masa (0,0216 / 0,0171 / 0,0075 / ~0), es EXACTAMENTE cero cuando")
print("el acoplamiento sobrevive al horizonte, y las unicas fugas son los")
print("dos eventos exceptuados, con masa 2e-5. La pieza analitica que queda")
print("-- acotar a priori la sensibilidad al timing del paseo critico de k --")
print("queda desacoplada de la dinamica de c. (Todo esto MIDE y estructura;")
print("no decide phi.)")
print("%.0fs" % (time.time() - t0))
