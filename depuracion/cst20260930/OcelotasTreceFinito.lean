import OcelotasFinito

/-! # Ocelotas: extensión del descenso finito hasta 31623

Se reutiliza el certificado hasta 11214. Sólo se evalúan las 20409 semillas
adicionales en el núcleo. El combustible agotado rechaza la semilla.
-/

namespace OcelotasTreceFinito

open Ocelotas

def semilla (n : ℕ) : Bool := OcelotasFinito.comprobar n n 1 1 225

theorem semilla_correcta {n : ℕ} (h : semilla n = true) :
    ∃ k, k ≤ 224 ∧ PrimerCruce n k ∧ T^[k] n < n := by
  have hc : OcelotasFinito.comprobar n (T^[0] n) (3 ^ S 0 n) (2 ^ 0) 225 = true := by
    simpa only [semilla, S, pow_zero, Function.iterate_zero, id_eq] using h
  obtain ⟨k, _, hkc, hk, hn⟩ := OcelotasFinito.comprobar_correcto n 225 0 (by omega) hc
  exact ⟨k, by omega, hk, hn⟩

def intervalo (inicio cantidad : ℕ) : Bool :=
  if cantidad = 0 then true
  else if cantidad = 1 then semilla inicio
  else
    intervalo inicio (cantidad / 2) &&
      intervalo (inicio + cantidad / 2) (cantidad - cantidad / 2)
termination_by cantidad
decreasing_by all_goals omega

theorem intervalo_correcto (cantidad : ℕ) : ∀ inicio,
    intervalo inicio cantidad = true →
    ∀ n, inicio ≤ n → n < inicio + cantidad → semilla n = true := by
  induction cantidad using Nat.strong_induction_on with
  | h cantidad ih =>
    intro inicio hc n hn hnfin
    rw [intervalo] at hc
    split at hc
    next hz => omega
    next hz =>
      split at hc
      next h1 =>
        have he : n = inicio := by omega
        simpa only [he] using hc
      next h1 =>
        simp only [Bool.and_eq_true] at hc
        obtain ⟨hizq, hder⟩ := hc
        by_cases hmitad : n < inicio + cantidad / 2
        · exact ih (cantidad / 2) (by omega) inicio hizq n hn hmitad
        · exact ih (cantidad - cantidad / 2) (by omega)
            (inicio + cantidad / 2) hder n (by omega) (by omega)

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem intervalo_comprobado : intervalo 11215 20409 = true := by
  decide +kernel

theorem existe_descenso_finito {n : ℕ} (hn : 2 ≤ n) (hnmax : n ≤ 31623) :
    ∃ k, k ≤ 224 ∧ PrimerCruce n k ∧ T^[k] n < n := by
  by_cases hsmall : n ≤ 11214
  · obtain ⟨k, hkc, hk, hd⟩ := OcelotasFinito.existe_descenso_finito hn hsmall
    exact ⟨k, by omega, hk, hd⟩
  · have hseed := intervalo_correcto 20409 11215 intervalo_comprobado n (by omega) (by omega)
    exact semilla_correcta hseed

theorem descenso_finito {n k : ℕ} (hn : 2 ≤ n) (hnmax : n ≤ 31623)
    (hk : PrimerCruce n k) : T^[k] n < n := by
  obtain ⟨j, _, hj, hd⟩ := existe_descenso_finito hn hnmax
  simpa only [OcelotasFinito.primer_cruce_unico hj hk] using hd

end OcelotasTreceFinito

#print axioms OcelotasTreceFinito.intervalo_comprobado
#print axioms OcelotasTreceFinito.existe_descenso_finito
#print axioms OcelotasTreceFinito.descenso_finito
