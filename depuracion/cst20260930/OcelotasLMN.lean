import OcelotasContador
import Mathlib.Analysis.Complex.ExponentialBounds

/-! # Ocelotas sin Rhin: convergentes de log2 3 y Laurent–Mignotte–Nesterenko

La cadena de diez rachas necesitaba Rhin para excluir `q > 82696`. Aquí se
excluyen `82696 < q < 53715833` con los convergentes 11 a 16 de `log2 3` y el
teorema de Lagrange (pares unimodulares de signos opuestos), y el resto con
una forma debilitada de la cota de Laurent, Mignotte y Nesterenko (1995):
`k log 2 − q log 3 ≥ exp(−27 (log(2k) + 21)^2)`. La criba ya certificada
cubre `q ≤ 82696` sin cambios.
-/

namespace OcelotasLMN

open Real Ocelotas OcelotasRachas OcelotasTrayectorias OcelotasFinito OcelotasCertificado
  OcelotasCierre OcelotasContador

/-! ## Logaritmos con veinte cifras (serie de `log (1 - x)`) -/

theorem log_dos_cotas :
    (0.693147180559945309362 : ℝ) < log 2 ∧ log 2 < 0.693147180559945309471 := by
  have t : |(2⁻¹ : ℝ)| = 2⁻¹ := by rw [abs_of_pos]; norm_num
  have z := Real.abs_log_sub_add_sum_range_le (show |(2⁻¹ : ℝ)| < 1 by rw [t]; norm_num) 64
  rw [t] at z
  norm_num1 at z
  rw [one_div (2 : ℝ), log_inv, ← sub_eq_add_neg] at z
  have h := abs_le.1 z
  constructor <;> linarith [h.1, h.2]

theorem log_tres_cotas :
    (1.098612288668109691335 : ℝ) < log 3 ∧ log 3 < 1.098612288668109691454 := by
  have t : |(3⁻¹ : ℝ)| = 3⁻¹ := by rw [abs_of_pos]; norm_num
  have z := Real.abs_log_sub_add_sum_range_le (show |(3⁻¹ : ℝ)| < 1 by rw [t]; norm_num) 42
  rw [t] at z
  norm_num1 at z
  have hd : log (2 / 3 : ℝ) = log 2 - log 3 := Real.log_div (by norm_num) (by norm_num)
  rw [hd] at z
  have h := abs_le.1 z
  have h2 := log_dos_cotas
  constructor <;> linarith [h.1, h.2, h2.1, h2.2]

/-! ## La forma lineal y el teorema de Lagrange -/

/-- `L a b = a log 2 − b log 3`. -/
noncomputable def L (a b : ℤ) : ℝ := (a : ℝ) * log 2 - (b : ℝ) * log 3

theorem L_comb (u v a b c d : ℤ) :
    L (u * a + v * c) (u * b + v * d) = u * L a b + v * L c d := by
  unfold L
  push_cast
  ring

