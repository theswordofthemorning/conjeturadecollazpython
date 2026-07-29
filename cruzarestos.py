# cruzarestos.py
#
# LA MALLA DE RESTOS CRUZADA CONTRA EL 221 Y EL 1276.
#
# Los dos lados se calculan por separado, y esa es toda la gracia:
#
#   LADO A (la malla) : para cada resto del 0 al 63 se toma un numero cualquiera
#                       que deje ese resto y se anota su arranque de 6 pasos.
#                       Aqui no se usa el 221 para nada.
#
#   LADO B (la trayectoria) : se recorre el 221 hasta el 1 y se mira, numero por
#                       numero, en que resto cae y como arranca DE VERDAD.
#
# Si el lado A predice bien el lado B, la malla sirve. El programa lo comprueba
# en los 173 numeros de las dos trayectorias y dice cuantos falla.
#
# OJO CON EL MAPA. Esto se hace con la regla CLASICA (3n+1), no con el atajo.
# Con el atajo el 1276 no aparece en la trayectoria del 221 —la ruta es otra— y
# toda la estructura del paso 57 se cae. El atajo da la biyeccion perfecta, la
# clasica da tu 221. No son la misma cosa y no se pueden mezclar.
#
# COMO SE LEE EL DIBUJO:
#
#   Los meridianos son los 64 restos y estan pintados segun quien los visita:
#     VERDE   = solo la primera mitad del 221 (posiciones 0 a 56)
#     NARANJA = solo la segunda mitad (que es la trayectoria del 1276)
#     ROJO    = las dos mitades pasan por ahi
#     GRIS    = ningun numero de las dos trayectorias cae nunca en ese resto
#
#   La linea negra que va dando saltos por el ecuador es EL PASEO: el orden real
#   en que el 221 va cayendo de resto en resto, del primero al ultimo.
#
#   Los puntitos rojos y azules de los paralelos son la malla de siempre: en ese
#   paso toca impar o par.

import math
import collections
import plotly.graph_objects as go


# ---------------------------------------------------------------------------
# Cambia esto aqui, guarda, y dale a Ctrl+B en Sublime.
# ---------------------------------------------------------------------------

K = 6               # pasos de arranque -> 2^K restos
NUMERO = 221        # la trayectoria grande
NUMERO_MITAD = 1276 # el numero del medio (posicion 57 del 221)

TAMANO_LETRA = 11
MOSTRAR_PASEO = True


MODULO = 2 ** K


# ------------------------------------------------------------- las cuentas

def paso(n):
    """La regla clasica de Collatz."""
    return n // 2 if n % 2 == 0 else 3 * n + 1


def secuencia_de(n):
    camino = [n]
    while n != 1:
        n = paso(n)
        camino.append(n)
    return camino


def patron_de_arranque(n, cuantos):
    """Los primeros `cuantos` pasos de n, como P (par) e I (impar)."""
    letras = []
    for _ in range(cuantos):
        letras.append("P" if n % 2 == 0 else "I")
        n = paso(n)
    return "".join(letras)


# --- LADO A: la malla, hecha sin mirar el 221 ---
#
# Para cada resto se usa un representante que no tiene nada que ver con las
# trayectorias: el propio resto mas una vuelta del modulo.

patron_del_resto = {}
for resto in range(MODULO):
    representante = (resto if resto else MODULO) + MODULO
    patron_del_resto[resto] = patron_de_arranque(representante, K)

print(f"LADO A — la malla de restos, k = {K}, modulo {MODULO}")
print(f"  {MODULO} restos, cada uno con su arranque de {K} pasos.")
print(f"  patrones distintos: {len(set(patron_del_resto.values()))}"
      f"  (con la regla clasica no salen los {MODULO}: dos impares nunca van")
print(f"  seguidos, asi que muchos patrones son imposibles)")


# --- LADO B: las trayectorias de verdad ---

grande = secuencia_de(NUMERO)
corte = grande.index(NUMERO_MITAD)
mitad = secuencia_de(NUMERO_MITAD)

