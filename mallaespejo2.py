# mallaespejo2.py
#
# EL ESPEJO EN BASE 2, QUE ES DONDE LAS DOS REGLAS SE TOCAN DE VERDAD.
#
# El espejo de mallaespejo.py era base 10 (complemento a diez) y Collatz es base
# 2 (dividir entre dos, y 3n+1). No se hablaban: la correlacion entre sus pasos
# daba 0,08, o sea nada.
#
# Asi que se cambia de base. En vez de complementar a la potencia de 10, se
# complementa a la POTENCIA DE 2:
#
#       espejo2(n)  =  (la potencia de 2 mas chica que supera a n)  -  n
#
# Y eso es lo mismo que "menos n, modulo 2^k". Importa porque ya esta verificado
# (mallaresiduos.py) que los primeros k pasos de Collatz los decide n mod 2^k.
# O sea que el espejo en base 2 actua sobre EXACTAMENTE la misma estructura que
# gobierna el arranque de Collatz. Si hay puente, tiene que estar aqui.
#
# Y LO HAY. Dos identidades exactas, que salen de dos lineas de algebra:
#
#   n PAR :   T(2^k - n)  =  2^(k-1) - T(n)
#             porque  (2^k - n)/2  =  2^(k-1) - n/2
#             -> el espejo y el dividir entre dos CONMUTAN (bajando un nivel).
#                El espejo es una simetria de la mitad par de Collatz.
#
#   n IMPAR:  T(2^k - n)  =  3·2^k + 2 - T(n)
#             porque  3(2^k - n) + 1  =  3·2^k + 2 - (3n + 1)
#             -> casi conmuta, pero le SOBRA UN +2. Ese +2 es el mismo "+1" del
#                3n+1 arrastrado, el que ya salia como el grosor 0,23 de la
#                lamina en collazlamina.py.
#
# El programa comprueba las dos antes de dibujar nada, y se para si fallan.
#
# PERO EL PUENTE MIDE UN PASO Y NO LLEGA AL SEGUNDO. La correlacion entre los
# pasos de n y los de su espejo2 es +0,06 — todavia MENOS que en base 10. El +2
# se acumula al iterar y borra la relacion. Un paso: identidad exacta. Dos pasos:
# ruido. Eso tambien se mide aqui, y es un resultado negativo que hay que
# registrar para no volver a buscar por ahi.
#
# LO QUE SI ES UN HALLAZGO: el espejo2 no tiene NINGUN 2-ciclo. Todos los numeros
# caen en un punto fijo, y los puntos fijos son exactamente las potencias de 2.
# Se demuestra en una linea: si 2^(k-1) < n < 2^k entonces 2^k - n < 2^(k-1), o
# sea que baja estrictamente. Es el analogo DEMOSTRADO de "todo cae en el 1".
# Y la cola de toda trayectoria de Collatz es una tirada de potencias de 2 (la del
# 221 termina en 16, 8, 4, 2, 1): los dos sistemas mueren en el mismo conjunto.
#
# El dibujo son tres paneles con la MISMA maquinaria y solo la regla cambiada:
# los numeros 1 … N repartidos por un circulo y una cuerda por cada paso.

import math
import collections
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ---------------------------------------------------------------------------
# Cambia esto aqui, guarda, y dale a Ctrl+B en Sublime.
# ---------------------------------------------------------------------------

N = 1024            # cuantos numeros entran en el circulo (potencia de 2 va bien)
TOPE_PRUEBA = 100000  # hasta donde se comprueban las identidades
TOPE_CORR = 30000     # hasta donde se mide la correlacion (pide muchos pasos)


# ------------------------------------------------------------- las reglas

def potencia_de_2(n):
    """La potencia de 2 mas chica que supera a n."""
    p = 1
    while p <= n:
        p *= 2
    return p


def potencia_de_10(n):
    p = 10
    while p <= n:
        p *= 10
    return p


def espejo2(n):
    """El complemento a la potencia de 2. Es lo mismo que -n modulo 2^k."""
    return potencia_de_2(n) - n


def espejo10(n):
    """El complemento a diez, el de las calculadoras mecanicas."""
    return potencia_de_10(n) - n


def T(n):
    """Un paso de Collatz."""
    return n // 2 if n % 2 == 0 else 3 * n + 1


def pasos_al_1(n):
    cuantos = 0
    while n != 1:
        n = T(n)
        cuantos += 1
    return cuantos


# --------------------------------- COMPROBACION 1: las dos identidades

