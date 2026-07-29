"""Dos lecturas tridimensionales de la conjetura de Collatz.

1. El paisaje  : cada semilla es una cresta; eje z = log2(valor).
2. El coral    : cada trayectoria se dibuja al reves (desde 1 hacia n) y gira
                 un angulo distinto segun el paso sea par o impar; los caminos
                 comparten tronco y el arbol crece solo.

Color: `viridis`, secuencial y perceptualmente uniforme (segura para daltonismo).
La magnitud va al color, la identidad nunca depende solo del color.
"""

from __future__ import annotations

import math

import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from mpl_toolkits.mplot3d.art3d import Line3DCollection

from collatz import secuencia

FONDO = "#12141a"
TINTA = "#e8eaed"
TINTA_SUAVE = "#9aa0a6"
MAPA = matplotlib.colormaps["viridis"]


def _estilo(ax, titulo: str, subtitulo: str) -> None:
    ax.set_facecolor(FONDO)
    for eje in (ax.xaxis, ax.yaxis, ax.zaxis):
        eje.pane.set_facecolor(FONDO)
        eje.pane.set_edgecolor("#2a2e37")
        eje.line.set_color("#2a2e37")
        eje.label.set_color(TINTA_SUAVE)
        eje._axinfo["grid"]["color"] = "#22262e"
        eje._axinfo["grid"]["linewidth"] = 0.6
    ax.tick_params(colors=TINTA_SUAVE, labelsize=8)
    ax.set_title(titulo, color=TINTA, fontsize=15, pad=18, loc="left")
    ax.text2D(
        0.0, 1.0, subtitulo,
        transform=ax.transAxes, color=TINTA_SUAVE, fontsize=9.5, va="bottom",
    )


def paisaje(hasta: int = 1000, salida: str = "paisaje3d.png", mostrar: bool = False):
    """Cresta por semilla: x = semilla, y = paso, z = log2(valor)."""
    trayectorias = [secuencia(n) for n in range(1, hasta + 1)]
    longitudes = np.array([len(t) - 1 for t in trayectorias], dtype=float)
    norma = Normalize(vmin=longitudes.min(), vmax=longitudes.max())

    segmentos, colores = [], []
    for n, camino in enumerate(trayectorias, start=1):
        z = np.log2(np.asarray(camino, dtype=float))
        puntos = np.column_stack([np.full(len(z), n, dtype=float), np.arange(len(z)), z])
        segmentos.append(np.stack([puntos[:-1], puntos[1:]], axis=1))
        colores.append(np.full(len(z) - 1, longitudes[n - 1]))

    fig = plt.figure(figsize=(13, 8.5), facecolor=FONDO)
    ax = fig.add_subplot(111, projection="3d")

    coleccion = Line3DCollection(
        np.concatenate(segmentos),
        colors=MAPA(norma(np.concatenate(colores))),
        linewidths=0.55,
        alpha=0.75,
    )
    ax.add_collection3d(coleccion)

    ax.set_xlim(1, hasta)
    ax.set_ylim(0, max(len(t) for t in trayectorias))
    ax.set_zlim(0, max(math.log2(max(t)) for t in trayectorias) * 1.02)
    ax.set_xlabel("semilla n", labelpad=10)
    ax.set_ylabel("paso", labelpad=10)
    ax.set_zlabel("log₂ del valor", labelpad=6)
    ax.view_init(elev=26, azim=-58)
    ax.set_box_aspect((1.7, 1.0, 0.62))

    # Etiquetas directas: solo las tres cimas, no un numero por punto.
    cimas = sorted(range(1, hasta + 1), key=lambda n: max(trayectorias[n - 1]))[-3:]
    for n in cimas:
        camino = trayectorias[n - 1]
        i = int(np.argmax(camino))
        ax.text(
            n, i, math.log2(camino[i]) + 0.5, f"n={n}",
            color=TINTA, fontsize=8.5, ha="center",
        )

    barra = fig.colorbar(
        plt.cm.ScalarMappable(norm=norma, cmap=MAPA),
        ax=ax, shrink=0.5, aspect=26, pad=0.02,
    )
    barra.set_label("pasos hasta 1", color=TINTA_SUAVE, fontsize=9)
    barra.ax.tick_params(colors=TINTA_SUAVE, labelsize=8)
    barra.outline.set_edgecolor("#2a2e37")

    _estilo(
        ax,
        "El paisaje de Collatz",
        f"Trayectorias de n = 1 … {hasta}. Todas suben distinto; todas terminan en 1.",
    )
    fig.tight_layout()
    fig.savefig(salida, dpi=150, facecolor=FONDO)
    if mostrar:
        plt.show()
    else:
        plt.close(fig)
    return salida


