# guardarmallas.py
#
# GUARDAR LAS MALLAS EN DISCO.
#
# Este es el paso 2 del plan original del laboratorio, el unico que faltaba:
# "haremos varias y las guardaremos". Hasta ahora todos los programas eran de
# un solo uso -- calculaban la malla, dibujaban el .html, y al cerrar el
# navegador no quedaba nada. El .html ademas esta en .gitignore, asi que ni
# eso sobrevivia.
#
# Aqui se calculan ONCE mallas circulares, ninguna de Collatz, y cada una se
# escribe en mallas/<nombre>.json. Eso es lo que despues se podra cruzar
# contra los numeros que genera Collatz sin volver a calcular nada.
#
# QUE ES UNA MALLA GUARDADA. Un aro de numeros, con su tamano y con lo que
# deja fuera:
#
#   orbita     el anillo en orden, empezando por el arranque
#   aro        cuantos numeros mide el anillo
#   cola       cuantos pasos tarda el arranque en entrar al anillo
#   visitados  los numeros que el anillo pisa, ordenados
#   evitados   los del 0 al modulo-1 que NO pisa   <- esto es lo que cruza
#
# LO QUE SE MIDE, NO SE SUPONE. De cada regla se recorre el espacio ENTERO
# (todos los estados posibles, no solo el arranque) y se parte en ciclos y
# colas. De ahi sale el unico juicio que importa:
#
#   cierra_limpio = (la cola mas larga de todo el espacio es 0)
#
# O sea: la regla cierra limpio si y solo si es una biyeccion, si todo estado
# esta en un anillo y nada se queda colgando en una cola. n -> n+k y n -> 2n
# (con el modulo adecuado) lo son; n -> n^2 no, y por eso hace renacuajos.
#
# EL FILTRO DE SIEMPRE. Once mallas tienen que dar cierres DISTINTOS, o la
# maquinaria no esta midiendo la regla sino a si misma. Se comprueba y se
# imprime cuantos tamanos distintos salieron.
#
# Y CUATRO COMPROBACIONES ANTES DE DAR NADA POR GUARDADO:
#
#   1. cada aro medido coincide con la formula que le toca
#   2. los cierres salen distintos entre si (discriminacion)
#   3. IDA Y VUELTA: cada archivo se vuelve a leer del disco y tiene que
#      salir identico a lo calculado. Guardar mal es peor que no guardar
#   4. el cruce contra Collatz que ya estaba verificado: los evitados de
#      2n (mod 27) tienen que ser exactamente los multiplos de 3, que son
#      los rayos mudos del arbol (mallascerradas.py)
#
# Si alguna falla el programa se para y no deja archivos a medias.

import os
import json
import math

# ---------------------------------------------------------------------------
# Cambia esto aqui, guarda, y dale a Ctrl+B en Sublime.
# ---------------------------------------------------------------------------

CARPETA = "mallas"      # donde se escriben los .json
ORBITA_MAXIMA = 400     # si el anillo es mas largo que esto, se guarda cortado


# --------------------------------------------------- recorrer el espacio

def descomponer_espacio(estados, paso):
    """Recorre TODOS los estados y los reparte en anillos.

    Devuelve (ciclos, cola_de): la lista de anillos encontrados, y cuantos
    pasos tarda cada estado en meterse en el suyo (0 si ya esta dentro).
    """
    ciclo_de = {}       # estado -> en que anillo termina
    cola_de = {}        # estado -> cuantos pasos tarda en llegar
    ciclos = []

    for inicio in estados:
        if inicio in ciclo_de:
            continue

        # caminar hasta pisar algo ya conocido
        camino = []
        posicion = {}
        actual = inicio
        while actual not in posicion and actual not in ciclo_de:
            posicion[actual] = len(camino)
            camino.append(actual)
            actual = paso(actual)

        if actual in ciclo_de:
            # el camino desemboca en un anillo que ya conociamos
            indice = ciclo_de[actual]
            distancia = cola_de[actual]
        else:
            # anillo nuevo: empieza donde nos repetimos
            corte = posicion[actual]
            indice = len(ciclos)
            ciclos.append(camino[corte:])
            for estado in camino[corte:]:
                ciclo_de[estado] = indice
                cola_de[estado] = 0
            camino = camino[:corte]
            distancia = 0

        # y hacia atras, cada paso del camino esta uno mas lejos
        for i in range(len(camino) - 1, -1, -1):
            distancia += 1
            ciclo_de[camino[i]] = indice
            cola_de[camino[i]] = distancia

    return ciclos, cola_de


