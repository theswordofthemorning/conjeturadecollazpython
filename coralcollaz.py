# coralcollaz.py
#
# EL CORAL DE HARRISS, Y LA PERILLA QUE HACE QUE LOS PUNTOS CALCEN.
#
# De donde sale esto (buscado en la web, no inventado):
#
#   Es el "Collatz Seaweed" de Edmund Harriss, matematico de la Universidad de
#   Arkansas. Salio en Numberphile con Alex Bellos y esta en el libro "Visions of
#   Numberland" / "Visions of the Universe". La regla, textual:
#
#     "si el paso actual es el doble del siguiente, gira una cantidad fija en
#      sentido horario; si no, gira LA MITAD de esa cantidad en antihorario"
#
#   O sea: paso par -> +θ,  paso impar -> −θ/2. Proporcion 2 a 1, signos
#   opuestos. Se dibuja AL REVES: desde el 1 hacia afuera, asi las trayectorias
#   que comparten final comparten tronco y las ramas brotan solas.
#
#   (viz3d.py:coral() de este repo ya hacia esto, con giro_par=7 y giro_impar=-17.
#    Los signos estaban bien pero la proporcion al reves: el impar era MAS grande
#    que el par, y Harriss lo tiene a la mitad.)
#
# LO QUE ESTE PROGRAMA AÑADE: medir si los puntos calzan.
#
# Dos cosas que se comprueban, no se suponen:
#
#   1. EL RUMBO DE UNA RAMA SOLO DEPENDE DE (A, B) — de cuantos impares y
#      cuantos pares hubo, no del orden. Porque los giros se suman y da igual
#      en que orden los sumes:  rumbo = A·θ_impar + B·θ_par.
#      Y (A, B) son EXACTAMENTE las coordenadas de collazmalla.py. O sea que los
#      rumbos del coral son la malla (A,B) que ya tenias, pasada a angulos.
#
#   2. SI LOS PUNTOS CALZAN O NO, y de que depende.
#      Depende de cuantos rumbos distintos permiten los angulos:
#
#         par 16, impar  -8  (Harriss)  ->  45 rumbos  ->  ver el aviso de abajo
#         par  7, impar -17  (tu repo)  -> 357 rumbos  ->      0 choques
#         par 60, impar -30             ->  13 rumbos  ->  46% choques
#         par 90, impar -45             ->   9 rumbos  ->  77% choques
#         par 120, impar -60            ->   6 rumbos  ->  97% choques
#
#      Con 120/-60 solo hay 6 direcciones posibles, el coral cae sobre una
#      reticula hexagonal, y 6.520 ramas distintas terminan en 221 puntos.
#      AHI los puntos calzan.
#
# ---------------------------------------------------------------------------
# CORRECCION IMPORTANTE (30-07-2026): EL "0 CHOQUES" DE HARRISS ERA FALSO
# ---------------------------------------------------------------------------
#
# Este archivo afirmaba que con 16/-8 el coral no se vuelve a juntar NUNCA. No
# es cierto: era el resultado de mirar solo 3.000 semillas. Con 45 rumbos SI
# hay choques, y son coincidencias exactas, no ruido de coma flotante.
#
#   primer HASTA con choque (barriendo semillas)   :  10.452
#   segundo choque                                 :  25.527
#   primera profundidad con choque (arbol entero)  :      31
#   a profundidad 59                               :  39.831 choques
#
# Los dos umbrales son distintos y los dos son ciertos: barrer por semillas solo
# ve las ramas que cuelgan de semillas chicas. Barriendo el arbol inverso
# completo el primer choque esta en la profundidad 31, con cero hasta la 30
# inclusive, exhaustivo.
#
# Que son exactos se comprobo en aritmetica entera: cada arista es una raiz
# 45-esima de la unidad, asi que dos ramas caen en el mismo punto si y solo si
# el polinomio ciclotomico Phi_45 divide al polinomio diferencia en Z[x]. Los
# dos primeros pares dan resto CERO, sin un solo float. Lo que se media como
# 1,4e-14 era el error de sumar 35 cosenos.
#
# LA CAUSA REFUERZA LA DOCTRINA EN VEZ DE ROMPERLA: 45 = 3^2 * 5. Las relaciones
# enteras entre las 45 raices son el triangulo (tres direcciones a 120 grados) y
# el pentagono (cinco a 72). El cierre lo trae la CONMENSURABILIDAD del angulo
# --16 y 8 dividen a 120--, no Collatz. Es el mismo fenomeno que el hexagono,
# solo que hace falta llegar a profundidad 31 para verlo.
#
# POR ESO HASTA VALE 11.000 Y NO 3.000. Con 3.000 este programa imprime "NO
# CALZAN" y esa es exactamente la lectura que resulto falsa. Con 11.000 pasa el
# umbral de 10.452 y el choque aparece. Si lo bajas otra vez, sabe lo que estas
# viendo: ausencia de evidencia, no evidencia de ausencia.
#
# HONESTIDAD SOBRE EL CIERRE: es matematica de verdad (si el grupo de
# direcciones es finito, por el principio del palomar las posiciones se
# repiten), pero lo trae EL ANGULO QUE ELEGIS TU, no Collatz. Collatz pone el
# paseo; el angulo pone el cierre.
#
# Genera un .html que ocupa toda la ventana.