/-- Lagrange para dos convergentes consecutivos: si `(P1, Q1)` y `(P2, Q2)` son
unimodulares y `L` toma en ellos signos opuestos, ningún `0 < q < Q2` mejora a `(P1, Q1)`. -/
theorem lagrange {P1 Q1 P2 Q2 : ℤ} (hQ1 : 0 < Q1)
    (hdet : P2 * Q1 - P1 * Q2 = 1 ∨ P2 * Q1 - P1 * Q2 = -1)
    (hsig : L P1 Q1 * L P2 Q2 < 0) {k q : ℤ} (hq : 0 < q) (hqQ : q < Q2) :
    |L P1 Q1| ≤ |L k q| := by
  set D := P2 * Q1 - P1 * Q2 with hD
  have hDD : D * D = 1 := by rcases hdet with h | h <;> rw [h] <;> norm_num
  set u := D * (q * P2 - k * Q2) with hu
  set v := D * (k * Q1 - q * P1) with hv
  have hk : k = u * P1 + v * P2 := by
    have : u * P1 + v * P2 = (D * D) * k := by rw [hu, hv, hD]; ring
    rw [this, hDD, one_mul]
  have hqq : q = u * Q1 + v * Q2 := by
    have : u * Q1 + v * Q2 = (D * D) * q := by rw [hu, hv, hD]; ring
    rw [this, hDD, one_mul]
  have hL : L k q = u * L P1 Q1 + v * L P2 Q2 := by rw [hk, hqq, L_comb]
  rw [hL]
  have hQ2 : 0 < Q2 := lt_trans hq hqQ
  rcases lt_trichotomy v 0 with hv0 | hv0 | hv0
  · -- v < 0: entonces u > 0
    have hu0 : 0 < u := by
      by_contra h
      rw [not_lt] at h
      have : u * Q1 + v * Q2 < 0 := by nlinarith
      omega
    have hur : (1 : ℝ) ≤ u := by exact_mod_cast hu0
    have hvr : (v : ℝ) ≤ -1 := by exact_mod_cast (show v ≤ -1 by omega)
    rcases lt_or_gt_of_ne (show L P1 Q1 ≠ 0 by intro h; rw [h, zero_mul] at hsig; exact lt_irrefl 0 hsig)
      with h1 | h1
    · have h2 : 0 < L P2 Q2 := by nlinarith
      rw [abs_of_neg h1, abs_of_neg (by nlinarith)]
      nlinarith
    · have h2 : L P2 Q2 < 0 := by nlinarith
      rw [abs_of_pos h1, abs_of_pos (by nlinarith)]
      nlinarith
  · -- v = 0: q = u Q1 con u ≥ 1
    have hu0 : 0 < u := by
      rw [hv0, zero_mul, add_zero] at hqq
      by_contra h
      rw [not_lt] at h
      nlinarith
    have hur : (1 : ℝ) ≤ u := by exact_mod_cast hu0
    rw [hv0]
    push_cast
    rw [zero_mul, add_zero, abs_mul, abs_of_pos (by linarith : (0 : ℝ) < u)]
    nlinarith [abs_nonneg (L P1 Q1)]
  · -- v > 0: entonces u < 0
    have hu0 : u < 0 := by
      by_contra h
      rw [not_lt] at h
      have : Q2 ≤ u * Q1 + v * Q2 := by nlinarith
      omega
    have hur : (u : ℝ) ≤ -1 := by exact_mod_cast (show u ≤ -1 by omega)
    have hvr : (1 : ℝ) ≤ v := by exact_mod_cast hv0
    rcases lt_or_gt_of_ne (show L P1 Q1 ≠ 0 by intro h; rw [h, zero_mul] at hsig; exact lt_irrefl 0 hsig)
      with h1 | h1
    · have h2 : 0 < L P2 Q2 := by nlinarith
      rw [abs_of_neg h1, abs_of_pos (by nlinarith)]
      nlinarith
    · have h2 : L P2 Q2 < 0 := by nlinarith
      rw [abs_of_pos h1, abs_of_neg (by nlinarith)]
      nlinarith

/-! ## Los convergentes 11 a 16 de log2 3 -/

theorem L11 : (1 / 10 ^ 8 : ℝ) < L 125743 79335 := by
  unfold L; have h2 := log_dos_cotas; have h3 := log_tres_cotas; push_cast; linarith [h2.1, h3.2]
theorem L12 : L 176251 111202 < -(1 / 10 ^ 8 : ℝ) := by
  unfold L; have h2 := log_dos_cotas; have h3 := log_tres_cotas; push_cast; linarith [h2.2, h3.1]
theorem L13 : (1 / 10 ^ 8 : ℝ) < L 301994 190537 := by
  unfold L; have h2 := log_dos_cotas; have h3 := log_tres_cotas; push_cast; linarith [h2.1, h3.2]
