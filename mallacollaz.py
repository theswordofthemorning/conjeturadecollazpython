# mallacollaz.py
#
# LA MALLA HECHA CON COLLATZ.
#
# Copia de mallabasica.py, pero en vez de numerar los ejes del 1 al 100 se
# ponen los numeros de verdad de dos trayectorias:
#
#   EJE Y (los paralelos, de polo a polo) : la trayectoria del 221, 115 numeros
#   EJE X (los meridianos, dando la vuelta): la trayectoria del 1276, 58 numeros
#
# El 1276 esta marcado en ROJO: es la posicion 57 del 221, y 57 es la mitad
# exacta de 114. Parte la trayectoria por el medio sin resto.
#
# OJO CON ESTO, QUE CAMBIA LO QUE SIGNIFICA LA MALLA:
#
#   La trayectoria del 1276 no es independiente de la del 221. ES la segunda
#   mitad de la del 221, numero por numero (el programa lo comprueba y lo dice).
#   Asi que el eje X es la cola del eje Y, no otro eje.
#
#   Eso tiene una consecuencia buena: como los dos numeros de cada cruce estan
#   en la MISMA trayectoria, entre ellos vale la identidad exacta que ya se
#   verifico en collazmalla.py:
#
#         2^B * (el de llegada)  =  3^A * (el de salida)  +  C
#
#   O sea que cada casilla de esta malla no es un dibujo: es una ecuacion que
#   se cumple. El programa las comprueba todas y dice cuantas fallan.
#
# El color de cada cruce es cuanto se desvia del equilibrio (log2(3) = 1,585
# divisiones por multiplicacion). Positivo = ese tramo cae hacia el 1.
#
# Los cruces GRISES Y HUECOS son los que van hacia atras (el numero del eje Y
# esta despues del numero del eje X en la trayectoria). Ahi no hay ecuacion que
# comprobar, y por eso se ve el borde en diagonal: es real, no es un recorte.
#
# COMO LEER LOS NUMEROS: ocupa toda la ventana. Las letras tienen tamaño fijo,
# asi que al hacer zoom con la rueda la bola crece y los numeros se SEPARAN y se
# leen mejor. No se deforman. Arrastra con el mouse para girar.

import math
import plotly.graph_objects as go


# ---------------------------------------------------------------------------
# Cambia estos numeros aqui, guarda, y dale a Ctrl+B en Sublime.
# ---------------------------------------------------------------------------

NUMERO_Y = 221      # el eje de los paralelos
NUMERO_X = 1276     # el eje de los meridianos (la posicion 57 del 221)

CADA_CUANTOS_Y = 1  # 1 = todos los numeros, 5 = uno de cada cinco
CADA_CUANTOS_X = 1

TAMANO_LETRA = 11
EQUILIBRIO = math.log2(3)


# ------------------------------------------------------------- las cuentas

def secuencia_de(n):
    camino = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        camino.append(n)
    return camino


eje_y = secuencia_de(NUMERO_Y)
eje_x = secuencia_de(NUMERO_X)

N_Y = len(eje_y)
N_X = len(eje_x)

print(f"EJE Y: trayectoria del {NUMERO_Y} -> {N_Y} numeros, {N_Y - 1} pasos.")
print(f"EJE X: trayectoria del {NUMERO_X} -> {N_X} numeros, {N_X - 1} pasos.")


# Donde esta el numero del eje X dentro de la trayectoria del eje Y.
if NUMERO_X in eje_y:
    corte = eje_y.index(NUMERO_X)
    print(f"\nEl {NUMERO_X} es la posicion {corte} de la trayectoria del {NUMERO_Y}.")
    if (N_Y - 1) % 2 == 0 and corte == (N_Y - 1) // 2:
        print(f"  Y {corte} es la MITAD EXACTA de {N_Y - 1}. Parte el camino sin resto.")
    pegado = eje_y[corte:] == eje_x
    print(f"  seq({NUMERO_Y})[{corte}:] == seq({NUMERO_X}) ?  {pegado}")
    if pegado:
        print(f"  -> la trayectoria del {NUMERO_X} ES la segunda mitad de la del"
              f" {NUMERO_Y}.")
        print(f"     El eje X es la cola del eje Y, no un eje aparte.")
else:
    corte = None
    print(f"\nEl {NUMERO_X} NO aparece en la trayectoria del {NUMERO_Y}.")
    print(f"  Los dos ejes son independientes: no hay identidad que comprobar.")


# --- la identidad exacta entre cada par de posiciones de la trayectoria Y ---
#
# Se recorre igual que en collazmalla.py: para cada posicion de salida i se va
# avanzando hasta j, llevando la cuenta de A (veces que se hizo 3n+1), B (veces
# que se hizo n/2) y C (el arrastre de los "+1").

