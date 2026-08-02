# A12 - COMPARADOR: tercera implementacion, sin compartir codigo con A1 ni A2.
# espejo por CONSTRUCCION DIGITAL sobre cadenas (la lectura del agente 1) y
# espejo como 10^d - n (la lectura del agente 2). Se comprueba que son LA MISMA
# funcion en 1..10^6, y la identidad de la suma con una tercera via (str).

def espejo_digital(n):
    # complemento digito a digito sobre la cadena: ceros finales se conservan,
    # primer digito no nulo por la derecha -> 10-d, resto -> 9-d.
    s = str(n)
    out = []
    visto_no_nulo = False
    for ch in reversed(s):
        d = int(ch)
        if not visto_no_nulo:
            if d == 0:
                out.append(0)
            else:
                out.append(10 - d)
                visto_no_nulo = True
        else:
            out.append(9 - d)
    out.reverse()
    return int("".join(str(x) for x in out))

def espejo_resta(n):
    return 10 ** len(str(n)) - n

fallos = 0
for n in range(1, 10**6 + 1):
    a = espejo_digital(n)
    b = espejo_resta(n)
    if a != b:
        print("DISCREPAN las dos lecturas en n =", n, a, b)
        fallos += 1
        if fallos > 5:
            raise SystemExit("demasiados fallos")
    if n + a != 10 ** len(str(n)):
        print("FALLO identidad en n =", n)
        fallos += 1
if fallos:
    raise SystemExit("HAY FALLOS")
print("Las dos definiciones (digital y 10^d - n) son LA MISMA funcion en 1..10^6, 0 discrepancias")
print("Identidad n + espejo(n) = 10^digitos(n): 0 fallos en 1..10^6")

# caso comun de los dos agentes
assert espejo_digital(47) == 53 and 47 + 53 == 10**2
assert espejo_digital(350) == 650 and 350 + 650 == 10**3
assert espejo_digital(5) == 5
# no-involucion (hallazgo de A1, confirmado por conteo de A2)
assert espejo_digital(95) == 5 and espejo_digital(5) == 5
assert espejo_digital(999) == 1 and espejo_digital(1) == 9
print("Caso comun 47<->53 (suma 100), 350<->650, fijo 5: los dos agentes y el comparador coinciden")
print("No-involucion 95->5->5 y 999->1->9: confirmada")

# el punto que separa a los dos agentes: para A2 la identidad es tautologia;
# para A1 es teorema. Medir que el contenido no-tautologico existe: la
# construccion digital NO menciona 10^d - n y aun asi coincide. Ya medido arriba.
