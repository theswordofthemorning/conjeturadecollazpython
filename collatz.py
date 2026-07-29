"""Motor de la conjetura de Collatz.

La regla: n -> n/2 si n es par, n -> 3n+1 si n es impar.
La conjetura dice que toda semilla n >= 1 termina cayendo en 1.
"""

from __future__ import annotations


def secuencia(n: int) -> list[int]:
    """Trayectoria completa de n hasta 1, incluyendo ambos extremos."""
    if n < 1:
        raise ValueError("la semilla debe ser >= 1")
    camino = [n]
    while n != 1:
        n = n >> 1 if n % 2 == 0 else 3 * n + 1
        camino.append(n)
    return camino


def altitud_maxima(n: int) -> int:
    """Valor mas alto que alcanza la trayectoria de n."""
    techo = n
    while n != 1:
        n = n >> 1 if n % 2 == 0 else 3 * n + 1
        if n > techo:
            techo = n
    return techo


def tabla_de_pasos(limite: int) -> list[int]:
    """Numero de pasos hasta 1 para cada n en [0, limite], con memoizacion.

    tabla[0] no tiene sentido y queda en 0; tabla[1] == 0.
    """
    tabla = [0] * (limite + 1)
    for n in range(2, limite + 1):
        x, extra = n, 0
        # Bajamos hasta caer en una semilla ya resuelta.
        while x >= n:
            x = x >> 1 if x % 2 == 0 else 3 * x + 1
            extra += 1
        tabla[n] = extra + tabla[x]
    return tabla


def verificar(limite: int, tope_pasos: int = 10_000_000) -> dict:
    """Comprueba que todo n en [1, limite] alcanza 1.

    Usa el atajo clasico: si la trayectoria cae por debajo de n, ese tramo ya
    fue verificado antes, asi que se puede cortar ahi. Eso convierte una
    busqueda cuadratica en algo casi lineal.

    Devuelve un informe; `contraejemplo` es None si la conjetura aguanta.
    """
    contraejemplo = None
    pasos_totales = 0
    peor_altitud = (1, 1)  # (semilla, techo)

    for n in range(2, limite + 1):
        x, pasos = n, 0
        techo = n
        while x >= n:
            x = x >> 1 if x % 2 == 0 else 3 * x + 1
            pasos += 1
            if x > techo:
                techo = x
            if pasos > tope_pasos:
                contraejemplo = n
                break
        pasos_totales += pasos
        if techo > peor_altitud[1]:
            peor_altitud = (n, techo)
        if contraejemplo is not None:
            break

    return {
        "limite": limite,
        "contraejemplo": contraejemplo,
        "pasos_de_descenso": pasos_totales,
        "mayor_altitud": peor_altitud,
    }


def records(limite: int) -> dict:
    """Semillas que baten un record de longitud o de altitud en [1, limite]."""
    tabla = tabla_de_pasos(limite)

    mejor_pasos = max(range(1, limite + 1), key=lambda n: tabla[n])
    escaladores = []
    techo_global = 0
    for n in range(1, limite + 1):
        techo = altitud_maxima(n)
        if techo > techo_global:
            techo_global = techo
            escaladores.append((n, techo))

    largos = []
    record = -1
    for n in range(1, limite + 1):
        if tabla[n] > record:
            record = tabla[n]
            largos.append((n, tabla[n]))

    return {
        "tabla": tabla,
        "mas_pasos": (mejor_pasos, tabla[mejor_pasos]),
        "records_de_longitud": largos,
        "records_de_altitud": escaladores,
    }