theorem L14 : L 16785921 10590737 < -(1 / 10 ^ 8 : ℝ) := by
  unfold L; have h2 := log_dos_cotas; have h3 := log_tres_cotas; push_cast; linarith [h2.2, h3.1]
theorem L15 : (1 / 10 ^ 8 : ℝ) < L 17087915 10781274 := by
  unfold L; have h2 := log_dos_cotas; have h3 := log_tres_cotas; push_cast; linarith [h2.1, h3.2]
theorem L16 : L 85137581 53715833 < 0 := by
  unfold L; have h2 := log_dos_cotas; have h3 := log_tres_cotas; push_cast; linarith [h2.2, h3.1]

/-- Para `0 < q < 53715833`, `|L k q|` es al menos `10^-8`. -/
theorem L_intervalos {k q : ℤ} (hq : 0 < q) (hqQ : q < 53715833) :
    (1 / 10 ^ 8 : ℝ) < |L k q| := by
  have c11 := L11; have c12 := L12; have c13 := L13
  have c14 := L14; have c15 := L15; have c16 := L16
  by_cases h12 : q < 111202
  · have := lagrange (P1 := 125743) (Q1 := 79335) (P2 := 176251) (Q2 := 111202) (by norm_num)
      (by norm_num) (by nlinarith) (k := k) hq h12
    rw [abs_of_pos (by linarith)] at this
    linarith
  by_cases h13 : q < 190537
  · have := lagrange (P1 := 176251) (Q1 := 111202) (P2 := 301994) (Q2 := 190537) (by norm_num)
      (by norm_num) (by nlinarith) (k := k) hq h13
    rw [abs_of_neg (by linarith)] at this
    linarith
  by_cases h14 : q < 10590737
  · have := lagrange (P1 := 301994) (Q1 := 190537) (P2 := 16785921) (Q2 := 10590737) (by norm_num)
      (by norm_num) (by nlinarith) (k := k) hq h14
    rw [abs_of_pos (by linarith)] at this
    linarith
  by_cases h15 : q < 10781274
  · have := lagrange (P1 := 16785921) (Q1 := 10590737) (P2 := 17087915) (Q2 := 10781274) (by norm_num)
      (by norm_num) (by nlinarith) (k := k) hq h15
    rw [abs_of_neg (by linarith)] at this
    linarith
  · have := lagrange (P1 := 17087915) (Q1 := 10781274) (P2 := 85137581) (Q2 := 53715833) (by norm_num)
      (by norm_num) (by nlinarith) (k := k) hq hqQ
    rw [abs_of_pos (by linarith)] at this
    linarith

/-! ## De una cota real de `Λ` a la forma entera -/

theorem lambda_pos {k q : ℕ} (hlt : 3 ^ q < 2 ^ k) : 0 < (k : ℝ) * log 2 - q * log 3 := by
  have hpos3 : (0 : ℝ) < (3 : ℝ) ^ q := by positivity
  have hltR : (3 : ℝ) ^ q < (2 : ℝ) ^ k := by exact_mod_cast hlt
  have hlog := Real.log_lt_log hpos3 hltR
  rw [Real.log_pow, Real.log_pow] at hlog
  linarith

