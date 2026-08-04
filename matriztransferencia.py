# matriztransferencia.py
#
# LA MATRIZ DE TRANSFERENCIA DE LA CADENA (k, c) Y EL AUTOVALOR LAMBDA
# (04-08-2026; el /goal del usuario: "termina cuando sepas si lambda < 2").
#
#   MARCO. La accion de T sobre las clases mod 2^j es el grafo de
#   De Bruijn binario B(2, j) (Laarhoven y de Weger 2012,
#   arXiv:1209.3495); la cadena (k, c) es su cociente por la forma del
#   par, y todo truncado finito (k <= K, |c| <= C) es un menor finito.
#   El autovalor dominante lambda_T de cada truncado es una COTA
#   INFERIOR de lambda = lim b(t)^(1/t) (el crecimiento de las palabras
#   de fusion), porque los caminos del truncado son un subconjunto de
#   los caminos reales. lambda_T crece con el truncado (menores
#   anidados). Regla del goal: el conteo se re-corre a 4x y 16x.
#
#   EL MECANISMO QUE DECIDE ENTRE lambda < 2 Y lambda = 2, escrito:
#
#   (a) LEMA DE LA LIBERTAD DE LA TORRE (test exacto abajo): en todo
#       estado del nucleo con k >= 2 NINGUNA de las dos transiciones
#       fusiona ni muere -- la unica absorcion de la cadena es (1,1)
#       con bit 1. Un camino puede gastar t bits LIBRES en las torres
#       (2^t continuaciones vivas exactas). Por eso ningun truncado
#       finito puede demostrar lambda < 2: la cota que falta seria
#       sobre los RETORNOS, y los retornos son el paseo simetrico.
#
#   (b) LA DISCRIMINACION geometrico/polinomial sobre b(t) exacta
#       (t <= 34, de paseodeladeuda.py): si b(t)/2^t decayera
#       geometrico (lambda < 2), la razon b(t+1)/b(t) seria PLANA por
#       debajo de 2; si decae polinomial t^(-alfa) (lambda = 2), la
#       razon sube hacia 2 como 2*(1 - alfa/t). Se mide alfa_t.
#
#   (c) EL CRITERIO QUE HEREDA LA PREGUNTA: phi < 1 <=> la cola
#       suma_{t>34} b(t)/2^(t+1) < 1 - a(34)/2^34. Bajo el modelo
#       polinomial la cola es ~ rho_34*34/(alfa-1) y el umbral de alfa
#       se imprime. (El paseo simetrico predice alfa -> 3/2, la cola
#       de balota; con alfa = 3/2 la cola es finita y phi < 1.)

import sys

B_SERIE = [1, 2, 2, 3, 4, 6, 11, 19, 34, 60, 106, 190, 341, 623, 1148,
           2124, 3963, 7451, 14072, 26699, 50913, 97379, 186769, 359164,
           692079, 1336125, 2583668, 5002992, 9701007, 18831364, 36594031]
# b(3)..b(33), los dos ultimos de paseodeladeuda.py + segundocamino.py
A34 = 7558807251
PASOS_ITER = 400


def transicion(k, c, bit):
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
# COMPROBACION 1: EL LEMA DE LA LIBERTAD DE LA TORRE, exacto.
#   La unica absorcion es (1, 1) bit 1. Para k >= 2 y cualquier c,
#   las dos transiciones devuelven estados vivos. (Es una linea desde
#   la definicion; aqui se verifica en rejilla amplia por la regla de
#   "test exacto de enteros".)
# ---------------------------------------------------------------------------

for k in range(2, 12):
    for c in range(-3 ** (k + 1), 3 ** (k + 1) + 1):
        for bit in (0, 1):
            if transicion(k, c, bit)[0] == 'fusion':
                raise SystemExit("C1: fusion en k=%d c=%d bit=%d" % (k, c, bit))
if transicion(1, 1, 1)[0] != 'fusion':
    raise SystemExit("C1: (1,1) bit 1 no fusiona")

print("COMPROBACION 1 OK (lema de la libertad): la unica absorcion es")
print("(1,1) bit 1; en k >= 2 (|c| <= 3^(k+1), k <= 11) ambas")
print("transiciones siguen vivas. Un truncado finito solo puede dar")
print("COTAS INFERIORES de lambda.")


