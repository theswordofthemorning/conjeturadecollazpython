import OcelotasLMN

/-! # Ocelotas: encierros racionales de log 2 y log 3 con 55 decimales

Serie de log(1-x) con resto demostrado en Mathlib. No usa LMN.
Las cotas permiten certificar signos de aproximantes mas grandes.
-/

namespace OcelotasLogaritmosPrecisos

open Real

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem log_dos_cotas :
    (0.6931471805599453094172321214581765680755001343602552540 : ℝ) < log 2 ∧
    log 2 < 0.6931471805599453094172321214581765680755001343602552543 := by
  have t : |(2⁻¹ : ℝ)| = 2⁻¹ := by rw [abs_of_pos]; norm_num
  have z := Real.abs_log_sub_add_sum_range_le (show |(2⁻¹ : ℝ)| < 1 by rw [t]; norm_num) 192
  rw [t] at z
  norm_num1 at z
  rw [one_div (2 : ℝ), log_inv, ← sub_eq_add_neg] at z
  have h := abs_le.1 z
  constructor <;> linarith [h.1, h.2]

theorem log_tres_cotas :
    (1.0986122886681096913952452369225257046474905578227494516 : ℝ) < log 3 ∧
    log 3 < 1.0986122886681096913952452369225257046474905578227494520 := by
  have t : |(3⁻¹ : ℝ)| = 3⁻¹ := by rw [abs_of_pos]; norm_num
  have z := Real.abs_log_sub_add_sum_range_le (show |(3⁻¹ : ℝ)| < 1 by rw [t]; norm_num) 128
  rw [t] at z
  norm_num1 at z
  have hd : log (2 / 3 : ℝ) = log 2 - log 3 := Real.log_div (by norm_num) (by norm_num)
  rw [hd] at z
  have h := abs_le.1 z
  have h2 := log_dos_cotas
  constructor <;> linarith [h.1, h.2, h2.1, h2.2]

end OcelotasLogaritmosPrecisos

#print axioms OcelotasLogaritmosPrecisos.log_dos_cotas
#print axioms OcelotasLogaritmosPrecisos.log_tres_cotas
