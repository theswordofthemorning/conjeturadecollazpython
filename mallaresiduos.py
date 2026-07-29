# mallaresiduos.py
#
# LA MALLA COMPLETA. Y "completa" aqui quiere decir algo exacto y comprobable.
#
# No es la malla de todo Collatz: eso seria demostrar la conjetura. Es la malla
# de los ARRANQUES, y de esos si estan TODOS.
#
# La idea: los primeros k pasos de un numero no dependen del numero entero.
# Dependen solo de su resto al dividirlo entre 2^k. Con k = 6 hay 64 restos, y
# todo numero del mundo cae en uno de esos 64. Su arranque ya esta decidido.
# El programa lo comprueba con numeros de verdad antes de dibujar nada.
#
# HAY DOS VERSIONES DE LA REGLA, Y DAN COSAS DISTINTAS. Importa saberlo:
#
#   CON_ATAJO = True   ->  en los impares se hace (3n+1)/2
#                          Los 2^k restos dan los 2^k patrones posibles, uno
#                          cada uno, sin repetir ni faltar. Biyeccion perfecta.
#                          Esta es la malla completa de verdad: cada patron
#                          imaginable de par/impar le toca a exactamente un
#                          resto. Comprobado de k=1 a k=10.
#
#   CON_ATAJO = False  ->  en los impares se hace 3n+1, la regla clasica
#                          Aqui NO hay biyeccion, y por una razon bonita:
#                          despues de 3n+1 el resultado es siempre par, asi que
#                          NUNCA puede haber dos impares seguidos. Eso prohibe
#                          la mayoria de los patrones.
#
#                          Y los que quedan son FIBONACCI. Los patrones posibles
#                          de k pasos son F(k+2):
#                              k=4 -> 8 = F(6)     k=6  -> 21 = F(8)
#                              k=8 -> 55 = F(10)   k=10 -> 144 = F(12)
#                          Comprobado en los diez. Fibonacci no lo metimos
#                          nosotros: sale solo de que dos impares no pueden ir
#                          juntos. Es la misma cuenta de "cuantas maneras hay de
#                          subir una escalera sin pisar dos escalones seguidos".
#
# EL EJE DE RESTOS CIERRA. Despues del resto 63 viene otra vez el 0. No es una
# eleccion de dibujo como la esfera del arbol: es que el modulo es circular por
# definicion, 64 y 0 son el mismo resto. Por eso los restos van en los
# meridianos, que dan la vuelta.
# Los pasos van en los paralelos, que NO cierran: hay un paso 1 y un paso k, y
# son los dos polos.
#
#   punto ROJO  = en ese paso toca el impar  (3n+1, o (3n+1)/2 con atajo)
#   punto AZUL  = en ese paso toca  n ÷ 2
#
# Genera un .html que ocupa toda la ventana. Rueda para zoom: las letras no
# crecen, asi que los numeros se separan y se leen mejor.

import math
import plotly.graph_objects as go


# ---------------------------------------------------------------------------
# Cambia esto aqui, guarda, y dale a Ctrl+B en Sublime.
#
#   k = 6  ->  64 restos    (se leen bien los numeros)
#   k = 8  -> 256 restos    (mas completo, mas apretado)
# ---------------------------------------------------------------------------

K = 6

CON_ATAJO = True              # True: biyeccion perfecta. False: sale Fibonacci.

CUANTOS_REPRESENTANTES = 12   # numeros distintos por resto para comprobar
CADA_CUANTOS_RESTOS = 1       # 1 = escribe todos los restos
TAMANO_LETRA = 11


MODULO = 2 ** K


# ------------------------------------------------------------- las cuentas

def patron_de_arranque(n, cuantos):
    """Los primeros `cuantos` pasos de n, como texto de P (par) e I (impar).

    No se para al llegar al 1: desde el 1 la regla sigue, asi que el patron
    siempre tiene la longitud pedida.
    """
    letras = []
    for _ in range(cuantos):
        if n % 2 == 0:
            letras.append("P")
            n = n // 2
        else:
            letras.append("I")
            n = (3 * n + 1) // 2 if CON_ATAJO else 3 * n + 1
    return "".join(letras)


