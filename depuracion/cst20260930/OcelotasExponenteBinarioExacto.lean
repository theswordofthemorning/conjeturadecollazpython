import OcelotasPrefijosBinarios

/-! # La bisección conserva exactamente el exponente afinado anterior -/

namespace OcelotasExponenteBinarioExacto

open OcelotasPrefijosBinarios

set_option maxRecDepth 10000

theorem techo_equiv (s b : ℕ) :
    OcelotasPrefijosAfinados.exponente s ≤ b ↔ s ^ 256 ≤ 2 ^ b := by
  by_cases hs : s ≤ 1
  · rcases (show s = 0 ∨ s = 1 by omega) with hz | hu
    · simp [hz, OcelotasPrefijosAfinados.exponente]
    · have hp : 0 < (2 : ℕ) ^ b := by positivity
      simp only [hu, OcelotasPrefijosAfinados.exponente, le_refl, if_true,
        Nat.zero_le, one_pow, true_iff]
      omega
  · have hp := Nat.pow_le_pow_left (by omega : 2 ≤ s) 256
    have hdos : (1 : ℕ) < 2 ^ 256 := by decide
    have hx : s ^ 256 - 1 ≠ 0 := by omega
    have he := Nat.log2_lt (k := b) hx
    simp only [OcelotasPrefijosAfinados.exponente, if_neg hs]
    omega

theorem buscar_exacto (x z combustible : ℕ)
    (he : ∀ b, z ≤ b ↔ x ≤ 2 ^ b) :
    ∀ inferior superior, inferior < z → z ≤ superior →
      superior - inferior ≤ 2 ^ combustible →
      buscar x inferior superior combustible = z := by
  induction combustible with
  | zero =>
    intro inferior superior hinf hsup hgap
    simp only [buscar]
    norm_num at hgap
    omega
  | succ combustible ih =>
    intro inferior superior hinf hsup hgap
    rw [pow_succ] at hgap
    simp only [buscar]
    split
    next hm =>
      apply ih _ _ hinf ((he _).2 hm)
      omega
    next hm =>
      have hmid : ¬z ≤ (inferior + superior) / 2 := fun hz => hm ((he _).1 hz)
      apply ih _ _ (by omega) hsup
      omega

theorem exponente_igual (s : ℕ) :
    OcelotasPrefijosBinarios.exponente s = OcelotasPrefijosAfinados.exponente s := by
  by_cases hs : s ≤ 1
  · simp [OcelotasPrefijosBinarios.exponente, OcelotasPrefijosAfinados.exponente, hs]
  · have hs0 : s ≠ 0 := by omega
    have hlow := Nat.pow_le_pow_left (Nat.log2_self_le hs0) 256
    have hhigh := Nat.pow_le_pow_left (Nat.le_of_lt (Nat.lt_log2_self (n := s))) 256
    have helow : s.log2 * 256 = 256 * s.log2 := by omega
    have hehigh : (s.log2 + 1) * 256 = 256 * s.log2 + 256 := by omega
    simp only [← pow_mul, helow] at hlow
    simp only [← pow_mul, hehigh] at hhigh
    simp only [OcelotasPrefijosBinarios.exponente, if_neg hs]
    split
    next hinf =>
      have hb := (techo_equiv s (256 * s.log2)).2 hinf
      have hbpow := OcelotasPrefijosAfinados.potencia_exponente s
      have hcomp : 2 ^ (256 * s.log2) ≤ 2 ^ OcelotasPrefijosAfinados.exponente s :=
        le_trans hlow hbpow
      have hb' := (Nat.pow_le_pow_iff_right (by decide : 1 < (2 : ℕ))).1 hcomp
      omega
    next hinf =>
      apply buscar_exacto _ _ 8 (techo_equiv s)
      · have h := (techo_equiv s (256 * s.log2)).not.mpr hinf
        omega
      · exact (techo_equiv s _).2 hhigh
      · norm_num

end OcelotasExponenteBinarioExacto

#print axioms OcelotasExponenteBinarioExacto.techo_equiv
#print axioms OcelotasExponenteBinarioExacto.buscar_exacto
#print axioms OcelotasExponenteBinarioExacto.exponente_igual
