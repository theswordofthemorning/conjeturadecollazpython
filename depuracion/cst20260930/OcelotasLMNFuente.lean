import OcelotasLMN

/-! # Ocelotas: del corolario publicado de LMN a la hipótesis usada

Fuente cotejada visualmente: Laurent–Mignotte–Nesterenko (1995), p. 288,
corolario 2. Se especializa con α₁ = 3, α₂ = 2, b₁ = q, b₂ = k, D = 1,
log A₁ = log 3 y log A₂ = 1. Los números 2 y 3 son multiplicativamente
independientes. La especialización es la hipótesis externa `LMN23`;
el teorema trascendente general no se formaliza aquí.

Se conservan el máximo, el término 0,14 y la constante 24,34 publicados.
El resto de la traducción, incluida la positividad de q, lo prueba Lean.
-/

namespace OcelotasLMNFuente

open Real Ocelotas OcelotasContador OcelotasLMN

/-- Corolario 2 de LMN especializado en 3 y 2, con coeficientes positivos. -/
def LMN23 : Prop :=
  ∀ k q : ℕ, 0 < k → 0 < q →
    -(24.34 * (max (log ((q : ℝ) + k / log 3) + 0.14)
      (max 21 (1 / 2))) ^ 2 * log 3) ≤
        log |(k : ℝ) * log 2 - q * log 3|

/-- La forma débil usada en la cadena se deduce de la especialización literal. -/
theorem debil_de_corolario (hL : LMN23) : LMNDebil := by
  intro k q hk hv hlt
  have hkR : (2 : ℝ) ≤ k := by exact_mod_cast hk
  have hqk : q < k := by
    have h2q : 2 ^ q ≤ 3 ^ q := Nat.pow_le_pow_left (by norm_num) q
    exact (Nat.pow_lt_pow_iff_right (by norm_num)).1 (lt_of_le_of_lt h2q hlt)
  have hq : 0 < q := by
    by_contra h
    have hq0 : q = 0 := by omega
    have h4 : (2 : ℕ) ^ 2 ≤ 2 ^ k := Nat.pow_le_pow_right (by norm_num) hk
    simp only [hq0, pow_zero, mul_one] at hv
    norm_num at h4
    omega
  have hqR : (0 : ℝ) < q := by exact_mod_cast hq
  have hqkR : (q : ℝ) < k := by exact_mod_cast hqk
  have h3 := log_tres_cotas
  have h31 : (1 : ℝ) < log 3 := by linarith [h3.1]
  have h3pos : (0 : ℝ) < log 3 := by linarith
  have hcoef : (24.34 : ℝ) * log 3 ≤ 27 := by linarith [h3.2]
  have hdiv : (k : ℝ) / log 3 ≤ k := by
    apply (div_le_iff₀ h3pos).2
    nlinarith
  have hbpos : (0 : ℝ) < q + k / log 3 := by positivity
  have hb : (q : ℝ) + k / log 3 ≤ 2 * k := by linarith
  have hlog := Real.log_le_log hbpos hb
  have hlog0 : (0 : ℝ) ≤ log (2 * (k : ℝ)) := Real.log_nonneg (by linarith)
  set M : ℝ := max (log ((q : ℝ) + k / log 3) + 0.14) (max 21 (1 / 2))
  have hMpos : 0 ≤ M := by
    dsimp [M]
    exact le_trans (by norm_num : (0 : ℝ) ≤ 21)
      (le_trans (le_max_left _ _) (le_max_right _ _))
  have hM : M ≤ log (2 * (k : ℝ)) + 21 := by
    dsimp [M]
    apply max_le
    · linarith
    · apply max_le <;> linarith
  have hsquare : M ^ 2 ≤ (log (2 * (k : ℝ)) + 21) ^ 2 := by nlinarith
  have hproduct : 24.34 * M ^ 2 * log 3 ≤ 27 * (log (2 * (k : ℝ)) + 21) ^ 2 := by
    calc
      24.34 * M ^ 2 * log 3 = (24.34 * log 3) * M ^ 2 := by ring
      _ ≤ 27 * M ^ 2 := mul_le_mul_of_nonneg_right hcoef (sq_nonneg M)
      _ ≤ 27 * (log (2 * (k : ℝ)) + 21) ^ 2 := by linarith
  have hLambda := lambda_pos hlt
  have hpublicada := hL k q (by omega) hq
  rw [abs_of_pos hLambda] at hpublicada
  have hdebil : -(27 * (log (2 * (k : ℝ)) + 21) ^ 2) ≤
      log ((k : ℝ) * log 2 - q * log 3) := by
    change -(24.34 * M ^ 2 * log 3) ≤ _ at hpublicada
    linarith
  have hexp := Real.exp_le_exp.mpr hdebil
  rwa [Real.exp_log hLambda] at hexp

/-- CST hasta diez rachas bajo el corolario publicado especializado. -/
theorem cst_corolario (hL : LMN23) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 10) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n :=
  cst_lmn (debil_de_corolario hL) hn hk hr

end OcelotasLMNFuente

#print axioms OcelotasLMNFuente.debil_de_corolario
#print axioms OcelotasLMNFuente.cst_corolario