/-- Si `Λ ≥ 1/N`, entonces `3^q ≤ (2^k − 3^q) N`, porque `Δ/3^q = e^Λ − 1 ≥ Λ`. -/
theorem entera_de_cota {k q N : ℕ} (hN : 0 < N) (hlt : 3 ^ q < 2 ^ k)
    (hc : (1 : ℝ) / N ≤ (k : ℝ) * log 2 - q * log 3) : 3 ^ q ≤ (2 ^ k - 3 ^ q) * N := by
  set Λ := (k : ℝ) * log 2 - q * log 3 with hΛ
  have hpos3 : (0 : ℝ) < (3 : ℝ) ^ q := by positivity
  have hpos2 : (0 : ℝ) < (2 : ℝ) ^ k := by positivity
  have hexp : Real.exp Λ = (2 : ℝ) ^ k / (3 : ℝ) ^ q := by
    have hL' : Λ = Real.log ((2 : ℝ) ^ k) - Real.log ((3 : ℝ) ^ q) := by
      rw [Real.log_pow, Real.log_pow, hΛ]
    rw [hL', Real.exp_sub, Real.exp_log hpos2, Real.exp_log hpos3]
  have h1 : Λ + 1 ≤ Real.exp Λ := Real.add_one_le_exp Λ
  have hNpos : (0 : ℝ) < N := by exact_mod_cast hN
  have hclave : (1 : ℝ) / N ≤ (2 : ℝ) ^ k / (3 : ℝ) ^ q - 1 := by rw [← hexp]; linarith
  rw [div_sub_one (ne_of_gt hpos3), div_le_div_iff₀ hNpos hpos3] at hclave
  have hcast : (((2 ^ k - 3 ^ q) * N : ℕ) : ℝ) = ((2 : ℝ) ^ k - (3 : ℝ) ^ q) * N := by
    rw [Nat.cast_mul, Nat.cast_sub hlt.le]
    push_cast
    ring
  have hfin : ((3 ^ q : ℕ) : ℝ) ≤ (((2 ^ k - 3 ^ q) * N : ℕ) : ℝ) := by
    rw [hcast]
    push_cast
    linarith
  exact_mod_cast hfin

/-- Para `0 < q < 53715833`, la forma entera con `N = 10^8`, sin Rhin. -/
theorem cota_intervalo {k q : ℕ} (hlt : 3 ^ q < 2 ^ k) (hq : 0 < q) (hqQ : q < 53715833) :
    3 ^ q ≤ (2 ^ k - 3 ^ q) * 10 ^ 8 := by
  apply entera_de_cota (by norm_num) hlt
  have h := L_intervalos (k := (k : ℤ)) (q := (q : ℤ)) (by exact_mod_cast hq)
    (by exact_mod_cast hqQ)
  have hp := lambda_pos hlt
  unfold L at h
  push_cast at h
  rw [abs_of_pos hp] at h
  push_cast
  linarith

/-! ## La cola: forma debilitada de Laurent–Mignotte–Nesterenko -/

/-- Implicada por el corolario 2 de Laurent, Mignotte y Nesterenko (1995) para `2` y `3`:
`log Λ ≥ −24,34 log 3 (max(log b' + 0,14, 21))^2`, con `b' ≤ 2k`. -/
def LMNDebil : Prop :=
  ∀ k q : ℕ, 2 ≤ k → 2 ^ k ≤ 2 * 3 ^ q → 3 ^ q < 2 ^ k →
    Real.exp (-(27 * (Real.log (2 * k) + 21) ^ 2)) ≤ (k : ℝ) * log 2 - q * log 3

theorem cola_lmn_entera (hL : LMNDebil) {k q t : ℕ} (hk2 : 2 ≤ k) (hv : 2 ^ k ≤ 2 * 3 ^ q)
    (hlt : 3 ^ q < 2 ^ k) (ht : k < 2 ^ (t + 1)) :
    3 ^ q ≤ (2 ^ k - 3 ^ q) * 2 ^ (19 * (t + 33) ^ 2) := by
  apply entera_de_cota (by positivity) hlt
  have h := hL k q hk2 hv hlt
  have hl2 := log_dos_cotas
  have hkR : (2 : ℝ) ≤ k := by exact_mod_cast hk2
  have hpos : (0 : ℝ) < 2 * k := by positivity
  have h2k : ((2 * k : ℕ) : ℝ) < ((2 ^ (t + 2) : ℕ) : ℝ) := by
    have : 2 * k < 2 ^ (t + 2) := by rw [pow_succ]; omega
    exact_mod_cast this
  push_cast at h2k
  have hlog : Real.log (2 * k) < (t + 2) * log 2 := by
    calc Real.log (2 * k) < Real.log ((2 : ℝ) ^ (t + 2)) := Real.log_lt_log hpos h2k
      _ = (t + 2) * log 2 := by rw [Real.log_pow]; push_cast; ring
  have hlog0 : 0 ≤ Real.log (2 * k) := Real.log_nonneg (by linarith)
  have hx1 : Real.log (2 * k) + 21 ≤ log 2 * (t + 33) := by nlinarith [hl2.1]
  have hx0 : 0 ≤ Real.log (2 * k) + 21 := by linarith
  have hsq : (Real.log (2 * k) + 21) ^ 2 ≤ (log 2 * (t + 33)) ^ 2 :=
    pow_le_pow_left₀ hx0 hx1 2
  have ht0 : (0 : ℝ) ≤ (t : ℝ) + 33 := by positivity
  have hX : 27 * (Real.log (2 * k) + 21) ^ 2 ≤ ((19 * (t + 33) ^ 2 : ℕ) : ℝ) * log 2 := by
    push_cast
    have : (log 2 * (t + 33)) ^ 2 = log 2 * (log 2 * (t + 33) ^ 2) := by ring
    nlinarith [hl2.1, hl2.2, sq_nonneg ((t : ℝ) + 33)]
  have hM : Real.exp (-(((19 * (t + 33) ^ 2 : ℕ) : ℝ) * log 2)) =
      1 / (((2 ^ (19 * (t + 33) ^ 2) : ℕ) : ℝ)) := by
    rw [Real.exp_neg, Real.exp_nat_mul, Real.exp_log (by norm_num)]
    push_cast
    rw [one_div]
  calc (1 : ℝ) / (((2 ^ (19 * (t + 33) ^ 2) : ℕ) : ℝ))
      = Real.exp (-(((19 * (t + 33) ^ 2 : ℕ) : ℝ) * log 2)) := hM.symm
    _ ≤ Real.exp (-(27 * (Real.log (2 * k) + 21) ^ 2)) := Real.exp_le_exp.2 (by linarith)
    _ ≤ _ := h

theorem cola_diez_lmn (t : ℕ) (ht : 25 ≤ t) : 364 * (19 * (t + 33) ^ 2 + 5) < 2 ^ t := by
  induction t, ht using Nat.le_induction with
  | base => norm_num
  | succ t ht ih =>
    rw [pow_succ 2 t]
    have : 19 * (t + 1 + 33) ^ 2 + 5 ≤ 2 * (19 * (t + 33) ^ 2 + 5) := by nlinarith
    omega

/-! ## La cadena de diez rachas sin Rhin -/

theorem impares_pos {n r : ℕ} {a b : ℕ → ℕ} (hw : Palabra n a b r) (hr : 0 < r) :
    0 < S (tiempo a b r) n := by
  rw [cuenta_impares hw r le_rfl]
  have ha := (hw 0 hr).1
  have hs := cuenta_impares hw 1 (by omega)
  have ht := tiempo_mono a b (show 1 ≤ r by omega)
  have hsum := S_add (tiempo a b 1) (tiempo a b r - tiempo a b 1) n
  rw [Nat.add_sub_of_le ht] at hsum
  rw [cuenta_impares hw r le_rfl, hs] at hsum
  simp only [acumulados] at hsum
  omega

theorem sin_fallo_intervalo {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr10 : r ≤ 10)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hq1 : 82696 < S (tiempo a b r) n) (hq2 : S (tiempo a b r) n < 53715833) : False := by
  have he := cota_intervalo hk.2 (by omega) hq2
  have hp := fallo_producto hw hr hk hf
  have hn : n < 1000000000 := by
    have h1 : (2 ^ tiempo a b r - 3 ^ S (tiempo a b r) n) * n <
        (2 ^ tiempo a b r - 3 ^ S (tiempo a b r) n) * 1000000000 := by
      calc _ < r * 3 ^ S (tiempo a b r) n := hp
        _ ≤ 10 * 3 ^ S (tiempo a b r) n := Nat.mul_le_mul_right _ hr10
        _ ≤ 10 * ((2 ^ tiempo a b r - 3 ^ S (tiempo a b r) n) * 10 ^ 8) :=
          Nat.mul_le_mul_left _ he
        _ = _ := by ring
    exact Nat.lt_of_mul_lt_mul_left h1
  have h30 : (2 : ℕ) ^ 30 = 1073741824 := by norm_num
  have hn2 : n + 1 < 2 ^ 30 := by omega
  have hc := criba_desde_trayectoria hw hn2
  have hcm := cota_monotona (by norm_num : 1 ≤ 30) hr10
  have hval : cota 10 30 = 5317 := by decide
  omega