print(f"\nLADO B — las trayectorias")
print(f"  {NUMERO}:  {len(grande)} numeros, {len(grande) - 1} pasos")
print(f"  {NUMERO_MITAD}: {len(mitad)} numeros, {len(mitad) - 1} pasos"
      f"  (es la posicion {corte} del {NUMERO})")


# --- EL CRUCE: la malla predice el arranque real? ---

fallos = []
comprobados = 0

for etiqueta, camino in ((str(NUMERO), grande), (str(NUMERO_MITAD), mitad)):
    for posicion, n in enumerate(camino):
        predicho = patron_del_resto[n % MODULO]
        de_verdad = patron_de_arranque(n, K)
        comprobados += 1
        if predicho != de_verdad:
            fallos.append((etiqueta, posicion, n, predicho, de_verdad))

print(f"\nEL CRUCE — la malla contra la realidad")
print(f"  numeros comprobados : {comprobados}")
print(f"  FALLOS              : {len(fallos)}")
for f in fallos[:5]:
    print(f"    {f[0]} posicion {f[1]}, n={f[2]}: decia {f[3]}, era {f[4]}")
if fallos:
    raise SystemExit("La malla no predice. Algo esta mal, no sigas.")
print(f"  -> la malla, calculada sin mirar el {NUMERO}, acierta el arranque de")
print(f"     los {comprobados} numeros de las dos trayectorias. Ni uno falla.")


# --- QUE RESTOS VISITA, Y QUE RESTOS NO ---

cuenta = collections.Counter(n % MODULO for n in grande)
visitados = set(cuenta)
nunca = sorted(set(range(MODULO)) - visitados)

primera = {n % MODULO for n in grande[:corte]}
segunda = {n % MODULO for n in grande[corte:]}

solo_primera = sorted(primera - segunda)
solo_segunda = sorted(segunda - primera)
las_dos = sorted(primera & segunda)

print(f"\nQUE RESTOS PISA EL {NUMERO}")
print(f"  restos distintos visitados: {len(visitados)} de {MODULO}")
print(f"  nunca visitados           : {len(nunca)}  ->  {nunca}")
print(f"\n  solo la primera mitad (posiciones 0-{corte - 1}): {len(solo_primera)}")
print(f"  solo la segunda mitad (el {NUMERO_MITAD})        : {len(solo_segunda)}")
print(f"  las dos mitades                            : {len(las_dos)}")
print(f"    -> {las_dos}")

# Lo que daria el puro azar, para saber si esto significa algo.
esperado = MODULO * (1 - (1 - 1 / MODULO) ** len(grande))
print(f"\n  COBERTURA: {len(visitados)} restos en {len(grande)} numeros.")
print(f"    si cayeran al azar se esperarian {esperado:.1f}")
print(f"    observado {len(visitados)}")
print(f"    -> la diferencia es de {len(visitados) - esperado:+.1f}. Es la")
print(f"       cobertura del azar: el {NUMERO} NO prefiere ningun resto.")
print(f"       Esto es un resultado NEGATIVO y hay que anotarlo como tal.")

print(f"\n  los restos mas pisados (el ciclo final 1-4-2 pasa por 1, 4 y 2):")
for resto, veces in cuenta.most_common(5):
    print(f"    resto {resto:>2}: {veces} veces   arranque {patron_del_resto[resto]}")


# ------------------------------------------------------------- la geometria
#
# Los restos van en los meridianos (cierran) y los pasos en los paralelos
# (no cierran). El ecuador queda libre porque los paralelos caen a 180/(K+1)
# grados y ninguno toca los 90 exactos: ahi se dibuja el paseo.

def bajada_del_paso(k):
    return k * 180.0 / (K + 1)


def giro_del_resto(resto):
    return resto * 360.0 / MODULO


def punto(k, resto):
    bajada = math.radians(bajada_del_paso(k))
    giro = math.radians(giro_del_resto(resto))
    return (math.sin(bajada) * math.cos(giro),
            math.sin(bajada) * math.sin(giro),
            math.cos(bajada))


def en_el_ecuador(resto, radio=1.0):
    giro = math.radians(giro_del_resto(resto))
    return (math.cos(giro) * radio, math.sin(giro) * radio, 0.0)


