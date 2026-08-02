# A31 - verificacion independiente (agente 2, Python desde cero)
#
# ENUNCIADO: los evitados de la malla 2n mod 27 son exactamente los multiplos
# de 3, y predicen que rayos del arbol (inverso de Collatz) son mudos.
#
# Piezas que verifico, todas derivadas desde la definicion del mapa CLASICO
# (par -> n/2, impar -> 3n+1), sin abrir ningun fichero del repo:
#
# (1) La malla: iterar n -> 2n (mod 27) empezando en 1. Que residuos visita
#     y cuales evita. Afirmacion: evita exactamente {0,3,6,...,24}.
# (2) El arbol: un "rayo" es v, 2v, 4v, 8v, ... (doblar es el antecesor que
#     siempre existe). El rayo "brota" en 2^k*v si ese nodo tiene ADEMAS un
#     antecesor impar x con 3x+1 = 2^k*v (x entero, impar, positivo).
#     Derivo el brote SIN reglas mod 6: pruebo x = (m-1)/3 y compruebo con el
#     mapa clasico hacia adelante que 3x+1 == m y x impar.
#     Un rayo es MUDO si no brota en ningun k (verifico k = 0..60).
# (3) El cruce: para cada rayo impar v de una muestra, comparar
#         prediccion:  (v mod 27) esta en el conjunto evitado de la malla
#         realidad:    el rayo es mudo (medido en (2))
#     El enunciado dice que coinciden siempre.
#
# BORDES probados: v=1 (el rayo del tronco, brota en 4 y su hijo impar es el
# propio 1), v=3 (primer mudo), k=0 (el nodo impar de arranque), arranque de
# la malla en 0 y en 3 (orbitas degeneradas), y el limite de la muestra.
#
# Todo con enteros de Python. Ningun float decide nada.

fallos = []

# ---------- (1) la malla 2n mod 27 ----------
MOD = 27
visitados = set()
n = 1
for _ in range(200):          # de sobra: el ciclo mide como mucho 27
    n = (2 * n) % MOD
    visitados.add(n)
evitados = set(range(MOD)) - visitados

multiplos3 = {r for r in range(MOD) if r % 3 == 0}
print("malla 2n mod 27, arrancando en 1:")
print("  visitados (" + str(len(visitados)) + "):", sorted(visitados))
print("  evitados  (" + str(len(evitados)) + "):", sorted(evitados))
if evitados != multiplos3:
    fallos.append("los evitados NO son los multiplos de 3: " + str(sorted(evitados)))
else:
    print("  evitados == multiplos de 3 mod 27: OK (9 de 27)")

# largo del ciclo (orden de 2 mod 27)
n, largo = 1, 0
while True:
    n = (2 * n) % MOD
    largo += 1
    if n == 1:
        break
print("  largo del aro:", largo, "(debe ser 18 = 27 - 9)")
if largo != 18:
    fallos.append("el aro no mide 18: " + str(largo))

# borde: arrancar la malla en un multiplo de 3 se queda dentro de ellos
n = 3
orb3 = set()
for _ in range(100):
    n = (2 * n) % MOD
    orb3.add(n)
if not orb3 <= multiplos3:
    fallos.append("la orbita de 3 se sale de los multiplos de 3: " + str(sorted(orb3)))
else:
    print("  borde: la orbita que arranca en 3 queda dentro de los multiplos de 3 (por eso el enunciado exige arrancar fuera)")
# borde: 0 es punto fijo
if (2 * 0) % MOD != 0:
    fallos.append("0 no es punto fijo de 2n mod 27")

# ---------- (2) brotes del arbol, derivados del mapa clasico ----------
def paso_clasico(x):
    # el mapa clasico: par -> x/2, impar -> 3x+1
    return x // 2 if x % 2 == 0 else 3 * x + 1

def tiene_antecesor_impar(m):
    # existe x impar positivo con 3x+1 == m ?  (sin usar reglas mod 6)
    if (m - 1) % 3 != 0:
        return False
    x = (m - 1) // 3
    if x <= 0 or x % 2 == 0:
        return False
    # comprobacion por el mapa hacia adelante: un paso clasico de x da m
    if paso_clasico(x) != m:
        return False
    return True

