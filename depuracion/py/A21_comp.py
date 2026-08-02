# -*- coding: utf-8 -*-
# A21_comp.py - COMPARADOR (agente 3). Tercera implementacion, sin copiar
# el estilo de ninguno de los dos agentes.
#
# Objetivos:
#  1) Caso comun (r=5, k=5) calculado por tercera via.
#  2) El iff del criterio, exhaustivo en k=8, con implementacion distinta
#     (vector de paridad bit a bit, no bucle sobre el numero).
#  3) CERRAR EL HUECO DE RANGO: la base declara excepciones {2,4,5} estables
#     hasta k=22; el agente 2 llego a 18 y el 1 a 7. Aqui: k=19..22 con numpy.
#     Logica: excepcion (buena con alturas m=0 distintas) exige que r o r+1
#     pise el 1 antes del paso k (si ninguno lo pisa, la descomposicion
#     altura = k + S + altura(T^k) vale para los dos y las alturas coinciden
#     porque S y T^k coinciden). Se calculan los candidatos que pisan el 1 y
#     SOLO para ellos se comparan alturas exactas.
#  4) Verificacion puntual de esa logica de descomposicion (muestra k<=10).

import numpy as np
import sys

fallos = 0
def check(cond, msg):
    global fallos
    if not cond:
        fallos += 1
        print("FALLO:", msg)

# ------------------------------------------------ tercera implementacion
def paso(n):
    return (3 * n + 1) >> 1 if n % 2 else n >> 1

def tray_k(n, k):
    """(T^k(n), S_k(n), toco_1_antes) por tercera via."""
    s = 0
    toco = False
    for _ in range(k):
        if n == 1:
            toco = True
        if n % 2:
            s += 1
        n = paso(n)
    return n, s, toco

def altura_c(n):
    h = 0
    while n != 1:
        n = 3 * n + 1 if n % 2 else n // 2
        h += 1
    return h

# 1) caso comun
t5, s5, _ = tray_k(5, 5)
t6, s6, _ = tray_k(6, 5)
print("1) caso comun r=5,k=5: T^5(5)=%d S=%d | T^5(6)=%d S=%d" % (t5, s5, t6, s6))
check((t5, s5) == (2, 2) and (t6, s6) == (2, 2), "caso comun r=5,k=5")
check(altura_c(5) == 5 and altura_c(6) == 8, "alturas clasicas (5,6)")
check(altura_c(4) == 2, "altura clasica de 4")

# 2) iff del criterio, exhaustivo k=8, m=1..12 mas m grandes sueltos
print("2) iff del criterio en k=8, exhaustivo en r")
k = 8
tam = 1 << k
n_buenas = 0
for r in range(tam):
    a, sa, _ = tray_k(r, k)
    b, sb, _ = tray_k(r + 1, k)
    buena = (a == b and sa == sb)
    if buena:
        n_buenas += 1
    # coincidencia en el paso k para m en muestras
    ok = all(tray_k((m << k) + r, k)[0] == tray_k((m << k) + r + 1, k)[0]
             for m in (1, 2, 3, 50, 999))
    check(ok == buena or (not buena and not ok) or buena,
          "consistencia r=%d" % r)
    if buena:
        check(ok, "buena k=8 r=%d falla en algun m" % r)
    else:
        # dos afines distintas: a lo sumo un cruce; con 5 m distintos no pueden coincidir todos
        check(not ok, "mala k=8 r=%d coincide en todas las muestras" % r)
print("   clases buenas en k=8: %d (a(8)=82 en la sucesion de los agentes; 170 es a(9))" % n_buenas)
check(n_buenas == 82, "conteo de buenas k=8 (a(8)=82)")

# 4) logica de la descomposicion: buena y sin pisar el 1 => alturas iguales
print("4) muestra: buena sin pisar 1 => alturas m=0 iguales (k=3..10 exhaustivo)")
for kk in range(3, 11):
    for r in range(1, (1 << kk) - 1):
        a, sa, ta = tray_k(r, kk)
        b, sb, tb = tray_k(r + 1, kk)
        if a == b and sa == sb:
            if not ta and not tb:
                check(altura_c(r) == altura_c(r + 1),
                      "buena sin tocar 1 con alturas distintas k=%d r=%d" % (kk, r))
            else:
                pass  # candidato a excepcion; abajo se listan
print("   ok")

# 3) el hueco: k = 19..22 con numpy
print("3) excepciones m=0 en k=19..22 (cierra el hueco 19..22 de la base)")
for k in range(19, 23):
    N = 1 << k
    val = np.arange(N, dtype=np.int64)
    S = np.zeros(N, dtype=np.int64)
    toco = np.zeros(N, dtype=bool)
    for _ in range(k):
        toco |= (val == 1)
        imp = (val & 1).astype(bool)
        S += imp
        val = np.where(imp, (3 * val + 1) >> 1, val >> 1)
    buena = (S[:-1] == S[1:]) & (val[:-1] == val[1:])
    nb = int(buena.sum())
    # candidatos a excepcion: buenas donde r o r+1 piso el 1 antes del paso k
    cand = np.nonzero(buena & (toco[:-1] | toco[1:]))[0]
    exc = sorted(int(r) for r in cand if altura_c(int(r)) != altura_c(int(r) + 1))
    print("   k=%d: %d buenas, candidatos que pisan 1: %d, excepciones: %s"
          % (k, nb, len(cand), exc))
    check(exc == [2, 4, 5], "excepciones k=%d no son [2,4,5]: %s" % (k, exc))

print()
if fallos:
    raise SystemExit("COMPARADOR: %d FALLOS" % fallos)
print("COMPARADOR: 0 fallos. Caso comun, iff en k=8, y excepciones {2,4,5} estables k=19..22.")
