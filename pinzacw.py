# pinzacw.py
#
# LANGOSTAS (bautizado 12-08: la pinza de dos tenazas).
# LA PINZA DE DOS LADOS + EL PASO PERRON/SCC DEL CERTIFICADO CW
# (12-08-2026; el punto 5 de la ruta post-9a -- "heredar el RITMO
# rho(M_T)", la tecnica del adversario 3 de la 9a adoptada como
# fichero del repo, sobre la escalera entera de Pumas; el escalon 10
# (22,5M estados, bandera ESCALON_10) YA CORRIO: su salida esta en
# pinzacw_salida10.txt).
#
#   EL PROBLEMA. certificadocw.py da la cota INFERIOR
#   rho(M_T) >= min_i (Mv)_i/v_i (Collatz-Wielandt, enteros). La
#   letra chica que la 9a nombro: para heredar el RITMO (que el
#   crecimiento real de los conteos es rho(M_T)^t) hace falta el
#   paso Perron/SCC: saber DONDE vive rho.
#
#   LO QUE ESTE FICHERO ESTABLECE, por escalon:
#     (1) LA DESCOMPOSICION SCC del grafo de la caja (Tarjan
#         iterativo): si hay UNA SOLA componente fuertemente
#         conexa no trivial S* (y ningun lazo propio fuera), el
#         algebra elemental de matrices no negativas da
#         rho(M_T) = rho(S*), y Perron-Frobenius aplica en S*.
#     (2) LA PINZA: sobre S*, con v ESTRICTAMENTE positivo,
#           min_{i en S*} (M_S* v)_i / v_i  <=  rho(S*)  <=
#           max_{i en S*} (M_S* v)_i / v_i
#         -- el lado izquierdo es CW (v >= 0 basta); el derecho es
#         subinvarianza (v > 0 en S* basta, SIN irreducibilidad).
#         Las dos comparaciones en aritmetica ENTERA exacta
#         (a*d < b*c); el float solo busca el vector.
#
#   COMPROBACIONES (SystemExit):
#     P1  en cada escalon hay EXACTAMENTE una SCC no trivial y
#         cero lazos propios fuera de ella (si no, se reporta y el
#         teorema "rho(M_T) = rho(S*)" no se afirma).
#     P2  la lambda_T publicada cae DENTRO de la pinza.
#     P3  la pinza es angosta: ancho <= ANCHO_TOPE.
#     P4  el lado inferior empata el certificado de certificadocw
#         (mismo objeto, otra restriccion: |dif| <= 2e-3).
#
#   Capa 1: mapa = cadena (k, c) del atajo (la transicion de
#   certificadocw, duplicada a proposito -- regla de la casa); las
#   cotas que se afirman son del TRUNCADO M_T (el puente
#   lambda >= lambda_T es el de Pumas, aparte); el vector se
#   recorta a S* y alli se fuerza v >= 1 (subir un peso a 1 solo
#   puede ENSANCHAR la pinza reportada, nunca invalidarla).

import time
import numpy as np

# LA SERIE DE CAJAS DE LA ESCALERA (documentada el 12-08-2026 pagando
# la deuda de la 10a revision, actarevision1208.txt III -- el
# adversario 2 tuvo que deducirla). Cada escalon s = 1..10 trunca la
# cadena a  k <= K,  |c| <= C,  con:
#
#     escalon 1:       K = 2        C = 12 = 3*2^K
#     escalones 2-10:  K = 2s-1     C = 3*2^(K+1)
#
# o, en UNA sola formula valida para los diez:  C_s = 3*4^s
# (C cuadruplica por escalon: 12, 48, 192, 768, 3072, 12288, 49152,
# 196608, 786432, 3145728) y K sube 2 -> 3 y de ahi de a 2 (impar).
# Es la MISMA ESCALERA de pumasescalera.py y certificadocw.py
# (verificado identico, 12-08-2026); el tercer campo es la lambda_T
# publicada que P2 exige reproducir.
ESCALERA = [
    (2, 12, 1.7400),
    (3, 48, 1.8667),
    (5, 192, 1.9336),
    (7, 768, 1.9556),
    (9, 3072, 1.9675),
    (11, 12288, 1.97545),
    (13, 49152, 1.980748),
    (15, 196608, 1.984415),
    (17, 786432, 1.987046),
]
ESCALON_10 = True          # (19, 3145728): 22,5M estados, ~20-40 min
                           # y ~8-10 GB de RAM; el certificado de
                           # certificadocw.py dio 1,989042
