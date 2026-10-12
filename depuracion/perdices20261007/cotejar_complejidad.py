"""Repeticiones, representantes y complejidad: cotejo con enteros exactos.

Mapa: atajo T(x) = x/2 si x es par y (3x+q)/2 si es impar; q = 1 salvo en
la sección racional. Índices en pasos de T. No hay ley aleatoria: todo
lo que sigue son cuentas exactas sobre órbitas y palabras finitas.
"""

import argparse
from fractions import Fraction
import hashlib
from itertools import combinations
import json
from math import isqrt
from pathlib import Path


def paso(x, q=1):
    return (3 * x + q) // 2 if x % 2 else x // 2


def orbita(n, pasos, q=1):
    xs = [n]
    for _ in range(pasos):
        xs.append(paso(xs[-1], q))
    return xs


def impares_acumulados(xs):
    s = [0]
    for x in xs:
        s.append(s[-1] + x % 2)
    return s


def extension_comun(bits, i, j):
    m = 0
    while j + m < len(bits) and bits[i + m] == bits[j + m]:
        m += 1
    return m


def leyes(nmax, pasos):
    """Ley local, global y expansiva en todas las repeticiones de las órbitas."""
    casos = expansivos = ciclicos = fallos_en_ciclo = 0
    peor_local = Fraction(0)
    peor_global = Fraction(0)
    donde_local = donde_global = None
    for n in range(nmax + 1):
        xs = orbita(n, pasos)
        bits = [x % 2 for x in xs[:pasos]]
        s = impares_acumulados(xs[:pasos])
        for i, j in combinations(range(pasos), 2):
            m = extension_comun(bits, i, j)
            # Congruencia: misma paridad en m pasos implica misma clase módulo 2^m.
            assert (xs[i] - xs[j]) % 2 ** m == 0, (n, i, j, m)
            d = j - i
            impares = s[j] - s[i]
            if xs[i] == xs[j]:
                ciclicos += 1
                if 2 ** (m + impares) >= 3 ** impares * (xs[i] + 1):
                    fallos_en_ciclo += 1
                # Un tramo que cierra un ciclo natural positivo es contractivo.
                if xs[i] >= 1:
                    assert 3 ** impares < 2 ** d, (n, i, j)
                continue
            casos += 1
            izquierda = 2 ** (m + impares)
            derecha = 3 ** impares * (xs[i] + 1)
            assert izquierda < derecha, ('local', n, i, j, m)
            cociente = Fraction(izquierda, derecha)
            if cociente > peor_local:
                peor_local, donde_local = cociente, dict(n=n, i=i, j=j, m=m, s=impares)
            global_izq = 2 ** (m + s[j])
            global_der = 3 ** s[j] * (n + 1)
            assert global_izq < global_der, ('global', n, i, j, m)
            cociente = Fraction(global_izq, global_der)
            if cociente > peor_global:
                peor_global, donde_global = cociente, dict(n=n, i=i, j=j, m=m, S_j=s[j])
            if 2 ** d <= 3 ** impares:
                expansivos += 1
    return dict(semillas=nmax + 1, corte=pasos, repeticiones_con_valores_distintos=casos,
                con_tramo_expansivo=expansivos, repeticiones_ciclicas=ciclicos,
                ciclicas_que_violan_la_cota=fallos_en_ciclo,
                peor_cociente_local=str(peor_local), peor_local_en=donde_local,
                peor_cociente_global=str(peor_global), peor_global_en=donde_global,
                alcance='Toda repetición con valores distintos cumple ambas cotas. Las '
                        'repeticiones cíclicas (valores iguales) quedan fuera de la hipótesis '
                        'y pueden violar la cota: la hipótesis es necesaria.')


