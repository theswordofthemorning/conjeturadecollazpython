# mallabasica.py
#
# LA MALLA BASICA, CON LOS NUMEROS PUESTOS. Aqui no hay Collatz.
#
# Una esfera con 100 paralelos y 100 meridianos, numerados del 1 al 100 cada
# uno, y con los numeros escritos por fuera para poder leerlos.
#
#   los numeros AZULES  son los paralelos   (van de polo a polo)
#   los numeros MARRONES son los meridianos (van dando la vuelta)
#
# EL CRUCE que se queria mirar esta marcado a lo grande: el paralelo 50 es el
# aro rojo, el meridiano 50 es el arco rojo, y donde se tocan hay un diamante
# con su etiqueta. Es un cruce como los otros 9.999, pero ahi esta.
#
# Donde el 50 SI hace algo, y es de verdad:
#
#   - Los meridianos cierran y los paralelos no. Los 100 meridianos son un
#     anillo: despues del 100 viene otra vez el 1. Los 100 paralelos son una
#     tira con dos puntas, y las puntas son los polos.
#
#   - Los 100 meridianos son en realidad 50 AROS COMPLETOS. El meridiano m y el
#     meridiano m+50 estan en lados opuestos, asi que juntos forman un circulo
#     entero. El 1 cierra con el 51, el 2 con el 52... y el 50 con el 100.
#     Ahi es donde el 50 cuadra: es el medio giro.
#
#   - El ecuador NO es el paralelo 50. Cae justo entre el 50 y el 51, porque con
#     100 paralelos no hay uno del medio. El 50 queda un pelo por encima.
#
# COMO LEER LOS NUMEROS: el grafico ocupa toda la ventana. Los numeros estan
# escritos en tamaño fijo, asi que al hacer zoom con la rueda la bola se agranda
# pero las letras no: los numeros se van SEPARANDO y se leen cada vez mejor.
# No se deforman nunca. Arrastra con el mouse para girar la bola.
#
# Si de entrada los ves demasiado apretados, sube CADA_CUANTOS_* a 5 o a 10 y
# vuelve a correrlo: pone solo uno de cada cinco (o diez).

import math
import plotly.graph_objects as go


# ---------------------------------------------------------------------------
# Cambia estos numeros aqui, guarda, y dale a Ctrl+B en Sublime.
# ---------------------------------------------------------------------------

PARALELOS = 100
MERIDIANOS = 100

CADA_CUANTOS_PARALELOS = 1     # 1 = todos, 5 = uno de cada cinco, 10 = ...
CADA_CUANTOS_MERIDIANOS = 1

TAMANO_LETRA = 11              # subelo si los quieres mas grandes
MOSTRAR_CRUCES = False         # los 10.000 puntos: tapan los numeros y pesan 8 MB

# El cruce que se quiere mirar.
PARALELO_MARCADO = 50
MERIDIANO_MARCADO = 50


# ------------------------------------------------------------- la geometria
#
# Un paralelo es una altura: cuanto hemos bajado desde el polo norte.
# Los polos no son paralelos, son puntos, asi que los dejamos libres: por eso
# se reparte entre PARALELOS + 1 y no entre PARALELOS.
#
# Un meridiano es un giro alrededor del eje. El meridiano 1 esta en el 0, y
# despues del ultimo se vuelve al 1: por eso aqui si se reparte entre
# MERIDIANOS justos.

def bajada_del_paralelo(p):
    """Grados desde el polo norte hasta el paralelo p."""
    return p * 180.0 / (PARALELOS + 1)


def giro_del_meridiano(m):
    """Grados de giro del meridiano m alrededor del eje."""
    return (m - 1) * 360.0 / MERIDIANOS


def punto(p, m):
    """Donde se cruzan el paralelo p y el meridiano m."""
    bajada = math.radians(bajada_del_paralelo(p))
    giro = math.radians(giro_del_meridiano(m))
    return (math.sin(bajada) * math.cos(giro),
            math.sin(bajada) * math.sin(giro),
            math.cos(bajada))


def latitud(p):
    """El paralelo p visto como latitud: + es norte, - es sur, 0 es el ecuador."""
    return 90.0 - bajada_del_paralelo(p)


def aro_del_paralelo(p, cuantos=180):
    """El circulo completo que dibuja el paralelo p."""
    bajada = math.radians(bajada_del_paralelo(p))
    puntos = []
    for k in range(cuantos + 1):
        giro = math.radians(k * 360.0 / cuantos)
        puntos.append((math.sin(bajada) * math.cos(giro),
                       math.sin(bajada) * math.sin(giro),
                       math.cos(bajada)))
    return puntos