def caminar_desde(arranque, paso):
    """La cola y el aro contados desde un arranque concreto."""
    visto = {}
    estado = arranque
    i = 0
    while estado not in visto:
        visto[estado] = i
        estado = paso(estado)
        i += 1
    return visto[estado], i - visto[estado]


def orbita_desde(arranque, paso, cola, aro):
    """El anillo en orden: se salta la cola y se da una vuelta entera."""
    estado = arranque
    for _ in range(cola):
        estado = paso(estado)
    anillo = []
    for _ in range(min(aro, ORBITA_MAXIMA)):
        anillo.append(estado)
        estado = paso(estado)
    return anillo


# --------------------------------------------------------- las once mallas
#
# Cada una trae: nombre de archivo, la regla en texto, el modulo, la lista de
# estados posibles, la funcion de un paso, como se lee el numero visible de un
# estado (los Fibonacci llevan pareja (a, b) y el numero es el primero), el
# arranque, y el aro que dice la formula (None si no hay formula).

def estados_sueltos(m):
    return list(range(m))


def estados_en_pareja(m):
    return [(a, b) for a in range(m) for b in range(m)]


CATALOGO = [
    # -- sumar de k en k: la formula es m / mcd(m, k)
    dict(nombre="sumar7-mod30", regla="n -> n+7 (mod 30)", modulo=30,
         estados=estados_sueltos(30), paso=lambda n: (n + 7) % 30,
         salida=lambda e: e, arranque=0,
         aro_esperado=30 // math.gcd(30, 7),
         formula="m / mcd(m, k) = 30 / mcd(30, 7)"),

    dict(nombre="sumar6-mod30", regla="n -> n+6 (mod 30)", modulo=30,
         estados=estados_sueltos(30), paso=lambda n: (n + 6) % 30,
         salida=lambda e: e, arranque=0,
         aro_esperado=30 // math.gcd(30, 6),
         formula="m / mcd(m, k) = 30 / mcd(30, 6)"),

    dict(nombre="sumar1-mod12", regla="n -> n+1 (mod 12)", modulo=12,
         estados=estados_sueltos(12), paso=lambda n: (n + 1) % 12,
         salida=lambda e: e, arranque=0,
         aro_esperado=12,
         formula="m / mcd(m, k) = 12 / mcd(12, 1)"),

    # -- Fibonacci: el estado es la pareja (a, b) y el numero visible es a
    dict(nombre="fibonacci-mod10", regla="Fibonacci (mod 10)", modulo=10,
         estados=estados_en_pareja(10),
         paso=lambda p: (p[1], (p[0] + p[1]) % 10),
         salida=lambda e: e[0], arranque=(0, 1),
         aro_esperado=60,
         formula="el periodo de Pisano de 10"),

    dict(nombre="fibonacci-mod100", regla="Fibonacci (mod 100)", modulo=100,
         estados=estados_en_pareja(100),
         paso=lambda p: (p[1], (p[0] + p[1]) % 100),
         salida=lambda e: e[0], arranque=(0, 1),
         aro_esperado=300,
         formula="el periodo de Pisano de 100"),

    # -- doblar modulo 3^j: la formula es 2 por 3^(j-1). El de 27 es la rueda
    #    maestra del arbol de Collatz; el de 81 es el siguiente engranaje.
    dict(nombre="duplicar-mod3", regla="n -> 2n (mod 3)", modulo=3,
         estados=estados_sueltos(3), paso=lambda n: (2 * n) % 3,
         salida=lambda e: e, arranque=1,
         aro_esperado=2,
         formula="el orden de 2 modulo 3^j = 2*3^(j-1), con j = 1"),

    dict(nombre="duplicar-mod9", regla="n -> 2n (mod 9)", modulo=9,
         estados=estados_sueltos(9), paso=lambda n: (2 * n) % 9,
         salida=lambda e: e, arranque=1,
         aro_esperado=6,
         formula="el orden de 2 modulo 3^j = 2*3^(j-1), con j = 2"),

    dict(nombre="duplicar-mod27", regla="n -> 2n (mod 27)", modulo=27,
         estados=estados_sueltos(27), paso=lambda n: (2 * n) % 27,
         salida=lambda e: e, arranque=1,
         aro_esperado=18,
         formula="el orden de 2 modulo 3^j = 2*3^(j-1), con j = 3"),

    dict(nombre="duplicar-mod81", regla="n -> 2n (mod 81)", modulo=81,
         estados=estados_sueltos(81), paso=lambda n: (2 * n) % 81,
         salida=lambda e: e, arranque=1,
         aro_esperado=54,
         formula="el orden de 2 modulo 3^j = 2*3^(j-1), con j = 4"),

    # -- triplicar: otro orden multiplicativo, para que no todo sea doblar
    dict(nombre="triplicar-mod10", regla="n -> 3n (mod 10)", modulo=10,
         estados=estados_sueltos(10), paso=lambda n: (3 * n) % 10,
         salida=lambda e: e, arranque=1,
         aro_esperado=4,
         formula="el orden de 3 modulo 10"),

    # -- y la que NO cierra limpio, que se guarda igual porque el negativo
    #    tambien es dato: sin ella la coleccion no discriminaria nada.
    dict(nombre="cuadrado-mod100", regla="n -> n^2 (mod 100)", modulo=100,
         estados=estados_sueltos(100), paso=lambda n: (n * n) % 100,
         salida=lambda e: e, arranque=2,
         aro_esperado=None,
         formula="ninguna: no es biyeccion, hace renacuajos (cola + aro)"),
]


