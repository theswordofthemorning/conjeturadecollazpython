"""Diagnóstico de la Ruta de Judas Iscariote (rama de Claude), 16-10-2026.

Mapa: atajo T(x) = x/2 si x es par y (3x+1)/2 si es impar, sobre enteros
positivos. Clase AB: prefijos de {1,110}^w, es decir, palabras que empiezan
por 11 y evitan 00 y 010. lambda(n) es el largo del mayor prefijo admitido
de las paridades de n. Bloques A=1 y B=110 con la convención de
RUTA_339 §4: A exige entrada impar, B entrada 3 mod 8; c_A=1 y c_B=5.

Secciones:
1. modelo uniforme de restos (heurística declarada, coma flotante);
2. conteo exacto c_L de palabras admitidas, contra fuerza bruta;
3. censo AB conservado: nodos más allá de B bits frente al modelo;
4. récords del censo: cambios, recargas firmadas, (R) y holgura del encaje;
5. enumeración exacta de palabras con a lo sumo m cambios y cotejo literal;
6. Siracusa: salida AB por residuos módulo 8 y transiciones entre impares;
7. colas reales: el atractor de t -> 1/3+2t/3, t -> 5/9+8t/9 es [1,5].
Las secciones 2 a 7 son exactas (enteros o Fraction). No repite censos:
la sección 3 lee el JSON existente. Implementación independiente de los
medidores de Perdices.
"""

import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
import time

CONSTANTE = {'A': 1, 'B': 5}
BITS_BLOQUE = {'A': '1', 'B': '110'}


def v2(z):
    assert z > 0
    return (z & -z).bit_length() - 1


def ell_de(n):
    """ceil(log2(n+5)) con enteros."""
    return (n + 4).bit_length()


def salida_ab_acotada(n, tope):
    """min(lambda(n), tope): posición del primer 0 no precedido por 11."""
    x, previo, antes = n, None, None
    for j in range(tope):
        e = x & 1
        if e == 0 and not (j >= 2 and previo == 1 and antes == 1):
            return j
        antes, previo = previo, e
        x = (3 * x + 1) // 2 if e else x // 2
    return tope


def salida_ab(n, tope=100_000):
    lam = salida_ab_acotada(n, tope)
    if lam == tope:
        raise RuntimeError(f'tope alcanzado sin salir: {n}')
    return lam


def paridades(n, largo):
    salida, x = [], n
    for _ in range(largo):
        e = x & 1
        salida.append(str(e))
        x = (3 * x + 1) // 2 if e else x // 2
    return ''.join(salida)


def raiz_biseccion(f, a, b, pasos=200):
    fa = f(a)
    for _ in range(pasos):
        m = (a + b) / 2
        fm = f(m)
        if (fa < 0) == (fm < 0):
            a, fa = m, fm
        else:
            b = m
    return (a + b) / 2


# 1. Modelo uniforme de restos ------------------------------------------

def modelo_uniforme(bits_censo):
    r = raiz_biseccion(lambda x: x ** 3 - x ** 2 - 1, 1.0, 2.0)
    h = math.log2(r)
    prob_a, prob_b = 1 / r, 1 / r ** 3
    largo_bloque = prob_a + 3 * prob_b
    impares_bloque = prob_a + 2 * prob_b
    return {
        'ley': 'restos uniformes módulo 2^L; bloques i.i.d. con P(A)=1/r, '
               'P(B)=1/r^3 (máxima entropía). Heurística, no teorema.',
        'r_raiz_de_x3_igual_x2_mas_1': r,
        'h_bits_por_paso': h,
        'c_igual_1_sobre_1_menos_h': 1 / (1 - h),
        'prediccion_primer_orden_bits_censo': bits_censo / (1 - h),
        'prob_A': prob_a,
        'prob_B': prob_b,
        'cambios_por_paso': 2 * prob_a * prob_b / largo_bloque,
        'crecimiento_bits_por_paso': impares_bloque / largo_bloque * math.log2(3) - 1,
    }


# 2. Conteo exacto de palabras admitidas ----------------------------------

def conteo_admitidas(lmax):
    """c_L para L>=1: composiciones de L en partes 1 y 3 (1,1,2,3,4,6,...)."""
    c = [1, 1, 1]
    while len(c) <= lmax:
        c.append(c[-1] + c[-3])
    return c


