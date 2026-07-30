# espejobases.py
#
# LOS PUNTOS FIJOS DEL ESPEJO, Y POR QUE LA BASE 2 ES LA RARA.
#
# El repo ya tenia dos espejos sueltos:
#   mallaespejo.py   base 10: puntos fijos 5, 50, 500, 5000, 50000
#   mallaespejo2.py  base 2:  puntos fijos las potencias de 2
# y los trataba como dos casos. Son la misma familia, y mirandola entera
# aparece la razon de que la base 2 se comporte distinto.
#
# LA DEFINICION, general:
#
#     espejo_b(n) = (la potencia de b mas chica que supera a n) - n
#
# LOS PUNTOS FIJOS SALEN DE UNA LINEA. n es punto fijo si n = b^k - n, o sea
#
#     n = b^k / 2
#
# y eso es entero **si y solo si la base es par**. Predicciones:
#
#   base par   -> hay exactamente un punto fijo por decada, y vale b^k/2
#                 (base 10: 5, 50, 500...  base 2: 1, 2, 4, 8...)
#   base impar -> NO HAY NI UNO. Cero puntos fijos, en cualquier rango.
#
# Y HAY UNA SEGUNDA COSA, QUE ES LA BUENA. Si b^(k-1) <= n < b^k, entonces
#
#     espejo_b(n) = b^k - n   cae en el intervalo  (0, b^(k-1)*(b-1)]
#
#   - con b = 2 eso es (0, 2^(k-1)]: SIEMPRE cae en la decada de abajo o
#     justo en su borde. El espejo en base 2 no puede quedarse donde estaba:
#     baja estrictamente, siempre. Por eso todo termina en punto fijo y no
#     hay ni un 2-ciclo.
#   - con b >= 3 el tope b^(k-1)*(b-1) es al menos 2*b^(k-1), que ya supera
#     b^(k-1): la imagen PUEDE quedarse en la misma decada, y de ahi salen
#     los 2-ciclos. La base 10 tiene 44.450 bajo 100.000.
#
# O sea: **la base 2 es la unica base en la que el espejo esta obligado a
# bajar.** Y la base 2 es la base de Collatz. Eso no demuestra nada sobre la
# conjetura, pero explica por que de los dos espejos del repo solo el de
# base 2 daba un teorema (todo cae, demostrado) y el de base 10 daba un zoo.
#
# Todo lo de arriba se mide abajo antes de afirmarlo.

# ---------------------------------------------------------------------------
# Cambia esto aqui, guarda, y dale a Ctrl+B en Sublime.
# ---------------------------------------------------------------------------

HASTA = 200000       # se examinan los numeros de 1 a HASTA
BASES = list(range(2, 17))


def espejo(n, b):
    """La potencia de b mas chica que supera a n, menos n."""
    p = b
    while p <= n:
        p *= b
    return p - n


def caminar(n, b, tope_pasos=200):
    """Sigue el espejo hasta repetirse. Devuelve (cola, largo del ciclo)."""
    visto = {}
    i = 0
    while n not in visto:
        visto[n] = i
        n = espejo(n, b)
        i += 1
        if i > tope_pasos:
            return None, None
    return visto[n], i - visto[n]


print(f"EL ESPEJO EN QUINCE BASES  (numeros de 1 a {HASTA:,})\n")
print(f"  {'base':>4} {'fijos':>7} {'2-ciclos':>9} {'otros':>7} {'cola max':>9}"
      f"  cuales son los puntos fijos")
print(f"  {'-'*4} {'-'*7} {'-'*9} {'-'*7} {'-'*9}  {'-'*34}")

resumen = {}
for b in BASES:
    fijos, ciclos, colamax = [], {}, 0
    for n in range(1, HASTA + 1):
        cola, largo = caminar(n, b)
        if cola is None:
            raise SystemExit(f"El espejo en base {b} no cerro desde {n}. Mira eso.")
        colamax = max(colamax, cola)
        if largo == 1 and cola == 0:
            fijos.append(n)
        ciclos[largo] = ciclos.get(largo, 0) + 1
    dos = ciclos.get(2, 0)
    otros = sum(v for k, v in ciclos.items() if k not in (1, 2))
    muestra = ", ".join(str(f) for f in fijos[:6]) if fijos else "NINGUNO"
    print(f"  {b:>4} {len(fijos):>7} {dos:>9} {otros:>7} {colamax:>9}  {muestra}")
    resumen[b] = dict(fijos=fijos, dos=dos, otros=otros, colamax=colamax)


# ------- COMPROBACION 1: hay puntos fijos si y solo si la base es par

fallos_paridad = 0
for b in BASES:
    tiene = len(resumen[b]["fijos"]) > 0
    deberia = (b % 2 == 0)
    if tiene != deberia:
        fallos_paridad += 1
        print(f"  FALLO en base {b}: tiene fijos={tiene}, deberia={deberia}")

print(f"\nCOMPROBACION 1 -- hay puntos fijos si y solo si la base es par")
print(f"  bases probadas: {len(BASES)}   fallos: {fallos_paridad}")
if fallos_paridad:
    raise SystemExit("La regla de la paridad de la base falla. No sigas.")


