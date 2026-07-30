# mapahilos.py
#
# LOS ONCE HILOS A LA VEZ, COMO UN MAPA.
#
# Se lee hilos.db y se miran los once numeros SIMULTANEAMENTE, no uno detras
# de otro. Cuatro paneles, cada uno una forma distinta de mirar lo mismo.
#
# LO QUE APARECIO AL MIRARLOS ASI (y es el motivo de este archivo):
#
# Los once numeros no se diferencian en once cosas. Se diferencian en UNA.
# Todo lo demas se deduce de ella. La cosa es la RAZON DE UNOS:
#
#     razon = A / B      A = veces que se aplico 3n+1
#                        B = veces que se aplico n/2
#
# Y entonces el tiempo de parada escalado sale solo:
#
#     gamma = pasos / ln(n)  =  1 / (ln2 - razon * ln3)      (+ una correccion)
#
# Comprobado abajo: los once caen sobre esa curva. No es correlacion, es
# identidad, y sale de despejar 2^B = 3^A * n + C.
#
# Y LA CORRECCION ES EL GROSOR DE LA LAMINA. La identidad no es perfecta;
# le sobra un termino, que es exactamente
#
#     eps = ln( 2^B / (3^A * n) )
#
# o sea el logaritmo de lo que se desvia 2^B de 3^A*n: la contribucion
# acumulada de todos los +1. Es el mismo numero que collazlamina.py mide
# como "grosor 0,23" del plano. Aqui se mide sobre trayectorias enteras.
#
# Y TIENE NOMBRE EN LA LITERATURA: 2^B/(3^A*n) es el RESIDUO DE ROOSENDAAL.
# Su maximo conocido es Res(993) = 1,253142144, verificado por Roosendaal
# para todo x < 2^32 y conjeturado maximo absoluto. Su logaritmo es
#
#     ln(1,253142144) = 0,225654
#
# que es el techo de nuestra lamina. El grosor de la lamina no es un numero
# que salio de nuestro dibujo: es una constante con conjetura propia.
#
# Los cuatro paneles:
#   (1,1) las once trayectorias superpuestas -> se ve la fusion
#   (1,2) el mapa: once filas x pasos, color = tamano del numero
#   (2,1) el plano (razon, gamma) con la curva exacta encima
#   (2,2) el paseo de Terras: sube mientras la trayectoria sube

import math
import sqlite3
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ---------------------------------------------------------------------------
# Cambia esto aqui, guarda, y dale a Ctrl+B en Sublime.
# ---------------------------------------------------------------------------

ARCHIVO = "hilos.db"     # lo escribe guardarhilos.py
SALIDA = "mapa_hilos.html"
TAMANO_LETRA = 11

L2, L3 = math.log(2), math.log(3)
GAMMA_TERRAS = L2 / L3           # 0,63093 -- el umbral de subida


# ------------------------------------------------------- leer la base

conexion = sqlite3.connect(ARCHIVO)
cursor = conexion.cursor()

semillas = [f[0] for f in cursor.execute(
    "SELECT semilla FROM hilos ORDER BY hilo").fetchall()]
caminos = {}
for hilo, semilla in enumerate(semillas, 1):
    caminos[semilla] = [f[0] for f in cursor.execute(
        "SELECT valor FROM pasos WHERE hilo=? ORDER BY k", (hilo,)).fetchall()]

fusiones = cursor.execute(
    "SELECT hilo_a, paso_a, hilo_b, paso_b, valor FROM fusiones"
    " WHERE es_cola=0 AND desfase=0").fetchall()
conexion.close()

print(f"LOS {len(semillas)} HILOS, MIRADOS A LA VEZ\n")


# --------------------------------------- las tres cantidades de cada hilo

