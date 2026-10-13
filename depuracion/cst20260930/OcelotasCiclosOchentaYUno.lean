import OcelotasCiclos
import OcelotasOchentaYUno

/-! # Ocelotas en ciclos: 81 rachas

Bajo LMN y el corolario 5.4 de Rozier-Terracol (hipótesis explícita).
Calibración: Hercher (2023) excluye los m-ciclos con m ≤ 91 por otra vía.
-/

namespace OcelotasCiclosOchentaYUno

open Ocelotas OcelotasContador OcelotasLMN OcelotasLMNFuente OcelotasCiclos

theorem cst_hasta (hL : LMNDebil) (hRT : OcelotasOchentaYUno.RozierTerracol54) : CSTHasta 81 :=
  fun hn hk hr => OcelotasOchentaYUno.descenso_contador hL hRT hn hk hr

/-- Ningún ciclo no trivial del atajo tiene a lo sumo 81 rachas impares. -/
theorem ciclo_exige (hL : LMNDebil) (hRT : OcelotasOchentaYUno.RozierTerracol54) {n L : ℕ} (hL1 : 1 ≤ L)
    (hc : T^[L] n = n) (hno : ∀ j, 2 ≤ T^[j] n) : 81 < rachasCiclicas n L :=
  OcelotasCiclos.ciclo_exige (cst_hasta hL hRT) hL1 hc hno

end OcelotasCiclosOchentaYUno

#print axioms OcelotasCiclosOchentaYUno.ciclo_exige
