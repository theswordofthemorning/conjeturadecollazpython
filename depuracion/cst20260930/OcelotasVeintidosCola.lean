import OcelotasLMN
import OcelotasGeometrica
import OcelotasVentanaRacional

/-! # Ocelotas: cola de veintidós rachas con puente desde q >= 4598951775 -/

namespace OcelotasVeintidosCola

open Ocelotas OcelotasRachas OcelotasTrayectorias OcelotasLMN

theorem cota_veintidos_lineal (m : ℕ) : cota 22 m ≤ 51580 * m :=
  OcelotasGeometrica.cota_lineal (by decide +kernel) m

theorem cola_veintidos_lmn (t : ℕ) (ht : 33 ≤ t) :
    8 * 51580 * (19 * (t + 33) ^ 2 + 6) + 5 < 5 * 2 ^ t := by
  induction t, ht using Nat.le_induction with
  | base => norm_num
  | succ t ht ih =>
    rw [pow_succ 2 t]
    have : 19 * (t + 1 + 33) ^ 2 + 6 ≤ 2 * (19 * (t + 33) ^ 2 + 6) := by nlinarith
    omega

theorem sin_fallo_cola (hL : LMNDebil) {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr22 : r ≤ 22)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hk32 : 2 ^ 32 ≤ tiempo a b r) (hqmin : 4598951775 ≤ S (tiempo a b r) n) : False := by
  have hk0 : 0 < tiempo a b r := by positivity
  have hlo : 2 ^ Nat.log 2 (tiempo a b r) ≤ tiempo a b r := Nat.pow_log_le_self 2 (by omega)
  have hhi : tiempo a b r < 2 ^ (Nat.log 2 (tiempo a b r) + 1) :=
    Nat.lt_pow_succ_log_self (by decide) _
  have ht32 : 32 ≤ Nat.log 2 (tiempo a b r) := Nat.le_log_of_pow_le (by decide) hk32
  have h32 : (2 : ℕ) ^ 32 = 4294967296 := by norm_num
  have he := cola_lmn_entera hL (by omega) (ventana_cruce hk).2 hk.2 hhi
  have hp := fallo_producto hw hr hk hf
  have hn : n < 32 * 2 ^ (19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2) := by
    have h1 : (2 ^ tiempo a b r - 3 ^ S (tiempo a b r) n) * n <
        (2 ^ tiempo a b r - 3 ^ S (tiempo a b r) n) *
          (32 * 2 ^ (19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2)) := by
      calc _ < r * 3 ^ S (tiempo a b r) n := hp
        _ ≤ 22 * 3 ^ S (tiempo a b r) n := Nat.mul_le_mul_right _ hr22
        _ ≤ 22 * ((2 ^ tiempo a b r - 3 ^ S (tiempo a b r) n) *
              2 ^ (19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2)) := Nat.mul_le_mul_left _ he
        _ ≤ 32 * ((2 ^ tiempo a b r - 3 ^ S (tiempo a b r) n) *
              2 ^ (19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2)) :=
          Nat.mul_le_mul_right _ (by norm_num)
        _ = _ := Nat.mul_left_comm _ _ _
    exact Nat.lt_of_mul_lt_mul_left h1
  have hn2 : n + 1 < 2 ^ (19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2 + 6) := by
    rw [pow_add]
    omega
  have hc := criba_desde_trayectoria hw hn2
  have hcm := cota_monotona (by omega : 1 ≤ 19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2 + 6) hr22
  have hd := cota_veintidos_lineal (19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2 + 6)
  have hki := OcelotasTiempoRacional.tiempo_del_cruce hk
  by_cases ht33 : 33 ≤ Nat.log 2 (tiempo a b r)
  · have hcola := cola_veintidos_lmn (Nat.log 2 (tiempo a b r)) ht33
    omega
  · have heq : Nat.log 2 (tiempo a b r) = 32 := by omega
    have hinf := OcelotasVentanaRacional.tiempo_tres_medios hk.2
    norm_num [heq] at hc hcm hd
    omega


end OcelotasVeintidosCola

#print axioms OcelotasVeintidosCola.cota_veintidos_lineal
#print axioms OcelotasVeintidosCola.cola_veintidos_lmn
#print axioms OcelotasVeintidosCola.sin_fallo_cola
