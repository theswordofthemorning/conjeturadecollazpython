import OcelotasLMN
import OcelotasTiempoRacional
import OcelotasLMNFuente

/-! # Ocelotas: una región finita para cualquier número fijo de rachas

Mapa atajo, semillas naturales n >= 2, primer cruce finito.
Bajo LMNDebil, un fallo con r rachas tiene k < 2^(2*r+32).
La cota es deliberadamente holgada; no afirma que la región sea vacía.
-/

namespace OcelotasCotaGeneral

open Ocelotas OcelotasRachas OcelotasTrayectorias OcelotasContador OcelotasLMN

set_option maxHeartbeats 1000000

theorem cota_binaria (r m : ℕ) : cota r m + m ≤ 2 ^ r * m := by
  induction r with
  | zero => simp [cota]
  | succ r ih =>
    have hd : 5 * cota (r + 1) m ≤ 5 * m + 8 * cota r m := by
      have h := Nat.div_mul_le_self (5 * m + 8 * cota r m - 1) 5
      simp only [cota]
      omega
    rw [pow_succ]
    nlinarith

theorem margen_inicial (r : ℕ) :
    40 * 2 ^ r * (2 * r + 65) ^ 2 + 1 < 2 ^ (2 * r + 32) := by
  induction r with
  | zero => norm_num
  | succ r ih =>
    have hp : (2 * (r + 1) + 65) ^ 2 ≤ 2 * (2 * r + 65) ^ 2 := by
      have he : 2 * (2 * r + 65) ^ 2 =
          (2 * (r + 1) + 65) ^ 2 + 4 * r ^ 2 + 252 * r + 3961 := by ring
      omega
    have hm := Nat.mul_le_mul_left (80 * 2 ^ r) hp
    have he : 2 * (r + 1) + 32 = (2 * r + 32) + 2 := by omega
    rw [he, pow_add 2 (2 * r + 32) 2, pow_succ 2 r]
    norm_num only [show (2 : ℕ) ^ 2 = 4 by norm_num]
    nlinarith

theorem margen_cola (r t : ℕ) (ht : 2 * r + 32 ≤ t) :
    40 * 2 ^ r * (t + 33) ^ 2 + 1 < 2 ^ t := by
  induction t, ht using Nat.le_induction with
  | base => simpa [Nat.add_assoc] using margen_inicial r
  | succ t ht ih =>
    have hp : (t + 1 + 33) ^ 2 ≤ 2 * (t + 33) ^ 2 := by nlinarith
    have hm := Nat.mul_le_mul_left (40 * 2 ^ r) hp
    rw [pow_succ 2 t]
    nlinarith

theorem semilla_del_fallo (hL : LMNDebil) {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hk2 : 2 ≤ tiempo a b r) :
    n < 2 ^ (19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2 + r) := by
  have hhi := Nat.lt_pow_succ_log_self (by decide : 1 < 2) (tiempo a b r)
  have he := cola_lmn_entera hL hk2 (ventana_cruce hk).2 hk.2 hhi
  have hp := fallo_producto hw hr hk hf
  have hsem : n < r * 2 ^ (19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2) := by
    apply Nat.lt_of_mul_lt_mul_left (a := 2 ^ tiempo a b r - 3 ^ S (tiempo a b r) n)
    calc
      _ < r * 3 ^ S (tiempo a b r) n := hp
      _ ≤ r * ((2 ^ tiempo a b r - 3 ^ S (tiempo a b r) n) *
          2 ^ (19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2)) := Nat.mul_le_mul_left r he
      _ = _ := Nat.mul_left_comm _ _ _
  have hrpow : r ≤ 2 ^ r := Nat.le_of_lt Nat.lt_two_pow_self
  calc
    n < r * 2 ^ (19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2) := hsem
    _ ≤ 2 ^ r * 2 ^ (19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2) :=
      Nat.mul_le_mul_right _ hrpow
    _ = _ := by rw [← pow_add, Nat.add_comm]

