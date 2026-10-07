import CasaPlano
import OcelotasVeinticuatro

/-! # El tramo del muro A que construye Ocelotas

Conecta el plano de la casa (`CasaPlano`) con el cierre de 24 rachas de Ocelotas
(`OcelotasVeinticuatro`, 04-10-2026). La única hipótesis externa es `LMN23`, la
especialización a 2 y 3 del corolario 2 de Laurent–Mignotte–Nesterenko (1995); es un
argumento de los teoremas, no un axioma.

Compilación: `comprobar_casa.py`, en esta carpeta. -/

namespace CasaOcelotas

open Ocelotas OcelotasContador OcelotasLMNFuente CasaPlano

/-- Bajo LMN, el muro A está en pie para todo número con a lo sumo 24 picos (rachas)
    antes de su primer cruce. -/
theorem muroA_hasta_24 (hL : LMN23) : MuroAHasta 24 :=
  tramo_de_descenso fun _ _ hn hk hr =>
    (OcelotasVeinticuatro.cst_veinticuatro_corolario hL hn hk hr).2

/-- Bajo LMN, una grieta en el muro A, es decir, un número cuyo pronóstico baja de 1 pero
    que nunca baja de sí mismo, necesita al menos 25 picos antes de su primer cruce. -/
theorem grieta_exige_25 (hL : LMN23) {n : ℕ} (hn : 2 ≤ n) (hc : Cruza n)
    (hd : ¬ Desciende n) : ∃ k, PrimerCruce n k ∧ 25 ≤ rachas n k := by
  obtain ⟨k, hk⟩ := primerCruce_de_cruza hc
  refine ⟨k, hk, ?_⟩
  by_contra h
  exact hd (muroA_hasta_24 hL n k hn hk (by omega))

end CasaOcelotas

#print axioms CasaOcelotas.muroA_hasta_24
#print axioms CasaOcelotas.grieta_exige_25
