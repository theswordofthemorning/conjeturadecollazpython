import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Algebra.Order.Floor.Semiring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-! # Ocelotas: criba logarítmica y aproximación por arriba

Lemas universales. No se certifican aquí las tablas Python ni el censo
de semillas. Los logaritmos son naturales; alfa y beta acotan exponentes
en base 2 mediante log 3 ≤ alfa * log 2 y log s ≤ beta * log 2.
-/

namespace OcelotasAfinada

open Real

noncomputable def cota (alfa beta : ℝ) : ℕ → ℕ
  | 0 => 0
  | i + 1 => Nat.floor (beta + alfa * cota alfa beta i)

theorem paso_real {n s p a : ℕ} {alfa beta : ℝ} (hs : 0 < s)
    (hn : n + 1 ≤ s) (hc : 2 ^ a ≤ (n + 1) * 3 ^ p)
    (halfa : log 3 ≤ alfa * log 2) (hbeta : log s ≤ beta * log 2) :
    (a : ℝ) ≤ beta + alfa * p := by
  have hpot : (2 : ℝ) ^ a ≤ (s : ℝ) * (3 : ℝ) ^ p := by
    exact_mod_cast le_trans hc (Nat.mul_le_mul_right (3 ^ p) hn)
  have hlog := Real.log_le_log (by positivity : (0 : ℝ) < (2 : ℝ) ^ a) hpot
  have hsR : (0 : ℝ) < s := by exact_mod_cast hs
  rw [Real.log_pow, Real.log_mul (ne_of_gt hsR) (by positivity), Real.log_pow] at hlog
  have hp : (0 : ℝ) ≤ p := by positivity
  have ha := mul_le_mul_of_nonneg_left halfa hp
  have h2 : (0 : ℝ) < log 2 := Real.log_pos (by norm_num)
  nlinarith

/-- La criba afinada para cualquier cadena que satisface las congruencias. -/
theorem criba_congruencias (A : ℕ → ℕ) {n s r : ℕ} {alfa beta : ℝ}
    (hs : 0 < s) (hn : n + 1 ≤ s) (h0 : A 0 = 0) (ha : 0 ≤ alfa)
    (halfa : log 3 ≤ alfa * log 2) (hbeta : log s ≤ beta * log 2)
    (hc : ∀ i, i < r → 2 ^ A (i + 1) ≤ (n + 1) * 3 ^ A i) :
    A r ≤ cota alfa beta r := by
  induction r with
  | zero => simp [cota, h0]
  | succ r ih =>
    have hprev := ih (fun i hi => hc i (by omega))
    have hp := paso_real hs hn (hc r (by omega)) halfa hbeta
    have hprevR : (A r : ℝ) ≤ cota alfa beta r := by exact_mod_cast hprev
    have hmul := mul_le_mul_of_nonneg_left hprevR ha
    simp only [cota]
    apply Nat.le_floor
    linarith

theorem cota_monotona {alfa beta : ℝ} (ha : 1 ≤ alfa) (hb : 0 ≤ beta) :
    Monotone (cota alfa beta) := by
  apply monotone_nat_of_le_succ
  intro i
  change cota alfa beta i ≤ Nat.floor (beta + alfa * cota alfa beta i)
  apply Nat.le_floor
  have hn : (0 : ℝ) ≤ cota alfa beta i := by positivity
  nlinarith

/-- Un par unimodular que encierra una pendiente controla su error por arriba.
Para U=(P,Q), V=(p,q), L(U)>0>L(V), ningún denominador positivo menor
que Q+q tiene error positivo menor que L(U). No exige convergentes. -/
theorem aproximacion_superior {x y : ℝ} {P Q p q k b : ℤ}
    (hQ : 0 < Q) (hq : 0 < q) (hdet : P * q - p * Q = 1)
    (hU : 0 < P * x - Q * y) (hV : p * x - q * y < 0)
    (hb : 0 < b) (hfin : b < Q + q) (hL : 0 < k * x - b * y) :
    P * x - Q * y ≤ k * x - b * y := by
  set u : ℤ := k * q - p * b with hu
  set v : ℤ := P * b - k * Q with hv
  have hk : k = u * P + v * p := by
    have he : u * P + v * p = k * (P * q - p * Q) := by rw [hu, hv]; ring
    rw [he, hdet, mul_one]
  have hbb : b = u * Q + v * q := by
    have he : u * Q + v * q = b * (P * q - p * Q) := by rw [hu, hv]; ring
    rw [he, hdet, mul_one]
  have he : (k : ℝ) * x - b * y =
      u * ((P : ℝ) * x - Q * y) + v * ((p : ℝ) * x - q * y) := by
    conv_lhs => rw [hk, hbb]
    push_cast
    ring
  have hu_pos : 0 < u := by
    by_contra hu_nonpos
    have hu0 : u ≤ 0 := by omega
    have hvpos : 0 < v := by
      by_contra hv_nonpos
      have : v ≤ 0 := by omega
      nlinarith
    have huR : (u : ℝ) ≤ 0 := by exact_mod_cast hu0
    have hvR : (0 : ℝ) < v := by exact_mod_cast hvpos
    have hm1 := mul_nonpos_of_nonpos_of_nonneg huR hU.le
    have hm2 := mul_neg_of_pos_of_neg hvR hV
    linarith
  have hv_nonpos : v ≤ 0 := by
    by_contra h
    have hvpos : 1 ≤ v := by omega
    have hu1 : 1 ≤ u := by omega
    nlinarith
  have huR : (1 : ℝ) ≤ u := by exact_mod_cast hu_pos
  have hvR : (v : ℝ) ≤ 0 := by exact_mod_cast hv_nonpos
  have hm1 := mul_le_mul_of_nonneg_right huR hU.le
  have hm2 := mul_nonneg_of_nonpos_of_nonpos hvR hV.le
  linarith

end OcelotasAfinada

#print axioms OcelotasAfinada.paso_real
#print axioms OcelotasAfinada.criba_congruencias
#print axioms OcelotasAfinada.cota_monotona
#print axioms OcelotasAfinada.aproximacion_superior