def cotejar_conteo(lmax_bruto):
    c = conteo_admitidas(lmax_bruto)
    acotadas = [0] + [salida_ab_acotada(n, lmax_bruto) for n in range(1, 1 << lmax_bruto)]
    filas, fallos = [], 0
    for largo in range(1, lmax_bruto + 1):
        cuenta = sum(1 for n in range(1, 1 << largo) if acotadas[n] >= largo)
        fallos += cuenta != c[largo]
        filas.append({'L': largo, 'fuerza_bruta': cuenta, 'c_L': c[largo]})
    return {'enunciado': '#{1<=n<2^L : lambda(n)>=L} = c_L',
            'lmax_fuerza_bruta': lmax_bruto, 'fallos': fallos, 'filas': filas}


# 3. Censo conservado frente al modelo --------------------------------------

def intervalo_maximo(c, bits):
    """Máximo de lambda bajo 2^bits según el modelo, con P(max>=L)=1-exp(-c_L 2^(bits-L))."""
    prob = {largo: 1 - math.exp(-c[largo] / 2 ** (largo - bits)) for largo in range(bits, len(c))}
    return {'bits': bits,
            'mediana': max(L for L, p in prob.items() if p >= 0.5),
            'cota_inferior_95': max(L for L, p in prob.items() if p >= 0.95),
            'cota_superior_5': max(L for L, p in prob.items() if p >= 0.05)}


def cotejar_censo(ruta, c):
    crudo = Path(ruta).read_bytes()
    datos = json.loads(crudo.decode('utf-8'))
    bits = datos['parametros']['bits']
    nodos = datos['nodos_visitados']
    hasta = sum(c[largo] for largo in range(1, bits + 1))
    mas_alla = nodos - 1 - hasta
    modelo = sum(Fraction(c[largo], 1 << (largo - bits)) for largo in range(bits + 1, len(c)))
    maximo = max(f['largo'] for f in datos['filas'])
    esperados = []
    for largo in range(maximo - 4, maximo + 3):
        e = c[largo] / 2 ** (largo - bits)
        esperados.append({'L': largo, 'esperado': e,
                          'prob_al_menos_uno_poisson': 1 - math.exp(-e)})
    return {
        'fuente': str(ruta).replace('\\', '/'),
        'sha256_fuente': hashlib.sha256(crudo).hexdigest(),
        'bits': bits,
        'nodos_visitados': nodos,
        'nodos_L_hasta_bits_exacto': hasta,
        'nodos_L_mas_alla_de_bits_censo': mas_alla,
        'nodos_L_mas_alla_de_bits_modelo': float(modelo),
        'cociente_censo_modelo': mas_alla / float(modelo),
        'maximo_lambda_censo': maximo,
        'esperados_modelo': esperados,
        'intervalos_modelo': [intervalo_maximo(c, bits), intervalo_maximo(c, bits + 10)],
        'semillas_record': sorted({int(f['minimo']) for f in datos['filas']}),
        'filas': datos['filas'],
    }


# 4. Récords: cambios, recargas y holgura ------------------------------------

def concatenacion_maxima(n, tope=100_000):
    """Mayor concatenación real de bloques desde n (RUTA_339 §4).

    En x = 3 mod 8 se toma B (A,A acabaría en par); en x = 7 mod 8 sólo
    cabe A; en x = 1 o 5 mod 8 cabe una última A y la frontera siguiente
    es par; en x par no cabe ningún bloque. Fronteras: (x, pasos, impares)."""
    x, pasos, impares = n, 0, 0
    bloques, fronteras = [], [(x, 0, 0)]
    while x % 2 == 1:
        if x % 8 == 3:
            bloques.append('B')
            x = (9 * x + 5) // 8
            pasos, impares = pasos + 3, impares + 2
        else:
            bloques.append('A')
            x = (3 * x + 1) // 2
            pasos, impares = pasos + 1, impares + 1
        fronteras.append((x, pasos, impares))
        if len(bloques) > tope:
            raise RuntimeError('tope de bloques')
    return ''.join(bloques), fronteras


