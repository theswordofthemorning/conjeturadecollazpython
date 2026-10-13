import OcelotasCiclos
import OcelotasCuarentaYSeis

/-! # Ocelotas en ciclos: 46 rachas

Bajo LMN y el censo propio hasta 7·10^11 (hipótesis explícita).
Calibración: Hercher (2023) excluye los m-ciclos con m ≤ 91 por otra vía.
-/

namespace OcelotasCiclosCuarentaYSeis

open Ocelotas OcelotasContador OcelotasLMN OcelotasLMNFuente OcelotasCiclos

theorem cst_hasta (hL : LMNDebil) (hC : OcelotasCuarentaYSeis.CensoPropio7e11) : CSTHasta 46 :=
  fun hn hk hr => OcelotasCuarentaYSeis.descenso_contador hL hC hn hk hr

/-- Ningún ciclo no trivial del atajo tiene a lo sumo 46 rachas impares. -/
theorem ciclo_exige (hL : LMNDebil) (hC : OcelotasCuarentaYSeis.CensoPropio7e11) {n L : ℕ} (hL1 : 1 ≤ L)
    (hc : T^[L] n = n) (hno : ∀ j, 2 ≤ T^[j] n) : 46 < rachasCiclicas n L :=
  OcelotasCiclos.ciclo_exige (cst_hasta hL hC) hL1 hc hno

end OcelotasCiclosCuarentaYSeis

#print axioms OcelotasCiclosCuarentaYSeis.ciclo_exige
