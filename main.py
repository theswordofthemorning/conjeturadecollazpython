"""Linea de comandos para jugar con la conjetura de Collatz.

  python main.py verificar --limite 1000000
  python main.py records   --limite 10000
  python main.py graficar  --paisaje 1000 --coral 3000
  python main.py camino    27
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


def cmd_graficar(args) -> None:
    import viz3d

    if args.paisaje:
        ruta, s = _cronometrar(viz3d.paisaje, args.paisaje, mostrar=args.mostrar)
        print(f"  paisaje  -> {ruta}  ({s:.1f} s)")
    if args.coral:
        ruta, s = _cronometrar(viz3d.coral, args.coral, mostrar=args.mostrar)
        print(f"  coral    -> {ruta}  ({s:.1f} s)")


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

    g = sub.add_parser("graficar", help="genera las vistas 3D")
    g.add_argument("--paisaje", type=int, default=1000, help="semillas del paisaje (0 = omitir)")
    g.add_argument("--coral", type=int, default=3000, help="semillas del coral (0 = omitir)")
    g.add_argument("--mostrar", action="store_true", help="abre la ventana interactiva")
    g.set_defaults(func=cmd_graficar)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
