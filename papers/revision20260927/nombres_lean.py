"""Comprueba que cada nombre Lean citado con \\lean{...} en los articulos existe.

Para cada nombre, toma el ultimo componente (tras el ultimo punto) y lo busca como
`theorem X`, `lemma X`, `def X`, `noncomputable def X`, `structure X` o
`namespace X` en los fuentes de depuracion/gao20260920 (y en rachas.lean).
Los nombres de archivo (X.lean) se buscan como archivos. Si el nombre trae
espacio de nombres (A.B), comprueba ademas que el archivo que define B declara
`namespace A`.

Uso: python -B -X utf8 nombres_lean.py
"""

import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
FUENTES = sorted((RAIZ / 'depuracion' / 'gao20260920' / 'formal').glob('*.lean'))
FUENTES += [RAIZ / 'depuracion' / 'gao20260920' / 'cadena_completa.lean',
            RAIZ / 'depuracion' / 'frente20260910' / 'rachas.lean']
TEXTOS = sorted((RAIZ / 'papers').glob('articulo_*.tex'))
NO_LEAN = {'905b95818eb3', 'depuracion/gao20260920/formal', 'cadena_completa', 'native_decide', 'implemented_by', 'infer_instance'}


def main():
    declarado = {}
    for f in FUENTES:
        texto = f.read_text(encoding='utf-8')
        espacios = re.findall(r'^namespace (\S+)', texto, re.M)
        for m in re.finditer(r'^(?:noncomputable )?(?:theorem|lemma|def|structure|inductive|abbrev) (\S+)',
                             texto, re.M):
            declarado.setdefault(m.group(1), set()).update(espacios or [''])
    archivos = {f.name for f in FUENTES}
    ok = True
    for tex in TEXTOS:
        nombres = sorted(set(re.findall(r'\\lean\{([^{}]*)\}', tex.read_text(encoding='utf-8'))))
        malos = []
        for n in nombres:
            if n in NO_LEAN:
                continue
            if n.endswith('.lean'):
                if n not in archivos:
                    malos.append(n)
                continue
            partes = n.split('.')
            final = partes[-1]
            if final not in declarado:
                malos.append(n)
                continue
            if len(partes) >= 2:
                espacio = partes[-2]
                if espacio not in declarado[final]:
                    malos.append(n + ' (espacio ' + espacio + ' no coincide: ' + str(sorted(declarado[final])) + ')')
        print(tex.name, ':', len(nombres), 'nombres;', 'sin problemas' if not malos else 'PROBLEMAS: ' + str(malos))
        ok = ok and not malos
    print('OK' if ok else 'FALLO')
    return ok


if __name__ == '__main__':
    raise SystemExit(0 if main() else 1)
