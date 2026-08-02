# A9 - verificacion independiente (agente 2, Python desde cero)
#
# ENUNCIADO: el rumbo de una rama del coral solo depende de (A,B):
#            rumbo = A*giro_impar + B*giro_par
# CUANTIFICADOR: todo n
#
# Interpretacion verificada: en el metodo de dibujo del coral, cada paso de la
# trayectoria gira el rumbo una cantidad fija segun la paridad del numero
# (giro_impar si el paso aplica la regla impar, giro_par si divide entre 2).
# El rumbo acumulado al final de una rama (o de cualquier tramo) seria entonces
# la suma ORDENADA de los giros. El enunciado afirma que esa suma solo depende
# de los CONTEOS A (pasos impares) y B (pasos pares), no del orden:
#            rumbo = A*giro_impar + B*giro_par
#
# MAPAS: se prueba sobre el mapa CLASICO (n/2 si par, 3n+1 si impar) y sobre el
# ATAJO (n/2 si par, (3n+1)/2 si impar). El enunciado es agnostico al mapa
# (habla del conteo de giros a lo largo de la rama), asi que debe valer en los dos.
#
# Aritmetica exacta: fractions.Fraction para los angulos, int para los conteos.
# Ningun float decide nada.

from fractions import Fraction

fallos = 0

def pasos_clasico(n):
    """Lista de paridades de la trayectoria clasica de n hasta 1.
    'I' = paso impar (3n+1), 'P' = paso par (n/2)."""
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
    """Paridades con el mapa del atajo: impar -> (3n+1)/2 cuenta como UN paso 'I'."""
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
    """El rumbo como lo construye el dibujo: girando paso a paso, en orden."""
    r = Fraction(0)
    for p in paridades:
        if p == 'I':
            r += gi
        else:
            r += gp
    return r

# dos pares de angulos distintos, exactos, sin relacion racional simple entre si
PARES_ANGULOS = [
    (Fraction(7, 360), Fraction(-13, 360)),
    (Fraction(355, 113), Fraction(-22, 7)),
]

# ---------------------------------------------------------------------------
# COMPROBACION 1: rumbo acumulado == A*gi + B*gp para todo n en 1..200000,
# mapa clasico y mapa atajo, con los dos pares de angulos.
# (n=1 incluido: rama vacia, A=B=0, rumbo 0 -- el borde k=0.)
# ---------------------------------------------------------------------------
N_MAX = 200000
grupos_clasico = {}   # (A,B) -> conjunto de rumbos vistos (como Fraction del par 1)
ejemplo_por_vector = {}  # (A,B) -> {vector_paridad: n}  para el chequeo de orden

gi1, gp1 = PARES_ANGULOS[0]
for n in range(1, N_MAX + 1):
    seq = pasos_clasico(n)
    A = sum(1 for p in seq if p == 'I')
    B = len(seq) - A
    r = rumbo_acumulado(seq, gi1, gp1)
    if r != A * gi1 + B * gp1:
        fallos += 1
        print("FALLO comprobacion 1 (clasico):", n, A, B)
    clave = (A, B)
    grupos_clasico.setdefault(clave, set()).add(r)
    if len(ejemplo_por_vector.setdefault(clave, {})) < 4:
        ejemplo_por_vector[clave].setdefault(tuple(seq), n)

print("comprobacion 1a (clasico, par de angulos 1): n = 1 ..", N_MAX, "-> fallos:", fallos)

# el segundo par de angulos y el atajo, en rango algo menor para no gastar CPU
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
print("comprobacion 1b (clasico y atajo, par de angulos 2): n = 1 .. 50000 -> fallos:", f2)
fallos += f2

# ---------------------------------------------------------------------------
# COMPROBACION 2: el contenido real del enunciado es la INDEPENDENCIA DEL ORDEN.
# Dos n con el mismo (A,B) pero VECTORES DE PARIDAD DISTINTOS deben dar el
# mismo rumbo. Buscamos esos pares de verdad (no vale que el grupo tenga un
# solo vector) y comprobamos.
# ---------------------------------------------------------------------------
grupos_con_orden_distinto = 0
testigo = None
f3 = 0
for clave, vectores in ejemplo_por_vector.items():
    if len(vectores) >= 2:
        grupos_con_orden_distinto += 1
        rumbos = set()
        for vec, n in vectores.items():
            rumbos.add(rumbo_acumulado(vec, gi1, gp1))
        if len(rumbos) != 1:
            f3 += 1
            print("FALLO comprobacion 2: clave", clave, "da", len(rumbos), "rumbos distintos")
        elif testigo is None:
            ns = sorted(vectores.values())[:2]
            testigo = (clave, ns)
