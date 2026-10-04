import OcelotasAfinada
import OcelotasTrayectorias

/-! # Bloques con una cota inferior de sus valores

T es el atajo. Si un bloque impar de longitud a y uno par de longitud b
terminan en y>=N, se puede conservar el factor (N+1)/(2N+1) de reducción.
Para acotar los impares del último bloque sólo se necesitan los valores
de los comienzos de los bloques, sin una cota inferior del valor final.
-/

namespace OcelotasSueloRachas

open Real Ocelotas OcelotasTrayectorias

theorem paso_suelo {n r i N : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hi : i < r)
    (hmin : N ≤ T^[tiempo a b (i + 1)] n) :
    (2 * N + 1) * 2 ^ a i * (T^[tiempo a b (i + 1)] n + 1) ≤
      (N + 1) * 3 ^ a i * (T^[tiempo a b i] n + 1) := by
  have hb := (hw i hi).2.1
  have hpot : 2 ≤ 2 ^ b i := by
    simpa using (Nat.pow_le_pow_right (by decide : 1 ≤ 2) hb)
  have he := identidad_par hw hi
  have hle : 2 * T^[tiempo a b (i + 1)] n ≤ T^[tiempo a b i + a i] n := by
    nlinarith
  have hm := Nat.mul_le_mul_left (N + 1) hle
  have hrazon : (2 * N + 1) * (T^[tiempo a b (i + 1)] n + 1) ≤
      (N + 1) * (T^[tiempo a b i + a i] n + 1) := by nlinarith
  calc
    _ = 2 ^ a i * ((2 * N + 1) * (T^[tiempo a b (i + 1)] n + 1)) := by ring
    _ ≤ 2 ^ a i * ((N + 1) * (T^[tiempo a b i + a i] n + 1)) :=
      Nat.mul_le_mul_left _ hrazon
    _ = (N + 1) * (2 ^ a i * (T^[tiempo a b i + a i] n + 1)) := by ring
    _ = (N + 1) * (3 ^ a i * (T^[tiempo a b i] n + 1)) := by rw [identidad_impar hw hi]
    _ = _ := by ring

theorem cadena_suelo {n r N : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hmin : ∀ i, i < r → N ≤ T^[tiempo a b i] n) :
    ∀ i, i < r → (2 * N + 1) ^ i * 2 ^ acumulados a i * (T^[tiempo a b i] n + 1) ≤
      (N + 1) ^ i * 3 ^ acumulados a i * (n + 1) := by
  intro i
  induction i with
  | zero => intro hi; simp [tiempo, acumulados]
  | succ i ih =>
    intro hi
    have h1 := Nat.mul_le_mul_left ((2 * N + 1) ^ i * 2 ^ acumulados a i)
      (paso_suelo hw (show i < r by omega) (hmin (i + 1) hi))
    have h2 := Nat.mul_le_mul_left ((N + 1) * 3 ^ a i) (ih (by omega))
    simp only [acumulados, pow_add, pow_succ]
    nlinarith only [h1, h2]

theorem congruencias_suelo {n r N : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hmin : ∀ i, i < r → N ≤ T^[tiempo a b i] n) :
    ∀ i, i < r → (2 * N + 1) ^ i * 2 ^ acumulados a (i + 1) ≤
      (n + 1) * (N + 1) ^ i * 3 ^ acumulados a i := by
  intro i hi
  have hd := Nat.le_of_dvd (by omega : 0 < T^[tiempo a b i] n + 1)
    (congruencia_racha hw hi)
  have hm := Nat.mul_le_mul_left ((2 * N + 1) ^ i * 2 ^ acumulados a i) hd
  have hc := cadena_suelo hw hmin i hi
  simpa [acumulados, pow_add, Nat.mul_assoc, Nat.mul_left_comm, Nat.mul_comm] using le_trans hm hc

theorem paso_real {n s N i p a : ℕ} {alfa beta gamma : ℝ}
    (hs : 0 < s) (hn : n + 1 ≤ s)
    (hc : (2 * N + 1) ^ i * 2 ^ a ≤ (n + 1) * (N + 1) ^ i * 3 ^ p)
    (halfa : log 3 ≤ alfa * log 2) (hbeta : log s ≤ beta * log 2)
    (hgamma : gamma * log 2 ≤ log (2 * N + 1) - log (N + 1)) :
    (a : ℝ) ≤ beta + alfa * p - gamma * i := by
  have hmul := Nat.mul_le_mul_right ((N + 1) ^ i * 3 ^ p) hn
  have hpot : (((2 * N + 1 : ℕ) : ℝ) ^ i) * (2 : ℝ) ^ a ≤
      (s : ℝ) * ((N + 1 : ℕ) : ℝ) ^ i * (3 : ℝ) ^ p := by
    exact_mod_cast le_trans hc (by simpa [Nat.mul_assoc] using hmul)
  have hsR : (0 : ℝ) < s := by exact_mod_cast hs
  have hlog := Real.log_le_log (by positivity) hpot
  rw [Real.log_mul (by positivity) (by positivity),
      Real.log_mul (by positivity) (by positivity),
      Real.log_mul (by positivity) (by positivity)] at hlog
  simp only [Real.log_pow] at hlog
  push_cast at hlog
  have hp := mul_le_mul_of_nonneg_left halfa (show (0 : ℝ) ≤ p by positivity)
  have hg := mul_le_mul_of_nonneg_left hgamma (show (0 : ℝ) ≤ i by positivity)
  have h2 : (0 : ℝ) < log 2 := Real.log_pos (by norm_num)
  by_contra h
  have hpos : 0 < (a : ℝ) - (beta + alfa * p - gamma * i) := by linarith
  have hprod := mul_pos hpos h2
  nlinarith

end OcelotasSueloRachas

#print axioms OcelotasSueloRachas.paso_suelo
#print axioms OcelotasSueloRachas.cadena_suelo
#print axioms OcelotasSueloRachas.congruencias_suelo
#print axioms OcelotasSueloRachas.paso_real