# ------------------------------------------------------------ calcularlas

print("CALCULANDO LAS MALLAS\n")

guardadas = []
fallos_formula = 0

for receta in CATALOGO:
    paso = receta["paso"]
    salida = receta["salida"]

    # el espacio entero, para saber si la regla cierra limpio de verdad
    ciclos, cola_de = descomponer_espacio(receta["estados"], paso)
    cola_maxima = max(cola_de.values())
    cierra_limpio = (cola_maxima == 0)

    # y el anillo del arranque, que es la malla que se guarda
    cola, aro = caminar_desde(receta["arranque"], paso)
    anillo = orbita_desde(receta["arranque"], paso, cola, aro)
    numeros = [salida(estado) for estado in anillo]
    visitados = sorted(set(numeros))
    pisados = set(visitados)
    evitados = [n for n in range(receta["modulo"]) if n not in pisados]

    # COMPROBACION 1: el aro medido tiene que ser el de la formula
    esperado = receta["aro_esperado"]
    if esperado is not None and aro != esperado:
        print(f"  FALLO en {receta['nombre']}: aro medido {aro},"
              f" la formula dice {esperado}")
        fallos_formula += 1

    malla = {
        "nombre": receta["nombre"],
        "regla": receta["regla"],
        "modulo": receta["modulo"],
        "arranque": str(receta["arranque"]),
        "cierra_limpio": cierra_limpio,
        "cola": cola,
        "aro": aro,
        "formula": receta["formula"],
        "orbita": numeros,
        "orbita_cortada": aro > ORBITA_MAXIMA,
        "visitados": visitados,
        "evitados": evitados,
        "espacio_completo": {
            "estados": len(receta["estados"]),
            "anillos": len(ciclos),
            "largos_de_anillo": sorted({len(c) for c in ciclos}),
            "cola_maxima": cola_maxima,
        },
    }
    guardadas.append(malla)

    marca = "cierra limpio" if cierra_limpio else "RENACUAJOS"
    print(f"  {receta['nombre']:<18} aro {aro:>4}   cola {cola}   "
          f"{len(ciclos):>3} anillos en el espacio   {marca}")

if fallos_formula:
    raise SystemExit("Algun aro no dio lo que dice su formula. No se guarda nada.")

print(f"\nCOMPROBACION 1 -- los {len(guardadas)} aros coinciden con su formula: 0 fallos")


# COMPROBACION 2: el filtro. Los cierres tienen que salir distintos.
tamanos = sorted({m["aro"] for m in guardadas})
print(f"\nCOMPROBACION 2 -- la maquinaria discrimina")
print(f"  tamanos de aro distintos: {len(tamanos)} de {len(guardadas)} mallas")
print(f"  {tamanos}")
if len(tamanos) < 5:
    raise SystemExit("Casi todas dan el mismo aro. La coleccion no mide nada.")


# ------------------------------------------------------------- escribirlas

if not os.path.isdir(CARPETA):
    os.makedirs(CARPETA)

escritos = []
for malla in guardadas:
    ruta = os.path.join(CARPETA, malla["nombre"] + ".json")
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(malla, archivo, ensure_ascii=False, indent=2)
    escritos.append(ruta)

