import OcelotasCiclos
import OcelotasVeinticuatro

/-! # Ocelotas en ciclos: 24 rachas

Sólo bajo LMN (forma débil), sin verificación numérica externa.
Calibración: Hercher (2023) excluye los m-ciclos con m ≤ 91 por otra vía.
-/

namespace OcelotasCiclosVeinticuatro

open Ocelotas OcelotasContador OcelotasLMN OcelotasLMNFuente OcelotasCiclos

theorem cst_hasta (hL : LMNDebil) : CSTHasta 24 :=
  fun hn hk hr => OcelotasVeinticuatro.descenso_contador hL hn hk hr

/-- Ningún ciclo no trivial del atajo tiene a lo sumo 24 rachas impares. -/
theorem ciclo_exige (hL : LMNDebil) {n L : ℕ} (hL1 : 1 ≤ L)
    (hc : T^[L] n = n) (hno : ∀ j, 2 ≤ T^[j] n) : 24 < rachasCiclicas n L :=
  OcelotasCiclos.ciclo_exige (cst_hasta hL) hL1 hc hno

end OcelotasCiclosVeinticuatro

#print axioms OcelotasCiclosVeinticuatro.ciclo_exige
