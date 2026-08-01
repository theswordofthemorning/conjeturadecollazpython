"""Linea de comandos para jugar con la conjetura de Collatz.

  python main.py verificar --limite 1000000
  python main.py records   --limite 10000
  python main.py camino    27

El subcomando `graficar` se retiro el 01-08-2026 junto con viz3d.py: aquellas
vistas 3D no tenian ni una comprobacion y arrastraban la proporcion de Harriss
invertida. Lo que dibujaban -- la altura sobre una esfera -- ya estaba medido y
era ruido: la correlacion entre latitud y log2(valor) es 0,12.
"""

from __future__ import annotations

import argparse
import time

import collatz


def _cronometrar(fn, *args, **kwargs):
    inicio = time.perf_counter()
    resultado = fn(*args, **kwargs)
    return resultado, time.perf_counter() - inicio


def cmd_verificar(args) -> None:
    informe, segundos = _cronometrar(collatz.verificar, args.limite)
    semilla, techo = informe["mayor_altitud"]

    print(f"\n  Verificacion de Collatz para n = 1 … {informe['limite']:,}")
    print(f"  {'-' * 52}")
    if informe["contraejemplo"] is None:
        print(f"  resultado          : sin contraejemplos")
    else:
        print(f"  resultado          : CONTRAEJEMPLO en n = {informe['contraejemplo']:,}")
    print(f"  pasos de descenso  : {informe['pasos_de_descenso']:,}")
    print(f"  mayor altitud      : n = {semilla:,} llega a {techo:,}")
    print(f"  tiempo             : {segundos:.2f} s\n")
    print("  Ojo: esto no demuestra nada. Solo dice que hasta aqui no se rompio.\n")


def cmd_records(args) -> None:
    datos, segundos = _cronometrar(collatz.records, args.limite)
    semilla, pasos = datos["mas_pasos"]

    print(f"\n  Records para n = 1 … {args.limite:,}   ({segundos:.2f} s)")
    print(f"  {'-' * 52}")
    print(f"  trayectoria mas larga: n = {semilla:,} con {pasos:,} pasos\n")

    print("  Records sucesivos de longitud")
    for n, p in datos["records_de_longitud"][-8:]:
        print(f"    n = {n:>9,}   {p:>4,} pasos")
    print("\n  Records sucesivos de altitud")
    for n, techo in datos["records_de_altitud"][-8:]:
        print(f"    n = {n:>9,}   sube hasta {techo:>18,}")
    print()


def cmd_camino(args) -> None:
    camino = collatz.secuencia(args.n)
    print(f"\n  n = {args.n}: {len(camino) - 1} pasos, techo {max(camino):,}\n")
    for i in range(0, len(camino), 10):
        print("   " + " -> ".join(f"{v:,}" for v in camino[i:i + 10]))
    print()


def main() -> None:
    p = argparse.ArgumentParser(description="Laboratorio de la conjetura de Collatz")
    sub = p.add_subparsers(dest="comando", required=True)

    v = sub.add_parser("verificar", help="busca contraejemplos hasta un limite")
    v.add_argument("--limite", type=int, default=1_000_000)
    v.set_defaults(func=cmd_verificar)

    r = sub.add_parser("records", help="semillas que baten records")
    r.add_argument("--limite", type=int, default=10_000)
    r.set_defaults(func=cmd_records)

    c = sub.add_parser("camino", help="imprime la trayectoria de una semilla")
    c.add_argument("n", type=int)
    c.set_defaults(func=cmd_camino)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
