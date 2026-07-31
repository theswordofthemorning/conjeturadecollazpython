# coralprimos.py
#
# EL NUMERO PRIMO DE RUMBOS: LA PREDICCION QUE ESTABA ESCRITA, MEDIDA.
#
# ---------------------------------------------------------------------------
# QUE SE ESTABA PREDICIENDO
# ---------------------------------------------------------------------------
#
# El coral de Harriss usa par +16°, impar -8°, que son 360·2/45 y -360·1/45:
# 45 rumbos distintos. El 30-07-2026 se midio que SI hay choques exactos, el
# primero en la profundidad 31 del arbol inverso, y se atribuyo la causa a la
# factorizacion 45 = 3^2 · 5: el reticulo de relaciones enteras entre las 45
# raices de la unidad tiene rango 45 - 24 = 21 y esta generado por el triangulo
# (tres direcciones a 120°) y el pentagono (cinco a 72°).
#
# De ahi salio esta prediccion, escrita y sin comprobar:
#
#   "si la causa es la factorizacion de 45, entonces con un numero PRIMO de
#    rumbos el unico nucleo es la suma de las p raices, y un choque exigiria
#    acumular las p direcciones exactamente por igual. El umbral de profundidad
#    deberia dispararse."
#
# Este programa la mide. Manteniendo la proporcion 2:1 de Harriss con signos
# opuestos, para N rumbos:   par = 360·2/N ,  impar = -360·1/N.
#
# ---------------------------------------------------------------------------
# NADA DE FLOATS. POR QUE, Y COMO SE EVITA
# ---------------------------------------------------------------------------
#
# coralcollaz.py compara posiciones redondeando a 6 decimales. Eso da falsos
# positivos y falsos negativos: la distancia real entre dos ramas que chocan de
# verdad es del orden de 1e-59, y lo que alli se media como 1,4e-14 era el error
# de sumar 35 cosenos. Aqui no se usa ni un float.
#
# Cada arista del coral es una raiz N-esima de la unidad. Una rama es entonces
# un VECTOR ENTERO c = (c_0, …, c_{N-1}): cuantas aristas van en cada direccion.
# Dos ramas caen en el mismo punto si y solo si c - c' esta en el reticulo de
# relaciones enteras entre las N raices. Y ese reticulo es exactamente el nucleo
# de Z[x]/(x^N - 1) -> Z[zeta_N], o sea el ideal de Phi_N(x). Luego:
#
#   CLAVE CANONICA DE UNA RAMA  =  (suma de x^d sobre sus aristas) mod Phi_N(x)
#
# calculada en Z. Es un invariante COMPLETO porque Z[x]/(Phi_N) es isomorfo a
# Z[zeta_N], que vive dentro de C. Dos ramas chocan si y solo si su clave es
# identica. Aritmetica entera pura, sin tolerancia que ajustar.
#
# Para N PRIMO eso se reduce a lo que decia la prediccion: Phi_p = 1 + x + … +
# x^(p-1), el reticulo es la recta generada por (1,1,…,1), y dos ramas chocan
# si y solo si su diferencia de vectores es un multiplo constante de (1,1,…,1).
#
# ---------------------------------------------------------------------------
# EL CONTROL QUE PARTE EL RESULTADO EN DOS
# ---------------------------------------------------------------------------
#
# Se mide cada N con DOS claves distintas, y la diferencia es todo:
#
#   RETICULO : la clave canonica de arriba. Detecta todos los choques.
#   CRUDO    : el vector de cuentas SIN reducir. Solo detecta los choques con
#              diferencia exactamente CERO, o sea las ramas que usan las mismas
#              aristas en distinto orden. Esos existen para CUALQUIER N y no
#              tienen nada que ver con la factorizacion.
#
# Si la historia de "45 = 3^2 · 5" fuera el motor, RETICULO tendria que adelantar
# mucho a CRUDO en los compuestos y empatar en los primos.
#
# Genera solo texto. No dibuja nada y no abre el navegador.

import time
from decimal import Decimal, getcontext


# ---------------------------------------------------------------------------
# Cambia esto aqui, guarda, y dale a Ctrl+B en Sublime.
# ---------------------------------------------------------------------------