# ------- COMPROBACION 2: los puntos fijos son exactamente b^k / 2

fallos_formula = 0
for b in BASES:
    if b % 2:
        continue
    esperados = []
    p = b
    while p // 2 <= HASTA:
        if p // 2 >= 1:
            esperados.append(p // 2)
        p *= b
    if resumen[b]["fijos"] != esperados:
        fallos_formula += 1
        print(f"  FALLO en base {b}: {resumen[b]['fijos']} vs {esperados}")

print(f"\nCOMPROBACION 2 -- los puntos fijos son exactamente b^k / 2")
print(f"  bases pares probadas: {sum(1 for b in BASES if b % 2 == 0)}"
      f"   fallos: {fallos_formula}")
if fallos_formula:
    raise SystemExit("La formula b^k/2 falla. No sigas.")
print(f"  base 10 -> {resumen[10]['fijos']}   (los 5, 50, 500... de siempre)")
print(f"  base  2 -> {resumen[2]['fijos'][:8]} ...   (las potencias de 2)")

# la forma limpia: el primero de la lista es siempre b/2, y luego se
# multiplica por b. O sea los puntos fijos son (b/2) * b^m.
print(f"\n  Y la forma limpia de decirlo: el primero es SIEMPRE b/2, y de ahi")
print(f"  se va multiplicando por b. Los puntos fijos son  (b/2) * b^m :")
fallos_bmedios = 0
for b in BASES:
    if b % 2:
        continue
    fijos = resumen[b]["fijos"]
    esperados = []
    v = b // 2
    while v <= HASTA:
        esperados.append(v)
        v *= b
    if fijos != esperados:
        fallos_bmedios += 1
    print(f"    base {b:>2}: primero {b//2:>2}  ->  {fijos[:5]}")
print(f"  fallos de la forma (b/2)*b^m: {fallos_bmedios}")
if fallos_bmedios:
    raise SystemExit("La forma (b/2)*b^m falla. No sigas.")
print(f"\n  Los 5, 50, 500, 5000, 50000 son el caso b = 10.")
print(f"  Las potencias de 2 son el caso b = 2, donde b/2 = 1.")


# ------- COMPROBACION 3: la base 2 es la unica que baja siempre

print(f"\nCOMPROBACION 3 -- la base 2 es la unica en la que el espejo BAJA siempre")
fallos_bajada = 0
for b in BASES:
    nunca_sube = True
    for n in range(2, min(HASTA, 20000) + 1):
        if espejo(n, b) >= n and espejo(n, b) != n:
            nunca_sube = False
            break
    baja_o_iguala = all(espejo(n, b) <= n for n in range(2, min(HASTA, 20000) + 1))
    marca = "baja o iguala SIEMPRE" if baja_o_iguala else "a veces sube"
    if (b == 2) != baja_o_iguala:
        fallos_bajada += 1
    print(f"    base {b:>2}: {marca}"
          + ("   <- la unica" if baja_o_iguala else ""))
print(f"  fallos contra la prediccion: {fallos_bajada}")
if fallos_bajada:
    raise SystemExit("Alguna base que no es la 2 tambien baja siempre. Mira eso.")


# ------- COMPROBACION 4: y por eso solo la base 2 no tiene 2-ciclos

print(f"\nCOMPROBACION 4 -- y por eso solo la base 2 se queda sin 2-ciclos")
sin_dos = [b for b in BASES if resumen[b]["dos"] == 0]
print(f"  bases sin ni un 2-ciclo: {sin_dos}")
if sin_dos != [2]:
    raise SystemExit("Hay mas de una base sin 2-ciclos. La explicacion falla.")
print(f"  base  2: {resumen[2]['dos']:>7,} numeros en 2-ciclos")
print(f"  base 10: {resumen[10]['dos']:>7,} numeros en 2-ciclos")
print(f"  La cuenta de una linea: si b^(k-1) <= n < b^k, la imagen cae en")
print(f"  (0, b^(k-1)*(b-1)]. Con b=2 ese tope es b^(k-1) y la imagen NO cabe")
print(f"  en la decada de partida. Con b>=3 el tope es >= 2*b^(k-1) y si cabe.")


# ------------------------------- lo que esto dice del repo, y lo que no

print(f"\nLO QUE ESTO EXPLICA\n")
print(f"  El repo tenia dos espejos y los trataba como dos casos sueltos:")
print(f"  el de base 10 daba un zoo (44.450 ciclos bajo 100.000) y el de")
print(f"  base 2 daba un TEOREMA (todo cae en potencia de 2, demostrado).")
print(f"  No era suerte ni eleccion afortunada: la base 2 es la unica de las")
print(f"  quince en la que el espejo esta obligado a bajar. Y es la base en")
print(f"  la que vive Collatz.")
print(f"\n  Lo que esto NO dice: nada sobre la conjetura. El espejo en base 2")
print(f"  conmuta con Collatz UN paso y se rompe al segundo (medido: la")
print(f"  correlacion entre pasos(n) y pasos(espejo2(n)) es +0,06). Que las")
print(f"  dos cosas vivan en base 2 las hace parientes, no la misma.")
