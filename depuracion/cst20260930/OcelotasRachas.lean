import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith
import Mathlib.Data.Nat.Log

/-! # Extensión de Ocelotas: núcleo aritmético de la criba exacta

Certifica la recurrencia entera deducida de las congruencias de las rachas.
No es todavía la formalización de CST para diez rachas: las congruencias,
la cota de Rhin, la reducción de k y el cálculo finito se enlazan por escrito
en REVISION_RACHAS.md y mediante certificar_rachas.py.
-/

namespace OcelotasRachas

/-- Cota de la suma de longitudes impares cuando `n+1 < 2^m`. -/
def cota : ℕ → ℕ → ℕ
  | 0, _ => 0
  | r + 1, m => (5 * m + 8 * cota r m - 1) / 5

/-- Aumentar el número de rachas conserva todos los candidatos anteriores. -/
theorem cota_paso_monotono (r m : ℕ) (hm : 1 ≤ m) :
    cota r m ≤ cota (r + 1) m := by
  simp only [cota]
  omega

theorem tres_cinco (p : ℕ) : (3 ^ p) ^ 5 ≤ (2 ^ p) ^ 8 := by
  calc
    (3 ^ p) ^ 5 = (3 ^ 5) ^ p := by simp only [← pow_mul, Nat.mul_comm]
    _ ≤ (2 ^ 8) ^ p := Nat.pow_le_pow_left (by decide) p
    _ = (2 ^ p) ^ 8 := by simp only [← pow_mul, Nat.mul_comm]

/-- `2^a ≤ (n+1)3^p` implica la desigualdad estricta `5a < 5m+8p`. -/
theorem paso_cota {n p a m : ℕ} (hn : n + 1 < 2 ^ m)
    (hc : 2 ^ a ≤ (n + 1) * 3 ^ p) : 5 * a < 5 * m + 8 * p := by
  have h1 : (2 ^ a) ^ 5 ≤ ((n + 1) * 3 ^ p) ^ 5 :=
    Nat.pow_le_pow_left hc 5
  have h2 : (n + 1) ^ 5 < (2 ^ m) ^ 5 :=
    Nat.pow_lt_pow_left hn (by decide)
  have h3 : ((n + 1) * 3 ^ p) ^ 5 < (2 ^ m) ^ 5 * (2 ^ p) ^ 8 := by
    rw [mul_pow]
    calc
      (n + 1) ^ 5 * (3 ^ p) ^ 5 ≤ (n + 1) ^ 5 * (2 ^ p) ^ 8 :=
        Nat.mul_le_mul_left _ (tres_cinco p)
      _ < (2 ^ m) ^ 5 * (2 ^ p) ^ 8 :=
        Nat.mul_lt_mul_of_pos_right h2 (by positivity)
  have h4 : 2 ^ (5 * a) < 2 ^ (5 * m + 8 * p) := by
    simpa [pow_mul, pow_add, Nat.mul_comm] using lt_of_le_of_lt h1 h3
  exact (Nat.pow_lt_pow_iff_right (by decide)).1 h4

/-- Iteración universal del núcleo; A_i es la suma hasta la racha i. -/
theorem cota_acumulada (A : ℕ → ℕ) (m r : ℕ) (h0 : A 0 = 0)
    (hpaso : ∀ i, i < r → 5 * A (i + 1) < 5 * m + 8 * A i) :
    A r ≤ cota r m := by
  induction r with
  | zero => simp [cota, h0]
  | succ r ih =>
    have ha := ih (fun i hi => hpaso i (by omega))
    have hb := hpaso r (by omega)
    simp only [cota]
    omega

/-- Las congruencias y una cota diádica de n+1 bastan para cribar q=A_r. -/
theorem criba_desde_congruencias (A : ℕ → ℕ) (n m r : ℕ)
    (h0 : A 0 = 0) (hn : n + 1 < 2 ^ m)
    (hc : ∀ i, i < r → 2 ^ A (i + 1) ≤ (n + 1) * 3 ^ A i) :
    A r ≤ cota r m := by
  apply cota_acumulada A m r h0
  intro i hi
  exact paso_cota hn (hc i hi)

/-- Cola infinita de la cota diádica para diez rachas, E=182, C=4. -/
theorem cola_diez (t : ℕ) (ht : 17 ≤ t) :
    364 * (4 + 14 * (t + 1)) < 2 ^ t := by
  induction t, ht using Nat.le_induction with
  | base => norm_num
  | succ t ht ih =>
    rw [pow_succ]
    omega

#guard cota 3 9 == 42
#guard cota 10 14 == 2402

end OcelotasRachas

#print axioms OcelotasRachas.tres_cinco
#print axioms OcelotasRachas.cota_paso_monotono
#print axioms OcelotasRachas.paso_cota
#print axioms OcelotasRachas.cota_acumulada
#print axioms OcelotasRachas.criba_desde_congruencias
#print axioms OcelotasRachas.cola_diez
