# A17_comp - comprobacion propia del COMPARADOR (tercera implementacion).
# Distinta de las dos anteriores: en vez de dos bucles con contador,
# construyo la trayectoria CLASICA entera como lista y DERIVO de ella
# el sigma del atajo comprimiendo los pares (impar, 3m+1) -> un paso.
# Asi ninguna de las dos cantidades se calcula con el bucle del agente 2.

def tray_clasica_hasta_parar(n, tope=10**7):
    v = n
    tray = [n]
    while len(tray) < tope:
        v = v // 2 if v % 2 == 0 else 3 * v + 1
        tray.append(v)
        if v < n:
            return tray
    raise SystemExit("no paro: n=%d" % n)

def medidas(n):
    tray = tray_clasica_hasta_parar(n)
    sigma_c = len(tray) - 1
    # comprimir: cada valor impar de la trayectoria (antes del final) genera
    # el par (impar -> 3m+1 -> mitad); en el atajo eso es UN paso.
    impares = sum(1 for x in tray[:-1] if x % 2 == 1)
    sigma_a = sigma_c - impares
    # verificacion cruzada del atajo por simulacion directa (independiente):
    v = n
    pasos = 0
    imp2 = 0
    while True:
        if v % 2 == 0:
            v //= 2
        else:
            v = (3 * v + 1) // 2
            imp2 += 1
        pasos += 1
        if v < n:
            break
    if pasos != sigma_a or imp2 != impares:
        raise SystemExit("DISCREPANCIA INTERNA en n=%d: %d,%d vs %d,%d"
                         % (n, sigma_a, impares, pasos, imp2))
    return sigma_c, sigma_a, impares

# 1. Casos comunes que dictaron los dos agentes:
esperados = {2: (1, 1, 0), 3: (6, 4, 2), 7: (11, 7, 4), 27: (96, 59, 37)}
for n, esp in esperados.items():
    got = medidas(n)
    if got != esp:
        raise SystemExit("n=%d: esperado %s, sale %s" % (n, esp, got))
    print("n=%-3d  sigma_clasico=%d = sigma_atajo=%d + impares=%d  OK" % (n, got[0], got[1], got[2]))

# 2. Semillas grandes que cito el agente 2, recalculadas aqui:
for n, esp in [((1 << 64) - 1, (329, 202, 127)), ((1 << 200) - 1, (1213, 744, 469)), (837799, (132, 81, 51))]:
    got = medidas(n)
    if got != esp:
        raise SystemExit("n de %d bits: esperado %s, sale %s" % (n.bit_length(), esp, got))
    print("n de %d bits: %d = %d + %d  OK (coincide con agente 2)" % (n.bit_length(), got[0], got[1], got[2]))

# 3. Barrido propio, corto pero con la implementacion distinta: 2..50000
for n in range(2, 50001):
    sc, sa, imp = medidas(n)
    if sc != sa + imp:
        raise SystemExit("CONTRAEJEMPLO n=%d" % n)
print("barrido propio (tercera implementacion) 2..50000: 0 fallos")

# 4. Ataque a la premisa compartida: probar la variante NO ESTRICTA (<= n)
#    del tiempo de parada, por si ambos coincidieron leyendo "estricto" mal.
#    Si la identidad SOLO vale con la lectura estricta, hay que saberlo.
def medidas_no_estricta(n):
    v = n; pasos = 0
    while True:
        v = v // 2 if v % 2 == 0 else 3 * v + 1
        pasos += 1
        if v <= n:  # NO estricta
            break
    sc = pasos
    v = n; pasos = 0; imp = 0
    while True:
        if v % 2 == 0:
            v //= 2
        else:
            v = (3 * v + 1) // 2; imp += 1
        pasos += 1
        if v <= n:
            break
    return sc, pasos, imp

fallos_ne = 0
for n in range(2, 50001):
    sc, sa, imp = medidas_no_estricta(n)
    if sc != sa + imp:
        fallos_ne += 1
print("variante NO estricta (<=): %d fallos en 2..50000" % fallos_ne)
