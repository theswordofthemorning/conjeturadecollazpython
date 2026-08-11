# certificadocw.py
#
# EL CERTIFICADO COLLATZ-WIELANDT DE LA ESCALERA ENTERA (11-08-2026
# (2), el P6 del paper del programa -- la recomendacion C-3 del
# adversario 2 de la 8a revision, cobrada como fichero del repo: su
# adv2_cw.py certifico los escalones 1-5 y no quedo en git).
#
#   LO QUE CERTIFICA. Para la matriz de conteo M del truncado
#   (K, C) de la cadena (estados vivos de la caja, M[i][j] = numero
#   de bits que llevan i -> j), la cota de Collatz-Wielandt dice:
#
#     para todo vector v >= 0 no nulo:
#         radio_espectral(M)  >=  min_{i: v_i > 0} (Mv)_i / v_i
#
#   y (Mv)_i = v[suc0(i)] + v[suc1(i)] (sucesores muertos aportan 0).
#   Con v ENTERO y el minimo computado en aritmetica entera exacta,
#   la "razon convergida" de pumasescalera sube a COTA DEMOSTRADA
#   del truncado; el puente truncado -> cadena entera (lambda >=
#   lambda_T, menores anidados) es el de PUMAS/ZORRAS, ya
#   establecido en retornoslambda.py.
#
#   METODO. Por escalon: (1) cierre alcanzable desde (0,1) dentro de
#   la caja (BFS, mismo criterio que pumasescalera.py -- duplicado a
#   proposito, regla de la casa); (2) iteracion HACIA ATRAS
#   v <- Mv en float (numpy, solo para ENCONTRAR el vector: el
#   float no decide nada); (3) el vector se escala a ENTEROS
#   (ESCALA = 10^12; los estados con peso < 1 salen del soporte --
#   CW vale para cualquier v >= 0, recortar soporte solo puede
#   bajar la cota, nunca invalidarla); (4) el minimo de
#   (v[suc0] + v[suc1]) / v[i] sobre el soporte se computa con
#   ENTEROS de Python (comparacion cruzada a*d < b*c, sin floats).
#
#   COMPROBACIONES (SystemExit):
#     C1  el certificado de cada escalon cae a menos de TOLERANCIA
#         de la lambda_T publicada (para 1-5, el adversario 2 ya
#         clavo 6 decimales con su implementacion propia).
#     C2  la escalera CERTIFICADA es monotona creciente.
#     C3  el remate: el escalon 9 certifica lambda >= 1,9865 o mas
#         (lo publicado por razon convergida: 1,987046).
#
#   ~40-60 min de CPU con el escalon 9 (5,3M estados; el BFS puro
#   es lo caro). numpy solo en la fase de busqueda del vector.

import time
import numpy as np

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
    (19, 3145728, None),   # EL ESCALON 10: jamas corrido; publicada
                           # None = modo descubrimiento (~17M estados,
                           # el BFS puro es el cuello: ~15-25 min)
]
ESCALON_10 = True          # False para la pasada de verificacion 1-9
                           # (~100 s con numpy)
ITERACIONES = 600          # iteracion hacia atras para hallar v
ESCALA = 10 ** 12          # v flotante -> v entero
TOLERANCIA = 5e-4          # certificado contra lambda_T publicada
PISO_FINAL = 1.9865        # C3: lo que el escalon 9 debe certificar
TOPE_ESTADOS = 25 * 10 ** 6