theorem sin_fallo_cola (hL : LMNDebil) {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr10 : r ≤ 10)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hk25 : 2 ^ 25 ≤ tiempo a b r) : False := by
  have hk0 : 0 < tiempo a b r := by positivity
  have hlo : 2 ^ Nat.log 2 (tiempo a b r) ≤ tiempo a b r := Nat.pow_log_le_self 2 (by omega)
  have hhi : tiempo a b r < 2 ^ (Nat.log 2 (tiempo a b r) + 1) :=
    Nat.lt_pow_succ_log_self (by decide) _
  have ht25 : 25 ≤ Nat.log 2 (tiempo a b r) := Nat.le_log_of_pow_le (by decide) hk25
  have h25 : (2 : ℕ) ^ 25 = 33554432 := by norm_num
  have he := cola_lmn_entera hL (by omega) (ventana_cruce hk).2 hk.2 hhi
  have hp := fallo_producto hw hr hk hf
  have hn : n < 16 * 2 ^ (19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2) := by
    have h1 : (2 ^ tiempo a b r - 3 ^ S (tiempo a b r) n) * n <
        (2 ^ tiempo a b r - 3 ^ S (tiempo a b r) n) *
          (16 * 2 ^ (19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2)) := by
      calc _ < r * 3 ^ S (tiempo a b r) n := hp
        _ ≤ 10 * 3 ^ S (tiempo a b r) n := Nat.mul_le_mul_right _ hr10
        _ ≤ 10 * ((2 ^ tiempo a b r - 3 ^ S (tiempo a b r) n) *
              2 ^ (19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2)) := Nat.mul_le_mul_left _ he
        _ ≤ 16 * ((2 ^ tiempo a b r - 3 ^ S (tiempo a b r) n) *
              2 ^ (19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2)) :=
          Nat.mul_le_mul_right _ (by norm_num)
        _ = _ := Nat.mul_left_comm _ _ _
    exact Nat.lt_of_mul_lt_mul_left h1
  have hn2 : n + 1 < 2 ^ (19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2 + 5) := by
    rw [pow_add]
    omega
  have hc := criba_desde_trayectoria hw hn2
  have hcm := cota_monotona (by omega : 1 ≤ 19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2 + 5) hr10
  have hd := cota_diez_lineal (19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2 + 5)
  have hki := tiempo_por_impares (impares_pos hw hr) (ventana_cruce hk).2
  have hcola := cola_diez_lmn (Nat.log 2 (tiempo a b r)) ht25
  omega

