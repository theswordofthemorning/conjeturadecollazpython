"""Reparte un modulo de hojas por coste del subarbol; Lean vuelve a probar todo.

Lee una salida de generar_prefijos_lean.py --hojas-por-modulo. Conserva
los nombres publicos, subdivide las hojas costosas y emite modulos de
partes mas un ensamblaje. El coste solo orienta la particion.
"""

import argparse
from pathlib import Path
import re


def terminal(estado):
    L, Q, R, r, m, a, c, q, s, anterior, F = estado
    if F == 0:
        raise ValueError("Combustible insuficiente")
    if r > L:
        return True
    if a < m:
        if c >= r:
            raise ValueError("Clase sin descenso certificado")
        return True
    if s > R:
        return True
    if not anterior:
        M = (a * ((L - r) // m) + c + 1).bit_length()
        C = 0
        for _ in range(R - s):
            C = (5 * M + 8 * C - 1) // 5
        return q + C < Q
    return False


def hijos(estado):
    L, Q, R, r, m, a, c, q, s, anterior, F = estado
    for b in (0, 1):
        x = a * b + c
        impar = x % 2 == 1
        yield (L, Q, R, r + m * b, 2 * m, 3 * a if impar else a,
               (3 * x + 1) // 2 if impar else x // 2,
               q + impar, s + (impar and not anterior), impar, F - 1)


def coste_acotado(estado, limite):
    pila = [estado]
    cantidad = 0
    while pila:
        actual = pila.pop()
        cantidad += 1
        if cantidad > limite:
            return None
        if not terminal(actual):
            pila.extend(hijos(actual))
    return cantidad


def cabecera(nombre, estado):
    parametros = [str(x) for x in estado]
    parametros[-2] = "true" if estado[-2] else "false"
    return f"theorem {nombre} : comprobar {' '.join(parametros)} = true := by"


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--origen", type=Path, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    analizador.add_argument("--nodos-hoja", type=int, required=True)
    analizador.add_argument("--nodos-modulo", type=int, required=True)
    argumentos = analizador.parse_args()
    assert 1 <= argumentos.nodos_hoja <= argumentos.nodos_modulo
    texto = argumentos.origen.read_text(encoding="utf-8")
    espacio = re.search(r"namespace (Ocelotas\w+)", texto).group(1)
    patron = (r"namespace (Bajo|Alto)\n(theorem (nodo_\d+) : comprobar "
              r"([^\n]+) = true := by\n  decide \+kernel)\nend \1")
    originales = list(re.finditer(patron, texto))
    assert originales and len(originales) == texto.count("theorem ")
    hojas, ensamblaje, raices = [], [], []

    def visitar(rama, nombre, estado):
        coste = coste_acotado(estado, argumentos.nodos_hoja)
        if coste is not None:
            hojas.append((rama, nombre, cabecera(nombre, estado) + "\n  decide +kernel", coste))
        else:
            for b, hijo in enumerate(hijos(estado)):
                visitar(rama, nombre + f"_h{b}", hijo)
            prueba = [cabecera(nombre, estado),
                      "  exact acepta_rama (by decide +kernel) (by decide +kernel)",
                      "    (by decide +kernel) (by decide +kernel)",
                      f"    {nombre}_h0 {nombre}_h1"]
            ensamblaje.append((rama, "\n".join(prueba)))

    for m in originales:
        rama, _, nombre, parametros = m.groups()
        valores = parametros.split()
        assert len(valores) == 11 and valores[-2] in ("true", "false")
        estado = tuple(int(v) if j != 9 else v == "true" for j, v in enumerate(valores))
        raices.append((rama, nombre))
        visitar(rama, nombre, estado)

    grupos, grupo, carga = [], [], 0
    for hoja in hojas:
        if grupo and (carga + hoja[3] > argumentos.nodos_modulo or len(grupo) >= 64):
            grupos.append(grupo)
            grupo, carga = [], 0
        grupo.append(hoja)
        carga += hoja[3]
    if grupo:
        grupos.append(grupo)
    preambulo = [f"namespace {espacio}",
                "open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques",
                "set_option maxRecDepth 100000", "set_option maxHeartbeats 0", ""]
    modulos = []
    for j, grupo in enumerate(grupos, 1):
        modulo = argumentos.salida.stem + f"Parte{j:02d}"
        modulos.append(modulo)
        lineas = ["import OcelotasPrefijosBloques", "",
                  "/-! Particion por coste; cada hoja se comprueba en el nucleo. -/"] + preambulo
        for rama, nombre, prueba, coste in grupo:
            lineas.extend([f"namespace {rama}", prueba, f"end {rama}", ""])
        lineas.append(f"end {espacio}")
        for rama, nombre, _, _ in grupo:
            lineas.append(f"#print axioms {espacio}.{rama}.{nombre}")
        argumentos.salida.with_name(modulo + ".lean").write_text("\n".join(lineas) + "\n", encoding="utf-8")
        print(f"{modulo}: {len(grupo)} hojas, {sum(h[3] for h in grupo)} nodos.")
    lineas = ["import " + modulo for modulo in modulos] + [""] + preambulo
    for rama, prueba in ensamblaje:
        lineas.extend([f"namespace {rama}", prueba, f"end {rama}", ""])
    lineas.append(f"end {espacio}")
    for rama, nombre in raices:
        lineas.append(f"#print axioms {espacio}.{rama}.{nombre}")
    argumentos.salida.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print(f"{len(raices)} raices; {len(hojas)} hojas; {len(ensamblaje)} uniones; {len(modulos)} modulos.")


if __name__ == "__main__":
    main()
