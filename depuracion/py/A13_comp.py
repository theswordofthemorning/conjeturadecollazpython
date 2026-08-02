# A13_comp - tercera implementacion del comparador, distinta de las dos.
# Uso cadenas binarias para el tamano de bloque (ninguna llamada a bit_length)
# y un limite NO redondo, 314159, por el punto 8 de la lista de la casa.

def bloque(n):
    # 2^(k-1) <= n < 2^k  via longitud de la cadena binaria
    return len(format(n, "b"))

def espejo1(n):
    # convenio del agente 1 (Lean): SIEMPRE 2^(j+1) - n con 2^j <= n < 2^(j+1)
    j = bloque(n) - 1
    return 2 ** (j + 1) - n

def espejo2(n):
    # convenio del agente 2 (Python): rama especial para potencias
    k = bloque(n)
    es_pot = (n & (n - 1)) == 0
    return n if es_pot else 2 ** k - n

LIM = 314159

# (a) los dos convenios son EL MISMO mapa sobre todo el rango
for n in range(1, LIM + 1):
    if espejo1(n) != espejo2(n):
        raise SystemExit("DISCREPAN los convenios en n=%d: %d vs %d" % (n, espejo1(n), espejo2(n)))
print("(a) espejo1 == espejo2 en 1..%d: son el mismo objeto" % LIM)

# (b) el caso comun: la orbita del 221 que el nucleo de Lean cerro con decide
orb = [221]
while (orb[-1] & (orb[-1] - 1)) != 0:
    orb.append(espejo1(orb[-1]))
print("(b) orbita del 221:", orb)
if orb != [221, 35, 29, 3, 1]:
    raise SystemExit("FALLO: la orbita del 221 no es la de Lean")

# (c) el enunciado LITERAL "baja estrictamente" con cuantificador todo_n:
# contraejemplos = las potencias de 2 (puntos fijos). El minimo es n=1.
contra = [n for n in range(1, 1025) if espejo1(n) >= n]
print("(c) donde NO baja estrictamente (1..1024):", contra)
son_pot = all((n & (n - 1)) == 0 for n in contra)
print("    todos son potencias de 2:", son_pot)

# (d) la conclusion para todo n del rango no redondo: cae en potencia fija
for n in range(1, LIM + 1):
    x = n
    for _ in range(bloque(n) + 1):
        if (x & (x - 1)) == 0:
            break
        x = espejo1(x)
    else:
        raise SystemExit("FALLO: %d no cae en <= bits pasos" % n)
    if espejo1(x) != x:
        raise SystemExit("FALLO: terminal no fijo en %d" % n)
print("(d) 1..%d: toda orbita cae en una potencia de 2 (fija) en <= bits pasos" % LIM)

# (e) la desigualdad literal de la ficha: 2^(k-1) < n < 2^k  =>  2^k - n < 2^(k-1)
for n in range(1, LIM + 1):
    k = bloque(n)
    if 2 ** (k - 1) < n:  # no potencia
        if not (2 ** k - n < 2 ** (k - 1)):
            raise SystemExit("FALLO en la linea de algebra de la ficha, n=%d" % n)
print("(e) la linea de algebra de la ficha: 0 fallos en 1..%d" % LIM)

print("COMPARADOR: 0 fallos propios")