def identidad_residuos(nmax, mmax, kmax):
    """Dos instantes tienen el mismo factor de largo m si y sólo si son congruentes."""
    comparaciones = 0
    for n in range(nmax + 1):
        xs = orbita(n, kmax + mmax)
        for m in range(mmax + 1):
            factores = [tuple(x % 2 for x in xs[t:t + m]) for t in range(kmax)]
            residuos = [xs[t] % 2 ** m for t in range(kmax)]
            for t, u in combinations(range(kmax), 2):
                assert (factores[t] == factores[u]) == (residuos[t] == residuos[u]), (n, m, t, u)
                comparaciones += 1
            assert len(set(factores)) == len(set(residuos))
    return dict(semillas=nmax + 1, largo_maximo=mmax, instantes=kmax, comparaciones=comparaciones)


def iniciales(nmax, mmax):
    """Umbral 3^K (n+1) <= 2^(m+K): valores bajo 2^m y factores distintos si los valores lo son."""
    revisados = repetidos = 0
    for n in range(nmax + 1):
        for m in range(1, mmax + 1):
            k = -1
            while 3 ** (k + 1) * (n + 1) <= 2 ** (m + k + 1):
                k += 1
            if k < 0:
                continue
            xs = orbita(n, k + m)
            for t in range(k + 1):
                assert xs[t] < 2 ** m, (n, m, t)
            valores = xs[:k + 1]
            factores = [tuple(x % 2 for x in xs[t:t + m]) for t in range(k + 1)]
            if len(set(valores)) == k + 1:
                assert len(set(factores)) == k + 1, (n, m)
                revisados += 1
            else:
                repetidos += 1
    bernoulli = all(3 ** m * (3 + m) <= 3 * 4 ** m for m in range(401))
    umbral = all(3 ** (m + 1) * (n + 1) <= 2 ** (2 * m + 1)
                 for n in range(nmax + 1) for m in range(5 * (n + 1), 5 * (n + 1) + 64))
    assert bernoulli and umbral
    return dict(pares_semilla_largo=revisados, con_valores_repetidos_antes_del_umbral=repetidos,
                bernoulli_hasta=400, umbral_explicito_comprobado=True)


def piso_cuadratico(a, b, radicando, c):
    """floor((a + b*sqrt(radicando))/c) para b >= 0, c > 0 y radicando no cuadrado."""
    assert b >= 0 and c > 0 and isqrt(radicando) ** 2 != radicando
    return (a + isqrt(b * b * radicando)) // c


def palabra_mecanica(pendiente, intercepto, largo):
    """Bits floor((k+1)alpha+rho) - floor(k alpha+rho), alpha=(a+b sqrt D)/c, rho=e/f."""
    a, b, radicando, c = pendiente
    e, f = intercepto
    pisos = [piso_cuadratico(k * a * f + e * c, k * b * f, radicando, c * f)
             for k in range(largo + 1)]
    return [pisos[k + 1] - pisos[k] for k in range(largo)]


def representantes_minimos(bits):
    """r_l: menor natural cuyos l primeros bits de paridad son bits[:l] (biyección)."""
    r, y, impares = 0, 0, 0
    salida = [0]
    for k, bit in enumerate(bits):
        if y % 2 != bit:
            r += 2 ** k
            y += 3 ** impares
        y = (3 * y + 1) // 2 if bit else y // 2
        impares += bit
        salida.append(r)
    return salida


