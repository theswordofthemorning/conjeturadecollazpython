"""Prepara aclaraciones OEIS conservando datos, indices, ejemplos y programa."""

from pathlib import Path

CARPETA = Path(__file__).resolve().parent


def main():
    for numero, mixtos in [('A399819', 8), ('A399820', 10), ('A399821', 12)]:
        original = (CARPETA / f'{numero}_antes.txt').read_text(encoding='utf-8')
        comentarios = [
            'Let T be the Collatz map (A014682): T(x) = x/2 for even x and (3*x+1)/2 for odd x. Iterate T simultaneously from r and r+1, for each integer r with 0 <= r < 2^n.',
            f'Count r if the two trajectories first meet after exactly n iterations, have the same number of odd inputs among these n iterations, and have opposite input parities at exactly {mixtos} of them. An iteration with opposite input parities is called a mixed-parity step; steps are numbered 1 through n, including the meeting step.',
            f'The first nonzero term is at n = {mixtos + 1}. The sequences A399819, A399820 and A399821 count the cases with 8, 10 and 12 mixed-parity steps, respectively.',
            'The equal odd counts ensure that the meeting holds for the entire residue class modulo 2^n: if each path has s odd inputs, replacing r by r + 2^n*m adds 3^s*m to both values at step n. Thus each counted r represents an infinite family of consecutive pairs, not just one numerical coincidence.',
            'These sequences refine A398793 by the number of mixed-parity steps. If e_j(n) denotes the same count with j mixed-parity steps, then sum_j e_j(n) = A398793(n-1) = A398792(n) - 2*A398792(n-1), for n >= 2. Only even j can occur, since equal odd counts require equally many mixed steps of each orientation.',
            'This decomposition records how different parity patterns contribute to the density of merging consecutive pairs, in connection with the question studied by Gao. The quantity e_j(n)/2^n is the density added at level n by that part of the count. Proving lim A398792(n)/2^n = 1 remains an open objective; the three fixed values j = 8, 10, 12 alone do not settle it.',
            'The counts require only finite trajectories and do not assume the Collatz conjecture. For lifted pairs r + 2^n*m, r + 2^n*m + 1 with m >= 1, equal finite total stopping times follow if their common trajectory reaches 1.'
        ]
        if mixtos == 8:
            comentarios.append('A concrete connection with earlier work is the pair (3067,3068), used by Elia and Tucker to disprove Garner\'s conjecture about equal-height pairs. Under T it first meets at 692 after 18 iterations, with 10 odd inputs on each path and 8 mixed-parity steps. Hence r = 3067 is one of the 237 classes counted by a(18).')
        salida = []
        insertado = False
        for linea in original.splitlines():
            if linea.startswith('%C '):
                if not insertado:
                    salida.extend('%C ' + comentario for comentario in comentarios)
                    salida.append('%D G.-G. Gao, On consecutive numbers of the same height in the Collatz problem, Discrete Mathematics 112 (1993), 261-267.')
                    insertado = True
                continue
            salida.append(linea)
            if linea.startswith('%H ') and mixtos == 8:
                salida.append('%H Marcus Elia and Amanda Tucker, <a href="https://arxiv.org/abs/1511.09141">Consecutive Integers and the Collatz Conjecture</a>, Integers 15 (2015), A54, Section 4.')
        texto = '\n'.join(salida).rstrip() + '\n'
        campos = ('%S ', '%T ', '%U ', '%O ', '%N ', '%e ', '%o ', '%Y ', '%K ', '%A ')
        assert [x for x in original.splitlines() if x.startswith(campos)] == [x for x in texto.splitlines() if x.startswith(campos)]
        (CARPETA / f'{numero}_propuesto.txt').write_text(texto, encoding='utf-8')
        print(numero, 'datos, offset, nombre, ejemplos, programa y referencias cruzadas conservados')


if __name__ == '__main__':
    main()