def fibonacci(cual):
    """F(1) = 1, F(2) = 1, F(3) = 2, ..."""
    a, b = 1, 1
    for _ in range(cual - 1):
        a, b = b, a + b
    return a


regla = "(3n+1)/2  (con atajo)" if CON_ATAJO else "3n+1  (la clasica)"
print(f"LA MALLA DE LOS ARRANQUES,  k = {K},  regla impar = {regla}")
print(f"  restos al dividir entre 2^{K} = {MODULO}: {MODULO}")
print(f"  patrones de {K} pasos que se podrian imaginar: 2^{K} = {MODULO}")


# --- COMPROBACION 1: el arranque depende solo del resto ---
#
# Para cada resto se toman varios numeros distintos que dejen ese mismo resto
# y se mira si todos dan el mismo patron de arranque.

patron_del_resto = {}
discrepancias = []

for resto in range(MODULO):
    patrones = set()
    for vuelta in range(CUANTOS_REPRESENTANTES):
        n = resto + vuelta * MODULO
        if n == 0:
            n = MODULO * CUANTOS_REPRESENTANTES   # el 0 no sirve, se usa otro
        patrones.add(patron_de_arranque(n, K))
    if len(patrones) != 1:
        discrepancias.append((resto, sorted(patrones)))
    patron_del_resto[resto] = sorted(patrones)[0]

print(f"\nCOMPROBACION 1 — el arranque depende solo del resto")
print(f"  restos probados            : {MODULO}")
print(f"  numeros probados por resto : {CUANTOS_REPRESENTANTES}")
print(f"  restos que dieron mas de un patron: {len(discrepancias)}")
if discrepancias:
    for resto, cuales in discrepancias[:5]:
        print(f"    resto {resto}: {cuales}")
    raise SystemExit("Falla la comprobacion 1. No sigas.")
print(f"  -> los {MODULO * CUANTOS_REPRESENTANTES:,} numeros probados obedecen"
      f" a su resto, sin excepcion.")


# --- COMPROBACION 2: cuantos patrones distintos salen, y son los que deben ---
#
# Con atajo se espera la biyeccion: los 2^k patrones, uno por resto.
# Sin atajo se espera Fibonacci: F(k+2), porque no puede haber dos I seguidas.

todos = [patron_del_resto[r] for r in range(MODULO)]
distintos = set(todos)

print(f"\nCOMPROBACION 2 — cuantos patrones distintos salen")
print(f"  casillas de resto             : {len(todos)}")
print(f"  patrones DISTINTOS que salieron: {len(distintos)}")

if CON_ATAJO:
    print(f"  patrones posibles              : {MODULO}")
    if len(distintos) != MODULO:
        raise SystemExit("Se esperaba biyeccion y no la hay. No sigas.")
    print(f"  -> BIYECCION PERFECTA: {MODULO} restos, {MODULO} patrones, uno por")
    print(f"     uno. Cada patron de par/impar que se pueda escribir le toca a")
    print(f"     exactamente un resto. No falta ninguno y no sobra ninguno.")
    print(f"     ESTA es la malla completa.")
else:
    esperados = fibonacci(K + 2)
    con_dos_impares = [p for p in distintos if "II" in p]
    print(f"  Fibonacci F({K + 2})                : {esperados}")
    print(f"  patrones con dos impares seguidos : {len(con_dos_impares)}")
    if len(distintos) != esperados or con_dos_impares:
        raise SystemExit("La cuenta de Fibonacci no cuadra. No sigas.")
    print(f"  -> NO hay biyeccion, y la razon es exacta: despues de 3n+1 el")
    print(f"     resultado es par, asi que dos impares NUNCA van seguidos.")
    print(f"     Los patrones que sobreviven son {esperados} = F({K + 2}).")
    print(f"     FIBONACCI SALE SOLO. No lo metimos nosotros.")
    print(f"  -> y como {MODULO} restos se reparten {esperados} patrones, hay")
    print(f"     patrones que le tocan a varios restos a la vez.")