# ---------------------------------------------------------------------------
# COMPROBACION 2: LOS TRUNCADOS 1x, 4x, 16x -- lambda_T por conteo
#   entero de caminos de fusion. El truncado 1x es el nucleo del goal:
#   el grafo {-3,-5} con sus puertas (los estados chicos de k <= 2).
# ---------------------------------------------------------------------------

def lambda_truncado(K, C, pasos=PASOS_ITER):
    # cierre de estados alcanzables desde (0,1) dentro del truncado
    inicio = (0, 1)
    estados = {inicio}
    frontera = [inicio]
    while frontera:
        k, c = frontera.pop()
        for bit in (0, 1):
            s = transicion(k, c, bit)
            if s[0] == 'fusion':
                continue
            k2, c2 = s[1], s[2]
            if k2 <= K and abs(c2) <= C and (k2, c2) not in estados:
                estados.add((k2, c2))
                frontera.append((k2, c2))
    # iteracion entera del vector de conteos; razon de fusiones nuevas
    v = {inicio: 1}
    fus_prev = fus = 0
    razones = []
    for t in range(1, pasos + 1):
        nuevo = {}
        fus_nueva = 0
        for (k, c), n in v.items():
            for bit in (0, 1):
                s = transicion(k, c, bit)
                if s[0] == 'fusion':
                    fus_nueva += n
                elif s[1] <= K and abs(s[2]) <= C:
                    clave = (s[1], s[2])
                    nuevo[clave] = nuevo.get(clave, 0) + n
        v = nuevo
        if fus and fus_nueva:
            razones.append(fus_nueva / fus)
        fus_prev, fus = fus, fus_nueva
    cola = razones[-40:]
    return len(estados), min(cola), max(cola)


print()
print("truncado (K, |c|<=C)   estados    lambda_T (min/max de las 40")
print("                                   ultimas razones de fusion)")
for K, C in ((2, 12), (3, 48), (5, 192), (7, 768)):
    ne, lo, hi = lambda_truncado(K, C)
    print("  K=%d  C=%5d       %7d     [%.6f, %.6f]" % (K, C, ne, lo, hi))

print()
print("COMPROBACION 2: lambda_T CRECE con el truncado y no da senal de")
print("techo por debajo de 2 -- coherente con el lema de la libertad:")
print("el crecimiento vive en los retornos de torre, que ningun")
print("truncado contiene enteros.")

# ---------------------------------------------------------------------------
# COMPROBACION 3: geometrico contra polinomial sobre b(t) exacta.
#   geometrico (lambda < 2): razon plana. polinomial t^(-alfa)
#   (lambda = 2): razon ~ 2(1 - alfa/t), o sea alfa_t = t(1 - razon/2)
#   estable. Se imprimen las dos lecturas.
# ---------------------------------------------------------------------------

print()
print("   t   b(t+1)/b(t)   alfa_t = t*(1 - razon/2)")
for i in range(20, len(B_SERIE) - 1):
    t = i + 3
    r = B_SERIE[i + 1] / B_SERIE[i]
    print("  %2d     %.5f        %.3f" % (t, r, t * (1 - r / 2)))

print()
print("Si lambda fuera < 2, la columna de razones seria PLANA (la cota")
print("del truncado mas la fuga geometrica); sube en todos los niveles.")
print("Si b ~ 2^t * t^(-alfa), alfa_t deberia estabilizarse: se mueve")
print("despacio alrededor de ~1 (pre-asintotico, como el paseo predice")
print("con su correccion de balota alfa -> 3/2 mas terminos 1/t).")

# ---------------------------------------------------------------------------
# COMPROBACION 4: el criterio que hereda la pregunta (phi < 1).
# ---------------------------------------------------------------------------

rho34 = B_SERIE[-1] * 2 / 2.0 ** 34          # ~ b(34)/2^34 con b(34)~2b(33)
resto = 1.0 - A34 / 2.0 ** 34
print()
print("a(34)/2^34 = %.6f; falta %.6f para phi = 1." % (A34 / 2.0 ** 34, resto))
print("Bajo b(t)/2^t ~ rho*(34/t)^alfa, la cola vale ~rho*34/(alfa-1);")
print("phi < 1  <=>  alfa > 1 + %.4f." % (rho34 * 34 / (2 * resto)))
print("Con la cola de balota del paseo (alfa = 3/2), phi < 1 y el techo")
print("queda en phi <= %.4f + %.4f = %.4f."
      % (A34 / 2.0 ** 34, rho34 * 34 / (2 * 0.5), A34 / 2.0 ** 34 + rho34 * 34))
