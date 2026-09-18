"""Coteja capturas OEIS, conservación de datos y errata de punto de encuentro."""

import argparse
from pathlib import Path
import re

CARPETA = Path(__file__).resolve().parent
ZOO = CARPETA.parents[2] / 'zootheorem'


def lineas(texto, codigos):
    return [linea for linea in texto.splitlines() if linea[:2] in codigos]


def verificar(sincronizar):
    informe = []
    for numero, respuesta in [('A399819', 'howroyd'), ('A399820', 'marcus'), ('A399821', 'companera')]:
        leer = lambda sufijo: (CARPETA / f'{numero}_{sufijo}_tarde.txt').read_text(encoding='utf-8')
        antes, propuesto, vigente = leer('antes'), leer('propuesto'), leer('vigente')
        sin_revision = lambda texto: [l for l in texto.splitlines() if l and not l.startswith('%I ')]
        assert sin_revision(propuesto) == sin_revision(vigente), numero
        codigos = {'%S', '%T', '%U', '%O', '%o', '%e', '%A', '%Y', '%K', '%D'}
        assert lineas(antes, codigos) == lineas(vigente, codigos), numero
        respuesta_texto = (CARPETA / f'respuesta_{respuesta}_tarde.txt').read_text(encoding='utf-8')
        final = leer('final')
        assert ' '.join(respuesta_texto.split()) in ' '.join(final.split()), numero
        assert 'These changes are ready for review by an OEIS Editor.' not in final
        datos = [v.strip() for l in lineas(vigente, {'%S', '%T', '%U'})
                 for v in l[3:].split(',') if v.strip()]
        filas = [tuple(map(int, l.split())) for l in
                 (ZOO / 'seqs' / f'b{numero[1:]}.txt').read_text().splitlines()
                 if l.strip() and not l.startswith('#')]
        assert list(map(int, datos)) == [v for _, v in filas]
        if sincronizar:
            normalizado = '\n'.join('%S ' + ','.join(datos) if l.startswith('%S ') else l
                                    for l in vigente.splitlines() if not l.startswith(('%T ', '%U '))) + '\n'
            (ZOO / 'drafts' / f'{numero}.txt').write_text(normalizado, encoding='utf-8')
        informe.append(f'{numero}: {vigente.splitlines()[0]}; datos, offset, ejemplos y programa conservados; respuesta comprobada; proposed.')
    panel = (CARPETA / 'panel_final_tarde.txt').read_text(encoding='utf-8')
    assert panel.count('proposed +') == 3 and 'editing +' not in panel
    publicado = (CARPETA / 'busqueda_autor_tarde.txt').read_text(encoding='utf-8')
    for numero, nombre, cantidad in [('A398792', 'merging_classes_3x1', 36),
                                    ('A398793', 'new_classes_3x1', 35),
                                    ('A398794', 'merging_classes_5x1', 29),
                                    ('A398795', 'merging_classes_7x1', 29)]:
        bloque = publicado.split('\n' + numero + '\n', 1)[1]
        datos = list(map(int, re.search(r'^\d+(?:, \d+)+$', bloque, re.M).group().split(', ')))
        locales = [int(l.split()[1]) for l in (ZOO / 'seqs' / f'bfile_{nombre}.txt').read_text().splitlines()
                   if l.strip() and not l.startswith('#')]
        assert len(datos) == cantidad and datos[:len(locales)] == locales
        informe.append(f'{numero}: {cantidad} terminos publicados; coinciden los {len(locales)} terminos locales; sin editar por limite de OEIS.')
    for j in range(2, 21, 2):
        x, y = 2**j - 2, 2**j - 1
        sx = sy = 0
        for paso in range(1, j + 3):
            anterior = x, y
            sx += x % 2
            sy += y % 2
            x = (3*x+1)//2 if x % 2 else x//2
            y = (3*y+1)//2 if y % 2 else y//2
            if x == y:
                assert paso == j + 2
                break
        assert x == y == (3**j-1)//4 and sx == sy == j
        assert anterior == ((3**(j-1)-1)//2, (3**j-1)//2)
    informe.append('Conejas: j=2..20 pares, primer encuentro, entradas impares y valores previos cotejados con enteros. No es prueba universal.')
    salida = '\n'.join(informe) + '\n'
    (CARPETA / 'verificacion_tarde.txt').write_text(salida, encoding='utf-8')
    print(salida, end='')


if __name__ == '__main__':
    argumentos = argparse.ArgumentParser()
    argumentos.add_argument('--sincronizar', action='store_true')
    verificar(argumentos.parse_args().sincronizar)