def analizar_semilla(n):
    palabra, fronteras = concatenacion_maxima(n)
    largo = fronteras[-1][1]
    assert paridades(n, largo) == ''.join(BITS_BLOQUE[p] for p in palabra)
    lam = salida_ab(n)
    ell = ell_de(n)
    etas = []
    for i in range(len(palabra) - 1):
        x = fronteras[i + 1][0]
        etas.append(v2(x + CONSTANTE[palabra[i + 1]]) - v2(x + CONSTANTE[palabra[i]]))
    v_in = v2(n + CONSTANTE[palabra[0]])
    ultimo = fronteras[-1][0]
    v_fin = v2(ultimo + CONSTANTE[palabra[-1]])
    cambios = sum(1 for i in range(len(palabra) - 1) if palabra[i] != palabra[i + 1])
    # Identidad por rachas: 2^L x_L - 3^S n = suma, sobre las rachas i, de
    # c_i (3^(S-S_i) 2^(D_i) - 3^(S-S_(i+1)) 2^(D_(i+1))): 2r términos.
    impares_total = fronteras[-1][2]
    inicios = [0] + [i + 1 for i in range(len(palabra) - 1) if palabra[i] != palabra[i + 1]]
    suma_rachas = 0
    for k, j0 in enumerate(inicios):
        j1 = inicios[k + 1] if k + 1 < len(inicios) else len(palabra)
        _, d0, s0 = fronteras[j0]
        _, d1, s1 = fronteras[j1]
        suma_rachas += CONSTANTE[palabra[j0]] * (3 ** (impares_total - s0) * (1 << d0)
                                                 - 3 ** (impares_total - s1) * (1 << d1))
    identidad_rachas = (ultimo << largo) - 3 ** impares_total * n == suma_rachas
    holgura_min, valuacion_max, encaje_ok = None, 0, True
    for i, letra in enumerate(palabra):
        x, pasos, impares = fronteras[i]
        v = v2(x + CONSTANTE[letra])
        valuacion_max = max(valuacion_max, v)
        cociente = Fraction(3 ** impares * (n + 5), 1 << (pasos + v))
        encaje_ok = encaje_ok and cociente >= 1
        holgura = math.log2(cociente.numerator) - math.log2(cociente.denominator)
        holgura_min = holgura if holgura_min is None else min(holgura_min, holgura)
    return {
        'n': n, 'log2_n': math.log2(n), 'ell': ell, 'lambda': lam, 'L': largo,
        'bloques': len(palabra), 'cambios': cambios,
        'cambios_por_paso': cambios / largo,
        'v_in': v_in, 'v_fin': v_fin, 'suma_eta': sum(etas),
        'eta_max': max(etas) if etas else 0,
        'eta_max_sobre_ell': (max(etas) if etas else 0) / ell,
        'etas_al_menos_ell_medios': sum(1 for e in etas if 2 * e >= ell),
        'identidad_R': largo == v_in + sum(etas) - v_fin,
        'rachas': len(inicios),
        'identidad_por_rachas': identidad_rachas,
        'L_igual_lambda': largo == lam,
        'encaje_ok': encaje_ok,
        'valuacion_max_usada': valuacion_max,
        'holgura_min_encaje_bits': holgura_min,
    }


def analizar_records(semillas, largo_min):
    filas = []
    for n in semillas:
        fila = analizar_semilla(n)
        if fila['lambda'] >= largo_min:
            filas.append(fila)
    resumen = {
        'largo_min': largo_min,
        'semillas': len(filas),
        'cambios_min': min(f['cambios'] for f in filas),
        'cambios_max': max(f['cambios'] for f in filas),
        'cambios_por_paso_min': min(f['cambios_por_paso'] for f in filas),
        'cambios_por_paso_max': max(f['cambios_por_paso'] for f in filas),
        'cambios_por_paso_media': sum(f['cambios_por_paso'] for f in filas) / len(filas),
        'eta_max': max(f['eta_max'] for f in filas),
        'eta_max_sobre_ell_max': max(f['eta_max_sobre_ell'] for f in filas),
        'etas_al_menos_ell_medios': sum(f['etas_al_menos_ell_medios'] for f in filas),
        'identidad_R_todas': all(f['identidad_R'] for f in filas),
        'identidad_por_rachas_todas': all(f['identidad_por_rachas'] for f in filas),
        'L_igual_lambda_todas': all(f['L_igual_lambda'] for f in filas),
        'encaje_ok_todas': all(f['encaje_ok'] for f in filas),
        'valuacion_max_usada': max(f['valuacion_max_usada'] for f in filas),
        'holgura_min_encaje_bits': min(f['holgura_min_encaje_bits'] for f in filas),
    }
    return {'resumen': resumen, 'filas': filas}


