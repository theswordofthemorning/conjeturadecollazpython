# mallascerradas.py
#
# LAS MALLAS QUE CIERRAN SOLAS, Y LA RUEDA QUE COLLATZ LLEVA DENTRO.
#
# Este era el plan original del laboratorio, pendiente desde antes de todo lo
# demas: construir mallas circulares con numeros que SI cierren entre ellos
# --independientes de Collatz--, guardarlas, y cruzarlas despues contra los
# numeros que genera Collatz buscando coincidencias de patron. Con el filtro
# de siempre: las mallas tienen que salir DISTINTAS entre progresiones, o el
# cruce no significa nada.
#
# PARTE 1 -- LOS AROS QUE CIERRAN SOLOS (ninguno es Collatz):
#
#   n -> n + 7   (mod 30)     cierra en 30 pasos  (la formula: 30/mcd(30,7))
#   Fibonacci    (mod 10)     cierra en 60 pasos  (el periodo de Pisano)
#   n -> 2n      (mod 27)     cierra en 18 pasos  (el orden de 2 modulo 27)
#   n -> n^2     (mod 100)    NO cierra limpio: renacuajos (cola + aro)
#
#   Cuatro reglas, cuatro cierres distintos, medidos caminando y no supuestos.
#   Eso es la discriminacion: cada progresion trae su aro de tamano propio, y
#   la del cuadrado ni siquiera trae aro limpio. Si todas dieran lo mismo, la
#   maquinaria no estaria midiendo nada.
#
# PARTE 2 -- EL CRUCE. Y aqui esta el hallazgo de esta pieza:
#
#   El arbol de Collatz se construye hacia atras DOBLANDO: v, 2v, 4v, 8v...
#   Y doblar modulo m es exactamente una de las progresiones cerradas de la
#   parte 1. O sea que el arbol lleva una de nuestras mallas dentro de serie.
#
#   Ya estaba verificado (collazarbol.py) que un numero tiene segundo padre si
#   y solo si deja resto 4 al dividirlo entre 6. Lo que eso implica al caminar
#   un rayo de duplicaciones, y que este programa comprueba brote a brote:
#
#     v multiplo de 3       -> el rayo NO brota nunca (rayo mudo)
#     v con resto 1 mod 3   -> brota exactamente en k = 2, 4, 6, ...
#     v con resto 2 mod 3   -> brota exactamente en k = 1, 3, 5, ...
#
#   EL RITMO DE BROTES ES PERIODICO DE PERIODO 2: el aro de 2 modulo 3.
#
#   Y hay una segunda rueda engranada: el hijo que brota en 2^k v es
#   u = (2^k v - 1)/3, siempre impar, y su clase mod 3 (que decide si el rayo
#   nuevo sera mudo, de fase par o de fase impar) la fija 2^k v mod 9. Entre
#   brote y brote se multiplica por 4, y 4 tiene orden 3 modulo 9 (4, 7, 1).
#   Asi que LAS CLASES DE LOS HIJOS CICLAN 1 -> 2 -> 0 CON PERIODO 3, siempre
#   en ese orden, empezando donde diga 2^k v mod 9.
#
#   Y la rueda maestra que engrana las dos: el patron completo de un rayo
#   (donde brota, y de que clase fina mod 9 es cada hijo) lo fija 2^k v mod 27,
#   que da vueltas al aro de 2 modulo 27. Orden: 18. El patron entero de
#   CUALQUIER rayo del arbol se repite cada 18 duplicaciones, exactas.
#
#   18 es el MISMO aro de "n -> 2n (mod 27)" de la parte 1, construido sin
#   mirar Collatz. Y el eco llega mas lejos: ese aro recorre los 18 numeros
#   que no son multiplos de 3, y deja fuera los 9 multiplos de 3 -- los mismos
#   que en el arbol hacen rayos mudos. La coincidencia de patron que buscaba
#   el plan original existe, y no es estadistica: es exacta.
#
# HONESTIDAD, en dos puntos. (1) Esto es matematica conocida: la estructura
# mod 6 / mod 9 del arbol inverso es estandar en la literatura de Collatz.
# Llegamos por nuestra cuenta, no es un descubrimiento. (2) La rueda gobierna
# la CONTABILIDAD del arbol hacia atras (donde brota, que clase de hijo). El
# destino hacia adelante sigue ciego a los restos: el negativo de
# cruzarestos.py (el 221 no prefiere ningun resto) sigue en pie. Las dos cosas
# son ciertas a la vez: el esqueleto es periodico, el viaje no.
#
# El programa comprueba todo antes de dibujar y se para si algo falla.

