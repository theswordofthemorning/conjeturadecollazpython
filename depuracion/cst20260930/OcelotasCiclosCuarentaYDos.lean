import OcelotasCiclos
import OcelotasCuarentaYDos

/-! # Ocelotas en ciclos: 42 rachas

Bajo LMN y el censo propio hasta 3·10^11 (hipótesis explícita).
Calibración: Hercher (2023) excluye los m-ciclos con m ≤ 91 por otra vía.
-/

namespace OcelotasCiclosCuarentaYDos

open Ocelotas OcelotasContador OcelotasLMN OcelotasLMNFuente OcelotasCiclos

theorem cst_hasta (hL : LMNDebil) (hC : OcelotasCuarentaYDos.CensoPropio3e11) : CSTHasta 42 :=
  fun hn hk hr => OcelotasCuarentaYDos.descenso_contador hL hC hn hk hr

/-- Ningún ciclo no trivial del atajo tiene a lo sumo 42 rachas impares. -/
theorem ciclo_exige (hL : LMNDebil) (hC : OcelotasCuarentaYDos.CensoPropio3e11) {n L : ℕ} (hL1 : 1 ≤ L)
    (hc : T^[L] n = n) (hno : ∀ j, 2 ≤ T^[j] n) : 42 < rachasCiclicas n L :=
  OcelotasCiclos.ciclo_exige (cst_hasta hL hC) hL1 hc hno

end OcelotasCiclosCuarentaYDos

#print axioms OcelotasCiclosCuarentaYDos.ciclo_exige