import math
import collections
import plotly.graph_objects as go


# ---------------------------------------------------------------------------
# Cambia esto aqui, guarda, y dale a Ctrl+B en Sublime.
#
#   HARRISS   -> ( 16.0,  -8.0)    el coral de verdad. Gira, y queda ACOTADO.
#   REPO      -> (  7.0, -17.0)    lo que tenia viz3d.py
#   NULO      -> (  8.0, -13.876)  giro medio CERO: deja de girar y se EXPANDE
#   HEXAGONO  -> (120.0, -60.0)    6 rumbos: cierra casi todo
#   CUADRADO  -> ( 90.0, -45.0)    9 rumbos
#   SUAVE     -> ( 60.0, -30.0)    13 rumbos
#
# El NULO no es un angulo elegido a dedo: es el unico que cumple
#     impar / par  =  -(divisiones por multiplicacion del coral)
# y esa razon la pone Collatz, no nosotros. El programa la mide y te la dice.
# ---------------------------------------------------------------------------

ANGULO_PAR = 16.0
ANGULO_IMPAR = -8.0

HASTA = 11000       # cuantas semillas se dibujan. Con 16/-8 el primer choque
                    # aparece en 10.452, asi que por debajo de eso el programa
                    # dice "NO CALZAN" y miente. Ver la correccion de arriba.
K_RESTOS = 6        # para la comprobacion contra la malla de restos
TOLERANCIA = 6      # decimales al comparar posiciones


# ------------------------------------------------------------- las cuentas

def secuencia_de(n):
    camino = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        camino.append(n)
    return camino


def construir_coral(hasta, grados_par, grados_impar):
    """El coral de Harriss. Devuelve, por cada camino de paridades:

        prefijo -> (posicion, rumbo, A impares, B pares)

    Se recorre cada trayectoria AL REVES, del 1 hacia la semilla. Los caminos
    que comparten principio comparten geometria, asi que el tronco se dibuja
    una sola vez y las ramas salen solas. Eso es lo que le da la forma.
    """
    gp = math.radians(grados_par)
    gi = math.radians(grados_impar)

    memo = {(): ((0.0, 0.0), math.pi / 2, 0, 0)}
    tramos = []          # (desde, hasta, profundidad)

    for n in range(2, hasta + 1):
        alreves = secuencia_de(n)[::-1]
        clave = ()
        for i in range(len(alreves) - 1):
            # alreves[i+1] == 2 * alreves[i]  <=>  el paso original fue n/2
            fue_par = alreves[i + 1] == 2 * alreves[i]
            nueva = clave + (fue_par,)
            if nueva not in memo:
                (x, y), rumbo, A, B = memo[clave]
                rumbo += gp if fue_par else gi
                A, B = (A, B + 1) if fue_par else (A + 1, B)
                destino = (x + math.cos(rumbo), y + math.sin(rumbo))
                memo[nueva] = (destino, rumbo, A, B)
                tramos.append(((x, y), destino, len(nueva)))
            clave = nueva

    return memo, tramos


