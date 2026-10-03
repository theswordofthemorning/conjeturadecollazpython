import OcelotasResiduosBloques

/-! # Ocelotas: certificado por residuos hasta 4912740

El intervalo queda dentro del censo conservado hasta 2^23.
La prueba siguiente evalúa el verificador en el núcleo de Lean;
no importa el censo ni su resultado como premisa.
-/

namespace OcelotasResiduosFinito

open Ocelotas OcelotasResiduos

theorem intervalo_comprobado : intervalo 4912740 225 = true :=
  OcelotasResiduosBloques.intervalo_comprobado

theorem existe_descenso_finito {n : ℕ} (hn : 2 ≤ n) (hmax : n ≤ 4912740) :
    ∃ k, k ≤ 224 ∧ PrimerCruce n k ∧ T^[k] n < n := by
  obtain ⟨k, hkc, hk, hd⟩ := intervalo_correcto intervalo_comprobado hn hmax
  exact ⟨k, by omega, hk, hd⟩

theorem descenso_finito {n k : ℕ} (hn : 2 ≤ n) (hmax : n ≤ 4912740)
    (hk : PrimerCruce n k) : T^[k] n < n := by
  obtain ⟨j, _, hj, hd⟩ := existe_descenso_finito hn hmax
  simpa only [OcelotasFinito.primer_cruce_unico hj hk] using hd

end OcelotasResiduosFinito

#print axioms OcelotasResiduosFinito.intervalo_comprobado
#print axioms OcelotasResiduosFinito.existe_descenso_finito
#print axioms OcelotasResiduosFinito.descenso_finito
