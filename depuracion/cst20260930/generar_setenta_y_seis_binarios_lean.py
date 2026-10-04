"""Genera una segunda cadena de 76 usando el certificado por biseccion.

Conserva las fuentes de la evaluacion original que sigue en marcha.
Las obligaciones numericas proceden del generador de tabla original;
solo cambian los nombres y el modulo que certifica la ventana.
"""

import argparse
from pathlib import Path
import re
import subprocess
import sys
import tempfile


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--certificado", type=Path, required=True)
    analizador.add_argument("--directorio", type=Path, required=True)
    argumentos = analizador.parse_args()
    carpeta = Path(__file__).resolve().parent
    assert argumentos.directorio.is_dir()
    with tempfile.TemporaryDirectory(prefix="ocelotas_tabla_binaria_") as temporal:
        destino = Path(temporal)
        subprocess.run([
            sys.executable, "-B", "-X", "utf8",
            str(carpeta / "generar_setenta_y_seis_lean.py"),
            "--certificado", str(argumentos.certificado.resolve()),
            "--salida", str(destino / "OcelotasSetentaYSeisTabla.lean"),
            "--filas-por-modulo", "16"
        ], check=True)
        archivos = sorted(destino.glob("*.lean"))
        assert len(archivos) == 8
        for archivo in archivos:
            texto = archivo.read_text(encoding="utf-8")
            texto = texto.replace("OcelotasSetentaYSeisTabla", "OcelotasSetentaYSeisTablaBinaria")
            texto = texto.replace("OcelotasSetentaYSeisPrefijos", "OcelotasSetentaYSeisPrefijosBinarios")
            nombre = archivo.name.replace("OcelotasSetentaYSeisTabla", "OcelotasSetentaYSeisTablaBinaria")
            (argumentos.directorio / nombre).write_text(texto, encoding="utf-8")
    texto = (carpeta / "OcelotasSetentaYSeis.lean").read_text(encoding="utf-8")
    texto = texto.replace("OcelotasSetentaYSeisTabla", "OcelotasSetentaYSeisTablaBinaria")
    texto = re.sub(r"\bOcelotasSetentaYSeis\b", "OcelotasSetentaYSeisBinarios", texto)
    (argumentos.directorio / "OcelotasSetentaYSeisBinarios.lean").write_text(texto, encoding="utf-8")
    print("Generados ocho modulos de tabla y el ensamblaje alternativo.")


if __name__ == "__main__":
    main()
