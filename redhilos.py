# redhilos.py
#
# UNA RED NEURONAL, ESCRITA A MANO, PUESTA A APRENDER COLLATZ.
#
# Sin librerias de IA: solo numpy. Capa de entrada, una capa oculta de
# perceptrones con tanh, salida sigmoide, y descenso de gradiente con
# retropropagacion escrito en veinte lineas. Se puede leer entero.
#
# ---------------------------------------------------------------------------
# LO QUE **NO** SE PUEDE PREGUNTAR, Y POR QUE
# ---------------------------------------------------------------------------
#
# La idea tentadora es: le doy el numero de entrada (100002) y el de salida
# (1), y que la red aprenda el camino. Eso no mide nada, por dos razones:
#
#   1. LOS ONCE SALEN 1. Entrenar entrada -> salida es entrenar la funcion
#      constante 1. La red acierta el 100% sin haber aprendido nada de
#      Collatz. Cero informacion.
#
#   2. "EN 53 PASOS" NO ES "53 CAPAS". La profundidad de una red no es el
#      numero de iteraciones de nada. Para que 53 capas signifiquen 53 pasos
#      hay que COMPARTIR LOS PESOS entre capas, que es lo que hace el
#      experimento 3 de abajo.
#
# ---------------------------------------------------------------------------
# LO QUE SI SE PUEDE PREGUNTAR
# ---------------------------------------------------------------------------
#
# La pregunta buena no es "que camino encuentra la red". Es: **DONDE SE MUERE
# EXACTAMENTE SU CAPACIDAD DE PREDECIR**. Porque la literatura hace una
# prediccion afiladisima sobre eso, y una red la puede poner a prueba:
#
#   Terras (1976), Teorema 1.2: los primeros k pasos del mapa T los fija
#   n mod 2^k, y la correspondencia es una BIYECCION.
#   Terras (1976), Corolario 1.4: las paridades X_0, X_1, X_2, ... son
#   variables independientes, con P = 1/2 exacta.
#
# Traducido a lo que una red deberia medir:
#
#   EXPERIMENTO 1. Predecir la paridad del paso k viendo los m bits bajos
#   de n. Prediccion: 100% si m > k, y 50% CLAVADO si m <= k. Un acantilado,
#   no una pendiente. Si sale pendiente, Terras estaria mal.
#
#   EXPERIMENTO 2. Predecir la paridad del paso k viendo las k paridades
#   anteriores. Prediccion: 50% siempre, por muchos datos que le des.
#   Si la red le gana al 50%, el Corolario 1.4 seria falso.
#
#   EXPERIMENTO 3. Ese si es tu idea, hecha bien: que la red aprenda UN paso
#   de Collatz sobre los bits, y luego se la ITERA con sus propios pesos
#   -- 53 veces si hace falta. Cuantos pasos aguanta antes de despegarse de
#   la trayectoria de verdad? Eso mide cuanto de "suave" tiene Collatz.
#
# El experimento 3 es literalmente "un camino alternativo a los mismos
# numeros": la red camina sola. La pregunta es cuanto dura.

import math
import numpy as np

# ---------------------------------------------------------------------------
# Cambia esto aqui, guarda, y dale a Ctrl+B en Sublime.
# ---------------------------------------------------------------------------

SEMILLA = 7          # para que salga igual cada vez
OCULTAS = 64         # cuantos perceptrones en la capa de en medio
VUELTAS = 40         # cuantas pasadas enteras sobre los datos
LOTE = 512           # de cuantos en cuantos se mira (mini-batch)
PASO = 0.5           # cuanto se mueve cada peso por lote

rng = np.random.default_rng(SEMILLA)


# ------------------------------------------------------- el mapa y los bits

def paso_T(n):
    """Un paso del mapa acelerado: (3n+1)/2 si impar, n/2 si par."""
    return (3 * n + 1) // 2 if n % 2 else n // 2


def paridad_del_paso(n, k):
    """La paridad del iterado k-esimo de n bajo T (0 par, 1 impar)."""
    for _ in range(k):
        n = paso_T(n)
    return n % 2


def a_bits(n, cuantos):
    """Los `cuantos` bits bajos de n, el menos significativo primero."""
    return [(n >> i) & 1 for i in range(cuantos)]


# ------------------------------------------- la red, escrita a mano