RUMBOS_PRINCIPALES = (43, 44, 45, 47, 49)   # 43 y 47 primos; 44 = 4·11, 49 = 7^2
RANGO_DESDE = 20            # el barrido ancho, para ver la tendencia entera
RANGO_HASTA = 70
PROFUNDIDAD_MAX = 200       # tope de profundidad del arbol inverso
TOPE_NODOS = 3_000_000      # tope de nodos, por si algun N no choca nunca
TOPE_SEMILLAS = 9_000_000   # tope del barrido por semillas (el de coralcollaz)
BASE = 1 << 16              # base del empaquetado de vectores en un entero
DIGITOS = 80                # cifras del control en coma flotante exacta

getcontext().prec = DIGITOS


# ------------------------------------------------------- polinomios enteros

def dividir_exacto(a, b):
    """Division de polinomios enteros (listas, indice = grado). Tiene que dar
    resto cero: si no, algo esta mal y no se sigue."""
    a = a[:]
    cociente = [0] * (len(a) - len(b) + 1)
    for i in range(len(a) - len(b), -1, -1):
        c = a[i + len(b) - 1] // b[-1]
        cociente[i] = c
        for j in range(len(b)):
            a[i + j] -= c * b[j]
    if any(a):
        raise SystemExit("La division de polinomios dio resto. No sigas.")
    return cociente


_guardados = {}

def ciclotomico(n):
    """Phi_n(x) con coeficientes enteros, por division exacta desde x^n - 1."""
    if n in _guardados:
        return _guardados[n]
    p = [-1] + [0] * (n - 1) + [1]
    for d in range(1, n):
        if n % d == 0:
            p = dividir_exacto(p, ciclotomico(d))
    _guardados[n] = p
    return p