print(f"EL CORAL DE HARRISS  —  par {ANGULO_PAR:+.1f}°, impar {ANGULO_IMPAR:+.1f}°")
print(f"  semillas dibujadas: 2 … {HASTA:,}")

coral, tramos = construir_coral(HASTA, ANGULO_PAR, ANGULO_IMPAR)
print(f"  ramas (caminos de paridad distintos): {len(coral):,}")


# --- COMPROBACION 1: el rumbo solo depende de (A, B) ---

rumbos_por_ab = collections.defaultdict(set)
for prefijo, (pos, rumbo, A, B) in coral.items():
    rumbos_por_ab[(A, B)].add(round(rumbo, 9))

malos = [ab for ab, rs in rumbos_por_ab.items() if len(rs) > 1]

print(f"\nCOMPROBACION 1 — el rumbo depende solo de (A, B)")
print(f"  pares (A, B) distintos     : {len(rumbos_por_ab):,}")
print(f"  con mas de un rumbo posible: {len(malos)}")
if malos:
    raise SystemExit("El rumbo depende del orden. Algo esta mal, no sigas.")
print(f"  -> confirmado: rumbo = A × {ANGULO_IMPAR:+.1f}° + B × {ANGULO_PAR:+.1f}°")
print(f"     y (A, B) son las coordenadas de collazmalla.py. Los rumbos del")
print(f"     coral SON esa malla pasada a angulos.")


# --- COMPROBACION 2: el final de cada rama lo decide el resto mod 2^k ---
#
# El coral se dibuja al reves, asi que los primeros pasos de la semilla (los que
# manda el resto) son los ULTIMOS tramos de la rama, los de la punta.

modulo = 2 ** K_RESTOS
por_resto = collections.defaultdict(set)
for n in range(modulo, modulo * 10):
    paridades = []
    x = n
    for _ in range(K_RESTOS):
        paridades.append(x % 2 == 0)
        x = x // 2 if x % 2 == 0 else 3 * x + 1
    por_resto[n % modulo].add(tuple(paridades))

descuadres = [r for r, cuales in por_resto.items() if len(cuales) > 1]
print(f"\nCOMPROBACION 2 — la punta de cada rama la decide el resto (mod {modulo})")
print(f"  restos probados        : {len(por_resto)}")
print(f"  restos con dos versiones: {len(descuadres)}")
if descuadres:
    raise SystemExit("El resto no decide la punta. No sigas.")
print(f"  -> los {K_RESTOS} ultimos giros de una rama los fija n mod {modulo}.")
print(f"     La malla de restos de mallaresiduos.py es la punta de este coral.")


# --- LA MEDIDA: calzan los puntos? ---

rumbos_distintos = {round(rumbo % (2 * math.pi), 6)
                    for _, rumbo, _, _ in coral.values()}

sitios = collections.defaultdict(list)
for prefijo, (pos, rumbo, A, B) in coral.items():
    sitios[(round(pos[0], TOLERANCIA), round(pos[1], TOLERANCIA))].append(prefijo)

choques = {p: ks for p, ks in sitios.items() if len(ks) > 1}
ramas_encimadas = sum(len(ks) - 1 for ks in choques.values())

print(f"\nCALZAN LOS PUNTOS?")
print(f"  rumbos distintos que permiten estos angulos: {len(rumbos_distintos)}")
print(f"  ramas                : {len(coral):,}")
print(f"  posiciones distintas : {len(sitios):,}")
print(f"  puntos con mas de una rama encima: {len(choques):,}")
print(f"  ramas encimadas      : {ramas_encimadas:,}"
      f"  ({100 * ramas_encimadas / len(coral):.1f}% del total)")