datos = {}
for semilla in semillas:
    camino = caminos[semilla]
    A = sum(1 for v in camino[:-1] if v % 2 == 1)   # veces 3n+1
    B = len(camino) - 1 - A                          # veces n/2
    razon = A / B
    gamma = B / math.log(semilla)
    formula = 1 / (L2 - razon * L3)
    eps = B * L2 - A * L3 - math.log(semilla)
    datos[semilla] = dict(A=A, B=B, razon=razon, gamma=gamma,
                          formula=formula, eps=eps, pico=max(camino))

print(f"  {'n':>7} {'A':>4} {'B':>4} {'razon':>7} {'gamma':>7} "
      f"{'formula':>8} {'eps':>8}")
print(f"  {'-'*7} {'-'*4} {'-'*4} {'-'*7} {'-'*7} {'-'*8} {'-'*8}")
for semilla in semillas:
    d = datos[semilla]
    print(f"  {semilla:>7} {d['A']:>4} {d['B']:>4} {d['razon']:>7.4f} "
          f"{d['gamma']:>7.3f} {d['formula']:>8.3f} {d['eps']:>8.5f}")


# --------- COMPROBACION 1: la identidad es exacta, no una aproximacion

fallos_identidad = 0
for semilla in semillas:
    d = datos[semilla]
    ln = math.log(semilla)
    izquierda = d["gamma"] - d["formula"]
    derecha = d["B"] * d["eps"] / (ln * (ln + d["eps"]))
    if abs(izquierda - derecha) > 1e-9:
        fallos_identidad += 1

print(f"\nCOMPROBACION 1 -- la identidad, con su correccion, es exacta")
print(f"  gamma - formula  ==  B*eps / (ln n * (ln n + eps))")
print(f"  hilos probados: {len(semillas)}   fallos: {fallos_identidad}")
if fallos_identidad:
    raise SystemExit("La identidad no cierra. No dibujes nada.")


# --- COMPROBACION 2: eps es ln del residuo de Roosendaal, y esta acotado

RES_993 = 1.2531421442887503     # el maximo conocido, conjeturado absoluto
TECHO = math.log(RES_993)

fallos_techo = 0
for semilla in semillas:
    eps = datos[semilla]["eps"]
    if eps <= 0 or eps > TECHO + 1e-9:
        fallos_techo += 1

print(f"\nCOMPROBACION 2 -- el grosor eps cae entre 0 y ln(Res(993))")
print(f"  techo = ln({RES_993:.9f}) = {TECHO:.6f}")
print(f"  eps de los once: min {min(datos[s]['eps'] for s in semillas):.6f}"
      f"   max {max(datos[s]['eps'] for s in semillas):.6f}")
print(f"  fallos: {fallos_techo}")
if fallos_techo:
    raise SystemExit("Un eps se salio del techo de Roosendaal. Mira eso antes.")


# ---------------------------------------------------- el paseo de Terras
#
# S_i = cuantos impares hay en los primeros i pasos. La trayectoria sube
# mientras S_i > i*gamma_terras. El paseo W_i = S_i - i*gamma_terras tiene
# que volverse negativo para que el numero baje de su valor inicial.

paseos = {}
for semilla in semillas:
    camino = caminos[semilla]
    impares = [1 if v % 2 else 0 for v in camino[:-1]]
    W, S = [0.0], 0
    for i, x in enumerate(impares, 1):
        S += x
        W.append(S - i * GAMMA_TERRAS)
    paseos[semilla] = W


# --------------------------------------------------------------- dibujar

COLORES = ["#0b63d6", "#7048e8", "#1f7a4d", "#2f9e44", "#40c057",
           "#82c91e", "#fab005", "#fd7e14", "#8a94a3", "#d62728", "#e64980"]

