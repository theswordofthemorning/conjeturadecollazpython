import GaoEnunciado
import GarnerEnunciado
import WuEnunciado

/-! # Lemas de lectura para la revisión humana

Ruta de Judas, J3b, 16-10-2026. No añaden resultados. Reescriben piezas de los
enunciados finales de Gao, Garner y Wu sin convenciones propias de Lean: el
`Nat.log` de Gao, la unicidad de la altura y la resta natural de Wu en `n = 1`.
Se compilan con el proyecto Lake de `depuracion/gao20260920/formal`.
-/

namespace LecturaRevision

/-- Gao: para `m ≥ 1`, la condición `k ≤ Nat.log 2 m` es `2^k ≤ m`. -/
theorem gao_encuentro_iff {m : ℕ} (hm : 1 ≤ m) :
    GaoEnunciado.encuentro m ↔
      ∃ k, 2 ^ k ≤ m ∧ GaoEnunciado.f^[k] m = GaoEnunciado.f^[k] (m + 1) := by
  have hm0 : m ≠ 0 := by omega
  constructor
  · rintro ⟨k, hk, he⟩
    exact ⟨k, (Nat.le_log_iff_pow_le (by norm_num) hm0).1 hk, he⟩
  · rintro ⟨k, hk, he⟩
    exact ⟨k, (Nat.le_log_iff_pow_le (by norm_num) hm0).2 hk, he⟩

/-- Gao: `m = 0` nunca cuenta, porque sólo admite `k = 0` y `0 ≠ 1`. -/
theorem gao_cero : ¬ GaoEnunciado.encuentro 0 := by
  rintro ⟨k, hk, he⟩
  rw [Nat.log_zero_right, Nat.le_zero] at hk
  subst hk
  simp at he

/-- Garner: la altura, si existe, es única; «la misma altura h» no es ambiguo. -/
theorem garner_altura_unica {n h h' : ℕ} (h₁ : GarnerEnunciado.altura n h)
    (h₂ : GarnerEnunciado.altura n h') : h = h' := by
  obtain ⟨a₁, b₁⟩ := h₁
  obtain ⟨a₂, b₂⟩ := h₂
  by_contra hne
  rcases Nat.lt_or_gt_of_ne hne with hlt | hlt
  · exact b₂ h hlt a₁
  · exact b₁ h' hlt a₂

/-- Wu: el 0 queda fijo bajo `C`. -/
theorem wu_iterado_cero (h : ℕ) : WuEnunciado.C^[h] 0 = 0 := by
  induction h with
  | zero => rfl
  | succ h ih =>
    rw [Function.iterate_succ_apply', ih]
    simp [WuEnunciado.C]

/-- Wu: el 0 no tiene altura. -/
theorem wu_cero_sin_altura (h : ℕ) : ¬ WuEnunciado.altura 0 h := by
  rintro ⟨h₁, -⟩
  rw [wu_iterado_cero] at h₁
  exact absurd h₁ (by norm_num)

/-- Wu: en `enUpla 1` la resta natural `1 - 1 = 0` no crea uplas falsas;
sólo cuenta el vecino 2. -/
theorem wu_enUpla_uno :
    WuEnunciado.enUpla 1 ↔ ∃ h, WuEnunciado.altura 1 h ∧ WuEnunciado.altura 2 h := by
  constructor
  · rintro ⟨h, h₁, h₀ | h₂⟩
    · exact absurd h₀ (wu_cero_sin_altura h)
    · exact ⟨h, h₁, h₂⟩
  · rintro ⟨h, h₁, h₂⟩
    exact ⟨h, h₁, Or.inr h₂⟩

/-- Wu: las dos alturas de Wu y de Garner son la misma definición. -/
theorem altura_wu_garner (n h : ℕ) : WuEnunciado.altura n h ↔ GarnerEnunciado.altura n h :=
  Iff.rfl

end LecturaRevision

#print axioms LecturaRevision.gao_encuentro_iff
#print axioms LecturaRevision.gao_cero
#print axioms LecturaRevision.garner_altura_unica
#print axioms LecturaRevision.wu_iterado_cero
#print axioms LecturaRevision.wu_cero_sin_altura
#print axioms LecturaRevision.wu_enUpla_uno
#print axioms LecturaRevision.altura_wu_garner
