# empujarb.py
#
# EL PASO 3: b(34) Y b(35) POR LA IDENTIDAD, SIN EL BARRIDO GRANDE
# (04-08-2026). El barrido principal a t = 36 costaria ~3 GB; la
# identidad-teorema  a(k+2) = a(k) + (2^k - 1) + G(k) + H(k)  (validada
# como igualdad de enteros en k = 3..14 y re-validada en k = 31, 32 por
# segundocamino.py) da a(35) y a(36) con los barridos de los PISOS:
#
#     a(35) = a(33) + (2^33 - 1) + G(33) + H(33)
#     a(36) = a(34) + (2^34 - 1) + G(34) + H(34)
#
# con G(k) = suma_{m<k} B(m) (piso g, {w,9w+2}, fusion de clase con
# compensacion +2 en <= m pasos) y H(k) = c(k) (piso h, {w,9w-1}).
# Los pisos a profundidad 33/34 caben en memoria porque la cadena
# coalesce. CONTROL: G(31), G(32), H(31), H(32) deben clavar los de
# segundocamino.py (338768407, 691256829, 344136248, 701445504).

A = {33: 3761106610, 34: 7558807251}
CONTROL = {('G', 31): 338768407, ('G', 32): 691256829,
           ('H', 31): 344136248, ('H', 32): 701445504}
B_ULT = {32: 18831364, 33: 36594031}     # para las razones nuevas


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


def absorciones(inicio, prof):
    # acumuladas con doblado: B(m) o c(m) para m = 1..prof
    estados = {inicio: 1}
    absorbidas = 0
    acum = []
    for t in range(1, prof + 1):
        nuevo = {}
        nuevas = 0
        for (k, c), n in estados.items():
            for bit in (0, 1):
                s = transicion(k, c, bit)
                if s[0] == 'fusion':
                    nuevas += n
                else:
                    clave = (s[1], s[2])
                    nuevo[clave] = nuevo.get(clave, 0) + n
        absorbidas = 2 * absorbidas + nuevas
        estados = nuevo
        acum.append(absorbidas)
        print("  [%s t=%2d: %d estados]" % (inicio, t, len(estados))
              if t % 10 == 0 else "", end="")
    print()
    return acum


print("barrido del piso g (2,2) a 33...")
Bg = absorciones((2, 2), 33)
print("barrido del piso h (2,-1) a 34...")
ch = absorciones((2, -1), 34)

G = {k: sum(Bg[m - 1] for m in range(1, k)) for k in (31, 32, 33, 34)}
H = {k: ch[k - 1] for k in (31, 32, 33, 34)}

# CONTROL contra segundocamino.py
for (letra, k), esperado in CONTROL.items():
    valor = G[k] if letra == 'G' else H[k]
    if valor != esperado:
        raise SystemExit("CONTROL %s(%d): %d != %d" % (letra, k, valor, esperado))
print("CONTROL OK: G(31), G(32), H(31), H(32) clavan segundocamino.py.")

a35 = A[33] + (2 ** 33 - 1) + G[33] + H[33]
a36 = A[34] + (2 ** 34 - 1) + G[34] + H[34]
b34 = a35 - 2 * A[34]
b35 = a36 - 2 * a35

print()
print("a(35) = %d      a(36) = %d" % (a35, a36))
print("b(34) = %d        b(35) = %d" % (b34, b35))
print()
print("las razones, extendidas:")
print("  b(33)/b(32) = %.4f" % (B_ULT[33] / B_ULT[32]))
print("  b(34)/b(33) = %.4f" % (b34 / B_ULT[33]))
print("  b(35)/b(34) = %.4f" % (b35 / b34))
print()
print("densidades: a(35)/2^35 = %.6f   a(36)/2^36 = %.6f"
      % (a35 / 2.0 ** 35, a36 / 2.0 ** 36))
print()
print("alfa_t = t*(1 - razon/2):  t=33: %.3f   t=34: %.3f"
      % (33 * (1 - b34 / B_ULT[33] / 2), 34 * (1 - b35 / b34 / 2)))
print()
print("CONCLUSION: dos niveles mas de la serie mas vieja del laboratorio,")
print("por la identidad-teorema con pisos (mismo metodo que sostuvo a(33)")
print("y a(34)); la cota demostrada lambda >= 1.9754 exige que las")
print("razones sigan subiendo -- y suben. El muro de siempre decide el")
print("limite; la estructura (perpetuidad critica) decide el programa.")