# el indice, para que un programa futuro sepa que hay sin abrir once archivos
indice = {
    "que_es": "mallas circulares cerradas, ninguna de Collatz, "
              "para cruzarlas despues contra los numeros que genera Collatz",
    "generado_por": "guardarmallas.py",
    "mallas": [
        {
            "nombre": m["nombre"],
            "regla": m["regla"],
            "modulo": m["modulo"],
            "aro": m["aro"],
            "cierra_limpio": m["cierra_limpio"],
            "archivo": m["nombre"] + ".json",
        }
        for m in guardadas
    ],
}
ruta_indice = os.path.join(CARPETA, "indice.json")
with open(ruta_indice, "w", encoding="utf-8") as archivo:
    json.dump(indice, archivo, ensure_ascii=False, indent=2)

print(f"\nESCRITAS {len(escritos)} mallas en la carpeta {CARPETA}/ (mas indice.json)")


# COMPROBACION 3: ida y vuelta. Se leen del disco y tienen que salir iguales.

fallos_vuelta = 0
for malla in guardadas:
    ruta = os.path.join(CARPETA, malla["nombre"] + ".json")
    with open(ruta, "r", encoding="utf-8") as archivo:
        leida = json.load(archivo)
    if leida != malla:
        print(f"  FALLO de ida y vuelta en {malla['nombre']}")
        fallos_vuelta += 1

print(f"\nCOMPROBACION 3 -- ida y vuelta: {len(guardadas)} archivos releidos del"
      f" disco, {fallos_vuelta} fallos")
if fallos_vuelta:
    raise SystemExit("Lo guardado no coincide con lo calculado. No sirve.")


# COMPROBACION 4: el cruce contra Collatz, leyendo del disco y no de memoria.
#
# En mallascerradas.py quedo verificado que un rayo del arbol (v, 2v, 4v, ...)
# no brota nunca si v es multiplo de 3. La malla de 2n (mod 27) se calculo sin
# mirar Collatz ni una vez. Sus evitados tienen que ser justo esos multiplos.

with open(os.path.join(CARPETA, "duplicar-mod27.json"), "r",
          encoding="utf-8") as archivo:
    rueda = json.load(archivo)

multiplos_de_3 = [n for n in range(27) if n % 3 == 0]

print(f"\nCOMPROBACION 4 -- el cruce contra Collatz, leido del disco")
print(f"  la malla {rueda['nombre']} evita: {rueda['evitados']}")
print(f"  los multiplos de 3 menores que 27: {multiplos_de_3}")
if rueda["evitados"] != multiplos_de_3:
    raise SystemExit("La rueda guardada no evita los multiplos de 3. No sigas.")

# y ahora se usa el archivo para predecir el arbol: un rayo es mudo si y solo
# si su semilla cae en un numero que la malla evita
def rayo_brota(v, k_max=30):
    w = v
    for _ in range(k_max):
        w = w * 2
        if w % 6 == 4:
            return True
    return False


evitados = set(rueda["evitados"])
fallos_prediccion = 0
mudos_predichos = 0
for v in range(1, 400, 2):
    predice_mudo = (v % 27) in evitados      # lo que dice el archivo
    es_mudo = not rayo_brota(v)              # lo que hace el arbol de verdad
    if predice_mudo:
        mudos_predichos += 1
    if predice_mudo != es_mudo:
        fallos_prediccion += 1

print(f"  usando SOLO el archivo, se predice que {mudos_predichos} de los 200"
      f" rayos impares son mudos")
print(f"  contra el arbol de verdad: {fallos_prediccion} fallos")
if fallos_prediccion:
    raise SystemExit("La malla guardada no predice el arbol. No sigas.")


# -------------------------------------------------------------- el listado

print(f"\nLAS MALLAS QUE QUEDAN EN DISCO\n")
print(f"  {'archivo':<24} {'regla':<24} {'aro':>5}  {'cierra':<7} evita")
print(f"  {'-' * 24} {'-' * 24} {'-' * 5}  {'-' * 7} {'-' * 20}")
for malla in guardadas:
    evita = len(malla["evitados"])
    print(f"  {malla['nombre'] + '.json':<24} {malla['regla']:<24}"
          f" {malla['aro']:>5}  {'si' if malla['cierra_limpio'] else 'NO':<7}"
          f" {evita} de {malla['modulo']} numeros")

print(f"\n  Once mallas circulares en disco, ninguna calculada con Collatz,")
print(f"  con {len(tamanos)} tamanos de cierre distintos. Ya no hay que")
print(f"  recalcularlas: se abren con json.load y se cruzan.")