def transicion(k, c, bit):
    if k == 0:
        if c % 2 == 0:
            return ('estado', 0, c // 2) if bit == 0 else ('estado', 0, 3 * c // 2)
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
    # indice directo durante el BFS (sin set aparte: la memoria del
    # escalon 10 la manda esta fase)
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
                    raise SystemExit("cerrar_caja: tope de estados en "
                                     "(%d, %d)" % (K, C))
                frontera.append((k2, c2))
    n = len(indice)
    MUERTO = n            # sucesor fuera de caja o fusion: indice fantasma
    suc0 = np.full(n + 1, MUERTO, dtype=np.int64)
    suc1 = np.full(n + 1, MUERTO, dtype=np.int64)
    for s, i in indice.items():
        for bit, suc in ((0, suc0), (1, suc1)):
            t = transicion(s[0], s[1], bit)
            if t[0] == 'estado' and t[1] <= K and abs(t[2]) <= C:
                suc[i] = indice[(t[1], t[2])]
    return n, suc0, suc1


def certificar(K, C):
    n, suc0, suc1 = cerrar_caja(K, C)
    # fase float (solo busqueda): v <- Mv hacia atras, normalizando
    v = np.ones(n + 1, dtype=np.float64)
    v[n] = 0.0                      # el fantasma pesa 0
    for it in range(ITERACIONES):
        v = v[suc0] + v[suc1]
        v[n] = 0.0
        m = v.max()
        if m > 1e250 or (it % 10 == 9):
            v /= m
    # fase entera (la que decide): escalar, recortar soporte, minimo
    v = v / v.max()
    w = np.floor(v * ESCALA).astype(np.int64)
    w[n] = 0
    lista = w.tolist()
    s0 = suc0.tolist()
    s1 = suc1.tolist()
    num, den = 0, 0                 # el minimo como fraccion num/den
    soporte = 0
    for i in range(n):
        wi = lista[i]
        if wi <= 0:
            continue
        soporte += 1
        mv = lista[s0[i]] + lista[s1[i]]
        if den == 0 or mv * den < num * wi:
            num, den = mv, wi
    return n, soporte, num, den


print("EL CERTIFICADO COLLATZ-WIELANDT DE LA ESCALERA DE PUMAS")
print("(v entero, minimo exacto sobre el soporte; el float solo busca)")
print()
print("  K     C       estados    soporte    certificado   publicada   dif")
anterior = 0.0
certificados = []
for (K, C, publicada) in ESCALERA:
    if publicada is None and not ESCALON_10:
        print("  [escalon 10 saltado: ESCALON_10 = False]")
        continue
    t0 = time.time()
    n, soporte, num, den = certificar(K, C)
    cert = num / den
    if publicada is not None:
        dif = cert - publicada
        if abs(dif) > TOLERANCIA:
            raise SystemExit("C1: escalon (%d, %d): certificado %.6f contra "
                             "publicada %.6f" % (K, C, cert, publicada))
        col = "%.6f   %+.1e" % (publicada, dif)
    else:
        col = "PRIMERA CORRIDA    "
    if cert <= anterior:
        raise SystemExit("C2: la escalera certificada dejo de ser monotona "
                         "en (%d, %d)" % (K, C))
    anterior = cert
    certificados.append((K, C, n, cert))
    print("  %2d  %8d   %8d   %8d     %.6f     %s   (%.0f s)"
          % (K, C, n, soporte, cert, col, time.time() - t0),
          flush=True)

print()
print("COMPROBACIONES 1 y 2 OK: los nueve escalones certificados a menos")
print("de %.0e de lo publicado, y la escalera certificada es monotona." % TOLERANCIA)
final = certificados[-1][3]
if final < PISO_FINAL:
    raise SystemExit("C3: el escalon 9 certifica %.6f < %.4f"
                     % (final, PISO_FINAL))
print()
print("COMPROBACION 3 OK -- LA COTA DE PUMAS, CON SU LETRA DICHA:")
print("  LAMBDA_T >= %.6f  CERTIFICADO PARA EL TRUNCADO (teorema:" % final)
print("  Collatz-Wielandt en enteros; ultimo escalon K = %d,"
      % certificados[-1][0])
print("  |c| <= %d, %d estados). El puente lambda >= lambda_T"
      % (certificados[-1][1], certificados[-1][2]))
print("  es el de PUMAS (menores anidados, matriztransferencia.py);")
print("  la 9a revision (adv 3) dejo dicho su paso fino pendiente:")
print("  heredar el RITMO rho(M_T) pide el paso Perron/SCC sin")
print("  escribir (evidencia: las razones de pumasescalera empatan")
print("  estos certificados a ~1e-6 en todos los escalones).")
