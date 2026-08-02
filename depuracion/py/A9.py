# A9 - verificacion independiente (agente 2, Python desde cero, a ciegas del Lean)
#
# ENUNCIADO: el rumbo de una rama del coral solo depende de (A,B):
#            rumbo = A*giro_impar + B*giro_par
# CUANTIFICADOR: todo n
# ESTADO EN LA BASE: demostrado ("los giros conmutan")
#
# Interpretacion, derivada desde la definicion del metodo de dibujo: en el
# coral cada paso de una rama gira el rumbo una cantidad FIJA segun la paridad
# del paso (giro_impar si aplica la regla impar, giro_par si divide entre 2).
# El rumbo al final de la rama es la suma ORDENADA de los giros. El enunciado
# afirma que esa suma solo depende de los CONTEOS A (impares) y B (pares):
#            rumbo = A*giro_impar + B*giro_par
# o sea: independencia del ORDEN de los pasos.
#
# MAPAS: se prueba sobre el CLASICO (n/2, 3n+1) y sobre el ATAJO
# (n/2, (3n+1)/2). El enunciado es agnostico al mapa (habla de conteos de
# giros a lo largo de la rama), asi que debe valer en los dos, y tambien
# sobre el arbol INVERSO (que es como se dibuja el coral de verdad).
#
# Aritmetica exacta: fractions.Fraction para los angulos, int para conteos.
# Ningun float decide nada.

from fractions import Fraction
import random

fallos = 0

def pasos_clasico(n):
    """Paridades de la trayectoria clasica de n hasta 1. 'I'=3n+1, 'P'=n/2."""
    seq = []
    while n != 1:
        if n % 2 == 0:
            seq.append('P')
            n //= 2
        else:
            seq.append('I')
            n = 3 * n + 1
    return seq

def pasos_atajo(n):
    """Paridades con el atajo: impar -> (3n+1)/2 cuenta como UN paso 'I'."""
    seq = []
    while n != 1:
        if n % 2 == 0:
            seq.append('P')
            n //= 2
        else:
            seq.append('I')
            n = (3 * n + 1) // 2
    return seq

def rumbo_acumulado(paridades, gi, gp):
    """El rumbo como lo construye el dibujo: girando paso a paso, EN ORDEN."""
    r = Fraction(0)
    for p in paridades:
        r += gi if p == 'I' else gp
    return r

# dos pares de angulos exactos distintos, con signos mezclados
PARES_ANGULOS = [
    (Fraction(7, 360), Fraction(-13, 360)),
    (Fraction(355, 113), Fraction(-22, 7)),
]

# ---------------------------------------------------------------------------
# COMPROBACION 1: rumbo acumulado == A*gi + B*gp para todo n = 1..200000,
# mapa clasico, primer par de angulos. n=1 incluido (rama vacia: el borde k=0).
# ---------------------------------------------------------------------------
N_MAX = 200000
ejemplo_por_vector = {}   # (A,B) -> {vector_paridad: n}
gi1, gp1 = PARES_ANGULOS[0]
f1 = 0
for n in range(1, N_MAX + 1):
    seq = pasos_clasico(n)
    A = sum(1 for p in seq if p == 'I')
    B = len(seq) - A
    if rumbo_acumulado(seq, gi1, gp1) != A * gi1 + B * gp1:
        f1 += 1
        print("FALLO comprobacion 1:", n, A, B)
    d = ejemplo_por_vector.setdefault((A, B), {})
    if len(d) < 4:
        d.setdefault(tuple(seq), n)
print("comprobacion 1a (clasico, angulos 1): n = 1 ..", N_MAX, "-> fallos:", f1)
fallos += f1

# segundo par de angulos y el mapa del atajo, rango menor
gi2, gp2 = PARES_ANGULOS[1]
f2 = 0
for n in range(1, 50001):
    for gen in (pasos_clasico, pasos_atajo):
        seq = gen(n)
        A = sum(1 for p in seq if p == 'I')
        B = len(seq) - A
        if rumbo_acumulado(seq, gi2, gp2) != A * gi2 + B * gp2:
            f2 += 1
            print("FALLO comprobacion 1b:", n, gen.__name__)
