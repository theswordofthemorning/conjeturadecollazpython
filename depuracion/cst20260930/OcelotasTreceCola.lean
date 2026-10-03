import OcelotasLMN

/-! # Ocelotas: cola bajo LMN hasta trece rachas, desde k >= 2^27 -/

namespace OcelotasTreceCola

open Ocelotas OcelotasRachas OcelotasTrayectorias OcelotasLMN

theorem cota_trece_lineal (m : ℕ) : cota 13 m ≤ 751 * m := by
  simp only [cota]
  omega

theorem cola_trece_lmn (t : ℕ) (ht : 27 ≤ t) : 1502 * (19 * (t + 33) ^ 2 + 5) < 2 ^ t := by
  induction t, ht using Nat.le_induction with
  | base => norm_num
  | succ t ht ih =>
    rw [pow_succ 2 t]
    have : 19 * (t + 1 + 33) ^ 2 + 5 ≤ 2 * (19 * (t + 33) ^ 2 + 5) := by nlinarith
    omega

theorem sin_fallo_cola (hL : LMNDebil) {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr13 : r ≤ 13)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hk27 : 2 ^ 27 ≤ tiempo a b r) : False := by
  have hk0 : 0 < tiempo a b r := by positivity
  have hlo : 2 ^ Nat.log 2 (tiempo a b r) ≤ tiempo a b r := Nat.pow_log_le_self 2 (by omega)
  have hhi : tiempo a b r < 2 ^ (Nat.log 2 (tiempo a b r) + 1) :=
    Nat.lt_pow_succ_log_self (by decide) _
  have ht27 : 27 ≤ Nat.log 2 (tiempo a b r) := Nat.le_log_of_pow_le (by decide) hk27
  have h27 : (2 : ℕ) ^ 27 = 134217728 := by norm_num
  have he := cola_lmn_entera hL (by omega) (ventana_cruce hk).2 hk.2 hhi
  have hp := fallo_producto hw hr hk hf
  have hn : n < 16 * 2 ^ (19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2) := by
    have h1 : (2 ^ tiempo a b r - 3 ^ S (tiempo a b r) n) * n <
        (2 ^ tiempo a b r - 3 ^ S (tiempo a b r) n) *
          (16 * 2 ^ (19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2)) := by
      calc _ < r * 3 ^ S (tiempo a b r) n := hp
        _ ≤ 13 * 3 ^ S (tiempo a b r) n := Nat.mul_le_mul_right _ hr13
        _ ≤ 13 * ((2 ^ tiempo a b r - 3 ^ S (tiempo a b r) n) *
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
  have hcm := cota_monotona (by omega : 1 ≤ 19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2 + 5) hr13
  have hd := cota_trece_lineal (19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2 + 5)
  have hki := tiempo_por_impares (impares_pos hw hr) (ventana_cruce hk).2
  have hcola := cola_trece_lmn (Nat.log 2 (tiempo a b r)) ht27
  omega


end OcelotasTreceCola

#print axioms OcelotasTreceCola.cota_trece_lineal
#print axioms OcelotasTreceCola.cola_trece_lmn
#print axioms OcelotasTreceCola.sin_fallo_cola