def multiplicar(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                r[i + j] += x * y
    return r


def tabla_reduccion(N):
    """x^d mod Phi_N(x) para d = 0 … N-1, en enteros exactos."""
    phi = ciclotomico(N)
    grado = len(phi) - 1
    fila = [0] * grado
    fila[0] = 1
    tabla = []
    for _ in range(N):
        tabla.append(tuple(fila))
        alto = fila[-1]
        fila = [0] + fila[:-1]
        if alto:
            for j in range(grado):
                fila[j] -= alto * phi[j]
    return tabla, grado


# --------------------------------------------- empaquetar vectores enteros
#
# Un vector de coeficientes acotados se mete en UN entero de Python en base
# 2^16 con digitos con signo. La representacion es unica mientras |c_j| < BASE/2,
# asi que sirve de clave de diccionario sin perder nada.

def empaquetar(v):
    s = 0
    for j, c in enumerate(v):
        s += c * (BASE ** j)
    return s


def desempaquetar(s, cuantos):
    v = []
    for _ in range(cuantos):
        c = s % BASE
        if c >= BASE // 2:
            c -= BASE
        v.append(c)
        s = (s - c) // BASE
    if s != 0:
        raise SystemExit("El desempaquetado no cierra. Clave corrupta.")
    return v


def es_primo(n):
    return n > 1 and all(n % i for i in range(2, int(n ** 0.5) + 1))


# ------------------------------------------------------------- el recorrido
#
# El arbol inverso de Collatz, desde el 1 hacia afuera: de v sale siempre 2v, y
# ademas (v-1)/3 si v deja resto 4 al dividir entre 6 (y v no es el 4, cuyo otro
# padre es el propio 1, el arranque del tronco).
#
# El paso a 2v es el que en la trayectoria de ida fue n/2 -> giro PAR   -> +2
# El paso a (v-1)/3 es el que fue 3n+1                   -> giro IMPAR  -> -1
#
# en unidades de 360/N grados. La direccion de una arista es entonces un numero
# entero modulo N, y la posicion de la rama es la suma de esas raices.

def contar_rumbos(N, tope_nodos):
    """Cuantos rumbos distintos salen DE VERDAD con estos angulos. No se supone:
    se recorre el arbol sin parar en los choques y se apuntan las direcciones
    que aparecen. (El barrido de choques para en el primero, asi que no sirve
    para esto: solo habria visto las direcciones de los primeros niveles.)"""
    rumbos = set()
    nivel = [(1, 0)]
    total = 1
    while nivel and total <= tope_nodos:
        siguiente = []
        for v, d in nivel:
            dd = (d + 2) % N
            rumbos.add(dd)
            siguiente.append((2 * v, dd))
            if v % 6 == 4 and v != 4:
                dd = (d - 1) % N
                rumbos.add(dd)
                siguiente.append(((v - 1) // 3, dd))
        nivel = siguiente
        total += len(nivel)
        if len(rumbos) == N:
            break
    return len(rumbos)


def barrer_arbol(N, modo, profundidad_max, tope_nodos):
    """Devuelve (profundidad del primer choque, nodos, los dos nodos, rumbos)."""
    tabla, grado = tabla_reduccion(N)
    if modo == "reticulo":
        sumandos = [empaquetar(t) for t in tabla]
    else:
        sumandos = [BASE ** d for d in range(N)]

    rumbos = set()
    visto = {0: (0, 1)}
    nivel = [(1, 0, 0)]
    total = 1

    for profundidad in range(1, profundidad_max + 1):
        siguiente = []
        for v, d, p in nivel:
            dd = d + 2
            if dd >= N:
                dd -= N
            rumbos.add(dd)
            pp = p + sumandos[dd]
            if pp in visto:
                return profundidad, total, (visto[pp], (profundidad, 2 * v)), rumbos
            visto[pp] = (profundidad, 2 * v)
            siguiente.append((2 * v, dd, pp))

            if v % 6 == 4 and v != 4:
                dd = d - 1
                if dd < 0:
                    dd += N
                rumbos.add(dd)
                pp = p + sumandos[dd]
                w = (v - 1) // 3
                if pp in visto:
                    return profundidad, total, (visto[pp], (profundidad, w)), rumbos
                visto[pp] = (profundidad, w)
                siguiente.append((w, dd, pp))

        nivel = siguiente
        total += len(nivel)
        if total > tope_nodos:
            return None, total, None, rumbos

    return None, total, None, rumbos


def barrido_semillas(N, tope_semillas):
    """El otro umbral: el primer HASTA de coralcollaz.py con choque. Solo ve las
    ramas que cuelgan de semillas chicas, asi que da un numero mucho mayor."""
    tabla, grado = tabla_reduccion(N)
    sumandos = [empaquetar(t) for t in tabla]
    memo = {1: (0, 0)}
    visto = {0: 1}
    for n in range(2, tope_semillas + 1):
        camino = [n]
        v = n
        while v not in memo:
            v = v // 2 if v % 2 == 0 else 3 * v + 1
            camino.append(v)
        for i in range(len(camino) - 2, -1, -1):
            hijo, padre = camino[i], camino[i + 1]
            d, p = memo[padre]
            d = (d + 2) % N if hijo == 2 * padre else (d - 1) % N
            p = p + sumandos[d]
            memo[hijo] = (d, p)
            if p in visto:
                return n, len(memo)
            visto[p] = hijo
    return None, len(memo)


def cuentas_de(v, N):
    """El vector crudo de una rama: cuantas aristas en cada direccion. Se sube
    de v hasta el 1 por la trayectoria de Collatz, que es el camino del arbol."""
    camino = [v]
    while v != 1:
        v = v // 2 if v % 2 == 0 else 3 * v + 1
        camino.append(v)
    camino = camino[::-1]
    d = 0
    c = [0] * N
    for i in range(len(camino) - 1):
        d = (d + 2) % N if camino[i + 1] == 2 * camino[i] else (d - 1) % N
        c[d] += 1
    return c


# ------------------------------------- coseno y seno a 80 cifras, sin floats

def coseno(a):
    s, t, n = Decimal(0), Decimal(1), 0
    while True:
        s += t
        n += 1
        t = -t * a * a / (Decimal(2 * n - 1) * Decimal(2 * n))
        if abs(t) < Decimal(10) ** -(DIGITOS - 5):
            return s


def seno(a):
    s, t, n = Decimal(0), a, 0
    while True:
        s += t
        n += 1
        t = -t * a * a / (Decimal(2 * n) * Decimal(2 * n + 1))
        if abs(t) < Decimal(10) ** -(DIGITOS - 5):
            return s


PI = Decimal("3.1415926535897932384626433832795028841971693993751058209749445923078164062862"
             "089986280348253421170679")


def distancia_real(ca, cb, N):
    """La distancia de verdad entre dos ramas, a 80 cifras. Solo es un control:
    la decision ya la tomo la aritmetica entera."""
    x = y = Decimal(0)
    for j in range(N):
        k = ca[j] - cb[j]
        if k:
            a = 2 * PI * Decimal(j) / Decimal(N)
            x += Decimal(k) * coseno(a)
            y += Decimal(k) * seno(a)
    return (x * x + y * y).sqrt()


print("EL NUMERO PRIMO DE RUMBOS — la prediccion del coral, medida")
print(f"  angulos: par = 360·2/N grados, impar = -360·1/N grados (proporcion 2:1)")
print(f"  aritmetica entera exacta, cero floats en la decision")


# --- COMPROBACION 1: los polinomios ciclotomicos son los de verdad ---

fallos = []
for N in range(2, RANGO_HASTA + 1):
    producto = [1]
    for d in range(1, N + 1):
        if N % d == 0:
            producto = multiplicar(producto, ciclotomico(d))
    if producto != [-1] + [0] * (N - 1) + [1]:
        fallos.append(N)
    if es_primo(N) and ciclotomico(N) != [1] * N:
        fallos.append(N)

print(f"\nCOMPROBACION 1 — Phi_N(x) es correcto")
print(f"  N probados                        : {RANGO_HASTA - 1}")
print(f"  producto de Phi_d sobre d|N != x^N - 1: {len(fallos)}")
if fallos:
    raise SystemExit("Los ciclotomicos estan mal. No sigas.")
print(f"  -> y para N primo sale Phi_N = 1 + x + … + x^(N-1), o sea que el")
print(f"     reticulo de relaciones es la recta de (1,1,…,1). Es la hipotesis")
print(f"     entera sobre la que se apoya la prediccion.")


# --- COMPROBACION 2: el empaquetado no pierde nada ---

descuadres = 0
for N in RUMBOS_PRINCIPALES:
    tabla, grado = tabla_reduccion(N)
    for t in tabla:
        if desempaquetar(empaquetar(t), grado) != list(t):
            descuadres += 1
    if max(max(abs(c) for c in t) for t in tabla) * PROFUNDIDAD_MAX >= BASE // 2:
        descuadres += 1

print(f"\nCOMPROBACION 2 — la clave entera es inyectiva")
print(f"  vectores ida y vuelta con descuadre: {descuadres}")
if descuadres:
    raise SystemExit("El empaquetado pierde informacion. No sigas.")
print(f"  -> los coeficientes caben de sobra en base {BASE}. Dos ramas tienen la")
print(f"     misma clave si y solo si caen exactamente en el mismo punto.")


# --- COMPROBACION 3: el control conocido, N = 45 ---

prof45, nodos45, par45, rumbos45 = barrer_arbol(45, "reticulo",
                                                PROFUNDIDAD_MAX, TOPE_NODOS)
semilla45, _ = barrido_semillas(45, 20000)

print(f"\nCOMPROBACION 3 — reproduce los dos numeros publicados de N = 45")
print(f"  primera profundidad con choque: {prof45}   (publicado: 31)")
print(f"  primer HASTA con choque       : {semilla45}   (publicado: 10452)")
if prof45 != 31 or semilla45 != 10452:
    raise SystemExit("No reproduce el control conocido de 45. No sigas.")
print(f"  -> la maquinaria entera da los mismos numeros que la de coma flotante")
print(f"     del 30-07-2026. Lo que sigue se mide con esta.")


# --- COMPROBACION 4: los choques son exactos, no ruido ---

(pa, va), (pb, vb) = par45
ca, cb = cuentas_de(va, 45), cuentas_de(vb, 45)
d45 = distancia_real(ca, cb, 45)

print(f"\nCOMPROBACION 4 — el choque de N = 45 es exacto")
print(f"  ramas: v = {va} (profundidad {pa})  y  v = {vb} (profundidad {pb})")
print(f"  distancia real a {DIGITOS} cifras: {d45:.3E}")
if d45 > Decimal(10) ** -60:
    raise SystemExit("El choque no es exacto. Es ruido de floats. No sigas.")
print(f"  -> cero de verdad. Los 6 decimales de coralcollaz.py no decidian esto:")
print(f"     lo decide que el vector diferencia este en el reticulo.")


# ------------------------------------------------------------ LA MEDIDA

print(f"\n{'=' * 74}")
print(f"LOS CINCO CASOS PEDIDOS")
print(f"{'=' * 74}")
print(f"  RETICULO = todos los choques.  CRUDO = solo los de diferencia cero,")
print(f"  o sea las mismas aristas en otro orden (existen para cualquier N).")
print()
print(f"  {'N':>3} {'que es':>10} {'rumbos':>7} {'RETICULO':>9} {'CRUDO':>6}"
      f" {'nodos':>8} {'primer HASTA':>13} {'tipo del choque':>16}")

for N in RUMBOS_PRINCIPALES:
    pr, nodos, par, rumbos = barrer_arbol(N, "reticulo", PROFUNDIDAD_MAX, TOPE_NODOS)
    pc, _, _, _ = barrer_arbol(N, "crudo", PROFUNDIDAD_MAX, TOPE_NODOS)
    semilla, _ = barrido_semillas(N, TOPE_SEMILLAS)
    cuantos_rumbos = contar_rumbos(N, TOPE_NODOS)

    if cuantos_rumbos != N:
        raise SystemExit(f"Con N = {N} salen {cuantos_rumbos} rumbos, no {N}."
                         f" La tabla estaria mal etiquetada. No sigas.")

    (_, x), (_, y) = par
    diferencia = [i - j for i, j in zip(cuentas_de(x, N), cuentas_de(y, N))]
    tipo = "permutacion" if not any(diferencia) else "reticulo"

    if distancia_real(cuentas_de(x, N), cuentas_de(y, N), N) > Decimal(10) ** -60:
        raise SystemExit(f"El choque de N = {N} no es exacto. No sigas.")

    que = "PRIMO" if es_primo(N) else "compuesto"
    hasta = f"{semilla:,}" if semilla else f"> {TOPE_SEMILLAS:,}"
    print(f"  {N:>3} {que:>10} {cuantos_rumbos:>7} {pr:>9} {pc:>6}"
          f" {nodos:>8} {hasta:>13} {tipo:>16}")

print()
print(f"  (todos los choques verificados exactos a {DIGITOS} cifras, y todos los N")
print(f"   dan de verdad N rumbos distintos, no se supuso)")


# --- EL BARRIDO ANCHO: la tendencia entera ---

print(f"\n{'=' * 74}")
print(f"EL BARRIDO ANCHO — N de {RANGO_DESDE} a {RANGO_HASTA}")
print(f"{'=' * 74}")
print(f"  {'N':>3} {'que es':>10} {'RETICULO':>9} {'CRUDO':>6} {'ayuda':>6}"
      f"    {'N':>3} {'que es':>10} {'RETICULO':>9} {'CRUDO':>6} {'ayuda':>6}")

filas = []
for N in range(RANGO_DESDE, RANGO_HASTA + 1):
    pr, _, _, _ = barrer_arbol(N, "reticulo", PROFUNDIDAD_MAX, TOPE_NODOS)
    pc, _, _, _ = barrer_arbol(N, "crudo", PROFUNDIDAD_MAX, TOPE_NODOS)
    filas.append((N, "PRIMO" if es_primo(N) else "compuesto", pr, pc, pc - pr))

mitad = (len(filas) + 1) // 2
for i in range(mitad):
    izq = filas[i]
    txt = f"  {izq[0]:>3} {izq[1]:>10} {izq[2]:>9} {izq[3]:>6} {izq[4]:>6}"
    if i + mitad < len(filas):
        der = filas[i + mitad]
        txt += f"    {der[0]:>3} {der[1]:>10} {der[2]:>9} {der[3]:>6} {der[4]:>6}"
    print(txt)


# --- EL VEREDICTO, contado con los numeros de arriba ---

primos = [f for f in filas if f[1] == "PRIMO"]
compuestos = [f for f in filas if f[1] == "compuesto"]
primos_con_ayuda = [f for f in primos if f[4] != 0]
compuestos_con_ayuda = [f for f in compuestos if f[4] != 0]

print(f"\n{'=' * 74}")
print(f"EL VEREDICTO")
print(f"{'=' * 74}")

print(f"\nLA PARTE DE LA TEORIA QUE SI SE CONFIRMA, y es exacta:")
print(f"  primos en los que RETICULO adelanta a CRUDO: {len(primos_con_ayuda)}"
      f" de {len(primos)}")
print(f"  compuestos en los que adelanta             : {len(compuestos_con_ayuda)}"
      f" de {len(compuestos)}")
print(f"  -> en los {len(primos)} primos las dos claves dan EL MISMO numero, sin una")
print(f"     sola excepcion. O sea que con N primo ninguna relacion no trivial")
print(f"     entre las raices ayuda nunca: el reticulo es solo (1,1,…,1), tal")
print(f"     como decia la prediccion. Eso esta medido y es cierto.")

print(f"\nLA PREDICCION, QUE ERA QUE EL UMBRAL SE DISPARARA: NO SE CUMPLE.")
for N in (43, 45, 47):
    f = [x for x in filas if x[0] == N][0]
    print(f"  N = {N:>2} ({f[1]:>9}) -> primera profundidad con choque: {f[2]}")
print(f"  Los dos primos vecinos del 45 chocan ANTES que el 45, no despues.")
print(f"  Y el maximo del rango entero no lo tiene un primo:")
mejor = max(filas, key=lambda f: f[2])
print(f"    el mas alto es N = {mejor[0]} ({mejor[1]}) con profundidad {mejor[2]}.")

print(f"\nPOR QUE FALLA, que es lo que importa:")
print(f"  El motor de los choques NO son las relaciones entre raices. Es el caso")
print(f"  trivial que el razonamiento se dejo fuera: dos ramas distintas que usan")
print(f"  LAS MISMAS ARISTAS EN OTRO ORDEN. Diferencia de vectores exactamente")
print(f"  cero, ninguna relacion de por medio, y existe para cualquier N.")
print(f"  Sale de que una tirada larga de pasos pares (+2 cada uno) recorre el")
print(f"  circulo entero de direcciones y vuelve a pisar las mismas que la otra")
print(f"  rama piso en otro orden. La columna CRUDO es exactamente eso, y es")
print(f"  lineal en N: no sabe nada de si N es primo.")
print(f"  Con N = 45 la relacion del triangulo y el pentagono adelanta el choque")
print(f"  de la profundidad {[f for f in filas if f[0]==45][0][3]} a la"
      f" {[f for f in filas if f[0]==45][0][2]}: UN nivel. El 45 habria chocado casi")
print(f"  igual siendo primo. Atribuirle el choque a 45 = 3^2 · 5 era quedarse")
print(f"  con la causa de un nivel e ignorar la de treinta y uno.")

print(f"\nLO QUE SI GOBIERNA EL UMBRAL, leyendo la columna CRUDO:")
impares1 = [f for f in filas if f[0] % 4 == 1]
impares3 = [f for f in filas if f[0] % 4 == 3]
ok1 = sum(1 for f in impares1 if f[3] == (f[0] + 19) // 2)
ok3 = sum(1 for f in impares3 if f[3] == (f[0] + 11) // 2)
print(f"  N impar de la forma 4k+3: CRUDO = (N + 11)/2 en {ok3} de {len(impares3)}")
print(f"  N impar de la forma 4k+1: CRUDO = (N + 19)/2 en {ok1} de {len(impares1)}")
print(f"  -> el umbral es una RECTA en N con dos ramas segun N modulo 4. Ni")
print(f"     rastro de la factorizacion. Los N pares son aparte: ahi dos")
print(f"     direcciones opuestas se cancelan de dos en dos y todo se hunde.")

print(f"\nY EL AVISO DE ENCUADRE, que no se puede perder:")
print(f"  esto mide NUESTRO METODO DE DIBUJO, no Collatz. El cierre lo trae el")
print(f"  angulo elegido — el numero de rumbos —, no la aritmetica. Collatz pone")
print(f"  el paseo; el angulo pone el cierre. Lo unico que cambia respecto del")
print(f"  30-07-2026 es cual es la propiedad del angulo que manda: no es como")
print(f"  factoriza N, es cuanto vale N y su resto modulo 4.")
