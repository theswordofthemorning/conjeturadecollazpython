# A16 - verificacion independiente, escrita desde cero.
#
# ENUNCIADO: T(2^k - n) = 3*2^k + 2 - T(n)  "en los impares casi conmuta,
# pero sobra un +2". Ambito declarado: n impar. Estado: demostrado (algebra).
#
# INTERPRETACION: T es el paso del mapa CLASICO (par -> n/2, impar -> 3n+1).
# Para n impar y 1 <= n < 2^k, el espejo 2^k - n tambien es impar, y
#   T(2^k - n) = 3*(2^k - n) + 1 = 3*2^k - 3n + 1
#   3*2^k + 2 - T(n) = 3*2^k + 2 - (3n + 1) = 3*2^k - 3n + 1
# o sea que la identidad es algebra de dos lineas SOBRE EL MAPA CLASICO.
# Con el mapa del atajo ((3n+1)/2) la constante correcta seria 3*2^(k-1)+1,
# no 3*2^k+2 -> el enunciado solo cuadra con el clasico. Lo compruebo.
#
# Todo con int exacto. Nada de floats.

def paso_clasico(n):
    if n % 2 == 0:
        return n // 2
    return 3 * n + 1

def paso_atajo(n):
    if n % 2 == 0:
        return n // 2
    return (3 * n + 1) // 2

# ---------------------------------------------------------------
# 1) NUCLEO: exhaustivo en n impar, 1 <= n < 2^k, para k = 1..16
# ---------------------------------------------------------------
casos = 0
fallos = 0
for k in range(1, 17):
    M = 2 ** k
    for n in range(1, M, 2):        # todos los impares del bloque
        esp = M - n                 # el espejo; es impar porque n es impar y M par
        if esp % 2 != 1:
            raise SystemExit("ERROR interno: espejo no impar, n=%d k=%d" % (n, k))
        lhs = paso_clasico(esp)
        rhs = 3 * M + 2 - paso_clasico(n)
        casos += 1
        if lhs != rhs:
            fallos += 1
            if fallos <= 5:
                print("FALLO impar: k=%d n=%d lhs=%d rhs=%d" % (k, n, lhs, rhs))
print("[1] clasico, n impar, k=1..16 exhaustivo: %d casos, %d fallos" % (casos, fallos))
if fallos:
    raise SystemExit("ROTO: la identidad falla en impares")

# ---------------------------------------------------------------
# 2) BORDES dentro del ambito: n=1 y n=2^k-1 explicitos
# ---------------------------------------------------------------
for k in range(1, 17):
    M = 2 ** k
    assert paso_clasico(M - 1) == 3 * M + 2 - paso_clasico(1)
    assert paso_clasico(1) == 3 * M + 2 - paso_clasico(M - 1)
print("[2] bordes n=1 y n=2^k-1: exactos en k=1..16")

# ---------------------------------------------------------------
# 3) FUERA DEL AMBITO: n PAR. El enunciado dice "en los impares";
#    compruebo que con n par la identidad es FALSA (y cuento cuantas veces).
#    Con n par: lhs = (2^k - n)/2 = 2^(k-1) - n/2, rhs = 3*2^k + 2 - n/2.
#    lhs = rhs exigiria 2^(k-1) = 3*2^k + 2, imposible -> debe fallar SIEMPRE.
# ---------------------------------------------------------------
casos_par = 0
fallos_par = 0
for k in range(2, 13):
    M = 2 ** k
    for n in range(2, M, 2):
        lhs = paso_clasico(M - n)
        rhs = 3 * M + 2 - paso_clasico(n)
        casos_par += 1
        if lhs != rhs:
            fallos_par += 1
print("[3] n par (fuera de ambito): %d casos, %d fallos (esperado: fallo total)"
      % (casos_par, fallos_par))
if fallos_par != casos_par:
    raise SystemExit("SORPRESA: algun n par cumple la identidad")

# ---------------------------------------------------------------
# 4) MAPA DEL ATAJO: la misma forma con constante 3*2^k+2 debe FALLAR,
#    y con la constante corregida 3*2^(k-1)+1 debe CUMPLIRSE.
#    (Discrimina el mapa: el enunciado es del clasico.)
# ---------------------------------------------------------------
f_mal = 0
f_bien = 0
casos_at = 0
for k in range(2, 13):
    M = 2 ** k
    for n in range(1, M, 2):
        esp = M - n
        casos_at += 1
        if paso_atajo(esp) != 3 * M + 2 - paso_atajo(n):
            f_mal += 1
        if paso_atajo(esp) != 3 * (M // 2) + 1 - paso_atajo(n):
            f_bien += 1
print("[4] atajo: con 3*2^k+2 fallan %d de %d; con 3*2^(k-1)+1 fallan %d de %d"
      % (f_mal, casos_at, f_bien, casos_at))
if f_mal != casos_at or f_bien != 0:
    raise SystemExit("El diagnostico de mapa no cuadra")

# ---------------------------------------------------------------
# 5) DONDE SE ROMPE DE VERDAD (la nota de la base dice "al segundo se rompe").
#    Con el mapa CLASICO y n impar:
#      T(n) = 3n+1 es PAR siempre, asi que T^2(n) = (3n+1)/2 en los dos lados
#      -> T^2 tambien conmuta, con constante 3*2^(k-1)+1 (algebra directa).
#    La suma T^2(esp)+T^2(n) = 3*2^(k-1)+1 es IMPAR (k>=2), luego un lado es
#    par y el otro impar -> en el TERCER paso las ramas divergen y se rompe.
#    Lo mido: numero de valores distintos de T^j(esp)+T^j(n) para j=1,2,3.
# ---------------------------------------------------------------
def iterar(n, j):
    for _ in range(j):
        n = paso_clasico(n)
    return n

for k in [6, 8, 10]:
    M = 2 ** k
    for j in [1, 2, 3]:
        sumas = set()
        for n in range(1, M, 2):
            sumas.add(iterar(M - n, j) + iterar(n, j))
        print("[5] k=%d j=%d: T^j(esp)+T^j(n) toma %d valores distintos"
              % (k, j, len(sumas)), "->", sorted(sumas)[:3] if len(sumas) <= 3 else "varios")
    # comprobacion dura del paso 2: constante exacta 3*2^(k-1)+1
    for n in range(1, M, 2):
        if iterar(M - n, 2) != 3 * (M // 2) + 1 - iterar(n, 2):
            raise SystemExit("el paso 2 NO conmuta en k=%d n=%d" % (k, n))
print("[5b] T^2(2^k - n) = 3*2^(k-1)+1 - T^2(n) exacto en todos los impares, k=6,8,10")
print("[5c] CONCLUSION: con el mapa clasico se rompe en el TERCER paso, no en el segundo.")
print("     (El 'segundo paso' de la nota solo es correcto contando pasos del ATAJO.)")

# ---------------------------------------------------------------
# 6) BORDE k=0: 2^0 - n = 1 - n; con n=1 el espejo es 0 y T(0) no esta
#    definido en el dominio (0 -> 0, y ademas 0 no es positivo).
#    Queda declarado como excluido, no comprobado.
# ---------------------------------------------------------------
print("[6] k=0 excluido: el espejo 1-n no es positivo para n>=1")

print()
print("VEREDICTO LOCAL: identidad exacta para n impar, 1 <= n < 2^k, mapa CLASICO.")
print("Total impares comprobados:", casos)
