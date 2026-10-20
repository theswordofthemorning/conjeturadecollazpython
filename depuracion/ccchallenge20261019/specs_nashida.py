"""Escribe G y sus debilitadas G_Ak, G_Bk en el formato de Nashida.

Formato (a confirmar leyendo classify_families.py): "r:A,b,e;..." con
modulo 2^k; el resto r se manda a (A*z + b) / 2^e y los restos que no
salen paran. Se comprueba cada spec contra la definicion directa en
todo z < 2^12.

  G(2m) = 3m, G(8m+7) = 9m+8, parar en el resto.
  G_Ak  rama A solo si z != 0 mod 2^k   (k = 2, 3, 4, 5)
  G_Bk  rama B solo si z != -1 mod 2^k  (k = 4, 5, 6, 7)
"""

import json


def directa(z, ka=None, kb=None):
    if z % 2 == 0 and (ka is None or z % 2**ka != 0):
        return 3 * z // 2
    if z % 8 == 7 and (kb is None or z % 2**kb != 2**kb - 1):
        return (9 * z + 1) // 8
    return None


def spec(ka=None, kb=None):
    k = max(3, ka or 0, kb or 0)
    piezas = []
    for r in range(2**k):
        if r % 2 == 0 and (ka is None or r % 2**ka != 0):
            piezas.append((r, 3, 0, 1))
        elif r % 8 == 7 and (kb is None or r % 2**kb != 2**kb - 1):
            piezas.append((r, 9, 1, 3))
    return k, piezas


def aplicar(k, piezas, z):
    for r, a, b, e in piezas:
        if z % 2**k == r:
            return (a * z + b) // 2**e
    return None


sistemas = {"G": (None, None)}
sistemas.update({f"G_A{k}": (k, None) for k in (2, 3, 4, 5)})
sistemas.update({f"G_B{k}": (None, k) for k in (4, 5, 6, 7)})

salida = {}
for nombre, (ka, kb) in sistemas.items():
    k, piezas = spec(ka, kb)
    for z in range(1, 2**12):
        assert aplicar(k, piezas, z) == directa(z, ka, kb), (nombre, z)
    texto = ";".join(f"{r}:{a},{b},{e}" for r, a, b, e in piezas)
    salida[nombre] = {"k": k, "spec": texto}
    print(f"{nombre}  k={k}  {texto}")

with open("specs_nashida.json", "w", encoding="utf-8") as f:
    json.dump(salida, f, indent=1)
