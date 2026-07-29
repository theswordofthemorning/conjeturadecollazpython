# collazarbol.py
#
# El arbol de Collatz sobre la esfera.
#
# TRONCO: la trayectoria del numero, de ida (F) y de vuelta (B), cerrando el
#         circulo completo. El polo sur es el 1, el polo norte es la semilla.
#
# RAMAS:  en cada VORTICE del tronco brota una rama hacia atras, con numeros
#         nuevos derivados por la propia regla. Nada viene de fuera.
#
# La regla para retroceder desde un numero v es corta:
#     - v siempre tiene un padre:  v * 2
#     - y tiene un SEGUNDO padre solo si v deja resto 4 al dividirlo entre 6;
#       ese segundo padre es  (v - 1) / 3
# Donde hay dos padres hay bifurcacion. Eso es un vortice.
#
#   punto ROJO  = numero impar (de el se sale con  n * 3 + 1)
#   punto AZUL  = numero par   (de el se sale con  n / 2)
#
# Genera un .html que se abre solo: girar con el mouse, zoom con la rueda,
# y el cursor encima de cualquier punto te dice que numero es.

import math
import plotly.graph_objects as go


# ---------------------------------------------------------------------------

NUMERO = 221

PROFUNDIDAD_RAMA = 14     # cuantos pasos hacia atras crece cada rama
APERTURA = 60.0           # cuanto se abre una rama al bifurcarse, en grados
MAX_NODOS = 8000          # freno de seguridad: el arbol completo es inmenso

MOSTRAR_NUMEROS_TRONCO = True
MOSTRAR_NUMEROS_RAMAS = False
TAMANO_LETRA = 9


# ---------------------------------------------------------------- la cuenta

def secuencia_de(n):
    camino = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        camino.append(n)
    return camino


