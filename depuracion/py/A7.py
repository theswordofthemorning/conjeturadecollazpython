# A7 — verificacion independiente (agente 2, Python desde cero)
#
# ENUNCIADO: con la regla CLASICA (n par -> n/2 ; n impar -> 3n+1) dos pasos
# impares nunca van seguidos: P(impar | impar) = 0 exacto, para todo n.
#
# MAPA USADO: el CLASICO. (Con el atajo (3n+1)/2 el enunciado seria FALSO,
# y eso se comprueba abajo como control A/B.)
#
# Todo con enteros de Python. Ningun float decide nada.

LIMITE = 200000          # trayectorias completas de 1..LIMITE
LIMITE_ALGEBRAICO = 10**6  # comprobacion directa n impar -> 3n+1 par

def paso_clasico(n):
    if n % 2 == 0:
        return n // 2
    return 3 * n + 1

def paso_atajo(n):
    if n % 2 == 0:
        return n // 2
    return (3 * n + 1) // 2

# ------------------------------------------------------------------
# COMPROBACION 1 (algebraica, exhaustiva en el rango):
# para todo n impar, 3n+1 es par. Incluye los bordes n=1, n=3.
# ------------------------------------------------------------------
fallos1 = 0
for n in range(1, LIMITE_ALGEBRAICO + 1, 2):
    if (3 * n + 1) % 2 != 0:
        fallos1 += 1
        print("CONTRAEJEMPLO comprobacion 1: n =", n)
if fallos1:
    raise SystemExit("FALLO comprobacion 1: " + str(fallos1))
print("comprobacion 1: n impar -> 3n+1 par, n = 1..%d impares (%d casos), 0 fallos"
      % (LIMITE_ALGEBRAICO, (LIMITE_ALGEBRAICO + 1) // 2))

# ------------------------------------------------------------------
# COMPROBACION 2 (dinamica): recorrer trayectorias enteras con el mapa
# clasico hasta llegar a 1, contando transiciones impar->impar.
# Bordes incluidos: n=1 (impar, 1->4->2->1), n=2 (par).
# ------------------------------------------------------------------
oportunidades = 0      # pasos que salen de un impar
impar_impar = 0        # de esos, cuantos aterrizan en impar
max_pasos = 0
for n0 in range(1, LIMITE + 1):
    n = n0
    pasos = 0
    while n != 1:
        siguiente = paso_clasico(n)
        if n % 2 == 1:
            oportunidades += 1
            if siguiente % 2 == 1:
                impar_impar += 1
                print("CONTRAEJEMPLO comprobacion 2: n0 =", n0, "n =", n)
        n = siguiente
        pasos += 1
        if pasos > 10**7:
            raise SystemExit("trayectoria sin terminar en n0 = " + str(n0))
    if pasos > max_pasos:
        max_pasos = pasos
# el 1 mismo tambien es impar: su sucesor es 4, par. Ya cubierto cuando
# alguna trayectoria pasa por 1? No: el bucle corta en 1. Probarlo aparte:
if paso_clasico(1) % 2 == 1:
    raise SystemExit("FALLO: el sucesor de 1 es impar")
oportunidades += 1  # la salida del 1, contada a mano

if impar_impar != 0:
    raise SystemExit("FALLO comprobacion 2: " + str(impar_impar) + " transiciones impar->impar")
print("comprobacion 2: trayectorias 1..%d, %d transiciones desde impar, 0 impar->impar (P = 0 exacto)"
      % (LIMITE, oportunidades))
print("  paso mas largo del rango:", max_pasos)

# ------------------------------------------------------------------
# COMPROBACION 3 (control A/B): con el mapa del ATAJO la prohibicion
# NO existe. Buscar el contraejemplo mas chico.
# ------------------------------------------------------------------
contra = None
for n in range(1, 1000, 2):
    s = paso_atajo(n)
    if s % 2 == 1:
        contra = (n, s)
        break
if contra is None:
    raise SystemExit("FALLO control A/B: el atajo tambien lo cumple (sospechoso)")
print("comprobacion 3 (control): con el ATAJO si hay impar->impar; el mas chico es %d -> %d"
      % contra)

# ------------------------------------------------------------------
# COMPROBACION 4 (demostracion en dos lineas, dejada por escrito):
# n impar => n = 2k+1 => 3n+1 = 6k+4 = 2*(3k+2), par. Verificada
# simbolicamente sobre el residuo mod 2: 3*1+1 = 4 = 0 (mod 2).
# ------------------------------------------------------------------
assert (3 * 1 + 1) % 2 == 0
print("comprobacion 4: identidad 3(2k+1)+1 = 2(3k+2); el argumento es algebraico, no muestral")

print()
print("VEREDICTO A7: SOSTENIDO. Con el mapa clasico, P(impar | impar) = 0 exacto.")
