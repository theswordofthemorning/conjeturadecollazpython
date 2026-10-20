"""Optimo exacto de las barreras de todas las ventanas, con una misma semilla."""

import argparse
from fractions import Fraction
import itertools
import json
from math import ceil, gcd
from pathlib import Path

from cotejar_congruencias import minimo_afin, minimo_por_bits, pasos, recorrer
from cotejar_denominador import afin, huella


CARPETA = Path(__file__).resolve().parent


def afin_por_paridades(palabra):
    """Construccion paso a paso, independiente de la composicion por bloques."""
    d, e, m = 1, 0, 1
    for bit in pasos(palabra):
        if bit:
            d, e = 3 * d, 3 * e + m
        m *= 2
    return d, e, m


def recorrido_racional(n, palabra):
    """Ramas prescritas; NO afirma paridad ni integridad de las fronteras."""
    fronteras = [Fraction(n)]
    for letra in palabra:
        x = fronteras[-1]
        for bit in pasos(letra):
            x = (3 * x + 1) / 2 if bit else x / 2
        fronteras.append(x)
    return fronteras


def ventanas(palabra):
    prefijos = [afin(palabra[:i]) for i in range(len(palabra) + 1)]
    filas = []
    for i in range(len(palabra)):
        du, eu, mu = prefijos[i]
        for j in range(i + 1, len(palabra) + 1):
            d, e, m = afin_por_paridades(palabra[i:j])
            assert (d, e, m) == afin(palabra[i:j])
            g = gcd(d - m, e)
            q, r = (d - m) // g, e // g
            assert q > 0 and q <= r <= 5 * q
            a = q * du
            c = mu * (m - r) - q * eu
            filas.append(dict(i=i, j=j, d=d, e=e, m=m, q=q, r=r,
                               a=a, c=c, umbral=Fraction(c, a)))
    return filas


def satisface(n, palabra, filas):
    fronteras = recorrido_racional(n, palabra)
    assert all(x > 0 for x in fronteras)
    cumple = True
    for f in filas:
        x, y = fronteras[f['i']], fronteras[f['j']]
        assert f['m'] * y == f['d'] * x + f['e']
        barrera = f['q'] * x + f['r'] >= f['m']
        assert barrera == (f['a'] * n >= f['c'])
        cumple &= barrera
    return cumple


def minimo_por_corte(palabra, i):
    """CRT ternario del pasado y binario del futuro; conserva una frontera entera."""
    du, eu, mu = afin_por_paridades(palabra[:i])
    dv, ev, mv = afin_por_paridades(palabra[i:])
    pasado = (eu * pow(mu, -1, du)) % du
    futuro = (-ev * pow(dv, -1, mv)) % mv
    x0 = pasado + du * (((futuro - pasado) * pow(du, -1, mv)) % mv)
    modulo_x = du * mv
    umbral_x = ceil(Fraction(eu + du, mu))
    x = x0 + modulo_x * max(0, ceil(Fraction(umbral_x - x0, modulo_x)))
    assert x % du == pasado and x % mv == futuro
    assert (mu * x - eu) % du == 0
    n = (mu * x - eu) // du
    assert n >= 1
    return n


def ventanas_expansivas_por_pasos(palabra, semilla_real):
    """Amplia a fronteras T interiores, incluyendo solo ventanas con 3^S>2^L."""
    bits = pasos(palabra)
    prefijos = [(1, 0, 1)]
    for bit in bits:
        d, e, m = prefijos[-1]
        prefijos.append((3 * d, 3 * e + m, 2 * m) if bit else (d, e, 2 * m))
    filas = []
    for i in range(len(bits)):
        du, eu, mu = prefijos[i]
        d, e, m = 1, 0, 1
        for j in range(i + 1, len(bits) + 1):
            d, e, m = ((3 * d, 3 * e + m, 2 * m) if bits[j - 1]
                       else (d, e, 2 * m))
            if d <= m:
                continue
            g = gcd(d - m, e)
            q, r = (d - m) // g, e // g
            umbral = Fraction(mu * (m - r) - q * eu, q * du)
            filas.append((i, j, d, e, m, q, r, umbral))
    maximo = max([Fraction(1)] + [f[-1] for f in filas])
    menor = ceil(maximo)
    for semilla in (menor, menor - 1, semilla_real):
        if semilla < 1:
            continue
        xs = [Fraction(semilla)]
        for bit in bits:
            xs.append((3 * xs[-1] + 1) / 2 if bit else xs[-1] / 2)
        aceptada = True
        for i, j, d, e, m, q, r, umbral in filas:
            assert m * xs[j] == d * xs[i] + e
            cumple = m <= q * xs[i] + r
            assert cumple == (umbral <= semilla)
            if semilla == semilla_real:
                assert xs[i].denominator == 1
                assert ((q * xs[i] + r) / m).denominator == 1
            aceptada &= cumple
        assert aceptada == (semilla >= menor)
    return dict(ventanas=len(filas), umbral=str(maximo),
                minimo_relajado=str(menor), ell_relajada=(menor + 4).bit_length(),
                ventanas_activas=[[f[0], f[1]] for f in filas if f[-1] == maximo])