def holguras_testigo():
    """Holgura, en bits, de los cuatro encajes (7) de TRES_CAMBIOS §5 (ell=1000)."""
    ell, filas = 1000, []
    for exponente, impares in ((1003, 2), (2584, 1000), (4254, 2054), (6855, 3724)):
        cociente = Fraction(3 ** impares << ell, 1 << exponente)
        filas.append({'D_mas_v': exponente, 'S': impares, 'cumple': cociente >= 1,
                      'holgura_bits': math.log2(cociente.numerator) - math.log2(cociente.denominator)})
    return filas


# 5. Pocos cambios: enumeración exacta ---------------------------------------

def decodificar_bloques(cadena):
    """Palabra de bloques de una cadena admitida completa: cada 0 cierra un B."""
    palabra, j = [], 0
    while j < len(cadena):
        if cadena[j:j + 3] == '110':
            palabra.append('B')
            j += 3
        elif cadena[j] == '1' and not (cadena[j:j + 2] == '10'):
            palabra.append('A')
            j += 1
        else:
            return None
    return ''.join(palabra)


def minimos_pocos_cambios(m_max, largo0):
    """Menor semilla de una concatenación real (RUTA_339 §4: A sólo exige
    entrada impar) que cruza largo0 con <= m cambios. Una cola AA puede ser
    en la órbita el comienzo de un B: la palabra cuenta igual, porque sus
    paridades coinciden con las reales."""
    exacto = {}
    pila = [(1, 1, 1, 'A', 0), (3, 2, 5, 'B', 0)]
    hojas = 0
    while pila:
        largo, impares, bk, ultima, m = pila.pop()
        if largo >= largo0:
            hojas += 1
            modulo = 1 << largo
            r = (-bk * pow(3, -impares, modulo)) % modulo or modulo
            if m not in exacto or r < exacto[m][0]:
                exacto[m] = (r, largo)
            continue
        for letra in 'AB':
            m2 = m + (letra != ultima)
            if m2 > m_max:
                continue
            if letra == 'A':
                pila.append((largo + 1, impares + 1, 3 * bk + (1 << largo), 'A', m2))
            else:
                pila.append((largo + 3, impares + 2, 9 * bk + 5 * (1 << largo), 'B', m2))
    filas = []
    for m in range(m_max + 1):
        semilla, largo = min(v for k, v in exacto.items() if k <= m)
        lam = salida_ab(semilla)
        # Cotejo literal: las primeras 'largo' paridades de la semilla se
        # descomponen en bloques con <= m cambios.
        palabra = decodificar_bloques(paridades(semilla, largo))
        cambios = None if palabra is None else sum(
            1 for i in range(len(palabra) - 1) if palabra[i] != palabra[i + 1])
        literal_ok = palabra is not None and cambios <= m and lam >= largo >= largo0
        filas.append({'cambios_max': m, 'semilla': str(semilla),
                      'log2_semilla': math.log2(semilla), 'largo_palabra': largo,
                      'lambda': lam, 'cambios_literales': cambios,
                      'cotejo_literal': literal_ok})
    return {'largo0': largo0, 'hojas': hojas, 'filas': filas}


def primera_semilla_bruta(m, largo0):
    """Menor n con un prefijo de bloques completos que cruza largo0 con <= m
    cambios, recorriendo semillas en orden: implementación independiente."""
    n = 0
    while True:
        n += 1
        for largo in (largo0, largo0 + 1, largo0 + 2):
            palabra = decodificar_bloques(paridades(n, largo))
            if palabra is None:
                continue
            if largo - (1 if palabra[-1] == 'A' else 3) >= largo0:
                continue
            if sum(1 for i in range(len(palabra) - 1) if palabra[i] != palabra[i + 1]) <= m:
                return n


