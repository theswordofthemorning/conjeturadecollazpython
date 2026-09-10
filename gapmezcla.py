# gapmezcla.py
#
# CORRECCION 10-09-2026: G3/G5 usan SOLO k=3,5; C6 de
# correlacionafin.py usa k=2,3,4,5. No son el mismo operador.
# invariantes comunes de k=2,3: SOLO constantes, para todo 2^m,
# demostrado en depuracion/frente20260910/invariantes.lean.
# La exposicion historica de abajo queda acotada por esa distincion.
# Esto no prueba gap uniforme ni contraccion de la cadena real.
#
# EL GAP DE LA MEZCLA: ¿HAY EXPANSION O NO? (12-08-2026 (3), la
# continuacion directa de correlacionafin.py C6/C11 -- y la prueba
# de la ULTIMA reparacion que quedaba en pie.)
#
#   DE DONDE VIENE. correlacionafin.py dejo el teorema de conteo
#   reescrito como una desigualdad de norma sobre la combinacion
#   convexa de las corrientes, y propuso (C6, punto 9 de la nota)
#   que la forma del teorema seria de EXPANSION: la norma del
#   operador de MEZCLA menor que 1, con el argumento de que el
#   subespacio invariante COMUN de las corrientes es trivial
#   (medido: una sola clase en m = 4, 6, 8).
#
#   LA PREGUNTA QUE ESO DEJA ABIERTA, Y QUE AQUI SE MIDE. Invariante
#   comun trivial da norma < 1 en dimension finita, SI -- pero eso no
#   sirve de nada si la norma tiende a 1 al crecer m: el telescopio
#   necesita una cota UNIFORME en la escala. La pregunta correcta no
#   es "¿es < 1?" sino "¿se queda lejos de 1 cuando m crece?".
#
#   EL OBJETO. Para la fibra k, el par de corrientes compartidas es
#   el operador de promediado  M_k = (I + P_k)/2  con
#   (P_k f)(u) = f(tau_k(u)), tau_k(u) = 3u + s_k. En media cero:
#     - UN paso NO puede contraer: P_k tiene DOS ciclos, luego el
#       indicador con signo chi es invariante y ||M_k|| = 1 EXACTO
#       (es el contraejemplo de correlacionafin C3, visto como
#       operador). Esto se COMPRUEBA aqui, no se supone.
#     - DOS pasos con fibras distintas (k, k'): chi_k no es
#       invariante de P_k', asi que ||M_k' M_k|| < 1. LA PREGUNTA ES
#       CUANTO, y como se mueve con m.
#
#   COMPROBACIONES (SystemExit):
#     G1  chi es invariante exacto de P_k (enteros) y ||M_k|| = 1
#     G2  la power iteration reproduce un autovalor conocido en un
#         caso de control (el operador de traslacion pura, cuyo
#         espectro es explicito) -- el instrumento se calibra antes
#         de usarse
#     G3  la norma de los productos de dos y tres pasos, por escala:
#         LA MEDICION QUE DECIDE si la via de expansion sirve
#
#   Capa 1: esto NO mide la cadena -- mide OPERADORES sobre Z/2^m,
#   que es donde vive la reparacion propuesta. Si el gap se cierra
#   con m, la via muere aunque la cadena contraiga (la cadena
#   contraeria por OTRA razon: no tener masa en las frecuencias
#   malas). Es exactamente la distincion de la casa entre "el
#   operador suelto" y "la orbita del DP".

M_ESCALAS = [5, 6, 7, 8, 9]
K_FIBRAS = [2, 3, 4, 5]
ITERS = 400


def pot3(k, _cache={0: 1}):
    if k not in _cache:
        _cache[k] = 3 ** k
    return _cache[k]


def s_de_k(k):
    return (1 - pot3(k)) // 2


def tau_de(k, N):
    sk = s_de_k(k) % N
    return [(3 * u + sk) % N for u in range(N)]


def ciclos(tau):
    n = len(tau)
    visto = [False] * n
    out = []
    for r in range(n):
        if visto[r]:
            continue
        comp = []
        x = r
        while not visto[x]:
            visto[x] = True
            comp.append(x)
            x = tau[x]
        out.append(comp)
    return out


def aplica_M(f, tau):
    # (I + P)/2 con (P f)(u) = f(tau(u))
    return [(f[u] + f[tau[u]]) / 2.0 for u in range(len(f))]