theorem log_tiempo_del_fallo (hL : LMNDebil) {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n) :
    Nat.log 2 (tiempo a b r) < 2 * r + 32 := by
  by_contra h
  have ht : 2 * r + 32 ≤ Nat.log 2 (tiempo a b r) := by omega
  have hk0 : 0 < tiempo a b r := by
    by_contra hzero
    have hz : tiempo a b r = 0 := by omega
    simp only [hz, Nat.log_zero_right] at ht
    omega
  have hlo := Nat.pow_log_le_self 2 (by omega : tiempo a b r ≠ 0)
  have hk2 : 2 ≤ tiempo a b r := by
    have hpow := Nat.pow_le_pow_right (by decide : 0 < 2) (by omega : 1 ≤ Nat.log 2 (tiempo a b r))
    norm_num at hpow
    omega
  have hn := semilla_del_fallo hL hw hr hk hf hk2
  have hn2 : n + 1 < 2 ^ (19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2 + r + 1) := by
    rw [pow_succ]
    omega
  have hc := criba_desde_trayectoria hw hn2
  have hb := cota_binaria r (19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2 + r + 1)
  have hm : 19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2 + r + 1 ≤
      20 * (Nat.log 2 (tiempo a b r) + 33) ^ 2 := by nlinarith
  have hmul := Nat.mul_le_mul_left (2 ^ r) hm
  have hki := OcelotasTiempoRacional.tiempo_del_cruce hk
  have hcola := margen_cola r (Nat.log 2 (tiempo a b r)) ht
  nlinarith

theorem tiempo_del_fallo (hL : LMNDebil) {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n) :
    tiempo a b r < 2 ^ (2 * r + 32) := by
  have ht := log_tiempo_del_fallo hL hw hr hk hf
  have hhi := Nat.lt_pow_succ_log_self (by decide : 1 < 2) (tiempo a b r)
  exact lt_of_lt_of_le hhi (Nat.pow_le_pow_right (by decide) (by omega))

theorem region_del_fallo (hL : LMNDebil) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hf : n ≤ T^[k] n) :
    k < 2 ^ (2 * rachas n k + 32) ∧
    n < 2 ^ (19 * (2 * rachas n k + 65) ^ 2 + rachas n k) := by
  by_cases hpar : n % 2 = 0
  · have hd := OcelotasCierre.descenso_par hn hpar hk
    omega
  · have himpar : n % 2 = 1 := by omega
    have hk2 : 2 ≤ k := by
      by_contra hsmall
      have hcases : k = 0 ∨ k = 1 := by omega
      rcases hcases with hz | hu
      · simpa [hz, S] using hk.2
      · simpa [hu, S, himpar] using hk.2
    obtain ⟨hpos, a, b, hw, he⟩ := palabra_del_cruce himpar hk
    have hkw : PrimerCruce n (tiempo a b (rachas n k)) := by rwa [he]
    have hfw : n ≤ T^[tiempo a b (rachas n k)] n := by rwa [he]
    have hlog := log_tiempo_del_fallo hL hw hpos hkw hfw
    have htiempo := tiempo_del_fallo hL hw hpos hkw hfw
    have hsem := semilla_del_fallo hL hw hpos hkw hfw (by omega)
    rw [he] at hlog htiempo hsem
    refine ⟨htiempo, lt_of_lt_of_le hsem ?_⟩
    apply Nat.pow_le_pow_right (by decide)
    have ht : Nat.log 2 k + 33 ≤ 2 * rachas n k + 65 := by omega
    nlinarith

/-- Enunciado desde la especialización publicada; LMN sigue como hipótesis. -/
theorem region_del_fallo_corolario (hL : OcelotasLMNFuente.LMN23)
    {n k : ℕ} (hn : 2 ≤ n) (hk : PrimerCruce n k) (hf : n ≤ T^[k] n) :
    k < 2 ^ (2 * rachas n k + 32) ∧
    n < 2 ^ (19 * (2 * rachas n k + 65) ^ 2 + rachas n k) :=
  region_del_fallo (OcelotasLMNFuente.debil_de_corolario hL) hn hk hf

/-- Cantidad de rachas arbitraria: un cruce suficientemente tardío desciende. -/
theorem descenso_de_tiempo_grande (hL : LMNDebil) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hgrande : 2 ^ (2 * rachas n k + 32) ≤ k) :
    T^[k] n < n := by
  by_contra hf
  have h := (region_del_fallo hL hn hk (by omega)).1
  omega

end OcelotasCotaGeneral

#print axioms OcelotasCotaGeneral.cota_binaria
#print axioms OcelotasCotaGeneral.margen_inicial
#print axioms OcelotasCotaGeneral.margen_cola
#print axioms OcelotasCotaGeneral.semilla_del_fallo
#print axioms OcelotasCotaGeneral.log_tiempo_del_fallo
#print axioms OcelotasCotaGeneral.tiempo_del_fallo

#print axioms OcelotasCotaGeneral.region_del_fallo

#print axioms OcelotasCotaGeneral.region_del_fallo_corolario
#print axioms OcelotasCotaGeneral.descenso_de_tiempo_grande