import math
import collections
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ---------------------------------------------------------------------------
# Cambia esto aqui, guarda, y dale a Ctrl+B en Sublime.
# ---------------------------------------------------------------------------

RAYOS = 200        # cuantos rayos impares se comprueban (v = 1, 3, 5, ...)
K_MAX = 44         # hasta donde se dobla cada rayo al comprobar

V_DIBUJO = 39      # el panel del ritmo dibuja los rayos impares 1 ... V_DIBUJO
K_DIBUJO = 24      # y hasta esta duplicacion
TAMANO_LETRA = 9


# ----------------------------------------------------- PARTE 1: los aros

def caminar_hasta_repetir(estado, paso):
    """Aplica la regla hasta pisar un estado ya visto.

    Devuelve (cola, aro): cuantos pasos tarda en entrar al ciclo, y cuanto
    mide el ciclo.
    """
    visto = {}
    i = 0
    while estado not in visto:
        visto[estado] = i
        estado = paso(estado)
        i += 1
    return visto[estado], i - visto[estado]


print("PARTE 1 -- LOS AROS QUE CIERRAN SOLOS  (medidos caminando)\n")

fallos_parte1 = 0

# n -> n + 7 (mod 30)
cola, aro_suma = caminar_hasta_repetir(0, lambda n: (n + 7) % 30)
esperado = 30 // math.gcd(30, 7)
print(f"  n -> n+7 (mod 30)   : cola {cola}, aro {aro_suma}"
      f"   (la formula 30/mcd(30,7) da {esperado})")
if cola != 0 or aro_suma != esperado:
    fallos_parte1 += 1

# Fibonacci (mod 10) y (mod 100): el estado es el par (a, b)
cola, aro_fib10 = caminar_hasta_repetir((0, 1), lambda p: (p[1], (p[0] + p[1]) % 10))
print(f"  Fibonacci (mod 10)  : cola {cola}, aro {aro_fib10}"
      f"   (el periodo de Pisano de 10 es 60)")
if cola != 0 or aro_fib10 != 60:
    fallos_parte1 += 1

cola, aro_fib100 = caminar_hasta_repetir((0, 1), lambda p: (p[1], (p[0] + p[1]) % 100))
print(f"  Fibonacci (mod 100) : cola {cola}, aro {aro_fib100}"
      f"   (el de 100 es 300)")
if cola != 0 or aro_fib100 != 300:
    fallos_parte1 += 1

# n -> 2n (mod 3^j): el orden de 2. La formula es 2 por 3^(j-1).
aros_dupl = []
for j in range(1, 6):
    modulo = 3 ** j
    cola, aro = caminar_hasta_repetir(1, lambda n, m=modulo: (2 * n) % m)
    aros_dupl.append(aro)
    if cola != 0 or aro != 2 * 3 ** (j - 1):
        fallos_parte1 += 1
print(f"  n -> 2n (mod 3^j)   : aros {aros_dupl} para j = 1 ... 5"
      f"   (la formula 2·3^(j-1) da {[2 * 3 ** (j - 1) for j in range(1, 6)]})")

# n -> n^2 (mod 100): renacuajos
ciclos_cuad = set()
peor_cola = 0
for n in range(100):
    cola, aro = caminar_hasta_repetir(n, lambda x: (x * x) % 100)
    peor_cola = max(peor_cola, cola)
    # reconstruir el ciclo para contarlo una sola vez
    x = n
    for _ in range(cola):
        x = (x * x) % 100
    ciclo = [x]
    y = (x * x) % 100
    while y != x:
        ciclo.append(y)
        y = (y * y) % 100
    ciclos_cuad.add(tuple(sorted(ciclo)))
