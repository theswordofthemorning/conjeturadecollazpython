"""Ensayo de dos familias singulares explicitas, con vectores naturales sin cota."""

import argparse
from hashlib import sha256
import json
from pathlib import Path

import z3

from buscar_constantes_libres import codificar, leer_reglas, verificar_modelo


def familia(nombre, binaria, ternaria):
    cero = [[0, 0], [0, 0]]
    identidad = [[1, 0], [0, 1]]
    if nombre == "imagen_comun":
        a = [[binaria, 0], [binaria, 0]]
        b = [[0, binaria], [0, binaria]]
        e = [[ternaria, 0], [ternaria, 0]]
        f = [[ternaria, 0], [0, ternaria]]
        g = [[0, ternaria], [0, ternaria]]
    else:
        assert nombre == "nucleo_comun"
        a = [[binaria, binaria], [0, 0]]
        b = [[0, 0], [binaria, binaria]]
        e = [[ternaria, 0], [0, ternaria]]
        f = [[0, ternaria], [ternaria, 0]]
        g = [[ternaria, 0], [0, ternaria]]
    return dict(a=a, b=b, c=cero, e=e, f=f, g=g)


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--sistema", type=Path, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    args = analizador.parse_args()
    reglas = leer_reglas(args.sistema)
    casos = []
    for nombre in ("imagen_comun", "nucleo_comun"):
        for binaria in (1, 2, 3):
            for ternaria in range(1, binaria + 1):
                solver, simbolos, _ = codificar(reglas, 3, "ambas", 5)
                fijadas = familia(nombre, binaria, ternaria)
                for s, matriz in fijadas.items():
                    for i in range(2):
                        for j in range(2):
                            solver.add(simbolos[s][0][i][j] == matriz[i][j])
                estado = solver.check()
                caso = dict(familia=nombre, binaria=binaria, ternaria=ternaria,
                            estado=str(estado), primera_fila_d="natural 0..3",
                            constantes="naturales sin cota")
                if estado == z3.sat:
                    modelo = solver.model()
                    valor = lambda x: modelo.eval(x, model_completion=True).as_long()
                    concretos = {s: ([[valor(x) for x in fila] for fila in m],
                                     [valor(x) for x in v]) for s, (m, v) in simbolos.items()}
                    caso["estrictas"] = verificar_modelo(reglas, concretos)
                    caso["simbolos"] = concretos
                elif estado == z3.unknown:
                    caso["motivo"] = solver.reason_unknown()
                casos.append(caso)
                print(nombre, binaria, ternaria, estado, flush=True)
    datos = dict(casos=casos, version_z3=z3.get_version_string(), semilla=0, hilos=1,
                 limite_segundos_por_caso=5,
                 fuente_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                 codificador_sha256=sha256(Path(__file__).with_name("buscar_constantes_libres.py").read_bytes()).hexdigest(),
                 sistema_sha256=sha256(args.sistema.read_bytes()).hexdigest(),
                 alcance="Ensayo finito de parametros matriciales con constantes sin cota. "
                         "No clasifica todas las familias singulares ni certifica UNSAT en Lean.")
    args.salida.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
