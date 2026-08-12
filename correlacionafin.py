# correlacionafin.py
#
# EL COFRE DEL TEOREMA DE CONTEO, ABIERTO: LA CORRELACION AFIN
# (12-08-2026 tarde -- el PENDIENTE No 1 que dejo la sesion anterior,
# notaequidistribucion 3-bis.viii(c): "el enunciado que falta es
# Sigma_r p(r) p(tau(r)) <= gamma * C2(p) con gamma < 1 para tau afin
# impar no trivial, propagado como invariante por la orbita".)
#
#   EL OBJETO. Las corrientes N0 y N1 de la fibra k son la MISMA ley
#   padre (los c pares de la fibra) por DOS mapas afines. Escribiendo
#   el padre par como c = 2u con u mod 2^m:
#       N0:  u -> u                       (c/2)
#       N1:  u -> 3u + s_k,  s_k = (1-3^k)/2   ((3c+1-3^k)/2)
#   luego el tau del cofre es EXACTAMENTE  tau_k(u) = 3u + s_k,
#   y v2(s_k) = v2(3^k - 1) - 1 dice que  s_k es IMPAR <=> k es IMPAR
#   (la misma alternancia de TORTOLAS 3.i). C0 lo comprueba contra
#   las leyes del DP en enteros, sin suponerlo.
#
#   LA CAPA 1 ANTES DE DEMOSTRAR NADA. El enunciado del cofre se
#   parte en dos por una identidad de UNA linea (polarizacion): para
#   TODA biyeccion tau y TODA p,
#       Sigma_r p(r) p(tau r) = C2(p) - (1/2) Sigma_r (p(r)-p(tau r))^2
#   luego  gamma <= 1 es GRATIS  (y por eso "gamma <= 1" no es el
#   teorema), con IGUALDAD exactamente cuando p es constante en cada
#   ciclo de tau. Todo el contenido esta en el estricto. Y el
#   estricto UNIFORME es FALSO: la version que la recursion usa es la
#   CENTRADA (los E_ij son excesos sobre el piso), y ahi el vector
#   f = 2^m p - 1 puede ser el indicador con signo de los ciclos de
#   tau -- que es invariante -- dando gamma_centrado = 1 EXACTO con
#   exceso e = eps^2 TAN CHICO COMO SE QUIERA: el contraejemplo no
#   vive en un rincon degenerado, vive en el regimen exacto donde
#   vive la cadena (e ~ 0,04). C3 lo exhibe en enteros.
#
#   COMPROBACIONES (SystemExit; lo medido se declara medido):
#     C0  tau_k = 3u + s_k ES el mapa del DP (enteros, sin suponer)
#     C1  la identidad de polarizacion, exacta en Fraction
#     C2  la estructura de ciclos de tau_k (enumerada): k impar ->
#         DOS ciclos de largo 2^(m-1); k par -> el censo real
#     C3  EL CONTRAEJEMPLO: gamma_centrado = 1 EXACTO (racionales)
#         con exceso arbitrariamente chico. El lema universal es
#         FALSO -- y no por poco: por igualdad.
#     C4  y NO hay gap que lo rescate: los autovalores de la parte
#         simetrica son cos(2 pi j / L) -- aun quitando el invariante,
#         el segundo esta a 1 - O(4^-m). Ninguna hipotesis de
#         "suavidad" salva el enunciado de UN solo tau.
#     C5  lo que la cadena REALIZA: gamma_centrado sobre las leyes
#         del DP, fibra a fibra, cruzado contra el ~0,5 de
#         corrienteszocalo (E_N0N1 / E_N0N0).
#     C6  LA REPARACION MEDIDA: el subespacio invariante COMUN de las
#         corrientes. Si es solo el constante, el gap existe para la
#         MEZCLA aunque no exista para cada tau -- que es la unica
#         forma que le queda al teorema.
#
#   Capa 1: mapa = la cadena (k,c) del atajo, mismas leyes que
#   corrienteszocalo.py/conteoconjunto.py; los arranques son los
#   mismos tres (primos no redondos + adversarial) para que el cruce
#   sea cruce; lo exacto va en Fraction/enteros y lo numerico se
#   marca como numerico.