largos_cuad = sorted({len(c) for c in ciclos_cuad})
print(f"  n -> n^2 (mod 100)  : NO cierra limpio: {len(ciclos_cuad)} ciclos"
      f" de largos {largos_cuad}, colas de hasta {peor_cola}")

if fallos_parte1:
    raise SystemExit("Un aro no dio su cierre esperado. No sigas.")

print(f"\n  -> cuatro reglas, cuatro cierres distintos: {aro_suma}, {aro_fib10},"
      f" {aros_dupl[2]}, y renacuajos.")
print(f"     La maquinaria discrimina. Cada progresion trae su aro propio.")


# ------------------------------------- PARTE 2: la rueda dentro del arbol

print(f"\nPARTE 2 -- LA RUEDA QUE COLLATZ LLEVA DENTRO")
print(f"  (rayos de duplicacion v, 2v, 4v, ... con v impar; un numero brota")
print(f"   si tiene segundo padre, o sea si deja resto 4 al dividirlo entre 6)\n")

CLASE_DEL_RESTO9 = {1: 0, 4: 1, 7: 2}   # 2^k·v mod 9  ->  clase del hijo mod 3

rayos_mudos = rayos_pares = rayos_impares = 0
fallos_ritmo = 0
fallos_hijos = 0
transiciones_hijos = 0
brotes_totales = 0

