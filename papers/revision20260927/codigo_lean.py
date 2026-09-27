"""Coteja los bloques de codigo Lean de los articulos con los fuentes reales.

Cada bloque Verbatim se parte en declaraciones (lineas que empiezan por def,
theorem, noncomputable def, ...). Se quitan los comentarios `--`, se juntan los
espacios, y se exige que cada declaracion aparezca tal cual en el fuente
correspondiente, tambien con los espacios juntados. Asi se admite partir lineas
para el PDF, pero no cambiar ni un simbolo.

Uso: python -B -X utf8 codigo_lean.py
"""

import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
FORMAL = RAIZ / 'depuracion' / 'gao20260920' / 'formal'
FUENTE = {
    'articulo_I_gao.tex': ['GaoEnunciado.lean', 'Hienas.lean', 'GaoLiteral.lean'],
    'articulo_II_garner.tex': ['GarnerEnunciado.lean'],
    'articulo_III_wu.tex': ['WuEnunciado.lean'],
}
INICIO = re.compile(r'^(noncomputable def|def|theorem|lemma)\b')


def juntar(texto):
    sin_comentarios = '\n'.join(l.split('--')[0] for l in texto.splitlines())
    return ' '.join(sin_comentarios.split())


def main():
    ok = True
    for nombre, fuentes in FUENTE.items():
        tex = (RAIZ / 'papers' / nombre).read_text(encoding='utf-8')
        fuente = juntar('\n'.join((FORMAL / f).read_text(encoding='utf-8') for f in fuentes))
        bloques = re.findall(r'\\begin\{Verbatim\}(?:\[[^\]]*\])?\n(.*?)\\end\{Verbatim\}', tex, re.S)
        declaraciones = []
        for b in bloques:
            actual = []
            for linea in b.splitlines():
                if INICIO.match(linea) and actual:
                    declaraciones.append('\n'.join(actual))
                    actual = []
                actual.append(linea)
            if actual:
                declaraciones.append('\n'.join(actual))
        malas = [d for d in declaraciones if juntar(d) not in fuente]
        print(nombre, ':', len(declaraciones), 'declaraciones;',
              'todas literales' if not malas else 'DISTINTAS:')
        for d in malas:
            print('   ', juntar(d))
        ok = ok and not malas
    print('OK' if ok else 'FALLO')
    return ok


if __name__ == '__main__':
    raise SystemExit(0 if main() else 1)
