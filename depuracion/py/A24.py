# A24 - verificacion independiente (agente 2, Python desde cero)
#
# ENUNCIADO: (8k+4, 8k+5) confluyen siempre en 3 pasos para todo k >= 0,
#            y tienen la MISMA ALTURA para todo k >= 1.
#
# MAPA USADO: el CLASICO (n par -> n/2 ; n impar -> 3n+1).
#   Lo delata la propia base: altura(4)=2 y altura(5)=5 solo salen con el
#   mapa clasico (4->2->1 son 2 pasos; 5->16->8->4->2->1 son 5).
#   "Altura" = numero de pasos del mapa clasico hasta llegar a 1.
#
# Todo con enteros de Python. Ningun float decide nada.

import sys

def paso(n):
    # mapa clasico
    if n % 2 == 0:
        return n // 2
    return 3 * n + 1

def altura(n, memo={1: 0}):
    # pasos clasicos hasta 1
    cadena = []
    while n not in memo:
        cadena.append(n)
        n = paso(n)
    h = memo[n]
    for x in reversed(cadena):
        h += 1
        memo[x] = h
    return memo[cadena[0]] if cadena else h

fallos = 0

# ---------------------------------------------------------------
# PARTE 0: demostracion algebraica de la confluencia, valida para
# TODO k >= 0 a la vez. Represento n = a*k + b (a, b enteros) y solo
# aplico el mapa cuando la paridad queda decidida por (a, b) para
# todo k: hace falta a par (entonces la paridad es la de b).
# ---------------------------------------------------------------

def paso_lineal(a, b):
    # devuelve (a', b', tipo) o corta si la paridad no es uniforme en k
    if a % 2 != 0:
        raise SystemExit("paridad no uniforme: a impar, el argumento algebraico no aplica")
    if b % 2 == 0:
        if a % 2 != 0 or b % 2 != 0 and False:
            pass
        # par para todo k: dividir. a/2 debe ser entero (a par).
        return a // 2, b // 2, 'P'
    else:
        return 3 * a, 3 * b + 1, 'I'

forma1 = (8, 4)
forma2 = (8, 5)
tipos1 = []
tipos2 = []
f1 = forma1
f2 = forma2
for _ in range(3):
    a, b, t = paso_lineal(*f1)
    f1 = (a, b)
    tipos1.append(t)
for _ in range(3):
    a, b, t = paso_lineal(*f2)
    f2 = (a, b)
    tipos2.append(t)

print("algebra: 8k+4 -> pasos", "".join(tipos1), "-> forma", f1)
print("algebra: 8k+5 -> pasos", "".join(tipos2), "-> forma", f2)

if f1 != (6, 4) or f2 != (6, 4):
    fallos += 1
    print("FALLO: las formas finales no son 6k+4 en los dos lados")
if sorted(tipos1) != ['I', 'P', 'P'] or sorted(tipos2) != ['I', 'P', 'P']:
    fallos += 1
    print("FALLO: no gastan 2 pares y 1 impar cada uno")
else:
    print("algebra: cada lado gasta 2 pares y 1 impar -> confluencia en 6k+4,")
    print("         demostrada para todo k >= 0 (paridades uniformes en k)")

# ---------------------------------------------------------------
# PARTE 1: confluencia por fuerza bruta, k = 0 .. 200000
#   T^3(8k+4) == T^3(8k+5) == 6k+4, exactamente en el paso 3.
# ---------------------------------------------------------------
K_CONF = 200000
peor = None
for k in range(0, K_CONF + 1):
    x = 8 * k + 4
    y = 8 * k + 5
    for _ in range(3):
        x = paso(x)
        y = paso(y)
    if not (x == y == 6 * k + 4):
        fallos += 1
        if peor is None:
            peor = k
            print("FALLO confluencia en k =", k, ":", x, y, "esperado", 6 * k + 4)
print("confluencia bruta: k = 0 ..", K_CONF, "->",
      "0 fallos" if peor is None else "FALLOS")

# comprobacion de que NO confluyen antes del paso 3 (en general):
antes = 0
for k in range(0, 1000 + 1):
    x = 8 * k + 4
    y = 8 * k + 5
    coincide_antes = False
    for i in range(1, 3):
        x = paso(x)
        y = paso(y)
        if x == y:
            coincide_antes = True
    if coincide_antes:
        antes += 1
print("pares (k<=1000) que ya coinciden en el paso 1 o 2:", antes)

# ---------------------------------------------------------------
# PARTE 2: misma altura. Bordes primero.
# ---------------------------------------------------------------
h4 = altura(4)
h5 = altura(5)
print("borde k=0: altura(4) =", h4, ", altura(5) =", h5,
      "->", "IGUALES" if h4 == h5 else "DISTINTAS (contraejemplo del k>=0)")
if h4 == h5:
    fallos += 1
    print("FALLO: se esperaba que k=0 fuera contraejemplo de la altura")

# k = 1 explicito
h12 = altura(12)
h13 = altura(13)
print("borde k=1: altura(12) =", h12, ", altura(13) =", h13)
if h12 != h13:
    fallos += 1
    print("FALLO: k=1 rompe el enunciado")

# barrido k = 1 .. 20000
K_ALT = 20000
malos = []
for k in range(1, K_ALT + 1):
    if altura(8 * k + 4) != altura(8 * k + 5):
        malos.append(k)
if malos:
    fallos += 1
    print("FALLO altura: k =", malos[:10])
print("altura: k = 1 ..", K_ALT, "->", len(malos), "fallos")

# ---------------------------------------------------------------
# PARTE 3: por que k=0 falla y k>=1 no.
#   La confluencia en el paso 3 solo garantiza misma altura si ninguna
#   de las dos trayectorias toca el 1 ANTES del paso 3. Con k >= 1,
#   8k+4 >= 12 y cada paso divide a lo sumo entre 2, asi que en los
#   pasos 0,1,2 el valor es >= 12/4 = 3 > 1: no puede haber tocado el 1.
#   Con k = 0, el 4 llega al 1 en el paso 2, antes de la cita.
# ---------------------------------------------------------------
x = 4
traza = [x]
for _ in range(3):
    x = paso(x)
    traza.append(x)
print("traza de 4:", traza, "-> toca el 1 en el paso 2, antes del paso 3")
minimo = min(8 * 1 + 4 // 4, 3)  # solo informativo
print("con k >= 1: 8k+4 >= 12, y T^j(n) >= n/2^j >= 3 > 1 para j < 3 ->")
print("  ninguna de las dos toca el 1 antes de confluir; la altura comun")
print("  es 3 + altura(6k+4) en los dos lados.")

# verificacion numerica de esa descomposicion, k = 1..5000:
desc = 0
for k in range(1, 5001):
    if altura(8 * k + 4) != 3 + altura(6 * k + 4):
        desc += 1
    if altura(8 * k + 5) != 3 + altura(6 * k + 4):
        desc += 1
if desc:
    fallos += 1
print("descomposicion altura = 3 + altura(6k+4): k = 1..5000 ->", desc, "fallos")

# ---------------------------------------------------------------
print()
if fallos == 0:
    print("VEREDICTO: 0 fallos. El enunciado tal como esta escrito SE SOSTIENE:")
    print("  - confluencia en 3 pasos: para todo k >= 0 (algebra + 200001 casos)")
    print("  - misma altura: para todo k >= 1 (20000 casos, 0 fallos),")
    print("    y k = 0 es contraejemplo real de la version sin recorte (2 vs 5)")
else:
    raise SystemExit("HUBO FALLOS: revisar arriba")