for indice in range(RAYOS):
    v = 2 * indice + 1
    brotes = []          # las k donde brota
    hijos = []           # el hijo de cada brote
    w = v
    for k in range(1, K_MAX + 1):
        w = w * 2
        if w % 6 == 4:
            brotes.append(k)
            hijos.append((w - 1) // 3)

    # COMPROBACION 1: el ritmo es periodo 2 con la fase que manda v mod 3
    if v % 3 == 0:
        esperados = []
        rayos_mudos += 1
    elif v % 3 == 1:
        esperados = list(range(2, K_MAX + 1, 2))
        rayos_pares += 1
    else:
        esperados = list(range(1, K_MAX + 1, 2))
        rayos_impares += 1
    if brotes != esperados:
        fallos_ritmo += 1

    # COMPROBACION 2: las clases de los hijos ciclan sumando 1 (mod 3),
    # y la primera la fija 2^k·v mod 9
    if brotes:
        brotes_totales += len(brotes)
        primera_w = v * 2 ** brotes[0]
        if hijos[0] % 3 != CLASE_DEL_RESTO9[primera_w % 9]:
            fallos_hijos += 1
        for j in range(len(hijos) - 1):
            transiciones_hijos += 1
            if hijos[j + 1] % 3 != (hijos[j] % 3 + 1) % 3:
                fallos_hijos += 1

print(f"COMPROBACION 1 -- el ritmo de brotes es periodico de periodo 2")
print(f"  rayos probados: {RAYOS} (hasta k = {K_MAX})")
print(f"    mudos (v multiplo de 3)      : {rayos_mudos}")
print(f"    brotan en k pares  (resto 1) : {rayos_pares}")
print(f"    brotan en k impares (resto 2): {rayos_impares}")
print(f"  rayos que no cumplieron su patron: {fallos_ritmo}")
if fallos_ritmo:
    raise SystemExit("El ritmo falla. No sigas.")

print(f"\nCOMPROBACION 2 -- los hijos ciclan 1 -> 2 -> 0 con periodo 3")
print(f"  brotes revisados: {brotes_totales:,}   transiciones: {transiciones_hijos:,}")
print(f"  fallos: {fallos_hijos}")
if fallos_hijos:
    raise SystemExit("El ciclo de los hijos falla. No sigas.")
print(f"  la clase del hijo la fija 2^k·v mod 9: " + str(CLASE_DEL_RESTO9))

# COMPROBACION 3: la rueda maestra. El patron completo del rayo (donde brota
# y la clase fina mod 9 de cada hijo) se repite cada 18 duplicaciones, y 18
# es el orden de 2 modulo 27 -- el aro de la parte 1.

def patron_del_rayo(v, k_max):
    patron = []
    w = v
    for k in range(1, k_max + 1):
        w = w * 2
        patron.append((w - 1) // 3 % 9 if w % 6 == 4 else None)
    return patron


fallos_maestra = 0
for indice in range(RAYOS):
    v = 2 * indice + 1
    patron = patron_del_rayo(v, K_MAX)
    minimo = None
    for d in (1, 2, 3, 6, 9, 18):
        if all(patron[i] == patron[i + d] for i in range(len(patron) - d)):
            minimo = d
            break
    esperado = 1 if v % 3 == 0 else 18
    if minimo != esperado:
        fallos_maestra += 1

print(f"\nCOMPROBACION 3 -- la rueda maestra: todo el patron repite cada 18")
print(f"  rayos probados: {RAYOS}   fallos: {fallos_maestra}")
if fallos_maestra:
    raise SystemExit("La rueda maestra falla. No sigas.")
print(f"  y 18 es el orden de 2 modulo 27: EL MISMO aro de la parte 1.")

# el aro de 2 mod 27 recorre justo los no-multiplos de 3
orbita_27 = [1]
while True:
    siguiente = (2 * orbita_27[-1]) % 27
    if siguiente == 1:
        break
    orbita_27.append(siguiente)
fuera_del_aro = sorted(set(range(27)) - set(orbita_27))   # el 0 tambien es multiplo de 3
if sorted(orbita_27) != [n for n in range(1, 27) if n % 3 != 0]:
    raise SystemExit("La orbita de 2 mod 27 no es la esperada. No sigas.")
print(f"  el aro recorre los {len(orbita_27)} numeros que no son multiplos de 3,")
print(f"  y deja fuera {fuera_del_aro} -- los multiplos de 3, los mismos que en")
print(f"  el arbol hacen rayos mudos. El eco es exacto.")

# COMPROBACION 4: contra los datos viejos del repo -- los vortices del 221
def secuencia_de(n):
    camino = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        camino.append(n)
    return camino


tronco = secuencia_de(221)
vortices = [w for w in tronco if w % 6 == 4 and w != 4]
fallos_vortices = sum(
    1 for w in vortices
    if (w - 1) // 3 % 3 != CLASE_DEL_RESTO9[w % 9]
)
print(f"\nCOMPROBACION 4 -- contra los datos viejos: los vortices del 221")
print(f"  vortices en el tronco: {len(vortices)} (el numero de siempre: 50)")
print(f"  que cumplen la regla de la rueda (2^k·v mod 9): "
      f"{len(vortices) - fallos_vortices}   fallos: {fallos_vortices}")
if len(vortices) != 50 or fallos_vortices:
    raise SystemExit("Los vortices del 221 no cuadran. No sigas.")

print(f"\nLA COINCIDENCIA QUE BUSCABA EL PLAN ORIGINAL")
print(f"  La malla circular de n -> 2n (mod 27) -- 18 pasos, construida sin")
print(f"  mirar Collatz -- es exactamente el tambor del arbol: cada rayo brota")
print(f"  al compas del aro de 2 mod 3 (periodo 2), sus hijos ciclan al compas")
print(f"  del aro de 4 mod 9 (periodo 3), y el patron entero repite cada 18.")
print(f"  No es estadistica: es exacta, brote a brote.")
print(f"  Limite honesto: la rueda gobierna el esqueleto del arbol hacia atras.")
print(f"  El destino hacia adelante sigue ciego a los restos (cruzarestos.py).")


# ------------------------------------------------------------- el dibujo

titulo_1 = f"<b>n -> n+7 (mod 30)</b><br><sub>cierra en {aro_suma} pasos</sub>"
titulo_2 = f"<b>Fibonacci (mod 10)</b><br><sub>cierra en {aro_fib10} (Pisano)</sub>"
titulo_3 = (f"<b>n -> 2n (mod 27) · LA RUEDA MAESTRA</b>"
            f"<br><sub>cierra en {aros_dupl[2]} · evita los multiplos de 3</sub>")
titulo_4 = (f"<b>el ritmo del arbol de Collatz</b>"
            f"<br><sub>brota cada 2 · hijos ciclan 1-2-0 cada 3 ·"
            f" todo repite cada 18</sub>")

figura = make_subplots(
    rows=2, cols=2,
    subplot_titles=[titulo_1, titulo_2, titulo_3, titulo_4],
    horizontal_spacing=0.08, vertical_spacing=0.12,
)


def sitio_en_aro(i, modulo, radio=1.0):
    """La casilla i de un aro de `modulo` posiciones, empezando arriba."""
    angulo = math.pi / 2 - 2 * math.pi * i / modulo
    return radio * math.cos(angulo), radio * math.sin(angulo)


def dibujar_aro(fila, columna, modulo, recorrido, color, nombre):
    """Un aro numerado y el recorrido dibujado como poligonal entre casillas."""
    # el circulo de referencia
    borde = [sitio_en_aro(t / 4.0, modulo) for t in range(4 * modulo + 1)]
    figura.add_trace(go.Scatter(
        x=[p[0] for p in borde], y=[p[1] for p in borde], mode="lines",
        line=dict(color="#dfe3ea", width=1), hoverinfo="skip", showlegend=False,
    ), row=fila, col=columna)

    # las casillas numeradas
    casillas = [sitio_en_aro(i, modulo, 1.16) for i in range(modulo)]
    figura.add_trace(go.Scatter(
        x=[p[0] for p in casillas], y=[p[1] for p in casillas],
        mode="text", text=[str(i) for i in range(modulo)],
        textfont=dict(size=TAMANO_LETRA, color="#20242c"),
        hoverinfo="skip", showlegend=False,
    ), row=fila, col=columna)

    # el recorrido
    puntos = [sitio_en_aro(i, modulo) for i in recorrido]
    figura.add_trace(go.Scatter(
        x=[p[0] for p in puntos], y=[p[1] for p in puntos], mode="lines",
        line=dict(color=color, width=1.6), opacity=0.75,
        name=nombre, hoverinfo="skip", showlegend=False,
    ), row=fila, col=columna)


# (1,1) la estrella del +7
recorrido_suma = [(7 * t) % 30 for t in range(aro_suma + 1)]
dibujar_aro(1, 1, 30, recorrido_suma, "#0b63d6", "n+7")

# (1,2) el paseo de Fibonacci por los digitos
fib = [0, 1]
while len(fib) < aro_fib10 + 1:
    fib.append((fib[-1] + fib[-2]) % 10)
dibujar_aro(1, 2, 10, fib[:aro_fib10 + 1], "#7048e8", "fibonacci")

# (2,1) la rueda maestra: la orbita de 2 mod 27
dibujar_aro(2, 1, 27, orbita_27 + [orbita_27[0]], "#d62728", "x2 mod 27")
# los multiplos de 3, marcados como los que el aro evita
mudos = [sitio_en_aro(m, 27) for m in fuera_del_aro]
figura.add_trace(go.Scatter(
    x=[p[0] for p in mudos], y=[p[1] for p in mudos], mode="markers",
    marker=dict(symbol="circle-open", size=10, color="#8a94a3",
                line=dict(width=2)),
    name="multiplos de 3: el aro los evita (y en el arbol son rayos mudos)",
    text=[f"<b>{m}</b><br>multiplo de 3: el aro no pasa por aqui"
          for m in fuera_del_aro],
    hovertemplate="%{text}<extra></extra>",
), row=2, col=1)

# (2,2) el ritmo del arbol: filas = rayos, columnas = duplicaciones
COLOR_CLASE = {0: "#8a94a3", 1: "#1f7a4d", 2: "#e8590c"}
NOMBRE_CLASE = {0: "hijo multiplo de 3 (rayo nuevo mudo)",
                1: "hijo con resto 1 (brotara en pares)",
                2: "hijo con resto 2 (brotara en impares)"}

# las lineas guia de cada rayo
guia_x, guia_y = [], []
for v in range(1, V_DIBUJO + 1, 2):
    guia_x += [1, K_DIBUJO, None]
    guia_y += [v, v, None]
figura.add_trace(go.Scatter(
    x=guia_x, y=guia_y, mode="lines",
    line=dict(color="#eef1f5", width=1), hoverinfo="skip", showlegend=False,
), row=2, col=2)

# los brotes, por clase de hijo
por_clase = {0: [], 1: [], 2: []}
for v in range(1, V_DIBUJO + 1, 2):
    w = v
    for k in range(1, K_DIBUJO + 1):
        w = w * 2
        if w % 6 == 4:
            hijo = (w - 1) // 3
            por_clase[hijo % 3].append((k, v, w, hijo))

for clase in (1, 2, 0):
    datos = por_clase[clase]
    figura.add_trace(go.Scatter(
        x=[d[0] for d in datos], y=[d[1] for d in datos], mode="markers",
        marker=dict(size=7, color=COLOR_CLASE[clase],
                    line=dict(color="white", width=0.8)),
        name=NOMBRE_CLASE[clase],
        text=[f"rayo del <b>{d[1]}</b> · duplicacion k={d[0]}"
              f"<br>2^{d[0]}·{d[1]} = {d[2]:,}"
              f"<br>brota el hijo <b>{d[3]:,}</b> (clase {d[3] % 3})"
              for d in datos],
        hovertemplate="%{text}<extra></extra>",
    ), row=2, col=2)

# la etiqueta de cada rayo, coloreada segun su fase
figura.add_trace(go.Scatter(
    x=[0.2] * len(range(1, V_DIBUJO + 1, 2)),
    y=list(range(1, V_DIBUJO + 1, 2)),
    mode="text", text=[str(v) for v in range(1, V_DIBUJO + 1, 2)],
    textfont=dict(
        size=TAMANO_LETRA + 1,
        color=[COLOR_CLASE[v % 3 if v % 3 else 0] if v % 3 == 0
               else COLOR_CLASE[v % 3] for v in range(1, V_DIBUJO + 1, 2)],
    ),
    hoverinfo="skip", showlegend=False,
), row=2, col=2)

# los ejes: los aros sin ejes y cuadrados; el ritmo con sus ejes visibles
for fila, columna, sufijo in ((1, 1, ""), (1, 2, "2"), (2, 1, "3")):
    figura.update_xaxes(range=[-1.45, 1.45], visible=False,
                        row=fila, col=columna)
    figura.update_yaxes(range=[-1.45, 1.45], visible=False,
                        scaleanchor=f"x{sufijo}", scaleratio=1,
                        row=fila, col=columna)

figura.update_xaxes(title_text="duplicacion k  (v, 2v, 4v, ...)",
                    range=[-0.8, K_DIBUJO + 0.8], dtick=2,
                    gridcolor="#eef1f5", zeroline=False, row=2, col=2)
figura.update_yaxes(title_text="la semilla impar v de cada rayo",
                    range=[0, V_DIBUJO + 1], dtick=6,
                    gridcolor="#ffffff", zeroline=False, row=2, col=2)

figura.update_layout(
    title=dict(
        text=f"Las mallas que cierran solas, y la rueda que Collatz lleva dentro"
             f"<br><sub>cuatro cierres distintos medidos ({aro_suma}, {aro_fib10},"
             f" {aros_dupl[2]}, renacuajos): la maquinaria discrimina"
             f"  ·  y el aro de n->2n (mod 27) es exactamente el tambor del arbol:"
             f" {RAYOS} rayos comprobados, 0 fallos"
             f"<br>en el panel del ritmo: gris = el hijo que brota es multiplo"
             f" de 3 (su rayo sera mudo), verde/naranja = la fase del hijo ·"
             f" las filas de v multiplo de 3 no tienen ni un punto: mudas</sub>",
        x=0.5,
    ),
    plot_bgcolor="white", paper_bgcolor="white",
    autosize=True,
    margin=dict(l=10, r=10, t=130, b=40),
    legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.04,
                bgcolor="rgba(255,255,255,0.9)"),
)

archivo = "mallas_cerradas.html"
figura.write_html(
    archivo,
    auto_open=True,
    default_width="100%",
    default_height="100vh",
    config=dict(responsive=True, scrollZoom=True, displaylogo=False),
)
print("\nGrafico guardado y abierto en el navegador:", archivo)
