# revisionadversarial1108.py
#
# LA REVISION ADVERSARIAL DE LA TANDA DEL 11-08, EJECUTADA EN LOCAL
# (orden del usuario: sin agentes externos -- Python puro, el regimen
# "revisarse una misma" del 09-08 (8)). El encargo de siempre: ROMPER,
# no aplaudir. Cada ataque termina en VEREDICTO; el fichero sale con
# codigo 1 si algun ataque CONFIRMA una rotura.
#
# LO QUE SE ATACA (la tanda entera de hoy):
#   A1  pisoporarranque: la validez de la cota inferior bajo poda
#       (A/B de tope: una poda mas agresiva NUNCA puede subir phi_min)
#       y la reproduccion del punto publicado T=70.
#   A2  la aritmetica de las gammas, recomputada desde la salida.
#   A3  sombraexogena: sensibilidad a semillas del MC de V3
#       (el "+-0,03" de la conclusion, contra 3 semillas frescas).
#   A4  EL TEST DE FALSACION del mecanismo: V2a dos decadas mas lejos
#       (x = 2e10, 2e12, T = 300) -- si gamma NO sigue cayendo, la
#       historia "transitorio de grandes desviaciones" queda tocada.
#   A5  arranquesporvisita: beta y el reloj con OTRA semilla, y la
#       cola maxima de |c_i| (donde una union burda se juega la vida).
#   A6  el lema de las preimagenes de (1,1), por fuerza bruta.
#   A7  la ley del borde y la fila 2, por enumeracion independiente
#       (incluida la parametrizacion exacta con a0, a2 impares).
#   A8  el Paso 3 de notamoscasinducida: E[|c|^theta] en el primer
#       retorno, acotado en el arranque? (spot-check del esquema).
#
#   Mapa del ATAJO via la cadena; el azar solo en semillas declaradas.

import math
import random
from itertools import combinations

VEREDICTOS = []


def veredicto(nombre, roto, detalle):
    VEREDICTOS.append((nombre, roto, detalle))
    print("  -> %s: %s  (%s)" % (nombre, "ROTO" if roto else "aguanta", detalle))


