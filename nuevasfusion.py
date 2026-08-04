# nuevasfusion.py
#
# LA ECUACION DE LAS CLASES NUEVAS (CIERVAS): b(k) cuenta encuentros en vortices.
#
#   clasesfusion.py demostro que cada clase buena mod 2^k se desdobla en dos
#   buenas mod 2^(k+1), asi que lo unico con contenido son las NUEVAS:
#   b(k) = a(k+1) - 2*a(k). La pregunta grande del repo (si la razon
#   b(k+1)/b(k) llega a 2) es sobre esa sucesion, y hasta hoy solo se podia
#   atacar restando dos barridos de 2^k.
#
#   ESTE FICHERO ESTABLECE QUE LAS NUEVAS TIENEN ECUACION (03-08-2026):
#
#   una clase r mod 2^(k+1) se estrena en el nivel k+1 exactamente cuando
#   los iterados a = T^k(r) y b = T^k(r+1) son DISTINTOS pero T los junta
#   en el paso k+1. Y T(a) = T(b) con a != b fuerza paridades opuestas y
#
#       a = 3b + 1  (b impar)     o     b = 3a + 1  (a impar)
#
#   -- la regla del segundo padre (v = 4 mod 6), la misma de los 51 vortices
#   del 221. El encuentro compensa las cuentas: S difiere exactamente en 1
#   antes del paso, y queda igualado al darlo (el lado impar suma su unidad).
#
#   O sea: b(k) cuenta los pares consecutivos cuyas trayectorias SE FUNDEN
#   POR PRIMERA VEZ EN UN VORTICE en el paso exacto k+1. La pregunta de la
#   razon 2 pasa de un conteo ciego a una congruencia con estructura.
#
#   Todo con el mapa del ATAJO ((3n+1)/2 en los impares), que es el de
#   clasesfusion.py. Comprobaciones antes de concluir, SystemExit si fallan.

K_MIN = 3       # primer nivel con clase buena (r = 4 mod 8)
K_MAX = 15      # ultimo k cuyo nivel k+1 se comprueba (2^16 restos: segundos)

# b(k) publicado en sucesiones.txt (k = 3 ...), para el cruce final
B_PUBLICADA = [1, 2, 2, 3, 4, 6, 11, 19, 34, 60, 106, 190, 341]


def paso(x):
    # el mapa del atajo
    return (3 * x + 1) // 2 if x % 2 else x // 2


def iterar(r, k):
    # devuelve (T^k(r), S_k(r)) por iteracion cruda, sin formula
    S = 0
    for _ in range(k):
        if r % 2:
            S += 1
        r = paso(r)
    return r, S


def buenas(k):
    # los r con el par (r, r+1) fundido en el paso k: mismo iterado y mismo S
    # (el criterio demostrado de clasesfusion.py; r+1 < 2^k, sin cruzar borde)
    res = set()
    for r in range(2 ** k - 1):
        a, Sa = iterar(r, k)
        b, Sb = iterar(r + 1, k)
        if a == b and Sa == Sb:
            res.add(r)
    return res


b_medida = []
for k in range(K_MIN, K_MAX + 1):
    Bk = buenas(k)
    Bk1 = buenas(k + 1)
    nuevas = sorted(r for r in Bk1 if (r % 2 ** k) not in Bk)
    heredadas = len(Bk1) - len(nuevas)

    # COMPROBACION 1: el doblado demostrado (cada buena hereda dos hijas)
    if heredadas != 2 * len(Bk):
        raise SystemExit("FALLO doblado: k=%d heredadas=%d, 2*a(k)=%d"
                         % (k, heredadas, 2 * len(Bk)))

    # COMPROBACION 2: toda nueva cumple la ecuacion del vortice
    for r in nuevas:
        a, Sa = iterar(r, k)
        b, Sb = iterar(r + 1, k)
        if a == b:
            raise SystemExit("FALLO: r=%d (k=%d) ya coincidia en el paso k"
                             % (r, k))
        junta = paso(a) == paso(b)
        vortice = (a == 3 * b + 1 and b % 2 == 1) or \
                  (b == 3 * a + 1 and a % 2 == 1)
        if not (junta and vortice and abs(Sa - Sb) == 1):
            raise SystemExit("FALLO ecuacion: k=%d r=%d a=%d b=%d Sa=%d Sb=%d"
                             % (k, r, a, b, Sa, Sb))

    # COMPROBACION 3 (el reciproco): ningun resto NO bueno a nivel k+1
    # cumple el encuentro compensado. Sin esto la ecuacion seria necesaria
    # pero no caracterizacion.
    for r in range(2 ** (k + 1) - 1):
        if r in Bk1:
            continue
        a, Sa = iterar(r, k)
        b, Sb = iterar(r + 1, k)
        if a != b and paso(a) == paso(b) and Sa + (a % 2) == Sb + (b % 2):
            raise SystemExit("FALLO reciproco: k=%d r=%d cumple y no es buena"
                             % (k, r))

    # COMPROBACION 6: LOS ESTRATOS POR PASOS MIXTOS (03-08-2026).
    #
    #   Un paso es MIXTO cuando las paridades del par difieren -- que ocurre
    #   exactamente cuando la diferencia d es impar. Delta_S cambia +-1 solo
    #   en pasos mixtos, y como empieza y termina en 0 (la fusion exige S
    #   igual), |M| ES PAR SIEMPRE: eso es un teorema de tres lineas, y aqui
    #   se comprueba en cada nueva. Ademas, MEDIDO (no demostrado): el
    #   estrato |M| = 2 tiene EXACTAMENTE UNA clase por nivel -- y es la
    #   familia del repunit de la COMPROBACION 5 --, y |M| = 4 tambien tiene
    #   exactamente una. Los estratos altos crecen como polinomios de grado
    #   creciente y entra un estrato nuevo cada dos niveles: la razon
    #   b(k+1)/b(k) -> 2 vendria de la ENTRADA de estratos, no de que cada
    #   estrato acelere. Es la forma de recursion tipo A076227/Zarubin.
    estratos = {}
    for r in nuevas:
        x, y = r, r + 1
        mixtos = 0
        for _ in range(k + 1):
            if (x % 2) != (y % 2):
                mixtos += 1
            x, y = paso(x), paso(y)
        if mixtos % 2 != 0:
            raise SystemExit("FALLO estrato: |M| impar en r=%d (k+1=%d): %d"
                             % (r, k + 1, mixtos))
        estratos[mixtos] = estratos.get(mixtos, 0) + 1
    if estratos.get(2, 0) != 1:
        raise SystemExit("FALLO estrato: |M|=2 tiene %d clases en k+1=%d "
                         "(medido: siempre exactamente 1)"
                         % (estratos.get(2, 0), k + 1))
    if k >= 4 and estratos.get(4, 0) != 1:
        raise SystemExit("FALLO estrato: |M|=4 tiene %d clases en k+1=%d "
                         "(medido: siempre exactamente 1 desde k+1=5)"
                         % (estratos.get(4, 0), k + 1))

    b_medida.append(len(nuevas))
    print("k=%2d  a(k)=%6d  nuevas=%5d  ecuacion %d/%d, reciproco limpio, "
          "estratos |M|: %s"
          % (k, len(Bk), len(nuevas), len(nuevas), len(nuevas),
             dict(sorted(estratos.items()))))