if ramas_encimadas == 0:
    print(f"\n  -> NO SE VE NINGUN CHOQUE **A ESTA ESCALA**. Ojo con leer esto")
    print(f"     como 'no cierra nunca': eso es justo lo que resulto falso el")
    print(f"     30-07-2026. Con 16/-8 el primer choque esta en HASTA = 10.452,")
    print(f"     y barriendo el arbol inverso entero aparece en la profundidad 31.")
    print(f"     Con HASTA = {HASTA:,} esto es ausencia de evidencia, no evidencia")
    print(f"     de ausencia. Sube HASTA antes de concluir nada.")
else:
    apilado = max(len(ks) for ks in choques.values())
    print(f"\n  -> CALZAN. {len(coral):,} ramas caen en solo {len(sitios):,} puntos.")
    print(f"     El punto mas cargado tiene {apilado} ramas encima.")
    print(f"     Pasa porque solo hay {len(rumbos_distintos)} rumbos posibles: el")
    print(f"     paseo queda atrapado en una reticula y por el principio del")
    print(f"     palomar los puntos se repiten. Es cierre de verdad, pero lo")
    print(f"     trae el ANGULO que elegiste, no Collatz.")


# --- DE DONDE SALE LA ESPIRAL, Y COMO SE APAGA ---
#
# La forma no la decide solo el angulo. La decide el angulo MULTIPLICADO por el
# desbalance entre pasos pares e impares, que ese si lo pone Collatz.

nodos_par = sum(1 for prefijo in coral if prefijo and prefijo[-1] is True)
nodos_total = len(coral) - 1
fraccion_par = nodos_par / nodos_total
fraccion_impar = 1 - fraccion_par
razon = fraccion_par / fraccion_impar

giro_medio = fraccion_par * ANGULO_PAR + fraccion_impar * ANGULO_IMPAR

print(f"\nDE DONDE SALE LA FORMA")
print(f"  pasos pares en el coral  : {100 * fraccion_par:.2f}%")
print(f"  pasos impares            : {100 * fraccion_impar:.2f}%")
print(f"  divisiones por multiplicacion: {razon:.4f}")
print(f"  equilibrio log2(3)           : {math.log2(3):.4f}")
print(f"    -> por encima del equilibrio: por eso las trayectorias caen al 1")
print(f"  GIRO MEDIO POR PASO: {giro_medio:+.4f}°")

if abs(giro_medio) < 0.01:
    print(f"    -> practicamente CERO: el coral no gira. Se va derecho y se")
    print(f"       EXPANDE, el radio crece a lo largo con la profundidad.")
else:
    print(f"    -> una vuelta completa cada {abs(360 / giro_medio):.0f} pasos")
    print(f"       las ramas profundas se ENROLLAN y el radio queda acotado.")
    print(f"  para apagar la espiral harian falta:  par {ANGULO_PAR:+.1f}°,"
          f" impar {-ANGULO_PAR * razon:+.3f}°")
    print(f"    (la condicion es impar/par = -{razon:.4f}, y esa razon la pone")
    print(f"     Collatz, no nosotros)")

profundidades = collections.defaultdict(list)
for prefijo, (pos, rumbo, A, B) in coral.items():
    profundidades[len(prefijo)].append(math.hypot(pos[0], pos[1]))

print(f"\n  RADIO MEDIO SEGUN LA PROFUNDIDAD DE LA RAMA")
print(f"    (crece a lo largo = se expande;  se queda quieto = acotado)")
for d in (25, 50, 100, 200):
    if d in profundidades:
        radio = sum(profundidades[d]) / len(profundidades[d])
        print(f"    {d:>3} pasos: radio {radio:>7.2f}   radio/pasos {radio / d:.3f}")


# ------------------------------------------------------------- el dibujo

figura = go.Figure()

# Las ramas, todas en un trazo, con corte entre cada tramo.
ex, ye = [], []
for desde, hasta_p, profundidad in tramos:
    ex += [desde[0], hasta_p[0], None]
    ye += [desde[1], hasta_p[1], None]

figura.add_trace(go.Scatter(
    x=ex, y=ye, mode="lines",
    line=dict(color="#8b95a4", width=1),
    name=f"las {len(tramos):,} ramas", hoverinfo="skip",
))

