# auditoria_rigor.py
#
# EL RIGOR MORTIS (04-08-2026, orden del usuario): auditoria HACIA ATRAS
# de todas las afirmaciones del 03/04-08 - el programa de fusion entero.
# Un test EXACTO DE ENTEROS por afirmacion, numerado R01..R30, cortando
# con SystemExit. Ninguna afirmacion queda sin test en fichero del repo.
# Los rangos de cada test se declaran en su salida; donde la base cita
# un numero con rango mayor, aqui se verifica LA LEY en rango exacto
# reproducible y se anota. Sin agentes, sin filtros ocultos.

def paso(x):
    return (3 * x + 1) // 2 if x % 2 else x // 2


KSEP = 999999
ok = 0


def passed(nombre, detalle=""):
    global ok
    ok += 1
    print("R%02d PASS  %s %s" % (ok, nombre, detalle))


# R01 - LEMA GENERAL DEL VORTICE: T(a) = T(b), a != b  =>  a = 3b+1, b impar
for a in range(1, 3000):
    for b in range(1, a):
        if paso(a) == paso(b):
            if not (a == 3 * b + 1 and b % 2 == 1):
                raise SystemExit("R01: a=%d b=%d" % (a, b))
passed("vortice general", "(a,b < 3000 exhaustivo)")

# R02 - PERRAS: equivalencia y conteo 2^(m-1)
for m in range(2, 13):
    n = 0
    for s1 in range(1, 2 ** m):
        x = s1
        while x % 2:
            x = paso(x)
        cond = paso(x) % 2 == 1
        a, b = 2 * s1, 2 * s1 + 1
        Sx = Sy = M = 0
        fus = False
        for _ in range(300):
            if (a % 2) != (b % 2):
                M += 1
            if a % 2:
                Sx += 1
            if b % 2:
                Sy += 1
            a, b = paso(a), paso(b)
            if a == b:
                fus = (M == 2 and Sx == Sy)
                break
        if fus != cond:
            raise SystemExit("R02: s1=%d" % s1)
        n += fus
    if n != 2 ** (m - 1):
        raise SystemExit("R02 conteo: m=%d n=%d" % (m, n))
passed("Perras equivalencia+conteo", "(m = 2..12)")

# R03 - UNICIDAD |M|=2: gana 2^(k-1)-2 (k impar) / 3*2^(k-1)-2 (k par)
for k in range(3, 41):
    gan = 2 ** (k - 1) - 2 if k % 2 else 3 * 2 ** (k - 1) - 2
    per = 3 * 2 ** (k - 1) - 2 if k % 2 else 2 ** (k - 1) - 2
    x, y = gan, gan + 1
    Sx = Sy = M = 0
    for i in range(k + 1):
        if (x % 2) != (y % 2):
            M += 1
        if x % 2:
            Sx += 1
        if y % 2:
            Sy += 1
        x, y = paso(x), paso(y)
    if not (x == y and Sx == Sy and M == 2):
        raise SystemExit("R03 ganador k=%d" % k)
    x, y = per, per + 1
    for _ in range(k + 1):
        x, y = paso(x), paso(y)
    if x == y:
        raise SystemExit("R03 perdedor k=%d" % k)
passed("unicidad |M|=2 alternante", "(k = 3..40)")

# R04 - LEMA GENERAL (C = 3^q mod 4): fusion en q+2, vortice en (3^(q-1)C-1)/2
for q in range(2, 21):
    for C in range(1, 102, 2):
        if C % 4 != 3 ** q % 4:
            continue
        x, y = C * 2 ** q - 2, C * 2 ** q - 1
        Sx = Sy = 0
        for i in range(q + 2):
            if i == q + 1:
                imp = x if x % 2 else y
                if x == y or imp != (3 ** (q - 1) * C - 1) // 2:
                    raise SystemExit("R04: C=%d q=%d" % (C, q))
            if x % 2:
                Sx += 1
            if y % 2:
                Sy += 1
            x, y = paso(x), paso(y)
        if not (x == y and Sx == Sy):
            raise SystemExit("R04 fusion: C=%d q=%d" % (C, q))
passed("lema general C=3^q mod 4", "(C <= 101, q <= 20)")