def aplica_M_adj(f, tau):
    # el adjunto: (I + P^T)/2, con (P^T f)(v) = suma sobre u con
    # tau(u) = v -- como tau es biyeccion, es f(tau^-1(v))
    N = len(f)
    inv = [0] * N
    for u in range(N):
        inv[tau[u]] = u
    return [(f[v] + f[inv[v]]) / 2.0 for v in range(N)]


def centrar(f):
    m = sum(f) / float(len(f))
    return [x - m for x in f]


def norma(f):
    return sum(x * x for x in f) ** 0.5


def norma_operador(taus, N, iters=ITERS):
    # norma de M_{k_r} ... M_{k_1} restringida a media cero, por
    # power iteration sobre A^T A (A = el producto)
    f = [0.0] * N
    for u in range(N):
        f[u] = ((u * 1103515245 + 12345) % 1000) / 1000.0 - 0.5
    f = centrar(f)
    n = norma(f)
    f = [x / n for x in f]
    val = 0.0
    for _ in range(iters):
        g = f
        for tau in taus:
            g = aplica_M(g, tau)
        for tau in reversed(taus):
            g = aplica_M_adj(g, tau)
        g = centrar(g)
        n = norma(g)
        if n == 0:
            return 0.0
        val = n
        f = [x / n for x in g]
    return val ** 0.5


print("EL GAP DE LA MEZCLA: hay expansion o no?")
print("la ultima reparacion en pie (correlacionafin C6, nota punto 9)")
print("puesta a prueba -- MEDICION SOBRE OPERADORES, no sobre la")
print("cadena")
print("CORRECCION 10-09: los productos de G3/G5 usan solo k=3,5.")
print("No refutan C6 con k=2..5 ni la mezcla completa de la cadena.")
print()

# ---------------------------------------------------------------
print("G1  un paso NO contrae: chi es invariante exacto")
malos = 0
for m in M_ESCALAS:
    N = 2 ** m
    for k in K_FIBRAS:
        if k % 2 == 0:
            continue                    # el obstructor vive en k impar
        tau = tau_de(k, N)
        cs = ciclos(tau)
        if len(cs) != 2:
            raise SystemExit("G1: k impar sin dos ciclos (m=%d k=%d)"
                             % (m, k))
        chi = [0.0] * N
        for u in cs[0]:
            chi[u] = 1.0
        for u in cs[1]:
            chi[u] = -1.0
        img = aplica_M(chi, tau)
        if any(abs(img[u] - chi[u]) > 1e-12 for u in range(N)):
            malos += 1
        if abs(sum(chi)) > 1e-12:
            malos += 1
if malos:
    raise SystemExit("G1: chi no es invariante (%d)" % malos)
print("    (I + P_k)/2 deja chi FIJO y chi tiene media cero, en toda")
print("    escala m = 5..9 y toda fibra impar: ||M_k|| = 1 EXACTO en")
print("    media cero. UN PASO NO CONTRAE -- el contraejemplo de")
print("    correlacionafin C3, visto como operador.")
print()

# ---------------------------------------------------------------
print("G2  calibracion del instrumento (control con espectro conocido)")
# la traslacion pura por 1: P f(u) = f(u+1); (I+P)/2 tiene
# autovalores (1 + e^(2 pi i j / N))/2, modulo |cos(pi j / N)|.
# En media cero el mayor es |cos(pi/N)| (j = 1).
import math
for m in (5, 6, 7):
    N = 2 ** m
    tr = [(u + 1) % N for u in range(N)]
    med = norma_operador([tr], N)
    teo = abs(math.cos(math.pi / N))
    if abs(med - teo) > 1e-3:
        raise SystemExit("G2: la power iteration NO reproduce el "
                         "espectro conocido (m=%d: %.6f vs %.6f)"
                         % (m, med, teo))
    print("    m = %d :  medido %.6f   teorico |cos(pi/N)| %.6f  OK"
          % (m, med, teo))
print("    el instrumento reproduce un espectro conocido a 1e-3.")
print()

# ---------------------------------------------------------------
print("G3  LA MEDICION QUE DECIDE: norma del producto por escala")
print("    (media cero; k = 3 y 5 son las fibras impares del zocalo,")
print("     que son las que traen obstructor)")
print()
print("      m     1 paso (k=3)   2 pasos (3,5)   3 pasos (3,5,3)"
      "   1-norma")