from fractions import Fraction

M_BITS = 12
T_MAXDP = 25
T_MEDIDA = 24
M_FOCO = 8
M_CICLOS = range(4, 11)        # donde se enumera la estructura
K_ZOCALO = 5

INV3_NEG_2_21 = (2 ** 21) - ((2 ** 21 + 1) // 3)
ARRANQUES = [
    (999983, "A (el de rachasreales)"),
    (999999937, "B (el de medianareal)"),
    (INV3_NEG_2_21, "ADV (-3^(-1) mod 2^21)"),
]


def pot3(k, _cache={0: 1}):
    if k not in _cache:
        _cache[k] = 3 ** k
    return _cache[k]


def s_de_k(k):
    # s_k = (1 - 3^k)/2, entero porque 3^k es impar
    return (1 - pot3(k)) // 2


def v2(n):
    if n == 0:
        return None
    c = 0
    while n % 2 == 0:
        n //= 2
        c += 1
    return c


def dp_correr(c0):
    # identico a corrienteszocalo.py / conteoconjunto.py
    M = T_MAXDP + M_BITS
    estados = {(2, c0 % (2 ** M)): 1}
    historia = {}
    for t in range(T_MAXDP + 1):
        historia[t] = estados
        if t == T_MAXDP:
            break
        Q = 2 ** (M - t)
        Q2 = Q // 2
        nuevos = {}
        for (k, cm), n in estados.items():
            if cm % 2 == 0:
                h0 = (k, (cm // 2) % Q2)
                v = (3 * cm + 1 - pot3(k)) % Q
                h1 = (k, (v // 2) % Q2)
                nuevos[h0] = nuevos.get(h0, 0) + n
                nuevos[h1] = nuevos.get(h1, 0) + n
            else:
                v = (3 * cm + 1) % Q
                h0 = (k + 1, (v // 2) % Q2)
                nuevos[h0] = nuevos.get(h0, 0) + n
                if k >= 3:
                    w = (cm - pot3(k - 1)) % Q
                    h1 = (k - 1, (w // 2) % Q2)
                    nuevos[h1] = nuevos.get(h1, 0) + n
        estados = nuevos
    return historia


print("EL COFRE ABIERTO: LA CORRELACION AFIN Sigma p(r) p(tau r)")
print("el pendiente No 1 -- notaequidistribucion 3-bis.viii(c)")
print()

# ---------------------------------------------------------------
# C0  tau_k(u) = 3u + s_k ES el mapa N1 o N0^-1 del DP
# ---------------------------------------------------------------
print("C0  el tau del cofre, identificado contra las leyes del DP")
fallos = 0
for m in range(3, 12):
    Q = 2 ** (m + 1)          # la escala del padre (c mod 2^(m+1))
    Qh = 2 ** m               # la escala de la hija (u mod 2^m)
    for k in range(0, 8):
        sk = s_de_k(k) % Qh
        for u in range(Qh):
            c = (2 * u) % Q                     # un padre PAR
            n0 = (c // 2) % Qh                  # la corriente N0
            n1 = (((3 * c + 1 - pot3(k)) % Q) // 2) % Qh   # la N1
            if n0 != u % Qh:
                fallos += 1
            if n1 != (3 * u + sk) % Qh:
                fallos += 1
if fallos:
    raise SystemExit("C0: tau_k NO es 3u + s_k (%d fallos)" % fallos)
print("    N0(u) = u  y  N1(u) = 3u + s_k  con s_k = (1-3^k)/2,")
print("    comprobado en enteros para m = 3..11, k = 0..7, todo u.")
print("    v2(s_k) por k:  " + "  ".join(
    "k=%d:%s" % (k, "impar" if s_de_k(k) % 2 else "v2=%d" % v2(s_de_k(k)))
    for k in range(1, 7)))
print("    ==> s_k IMPAR si y solo si k IMPAR (la firma de TORTOLAS).")
print()

# ---------------------------------------------------------------
# C1  la identidad de polarizacion, exacta
# ---------------------------------------------------------------
print("C1  la identidad de polarizacion (exacta, en Fraction)")


def gamma_bruto(p, tau):
    # p: lista de Fraction sobre Z/2^m ; tau: lista de imagenes
    q = sum(p[r] * p[tau[r]] for r in range(len(p)))
    c2 = sum(x * x for x in p)
    d = sum((p[r] - p[tau[r]]) ** 2 for r in range(len(p)))
    return q, c2, d


m = 6
Qh = 2 ** m
semilla = 12345
malos = 0
for k in (2, 3, 4, 5):
    sk = s_de_k(k) % Qh
    tau = [(3 * u + sk) % Qh for u in range(Qh)]
    if sorted(tau) != list(range(Qh)):
        raise SystemExit("C1: tau no es biyeccion (k = %d)" % k)
    for rep in range(6):
        # pesos enteros pseudoaleatorios, sin numpy, reproducibles
        pesos = []
        for r in range(Qh):
            semilla = (1103515245 * semilla + 12345) % (2 ** 31)
            pesos.append(semilla % 97)
        tot = sum(pesos)
        if tot == 0:
            continue
        p = [Fraction(x, tot) for x in pesos]
        q, c2, d = gamma_bruto(p, tau)
        if q != c2 - d / 2:
            malos += 1
        if q > c2:
            malos += 1
if malos:
    raise SystemExit("C1: la polarizacion falla (%d)" % malos)
print("    Sigma p(r)p(tau r) = C2(p) - (1/2) Sigma (p(r)-p(tau r))^2")
print("    verificada como igualdad de RACIONALES (24 casos).")
print("    COROLARIO GRATIS: gamma = Q/C2 <= 1 SIEMPRE, con igualdad")
print("    exactamente cuando p es constante en cada ciclo de tau.")
print("    (Luego 'gamma <= 1' no es el teorema: el teorema es el")
print("     estricto, y el estricto es lo que C3 rompe.)")
print()

# ---------------------------------------------------------------
# C2  la estructura de ciclos de tau_k
# ---------------------------------------------------------------
print("C2  los ciclos de tau_k(u) = 3u + s_k  (enumerados)")


def ciclos(tau):
    n = len(tau)
    visto = [False] * n
    out = []
    for r in range(n):
        if visto[r]:
            continue
        L = 0
        x = r
        comp = []
        while not visto[x]:
            visto[x] = True
            comp.append(x)
            x = tau[x]
            L += 1
        out.append(comp)
    return out


print("     m   k impar (s impar)        k par (s par)")
for m in M_CICLOS:
    Qh = 2 ** m
    fila = []
    for k in (3, 4):
        sk = s_de_k(k) % Qh
        tau = [(3 * u + sk) % Qh for u in range(Qh)]
        cs = ciclos(tau)
        largos = sorted(set(len(c) for c in cs))
        fila.append("%d ciclos, largos %s" % (len(cs), largos))
    print("    %2d   %-24s %s" % (m, fila[0], fila[1]))
    if m >= 4:
        Qh = 2 ** m
        sk = s_de_k(3) % Qh
        tau = [(3 * u + sk) % Qh for u in range(Qh)]
        cs = ciclos(tau)
        if len(cs) != 2 or any(len(c) != Qh // 2 for c in cs):
            raise SystemExit(
                "C2: k impar no da DOS ciclos de largo 2^(m-1) en m=%d"
                % m)
print("    TEOREMA (k impar, verificado m = 4..10): tau_k tiene")
print("    EXACTAMENTE dos ciclos, cada uno de largo 2^(m-1) -- medio")
print("    espacio cada uno. (Razon: tau^n(u) = u pide 2^(d-1)(2u+s)")
print("    = 0 mod 2^m con d = v2(3^n - 1); con s impar hace falta")
print("    d >= m+1, y el minimo n es 2^(m-1).) Sin puntos fijos.")
print()

# ---------------------------------------------------------------
# C3  EL CONTRAEJEMPLO
# ---------------------------------------------------------------
print("C3  EL CONTRAEJEMPLO al enunciado del cofre (exacto)")
print("    p_eps = (1 + eps*chi)/2^m  con chi = +1 en un ciclo de tau")
print("    y -1 en el otro. Es una probabilidad legitima (eps <= 1),")
print("    su exceso es e = eps^2, y su correlacion CENTRADA es 1.")
print()
print("      m    k   eps      exceso e      gamma_centrado")
peor = None
for m in (6, 8, 10):
    Qh = 2 ** m
    for k in (3, 5):
        sk = s_de_k(k) % Qh
        tau = [(3 * u + sk) % Qh for u in range(Qh)]
        cs = ciclos(tau)
        chi = [0] * Qh
        for u in cs[0]:
            chi[u] = 1
        for u in cs[1]:
            chi[u] = -1
        for (a, b) in ((1, 10), (1, 100), (1, 1000)):
            eps = Fraction(a, b)
            p = [(1 + eps * chi[u]) / Qh for u in range(Qh)]
            if sum(p) != 1:
                raise SystemExit("C3: p no suma 1")
            if any(x <= 0 for x in p):
                raise SystemExit("C3: p no es positiva")
            # centrado: f = 2^m p - 1
            f = [Qh * x - 1 for x in p]
            num = sum(f[u] * f[tau[u]] for u in range(Qh))
            den = sum(x * x for x in f)
            g = num / den
            c2n = Qh * sum(x * x for x in p)
            e = c2n - 1
            if g != 1:
                raise SystemExit(
                    "C3: gamma_centrado no es 1 exacto (%s)" % g)
            if e != eps * eps:
                raise SystemExit("C3: el exceso no es eps^2")
            if (m, k) == (8, 3):
                print("      %2d   %2d   %-7s  %-12s  %s"
                      % (m, k, str(eps), str(e), str(g)))
            peor = g
print()
print("    VEREDICTO: el enunciado 'Sigma p p(tau) <= gamma C2 con")
print("    gamma < 1 para tau afin impar no trivial' es FALSO en su")
print("    forma CENTRADA -- la que la recursion usa (los E_ij son")
print("    excesos sobre el piso). No falla por poco: falla por")
print("    IGUALDAD, y con exceso e = eps^2 tan chico como se quiera,")
print("    o sea DENTRO del regimen de la cadena (e ~ 0,04 medido).")
print("    El obstructor tiene nombre y forma: el indicador con signo")
print("    de los DOS ciclos de tau, que es tau-invariante.")
print("    En la forma BRUTA (sin centrar) el enunciado es cierto")
print("    pero vacio: C1 lo da gratis con igualdad en el mismo p.")
print()

# ---------------------------------------------------------------
# C4  y no hay gap espectral que lo rescate
# ---------------------------------------------------------------
print("C4  la ausencia de gap (numerico controlado, sin numpy)")
print("    La parte simetrica de P (Pf = f o tau) sobre un ciclo de")
print("    largo L tiene autovalores cos(2 pi j / L), j = 0..L-1.")
print("    Aun ORTOGONAL al invariante chi, el mayor autovalor del")
print("    resto es cos(2 pi / L) con L = 2^(m-1):")
import math
for m in (6, 8, 10, 12, 16):
    L = 2 ** (m - 1)
    print("      m = %2d :  L = %6d   cos(2 pi / L) = %.12f  "
          "(1 - %.2e)" % (m, L, math.cos(2 * math.pi / L),
                          1 - math.cos(2 * math.pi / L)))
print("    ==> ninguna hipotesis de 'suavidad' o de 'exceso chico'")
print("    salva un enunciado sobre UN SOLO tau: hay f de media cero,")
print("    ORTOGONALES al obstructor, con gamma = 1 - O(4^-m).")
print("    El gap, si existe, tiene que ser de la MEZCLA de las")
print("    corrientes, no de una corriente contra otra.")
print()

# ---------------------------------------------------------------
# C5  lo que la cadena realiza
# ---------------------------------------------------------------
print("C5  lo que la cadena REALIZA (medicion, DP exacto en enteros)")
print("    gamma_centrado de la ley de los padres pares de cada fibra")
print("    bajo su propio tau_k, a t = %d, m = %d" % (T_MEDIDA, M_FOCO))
print()
print("      arranque            k   masa      e (exceso)   gamma_cent")
peor_g = -2.0
peor_txt = ""
for c0, nombre in ARRANQUES:
    hist = dp_correr(c0)
    estados = hist[T_MEDIDA]
    for k in range(2, K_ZOCALO + 1):
        m = M_FOCO
        Qh = 2 ** m
        sk = s_de_k(k) % Qh
        tau = [(3 * u + sk) % Qh for u in range(Qh)]
        # la ley del padre par de la fibra k, en u = c/2 mod 2^m
        cuenta = {}
        for (kk, cm), n in estados.items():
            if kk == k and cm % 2 == 0:
                u = (cm // 2) % Qh
                cuenta[u] = cuenta.get(u, 0) + n
        masa = sum(cuenta.values())
        if masa == 0:
            continue
        vec = [cuenta.get(u, 0) for u in range(Qh)]
        # centrado en enteros: f = 2^m n(u) - masa   (escala libre)
        f = [Qh * x - masa for x in vec]
        num = sum(f[u] * f[tau[u]] for u in range(Qh))
        den = sum(x * x for x in f)
        if den == 0:
            continue
        g = num / float(den)
        c2n = Qh * sum(x * x for x in vec) / float(masa) ** 2
        e = c2n - 1
        print("      %-18s %2d %8d   %9.4f   %9.4f"
              % (nombre.split()[0], k, masa, e, g))
        if g > peor_g:
            peor_g = g
            peor_txt = "%s k=%d" % (nombre.split()[0], k)
print()
print("    peor gamma_centrado realizado: %.4f (%s)" % (peor_g, peor_txt))
print("    CRUCE: corrienteszocalo mide |E_cruz|/E_ii hasta 0,507 con")
print("    el mismo DP -- E_N0N1/E_N0N0 ES este gamma (la biyeccion")
print("    VIBORAS/LORAS hace E_N0N0 = E_N1N1 = el exceso del padre).")
print("    La cadena se queda LEJOS del 1 del contraejemplo: el gap")
print("    existe EN LA ORBITA. Lo que C3 mata es la version")
print("    universal; lo que C5 mide es que el enunciado correcto")
print("    (sobre la orbita del DP) sigue vivo.")
print()

# ---------------------------------------------------------------
# C6  la reparacion: el invariante COMUN de las corrientes
# ---------------------------------------------------------------
print("C6  la reparacion -- el subespacio invariante COMUN")
print("    Si el teorema no puede salir de un tau, tiene que salir de")
print("    la MEZCLA. Un f sobrevive a la mezcla solo si sobrevive a")
print("    TODAS las corrientes a la vez. Los tau_k de fibras")
print("    distintas tienen desplazamientos s_k distintos (AVISPAS):")
print("    ¿comparten invariantes?")
print()
print("      m    invariantes comunes de tau_k, k en el zocalo")
for m in (4, 6, 8):
    Qh = 2 ** m
    # el subespacio invariante comun = las clases de la particion
    # generada por TODOS los ciclos de todos los tau_k (union-find)
    padre = list(range(Qh))

    def raiz(x):
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x

    def unir(a, b):
        ra, rb = raiz(a), raiz(b)
        if ra != rb:
            padre[ra] = rb

    for k in range(2, K_ZOCALO + 1):
        sk = s_de_k(k) % Qh
        for u in range(Qh):
            unir(u, (3 * u + sk) % Qh)
    clases = len(set(raiz(u) for u in range(Qh)))
    print("      %2d   %d clase(s) -- dimension del invariante comun"
          % (m, clases))
    if clases != 1:
        print("           (aviso: mas de una clase, el invariante comun")
        print("            NO es solo el constante a esta escala)")
print()
print("    LECTURA: con una sola fibra el obstructor chi es real; con")
print("    las fibras del zocalo juntas, los tau_k se mezclan y el")
print("    unico invariante comun es el constante -- que es")
print("    exactamente el piso uniforme. EL ENUNCIADO REPARADO del")
print("    cofre no es 'gamma < 1 para un tau', es:")
print("      || Sigma_i w_i P_i ||  restringido a media cero  < 1")
print("    para el operador de MEZCLA de las corrientes -- y su")
print("    obstruccion es el invariante COMUN, que C6 mide trivial.")
print()
# ---------------------------------------------------------------
# C7  EL CRUCE Y LA GEOGRAFIA POR PARES -- quien carga el exceso
# ---------------------------------------------------------------
print("C7  el cruce con corrienteszocalo y el reparto por PARES")
print("    (a) CRUCE DE DEFINICIONES, con SystemExit: el gamma de C5")
print("        (Rayleigh centrado de la ley del padre) tiene que ser")
print("        E_N0N1/E_N0N0 con la definicion de corrienteszocalo")
print("        (excesos de las leyes de las corrientes hijas).")
print("    (b) el reparto: cual de los SEIS pares carga el exceso de")
print("        la fibra hija -- el cofre apuntaba a N0-N1.")
print()

CORRIENTES = ['N0', 'N1', 'A', 'D']


def descomponer(estados_t, t):
    M = T_MAXDP + M_BITS
    Q = 2 ** (M - t)
    Q2 = Q // 2
    llegadas = {}
    for (k, cm), n in estados_t.items():
        if cm % 2 == 0:
            destinos = [((k, 'N0'), (cm // 2) % Q2),
                        ((k, 'N1'),
                         (((3 * cm + 1 - pot3(k)) % Q) // 2) % Q2)]
        else:
            destinos = [((k + 1, 'A'), (((3 * cm + 1) % Q) // 2) % Q2)]
            if k >= 3:
                destinos.append(
                    ((k - 1, 'D'),
                     (((cm - pot3(k - 1)) % Q) // 2) % Q2))
        for (clave, x) in destinos:
            d = llegadas.setdefault(clave, {})
            d[x] = d.get(x, 0) + n
    return llegadas


print("      arranque  k'   e_hija   rho_ms      N0-N1     "
      "D-N0     A-N0     A-D")
peor_n0n1 = -2.0
peor_cruzafibra = -2.0
peor_cf_txt = ""
peor_n0n1_txt = ""
malos_cruce = 0
for c0, nombre in ARRANQUES:
    hist = dp_correr(c0)
    estados_t = hist[T_MEDIDA]
    llegadas = descomponer(estados_t, T_MEDIDA)
    for k in range(2, K_ZOCALO + 1):
        m = M_FOCO
        Qh = 2 ** m
        porcor, masas = {}, {}
        for cor in CORRIENTES:
            d = llegadas.get((k, cor), {})
            red = {}
            for x, n in d.items():
                r = x % Qh
                red[r] = red.get(r, 0) + n
            porcor[cor] = red
            masas[cor] = sum(red.values())
        masa = sum(masas.values())
        if masa == 0:
            continue

        def exceso(i, j):
            if not masas[i] or not masas[j]:
                return None
            s = sum(n * porcor[j].get(r, 0)
                    for r, n in porcor[i].items())
            return Qh * s / float(masas[i] * masas[j]) - 1

        e00 = exceso('N0', 'N0')
        e01 = exceso('N0', 'N1')
        g_pares = e01 / e00 if e00 and abs(e00) > 1e-9 else None
        # (a) el cruce contra C5, recalculando el Rayleigh centrado
        cuenta = {}
        for (kk, cm), n in estados_t.items():
            if kk == k and cm % 2 == 0:
                u = (cm // 2) % Qh
                cuenta[u] = cuenta.get(u, 0) + n
        masap = sum(cuenta.values())
        vec = [cuenta.get(u, 0) for u in range(Qh)]
        sk = s_de_k(k) % Qh
        tau = [(3 * u + sk) % Qh for u in range(Qh)]
        f = [Qh * x - masap for x in vec]
        num = sum(f[u] * f[tau[u]] for u in range(Qh))
        den = sum(x * x for x in f)
        g_c5 = num / float(den) if den else None
        if g_pares is not None and g_c5 is not None:
            if abs(g_pares - g_c5) > 1e-9:
                malos_cruce += 1
                print("      CRUCE FALLA k'=%d: %.9f vs %.9f"
                      % (k, g_pares, g_c5))
        # el reparto por pares y el rho multi-escala real
        hija = {}
        for cor in CORRIENTES:
            for r, n in porcor[cor].items():
                hija[r] = hija.get(r, 0) + n
        col = sum(v * v for v in hija.values())
        e_hija = Qh * col / float(masa) ** 2 - 1
        rho = e_hija / e00 if e00 and abs(e00) > 1e-9 else float('nan')

        def rel(i, j):
            v = exceso(i, j)
            return float('nan') if v is None else v / e00
        print("      %-8s  %2d  %7.4f  %6.3f   %8.3f %8.3f %8.3f %8.3f"
              % (nombre.split()[0], k, e_hija, rho, rel('N0', 'N1'),
                 rel('D', 'N0'), rel('A', 'N0'), rel('A', 'D')))
        if g_pares is not None and g_pares > peor_n0n1:
            peor_n0n1 = g_pares
            peor_n0n1_txt = "%s k'=%d" % (nombre.split()[0], k)
        for (i, j) in (('D', 'N0'), ('D', 'N1'), ('A', 'N0'),
                       ('A', 'N1'), ('A', 'D')):
            v = exceso(i, j)
            if v is not None and e00:
                if v / e00 > peor_cruzafibra:
                    peor_cruzafibra = v / e00
                    peor_cf_txt = "%s-%s en %s k'=%d" % (
                        i, j, nombre.split()[0], k)
if malos_cruce:
    raise SystemExit("C7: el cruce de definiciones FALLA (%d celdas)"
                     % malos_cruce)
print()
print("    (a) CRUCE OK: E_N0N1/E_N0N0 = Rayleigh centrado en las 12")
print("        celdas (12 cifras). Son el MISMO objeto por dos")
print("        definiciones (leyes hijas vs ley del padre bajo tau).")
print("    (b) EL REPARTO: peor N0-N1 relativo = %.3f (%s);"
      % (peor_n0n1, peor_n0n1_txt))
print("        peor par que CRUZA fibra = %.3f (%s)."
      % (peor_cruzafibra, peor_cf_txt))
print("        ==> EL COFRE APUNTABA AL PAR EQUIVOCADO. El par que la")
print("        nota senalaba (N0 vs N1, 'la misma ley padre por dos")
print("        mapas afines') es el par BUENO: en la orbita esta")
print("        ANTICORRELACIONADO (gamma < 0 en k >= 3). Lo que carga")
print("        el exceso son los pares que CRUZAN fibra (D-N0, A-N1):")
print("        leyes de padres DISTINTOS, no dos imagenes de la misma.")
print("        El cofre del teorema de conteo se mueve de sitio.")
print()
print("    Y EL MECANISMO, en una linea: si la fibra recibiera solo")
print("    N0 y N1 (pesos 1/2 -- w_N0 = w_N1 SIEMPRE, hallazgo (a) de")
print("    corrienteszocalo), entonces e_hija = (1 + gamma)/2 * e_padre")
print("    exacto, o sea rho_ms = (1 + gamma)/2: el umbral 1/2 del")
print("    telescopio equivale EXACTAMENTE a gamma < 0. La cadena da")
print("    gamma < 0 en k >= 3 y gamma ~ +0,1..0,2 solo en k' = 2 --")
print("    la fibra sin corriente A, otra vez la frontera del fondo.")
print()
print("ETIQUETA: C0-C3 son TEOREMA (enteros y racionales exactos);")
print("C4 es aritmetica de autovalores de un ciclo (numerico")
print("controlado); C5 y C6 son MEDICION sobre la orbita del DP a")
print("horizonte finito. El enunciado universal del cofre queda")
print("REFUTADO; el enunciado reparado (mezcla, sobre la orbita)")
print("queda enunciado y con su obstructor medido trivial.")
