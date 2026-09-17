"""Control acotado de la definicion, la suma de estratos y los ejemplos citados."""

import importlib.util
from collections import Counter
from fractions import Fraction
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
LAB = CARPETA.parents[1]
ZOO = LAB.parent / 'zootheorem'


def cargar(nombre, ruta):
    especificacion = importlib.util.spec_from_file_location(nombre, ruta)
    modulo = importlib.util.module_from_spec(especificacion)
    especificacion.loader.exec_module(modulo)
    return modulo


def main():
    directo = cargar('directo', ZOO / 'verify/verify_strata.py')
    simbolico = cargar('simbolico', LAB / 'estratoscadena.py')
    tabla, _ = simbolico.barrido_estratos((0, 1), 13)
    datos = {j: directo.read_data(numero) for j, numero in directo.SEQUENCES.items()}
    acumulado = 0
    masa = Fraction(0)
    for n in range(1, 14):
        estratos = Counter()
        buenas = 0
        for residuo in range(1 << n):
            trayectoria = directo.trajectory_pair(residuo, n)
            if trayectoria is None:
                continue
            tiempo, izquierda, derecha, mixtos, _, _ = trayectoria
            if izquierda != derecha:
                continue
            buenas += 1
            if tiempo == n:
                assert len(mixtos) % 2 == 0
                estratos[len(mixtos)] += 1
        assert dict(estratos) == tabla.get(n, {}), (n, estratos, tabla.get(n))
        assert sum(estratos.values()) == buenas - 2 * acumulado
        masa += Fraction(sum(estratos.values()), 1 << n)
        assert masa == Fraction(buenas, 1 << n)
        for j in datos:
            assert estratos[j] == datos[j].get(n, 0)
        acumulado = buenas
        print(n, buenas, dict(sorted(estratos.items())), masa)
    for residuo, n, j in [(65, 9, 8), (769, 11, 10), (1025, 13, 12), (3067, 18, 8)]:
        tiempo, izquierda, derecha, mixtos, ruta_a, ruta_b = directo.trajectory_pair(residuo, n)
        assert tiempo == n and izquierda == derecha and len(mixtos) == j
        print('Testigo:', residuo, 'n:', n, 'impares:', izquierda, derecha,
              'mixtos:', mixtos, 'encuentro:', ruta_a[-1])
    for m in [0, 1, 2, 3, 1000]:
        resultado = directo.trajectory_pair((1 << 19) * m + 3067, 18)
        assert resultado[:4] == (18, 10, 10, [1, 2, 3, 6, 9, 14, 15, 18])
        assert resultado[4][-1] == 2 * 3**10 * m + 692
    print('OK: calculo directo y simbolico 1..13; identidad y telescopado racional; testigos y levantamientos.')
    print('El control finito no prueba una afirmacion asintotica ni formaliza la descomposicion en Lean.')


if __name__ == '__main__':
    main()