/-- **Ocelotas sin Rhin.** Descenso para palabras de una a diez rachas, bajo la forma
debilitada de Laurent–Mignotte–Nesterenko. -/
theorem ocelotas_diez_lmn (hL : LMNDebil) {n r : ℕ} {a b : ℕ → ℕ}
    (hn : 2 ≤ n) (hw : Palabra n a b r) (hr : 0 < r) (hr10 : r ≤ 10)
    (hk : PrimerCruce n (tiempo a b r)) : T^[tiempo a b r] n < n := by
  by_contra hdesc
  have hf : n ≤ T^[tiempo a b r] n := by omega
  let k := tiempo a b r
  let q := S k n
  have hk2 : 2 ≤ k := by
    have ha := (hw 0 hr).1
    have hb := (hw 0 hr).2.1
    have ht := tiempo_mono a b (show 1 ≤ r by omega)
    simp only [tiempo] at ht
    dsimp [k]
    omega
  have hkd : k = Nat.log2 (3 ^ q) + 1 := k_de_q (ventana_estricta hk hk2) hk.2
  have hq1 : 1 ≤ q := by
    by_contra h
    have hq0 : q = 0 := by omega
    simp only [hq0, pow_zero, show Nat.log2 1 = 0 from rfl] at hkd
    omega
  by_cases hqmax : q ≤ 82696
  · have hc := criba_certificada q hq1 hqmax
    simp only [CertificadoAritmetico] at hc
    rw [← hkd] at hc
    rcases hc with hsemilla | hfuera
    · have hp := fallo_producto hw hr hk hf
      have hrP := Nat.mul_le_mul_right (3 ^ q) hr10
      change (2 ^ k - 3 ^ q) * n < r * 3 ^ q at hp
      have hnsmall : n < 11215 := Nat.lt_of_mul_lt_mul_left
        (show (2 ^ k - 3 ^ q) * n < (2 ^ k - 3 ^ q) * 11215 by nlinarith)
      exact hdesc (descenso_finito hn (by omega) hk)
    · have hcribado : q ≤ cota 10 ((q - 1) / 182) :=
        criba_fallo hw hr hr10 hk hf hfuera
      have hlineal := cota_diez_lineal ((q - 1) / 182)
      omega
  · by_cases hqm : q < 53715833
    · exact sin_fallo_intervalo hw hr hr10 hk hf (Nat.lt_of_not_le hqmax) hqm
    · have h2q : 2 ^ q ≤ 3 ^ q := Nat.pow_le_pow_left (by norm_num) q
      have hqk : q < k := by
        have : 2 ^ q < 2 ^ k := lt_of_le_of_lt h2q hk.2
        exact (Nat.pow_lt_pow_iff_right (by norm_num)).1 this
      have h25 : (2 : ℕ) ^ 25 = 33554432 := by norm_num
      exact sin_fallo_cola hL hw hr hr10 hk hf (by omega)