# COMPROBACION 4: el conteo reproduce la sucesion publicada
if b_medida != B_PUBLICADA[:len(b_medida)]:
    raise SystemExit("FALLO cruce: b medida %s != publicada %s"
                     % (b_medida, B_PUBLICADA[:len(b_medida)]))

# ---------------------------------------------------------------------------
# COMPROBACION 5: LA FAMILIA EXTREMAL - EL TEOREMA DE CONEJAS (03-08-2026).
#
#   Midiendo QUE vortices producen las nuevas salio que el b maximo de cada
#   nivel es un REPUNIT TERNARIO -- 13, 121, 1093, 9841, 88573, 797161 son
#   (3^m - 1)/2 con m impar -- y que el resto extremal es el par "casi todo
#   unos" (2^j - 2, 2^j - 1). Eso se demuestra en cuatro lineas, con j PAR:
#
#     lado 2^j - 1:  j impares seguidos -> 3^j - 1 (paso j), luego dos pasos
#                    pares -> (3^j - 1)/2 -> (3^j - 1)/4.        S = j.
#     lado 2^j - 2:  un par -> 2^(j-1) - 1, luego j-1 impares -> 3^(j-1) - 1
#                    (paso j), un par -> b = (3^(j-1) - 1)/2, que es IMPAR
#                    porque j-1 es impar -> (3b + 1)/2.          S = j.
#
#   Y el encuentro cuadra exacto: 3b + 1 = (3^j - 1)/2, o sea los dos caminos
#   caen en el MISMO numero en el paso j+2, con la misma S, y en el paso j+1
#   todavia difieren (b impar contra (3^j - 1)/2 par). Luego la clase
#   r = 2^j - 2 es buena mod 2^(j+2) y NO buena mod 2^(j+1): ES NUEVA.
#
#   COROLARIO: b(j+2) >= 1 para todo j par -- las nuevas nunca se acaban --
#   con el vortice en el repunit (3^(j-1) - 1)/2. Que ese b sea ademas el
#   MAXIMO del nivel esta solo medido (k = 3..15), no demostrado.
#
#   AVISO DE PATRON REFUTADO, para no rederivarlo: "todo b es 1 mod 3" vale
#   hasta k+1 = 14 y SE ROMPE en k+1 = 15 con b = 2255 = 2 (mod 3)
#   (r = 16891). Era muestra chica, no ley. No publicarlo.
# ---------------------------------------------------------------------------

for j in range(4, 61, 2):
    x, y = 2 ** j - 2, 2 ** j - 1
    Sx = Sy = 0
    for pasos_dados in range(1, j + 3):
        if x % 2:
            Sx += 1
        if y % 2:
            Sy += 1
        x, y = paso(x), paso(y)
        if pasos_dados == j + 1:
            if x == y:
                raise SystemExit("FALLO familia: j=%d ya juntos en j+1" % j)
            impar = x if x % 2 else y
            if impar != (3 ** (j - 1) - 1) // 2:
                raise SystemExit("FALLO familia: j=%d vortice %d != repunit"
                                 % (j, impar))
    if not (x == y and Sx == Sy):
        raise SystemExit("FALLO familia: j=%d no se funden en j+2 (S %d/%d)"
                         % (j, Sx, Sy))
print()
print("COMPROBACION 5 OK: la familia (2^j-2, 2^j-1) se funde en el paso j+2")
print("con vortice en el repunit (3^(j-1)-1)/2, para j = 4, 6, ..., 60.")
print("Demostrado en el comentario; b(j+2) >= 1 para todo j par.")

# ---------------------------------------------------------------------------
# COMPROBACION 7: LA UNICIDAD DE |M| = 2 - EL TEOREMA DE YEGUAS (03-08-2026).
#
#   TEOREMA: en cada nivel k+1 >= 4 hay EXACTAMENTE UNA clase nueva con
#   |M| = 2, y es  r = 2^(k-1) - 2  si k es impar,  r = 3*2^(k-1) - 2  si
#   k es par. La primera fila del triangulo de estratos es 1, 1, 1, ...
#
#   DEMOSTRACION, en cuatro piezas:
#
#   (1) |M| = 2 fuerza r PAR. Si r es impar, tras el paso 0 la diferencia
#       es d1 = (r+1)/2 - (3r+1)/2 = -r, impar; y paso mixto <=> d impar
#       (paridades opuestas <=> diferencia impar), asi que el paso 1 ya
#       seria mixto y |M| >= 4.
#
#   (2) SOLO DOS CANDIDATOS POR NIVEL. Con r par, d1 = r + 2, y en cada
#       paso compartido d pierde EXACTAMENTE un factor 2 (ambos pares:
#       d' = d/2; ambos impares: d' = 3d/2 -- v2 baja 1 en los dos casos).
#       El segundo mixto llega exactamente cuando d se hace impar, o sea
#       tras v2(r+2) pasos compartidos. Fusion en el paso k+1 con |M| = 2
#       exige que ese mixto sea el paso k: v2(r+2) = k - 1. En el rango
#       r < 2^(k+1) - 1 eso deja r + 2 = 2^(k-1) o 3*2^(k-1): candidatos
#       A = 2^(k-1) - 2  y  B = 3*2^(k-1) - 2. (5*2^(k-1) ya se sale.)
#
#   (3) EL GANADOR CUMPLE, alternando. Con q = k - 1 y la identidad
#       T(c*2^m - 1) = 3c*2^(m-1) - 1:
#       . A, k impar: es la familia de la COMPROBACION 5 con j = k-1 par.
#       . B, k par (q impar): el lado impar 3*2^q - 1 hace q impares hasta
#         3^(q+1) - 1; como q+1 es par, 3^(q+1) = 1 (mod 8) y siguen DOS
#         pares: (3^(q+1)-1)/2, (3^(q+1)-1)/4. El lado par gasta un par,
#         hace q-1 impares hasta 3^q - 1, y como q es impar 3^q = 3
#         (mod 4): sale b = (3^q - 1)/2 IMPAR, y (3b+1)/2 = (3^(q+1)-1)/4.
#         Encuentro exacto en el paso q+2 = k+1, con S = q en los dos.
#
#   (4) EL PERDEDOR FALLA SIEMPRE. Las mismas cuentas con la paridad de q
#       invertida dejan en el paso k los valores (3^q - 1)/2 y
#       (3^(q+1) - 1)/2 con las paridades cambiadas, y el encuentro pediria
#       3^q - 1 = 3^(q+2) - 1, que es falso. Su segundo mixto no es
#       vortice, luego necesita un tercero: |M| >= 4.
#
#   Junto con la COMPROBACION 6 (que ya verifica dist[2] == 1 por fuerza
#   bruta en k <= 15), esto cierra la primera fila del triangulo para TODO
#   nivel. Aqui se comprueban las piezas (3) y (4) hasta k = 60.
# ---------------------------------------------------------------------------

