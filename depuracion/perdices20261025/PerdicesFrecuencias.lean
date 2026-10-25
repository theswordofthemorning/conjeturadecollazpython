import Mathlib.Data.Nat.Choose.Sum
import Mathlib.Data.Rat.Lemmas
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-! Balance de frecuencias de una misma trayectoria del atajo.
El criterio es condicional: no prueba que una órbita excepcional mezcle. -/

namespace PerdicesFrecuencias

def T (n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

def marca (m r n : ℕ) : ℕ := if n % m = r then 1 else 0

def potencial (n : ℕ) : ℕ := marca 9 2 n + marca 3 2 n

theorem potencial_acotado (n : ℕ) : potencial n ≤ 2 := by
  unfold potencial marca
  split_ifs <;> omega

theorem identidad_local (n : ℕ) :
    n % 2 + marca 18 4 n + marca 3 1 n = potencial (T n) := by
  unfold T potencial marca
  split_ifs <;> omega

def cuenta (x : ℕ → ℕ) (K m r : ℕ) : ℕ :=
  ∑ j ∈ Finset.range K, marca m r (x j)

def subidas (x : ℕ → ℕ) (K : ℕ) : ℕ :=
  ∑ j ∈ Finset.range K, x j % 2

theorem balance (x : ℕ → ℕ) (hx : ∀ j, x (j + 1) = T (x j)) (K : ℕ) :
    subidas x K + cuenta x K 18 4 + cuenta x K 3 1 + potencial (x 0) =
      cuenta x K 9 2 + cuenta x K 3 2 + potencial (x K) := by
  induction K with
  | zero => simp [subidas, cuenta]
  | succ K ih =>
    have h := identidad_local (x K)
    rw [← hx K] at h
    simp only [subidas, cuenta, Finset.sum_range_succ] at ih ⊢
    unfold potencial at h
    unfold potencial at ih ⊢
    omega

theorem subidas_acotadas (x : ℕ → ℕ) (hx : ∀ j, x (j + 1) = T (x j)) (K : ℕ) :
    subidas x K + cuenta x K 3 1 ≤ cuenta x K 9 2 + cuenta x K 3 2 + 2 := by
  have h := balance x hx K
  have hp := potencial_acotado (x K)
  omega

/-- Tres desigualdades marginales, implicadas por TV <= 1/100
respecto de nu_2, bastan para este criterio entero. -/
theorem frecuencias_fuerzan_densidad {K S C1 C2 C9 : ℕ}
    (hK : 163 ≤ K)
    (hbalance : S + C1 ≤ C9 + C2 + 2)
    (h1 : 97 * K ≤ 300 * C1)
    (h2 : 300 * C2 ≤ 203 * K)
    (h9 : 6300 * C9 ≤ 1663 * K) :
    27 * S < 17 * K := by
  nlinarith

theorem densidad_fuerza_cruce {K S : ℕ}
    (hK : 0 < K) (hS : 27 * S ≤ 17 * K) :
    3 ^ S < 2 ^ K := by
  have h1 : (3 : ℕ) ^ (27 * S) ≤ 3 ^ (17 * K) :=
    Nat.pow_le_pow_right (by decide) hS
  have hbase : (3 : ℕ) ^ 17 < 2 ^ 27 := by norm_num
  have h2 : ((3 : ℕ) ^ 17) ^ K < (2 ^ 27) ^ K :=
    Nat.pow_lt_pow_left hbase (by omega)
  rw [← pow_mul, ← pow_mul] at h2
  by_contra hn
  have h3 : ((2 : ℕ) ^ K) ^ 27 ≤ (3 ^ S) ^ 27 :=
    Nat.pow_le_pow_left (by omega) 27
  rw [← pow_mul, ← pow_mul] at h3
  have h4 : (2 : ℕ) ^ (27 * K) ≤ 3 ^ (27 * S) := by
    simpa [Nat.mul_comm] using h3
  exact (not_lt_of_ge h4) (h1.trans_lt h2)

theorem criterio_orbital (x : ℕ → ℕ)
    (hx : ∀ j, x (j + 1) = T (x j)) (K : ℕ)
    (hK : 163 ≤ K)
    (h1 : 97 * K ≤ 300 * cuenta x K 3 1)
    (h2 : 300 * cuenta x K 3 2 ≤ 203 * K)
    (h9 : 6300 * cuenta x K 9 2 ≤ 1663 * K) :
    3 ^ subidas x K < 2 ^ K := by
  have hs := frecuencias_fuerzan_densidad hK (subidas_acotadas x hx K) h1 h2 h9
  exact densidad_fuerza_cruce (by omega) (le_of_lt hs)

end PerdicesFrecuencias

#print axioms PerdicesFrecuencias.potencial_acotado
#print axioms PerdicesFrecuencias.identidad_local
#print axioms PerdicesFrecuencias.balance
#print axioms PerdicesFrecuencias.subidas_acotadas
#print axioms PerdicesFrecuencias.frecuencias_fuerzan_densidad
#print axioms PerdicesFrecuencias.densidad_fuerza_cruce
#print axioms PerdicesFrecuencias.criterio_orbital
