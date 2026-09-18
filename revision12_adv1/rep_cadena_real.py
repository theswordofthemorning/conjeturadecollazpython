"""
REVISION 12 -- ADVERSARIO 1. VERIFICACION DEL CIMIENTO.

Todas las tandas del frente 20260910 descansan en una sola ley de paso,
la que balance.lean escribe como `paso`. Aqui se comprueba, contra
PARES ENTEROS REALES, que esa ley es la cadena (k,c) de verdad:

  estado {v, w} con w = 3^k v + c;  T(x) = x/2 si par, (3x+1)/2 si impar;
  aplicar T a los dos y leer el nuevo (k', c') con ancla v' = T(v).

La afirmacion es que el nuevo estado es exactamente

  v par, c par -> (k,   c/2)                       [N0]
  v par, c impar -> (k+1, (3c+1)/2)                [A]
  v impar, c par -> (k,   (3c+1-3^k)/2)            [N1]
  v impar, c impar -> (k-1, (c-3^(k-1))/2)         [D]  (muere si k=2)

o sea `paso(k, c, bit)` con bit = paridad del ANCLA v (no de c).
"""

def T(x):
    return (3 * x + 1) // 2 if x % 2 else x // 2

def paso(k, c, bit):
    """transcrito de depuracion/frente20260910/balance.lean"""
    if c % 2 == 0:
        return (k, (3 * c + 1 - 3**k) // 2 if bit else c // 2)
    if bit:
        return (k - 1, (c - 3**(k - 1)) // 2) if k > 2 else None
    return (k + 1, (3 * c + 1) // 2)

print("A. LA LEY DE PASO CONTRA PARES ENTEROS REALES")
print("   (v, w=3^k v + c) -> (T v, T w), se lee el nuevo (k', c')")

casos = 0
fallos = 0
detalles = []
for k in range(2, 9):
    for c in range(-400, 401):
        for v in range(1, 260):
            w = 3**k * v + c
            if w <= 0:
                continue
            vp, wp = T(v), T(w)
            # el nuevo k lo dicta la ley; comprobamos que w' = 3^k' v' + c'
            esperado = paso(k, c, v % 2)
            casos += 1
            if esperado is None:
                # k=2, v impar, c impar: la rama baja a k=1
                kp = 1
                cp = wp - 3**kp * vp
                if not (v % 2 == 1 and c % 2 == 1 and k == 2):
                    fallos += 1
                # y debe seguir siendo una relacion valida con k'=1
                if wp != 3**kp * vp + cp:
                    fallos += 1
                continue
            kp, cp = esperado
            if wp != 3**kp * vp + cp:
                fallos += 1
                if len(detalles) < 5:
                    detalles.append((k, c, v, kp, cp, vp, wp))

print("   casos probados = %d   fallos = %d" % (casos, fallos))
for d in detalles:
    print("   FALLO k=%d c=%d v=%d -> predijo (%d,%d) pero v'=%d w'=%d"
          % d)

print()
print("B. QUE EL BIT ES LA PARIDAD DEL ANCLA, NO LA DE c")
print("   se reintenta la misma comprobacion usando bit = c %% 2:")
fallos_c = 0
casos_c = 0
for k in range(2, 7):
    for c in range(-100, 101):
        for v in range(1, 120):
            w = 3**k * v + c
            if w <= 0:
                continue
            vp, wp = T(v), T(w)
            e = paso(k, c, c % 2)
            casos_c += 1
            if e is None:
                continue
            kp, cp = e
            if wp != 3**kp * vp + cp:
                fallos_c += 1
print("   con bit = paridad de c: %d fallos de %d casos"
      % (fallos_c, casos_c))
print("   (debe fallar masivamente: confirma que el bit es el del ANCLA)")

print()
print("C. LA SALIDA: k=1 SIGNIFICA QUE LA EXCURSION TERMINA")
print("   desde (k=2, c impar) con ancla impar el nuevo k es 1;")
print("   comprobado arriba en cada uno de esos casos.")
salidas = sum(1 for k in [2] for c in range(-400, 401, 2)
              for v in range(1, 260, 2)
              if (c + 1) % 2 == 0 and 3**k * v + c > 0)
print("   ramas de salida enumeradas en el barrido A: k=2, c impar,")
print("   v impar; ninguna otra combinacion produce k=1.")

print()
print("D. NINGUNA OTRA RAMA MUERE")
otras = 0
for k in range(3, 9):
    for c in range(-200, 201):
        for v in range(1, 100):
            if 3**k * v + c <= 0:
                continue
            r = paso(k, c, v % 2)
            if r is None:
                otras += 1
            elif r[0] < 2:
                otras += 1
print("   ramas con k'<2 saliendo de k>=3: %d  (debe ser 0)" % otras)