def arco_del_meridiano(m, cuantos=180):
    """El arco de polo a polo que dibuja el meridiano m."""
    giro = math.radians(giro_del_meridiano(m))
    puntos = []
    for k in range(cuantos + 1):
        bajada = math.radians(k * 180.0 / cuantos)
        puntos.append((math.sin(bajada) * math.cos(giro),
                       math.sin(bajada) * math.sin(giro),
                       math.cos(bajada)))
    return puntos


# ------------------------------------------------------------- las cuentas

cruces = PARALELOS * MERIDIANOS
mitad = MERIDIANOS // 2

print(f"Malla de {PARALELOS} paralelos x {MERIDIANOS} meridianos.")
print(f"Cruces: {cruces:,}  (cada paralelo cruza a cada meridiano una sola vez)")

print(f"\nLOS MERIDIANOS CIERRAN")
print(f"  despues del meridiano {MERIDIANOS} viene otra vez el 1")
if MERIDIANOS % 2 == 0:
    print(f"  y se emparejan de dos en dos: el meridiano m y el m+{mitad} son")
    print(f"  el mismo aro completo, asi que los {MERIDIANOS} son {mitad} circulos:")
    print(f"    1 cierra con {1 + mitad}  ·  2 con {2 + mitad}  ·  ...  ·"
          f"  {mitad} con {MERIDIANOS}")

print(f"\nLOS PARALELOS NO CIERRAN")
print(f"  son una tira con dos puntas, y las puntas son los polos")
print(f"  paralelo 1   -> latitud {latitud(1):+.3f}  (casi el polo norte)")
print(f"  paralelo {PARALELOS} -> latitud {latitud(PARALELOS):+.3f}  (casi el polo sur)")

print(f"\nEL ECUADOR NO ES EL PARALELO {PARALELOS // 2}")
print(f"  paralelo {PARALELOS // 2}  -> latitud {latitud(PARALELOS // 2):+.3f}")
print(f"  paralelo {PARALELOS // 2 + 1}  -> latitud {latitud(PARALELOS // 2 + 1):+.3f}")
print(f"  el ecuador cae justo en medio de los dos.")

xc, yc, zc = punto(PARALELO_MARCADO, MERIDIANO_MARCADO)
print(f"\nEL CRUCE {PARALELO_MARCADO}-{MERIDIANO_MARCADO}  (el marcado en rojo)")
print(f"  esta en x={xc:+.4f}  y={yc:+.4f}  z={zc:+.4f}")
print(f"  latitud {latitud(PARALELO_MARCADO):+.3f}°, giro "
      f"{giro_del_meridiano(MERIDIANO_MARCADO):.1f}°")

cuantos_num_p = len(range(1, PARALELOS + 1, CADA_CUANTOS_PARALELOS))
cuantos_num_m = len(range(1, MERIDIANOS + 1, CADA_CUANTOS_MERIDIANOS))
print(f"\nNumeros escritos: {cuantos_num_p} de paralelo, {cuantos_num_m} de meridiano.")
print(f"  Haz zoom con la rueda: las letras no crecen, asi que se van separando.")


# ------------------------------------------------------------- el dibujo

figura = go.Figure()


def trazo_de_lineas(grupos, color, ancho, nombre):
    """Mete varias lineas en un solo trazo, con un corte (None) entre cada una."""
    ex, ye, ze = [], [], []
    for puntos in grupos:
        ex.extend([v[0] for v in puntos] + [None])
        ye.extend([v[1] for v in puntos] + [None])
        ze.extend([v[2] for v in puntos] + [None])
    figura.add_trace(go.Scatter3d(
        x=ex, y=ye, z=ze, mode="lines",
        line=dict(color=color, width=ancho),
        name=nombre, hoverinfo="skip",
    ))


# La bola, muy transparente para que los numeros de delante se lean limpios.
malla_u = [i * math.pi / 30 for i in range(31)]
malla_v = [j * 2 * math.pi / 60 for j in range(61)]
figura.add_trace(go.Surface(
    x=[[0.98 * math.sin(u) * math.cos(v) for v in malla_v] for u in malla_u],
    y=[[0.98 * math.sin(u) * math.sin(v) for v in malla_v] for u in malla_u],
    z=[[0.98 * math.cos(u) for v in malla_v] for u in malla_u],
    colorscale=[[0, "#f2f5f9"], [1, "#f2f5f9"]],
    opacity=0.22, showscale=False, hoverinfo="skip", showlegend=False,
))


