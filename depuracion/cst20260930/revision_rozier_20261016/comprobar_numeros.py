"""Comprobaciones exactas para la respuesta a Rozier, sin importar generadores.

No comprueba la cobertura de Roosendaal hasta el record. Comprueba las
trayectorias publicadas, las constantes del argumento RT y los margenes
de las dos colas. Las aproximaciones decimales son solo de presentacion.
"""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def logaritmo(x, terminos=180):
    y = (x - 1) / (x + 1)
    suma = Fraction(0)
    potencia = y
    for i in range(terminos):
        suma += potencia / (2 * i + 1)
        potencia *= y * y
    resto = potencia / ((2 * terminos + 1) * (1 - y * y))
    return 2 * suma, 2 * (suma + resto)


def clasica(n):
    pasos = 0
    while n != 1:
        n = 3 * n + 1 if n % 2 else n // 2
        pasos += 1
        assert pasos <= 100000
    return pasos


def atajo(n):
    pasos = impares = 0
    while n != 1:
        impar = n % 2
        n = (3 * n + 1) // 2 if impar else n // 2
        pasos += 1
        impares += impar
        assert pasos <= 100000
    return pasos, impares


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--fuentes', type=Path, required=True)
    ap.add_argument('--carpeta', type=Path, required=True)
    ap.add_argument('--salida', type=Path, required=True)
    args = ap.parse_args()
    registros = []
    lineas = (args.fuentes / 'roosendaal_delays.txt').read_text().splitlines()
    for linea in lineas:
        if not linea.strip():
            continue
        n = int(linea.replace(',', ''))
        d = clasica(n)
        t, q = atajo(n)
        assert d == t + q
        if registros:
            assert n > registros[-1]['n'] and d > registros[-1]['clasico']
        registros.append(dict(n=n, clasico=d, atajo=t, impares=q))
    assert registros[-1]['n'] == 46645791847966786687
    assert registros[-1]['clasico'] == 2480

    # Censo pequeno independiente de maximos de T, con memorizacion exacta.
    maximos = {1: 1}
    anteriores = 0
    for n in range(2, 113384):
        x, camino = n, []
        while x not in maximos:
            camino.append(x)
            x = (3 * x + 1) // 2 if x % 2 else x // 2
        m = maximos[x]
        for x in reversed(camino):
            m = max(m, x)
            maximos[x] = m
        if n < 113383:
            anteriores = max(anteriores, maximos[n])
    assert anteriores < 10 ** 9 <= maximos[113383]

    # H(j)>=m equivale a (3m+1)^q >= 2^j*m^q, q=floor(j*log2/log3).
    m = 113383
    q = 0
    candidatos = []
    for j in range(2, 1540):
        while 3 ** (q + 1) < 2 ** j:
            q += 1
        assert 3 ** q < 2 ** j < 3 ** (q + 1)
        if (3 * m + 1) ** q >= 2 ** j * m ** q:
            candidatos.append((j, q))
    assert candidatos == [(1539, 971)]
    assert (3 * m + 1) ** 970 < 2 ** 1539 * m ** 970
    assert (3 * m + 1) ** 971 >= 2 ** 1539 * m ** 971
    assert 1539 + 971 == 2510 > 2480

    # Puente propio: una pareja unimodular controla todos q<2966.
    l2 = logaritmo(Fraction(2))
    l3 = logaritmo(Fraction(3))
    assert 3647 * 665 - 1054 * 2301 == 1
    assert 3647 * l2[0] - 2301 * l3[1] > Fraction(1, 1200)
    assert 1054 * l2[1] - 665 * l3[0] < 0
    assert 2480 * 1200 == 2976000 < 4912741

    colas = []
    for r in [81, 82, 83, 84]:
        a = -((-5 * (8 ** r - 5 ** r)) // (3 * 5 ** r))
        def margen_lmn(h):
            return 5 * 2 ** h - 8 * a * (19 * (h + 33) ** 2 + 8) - 5
        def margen_rhin(h):
            return 5 * 2 ** h - 8 * a * (14 * (h + 1) + 8) - 5
        hl = next(h for h in range(1, 150) if margen_lmn(h) > 0)
        hr = next(h for h in range(1, 150) if margen_rhin(h) > 0)
        colas.append(dict(rachas=r, A=a, H_LMN=hl, H_Rhin=hr,
                          margen_LMN=margen_lmn(hl), margen_Rhin=margen_rhin(hr)))

    ventanas = []
    for r in [82, 84]:
        d = json.loads((args.carpeta / f'pesos_{r}_diagnostico.json').read_text())
        fallos = [f for f in d['filas'] if f['remite'] == 'falla']
        assert len(fallos) == 1
        f = fallos[0]
        c = Fraction(f['lambda_inferior'])
        # Para k>q>=q_inicio, Rhin k^-13.3 <=q_inicio^-13 < c.
        assert c * f['q_inicio'] ** 13 > 1
        hr = next(v['H_Rhin'] for v in colas if v['rachas'] == r)
        k_maximo = (8 * (f['q_fin'] - 1) + 5) // 5
        assert k_maximo < 2 ** hr
        ventana = dict(rachas=r, q_inicio=f['q_inicio'], q_fin=f['q_fin'],
                       semilla=f['pieza_fallida'], c=str(c),
                       rhin_menor_cota_finita=True, k_maximo=k_maximo,
                       ventana_anterior_a_cola_rhin=True)
        ventanas.append(ventana)

    salida = dict(estado='comprobaciones exactas aceptadas; cobertura externa no reproducida',
                  sha256_guion=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  registros_comprobados=len(registros), ultimos_registros=registros[-3:],
                  maximo_anterior_a_113383=anteriores, maximo_113383=maximos[113383],
                  RT=dict(j_min=1539, q_min=971, delay_min=2510),
                  puente_propio=dict(q_max=2480, c='1/1200', semilla_menor=2976000,
                                     certificado_Lean_hasta=4912740),
                  colas=colas, ventanas=ventanas)
    args.salida.write_text(json.dumps(salida, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(salida, indent=2))


if __name__ == '__main__':
    main()
