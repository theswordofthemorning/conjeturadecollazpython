# A11 - verificacion independiente (agente 2, Python, a ciegas)
#
# ENUNCIADO (ficha A11): si n tarda S pasos, el numero de la posicion k de su
# trayectoria tarda S-k pasos; luego el de la posicion S/2 tarda S/2 pasos.
# Ambito declarado en las notas de la base: todo n con cantidad PAR de pasos.
#
# MAPA: clasico (par -> n/2, impar -> 3n+1), pasos contados hasta llegar a 1
# por primera vez. Todo con enteros de Python, ni un float en lo que decide.

import sys

LIMITE = 20000          # el rango que declara la base (2..20000)

def trayectoria(n):
    """Lista [n, T(n), ..., 1] con el mapa clasico, parando en el primer 1."""
    seq = [n]
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        seq.append(n)
    return seq

# memoizacion de pasos, derivada de la misma definicion (independiente de la
# trayectoria explicita para poder cruzar las dos)
_pasos = {1: 0}
def pasos(n):
    pila = []
    m = n
    while m not in _pasos:
        pila.append(m)
        m = m // 2 if m % 2 == 0 else 3 * m + 1
    base = _pasos[m]
    for x in reversed(pila):
        base += 1
        _pasos[x] = base
    return _pasos[n]

fallos_parte1 = 0
comprobados_parte1 = 0
pares_S = 0            # cuantos n tienen S par
fallos_parte2 = 0
impares_con_floor_ok = 0   # contraejemplo-busqueda: S impar, floor(S/2) "funciona"
impares_S = 0

for n in range(2, LIMITE + 1):
    seq = trayectoria(n)
    S = len(seq) - 1
    if pasos(n) != S:
        raise SystemExit("incoherencia interna entre trayectoria y pasos en n=%d" % n)
    # PARTE 1: cada posicion k tarda S-k. Se comprueba en TODAS las k, 0..S.
    for k, v in enumerate(seq):
        comprobados_parte1 += 1
        if pasos(v) != S - k:
            fallos_parte1 += 1
            print("FALLO parte 1: n=%d k=%d valor=%d pasos=%d esperado=%d"
                  % (n, k, v, pasos(v), S - k))
    # PARTE 2: la posicion S/2 tarda S/2 (solo tiene sentido con S par)
    if S % 2 == 0:
        pares_S += 1
        if pasos(seq[S // 2]) != S // 2:
            fallos_parte2 += 1
            print("FALLO parte 2: n=%d S=%d" % (n, S))
    else:
        impares_S += 1
        # borde: con S impar el enunciado literal no esta definido; si alguien
        # lo leyera con floor, seria falso: seq[S//2] tarda S - S//2 = ceil(S/2)
        if pasos(seq[S // 2]) == S // 2:
            impares_con_floor_ok += 1

# BORDES explicitos
seq1 = trayectoria(1)
assert seq1 == [1] and pasos(1) == 0          # n=1: S=0 (par), posicion 0 tarda 0
assert pasos(2) == 1                          # n=2: S=1 impar -> fuera del ambito
seq2 = trayectoria(2)
assert pasos(seq2[0]) == 1 and pasos(seq2[1]) == 0   # parte 1 vale igual con S impar

# el 221, el caso citado por la base
S221 = pasos(221)
seq221 = trayectoria(221)
mitad221 = seq221[S221 // 2]

print("rango: n = 2 .. %d (mapa clasico, pasos hasta el primer 1)" % LIMITE)
print("parte 1 (pasos(seq[k]) == S-k): %d comprobaciones, %d fallos"
      % (comprobados_parte1, fallos_parte1))
print("n con S par: %d   | fallos de la parte 2 (posicion S/2 tarda S/2): %d"
      % (pares_S, fallos_parte2))
print("n con S impar: %d | de ellos, con floor(S/2) 'funcionaria' en: %d"
      % (impares_S, impares_con_floor_ok))
print("el 221: S = %d (par: %s), seq[S/2] = %d, pasos = %d"
      % (S221, S221 % 2 == 0, mitad221, pasos(mitad221)))
print("bordes: n=1 -> S=0, posicion 0 tarda 0 (vale); n=2 -> S=1 impar, fuera del ambito")

if fallos_parte1 == 0 and fallos_parte2 == 0:
    print("VEREDICTO LOCAL: 0 fallos en el ambito declarado (S par); parte 1 vale para todo n")
else:
    raise SystemExit("HAY FALLOS")