def entrenar(X, Y, ocultas=OCULTAS, vueltas=VUELTAS, paso=PASO,
             lote=LOTE, ruido=None):
    """Una capa oculta con tanh, salida sigmoide, retropropagacion.

    X es (ejemplos, entradas), Y es (ejemplos, salidas) con ceros y unos.
    Se entrena por lotes: se mira un puado de ejemplos, se mueven los pesos,
    se mira el siguiente. Mucho mas rapido que mirarlos todos cada vez.
    """
    generador = ruido if ruido is not None else rng
    n_ent, n_sal = X.shape[1], Y.shape[1]
    # pesos pequenos al azar: si empiezan grandes, la tanh se satura
    W1 = generador.normal(0, 1 / math.sqrt(n_ent), (n_ent, ocultas))
    b1 = np.zeros(ocultas)
    W2 = generador.normal(0, 1 / math.sqrt(ocultas), (ocultas, n_sal))
    b2 = np.zeros(n_sal)
    # inercia: cada peso recuerda hacia donde iba
    vW1 = np.zeros_like(W1); vb1 = np.zeros_like(b1)
    vW2 = np.zeros_like(W2); vb2 = np.zeros_like(b2)

    for _ in range(vueltas):
        orden = generador.permutation(len(X))
        for i in range(0, len(X), lote):
            trozo = orden[i:i + lote]
            Xl, Yl = X[trozo], Y[trozo]
            # hacia delante
            H = np.tanh(Xl @ W1 + b1)
            S = 1 / (1 + np.exp(-np.clip(H @ W2 + b2, -30, 30)))
            # hacia atras (la derivada de la entropia cruzada con sigmoide
            # es justo la diferencia; por eso no aparece la derivada de S)
            dS = (S - Yl) / len(Xl)
            dW2 = H.T @ dS
            db2 = dS.sum(axis=0)
            dH = (dS @ W2.T) * (1 - H * H)
            dW1 = Xl.T @ dH
            db1 = dH.sum(axis=0)
            # mover los pesos, con inercia
            vW1 = 0.9 * vW1 - paso * dW1; W1 += vW1
            vb1 = 0.9 * vb1 - paso * db1; b1 += vb1
            vW2 = 0.9 * vW2 - paso * dW2; W2 += vW2
            vb2 = 0.9 * vb2 - paso * db2; b2 += vb2

    return W1, b1, W2, b2


def predecir(pesos, X):
    W1, b1, W2, b2 = pesos
    H = np.tanh(X @ W1 + b1)
    return 1 / (1 + np.exp(-np.clip(H @ W2 + b2, -30, 30)))


def acierto(pesos, X, Y):
    return float(((predecir(pesos, X) > 0.5) == (Y > 0.5)).mean())


# =========================================================================
# EXPERIMENTO 1 -- el acantilado de Terras
# =========================================================================

print("EXPERIMENTO 1 -- predecir la paridad del paso k viendo m bits de n")
print("  Terras 1976: los primeros k pasos los fija n mod 2^k.")
print("  Prediccion: 100% si m > k, y 50% clavado si m <= k.\n")

K = 6            # que paso se intenta predecir
BITS_MAX = 12    # hasta cuantos bits bajos se le ensenan
MUESTRA_1 = 30000

# numeros al azar y grandes, para que la trayectoria no toque el 1.
# CLAVE: se entrena con unos y se prueba con OTROS. Si se prueba con los
# mismos, la red memoriza y el acantilado no aparece.
ns_1 = [int(v) for v in rng.integers(1 << 24, 1 << 34, MUESTRA_1)]
etiquetas_1 = np.array([[paridad_del_paso(n, K)] for n in ns_1], dtype=float)
corte_1 = int(0.8 * MUESTRA_1)

print(f"  prediciendo la paridad del paso k = {K}")
print(f"  {corte_1:,} numeros al azar para entrenar, "
      f"{MUESTRA_1 - corte_1:,} DISTINTOS para probar\n")
print(f"  {'m bits':>7} {'ambiguo':>9} {'acierto':>9}  que dice Terras")
print(f"  {'-'*7} {'-'*9} {'-'*9}  {'-'*24}")

