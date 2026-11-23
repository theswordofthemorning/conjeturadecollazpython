"""Propuesta B: presupuesto de un argumento tipo Stepanov para MuroB.

Mapa: atajo T sobre enteros positivos. Una palabra de paridades de
longitud L es expansiva si todos sus prefijos cumplen 3^S_k >= 2^k,
es decir P_k >= 1 para 1 <= k <= L. Cada palabra corresponde a una sola
clase módulo 2^L. MuroB falla en n si y sólo si todos los prefijos de la
palabra de n son expansivos: n está en el conjunto 2-ádico
K = {x en Z_2 : P_k(x) >= 1 para todo k}.

1. Conteo exacto e(L) de palabras expansivas (programación dinámica en S,
   umbrales enteros exactos) y comparación con la tasa de Chernoff.
2. Récords del tiempo de parada de coeficiente tau(n), el primer k con
   P_k < 1: el menor n con tau(n) >= L es el menor representante entero
   de los cilindros expansivos de longitud L.
3. Control de la tautología: los menores 2x2 de los datos de bloque son
   2^t_i 3^S_i rho_ventana.

Todo es conteo exacto o medición finita; nada aquí es una prueba universal.
"""

import argparse
import json
import math
from pathlib import Path


def umbrales(longitud):
    """smin[k] = menor S con 3^S >= 2^k, con enteros exactos."""
    smin = [0]
    s = 0
    for k in range(1, longitud + 1):
        while 3 ** s < 2 ** k:
            s += 1
        smin.append(s)
    return smin


def conteo_expansivas(longitud, smin):
    cuentas = {0: 1}
    resultado = []
    for k in range(1, longitud + 1):
        nuevas = {}
        for s, c in cuentas.items():
            for t in (s, s + 1):
                if t >= smin[k]:
                    nuevas[t] = nuevas.get(t, 0) + c
        cuentas = nuevas
        resultado.append(sum(cuentas.values()))
    return resultado


def tasa_chernoff():
    """rho = min_theta ((3/2)^theta + (1/2)^theta)/2, por búsqueda ternaria."""
    def f(theta):
        return (1.5 ** theta + 0.5 ** theta) / 2
    a, b = 0.0, 2.0
    for _ in range(200):
        m1, m2 = a + (b - a) / 3, b - (b - a) / 3
        if f(m1) < f(m2):
            b = m2
        else:
            a = m1
    return f((a + b) / 2), (a + b) / 2


def tau(n, smin, tope):
    """Primer k con 3^S_k < 2^k; None si no ocurre antes de tope."""
    s = 0
    x = n
    for k in range(1, tope + 1):
        if x % 2:
            s += 1
            x = (3 * x + 1) // 2
        else:
            x //= 2
        if s < smin[k]:
            return k
    return None


def records_tau(limite, smin, tope):
    records = []
    mejor = 0
    for n in range(2, limite + 1):
        t = tau(n, smin, tope)
        assert t is not None, n
        if t > mejor:
            mejor = t
            records.append((n, t))
    return records


def datos_bloque(n, t):
    """(S_t, rho_t) con 2^t T^t(n) = 3^S_t n + rho_t."""
    s, rho, x = 0, 0, n
    for j in range(t):
        if x % 2:
            rho = 3 * rho + 2 ** j
            s += 1
            x = (3 * x + 1) // 2
        else:
            x //= 2
    assert 2 ** t * x == 3 ** s * n + rho
    return s, rho, x


def control_tautologia(n, tiempos):
    """Comprueba 3^S_i rho_j - 3^S_j rho_i = 2^t_i 3^S_i rho_ventana para t_i < t_j."""
    for i, ti in enumerate(tiempos):
        for tj in tiempos[i + 1:]:
            si, ri, xi = datos_bloque(n, ti)
            sj, rj, _ = datos_bloque(n, tj)
            sv, rv, _ = datos_bloque(xi, tj - ti)
            assert 3 ** si * rj - 3 ** sj * ri == 2 ** ti * 3 ** si * rv
    return len(tiempos) * (len(tiempos) - 1) // 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--longitud", type=int, default=2000)
    parser.add_argument("--limite-records", type=int, default=2000000)
    parser.add_argument("--salida", type=Path, required=True)
    args = parser.parse_args()

    smin = umbrales(max(args.longitud, 2000))
    cuentas = conteo_expansivas(args.longitud, smin)
    rho, theta = tasa_chernoff()
    beta_teorica = 1 + math.log2(rho)
    puntos = [10, 50, 100, 250, 500, 1000, 1500, args.longitud]
    beta_medida = {L: math.log2(cuentas[L - 1]) / L for L in puntos if L <= args.longitud}
    # Pendiente entre L/2 y L: elimina el factor polinómico de tipo ballot.
    L = args.longitud
    pendiente = (math.log2(cuentas[L - 1]) - math.log2(cuentas[L // 2 - 1])) / (L - L // 2)

    records = records_tau(args.limite_records, smin, 2000)
    exponentes = [(n, t, math.log2(n) / t) for n, t in records if t >= 20]
    # Densidad exacta de tau >= t: e(t)/2^t. Un récord aleatorio aparece hacia
    # log2 n ~ t - log2 e(t), incluido el factor polinómico.
    esperado = {t: t - math.log2(cuentas[t - 1]) for _, t, _ in exponentes}

    pares = control_tautologia(6416623, [5, 13, 21, 34, 53])
    pares += control_tautologia(2 ** 40 - 1, [3, 10, 17, 25, 40])

    datos = dict(
        mapa="atajo T; palabra expansiva: P_k>=1 para todo prefijo",
        conteo_exacto={str(L): str(cuentas[L - 1]) for L in puntos if L <= args.longitud},
        beta_medida={str(k): round(v, 6) for k, v in beta_medida.items()},
        pendiente_beta_entre_L_medio_y_L=round(pendiente, 6),
        chernoff=dict(rho=rho, theta=theta, beta=beta_teorica),
        records_tau=[dict(n=n, tau=t, log2n_sobre_tau=round(e, 4), log2n=round(math.log2(n), 2),
                          log2n_esperado_aleatorio=round(esperado[t], 2))
                     for n, t, e in exponentes],
        prediccion_aleatoria_log2n_sobre_tau=round(1 - beta_teorica, 4),
        menores_2x2_tautologicos_cotejados=pares,
        alcance=("Conteo exacto de palabras y medicion finita de records. La pendiente estima beta; "
                 "la prediccion aleatoria 1-beta es heuristica. Nada prueba MuroB."),
    )
    args.salida.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("beta medida:", {k: round(v, 4) for k, v in beta_medida.items()})
    print("pendiente L/2..L: %.5f   Chernoff: beta=%.5f (rho=%.5f, theta=%.4f)"
          % (pendiente, beta_teorica, rho, theta))
    print("records tau: n, tau, log2 n / tau, log2 n, esperado t - log2 e(t)")
    for n, t, e in exponentes:
        print("  %10d %4d %.4f %6.2f %6.2f" % (n, t, e, math.log2(n), esperado[t]))
    print("prediccion aleatoria log2 n / tau ~ 1 - beta = %.4f" % (1 - beta_teorica))
    print("menores 2x2 tautologicos cotejados:", pares)


if __name__ == "__main__":
    main()
