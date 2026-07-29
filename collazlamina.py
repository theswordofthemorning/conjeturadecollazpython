# collazlamina.py
#
# LA LAMINA.
#
# Al triangulo plano le faltaba su tercera dimension. Se la devolvemos, pero
# no girandolo: usando las magnitudes que ya estaban en la ecuacion.
#
# Cada par de puntos de la trayectoria tiene tres numeros reales:
#   - el tamaño del numero de SALIDA
#   - el tamaño del numero de LLEGADA
#   - cuanto se desvia del equilibrio (divisiones de mas respecto de 1,585)
#
# Y resulta que los 6.555 pares NO llenan el espacio: caen todos sobre una
# lamina finisima, la del plano
#
#       desviacion = tamaño de salida - tamaño de llegada
#
# Ninguno cae por debajo. Y lo poco que sobresalen por encima es exactamente
# la contribucion de los "+1" del 3n+1. Ese "+1" es el grosor de la lamina.
#
# Genera un .html que se abre solo: girar con el mouse, zoom con la rueda.

import math
import plotly.graph_objects as go


NUMERO = 221
EQUILIBRIO = math.log2(3)      # 1,585 divisiones por multiplicacion


def secuencia_de(n):
    camino = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        camino.append(n)
    return camino


seq = secuencia_de(NUMERO)
L = len(seq)


# ----------------------------------------------- los pares y sus magnitudes

salida, llegada, desviacion, altura = [], [], [], []
textos = []
fallos = 0

for i in range(L):
    A = B = C = 0
    for j in range(i + 1, L):
        if seq[j - 1] % 2 == 1:
            C = 3 * C + 2 ** B
            A += 1
        else:
            B += 1

        x, y = seq[i], seq[j]
        if 2 ** B * y != 3 ** A * x + C:
            fallos += 1

        sx, sy = math.log2(x), math.log2(y)
        d = B - A * EQUILIBRIO          # divisiones de mas sobre el equilibrio
        h = d - (sx - sy)               # cuanto sobresale del plano

        salida.append(sx)
        llegada.append(sy)
        desviacion.append(d)
        altura.append(h)
        textos.append(
            f"<b>{x:,} → {y:,}</b><br>"
            f"{A} × 3   y   {B} ÷ 2<br>"
            f"desviacion del equilibrio: {d:+.3f}<br>"
            f"sobresale del plano: {h:.4f}"
        )

print(f"Trayectoria del {NUMERO}: {L - 1} pasos, {len(salida):,} pares.")
print(f"Fallos en la identidad: {fallos}")
if fallos:
    raise SystemExit("La identidad falla. No sigas.")

print(f"\nLA LAMINA")
print(f"  todos los pares caen entre {min(altura):.6f} y {max(altura):.6f}")
print(f"  por encima del plano. Ninguno por debajo: {all(h >= -1e-9 for h in altura)}")
print(f"  grosor de la lamina: {max(altura) - min(altura):.4f}")
print(f"  tamaño del espacio : {max(desviacion) - min(desviacion):.2f}")
print(f"  la lamina ocupa el {100*(max(altura)-min(altura))/(max(desviacion)-min(desviacion)):.2f}% del alto")


# ----------------------------------------------------------- el dibujo

figura = go.Figure()

# El plano, semitransparente, para que se vea que los puntos lo abrazan.
paso_x = [min(salida) + k * (max(salida) - min(salida)) / 12 for k in range(13)]
paso_y = [min(llegada) + k * (max(llegada) - min(llegada)) / 12 for k in range(13)]
figura.add_trace(go.Surface(
    x=paso_x, y=paso_y,
    z=[[sx - sy for sx in paso_x] for sy in paso_y],
    colorscale=[[0, "#b9c4d4"], [1, "#b9c4d4"]],
    opacity=0.28, showscale=False, hoverinfo="skip",
    name="el plano", showlegend=False,
))

figura.add_trace(go.Scatter3d(
    x=salida, y=llegada, z=desviacion,
    mode="markers",
    marker=dict(
        size=2.6,
        color=altura,
        colorscale=[[0, "#cfe0f5"], [0.5, "#3f74c0"], [1, "#0b2447"]],
        colorbar=dict(title=dict(text="cuanto aportan<br>los «+1»", side="right"),
                      thickness=14, len=0.45, x=1.02),
        opacity=0.85,
    ),
    name=f"los {len(salida):,} pares",
    text=textos, hovertemplate="%{text}<extra></extra>",
))

# La trayectoria entera, como un solo par: del NUMERO al 1.
figura.add_trace(go.Scatter3d(
    x=[salida[L - 2]], y=[llegada[L - 2]], z=[desviacion[L - 2]],
    mode="markers",
    marker=dict(symbol="diamond", size=9, color="#d62728",
                line=dict(color="white", width=1)),
    name=f"la trayectoria entera: {NUMERO} → 1",
    text=[textos[L - 2]], hovertemplate="%{text}<extra></extra>",
))

sin_reja = dict(backgroundcolor="white", gridcolor="#e8ecf2",
                zerolinecolor="#d0d6de", showbackground=True)

figura.update_layout(
    title=dict(
        text=f"La lamina de Collatz — trayectoria del {NUMERO}"
             f"<br><sub>{len(salida):,} pares. Ninguno cae por debajo del plano, y lo que "
             f"sobresalen —{max(altura):.3f} como maximo— es solo el «+1» del 3n+1</sub>",
        x=0.5,
    ),
    scene=dict(
        xaxis=dict(title="tamaño del numero de salida", **sin_reja),
        yaxis=dict(title="tamaño del numero de llegada", **sin_reja),
        zaxis=dict(title="divisiones de mas sobre el equilibrio", **sin_reja),
        camera=dict(eye=dict(x=1.7, y=-1.5, z=0.7)),
    ),
    paper_bgcolor="white", width=1100, height=950,
    legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.9)"),
)

archivo = f"lamina_{NUMERO}.html"
figura.write_html(archivo, auto_open=True)
print("\nGrafico guardado y abierto en el navegador:", archivo)
