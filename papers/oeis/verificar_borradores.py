"""Verifica los tres borradores OEIS del 27-09-2026 antes de cualquier envio.

1. Ejecuta, tal cual, el programa Python (%o) de los borradores 1 y 2 y compara
   su salida con los datos (%S).
2. Coteja %S con las b-files de esta carpeta (terminos_oeis.py).
3. Comprueba el desfase %O (primer indice, posicion del primer |a| >= 2).
4. Comprueba las formulas %F:
   - Gao: a(n+1) >= 2*a(n) en todos los terminos;
   - Wu: a(n) = #{1 <= k < 2^n: k o k-1 en A078417}, con la b-file oficial de
     A078417 (copia en depuracion/oeis20260924) mientras alcance.
5. Recalcula los ejemplos (%e) y las cifras citadas en los comentarios.

Uso: python -B -X utf8 verificar_borradores.py
Termina con SystemExit(1) si algo no cuadra.
"""

import contextlib
import io
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
B078417 = CARPETA.parent.parent / 'depuracion' / 'oeis20260924' / 'b078417_oficial.txt'


def leer(nombre):
    lineas = (CARPETA / nombre).read_text(encoding='utf-8').splitlines()
    datos = None
    programa = []
    desfase = None
    for linea in lineas:
        if linea.startswith('%S '):
            datos = [int(x) for x in linea.split(' ', 2)[2].split(',')]
        if linea.startswith('%o '):
            programa.append(linea.split(' ', 2)[2] if len(linea.split(' ', 2)) > 2 else '')
        if linea.startswith('%O '):
            desfase = tuple(int(x) for x in linea.split(' ', 2)[2].split(','))
    return datos, programa, desfase


def ejecutar(programa):
    codigo = '\n'.join(l for l in programa if l != '(Python)')
    salida = io.StringIO()
    with contextlib.redirect_stdout(salida):
        exec(codigo, {})
    return eval(salida.getvalue().strip())


def leer_bfile(nombre):
    valores = []
    for linea in (CARPETA / nombre).read_text(encoding='ascii').splitlines():
        indice, valor = linea.split()
        valores.append((int(indice), int(valor)))
    return valores


def desfase_correcto(datos, primero):
    for i, v in enumerate(datos):
        if abs(v) >= 2:
            return (primero, primero + i)
    return (primero, 1)


def coalescen_en(m, n):
    """Paso j <= n en que m y m+1 coalescen en el sentido de Gao, o None."""
    x, y, hx, hy = m, m + 1, 0, 0
    for j in range(n + 1):
        if x == 1 or y == 1:
            return None
        if x == y:
            return j if hx == hy else None
        hx += x % 2 == 0
        hy += y % 2 == 0
        x = x // 2 if x % 2 == 0 else 3 * x + 1
        y = y // 2 if y % 2 == 0 else 3 * y + 1
    return None


def pasos(k):
    s = 0
    while k != 1:
        k = k // 2 if k % 2 == 0 else 3 * k + 1
        s += 1
    return s


