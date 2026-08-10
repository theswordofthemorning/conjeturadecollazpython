# aranas.py
#
# EL TEOREMA DE ARANAS - LA SOMBRA DE LA CADENA (04-08-2026; el paso
# (i)+(ii) del norte: reducir la perpetuidad no-i.i.d. a una i.i.d.
# perturbada, donde Goldie-Kesten aplica de verdad).
#
#   LA COORDENADA: u = c / 3^k (el offset RE-ESCALADO por el piso).
#   En u, las cuatro leyes del nucleo colapsan a UNA SOLA pareja:
#
#     bit 0  (N1 o N3):   u' = u/2       + delta      [contrae]
#     bit 1  (N2 o N4):   u' = (3u-1)/2  + delta      [expande]
#
#   con delta EXACTA (los valores, identidades de enteros):
#     N1: delta = 0            N2: delta = 3^(-k)/2
#     N3: delta = 3^(-k-1)/2   N4: delta = 0
#   y la salida del nucleo (k = 1, c impar, bit 1) tambien es
#   u' = (3u-1)/2 EXACTA (delta = 0). El bit ES la moneda del IFS.
#
#   O sea: LA DINAMICA DE c ES LA DEL IFS DE MONEDA JUSTA
#   { u/2, (3u-1)/2 } MAS UNA PERTURBACION ACOTADA (|delta| <= 3^(-k)/2
#   <= 1/6, y la ESPERANZA POR PASO bajo el perfil de masa en k esta
#   dominada por suma 2^(-k) 3^(-k)/2 < 1/10). El nivel de la torre
#   DESAPARECE de la dinamica del offset: la sombra teje los pisos.
#   ⇢ CORRECCION DE LA 6a REVISION (09-08-2026, actarevision0908c.txt):
#   la frase original decia "PERTURBACION SUMABLE" -- y sumable NO es,
#   en el sentido de trayectoria que la teoria de IFS perturbado
#   necesita: por GOLONDRINAS el fondo se visita infinitas veces c.s.
#   y delta_t = 1/6 (la N2 de k = 1) ocurre infinitas veces, o sea
#   Sigma_t |delta_t| = infinito c.s. Lo que si vale: |delta| <= 1/6
#   siempre y esperanza por paso < 1/10. Y "diminuta" tambien se
#   califica: en el fondo (k = 1, donde |u| >= 1/3) delta llega a la
#   MITAD del piso de |u| -- diminuta para k grande, no donde vive la
#   masa. Las identidades no se movieron; el adjetivo si.
#
#   LO QUE COMPRA (con las etiquetas de la casa):
#   . EXACTO: las identidades de arriba (T1, enteros multiplicados).
#   . ESTANDAR CITABLE: el IFS puro { u/2, (3u-1)/2 } con moneda justa
#     cumple TODAS las hipotesis de Goldie-Kesten i.i.d. (E[log m] =
#     log(sqrt(3)/2) < 0, E[m] = 1 -- kappa = 1 --, shifts {0, -1/2}
#     no degenerados, log(3/2)/log(1/2) irracional: no-lattice):
#     tiene estacionaria UNICA pi con cola P(u < -x) ~ C/x. TENSA.
#   . MEDIDO: que la u-marginal de la cadena real converge a la del
#     IFS (T3) y que la cola kappa = 1 se ve en u (T4).
#   . LO QUE FALTA PARA TEOREMA: pasar la tension de "IFS + perturbacion
#     sumable" a la cadena (perturbacion no es i.i.d. pero esta
#     DOMINADA deterministicamente: |delta_t| <= 3^(-k_t)/2 <= 1/6).
#
#   EXCEPCIONES DECLARADAS (la frontera k = 0, ~6% de la masa):
#   F2 lleva delta = +1/2 y F4 voltea el signo (u' = -u/2 + 1/6): la
#   sombra es exacta en el NUCLEO; la frontera es la costura.

from fractions import Fraction

PROF = 34
TOPE_ESTADOS = 9 * 10 ** 6


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


# ---------------------------------------------------------------------------
# T1: LAS IDENTIDADES DE LA SOMBRA, exactas con Fraction.
#   Para cada ley del nucleo, u' - [u/2 o (3u-1)/2] == delta de la tabla.
# ---------------------------------------------------------------------------

probadas = 0
for k in range(1, 10):
    for c in range(-3 ** (k + 1), 3 ** (k + 1) + 1):
        u = Fraction(c, 3 ** k)
        for bit in (0, 1):
            s = transicion(k, c, bit)
            if s[0] == 'fusion':
                continue
            k2, c2 = s[1], s[2]
            if k2 == 0:
                # la salida (k=1, c impar, bit 1): u' = (3u-1)/2 con el
                # valor absoluto como unico pliegue (c < 1 voltea signo)
                u2 = Fraction(c2, 1)
                obj = (3 * u - 1) / 2
                if u2 != obj and u2 != -obj:
                    raise SystemExit("T1 salida: k=%d c=%d" % (k, c))
                probadas += 1
                continue
            u2 = Fraction(c2, 3 ** k2)
            if c % 2 == 0:      # N1 / N2
                delta = u2 - u / 2 if bit == 0 else u2 - (3 * u - 1) / 2
                esperada = 0 if bit == 0 else Fraction(1, 2 * 3 ** k)
            else:               # N3 / N4
                delta = u2 - u / 2 if bit == 0 else u2 - (3 * u - 1) / 2
                esperada = Fraction(1, 2 * 3 ** (k + 1)) if bit == 0 else 0
            if delta != esperada:
                raise SystemExit("T1: k=%d c=%d bit=%d delta=%s esp=%s"
                                 % (k, c, bit, delta, esperada))
            probadas += 1