# --- el eje de restos cierra ---

print(f"\nEL EJE DE RESTOS CIERRA")
print(f"  despues del resto {MODULO - 1} viene otra vez el 0: {MODULO} y 0 son el")
print(f"  mismo resto. Es el modulo, no es una eleccion de dibujo.")
print(f"  resto 0  -> {patron_del_resto[0]}")
print(f"  resto {MODULO - 1} -> {patron_del_resto[MODULO - 1]}")

print(f"\nEL EJE DE PASOS NO CIERRA")
print(f"  hay un paso 1 y un paso {K}, y no se tocan. Son los dos polos.")

impares_por_paso = [sum(1 for r in range(MODULO) if patron_del_resto[r][k] == "I")
                    for k in range(K)]
print(f"\nCUANTOS RESTOS TOCAN IMPAR EN CADA PASO (de {MODULO})")
for k in range(K):
    print(f"  paso {k + 1}: {impares_por_paso[k]:>4}   "
          f"({100 * impares_por_paso[k] / MODULO:>5.1f}%)")


# ------------------------------------------------------------- la geometria
#
# Los restos van en los meridianos, porque cierran dando la vuelta.
# Los pasos van en los paralelos, porque tienen principio y fin.

def bajada_del_paso(k):
    """Grados desde el polo norte hasta el paso k (k va de 1 a K)."""
    return k * 180.0 / (K + 1)


def giro_del_resto(resto):
    """Grados de giro del resto (va de 0 a MODULO - 1)."""
    return resto * 360.0 / MODULO


def punto(k, resto):
    bajada = math.radians(bajada_del_paso(k))
    giro = math.radians(giro_del_resto(resto))
    return (math.sin(bajada) * math.cos(giro),
            math.sin(bajada) * math.sin(giro),
            math.cos(bajada))


def aro_del_paso(k, cuantos=240):
    bajada = math.radians(bajada_del_paso(k))
    salida = []
    for t in range(cuantos + 1):
        giro = math.radians(t * 360.0 / cuantos)
        salida.append((math.sin(bajada) * math.cos(giro),
                       math.sin(bajada) * math.sin(giro),
                       math.cos(bajada)))
    return salida


def arco_del_resto(resto, cuantos=120):
    giro = math.radians(giro_del_resto(resto))
    salida = []
    for t in range(cuantos + 1):
        bajada = math.radians(t * 180.0 / cuantos)
        salida.append((math.sin(bajada) * math.cos(giro),
                       math.sin(bajada) * math.sin(giro),
                       math.cos(bajada)))
    return salida


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
    x=[[0.98 * math.sin(u) * math.cos(v) for v in malla_v] for u in malla_u],
    y=[[0.98 * math.sin(u) * math.sin(v) for v in malla_v] for u in malla_u],
    z=[[0.98 * math.cos(u) for v in malla_v] for u in malla_u],
    colorscale=[[0, "#f2f5f9"], [1, "#f2f5f9"]],
    opacity=0.20, showscale=False, hoverinfo="skip", showlegend=False,
))

trazo_de_lineas([aro_del_paso(k) for k in range(1, K + 1)],
                "#c3cad6", 2, f"los {K} pasos  (no cierran: hay primero y ultimo)")
trazo_de_lineas([arco_del_resto(r) for r in range(MODULO)],
                "#d5dae3", 1, f"los {MODULO} restos  (cierran: {MODULO} = 0)")


# --- el resto 0 y el ultimo, para que se vea que son vecinos ---

trazo_de_lineas([arco_del_resto(0)], "#0b63d6", 5, "resto 0")
trazo_de_lineas([arco_del_resto(MODULO - 1)], "#7048e8", 5,
                f"resto {MODULO - 1}  (el de al lado del 0: aqui cierra)")


# --- LOS CRUCES: cada uno es un paso ya decidido, y ninguno queda vacio ---

impar_dice = "(3n+1)/2" if CON_ATAJO else "n × 3 + 1"