def coral(
    hasta: int = 3000,
    giro_par: float = 7.0,
    giro_impar: float = -17.0,
    alabeo: float = 9.0,
    salida: str = "coral3d.png",
    mostrar: bool = False,
):
    """Arbol 3D: recorre cada trayectoria al reves y gira segun la paridad.

    Los caminos que comparten prefijo comparten geometria, asi que el tronco se
    dibuja una sola vez y las ramas emergen solas.
    """
    gp, gi, al = map(math.radians, (giro_par, giro_impar, alabeo))

    # prefijo de movimientos -> (posicion, rumbo, cabeceo, profundidad)
    memo: dict[tuple, tuple] = {(): (np.zeros(3), math.pi / 2, 0.0, 0)}
    segmentos, profundidades = [], []

    for n in range(2, hasta + 1):
        rev = secuencia(n)[::-1]  # de 1 hacia n
        clave: tuple = ()
        for i in range(len(rev) - 1):
            # rev[i+1] == 2*rev[i]  <=>  el paso original fue una division por 2
            par = rev[i + 1] == 2 * rev[i]
            nueva = clave + (par,)
            if nueva not in memo:
                pos, rumbo, cabeceo, prof = memo[clave]
                rumbo += gp if par else gi
                cabeceo += al if par else -al * 0.5
                paso = np.array([
                    math.cos(cabeceo) * math.cos(rumbo),
                    math.cos(cabeceo) * math.sin(rumbo),
                    math.sin(cabeceo),
                ])
                destino = pos + paso
                memo[nueva] = (destino, rumbo, cabeceo, prof + 1)
                segmentos.append((pos, destino))
                profundidades.append(prof + 1)
            clave = nueva

    segmentos = np.asarray(segmentos, dtype=float)
    profundidades = np.asarray(profundidades, dtype=float)
    norma = Normalize(vmin=profundidades.min(), vmax=profundidades.max())

    fig = plt.figure(figsize=(11.5, 9.5), facecolor=FONDO)
    ax = fig.add_subplot(111, projection="3d")
    ax.add_collection3d(
        Line3DCollection(
            segmentos,
            colors=MAPA(norma(profundidades)),
            linewidths=0.6,
            alpha=0.8,
        )
    )

    puntos = segmentos.reshape(-1, 3)
    for fijar, col in ((ax.set_xlim, 0), (ax.set_ylim, 1), (ax.set_zlim, 2)):
        lo, hi = puntos[:, col].min(), puntos[:, col].max()
        margen = (hi - lo) * 0.05 + 1e-9
        fijar(lo - margen, hi + margen)
    ax.set_xlabel("x", labelpad=8)
    ax.set_ylabel("y", labelpad=8)
    ax.set_zlabel("z", labelpad=6)
    ax.view_init(elev=22, azim=-72)
    ax.set_box_aspect((1.3, 1.3, 0.85))

    barra = fig.colorbar(
        plt.cm.ScalarMappable(norm=norma, cmap=MAPA),
        ax=ax, shrink=0.5, aspect=26, pad=0.02,
    )
    barra.set_label("distancia al 1 (pasos)", color=TINTA_SUAVE, fontsize=9)
    barra.ax.tick_params(colors=TINTA_SUAVE, labelsize=8)
    barra.outline.set_edgecolor("#2a2e37")

    _estilo(
        ax,
        "El coral de Collatz",
        f"{hasta - 1} trayectorias trazadas desde el 1 hacia afuera "
        f"(par: {giro_par:+.0f}°, impar: {giro_impar:+.0f}°).",
    )
    fig.tight_layout()
    fig.savefig(salida, dpi=150, facecolor=FONDO)
    if mostrar:
        plt.show()
    else:
        plt.close(fig)
    return salida