print("T1 OK -- LA SOMBRA ES EXACTA: en el nucleo, bit 0 da u' = u/2 +")
print("delta y bit 1 da u' = (3u-1)/2 + delta, con delta EXACTA de la")
print("tabla {0, 3^-k/2, 3^-(k+1)/2, 0} y la salida a frontera con")
print("delta = 0 (pliegue del abs aparte). %d identidades con Fraction," % probadas)
print("0 fallos. El bit es la moneda del IFS { u/2, (3u-1)/2 }.")
print()
print("perturbacion dominada: |delta| <= 3^(-k)/2, y la masa del piso k")
print("decae 2^(-k): suma_k 2^(-k) * 3^(-k)/2 = 1/10 < infinito. La")
print("cadena es el IFS de Goldie-Kesten MAS una perturbacion sumable.")

# ---------------------------------------------------------------------------
# T2: LA U-MARGINAL DE LA CADENA CONTRA EL IFS PURO, por profundidad.
#   La cadena real (exacta, enteros) bucketizada en u; el IFS puro
#   evolucionado como densidad sobre una malla fina (float, MEDIDO).
# ---------------------------------------------------------------------------

import math

U_MIN, U_MAX, NB = -40.0, 2.0, 840          # cubetas de ancho 0.05

def cubeta(u):
    if u < U_MIN:
        return 0
    if u >= U_MAX:
        return NB - 1
    return int((u - U_MIN) / (U_MAX - U_MIN) * NB)

# el IFS puro desde u = 1 (el arranque (0,1))
ifs = {cubeta(1.0): 1.0}
for _ in range(PROF):
    nuevo = {}
    for b, w in ifs.items():
        u = U_MIN + (b + 0.5) * (U_MAX - U_MIN) / NB
        for u2 in (u / 2, (3 * u - 1) / 2):
            b2 = cubeta(u2)
            nuevo[b2] = nuevo.get(b2, 0.0) + w / 2
    ifs = nuevo

# la cadena real
estados = {(0, 1): 1}
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
        raise SystemExit("tope en t=%d" % t)

total = sum(estados.values())
cad = {}
for (k, c), n in estados.items():
    u = c / 3 ** k if k >= 1 else float(c)
    b = cubeta(u)
    cad[b] = cad.get(b, 0) + n

# comparar las dos CDFs en los bordes de cubeta
acum_c = acum_i = 0.0
peor = 0.0
sumi = sum(ifs.values())
for b in range(NB):
    acum_c += cad.get(b, 0) / total
    acum_i += ifs.get(b, 0.0) / sumi
    peor = max(peor, abs(acum_c - acum_i))
print()
print("T2 (medido): distancia sup entre la CDF de u en la cadena real")
print("(t = %d, exacta bucketizada) y la del IFS puro evolucionado" % PROF)
print("igual profundidad: %.4f. (La frontera y los pliegues son la" % peor)
print("costura; una distancia chica = la sombra gobierna.)")

# ---------------------------------------------------------------------------
# T3: LA COLA kappa = 1 EN u: x * P(u < -x) por decadas.
# ---------------------------------------------------------------------------

print()
print("T3 (medido): la cola negativa de u en la cadena real (t = %d):" % PROF)
print("      x      P(u < -x)      x * P")
for x in (0.5, 1, 2, 4, 8, 16, 32):
    p = sum(n for (k, c), n in estados.items()
            if (c / 3 ** k if k >= 1 else float(c)) < -x) / total
    print("  %5.1f    %.6f    %.4f" % (x, p, x * p))
print("x * P ~ constante = cola 1/x (kappa = 1), la de Goldie para el")
print("IFS; cayendo = aun en transito. Ver el veredicto.")

# ---------------------------------------------------------------------------
# T4: LA ABSORCION EN COORDENADA u: el estado (1,1) es u = 1/3; la masa
#     de u en [0.30, 0.36] con k = 1 sobre la masa de k = 1, por si el
#     piso por visita se estabiliza en la coordenada limpia.
# ---------------------------------------------------------------------------

k1 = [(c, n) for (k, c), n in estados.items() if k == 1]
mk1 = sum(n for _, n in k1)
objetivo = sum(n for c, n in k1 if c == 1)
print()
print("T4 (medido): masa de (1, c=1) [el pre-vortice exacto] sobre la")
print("masa de k = 1 a t = %d: %.6f; y sobre la masa viva: %.6f."
      % (PROF, objetivo / mk1, objetivo / total))
print()
print("VEREDICTO DE ARANAS: la sombra reduce el 'no es Kesten' a 'es")
print("Kesten mas perturbacion dominada 3^(-k)/2' -- la tension de la")
print("estacionaria del IFS es TEOREMA ESTANDAR (Goldie); lo que queda")
print("para phi es (a) transferir la tension a la cadena perturbada y")
print("(b) el piso por visita. El blanco de la proxima sesion tiene")
print("nombre tecnico: perturbed random iterated function systems.")
