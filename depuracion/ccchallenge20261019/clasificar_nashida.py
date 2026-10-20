"""Clasifica G, su escalera y las ramas sueltas con el clasificador de Nashida.

Uso (desde fuera del clon de Nashida, que es codigo de terceros):
    python -I -B -X utf8 clasificar_nashida.py CLASSIFY_FAMILIES.py SPECS_NASHIDA.json [SALIDA.txt]

CLASSIFY_FAMILIES.py es computations/classify_families.py del repo
harappa/collatz-termination-certificate-dichotomy (commit a138adb). Se
carga por su ruta y se usan sus funciones (parse, comp_kinds, categorize,
certificate, check_certificate). Este guion solo lee; si se da SALIDA,
escribe ahi lo mismo que sale en pantalla.

  1. Los 9 sistemas de specs_nashida.json y las dos ramas sueltas
     (peldanos 3 y 4 de la escalera, que YAH y AProVE si probaron). Las
     8 debilitadas se cotejan tambien con funcion() de
     ../judas20261016/escalera/yah/debilitar.py.
  2. Si el veredicto cambia al leer el mapa modulo 2^k mayor (hasta 2^10).
  3. Debilitadas de una clase: G parando ademas en un solo resto mod 2^k
     (hasta 2^12). Usa un criterio rapido que vale porque las dos ramas de
     G expanden; hasta 2^7 se coteja con comp_kinds.
  4. Las dos debilitaciones a la vez: parar en 0 mod 2^a y en -1 mod 2^b.
  5. Las desenredadas de 3 y 4: si terminan y si su certificado
     escalonado pasa chk1-chk4 (en Python, no en Lean).
"""

import hashlib
import importlib.util
import json
import math
import os
import sys
from collections import deque

sys.dont_write_bytecode = True

DEBILITAR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "judas20261016",
                         "escalera", "yah", "debilitar.py")

lineas = []


def decir(texto=""):
    print(texto)
    lineas.append(texto)


def cargar(ruta, nombre="classify_families"):
    modulo = importlib.util.spec_from_file_location(nombre, ruta)
    cf = importlib.util.module_from_spec(modulo)
    modulo.loader.exec_module(cf)
    return cf


def directa(z, nombre):
    """Un paso del sistema escrito a mano (None = para)."""
    ka = int(nombre[3:]) if nombre.startswith("G_A") else None
    kb = int(nombre[3:]) if nombre.startswith("G_B") else None
    rama_a = nombre != "rama_B"
    rama_b = nombre != "rama_A"
    if rama_a and z % 2 == 0 and (ka is None or z % 2**ka != 0):
        return 3 * z // 2
    if rama_b and z % 8 == 7 and (kb is None or z % 2**kb != 2**kb - 1):
        return (9 * z + 1) // 8
    return None


def mapa(cf, k, para_en=(), a=None, b=None):
    """G modulo 2^k, parando ademas en los restos de para_en, en 0 mod 2^a
    y en -1 mod 2^b."""
    br = []
    for r in range(2**k):
        if r in para_en:
            br.append(None)
        elif r % 2 == 0 and (a is None or r % 2**a != 0):
            br.append((3, 0, 1))
        elif r % 8 == 7 and (b is None or r % 2**b != 2**b - 1):
            br.append((9, 1, 3))
        else:
            br.append(None)
    return cf.GMap(k, br)


def refinar(cf, g, k2):
    """El mismo mapa leido modulo 2^k2."""
    return cf.GMap(k2, [g.br[r % g.m] for r in range(2**k2)], g.name)


def ciclo_corto(comp, adj):
    """El ciclo mas corto dentro de la componente."""
    cs = set(comp)
    mejor = None
    for v in sorted(comp):
        previo = {v: None}
        cola = deque([v])
        cierre = None
        while cola and cierre is None:
            u = cola.popleft()
            for t in adj[u]:
                if t not in cs:
                    continue
                if t == v:
                    cierre = u
                    break
                if t not in previo:
                    previo[t] = u
                    cola.append(t)
        if cierre is None:
            continue
        camino = [cierre]
        while camino[-1] != v:
            camino.append(previo[camino[-1]])
        camino.reverse()
        if mejor is None or len(camino) < len(mejor):
            mejor = camino
        if len(mejor) == 1:
            break
    return mejor


