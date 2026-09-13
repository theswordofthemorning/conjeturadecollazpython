"""Regresion: un corte de calculo no es un contraejemplo de Collatz."""

from pathlib import Path
import subprocess
import sys

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
import collatz


def main():
    corto = collatz.verificar(10, tope_pasos=1)
    assert corto["estado"] == "inconcluso"
    assert corto["limite_verificado"] == 2
    assert corto["semilla_pendiente"] == 3
    assert corto["contraejemplo"] is None
    assert collatz.verificar(2, tope_pasos=1)["estado"] == "completo"
    assert collatz.verificar(1)["limite_verificado"] == 1
    completo = collatz.verificar(1001)
    assert completo["estado"] == "completo"
    assert completo["limite_verificado"] == 1001
    tabla = collatz.tabla_de_pasos(1001)
    for n in range(1, 1002):
        # Otra forma de contar: trayectoria completa, sin parada al descender.
        camino = collatz.secuencia(n)
        assert tabla[n] == len(camino) - 1
        assert collatz.altitud_maxima(n) == max(camino)
    assert tabla[27] == 111
    for llamada in (lambda: collatz.altitud_maxima(0),
                    lambda: collatz.tabla_de_pasos(0),
                    lambda: collatz.verificar(0),
                    lambda: collatz.verificar(10, 0),
                    lambda: collatz.records(0)):
        try:
            llamada()
        except ValueError:
            pass
        else:
            raise AssertionError("Una entrada fuera del dominio fue aceptada")
    cli = subprocess.run(
        [sys.executable, "-X", "utf8", str(RAIZ / "main.py"),
         "verificar", "--limite", "10", "--tope-pasos", "1"],
        capture_output=True, text=True, encoding="utf-8", check=True,
    )
    assert "inconcluso" in cli.stdout and "CONTRAEJEMPLO" not in cli.stdout
    print("OK: tope, prefijo verificado, CLI, dominio y 1001 trayectorias clasicas.")


if __name__ == "__main__":
    main()