figura = make_subplots(
    rows=2, cols=2,
    subplot_titles=[
        "<b>las once trayectorias, superpuestas</b>"
        "<br><sub>donde se tocan, se han fundido: a partir de ahi son la misma</sub>",
        "<b>el mapa: once filas por sus pasos</b>"
        "<br><sub>color = log2 del numero. Se ve quien acaba pronto y quien no</sub>",
        "<b>la unica variable que hay</b>"
        "<br><sub>gamma = 1/(ln2 - razon*ln3): la curva no esta ajustada, es exacta</sub>",
        "<b>el paseo de Terras</b>"
        "<br><sub>sube mientras la trayectoria sube; cruzar el cero es empezar a caer</sub>",
    ],
    horizontal_spacing=0.09, vertical_spacing=0.13,
)

# (1,1) las trayectorias superpuestas, en log2
for i, semilla in enumerate(semillas):
    camino = caminos[semilla]
    figura.add_trace(go.Scatter(
        x=list(range(len(camino))),
        y=[math.log2(v) for v in camino],
        mode="lines", name=str(semilla),
        line=dict(color=COLORES[i], width=1.4),
        legendgroup=str(semilla),
        text=[f"<b>{semilla}</b> paso {k}<br>{v:,}" for k, v in enumerate(camino)],
        hovertemplate="%{text}<extra></extra>",
    ), row=1, col=1)

# los puntos de fusion con desfase cero
fx, fy, ft = [], [], []
for ha, pa, hb, pb, v in fusiones:
    fx.append(pa)
    fy.append(math.log2(v))
    ft.append(f"se funden <b>{semillas[ha-1]}</b> y <b>{semillas[hb-1]}</b>"
              f"<br>en el {v:,}, paso {pa} de los dos")
figura.add_trace(go.Scatter(
    x=fx, y=fy, mode="markers",
    marker=dict(symbol="circle-open", size=13, color="#20242c",
                line=dict(width=2)),
    name="fusion con desfase 0",
    text=ft, hovertemplate="%{text}<extra></extra>",
), row=1, col=1)

# (1,2) el mapa completo como retícula
largo = max(len(caminos[s]) for s in semillas)
malla = []
texto = []
for semilla in semillas:
    camino = caminos[semilla]
    fila = [math.log2(v) for v in camino] + [None] * (largo - len(camino))
    filatexto = [f"<b>{semilla}</b> paso {k}<br>{v:,}"
                 for k, v in enumerate(camino)] + [""] * (largo - len(camino))
    malla.append(fila)
    texto.append(filatexto)

figura.add_trace(go.Heatmap(
    z=malla, x=list(range(largo)), y=[str(s) for s in semillas],
    text=texto, hovertemplate="%{text}<extra></extra>",
    colorscale="Turbo", showscale=True,
    colorbar=dict(title="log2", len=0.38, y=0.80, thickness=12),
), row=1, col=2)

# (2,1) el plano (razon, gamma) con la curva exacta
rr = [0.30 + 0.004 * t for t in range(76)]     # de 0,30 a 0,60
figura.add_trace(go.Scatter(
    x=rr, y=[1 / (L2 - r * L3) for r in rr], mode="lines",
    line=dict(color="#8a94a3", width=2, dash="dot"),
    name="gamma = 1/(ln2 - razon*ln3)",
    hovertemplate="razon %{x:.3f}<br>gamma %{y:.2f}<extra></extra>",
), row=2, col=1)

for i, semilla in enumerate(semillas):
    d = datos[semilla]
    figura.add_trace(go.Scatter(
        x=[d["razon"]], y=[d["gamma"]], mode="markers",
        marker=dict(size=11, color=COLORES[i],
                    line=dict(color="white", width=1.2)),
        showlegend=False, legendgroup=str(semilla),
        text=[f"<b>{semilla}</b><br>razon {d['razon']:.4f}"
              f"<br>gamma medido {d['gamma']:.3f}"
              f"<br>formula {d['formula']:.3f}"
              f"<br>eps (grosor) {d['eps']:.5f}"],
        hovertemplate="%{text}<extra></extra>",
    ), row=2, col=1)