def rayo_es_mudo(v, kmax=60):
    # el rayo v, 2v, 4v, ...: brota si algun 2^k*v tiene antecesor impar
    m = v
    for _k in range(kmax + 1):
        if tiene_antecesor_impar(m):
            return False, _k
        m = 2 * m
    return True, None

# control puntual de tiene_antecesor_impar contra fuerza bruta chica:
# para m = 1..2000, buscar x impar en 1..m con 3x+1 == m por bucle directo
for m in range(1, 2001):
    brute = any(3 * x + 1 == m for x in range(1, m + 1, 2))
    if brute != tiene_antecesor_impar(m):
        fallos.append("antecesor impar discrepa en m=" + str(m))
        break
else:
    print("control: antecesor impar contra fuerza bruta, m = 1..2000, 0 fallos")

# ---------- (3) el cruce: 200 rayos impares ----------
MUESTRA = 200          # los 200 primeros impares: v = 1, 3, 5, ..., 399
predichos_mudos = 0
medidos_mudos = 0
discrepancias = []
for i in range(MUESTRA):
    v = 2 * i + 1
    pred_mudo = (v % MOD) in evitados          # la prediccion de la malla
    mudo, k_brote = rayo_es_mudo(v)
    if pred_mudo:
        predichos_mudos += 1
    if mudo:
        medidos_mudos += 1
    if pred_mudo != mudo:
        discrepancias.append((v, pred_mudo, mudo))

print("rayos impares v = 1..399 (" + str(MUESTRA) + " rayos):")
print("  predichos mudos por la malla:", predichos_mudos)
print("  medidos mudos en el arbol   :", medidos_mudos)
print("  discrepancias               :", len(discrepancias))
if discrepancias:
    fallos.append("cruce malla-arbol discrepa: " + str(discrepancias[:5]))
if predichos_mudos != 67:
    fallos.append("los predichos mudos no son 67: " + str(predichos_mudos))

# bordes concretos del cruce
mudo1, k1 = rayo_es_mudo(1)
print("  borde v=1: mudo=", mudo1, " primer brote en k=", k1, " (nodo", 2**k1 if k1 is not None else "-", ")")
if mudo1:
    fallos.append("v=1 salio mudo y no debe (4 = 3*1+1 brota)")
mudo3, _ = rayo_es_mudo(3)
if not mudo3:
    fallos.append("v=3 salio con brote y debe ser mudo")
else:
    print("  borde v=3: mudo, como predice la malla")

# extension del rango: rayos impares grandes, cruzando la frontera de la muestra
extra_disc = 0
for v in list(range(399, 1001, 2)) + [99999, 100001, 3**7, 3**7 + 2]:
    pred_mudo = (v % MOD) in evitados
    mudo, _ = rayo_es_mudo(v)
    if pred_mudo != mudo:
        extra_disc += 1
        fallos.append("discrepancia extra en v=" + str(v))
print("  extension v = 399..999 impares + {99999, 100001, 3^7, 3^7+2}: discrepancias =", extra_disc)

# ---------- (4) la razon estructural, comprobada aparte ----------
# brote en 2^k*v exige (2^k*v - 1) % 3 == 0, o sea 2^k*v = 1 (mod 3).
# si 3|v eso es imposible (0 = 1 mod 3); si no, 2^k alterna 1,2 mod 3 y
# el brote llega en cuanto k tenga la paridad buena y k >= 1 (nodo par).
# comprobacion: para v impar no multiplo de 3, el primer brote esta en k <= 2.
peor_k = 0
for i in range(500):
    v = 2 * i + 1
    if v % 3 == 0:
        continue
    mudo, k = rayo_es_mudo(v, kmax=5)
    if mudo:
        fallos.append("v=" + str(v) + " no multiplo de 3 salio mudo con kmax=5")
    else:
        peor_k = max(peor_k, k)
print("primer brote de los no-multiplos de 3 (v impar < 1000): siempre k <=", peor_k)

# ---------- veredicto ----------
if fallos:
    for f in fallos:
        print("FALLO:", f)
    raise SystemExit("A31: " + str(len(fallos)) + " fallos")
print()
print("A31 SOSTIENE: evitados de la malla = multiplos de 3 (9 de 27, aro de largo 18),")
print("y la prediccion malla->arbol acierta en los 200 rayos (67 mudos) y en la extension.")
