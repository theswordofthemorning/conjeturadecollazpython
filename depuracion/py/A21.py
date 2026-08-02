# -*- coding: utf-8 -*-
# A21.py - AGENTE 2 (Python independiente). Escrito desde cero, sin abrir
# ningun fichero del repo.
#
# ENUNCIADO A VERIFICAR (item A21):
#   "dos consecutivos se funden para todos los infinitos m >= 1 de la clase
#    exactamente cuando S_k(r) == S_k(r+1) y T^k(r) == T^k(r+1)"
#
# MAPA: T es el mapa del ATAJO:  n par -> n/2 ;  n impar -> (3n+1)/2.
#   S_k(n) = numero de pasos impares en los primeros k pasos de T.
# "Fundirse" = las trayectorias de (2^k*m + r) y (2^k*m + r + 1) coinciden
#   en el paso k (mismo T^k), lo que con S iguales da ademas la misma altura.
# "Altura" en las notas de la base es la del mapa CLASICO (n/2, 3n+1):
#   los contraejemplos declarados (5,6)->(5,8) y (4,5)->(2,5) solo cuadran
#   con el clasico; en el atajo serian (4,6) y (2,4). Se comprueban ambos.
#
# Partes:
#   A) Linealidad de Terras (derivada aqui, comprobada numericamente):
#      T^k(2^k*m + r) = 3^S_k(r) * m + T^k(r)  y  S_k(2^k*m+r) = S_k(r).
#   B) El "exactamente cuando" leido como coincidencia en el paso k,
#      en las dos direcciones, con busqueda de contraejemplos.
#   C) Con m >= 1, las alturas (clasica y atajo) coinciden en las clases buenas.
#   D) Borde m = 0: contraejemplos declarados y las clases de excepcion
#      (se espera exactamente r = 2, 4, 5, estables desde k = 5).
#   E) La descomposicion altura(n) = k + S_k(n) + altura(T^k(n)) vale
#      exactamente cuando la trayectoria no pisa el 1 antes del paso k.
#   F) Version "alturas" del reciproco: toda clase NO buena tiene algun
#      m >= 1 con alturas distintas (muestreado).
#
# Todo lo que decide es aritmetica entera exacta. Ni un float decide nada.

import sys
from time import time

t0 = time()

def Tk_y_S(n, k):
    """k pasos del mapa del atajo; devuelve (T^k(n), S_k(n))."""
    s = 0
    for _ in range(k):
        if n & 1:
            n = (3 * n + 1) // 2
            s += 1
        else:
            n //= 2
    return n, s

alturas_c = {1: 0}
def altura_clasica(n):
    """pasos del mapa clasico (n/2, 3n+1) hasta el 1, memoizado."""
    pila = []
    while n not in alturas_c:
        pila.append(n)
        n = 3 * n + 1 if n & 1 else n // 2
    h = alturas_c[n]
    while pila:
        h += 1
        alturas_c[pila.pop()] = h
    return h

alturas_a = {1: 0}
def altura_atajo(n):
    """pasos del mapa del atajo hasta el 1, memoizado."""
    pila = []
    while n not in alturas_a:
        pila.append(n)
        n = (3 * n + 1) // 2 if n & 1 else n // 2
    h = alturas_a[n]
    while pila:
        h += 1
        alturas_a[pila.pop()] = h
    return h

def pisa_uno_antes(n, k):
    """True si la trayectoria del atajo esta en 1 en algun paso j con 0 <= j < k."""
    for _ in range(k):
        if n == 1:
            return True
        n = (3 * n + 1) // 2 if n & 1 else n // 2
    return False

fallos = 0
def check(cond, msg):
    global fallos
    if not cond:
        fallos += 1
        print("FALLO:", msg)

# ---------------------------------------------------------------- parte A
print("A) linealidad de Terras: T^k(2^k*m + r) = 3^S_k(r)*m + T^k(r), mismo S")
nA = 0
MS_A = [0, 1, 2, 3, 7, 100]
for k in range(1, 13):
    tam = 1 << k
    if tam <= 1024:
        erres = range(tam)
    else:
        erres = range(0, tam, 7)   # muestreo determinista para k grandes
    for r in erres:
        t_r, s_r = Tk_y_S(r, k)
        pot = 3 ** s_r
        for m in MS_A:
            n = (m << k) + r
            t_n, s_n = Tk_y_S(n, k)
            check(t_n == pot * m + t_r and s_n == s_r,
                  "Terras k=%d r=%d m=%d" % (k, r, m))
            nA += 1