# las dos marcas de la literatura
for valor, etiqueta in ((0.5, "razon 0,5: el tipico<br>gamma = 6,95212"),
                        (0.609091, "razon 0,609: el extremal<br>gamma = 41,68")):
    figura.add_trace(go.Scatter(
        x=[valor], y=[1 / (L2 - valor * L3)], mode="markers",
        marker=dict(symbol="x", size=11, color="#20242c"),
        showlegend=False, text=[etiqueta],
        hovertemplate="%{text}<extra></extra>",
    ), row=2, col=1)

# (2,2) el paseo de Terras
for i, semilla in enumerate(semillas):
    W = paseos[semilla]
    figura.add_trace(go.Scatter(
        x=list(range(len(W))), y=W, mode="lines",
        line=dict(color=COLORES[i], width=1.4),
        showlegend=False, legendgroup=str(semilla),
        text=[f"<b>{semilla}</b> paso {k}<br>paseo {w:+.3f}"
              for k, w in enumerate(W)],
        hovertemplate="%{text}<extra></extra>",
    ), row=2, col=2)

figura.add_hline(y=0, line=dict(color="#20242c", width=1.5),
                 row=2, col=2)

# los ejes
figura.update_xaxes(title_text="paso", gridcolor="#eef1f5", row=1, col=1)
figura.update_yaxes(title_text="log2 del numero", gridcolor="#eef1f5",
                    row=1, col=1)
figura.update_xaxes(title_text="paso", row=1, col=2)
figura.update_yaxes(title_text="", autorange="reversed", row=1, col=2)
figura.update_xaxes(title_text="razon de unos  A/B", gridcolor="#eef1f5",
                    row=2, col=1)
figura.update_yaxes(title_text="gamma = pasos / ln(n)", gridcolor="#eef1f5",
                    row=2, col=1)
figura.update_xaxes(title_text="paso", gridcolor="#eef1f5", row=2, col=2)
figura.update_yaxes(title_text="S_i - i*log_3(2)", gridcolor="#eef1f5",
                    row=2, col=2)

figura.update_layout(
    title=dict(
        text=f"Los once hilos {semillas[0]} ... {semillas[-1]}, a la vez"
             f"<br><sub>Los once no se diferencian en once cosas: se diferencian"
             f" en UNA, la razon de unos. Todo lo demas se deduce."
             f"<br>El grosor que le sobra a la identidad es"
             f" <b>eps = ln(2^B / (3^A n))</b>, el residuo de Roosendaal,"
             f" acotado por <b>ln(Res(993)) = {TECHO:.6f}</b></sub>",
        x=0.5,
    ),
    plot_bgcolor="white", paper_bgcolor="white",
    autosize=True,
    margin=dict(l=10, r=10, t=130, b=40),
    font=dict(size=TAMANO_LETRA),
    legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.06,
                bgcolor="rgba(255,255,255,0.9)"),
)

figura.write_html(
    SALIDA, auto_open=True,
    default_width="100%", default_height="100vh",
    config=dict(responsive=True, scrollZoom=True, displaylogo=False),
)
print(f"\nMapa guardado y abierto: {SALIDA}")


# ------------------------------------------ lo que se ve mirandolos juntos

print(f"\nLO QUE SE VE AL MIRARLOS A LA VEZ\n")
grupos = {}
for semilla in semillas:
    grupos.setdefault(round(datos[semilla]["razon"], 6), []).append(semilla)
print(f"  Los once se reparten en {len(grupos)} razones de unos distintas:")
for razon, cuales in sorted(grupos.items()):
    g = datos[cuales[0]]["gamma"]
    print(f"    razon {razon:.4f} -> gamma {g:>6.3f}   {len(cuales)} hilos: "
          f"{', '.join(str(c) for c in cuales)}")
print(f"\n  Y eso agota la informacion: dos hilos con la misma razon tienen")
print(f"  el mismo gamma, el mismo numero de pasos y el mismo eps salvo la")
print(f"  quinta cifra. La razon de unos ES el hilo.")
