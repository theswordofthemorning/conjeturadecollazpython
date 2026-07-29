# collazmalla.py
#
# LA MALLA REAL.
#
# Entre CUALQUIER par de puntos de una trayectoria de Collatz existe una
# igualdad exacta. Si entre los dos puntos hubo A multiplicaciones por 3 y
# B divisiones entre 2, entonces se cumple, sin excepcion:
#
#       2^B * (el numero de llegada)  =  3^A * (el numero de salida)  +  C
#
# Ese C es un entero que sale del propio camino.
#
# Este programa calcula esa relacion para TODOS los pares de la trayectoria,
# comprueba que se cumple, y dibuja el mapa que forman: cada par tiene dos
# coordenadas reales, A y B. Esa es la malla.
#
# La linea diagonal es el punto de equilibrio. Por encima de ella la
# trayectoria cae hacia el 1; por debajo subiria para siempre; justo encima
# giraria en circulo. El unico circulo que existe esta marcado con una estrella:
# es el 1 -> 4 -> 2 -> 1, o sea, la ecuacion 4 = 3 + 1.
#
# Genera un .html que se abre solo. Rueda para zoom, cursor encima para leer.

import math
import plotly.graph_objects as go


NUMERO = 221


def secuencia_de(n):
    camino = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        camino.append(n)
    return camino


seq = secuencia_de(NUMERO)
L = len(seq)

print(f"Trayectoria del {NUMERO}: {L} numeros, {L - 1} pasos.")


# ------------------------------------------- todos los pares y su relacion

casillas = {}      # (A, B) -> {cuantos, ejemplo}
fallos = 0
total_pares = 0

for i in range(L):
    A = B = C = 0
    for j in range(i + 1, L):
        # el paso que va de la posicion j-1 a la j
        if seq[j - 1] % 2 == 1:        # fue 3n+1
            C = 3 * C + 2 ** B
            A += 1
        else:                          # fue n/2
            B += 1

        # la comprobacion, para cada uno de los pares
        if 2 ** B * seq[j] != 3 ** A * seq[i] + C:
            fallos += 1

        total_pares += 1
        if (A, B) not in casillas:
            casillas[(A, B)] = {"cuantos": 0, "desde": seq[i], "hasta": seq[j], "C": C}
        casillas[(A, B)]["cuantos"] += 1

print(f"Pares comprobados: {total_pares:,}")
print(f"Fallos en la identidad: {fallos}")
print(f"Casillas (A,B) distintas: {len(casillas):,}")

if fallos:
    print("La identidad falla. Algo esta mal, no sigas.")
    raise SystemExit


# ------------------------------------------- el balance de la trayectoria

A_total = sum(1 for k in range(L - 1) if seq[k] % 2 == 1)
B_total = (L - 1) - A_total
equilibrio = math.log2(3)

print(f"\nLa trayectoria entera: {A_total} multiplicaciones, {B_total} divisiones.")
print(f"  proporcion divisiones/multiplicaciones = {B_total / A_total:.4f}")
print(f"  punto de equilibrio                    = {equilibrio:.4f}")
print(f"  -> la trayectoria {'CAE hacia el 1' if B_total/A_total > equilibrio else 'SUBE'}")


# ------------------------------------------- el dibujo

listas = sorted(casillas.items())
ejes_A = [a for (a, b), _ in listas]
ejes_B = [b for (a, b), _ in listas]
cuantos = [d["cuantos"] for _, d in listas]


def recorta(n, largo=26):
    t = f"{n:,}"
    return t if len(t) <= largo else t[:largo] + "…"


textos = []
for (a, b), d in listas:
    textos.append(
        f"<b>{a} × 3   y   {b} ÷ 2</b><br>"
        f"{d['cuantos']} pares de la trayectoria caen aqui<br><br>"
        f"ejemplo:  {d['desde']:,} → {d['hasta']:,}<br>"
        f"2^{b} × {d['hasta']:,} = 3^{a} × {d['desde']:,} + {recorta(d['C'])}"
    )