def cotejar_minimalidad(largos, m_max):
    filas = []
    for largo0 in largos:
        enumeradas = minimos_pocos_cambios(m_max, largo0)['filas']
        for m in range(m_max + 1):
            bruta = primera_semilla_bruta(m, largo0)
            filas.append({'largo0': largo0, 'cambios_max': m, 'enumeracion': int(enumeradas[m]['semilla']),
                          'fuerza_bruta': bruta, 'coincide': bruta == int(enumeradas[m]['semilla'])})
    return filas


# 6. Siracusa -------------------------------------------------------------

def salida_siracusa(n):
    """lambda(n) leída en la órbita impar de n impar: nu=1 si y=3,7 mod 8;
    nu=2 si y=1 mod 8; nu>=3 si y=5 mod 8. Se sale al primer nu>=3, al
    primer nu=2 tras otro nu=2, o si el primer impar tiene nu>=2."""
    y, p, previo_dos, primero = n, 0, False, True
    while True:
        r = y % 8
        if r in (3, 7):
            y = (3 * y + 1) // 2
            p += 1
            previo_dos = False
        elif r == 1:
            if primero or previo_dos:
                return p + 1
            y = (3 * y + 1) // 4
            p += 2
            previo_dos = True
        else:
            if primero or previo_dos:
                return p + 1
            return p + 2
        primero = False


def cotejar_siracusa(n_max, bits_tabla):
    discrepancias, ejemplos, revisadas = 0, [], 0
    for n in range(1, n_max + 1, 2):
        revisadas += 1
        a, b = salida_ab(n), salida_siracusa(n)
        if a != b:
            discrepancias += 1
            if len(ejemplos) < 5:
                ejemplos.append([n, a, b])
    tabla = {}
    for y in range(1, 1 << bits_tabla, 2):
        z = 3 * y + 1
        nu = v2(z)
        entrada = tabla.setdefault(y % 8, (set(), set()))
        entrada[0].add(min(nu, 3))
        entrada[1].add((z >> nu) % 8)
    transiciones = {str(k): {'nu (3 = nu>=3)': sorted(v[0]), 'siguiente_impar_mod8': sorted(v[1])}
                    for k, v in sorted(tabla.items())}
    return {'semillas_impares': revisadas, 'discrepancias': discrepancias,
            'ejemplos': ejemplos, 'bits_tabla': bits_tabla, 'transiciones': transiciones}


# 7. Colas reales -------------------------------------------------------------

