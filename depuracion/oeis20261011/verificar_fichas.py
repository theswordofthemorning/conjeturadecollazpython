# Ejecuta tal cual el programa %o de cada ficha y lo coteja con %S; revisa ejemplos y offsets.
# Uso: python -B -X utf8 verificar_fichas.py --carpeta .
import argparse
import contextlib
import io
import os


def leer(ruta):
    campos = {}
    with open(ruta, encoding='utf8') as f:
        for linea in f:
            linea = linea.rstrip('\n')
            clave, resto = linea[:2], linea[11:]
            campos.setdefault(clave, []).append(resto)
    return campos


def ejecutar(lineas):
    salida = io.StringIO()
    codigo = '\n'.join(l for l in lineas if l != '(Python)')
    with contextlib.redirect_stdout(salida):
        exec(codigo, {})
    return [int(x) for x in salida.getvalue().strip().strip('[]').split(',')]


def C(x):
    return x // 2 if x % 2 == 0 else 3 * x + 1


def T(x):
    return x // 2 if x % 2 == 0 else (3 * x + 1) // 2


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--carpeta', required=True)
    carpeta = p.parse_args().carpeta
    todo = True
    for nombre in ('ficha_1_encuentro.txt', 'ficha_2_casiciclos.txt', 'ficha_3_racha_wu.txt'):
        f = leer(os.path.join(carpeta, nombre))
        datos = [int(x) for x in ''.join(f['%S']).split(',')]
        prog = ejecutar(f['%o'])
        n = min(len(prog), len(datos))
        ok_prog = prog[:n] == datos[:n] and n >= 16
        primero, segundo = (int(x) for x in f['%O'][0].split(','))
        pos = next(i for i, v in enumerate(datos, primero) if abs(v) >= 2)
        ok_off = pos == segundo
        largo = len(','.join(map(str, datos)))
        print(nombre, '| programa = datos en %d términos: %s | offset: %s | %d caracteres'
              % (n, ok_prog, ok_off, largo))
        todo = todo and ok_prog and ok_off and largo <= 260
    # Ejemplos
    t12 = [12]
    for _ in range(3):
        t12.append(C(t12[-1]))
    t13 = [13]
    for _ in range(3):
        t13.append(C(t13[-1]))
    a = [14]; b = [15]
    for _ in range(9):
        a.append(C(a[-1])); b.append(C(b[-1]))
    ej1 = t12 == [12, 6, 3, 10] and t13 == [13, 40, 20, 10] and a[9] == b[9] and \
        all(a[i] != b[i] for i in range(9)) and a == [14, 7, 22, 11, 34, 17, 52, 26, 13, 40] and \
        b == [15, 46, 23, 70, 35, 106, 53, 160, 80, 40]
    x = [7]
    for _ in range(8):
        x.append(T(x[-1]))
    q = sum(v % 2 for v in x[:8])
    ej2 = x == [7, 11, 17, 26, 13, 20, 10, 5, 8] and q == 5 and 3 ** 5 < 2 ** 8 and \
        [3, T(3), T(T(3)), T(T(T(3)))] == [3, 5, 8, 4]

    def h(k):
        s = 0
        while k != 1:
            k, s = C(k), s + 1
        return s
    ej3 = h(12) == h(13) == 9 and h(14) == h(15) == 17 and h(28) == h(29) == h(30) == 18 and h(27) != 18 and h(31) != 18
    garner = all(C(C(C(8 * k + 4))) == 6 * k + 4 == C(C(C(8 * k + 5))) for k in range(1, 1000))
    print('ejemplos ficha 1: %s, ficha 2: %s, ficha 3: %s; pares de Garner: %s' % (ej1, ej2, ej3, garner))
    todo = todo and ej1 and ej2 and ej3 and garner
    print('OK' if todo else 'FALLO')


if __name__ == '__main__':
    main()