for k in range(3, 61):
    ganador = 2 ** (k - 1) - 2 if k % 2 == 1 else 3 * 2 ** (k - 1) - 2
    perdedor = 3 * 2 ** (k - 1) - 2 if k % 2 == 1 else 2 ** (k - 1) - 2
    if (ganador + 2) % 2 ** (k - 1) != 0 or (ganador + 2) % 2 ** k == 0:
        raise SystemExit("FALLO v2: k=%d" % k)
    # el ganador: se funde en k+1, S igual, distinto en k, |M| = 2
    x, y = ganador, ganador + 1
    Sx = Sy = mixtos = 0
    for paso_i in range(k + 1):
        if (x % 2) != (y % 2):
            mixtos += 1
        if x % 2:
            Sx += 1
        if y % 2:
            Sy += 1
        if paso_i == k and x == y:
            raise SystemExit("FALLO unicidad: k=%d ganador junto en k" % k)
        x, y = paso(x), paso(y)
    if not (x == y and Sx == Sy and mixtos == 2):
        raise SystemExit("FALLO unicidad: k=%d ganador no cumple "
                         "(M=%d, S %d/%d)" % (k, mixtos, Sx, Sy))
    # el perdedor: NO se funde en el paso k+1
    x, y = perdedor, perdedor + 1
    for _ in range(k + 1):
        x, y = paso(x), paso(y)
    if x == y:
        raise SystemExit("FALLO unicidad: k=%d el perdedor SI se fundio" % k)

print()
print("COMPROBACION 7 OK: la unicidad de |M| = 2 esta demostrada (comentario)")
print("y comprobada hasta k = 60: gana 2^(k-1)-2 con k impar, 3*2^(k-1)-2")
print("con k par, y el perdedor nunca se funde en el paso k+1.")
print("La primera fila del triangulo de estratos es 1, 1, 1, ... para siempre.")

# ---------------------------------------------------------------------------
# COMPROBACION 8: EL LEMA GENERAL Y LA FAMILIA |M| = 4 (03-08-2026).
#
#   LEMA (generaliza la COMPROBACION 5 a prefijo impar arbitrario): para
#   todo C impar y q >= 2 con  C = 3^q (mod 4),  el par
#
#       ( C*2^q - 2 ,  C*2^q - 1 )
#
#   se funde EXACTAMENTE en el paso q+2, con S = q en los dos lados y
#   vortice en b = (3^(q-1)*C - 1)/2. Demostracion, igual que la del
#   repunit: el lado impar hace q impares hasta 3^q*C - 1 (identidad
#   T(c*2^m - 1) = 3c*2^(m-1) - 1); el lado par gasta un par y hace q-1
#   impares hasta 3^(q-1)*C - 1. La condicion C = 3^q (mod 4) hace impar
#   a b = (3^(q-1)*C - 1)/2 y par a (3^q*C - 1)/2 (esto ultimo es
#   automatico: 3^q*C = 9*3^(q-1)*C = 1 (mod 4)), y el encuentro cuadra:
#   3b + 1 = (3^q*C - 1)/2. Los casos C = 1 y C = 3 son EXACTAMENTE la
#   alternancia del teorema de |M| = 2.
#
#   Y LA FAMILIA |M| = 4, demostrada con el lema: la clase
#
#       r = 2^(k-1) - 3   (k par)      r = 3*2^(k-1) - 3   (k impar)
#
#   -- el vecino izquierdo del PERDEDOR de |M| = 2, con r IMPAR -- tiene
#   mixtos en [0, 1, 2, k] y se funde en k+1. Los dos primeros pasos se
#   calculan a mano: con w = c*2^(k-1) (c = 1 o 3), el par (w-3, w-2) va a
#   (3c*2^(k-2) - 4, c*2^(k-2) - 1) y de ahi a (3c*2^(k-3) - 2,
#   3c*2^(k-3) - 1): EL PAR VUELVE A SER CONSECUTIVO (d2 = 1), y es el
#   del lema con C = 3c, q = k-3 -- la condicion C = 3^q (mod 4) cuadra
#   en las dos ramas. Fusion en 2 + (q+2) = k+1. LOS ESTRATOS SE REDUCEN
#   UNOS A OTROS: |M| = 4 es un preludio de dos mixtos + un |M| = 2
#   desplazado. Esa reduccion es la forma de la recursion del triangulo.
#
#   La UNICIDAD de |M| = 4 sigue MEDIDA (comprobacion 6, k <= 15), no
#   demostrada: faltaria descartar los otros patrones de posiciones.
# ---------------------------------------------------------------------------

for q in range(2, 41):
    for C in range(1, 202, 2):
        if C % 4 != 3 ** q % 4:
            continue
        x, y = C * 2 ** q - 2, C * 2 ** q - 1
        Sx = Sy = 0
        for i in range(q + 2):
            if i == q + 1:
                if x == y:
                    raise SystemExit("FALLO lema: C=%d q=%d juntos antes"
                                     % (C, q))
                impar = x if x % 2 else y
                if impar != (3 ** (q - 1) * C - 1) // 2:
                    raise SystemExit("FALLO lema: C=%d q=%d vortice %d"
                                     % (C, q, impar))
            if x % 2:
                Sx += 1
            if y % 2:
                Sy += 1
            x, y = paso(x), paso(y)
        if not (x == y and Sx == Sy):
            raise SystemExit("FALLO lema: C=%d q=%d no funden (S %d/%d)"
                             % (C, q, Sx, Sy))

for k in range(4, 61):
    r = 2 ** (k - 1) - 3 if k % 2 == 0 else 3 * 2 ** (k - 1) - 3
    x, y = r, r + 1
    Sx = Sy = 0
    pos = []
    for i in range(k + 1):
        if (x % 2) != (y % 2):
            pos.append(i)
        if x % 2:
            Sx += 1
        if y % 2:
            Sy += 1
        if i == k and x == y:
            raise SystemExit("FALLO familia M4: k=%d juntos antes" % k)
        x, y = paso(x), paso(y)
    if not (x == y and Sx == Sy and pos == [0, 1, 2, k]):
        raise SystemExit("FALLO familia M4: k=%d (mixtos %s, S %d/%d)"
                         % (k, pos, Sx, Sy))

print()
print("COMPROBACION 8 OK: el lema general (C impar, C = 3^q mod 4) en todos")
print("los pares C <= 201, q <= 40; y la familia |M| = 4 (el vecino del")
print("perdedor, r impar) fusiona en k+1 con mixtos [0,1,2,k], k = 4..60.")
print("Los estratos se reducen unos a otros: dos mixtos de preludio + un")
print("|M| = 2 desplazado. La recursion del triangulo tiene esa forma.")

