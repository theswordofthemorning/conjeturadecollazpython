import Mathlib.Data.Int.ModEq
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.LinearCombination

/-! # Jinetas: álgebra del intercambio y del relleno de ceros

Palabras leídas en orden temporal, false = par, true = impar.
Se certifica el álgebra sobre palabras y enteros, no el traslado infinito
de Rozier–Terracol ni una exclusión universal de segmentos paradójicos.
-/

namespace Jinetas

def unos : List Bool → ℕ
  | [] => 0
  | bit :: resto => (if bit then 1 else 0) + unos resto

def aditivo : List Bool → ℤ
  | [] => 0
  | bit :: resto => (if bit then (3 : ℤ) ^ unos resto else 0) + 2 * aditivo resto

theorem unos_append (a b : List Bool) : unos (a ++ b) = unos a + unos b := by
  induction a with
  | nil => simp [unos]
  | cons bit resto ih =>
    cases bit <;> simp [unos, ih, Nat.add_assoc]

theorem aditivo_append (a b : List Bool) :
    aditivo (a ++ b) = (3 : ℤ) ^ unos b * aditivo a + 2 ^ a.length * aditivo b := by
  induction a with
  | nil => simp [aditivo]
  | cons bit resto ih =>
    cases bit <;> simp [aditivo, unos_append, ih, pow_add, pow_succ] <;> ring

theorem intercambio_aditivo (a b : List Bool) :
    aditivo (a ++ [false, true] ++ b) - aditivo (a ++ [true, false] ++ b) =
      2 ^ a.length * (3 : ℤ) ^ unos b := by
  simp [aditivo_append, aditivo, unos]
  ring

theorem intercambio_margen (D r B e h c H Q : ℤ) :
    D * (r + e * h - c * e * H) - (B - e * Q) - (D * r - B) =
      e * (D * (h - c * H) + Q) := by
  ring

theorem sin_acarreo {D e h Q : ℤ} (hD : 0 < D) (he : 0 < e)
    (hh : 0 < h) (hQ : 0 < Q) : 0 < e * (D * h + Q) := by
  exact mul_pos he (add_pos (mul_pos hD hh) hQ)

theorem con_acarreo {D e h H Q : ℤ} (he : 0 < e) :
    e * (D * (h - H) + Q) ≤ 0 ↔ Q ≤ D * (H - h) := by
  constructor <;> intro hsigno <;> nlinarith

theorem criterio_residuo (A B r M : ℤ) :
    (A * r + B) % M = 0 ↔ ∃ z : ℤ, A * r + B = M * z := by
  rw [← Int.dvd_iff_emod_eq_zero]
  exact dvd_def

theorem intercambio_residuo (P Q e H B r h c z t : ℤ)
    (hcong : P * Q * r + B = e * H * z) (hinv : P * h = 1 + t * H) :
    P * Q * (r + e * h - c * e * H) + (B - e * Q) =
      e * H * (z + Q * t - P * Q * c) := by
  linear_combination hcong + e * Q * hinv

theorem criterio_margen {M A B u v : ℤ} (hM : 0 < M)
    (hafin : M * v = A * u + B) : u ≤ v ↔ (M - A) * u ≤ B := by
  constructor <;> intro h <;> nlinarith

theorem relleno_aditivo (k : ℕ) (w : List Bool) :
    aditivo (List.replicate k false ++ w) = (2 : ℤ) ^ k * aditivo w := by
  induction k with
  | zero => simp
  | succ k ih => simp [List.replicate_succ, aditivo, ih, pow_succ]; ring

theorem relleno_congruencia {e M A B n : ℤ} (he : e ≠ 0) :
    (e * M ∣ A * (e * n) + e * B) ↔ (M ∣ A * n + B) := by
  have h : A * (e * n) + e * B = e * (A * n + B) := by ring
  rw [h]
  exact mul_dvd_mul_iff_left he

theorem relleno_margen {e M A B n : ℤ} (he : 0 < e) :
    (e * M - A) * (e * n) ≤ e * B ↔ (e * M - A) * n ≤ B := by
  have h : (e * M - A) * (e * n) = e * ((e * M - A) * n) := by ring
  rw [h, mul_le_mul_iff_right₀ he]

def paso (n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

def palabra : ℕ → ℕ → List Bool
  | 0, _ => []
  | k + 1, n => decide (n % 2 = 1) :: palabra k (paso n)

/-- Control independiente por evaluación del mapa; no usa la inversa modular. -/
theorem testigos_intercambio :
    palabra 8 188 = [false, false, true, true, true, true, false, true] ∧
    palabra 8 18 = [false, true, false, true, true, true, false, true] ∧
    palabra 8 189 = [true, false, false, true, true, true, false, true] ∧
    paso^[8] 188 = 182 ∧ paso^[8] 18 = 20 ∧ paso^[8] 189 = 182 ∧
    3 ^ 5 < (2 : ℕ) ^ 8 := by
  decide

end Jinetas

#print axioms Jinetas.unos_append
#print axioms Jinetas.aditivo_append
#print axioms Jinetas.intercambio_aditivo
#print axioms Jinetas.intercambio_margen
#print axioms Jinetas.sin_acarreo
#print axioms Jinetas.con_acarreo
#print axioms Jinetas.criterio_residuo
#print axioms Jinetas.intercambio_residuo
#print axioms Jinetas.criterio_margen
#print axioms Jinetas.relleno_aditivo
#print axioms Jinetas.relleno_congruencia
#print axioms Jinetas.relleno_margen
#print axioms Jinetas.testigos_intercambio