print(f"EL ESPEJO EN BASE 2  —  comprobando hasta {TOPE_PRUEBA:,}\n")

bien_par = bien_impar = 0
mal_par = mal_impar = 0
primer_fallo = None

for n in range(1, TOPE_PRUEBA + 1):
    k = potencia_de_2(n)
    reflejo = k - n
    if reflejo < 1:
        continue
    if n % 2 == 0:
        # el espejo y el dividir entre dos conmutan
        if T(reflejo) == k // 2 - T(n):
            bien_par += 1
        else:
            mal_par += 1
            primer_fallo = primer_fallo or ("par", n)
    else:
        # casi conmutan, pero sobra un +2
        if T(reflejo) == 3 * k + 2 - T(n):
            bien_impar += 1
        else:
            mal_impar += 1
            primer_fallo = primer_fallo or ("impar", n)

print("COMPROBACION 1 — las dos identidades")
print(f"  n PAR   ·  T(2^k - n) = 2^(k-1) - T(n)")
print(f"    cumplen: {bien_par:>7,}    fallan: {mal_par}")
print(f"  n IMPAR ·  T(2^k - n) = 3·2^k + 2 - T(n)")
print(f"    cumplen: {bien_impar:>7,}    fallan: {mal_impar}")
if mal_par or mal_impar:
    print(f"  primer fallo: {primer_fallo}")
    raise SystemExit("La identidad falla. Algo esta mal, no sigas.")
print(f"  -> las dos exactas en {bien_par + bien_impar:,} comprobaciones.")
print(f"     En los pasos PARES el espejo es una simetria de Collatz: espejar y")
print(f"     dividir entre dos dan lo mismo en cualquier orden.")
print(f"     En los IMPARES se rompe, y se rompe por exactamente +2.")

print(f"\n  ejemplos a mano:")
for n in (5, 7, 221, 1276, 99999):
    k = potencia_de_2(n)
    reflejo = espejo2(n)
    if n % 2:
        print(f"    n={n:<6} 2^k={k:<7} espejo={reflejo:<6}"
              f" T(espejo)={T(reflejo):<7} 3·{k}+2-T({n})={3 * k + 2 - T(n)}")
    else:
        print(f"    n={n:<6} 2^k={k:<7} espejo={reflejo:<6}"
              f" T(espejo)={T(reflejo):<7} {k // 2}-{n // 2}={k // 2 - T(n)}")


# ------------------- COMPROBACION 2: todo cae en una potencia de 2

fijos = []
colas = collections.Counter()
largos = collections.Counter()

for n in range(1, TOPE_PRUEBA + 1):
    visto = {}
    x = n
    i = 0
    while x not in visto:
        visto[x] = i
        x = espejo2(x)
        i += 1
    cola = visto[x]
    largos[i - cola] += 1
    colas[cola] += 1
    if i - cola == 1 and cola == 0:
        fijos.append(n)

print(f"\nCOMPROBACION 2 — todo cae en una potencia de 2")
print(f"  largos de ciclo: {dict(largos)}")
if set(largos) != {1}:
    raise SystemExit("Aparecio un ciclo de largo > 1. No sigas.")
no_son_potencia = [n for n in fijos if n & (n - 1) != 0]
print(f"  puntos fijos           : {len(fijos)}")
print(f"  que NO son potencia de 2: {len(no_son_potencia)}")
if no_son_potencia:
    raise SystemExit("Hay un punto fijo que no es potencia de 2. No sigas.")
print(f"  -> {fijos[:8]} … {fijos[-3:]}")
print(f"     Ni un solo 2-ciclo en {TOPE_PRUEBA:,} numeros: TODO cae en punto")
print(f"     fijo, y los puntos fijos son exactamente las potencias de 2.")
print(f"     Se demuestra en una linea: si 2^(k-1) < n < 2^k entonces")
print(f"     2^k - n < 2^(k-1), o sea que el espejo baja estrictamente.")
print(f"  cola mas larga: {max(colas)}    cola media: "
      f"{sum(k * v for k, v in colas.items()) / TOPE_PRUEBA:.2f}")


# ------------------- EL NEGATIVO: el puente no llega al segundo paso

def correlacion(xs, ys):
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    arriba = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    abajo = math.sqrt(sum((a - mx) ** 2 for a in xs)
                      * sum((b - my) ** 2 for b in ys))
    return arriba / abajo