print("comprobacion 1b (clasico y atajo, angulos 2): n = 1 .. 50000 -> fallos:", f2)
fallos += f2

# ---------------------------------------------------------------------------
# COMPROBACION 2: el contenido real es la INDEPENDENCIA DEL ORDEN. Dos n con
# el mismo (A,B) pero VECTORES DE PARIDAD DISTINTOS deben dar el mismo rumbo.
# Exigimos que existan de verdad (no-vacuidad) y que coincidan.
# ---------------------------------------------------------------------------
grupos_multi = 0
testigo = None
f3 = 0
for clave, vectores in ejemplo_por_vector.items():
    if len(vectores) >= 2:
        grupos_multi += 1
        rumbos = {rumbo_acumulado(vec, gi1, gp1) for vec in vectores}
        if len(rumbos) != 1:
            f3 += 1
            print("FALLO comprobacion 2: clave", clave, "->", len(rumbos), "rumbos")
        elif testigo is None:
            testigo = (clave, sorted(vectores.values())[:2])
print("comprobacion 2: grupos (A,B) con >= 2 ordenes distintos:", grupos_multi,
      "-> fallos:", f3)
if testigo:
    print("  testigo: (A,B) =", testigo[0], "con n =", testigo[1],
          "-> ordenes distintos, mismo rumbo exacto")
fallos += f3

# ---------------------------------------------------------------------------
# COMPROBACION 3: permutacion aleatoria. Barajar el vector de paridad de un
# camino y exigir el mismo rumbo: la conmutatividad atacada de frente.
# ---------------------------------------------------------------------------
random.seed(9)
f4 = 0
pruebas = 0
for n in random.sample(range(2, 100000), 2000):
    seq = pasos_clasico(n)
    if len(seq) < 2:
        continue
    barajado = seq[:]
    random.shuffle(barajado)
    pruebas += 1
    if rumbo_acumulado(seq, gi1, gp1) != rumbo_acumulado(barajado, gi1, gp1):
        f4 += 1
print("comprobacion 3: permutaciones aleatorias:", pruebas, "-> fallos:", f4)
fallos += f4

# ---------------------------------------------------------------------------
# COMPROBACION 4: tramos parciales (una rama no tiene por que llegar al 1).
# Para 27 y 221, TODOS los pares i <= j: rumbo del tramo = A_t*gi + B_t*gp.
# Incluye tramos de largo 0.
# ---------------------------------------------------------------------------
f5 = 0
pares_probados = 0
for n0 in (27, 221):
    seq = pasos_clasico(n0)
    L = len(seq)
    pref = [Fraction(0)]
    prefA = [0]
    for p in seq:
        pref.append(pref[-1] + (gi1 if p == 'I' else gp1))
        prefA.append(prefA[-1] + (1 if p == 'I' else 0))
    for i in range(L + 1):
        for j in range(i, L + 1):
            A = prefA[j] - prefA[i]
            B = (j - i) - A
            pares_probados += 1
            if pref[j] - pref[i] != A * gi1 + B * gp1:
                f5 += 1
print("comprobacion 4: tramos parciales de 27 y 221:", pares_probados,
      "tramos -> fallos:", f5)
fallos += f5

# ---------------------------------------------------------------------------
# COMPROBACION 5: el arbol INVERSO del mapa clasico (como se dibuja el coral):
# desde 1, hijo par 2v siempre, hijo impar (v-1)/3 si v = 4 (mod 6) y > 1.
# Cada rama del arbol lleva su camino; rumbo secuencial contra la formula.
# ---------------------------------------------------------------------------
D = 22
frontera = [(1, ())]
ramas = [(1, ())]
for prof in range(D):
    nueva = []
    for v, cam in frontera:
        nueva.append((2 * v, cam + ('P',)))
        if v % 6 == 4:
            w = (v - 1) // 3
            if w > 1:
                nueva.append((w, cam + ('I',)))
    ramas.extend(nueva)
    frontera = nueva
