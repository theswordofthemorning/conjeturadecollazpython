"""
REVISION 12 -- ADVERSARIO 1, TANDA 1, ATAQUE PROPIO.
LEEME seccion 3 dice: "No implica un margen uniforme en m. La SVD
flotante da normas 0.707107 ... 0.931140 para m=2..8. Esa ventana NO
determina su limite."

Extiendo la ventana. La norma espectral de M2 M3 en media cero se
estima por iteracion de potencia sobre (M2M3)^T (M2M3), aplicando los
operadores como permutaciones en O(2^m): no se construye ninguna
matriz, asi que llega a m=20 en vez de m=8.
"""
import numpy as np

def tau(k, x, mod):
    return (3 * x - (3**k - 1) // 2) % mod

def normas(m, iters=20000, tol=1e-14):
    mod = 1 << m
    x = np.arange(mod, dtype=np.int64)
    p2 = (3 * x - 4) % mod
    p3 = (3 * x - 13) % mod
    i2 = np.empty(mod, dtype=np.int64); i2[p2] = x   # perm inversa
    i3 = np.empty(mod, dtype=np.int64); i3[p3] = x
    # A  v = M2 (M3 v),  (M_k v)[x] = (v[x] + v[perm_k[x]])/2
    A     = lambda v: (lambda w: (w + w[p2]) / 2)((v + v[p3]) / 2)
    # A^T w = M3^T (M2^T w),  (M_k^T w)[x] = (w[x] + w[inv_k[x]])/2
    At    = lambda w: (lambda u: (u + u[i3]) / 2)((w + w[i2]) / 2)
    rng = np.random.default_rng(12)
    v = rng.standard_normal(mod)
    v -= v.mean()
    v /= np.linalg.norm(v)
    prev = 0.0
    for i in range(iters):
        w = At(A(v))
        w -= w.mean()                      # media cero es invariante
        lam = np.linalg.norm(w)
        if lam == 0:
            return 0.0, i
        v = w / lam
        if abs(lam - prev) < tol * max(lam, 1e-30):
            return np.sqrt(lam), i
        prev = lam
    return np.sqrt(lam), iters

print("norma espectral de M2 M3 en media cero (iteracion de potencia)")
print("  m        norma           1 - norma      gap(m)/gap(m-1)")
prevgap = None
for m in range(2, 21):
    s, it = normas(m)
    gap = 1.0 - s
    r = ("%8.5f" % (gap / prevgap)) if prevgap else "     ---"
    print(f"  {m:2d}   {s:.12f}   {gap:.10f}   {r}   (it={it})")
    prevgap = gap
