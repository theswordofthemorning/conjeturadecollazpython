# mallaespejo.py
#
# EL A/B: LA MISMA MAQUINARIA, DOS REGLAS DISTINTAS.
#
# Esto no es un dibujo bonito, es una prueba. La idea:
#
#   Si una maquina de mallas devuelve la misma malla para cualquier cosa que le
#   metas, no esta midiendo lo que le metes: se esta midiendo a si misma. Para
#   que sirva de algo, dos reglas distintas tienen que dar mallas DISTINTAS.
#
# Asi que se meten dos reglas por el mismo embudo, sin cambiar nada del dibujo:
#
#   ESPEJO   : n -> (la potencia de 10 mas chica que supera a n) − n
#              Es el complemento a diez, el de las calculadoras mecanicas.
#              n + espejo(n) = 10^k SIEMPRE. Cierra en 2 pasos y esta demostrado.
#
#   COLLATZ  : n -> n/2 si par, 3n+1 si impar
#              Un solo sumidero conocido (1-4-2), trayectorias de 100+ pasos,
#              y sigue siendo conjetura.
#
# EL DIBUJO ES EXACTAMENTE EL MISMO PARA LAS DOS:
#   - los numeros 1 … N repartidos por un circulo, el angulo va con el numero
#   - una cuerda por cada paso de la regla:  n  ---->  regla(n)
#   - si el paso se sale del rango 1 … N, se marca aparte (eso tambien es un dato)
#
# Lo que sale, y no lo elegimos nosotros:
#
#   El espejo da CUERDAS PARALELAS. Porque n y 10^k−n caen en angulos simetricos
#   respecto del mismo eje, asi que todas las cuerdas de una decada son paralelas
#   entre si. Orden perfecto, cero grados de libertad.
#
#   Collatz da un ENREDO, y ademas se ESCAPA: 3n+1 se va del rango todo el rato.
#   El espejo nunca se escapa de su decada.
#
# Genera un .html con los dos paneles lado a lado, para verlos juntos.

import math
import collections
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ---------------------------------------------------------------------------
# Cambia esto aqui, guarda, y dale a Ctrl+B en Sublime.
# ---------------------------------------------------------------------------

N = 1000            # cuantos numeros entran en el circulo
MOSTRAR_NUMEROS = False   # con N=1000 son demasiados; ponlo True con N pequeño
TAMANO_LETRA = 8


# ------------------------------------------------------------- las reglas

def espejo(n):
    """El complemento a diez: lo que le falta a n para llegar a la potencia."""
    potencia = 10
    while potencia <= n:
        potencia *= 10
    return potencia - n


def collatz(n):
    """La regla clasica."""
    return n // 2 if n % 2 == 0 else 3 * n + 1


REGLAS = (
    ("ESPEJO", espejo, "#0b63d6",
     "n + espejo(n) = 10^k · cierra en 2 pasos · DEMOSTRADO"),
    ("COLLATZ", collatz, "#d62728",
     "un solo sumidero (1-4-2) · 114 pasos el 221 · CONJETURA"),
)


# ------------------------------------------------------- medir cada regla

def medir(regla, hasta):
    """La misma bateria de medidas para cualquier regla."""
    colas = collections.Counter()
    largos = collections.Counter()
    ciclos = set()
    fijos = []
    se_quedan = 0
    se_escapan = 0

    for semilla in range(1, hasta + 1):
        # a donde va en un paso, y si eso se sale del rango dibujable
        destino = regla(semilla)
        if 1 <= destino <= hasta:
            se_quedan += 1
        else:
            se_escapan += 1

        # la orbita completa: cuanto tarda en entrar en un ciclo y que ciclo es
        visto = {}
        x = semilla
        i = 0
        while x not in visto:
            visto[x] = i
            x = regla(x)
            i += 1
        cola = visto[x]
        largo = i - cola
        colas[cola] += 1
        largos[largo] += 1
        ciclos.add(tuple(sorted(k for k, v in visto.items() if v >= cola)))
        if largo == 1 and cola == 0:
            fijos.append(semilla)

    return {
        "colas": colas,
        "largos": largos,
        "ciclos": ciclos,
        "fijos": fijos,
        "se_quedan": se_quedan,
        "se_escapan": se_escapan,
    }


medidas = {}
print(f"EL A/B — la misma maquinaria, dos reglas.  N = {N:,}\n")

for nombre, regla, color, resumen in REGLAS:
    m = medir(regla, N)
    medidas[nombre] = m
    print(f"--- {nombre} ---")
    print(f"  pasos que se QUEDAN en 1 … {N:,} : {m['se_quedan']:>6,}"
          f"  ({100 * m['se_quedan'] / N:.1f}%)")
    print(f"  pasos que se ESCAPAN del rango   : {m['se_escapan']:>6,}"
          f"  ({100 * m['se_escapan'] / N:.1f}%)")
    print(f"  ciclos distintos a los que se cae: {len(m['ciclos']):>6,}")
    print(f"  puntos fijos (n -> n)            : {len(m['fijos']):>6}"
          f"   {m['fijos'][:8]}")
    print(f"  largos de ciclo    : {dict(sorted(m['largos'].items()))}")
    cola_max = max(m["colas"])
    cola_media = sum(k * v for k, v in m["colas"].items()) / N
    print(f"  cola mas larga     : {cola_max}")
    print(f"  cola media         : {cola_media:.2f} pasos")
    print()


# ------------------------------------------------ la comparacion, en frio

e = medidas["ESPEJO"]
c = medidas["COLLATZ"]

