"""Sincroniza exclusivamente las fichas enviadas y el estado editorial local."""

import argparse
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
LAB = CARPETA.parents[1]
ZOO = LAB.parent / 'zootheorem'


def sustituir(texto, anterior, nuevo):
    assert texto.count(anterior) == 1, anterior
    return texto.replace(anterior, nuevo)


def normalizar_datos(texto):
    lineas = texto.splitlines()
    datos = [valor.strip() for linea in lineas if linea.startswith(('%S ', '%T ', '%U '))
             for valor in linea[3:].split(',') if valor.strip()]
    assert all(valor.isdigit() for valor in datos)
    return '\n'.join('%S ' + ','.join(datos) if linea.startswith('%S ') else linea
                     for linea in lineas if not linea.startswith(('%T ', '%U '))).rstrip() + '\n'


def normalizar_copias():
    for numero in ['A399819', 'A399820', 'A399821']:
        ruta = ZOO / 'drafts' / f'{numero}.txt'
        vigente = (CARPETA / f'{numero}_vigente.txt').read_text(encoding='utf-8')
        assert ruta.read_text(encoding='utf-8').strip() == vigente.strip()
        ruta.write_text(normalizar_datos(vigente), encoding='utf-8')
    ruta = ZOO / 'drafts/REVISION_20260917.md'
    texto = ruta.read_text(encoding='utf-8')
    texto = sustituir(texto,
        'The three draft text files were copied from the final live internal format\n'
        'and compared with the prepared text. No approval is claimed.',
        'The three draft text files were copied from the final live internal format\n'
        'and compared with the prepared text. DATA was joined onto one %S line\n'
        'for the existing local parser; every integer was preserved. The laboratory\n'
        'retains the literal server wrapping separately. No approval is claimed.')
    ruta.write_text(texto, encoding='utf-8')
    print('DATA normalizada sin alterar enteros; capturas literales preservadas.')


def main():
    cambios = {}
    for numero in ['A399819', 'A399820', 'A399821']:
        vigente = (CARPETA / f'{numero}_vigente.txt').read_text(encoding='utf-8')
        propuesto = (CARPETA / f'{numero}_propuesto.txt').read_text(encoding='utf-8')
        normalizar = lambda t: [l for l in t.splitlines() if l and not l.startswith('%I ')]
        assert normalizar(vigente) == normalizar(propuesto)
        cambios[ZOO / 'drafts' / f'{numero}.txt'] = normalizar_datos(vigente)
    ruta_plan = ZOO / 'PLAN_INVESTIGACION.md'
    plan = ruta_plan.read_text(encoding='utf-8')
    plan = sustituir(plan, '# Current plan — 2026-09-13', '# Current plan — 2026-09-17')
    plan = sustituir(plan,
        'A398792–A398795 are published. A399819–A399821 were last observed\n'
        '**proposed** after resubmission on 13-09; approval remains unconfirmed.\n'
        'Local text, offsets, ranges and the prepared but unposted A398792\n'
        'clarification: [revision note](drafts/REVISION_20260913.md).\n'
        'OEIS acceptance does not establish the asymptotic argument.',
        'A398792–A398795 are published. A399819–A399821 were observed\n'
        '**proposed** after clarification and resubmission on 17-09 (revisions\n'
        '#10, #9, #9). Irvine was answered in A399819; companion notes were posted.\n'
        'Approval remains pending. Definitions, the density motivation and the\n'
        'Elia–Tucker example are documented in [the reply record](drafts/REVISION_20260917.md).\n'
        'The prepared A398792 clarification remains unposted; see\n'
        '[the earlier audit](drafts/REVISION_20260913.md).\n'
        'OEIS acceptance does not establish the asymptotic argument.')
    cambios[ruta_plan] = plan
    ruta_arsenal = ZOO / 'drafts/ARSENAL.md'
    arsenal = ruta_arsenal.read_text(encoding='utf-8')
    arsenal = sustituir(arsenal, '# OEIS: working checklist — 13-09-2026', '# OEIS: working checklist — 17-09-2026')
    arsenal = sustituir(arsenal, '| Entry | State observed 13-09 |', '| Entry | State observed 17-09 |')
    arsenal = sustituir(arsenal,
        'Details and witnesses: [REVISION_20260913.md](REVISION_20260913.md).',
        'Irvine answered; comments clarified and all three resubmitted on 17-09.\n'
        'Reply and verification: [REVISION_20260917.md](REVISION_20260917.md).\n'
        'Offsets and historical verification: [REVISION_20260913.md](REVISION_20260913.md).')
    arsenal = sustituir(arsenal,
        'The new data/verifier files are local until published to the remote.',
        'The 17-09 editorial synchronization is local; no GitHub push in this session.')
    cambios[ruta_arsenal] = arsenal
    cambios[ZOO / 'drafts/RESPUESTA_IRVINE_20260917.txt'] = (CARPETA / 'respuesta_irvine.txt').read_text(encoding='utf-8')
    cambios[ZOO / 'drafts/REVISION_20260917.md'] = '''# OEIS clarification and reply — 2026-09-17

Sean A. Irvine asked on A399819 for an understandable definition and an
explanation of its relevance to Collatz. The [complete reply](RESPUESTA_IRVINE_20260917.txt)
was posted in [the discussion](https://oeis.org/draft/A399819) at 16:35 EDT.
Short corresponding notes were posted on A399820 and A399821.

All three entries received direct definitions, a description of lifting
residue classes, the identity sum_j e_j(n)=A398793(n-1), and the density
motivation with explicit convergence qualifications. Gao's paper was added
as a reference. A399819 also links Elia and Tucker and identifies their
3067–3068 example as one of the 237 classes at level 18 with eight mixed steps.
Data, offsets, names, original examples and programs were preserved.

| Entry | Final revision | State checked after resubmission |
|---|---|---|
| A399819 | #10 | proposed |
| A399820 | #9 | proposed |
| A399821 | #9 | proposed |

The three draft text files were copied from the final live internal format
and compared with the prepared text. No approval is claimed.

Validation for this reply: direct iteration and the independent symbolic
algorithm agreed for all levels 1..13; exact rational telescoping and the
four cited witnesses were checked. The earlier direct verification through
20 remains the provenance for that range; later terms retain the original
symbolic provenance. No larger sweep was rerun.

Lean 4.32.2 checked `lean/mirror_theorem.lean`; the lifting and periodicity
lemmas use only `propext` and `Quot.sound`, with no `sorryAx`. The density
argument and decomposition explained in the reply are written arguments,
not newly formalized Lean results. No progress on P1–P3 is claimed.

The companion laboratory preserves literal browser captures, the script,
the bounded check and a mathematical explanation in
`depuracion/oeis20260917/LEEME.md`. This note records the actual submission,
not a new research theorem. The A398792 clarification from 13-09 remains
unposted. No commit or GitHub push was made during this session.
'''
    for ruta in [ZOO / 'drafts/RESPUESTA_IRVINE_20260917.txt', ZOO / 'drafts/REVISION_20260917.md']:
        assert not ruta.exists(), ruta
    for ruta, texto in cambios.items():
        ruta.write_text(texto, encoding='utf-8')
        print(ruta.relative_to(ZOO))


if __name__ == '__main__':
    argumentos = argparse.ArgumentParser(description=__doc__)
    argumentos.add_argument('--normalizar-datos', action='store_true')
    opciones = argumentos.parse_args()
    if opciones.normalizar_datos:
        normalizar_copias()
    else:
        main()