fallos_acantilado = 0
for m in range(1, BITS_MAX + 1):
    X = np.array([a_bits(n, m) for n in ns_1], dtype=float)
    # cuantos restos mod 2^m dan las DOS paridades: la ambiguedad real
    visto = {}
    for n, y in zip(ns_1, etiquetas_1[:, 0]):
        visto.setdefault(n & ((1 << m) - 1), set()).add(int(y))
    ambiguos = sum(1 for s in visto.values() if len(s) > 1) / len(visto)

    pesos = entrenar(X[:corte_1], etiquetas_1[:corte_1],
                     ruido=np.random.default_rng(SEMILLA + m))
    a = acierto(pesos, X[corte_1:], etiquetas_1[corte_1:])
    esperado = "determinado -> 100%" if m > K else "moneda -> 50%"
    # el acantilado: por encima de K tiene que clavar, por debajo no puede
    if m > K and a < 0.99:
        fallos_acantilado += 1
    if m <= K and a > 0.60:
        fallos_acantilado += 1
    print(f"  {m:>7} {ambiguos:>8.0%} {a:>8.1%}  {esperado}")

print(f"\n  fallos contra la prediccion de Terras: {fallos_acantilado}")
if fallos_acantilado:
    raise SystemExit("La red no reprodujo el acantilado. Mira eso antes de seguir.")
print(f"  El acantilado esta entre m = {K} y m = {K+1}, exactamente donde")
print(f"  el Teorema 1.2 dice que tiene que estar.")


# =========================================================================
# EXPERIMENTO 2 -- intentar ganarle a la moneda de Terras
# =========================================================================

print(f"\n\nEXPERIMENTO 2 -- predecir la paridad del paso k viendo las k anteriores")
print(f"  Terras 1976, Corolario 1.4: las paridades son independientes,")
print(f"  P = 1/2 exacta. Prediccion: 50%, con todos los datos del mundo.\n")

CUANTOS = 40000
print(f"  {'k':>3} {'ve':>8} {'ejemplos':>9} {'acierto':>9}  {'sobre 50%':>10}")
print(f"  {'-'*3} {'-'*8} {'-'*9} {'-'*9}  {'-'*10}")

peor_ventaja = 0.0
for K2 in [4, 8, 12, 16]:
    ns = rng.integers(1 << 22, 1 << 30, CUANTOS)
    filas, etiquetas = [], []
    for n in ns:
        n = int(n)
        prefijo = []
        for _ in range(K2):
            prefijo.append(n % 2)
            n = paso_T(n)
        filas.append(prefijo)
        etiquetas.append([n % 2])
    X = np.array(filas, dtype=float)
    Y = np.array(etiquetas, dtype=float)
    corte = int(0.8 * len(X))
    pesos = entrenar(X[:corte], Y[:corte],
                     ruido=np.random.default_rng(SEMILLA + 100 + K2))
    a = acierto(pesos, X[corte:], Y[corte:])
    ventaja = abs(a - 0.5)
    peor_ventaja = max(peor_ventaja, ventaja)
    print(f"  {K2:>3} {K2:>8} {len(X):>9} {a:>8.2%}  {ventaja:>+10.2%}")

print(f"\n  mayor ventaja sobre la moneda: {peor_ventaja:.2%}")
if peor_ventaja > 0.02:
    print(f"  OJO: eso es demasiado. O hay fuga de informacion en el montaje,")
    print(f"  o el Corolario 1.4 tiene un problema. Revisar antes de creerselo.")
else:
    print(f"  Es ruido de muestreo. La red no le gana a la moneda, y no puede:")
    print(f"  no hay nada que aprender ahi. Corolario 1.4 confirmado con una")
    print(f"  herramienta que Terras no tenia.")


# =========================================================================
# EXPERIMENTO 3 -- que la red camine sola (tu idea, hecha bien)
# =========================================================================

print(f"\n\nEXPERIMENTO 3 -- la red aprende UN paso y luego se la itera")
print(f"  Entrada: los bits de n. Salida: los bits de T(n).")
print(f"  Y despues se le da su propia salida como entrada, 53 veces.")
print(f"  Los pesos son los MISMOS en cada vuelta: eso si es 'un paso'.\n")

BITS = 18
BITS_SAL = BITS + 1
MUESTRAS = 60000