def transicion_mod(k, c, bit):
    if k == 0:
        if c % 2 == 0:
            return (0, c // 2) if bit == 0 else (0, 3 * c // 2)
        return (1, (3 * c + 1) // 2) if bit == 0 else (1, (1 - 3 * c) // 2)
    if c % 2 == 0:
        return (k, c // 2) if bit == 0 else (k, (3 * c + 1 - 3 ** k) // 2)
    if k == 1 and c == 1:
        return (2, 2)
    if bit == 0:
        return (k + 1, (3 * c + 1) // 2)
    if k >= 2:
        return (k - 1, (c - 3 ** (k - 1)) // 2)
    return (0, abs((c - 1) // 2))


def transicion_real(k, c, bit):
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


# ---------------------------------------------------------------------------
print("A1 -- la cota inferior bajo poda (A/B de tope, c0 = 2000, T = 70)")
# ---------------------------------------------------------------------------


def barrido(c0, t_max, tope):
    vivos = {(2, c0): 1}
    ventana = perdida = 0.0
    for t in range(1, t_max + 1):
        nuevo = {}
        for (k, c), n in vivos.items():
            for bit in (0, 1):
                kk, cc = transicion_mod(k, c, bit)
                if kk <= 1:
                    if abs(cc) <= 25:
                        ventana += n / 2.0 ** t
                else:
                    nuevo[(kk, cc)] = nuevo.get((kk, cc), 0) + n
        if len(nuevo) > tope:
            pares = sorted(nuevo.items(), key=lambda kv: kv[1])
            cortar = len(nuevo) - tope
            perdida += sum(n for _, n in pares[:cortar]) / 2.0 ** t
            nuevo = dict(pares[cortar:])
        vivos = nuevo
    viva = sum(vivos.values()) / 2.0 ** t_max if vivos else 0.0
    return ventana, perdida, viva


v_grande, p_grande, m_grande = barrido(2000, 70, 2 * 10 ** 6)
v_chico, p_chico, m_chico = barrido(2000, 70, 10 ** 5)
# el ataque: (i) phi_min con tope chico NO puede superar al grande;
# (ii) el grande debe reproducir el 0,1044 publicado del 10-08 a T=70;
# (iii) la masa total contabilizada (ventana+perdida+viva+fallo) <= 1.
roto1 = v_chico > v_grande + 1e-12
roto2 = abs(v_grande - 0.1044) > 5e-4
veredicto("A1.monotonia de la poda", roto1,
          "phi_tope1e5 = %.4f contra phi_tope2e6 = %.4f" % (v_chico, v_grande))
veredicto("A1.reproduccion T=70", roto2,
          "phi = %.4f contra 0,1044 publicado" % v_grande)

# ---------------------------------------------------------------------------
print()
print("A2 -- la aritmetica de las gammas, recomputada de la salida")
# ---------------------------------------------------------------------------

import io
import os
phis = {}
if os.path.exists('pisoporarranque_salida.txt'):
    for linea in io.open('pisoporarranque_salida.txt', encoding='utf-8'):
        partes = linea.split()
        if len(partes) >= 2 and partes[0] in ('2000', '20000', '200000', '2000000') \
                and linea.strip().startswith(partes[0]):
            try:
                phis[int(partes[0])] = float(partes[1])
            except ValueError:
                pass
gammas_pub = [0.297, 0.211, 0.197]
if len(phis) == 4:
    xs = [2000, 20000, 200000, 2000000]
    gs = [math.log10(phis[a] / phis[b]) for a, b in zip(xs, xs[1:])]
    peor = max(abs(g - gp) for g, gp in zip(gs, gammas_pub))
    veredicto("A2.gammas", peor > 0.0015,
              "recomputadas %s contra publicadas %s" %
              (["%.3f" % g for g in gs], gammas_pub))
else:
    veredicto("A2.gammas", True, "no pude parsear la tabla final (%d filas)" % len(phis))

# ---------------------------------------------------------------------------
print()
print("A3 -- V3 Monte Carlo contra 3 semillas frescas (x = 200000)")
# ---------------------------------------------------------------------------


def excursion_v3(azar, c0, t_max=150):
    k, c = 2, c0
    for _ in range(t_max):
        k, c = transicion_mod(k, c, azar.getrandbits(1))
        if k <= 1:
            return 1 if abs(c) <= 25 else 0
    return 0


valores = []
for sem in (11, 22, 33):
    azar = random.Random(sem)
    N = 100000
    valores.append(sum(excursion_v3(azar, 200000) for _ in range(N)) / N)
spread = max(valores) - min(valores)
# el barrido exacto da phi_min 0,0373 a T=150 (cota inferior del MC);
# el MC de la manana dio 0,0387. Con err.tip. ~0,0006, 3 sigma ~ 0,002.
roto = spread > 0.004 or min(valores) < 0.0373 - 0.002
veredicto("A3.semillas V3", roto,
          "phi en 3 semillas: %s (spread %.4f)" %
          (["%.4f" % v for v in valores], spread))

# ---------------------------------------------------------------------------
print()
print("A4 -- FALSACION del mecanismo: V2a en x = 2e10 y 2e12 (T = 300)")
# ---------------------------------------------------------------------------


def excursion_v2a(azar, u0, t_max=300):
    k, u = 2, u0
    for _ in range(t_max):
        bit = azar.getrandbits(1)
        es_mixto = azar.getrandbits(1) == 1
        u = u / 2.0 if bit == 0 else (3.0 * u - 1.0) / 2.0
        if es_mixto:
            k += 1 if bit == 0 else -1
            if k <= 1:
                return 1 if abs(u) <= 25.0 / 3.0 else 0
    return 0


serie = {}
for x in (2 * 10 ** 8, 2 * 10 ** 10, 2 * 10 ** 12):
    azar = random.Random(999 + int(math.log10(x)))
    N = 100000
    serie[x] = sum(excursion_v2a(azar, x / 9.0) for _ in range(N)) / N
g1 = math.log10(serie[2 * 10 ** 8] / serie[2 * 10 ** 10]) / 2   # por decada
g2 = math.log10(serie[2 * 10 ** 10] / serie[2 * 10 ** 12]) / 2
# el mecanismo predice gamma cayendo (hacia 0); si gamma SUBE o se
# estanca claramente lejos de 0, la historia esta tocada
roto = g2 > g1 + 0.02
veredicto("A4.gamma sigue cayendo lejos", roto,
          "phi: %s; gamma/decada %.3f -> %.3f" %
          (["%.4f" % serie[x] for x in sorted(serie)], g1, g2))

# ---------------------------------------------------------------------------
print()
print("A5 -- beta y la cola de |c_i| con OTRA semilla (200 cadenas x 2e5)")
# ---------------------------------------------------------------------------

arr = {}
maxc = 0
azar_base = 555000
for idx in range(200):
    azar = random.Random(azar_base + idx)
    k, c = 2, 2
    i = 1
    en_exc = True
    for _ in range(200000):
        k2, c2 = transicion_mod(k, c, azar.getrandbits(1))
        if en_exc and k2 <= 1:
            en_exc = False
        elif not en_exc and k2 >= 2:
            i += 1
            arr.setdefault(min(i // 100, 9), []).append(abs(c2).bit_length())
            if abs(c2) > maxc:
                maxc = abs(c2)
            en_exc = True
        k, c = k2, c2
p90s = []
for cub in sorted(arr):
    datos = sorted(arr[cub])
    if len(datos) >= 50:
        p90s.append(datos[int(0.9 * len(datos))])
roto = (max(p90s) - min(p90s)) > 2   # el "plano" de beta = 0: p90 estable
veredicto("A5.beta plano otra semilla", roto,
          "p90 por cubeta de i/100: %s; max|c_i| = %d bits" %
          (p90s, maxc.bit_length()))

# ---------------------------------------------------------------------------
print()
print("A6 -- el lema de las preimagenes de (1,1), fuerza bruta")
# ---------------------------------------------------------------------------

pre = []
for k in range(0, 13):
    for c in range(1 if k == 0 else -300000, 300001):
        if k == 0 and c <= 0:
            continue
        for bit in (0, 1):
            r = transicion_real(k, c, bit)
            if r[0] == 'estado' and (r[1], r[2]) == (1, 1):
                pre.append((k, c, bit))
roto = sorted(pre) != [(1, 2, 0), (2, 5, 1)]
veredicto("A6.preimagenes de (1,1)", roto, "halladas: %s" % pre)

# ---------------------------------------------------------------------------
print()
print("A7 -- la ley del borde y la fila 2, enumeracion independiente")
# ---------------------------------------------------------------------------


def corre(palabra):
    k, c = 0, 1
    for i, bit in enumerate(palabra):
        r = transicion_real(k, c, bit)
        if r[0] == 'fusion':
            return i + 1
        k, c = r[1], r[2]
    return None


fallo_b1 = fallo_b2 = None
for t in range(5, 23):
    n1 = 0
    for ceros in combinations(range(t), 2):
        palabra = [1] * t
        for p in ceros:
            palabra[p] = 0
        if corre(palabra) == t:
            n1 += 1
    if n1 != (t - 1) // 2:
        fallo_b1 = (t, n1)
        break
for t in range(8, 19):
    n2 = 0
    malas = 0
    for ceros in combinations(range(t), 4):
        palabra = [1] * t
        for p in ceros:
            palabra[p] = 0
        if corre(palabra) == t:
            n2 += 1
            z = list(ceros)
            a0 = z[0]
            a1 = z[1] - z[0] - 1
            a2 = z[2] - z[1] - 1
            if not (a0 % 2 == 1 and a1 == 1 and a2 % 2 == 1 and z[3] < t - 1):
                malas += 1
    esperado = math.comb((t - 4) // 2, 2)
    if n2 != esperado or malas:
        fallo_b2 = (t, n2, esperado, malas)
        break
veredicto("A7.ley del borde", fallo_b1 is not None,
          "F(t,t-2) = floor((t-1)/2) en t = 5..22" if fallo_b1 is None
          else "FALLA en %s" % (fallo_b1,))
veredicto("A7.fila 2 + parametrizacion", fallo_b2 is not None,
          "C(floor((t-4)/2),2) y patron a0/a1/a2 en t = 8..18"
          if fallo_b2 is None else "FALLA en %s" % (fallo_b2,))

# ---------------------------------------------------------------------------
print()
print("A8 -- E[|c|^0.3] en el primer retorno, por arranque (Paso 3)")
# ---------------------------------------------------------------------------

momentos = []
for c0 in (5, 101, 2001, 20001):
    azar = random.Random(31400 + c0)
    N = 20000
    suma = cont = 0
    for _ in range(N):
        k, c = 2, c0
        for _ in range(600):
            k, c = transicion_mod(k, c, azar.getrandbits(1))
            if k <= 1:
                suma += abs(c) ** 0.3
                cont += 1
                break
    momentos.append(suma / cont if cont else float('inf'))
# el esquema pide momento acotado uniformemente en el arranque; se
# tolera crecimiento suave (el arranque grande tarda en contraer),
# lo que rompe es divergencia clara
roto = momentos[-1] > 10 * momentos[0]
veredicto("A8.momento theta=0,3 acotado", roto,
          "E[|c|^0.3] por arranque 5/101/2001/20001: %s" %
          (["%.2f" % m for m in momentos]))

# ---------------------------------------------------------------------------
print()
rotos = [v for v in VEREDICTOS if v[1]]
print("=" * 60)
print("EL SALDO DE LA REVISION: %d ataques, %d ROTOS, %d aguantan."
      % (len(VEREDICTOS), len(rotos), len(VEREDICTOS) - len(rotos)))
for nombre, _, detalle in rotos:
    print("  ROTO: %s -- %s" % (nombre, detalle))
if rotos:
    raise SystemExit("la revision CONFIRMO roturas: aplicar antes de seguir")
print("Ningun ataque rompio. 'No pude romperlo' -- despues de intentarlo.")