if ESCALON_10:
    ESCALERA.append((19, 3145728, 1.989042))
ITERACIONES = 1200
ESCALA = 10 ** 12
ANCHO_TOPE = 0.02          # convencion de gate, sin derivacion
DIF_CERT_TOPE = 2e-3
TOPE_ESTADOS = 25 * 10 ** 6


def transicion(k, c, bit):
    if k == 0:
        if c % 2 == 0:
            return ('estado', 0, c // 2) if bit == 0 \
                else ('estado', 0, 3 * c // 2)
        return ('estado', 1, (3 * c + 1) // 2) if bit == 0 \
            else ('estado', 1, (1 - 3 * c) // 2)
    if c % 2 == 0:
        return ('estado', k, c // 2) if bit == 0 \
            else ('estado', k, (3 * c + 1 - 3 ** k) // 2)
    if bit == 0:
        return ('estado', k + 1, (3 * c + 1) // 2)
    if k >= 2:
        return ('estado', k - 1, (c - 3 ** (k - 1)) // 2)
    g = (c - 1) // 2
    if g == 0:
        return ('fusion',)
    return ('estado', 0, abs(g))


def cerrar_caja(K, C):
    inicio = (0, 1)
    indice = {inicio: 0}
    frontera = [inicio]
    while frontera:
        k, c = frontera.pop()
        for bit in (0, 1):
            s = transicion(k, c, bit)
            if s[0] == 'fusion':
                continue
            k2, c2 = s[1], s[2]
            if k2 <= K and abs(c2) <= C and (k2, c2) not in indice:
                indice[(k2, c2)] = len(indice)
                if len(indice) > TOPE_ESTADOS:
                    raise SystemExit("cerrar_caja: tope de estados")
                frontera.append((k2, c2))
    n = len(indice)
    MUERTO = n
    suc0 = np.full(n + 1, MUERTO, dtype=np.int64)
    suc1 = np.full(n + 1, MUERTO, dtype=np.int64)
    for s, i in indice.items():
        for bit, suc in ((0, suc0), (1, suc1)):
            t = transicion(s[0], s[1], bit)
            if t[0] == 'estado' and t[1] <= K and abs(t[2]) <= C:
                suc[i] = indice[(t[1], t[2])]
    return n, suc0, suc1


def tarjan_scc(n, s0, s1):
    # Tarjan iterativo; devuelve etiqueta de SCC por nodo y tamanos
    indice = [-1] * n
    low = [0] * n
    en_pila = [False] * n
    pila = []
    etiqueta = [-1] * n
    contador = [0]
    n_scc = [0]
    tam = []
    for raiz in range(n):
        if indice[raiz] != -1:
            continue
        trabajo = [(raiz, 0)]
        while trabajo:
            v, fase = trabajo.pop()
            if fase == 0:
                indice[v] = low[v] = contador[0]
                contador[0] += 1
                pila.append(v)
                en_pila[v] = True
            hijos = [s for s in (s0[v], s1[v]) if s < n]
            avanzado = False
            for idx in range(fase, len(hijos)):
                h = hijos[idx]
                if indice[h] == -1:
                    trabajo.append((v, idx + 1))
                    trabajo.append((h, 0))
                    avanzado = True
                    break
                elif en_pila[h]:
                    if indice[h] < low[v]:
                        low[v] = indice[h]
            if avanzado:
                continue
            if low[v] == indice[v]:
                t = 0
                while True:
                    w = pila.pop()
                    en_pila[w] = False
                    etiqueta[w] = n_scc[0]
                    t += 1
                    if w == v:
                        break
                tam.append(t)
                n_scc[0] += 1
            if trabajo:
                padre = trabajo[-1][0]
                if low[v] < low[padre]:
                    low[padre] = low[v]
    return etiqueta, tam


print("LA PINZA DE DOS LADOS + PERRON/SCC (escalones 1-%d de Pumas)"
      % len(ESCALERA))
print()
print("  K      estados   SCCs   no-triv  |S*|      pinza inferior  "
      "superior   ancho    publicada")
for (K, C, publicada) in ESCALERA:
    t0 = time.time()
    n, suc0, suc1 = cerrar_caja(K, C)
    s0l = suc0.tolist()
    s1l = suc1.tolist()
    etiqueta, tam = tarjan_scc(n, s0l, s1l)
    # no triviales: tamano >= 2, o singleton con lazo propio
    no_triv = []
    for sc in range(len(tam)):
        if tam[sc] >= 2:
            no_triv.append(sc)
    lazos_fuera = 0
    for i in range(n):
        if (s0l[i] == i or s1l[i] == i) and tam[etiqueta[i]] == 1:
            lazos_fuera += 1
    if len(no_triv) != 1 or lazos_fuera > 0:
        raise SystemExit("P1: escalon K = %d: %d SCCs no triviales, %d "
                         "lazos sueltos -- rho(M_T) = rho(S*) NO se "
                         "afirma" % (K, len(no_triv), lazos_fuera))
    sc_star = no_triv[0]
    en_star = [etiqueta[i] == sc_star for i in range(n)]
    # el vector por iteracion hacia atras (float SOLO busca)
    v = np.ones(n + 1, dtype=np.float64)
    v[n] = 0.0
    for it in range(ITERACIONES):
        v = v[suc0] + v[suc1]
        v[n] = 0.0
        if it % 10 == 9:
            v /= v.max()
    v = v / v.max()
    w = np.floor(v * ESCALA).astype(np.int64).tolist()
    # restringir a S*: v > 0 forzado (subir a 1 solo ensancha)
    for i in range(n):
        if en_star[i] and w[i] <= 0:
            w[i] = 1
    # la pinza en enteros: solo aristas DENTRO de S*
    num_min = den_min = 0
    num_max = den_max = 0
    for i in range(n):
        if not en_star[i]:
            continue
        mv = 0
        for s in (s0l[i], s1l[i]):
            if s < n and en_star[s]:
                mv += w[s]
        wi = w[i]
        if den_min == 0 or mv * den_min < num_min * wi:
            num_min, den_min = mv, wi
        if den_max == 0 or mv * den_max > num_max * wi:
            num_max, den_max = mv, wi
    inf = num_min / den_min
    sup = num_max / den_max
    ancho = sup - inf
    # las publicadas vienen redondeadas (4-6 decimales): la misma
    # TOLERANCIA que certificadocw.py
    if not (inf - 5e-4 <= publicada <= sup + 5e-4):
        raise SystemExit("P2: escalon K = %d: publicada %.6f fuera de "
                         "[%.6f, %.6f]" % (K, publicada, inf, sup))
    if ancho > ANCHO_TOPE:
        raise SystemExit("P3: escalon K = %d: ancho %.4f > %.2f"
                         % (K, ancho, ANCHO_TOPE))
    if abs(inf - publicada) > DIF_CERT_TOPE:
        raise SystemExit("P4: escalon K = %d: inferior %.6f contra "
                         "certificado %.6f" % (K, inf, publicada))
    print("  %2d   %8d   %5d     %d     %7d     %.6f      %.6f   "
          "%.5f   %.6f   (%.0f s)"
          % (K, n, len(tam), len(no_triv), tam[sc_star], inf, sup,
             ancho, publicada, time.time() - t0), flush=True)

print()
print("P1-P4 OK EN LOS %d ESCALONES: una sola SCC no trivial y cero"
      % len(ESCALERA))
print("lazos sueltos (asi que rho(M_T) = rho(S*), Perron aplica), la")
print("publicada dentro de la pinza, el ancho bajo el tope, y el lado")
print("inferior empata el certificado. LA LETRA CHICA DEL RITMO esta")
print("pagada para toda la escalera corrida: rho(M_T) esta PINZADO por")
print("dos lados en enteros y vive en la SCC unica.")