relacion = {}     # (i, j) -> (A, B, C)

for i in range(N_Y):
    A = B = C = 0
    for j in range(i + 1, N_Y):
        if eje_y[j - 1] % 2 == 1:
            C = 3 * C + 2 ** B
            A += 1
        else:
            B += 1
        relacion[(i, j)] = (A, B, C)


# ------------------------------------------------------------- la geometria
#
# Igual que en mallabasica.py: los paralelos son alturas y los meridianos son
# giros. Los polos quedan libres (por eso N_Y + 1) y los meridianos cierran
# (por eso N_X justo).

def bajada_del_paralelo(p):
    """Grados desde el polo norte hasta el paralelo p (p va de 1 a N_Y)."""
    return p * 180.0 / (N_Y + 1)


def giro_del_meridiano(m):
    """Grados de giro del meridiano m (m va de 1 a N_X)."""
    return (m - 1) * 360.0 / N_X


def punto(p, m):
    bajada = math.radians(bajada_del_paralelo(p))
    giro = math.radians(giro_del_meridiano(m))
    return (math.sin(bajada) * math.cos(giro),
            math.sin(bajada) * math.sin(giro),
            math.cos(bajada))


def aro_del_paralelo(p, cuantos=180):
    bajada = math.radians(bajada_del_paralelo(p))
    salida = []
    for k in range(cuantos + 1):
        giro = math.radians(k * 360.0 / cuantos)
        salida.append((math.sin(bajada) * math.cos(giro),
                       math.sin(bajada) * math.sin(giro),
                       math.cos(bajada)))
    return salida


def arco_del_meridiano(m, cuantos=180):
    giro = math.radians(giro_del_meridiano(m))
    salida = []
    for k in range(cuantos + 1):
        bajada = math.radians(k * 180.0 / cuantos)
        salida.append((math.sin(bajada) * math.cos(giro),
                       math.sin(bajada) * math.sin(giro),
                       math.cos(bajada)))
    return salida


# ------------------------------------- los cruces, con su ecuacion cada uno

hacia_x, hacia_y, hacia_z = [], [], []
desviacion, textos = [], []
atras_x, atras_y, atras_z, atras_texto = [], [], [], []

fallos = 0
comprobados = 0

for p in range(1, N_Y + 1):
    i = p - 1                        # posicion en la trayectoria del eje Y
    for m in range(1, N_X + 1):
        salida_y = eje_y[i]
        salida_x = eje_x[m - 1]
        x, y, z = punto(p, m)

        # Si el eje X es la cola del eje Y, el numero del meridiano m esta en la
        # posicion corte + (m - 1) de la trayectoria grande.
        j = corte + m - 1 if corte is not None else None

        if j is not None and i < j:
            A, B, C = relacion[(i, j)]
            # La comprobacion, casilla por casilla.
            if 2 ** B * eje_y[j] != 3 ** A * eje_y[i] + C:
                fallos += 1
            comprobados += 1

            d = B - A * EQUILIBRIO
            hacia_x.append(x)
            hacia_y.append(y)
            hacia_z.append(z)
            desviacion.append(d)
            textos.append(
                f"<b>{salida_y:,}</b>  →  <b>{salida_x:,}</b><br>"
                f"paralelo {p} (posicion {i})  ×  meridiano {m} (posicion {j})<br>"
                f"{A} veces ×3   y   {B} veces ÷2<br>"
                f"desviacion del equilibrio: {d:+.3f}<br>"
                f"2^{B} × {salida_x:,} = 3^{A} × {salida_y:,} + C"
            )
        else:
            atras_x.append(x)
            atras_y.append(y)
            atras_z.append(z)
            atras_texto.append(
                f"{salida_y:,}  y  {salida_x:,}<br>"
                f"paralelo {p} × meridiano {m}<br>"
                f"va hacia atras: no hay ecuacion"
            )

print(f"\nCRUCES DE LA MALLA: {N_Y} × {N_X} = {N_Y * N_X:,}")
print(f"  con ecuacion (van hacia adelante): {comprobados:,}")
print(f"  hacia atras (grises y huecos)    : {len(atras_x):,}")
print(f"  FALLOS EN LA IDENTIDAD           : {fallos}")
if fallos:
    raise SystemExit("La identidad falla. Algo esta mal, no sigas.")
if comprobados:
    print(f"\n  desviacion del equilibrio: de {min(desviacion):+.3f}"
          f" a {max(desviacion):+.3f}")

pico = max(eje_y)
print(f"\nEl numero mas alto de las dos trayectorias es {pico:,}"
      f" (posicion {eje_y.index(pico)} del {NUMERO_Y}).")


# ------------------------------------------------------------- el dibujo

figura = go.Figure()


