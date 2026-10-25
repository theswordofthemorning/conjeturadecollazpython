import Mathlib.Data.Rat.Lemmas
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity

/-! Núcleos exactos del sesgo de frontera. La inyección de palabras,
su conteo y la no convergencia de la medida conservan prueba escrita.
No se declara aquí un teorema de ausencia de órbitas excepcionales. -/

namespace PerdicesSesgoFrontera

theorem intercambio_seguro {P : ℚ} (j : ℕ)
    (hP : 3 / 2 ≤ P) (hj : 1 ≤ j) :
    1 ≤ P * 2 ^ j / 3 := by
  have hpow : (2 : ℚ) ≤ 2 ^ j := by
    simpa using pow_le_pow_right₀ (by norm_num : (1 : ℚ) ≤ 2) hj
  have hP0 : 0 ≤ P := by linarith
  have hmul := mul_le_mul_of_nonneg_left hpow hP0
  linarith

theorem identidad_desviacion {N M R Q B RB : ℚ}
    (hN : 0 < N) (hM : 0 < M)
    (hcuenta : M = 2 * N - B) (hresiduo : Q = N - R - B + RB) :
    N * (R / N - 1 / 3) + M * (Q / M - 1 / 3) = RB - 2 * B / 3 := by
  field_simp
  nlinarith only [hcuenta, hresiduo]

theorem desviacion_dos_horizontes {N M B RB d e : ℚ}
    (hN : 0 < N) (hM : 0 ≤ M) (hM2 : M ≤ 2 * N)
    (hRB : RB ≤ B / 2) (hid : N * d + M * e = RB - 2 * B / 3) :
    B / (18 * N) ≤ max |d| |e| := by
  let t := max |d| |e|
  have ht : 0 ≤ t := le_trans (abs_nonneg d) (le_max_left _ _)
  have hd : -t ≤ d := le_trans (neg_le_neg (le_max_left _ _)) (neg_abs_le d)
  have he : -t ≤ e := le_trans (neg_le_neg (le_max_right _ _)) (neg_abs_le e)
  have h1 := mul_le_mul_of_nonneg_left hd (le_of_lt hN)
  have h2 := mul_le_mul_of_nonneg_left he hM
  have h3 := mul_le_mul_of_nonneg_right hM2 ht
  apply (div_le_iff₀ (show 0 < 18 * N by positivity)).2
  change B ≤ t * (18 * N)
  nlinarith only [hRB, hid, h1, h2, h3]

theorem piso_trasladado {N NH B BH : ℚ}
    (hNH : 0 < NH)
    (hB : N ≤ 16 * B) (hBH : B ≤ BH) (hcrece : NH ≤ 128 * N) :
    1 / 36864 ≤ BH / (18 * NH) := by
  apply (div_le_div_iff₀ (by norm_num : (0 : ℚ) < 36864)
    (show 0 < 18 * NH by positivity)).2
  nlinarith only [hB, hBH, hcrece]

theorem paso_libre {N M B RB d e : ℚ}
    (hN : 0 < N) (hM : M = 2 * N - B)
    (hB : B = 0) (hRB : RB = 0)
    (hid : N * d + M * e = RB - 2 * B / 3) :
    e = -d / 2 := by
  subst B
  subst RB
  have h : M = 2 * N := by simpa using hM
  rw [h] at hid
  nlinarith only [hid, hN]

/-- El encaje es el del mínimo exponente s con 2^j <= 3^s. -/
theorem incremento_unitario {s : ℕ → ℕ} (k : ℕ)
    (hinf : ∀ j, 2 ^ j ≤ 3 ^ s j)
    (hsup : ∀ j, 3 ^ s j < 3 * 2 ^ j) :
    s k ≤ s (k + 1) ∧ s (k + 1) ≤ s k + 1 := by
  have hz : 0 < (2 : ℕ) ^ k := by positivity
  constructor
  · by_contra hn
    have he : s (k + 1) + 1 ≤ s k := by omega
    have hp := Nat.pow_le_pow_right (n := 3) (by decide) he
    have hi := hinf (k + 1)
    have hu := hsup k
    rw [pow_add] at hp hi
    norm_num at hp hi
    nlinarith
  · by_contra hn
    have he : s k + 2 ≤ s (k + 1) := by omega
    have hp := Nat.pow_le_pow_right (n := 3) (by decide) he
    have hi := hinf k
    have hu := hsup (k + 1)
    rw [pow_add] at hp hu
    norm_num at hp hu
    nlinarith

