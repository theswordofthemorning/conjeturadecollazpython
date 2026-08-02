# A24_comp - comprobacion del COMPARADOR (tercera implementacion, minima)
# No comparte codigo con A24.py del agente 2: uso recursion con tope y
# calculo la trayectoria entera como lista, sin memo.

def T(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1

def tray(n, tope=2000):
    v = [n]
    while v[-1] != 1 and len(v) < tope:
        v.append(T(v[-1]))
    return v

fallos = 0

# caso comun de los dos agentes: k = 1 -> (12, 13)
t12, t13 = tray(12), tray(13)
print("k=1: T^3(12) =", t12[3], " T^3(13) =", t13[3],
      " altura(12) =", len(t12) - 1, " altura(13) =", len(t13) - 1)
if not (t12[3] == t13[3] == 10 and len(t12) - 1 == len(t13) - 1 == 9):
    fallos += 1

# caso k = 7 del agente 1: (60, 61) -> 46, alturas 19
t60, t61 = tray(60), tray(61)
if not (t60[3] == t61[3] == 46 and len(t60) - 1 == len(t61) - 1 == 19):
    fallos += 1
print("k=7: confluyen en", t60[3], "alturas", len(t60) - 1, len(t61) - 1)

# borde k = 0: confluyen (T^3 ambos 4) pero alturas 2 y 5.
# OJO: aqui hay que iterar T MAS ALLA del 1 (la trayectoria de 4 toca el 1
# en el paso 2, ANTES del paso 3 — que es exactamente el fenomeno del item).
a, b = 4, 5
for _ in range(3):
    a, b = T(a), T(b)
t4, t5 = tray(4), tray(5)
print("k=0: T^3(4) =", a, " T^3(5) =", b,
      " alturas:", len(t4) - 1, len(t5) - 1)
if not (a == b == 4 and len(t4) - 1 == 2 and len(t5) - 1 == 5):
    fallos += 1

# barrido corto propio, desplazado y NO redondo a proposito: k = 1 .. 33333
malos = 0
for k in range(1, 33334):
    a, b = 8 * k + 4, 8 * k + 5
    for _ in range(3):
        a, b = T(a), T(b)
    if not (a == b == 6 * k + 4):
        malos += 1
print("confluencia k = 1..33333:", malos, "fallos")
if malos:
    fallos += 1

# altura en un rango desplazado que los agentes no tocaron: k = 20001 .. 25000
malos2 = 0
for k in range(20001, 25001):
    if len(tray(8 * k + 4, 5000)) != len(tray(8 * k + 5, 5000)):
        malos2 += 1
print("altura k = 20001..25000:", malos2, "fallos")
if malos2:
    fallos += 1

# el punto fino: en el ATAJO, 8k+5 llega a 6k+4 en 2 pasos, no en 3
def atajo(n):
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2

x = 8 * 3 + 5  # k = 3 de ejemplo
pasos = 0
while x != 6 * 3 + 4:
    x = atajo(x)
    pasos += 1
print("atajo: 8k+5 (k=3) llega a 6k+4 en", pasos, "pasos ->",
      "el enunciado de 3 pasos SOLO cuadra en el clasico" if pasos == 2 else "?")

print("FALLOS TOTALES:", fallos)
raise SystemExit("HUBO FALLOS" if fallos else None)