def trazo_de_lineas(grupos, color, ancho, nombre, leyenda=True):
    ex, ye, ze = [], [], []
    for puntos in grupos:
        ex.extend([v[0] for v in puntos] + [None])
        ye.extend([v[1] for v in puntos] + [None])
        ze.extend([v[2] for v in puntos] + [None])
    figura.add_trace(go.Scatter3d(
        x=ex, y=ye, z=ze, mode="lines",
        line=dict(color=color, width=ancho),
        name=nombre, hoverinfo="skip", showlegend=leyenda,
    ))


# La bola, muy transparente para que los numeros se lean.
malla_u = [k * math.pi / 30 for k in range(31)]
malla_v = [k * 2 * math.pi / 60 for k in range(61)]
figura.add_trace(go.Surface(
    x=[[0.98 * math.sin(u) * math.cos(v) for v in malla_v] for u in malla_u],
    y=[[0.98 * math.sin(u) * math.sin(v) for v in malla_v] for u in malla_u],
    z=[[0.98 * math.cos(u) for v in malla_v] for u in malla_u],
    colorscale=[[0, "#f2f5f9"], [1, "#f2f5f9"]],
    opacity=0.20, showscale=False, hoverinfo="skip", showlegend=False,
))


# El paralelo del numero marcado: el 1276 esta en la posicion `corte`,
# o sea en el paralelo corte + 1.
paralelo_rojo = corte + 1 if corte is not None else None

trazo_de_lineas(
    [aro_del_paralelo(p) for p in range(1, N_Y + 1) if p != paralelo_rojo],
    "#ccd4e0", 1, f"paralelos: trayectoria del {NUMERO_Y}  ({N_Y} numeros)",
)
trazo_de_lineas(
    [arco_del_meridiano(m) for m in range(2, N_X + 1)],
    "#d5dae3", 1, f"meridianos: trayectoria del {NUMERO_X}  ({N_X} numeros)",
)


# --- EL NUMERO CENTRAL, EN ROJO ---
#
# El 1276 aparece dos veces: como paralelo (es la posicion 57 del 221) y como
# meridiano 1 (es el arranque de su propia trayectoria). Donde se cruzan esta
# el centro de toda la estructura: el 1276 consigo mismo.

if paralelo_rojo is not None:
    trazo_de_lineas([aro_del_paralelo(paralelo_rojo)], "#d62728", 6,
                    f"paralelo {paralelo_rojo}: el {NUMERO_X}"
                    f"  (posicion {corte} del {NUMERO_Y})")

trazo_de_lineas([arco_del_meridiano(1)], "#e8590c", 6,
                f"meridiano 1: el {NUMERO_X} otra vez")


# --- los cruces que van hacia adelante: cada uno es una ecuacion ---

figura.add_trace(go.Scatter3d(
    x=hacia_x, y=hacia_y, z=hacia_z, mode="markers",
    marker=dict(
        size=3.4, color=desviacion,
        colorscale=[[0, "#f7d8a0"], [0.5, "#5b8dd9"], [1, "#0b2447"]],
        colorbar=dict(title=dict(text="desviacion<br>del equilibrio", side="right"),
                      thickness=14, len=0.42, x=0.98),
        opacity=0.9, line=dict(width=0),
    ),
    name=f"cruces con ecuacion: {comprobados:,}  ({fallos} fallos)",
    text=textos, hovertemplate="%{text}<extra></extra>",
))


# --- los cruces que van hacia atras: huecos, para que se vea el borde ---

if atras_x:
    figura.add_trace(go.Scatter3d(
        x=atras_x, y=atras_y, z=atras_z, mode="markers",
        marker=dict(size=2.4, color="rgba(0,0,0,0)",
                    line=dict(color="#b8bfc9", width=1)),
        name=f"cruces hacia atras: {len(atras_x):,}  (sin ecuacion)",
        text=atras_texto, hovertemplate="%{text}<extra></extra>",
    ))


# --- el centro: el numero marcado consigo mismo ---

if paralelo_rojo is not None:
    cx, cy, cz = punto(paralelo_rojo, 1)
    figura.add_trace(go.Scatter3d(
        x=[cx], y=[cy], z=[cz], mode="markers",
        marker=dict(symbol="diamond", size=14, color="#d62728",
                    line=dict(color="white", width=2)),
        name=f"EL CENTRO: el {NUMERO_X} consigo mismo",
        text=[f"<b>{NUMERO_X:,}</b><br>posicion {corte} del {NUMERO_Y}"
              f"<br>mitad exacta de {N_Y - 1} pasos"
              f"<br><br>aqui se cruzan el paralelo y el meridiano rojos"],
        hovertemplate="%{text}<extra></extra>",
    ))
    figura.add_trace(go.Scatter3d(
        x=[cx * 1.30], y=[cy * 1.30], z=[cz * 1.30 + 0.10],
        mode="text", text=[f"<b>{NUMERO_X:,}</b>"],
        textfont=dict(size=TAMANO_LETRA + 8, color="#d62728"),
        hoverinfo="skip", showlegend=False,
    ))


