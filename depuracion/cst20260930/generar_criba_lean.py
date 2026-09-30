"""Genera bloques de la criba; Lean comprueba sus extremos y todas las transiciones.

Cada extremo inicial se calcula con enteros exactos. El generador no forma
parte de la base de confianza: emite enunciados demostrados con decide +kernel.
"""

import argparse
import hashlib
import json
from pathlib import Path


ESCALA = 2 ** 48


def generar(hasta, bloque):
    if hasta != 82696 or not 1 <= bloque <= 2048:
        raise ValueError("Este cierre requiere hasta=82696 y 1<=bloque<=2048")
    lineas = [
        "import OcelotasCriba", "",
        "/-! Certificado generado por generar_criba_lean.py.",
        "Cada bloque comprueba en el núcleo su punto inicial y sus pasos.",
        "La cobertura final incluye todos los exponentes 1,...,82696. -/", "",
        "set_option maxRecDepth 100000", "set_option maxHeartbeats 0", "",
        "namespace OcelotasCertificado", "",
        "open Ocelotas OcelotasFinito OcelotasCriba OcelotasTrayectorias", "",
    ]
    intervalos = []
    por_semilla, por_criba, anchura_maxima = 0, 0, 0
    pasos_uno, pasos_dos = 0, 0
    huella = hashlib.sha256()
    for indice, inicio in enumerate(range(0, hasta, bloque)):
        cantidad = min(bloque, hasta - inicio)
        potencia = 3 ** inicio
        k = potencia.bit_length()
        denominador = 2 ** k
        inferior = ESCALA * potencia // denominador
        superior = (ESCALA * potencia + denominador - 1) // denominador
        marco = f"⟨{inferior}, {superior}, {k}⟩"
        intervalos.append((inicio + 1, inicio + cantidad))
        lineas.extend([
            f"theorem bloque_{indice:03d} (q : ℕ) (hlo : {inicio + 1} ≤ q)",
            f"    (hhi : q ≤ {inicio + cantidad}) : CertificadoAritmetico q := by",
            f"  have he : Encierra {inicio} {marco} := by decide +kernel",
            f"  have hc : recorrer {inicio} {marco} {cantidad} = true := by decide +kernel",
            f"  exact recorrer_correcto {cantidad} {inicio} {marco} he hc q (by omega) (by omega)",
            "",
        ])
        assert inferior * denominador <= ESCALA * potencia <= superior * denominador
        for q in range(inicio + 1, inicio + cantidad + 1):
            potencia *= 3
            if 3 * superior < 2 * ESCALA:
                inferior, superior = 3 * inferior // 2, (3 * superior + 1) // 2
                k += 1
                pasos_uno += 1
            else:
                inferior, superior = 3 * inferior // 4, (3 * superior + 3) // 4
                k += 2
                pasos_dos += 1
            denominador = 2 ** k
            assert inferior * denominador <= ESCALA * potencia <= superior * denominador
            assert ESCALA < 2 * inferior and superior < ESCALA
            assert k == potencia.bit_length()
            if 11225 * superior <= 11215 * ESCALA:
                por_semilla += 1
            else:
                m = (q - 1) // 182
                assert (2 ** m + 11) * superior <= 2 ** m * ESCALA
                por_criba += 1
            anchura_maxima = max(anchura_maxima, superior - inferior)
            huella.update(f"{q},{inferior},{superior},{k}\n".encode())

    lineas.extend([
        "theorem criba_certificada : ∀ q, 1 ≤ q → q ≤ 82696 → CertificadoAritmetico q := by",
        "  intro q hlo hhi",
    ])

    def cubrir(primero, ultimo, margen):
        if ultimo == primero + 1:
            lineas.append(margen + f"exact bloque_{primero:03d} q (by omega) (by omega)")
            return
        medio = (primero + ultimo) // 2
        corte = intervalos[medio - 1][1]
        lineas.append(margen + f"by_cases h{corte} : q ≤ {corte}")
        lineas.append(margen + "·")
        cubrir(primero, medio, margen + "  ")
        lineas.append(margen + "·")
        cubrir(medio, ultimo, margen + "  ")

    cubrir(0, len(intervalos), "  ")
    lineas.extend([
        "", "/-- Descenso para palabras reales de una a diez rachas; Rhin sigue explícito. -/",
        "theorem ocelotas_diez (hR : RhinEntera) {n r : ℕ} {a b : ℕ → ℕ}",
        "    (hn : 2 ≤ n) (hw : Palabra n a b r) (hr : 0 < r) (hr10 : r ≤ 10)",
        "    (hk : PrimerCruce n (tiempo a b r)) : T^[tiempo a b r] n < n :=",
        "  diez_de_certificado hR criba_certificada hn hw hr hr10 hk", "",
        "end OcelotasCertificado", "",
        "#print axioms OcelotasCertificado.criba_certificada",
        "#print axioms OcelotasCertificado.ocelotas_diez", "",
    ])
    return "\n".join(lineas), {
        "intervalo_q_cerrado": [1, hasta],
        "tamano_bloque": bloque,
        "bloques": len(intervalos),
        "escala": ESCALA,
        "exponentes_cotejados_con_potencias_exactas": hasta,
        "por_cota_semilla": por_semilla,
        "por_criba_lineal": por_criba,
        "pasos_exponente_uno": pasos_uno,
        "pasos_exponente_dos": pasos_dos,
        "anchura_maxima_intervalo": anchura_maxima,
        "ultimo_exponente_k": k,
        "ultimo_bloque_cerrado": list(intervalos[-1]),
        "sha256_filas_q_inferior_superior_k": huella.hexdigest(),
        "fallos": 0,
    }


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument("--hasta", type=int, required=True)
    analizador.add_argument("--bloque", type=int, required=True)
    analizador.add_argument("--lean", type=Path, required=True)
    analizador.add_argument("--salida", type=Path, required=True)
    argumentos = analizador.parse_args()
    fuente, datos = generar(argumentos.hasta, argumentos.bloque)
    argumentos.lean.write_text(fuente, encoding="utf-8")
    datos["sha256_lean"] = hashlib.sha256(argumentos.lean.read_bytes()).hexdigest()
    datos["sha256_generador"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    contenido = json.dumps(datos, ensure_ascii=False, indent=2) + "\n"
    argumentos.salida.write_text(contenido, encoding="utf-8")
    print(contenido, end="")


if __name__ == "__main__":
    main()