def main():
    ok = True

    # Borrador 1: Gao
    datos, programa, desfase = leer('borrador_1_gao.txt')
    salida = ejecutar(programa)
    bien = salida == datos[:len(salida)]
    print('Gao: programa de la ficha da %d terminos iguales a %%S: %s' % (len(salida), bien))
    ok = ok and bien
    b = leer_bfile('bfile_gao_tabla3.txt')
    bien = [v for _, v in b] == datos and b[0][0] == 1
    print('Gao: b-file (n = 1..%d) igual a %%S: %s' % (b[-1][0], bien))
    ok = ok and bien
    bien = desfase == desfase_correcto(datos, 1)
    print('Gao: %%O %s, correcto %s: %s' % (desfase, desfase_correcto(datos, 1), bien))
    ok = ok and bien
    bien = all(datos[i + 1] >= 2 * datos[i] for i in range(len(datos) - 1))
    print('Gao: a(n+1) >= 2 a(n) en todos los terminos: %s' % bien)
    ok = ok and bien
    lista4 = [m for m in range(2 ** 4 - 1) if coalescen_en(m, 4) is not None]
    lista5 = [m for m in range(2 ** 5 - 1) if coalescen_en(m, 5) is not None]
    bien = lista4 == [12] and lista5 == [12, 18, 20, 28] and coalescen_en(18, 5) == 5
    bien = bien and coalescen_en(14, 8) is None and coalescen_en(14, 9) == 9
    print('Gao: ejemplos a(4) = {12}, a(5) = {12, 18, 20, 28}, 14 entra en n = 9: %s' % bien)
    ok = ok and bien
    cifras = (round(datos[23] / 2 ** 24, 3), round(datos[27] / 2 ** 28, 3))
    bien = cifras == (0.389, 0.4)
    print('Gao: a(24)/2^24 y a(28)/2^28 redondeados:', cifras, bien)
    ok = ok and bien

    # Borrador 2: Wu
    datos, programa, desfase = leer('borrador_2_wu.txt')
    salida = ejecutar(programa)
    bien = salida == datos[:len(salida)]
    print('Wu: programa de la ficha da %d terminos iguales a %%S: %s' % (len(salida), bien))
    ok = ok and bien
    b = leer_bfile('bfile_wu_rachas.txt')
    bien = [v for _, v in b] == datos and b[0][0] == 1
    print('Wu: b-file (n = 1..%d) igual a %%S: %s' % (b[-1][0], bien))
    ok = ok and bien
    bien = desfase == desfase_correcto(datos, 1)
    print('Wu: %%O %s, correcto %s: %s' % (desfase, desfase_correcto(datos, 1), bien))
    ok = ok and bien
    a078417 = set()
    ultimo = 0
    for linea in B078417.read_text(encoding='utf-8').splitlines():
        partes = linea.split()
        if len(partes) == 2 and not linea.startswith('#'):
            a078417.add(int(partes[1]))
            ultimo = max(ultimo, int(partes[1]))
    comprobados = 0
    for n in range(1, 40):
        if 2 ** n > ultimo:
            break
        cuenta = sum(1 for k in range(1, 2 ** n) if k in a078417 or (k - 1) in a078417)
        bien = cuenta == datos[n - 1]
        ok = ok and bien
        comprobados = n
    print('Wu: %%F con la b-file oficial de A078417 (hasta %d) para n = 1..%d: %s'
          % (ultimo, comprobados, ok))
    ejemplo = [k for k in range(1, 16) if (k > 1 and pasos(k) == pasos(k - 1)) or pasos(k) == pasos(k + 1)]
    bien = ejemplo == [12, 13, 14, 15] and [pasos(k) for k in ejemplo] == [9, 9, 17, 17]
    print('Wu: ejemplo a(4) = {12, 13, 14, 15} con 9, 9, 17, 17 pasos: %s' % bien)
    ok = ok and bien
    cifras = tuple(round(datos[n - 1] / (2 ** n - 1), 3) for n in (10, 24, 26))
    bien = cifras == (0.606, 0.725, 0.732)
    bien = bien and all(datos[n] / (2 ** (n + 1) - 1) > datos[n - 1] / (2 ** n - 1) for n in range(3, 26))
    print('Wu: cifras 0.606, 0.725, 0.732 y crecimiento desde n = 4:', cifras, bien)
    ok = ok and bien

    # Borrador 3: A078441 (la tabla 1 de Gao son terminos de A078441)
    b078441 = {}
    ruta = Path(__file__).resolve().parent / 'b078441_oficial.txt'
    if ruta.exists():
        for linea in ruta.read_text(encoding='utf-8').splitlines():
            partes = linea.split()
            if len(partes) == 2:
                b078441[int(partes[0])] = int(partes[1])
        tabla1 = {7: 943, 17: 7083, 25: 57346, 40: 596310, 65: 5772712, 98: 98041684,
                  176: 722067240}
        bien = all(b078441[k] == v for k, v in tabla1.items())
        bien = bien and b078441[177] > 2 ** 30
        print('A078441: los comienzos de la tabla 1 de Gao son a(7), ..., a(176), y a(177) > 2^30: %s' % bien)
        ok = ok and bien
    else:
        print('A078441: falta b078441_oficial.txt en esta carpeta (no se coteja)')
        ok = False

    print('OK' if ok else 'FALLO')
    return ok


if __name__ == '__main__':
    raise SystemExit(0 if main() else 1)