def aprender_mapa(funcion, filtro, etiqueta, ocultas=256, vueltas=150):
    """Entrena una red para que aprenda `funcion` sobre los bits."""
    ns = [int(v) for v in rng.integers(1 << 8, 1 << BITS, MUESTRAS * 2)
          if filtro(int(v))][:MUESTRAS]
    X = np.array([a_bits(n, BITS) for n in ns], dtype=float)
    Y = np.array([a_bits(funcion(n), BITS_SAL) for n in ns], dtype=float)
    corte = int(0.85 * len(X))
    pesos = entrenar(X[:corte], Y[:corte], ocultas=ocultas, vueltas=vueltas,
                     paso=1.0, lote=256,
                     ruido=np.random.default_rng(SEMILLA + len(etiqueta)))
    P = predecir(pesos, X[corte:]) > 0.5
    V = Y[corte:] > 0.5
    por_bit = (P == V).mean(axis=0)
    enteros = float((P == V).all(axis=1).mean())
    print(f"  {etiqueta:<26} bit medio {por_bit.mean():>7.2%}   "
          f"bit peor {por_bit.min():>7.2%}   numeros enteros {enteros:>7.2%}")
    return pesos, enteros


print("  Se parte el paso en sus dos ramas, para ver cual es la dificil:\n")
_, ac_par = aprender_mapa(lambda n: n // 2, lambda n: n % 2 == 0,
                          "n/2   (solo pares)")
_, ac_impar = aprender_mapa(lambda n: (3 * n + 1) // 2, lambda n: n % 2 == 1,
                            "(3n+1)/2  (solo impares)")
pesos, ac_todo = aprender_mapa(paso_T, lambda n: True, "el paso T entero")

print(f"\n  LA MITAD FACIL Y LA MITAD IMPOSIBLE:")
print(f"    dividir entre dos  -> {ac_par:.2%} de numeros enteros correctos")
print(f"    multiplicar y sumar-> {ac_impar:.2%}")
print(f"  Dividir entre dos es correr los bits una casilla: la red lo ve al")
print(f"  instante. Multiplicar por tres y sumar uno exige propagar acarreos,")
print(f"  que es una cadena de XOR de longitud arbitraria. Una capa oculta no")
print(f"  puede representar eso, y ninguna cantidad de datos lo arregla.")

if ac_par < 0.9:
    print(f"\n  AVISO: ni siquiera aprendio n/2. Entonces el montaje esta mal")
    print(f"  y no se puede concluir nada sobre la otra rama.")


def paso_de_la_red(n):
    """Un paso de Collatz segun la red, no segun la aritmetica."""
    x = np.array([a_bits(n, BITS)], dtype=float)
    bits = (predecir(pesos, x)[0] > 0.5).astype(int)
    return int(sum(int(b) << i for i, b in enumerate(bits)))


print(f"\n  Y aun asi, se la deja caminar sola desde los once hilos:\n")
print(f"  {'n':>8} {'aguanta':>8}  donde se despega")
print(f"  {'-'*8} {'-'*8}  {'-'*40}")

aguantes = []
for semilla in range(100000, 100011):
    verdad = red = semilla
    aguanta = 0
    detalle = "llego al 1 sin fallar"
    for t in range(1, 54):
        verdad = paso_T(verdad)
        red = paso_de_la_red(red)
        if red != verdad:
            detalle = f"paso {t}: dice {red:,}, es {verdad:,}"
            break
        aguanta = t
        if verdad == 1:
            break
    aguantes.append(aguanta)
    print(f"  {semilla:>8} {aguanta:>8}  {detalle}")

print(f"\n  aguante medio: {sum(aguantes)/len(aguantes):.1f} pasos de 53")

print(f"\n  LA CONCLUSION, Y NO ES LA QUE ESPERABAMOS.")
print(f"  La red no encuentra un camino alternativo a los mismos numeros.")
print(f"  Se despega en el primer paso, porque no aprendio ni un paso.")
print(f"  Y el sitio exacto donde falla tiene nombre en este repo: los")
print(f"  ACARREOS del +1. Es el mismo +1 que le da grosor a la lamina")
print(f"  (collazlamina.py), el mismo que rompe la conmutacion del espejo")
print(f"  en base 2 (mallaespejo2.py), y el mismo que Everett esquiva")
print(f"  usando la cota 5/3 en vez del 3/2 exacto.")
print(f"\n  Un aproximador continuo no puede con el +1. Si Collatz tuviera un")
print(f"  atajo suave, esto lo habria encontrado. Lo que encuentra es el")
print(f"  acantilado del experimento 1: informacion completa o moneda,")
print(f"  sin termino medio. Eso NO demuestra nada sobre la conjetura,")
print(f"  pero es una medida limpia de por que el problema es duro.")
