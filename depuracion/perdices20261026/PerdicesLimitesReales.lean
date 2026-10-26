import Mathlib.Analysis.SpecificLimits.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

/-! Ramas prescritas A=1 y B=110 sobre reales negativos.
No se identifica esta construccion con una orbita entera de Collatz. -/

namespace PerdicesLimitesReales

open Filter
open scoped Topology

noncomputable def paso (q : ℝ) : ℝ := if q ≤ 3 then (3 * q - 1) / 2 else (9 * q - 5) / 8
noncomputable def razon (q : ℝ) : ℝ := if q ≤ 3 then 2 / 3 else 8 / 9
noncomputable def termino (q : ℝ) : ℝ := if q ≤ 3 then 1 / 3 else 5 / 9

noncomputable def estado (q : ℝ) : ℕ → ℝ
  | 0 => q
  | k + 1 => paso (estado q k)

noncomputable def inverso (q : ℝ) : ℕ → ℝ
  | 0 => 1
  | k + 1 => inverso q k * razon (estado q k)

noncomputable def suma (q : ℝ) : ℕ → ℝ
  | 0 => 0
  | k + 1 => suma q k - inverso q k * termino (estado q k)

theorem intervalo_paso {q : ℝ} (h : 1 ≤ q ∧ q ≤ 4) :
    1 ≤ paso q ∧ paso q ≤ 4 := by
  unfold paso
  split_ifs with hq <;> constructor <;> linarith [h.1, h.2]

theorem intervalo_orbital {q : ℝ} (h : 1 ≤ q ∧ q ≤ 4) (k : ℕ) :
    1 ≤ estado q k ∧ estado q k ≤ 4 := by
  induction k with
  | zero => exact h
  | succ k hk => exact intervalo_paso hk

theorem identidad_local (q : ℝ) : razon q * paso q = q - termino q := by
  unfold razon paso termino
  split_ifs <;> ring

theorem identidad_parcial (q : ℝ) (k : ℕ) :
    suma q k = -q + inverso q k * estado q k := by
  induction k with
  | zero => simp [suma, inverso, estado]
  | succ k hk =>
    simp only [suma, inverso, estado, hk]
    rw [mul_assoc, identidad_local]
    ring

theorem cota_inverso (q : ℝ) (k : ℕ) :
    0 ≤ inverso q k ∧ inverso q k ≤ (8 / 9 : ℝ) ^ k := by
  induction k with
  | zero => norm_num [inverso]
  | succ k hk =>
    have hr : 0 ≤ razon (estado q k) ∧ razon (estado q k) ≤ (8 / 9 : ℝ) := by
      unfold razon
      split_ifs <;> norm_num
    constructor
    · exact mul_nonneg hk.1 hr.1
    · simpa only [inverso, pow_succ] using mul_le_mul hk.2 hr.2 hr.1 (by positivity)

theorem cota_error {q : ℝ} (h : 1 ≤ q ∧ q ≤ 4) (k : ℕ) :
    0 ≤ suma q k + q ∧ suma q k + q ≤ 4 * (8 / 9 : ℝ) ^ k := by
  rw [identidad_parcial]
  have he := intervalo_orbital h k
  have hi := cota_inverso q k
  constructor
  · nlinarith
  · nlinarith [mul_le_mul hi.2 he.2 (by linarith : 0 ≤ estado q k) (by positivity)]

theorem limite_real {q : ℝ} (h : 1 ≤ q ∧ q ≤ 4) :
    Tendsto (suma q) atTop (𝓝 (-q)) := by
  have hp : Tendsto (fun k : ℕ => (8 / 9 : ℝ) ^ k) atTop (𝓝 0) :=
    tendsto_pow_atTop_nhds_zero_of_lt_one (by norm_num) (by norm_num)
  have he : Tendsto (fun k => suma q k + q) atTop (𝓝 0) := by
    apply squeeze_zero (fun k => (cota_error h k).1) (fun k => (cota_error h k).2)
    simpa using hp.const_mul 4
  simpa using he.sub_const q

theorem testigo_denominador_par :
    Tendsto (suma (3 / 2)) atTop (𝓝 (-(3 / 2 : ℝ))) :=
  limite_real (by norm_num)

theorem testigo_entero_negativo :
    Tendsto (suma 2) atTop (𝓝 (-2 : ℝ)) ∧ paso 2 = 5 / 2 := by
  exact ⟨limite_real (by norm_num), by norm_num [paso]⟩

theorem numeradores_impares (a : ℤ) (d : ℕ) (ha : a % 2 = 1) (hd : 1 ≤ d) :
    (3 * a - 2 ^ d) % 2 = 1 ∧ (9 * a - 5 * 2 ^ d) % 2 = 1 := by
  obtain ⟨j, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (by omega : d ≠ 0)
  simp [Int.sub_emod, Int.mul_emod, pow_succ, ha]

theorem no_fijo_diadico (a c e : ℤ) (d : ℕ)
    (ha : a % 2 = 1) (hc : c % 2 = 1) (hd : 1 ≤ d) :
    c * a ≠ 2 ^ d * e := by
  intro he
  obtain ⟨j, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (by omega : d ≠ 0)
  have hm := congrArg (fun z : ℤ => z % 2) he
  simp [Int.mul_emod, pow_succ, ha, hc] at hm

end PerdicesLimitesReales

#print axioms PerdicesLimitesReales.intervalo_paso
#print axioms PerdicesLimitesReales.intervalo_orbital
#print axioms PerdicesLimitesReales.identidad_local
#print axioms PerdicesLimitesReales.identidad_parcial
#print axioms PerdicesLimitesReales.cota_inverso
#print axioms PerdicesLimitesReales.cota_error
#print axioms PerdicesLimitesReales.limite_real
#print axioms PerdicesLimitesReales.testigo_denominador_par
#print axioms PerdicesLimitesReales.testigo_entero_negativo
#print axioms PerdicesLimitesReales.numeradores_impares
#print axioms PerdicesLimitesReales.no_fijo_diadico
