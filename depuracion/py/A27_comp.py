# A27_comp.py - comprobacion propia del COMPARADOR, independiente de los dos agentes.
# Mapa del ATAJO. Enteros exactos. Nada de floats.
# Ataques:
#  [1] caso comun de los dos agentes: k=2, restos 1 y 2, m=0 (ciclo trivial {1,2})
#  [2] unicidad sobre TODO Z (el agente Lean solo cubrio Nat): fuerza bruta cruda
#      k=1..8, m en [-80,80], contando soluciones por clase SIN usar la formula
#  [3] toda solucion encontrada coincide con la formula cerrada
#  [4] borde k=0: denominador 0 y todo n es 0-ciclo (el enunciado necesita k>=1)
#  [5] el caso 221 del repo: A=41, B=73 con el atajo (k = B = 73, S = A = 41)

def T(n):
    # atajo sobre todo Z; las dos ramas dividen un par, la division es exacta
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2

def Tk_S(r, k):
    x, S = r, 0
    for _ in range(k):
        if x % 2 != 0:
            S += 1
        x = T(x)
    return x, S

# [1] caso comun
for r in (1, 2):
    tk, S = Tk_S(r, 2)
    den = 3 ** S - 4
    num = r - tk
    assert num % den == 0
    m = num // den
    n = 4 * m + r
    x = n
    for _ in range(2):
        x = T(x)
    print(f"[1] k=2 r={r}: T^2(r)={tk} S={S} m={m} n={n} cicla={x == n}")
    if m != 0 or x != n:
        raise SystemExit("[1] FALLO: el caso comun no da m=0 ciclando")

# [2]+[3] unicidad sobre Z, cruda
peor = 0
desacuerdos = 0
for k in range(1, 9):
    for r in range(2 ** k):
        tk, S = Tk_S(r, k)
        den = 3 ** S - 2 ** k
        if den == 0:
            raise SystemExit(f"[2] FALLO: denominador 0 en k={k} r={r}")
        soluciones = []
        for m in range(-80, 81):
            n = (2 ** k) * m + r
            x = n
            for _ in range(k):
                x = T(x)
            if x == n:
                soluciones.append(m)
        peor = max(peor, len(soluciones))
        num = r - tk
        m_formula = num // den if num % den == 0 else None
        for m in soluciones:
            if m != m_formula:
                desacuerdos += 1
print(f"[2] k=1..8, m=-80..80: maximo de soluciones por clase = {peor}")
print(f"[3] soluciones que la formula no da: {desacuerdos}")
if peor > 1:
    raise SystemExit("[2] FALLO: hay una clase con DOS candidatos -> unicidad rota")
if desacuerdos != 0:
    raise SystemExit("[3] FALLO: una solucion real no coincide con la formula")

# [4] borde k=0
print(f"[4] k=0: denominador 3^0 - 2^0 = {3**0 - 2**0} (indefinido); "
      f"T^0(n)=n para todo n -> infinitos candidatos, el enunciado exige k>=1")

# [5] el 221 con el atajo: 73 pasos, 41 impares
tk, S = Tk_S(221, 73)
print(f"[5] 221: T^73(221)={tk}, S={S} (esperado A=41)")
if S != 41:
    raise SystemExit("[5] FALLO: el 221 no da A=41 en el atajo")

print("COMPARADOR: 0 fallos en las cinco comprobaciones")