# --- los paralelos y los meridianos ---
#
# Los de diez en diez van mas oscuros para poder contar hasta el 50 de un golpe.

trazo_de_lineas(
    [aro_del_paralelo(p) for p in range(1, PARALELOS + 1)
     if p % 10 != 0 and p != PARALELO_MARCADO],
    "#ccd4e0", 1, f"paralelos  (1 … {PARALELOS})",
)
trazo_de_lineas(
    [aro_del_paralelo(p) for p in range(10, PARALELOS + 1, 10)
     if p != PARALELO_MARCADO],
    "#7b8798", 2, "paralelos de 10 en 10",
)
trazo_de_lineas(
    [arco_del_meridiano(m) for m in range(1, MERIDIANOS + 1)
     if m % 10 != 0 and m != MERIDIANO_MARCADO],
    "#d5dae3", 1, f"meridianos  (1 … {MERIDIANOS})",
)
trazo_de_lineas(
    [arco_del_meridiano(m) for m in range(10, MERIDIANOS + 1, 10)
     if m != MERIDIANO_MARCADO],
    "#8b95a4", 2, "meridianos de 10 en 10",
)


# --- el ecuador, para que se vea que el paralelo 50 no es el ---

figura.add_trace(go.Scatter3d(
    x=[math.cos(math.radians(g)) for g in range(0, 361, 2)],
    y=[math.sin(math.radians(g)) for g in range(0, 361, 2)],
    z=[0.0] * len(range(0, 361, 2)),
    mode="lines", line=dict(color="#1f7a4d", width=5, dash="dash"),
    name=f"el ecuador (cae entre el {PARALELOS // 2} y el {PARALELOS // 2 + 1})",
    hoverinfo="skip",
))


# --- el par de meridianos que forman un aro completo: el 50 y el 100 ---

if MERIDIANOS % 2 == 0:
    trazo_de_lineas(
        [arco_del_meridiano(mitad) + arco_del_meridiano(MERIDIANOS)],
        "#0b63d6", 4,
        f"meridiano {mitad} + meridiano {MERIDIANOS} = un aro entero",
    )


# --- EL CRUCE: el paralelo marcado y el meridiano marcado, en rojo ---

trazo_de_lineas([aro_del_paralelo(PARALELO_MARCADO)], "#d62728", 6,
                f"paralelo {PARALELO_MARCADO}")
trazo_de_lineas([arco_del_meridiano(MERIDIANO_MARCADO)], "#e8590c", 6,
                f"meridiano {MERIDIANO_MARCADO}")


# --- los cruces, si se piden (tapan los numeros) ---

if MOSTRAR_CRUCES:
    cx, cy, cz, textos = [], [], [], []
    for p in range(1, PARALELOS + 1):
        for m in range(1, MERIDIANOS + 1):
            x, y, z = punto(p, m)
            cx.append(x)
            cy.append(y)
            cz.append(z)
            textos.append(f"paralelo <b>{p}</b> × meridiano <b>{m}</b>")
    figura.add_trace(go.Scatter3d(
        x=cx, y=cy, z=cz, mode="markers",
        marker=dict(size=1.6, color="#5b6b7a", opacity=0.5),
        name=f"los {cruces:,} cruces",
        text=textos, hovertemplate="%{text}<extra></extra>",
    ))


# --- LOS NUMEROS ---
#
# Van escritos por fuera de la bola. Se ponen a dos distancias que se van
# alternando (una fila mas cerca, una mas lejos) para que dos numeros vecinos
# nunca se pisen entre ellos.
#
# El tamaño de la letra es fijo en pantalla: al hacer zoom la bola crece y los
# numeros no, asi que se separan. Nunca se deforman.

def poner_numeros(posiciones, textos, color, nombre):
    figura.add_trace(go.Scatter3d(
        x=[v[0] for v in posiciones], y=[v[1] for v in posiciones],
        z=[v[2] for v in posiciones],
        mode="text", text=textos,
        textfont=dict(size=TAMANO_LETRA, color=color),
        name=nombre, hoverinfo="skip", showlegend=False,
    ))


# Los numeros de paralelo, por delante (en el meridiano 1).
sitios, etiquetas, sitios_rojo, etiquetas_rojo = [], [], [], []
for p in range(1, PARALELOS + 1, CADA_CUANTOS_PARALELOS):
    fuera = 1.05 + (p % 2) * 0.07          # una fila cerca, una lejos
    base = punto(p, 1)
    sitio = (base[0] * fuera, base[1] * fuera, base[2] * fuera)
    if p == PARALELO_MARCADO:
        sitios_rojo.append(sitio)
        etiquetas_rojo.append(f"<b>{p}</b>")
    else:
        sitios.append(sitio)
        etiquetas.append(str(p))

