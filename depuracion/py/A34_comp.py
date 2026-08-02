# Comparador A34: recalculo independiente de la criba de descenso (mapa del ATAJO)
# superviviente r mod 2^k  <=>  3^{s_j} >= 2^j para todo j <= k
import math

def a_directo(k):
    cnt = 0
    for r in range(2**k):
        v = r; s = 0; vivo = True
        for j in range(1, k+1):
            if v & 1:
                v = (3*v+1)//2; s += 1
            else:
                v //= 2
            if 3**s < 2**j:
                vivo = False; break
        if vivo: cnt += 1
    return cnt

prefijo = [a_directo(k) for k in range(1, 17)]
print("a(1..16) =", prefijo)
print("a(12) =", prefijo[11], " a(13) =", prefijo[12], " a(16) =", prefijo[15])

# conteo combinatorio por vectores de paridad (dinamica sobre (j, s)) hasta k grande
def a_comb(kmax):
    # estados: numero de vectores de longitud j con conteo de unos s y todos los prefijos vivos
    from collections import defaultdict
    est = {0: 1}  # s -> conteo, j = 0
    res = []
    for j in range(1, kmax+1):
        nuevo = defaultdict(int)
        for s, c in est.items():
            for b in (0, 1):
                s2 = s + b
                if 3**s2 >= 2**j:
                    nuevo[s2] += c
        est = dict(nuevo)
        res.append(sum(est.values()))
    return res

serie = a_comb(400)
print("comb a(1..16) =", serie[:16], "coincide:", serie[:16] == prefijo)
print("a(22) =", serie[21])
al2 = math.log2
print("log2(a(k))/k:  k=12:", round(al2(serie[11])/12,4),
      " k=16:", round(al2(serie[15])/16,4),
      " k=100:", round(al2(serie[99])/100,4),
      " k=400:", round(al2(serie[399])/400,4))
# pendiente por tramo 200..400
print("pendiente 200..400:", round((al2(serie[399])-al2(serie[199]))/200, 4))

alpha = math.log(2)/math.log(3)
H = -alpha*al2(alpha) - (1-alpha)*al2(1-alpha)
print("alpha = log_3 2 =", round(alpha,6), "  H(alpha) =", round(H,6))

# monotonia y densidad
assert all(serie[i+1] <= 2*serie[i] for i in range(len(serie)-1)), "densidad crece"
assert all(serie[i] <= serie[i+1] for i in range(len(serie)-1)), "cardinal decrece"
print("a(k+1) <= 2a(k) y a(k) <= a(k+1) en k=1..399: OK")
# borde: 2^k - 1 sobrevive (racha de impares)
for k in (5, 10, 16):
    v = 2**k - 1; s = 0; vivo = True
    for j in range(1, k+1):
        if v & 1: v = (3*v+1)//2; s += 1
        else: v //= 2
        if 3**s < 2**j: vivo = False; break
    print(f"2^{k}-1 sobrevive:", vivo)
