import Mathlib.Tactic.NormNum
import Mathlib.Tactic.IntervalCases
import Mathlib.Tactic.Linarith

/-! Control simultáneo sobre la misma parte impar. Los enlaces con las
paridades orbitales se demuestran por escrito en CONGRUENCIAS.md. -/

namespace PerdicesCongruencias

def minimoResiduo (j : ℕ) : ℕ :=
  match j with
  | 0 => 71
  | 1 => 13
  | 2 => 47
  | 3 => 37
  | 4 => 23
  | _ => 61

def sobrecoste (j : ℕ) : ℕ :=
  match j with
  | 1 => 6
  | 4 => 7
  | _ => 8

theorem potencia_periodica {a m k : ℕ} (h : a ^ k % m = 1) (b : ℕ) :
    a ^ b % m = a ^ (b % k) % m := by
  conv_lhs => rw [← Nat.mod_add_div b k, pow_add, pow_mul]
  rw [Nat.mul_mod, Nat.pow_mod (a ^ k) (b / k) m, h,
    one_pow]
  simp

theorem tabla_compartida {b r : ℕ}
    (h9 : (2 ^ b * r + 1) % 9 = 0)
    (h8 : (3 ^ b * r + 1) % 8 = 0) :
    r % 72 = minimoResiduo (b % 6) := by
  have h2 := potencia_periodica (a := 2) (m := 9) (k := 6) (by norm_num) b
  have h3 := potencia_periodica (a := 3) (m := 8) (k := 6) (by norm_num) b
  rw [Nat.add_mod, Nat.mul_mod, h2] at h9
  rw [Nat.add_mod, Nat.mul_mod, h3] at h8
  have hb : b % 6 < 6 := Nat.mod_lt _ (by omega)
  interval_cases j : b % 6 <;>
    norm_num [j, minimoResiduo] at h9 h8 ⊢ <;> omega

theorem parte_impar_minima {b r : ℕ}
    (h9 : (2 ^ b * r + 1) % 9 = 0)
    (h8 : (3 ^ b * r + 1) % 8 = 0) :
    minimoResiduo (b % 6) ≤ r ∧ 13 ≤ r := by
  have h := tabla_compartida h9 h8
  have hr := Nat.mod_le r 72
  have hb : b % 6 < 6 := Nat.mod_lt _ (by omega)
  constructor
  · omega
  · interval_cases j : b % 6 <;> norm_num [j, minimoResiduo] at h <;> omega

theorem no_parte_impar_uno {b : ℕ}
    (h9 : (2 ^ b + 1) % 9 = 0) : (3 ^ b + 1) % 8 ≠ 0 := by
  intro h8
  have h := parte_impar_minima (r := 1) (by simpa using h9) (by simpa using h8)
  omega

theorem semilla_cota {n b q r : ℕ}
    (hn : n + 5 = 32 * q) (hq : 9 * q = 2 ^ b * r + 1)
    (h9 : (2 ^ b * r + 1) % 9 = 0)
    (h8 : (3 ^ b * r + 1) % 8 = 0) :
    2 ^ (b + 5) < n + 5 := by
  have hr := (parte_impar_minima h9 h8).2
  have hp : 0 < (2 : ℕ) ^ b := pow_pos (by omega) _
  rw [pow_add]
  norm_num
  nlinarith

theorem semilla_cota_residual {n b q r : ℕ}
    (hn : n + 5 = 32 * q) (hq : 9 * q = 2 ^ b * r + 1)
    (h9 : (2 ^ b * r + 1) % 9 = 0)
    (h8 : (3 ^ b * r + 1) % 8 = 0) :
    2 ^ b * 2 ^ (sobrecoste (b % 6) - 1) < n + 5 := by
  have hr := (parte_impar_minima h9 h8).1
  have hp : 0 < (2 : ℕ) ^ b := pow_pos (by omega) _
  have hb : b % 6 < 6 := Nat.mod_lt _ (by omega)
  interval_cases j : b % 6 <;>
    norm_num [j, minimoResiduo, sobrecoste] at hr ⊢ <;> nlinarith

theorem semilla_cota_superior_optima {n b q : ℕ}
    (hbpos : 1 ≤ b) (hn : n + 5 = 32 * q)
    (hq : 9 * q = 2 ^ b * minimoResiduo (b % 6) + 1) :
    n + 5 ≤ 2 ^ b * 2 ^ sobrecoste (b % 6) := by
  have hp : 2 ≤ (2 : ℕ) ^ b := by
    simpa using Nat.pow_le_pow_right (n := 2) (by omega) hbpos
  have hb : b % 6 < 6 := Nat.mod_lt _ (by omega)
  interval_cases j : b % 6 <;>
    norm_num [j, minimoResiduo, sobrecoste] at hq ⊢ <;> nlinarith

theorem congruencias_familias_optimas {b j : ℕ}
    (hj : j < 6) (hb : b % 12 = j) :
    (2 ^ b * minimoResiduo j + 1) % 9 = 0 ∧
    (3 ^ b * minimoResiduo j + 1) % 16 = 8 := by
  have h2 := potencia_periodica (a := 2) (m := 9) (k := 12) (by norm_num) b
  have h3 := potencia_periodica (a := 3) (m := 16) (k := 12) (by norm_num) b
  constructor
  · rw [Nat.add_mod, Nat.mul_mod, h2, hb]
    interval_cases j <;> norm_num [minimoResiduo]
  · rw [Nat.add_mod, Nat.mul_mod, h3, hb]
    interval_cases j <;> norm_num [minimoResiduo]

end PerdicesCongruencias

#print axioms PerdicesCongruencias.potencia_periodica
#print axioms PerdicesCongruencias.tabla_compartida
#print axioms PerdicesCongruencias.parte_impar_minima
#print axioms PerdicesCongruencias.no_parte_impar_uno
#print axioms PerdicesCongruencias.semilla_cota
#print axioms PerdicesCongruencias.semilla_cota_residual
#print axioms PerdicesCongruencias.semilla_cota_superior_optima
#print axioms PerdicesCongruencias.congruencias_familias_optimas