# ---------------------------------------------------------------------------
# COMPROBACION 9: LA RUTA IMPAR DE |M| = 4, DEMOSTRADA (03-08-2026).
#
#   Tres piezas, con las cuentas del gap g (la diferencia con signo):
#
#   (i) r IMPAR implica pasos 0, 1 y 2 MIXTOS, o sea |M| >= 4 siempre.
#       Paso 0: consecutivos, mixto. Con r impar el paso da gap -r, impar:
#       paso 1 mixto. En el paso 1, si r = 1 (mod 4) el lado menor es
#       impar y el gap pasa a -1; si r = 3 (mod 4) el menor es par y el
#       gap pasa a 2r + 1. Impar en los dos casos: paso 2 mixto. (Es el
#       reverso del teorema de |M| = 2, que forzaba r par.)
#
#   (ii) LA CONTRACCION EXACTA: si r = 1 (mod 4), los valores en el paso
#        2 son CONSECUTIVOS otra vez: { (3r+1)/4, (3r+1)/4 + 1 }.
#
#   (iii) UNICIDAD DENTRO DE LA RUTA r = 1 (mod 4): una clase nueva con
#        |M| = 4 y r = 1 (mod 4) queda, tras la contraccion, en el par
#        consecutivo de menor s2 = (3r+1)/4, al que se aplica ENTERO el
#        argumento de |M| = 2: s2 par (si no, quinto mixto), la v2 baja
#        de a uno en los compartidos => v2(s2 + 2) = k - 3, o sea
#        s2 + 2 = C*2^(k-3) con C impar; el rango r < 2^(k+1) da C <= 11;
#        la necesidad del lema general (la pieza 4: el vortice con la
#        paridad cambiada pediria 3^(q-1)*C - 1 = 3^(q+1)*C - 1) da
#        C = 3^(k-3) (mod 4); y para que r = (4*s2 - 1)/3 sea ENTERO hace
#        falta s2 = 1 (mod 3), o sea 3 | C. Quedan C = 3 y C = 9, y el
#        mod 4 elige EXACTAMENTE UNO: r = 2^(k-1) - 3 o 3*2^(k-1) - 3.
#
#   Lo que queda para la unicidad TOTAL de |M| = 4 (y sigue medido, no
#   demostrado): descartar la ruta r = 3 (mod 4) (su paso 2 deja gap
#   2r + 1, no contrae) y las rutas con r par (mixtos [0, i, j, k] con
#   i >= 2). La fuerza bruta de la comprobacion 6 las descarta en k <= 15.
# ---------------------------------------------------------------------------

