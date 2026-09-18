"""Prepara las tres aclaraciones; conserva literalmente los campos de conteo."""

import hashlib
import json
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
GAO = 'Guo-Gang Gao, <a href="https://doi.org/10.1016/0012-365X(93)90240-T">On consecutive numbers of the same height in the Collatz problem</a>, Discrete Mathematics, Volume 112, pages 261-267, 1993.'
TERRAS = 'Riho Terras, <a href="https://doi.org/10.4064/aa-30-3-241-252">A stopping time problem on the positive integers</a>, Acta Arithmetica 30 (1976), 241-252.'
GARNER = 'Lynn E. Garner, <a href="https://doi.org/10.1016/S0012-365X(85)80020-0">On heights in the Collatz 3n+1 problem</a>, Discrete Mathematics 55 (1985), 57-64.'


def preparar(numero, desacuerdos, inicio):
    anterior = (CARPETA / f'{numero}_antes_tarde.txt').read_text(encoding='utf-8')
    lineas = anterior.splitlines()
    nombre = (f'Number of integers 0 <= r < 2^n whose trajectories from r and r+1 '
              f'under the Collatz map (A014682) first meet after n iterations, '
              f'with equal numbers of odd inputs and exactly {desacuerdos} positions of opposite input parity.')
    comentarios = [
        'Let T be the Collatz map (A014682): T(x) = x/2 for even x and (3*x+1)/2 for odd x. For each integer r with 0 <= r < 2^n, set x_i = T^i(r) and y_i = T^i(r+1), for i = 0,...,n.',
        f'Count r if x_n = y_n, x_i != y_i for every 0 <= i < n, the lists x_0,...,x_(n-1) and y_0,...,y_(n-1) contain equally many odd terms, and exactly {desacuerdos} indices i in 0,...,n-1 have x_i and y_i of opposite parity.',
        'A mixed-parity step is defined here to be an iteration whose two input values have opposite parity, namely an index i with x_i and y_i of opposite parity. This is step i+1 in the examples, where steps are numbered 1 through n.',
        'A merging class at level n is defined here to be a residue class modulo 2^n whose two trajectories satisfy x_n = y_n and have equal numbers of odd inputs before that meeting. Such a class is new at level n when x_i != y_i for every 0 <= i < n. The phrases "mixed-parity step" and "merging class" are local terminology in these three entries.',
        f'The first nonzero term is at n = {inicio}. A399819, A399820 and A399821 impose 8, 10 and 12 opposite-parity positions, respectively.',
        'The equal odd counts make this a property of the whole residue class: if each path has s odd inputs, replacing r by r + 2^n*m adds 3^s*m to both values at step n (Terras). The first meeting and its parity pattern are preserved for every integer m >= 0.',
        'Writing e_j(n) for the same count with j opposite-parity positions, sum_j e_j(n) = A398793(n-1) = A398792(n) - 2*A398792(n-1), for n >= 2. Only even j occur, since the two orientations of an opposite-parity position must occur equally often.',
        'Thus e_j(n)/2^n is the density of the residue classes first meeting at step n with j opposite-parity positions. These counts refine A398793 by parity pattern, in connection with the consecutive-pair questions studied by Gao. They do not establish that lim A398792(n)/2^n = 1.',
        'The counts use finite trajectories and require no convergence assumption. For lifted pairs r + 2^n*m, r + 2^n*m + 1 with m >= 1, equal finite total stopping times follow if their common trajectory reaches 1.'
    ]
    if numero == 'A399819':
        comentarios.extend(l[3:] for l in lineas if l.startswith('%C A concrete connection'))
    enlaces = [l[3:] for l in lineas if l.startswith('%H ')]
    for enlace in [GAO, TERRAS] + ([GARNER] if numero == 'A399819' else []):
        if enlace not in enlaces:
            enlaces.append(enlace)
    enlaces.sort(key=lambda t: ('Elia' if t.startswith('Marcus Elia') else
                               'Garner' if t.startswith('Lynn') else
                               'Gao' if t.startswith('Guo') else
                               'Terras' if t.startswith('Riho') else 'Said'))
    salida = []
    puestos = set()
    for linea in lineas:
        codigo = linea[:2]
        if codigo in ('%N', '%C', '%H'):
            if codigo not in puestos:
                valores = {'%N': [nombre], '%C': comentarios, '%H': enlaces}[codigo]
                salida.extend(codigo + ' ' + valor for valor in valores)
                puestos.add(codigo)
        else:
            salida.append(linea)
    conservados = lambda ls: [l for l in ls if not l.startswith(('%N ', '%C ', '%H '))]
    assert conservados(lineas) == conservados(salida)
    texto = '\n'.join(salida) + '\n'
    (CARPETA / f'{numero}_propuesto_tarde.txt').write_text(texto, encoding='utf-8')
    return {'numero': numero, 'sha256_antes': hashlib.sha256(anterior.encode()).hexdigest(),
            'sha256_propuesto': hashlib.sha256(texto.encode()).hexdigest(),
            'campos_modificados': ['NAME', 'COMMENTS', 'LINKS'],
            'datos_offset_programa_ejemplos': 'conservados literalmente'}


if __name__ == '__main__':
    cambios = [preparar(numero, j, inicio) for numero, j, inicio in
               [('A399819', 8, 9), ('A399820', 10, 11), ('A399821', 12, 13)]]
    (CARPETA / 'cambios_tarde.json').write_text(
        json.dumps({'fecha': '2026-09-17', 'cambios': cambios}, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8')
    print('Tres aclaraciones preparadas; datos, offsets, ejemplos y programas conservados.')