f6 = 0
for v, cam in ramas:
    A = cam.count('I')
    B = cam.count('P')
    if rumbo_acumulado(cam, gi1, gp1) != A * gi1 + B * gp1:
        f6 += 1
print("comprobacion 5: arbol inverso hasta profundidad", D, ":", len(ramas),
      "ramas -> fallos:", f6)
fallos += f6

# ---------------------------------------------------------------------------
# COMPROBACION 6: bordes sueltos.
# ---------------------------------------------------------------------------
casos_borde = []
casos_borde.append(("n=1 rama vacia (A=0,B=0) -> rumbo 0",
                    pasos_clasico(1) == [] and rumbo_acumulado([], gi1, gp1) == 0))
seq2 = pasos_clasico(2)
casos_borde.append(("n=2 (A=0,B=1) -> rumbo = gp",
                    seq2 == ['P'] and rumbo_acumulado(seq2, gi1, gp1) == gp1))
seqp = pasos_clasico(2 ** 40)
casos_borde.append(("n=2^40 (A=0,B=40) -> 40*gp",
                    all(p == 'P' for p in seqp) and len(seqp) == 40 and
                    rumbo_acumulado(seqp, gi1, gp1) == 40 * gp1))
seq27 = pasos_clasico(27)
A27 = sum(1 for p in seq27 if p == 'I'); B27 = len(seq27) - A27
casos_borde.append(("giro_impar = 0 -> rumbo = B*gp",
                    rumbo_acumulado(seq27, Fraction(0), gp1) == B27 * gp1))
casos_borde.append(("giro_par = 0 -> rumbo = A*gi",
                    rumbo_acumulado(seq27, gi1, Fraction(0)) == A27 * gi1))
# base canonica: gi=(1,0), gp=(0,1) -> el rumbo ES (A,B). Por linealidad esto
# implica la identidad para CUALQUIER par de valores (reales incluidos).
casos_borde.append(("base canonica (linealidad)",
                    rumbo_acumulado(seq27, Fraction(1), Fraction(0)) == A27 and
                    rumbo_acumulado(seq27, Fraction(0), Fraction(1)) == B27))
for nombre, ok in casos_borde:
    print("comprobacion 6:", nombre, "->", "OK" if ok else "FALLO")
    if not ok:
        fallos += 1

# ---------------------------------------------------------------------------
# COMPROBACION 7: control de discriminacion. Una regla ALTERNATIVA en la que
# el giro del paso j se pesa por j (depende del orden) DEBE romper la formula
# en algun caso. Si mi test no la detectara, el test no valdria nada.
# ---------------------------------------------------------------------------
def rumbo_orden(paridades, gi, gp):
    r = Fraction(0)
    for j, p in enumerate(paridades, start=1):
        r += (gi if p == 'I' else gp) * j
    return r

rotos = 0
for clave, vectores in ejemplo_por_vector.items():
    if len(vectores) >= 2:
        if len({rumbo_orden(v, gi1, gp1) for v in vectores}) > 1:
            rotos += 1
ok_control = rotos > 0
print("comprobacion 7: la regla dependiente del orden da", rotos,
      "grupos ambiguos (debe ser > 0) ->", "OK" if ok_control else "FALLO")
if not ok_control:
    fallos += 1

# ---------------------------------------------------------------------------
# VEREDICTO
# ---------------------------------------------------------------------------
if fallos:
    raise SystemExit("A9: %d fallos -> el enunciado NO se sostiene tal cual" % fallos)
print()
print("A9: 0 fallos. rumbo = A*giro_impar + B*giro_par, exacto, para todo n")
print("probado, en los dos mapas y en el arbol inverso, con angulos")
print("arbitrarios, en tramos parciales y en todos los bordes. La razon es")
print("la conmutatividad de la suma: el rumbo es la suma de los giros y una")
print("suma finita no depende del orden de sus sumandos. El control")
print("dependiente del orden si falla, o sea que el test discrimina.")
