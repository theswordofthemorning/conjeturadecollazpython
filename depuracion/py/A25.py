# A25 -- verificacion independiente (agente 2, Python desde cero)
#
# ENUNCIADO: (32m+5, 32m+6) se funden para todo m >= 1.
# "Se funden" = existe un indice de paso j tal que T^j(n1) = T^j(n2)
# con el MISMO j (desfase 0); de ahi sale la misma altura.
#
# MAPA USADO: el CLASICO  (n par -> n/2 ; n impar -> 3n+1).
# Todo con enteros de Python; ni un float en la cadena que decide.

# ---------- 1. derivacion simbolica: T^j(32m+5) y T^j(32m+6) como (a*m + b) ----------
# Represento cada valor como par (a, b) = a*m + b con a, b enteros.
# Un paso simbolico solo es legitimo si la paridad de a*m+b NO depende de m:
#   - a par y b par   -> siempre par
#   - a par y b impar -> siempre impar
#   - a impar         -> la paridad depende de m: ABORTAR (no paso aqui)

def paso_simbolico(a, b):
    if a % 2 != 0:
        raise SystemExit("paridad depende de m: la derivacion simbolica no aplica")
    if b % 2 == 0:
        # siempre par: dividir. a/2 y b/2 deben ser enteros: a par, b par
        if a % 2 or b % 2:
            raise SystemExit("division no entera en el paso simbolico")
        return (a // 2, b // 2)
    else:
        # siempre impar
        return (3 * a, 3 * b + 1)

def trayecto_simbolico(a, b, pasos):
    tray = [(a, b)]
    for _ in range(pasos):
        a, b = paso_simbolico(a, b)
        tray.append((a, b))
    return tray

t1 = trayecto_simbolico(32, 5, 6)   # 32m+5, seis pasos
t2 = trayecto_simbolico(32, 6, 6)   # 32m+6, seis pasos

print("trayectoria simbolica de 32m+5 :", t1)
print("trayectoria simbolica de 32m+6 :", t2)

if t1[6] != t2[6]:
    raise SystemExit("FALLO: los pasos 6 simbolicos no coinciden")
print("PASO 6 COMUN: %d*m + %d  (identidad polinomica, vale para TODO entero m >= 0)"
      % t1[6])

# La derivacion simbolica demuestra: T^6(32m+5) = T^6(32m+6) = 18m+4 para todo m,
# porque cada paridad intermedia quedo fija (independiente de m). Eso es la fusion
# con desfase 0 en el paso 6, para todo m entero (incluido m = 0).

# ---------- 2. la hipotesis m >= 1: nadie toca el 1 antes del paso 6 ----------
# Para que "se funden" implique "misma altura", ninguna de las dos trayectorias
# puede haber llegado al 1 antes del paso de fusion. Compruebo el minimo simbolico.
minimos = []
for (a, b) in t1[:6] + t2[:6]:
    # valor con m = 1 es el minimo sobre m >= 1 (a > 0 en todos)
    if a <= 0:
        raise SystemExit("coeficiente no positivo, revisar")
    minimos.append(a * 1 + b)
print("valor minimo tocado antes del paso 6 con m = 1:", min(minimos))
if min(minimos) <= 1:
    raise SystemExit("FALLO: alguien toca el 1 antes de la fusion con m >= 1")

# ---------- 3. fuerza bruta numerica: fusion, desfase y altura ----------
def paso(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1

def altura(n):
    # pasos del mapa clasico hasta llegar a 1
    c = 0
    while n != 1:
        n = paso(n)
        c += 1
    return c

def primer_encuentro(n1, n2, tope=1000):
    # primer j con T^j(n1) == T^j(n2), mismo indice
    a, b = n1, n2
    for j in range(tope + 1):
        if a == b:
            return j
        a, b = paso(a), paso(b)
    return None

RANGO = 20000
fallos_fusion = 0
fallos_altura = 0
fallos_paso6 = 0
for m in range(1, RANGO + 1):
    n1, n2 = 32 * m + 5, 32 * m + 6
    j = primer_encuentro(n1, n2)
    if j is None:
        fallos_fusion += 1
        print("SIN FUSION en m =", m)
        continue
    if j != 6:
        fallos_paso6 += 1
        print("fusion en paso", j, "y no 6, m =", m)
    if altura(n1) != altura(n2):
        fallos_altura += 1
        print("ALTURAS DISTINTAS en m =", m)

print("m = 1 .. %d : fallos de fusion = %d, fusiones fuera del paso 6 = %d, "
      "fallos de altura = %d" % (RANGO, fallos_fusion, fallos_paso6, fallos_altura))
if fallos_fusion or fallos_altura:
    raise SystemExit("FALLO en el rango central")

# ---------- 4. bordes ----------
print("--- bordes ---")
# m = 0: el par (5, 6)
j0 = primer_encuentro(5, 6)
print("m = 0: par (5,6), primer encuentro en paso", j0,
      "| altura(5) =", altura(5), "| altura(6) =", altura(6))
# La fusion en el paso 6 TAMBIEN vale en m = 0 (T^6(5) = T^6(6) = 4),
# pero la ALTURA no coincide porque el 5 toca el 1 en el paso 5, antes de fundirse.
if j0 != 6:
    print("aviso: encuentro de (5,6) no es 6 sino", j0)
v5 = 5
tray5 = [5]
for _ in range(6):
    v5 = paso(v5)
    tray5.append(v5)
print("trayectoria de 5, pasos 0..6:", tray5, " (toca el 1 en el paso 5)")
if altura(5) == altura(6):
    raise SystemExit("m = 0 deberia romper la igualdad de alturas y no la rompe")

# m = 1 explicito, y los m que la base dice haber probado
for m in [1, 2, 7, 100, 3125, 9999, 40000]:
    n1, n2 = 32 * m + 5, 32 * m + 6
    j = primer_encuentro(n1, n2)
    ok = (j == 6 and altura(n1) == altura(n2))
    print("m = %6d : par (%7d, %7d), encuentro en paso %s, alturas iguales: %s"
          % (m, n1, n2, j, ok))
    if not ok:
        raise SystemExit("FALLO en m = %d" % m)

# m negativo no forma parte del enunciado (m >= 1); no se evalua.

print("VEREDICTO LOCAL: identidad simbolica T^6(32m+5) = T^6(32m+6) = 18m+4 "
      "para todo m, minimo intermedio 7 > 1 con m >= 1, y fuerza bruta "
      "m = 1..%d sin un solo fallo. El enunciado SE SOSTIENE." % RANGO)
