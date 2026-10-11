"""Compara T, la transición G y los reinicios F con aritmética entera."""

import argparse
import hashlib
from itertools import product
import json
from pathlib import Path


def valuacion(x, primo):
    assert x > 0 and primo in (2, 3)
    cuenta = 0
    while x % primo == 0:
        cuenta += 1
        x //= primo
    return cuenta


def transicion(z):
    assert z % 8 == 7
    v = valuacion(9 * z + 1, 2)
    return 3 ** (v - 3) * ((9 * z + 1) // 2 ** v), v - 3


def datos_reinicio(h):
    assert h > 0 and h % 2 == 1
    a = valuacion(9 * h - 1, 2)
    m = (9 * h - 1) // 2 ** a
    carga = 3 ** a * m + 1
    k = valuacion(carga, 2)
    siguiente = None
    if k % 3 == 0:
        b = k // 3
        siguiente = 9 ** (b - 1) * (carga // 2 ** k)
    return siguiente, a, k, carga


def inversa(siguiente):
    if siguiente <= 0 or siguiente % 2 == 0:
        return None
    orden = valuacion(siguiente, 3)
    if orden % 2:
        return None
    b = orden // 2 + 1
    carga = 8 ** b * (siguiente // 9 ** (b - 1))
    a = valuacion(carga - 1, 3)
    if a == 0:
        return None
    m = (carga - 1) // 3 ** a
    numerador = 2 ** a * m + 1
    return numerador // 9 if numerador % 9 == 0 else None


def recorrer_palabra(x, palabra):
    for bit in palabra:
        assert x % 2 == int(bit)
        x = (3 * x + 1) // 2 if x % 2 else x // 2
    return x


def salidas(zmax):
    dominios, rechazados, resonantes, ceros = 0, 0, 0, 0
    for z in range(zmax + 1):
        v = valuacion(z + 1, 2)
        assert (z % 8 == 7) == (v >= 3)
        if z % 8 != 7:
            continue
        dominios += 1
        if v > 3:
            y, a = transicion(z)
            assert a == 0 and 8 * (y + 1) == 9 * (z + 1)
            assert valuacion(y + 1, 2) == v - 3
            ceros += 1
        y = z
        if v % 3:
            for _ in range(v // 3):
                assert y % 8 == 7
                y, a = transicion(y)
                assert a == 0
            assert y % 8 != 7
            rechazados += 1
        else:
            for _ in range(v // 3 - 1):
                y, a = transicion(y)
                assert a == 0
            assert valuacion(y + 1, 2) == 3
            assert y + 1 == 8 * 9 ** (v // 3 - 1) * ((z + 1) // 2 ** v)
            resonantes += 1
    return dict(dominio=dominios, salidas_por_residuo=rechazados,
                llegada_a_cambio=resonantes, pasos_sin_cambio=ceros,
                unidad='Pasos de G; no son pasos de T ni el instante del primer bit incompatible.')


def reinicios(hmax):
    aceptados, rechazados, identidades, imagenes = 0, 0, 0, set()
    ejemplos = []
    for h in range(1, hmax + 1, 2):
        siguiente, a, k, carga = datos_reinicio(h)
        z = 8 * h - 1
        y, aa = transicion(z)
        assert aa == a and y + 1 == carga
        assert a >= 1 and k >= 1 and 13 * h <= carga
        if siguiente is None:
            for _ in range(k // 3):
                assert y % 8 == 7
                y, cero = transicion(y)
                assert cero == 0
            assert y % 8 != 7
            rechazados += 1
            continue
        b = k // 3
        for _ in range(b - 1):
            y, cero = transicion(y)
            assert cero == 0
        assert y + 1 == 8 * siguiente
        assert siguiente % 2 == 1 and 8 * siguiente >= 13 * h
        assert valuacion(siguiente, 3) == 2 * (b - 1)
        assert inversa(siguiente) == h
        palabra = '110' + '1' * a + '110' * (b - 1)
        assert recorrer_palabra(32 * h - 5, palabra) == 32 * siguiente - 5
        assert 2 ** (a + 3 * b) * siguiente == 9 ** (b - 1) * (3 ** a * (9 * h - 1) + 2 ** a)
        aceptados += 1
        identidades += len(palabra)
        imagenes.add(siguiente)
        if h in (3, 21, 117, 147, 323):
            ejemplos.append(dict(h=h, siguiente=siguiente, a=a, b=b, palabra=palabra))
    inversas = 0
    for y in range(1, hmax + 1, 2):
        h = inversa(y)
        assert (h is not None) == (y in imagenes)
        if h is not None:
            assert 0 < h < y and h % 2 == 1 and datos_reinicio(h)[0] == y
            inversas += 1
    return dict(entradas=(hmax + 1) // 2, reinicios_admisibles=aceptados,
                salidas_tras_cambio=rechazados, pasos_T_cotejados=identidades,
                inversas_en_rango=inversas, ejemplos=ejemplos)


def cadenas(hmax, corte):
    salen, truncadas, mayor, ejemplo = 0, 0, 0, None
    for h in range(1, hmax + 1, 2):
        x, camino = h, [h]
        for _ in range(corte):
            y, a, k, carga = datos_reinicio(x)
            if y is None:
                salen += 1
                if len(camino) - 1 > mayor:
                    mayor, ejemplo = len(camino) - 1, camino
                break
            assert y > x
            x = y
            camino.append(x)
        else:
            truncadas += 1
    return dict(salen=salen, truncadas=truncadas, mayor_cadena_terminada=mayor,
                ejemplo=ejemplo, alcance='Medición finita con corte explícito; '
                        'una cadena truncada no cuenta como terminada ni como infinita.')


def cilindros(amax, bmax, qmax):
    alfabeto = list(product(range(1, amax + 1), range(1, bmax + 1)))
    historias, representantes, transiciones, pasos = 0, 0, 0, 0
    for q in range(qmax + 1):
        for historia in product(alfabeto, repeat=q):
            a_total, b_total, modulo = 1, 0, 1
            palabra = ''
            for a, b in historia:
                a_nueva, m_nuevo = 3 ** (a + 2 * b), 2 ** (a + 3 * b)
                e_nuevo = 9 ** (b - 1) * (3 ** a - 2 ** a)
                a_total, b_total, modulo = (a_nueva * a_total,
                    a_nueva * b_total + modulo * e_nuevo, modulo * m_nuevo)
                palabra += '110' + '1' * a + '110' * (b - 1)
            residuo = ((b_total + modulo) * pow(a_total, -1, 2 * modulo)) % (2 * modulo)
            assert residuo % 2 == 1
            for desplazamiento in (0, 1):
                h = residuo + desplazamiento * 2 * modulo
                y = h
                for a, b in historia:
                    yy, aa, k, carga = datos_reinicio(y)
                    assert (aa, k) == (a, 3 * b) and yy is not None
                    y = yy
                    transiciones += 1
                assert modulo * y == a_total * h - b_total
                assert recorrer_palabra(32 * h - 5, palabra) == 32 * y - 5
                representantes += 1
                pasos += len(palabra)
            historias += 1
    return dict(historias=historias, representantes=representantes,
                transiciones=transiciones, pasos_T=pasos,
                alcance='Cada historial finito admite una clase modular; no garantiza '
                        'que un natural fijo realice un historial infinito.')


def fuentes(rmax):
    ejemplos, pasos = [], 0
    for r in range(rmax + 1):
        modulo = 2 ** (4 * r + 1)
        base = pow(11, -1, modulo)
        h = base + modulo * ((3 - base) * pow(modulo, -1, 9) % 9)
        assert h % 9 == 3 and (11 * h - 1) % modulo == 0
        assert inversa(h) is None
        y = h
        for _ in range(r):
            yy, a, k, carga = datos_reinicio(y)
            assert (a, k) == (1, 3) and yy == (27 * y - 1) // 16
            y = yy
            pasos += 1
        assert recorrer_palabra(32 * h - 5, '1101' * r) == 32 * y - 5
        if r in (0, 1, 2, rmax):
            ejemplos.append(dict(reinicios=r, h=str(h), salida=str(y)))
    return dict(longitudes=rmax + 1, reinicios_cotejados=pasos, ejemplos=ejemplos,
                alcance='Longitudes arbitrarias en la prueba escrita; semillas variables. '
                        'Una fuente sin predecesor puede sobrevivir cualquier corte finito prefijado.')


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--zmax', type=int, default=4095)
    analizador.add_argument('--hmax', type=int, default=4095)
    analizador.add_argument('--corte', type=int, default=32)
    analizador.add_argument('--amax', type=int, default=3)
    analizador.add_argument('--bmax', type=int, default=3)
    analizador.add_argument('--qmax', type=int, default=3)
    analizador.add_argument('--rmax', type=int, default=16)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    assert args.zmax >= 0 and args.hmax >= 1 and args.corte >= 0
    assert args.amax >= 1 and args.bmax >= 1 and args.qmax >= 0 and args.rmax >= 0
    resultado = dict(parametros={k: v for k, v in vars(args).items() if k != 'salida'},
                     salidas=salidas(args.zmax), reinicios=reinicios(args.hmax),
                     cadenas=cadenas(args.hmax, args.corte),
                     cilindros=cilindros(args.amax, args.bmax, args.qmax),
                     fuentes=fuentes(args.rmax))
    resultado['sha256_fuente_lf'] = hashlib.sha256(
        Path(__file__).read_text(encoding='utf-8').encode('utf-8')).hexdigest()
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"OK: {resultado['salidas']['dominio']} entradas de G, "
          f"{resultado['reinicios']['entradas']} entradas de F y "
          f"{resultado['reinicios']['pasos_T_cotejados']} pasos de T cotejados; "
          f"{resultado['cadenas']['truncadas']} cadenas truncadas.")


if __name__ == '__main__':
    main()