for r in range(1, 2 ** 14, 2):
    x, y = r, r + 1
    for i in range(3):
        if (x % 2) == (y % 2):
            raise SystemExit("FALLO (i): r=%d paso %d no mixto" % (r, i))
        if i == 2 and r % 4 == 1:
            # la contraccion es el ESTADO TRAS DOS PASOS (aqui, antes de
            # dar el tercero): el primer chequeo seguia un paso de mas
            lo, hi = min(x, y), max(x, y)
            if not (lo == (3 * r + 1) // 4 and hi == lo + 1):
                raise SystemExit("FALLO (ii): r=%d tras2=(%d,%d)" % (r, x, y))
        x, y = paso(x), paso(y)

for k in range(5, 61):
    finales = []
    for C in (1, 3, 5, 7, 9, 11):
        s2 = C * 2 ** (k - 3) - 2
        if s2 % 3 == 1 and C % 4 == 3 ** (k - 3) % 4:
            finales.append((4 * s2 - 1) // 3)
    esperado = 2 ** (k - 1) - 3 if k % 2 == 0 else 3 * 2 ** (k - 1) - 3
    if finales != [esperado]:
        raise SystemExit("FALLO (iii): k=%d candidatos %s, esperado %d"
                         % (k, finales, esperado))

print()
print("COMPROBACION 9 OK: r impar fuerza |M| >= 4 (exhaustivo r < 2^14);")
print("la contraccion (3r+1)/4 es exacta en r = 1 (mod 4); y la unicidad")
print("DENTRO de esa ruta esta demostrada: C en {3, 9} y el mod 4 elige")
print("uno solo, k = 5..60. Para la unicidad total faltan las rutas")
print("r = 3 (mod 4) y r par (descartadas por fuerza bruta en k <= 15).")

# ---------------------------------------------------------------------------
# COMPROBACION 10: LA COORDENADA D (COMADREJAS), Y r = 3 (mod 4) EXCLUIDA
# (03-08-2026). Con esto la unicidad de |M| = 4 queda DEMOSTRADA para todo
# r impar; solo falta la ruta r par.
#
#   LA COORDENADA. Para el par {s, s+g} (s el menor, g el gap) se define
#
#       D = g - 2s - 1
#
#   (a) EL VORTICE ES D = 0 CON s IMPAR: la fusion en un paso mixto exige
#       (3s+1)/2 = (s+g)/2, o sea g = 2s+1; y con s par el mixto es beta,
#       que agranda el gap y no fusiona nunca.
#   (b) EN PASOS COMPARTIDOS, D ES IMPAR Y EVOLUCIONA AFIN:
#       ambos pares: D -> (D-1)/2; ambos impares: D -> (3D-1)/2.
#       (g par, 2s par => D impar. Y g = D + 2s + 1: g impar <=> D par,
#       o sea el tramo compartido TERMINA exactamente cuando D se hace
#       par, y el mixto que sigue es vortice si y solo si ese D es 0.)
#   (c) D NEGATIVO ES INVARIANTE: si D < 0, (D-1)/2 < 0 y (3D-1)/2 < 0.
#       Un par que entra en D < 0 no puede terminar su tramo compartido
#       en D = 0: SU SIGUIENTE MIXTO NUNCA ES VORTICE.
#
#   LA EXCLUSION DE r = 3 (mod 4), con las cuentas de la comprobacion 9:
#   tras los mixtos 0 y 1 el par es { (r+1)/4, (r+1)/4 + 2r+1 }.
#
#   . r = 3 (mod 8): (r+1)/4 impar, el mixto 2 es alfa y deja
#     s3 = (3r+7)/8, g3 = (3r-1)/4, o sea D3 = -3 < 0. Por (c), el cuarto
#     mixto no es vortice: |M| >= 6. NINGUNA nueva de |M| = 4 aqui.
#   . r = 7 (mod 8): (r+1)/4 par, el mixto 2 es beta y g3 = 2r+1 dejado
#     en impar por la regla de paridad de beta (g = 3 mod 4): el paso 3
#     TAMBIEN es mixto. Para k > 3 eso ya son 4 mixtos antes del vortice:
#     |M| >= 5, y como |M| es par, |M| >= 6. (El borde k = 3 es el nivel
#     4, cubierto exhaustivamente por la comprobacion 6: solo hay |M|=2.)
#
#   Con la comprobacion 9 (unicidad en r = 1 mod 4) queda: entre los r
#   IMPARES hay exactamente UNA clase |M| = 4 por nivel. La ruta r PAR
#   sigue descartada solo por fuerza bruta (k <= 15) - el mapa de
#   dependencias mantiene unicidad_M4 en medido por eso.
# ---------------------------------------------------------------------------

for r in range(3, 2 ** 15, 8):
    # r = 3 (mod 8): estado tras 3 pasos, la D, y que el siguiente mixto
    # llega con D < 0 y no fusiona
    x, y = r, r + 1
    for _ in range(3):
        x, y = paso(x), paso(y)
    s, g = min(x, y), abs(x - y)
    if not (s == (3 * r + 7) // 8 and g == (3 * r - 1) // 4):
        raise SystemExit("FALLO estado X1: r=%d (%d,%d)" % (r, x, y))
    D = g - 2 * s - 1
    if D != -3:
        raise SystemExit("FALLO D3: r=%d D=%d" % (r, D))
    while (x % 2) == (y % 2):            # el tramo compartido hasta el mixto
        x, y = paso(x), paso(y)
        s, g = min(x, y), abs(x - y)
        D = g - 2 * s - 1
        if D >= 0:
            raise SystemExit("FALLO invariante: r=%d D=%d >= 0" % (r, D))
    if paso(x) == paso(y):
        raise SystemExit("FALLO exclusion X1: r=%d fusiona en el 4o mixto" % r)

for r in range(7, 2 ** 15, 8):
    # r = 7 (mod 8): el paso 3 tambien es mixto
    x, y = r, r + 1
    for _ in range(3):
        x, y = paso(x), paso(y)
    if (x % 2) == (y % 2):
        raise SystemExit("FALLO X2: r=%d paso 3 compartido" % r)

print()
print("COMPROBACION 10 OK: la coordenada D = g - 2s - 1 (vortice <=> D = 0")
print("con s impar; D < 0 invariante en compartidos). La ruta r = 3 (mod 8)")
print("cae en D = -3 y su cuarto mixto nunca es vortice; la r = 7 (mod 8)")
print("encadena cuatro mixtos seguidos. EXCLUIDAS de |M| = 4, r < 2^15.")
print("La unicidad de |M| = 4 queda demostrada para TODO r impar.")

# ---------------------------------------------------------------------------
# COMPROBACION 11: LA COORDENADA E (COMADREJAS) ES AUTONOMA, y r par acorralada
# (03-08-2026).
#
#   TEOREMA (la herramienta): dentro de un tramo compartido, la cantidad
#
#       E = D - 3s      (D la de la comprobacion 10, s el menor del par)
#
#   evoluciona SOLA, sin mirar los valores. Porque D es impar durante el
#   tramo, la paridad de E determina la del menor (E impar <=> s par), o
#   sea que la propia E elige su mapa:
#
#       E impar -> paso compartido-par   -> E' = (E - 1)/2
#       E par   -> paso compartido-impar -> E' = (3E - 4)/2
#
#   COROLARIO (la orbita del rebote): un par con r PAR arranca en D = 1
#   (D1 = r+2 - r - 1), su primer mixto llega exactamente en D = 0, y si
#   ahi s es par REBOTA a (s', D') = (s/2, 3(s/2)+1), o sea E = 1. Desde
#   E = 1 la orbita es FORZADA: 1, 0, -2, -5, -3, y despues el ciclo
#   (-2, -5, -3) para siempre.
#
#   COROLARIO 2 (el vortice del rebote es imposible): el tramo rebotado
#   solo puede terminar en vortice con E = -3s, y en la orbita eso exige
#   (E, s) = (-3, 1): el par {1, 4}. Pero la cadena hacia atras esta
#   FORZADA por las paridades de la orbita (E impar: s = 2s'; E par:
#   s = (2s' - 1)/3), y desde s = 1 da 1, 2, 1, 2, 4 y pide (2*4 - 1)/3 =
#   7/3 (o 1/3 en el arranque corto): NO ES ENTERO. Ningun tramo rebotado
#   termina en vortice. (Consistente con |M| par: [0, rebote, vortice]
#   serian 3 mixtos; la E lo re-demuestra por via independiente.)
#
#   LO QUE QUEDA PARA r PAR EN |M| = 4: el patron [0, rebote, m3,
#   vortice], donde el tramo rebotado termina en un mixto NO vortice y un
#   cuarto tramo debe clavar el 0. La E tras ese tercer mixto depende del
#   valor (E'' = (E - 12s - 7)/2 en alfa sin vuelco, etc.) y el descarte
#   general queda ABIERTO. Aqui se acorrala con un barrido dirigido que
#   no construye buenas(k): pares (r, r+1) sueltos con r par, siguiendo
#   cada uno hasta su primera fusion. NINGUNO funde con |M| = 4 y S
#   igualada. (El barrido cubre niveles k+1 <= TOPE_PASOS, muy por encima
#   del k = 15 de la fuerza bruta por niveles.)
# ---------------------------------------------------------------------------

# la orbita de E, verificada como teorema de mapa: 20 pasos desde E = 1
orb = [1]
for _ in range(20):
    E = orb[-1]
    orb.append((E - 1) // 2 if E % 2 else (3 * E - 4) // 2)
if orb[:5] != [1, 0, -2, -5, -3] or orb[4:10] != [-3, -2, -5, -3, -2, -5]:
    raise SystemExit("FALLO orbita E: %s" % orb[:10])

TOPE_PASOS = 400
peor_M = {}
for r in range(2, 2 ** 20, 2):
    x, y = r, r + 1
    dS = 0
    mixtos = 0
    for _ in range(TOPE_PASOS):
        px, py = x % 2, y % 2
        if px != py:
            mixtos += 1
            dS += py - px
        x, y = paso(x), paso(y)
        if x == y:
            if dS == 0 and mixtos == 4:
                raise SystemExit("CONTRAEJEMPLO r par |M|=4: r = %d" % r)
            if dS == 0:
                peor_M[mixtos] = peor_M.get(mixtos, 0) + 1
            break

print()
print("COMPROBACION 11 OK: E = D - 3s es autonoma (E impar -> (E-1)/2,")
print("E par -> (3E-4)/2). [CORRECCION 03-08 noche: el corolario de 'la")
print("orbita del rebote es 1,0,-2,-5,-3' que estaba aqui era de la")
print("FAMILIA FANTASMA (w,6w+2); el rebote real es (w,9w+2) con")
print("E = 3w+1, dependiente de w -- ver comprobacion 12.] El barrido")
print("dirigido r par < 2^20 SI vale: NINGUNA fusion con |M| = 4 y S")
print("igualada. Estratos pares vistos: %s"
      % dict(sorted(peor_M.items())))

# ---------------------------------------------------------------------------
# COMPROBACION 12: EL TERCER MIXTO DE r PAR, CLASIFICADO (03-08-2026).
#
#   El estado tras el rebote es (w, 6w+2) con D = 3w+1, E = 1. Dentro de
#   un tramo el par (D, E) es DETERMINISTA (los dos autonomos, y
#   s = (D-E)/3 se recupera), asi que el tercer mixto se clasifica
#   entero. Para |M| = 4 ese tercer mixto no puede ser vortice (D > 0)
#   y el CUARTO tiene que serlo. Tres casos:
#
#   CASO A (w impar): el estado del rebote ya es mixto (g = 5w+2 impar).
#     Es alfa sin vuelco (s = w impar, D > 0) y deja D' = -(3w+1)/2 - 1,
#     NEGATIVO: el semieje absorbente impide el vortice. |M| >= 6.
#     DEMOSTRADO.
#
#   CASO B-alfa (w par, el tramo rebotado termina en E de {1, -5, -3},
#     o sea s impar): el mixto es alfa sin vuelco con D = E + 3s <= 3s+1,
#     y D' = D/2 - 3s - 2 <= (3s+1)/2 - 3s - 2 < 0: NEGATIVO otra vez.
#     |M| >= 6. DEMOSTRADO.
#
#   CASO B-beta (w par, el tramo termina en E de {0, -2}, s par): el
#     mixto es beta y D' = 3D/2 + 3s + 1 > 0. El cuarto tramo arranca en
#     (D, E) = (15u+1, 12u+1) o (15u-2, 12u-2) con u = s/2, y las
#     paridades fuerzan cadenas (u par, v impar, t impar, ...) donde cada
#     rama que se corta lo hace en un mixto con D grande y != 0 -- pero
#     el arbol 2-adico completo QUEDA ABIERTO. Es la unica puerta que le
#     queda a un |M| = 4 con r par, y aqui se acorrala: ningun estado
#     post-rebote (w, 6w+2) con w < 2^16 funde en su segundo mixto.
#     (Superconjunto: cubre todos los rebotes reales de cualquier r.)
# ---------------------------------------------------------------------------

# >>> CORRECCION (03-08-2026, noche): TODO EL ANALISIS ANTERIOR DE ESTA
# >>> COMPROBACION ERA SOBRE UNA FAMILIA FANTASMA. El estado con D = 0 es
# >>> el par {s, 3s+1} (gap 2s+1), y su rebote beta da (s/2, (9s+4)/2) =
# >>> (w, 9w+2) -- NO (w, 6w+2) como decia aqui. La delato LA ECUACION DE
# >>> RENOVACION, que no cerraba (0,4039 contra 0,4453) hasta poner la
# >>> familia buena (0,4504). Los casos A y B-alfa "excluidos" eran del
# >>> fantasma y QUEDAN RETIRADOS. Lo que si vale del bloque original:
# >>> el teorema de |M| par y el barrido real de la comprobacion 11.
#
# LO QUE SE COMPRUEBA AHORA, con la familia REAL:
#   (a) el rebote de los pares de verdad cae SIEMPRE en (w, 9w+2) --
#       derivacion de dos lineas: en D = 0 el par es {s, 3s+1}; beta con
#       s = 2w par da (w, (9*2w+4)/2) = (w, 9w+2);
#   (b) TEOREMA DE PARIDAD DEL REBOTE: el tramo post-rebote NUNCA puede
#       terminar en una fusion DE CLASE: seria |M| = 3 (mixtos 0, rebote,
#       vortice), impar, y Delta_S = +2 +- 1 != 0. Toda fusion de clase
#       con r par y rebote necesita |M| >= 4. (Puro conteo, sin familias.)

vistos_rebote = 0
for r in range(2, 2 ** 15, 2):
    x, y = paso(r), paso(r + 1)
    for _ in range(300):
        s, g = min(x, y), abs(x - y)
        if g % 2:
            if g == 2 * s + 1 and s % 2 == 0:      # rebote real
                nx, ny = paso(x), paso(y)
                w0 = s // 2
                if {nx, ny} != {w0, 9 * w0 + 2}:
                    raise SystemExit("FALLO familia real: r=%d -> (%d,%d)"
                                     % (r, nx, ny))
                vistos_rebote += 1
            break
        x, y = paso(x), paso(y)

print()
print("COMPROBACION 12 (corregida) OK: %d rebotes de pares reales, TODOS"
      % vistos_rebote)
print("en la familia (w, 9w+2); la familia (w, 6w+2) del analisis anterior")
print("era un FANTASMA (la cazo la ecuacion de renovacion al no cerrar).")
print("Y el teorema de paridad: el tramo post-rebote nunca da fusion de")
print("clase (|M| = 3 impar, Delta_S = +2 +- 1): r par exige |M| >= 4.")

# ---------------------------------------------------------------------------
# COMPROBACION 13: EL CENSO DE FAMILIAS DEL MAPA DE E (03-08-2026, idea
# del usuario: "toda orbita relevante de E pertenece a una de N familias").
#
#   El mapa de E, mirado como sistema dinamico propio sobre Z:
#
#       E impar -> (E - 1)/2        E par -> (3E - 4)/2
#
#   es un mapa DE TIPO COLLATZ (mitad contrae, mitad expande; la deriva
#   media es contractiva: -log 2 + log(3/2) < 0). Censo exhaustivo en
#   [-10^5, 10^5]: TODA orbita cae en uno de DIEZ ciclos -- ninguna
#   escapa ni tarda mas de 5.000 pasos. Las diez familias (minimo, largo):
#
#       (-1, 1)  (4, 1)  (-11, 2)  (-5, 3)  (24, 3)
#       (-59, 5)  (-77, 5)  (84, 11)  (-4163, 27)  (-5099, 27)
#
#   El del rebote es (-5, 3) = {-2, -5, -3}, y atrae al 47% de todo el
#   rango. AVISO de alcance: censo medido en un rango, no teorema -- la
#   completitud de la lista para todo Z es exactamente el tipo de
#   pregunta que en Collatz lleva 90 anos abierta. Lo que cambia el
#   programa: las rutas de los estratos dejan de analizarse una a una y
#   pasan a clasificarse por la familia de E en que viven y por donde el
#   vortice (D = 0) interrumpe la orbita antes del ciclo.
# ---------------------------------------------------------------------------

def mapaE(E):
    return (E - 1) // 2 if E % 2 else (3 * E - 4) // 2

CENSO_N = 100000
FAMILIAS_ESPERADAS = {(-1, 1), (4, 1), (-11, 2), (-5, 3), (24, 3),
                      (-59, 5), (-77, 5), (84, 11), (-4163, 27), (-5099, 27)}
familias = {}
for e0 in range(-CENSO_N, CENSO_N + 1):
    E = e0
    vistos = set()
    while E not in vistos:
        if len(vistos) > 5000 or abs(E) > 10 ** 12:
            raise SystemExit("FALLO censo: E0=%d no cierra" % e0)
        vistos.add(E)
        E = mapaE(E)
    ciclo = [E]
    x = mapaE(E)
    while x != E:
        ciclo.append(x)
        x = mapaE(x)
    familias[(min(ciclo), len(ciclo))] = familias.get(
        (min(ciclo), len(ciclo)), 0) + 1
if set(familias) != FAMILIAS_ESPERADAS:
    raise SystemExit("FALLO censo: familias %s" % sorted(familias))

print()
print("COMPROBACION 13 OK: censo de E en [-10^5, 10^5]: DIEZ familias,")
print("ninguna orbita escapa. Cuencas:")
for (rep, largo), cnt in sorted(familias.items()):
    print("  ciclo min %6d largo %2d: %6d orbitas" % (rep, largo, cnt))

# ---------------------------------------------------------------------------
# COMPROBACION 14: LA RAMA B-BETA EN EL MAPA (D, E), A 10^7 (03-08-2026).
#
#   El cuarto tramo de un |M| = 4 con r par es DETERMINISTA en (D, E):
#   no hay que simular pares de numeros, solo iterar
#
#       E impar: (D, E) -> ((D-1)/2, (E-1)/2)
#       E par  : (D, E) -> ((3D-1)/2, (3E-4)/2)
#
#   desde los dos arranques que dejo la comprobacion 12 (u = s/2 del
#   estado en que termino el tramo rebotado):
#
#       E_n =  0:  (15u+1, 12u+1)     E_n = -2:  (15u-2, 12u-2)
#
#   El tramo termina en el primer D par, y |M| = 4 exigiria terminar en
#   D = 0 EXACTO. Dos hechos demostrados en papel que lo estrechan:
#   E < 0 tambien es absorbente (mismos mapas que D), y el vortice
#   exigiria pasar por (D, E) = (1, 1 - 3s) con s par -- el pre-vortice
#   tiene forma fija. Lo que sigue abierto es el arbol 2-adico de
#   paridades que decide si algun u lo alcanza. Aqui: NINGUN u <= 10^7
#   en ninguna de las dos familias termina en D = 0. (Antes el
#   acorralado era w < 2^16; esto lo multiplica por ~300 sin tocar un
#   par de numeros de verdad.)
# ---------------------------------------------------------------------------

# >>> CORRECCION (03-08-2026, noche): los arranques (15u+1, 12u+1) y
# >>> (15u-2, 12u-2) salian de la familia fantasma y ESTE BLOQUE QUEDA
# >>> REESCRITO. El arranque real del tramo post-rebote es
# >>> (D, E) = (6w+1, 3w+1) -- del par (w, 9w+2): D = 8w+2-2w-1, E = D-3w.
# >>> Se itera el mapa (D, E) puro desde ahi: si algun tramo terminara en
# >>> D = 0 seria un encuentro de VALOR con |M| = 3, que el teorema de
# >>> paridad de arriba ya excluye como fusion de CLASE; aqui se mide
# >>> ademas que ni siquiera eso ocurre para w <= 10^6.

for w in range(1, 10 ** 6 + 1):
    D, E = 6 * w + 1, 3 * w + 1
    while D % 2:
        if E % 2:
            D, E = (D - 1) // 2, (E - 1) // 2
        else:
            D, E = (3 * D - 1) // 2, (3 * E - 4) // 2
    if D == 0:
        raise SystemExit("ENCUENTRO DE VALOR en el tramo post-rebote: w=%d"
                         % w)

print()
print("COMPROBACION 14 (corregida) OK: el tramo post-rebote REAL, iterado")
print("en el mapa (D, E) puro desde (6w+1, 3w+1) para w <= 10^6: ninguno")
print("termina en D = 0 -- ni siquiera hay encuentro de valor, ademas de")
print("que el teorema de paridad ya prohibe la fusion de clase ahi.")

# ---------------------------------------------------------------------------
# COMPROBACION 15: LA MITAD EXACTA DEL ESTRATO 2, DEMOSTRADA (03-08-2026).
# La perla de la comprobacion 11 ("exactamente 2^18, huele a biyeccion de
# Terras") deja de ser perla: es un teorema, y este es su enunciado.
#
#   TEOREMA. Para r PAR, el par (r, r+1) se funde con |M| = 2 si y solo
#   si en el vector de paridad de s1 = r/2 EL PRIMER 0 VA SEGUIDO DE UN 1.
#   Y el conteo es exacto: entre los r pares con s1 en [1, 2^m), fusionan
#   EXACTAMENTE 2^(m-1), para todo m >= 2.
#
#   DEMOSTRACION.
#   (a) El mixto 0 deja (s1, D = 1) con el lado de r como menor (beta no
#       voltea el orden, y los compartidos tampoco). Con D = 1 los
#       compartidos-impar mantienen D = 1, y el PRIMER valor PAR de la
#       trayectoria de s1 (posicion j, con j = impares iniciales) da el
#       compartido-par que baja D a 0.
#   (b) El mixto con D = 0 es vortice si y solo si su menor es impar, y
#       ese menor es T^(j+1)(s1): el bit j+1 del vector. Fusion en el
#       paso j + 3 (j = 0 es Garner: (8k+4, 8k+5) en 3 pasos).
#   (c) Delta_S = 0 automatico: el paso 0 suma al lado r+1 (impar) y el
#       vortice suma al lado r (el menor). Uno y uno.
#   (d) El conteo, por la biyeccion de Terras (residuo <-> vector):
#       los patrones 1^j 0 1 * con j <= m-2 suman 2^(m-1) - 1 residuos;
#       el complemento 1^j 0 0 * otros tantos; y quedan DOS residuos
#       frontera: 2^(m-1) - 1 (vector 1^(m-1) 0) y 2^m - 1 (vector 1^m).
#       El primero funde <=> (3^(m-1) - 1)/2 impar <=> m PAR; el segundo
#       <=> (3^m - 1)/2 impar <=> m IMPAR. Exactamente uno por cada m:
#       total 2^(m-1) - 1 + 1 = 2^(m-1), sin casos.
#
#   Es la primera MEDIDA exacta de una fila del triangulo: el estrato 2
#   pesa exactamente 1/2 entre los r pares. Y conecta la primera fila
#   con Terras 1.4 (la moneda): "primer 0 seguido de 1" es un suceso de
#   probabilidad 1/2 sobre bits equidistribuidos.
# ---------------------------------------------------------------------------

M_TOPE = 16
fundidos_por_m = {}
for s1 in range(1, 2 ** M_TOPE):
    # el bit condicion: primer 0 del vector de s1, seguido de 1?
    x = s1
    while x % 2:
        x = paso(x)
    condicion = (paso(x) % 2 == 1)      # T^(j+1)(s1) impar
    # la fusion real del par (2*s1, 2*s1 + 1), por simulacion cruda
    a, b = 2 * s1, 2 * s1 + 1
    mixtos = 0
    fundio = False
    for _ in range(200):
        if (a % 2) != (b % 2):
            mixtos += 1
        a, b = paso(a), paso(b)
        if a == b:
            fundio = (mixtos == 2)
            break
    if fundio != condicion:
        raise SystemExit("FALLO teorema mitad: s1=%d cond=%r fundio=%r"
                         % (s1, condicion, fundio))
    for m in range(2, M_TOPE + 1):
        if s1 < 2 ** m and fundio:
            fundidos_por_m[m] = fundidos_por_m.get(m, 0) + 1
for m in range(2, M_TOPE + 1):
    if fundidos_por_m.get(m, 0) != 2 ** (m - 1):
        raise SystemExit("FALLO conteo mitad: m=%d da %d, no 2^(m-1)"
                         % (m, fundidos_por_m.get(m, 0)))

print()
print("COMPROBACION 15 OK: TEOREMA DE LA MITAD EXACTA. r par funde con")
print("|M| = 2 <=> el primer 0 del vector de r/2 va seguido de 1; y entre")
print("s1 < 2^m fusionan EXACTAMENTE 2^(m-1), comprobado m = 2..%d con la"
      % M_TOPE)
print("equivalencia exhaustiva. La primera fila del triangulo tiene MEDIDA")
print("exacta 1/2, y es Terras 1.4 (la moneda) actuando sobre dos bits.")

# ---------------------------------------------------------------------------
# COMPROBACION 16: EL TEOREMA DEL REINICIO UNIFORME, y la ecuacion de
# renovacion exacta (03-08-2026).
#
#   TEOREMA. (a) Si r = 4t + 1 (la rama de contraccion), tras dos pasos
#   el par es EXACTAMENTE (3t + 1, 3t + 2) -- un par consecutivo fresco.
#   Y t -> 3t + 1 es biyeccion de Z/2^m para todo m (3 es impar), asi
#   que si r recorre su clase uniformemente, EL PAR CONTRAIDO ES
#   UNIFORME: la autosimilitud del problema de fusion es exacta, no
#   aproximada. P(fusion | contraccion) = f, la misma incognita.
#
#   (b) En la rama del rebote (r par cuyo primer 0 va seguido de 0), el
#   parametro del estado post-rebote es w = T^(j+2)(s1), y por Terras
#   1.2 (fijado el prefijo de paridad, el iterado recorre las clases
#   biyectivamente) w es EXACTAMENTE uniforme sobre los residuos.
#
#   COROLARIO (la ecuacion de renovacion, con las cuatro ramas exactas
#   de medida 1/4 + 1/4 + 1/4 + 1/4 sobre r):
#
#       f  =  1/4 * 1  +  1/4 * f  +  1/4 * g  +  1/4 * h
#
#   donde f = P(fusion de un par consecutivo uniforme), g = P(fusion
#   del estado post-rebote (w, 6w+2), w uniforme), h = P(fusion tras la
#   ruta r = 3 (mod 4)). Despejando: f = 1/3 + (g + h)/3, y en
#   particular f >= 1/3 DEMOSTRADO (cota estructural; la cota numerica
#   a(32)/2^32 = 0,4357 es mejor, pero esta sale de tres lineas y de
#   ella cuelga el programa: calcular g y h con el mismo metodo de dos
#   bits cierra el sistema y decide f -- y f = 1 seria la conjetura de
#   Wu en densidad, la pregunta mas vieja del laboratorio).
#
#   Demostracion de (a): r = 4t+1 impar -> (3r+1)/2 = 6t+2, (r+1)/2 =
#   2t+1; segundo paso: 6t+2 par -> 3t+1, 2t+1 impar -> 3t+2. QED.
#   La de (b) es Terras 1.2 aplicado al prefijo 1^j 0 0.
# ---------------------------------------------------------------------------

for t in range(0, 2 ** 14):
    r = 4 * t + 1
    x, y = r, r + 1
    for _ in range(2):
        x, y = paso(x), paso(y)
    if {x, y} != {3 * t + 1, 3 * t + 2}:
        raise SystemExit("FALLO contraccion literal: t=%d -> (%d,%d)"
                         % (t, x, y))
for m in range(1, 13):
    if len({(3 * t + 1) % 2 ** m for t in range(2 ** m)}) != 2 ** m:
        raise SystemExit("FALLO biyeccion 3t+1 mod 2^%d" % m)

for j in range(6):
    conteo = {}
    for s1 in range(2 ** (j + 8)):
        x = s1
        ok = True
        for _ in range(j):              # j impares...
            if x % 2 == 0:
                ok = False
                break
            x = paso(x)
        if not ok or x % 2:             # ...luego un par...
            continue
        x = paso(x)
        if x % 2:                       # ...y otro par (la rama rebote)
            continue
        w = paso(x)                     # w = T^(j+2)(s1)
        conteo[w % 64] = conteo.get(w % 64, 0) + 1
    if len(conteo) != 64 or len(set(conteo.values())) != 1:
        raise SystemExit("FALLO uniformidad rebote: j=%d clases=%d"
                         % (j, len(conteo)))

print()
print("COMPROBACION 16 OK: REINICIO UNIFORME. La contraccion es literal")
print("(4t+1 -> par (3t+1, 3t+2)) y 3t+1 es biyeccion mod 2^m; el w del")
print("rebote es uniforme (j = 0..5, 64 clases exactas). La ecuacion de")
print("renovacion f = 1/4 + f/4 + g/4 + h/4 es EXACTA, y f >= 1/3 queda")
print("demostrado en tres lineas. Calcular g y h cierra el sistema.")

# ---------------------------------------------------------------------------
# COMPROBACION 17: EL LEMA DEL BALANCE FORZADO (03-08-2026, noche).
#
#   LEMA. Toda fusion DE CLASE ENTERA esta S-balanceada: si
#   T^t(r) = T^t(r+1) para TODOS los r de una clase residual mod 2^p
#   (con t <= p), entonces S_t(r) = S_t(r+1) en esa clase.
#
#   DEMOSTRACION (tres lineas, desde Terras 1.2). Sobre la clase, ambos
#   lados son afines: 2^t T^t(r) = 3^(Sx) r + Cx y 2^t T^t(r+1) =
#   3^(Sy) (r+1) + Cy, con Sx, Sy, Cx, Cy constantes de la clase.
#   Igualdad para infinitos r obliga a igualar coeficientes:
#   3^(Sx) = 3^(Sy), o sea Sx = Sy. QED.
#
#   COROLARIO 1 (la fusion desbalanceada tiene MEDIDA CERO). Un encuentro
#   T^t(r) = T^t(r+1) con S distintas es una ecuacion afin con
#   coeficientes distintos: a lo sumo UNA solucion r por clase. Union
#   numerable de puntos: medida 2-adica cero. (El 10,3% de fusiones
#   desbalanceadas que se miden desde el estado rebote son el fenomeno
#   de cerca del atractor -- numeros chicos chocando en el ciclo --,
#   no masa estructural.)
#
#   COROLARIO 2 (solo el delta balanceado importa). Lo mismo vale para
#   pares {v, v+1} reentrantes con delta arrastrado d != 0: fundirse de
#   clase exigiria compensacion de clase, que el lema prohibe. Luego en
#   la ecuacion de renovacion solo sobreviven (salvo medida cero) las
#   reentradas consecutivas con d = 0 (que valen f) y las reentradas
#   rebote con el delta canonico (que valen g): EL SISTEMA COLAPSA A
#   LAS DOS INCOGNITAS f Y g MAS LAS MASAS DE CLASE, que son calculables.
#
#   Aqui se verifica el lema exhaustivamente: todas las clases mod 2^12
#   cuya fusion ocurre en t <= 12 pasos (fusion valida para TODA la
#   clase, comprobada con dos representantes lejanos) tienen S igualadas.
# ---------------------------------------------------------------------------

M_BAL = 12
clases_fundidas = 0
for r0 in range(2 ** M_BAL):
    # representantes lejanos de la clase r0 mod 2^M_BAL
    testigos = (r0, r0 + 2 ** M_BAL * 12345)
    fusion_t = None
    for t in range(1, M_BAL + 1):
        vale = True
        for rep in testigos:
            x, y = rep, rep + 1
            Sx = Sy = 0
            for _ in range(t):
                if x % 2:
                    Sx += 1
                if y % 2:
                    Sy += 1
                x, y = paso(x), paso(y)
            if x != y:
                vale = False
                break
        if vale:
            fusion_t = t
            break
    if fusion_t is None:
        continue
    clases_fundidas += 1
    for rep in testigos:
        x, y = rep, rep + 1
        Sx = Sy = 0
        for _ in range(fusion_t):
            if x % 2:
                Sx += 1
            if y % 2:
                Sy += 1
            x, y = paso(x), paso(y)
        if Sx != Sy:
            raise SystemExit("FALLO balance: clase %d funde en t=%d con "
                             "S %d/%d" % (r0, fusion_t, Sx, Sy))

print()
print("COMPROBACION 17 OK: LEMA DEL BALANCE FORZADO. Las %d clases mod 2^%d"
      % (clases_fundidas, M_BAL))
print("que funden en t <= %d pasos para toda la clase tienen S igualadas," % M_BAL)
print("sin excepcion. Corolarios: la fusion desbalanceada tiene medida")
print("cero (choques esporadicos cerca del atractor), y en la renovacion")
print("solo sobreviven las reentradas con delta canonico: el sistema")
print("colapsa a las incognitas f y g mas masas de clase calculables.")

print()
print("b(k) medida  :", b_medida)
print("b(k) publicada:", B_PUBLICADA[:len(b_medida)])
print()
print("CONCLUSION: en los %d niveles comprobados (k = %d..%d), una clase se"
      % (K_MAX - K_MIN + 1, K_MIN, K_MAX))
print("estrena en el nivel k+1 EXACTAMENTE cuando T^k(r) y T^k(r+1) se")
print("encuentran por primera vez en un vortice (a = 3b+1, paridades")
print("opuestas, S compensada en 1). Cero fallos y cero falsos positivos:")
print("es caracterizacion, no tendencia. b(k) = numero de soluciones de esa")
print("congruencia por nivel -- la pregunta de la razon 2 tiene ecuacion.")