def padres(v):
    """De donde puede venir v. Aqui es donde nacen los vortices."""
    lista = [v * 2]
    if v % 6 == 4 and v != 4:      # el 4 se excluye: su otro padre es el 1
        lista.append((v - 1) // 3)
    return lista


tronco = secuencia_de(NUMERO)
pasos = len(tronco) - 1

vortices = [v for v in tronco if v % 6 == 4 and v != 4]
print(f"{NUMERO}: {pasos} pasos.")
print(f"Vortices en el tronco (numeros con dos padres): {len(vortices)}")
print(f"  {vortices}")


# ---------------------------------------------------------------- la esfera
#
# La altura de un numero la marca su distancia al 1:
#   distancia 0   -> polo sur  (el 1)
#   distancia 114 -> polo norte (la semilla)
# La longitud (hacia donde apunta) no la deciden los numeros: es una eleccion
# de dibujo. Aqui las ramas se reparten en abanico alrededor de la bola.

def posicion(distancia_al_1, longitud):
    caida = math.radians((pasos - distancia_al_1) * (180.0 / pasos))
    giro = math.radians(longitud)
    return (math.sin(caida) * math.cos(giro),
            math.sin(caida) * math.sin(giro),
            math.cos(caida))


# --- el tronco: ida por una cara, vuelta por la otra ---

tronco_puntos = []     # (x, y, z, valor, distancia, mitad)

for i, v in enumerate(tronco):                       # ida
    d = pasos - i
    x, y, z = posicion(d, 0)
    tronco_puntos.append((x, y, z, v, d, "F"))

for i in range(pasos - 1, 0, -1):                    # vuelta, por detras
    v = tronco[i]
    d = pasos - i
    x, y, z = posicion(d, 180)
    tronco_puntos.append((x, y, z, v, d, "B"))


# --- las ramas ---

brotes = []            # de donde sale cada rama
for i in range(1, len(tronco)):
    v = tronco[i]
    d = pasos - i
    if d + 1 > pasos:                 # no se puede crecer por encima del polo
        continue
    for p in padres(v):
        if p != tronco[i - 1]:        # el padre del tronco no cuenta: ya esta
            brotes.append((d, v, p))

print(f"Ramas que brotan del tronco: {len(brotes)}")

rama_puntos = []       # (x, y, z, valor, distancia)
rama_lineas = []       # (punto, punto)
cortado = False

for k, (d_vortice, v_vortice, primer_padre) in enumerate(brotes):
    longitud_inicial = (k + 0.5) * 360.0 / len(brotes)
    origen = posicion(d_vortice, 0)

    pila = [(primer_padre, d_vortice + 1, longitud_inicial, APERTURA, origen)]

    while pila:
        if len(rama_puntos) >= MAX_NODOS:
            cortado = True
            break

        valor, d, longitud, apertura, viene_de = pila.pop()
        if d > pasos:
            continue

        aqui = posicion(d, longitud)
        rama_lineas.append((viene_de, aqui))
        rama_puntos.append((aqui[0], aqui[1], aqui[2], valor, d))

        if d - (d_vortice + 1) >= PROFUNDIDAD_RAMA:
            continue

        siguientes = padres(valor)
        if len(siguientes) == 1:
            pila.append((siguientes[0], d + 1, longitud, apertura, aqui))
        else:
            pila.append((siguientes[0], d + 1, longitud - apertura / 2,
                         apertura / 2, aqui))
            pila.append((siguientes[1], d + 1, longitud + apertura / 2,
                         apertura / 2, aqui))

    if cortado:
        break

print(f"Numeros nuevos dibujados en las ramas: {len(rama_puntos):,}")
if cortado:
    print(f"  AVISO: se corto en {MAX_NODOS:,} nodos. El arbol entero es mucho")
    print(f"  mayor; no lo estas viendo completo. Sube MAX_NODOS o baja")
    print(f"  PROFUNDIDAD_RAMA para ver otra porcion.")


# ---------------------------------------------------------------- el dibujo

figura = go.Figure()

# La bola, casi transparente, solo para dar sensacion de planeta.
malla_u = [i * math.pi / 30 for i in range(31)]
malla_v = [j * 2 * math.pi / 60 for j in range(61)]
figura.add_trace(go.Surface(
    x=[[0.985 * math.sin(u) * math.cos(v) for v in malla_v] for u in malla_u],
    y=[[0.985 * math.sin(u) * math.sin(v) for v in malla_v] for u in malla_u],
    z=[[0.985 * math.cos(u) for v in malla_v] for u in malla_u],
    colorscale=[[0, "#e3e7ee"], [1, "#e3e7ee"]],
    opacity=0.25, showscale=False, hoverinfo="skip", showlegend=False,
))


# Las ramas, todas en un solo trazo con cortes entre medio.
rx, ry, rz = [], [], []
for desde, hasta in rama_lineas:
    rx += [desde[0], hasta[0], None]
    ry += [desde[1], hasta[1], None]
    rz += [desde[2], hasta[2], None]

figura.add_trace(go.Scatter3d(
    x=rx, y=ry, z=rz, mode="lines",
    line=dict(color="#aab2c0", width=1.5),
    name="ramas", hoverinfo="skip",
))

for color, nombre, quiero_par in (("blue", "par  (n ÷ 2)", True),
                                  ("red", "impar  (n × 3 + 1)", False)):
    cuales = [p for p in rama_puntos if (p[3] % 2 == 0) == quiero_par]
    if not cuales:
        continue
    figura.add_trace(go.Scatter3d(
        x=[p[0] for p in cuales], y=[p[1] for p in cuales], z=[p[2] for p in cuales],
        mode="markers", marker=dict(color=color, size=2.5),
        name=f"rama · {nombre}",
        text=[f"<b>{p[3]}</b><br>a {p[4]} pasos del 1" for p in cuales],
        hovertemplate="%{text}<extra></extra>",
    ))


# El tronco, encima de todo y mas grueso.
figura.add_trace(go.Scatter3d(
    x=[p[0] for p in tronco_puntos] + [tronco_puntos[0][0]],
    y=[p[1] for p in tronco_puntos] + [tronco_puntos[0][1]],
    z=[p[2] for p in tronco_puntos] + [tronco_puntos[0][2]],
    mode="lines", line=dict(color="#2b3038", width=5),
    name=f"tronco: {NUMERO} → 1 → {NUMERO}", hoverinfo="skip",
))

for color, nombre, quiero_par in (("blue", "par  (n ÷ 2)", True),
                                  ("red", "impar  (n × 3 + 1)", False)):
    cuales = [p for p in tronco_puntos if (p[3] % 2 == 0) == quiero_par]
    figura.add_trace(go.Scatter3d(
        x=[p[0] for p in cuales], y=[p[1] for p in cuales], z=[p[2] for p in cuales],
        mode="markers", marker=dict(color=color, size=5,
                                    line=dict(color="white", width=1)),
        name=f"tronco · {nombre}",
        text=[f"<b>{p[3]}</b><br>{p[5]} · a {p[4]} pasos del 1" for p in cuales],
        hovertemplate="%{text}<extra></extra>",
    ))


# Los vortices: los puntos del tronco donde de verdad brota algo.
son_vortice = [p for p in tronco_puntos if p[3] % 6 == 4 and p[3] != 4]
figura.add_trace(go.Scatter3d(
    x=[p[0] for p in son_vortice], y=[p[1] for p in son_vortice],
    z=[p[2] for p in son_vortice],
    mode="markers",
    marker=dict(color="rgba(0,0,0,0)", size=11,
                line=dict(color="#c26a00", width=3)),
    name="vortices (dos padres)",
    text=[f"<b>{p[3]}</b><br>vortice · padres: {p[3]*2} y {(p[3]-1)//3}"
          for p in son_vortice],
    hovertemplate="%{text}<extra></extra>",
))


# Los dos polos.
figura.add_trace(go.Scatter3d(
    x=[0, 0], y=[0, 0], z=[1, -1], mode="markers",
    marker=dict(color="#111318", size=8, symbol="diamond"),
    name="polos",
    text=[f"polo norte<br><b>{NUMERO}</b>, la semilla",
          "polo sur<br><b>el 1</b>, donde llega todo"],
    hovertemplate="%{text}<extra></extra>",
))


def poner_numeros(puntos, indice_valor, nombre):
    figura.add_trace(go.Scatter3d(
        x=[p[0] * 1.06 for p in puntos], y=[p[1] * 1.06 for p in puntos],
        z=[p[2] * 1.06 for p in puntos],
        mode="text", text=[str(p[indice_valor]) for p in puntos],
        textfont=dict(size=TAMANO_LETRA, color="#20242c"),
        name=nombre, hoverinfo="skip", showlegend=False,
    ))


if MOSTRAR_NUMEROS_TRONCO:
    poner_numeros(tronco_puntos, 3, "numeros del tronco")
if MOSTRAR_NUMEROS_RAMAS:
    poner_numeros(rama_puntos, 3, "numeros de las ramas")


sin_eje = dict(showbackground=False, showgrid=False, zeroline=False,
               showticklabels=False, title="", visible=False)

figura.update_layout(
    title=dict(
        text=f"El arbol de Collatz del {NUMERO} sobre la esfera"
             f"<br><sub>tronco de {pasos} pasos · {len(brotes)} vortices ·"
             f" {len(rama_puntos):,} numeros nuevos, todos derivados por la regla"
             f"{' · VISTA RECORTADA' if cortado else ''}</sub>",
        x=0.5,
    ),
    scene=dict(xaxis=sin_eje, yaxis=sin_eje, zaxis=sin_eje,
               aspectmode="cube",
               camera=dict(eye=dict(x=1.6, y=1.5, z=0.8))),
    paper_bgcolor="white", width=1150, height=1000,
    legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.88)"),
)

archivo = f"arbol_{NUMERO}.html"
figura.write_html(archivo, auto_open=True)
print("Grafico guardado y abierto en el navegador:", archivo)
