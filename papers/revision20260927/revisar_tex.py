"""Controles de forma de los tres articulos (27-09-2026).

Para cada .tex de papers/:
- lineas de codigo (entornos Verbatim) de mas de LARGO_MAXIMO caracteres;
- largo del resumen en texto plano aproximado (arXiv admite hasta 1920);
- marcas [TO CONFIRM] y [TO UPDATE] que quedan para el autor;
- citas usadas sin \\bibitem y \\bibitem nunca citados.

Uso: python -B -X utf8 revisar_tex.py
"""

import re
from pathlib import Path

CARPETA = Path(__file__).resolve().parent.parent
LARGO_MAXIMO = 72
LIMITE_RESUMEN = 1920


def resumen_plano(texto):
    m = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', texto, re.S)
    if not m:
        return ''
    r = m.group(1)
    r = re.sub(r'\\(texttt|emph|lean)\{([^{}]*)\}', r'\2', r)
    r = r.replace('$', '')
    r = re.sub(r'\\[a-zA-Z]+', '', r)
    r = r.replace('{', '').replace('}', '')
    return ' '.join(r.split())


def main():
    ok = True
    for tex in sorted(CARPETA.glob('articulo_*.tex')):
        texto = tex.read_text(encoding='utf-8')
        print('==', tex.name)
        bloques = re.findall(r'\\begin\{Verbatim\}(?:\[[^\]]*\])?\n(.*?)\\end\{Verbatim\}',
                             texto, re.S)
        largas = [l for b in bloques for l in b.splitlines() if len(l) > LARGO_MAXIMO]
        print('   bloques de codigo:', len(bloques), ' lineas largas:', len(largas))
        for l in largas:
            print('     ', len(l), l)
        resumen = resumen_plano(texto)
        print('   resumen: %d caracteres (limite %d)' % (len(resumen), LIMITE_RESUMEN))
        marcas = re.findall(r'\[TO (?:CONFIRM|UPDATE)[^\]]*\]', texto)
        print('   marcas para el autor:', len(marcas), sorted(set(marcas)))
        citas = set()
        for grupo in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]*)\}', texto):
            citas |= {c.strip() for c in grupo.split(',')}
        items = set(re.findall(r'\\bibitem\{([^}]*)\}', texto))
        sin_item = citas - items
        sin_cita = items - citas
        print('   citas sin bibitem:', sorted(sin_item), ' bibitem sin cita:', sorted(sin_cita))
        ok = ok and not largas and len(resumen) <= LIMITE_RESUMEN and not sin_item
    print('OK' if ok else 'REVISAR')
    return ok


if __name__ == '__main__':
    raise SystemExit(0 if main() else 1)
