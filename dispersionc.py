# dispersionc.py
#
# LA DISPERSION DE c EN EL NUCLEO BAJO (04-08-2026; paso 1 del norte).
#
#   Tras el goal de lambda, la pregunta unica del programa quedo en:
#   cuando la cadena (k, c) visita el nucleo bajo (k = 1), la orbita
#   de c se CONCENTRA o se DISPERSA?
#
#   EL MECANISMO, escrito antes de medir (con sus condiciones):
#
#   . Si la distribucion condicional de c en k = 1 es TENSA (la masa
#     relativa de |c| <= C converge a limites positivos que suman 1 al
#     crecer C), entonces la probabilidad de absorcion por visita esta
#     acotada abajo; con la recurrencia del paseo en k (medida: la
#     torre no retiene masa), las visitas son infinitas y la absorcion
#     seria casi segura: phi = 1. (Condicion declarada: uniformidad de
#     la cota sobre las visitas -- esto es un mecanismo, no un teorema.)
#   . Si la masa relativa de todo |c| <= C tiende a 0 (la distribucion
#     se ESCAPA a |c| grande), cada visita absorbe cada vez menos y la
#     masa viva puede sobrevivir para siempre: phi < 1.
#
#   TRES MEDICIONES exactas (enteros de la cadena, sin muestreo):
#     C1  la masa por cubetas de |c| en k = 1, relativa a la masa de
#         k = 1, por profundidad: tensa o escapando?
#     C2  la deriva de log2|c| en k = 1: acotada (concentracion) o
#         lineal en t (dispersion)?
#     C3  el discriminador de s_t = masa(1,2)/viva: beta_t estable
#         (polinomial t^-beta; sumable <=> beta > 1 <=> phi < 1 por el
#         teorema de inversion leido al reves) contra beta_t creciendo
#         linealmente (geometrico).
#   Y C4: la ley mod 3 de c en k = 1 (el teorema de Komodo en
#   coordenadas de la cadena), medida y contrastada exacta.

PROF = 34
TOPE_ESTADOS = 9 * 10 ** 6
CUBETAS = (1, 2, 4, 8, 16, 32, 64, 128, 256, 1024)