figura = go.Figure()

# La zona de arriba: donde la trayectoria cae hacia el 1.
tope_A = max(ejes_A) + 1
figura.add_trace(go.Scatter(
    x=[0, tope_A, tope_A, 0],
    y=[0, tope_A * equilibrio, max(ejes_B) + 4, max(ejes_B) + 4],
    fill="toself", fillcolor="rgba(120,170,255,0.08)",
    line=dict(width=0), hoverinfo="skip",
    name="por aqui la trayectoria CAE hacia el 1",
))

# La linea de equilibrio.
figura.add_trace(go.Scatter(
    x=[0, tope_A], y=[0, tope_A * equilibrio],
    mode="lines", line=dict(color="#c26a00", width=2, dash="dash"),
    name=f"equilibrio: {equilibrio:.3f} divisiones por multiplicacion",
    hoverinfo="skip",
))

# Las casillas.
figura.add_trace(go.Scatter(
    x=ejes_A, y=ejes_B, mode="markers",
    marker=dict(
        size=9, symbol="square",
        color=cuantos,
        colorscale=[[0, "#dce7f7"], [0.5, "#5b8dd9"], [1, "#12305e"]],
        colorbar=dict(title=dict(text="pares<br>por casilla", side="right"),
                      thickness=14, len=0.5, x=1.02),
        line=dict(color="white", width=0.6),
    ),
    name=f"las {len(casillas)} casillas de la malla",
    text=textos, hovertemplate="%{text}<extra></extra>",
))

# El unico ciclo que existe: 4 = 3 + 1.
figura.add_trace(go.Scatter(
    x=[1], y=[2], mode="markers",
    marker=dict(symbol="star", size=22, color="#d62728",
                line=dict(color="white", width=1.5)),
    name="el unico ciclo:  4 = 3 + 1",
    text=["<b>1 → 4 → 2 → 1</b><br>1 multiplicacion, 2 divisiones<br>"
          "2² = 3¹ + 1<br><b>4 = 3 + 1</b><br><br>"
          "la unica referencia circular de Collatz"],
    hovertemplate="%{text}<extra></extra>",
))

# La trayectoria entera, como un solo par.
figura.add_trace(go.Scatter(
    x=[A_total], y=[B_total], mode="markers",
    marker=dict(symbol="diamond", size=18, color="#111318",
                line=dict(color="white", width=1.5)),
    name=f"la trayectoria entera del {NUMERO}",
    text=[f"<b>{NUMERO} → 1</b><br>{A_total} multiplicaciones, {B_total} divisiones<br>"
          f"2^{B_total} = 3^{A_total} × {NUMERO} + C<br>"
          f"= {recorta(2 ** B_total, 40)}"],
    hovertemplate="%{text}<extra></extra>",
))

figura.add_annotation(
    x=tope_A * 0.62, y=tope_A * equilibrio * 0.62 - 6,
    text="por debajo de la linea<br>el numero subiria para siempre",
    showarrow=False, font=dict(size=10, color="#8a7150"), align="center",
)

figura.update_layout(
    title=dict(
        text=f"La malla real de la trayectoria del {NUMERO}"
             f"<br><sub>{total_pares:,} pares, {len(casillas)} casillas, "
             f"0 fallos en la identidad · cada casilla es una relacion exacta "
             f"entre dos numeros del recorrido</sub>",
        x=0.5,
    ),
    xaxis=dict(title="multiplicaciones por 3   (A)", gridcolor="#eef1f5",
               zeroline=False, dtick=5),
    yaxis=dict(title="divisiones entre 2   (B)", gridcolor="#eef1f5",
               zeroline=False, dtick=10, scaleanchor="x", scaleratio=1),
    plot_bgcolor="white", paper_bgcolor="white",
    width=800, height=1020,
    legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.9)",
                bordercolor="#dfe3ea", borderwidth=1),
)

archivo = f"malla_{NUMERO}.html"
figura.write_html(archivo, auto_open=True)
print("\nGrafico guardado y abierto en el navegador:", archivo)
