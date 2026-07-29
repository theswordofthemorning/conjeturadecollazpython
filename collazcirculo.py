# collazcirculo.py
#
# Toma un numero, calcula su recorrido de Collatz hasta el 1, y en vez de
# dibujarlo como una recta lo dibuja como una vuelta completa al globo.
#
#   IDA   (F, frontal)  : del numero hasta el 1, por la mitad de delante.
#   VUELTA (B, backside): del 1 de regreso al numero, por la mitad de atras.
#
# El avion nunca retrocede: sigue siempre hacia adelante y termina donde salio.
# Los mismos numeros aparecen dos veces, una en cada mitad.
#
#   circulo ROJO  = ese paso fue  n * 3 + 1   (el numero era impar)
#   circulo AZUL  = ese paso fue  n / 2       (el numero era par)
#   circulo GRIS  = los dos polos: la salida y el punto de giro (el 1)
#
# Genera un archivo .html que se abre solo en el navegador.
# Ahi puedes hacer zoom con la rueda del mouse, arrastrar para moverte,
# y pasar el cursor por encima de un punto para ver que numero es.

import math
import plotly.graph_objects as go


# ---------------------------------------------------------------------------
# Escribe tu numero aqui abajo, guarda, y dale a Ctrl+B en Sublime.
# ---------------------------------------------------------------------------

NUMERO = 221

MOSTRAR_NUMEROS = True   # ponlo en False si quieres el circulo limpio
TAMANO_LETRA = 10        # subelo si necesitas los numeros mas grandes


# ---------------------------------------------------------------- la cuenta

valores = [NUMERO]     # todos los numeros por los que vamos pasando
colores = ["gray"]     # de que color es el circulo de cada numero

n = NUMERO
while n != 1:
    if n % 2 == 0:          # es par  -> lo divido entre 2
        n = n // 2
        colores.append("blue")
    else:                   # es impar -> lo multiplico por 3 y le sumo 1
        n = n * 3 + 1
        colores.append("red")
    valores.append(n)

pasos = len(valores) - 1

print("Numero de partida:", NUMERO)
print("Pasos hasta el 1:", pasos)
print("Numero mas alto del recorrido:", max(valores))


# ---------------------------------------------------------------- la vuelta
#
# La ida ocupa media vuelta y el regreso la otra media, asi que damos
# exactamente el doble de pasos que la recta original.

posiciones_en_la_vuelta = 2 * pasos
grados_por_paso = 360.0 / posiciones_en_la_vuelta


def donde_esta(t):
    """Para el avance t (0, 1, 2...), devuelve su angulo en grados.

    Empezamos arriba del todo (90 grados) y avanzamos en el sentido
    de las agujas del reloj hasta volver al mismo sitio.
    """
    return 90.0 - t * grados_por_paso


def que_numero(t):
    """Que numero del recorrido le toca al avance t.

    En la ida vamos hacia adelante por la lista; en la vuelta, hacia atras.
    """
    if t <= pasos:
        return t
    return posiciones_en_la_vuelta - t


def que_mitad(t):
    if t == 0:
        return "salida"
    if t == pasos:
        return "giro"
    if t < pasos:
        return "F"
    return "B"


# Recorremos toda la vuelta y anotamos donde cae cada cosa.
equis, ye, numero_de, mitad_de, color_de = [], [], [], [], []

for t in range(posiciones_en_la_vuelta):
    angulo = math.radians(donde_esta(t))
    i = que_numero(t)
    equis.append(math.cos(angulo))
    ye.append(math.sin(angulo))
    numero_de.append(valores[i])
    mitad_de.append(que_mitad(t))
    color_de.append(colores[i])


# ---------------------------------------------------------------- el dibujo

figura = go.Figure()