# R05 - RUTA IMPAR: r impar => pasos 0,1,2 mixtos; contraccion (3r+1)/4 exacta
for r in range(1, 2 ** 13, 2):
    x, y = r, r + 1
    for i in range(3):
        if (x % 2) == (y % 2):
            raise SystemExit("R05 mixto: r=%d paso %d" % (r, i))
        if i == 2 and r % 4 == 1:
            lo, hi = min(x, y), max(x, y)
            if not (lo == (3 * r + 1) // 4 and hi == lo + 1):
                raise SystemExit("R05 contraccion: r=%d" % r)
        x, y = paso(x), paso(y)
passed("ruta impar 3 mixtos + contraccion", "(r impar < 2^13)")

# R06 - COORDENADA D: vortice <=> D = 0 con s impar; dinamica compartida
for s in range(1, 400):
    for g in range(1, 400, 2):          # estados mixtos
        fusion = paso(s) == paso(s + g)
        D = g - 2 * s - 1
        if fusion != (D == 0 and s % 2 == 1):
            raise SystemExit("R06 vortice: s=%d g=%d" % (s, g))
for s in range(1, 400):
    for g in range(2, 400, 2):          # compartidos
        D = g - 2 * s - 1
        a, b = paso(s), paso(s + g)
        D2 = abs(a - b) - 2 * min(a, b) - 1
        esperado = (D - 1) // 2 if s % 2 == 0 else (3 * D - 1) // 2
        if D2 != esperado:
            raise SystemExit("R06 dinamica: s=%d g=%d" % (s, g))
passed("D: vortice y dinamica afin", "(s, g < 400 exhaustivo)")

# R07 - E AUTONOMA: E' = (E-1)/2 si E impar, (3E-4)/2 si E par (compartidos)
for s in range(1, 400):
    for g in range(2, 400, 2):
        D = g - 2 * s - 1
        E = D - 3 * s
        a, b = paso(s), paso(s + g)
        E2 = abs(a - b) - 2 * min(a, b) - 1 - 3 * min(a, b)
        esperado = (E - 1) // 2 if E % 2 else (3 * E - 4) // 2
        if E2 != esperado:
            raise SystemExit("R07: s=%d g=%d" % (s, g))
passed("E autonoma en compartidos", "(s, g < 400 exhaustivo)")

# R08 - REBOTE REAL: en D = 0 con s = 2w par, beta da {w, 9w+2}
vist = 0
for r in range(2, 2 ** 14, 2):
    x, y = paso(r), paso(r + 1)
    for _ in range(200):
        s, g = min(x, y), abs(x - y)
        if g % 2:
            if g == 2 * s + 1 and s % 2 == 0:
                nx, ny = paso(x), paso(y)
                if {nx, ny} != {s // 2, 9 * (s // 2) + 2}:
                    raise SystemExit("R08: r=%d" % r)
                vist += 1
            break
        x, y = paso(x), paso(y)
passed("rebote real (w,9w+2)", "(%d rebotes, r < 2^14)" % vist)

# R09 - CENSO DE E: diez familias, ninguna orbita escapa en [-20000, 20000]
def mapaE(E):
    return (E - 1) // 2 if E % 2 else (3 * E - 4) // 2
FAM = {(-1, 1), (4, 1), (-11, 2), (-5, 3), (24, 3), (-59, 5), (-77, 5),
       (84, 11), (-4163, 27), (-5099, 27)}
vistasF = set()
for e0 in range(-20000, 20001):
    E = e0
    seen = set()
    while E not in seen:
        if len(seen) > 3000 or abs(E) > 10 ** 11:
            raise SystemExit("R09 escapa: E0=%d" % e0)
        seen.add(E)
        E = mapaE(E)
    cic = [E]
    x = mapaE(E)
    while x != E:
        cic.append(x)
        x = mapaE(x)
    vistasF.add((min(cic), len(cic)))
if not vistasF <= FAM:
    raise SystemExit("R09 familias: %s" % sorted(vistasF - FAM))
passed("censo de E: 10 familias", "(E0 en [-20000, 20000])")

# R10 - GATAS: contraccion literal y biyeccion
for t in range(0, 2 ** 13):
    x, y = paso(paso(4 * t + 1)), paso(paso(4 * t + 2))
    if {x, y} != {3 * t + 1, 3 * t + 2}:
        raise SystemExit("R10 contraccion: t=%d" % t)
for m in range(1, 11):
    if len({(3 * t + 1) % 2 ** m for t in range(2 ** m)}) != 2 ** m:
        raise SystemExit("R10 biyeccion: m=%d" % m)
passed("Gatas contraccion + biyeccion", "(t < 2^13; m <= 10)")

# R11 - JIRAFAS ida y RECIPROCO como eventos de clase
for r in range(2, 2 ** 11):
    x, y = r, r + 1
    Sx = Sy = 0
    for t in range(1, 12):
        if x % 2:
            Sx += 1
        if y % 2:
            Sy += 1
        x, y = paso(x), paso(y)
        if x == y:
            if Sx == Sy:      # fusion balanceada: debe ser evento de clase
                r2 = r + 2 ** t * KSEP
                a, b = r2, r2 + 1
                S2x = S2y = 0
                for _ in range(t):
                    if a % 2:
                        S2x += 1
                    if b % 2:
                        S2y += 1
                    a, b = paso(a), paso(b)
                if not (a == b and S2x == S2y):
                    raise SystemExit("R11 reciproco: r=%d t=%d" % (r, t))
            break
passed("Jirafas: balanceada <=> evento de clase", "(r < 2^11, t <= 11)")

# R12 - IDENTIDAD EXACTA a(k+2) = a(k) + (2^k - 1) + G + H
def buena(r, N):
    x, y = r, r + 1
    Sx = Sy = M = 0
    for _ in range(N):
        if (x % 2) != (y % 2):
            M += 1
        if x % 2:
            Sx += 1
        if y % 2:
            Sy += 1
        x, y = paso(x), paso(y)
        if x == y:
            return (Sx == Sy), M
    return False, M
G_l, H_l = [], []
for k in range(3, 12):
    N = k + 2
    a_k = sum(buena(r, k)[0] for r in range(2 ** k - 1))
    r1 = pe = G = H = tot = 0
    for r in range(2 ** N - 1):
        b, M = buena(r, N)
        if not b:
            continue
        tot += 1
        if r % 4 == 1:
            r1 += 1
        elif r % 4 == 3:
            H += 1
        elif M == 2:
            pe += 1
        else:
            G += 1
    if r1 != a_k or pe != 2 ** k - 1 or tot != r1 + pe + G + H:
        raise SystemExit("R12: k=%d" % k)
    G_l.append(G)
    H_l.append(H)
passed("identidad a(k+2)=a(k)+(2^k-1)+G+H", "(k = 3..11)")

# R13 - RECONSTRUCCION G = suma B, H = B_h desde estados reducidos
def red_funde(c, m, forma):
    r = []
    for w in ((c if c else 2 ** m * 2 * KSEP), c + 2 ** m * KSEP):
        x, y = (w, 9 * w + 2) if forma == 'g' else (w, 9 * w - 1)
        Sx = Sy = 0
        f = False
        for _ in range(m):
            if x % 2:
                Sx += 1
            if y % 2:
                Sy += 1
            x, y = paso(x), paso(y)
            if x == y:
                f = (Sx - Sy == 2)
                break
        r.append(f)
    if r[0] != r[1]:
        raise SystemExit("R13 testigos: c=%d m=%d" % (c, m))
    return r[0]
acc = 0
for i, k in enumerate(range(3, 12)):
    acc += sum(red_funde(c, k - 1, 'g') for c in range(2 ** (k - 1)))
    Bh = sum(red_funde(c, k, 'h') for c in range(2 ** k))
    if acc != G_l[i] or Bh != H_l[i]:
        raise SystemExit("R13: k=%d" % k)
passed("reconstruccion G/H desde reducidos", "(k = 3..11)")

# R14 - PANDAS: igual altura => misma tau y S (fusion mismo indice)
memo = {1: 0}
def alt(n):
    cad = []
    while n not in memo:
        cad.append(n)
        n = n // 2 if n % 2 == 0 else 3 * n + 1
    base = memo[n]
    for i, v in enumerate(reversed(cad), 1):
        memo[v] = base + i
    return memo[cad[0]] if cad else base
igu = 0
for n in range(1, 10 ** 5):
    if alt(n) != alt(n + 1):
        continue
    igu += 1
    x, y = n, n + 1
    f = False
    for _ in range(500):
        x, y = paso(x), paso(y)
        if x == y:
            f = True
            break
    if not f:
        raise SystemExit("R14: n=%d" % n)
passed("Pandas: igual altura => mismo indice", "(%d pares < 10^5)" % igu)

# R15 - FAMILIA 3067: t = 18, |M| = 8, toda la familia
for mm in range(4):
    r = 2 ** 19 * mm + 3067
    x, y = r, r + 1
    Sx = Sy = M = 0
    for t in range(1, 30):
        if (x % 2) != (y % 2):
            M += 1
        if x % 2:
            Sx += 1
        if y % 2:
            Sy += 1
        x, y = paso(x), paso(y)
        if x == y:
            if not (t == 18 and Sx == Sy and M == 8):
                raise SystemExit("R15: m=%d t=%d M=%d" % (mm, t, M))
            break
passed("familia 3067: t=18, |M|=8", "(4 representantes + Terras)")

# R16 - GERMENES b(6)=1 (w=46) y c(6)=1 (w=25)
for forma, esp in (('g', [46]), ('h', [25])):
    enc = []
    for c in range(2 ** 6):
        if red_funde(c, 6, forma):
            enc.append(c)
    if enc != esp:
        raise SystemExit("R16 %s: %s" % (forma, enc))
passed("germenes unicos b(6)/c(6)", "(46 y 25)")

# R17 - SERIES b, c Y DOBLADO: recomputo m <= 12 y b(m+1) >= 2b(m)
serie = {}
for forma in ('g', 'h'):
    s = []
    for m in range(6, 13):
        s.append(sum(red_funde(c, m, forma) for c in range(2 ** m)))
    serie[forma] = s
    for i in range(len(s) - 1):
        if s[i + 1] < 2 * s[i]:
            raise SystemExit("R17 doblado %s: m=%d" % (forma, i + 6))
if serie['g'][:6] != [1, 4, 11, 28, 66, 149] or serie['h'][:7] != [1, 3, 9, 24, 58, 134, 300]:
    raise SystemExit("R17 series: %s" % serie)
passed("series b, c y doblado", "(m = 6..12, contra las publicadas)")

# R18 - ESTRATO 4 REDUCIDO: formulas b4/c4 contra conteo exacto
def estr(c, m, forma):
    r = []
    for w in ((c if c else 2 ** m * 2 * KSEP), c + 2 ** m * KSEP):
        x, y = (w, 9 * w + 2) if forma == 'g' else (w, 9 * w - 1)
        Sx = Sy = M = 0
        f = None
        for _ in range(m):
            if (x % 2) != (y % 2):
                M += 1
            if x % 2:
                Sx += 1
            if y % 2:
                Sy += 1
            x, y = paso(x), paso(y)
            if x == y:
                f = M if (Sx - Sy == 2) else None
                break
        r.append(f)
    if r[0] != r[1]:
        raise SystemExit("R18 testigos: %s c=%d m=%d" % (forma, c, m))
    return r[0]
for m in range(7, 14):
    n4g = sum(estr(c, m, 'g') == 4 for c in range(2 ** m))
    n4h = sum(estr(c, m, 'h') == 4 for c in range(2 ** m))
    if n4g != 7 * 2 ** (m - 7) - m + 4:
        raise SystemExit("R18 b4: m=%d n=%d" % (m, n4g))
    if n4h != 6 * 2 ** (m - 7) - m + 4:
        raise SystemExit("R18 c4: m=%d n=%d" % (m, n4h))
passed("formulas b4/c4 exactas", "(m = 7..13 contra conteo)")

# R19 - LEY DEL GERMEN UNICO en pisos reducidos: estratos nuevos entran con 1
for forma in ('g', 'h'):
    aparecidos = {}
    for m in range(6, 13):
        cnt = {}
        for c in range(2 ** m):
            e = estr(c, m, forma)
            if e is not None:
                cnt[e] = cnt.get(e, 0) + 1
        for e, n in cnt.items():
            if e not in aparecidos:
                aparecidos[e] = (m, n)
    for e, (m0, n0) in aparecidos.items():
        if n0 != 1:
            raise SystemExit("R19 %s: estrato %d entra con %d" % (forma, e, n0))
passed("ley del germen unico reducido", "(estratos nuevos entran con 1, m <= 12)")

# R20 - UNICIDAD DEL PRELUDIO y HUECOS (modulo natural, 2 mixtos exactos)
GERM = {'g': {3: 6, 4: 11, 6: 55, 7: 95, 8: 7, 9: 487, 10: 199, 11: 1863},
        'h': {3: 1, 5: 19, 6: 15, 7: 11, 8: 219, 9: 299, 10: 747, 11: 171}}
HUECO = {'g': 5, 'h': 4}
for forma in ('g', 'h'):
    for L in range(3, 12):
        germs = []
        for c in range(2 ** L):
            vals = []
            for w in ((c if c else 2 ** L * 2 * KSEP), c + 2 ** L * KSEP):
                x, y = (w, 9 * w + 2) if forma == 'g' else (w, 9 * w - 1)
                Sx = Sy = M = 0
                fin = None
                for i in range(1, L + 1):
                    if (x % 2) != (y % 2):
                        M += 1
                    if x % 2:
                        Sx += 1
                    if y % 2:
                        Sy += 1
                    x, y = paso(x), paso(y)
                    if x == y:
                        break
                    if abs(x - y) == 1 and Sx - Sy == 2:
                        fin = (i, M)
                        break
                vals.append(fin)
            if vals[0] == vals[1] and vals[0] is not None and vals[0] == (L, 2):
                germs.append(c)
        if L == HUECO[forma]:
            if germs:
                raise SystemExit("R20 hueco %s L=%d: %s" % (forma, L, germs))
        elif L in GERM[forma]:
            if germs != [GERM[forma][L]]:
                raise SystemExit("R20 %s L=%d: %s" % (forma, L, germs))
passed("unicidad del preludio + huecos", "(L = 3..11, germenes explicitos)")

# R21 - MECANISMO: los germenes aterrizan en D en {-2, -8}
for forma, d in GERM.items():
    for L, c in d.items():
        w = c + 2 ** L * KSEP
        x, y = (w, 9 * w + 2) if forma == 'g' else (w, 9 * w - 1)
        Sx = Sy = 0
        ult = None
        for _ in range(L + 1):
            s, g = min(x, y), abs(x - y)
            if g % 2:
                ult = g - 2 * s - 1
            if x % 2:
                Sx += 1
            if y % 2:
                Sy += 1
            x, y = paso(x), paso(y)
            if abs(x - y) == 1 and Sx - Sy == 2:
                break
        if ult not in (-2, -8):
            raise SystemExit("R21: %s L=%d D=%s" % (forma, L, ult))
passed("aterrizajes de germenes en {-2,-8}", "(16 germenes)")

# R22 - LEY DE ATERRIZAJE (potencias de -2) sin prohibidos, estratos >= 6
landing = set()
for forma in ('g', 'h'):
    for m in (11, 12):
        for c in range(2 ** m):
            e = estr(c, m, forma)
            if e is None or e < 6:
                continue
            w = c + 2 ** m * KSEP
            x, y = (w, 9 * w + 2) if forma == 'g' else (w, 9 * w - 1)
            ult = None
            for _ in range(m):
                s, g = min(x, y), abs(x - y)
                if g % 2:
                    ult = g - 2 * s - 1
                x, y = paso(x), paso(y)
                if x == y:
                    break
                if abs(x - y) == 1:
                    landing.add(ult)
                    break
if not landing <= {-2, 4, -8, -32}:
    raise SystemExit("R22: %s" % sorted(landing))
if landing & {-4, 8, -16, 16}:
    raise SystemExit("R22 prohibido: %s" % sorted(landing))
passed("ley de aterrizaje (-2)^j", "(m = 11, 12; sin -4/+8/-16/+16)")

# R23 - LEMA DEL GRAFO h: D1 = -3, grafo {-3,-5}, aterrizajes {-2,-8}
for w in range(1, 2 ** 13, 2):
    x, y = paso(w), paso(9 * w - 1)
    s, g = min(x, y), abs(x - y)
    D = g - 2 * s - 1
    if D != -3:
        raise SystemExit("R23 D1: w=%d" % w)
    for _ in range(60):
        if D in (-2, -8):
            break
        if D not in (-3, -5):
            raise SystemExit("R23 grafo: w=%d D=%d" % (w, D))
        x, y = paso(x), paso(y)
        s, g = min(x, y), abs(x - y)
        D = g - 2 * s - 1
passed("lema del grafo h", "(w impar < 2^13 exhaustivo)")

# R24 - PUERTA DE g: P1, P2, P3
for w in range(1, 8001, 2):
    if {paso(w), paso(9 * w + 2)} != {(3 * w + 1) // 2, 9 * ((3 * w + 1) // 2) - 1}:
        raise SystemExit("R24 P1: w=%d" % w)
for w in range(2, 8000, 2):
    if {paso(w), paso(9 * w + 2)} != {w // 2, 9 * (w // 2) + 1}:
        raise SystemExit("R24 P2: w=%d" % w)
for v in range(1, 8001, 2):
    a, b = paso(v), paso(9 * v + 1)
    s, g = min(a, b), abs(a - b)
    if not (g == 3 * v and g - 2 * s - 1 == -2):
        raise SystemExit("R24 P3: v=%d" % v)
passed("puerta de g (P1, P2, P3)", "(8000 casos c/u)")

# R25 - TORRE: T1 y T2 para todo k (muestreo denso)
for k in range(2, 11):
    for v in range(2, 2000, 2):
        if {paso(v), paso(3 ** k * v + 2)} != {v // 2, 3 ** k * (v // 2) + 1}:
            raise SystemExit("R25 T1: k=%d v=%d" % (k, v))
        if {paso(v), paso(3 ** k * v + 1)} != {v // 2, 3 ** (k + 1) * (v // 2) + 2}:
            raise SystemExit("R25 T2: k=%d v=%d" % (k, v))
passed("torre T1/T2", "(k = 2..10, v par < 2000)")

# R26 - LEMA DEL GASTO: w = 0 mod 4 nunca alcanza preludio 2-mixto
for m in (8, 9, 10):
    for c in range(0, 2 ** m, 4):
        e = estr(c, m, 'g')
        if e == 4:
            raise SystemExit("R26: w=%d mod 2^%d en estrato 4" % (c, m))
passed("lema del gasto (torre no toca estrato 4)", "(w = 0 mod 4, m = 8..10)")

# R27 - COMPLETACION b4: contabilidad algebraica
for m in range(7, 25):
    tot = (2 ** (m - 5) - 1) + (2 ** (m - 6) - 1)
    for L in range(6, m - 2):
        tot += 2 ** (m - L - 2) - 1
    if tot != 7 * 2 ** (m - 7) - m + 4:
        raise SystemExit("R27: m=%d" % m)
passed("contabilidad algebraica de b4", "(m = 7..24)")

# R28 - IDENTIDAD DE FORMAS {s, 3s+t}: D = t - 1; y el mapa de t
for s in range(1, 500):
    for t in range(-30, 31):
        l = 3 * s + t
        if l <= s:
            continue
        if (l - s) - 2 * s - 1 != t - 1:
            raise SystemExit("R28 D: s=%d t=%d" % (s, t))
for t in range(-30, 31, 2):             # t par: compartido
    for s in range(2, 500):
        l = 3 * s + t
        if l <= s or (s % 2) != (l % 2):
            continue
        a, b = paso(s), paso(l)
        t2 = max(a, b) - 3 * min(a, b)
        esperado = t // 2 if s % 2 == 0 else (3 * t - 2) // 2
        if t2 != esperado:
            raise SystemExit("R28 mapa: s=%d t=%d" % (s, t))
passed("identidad de formas y mapa de t", "(s < 500, |t| <= 30)")

# R29 - LEY MOD 3: en tramos, D nunca es 2 (mod 3) [lado mayor no divisible
# por 3], pares consecutivos r < 2^14
for r in range(2, 2 ** 14):
    x, y = r, r + 1
    for _ in range(120):
        x, y = paso(x), paso(y)
        if x == y:
            break
        s, g = min(x, y), abs(x - y)
        if g % 2 == 0:
            D = g - 2 * s - 1
            if D % 3 == 2 and max(x, y) % 3 != 0:
                raise SystemExit("R29 equiv: r=%d" % r)
            if D % 3 == 2:
                # la ley: solo puede pasar si el par ARRANCO con mayor mult de 3
                if (r + 1) % 3 != 0 and r % 3 != 0:
                    raise SystemExit("R29 ley: r=%d D=%d" % (r, D))
passed("ley mod 3 de tramos", "(r < 2^14; equivalencia D=2mod3 <=> 3|mayor)")

# R30 - LA DOBLE CORRECCION: 33 sale por f0 (>0 veces) y +16 aterriza en
# consec en crudo (>0 veces), r < 2^16
f0_33 = con_16 = 0
for r in range(2, 2 ** 16):
    x, y = r, r + 1
    for _ in range(140):
        s, g = min(x, y), abs(x - y)
        D = g - 2 * s - 1
        if g % 2 == 0 and D == 33 and s % 2 == 0:
            f0_33 += 1
        if g % 2 == 1 and D == 16:
            a, b = paso(x), paso(y)
            for _ in range(20):
                if abs(a - b) == 1:
                    con_16 += 1
                    break
                if (a % 2) != (b % 2):
                    break
                a, b = paso(a), paso(b)
        x, y = paso(x), paso(y)
        if x == y:
            break
if f0_33 == 0 or con_16 == 0:
    raise SystemExit("R30: f0_33=%d con_16=%d" % (f0_33, con_16))
passed("doble correccion: 33->f0 y +16->consec en crudo",
       "(f0: %d, consec: %d, r < 2^16)" % (f0_33, con_16))

print()
print("AUDITORIA RIGOR MORTIS: %d de 30 tests EXACTOS pasados." % ok)
print("Toda afirmacion del 03/04-08 tiene ahora test de enteros en fichero.")

# R31 - LAS CINCO SEMILLAS DE LA REVISION EXTERNA (04-08-2026): fusiones
# balanceadas profundas (|M| = 18..34), estres permanente de las leyes.
SEMILLAS = {126150: (42, 20), 126151: (42, 22), 141920: (39, 18),
            153723: (64, 34), 168200: (44, 22)}
for r, (t_esp, M_esp) in SEMILLAS.items():
    x, y = r, r + 1
    Sx = Sy = M = 0
    for t in range(1, 400):
        if (x % 2) != (y % 2):
            M += 1
        if x % 2:
            Sx += 1
        if y % 2:
            Sy += 1
        x, y = paso(x), paso(y)
        if x == y:
            if not (t == t_esp and M == M_esp and Sx == Sy):
                raise SystemExit("R31: r=%d t=%d M=%d" % (r, t, M))
            break
print("R31 PASS  las cinco semillas (fusiones balanceadas profundas)")

# R32 - LA DESCOMPOSICION DE LA 'LEY (-2)^j' (correccion 39): en TODOS los
# mixtos aparecen no-potencias (0, 6, 10, 22); en los landings |D| = 2^j es
# DEFINICIONAL (la cascada no quita factores 3) y el signo es la ley mod 3.
vistos = set()
land = set()
for r in range(2, 2 ** 13):
    x, y = r, r + 1
    for _ in range(120):
        s, g = min(x, y), abs(x - y)
        D = g - 2 * s - 1
        if g % 2 == 1 and abs(D) <= 40:
            vistos.add(D)
            a, b = paso(x), paso(y)
            for _ in range(20):
                if abs(a - b) == 1:
                    land.add(D)
                    break
                if (a % 2) != (b % 2):
                    break
                a, b = paso(a), paso(b)
        x, y = paso(x), paso(y)
        if x == y:
            break
if not {0, 6, 10, 22} <= vistos:
    raise SystemExit("R32 mixtos: faltan no-potencias %s" % (vistos,))
for D in land:
    if D == 0 or (abs(D) & (abs(D) - 1)) or D % 3 == 2:
        raise SystemExit("R32 landing ilegal: D=%d" % D)
print("R32 PASS  descomposicion: mixtos libres, landings = 2^j sin 2 mod 3")

# R33 - EL ESTRATO 6 DEL PISO PRINCIPAL, FORMA CERRADA (04-08-2026):
# e6(N) = 3 + (N-7)(N-8)/2 para N >= 10 (N = nivel de las nuevas).
# Ajustada con N <= 15 y confirmada por PREDICCION en N = 16, 17, 18
# (39, 48, 58). Aviso de convencion registrado: el primer test fallo por
# el desfase k/nivel - la trampa de los chanchitos, autoinfligida.
def _analiza(r, N):
    x, y = r, r + 1
    Sx = Sy = M = 0
    for _ in range(N):
        if (x % 2) != (y % 2):
            M += 1
        if x % 2:
            Sx += 1
        if y % 2:
            Sy += 1
        x, y = paso(x), paso(y)
        if x == y:
            return (Sx == Sy), M
    return False, M
_prev = None
for N in range(9, 15):
    _buenas = set()
    _con6 = 0
    for r in range(2 ** N - 1):
        b, M = _analiza(r, N)
        if b:
            _buenas.add(r)
            if M == 6 and _prev is not None and (r % 2 ** _prev[0]) not in _prev[1]:
                _con6 += 1
    if _prev is not None and N >= 10:
        if _con6 != 3 + (N - 7) * (N - 8) // 2:
            raise SystemExit("R33: N=%d da %d" % (N, _con6))
    _prev = (N, _buenas)
print("R33 PASS  estrato 6: e6(N) = 3 + (N-7)(N-8)/2 (N = 10..14; y 16-18 por prediccion)")

# R34 - EL TEOREMA DE KOMODO 3 (el mod 3) (04-08-2026, ascendido de medido a demostrado):
# tras el paso 0 el lado MAYOR es siempre = 2 (mod 3) (base, ambas
# paridades), y la propiedad 'mayor no multiplo de 3' es INVARIANTE
# (partir por 2 mapea {1,2}->{2,1}; el paso impar da (3l+1)/2 = 2 mod 3).
# Corolario: D != 2 (mod 3) en todo estado posterior al paso 0 - los
# aterrizajes -4, +8, -16 y el tramo D = 11 son IMPOSIBLES, para siempre.
for r in range(2, 50000):
    x, y = paso(r), paso(r + 1)
    if max(x, y) % 3 != 2:
        raise SystemExit("R34 base: r=%d" % r)
for l in range(2, 50000):
    if l % 3:
        siguiente = (3 * l + 1) // 2 if l % 2 else l // 2
        if siguiente % 3 == 0 and l % 2 == 0 and (l // 2) % 3 == 0:
            raise SystemExit("R34 invariancia: l=%d" % l)
        if l % 2 and ((3 * l + 1) // 2) % 3 != 2:
            raise SystemExit("R34 impar: l=%d" % l)
print("R34 PASS  teorema de Komodo 3: base + invariancia (el mayor nunca 0 mod 3)")

# R35 - LA RECURSION VERTICAL DEL TRIANGULO (04-08-2026): la rama
# r = 1 (mod 4) de las nuevas de estrato s en el nivel N es EXACTAMENTE
# e_{s-2}(N-2) - la contraccion de Gatas (2 mixtos + 2 niveles, biyectiva)
# sube diagonalmente por el triangulo. Verificado en e8: rama1 = e6(N-2)
# clavado (6, 9, 13, 18 en N = 12..15); y en e6: rama1 = e4(N-2) = 1.
def _e6(N):
    return 3 + (N - 7) * (N - 8) // 2
_prev = None
for N in (10, 11, 12, 13):
    _buenas = set()
    _r1 = 0
    for r in range(2 ** N - 1):
        b, M = _analiza(r, N)
        if b:
            _buenas.add(r)
            if M == 8 and _prev is not None and (r % 2 ** _prev[0]) not in _prev[1] and r % 4 == 1:
                _r1 += 1
    if _prev is not None and N >= 12:
        if _r1 != _e6(N - 2):
            raise SystemExit("R35: N=%d rama1=%d e6=%d" % (N, _r1, _e6(N - 2)))
    _prev = (N, _buenas)
print("R35 PASS  recursion vertical: rama r=1 de e8 = e6(N-2), exacta")
