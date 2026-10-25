import Mathlib.NumberTheory.Padics.PadicVal.Basic
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Tactic.NormNum

/-! Balance ternario de una trayectoria natural. No supone mezcla. -/

namespace PerdicesValuaciones

instance : Fact (Nat.Prime 3) := ⟨by decide⟩

def T (n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

theorem identidad_local (n : ℕ) :
    padicValNat 3 (4 * T n + 1) = padicValNat 3 (2 * n + 1) + n % 2 := by
  by_cases h : n % 2 = 0
  · have he : 4 * (n / 2) + 1 = 2 * n + 1 := by omega
    simp [T, h, he]
  · have hp : n % 2 = 1 := by omega
    have he : 4 * ((3 * n + 1) / 2) + 1 = 3 * (2 * n + 1) := by omega
    simp only [T, h, ite_false, he]
    rw [padicValNat.mul (by decide) (by omega)]
    norm_num [padicValNat.self, hp, Nat.add_comm]

def profundidad (m n : ℕ) : ℕ := m - min m (padicValNat 3 (2 * n + 1))

def activa (m n : ℕ) : ℕ := if padicValNat 3 (2 * n + 1) < m then n % 2 else 0

def critica (m n : ℕ) : ℕ := if m ≤ padicValNat 3 (2 * n + 1) then n % 2 else 0

theorem profundidad_acotada (m n : ℕ) : profundidad m n ≤ m := by
  unfold profundidad
  omega

theorem paridad_separada (m n : ℕ) : activa m n + critica m n = n % 2 := by
  unfold activa critica
  split_ifs <;> omega

theorem identidad_truncada (m n : ℕ) :
    profundidad m n = profundidad m (2 * T n) + activa m n := by
  have h := identidad_local n
  have hm : n % 2 < 2 := Nat.mod_lt _ (by decide)
  have he : 2 * (2 * T n) + 1 = 4 * T n + 1 := by omega
  unfold profundidad activa
  rw [he]
  split_ifs <;> omega

open Finset in
theorem balance_trayectoria (m K : ℕ) (x : ℕ → ℕ)
    (hx : ∀ j, x (j + 1) = T (x j)) :
    (∑ j ∈ range K, x j % 2) + (∑ j ∈ range K, profundidad m (2 * x j)) +
      profundidad m (2 * x K) =
    (∑ j ∈ range K, profundidad m (x j)) + (∑ j ∈ range K, critica m (x j)) +
      profundidad m (2 * x 0) := by
  induction K with
  | zero => simp
  | succ K ih =>
    simp only [sum_range_succ]
    have hl := identidad_truncada m (x K)
    have hp := paridad_separada m (x K)
    rw [← hx K] at hl
    omega

end PerdicesValuaciones

#print axioms PerdicesValuaciones.identidad_local
#print axioms PerdicesValuaciones.profundidad_acotada
#print axioms PerdicesValuaciones.paridad_separada
#print axioms PerdicesValuaciones.identidad_truncada
#print axioms PerdicesValuaciones.balance_trayectoria