def comprobar(palabra):
    filas = ventanas(palabra)
    umbral = max([Fraction(1)] + [f['umbral'] for f in filas])
    minimo_relajado = ceil(umbral)
    assert satisface(minimo_relajado, palabra, filas)
    if minimo_relajado > 1:
        assert not satisface(minimo_relajado - 1, palabra, filas)
    n, modulo = minimo_afin(palabra)
    assert (n, modulo) == minimo_por_bits(palabra)
    for i in range(len(palabra) + 1):
        assert minimo_por_corte(palabra, i) == n
    for semilla in (n, n + modulo):
        final = recorrer(semilla, palabra)
        assert Fraction(final) == recorrido_racional(semilla, palabra)[-1]
        assert satisface(semilla, palabra, filas)
    assert minimo_relajado <= n
    activas = [[f['i'], f['j']] for f in filas if f['umbral'] == umbral]
    return dict(palabra=palabra, L=len(pasos(palabra)), ventanas=len(filas),
                minimo_real=str(n), ell_real=(n + 4).bit_length(),
                umbral=str(umbral), minimo_relajado=str(minimo_relajado),
                ell_relajada=(minimo_relajado + 4).bit_length(),
                ventanas_activas=activas,
                certifica_L_menor_igual_3ell=len(pasos(palabra)) <=
                    3 * (minimo_relajado + 4).bit_length())


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--bloques-max', type=int, required=True)
    analizador.add_argument('--familia-max', type=int, required=True)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    assert 1 <= args.bloques_max <= 10 and 1 <= args.familia_max <= 64
    niveles = []
    total_ventanas, total_cortes = 0, 0
    for k in range(args.bloques_max + 1):
        filas = [comprobar(''.join(w)) for w in itertools.product('AB', repeat=k)]
        cantidad = sum(f['ventanas'] for f in filas)
        total_ventanas += cantidad
        total_cortes += (k + 1) * len(filas)
        niveles.append(dict(bloques=k, palabras=len(filas), ventanas=cantidad,
                            igual_minimo=sum(f['minimo_real'] == f['minimo_relajado']
                                             for f in filas),
                            certifica_pendiente_3=sum(f['certifica_L_menor_igual_3ell']
                                                       for f in filas)))
    familias = []
    for b in range(args.familia_max + 1):
        f = comprobar('A' + 'B' * b)
        if b:
            assert f['umbral'] == str(Fraction(2 * 8 ** b - 11, 3))
            esperado = ((2 if b % 2 == 0 else 4) * 8 ** b - 11) // 3
            assert int(f['minimo_real']) == esperado
        assert f['L'] <= f['ell_relajada'] + 1
        familias.append(f | dict(b=b))
        total_ventanas += f['ventanas']
        total_cortes += len(f['palabra']) + 1
    # Se leen solo las 34 palabras ya reconstruidas; no se repite su censo.
    fuente = CARPETA / 'cotejo_denominador.json'
    historicos = json.loads(fuente.read_text(encoding='utf-8'))['testigos_historicos']
    testigos = []
    for viejo in historicos:
        f = comprobar(viejo['palabra'])
        assert f['minimo_real'] == viejo['minimo'] and f['L'] == viejo['L']
        f['pasos_expansivos'] = ventanas_expansivas_por_pasos(f['palabra'], int(f['minimo_real']))
        assert int(f['minimo_relajado']) <= int(f['pasos_expansivos']['minimo_relajado'])
        assert int(f['pasos_expansivos']['minimo_relajado']) <= int(f['minimo_real'])
        testigos.append(f)
        total_ventanas += f['ventanas']
        total_cortes += len(f['palabra']) + 1
    testigo = next(f for f in testigos if f['minimo_real'] == '6416623')
    assert testigo['L'] == 53 and testigo['ventanas'] == 561
    assert testigo['umbral'] == '4247/729' and testigo['minimo_relajado'] == '6'
    assert satisface(7, testigo['palabra'], ventanas(testigo['palabra']))
    assert recorrido_racional(7, testigo['palabra'])[:4] == [7, 11, 17, Fraction(79, 4)]
    assert testigo['pasos_expansivos']['minimo_relajado'] == '23'
    assert testigo['pasos_expansivos']['ventanas'] == 1391
    assert testigo['pasos_expansivos']['umbral'] == '3964757/177147'
    assert recorrido_racional(23, testigo['palabra'])[:4] == [23, 35, 53, Fraction(241, 4)]
    resultado = dict(
        alcance='Optimo de una relajacion racional, no del reloj orbital. '
                'Contrastes finitos exactos; sin nuevo censo ni extrapolacion.',
        parametros={k: v for k, v in vars(args).items() if k != 'salida'},
        niveles=niveles, familia_AB=familias, testigos_historicos=testigos,
        ventanas_distintas_por_palabra_contadas=total_ventanas,
        cortes_CRT_cotejados=total_cortes,
        ventanas_T_expansivas=sum(f['pasos_expansivos']['ventanas'] for f in testigos),
        resumen_historico=dict(total=len(testigos),
            certifica_pendiente_3=sum(f['certifica_L_menor_igual_3ell'] for f in testigos)),
        testigo_relajado=testigo | dict(semilla_impar=7,
            fronteras_iniciales=['7', '11', '17', '79/4'],
            primera_divisibilidad_fallida='8 no divide 17+5=22'),
        fuentes_sha256_lf={p.name: huella(p) for p in
            (Path(__file__), CARPETA / 'cotejar_congruencias.py',
             CARPETA / 'cotejar_denominador.py', fuente)})
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n',
                          encoding='utf-8')
    print(json.dumps(dict(palabras=sum(f['palabras'] for f in niveles),
                          familia=len(familias), ventanas=total_ventanas, cortes=total_cortes,
                          historicos=resultado['resumen_historico'],
                          testigo=testigo), ensure_ascii=False))


if __name__ == '__main__':
    main()