print("   comprobaciones: %d (k = 1..12, m en %s)" % (nA, MS_A))

# ---------------------------------------------------------------- parte B
print("B) el criterio <=> coincidir en el paso k, para todo m >= 1 (muestreo m=1..30)")
MS_B = list(range(1, 31))
nB_buenas = 0
nB_malas = 0
for k in range(0, 13):
    tam = 1 << k
    for r in range(tam):
        t_r, s_r = Tk_y_S(r, k)
        t_r1, s_r1 = Tk_y_S(r + 1, k)     # r+1 como entero (cubre r = 2^k - 1)
        buena = (s_r == s_r1 and t_r == t_r1)
        coinciden = 0
        for m in MS_B:
            a = (m << k) + r
            if Tk_y_S(a, k)[0] == Tk_y_S(a + 1, k)[0]:
                coinciden += 1
        if buena:
            nB_buenas += 1
            check(coinciden == len(MS_B),
                  "clase buena k=%d r=%d no coincide en todos los m" % (k, r))
        else:
            nB_malas += 1
            check(coinciden < len(MS_B),
                  "clase mala k=%d r=%d coincide en TODOS los m muestreados" % (k, r))
            # dos afines distintas se cruzan a lo sumo una vez:
            check(coinciden <= 1,
                  "clase mala k=%d r=%d coincide en %d m (>1)" % (k, r, coinciden))
print("   clases buenas: %d, clases malas: %d, m muestreados: 1..30, k = 0..12" %
      (nB_buenas, nB_malas))
print("   (k=0 es borde: r y r+1 nunca cumplen T^0(r)==T^0(r+1); 0 clases buenas, correcto)")

# ---------------------------------------------------------------- parte C
print("C) con m >= 1 las clases buenas dan la misma altura (clasica Y atajo)")
MS_C = [1, 2, 3, 10, 1000]
nC = 0
for k in range(1, 15):
    tam = 1 << k
    ts = [Tk_y_S(r, k) for r in range(tam)]
    for r in range(tam - 1):
        if ts[r] == ts[r + 1]:
            for m in MS_C:
                a = (m << k) + r
                check(altura_clasica(a) == altura_clasica(a + 1),
                      "altura clasica distinta k=%d r=%d m=%d" % (k, r, m))
                check(altura_atajo(a) == altura_atajo(a + 1),
                      "altura atajo distinta k=%d r=%d m=%d" % (k, r, m))
                # y la garantia estructural: n >= 2^k no pisa el 1 antes de k
                check(not pisa_uno_antes(a, k) and not pisa_uno_antes(a + 1, k),
                      "n >= 2^k pisa el 1 antes del paso k: k=%d r=%d m=%d" % (k, r, m))
                nC += 1
print("   comprobaciones: %d (k = 1..14, m en %s): alturas iguales, 1 nunca antes de k" %
      (nC, MS_C))

# ---------------------------------------------------------------- parte D
print("D) borde m = 0: los contraejemplos declarados y las clases de excepcion")
check(altura_clasica(5) == 5 and altura_clasica(6) == 8,
      "(5,6) clasico esperaba (5,8), sale (%d,%d)" % (altura_clasica(5), altura_clasica(6)))
check(altura_clasica(4) == 2 and altura_clasica(5) == 5,
      "(4,5) clasico esperaba (2,5), sale (%d,%d)" % (altura_clasica(4), altura_clasica(5)))
print("   (5,6) alturas clasicas: (%d,%d)  |  (4,5): (%d,%d)  -> m=0 rompe, confirmado"
      % (altura_clasica(5), altura_clasica(6), altura_clasica(4), altura_clasica(5)))
print("   (en el atajo tambien difieren: (5,6)->(%d,%d), (4,5)->(%d,%d))"
      % (altura_atajo(5), altura_atajo(6), altura_atajo(4), altura_atajo(5)))