def aro_del_paso(k, cuantos=240):
    bajada = math.radians(bajada_del_paso(k))
    return [(math.sin(bajada) * math.cos(math.radians(t * 360.0 / cuantos)),
             math.sin(bajada) * math.sin(math.radians(t * 360.0 / cuantos)),
             math.cos(bajada)) for t in range(cuantos + 1)]


def arco_del_resto(resto, cuantos=120):
    giro = math.radians(giro_del_resto(resto))
    return [(math.sin(math.radians(t * 180.0 / cuantos)) * math.cos(giro),
             math.sin(math.radians(t * 180.0 / cuantos)) * math.sin(giro),
             math.cos(math.radians(t * 180.0 / cuantos))) for t in range(cuantos + 1)]


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


malla_u = [t * math.pi / 30 for t in range(31)]
malla_v = [t * 2 * math.pi / 60 for t in range(61)]
figura.add_trace(go.Surface(
    x=[[0.97 * math.sin(u) * math.cos(v) for v in malla_v] for u in malla_u],
    y=[[0.97 * math.sin(u) * math.sin(v) for v in malla_v] for u in malla_u],
    z=[[0.97 * math.cos(u) for v in malla_v] for u in malla_u],
    colorscale=[[0, "#f2f5f9"], [1, "#f2f5f9"]],
    opacity=0.18, showscale=False, hoverinfo="skip", showlegend=False,
))

# Los paralelos: los K pasos.
trazo_de_lineas([aro_del_paso(k) for k in range(1, K + 1)],
                "#c3cad6", 2, f"los {K} pasos del arranque")


# --- los meridianos, pintados segun quien los visita ---

grupos = (
    (nunca, "#c9ced6", 1, f"nunca visitado  ({len(nunca)} restos)"),
    (solo_primera, "#1f7a4d", 3,
     f"solo la 1a mitad del {NUMERO}  ({len(solo_primera)})"),
    (solo_segunda, "#e8590c", 3,
     f"solo la 2a mitad = el {NUMERO_MITAD}  ({len(solo_segunda)})"),
    (las_dos, "#d62728", 5, f"las dos mitades  ({len(las_dos)})"),
)

for restos, color, ancho, nombre in grupos:
    if restos:
        trazo_de_lineas([arco_del_resto(r) for r in restos], color, ancho, nombre)


# --- la malla de fondo: en cada paso toca impar o par ---

for letra, color, nombre in (("I", "#d62728", "impar  →  n × 3 + 1"),
                             ("P", "#1f77b4", "par    →  n ÷ 2")):
    ex, ye, ze, textos = [], [], [], []
    for k in range(1, K + 1):
        for resto in range(MODULO):
            if patron_del_resto[resto][k - 1] != letra:
                continue
            x, y, z = punto(k, resto)
            ex.append(x)
            ye.append(y)
            ze.append(z)
            veces = cuenta.get(resto, 0)
            textos.append(
                f"<b>resto {resto}</b> (mod {MODULO})  ·  <b>paso {k}</b><br>"
                f"arranque: <b>{patron_del_resto[resto]}</b><br>"
                f"el {NUMERO} cae aqui {veces} "
                f"{'vez' if veces == 1 else 'veces'}"
            )
    figura.add_trace(go.Scatter3d(
        x=ex, y=ye, z=ze, mode="markers",
        marker=dict(size=4, color=color, opacity=0.75,
                    line=dict(color="white", width=0.5)),
        name=f"{nombre}   ({len(ex)})",
        text=textos, hovertemplate="%{text}<extra></extra>",
    ))


# --- EL PASEO: el orden real en que el 221 va cayendo de resto en resto ---