def linea_del_arco(desde, hasta, estilo, nombre):
    """Dibuja el trazo del avion entre dos avances de la vuelta."""
    tramo = list(range(desde, hasta + 1))
    figura.add_trace(go.Scatter(
        x=[equis[t % posiciones_en_la_vuelta] for t in tramo],
        y=[ye[t % posiciones_en_la_vuelta] for t in tramo],
        mode="lines",
        line=dict(color="#c8ccd4", width=2, dash=estilo),
        name=nombre,
        hoverinfo="skip",
    ))


linea_del_arco(0, pasos, "solid", "ida  (F, frontal)")
linea_del_arco(pasos, posiciones_en_la_vuelta, "dot", "vuelta  (B, backside)")


def grupo_de_puntos(color, nombre, tamano):
    """Dibuja todos los circulos de un mismo color."""
    cuales = [t for t in range(posiciones_en_la_vuelta) if color_de[t] == color]
    if not cuales:
        return
    figura.add_trace(go.Scatter(
        x=[equis[t] for t in cuales],
        y=[ye[t] for t in cuales],
        mode="markers",
        marker=dict(color=color, size=tamano, line=dict(color="white", width=1)),
        name=nombre,
        text=[f"<b>{numero_de[t]}</b><br>{mitad_de[t]} · avance {t}" for t in cuales],
        hovertemplate="%{text}<extra></extra>",
    ))


grupo_de_puntos("red", "n × 3 + 1   (impar)", 10)
grupo_de_puntos("blue", "n ÷ 2   (par)", 10)

# Los dos polos: la salida y el punto de giro. Son las bisagras del circulo.
figura.add_trace(go.Scatter(
    x=[equis[0], equis[pasos]],
    y=[ye[0], ye[pasos]],
    mode="markers",
    marker=dict(color="#3c4048", size=18, line=dict(color="white", width=2)),
    name="polos: salida y giro",
    text=[f"<b>{NUMERO}</b><br>salida y llegada", "<b>1</b><br>punto de giro"],
    hovertemplate="%{text}<extra></extra>",
))


# Los numeros van escritos por fuera del circulo, apuntando hacia afuera
# como los rayos de una rueda. Al hacer zoom se separan y se leen bien.
if MOSTRAR_NUMEROS:
    for t in range(posiciones_en_la_vuelta):
        grados = donde_esta(t) % 360
        angulo = math.radians(grados)
        # Para que el texto no quede cabeza abajo en la mitad izquierda.
        if 90 < grados < 270:
            giro_texto = -(grados + 180)
        else:
            giro_texto = -grados
        # Cuantas mas cifras tenga el numero, mas afuera hay que ponerlo
        # para que su punta no se meta encima de los circulos.
        fuera = 1.03 + len(str(numero_de[t])) * 0.008

        figura.add_annotation(
            x=math.cos(angulo) * fuera,
            y=math.sin(angulo) * fuera,
            text=str(numero_de[t]),
            textangle=giro_texto,
            showarrow=False,
            font=dict(size=TAMANO_LETRA, color="#20242c"),
            xanchor="center",
            yanchor="middle",
        )

figura.update_layout(
    title=dict(
        text=f"Collatz de {NUMERO} dado la vuelta al globo"
             f"<br><sub>{pasos} pasos de ida por delante, {pasos} de vuelta por detras"
             f" · {posiciones_en_la_vuelta} posiciones en total</sub>",
        x=0.5,
    ),
    plot_bgcolor="white",
    paper_bgcolor="white",
    width=1000,
    height=1000,
    showlegend=True,
    legend=dict(x=0.5, y=0.5, xanchor="center", yanchor="middle",
                bgcolor="rgba(255,255,255,0.85)"),
)

sin_ejes = dict(showgrid=False, zeroline=False, visible=False)
figura.update_xaxes(range=[-1.35, 1.35], **sin_ejes)
figura.update_yaxes(range=[-1.35, 1.35], scaleanchor="x", scaleratio=1, **sin_ejes)

archivo = f"circulo_{NUMERO}.html"
figura.write_html(archivo, auto_open=True)
print("Grafico guardado y abierto en el navegador:", archivo)
