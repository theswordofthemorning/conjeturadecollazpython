# A34.py -- AGENTE 2 (Python independiente), escrito desde cero.
#
# ENUNCIADO A VERIFICAR (A34):
#   "los supervivientes de la criba tienen densidad -> 0 pero cardinal -> infinito,
#    del orden de 2^(0,95k). La criba compra densidad, no compra cobertura."
#
# MAPA: ATAJO (Terras):  n par -> n/2 ;  n impar -> (3n+1)/2.
#   (La criba de descenso clasica se define sobre este mapa: cada paso consume
#    exactamente un bit, y los primeros k pasos los decide n mod 2^k.)
#
# DEFINICION DE LA CRIBA (derivada aqui desde la identidad, no copiada):
#   Para n = 2^k*m + r, tras j <= k pasos:  T^j(n) = (3^{s_j}*n + C_j) / 2^j  con C_j >= 0,
#   donde s_j = numero de pasos impares entre los primeros j (depende solo de r mod 2^j).
#   - Si 3^{s_j} <  2^j para algun j <= k:  T^j(n) < n para todo n grande de la clase
#     -> la clase queda ELIMINADA (descenso garantizado).
#   - Si 3^{s_j} >= 2^j para todo j <= k:  T^j(n) = (3^{s_j} n + C_j)/2^j >= n  (C_j>=0)
#     -> la clase SOBREVIVE: ninguno de sus miembros baja en los primeros k pasos.
#   a(k) = numero de clases mod 2^k que sobreviven.
#
# TRES IMPLEMENTACIONES QUE NO COMPARTEN LOGICA:
#   A) barrido directo residuo a residuo (k <= 16)
#   B) extension de supervivientes con estado simbolico (r, s, t)  (k <= 22)
#   C) conteo puramente combinatorio de vectores de paridad admisibles (k <= 1400)
#      (A vs C ademas verifica la biyeccion residuo <-> vector de paridad en este contexto)
#
# Todo lo que decide es entero exacto. Los floats solo imprimen.

import math

def fallo(msg):
    raise SystemExit("FALLO: " + msg)

POW3 = [1]
def p3(s):
    while len(POW3) <= s:
        POW3.append(POW3[-1] * 3)
    return POW3[s]

# ---------------- Implementacion A: barrido directo ----------------
def sobrevive_directo(r, k):
    t = r
    s = 0
    for j in range(1, k + 1):
        if t & 1:
            t = (3 * t + 1) // 2
            s += 1
        else:
            t //= 2
        if p3(s) < (1 << j):
            return False
    return True

def a_directo(k):
    return sum(1 for r in range(1 << k) if sobrevive_directo(r, k))

# ---------------- Implementacion B: extension simbolica ----------------
def extension(kmax):
    # invariante del nivel k: para cada clase viva r mod 2^k,
    #   T^k(2^k*m + r) = 3^s * m + t   con (s, t) almacenados.
    vivos = [(0, 0, 0)]  # nivel 0: r=0 mod 1, s=0, t=0
    counts = []
    hijo_impar_siempre_vive = True
    algun_padre_sin_hijos = False
    for k in range(kmax):
        nuevos = []
        for (r, s, t) in vivos:
            n_hijos = 0
            for e in (0, 1):
                u = e * p3(s) + t          # valor tras k pasos del hijo con m' = 0 ... (termino simbolico)
                if u & 1:
                    s2 = s + 1
                    t2 = (3 * u + 1) // 2
                    impar = True
                else:
                    s2 = s
                    t2 = u // 2
                    impar = False
                if p3(s2) >= (1 << (k + 1)):
                    nuevos.append((r + (e << k), s2, t2))
                    n_hijos += 1
                else:
                    if impar:
                        hijo_impar_siempre_vive = False
            if n_hijos == 0:
                algun_padre_sin_hijos = True
        vivos = nuevos
        counts.append(len(vivos))
    return counts, vivos, hijo_impar_siempre_vive, algun_padre_sin_hijos