def thue_morse_ab(kmax):
    """Thue-Morse sobre A=1, B=110: prefijo mu^k(011) = U V V con |U|=|V| en paridades."""
    tm = [0]
    while len(tm) < 3 * 2 ** kmax:
        tm = tm + [1 - b for b in tm]
    bits = []
    for b in tm[:3 * 2 ** kmax]:
        bits.extend([1] if b == 0 else [1, 1, 0])
    reps = representantes_minimos(bits)
    filas = []
    for k in range(1, kmax + 1):
        largo_v = 2 ** (k + 1)                      # |code(mu^k(0))| = |code(mu^k(1))|
        largo = 3 * largo_v
        assert bits[largo_v:2 * largo_v] == bits[2 * largo_v:3 * largo_v]
        r = reps[largo]
        xs = orbita(r, largo)
        s = impares_acumulados(xs[:largo])
        j, m = 2 * largo_v, largo_v
        assert s[j] == 3 * 2 ** k and xs[largo_v] != xs[j]
        # Ley global con la repetición (i, j, m) = (|U|, |UV|, |V|).
        assert 2 ** (m + s[j]) < 3 ** s[j] * (r + 1)
        cota = Fraction(2 ** (m + s[j]), 3 ** s[j])
        filas.append(dict(k=k, largo=largo, bits_representante=r.bit_length(),
                          bits_cota=(cota.numerator // cota.denominator).bit_length()))
    return filas


def complejidad(bits, m):
    return len({tuple(bits[t:t + m]) for t in range(len(bits) - m + 1)})


def sturmianas(largo, cortes):
    pendientes = {
        'sqrt2-1/2': (-1, 2, 2, 2),        # 0,9142...
        '(sqrt5-4/5)/2': (-4, 5, 5, 10),   # 0,7180...
        'sqrt3-1': (-1, 1, 3, 1),          # 0,7320...
        '(sqrt5+1)/4': (1, 1, 5, 4),       # 0,8090...
        '(sqrt5-1)/2': (-1, 1, 5, 2),      # 0,6180..., contractiva
    }
    interceptos = {'0': (0, 1), '1/3': (1, 3)}
    resultado = []
    for nombre, pendiente in pendientes.items():
        for nombre_i, intercepto in interceptos.items():
            bits = palabra_mecanica(pendiente, intercepto, largo)
            for m in range(1, 13):
                assert complejidad(bits, m) == m + 1, (nombre, nombre_i, m)
            reps = representantes_minimos(bits)
            for l in range(largo + 1):
                xs = orbita(reps[l], l)
                assert [x % 2 for x in xs[:l]] == bits[:l]
                assert reps[l] < 2 ** l or l == 0
            # Extensión común de los sufijos i<j de la palabra completa, por programación dinámica.
            lce = [[0] * (largo + 1) for _ in range(largo + 1)]
            for i in range(largo - 1, -1, -1):
                for j in range(largo - 1, i, -1):
                    if bits[i] == bits[j]:
                        lce[i][j] = lce[i + 1][j + 1] + 1
            filas = []
            for l in cortes:
                if l > largo:
                    continue
                xs = orbita(reps[l], l)
                s = impares_acumulados(xs[:l])
                mejor = Fraction(0)
                for j in range(1, l):
                    for i in range(j):
                        m = min(lce[i][j], l - j)
                        if m == 0 or xs[i] == xs[j]:
                            continue
                        cota = Fraction(2 ** (m + s[j]), 3 ** s[j])
                        # Ley global sobre el representante mínimo: r + 1 > cota.
                        assert reps[l] + 1 > cota, (nombre, l, i, j)
                        mejor = max(mejor, cota)
                filas.append(dict(largo=l, bits_representante=reps[l].bit_length(),
                                  bits_cota=(mejor.numerator // mejor.denominator).bit_length()
                                  if mejor >= 1 else 0))
            resultado.append(dict(pendiente=nombre, intercepto=nombre_i, filas=filas))
    return resultado


def lenguaje_ab(prefijo_ultimos, bit, largo_actual):
    """Prefijos de {1,110}^w: empiezan por 11 y evitan 00 y 010."""
    a, b = prefijo_ultimos
    if largo_actual == 0:
        return bit == 1
    if largo_actual == 1:
        return bit == 1
    if b == 0 and bit == 0:
        return False
    if a == 0 and b == 1 and bit == 0:
        return False
    return True


def minimo_uniforme_ab(lmax, cota_bits):
    """Menor natural que sigue algún prefijo de largo L de {1,110}^w, por niveles."""
    cota = 2 ** cota_bits
    # Estado: (representante r < 2^k, y = T^k(r), impares, dos últimos bits).
    nivel = [(0, 0, 0, (1, 1))]
    filas = []
    maximo_estados = 1
    for k in range(lmax):
        siguiente = []
        for r, y, impares, ultimos in nivel:
            for ajuste in (0, 1):
                rr, yy = (r, y) if ajuste == 0 else (r + 2 ** k, y + 3 ** impares)
                if rr >= cota:
                    continue
                bit = yy % 2
                if not lenguaje_ab(ultimos, bit, k):
                    continue
                nuevo_y = (3 * yy + 1) // 2 if bit else yy // 2
                siguiente.append((rr, nuevo_y, impares + bit, (ultimos[1], bit)))
        nivel = siguiente
        maximo_estados = max(maximo_estados, len(nivel))
        largo = k + 1
        if not nivel:
            filas.append(dict(largo=largo, minimo=None, nota=f'mayor o igual que 2^{cota_bits}'))
            break
        minimo = min(r for r, _, _, _ in nivel)
        filas.append(dict(largo=largo, minimo=str(minimo), bits=minimo.bit_length(),
                          clases_bajo_la_cota=len(nivel)))
    return filas, maximo_estados


def sigue_ab(x, largo):
    bits = []
    for _ in range(largo):
        bits.append(x % 2)
        x = paso(x)
    ultimos = (1, 1)
    for k, bit in enumerate(bits):
        if not lenguaje_ab(ultimos, bit, k):
            return False
        ultimos = (ultimos[1], bit)
    return True


def cotejo_fuerza_bruta_ab(filas, lmax_bruto):
    """Implementación independiente: recorrer naturales hasta el primero que sigue AB."""
    comprobados = 0
    for fila in filas:
        if fila['largo'] > lmax_bruto or fila['minimo'] is None:
            continue
        objetivo = int(fila['minimo'])
        x = 1
        while not sigue_ab(x, fila['largo']):
            x += 1
        assert x == objetivo, (fila, x)
        comprobados += 1
    return comprobados


def lambda_ab(n):
    """Mayor L tal que las L primeras paridades de n son prefijo de {1,110}^w."""
    x, ultimos, k = n, (1, 1), 0
    while True:
        bit = x % 2
        if not lenguaje_ab(ultimos, bit, k):
            return k
        ultimos, x, k = (ultimos[1], bit), paso(x), k + 1


def records_ab(filas):
    """Cota 3 log2(n)+1 sobre la tabla exacta y parte explicada por la ley en cada récord."""
    for fila in filas:
        if fila['minimo'] is not None:
            # lambda(n) >= L implica n >= minimo(L); se exige minimo^3 >= 2^(L-1).
            assert int(fila['minimo']) ** 3 >= 2 ** (fila['largo'] - 1), fila
    minimos = sorted({int(f['minimo']) for f in filas if f['minimo'] is not None})
    salida = []
    for n in minimos:
        largo = lambda_ab(n)
        xs = orbita(n, largo)
        bits = [x % 2 for x in xs[:largo]]
        s = impares_acumulados(xs[:largo])
        mejor = Fraction(0)
        for i, j in combinations(range(largo), 2):
            m = extension_comun(bits, i, j)
            if m and xs[i] != xs[j]:
                mejor = max(mejor, Fraction(2 ** (m + s[j]), 3 ** s[j]))
        assert n + 1 > mejor
        salida.append(dict(semilla=str(n), bits=n.bit_length(), lambda_=largo,
                           bits_explicados_por_la_ley=(mejor.numerator // mejor.denominator).bit_length()
                           if mejor >= 1 else 0))
    return salida


def racionales(pmax, qmax, pasos):
    """Mapa 3x+q (q impar): misma ley con |x|+q; cubre p/q en Z_(2)."""
    casos = 0
    peor = Fraction(0)
    for q in range(1, qmax + 1, 2):
        for p in range(-pmax, pmax + 1):
            xs = orbita(p, pasos, q)
            bits = [x % 2 for x in xs[:pasos]]
            s = impares_acumulados(xs[:pasos])
            for i, j in combinations(range(pasos), 2):
                m = extension_comun(bits, i, j)
                assert (xs[i] - xs[j]) % 2 ** m == 0
                if xs[i] == xs[j] or m == 0:
                    continue
                impares = s[j] - s[i]
                izquierda = 2 ** (m + impares)
                derecha = 3 ** impares * (abs(xs[i]) + q)
                assert izquierda < derecha, ('racional local', p, q, i, j)
                assert 2 ** (m + s[j]) < 3 ** s[j] * (abs(p) + q), ('racional global', p, q, i, j)
                casos += 1
                peor = max(peor, Fraction(izquierda, derecha))
    return dict(numeradores=2 * pmax + 1, denominadores_impares_hasta=qmax, corte=pasos,
                repeticiones=casos, peor_cociente_local=str(peor))


def familia_ajustada(lmax):
    """n = 2^L - 1: la cota local con i=0, j=1, m=L-1 se cumple con cociente exacto 1/3."""
    for largo in range(2, lmax + 1):
        n = 2 ** largo - 1
        xs = orbita(n, largo + 1)
        bits = [x % 2 for x in xs]
        m = extension_comun(bits[:largo + 1], 0, 1)
        assert m == largo - 1 and xs[0] != xs[1]
        assert Fraction(2 ** (m + 1), 3 * (n + 1)) == Fraction(1, 3)
    return dict(largos=f'2..{lmax}', cociente_local='1/3')


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('--nmax', type=int, default=255)
    analizador.add_argument('--pasos', type=int, default=48)
    analizador.add_argument('--mmax', type=int, default=8)
    analizador.add_argument('--kmax', type=int, default=24)
    analizador.add_argument('--largo-sturm', type=int, default=400)
    analizador.add_argument('--lmax-ab', type=int, default=90)
    analizador.add_argument('--cota-bits-ab', type=int, default=34)
    analizador.add_argument('--lmax-bruto', type=int, default=30)
    analizador.add_argument('--pmax', type=int, default=64)
    analizador.add_argument('--qmax', type=int, default=9)
    analizador.add_argument('--salida', type=Path, required=True)
    args = analizador.parse_args()
    assert args.nmax >= 0 and args.pasos >= 2 and args.mmax >= 0 and args.kmax >= 2
    assert args.largo_sturm >= 16 and 1 <= args.cota_bits_ab <= 40 and args.qmax >= 1
    cortes = [l for l in (16, 32, 64, 128, 256, 400, 800) if l <= args.largo_sturm]
    filas_ab, estados = minimo_uniforme_ab(args.lmax_ab, args.cota_bits_ab)
    resultado = dict(
        parametros={k: v for k, v in vars(args).items() if k != 'salida'},
        leyes=leyes(args.nmax, args.pasos),
        identidad_residuos=identidad_residuos(min(args.nmax, 127), args.mmax, args.kmax),
        umbral_inicial=iniciales(min(args.nmax, 63), 24),
        sturmianas=sturmianas(args.largo_sturm, cortes),
        thue_morse_ab=thue_morse_ab(8),
        racionales=racionales(args.pmax, args.qmax, min(args.pasos, 40)),
        familia_ajustada=familia_ajustada(64),
        minimo_uniforme_ab=dict(
            cota=f'2^{args.cota_bits_ab}', filas=filas_ab, maximo_de_clases=estados,
            comprobados_por_fuerza_bruta=cotejo_fuerza_bruta_ab(filas_ab, args.lmax_bruto),
            cota_tres_log2_comprobada=True, records=records_ab(filas_ab),
            alcance='Medición exacta: mínimo sobre todas las palabras de {1,110}^w de largo L. '
                    'No es una cota demostrada para todo L.'))
    resultado['sha256_fuente_lf'] = hashlib.sha256(
        Path(__file__).read_text(encoding='utf-8').encode('utf-8')).hexdigest()
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n',
                           encoding='utf-8')
    leyes_r = resultado['leyes']
    print(f"OK: {leyes_r['repeticiones_con_valores_distintos']} repeticiones, "
          f"{resultado['identidad_residuos']['comparaciones']} comparaciones factor-residuo, "
          f"{len(resultado['sturmianas'])} palabras sturmianas, "
          f"{resultado['racionales']['repeticiones']} repeticiones racionales.")


if __name__ == '__main__':
    main()