poner_numeros(sitios, etiquetas, "#1f4e79", "numeros de paralelo")
if sitios_rojo:
    poner_numeros(sitios_rojo, etiquetas_rojo, "#d62728", "paralelo marcado")


# Los numeros de meridiano, repartidos por el ecuador.
sitios, etiquetas, sitios_rojo, etiquetas_rojo = [], [], [], []
for m in range(1, MERIDIANOS + 1, CADA_CUANTOS_MERIDIANOS):
    fuera = 1.06 + (m % 2) * 0.08
    giro = math.radians(giro_del_meridiano(m))
    sitio = (math.cos(giro) * fuera, math.sin(giro) * fuera, 0.0)
    if m == MERIDIANO_MARCADO:
        sitios_rojo.append(sitio)
        etiquetas_rojo.append(f"<b>{m}</b>")
    else:
        sitios.append(sitio)
        etiquetas.append(str(m))

poner_numeros(sitios, etiquetas, "#7a3e00", "numeros de meridiano")
if sitios_rojo:
    poner_numeros(sitios_rojo, etiquetas_rojo, "#e8590c", "meridiano marcado")


# --- el punto del cruce, con su etiqueta pegada al lado ---

figura.add_trace(go.Scatter3d(
    x=[xc], y=[yc], z=[zc], mode="markers",
    marker=dict(symbol="diamond", size=13, color="#d62728",
                line=dict(color="white", width=2)),
    name=f"EL CRUCE:  paralelo {PARALELO_MARCADO} × meridiano {MERIDIANO_MARCADO}",
    text=[f"<b>paralelo {PARALELO_MARCADO} × meridiano {MERIDIANO_MARCADO}</b>"
          f"<br>latitud {latitud(PARALELO_MARCADO):+.3f}°  —  no es el ecuador"
          f"<br>giro {giro_del_meridiano(MERIDIANO_MARCADO):.1f}°"
          f"<br><br>uno de los {cruces:,} cruces"],
    hovertemplate="%{text}<extra></extra>",
))

figura.add_trace(go.Scatter3d(
    x=[xc * 1.22], y=[yc * 1.22], z=[zc * 1.22 + 0.10],
    mode="text",
    text=[f"<b>{PARALELO_MARCADO} × {MERIDIANO_MARCADO}</b>"],
    textfont=dict(size=TAMANO_LETRA + 7, color="#d62728"),
    hoverinfo="skip", showlegend=False,
))


# --- los polos: las dos puntas de la tira de paralelos ---

figura.add_trace(go.Scatter3d(
    x=[0, 0], y=[0, 0], z=[1, -1], mode="markers",
    marker=dict(color="#111318", size=7, symbol="diamond"),
    name="polos (no son paralelos, son las puntas)",
    text=["polo norte<br>por encima del paralelo 1",
          f"polo sur<br>por debajo del paralelo {PARALELOS}"],
    hovertemplate="%{text}<extra></extra>",
))


sin_eje = dict(showbackground=False, showgrid=False, zeroline=False,
               showticklabels=False, title="", visible=False)

figura.update_layout(
    title=dict(
        text=f"La malla basica — {PARALELOS} paralelos × {MERIDIANOS} meridianos"
             f"<br><sub>numeros de paralelo en azul · de meridiano en marron ·"
             f" el cruce {PARALELO_MARCADO}×{MERIDIANO_MARCADO} en rojo ·"
             f" {cruces:,} cruces en total, sin Collatz"
             f"<br>rueda para hacer zoom: la bola crece y los numeros no,"
             f" asi que se separan y se leen mejor</sub>",
        x=0.5,
    ),
    scene=dict(xaxis=sin_eje, yaxis=sin_eje, zaxis=sin_eje,
               aspectmode="cube",              # nunca se deforma
               camera=dict(eye=dict(x=1.35, y=1.30, z=0.75))),
    paper_bgcolor="white",
    autosize=True,                             # ocupa toda la ventana
    margin=dict(l=0, r=0, t=95, b=0),
    legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.9)",
                bordercolor="#dfe3ea", borderwidth=1),
)

archivo = f"malla_basica_{PARALELOS}x{MERIDIANOS}.html"
figura.write_html(
    archivo,
    auto_open=True,
    default_width="100%",
    default_height="100vh",                    # alto de toda la ventana
    config=dict(responsive=True, scrollZoom=True, displaylogo=False),
)
print("\nGrafico guardado y abierto en el navegador:", archivo)