def colas_ab(max_bloques):
    uno, cinco = Fraction(1), Fraction(5)
    afin = {'A': (Fraction(2, 3), Fraction(1, 3)), 'B': (Fraction(8, 9), Fraction(5, 9))}
    imagen_a = [afin['A'][0] * t + afin['A'][1] for t in (uno, cinco)]
    imagen_b = [afin['B'][0] * t + afin['B'][1] for t in (uno, cinco)]
    cubre = imagen_a[0] == uno and imagen_b[1] == cinco and imagen_b[0] <= imagen_a[1]
    revisadas, fallos, minimo, maximo = 0, 0, None, None
    for largo in range(1, max_bloques + 1):
        for k in range(1 << largo):
            palabra = ''.join('B' if (k >> i) & 1 else 'A' for i in range(largo))
            a, b = Fraction(1), Fraction(0)
            for letra in reversed(palabra):
                alfa, beta = afin[letra]
                a, b = alfa * a, alfa * b + beta
            cola = b / (1 - a)
            minimo = cola if minimo is None else min(minimo, cola)
            maximo = cola if maximo is None else max(maximo, cola)
            # -cola debe ser un ciclo de T con esas paridades (q impar).
            x = -cola
            cadena = ''.join(BITS_BLOQUE[p] for p in palabra)
            ok = x.denominator % 2 == 1
            for bit in cadena:
                e = x.numerator % 2
                ok = ok and str(e) == bit
                x = (3 * x + 1) / 2 if e else x / 2
            ok = ok and x == -cola and uno <= cola <= cinco
            revisadas += 1
            fallos += not ok
    return {
        'imagen_A_de_[1,5]': [str(v) for v in imagen_a],
        'imagen_B_de_[1,5]': [str(v) for v in imagen_b],
        'las_imagenes_cubren_[1,5]': cubre,
        'palabras_periodicas_revisadas': revisadas,
        'fallos_ciclo_o_rango': fallos,
        'cola_min': str(minimo), 'cola_max': str(maximo),
    }


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--censo', type=Path, required=True)
    analizador.add_argument('--largo-records', type=int, default=40)
    analizador.add_argument('--conteo', type=int, default=18)
    analizador.add_argument('--cambios', type=int, default=3)
    analizador.add_argument('--largo', type=int, default=110)
    analizador.add_argument('--siracusa', type=int, default=400_000)
    analizador.add_argument('--bits-tabla', type=int, default=14)
    analizador.add_argument('--bloques-colas', type=int, default=6)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    inicio = time.time()
    c = conteo_admitidas(700)
    censo = cotejar_censo(args.censo, c)
    resultado = {
        'fecha': '16-10-2026',
        'parametros': {k: (str(v).replace('\\', '/') if isinstance(v, Path) else v)
                       for k, v in vars(args).items()},
        'modelo_uniforme': modelo_uniforme(censo['bits']),
        'conteo_exacto': cotejar_conteo(args.conteo),
        'censo': {k: v for k, v in censo.items() if k not in ('filas', 'semillas_record')},
        'records': analizar_records(censo['semillas_record'], args.largo_records),
        'testigo_tres_cambios': holguras_testigo(),
        'pocos_cambios': minimos_pocos_cambios(args.cambios, args.largo),
        'cotejo_minimalidad': cotejar_minimalidad((8, 12, 16, 20), args.cambios),
        'siracusa': cotejar_siracusa(args.siracusa, args.bits_tabla),
        'colas': colas_ab(args.bloques_colas),
    }
    resultado['segundos'] = round(time.time() - inicio, 1)
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=1) + '\n',
                           encoding='utf-8')
    m = resultado['modelo_uniforme']
    print(f"modelo: r={m['r_raiz_de_x3_igual_x2_mas_1']:.6f} h={m['h_bits_por_paso']:.5f} "
          f"c={m['c_igual_1_sobre_1_menos_h']:.4f} cambios/paso={m['cambios_por_paso']:.4f} "
          f"crecimiento={m['crecimiento_bits_por_paso']:.4f}")
    ce = resultado['conteo_exacto']
    print(f"conteo exacto hasta L={ce['lmax_fuerza_bruta']}: fallos={ce['fallos']}")
    cs = resultado['censo']
    print(f"censo: más allá de {cs['bits']} bits {cs['nodos_L_mas_alla_de_bits_censo']} nodos; "
          f"modelo {cs['nodos_L_mas_alla_de_bits_modelo']:.1f}; cociente {cs['cociente_censo_modelo']:.6f}")
    for e in cs['esperados_modelo']:
        print(f"  L={e['L']}: esperado {e['esperado']:.4f}, P>=1 {e['prob_al_menos_uno_poisson']:.3f}")
    print('  intervalos del máximo:', json.dumps(cs['intervalos_modelo'], ensure_ascii=False))
    print('récords:', json.dumps(resultado['records']['resumen'], ensure_ascii=False))
    for f in resultado['records']['filas'][-4:]:
        print(f"  n={f['n']} ell={f['ell']} L={f['L']} cambios={f['cambios']} v_in={f['v_in']} "
              f"v_fin={f['v_fin']} suma_eta={f['suma_eta']} eta_max={f['eta_max']} "
              f"val_max={f['valuacion_max_usada']} holgura_min={f['holgura_min_encaje_bits']:.2f}")
    print('testigo §5, holguras:', [round(f['holgura_bits'], 2) for f in resultado['testigo_tres_cambios']])
    for f in resultado['pocos_cambios']['filas']:
        print(f"pocos cambios <= {f['cambios_max']}: log2 semilla {f['log2_semilla']:.2f} "
              f"lambda {f['lambda']} cotejo {f['cotejo_literal']}")
    cm = resultado['cotejo_minimalidad']
    print(f"minimalidad por fuerza bruta: {sum(f['coincide'] for f in cm)}/{len(cm)} coinciden")
    s = resultado['siracusa']
    print(f"siracusa: {s['semillas_impares']} impares, discrepancias {s['discrepancias']}")
    print('transiciones:', json.dumps(s['transiciones'], ensure_ascii=False))
    print('colas:', json.dumps(resultado['colas'], ensure_ascii=False))
    print(f"segundos: {resultado['segundos']}")


if __name__ == '__main__':
    main()