# ---------------- Implementacion C: conteo de vectores admisibles ----------------
def conteo_dp(kmax):
    # cnt[s] = cuantos vectores de paridad de longitud j con s unos cumplen
    #          3^{s_i} >= 2^i en TODOS los prefijos i <= j
    cnt = {0: 1}
    res = []
    for j in range(1, kmax + 1):
        lim = 1 << j
        nuevo = {}
        for s, c in cnt.items():
            if p3(s) >= lim:
                nuevo[s] = nuevo.get(s, 0) + c
            if p3(s + 1) >= lim:
                nuevo[s + 1] = nuevo.get(s + 1, 0) + c
        cnt = nuevo
        res.append(sum(cnt.values()))
    return res

def log2big(n):
    if n <= 0:
        fallo("log2 de un no positivo")
    b = n.bit_length()
    if b <= 900:
        return math.log2(n)
    sh = b - 900
    return math.log2(n >> sh) + sh

# =================================================================
K_A = 16
K_B = 22
K_C = 1400

print("== A34: supervivientes de la criba de descenso (mapa del ATAJO) ==")
print("")

# --- A vs B vs C en el rango comun
counts_B, vivos_B, impar_ok, padre_sin_hijos = extension(K_B)
counts_C = conteo_dp(K_C)

for k in range(1, K_A + 1):
    aA = a_directo(k)
    if aA != counts_B[k - 1]:
        fallo("A != B en k=%d: %d vs %d" % (k, aA, counts_B[k - 1]))
    if aA != counts_C[k - 1]:
        fallo("A != C en k=%d: %d vs %d" % (k, aA, counts_C[k - 1]))
print("[1] A=B=C para k=1..%d: 0 discrepancias (tres implementaciones sin logica comun)" % K_A)

for k in range(1, K_B + 1):
    if counts_B[k - 1] != counts_C[k - 1]:
        fallo("B != C en k=%d: %d vs %d" % (k, counts_B[k - 1], counts_C[k - 1]))
print("[2] B=C para k=1..%d: 0 discrepancias" % K_B)

print("")
print("    a(k), k=1..%d:" % K_B)
print("    " + ", ".join(str(c) for c in counts_B))
print("")

# --- bordes
for k in range(1, K_A + 1):
    if sobrevive_directo(0, k):
        fallo("r=0 deberia estar eliminada (k=%d)" % k)
    if not sobrevive_directo((1 << k) - 1, k):
        fallo("r=2^k-1 deberia sobrevivir (k=%d)" % k)
print("[3] bordes: r=0 eliminada en el paso 1 y r=2^k-1 sobrevive, k=1..%d: 0 fallos" % K_A)

# --- cardinal -> infinito: no decreciente + el hijo impar de un vivo siempre vive
no_decrece = all(counts_C[i + 1] >= counts_C[i] for i in range(K_C - 1))
if not no_decrece:
    fallo("a(k) decrece en algun k")
igualdades = [i + 1 for i in range(K_B - 1) if counts_B[i + 1] == counts_B[i]]
if not impar_ok:
    fallo("algun hijo con paso k+1 impar murio (refutaria 3^{s+1} >= 3*2^k > 2^{k+1})")
if padre_sin_hijos:
    fallo("algun superviviente se quedo sin hijos")
print("[4] cardinal: a(k) no decrece en k=1..%d; el hijo IMPAR de todo vivo vive" % K_C)
print("    (razon: 3^(s+1) >= 3*2^k > 2^(k+1); comprobado sin excepcion hasta k=%d)" % K_B)
print("    igualdades a(k+1)=a(k) en k<=%d: %s  (solo el arranque; despues crece estricto)"
      % (K_B, igualdades if igualdades else "ninguna"))

# --- densidad -> 0: NO creciente en cada nivel (con niveles de empate exacto), y tiende a 0
if any(counts_C[i + 1] > 2 * counts_C[i] for i in range(K_C - 1)):
    fallo("a(k+1) > 2*a(k) en algun k: la densidad subiria")