if MOSTRAR_PASEO:
    restos_del_paseo = [n % MODULO for n in grande]
    sitios = [en_el_ecuador(r) for r in restos_del_paseo]

    figura.add_trace(go.Scatter3d(
        x=[v[0] for v in sitios], y=[v[1] for v in sitios], z=[v[2] for v in sitios],
        mode="lines",
        line=dict(color="#20242c", width=2),
        name=f"el paseo del {NUMERO}: {len(grande) - 1} saltos de resto en resto",
        hoverinfo="skip",
    ))
    figura.add_trace(go.Scatter3d(
        x=[v[0] for v in sitios], y=[v[1] for v in sitios], z=[v[2] for v in sitios],
        mode="markers",
        marker=dict(size=4, color=list(range(len(grande))),
                    colorscale=[[0, "#f7d8a0"], [0.5, "#5b8dd9"], [1, "#0b2447"]],
                    colorbar=dict(title=dict(text="posicion en<br>la trayectoria",
                                             side="right"),
                                  thickness=14, len=0.40, x=0.98)),
        name="donde cae cada numero",
        text=[f"posicion <b>{i}</b> del {NUMERO}<br>"
              f"el numero es <b>{n:,}</b><br>"
              f"resto {n % MODULO} (mod {MODULO})<br>"
              f"arranque {patron_del_resto[n % MODULO]}"
              + (f"<br><br>ES EL {NUMERO_MITAD}: la mitad exacta" if i == corte else "")
              for i, n in enumerate(grande)],
        hovertemplate="%{text}<extra></extra>",
    ))

    # El numero del medio, marcado.
    medio = en_el_ecuador(NUMERO_MITAD % MODULO)
    figura.add_trace(go.Scatter3d(
        x=[medio[0]], y=[medio[1]], z=[medio[2]], mode="markers",
        marker=dict(symbol="diamond", size=13, color="#d62728",
                    line=dict(color="white", width=2)),
        name=f"el {NUMERO_MITAD} (posicion {corte}, la mitad exacta)",
        text=[f"<b>{NUMERO_MITAD:,}</b><br>posicion {corte} del {NUMERO}"
              f"<br>resto {NUMERO_MITAD % MODULO} (mod {MODULO})"],
        hovertemplate="%{text}<extra></extra>",
    ))


# --- los numeros de resto ---

sitios, etiquetas, colores = [], [], []
for resto in range(MODULO):
    fuera = 1.10 + (resto % 2) * 0.10
    sitios.append(en_el_ecuador(resto, fuera))
    etiquetas.append(str(resto))

figura.add_trace(go.Scatter3d(
    x=[v[0] for v in sitios], y=[v[1] for v in sitios], z=[v[2] for v in sitios],
    mode="text", text=etiquetas,
    textfont=dict(size=TAMANO_LETRA, color="#7a3e00"),
    hoverinfo="skip", showlegend=False,
))

sitios, etiquetas = [], []
for k in range(1, K + 1):
    base = punto(k, 0)
    sitios.append((base[0] * 1.22, base[1] * 1.22, base[2] * 1.22))
    etiquetas.append(f"paso {k}")
figura.add_trace(go.Scatter3d(
    x=[v[0] for v in sitios], y=[v[1] for v in sitios], z=[v[2] for v in sitios],
    mode="text", text=etiquetas,
    textfont=dict(size=TAMANO_LETRA, color="#1f4e79"),
    hoverinfo="skip", showlegend=False,
))


sin_eje = dict(showbackground=False, showgrid=False, zeroline=False,
               showticklabels=False, title="", visible=False)

figura.update_layout(
    title=dict(
        text=f"La malla de restos (mod {MODULO}) cruzada contra el {NUMERO}"
             f" y el {NUMERO_MITAD}"
             f"<br><sub>la malla se calculo sin mirar las trayectorias y acierta"
             f" el arranque de los {comprobados} numeros: {len(fallos)} fallos"
             f"<br>pero solo pisa {len(visitados)} de {MODULO} restos, y el azar"
             f" daria {esperado:.1f}: NO hay preferencia por ningun resto"
             f"  ·  regla clasica 3n+1</sub>",
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

archivo = f"cruce_restos_k{K}_{NUMERO}_{NUMERO_MITAD}.html"
figura.write_html(
    archivo,
    auto_open=True,
    default_width="100%",
    default_height="100vh",
    config=dict(responsive=True, scrollZoom=True, displaylogo=False),
)
print("\nGrafico guardado y abierto en el navegador:", archivo)