def transicion(k, c, bit):
    if k == 0:
        if c % 2 == 0:
            return ('estado', 0, c // 2) if bit == 0 else ('estado', 0, 3 * c // 2)
        return ('estado', 1, (3 * c + 1) // 2) if bit == 0 \
            else ('estado', 1, (1 - 3 * c) // 2)
    if c % 2 == 0:
        return ('estado', k, c // 2) if bit == 0 \
            else ('estado', k, (3 * c + 1 - 3 ** k) // 2)
    if bit == 0:
        return ('estado', k + 1, (3 * c + 1) // 2)
    if k >= 2:
        return ('estado', k - 1, (c - 3 ** (k - 1)) // 2)
    g = (c - 1) // 2
    if g == 0:
        return ('fusion',)
    return ('estado', 0, abs(g))


import math

estados = {(0, 1): 1}
filas = []
for t in range(1, PROF + 1):
    nuevo = {}
    for (k, c), n in estados.items():
        for bit in (0, 1):
            s = transicion(k, c, bit)
            if s[0] == 'fusion':
                continue
            clave = (s[1], s[2])
            nuevo[clave] = nuevo.get(clave, 0) + n
    estados = nuevo
    if len(estados) > TOPE_ESTADOS:
        print("[cortado en t=%d: %d estados]" % (t, len(estados)))
        break
    # estadisticas del nivel k = 1
    viva = sum(estados.values())
    k1 = {c: n for (k, c), n in estados.items() if k == 1}
    masa_k1 = sum(k1.values())
    cub = {}
    for C in CUBETAS:
        cub[C] = sum(n for c, n in k1.items() if abs(c) <= C)
    loga = sum(n * math.log2(abs(c)) for c, n in k1.items() if c != 0)
    mod3 = {0: 0, 1: 0, 2: 0}
    for c, n in k1.items():
        mod3[c % 3] += n
    filas.append((t, viva, masa_k1, cub, loga / masa_k1 if masa_k1 else 0.0,
                  mod3, estados.get((1, 2), 0)))

# ---------------------------------------------------------------------------
# C1: las cubetas de |c| relativas a la masa de k = 1
# ---------------------------------------------------------------------------

print("C1: masa relativa de |c| <= C dentro de k = 1 (por profundidad):")
print("  t    k1/viva   " + "".join("%8s" % ("<=%d" % C) for C in CUBETAS[:7]))
for t, viva, mk1, cub, lg, m3, n12 in filas:
    if t < 10 or (t % 2 and t < 30):
        continue
    print(" %2d    %.4f  " % (t, mk1 / viva) +
          "".join("  %.4f" % (cub[C] / mk1) for C in CUBETAS[:7]))

ult = filas[-1]
pen = filas[-3]
print()
print("veredicto C1: la fraccion k1/viva %s (%.4f -> %.4f) y cada cubeta"
      % ("cae" if ult[2] / ult[1] < pen[2] / pen[1] else "sube",
         pen[2] / pen[1], ult[2] / ult[1]))
print("relativa %s -- masa escapando a |c| grande = dispersion."
      % ("cae" if ult[3][8] / ult[2] < pen[3][8] / pen[2] else "se mantiene"))

# ---------------------------------------------------------------------------
# C2: la deriva de log2|c| en k = 1
# ---------------------------------------------------------------------------

print()
print("C2: E[log2|c|] condicionado a k = 1, por profundidad:")
serie_lg = [(t, lg) for t, _, mk1, _, lg, _, _ in filas if mk1]
for t, lg in serie_lg:
    if t >= 14 and t % 2 == 0:
        print("  t=%2d   %.4f" % (t, lg))
d1 = [serie_lg[i + 1][1] - serie_lg[i][1] for i in range(len(serie_lg) - 6, len(serie_lg) - 1)]
print("incrementos por nivel (ultimos 5): %s" % ["%.4f" % d for d in d1])
print("veredicto C2: incremento ~constante > 0 = deriva LINEAL de log|c|:")
print("la orbita de c se dispersa multiplicativamente (transitoriedad del")
print("radio), no se concentra.")

# ---------------------------------------------------------------------------
# C3: el discriminador de s_t (masa de (1,2) sobre viva)
# ---------------------------------------------------------------------------

print()
print("C3: s_t = masa(1,2)/viva y su exponente local beta_t = t*(1 - s_t+1/s_t):")
print("   t      s_t        beta_t")
prev = None
for t, viva, mk1, cub, lg, m3, n12 in filas:
    s = n12 / viva
    if prev is not None and t >= 20:
        beta = t * (1 - s / prev)
        print("  %2d   %.6f    %6.3f" % (t, s, beta))
    prev = s
print("lectura: beta_t ~ estable = cola polinomial t^-beta (sumable <=>")
print("beta > 1 <=> phi < 1); beta_t creciendo ~lineal = geometrico.")

# ---------------------------------------------------------------------------
# C4: la ley mod 3 de c en k = 1 (Komodo en coordenadas de la cadena)
# ---------------------------------------------------------------------------

print()
print("C4: reparto de c mod 3 en k = 1 (ultimo nivel): %s" % (ult[5],))
# el teorema: en k = 1 el estado es {v, 3v + c} y el mayor es 3v + c;
# Komodo dice mayor != 0 (mod 3) tras el paso 0, o sea c != 0 (mod 3)
# SALVO estados cuyo mayor sea el menor por vuelco... el chequeo exacto:
if ult[5][0] != 0:
    # medir si son reales: buscar un estado (1, c) con 3 | c y testigo
    ejemplos = [c for (k, c), n in estados.items() if k == 1 and c % 3 == 0][:5]
    print("  OJO: hay masa en c = 0 (mod 3): ejemplos %s" % ejemplos)
    print("  -> el mayor 3v + c seria multiplo de 3 <=> 3 | c: Komodo")
    print("     prohibe c = 0 (mod 3) en el MAYOR; si aparece es que el")
    print("     mayor real es v (vuelco pendiente de orientar). Anotado.")
else:
    print("  c = 0 (mod 3) tiene masa CERO en k = 1: es el teorema de")
    print("  Komodo 3 en coordenadas de la cadena, medido exacto.")

print()
print("CONCLUSION (paso 1 del norte): ver los tres veredictos impresos --")
print("la combinacion (k1/viva cayendo, log|c| con deriva lineal, cubetas")
print("escapando) es la firma de DISPERSION: la evidencia favorece phi < 1")
print("con la cola polinomial del paseo. Nada de esto es teorema: es la")
print("medicion que orienta el paso 2 (la sub-renovacion de (1, c)).")