theorem descenso_contador_lmn (hL : LMNDebil) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 10) : T^[k] n < n := by
  by_cases hpar : n % 2 = 0
  · exact descenso_par hn hpar hk
  · obtain ⟨hpos, a, b, hw, he⟩ := palabra_del_cruce (by omega : n % 2 = 1) hk
    have hh := ocelotas_diez_lmn hL hn hw hpos hr
    rw [he] at hh
    exact hh hk

/-- **CST hasta diez rachas sin Rhin**, bajo la forma debilitada de Laurent, Mignotte y
Nesterenko (1995): primer descenso = primer cruce del coeficiente. -/
theorem cst_lmn (hL : LMNDebil) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 10) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n :=
  ⟨fun _ hj => no_desciende_antes hk hj, descenso_contador_lmn hL hn hk hr⟩

theorem fallo_exige_once_lmn (hL : LMNDebil) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hf : n ≤ T^[k] n) : 11 ≤ rachas n k := by
  by_contra h
  have := descenso_contador_lmn hL hn hk (by omega : rachas n k ≤ 10)
  omega

end OcelotasLMN

#print axioms OcelotasLMN.log_dos_cotas
#print axioms OcelotasLMN.log_tres_cotas
#print axioms OcelotasLMN.lagrange
#print axioms OcelotasLMN.L_intervalos
#print axioms OcelotasLMN.entera_de_cota
#print axioms OcelotasLMN.cota_intervalo
#print axioms OcelotasLMN.cola_lmn_entera
#print axioms OcelotasLMN.sin_fallo_intervalo
#print axioms OcelotasLMN.sin_fallo_cola
#print axioms OcelotasLMN.ocelotas_diez_lmn
#print axioms OcelotasLMN.cst_lmn
#print axioms OcelotasLMN.fallo_exige_once_lmn