# --- LOS NUMEROS ---
#
# A dos distancias que se alternan, para que dos vecinos no se pisen.

def poner_numeros(sitios, etiquetas, color, nombre):
    figura.add_trace(go.Scatter3d(
        x=[v[0] for v in sitios], y=[v[1] for v in sitios],
        z=[v[2] for v in sitios],
        mode="text", text=etiquetas,
        textfont=dict(size=TAMANO_LETRA, color=color),
        name=nombre, hoverinfo="skip", showlegend=False,
    ))


# Los numeros del eje Y, por delante (sobre el meridiano 1).
sitios, etiquetas = [], []
rojo_sitio, rojo_etiqueta = [], []
for p in range(1, N_Y + 1, CADA_CUANTOS_Y):
    fuera = 1.05 + (p % 2) * 0.08
    base = punto(p, 1)
    sitio = (base[0] * fuera, base[1] * fuera, base[2] * fuera)
    if p == paralelo_rojo:
        rojo_sitio.append(sitio)
        rojo_etiqueta.append(f"<b>{eje_y[p - 1]:,}</b>")
    else:
        sitios.append(sitio)
        etiquetas.append(f"{eje_y[p - 1]:,}")

poner_numeros(sitios, etiquetas, "#1f4e79", f"numeros del {NUMERO_Y}")
if rojo_sitio:
    poner_numeros(rojo_sitio, rojo_etiqueta, "#d62728", "el numero central")


# Los numeros del eje X, repartidos por el ecuador.
sitios, etiquetas = [], []
rojo_sitio, rojo_etiqueta = [], []
for m in range(1, N_X + 1, CADA_CUANTOS_X):
    fuera = 1.07 + (m % 2) * 0.10
    giro = math.radians(giro_del_meridiano(m))
    sitio = (math.cos(giro) * fuera, math.sin(giro) * fuera, 0.0)
    if m == 1:
        rojo_sitio.append(sitio)
        rojo_etiqueta.append(f"<b>{eje_x[0]:,}</b>")
    else:
        sitios.append(sitio)
        etiquetas.append(f"{eje_x[m - 1]:,}")

poner_numeros(sitios, etiquetas, "#7a3e00", f"numeros del {NUMERO_X}")
if rojo_sitio:
    poner_numeros(rojo_sitio, rojo_etiqueta, "#e8590c", "el central otra vez")


# --- los polos ---

figura.add_trace(go.Scatter3d(
    x=[0, 0], y=[0, 0], z=[1, -1], mode="markers",
    marker=dict(color="#111318", size=7, symbol="diamond"),
    name="polos",
    text=[f"polo norte<br>por encima del {eje_y[0]:,} (la semilla)",
          f"polo sur<br>por debajo del {eje_y[-1]} (el final)"],
    hovertemplate="%{text}<extra></extra>",
))


sin_eje = dict(showbackground=False, showgrid=False, zeroline=False,
               showticklabels=False, title="", visible=False)

figura.update_layout(
    title=dict(
        text=f"La malla de Collatz — eje Y: el {NUMERO_Y} ({N_Y} numeros)"
             f"  ·  eje X: el {NUMERO_X} ({N_X} numeros)"
             f"<br><sub>el {NUMERO_X} en rojo es la posicion {corte}, la mitad exacta"
             f" de {N_Y - 1} pasos  ·  {comprobados:,} cruces son una ecuacion exacta,"
             f" {fallos} fallos"
             f"<br>el eje X es la segunda mitad del eje Y: por eso hay ecuacion"
             f" entre cada par  ·  rueda para hacer zoom, los numeros se separan</sub>",
        x=0.5,
    ),
    scene=dict(xaxis=sin_eje, yaxis=sin_eje, zaxis=sin_eje,
               aspectmode="cube",
               camera=dict(eye=dict(x=1.35, y=1.30, z=0.75))),
    paper_bgcolor="white",
    autosize=True,
    margin=dict(l=0, r=0, t=100, b=0),
    legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.9)",
                bordercolor="#dfe3ea", borderwidth=1),
)

archivo = f"malla_collaz_{NUMERO_Y}_{NUMERO_X}.html"
figura.write_html(
    archivo,
    auto_open=True,
    default_width="100%",
    default_height="100vh",
    config=dict(responsive=True, scrollZoom=True, displaylogo=False),
)
print("\nGrafico guardado y abierto en el navegador:", archivo)
