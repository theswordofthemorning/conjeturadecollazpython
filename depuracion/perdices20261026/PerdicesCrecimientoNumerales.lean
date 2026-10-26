import Mathlib.Analysis.SpecificLimits.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-! Núcleos cuantitativos del argumento binario/ternario y sus bordes.
La traducción de las reglas y familias matriciales conserva prueba escrita. -/

namespace PerdicesCrecimientoNumerales

theorem cinco_cuatro (n : ℕ) : 2 ^ (5 * (n + 1) + 1) ≤ 3 ^ (4 * (n + 1)) := by
  induction n with
  | zero => norm_num
  | succ n ih =>
    have h2 : 5 * (n + 1 + 1) + 1 = (5 * (n + 1) + 1) + 5 := by ring
    have h3 : 4 * (n + 1 + 1) = 4 * (n + 1) + 4 := by ring
    change 2 ^ (5 * (n + 1 + 1) + 1) ≤ 3 ^ (4 * (n + 1 + 1))
    rw [h2, h3]
    calc
      2 ^ ((5 * (n + 1) + 1) + 5) = 2 ^ (5 * (n + 1) + 1) * 32 := by
        rw [pow_add]; norm_num
      _ ≤ 3 ^ (4 * (n + 1)) * 32 := Nat.mul_le_mul_right 32 ih
      _ ≤ 3 ^ (4 * (n + 1)) * 81 := Nat.mul_le_mul_left _ (by decide : 32 ≤ 81)
      _ = 3 ^ (4 * (n + 1) + 4) := by rw [pow_add]; norm_num

theorem potencia_supera_lineal (l : ℝ) (hl : 2 ≤ l) (n : ℕ) :
    (n : ℝ) + 1 ≤ l ^ n := by
  induction n with
  | zero => norm_num
  | succ n ih =>
    rw [pow_succ, Nat.cast_succ]
    have hn : 0 ≤ (n : ℝ) := Nat.cast_nonneg n
    have hprod := mul_le_mul_of_nonneg_right ih (show 0 ≤ l by linarith)
    have hresto := mul_nonneg (show 0 ≤ l - 2 by linarith) (show 0 ≤ (n : ℝ) + 1 by linarith)
    nlinarith

theorem coeficiente_de_potencias_acotadas (l z c : ℝ) (hl : 2 ≤ l)
    (hz : 0 ≤ z) (h : ∀ n : ℕ, l ^ n * z ≤ c) : z = 0 := by
  by_contra hne
  have hzpos : 0 < z := lt_of_le_of_ne hz (Ne.symm hne)
  obtain ⟨n, hn⟩ := exists_nat_gt (c / z)
  have hcn : c < (n : ℝ) * z := (div_lt_iff₀ hzpos).mp hn
  have hp := mul_le_mul_of_nonneg_right (potencia_supera_lineal l hl n) hz
  have hc := h n
  nlinarith

theorem incompatibilidad_cinco_cuatro (l z c : ℝ) (hl : 2 ≤ l)
    (hz : 0 ≤ z)
    (h : ∀ n : ℕ, l ^ (5 * n + 4) * z ≤ c * l ^ (4 * n + 4)) : z = 0 := by
  apply coeficiente_de_potencias_acotadas l z c hl hz
  intro n
  have hexp : 5 * n + 4 = (4 * n + 4) + n := by ring
  have hn := h n
  rw [hexp, pow_add, mul_assoc] at hn
  rw [mul_comm c] at hn
  have hp : 0 < l ^ (4 * n + 4) := pow_pos (show 0 < l by linarith) _
  exact (mul_le_mul_iff_right₀ hp).mp (by simpa only [mul_comm] using hn)

theorem piso_recursion (x : ℕ → ℝ) (l d : ℝ)
    (hl : 0 ≤ l) (hd : 0 ≤ d) (hx : 0 ≤ x 0)
    (hrec : ∀ n, x (n + 1) = l * x n + d) :
    ∀ n, l ^ n * d ≤ x (n + 1) := by
  intro n
  induction n with
  | zero =>
    rw [hrec]
    simp only [pow_zero, one_mul]
    nlinarith [mul_nonneg hl hx]
  | succ n ih =>
    rw [hrec (n + 1), pow_succ]
    have hh := mul_le_mul_of_nonneg_left ih hl
    nlinarith

theorem imagen_factor_uno (a0 a1 b0 b1 e1 f0 f1 g0 c0 c1 : ℝ)
    (ha : 0 ≤ a0) (hb : 0 ≤ b1) (hf : 0 ≤ f0)
    (hfb : g0 + a1 ≤ b1 + f1)
    (heb : f1 + b1 ≤ b0 + e1)
    (hgc : c0 + a1 + b0 ≤ c1 + g0)
    (hec : c1 + b1 ≤ c0 + e1)
    (hd2 : e1 ≤ a1) (hd3 : f0 ≤ b1) (hfc : 2 * a0 ≤ f0) :
    a0 = 0 ∧ a1 - e1 = 0 ∧ b1 - f0 = 0 := by
  refine ⟨?_, ?_, ?_⟩ <;> linarith

theorem nucleo_factor_uno (x y z w : ℝ) (hx : 0 ≤ x)
    (hec : y ≤ z) (hfc : 2 * x ≤ w) (hd2 : z ≤ x) (hd3 : w ≤ y) :
    x = 0 ∧ y = 0 ∧ z = 0 ∧ w = 0 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> linarith

theorem ponderacion_positiva (u v x y : ℝ) (hu : 0 < u) (hv : 0 < v)
    (hx : 0 ≤ x) (hy : 0 ≤ y) (h : u * x + v * y = 0) : x = 0 ∧ y = 0 := by
  constructor <;> nlinarith [mul_nonneg (le_of_lt hu) hx, mul_nonneg (le_of_lt hv) hy]

end PerdicesCrecimientoNumerales

#print axioms PerdicesCrecimientoNumerales.cinco_cuatro
#print axioms PerdicesCrecimientoNumerales.potencia_supera_lineal
#print axioms PerdicesCrecimientoNumerales.coeficiente_de_potencias_acotadas
#print axioms PerdicesCrecimientoNumerales.incompatibilidad_cinco_cuatro
#print axioms PerdicesCrecimientoNumerales.piso_recursion
#print axioms PerdicesCrecimientoNumerales.imagen_factor_uno
#print axioms PerdicesCrecimientoNumerales.nucleo_factor_uno
#print axioms PerdicesCrecimientoNumerales.ponderacion_positiva