def factor(g, ciclo):
    """Lo que multiplica una vuelta al ciclo: producto de A / 2^e."""
    num, den = 1, 1
    for s in ciclo:
        A, _, e = g.br[s]
        num *= A
        den *= 2**e
    return f"{num}/{den}"


def enredado_rapido(cf, g):
    """Enredo cuando todas las ramas expanden (A > 2^e), como en G: todo
    ciclo expande y basta ver si alguna componente fuerte tiene un resto
    con dos salidas dentro de ella."""
    nodos, adj = cf.graph(g)
    for comp in cf.tarjan(nodos, adj):
        cs = set(comp)
        if max(sum(1 for t in adj[v] if t in cs) for v in comp) >= 2:
            return True
    return False


def describir(cf, g):
    """Las componentes con ciclo: tipo, tamano, restos que ramifican, ciclo
    mas corto y, si es un ciclo simple, sus puntos periodicos."""
    comps, adj, kinds = cf.comp_kinds(g)
    for comp, kd in zip(comps, kinds):
        if kd == "TRIV":
            continue
        cs = set(comp)
        ramifican = [v for v in comp if sum(1 for t in adj[v] if t in cs) >= 2]
        ciclo = ciclo_corto(comp, adj)
        mcm = cf.max_cycle_mean(g, comp, adj)
        decir(f"   componente {kd}: {len(comp)} restos, {len(ramifican)} ramifican, "
              f"ciclo mas corto {ciclo} (x{factor(g, ciclo)}), "
              f"media max. por paso x{math.exp(mcm):.4f}")
        if ramifican:
            v = min(ramifican)
            decir(f"      ejemplo: {v} -> {[t for t in adj[v] if t in cs]} dentro de la componente")
        if kd == "EXP1":
            puntos, _ = cf.periodic_points(g, cf.cycle_of(comp, adj))
            decir(f"      ciclo simple {cf.cycle_of(comp, adj)}, "
                  f"puntos periodicos {[str(p) for p in puntos]}")


def certificar(cf, g):
    cert = cf.certificate(g)
    ok = cert is not None and cf.check_certificate(g, cert)
    if cert is None:
        decir("   certificado escalonado: NO SE CONSTRUYE")
        return
    tipos = sorted({cert["kind"][l] for l in set(cert["lvl"]) if l})
    decir(f"   certificado escalonado: {'pasa chk1-chk4' if ok else 'FALLA'}; "
          f"tipos de etapa {tipos}, E={cert['E']}, N0={cert['N0']}, B={cert['B']}")