# Las puntas de rama, coloreadas por cuan lejos del 1 estan.
px, py, prof, textos = [], [], [], []
for prefijo, (pos, rumbo, A, B) in coral.items():
    px.append(pos[0])
    py.append(pos[1])
    prof.append(len(prefijo))
    textos.append(
        f"a <b>{len(prefijo)}</b> pasos del 1<br>"
        f"{A} impares  y  {B} pares<br>"
        f"rumbo {math.degrees(rumbo) % 360:.1f}°"
    )

figura.add_trace(go.Scatter(
    x=px, y=py, mode="markers",
    marker=dict(size=2.6, color=prof,
                colorscale=[[0, "#f7d8a0"], [0.5, "#5b8dd9"], [1, "#0b2447"]],
                colorbar=dict(title=dict(text="pasos<br>hasta el 1", side="right"),
                              thickness=14, len=0.42),
                opacity=0.85),
    name=f"los {len(coral):,} caminos",
    text=textos, hovertemplate="%{text}<extra></extra>",
))

# Los puntos donde CALZAN varias ramas.
if choques:
    cx = [p[0] for p in choques]
    cy = [p[1] for p in choques]
    ct = [f"<b>{len(ks)} ramas caen en este punto</b><br>"
          f"pasos hasta el 1: {sorted({len(k) for k in ks})}"
          for ks in choques.values()]
    figura.add_trace(go.Scatter(
        x=cx, y=cy, mode="markers",
        marker=dict(size=9, color="rgba(0,0,0,0)",
                    line=dict(color="#d62728", width=1.6)),
        name=f"puntos donde CALZAN: {len(choques):,}",
        text=ct, hovertemplate="%{text}<extra></extra>",
    ))

# El 1, donde arranca todo.
figura.add_trace(go.Scatter(
    x=[0], y=[0], mode="markers",
    marker=dict(symbol="diamond", size=14, color="#d62728",
                line=dict(color="white", width=2)),
    name="el 1 (de aqui sale todo)",
    text=["<b>el 1</b><br>el coral crece desde aqui hacia afuera"],
    hovertemplate="%{text}<extra></extra>",
))

if ramas_encimadas:
    remate = (f"CALZAN: {len(coral):,} ramas caen en {len(sitios):,} puntos"
              f" ({100 * ramas_encimadas / len(coral):.0f}% encimadas),"
              f" porque solo hay {len(rumbos_distintos)} rumbos posibles")
else:
    remate = (f"sin choques a esta escala: {len(coral):,} ramas, {len(sitios):,}"
              f" puntos distintos, con {len(rumbos_distintos)} rumbos posibles"
              f" — pero con 45 rumbos los hay a partir de la profundidad 31")

figura.update_layout(
    title=dict(
        text=f"El coral de Harriss  —  par {ANGULO_PAR:+.0f}°,"
             f" impar {ANGULO_IMPAR:+.0f}°  ·  semillas 2 … {HASTA:,}"
             f"<br><sub>{remate}"
             f"<br>rumbo = A × {ANGULO_IMPAR:+.0f}° + B × {ANGULO_PAR:+.0f}°:"
             f" solo depende de (A, B), las coordenadas de collazmalla.py</sub>",
        x=0.5,
    ),
    xaxis=dict(showgrid=False, zeroline=False, visible=False),
    yaxis=dict(showgrid=False, zeroline=False, visible=False,
               scaleanchor="x", scaleratio=1),
    plot_bgcolor="white", paper_bgcolor="white",
    autosize=True,
    margin=dict(l=10, r=10, t=95, b=10),
    legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.9)",
                bordercolor="#dfe3ea", borderwidth=1),
)

archivo = f"coral_{ANGULO_PAR:g}_{ANGULO_IMPAR:g}.html"
figura.write_html(
    archivo,
    auto_open=True,
    default_width="100%",
    default_height="100vh",
    config=dict(responsive=True, scrollZoom=True, displaylogo=False),
)
print("\nGrafico guardado y abierto en el navegador:", archivo)
