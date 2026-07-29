# collazejecucion.py
#
# Pide un numero, le aplica la regla de Collatz hasta llegar al 1,
# y dibuja el recorrido como una linea de tiempo de izquierda a derecha.
#
#   circulo ROJO  = ese paso fue  n * 3 + 1   (el numero era impar)
#   circulo AZUL  = ese paso fue  n / 2       (el numero era par)
#   circulo GRIS  = el numero con el que empezaste

import sys
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
# LA FORMA MAS SIMPLE DE USARLO:
# escribe tu numero aqui abajo, guarda, y dale a Ctrl+B en Sublime.
#
#     NUMERO_FIJO = 221
#
# Si lo dejas en None, el programa te preguntara el numero.
# ---------------------------------------------------------------------------

NUMERO_FIJO = 2213046546463218645

TAMANO_LETRA = 13      # subelo si necesitas los numeros mas grandes
CUANTOS_SE_VEN = 30    # cuantos circulos entran de golpe en la ventana


def pedir_numero():
    """Consigue el numero de la manera que se pueda."""

    # 1) Lo pusiste a mano arriba. Listo.
    if NUMERO_FIJO is not None:
        return NUMERO_FIJO

    # 2) Hay una consola de verdad donde puedes escribir.
    if sys.stdin is not None and sys.stdin.isatty():
        escrito = input("Escribe un numero entero positivo: ")
        return int(escrito.strip().lstrip("﻿"))

    # 3) No hay consola (esto pasa en Sublime Text): abrimos una ventanita.
    import tkinter
    from tkinter import simpledialog

    ventana = tkinter.Tk()
    ventana.withdraw()
    valor = simpledialog.askinteger("Collatz", "Escribe un numero entero positivo:")
    ventana.destroy()
    return valor


# ---------------------------------------------------------------- el numero

numero = pedir_numero()

if numero is None:
    print("No escribiste ningun numero. Adios.")
    raise SystemExit

if numero < 1:
    print("Tiene que ser 1 o mas grande.")
    raise SystemExit


# ---------------------------------------------------------------- la cuenta

valores = [numero]     # todos los numeros por los que vamos pasando
colores = ["gray"]     # de que color es el circulo de cada numero

n = numero
while n != 1:
    if n % 2 == 0:          # es par  -> lo divido entre 2
        n = n // 2
        colores.append("blue")
    else:                   # es impar -> lo multiplico por 3 y le sumo 1
        n = n * 3 + 1
        colores.append("red")
    valores.append(n)

pasos = len(valores) - 1

print("Empezaste en", numero)
print("Tardo", pasos, "pasos en llegar al 1")
print("El numero mas alto al que subio fue", max(valores))
print("El recorrido completo fue:")
print(valores)


# ---------------------------------------------------------------- el dibujo

posiciones = list(range(len(valores)))   # 0, 1, 2, 3... de izquierda a derecha
altura = [0] * len(valores)              # todos los circulos a la misma altura

# Los numeros van escritos en vertical, asi que cuantas mas cifras tengan,
# mas alta tiene que ser la hoja para que quepan sin cortarse.
mas_cifras = max(len(str(v)) for v in valores)
alto_figura = 3.2 + mas_cifras * 0.30
tope_arriba = 1.2 + mas_cifras * 0.55


def dibujar_en(ax):
    """Pinta la linea de tiempo dentro del recuadro que le pasemos."""

    ax.plot(posiciones, altura, color="lightgray", linewidth=1.5, zorder=1)
    ax.scatter(posiciones, altura, c=colores, s=200, zorder=2)

    # El numero va encima de su circulo, escrito de abajo hacia arriba.
    # Asi da igual que tenga muchos digitos: nunca se pisa con el de al lado.
    for i in range(len(valores)):
        ax.text(
            i, 0.6, str(valores[i]),
            fontsize=TAMANO_LETRA,
            rotation=90,
            ha="center",
            va="bottom",
        )

    ax.set_ylim(-2, tope_arriba)
    ax.axis("off")


titulo = "Collatz de " + str(numero) + "   (" + str(pasos) + " pasos)"


# 1) La imagen larga completa, guardada en un archivo.
#    Esta la puedes abrir aparte y recorrerla con el visor de imagenes.

ancho_total = max(8, len(valores) * 0.5)
if ancho_total > 400:          # freno de seguridad para recorridos enormes
    ancho_total = 400

fig_larga, ax_largo = plt.subplots(figsize=(ancho_total, alto_figura))
dibujar_en(ax_largo)
ax_largo.set_xlim(-1, len(valores))
ax_largo.set_title(titulo, fontsize=TAMANO_LETRA + 2)

nombre = "collatz_" + str(numero) + ".png"
fig_larga.savefig(nombre, dpi=100, bbox_inches="tight")
plt.close(fig_larga)
print("Grafico guardado en el archivo:", nombre)


# 2) La ventana con la barra de abajo para desplazarte por el recorrido.

fig, ax = plt.subplots(figsize=(14, alto_figura + 0.8))
fig.subplots_adjust(left=0.02, right=0.98, top=0.88, bottom=0.16)
dibujar_en(ax)
ax.set_title(titulo, fontsize=TAMANO_LETRA + 2)

if len(valores) > CUANTOS_SE_VEN:
    ax.set_xlim(-0.6, CUANTOS_SE_VEN)

    hueco_barra = fig.add_axes([0.08, 0.04, 0.84, 0.04])
    barra = Slider(
        hueco_barra,
        "mover",
        0,
        len(valores) - CUANTOS_SE_VEN,
        valinit=0,
        valstep=1,
    )

    def mover(donde):
        ax.set_xlim(donde - 0.6, donde + CUANTOS_SE_VEN)
        fig.canvas.draw_idle()

    barra.on_changed(mover)
else:
    ax.set_xlim(-0.6, len(valores) - 0.4)

plt.show()