print(f"\nEL NEGATIVO — el puente mide un paso y no llega al segundo")
correlaciones = {}
for nombre, regla in (("base 2", espejo2), ("base 10", espejo10)):
    equis, ye = [], []
    for n in range(2, TOPE_CORR + 1):
        reflejo = regla(n)
        if reflejo >= 2:
            equis.append(pasos_al_1(n))
            ye.append(pasos_al_1(reflejo))
    c = correlacion(equis, ye)
    correlaciones[nombre] = c
    print(f"  correlacion pasos(n) vs pasos(espejo {nombre}): {c:+.4f}"
          f"   ({len(equis):,} pares)")
print(f"  -> la base 2 correlaciona MENOS que la base 10. El +2 se acumula al")
print(f"     iterar y borra la relacion. Un paso: identidad exacta. Dos: ruido.")

# Los dos sistemas mueren en el mismo conjunto, eso si.
camino = [221]
while camino[-1] != 1:
    camino.append(T(camino[-1]))
cola_de_potencias = [x for x in camino if x & (x - 1) == 0]
print(f"\n  (lo que si comparten: la cola de toda trayectoria de Collatz es una")
print(f"   tirada de potencias de 2, que son los puntos fijos del espejo2.")
print(f"   La del 221 termina en {cola_de_potencias}.)")


# ------------------------------------------- el A/B/C de las tres reglas

REGLAS = (
    ("ESPEJO base 10", espejo10, "#0b63d6",
     "n + espejo = 10^k · miles de 2-ciclos · no habla con Collatz"),
    ("ESPEJO base 2", espejo2, "#1f7a4d",
     "n + espejo = 2^k · cero 2-ciclos · conmuta con Collatz en los pares"),
    ("COLLATZ", T, "#d62728",
     "un solo sumidero (1-4-2) · se escapa del rango · CONJETURA"),
)

print(f"\n{'=' * 70}")
print(f"EL A/B/C — la misma maquinaria, tres reglas.  N = {N:,}")
print(f"{'=' * 70}")

resumen = {}
for nombre, regla, _, _ in REGLAS:
    se_quedan = sum(1 for n in range(1, N + 1) if 1 <= regla(n) <= N)
    ciclos = set()
    fijos_aqui = []
    colas_aqui = collections.Counter()
    for n in range(1, N + 1):
        visto = {}
        x = n
        i = 0
        while x not in visto:
            visto[x] = i
            x = regla(x)
            i += 1
        cola = visto[x]
        colas_aqui[cola] += 1
        ciclos.add(tuple(sorted(k for k, v in visto.items() if v >= cola)))
        if i - cola == 1 and cola == 0:
            fijos_aqui.append(n)
    resumen[nombre] = {
        "se_quedan": se_quedan,
        "ciclos": ciclos,
        "fijos": fijos_aqui,
        "cola_max": max(colas_aqui),
        "cola_media": sum(k * v for k, v in colas_aqui.items()) / N,
    }

etiquetas = [nombre for nombre, _, _, _ in REGLAS]
print(f"  {'':<22}" + "".join(f"{e:>20}" for e in etiquetas))
for fila, saca in (
    ("ciclos distintos", lambda d: f"{len(d['ciclos']):,}"),
    ("puntos fijos", lambda d: f"{len(d['fijos'])}"),
    ("cola mas larga", lambda d: f"{d['cola_max']}"),
    ("cola media", lambda d: f"{d['cola_media']:.2f}"),
    ("se escapan (NO vale)", lambda d: f"{100 * (N - d['se_quedan']) / N:.1f}%"),
):
    print(f"  {fila:<22}" + "".join(f"{saca(resumen[e]):>20}" for e in etiquetas))
print()
print(f"  -> tres reglas, tres mallas distintas. La maquinaria discrimina:")
print(f"     lo que dibuja depende de lo que se le mete, no de como dibuja.")
print()
print(f"  CUIDADO CON LA ULTIMA FILA -- NO DISCRIMINA (correccion del 30-07-2026).")
print(f"  Aqui parece que separa, pero es un espejismo: separa a los espejos de")
print(f"  Collatz solo porque los espejos estan ACOTADOS por construccion. Entre")
print(f"  dos reglas del mismo tipo no separa nada: medida con 3n+1 contra 3n-1")
print(f"  da 33,3% en las dos, con los MISMOS conteos absolutos, a N = 256, 1024,")
print(f"  4096 y 10.000. Se escapan los impares con 3n±1 > N, y el ±1 casi nunca")
print(f"  cambia de lado del corte. Esa fila mide el RANGO, no la REGLA.")
print(f"  Las tres que si valen son: ciclos distintos, cola mas larga, cola media.")


