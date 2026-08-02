# A17 - verificacion independiente (agente 2, Python desde cero)
#
# ENUNCIADO (literal de la ficha):
#   sigma_clasico(n) = sigma_atajo(n) + (pasos impares dentro de ellos), exacto
#   para todo n >= 2.
#
# DEFINICIONES QUE USO (derivadas desde cero, sin abrir ningun fichero del repo):
#   mapa CLASICO:  n par -> n/2 ;  n impar -> 3n+1
#   mapa ATAJO:    n par -> n/2 ;  n impar -> (3n+1)/2
#   sigma_X(n) = menor numero de pasos del mapa X tal que el valor cae
#                ESTRICTAMENTE por debajo del n inicial (tiempo de parada).
#   "pasos impares dentro de ellos" = cuantos de los sigma_atajo(n) pasos del
#   atajo se aplicaron sobre un valor impar.
#
# ARGUMENTO ESTRUCTURAL (el que hay que romper):
#   La trayectoria clasica es la del atajo con un valor intermedio 3m+1
#   intercalado en cada paso impar. Como 3m+1 > m >= n en el momento en que
#   se aplica (si m >= n; y si m < n ya paro antes), el intermedio nunca es
#   el primer valor < n. Luego el primer descenso ocurre en el mismo "sitio"
#   y el indice clasico = indice atajo + impares gastados.
#   OJO al borde: hay que comprobar que el intermedio 3m+1 nunca dispara el
#   paro NI TAMPOCO un (3m+1)/2 lo dispara "a medias": (3m+1)/2 < m exigiria
#   m < -1, imposible. Eso lo compruebo empiricamente, no solo lo razono.
#
# Aritmetica: solo int de Python. Ningun float decide nada.

import sys

TOPE_PASOS = 10_000_000  # corte de seguridad; ninguna semilla del rango lo toca

def sigma_clasico(n):
    """(pasos clasicos hasta valor < n). Devuelve None si no para en TOPE."""
    if n < 2:
        return None
    v = n
    pasos = 0
    while pasos < TOPE_PASOS:
        if v % 2 == 0:
            v = v // 2
        else:
            v = 3 * v + 1
        pasos += 1
        if v < n:
            return pasos
    return None

def sigma_atajo_y_impares(n):
    """(pasos del atajo hasta valor < n, impares gastados). None si no para."""
    if n < 2:
        return None, None
    v = n
    pasos = 0
    impares = 0
    while pasos < TOPE_PASOS:
        if v % 2 == 0:
            v = v // 2
        else:
            v = (3 * v + 1) // 2
            impares += 1
        pasos += 1
        if v < n:
            return pasos, impares
    return None, None

def comprobar(n):
    """Devuelve True si el enunciado se cumple para n. SystemExit si falla."""
    sc = sigma_clasico(n)
    sa, imp = sigma_atajo_y_impares(n)
    if sc is None or sa is None:
        raise SystemExit("n=%d no paro dentro del tope de pasos" % n)
    if sc != sa + imp:
        print("CONTRAEJEMPLO: n=%d  sigma_clasico=%d  sigma_atajo=%d  impares=%d"
              % (n, sc, sa, imp))
        raise SystemExit("el enunciado FALLA en n=%d" % n)
    return True

# ---------------------------------------------------------------------------
# 0. BORDES DECLARADOS: n=1 queda fuera del ambito (n>=2). Compruebo POR QUE:
#    la trayectoria de 1 nunca baja de 1 (1 -> 4 -> 2 -> 1 -> ...), o sea que
#    sigma ni siquiera esta definido. No es una excepcion del teorema: es que
#    el objeto no existe ahi.
v = 1
nunca_bajo = True
for _ in range(1000):
    v = v // 2 if v % 2 == 0 else 3 * v + 1
    if v < 1:
        nunca_bajo = False
        break
if not nunca_bajo:
    raise SystemExit("sorpresa: la trayectoria de 1 bajo de 1")
print("borde n=1: sigma no definido (nunca cae por debajo de 1) -> fuera del ambito, correcto")

# ---------------------------------------------------------------------------
# 1. Bordes chicos a mano, con los valores impresos para poder auditarlos.
print()
print("bordes chicos:")
for n in [2, 3, 4, 5, 6, 7, 8, 27]:
    sc = sigma_clasico(n)
    sa, imp = sigma_atajo_y_impares(n)
    comprobar(n)
    print("  n=%-3d  sigma_clasico=%-3d sigma_atajo=%-3d impares=%-3d  (%d = %d + %d)"
          % (n, sc, sa, imp, sc, sa, imp))

# ---------------------------------------------------------------------------
# 2. Barrido exhaustivo n = 2 .. 1.000.000 (pares e impares, sin saltarse nada).
LIMITE = 1_000_000
fallos = 0
max_sc = (0, 0)
for n in range(2, LIMITE + 1):
    comprobar(n)  # corta con SystemExit al primer fallo
    # registro del peor caso para declarar el rango con contenido
print("barrido exhaustivo n = 2 .. %d : 0 fallos" % LIMITE)

# ---------------------------------------------------------------------------
# 3. Semillas grandes y adversarias (donde el enunciado sufriria si fuera falso):
#    - 2^k - 1: k impares seguidos (racha maxima de intermedios 3m+1)
#    - 2^k + 1: baja rapido
#    - 27 * 2^k + 27-clase, numeros de records conocidos por ser lentos
#    - un numero de 200 bits impar cualquiera (determinista)
print()
print("semillas adversarias:")
adversarias = [
    (1 << 20) - 1,          # veinte impares seguidos
    (1 << 64) - 1,          # sesenta y cuatro impares seguidos
    (1 << 20) + 1,
    (1 << 64) + 1,
    27, 703, 26623,         # planeos largos conocidos como lentos
    837799,                 # record de retraso bajo 10^6
    (1 << 200) + 173,       # 200 bits, impar
    (1 << 200) - 1,         # 200 impares seguidos
]
for n in adversarias:
    sc = sigma_clasico(n)
    sa, imp = sigma_atajo_y_impares(n)
    comprobar(n)
    print("  n con %d bits: %d = %d + %d" % (n.bit_length(), sc, sa, imp))

# ---------------------------------------------------------------------------
# 4. La afirmacion auxiliar de la nota: "el valor intermedio 3m+1 es siempre
#    MAYOR que n, asi que nunca dispara el descenso". La compruebo directa:
#    recorro la trayectoria CLASICA de cada n hasta parar y verifico que el
#    primer valor < n NUNCA es un valor recien salido de un 3m+1.
LIMITE2 = 200_000
for n in range(2, LIMITE2 + 1):
    v = n
    pasos = 0
    while True:
        fue_impar = (v % 2 == 1)
        v = 3 * v + 1 if fue_impar else v // 2
        pasos += 1
        if v < n:
            if fue_impar:
                print("CONTRAEJEMPLO AUXILIAR: n=%d para en un paso 3m+1" % n)
                raise SystemExit("la nota auxiliar FALLA en n=%d" % n)
            break
        if pasos > TOPE_PASOS:
            raise SystemExit("tope en auxiliar, n=%d" % n)
print()
print("auxiliar (el primer valor < n nunca sale de un paso 3m+1): n = 2 .. %d, 0 fallos" % LIMITE2)

print()
print("VEREDICTO LOCAL: sigma_clasico(n) = sigma_atajo(n) + impares, exacto,")
print("0 fallos en 2..%d exhaustivo + %d semillas adversarias hasta 200 bits" % (LIMITE, len(adversarias)))