print("=" * 66)
print("LA MALLA SALE DISTINTA?  (si sale igual, la maquinaria no mide nada)")
print("=" * 66)
filas = [
    ("ciclos distintos", f"{len(e['ciclos']):,}", f"{len(c['ciclos']):,}"),
    ("puntos fijos", f"{len(e['fijos'])}", f"{len(c['fijos'])}"),
    ("cola mas larga", f"{max(e['colas'])}", f"{max(c['colas'])}"),
    ("cola media", f"{sum(k*v for k,v in e['colas'].items())/N:.2f}",
     f"{sum(k*v for k,v in c['colas'].items())/N:.2f}"),
    ("pasos que se escapan", f"{100*e['se_escapan']/N:.1f}%",
     f"{100*c['se_escapan']/N:.1f}%"),
]
print(f"  {'':<24} {'ESPEJO':>12} {'COLLATZ':>12}")
for etiqueta, a, b in filas:
    print(f"  {etiqueta:<24} {a:>12} {b:>12}")
print()
veces = len(e["ciclos"]) / len(c["ciclos"])
print(f"  -> el espejo tiene {veces:.0f} veces mas ciclos que Collatz.")
print(f"     Las mallas NO se parecen en nada. La maquinaria discrimina:")
print(f"     lo que dibuja depende de lo que le metes, no de como dibuja.")


# ------------------------------------------------------------- el dibujo

def donde(n):
    """El numero n, repartido por el circulo. El angulo va con el numero."""
    a = 2 * math.pi * (n - 1) / N
    return math.cos(a), math.sin(a)


figura = make_subplots(
    rows=1, cols=2,
    subplot_titles=[f"<b>{nombre}</b><br><sub>{resumen}</sub>"
                    for nombre, _, _, resumen in REGLAS],
    horizontal_spacing=0.06,
)

for columna, (nombre, regla, color, resumen) in enumerate(REGLAS, start=1):
    m = medidas[nombre]

    # El aro de fuera, para tener referencia.
    aro = [donde(1 + k * N / 240) for k in range(241)]
    figura.add_trace(go.Scatter(
        x=[p[0] for p in aro], y=[p[1] for p in aro], mode="lines",
        line=dict(color="#dfe3ea", width=1),
        hoverinfo="skip", showlegend=False,
    ), row=1, col=columna)

    # Las cuerdas que se quedan dentro del rango.
    dentro_x, dentro_y = [], []
    # Los que se escapan: un pinchito hacia afuera, para que se vea.
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
        line=dict(color=color, width=0.7),
        opacity=0.55,
        name=f"{nombre}: {m['se_quedan']:,} pasos que se quedan",
        hoverinfo="skip",
    ), row=1, col=columna)

    if fuera_x:
        figura.add_trace(go.Scatter(
            x=fuera_x, y=fuera_y, mode="lines",
            line=dict(color="#c26a00", width=1.2),
            name=f"{nombre}: {m['se_escapan']:,} pasos que se ESCAPAN del rango",
            hoverinfo="skip",
        ), row=1, col=columna)

    # Los puntos fijos: donde la regla se queda quieta.
    if m["fijos"]:
        sitios = [donde(n) for n in m["fijos"]]
        figura.add_trace(go.Scatter(
            x=[p[0] for p in sitios], y=[p[1] for p in sitios],
            mode="markers",
            marker=dict(symbol="diamond", size=11, color="#111318",
                        line=dict(color="white", width=1.5)),
            name=f"{nombre}: puntos fijos {m['fijos'][:6]}",
            text=[f"<b>{n}</b><br>{nombre}: se queda quieto aqui"
                  for n in m["fijos"]],
            hovertemplate="%{text}<extra></extra>",
        ), row=1, col=columna)

    if MOSTRAR_NUMEROS:
        sitios = [donde(n) for n in range(1, N + 1)]
        figura.add_trace(go.Scatter(
            x=[p[0] * 1.06 for p in sitios], y=[p[1] * 1.06 for p in sitios],
            mode="text", text=[str(n) for n in range(1, N + 1)],
            textfont=dict(size=TAMANO_LETRA, color="#20242c"),
            hoverinfo="skip", showlegend=False,
        ), row=1, col=columna)

    figura.update_xaxes(range=[-1.25, 1.25], showgrid=False, zeroline=False,
                        visible=False, row=1, col=columna)
    figura.update_yaxes(range=[-1.25, 1.25], showgrid=False, zeroline=False,
                        visible=False, scaleanchor=f"x{columna if columna > 1 else ''}",
                        scaleratio=1, row=1, col=columna)

figura.update_layout(
    title=dict(
        text=f"El A/B de la maquinaria — los numeros 1 … {N:,} en el mismo"
             f" circulo, una cuerda por cada paso"
             f"<br><sub>ESPEJO: {len(e['ciclos']):,} ciclos, cuerdas paralelas,"
             f" nunca se escapa  ·  COLLATZ: {len(c['ciclos']):,} ciclo,"
             f" un enredo, se escapa el {100*c['se_escapan']/N:.0f}% de las veces"
             f"<br>mismo dibujo para las dos: si salen distintas, la diferencia"
             f" es de la aritmetica</sub>",
        x=0.5,
    ),
    plot_bgcolor="white", paper_bgcolor="white",
    autosize=True,
    margin=dict(l=10, r=10, t=115, b=60),
    legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.02,
                bgcolor="rgba(255,255,255,0.9)"),
)

archivo = f"malla_ab_espejo_collatz_{N}.html"
figura.write_html(
    archivo,
    auto_open=True,
    default_width="100%",
    default_height="100vh",
    config=dict(responsive=True, scrollZoom=True, displaylogo=False),
)
print("\nGrafico guardado y abierto en el navegador:", archivo)
