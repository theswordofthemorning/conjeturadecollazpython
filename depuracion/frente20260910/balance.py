"""Balance exacto del exceso: paridad, salida y mezcla de corrientes.

Reutiliza el DP local ya cruzado con pares reales. No es una revision
independiente ciega. Las identidades se comparan en Fraction sin filtros;
los cocientes decimales solo se imprimen despues de la comprobacion.
"""

import argparse
import json
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations
from pathlib import Path

from contraccion import avanzar, control_pares, control_palabras, exceso


def energia(conteos, modulo):
    masa = sum(conteos.values())
    if masa == 0:
        return Fraction(0)
    return Fraction(modulo * sum(n*n for n in conteos.values()), masa*masa) - 1


def distancia(a, b, modulo):
    ma, mb = sum(a.values()), sum(b.values())
    escalar = sum(n*b.get(r, 0) for r, n in a.items())
    return (energia(a, modulo) + energia(b, modulo) + 2
            - Fraction(2*modulo*escalar, ma*mb))


def balance(estados, siguientes, m):
    modulo = 2**m
    grupos = defaultdict(Counter)
    for (k, c), peso in estados.items():
        grupos[k, c % 2][c % (2*modulo)] += peso
    masas = {clave: sum(conteo.values()) for clave, conteo in grupos.items()}
    eg = {clave: energia(conteo, modulo) for clave, conteo in grupos.items()}
    vivos = sum(masas.values())
    salida = masas.get((2, 1), 0)
    s = Fraction(salida, 2*vivos)
    vivos_hijos = 2*vivos-salida
    if sum(siguientes.values()) != vivos_hijos:
        raise SystemExit("B1: supervivencia incorrecta")

    q, r, g = Fraction(0), Fraction(0), Fraction(0)
    for k in {k for k, _ in grupos}:
        par, impar = masas.get((k, 0), 0), masas.get((k, 1), 0)
        masa = par+impar
        a, b = Fraction(par, masa), Fraction(impar, masa)
        u, v = eg.get((k, 0), 0), eg.get((k, 1), 0)
        peso = Fraction(masa, vivos)
        q += peso*(a-b)**2
        r += peso*(a-b)*(a*u-b*v)
        g += peso*(a*u+b*v)
    ep = exceso(estados, m+1)
    if ep != g+q+r:
        raise SystemExit("B2: descomposicion de paridad incorrecta")

    corrientes = defaultdict(Counter)
    for (k, paridad), conteo in grupos.items():
        for c, peso in conteo.items():
            if paridad == 0:
                corrientes[k, "N0"][(c//2) % modulo] += peso
                corrientes[k, "N1"][((3*c+1-3**k)//2) % modulo] += peso
            else:
                corrientes[k+1, "A"][((3*c+1)//2) % modulo] += peso
                if k > 2:
                    corrientes[k-1, "D"][((c-3**(k-1))//2) % modulo] += peso
    reconstruido = Counter()
    masas_corrientes = {}
    for (k, nombre), conteo in corrientes.items():
        masas_corrientes[k, nombre] = sum(conteo.values())
        fuente = (k, 0) if nombre in ("N0", "N1") else (
            (k-1, 1) if nombre == "A" else (k+1, 1))
        if (energia(conteo, modulo) != eg[fuente]
                or masas_corrientes[k, nombre] != masas[fuente]):
            raise SystemExit("B3: la corriente no conserva masa y energia de su fuente")
        for c, n in conteo.items():
            reconstruido[k, c] += n
    directo = Counter()
    for (k, c), n in siguientes.items():
        directo[k, c % modulo] += n
    if reconstruido != directo:
        raise SystemExit("B4: las cuatro corrientes no reproducen el DP")

    mezcla = Fraction(0)
    por_par = defaultdict(Fraction)
    bruto = Fraction(0)
    for k in {k for k, _ in corrientes}:
        claves = [clave for clave in corrientes if clave[0] == k]
        total = sum(masas_corrientes[clave] for clave in claves)
        entrada = sum((masas_corrientes[clave] * energia(corrientes[clave], modulo)
                       for clave in claves), Fraction(0))
        resta = Fraction(0)
        for i, j in combinations(claves, 2):
            d = distancia(corrientes[i], corrientes[j], modulo)
            if d < 0:
                raise SystemExit("B5: distancia negativa")
            aporte = Fraction(masas_corrientes[i]*masas_corrientes[j], total)*d
            resta += aporte
            por_par[tuple(sorted((i[1], j[1])))] += aporte/(2*vivos)
        hija = Counter()
        for clave in claves:
            hija.update(corrientes[clave])
        if total*energia(hija, modulo) != entrada-resta:
            raise SystemExit("B6: identidad de varianza incorrecta")
        bruto += entrada
        mezcla += resta
    e_salida = eg.get((2, 1), Fraction(0))
    if bruto != 2*vivos*g-salida*e_salida:
        raise SystemExit("B7: energia descartada incorrecta")
    delta = mezcla/(2*vivos)
    eh = exceso(siguientes, m)
    if (1-s)*eh != ep-q-r-s*e_salida-delta:
        raise SystemExit("B8: balance global incorrecto")
    margen = delta+q+r+s*e_salida-Fraction(1+s, 2)*ep
    if margen != (1-s)*(ep/2-eh):
        raise SystemExit("B9: umbral incorrecto")
    return {"ep": ep, "eh": eh, "s": s, "q": q, "r": r,
            "salida": s*e_salida, "delta": delta, "margen": margen,
            "n0n1": por_par.get(("N0", "N1"), Fraction(0))}


def controles():
    casos = 0
    for m in range(1, 6):
        n = 2**m
        uniformes = Counter({(k, c): k-1 for k in range(2, 6) for c in range(2*n)})
        todo_par = Counter({(2, 2*r): 1 for r in range(n)})
        todo_impar = Counter({(2, 2*r+1): 1 for r in range(n)})
        sesgado = Counter({(2, 0): n, **{(2, 2*r+1): 3 for r in range(n)}})
        for estados in (uniformes, todo_par, todo_impar, sesgado):
            siguientes, _ = avanzar(estados)
            b = balance(estados, siguientes, m)
            if estados == uniformes and (b["ep"] != 0 or b["eh"] != 0):
                raise SystemExit("El piso uniforme no se conserva")
            casos += 1
        if m == 2:
            if (b["ep"], b["eh"], b["s"]) != (Fraction(5, 8), Fraction(6, 5), Fraction(3, 8)):
                raise SystemExit("El testigo sintetico no coincide")
            print("TESTIGO SINTETICO k=2, m=2: n(0)=4; n(1)=n(3)=n(5)=n(7)=3.")
            print(f"  e_padre={b['ep']}, e_hija={b['eh']}, rho={b['eh']/b['ep']}; "
                  f"s={b['s']}, Q={b['q']}, R={b['r']}, Delta={b['delta']}.")
            print("  Ley arbitraria: no se afirma que sea alcanzable desde una semilla.")
    print(f"CONTROLES: {casos} leyes sinteticas, incluyendo grupos vacios y piso cero: OK.")
    equilibrado = Counter({(2, 0): 1, (2, 1): 1})
    siguientes, _ = avanzar(equilibrado)
    b = balance(equilibrado, siguientes, 2)
    if (b["ep"], b["eh"], b["q"], b["r"], b["delta"]) != (3, 3, 0, 0, 0):
        raise SystemExit("El testigo con paridad equilibrada no coincide")
    print("TESTIGO EQUILIBRADO k=2, m=2: n(0)=n(1)=1; e_padre=e_hija=3;")
    print("  Q=R=Delta=0: equilibrar la paridad no basta. Ley sintetica, no orbita.")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--tiempos", type=int, nargs="+", default=[8, 12, 16, 20])
    p.add_argument("--m-min", type=int, default=1)
    p.add_argument("--m-max", type=int, default=10)
    p.add_argument("--semillas", type=int, nargs="+", default=[1, 5, 999983, 999999937, 1398101])
    p.add_argument("--registro", help="JSON de cada celda, con numeradores y denominadores exactos")
    args = p.parse_args()
    if min(args.tiempos) < 0 or not 1 <= args.m_min <= args.m_max:
        p.error("Rangos invalidos")
    control_pares()
    controles()
    print("COLUMNAS: rho; s; Q/e; R/e; salida/e; Delta/e; margen/e; cuota N0-N1 de Delta.")
    celdas, fallos = 0, 0
    rangos = {}
    testigos = {}
    registro = []
    for semilla in args.semillas:
        estados, absorbidas = Counter({(2, semilla): 1}), 0
        for t in range(max(args.tiempos)+1):
            if sum(estados.values())+absorbidas != 2**t:
                raise SystemExit("No se conserva la masa total")
            if t == 8:
                control_palabras(semilla, t, estados)
            siguientes, salidas = avanzar(estados)
            if t in args.tiempos:
                for m in range(args.m_min, args.m_max+1):
                    b = balance(estados, siguientes, m)
                    if args.registro:
                        registro.append({"c0": semilla, "t": t, "m": m,
                                         **{k: {"num": v.numerator, "den": v.denominator}
                                            for k, v in b.items()}})
                    celdas += 1
                    if b["ep"] == 0:
                        if b["eh"] != 0:
                            raise SystemExit("Exceso creado desde el piso")
                        continue
                    rho = b["eh"]/b["ep"]
                    fallos += rho >= Fraction(1, 2)
                    for nombre in ("q", "r", "salida", "delta", "margen"):
                        valor = b[nombre]/b["ep"]
                        minimo, maximo = rangos.get(nombre, (valor, valor))
                        abajo, arriba = testigos.get(nombre, ((semilla, t, m), (semilla, t, m)))
                        testigos[nombre] = ((semilla, t, m) if valor < minimo else abajo,
                                            (semilla, t, m) if valor > maximo else arriba)
                        rangos[nombre] = min(minimo, valor), max(maximo, valor)
                    if m == min(8, args.m_max):
                        cuota = b["n0n1"]/b["delta"] if b["delta"] else Fraction(0)
                        valores = [rho, b["s"], *(b[n]/b["ep"] for n in
                                   ("q", "r", "salida", "delta", "margen")), cuota]
                        print(f"c0={semilla} t={t} m={m}: "
                              + " ".join(f"{float(v):.6f}" for v in valores), flush=True)
            estados, absorbidas = siguientes, 2*absorbidas+salidas
    print(f"FIN: {celdas} balances exactos; {fallos} cruces de rho >= 1/2.")
    for nombre, (minimo, maximo) in rangos.items():
        print(f"  {nombre}/e en [{float(minimo):.6f}, {float(maximo):.6f}]; "
              f"testigos (c0,t,m)={testigos[nombre]}.")
    if args.registro:
        Path(args.registro).write_text(json.dumps({"parametros": vars(args), "celdas": registro},
                                                 indent=2) + "\n", encoding="utf-8")
    print("Identidades comprobadas; margenes medidos, sin teorema de contraccion ni revision ciega.")


if __name__ == "__main__":
    main()
