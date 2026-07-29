# collazcruce.py
#
# Dibuja DOS circulos de Collatz cruzandose sobre una esfera, como los aros
# de una lampara antigua de hierro.
#
# Cada circulo es una trayectoria completa: la ida del numero hasta el 1 por
# una mitad, y la vuelta del 1 al numero por la otra mitad.
#
# Para que dos circulos encajen tienen que tener EXACTAMENTE los mismos pasos,
# o sus puntos no caen en el mismo sitio y la malla queda torcida.
#
#   circulo ROJO  = ese paso fue  n * 3 + 1   (el numero era impar)
#   circulo AZUL  = ese paso fue  n / 2       (el numero era par)
#
# Genera un .html que se abre solo. Con el mouse lo giras, con la rueda haces
# zoom, y pasando el cursor por encima ves que numero es cada punto.

import math
import plotly.graph_objects as go


# ---------------------------------------------------------------------------
# Los dos numeros. Tienen que tener el mismo numero de pasos.
# El 55863 esta elegido a proposito: aguanta hasta el paso 110 sin tocar
# la trayectoria del 221, asi que casi todo su recorrido es suyo.
# ---------------------------------------------------------------------------

NUMERO_A = 221
NUMERO_B = 55863

MOSTRAR_NUMEROS = True   # ponlo en False para ver solo los circulos limpios
TAMANO_LETRA = 9


def secuencia_de(n):
    """El recorrido de n hasta el 1, y el color de cada paso."""
    valores = [n]
    colores = ["gray"]
    while n != 1:
        if n % 2 == 0:
            n = n // 2
            colores.append("blue")
        else:
            n = n * 3 + 1
            colores.append("red")
        valores.append(n)
    return valores, colores


valores_A, colores_A = secuencia_de(NUMERO_A)
valores_B, colores_B = secuencia_de(NUMERO_B)

pasos_A = len(valores_A) - 1
pasos_B = len(valores_B) - 1

if pasos_A != pasos_B:
    print("Estos dos numeros NO encajan.")
    print(f"  {NUMERO_A} tiene {pasos_A} pasos y {NUMERO_B} tiene {pasos_B}.")
    print("  Hacen falta dos numeros con exactamente los mismos pasos.")
    raise SystemExit

pasos = pasos_A
posiciones = 2 * pasos          # la vuelta completa: ida + vuelta
grados_por_paso = 360.0 / posiciones

print(f"{NUMERO_A} y {NUMERO_B}: {pasos} pasos cada uno, {posiciones} posiciones por circulo.")

comunes = set(valores_A) & set(valores_B)
print(f"Numeros que comparten los dos recorridos: {len(comunes)} -> {sorted(comunes, reverse=True)}")


# ---------------------------------------------------------------- la esfera
#
# El eje de la esfera va del polo norte (la semilla) al polo sur (el 1).
# El circulo A se dibuja en un meridiano y el B en el meridiano de al lado,
# girado un cuarto de vuelta. Por eso se cruzan justo en los dos polos.

def recorrer(valores, colores, meridiano, nombre):
    """Reparte una trayectoria alrededor de la esfera por un meridiano."""
    equis, ye, zeta = [], [], []
    etiquetas, colores_punto, textos = [], [], []

    giro = math.radians(meridiano)

    for t in range(posiciones):
        # Cuanto hemos bajado desde el polo norte.
        bajada = math.radians(t * grados_por_paso)

        # En la ida avanzamos por la lista; en la vuelta, hacia atras.
        i = t if t <= pasos else posiciones - t

        if t == 0:
            mitad = "salida"
        elif t == pasos:
            mitad = "giro (el 1)"
        elif t < pasos:
            mitad = "F"
        else:
            mitad = "B"

        equis.append(math.sin(bajada) * math.cos(giro))
        ye.append(math.sin(bajada) * math.sin(giro))
        zeta.append(math.cos(bajada))

        colores_punto.append(colores[i])
        etiquetas.append(str(valores[i]))
        textos.append(f"<b>{valores[i]}</b><br>circulo {nombre} · {mitad} · avance {t}")

    return equis, ye, zeta, etiquetas, colores_punto, textos


circulo_A = recorrer(valores_A, colores_A, 0, str(NUMERO_A))
circulo_B = recorrer(valores_B, colores_B, 90, str(NUMERO_B))


# ---------------------------------------------------------------- el dibujo

figura = go.Figure()