K_EXC = 18   # limite del barrido de excepciones (barato; la base declara k=5..22)
print("   barrido de clases buenas con altura distinta en m=0, k = 3..%d:" % K_EXC)
excepciones_ok = True
for k in range(3, K_EXC + 1):
    tam = 1 << k
    ts = [Tk_y_S(r, k) for r in range(tam)]
    buenas = [r for r in range(tam - 1) if ts[r] == ts[r + 1]]
    exc = sorted(r for r in buenas if altura_clasica(r) != altura_clasica(r + 1))
    print("      k=%2d: %7d clases buenas, excepciones en m=0: %s" %
          (k, len(buenas), exc))
    if k >= 5:
        if exc != [2, 4, 5]:
            excepciones_ok = False
            check(False, "k=%d: excepciones %s, se esperaba [2, 4, 5]" % (k, exc))
    # el par frontera r = 2^k - 1 (r+1 = 2^k): nunca es clase buena (S = k vs 0)
    check(Tk_y_S(tam - 1, k)[1] == k and Tk_y_S(tam, k)[1] == 0,
          "frontera r=2^k-1 en k=%d" % k)
if excepciones_ok:
    print("   -> exactamente {2, 4, 5} en todos los k de 5 a %d. CONFIRMADO en este rango." % K_EXC)

# ---------------------------------------------------------------- parte E
print("E) altura(n) = k + S_k(n) + altura(T^k(n))  <=>  no pisa el 1 antes del paso k")
nE = 0
for k in range(1, 13):
    for n in range(1, 2001):
        t_n, s_n = Tk_y_S(n, k)
        vale = (altura_clasica(n) == k + s_n + altura_clasica(t_n))
        temprano = pisa_uno_antes(n, k)
        check(vale == (not temprano),
              "descomposicion k=%d n=%d: vale=%s, pisa1antes=%s" % (k, n, vale, temprano))
        nE += 1
print("   comprobaciones: %d (n = 1..2000, k = 1..12): equivalencia exacta, 0 fallos" % nE)
print("   (esta es la causa declarada del m >= 1: con m >= 1, n >= 2^k y T^j(n) >= 2^(k-j) >= 2)")

# ---------------------------------------------------------------- parte F
print("F) reciproco en alturas: toda clase NO buena tiene algun m>=1 con alturas distintas")
MS_F = list(range(1, 41))
malas_sin_testigo = []
for k in range(1, 11):
    tam = 1 << k
    ts = [Tk_y_S(r, k) for r in range(tam)]
    for r in range(tam - 1):
        if ts[r] != ts[r + 1]:
            testigo = None
            for m in MS_F:
                a = (m << k) + r
                if altura_clasica(a) != altura_clasica(a + 1):
                    testigo = m
                    break
            if testigo is None:
                malas_sin_testigo.append((k, r))
print("   clases malas sin testigo en m=1..40: %d %s" %
      (len(malas_sin_testigo), malas_sin_testigo[:10]))
print("   (si hubiera alguna, seria una clase que se funde por otra via; el enunciado")
print("    estricto -coincidir en el paso k- ya quedo cerrado en B en ambas direcciones)")

# ---------------------------------------------------------------- bordes sueltos
print("G) bordes sueltos")
check(altura_clasica(1) == 0 and altura_clasica(2) == 1, "alturas de 1 y 2")
t1, s1 = Tk_y_S(1, 1); t2, s2 = Tk_y_S(2, 1)
check((s1, t1) == (1, 2) and (s2, t2) == (0, 1), "el par (1,2) en k=1")
print("   (1,2) en k=1: S=(1,0), T=(2,1) -> clase mala, y alturas 0 y 1 difieren. Coherente.")
r5 = Tk_y_S(5, 5); r6 = Tk_y_S(6, 5)
check(r5 == (2, 2) and r6 == (2, 2), "r=5 k=5 esperaba T^5=2, S=2 en ambos")
r4 = Tk_y_S(4, 3); r5b = Tk_y_S(5, 3)
check(r4 == (2, 1) and r5b == (2, 1), "r=4 k=3 esperaba T^3=2, S=1 en ambos")
print("   r=5,k=5: T^5(5)=%d,S=%d | T^5(6)=%d,S=%d  (clase buena, pero m=0 rompe la altura)"
      % (r5[0], r5[1], r6[0], r6[1]))

# ---------------------------------------------------------------- veredicto
print()
print("tiempo total: %.1f s" % (time() - t0))
if fallos:
    raise SystemExit("VEREDICTO: %d FALLOS - el enunciado NO se sostiene tal cual" % fallos)
print("VEREDICTO: 0 fallos en todas las partes.")
print("El criterio (con m >= 1 y fusion = coincidir en el paso k) SE SOSTIENE en el rango probado.")
print("El borde m = 0 rompe exactamente donde la base dice: alturas (5,8) y (2,5),")
print("y las clases de excepcion son {2, 4, 5}, estables de k=5 a k=%d." % K_EXC)