# ------------------------------------------------------------- el dibujo

def donde(n):
    """El numero n, repartido por el circulo. El angulo va con el numero."""
    a = 2 * math.pi * (n - 1) / N
    return math.cos(a), math.sin(a)


figura = make_subplots(
    rows=1, cols=3,
    subplot_titles=[f"<b>{nombre}</b><br><sub>{texto}</sub>"
                    for nombre, _, _, texto in REGLAS],
    horizontal_spacing=0.04,
)

for columna, (nombre, regla, color, _) in enumerate(REGLAS, start=1):
    datos = resumen[nombre]

    aro = [donde(1 + k * N / 240) for k in range(241)]
    figura.add_trace(go.Scatter(
        x=[p[0] for p in aro], y=[p[1] for p in aro], mode="lines",
        line=dict(color="#dfe3ea", width=1),
        hoverinfo="skip", showlegend=False,
    ), row=1, col=columna)

    dentro_x, dentro_y = [], []
    fuera_x, fuera_y = [], []
    for n in range(1, N + 1):
        destino = regla(n)
        x0, y0 = donde(n)
        if 1 <= destino <= N:
            x1, y1 = donde(destino)
            dentro_x += [x0, x1, None]
            dentro_y += [y0, y1, None]
        else:
            fuera_x += [x0, x0 * 1.13, None]
            fuera_y += [y0, y0 * 1.13, None]

    figura.add_trace(go.Scatter(
        x=dentro_x, y=dentro_y, mode="lines",
        line=dict(color=color, width=0.7), opacity=0.55,
        name=f"{nombre}: {datos['se_quedan']:,} pasos dentro del rango",
        hoverinfo="skip",
    ), row=1, col=columna)

    if fuera_x:
        figura.add_trace(go.Scatter(
            x=fuera_x, y=fuera_y, mode="lines",
            line=dict(color="#c26a00", width=1.2),
            name=f"{nombre}: {N - datos['se_quedan']:,} se ESCAPAN",
            hoverinfo="skip",
        ), row=1, col=columna)

    if datos["fijos"]:
        sitios = [donde(n) for n in datos["fijos"]]
        figura.add_trace(go.Scatter(
            x=[p[0] for p in sitios], y=[p[1] for p in sitios],
            mode="markers",
            marker=dict(symbol="diamond", size=9, color="#111318",
                        line=dict(color="white", width=1.2)),
            name=f"{nombre}: {len(datos['fijos'])} puntos fijos",
            text=[f"<b>{n}</b><br>{nombre}: se queda quieto" for n in datos["fijos"]],
            hovertemplate="%{text}<extra></extra>",
        ), row=1, col=columna)

    sufijo = "" if columna == 1 else str(columna)
    figura.update_xaxes(range=[-1.25, 1.25], showgrid=False, zeroline=False,
                        visible=False, row=1, col=columna)
    figura.update_yaxes(range=[-1.25, 1.25], showgrid=False, zeroline=False,
                        visible=False, scaleanchor=f"x{sufijo}", scaleratio=1,
                        row=1, col=columna)

e2 = resumen["ESPEJO base 2"]
e10 = resumen["ESPEJO base 10"]
col = resumen["COLLATZ"]

figura.update_layout(
    title=dict(
        text=f"El espejo en base 2, donde las dos reglas se tocan  —"
             f"  los numeros 1 … {N:,} en el mismo circulo, una cuerda por paso"
             f"<br><sub>identidades exactas en {bien_par + bien_impar:,}"
             f" comprobaciones: en los pares el espejo2 CONMUTA con Collatz,"
             f" en los impares se rompe por +2"
             f"<br>pero el puente mide UN paso: correlacion de trayectorias"
             f" {correlaciones['base 2']:+.3f} (base 10: "
             f"{correlaciones['base 10']:+.3f})"
             f"  ·  ciclos: {len(e10['ciclos']):,} / {len(e2['ciclos']):,} /"
             f" {len(col['ciclos']):,}</sub>",
        x=0.5,
    ),
    plot_bgcolor="white", paper_bgcolor="white",
    autosize=True,
    margin=dict(l=10, r=10, t=120, b=70),
    legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.02,
                bgcolor="rgba(255,255,255,0.9)"),
)

archivo = f"malla_espejo2_{N}.html"
figura.write_html(
    archivo,
    auto_open=True,
    default_width="100%",
    default_height="100vh",
    config=dict(responsive=True, scrollZoom=True, displaylogo=False),
)
print("\nGrafico guardado y abierto en el navegador:", archivo)