for m in M_ESCALAS:
    N = 2 ** m
    t3 = tau_de(3, N)
    t5 = tau_de(5, N)
    n1 = norma_operador([t3], N)
    n2 = norma_operador([t3, t5], N)
    n3 = norma_operador([t3, t5, t3], N)
    print("     %2d     %10.6f   %13.6f   %15.6f   %8.2e"
          % (m, n1, n2, n3, 1.0 - n2))
print()
print("G4  EL TESTIGO EXPLICITO (sin power iteration -- capa 1: un")
print("    1,000000 de un metodo iterativo no se cree sin testigo)")
print("    EL PORQUE, en una linea de teoria: P manda caracteres a")
print("    caracteres, (P e_j)(u) = e^(2 pi i j s / N) * e_(3j)(u),")
print("    asi que M = (I+P)/2 actua sobre la ORBITA de j bajo")
print("    j -> 3j como (I + shift con fases)/2. En una orbita de")
print("    largo L ese operador tiene autovalores (1+w)/2 con w^L")
print("    fijo, luego alguno esta a angulo <= 2 pi / L de 1 y su")
print("    modulo es >= cos(pi/L). Y los ciclos de j -> 3j miden")
print("    ~2^(m-2): el gap es O(4^-m) POR CONSTRUCCION.")
print()
print("    [CAPA 1, EN VIVO: el primer testigo que se probo aqui fue")
print("     UN caracter suelto, y dio 0,707107 EXACTO en toda escala")
print("     -- justo lo que tenia que dar, porque P manda e_j a")
print("     e_(3j), que le es ORTOGONAL: ||e_j + fase e_3j||/2 =")
print("     sqrt(2)/2. El testigo no era malo por poco: estaba mal")
print("     construido. El casi-invariante es la COMBINACION sobre")
print("     la orbita entera, con los coeficientes del autovector.]")
print()
print("      m    L    cos(pi/2L)   testigo de orbita: 1 paso  2 pasos")
import cmath
for m in M_ESCALAS:
    N = 2 ** m
    t3 = tau_de(3, N)
    t5 = tau_de(5, N)
    # la orbita de j = 1 bajo j -> 3j (mod N) y su largo
    orb = [1]
    x = 3 % N
    while x != 1:
        orb.append(x)
        x = (3 * x) % N
    L = len(orb)
    s3 = s_de_k(3) % N
    # fases: P e_j = e^(2 pi i j s / N) e_(3j)
    fases = [cmath.exp(2j * cmath.pi * j * s3 / N) for j in orb]
    prod = 1 + 0j
    for z in fases:
        prod *= z
    # lambda^L = prod: se elige la raiz de argumento minimo
    arg0 = cmath.phase(prod) / L
    mejor1 = mejor2 = 0.0
    for r in range(L):
        lam = cmath.exp(1j * (arg0 + 2 * cmath.pi * r / L))
        # a_t = prod_{q<t} fase_q / lam^t
        a, acum = [1 + 0j], 1 + 0j
        for t in range(1, L):
            acum *= fases[t - 1]
            a.append(acum / lam ** t)
        # el vector en el espacio directo (parte real: f es real)
        v = [0j] * N
        for t, j in enumerate(orb):
            for u in range(N):
                v[u] += a[t] * cmath.exp(2j * cmath.pi * j * u / N)
        f = [z.real for z in v]
        f = centrar(f)
        n0 = norma(f)
        if n0 < 1e-9:
            continue
        g1 = centrar(aplica_M(f, t3))
        g2 = centrar(aplica_M(aplica_M(f, t3), t5))
        mejor1 = max(mejor1, norma(g1) / n0)
        mejor2 = max(mejor2, norma(g2) / n0)
    print("     %2d %5d   %.8f          %9.6f %9.6f"
          % (m, L, math.cos(math.pi / (2 * L)), mejor1, mejor2))
    if mejor1 < 0.9:
        raise SystemExit("G4: el testigo de orbita NO confirma la "
                         "ausencia de gap en m = %d (1 paso: %.6f)"
                         % (m, mejor1))