print("comprobacion 2: grupos (A,B) con al menos dos ordenes distintos:",
      grupos_con_orden_distinto, "-> fallos:", f3)
if testigo:
    print("  testigo: (A,B) =", testigo[0], "con n =", testigo[1],
          "-> vectores de paridad distintos, mismo rumbo exacto")
fallos += f3

# ---------------------------------------------------------------------------
# COMPROBACION 3: tramos parciales (una 'rama' no tiene por que llegar al 1).
# Para n = 27 y n = 221, TODOS los pares de posiciones i < j: el rumbo ganado
# en el tramo debe ser A_tramo*gi + B_tramo*gp. Incluye tramos de largo 0.
# ---------------------------------------------------------------------------
f4 = 0
pares_probados = 0
for n0 in (27, 221):
    seq = pasos_clasico(n0)
    L = len(seq)
    # rumbos prefijo exactos
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
                f4 += 1
print("comprobacion 3: tramos parciales de 27 y 221 (incluye largo 0):",
      pares_probados, "tramos -> fallos:", f4)
fallos += f4

# ---------------------------------------------------------------------------
# COMPROBACION 4: bordes sueltos, uno a uno.
# ---------------------------------------------------------------------------
casos_borde = []
# n = 1: rama vacia, A = B = 0, rumbo 0
casos_borde.append(("n=1 rama vacia", pasos_clasico(1) == [] and
                    rumbo_acumulado([], gi1, gp1) == 0))
# n = 2: A = 0, B = 1
seq2 = pasos_clasico(2)
casos_borde.append(("n=2 (A=0,B=1)", seq2 == ['P'] and
                    rumbo_acumulado(seq2, gi1, gp1) == 0 * gi1 + 1 * gp1))
# potencia de 2 grande: A = 0 puro
seqp = pasos_clasico(2 ** 40)
casos_borde.append(("n=2^40 (A=0,B=40)",
                    all(p == 'P' for p in seqp) and len(seqp) == 40 and
                    rumbo_acumulado(seqp, gi1, gp1) == 40 * gp1))
# giro nulo en uno de los dos lados: gi = 0 -> rumbo = B*gp
seq27 = pasos_clasico(27)
A27 = sum(1 for p in seq27 if p == 'I'); B27 = len(seq27) - A27
casos_borde.append(("giro_impar = 0",
                    rumbo_acumulado(seq27, Fraction(0), gp1) == B27 * gp1))
casos_borde.append(("giro_par = 0",
                    rumbo_acumulado(seq27, gi1, Fraction(0)) == A27 * gi1))
# vectores unitarios: gi=(1,0), gp=(0,1) -> el rumbo ES (A,B); esto demuestra
# que la identidad vale para CUALQUIER par de valores reales, por linealidad
ok_unit = (rumbo_acumulado(seq27, Fraction(1), Fraction(0)) == A27 and
           rumbo_acumulado(seq27, Fraction(0), Fraction(1)) == B27)
casos_borde.append(("base canonica (linealidad)", ok_unit))

for nombre, ok in casos_borde:
    print("comprobacion 4:", nombre, "->", "OK" if ok else "FALLO")
    if not ok:
        fallos += 1

# ---------------------------------------------------------------------------
# VEREDICTO
# ---------------------------------------------------------------------------
if fallos:
    raise SystemExit("A9: %d fallos -> el enunciado NO se sostiene tal cual" % fallos)
print()
print("A9: 0 fallos en todo. rumbo = A*giro_impar + B*giro_par, exacto,")
print("para todo n probado, en los dos mapas, con angulos arbitrarios,")
print("en tramos parciales y en todos los bordes. La razon es la conmutatividad")
print("de la suma de angulos: el rumbo es la suma de los giros y una suma no")
print("depende del orden de sus sumandos.")
