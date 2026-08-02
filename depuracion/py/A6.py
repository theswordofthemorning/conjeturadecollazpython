# A6 - verificacion independiente (agente 2, Python desde cero)
#
# ENUNCIADO: un numero v tiene dos padres en el arbol (mapa CLASICO:
#   par -> n/2, impar -> 3n+1) si y solo si v deja resto 4 al dividirlo
#   entre 6; y el segundo padre es (v-1)/3. Ambito declarado: todo v >= 1.
#
# Un "padre" de v es un u >= 1 con paso(u) == v.
# Todo se hace con enteros exactos. Ningun float decide nada.

LIMITE_V = 500_000          # verificamos todos los v de 1 a LIMITE_V
LIMITE_U = 2 * LIMITE_V + 1 # el padre par de v es 2v, asi que con esto cubrimos todo

def paso(n):
    # mapa CLASICO
    if n % 2 == 0:
        return n // 2
    return 3 * n + 1

# ---- construir el mapa de padres por fuerza bruta, sin formulas ----
padres = {}   # v -> lista de padres u
for u in range(1, LIMITE_U + 1):
    v = paso(u)
    padres.setdefault(v, []).append(u)

# ---- comprobacion principal ----
fallos_iff = 0        # el "si y solo si" del conteo
fallos_padre = 0      # la identidad del segundo padre
fallos_conjunto = 0   # que el conjunto de padres sea exactamente {2v, (v-1)/3}
casos_dos = 0
casos_uno = 0

for v in range(1, LIMITE_V + 1):
    lista = sorted(padres.get(v, []))
    n_padres = len(lista)
    predicho_dos = (v % 6 == 4)

    if (n_padres == 2) != predicho_dos:
        fallos_iff += 1
        if fallos_iff <= 5:
            print("FALLO IFF: v =", v, "v%6 =", v % 6, "padres =", lista)
        continue

    if predicho_dos:
        casos_dos += 1
        segundo = (v - 1) // 3
        # el segundo padre debe ser entero exacto, impar y >= 1
        if (v - 1) % 3 != 0 or segundo % 2 != 1 or segundo < 1:
            fallos_padre += 1
            if fallos_padre <= 5:
                print("FALLO PADRE (forma): v =", v, "segundo =", segundo)
        if set(lista) != {2 * v, segundo}:
            fallos_conjunto += 1
            if fallos_conjunto <= 5:
                print("FALLO CONJUNTO: v =", v, "padres =", lista,
                      "esperados =", sorted([2 * v, segundo]))
    else:
        casos_uno += 1
        # todo v >= 1 debe tener exactamente 1 padre (el 2v), nunca 0 ni 3
        if n_padres != 1 or lista != [2 * v]:
            fallos_iff += 1
            if fallos_iff <= 5:
                print("FALLO CONTEO NO-4: v =", v, "padres =", lista)

# ---- bordes explicitos ----
print("--- bordes ---")
for v in (1, 2, 3, 4, 5, 6, 7, 10, 16, 22, LIMITE_V - (LIMITE_V - 4) % 6):
    lista = sorted(padres.get(v, []))
    print("v =", v, " v%6 =", v % 6, " padres =", lista)

# v = 4 es el borde historico: su segundo padre es 1 (el arranque del tronco)
assert sorted(padres[4]) == [1, 8], "el 4 debe tener padres {1, 8}"

# ---- comprobacion algebraica del iff, aparte de la fuerza bruta ----
# direccion =>: si u impar y 3u+1 = v entonces u = 2t+1 y v = 6t+4, o sea v%6==4
# direccion <=: si v = 6t+4 entonces (v-1)/3 = 2t+1 es impar y paso lo manda a v
fallos_alg = 0
for t in range(0, 200_000):
    v = 6 * t + 4
    u = (v - 1) // 3
    if u != 2 * t + 1 or paso(u) != v:
        fallos_alg += 1
print("--- resumen ---")
print("v verificados: 1 ..", LIMITE_V)
print("casos con dos padres (v%6==4):", casos_dos)
print("casos con un padre:", casos_uno)
print("fallos iff:", fallos_iff)
print("fallos forma del segundo padre:", fallos_padre)
print("fallos conjunto de padres:", fallos_conjunto)
print("fallos algebraicos (t = 0 .. 199999):", fallos_alg)

if fallos_iff or fallos_padre or fallos_conjunto or fallos_alg:
    raise SystemExit("HAY FALLOS: el enunciado NO se sostiene tal cual")
print("VEREDICTO LOCAL: 0 fallos en todo el rango")