print()
print("    Testigos CONSTRUIDOS (autovector sobre la orbita de")
print("    frecuencias, sin iteracion): sobreviven a un paso con")
print("    razon > 0,9 en toda escala, y la razon SUBE con m. La")
print("    ausencia de gap NO es un artefacto del metodo iterativo:")
print("    tiene testigo explicito y razon teorica (cos(pi/2L) con")
print("    L ~ 2^(m-2)).")
print()
print("G5  LA DISCREPANCIA, RESUELTA POR BLOQUES (capa 1: G3 dio")
print("    1,000000 para dos pasos y el testigo de G4 solo 0,707 --")
print("    una de las dos esta mal, y no se publica ninguna hasta")
print("    saber cual)")
print("    LA VIA EXACTA: los DOS operadores usan el MISMO permutador")
print("    de frecuencias (j -> 3j; solo cambian las fases), asi que")
print("    las orbitas de frecuencia son bloques invariantes para los")
print("    dos a la vez. La norma del producto es entonces el MAXIMO")
print("    de las normas de bloques de tamano L -- cada uno chico y")
print("    con power iteration que si converge.")
print()


def norma_bloque(orbita, ss, N, iters=3000):
    # M_k en la base {e_j : j en orbita}: e_j -> (e_j + fase_j
    # e_(3j))/2, con fase_j = exp(2 pi i j s_k / N)
    L = len(orbita)
    pos = {j: t for t, j in enumerate(orbita)}
    mats = []
    for s in ss:
        A = [[0j] * L for _ in range(L)]
        for t, j in enumerate(orbita):
            A[t][t] += 0.5
            A[pos[(3 * j) % N]][t] += 0.5 * cmath.exp(
                2j * cmath.pi * j * s / N)
        mats.append(A)

    def mul(A, v):
        return [sum(A[i][t] * v[t] for t in range(L))
                for i in range(L)]

    def muladj(A, v):
        return [sum(A[i][t].conjugate() * v[i] for i in range(L))
                for t in range(L)]
    v = [complex((i * 7919 % 101) / 101.0 - 0.5,
                 (i * 6271 % 97) / 97.0 - 0.5) for i in range(L)]
    nv = sum(abs(z) ** 2 for z in v) ** 0.5
    v = [z / nv for z in v]
    val = 0.0
    for _ in range(iters):
        w = v
        for A in mats:
            w = mul(A, w)
        for A in reversed(mats):
            w = muladj(A, w)
        nv = sum(abs(z) ** 2 for z in w) ** 0.5
        if nv == 0:
            return 0.0
        val = nv
        v = [z / nv for z in w]
    return val ** 0.5


print("      m   bloques   ||1 paso||   ||2 pasos||   ||3 pasos||")
for m in M_ESCALAS:
    N = 2 ** m
    s3, s5 = s_de_k(3) % N, s_de_k(5) % N
    vistos = set()
    orbitas = []
    for j in range(1, N):            # j = 0 es la constante: fuera
        if j in vistos:
            continue
        o, x = [], j
        while x not in vistos:
            vistos.add(x)
            o.append(x)
            x = (3 * x) % N
        orbitas.append(o)
    n1 = max(norma_bloque(o, [s3], N) for o in orbitas)
    n2 = max(norma_bloque(o, [s3, s5], N) for o in orbitas)
    n3 = max(norma_bloque(o, [s3, s5, s3], N) for o in orbitas)
    print("     %2d %8d   %10.6f   %11.6f   %11.6f"
          % (m, len(orbitas), n1, n2, n3))
    if n1 < 0.9:
        raise SystemExit("G5: el bloque contradice a G4 en m = %d" % m)
print()
print("    LA DISCREPANCIA, EXPLICADA (y sin contradiccion): G4 midio")
print("    UN bloque -- el de la frecuencia j = 1, donde el testigo")
print("    de un paso da cos(pi/2L) clavado y el de dos pasos cae a")
print("    0,707 --, mientras G5 toma el MAXIMO sobre TODOS los")
print("    bloques. El peor bloque es otro, y ahi la norma es 1")
print("    EXACTA: hay orbitas de frecuencia cuyo producto de fases")
print("    es 1 (Sigma de la orbita = 0 mod N), y entonces el")
print("    autovalor lambda = 1 es alcanzable para los DOS")
print("    operadores k=3,5 a la vez. C6 incluyo TAMBIEN k=2,4:")
print("    no hubo un invariante oculto por el cambio de base, sino")
print("    un cambio de operadores. Con k=2,3 solo quedan constantes")
print("    (Lean: depuracion/frente20260910/invariantes.lean).")
print()
print("    ==> VEREDICTO ACOTADO: los productos (3), (3,5),")
print("    (3,5,3) tienen norma 1 en la ventana; el testigo comun")
print("    explica exactamente por que. Esto NO decide el gap")
print("    uniforme de mezclas con alturas pares, ni identifica")
print("    estos productos con las cuatro corrientes de la cadena.")
print()
print("    SIGUE ABIERTO: la contraccion del funcional condicional")
print("    con pesos y supervivencia. G6 mide la energia de la ley")
print("    en un bloque malo para (3,5); no prueba que evitar ese")
print("    bloque sea la unica fuente posible de contraccion.")
print()

