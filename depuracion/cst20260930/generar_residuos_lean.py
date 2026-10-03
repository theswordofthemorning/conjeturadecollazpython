"""Divide el certificado finito en bloques evaluados por decide +kernel.

Python propone estados y una particion binaria; acepta_rama recompone la
particion en Lean. Ningun resultado del censo se usa como una premisa.
"""

import argparse
from pathlib import Path


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--limite", type=int, required=True)
    analizador.add_argument("--combustible", type=int, required=True)
    analizador.add_argument("--profundidad", type=int, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    L, F, D = argumentos.limite, argumentos.combustible, argumentos.profundidad
    assert L >= 2 and 0 <= D < F
    lineas = ["import OcelotasResiduos", "",
              "/-! Generado por generar_residuos_lean.py. Cada bloque se evalúa en el núcleo. -/",
              "namespace OcelotasResiduosBloques", "open OcelotasResiduos", "",
              "set_option maxRecDepth 100000", "set_option maxHeartbeats 0", ""]
    nodos, bloques = 0, 0

    def visitar(r, m, a, c, k):
        nonlocal nodos, bloques
        identificador = nodos
        nodos += 1
        cabecera = (f"theorem nodo_{identificador} : comprobar {L} {r} {m} {a} {c} "
                    f"{F - k} = true := by")
        if k == D or a < m or r + m > L:
            lineas.extend([cabecera, "  decide +kernel", ""])
            if k == D and a >= m:
                bloques += 1
                if bloques % 16 == 0:
                    lineas.extend([f"#print axioms nodo_{identificador}", ""])
        else:
            hijos = []
            for b in (0, 1):
                x = a * b + c
                hijos.append(visitar(r + m * b, 2 * m,
                                     3 * a if x % 2 else a,
                                     (3 * x + 1) // 2 if x % 2 else x // 2, k + 1))
            lineas.extend([cabecera,
                "  exact acepta_rama (by decide) (by decide) (by decide)",
                f"    nodo_{hijos[0]} nodo_{hijos[1]}", ""])
        return identificador

    visitar(2, 1, 1, 2, 0)
    lineas.extend([f"theorem intervalo_comprobado : intervalo {L} {F} = true := nodo_0", "",
                   "end OcelotasResiduosBloques", "",
                   "#print axioms OcelotasResiduosBloques.intervalo_comprobado"])
    argumentos.salida.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print(f"{nodos} nodos; {bloques} bloques pendientes a profundidad {D}.")


if __name__ == "__main__":
    main()
