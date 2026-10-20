"""Controles del perfil acotado sin instalar ni ejecutar YAH.

Uso: python -B -X utf8 comprobar_plan.py
"""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


def cargar():
    ruta = Path(__file__).with_name("lanzar.py")
    especificacion = importlib.util.spec_from_file_location("tanda_yah", ruta)
    modulo = importlib.util.module_from_spec(especificacion)
    especificacion.loader.exec_module(modulo)
    return modulo


class Controles(unittest.TestCase):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporal.cleanup)
        self.base = Path(self.temporal.name)
        self.tanda = cargar()
        self.tanda.RES = str(self.base / "resultados")
        self.tanda.SISTEMAS = str(self.base / "sistemas")
        Path(self.tanda.RES).mkdir()
        Path(self.tanda.SISTEMAS).mkdir()
        for nombre in self.tanda.CALIBRACION + ["G_B4", "G_B5", "G_B6", "G_B7"]:
            (Path(self.tanda.SISTEMAS) / (nombre + ".srs")).write_text("a -> b\n", encoding="utf-8")

    def ejecutar(self, fallo=None):
        ejecutados = []

        def simular(nombre, topes, resumen):
            ejecutados.append(nombre)
            self.assertEqual(topes, [30])
            resumen[nombre] = {"veredicto": "sin prueba" if nombre == fallo else "QED"}
            return nombre != fallo

        with patch.dict("os.environ", {"TANDA_RESULTADOS": self.tanda.RES}), \
                patch("sys.argv", ["lanzar.py", "--diagnostico"]), \
                patch.object(self.tanda.signal, "signal"), \
                patch.object(self.tanda.os, "symlink"), \
                patch.object(self.tanda, "decir"), \
                patch.object(self.tanda, "memoria_disponible", return_value=8 * 2 ** 30), \
                patch.object(self.tanda, "cascada", side_effect=simular):
            self.tanda.main()
        return ejecutados, json.loads((Path(self.tanda.RES) / "resumen.json").read_text(encoding="utf-8"))

    def test_calibracion_fallida_impide_experimentos(self):
        ejecutados, _ = self.ejecutar("peldano2_sinL")
        self.assertEqual(ejecutados, self.tanda.CALIBRACION[:2])

    def test_primer_resistente_detiene_escalera(self):
        ejecutados, resumen = self.ejecutar("G_B4")
        self.assertEqual(ejecutados, self.tanda.CALIBRACION + ["G_B4"])
        self.assertEqual(resumen["presupuesto_segundos"], 1800)
        self.assertEqual(resumen["trabajadores"], 4)
        self.assertEqual(len(resumen["sha256_sistemas"]), 8)
        self.assertTrue(all(len(h) == 64 for h in resumen["sha256_sistemas"].values()))

    def test_solo_qed_permita_subir(self):
        ejecutados, _ = self.ejecutar()
        self.assertEqual(ejecutados[-4:], ["G_B4", "G_B5", "G_B6", "G_B7"])

    def test_carpeta_historica_se_conserva(self):
        carpeta = Path(self.tanda.RES) / "G_B4"
        carpeta.mkdir()
        evidencia = carpeta / "prueba.log"
        evidencia.write_bytes(b"conservar exactamente\r\n")
        with self.assertRaises(FileExistsError):
            self.tanda.cascada("G_B4", [30], {})
        self.assertEqual(evidencia.read_bytes(), b"conservar exactamente\r\n")

    def test_resumen_historico_se_conserva(self):
        ruta = Path(self.tanda.RES) / "resumen.json"
        ruta.write_bytes(b"evidencia historica")
        with self.assertRaises(SystemExit):
            self.ejecutar()
        self.assertEqual(ruta.read_bytes(), b"evidencia historica")

    def test_presupuesto_no_lanza_otro_proceso(self):
        self.tanda.limite_tanda = 0
        with patch.object(self.tanda, "correr_forma") as correr, patch.object(self.tanda, "decir"):
            resumen = {}
            self.assertFalse(self.tanda.cascada("G_B4", [30], resumen))
            correr.assert_not_called()
        self.assertEqual(resumen["G_B4"]["veredicto"], "parado: presupuesto agotado")

    def test_presupuesto_interrumpe_espera_memoria(self):
        self.tanda.limite_tanda = 0
        with patch.object(self.tanda, "memoria_disponible", return_value=0):
            self.assertFalse(self.tanda.esperar_memoria())

    def test_tope_del_hijo_se_acorta_al_presupuesto(self):
        actual = str(Path(self.tanda.SISTEMAS) / "G_B4.srs")
        with patch.object(self.tanda, "esperar_memoria", return_value=True), \
                patch.object(self.tanda, "segundos_disponibles", return_value=7.5), \
                patch.object(self.tanda.subprocess, "Popen") as proceso:
            proceso.return_value.wait.return_value = 29
            resultado, _, _ = self.tanda.correr_forma(
                actual, ("natural", 1, 3), False, 30, self.tanda.RES, 1)
        proceso.return_value.wait.assert_called_once_with(timeout=7.5)
        self.assertEqual(resultado, "UNSAT")

    def test_error_detiene_cascada(self):
        with patch.object(self.tanda, "correr_forma", return_value=("error 1", None, 0)) as correr, \
                patch.object(self.tanda, "decir"):
            resumen = {}
            self.assertFalse(self.tanda.cascada("G_B4", [30], resumen))
            self.assertEqual(correr.call_count, 1)
        self.assertEqual(resumen["G_B4"]["veredicto"], "parado: error 1")


if __name__ == "__main__":
    unittest.main()