# ---------------------------------------------------------------
# G6  ENTONCES, DONDE PONE MASA LA ORBITA?
# ---------------------------------------------------------------
print("G6  entonces, DONDE pone masa la orbita? (la pregunta que G5")
print("    deja abierta, medida sobre el DP real)")
print("    Si el operador no contrae pero la cadena si, la salida es")
print("    que la ley del DP no cargue los bloques malos. Aqui se")
print("    identifica el bloque PEOR de cada escala y se mide su")
print("    cuota de masa espectral en la ley real, contra la cuota")
print("    que le tocaria a ciegas (dim del bloque / (N-1)).")
print()

M_BITS_DP = 12
T_MAXDP = 25
T_MED = 24


def dp_correr(c0):
    # duplicado deliberado (la casa no importa ficheros: los ejecuta)
    M = T_MAXDP + M_BITS_DP
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


ARRANQUES = [(999983, "A"), (999999937, "B"),
             ((2 ** 21) - ((2 ** 21 + 1) // 3), "ADV")]
print("      m   bloque peor      a ciegas    cuota REAL (A/B/ADV)")
for m in (6, 7):
    N = 2 ** m
    s3 = s_de_k(3) % N
    vistos = set()
    orbitas = []
    for j in range(1, N):
        if j in vistos:
            continue
        o, x = [], j
        while x not in vistos:
            vistos.add(x)
            o.append(x)
            x = (3 * x) % N
        orbitas.append(o)
    peor, peor_o = -1.0, None
    for o in orbitas:
        v = norma_bloque(o, [s3], N, iters=600)
        if v > peor:
            peor, peor_o = v, o
    dim = len(peor_o)
    ciegas = dim / float(N - 1)
    cuotas = []
    for c0, nom in ARRANQUES:
        estados = dp_correr(c0)[T_MED]
        cuenta = {}
        for (kk, cm), n in estados.items():
            if 2 <= kk <= 5 and cm % 2 == 0:
                u = (cm // 2) % N
                cuenta[u] = cuenta.get(u, 0) + n
        masa = sum(cuenta.values())
        vec = [cuenta.get(u, 0) for u in range(N)]
        f = [N * x - masa for x in vec]
        F = []
        for j in range(N):
            s = 0j
            for u, x in enumerate(f):
                if x:
                    s += x * cmath.exp(-2j * cmath.pi * j * u / N)
            F.append(s)
        tot = sum(abs(F[j]) ** 2 for j in range(1, N))
        mala = sum(abs(F[j]) ** 2 for j in peor_o)
        cuotas.append(mala / tot if tot > 0 else 0.0)
    print("     %2d   norma %.4f dim %2d   %.4f      %.4f  %.4f  %.4f"
          % (m, peor, dim, ciegas, cuotas[0], cuotas[1], cuotas[2]))
print()
print("    LECTURA: si la cuota REAL queda por DEBAJO de la cuota a")
print("    ciegas, la ley del DP EVITA el bloque malo y ahi esta el")
print("    mecanismo -- el enunciado final seria 'la orbita del DP no")
print("    carga las orbitas de frecuencia invariantes'. Si queda por")
print("    ENCIMA, ni siquiera eso: la contraccion vendria de la")
print("    mezcla ENTRE fibras (los pesos w y las corrientes A/D), y")
print("    no del reparto espectral dentro de una fibra.")
print("    MEDICION a horizonte finito sobre el zocalo k = 2..5, dos")
print("    escalas, tres arranques. No es teorema: es la sonda que")
print("    dice por donde seguir.")