def main(argv):
    ruta_cf, ruta_specs = argv[0], argv[1]
    salida = argv[2] if len(argv) > 2 else None
    with open(ruta_cf, "rb") as fh:
        huella = hashlib.sha256(fh.read()).hexdigest()
    cf = cargar(ruta_cf)
    # debilitar.py no tiene efectos al importarlo: main() solo corre como programa.
    deb = cargar(DEBILITAR, "debilitar")
    with open(ruta_specs, encoding="utf-8") as fh:
        sistemas = json.load(fh)
    sistemas["rama_A"] = {"k": 3, "spec": "0:3,0,1;2:3,0,1;4:3,0,1;6:3,0,1"}
    sistemas["rama_B"] = {"k": 3, "spec": "7:9,1,3"}

    decir(f"classify_families.py SHA-256 {huella}")
    decir(f"Python {sys.version.split()[0]}")
    decir("Categorias de Nashida: INF = enredado (open: sin ciclo ni escape de z <= 500")
    decir("en 5000 pasos); FIN-term = desenredado y termina (exp-noup: un ciclo")
    decir("expansivo; exp-up: ciclos expansivos en serie).")
    decir("En estos mapas el veredicto enredado es exacto, sin coma flotante: las dos")
    decir("ramas expanden (3 > 2^1, 9 > 2^3), todo ciclo expande y basta un resto con")
    decir("dos salidas dentro de una componente fuerte (el 'ejemplo' de cada una).")

    decir("\n1. Clasificacion. Cada spec coincide en 1 <= z < 2^12 con la definicion")
    decir("   directa y, en las 8 debilitadas, con funcion() de debilitar.py")
    for nombre, d in sistemas.items():
        g = cf.parse(d["k"], d["spec"], nombre)
        assert g.positive(), nombre
        assert all(g.step(z) == directa(z, nombre) for z in range(1, 2**12)), nombre
        if nombre[:3] in ("G_A", "G_B"):
            g_deb = deb.funcion(nombre[2], int(nombre[3:]))
            assert all(g.step(z) == g_deb(z) for z in range(1, 2**12)), nombre
        cat, _ = cf.categorize(g)
        decir(f"\n{nombre}  k={d['k']}  categoria: {cat}")
        describir(cf, g)
        if cat.startswith("FIN-term"):
            certificar(cf, g)

    decir("\n2. Veredicto al leer el mapa modulo 2^k mayor (comp_kinds hasta 2^10)")
    decir("   E = enredado, D = desenredado")
    for nombre, d in sistemas.items():
        g = cf.parse(d["k"], d["spec"], nombre)
        fila = []
        for k2 in range(d["k"], 11):
            fila.append("E" if "INF" in cf.comp_kinds(refinar(cf, g, k2))[2] else "D")
        decir(f"   {nombre:7s} k={d['k']}..10: {' '.join(fila)}")

    decir("\n3. Debilitadas de una clase: G parando ademas en un solo resto r mod 2^k")
    libres_por_k = {}
    for k2 in range(3, 13):
        base = mapa(cf, k2)
        activos = [r for r in range(base.m) if base.br[r] is not None]
        libres = []
        for r in activos:
            br = list(base.br)
            br[r] = None
            h = cf.GMap(k2, br)
            rapido = enredado_rapido(cf, h)
            if k2 <= 7:
                assert rapido == ("INF" in cf.comp_kinds(h)[2]), (k2, r)
            if not rapido:
                libres.append(r)
        libres_por_k[k2] = libres
        decir(f"   mod 2^{k2:<2d}: {len(activos):4d} restos posibles, "
              f"desenredadas: {libres or 'ninguna'}")
    decir("   (hasta 2^7 el criterio rapido coincide con comp_kinds en cada caso)")

    decir("\n4. Las dos debilitaciones a la vez: parar en 0 mod 2^a y en -1 mod 2^b")
    pares_libres = []
    for a in range(2, 7):
        fila = []
        for b in range(4, 9):
            h = mapa(cf, max(a, b), a=a, b=b)
            if enredado_rapido(cf, h):
                fila.append("E")
            else:
                fila.append("D")
                pares_libres.append((a, b))
        decir(f"   a={a}: b=4..8 -> {' '.join(fila)}")

    decir("\n5. Las desenredadas de 3 y 4: terminacion y certificado escalonado")
    casos = []
    for k2, libres in libres_por_k.items():
        for r in libres:
            casos.append((f"G + parar en {r} mod {2**k2}", mapa(cf, k2, para_en=(r,))))
    for a, b in pares_libres:
        casos.append((f"G_A{a} y G_B{b} a la vez", mapa(cf, max(a, b), a=a, b=b)))
    for nombre, g in casos:
        cat, _ = cf.categorize(g)
        decir(f"\n{nombre}  k={g.k}  categoria: {cat}")
        describir(cf, g)
        if cat.startswith("FIN-term"):
            certificar(cf, g)

    if salida:
        with open(salida, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lineas) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