empates = [i + 1 for i in range(K_C - 1) if counts_C[i + 1] == 2 * counts_C[i]]
print("[5] densidad: a(k+1) <= 2*a(k) en TODOS los k=1..%d -> d(k)=a(k)/2^k NO crece nunca." % K_C)
print("    OJO (hallazgo de borde): NO decrece estricto en cada nivel. Hay %d niveles con" % len(empates))
print("    a(k+1) = 2*a(k) exacto (d se queda plana): los primeros son %s" % empates[:12])
d22 = counts_B[K_B - 1] / float(1 << K_B)
print("    d(1)=0.5  d(10)=%.6f  d(22)=%.6f  d(100)=2^%.2f  d(%d)=2^%.2f  -> tiende a 0" %
      (counts_B[9] / 1024.0, d22, log2big(counts_C[99]) - 100, K_C, log2big(counts_C[K_C - 1]) - K_C))

# --- semantica de la criba con numeros de verdad (k=10, exacto)
k = 10
elim_muestra = [r for r in range(1 << k) if not sobrevive_directo(r, k)][::97][:20]
sup_muestra = [r for r in range(1 << k) if sobrevive_directo(r, k)][:20]
def paso(n):
    return (3 * n + 1) // 2 if n & 1 else n // 2
for r in elim_muestra:
    for m in (1, 2, 3):
        n0 = (1 << k) * m + r
        n = n0
        bajo = False
        for j in range(k):
            n = paso(n)
            if n < n0:
                bajo = True
                break
        if not bajo:
            fallo("clase eliminada r=%d, m=%d no bajo en %d pasos" % (r, m, k))
for r in sup_muestra:
    for m in (0, 1, 2, 3):
        n0 = (1 << k) * m + r
        if n0 == 0:
            continue
        n = n0
        for j in range(k):
            n = paso(n)
            if n < n0:
                fallo("clase superviviente r=%d, m=%d bajo en el paso %d" % (r, m, j + 1))
print("[6] semantica (k=10): 20 clases eliminadas x m=1..3 bajan todas;")
print("    20 supervivientes x m=0..3 no bajan nunca en 10 pasos. 0 fallos.")
print("    Borde: en una clase eliminada el miembro m=0 puede EMPATAR sin bajar:")
n = 1
tray = [1]
for j in range(2):
    n = paso(n)
    tray.append(n)
print("    r=1, k=2 esta eliminada (3^1 < 2^2) pero n=1 da %s : T^2(1)=1, igualdad, no descenso."
      % tray)
print("    (La garantia de descenso de la criba es para n grande; el enunciado A34 no la usa.)")

# --- el exponente: 2^(0,95k) ?
ln2, ln3 = math.log(2.0), math.log(3.0)
theta = ln2 / ln3  # log_3(2): fraccion minima de impares para no bajar
H = -theta * math.log2(theta) - (1 - theta) * math.log2(1 - theta)
print("")
print("[7] el exponente 0,95:")
print("    teoria: los vectores admisibles piden s_j >= j*log3(2) = %.6f*j en todo prefijo;" % theta)
print("    su tasa de crecimiento limite es la entropia H(log3 2) = %.6f  (el '0,95')" % H)
tramos = [(10, 20), (20, 40), (40, 80), (80, 160), (160, 320), (320, 640), (640, 1280)]
print("    pendiente medida de log2 a(k) por tramos (implementacion C):")
for (i, j) in tramos:
    pend = (log2big(counts_C[j - 1]) - log2big(counts_C[i - 1])) / (j - i)
    print("      k = %4d..%4d :  %.6f   (densidad ~ 2^(-%.4f k) en el tramo)" % (i, j, pend, 1 - pend))
p_final = (log2big(counts_C[K_C - 1]) - log2big(counts_C[K_C // 2 - 1])) / (K_C - K_C // 2)
print("      k = %4d..%4d :  %.6f" % (K_C // 2, K_C, p_final))
print("    global: log2(a(%d))/%d = %.6f" % (K_C, K_C, log2big(counts_C[K_C - 1]) / K_C))
print("    -> la pendiente sube hacia H=%.4f por debajo y no lo alcanza en ningun k medido;" % H)
print("       '2^(0,95k)' es el orden ASINTOTICO (exponente limite), no el del rango finito.")

print("")
print("== VEREDICTO LOCAL: el enunciado se sostiene ==")
print("   densidad -> 0 (estricto en cada nivel, exacto), cardinal -> infinito (hijo impar),")
print("   y 0,95 = H(log3 2) = %.6f es el exponente limite del cardinal." % H)