for letra, color, nombre in (("I", "#d62728", f"impar  →  {impar_dice}"),
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
            cuantos_comparten = todos.count(patron_del_resto[resto])
            textos.append(
                f"<b>resto {resto}</b> (mod {MODULO})  ·  <b>paso {k}</b><br>"
                f"aqui toca: {impar_dice if letra == 'I' else 'n ÷ 2'}<br>"
                f"arranque completo: <b>{patron_del_resto[resto]}</b><br>"
                f"restos con este mismo arranque: {cuantos_comparten}<br><br>"
                f"todo numero que deje resto {resto} al dividirlo<br>"
                f"entre {MODULO} arranca asi. Sin excepcion."
            )
    figura.add_trace(go.Scatter3d(
        x=ex, y=ye, z=ze, mode="markers",
        marker=dict(size=6, color=color, line=dict(color="white", width=0.8)),
        name=f"{nombre}   ({len(ex)} cruces)",
        text=textos, hovertemplate="%{text}<extra></extra>",
    ))


# --- los numeros ---

def poner_numeros(sitios, etiquetas, color, nombre):
    figura.add_trace(go.Scatter3d(
        x=[v[0] for v in sitios], y=[v[1] for v in sitios],
        z=[v[2] for v in sitios],
        mode="text", text=etiquetas,
        textfont=dict(size=TAMANO_LETRA, color=color),
        name=nombre, hoverinfo="skip", showlegend=False,
    ))


# Los restos, por el ecuador, a dos distancias alternadas.
sitios, etiquetas = [], []
for resto in range(0, MODULO, CADA_CUANTOS_RESTOS):
    fuera = 1.07 + (resto % 2) * 0.09
    giro = math.radians(giro_del_resto(resto))
    sitios.append((math.cos(giro) * fuera, math.sin(giro) * fuera, 0.0))
    etiquetas.append(str(resto))
poner_numeros(sitios, etiquetas, "#7a3e00", "numeros de resto")

# Los pasos, por delante.
sitios, etiquetas = [], []
for k in range(1, K + 1):
    base = punto(k, 0)
    sitios.append((base[0] * 1.18, base[1] * 1.18, base[2] * 1.18))
    etiquetas.append(f"paso {k}")
poner_numeros(sitios, etiquetas, "#1f4e79", "numeros de paso")


figura.add_trace(go.Scatter3d(
    x=[0, 0], y=[0, 0], z=[1, -1], mode="markers",
    marker=dict(color="#111318", size=7, symbol="diamond"),
    name="polos (las dos puntas del eje de pasos)",
    text=["polo norte<br>por encima del paso 1",
          f"polo sur<br>por debajo del paso {K}"],
    hovertemplate="%{text}<extra></extra>",
))


if CON_ATAJO:
    remate = (f"BIYECCION: los {MODULO} restos dan los {MODULO} patrones"
              f" posibles, uno por uno")
else:
    remate = (f"los {MODULO} restos dan solo {len(distintos)} patrones"
              f" = F({K + 2}) de Fibonacci, porque dos impares no van seguidos")

sin_eje = dict(showbackground=False, showgrid=False, zeroline=False,
               showticklabels=False, title="", visible=False)

figura.update_layout(
    title=dict(
        text=f"La malla completa de los arranques de Collatz  —  k = {K},"
             f"  impar = {regla}"
             f"<br><sub>{MODULO} restos × {K} pasos = {MODULO * K:,} cruces,"
             f" ninguno vacio  ·  {remate}"
             f"<br>el eje de restos CIERRA ({MODULO} = 0), el de pasos no"
             f"  ·  esto no es dibujo: todo numero cae en un resto y arranca"
             f" como dice su casilla</sub>",
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

archivo = f"malla_residuos_k{K}_{'atajo' if CON_ATAJO else 'clasica'}.html"
figura.write_html(
    archivo,
    auto_open=True,
    default_width="100%",
    default_height="100vh",
    config=dict(responsive=True, scrollZoom=True, displaylogo=False),
)
print("\nGrafico guardado y abierto en el navegador:", archivo)