# Una esfera casi transparente por debajo, solo para dar sensacion de bola.
malla_u = [i * math.pi / 30 for i in range(31)]
malla_v = [j * 2 * math.pi / 60 for j in range(61)]
figura.add_trace(go.Surface(
    x=[[0.985 * math.sin(u) * math.cos(v) for v in malla_v] for u in malla_u],
    y=[[0.985 * math.sin(u) * math.sin(v) for v in malla_v] for u in malla_u],
    z=[[0.985 * math.cos(u) for v in malla_v] for u in malla_u],
    colorscale=[[0, "#dfe3ea"], [1, "#dfe3ea"]],
    opacity=0.30,
    showscale=False,
    hoverinfo="skip",
    name="planeta",
    showlegend=False,
))


def dibujar_circulo(datos, estilo, nombre_circulo):
    equis, ye, zeta, etiquetas, colores_punto, textos = datos

    # El trazo del avion, cerrando la vuelta.
    figura.add_trace(go.Scatter3d(
        x=equis + [equis[0]], y=ye + [ye[0]], z=zeta + [zeta[0]],
        mode="lines",
        line=dict(color="#8f97a3", width=3, dash=estilo),
        name=f"trayectoria {nombre_circulo}",
        hoverinfo="skip",
    ))

    # Los circulos de colores.
    for color, titulo in (("red", "n × 3 + 1"), ("blue", "n ÷ 2")):
        cuales = [t for t in range(posiciones) if colores_punto[t] == color]
        if not cuales:
            continue
        figura.add_trace(go.Scatter3d(
            x=[equis[t] for t in cuales],
            y=[ye[t] for t in cuales],
            z=[zeta[t] for t in cuales],
            mode="markers",
            marker=dict(color=color, size=4),
            name=f"{titulo}  ({nombre_circulo})",
            text=[textos[t] for t in cuales],
            hovertemplate="%{text}<extra></extra>",
        ))

    # Los numeros, puestos un poco por fuera de la bola.
    if MOSTRAR_NUMEROS:
        figura.add_trace(go.Scatter3d(
            x=[v * 1.07 for v in equis],
            y=[v * 1.07 for v in ye],
            z=[v * 1.07 for v in zeta],
            mode="text",
            text=etiquetas,
            textfont=dict(size=TAMANO_LETRA, color="#20242c"),
            name=f"numeros {nombre_circulo}",
            hoverinfo="skip",
            showlegend=False,
        ))


dibujar_circulo(circulo_A, "solid", str(NUMERO_A))
dibujar_circulo(circulo_B, "dash", str(NUMERO_B))


# Los dos ejes del circulo A: las dos varillas que atraviesan la rueda.
def dibujar_eje(desde, hasta, nombre, color):
    figura.add_trace(go.Scatter3d(
        x=[desde[0], hasta[0]], y=[desde[1], hasta[1]], z=[desde[2], hasta[2]],
        mode="lines",
        line=dict(color=color, width=5, dash="dot"),
        name=nombre,
        hoverinfo="skip",
    ))


medio = pasos // 2   # el paso del ecuador

dibujar_eje(
    (0, 0, 1.25), (0, 0, -1.25),
    f"eje polar:  {NUMERO_A} ↔ 1",
    "#111318",
)
dibujar_eje(
    (1.25, 0, 0), (-1.25, 0, 0),
    f"eje ecuador:  {valores_A[medio]} ↔ {valores_A[medio]}",
    "#c26a00",
)


# Los puntos donde los dos circulos se tocan de verdad: los dos polos.
figura.add_trace(go.Scatter3d(
    x=[0, 0], y=[0, 0], z=[1, -1],
    mode="markers",
    marker=dict(color="#111318", size=9, symbol="diamond"),
    name="polos: donde se cruzan",
    text=[f"polo norte<br>{NUMERO_A} y {NUMERO_B} salen de aqui",
          "polo sur<br><b>el 1</b>, donde llegan los dos"],
    hovertemplate="%{text}<extra></extra>",
))


sin_eje = dict(showbackground=False, showgrid=False, zeroline=False,
               showticklabels=False, title="", visible=False)

figura.update_layout(
    title=dict(
        text=f"Dos trayectorias de Collatz cruzandose:  {NUMERO_A}  y  {NUMERO_B}"
             f"<br><sub>{pasos} pasos cada una · {posiciones} posiciones por circulo"
             f" · se cruzan en los dos polos</sub>",
        x=0.5,
    ),
    scene=dict(
        xaxis=sin_eje, yaxis=sin_eje, zaxis=sin_eje,
        aspectmode="cube",
        camera=dict(eye=dict(x=1.5, y=1.5, z=0.9)),
    ),
    paper_bgcolor="white",
    width=1100,
    height=1000,
    legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.88)"),
)

archivo = f"cruce_{NUMERO_A}_{NUMERO_B}.html"
figura.write_html(archivo, auto_open=True)
print("Grafico guardado y abierto en el navegador:", archivo)