theorem incremento_ocho {s : ℕ → ℕ} (k : ℕ)
    (hinf : ∀ j, 2 ^ j ≤ 3 ^ s j)
    (hsup : ∀ j, 3 ^ s j < 3 * 2 ^ j) :
    s k + 5 ≤ s (k + 8) := by
  have hz : 0 < (2 : ℕ) ^ k := by positivity
  by_contra hn
  have he : s (k + 8) ≤ s k + 4 := by omega
  have hp := Nat.pow_le_pow_right (n := 3) (by decide) he
  have hu := hsup k
  have hl := hinf (k + 8)
  rw [pow_add] at hp hl
  norm_num at hp hl
  nlinarith

theorem incremento_tres {s : ℕ → ℕ} (k : ℕ)
    (hinf : ∀ j, 2 ^ j ≤ 3 ^ s j)
    (hsup : ∀ j, 3 ^ s j < 3 * 2 ^ j) :
    s (k + 3) ≤ s k + 2 := by
  have hz : 0 < (2 : ℕ) ^ k := by positivity
  by_contra hn
  have he : s k + 3 ≤ s (k + 3) := by omega
  have hp := Nat.pow_le_pow_right (n := 3) (by decide) he
  have hu := hsup (k + 3)
  have hl := hinf k
  rw [pow_add] at hp hu
  norm_num at hp hu
  nlinarith

theorem ocho_incrementos {a b c d e f g h i : ℕ}
    (hab : b ≤ a + 1) (hbc : c ≤ b + 1)
    (hcd : d ≤ c + 1) (hde : e ≤ d + 1)
    (hef : f ≤ e + 1) (hfg : g ≤ f + 1)
    (hgh : h ≤ g + 1) (hhi : i ≤ h + 1)
    (hcinco : a + 5 ≤ i) :
    (b = a + 1 ∧ c = b + 1) ∨ (d = c + 1 ∧ e = d + 1) ∨
    (f = e + 1 ∧ g = f + 1) ∨ (h = g + 1 ∧ i = h + 1) := by
  omega

theorem frontera_alta {s : ℕ → ℕ} (k : ℕ)
    (hinf : ∀ j, 2 ^ j ≤ 3 ^ s j)
    (hsup : ∀ j, 3 ^ s j < 3 * 2 ^ j)
    (h1 : s (k + 1) = s k + 1) (h2 : s (k + 2) = s (k + 1) + 1) :
    3 * 2 ^ (k + 1) ≤ 2 * 3 ^ s (k + 1) ∧
      3 ^ s (k + 1) < 2 ^ (k + 2) := by
  constructor
  · have hi := hinf k
    rw [h1, pow_add, pow_add]
    norm_num
    nlinarith
  · have hi := hsup (k + 2)
    rw [h2, pow_add] at hi
    norm_num at hi
    nlinarith

theorem oscilacion_tres {a b c d : ℚ}
    (hlibre : 2 * b = -a ∨ 2 * c = -b ∨ 2 * d = -c) :
    |a| ≤ 3 * max |b - a| (max |c - b| |d - c|) := by
  let t := max |b - a| (max |c - b| |d - c|)
  have ht : 0 ≤ t := le_trans (abs_nonneg (b - a)) (le_max_left _ _)
  have hba : |b - a| ≤ t := le_max_left _ _
  have hcb : |c - b| ≤ t := (le_max_left _ _).trans (le_max_right _ _)
  have hdc : |d - c| ≤ t := (le_max_right _ _).trans (le_max_right _ _)
  rcases abs_le.mp hba with ⟨hba1, hba2⟩
  rcases abs_le.mp hcb with ⟨hcb1, hcb2⟩
  rcases abs_le.mp hdc with ⟨hdc1, hdc2⟩
  change |a| ≤ 3 * t
  apply abs_le.mpr
  rcases hlibre with h | h | h <;> constructor <;> linarith

end PerdicesSesgoFrontera

#print axioms PerdicesSesgoFrontera.intercambio_seguro
#print axioms PerdicesSesgoFrontera.identidad_desviacion
#print axioms PerdicesSesgoFrontera.desviacion_dos_horizontes
#print axioms PerdicesSesgoFrontera.piso_trasladado
#print axioms PerdicesSesgoFrontera.paso_libre
#print axioms PerdicesSesgoFrontera.incremento_unitario
#print axioms PerdicesSesgoFrontera.incremento_ocho
#print axioms PerdicesSesgoFrontera.incremento_tres
#print axioms PerdicesSesgoFrontera.ocho_incrementos
#print axioms PerdicesSesgoFrontera.frontera_alta
#print axioms PerdicesSesgoFrontera.oscilacion_tres
