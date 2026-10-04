import OcelotasSueloCriba
import OcelotasTreceBase

/-! # Especialización entera de la criba con suelo 4095

Alfa=317/200, beta=B/256 y gamma=4095/4096.
El suelo sólo se exige antes del último bloque. La conclusión no
supone un fallo de CST; basta un primer cruce finito y n>=4095.
-/

namespace OcelotasSueloNumerica

open Real Ocelotas OcelotasTrayectorias

set_option maxRecDepth 8192
set_option maxHeartbeats 1000000

theorem gamma_valida :
    (4095 / 4096 : ℝ) * log 2 ≤ log 8191 - log 4096 := by
  have hp : (2 : ℕ) ^ 4095 * 4096 ^ 4096 ≤ 8191 ^ 4096 := by decide +kernel
  have hpR : (2 : ℝ) ^ 4095 * 4096 ^ 4096 ≤ 8191 ^ 4096 := by exact_mod_cast hp
  have hl := Real.log_le_log (by positivity) hpR
  rw [Real.log_mul (by positivity) (by positivity)] at hl
  simp only [Real.log_pow] at hl
  norm_num at hl
  linarith

def cota (B : ℕ) : ℕ → ℕ
  | 0 => 0
  | i + 1 => (400 * B + 162304 * cota B i - 102375 * i) / 102400

theorem doble_indice (B : ℕ) (hB : 512 ≤ B) (r : ℕ) : 2 * r ≤ cota B r := by
  induction r with
  | zero => simp [cota]
  | succ r ih =>
    simp only [cota]
    apply (Nat.le_div_iff_mul_le (by decide : 0 < (102400 : ℕ))).2
    omega

theorem cota_real (B r : ℕ) (hB : 512 ≤ B) :
    cota B r = OcelotasSueloCriba.cota (1585 / 1000) ((B : ℝ) / 256) (4095 / 4096) r := by
  induction r with
  | zero => rfl
  | succ r ih =>
    have hd := doble_indice B hB r
    have hsub : 102375 * r ≤ 400 * B + 162304 * cota B r := by omega
    simp only [cota, OcelotasSueloCriba.cota]
    rw [← ih]
    have he : (B : ℝ) / 256 + (1585 / 1000 : ℝ) * cota B r - (4095 / 4096 : ℝ) * r =
        ((400 * B + 162304 * cota B r - 102375 * r : ℕ) : ℝ) / 102400 := by
      rw [Nat.cast_sub hsub]
      push_cast
      ring
    rw [he]
    exact (Nat.floor_div_eq_div (400 * B + 162304 * cota B r - 102375 * r) 102400).symm

theorem criba_desde_potencia {n s r R B : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hk : PrimerCruce n (tiempo a b r)) (hN : 4095 ≤ n)
    (hs : 0 < s) (hn : n + 1 ≤ s) (hr : r ≤ R) (hB : 512 ≤ B)
    (hpot : s ^ 256 ≤ 2 ^ B) : S (tiempo a b r) n ≤ cota B R := by
  have hbeta := OcelotasTreceBase.beta_de_potencia hs hpot
  have hBR : (512 : ℝ) ≤ B := by exact_mod_cast hB
  have hc := OcelotasSueloCriba.criba_primer_cruce (N := 4095)
    hw hk hN hs hn hr (by norm_num : (3 / 2 : ℝ) ≤ 1585 / 1000)
    (by linarith : (2 : ℝ) ≤ (B : ℝ) / 256)
    (by norm_num : (4095 / 4096 : ℝ) ≤ 1) OcelotasTreceBase.alfa_valida hbeta
    (by norm_num; exact gamma_valida)
  rw [← cota_real B R hB] at hc
  exact hc

end OcelotasSueloNumerica

#print axioms OcelotasSueloNumerica.gamma_valida
#print axioms OcelotasSueloNumerica.doble_indice
#print axioms OcelotasSueloNumerica.cota_real
#print axioms OcelotasSueloNumerica.criba_desde_potencia
