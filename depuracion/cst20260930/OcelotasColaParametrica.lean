import OcelotasLMN
import OcelotasLMNFuente
import OcelotasGeometrica
import OcelotasTiempoRacional

/-! # Ocelotas: criterio entero uniforme para excluir una cola infinita

R es un limite de rachas; A domina la suma geometrica; R <= 2^c.
Una desigualdad entera en H descarta todos los tiempos k >= 2^H.
LMN sigue externo y se supone un primer cruce finito. No cierra la
region restante ni afirma existencia universal de ese primer cruce.
-/

namespace OcelotasColaParametrica

open Ocelotas OcelotasRachas OcelotasTrayectorias OcelotasContador OcelotasLMN

set_option maxHeartbeats 1000000

theorem margen_cola {A c H : ℕ}
    (hbase : 8 * A * (19 * (H + 33) ^ 2 + c + 1) + 5 < 5 * 2 ^ H)
    {t : ℕ} (ht : H ≤ t) :
    8 * A * (19 * (t + 33) ^ 2 + c + 1) + 5 < 5 * 2 ^ t := by
  induction t, ht using Nat.le_induction with
  | base => exact hbase
  | succ t ht ih =>
    have hp : (t + 1 + 33) ^ 2 ≤ 2 * (t + 33) ^ 2 := by
      have he : 2 * (t + 33) ^ 2 = (t + 1 + 33) ^ 2 + t ^ 2 + 64 * t + 1022 := by ring
      omega
    have hm : 19 * (t + 1 + 33) ^ 2 + c + 1 ≤
        2 * (19 * (t + 33) ^ 2 + c + 1) := by omega
    have hmul := Nat.mul_le_mul_left (8 * A) hm
    rw [pow_succ 2 t]
    nlinarith

theorem semilla_del_fallo {n r c : ℕ} {a b : ℕ → ℕ}
    (hL : LMNDebil) (hw : Palabra n a b r) (hr : 0 < r) (hrc : r ≤ 2 ^ c)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hk2 : 2 ≤ tiempo a b r) :
    n < 2 ^ (19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2 + c) := by
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
  calc
    n < r * 2 ^ (19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2) := hsem
    _ ≤ 2 ^ c * 2 ^ (19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2) :=
      Nat.mul_le_mul_right _ hrc
    _ = _ := by rw [← pow_add, Nat.add_comm]

theorem log_tiempo_del_fallo {R A c H n r : ℕ} {a b : ℕ → ℕ}
    (hL : LMNDebil) (hR : R ≤ 2 ^ c)
    (hA : 5 * 8 ^ R ≤ (3 * A + 5) * 5 ^ R)
    (hbase : 8 * A * (19 * (H + 33) ^ 2 + c + 1) + 5 < 5 * 2 ^ H)
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ R)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hk2 : 2 ≤ tiempo a b r) : Nat.log 2 (tiempo a b r) < H := by
  by_contra h
  have ht : H ≤ Nat.log 2 (tiempo a b r) := by omega
  have hn := semilla_del_fallo hL hw hr (le_trans hrR hR) hk hf hk2
  have hn2 : n + 1 < 2 ^ (19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2 + c + 1) := by
    rw [pow_succ]
    omega
  have hc := criba_desde_trayectoria hw hn2
  have hmono := cota_monotona (by omega : 1 ≤ 19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2 + c + 1) hrR
  have hgeom := OcelotasGeometrica.cota_lineal hA
    (19 * (Nat.log 2 (tiempo a b r) + 33) ^ 2 + c + 1)
  have hki := OcelotasTiempoRacional.tiempo_del_cruce hk
  have hlo := Nat.pow_log_le_self 2 (by omega : tiempo a b r ≠ 0)
  have hcola := margen_cola hbase ht
  simp only [Nat.mul_assoc] at hcola
  omega

/-- Un certificado de tres desigualdades enteras acota todos los fallos con r <= R. -/
theorem region_del_fallo {R A c H n k : ℕ}
    (hL : LMNDebil) (hR : R ≤ 2 ^ c)
    (hA : 5 * 8 ^ R ≤ (3 * A + 5) * 5 ^ R)
    (hbase : 8 * A * (19 * (H + 33) ^ 2 + c + 1) + 5 < 5 * 2 ^ H)
    (hn : 2 ≤ n) (hk : PrimerCruce n k) (hrR : rachas n k ≤ R)
    (hf : n ≤ T^[k] n) :
    k < 2 ^ H ∧ n < 2 ^ (19 * (H + 32) ^ 2 + c) := by
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
    have hlog := log_tiempo_del_fallo hL hR hA hbase hw hpos hrR hkw hfw (by omega)
    have hsem := semilla_del_fallo hL hw hpos (le_trans hrR hR) hkw hfw (by omega)
    rw [he] at hlog hsem
    have hhi := Nat.lt_pow_succ_log_self (by decide : 1 < 2) k
    refine ⟨lt_of_lt_of_le hhi (Nat.pow_le_pow_right (by decide) (by omega)), ?_⟩
    apply lt_of_lt_of_le hsem
    apply Nat.pow_le_pow_right (by decide)
    have ht : Nat.log 2 k + 33 ≤ H + 32 := by omega
    nlinarith

theorem region_del_fallo_corolario {R A c H n k : ℕ}
    (hL : OcelotasLMNFuente.LMN23) (hR : R ≤ 2 ^ c)
    (hA : 5 * 8 ^ R ≤ (3 * A + 5) * 5 ^ R)
    (hbase : 8 * A * (19 * (H + 33) ^ 2 + c + 1) + 5 < 5 * 2 ^ H)
    (hn : 2 ≤ n) (hk : PrimerCruce n k) (hrR : rachas n k ≤ R)
    (hf : n ≤ T^[k] n) :
    k < 2 ^ H ∧ n < 2 ^ (19 * (H + 32) ^ 2 + c) :=
  region_del_fallo (OcelotasLMNFuente.debil_de_corolario hL) hR hA hbase hn hk hrR hf

theorem cst_en_cola {R A c H n k : ℕ}
    (hL : LMNDebil) (hR : R ≤ 2 ^ c)
    (hA : 5 * 8 ^ R ≤ (3 * A + 5) * 5 ^ R)
    (hbase : 8 * A * (19 * (H + 33) ^ 2 + c + 1) + 5 < 5 * 2 ^ H)
    (hn : 2 ≤ n) (hk : PrimerCruce n k) (hrR : rachas n k ≤ R)
    (hgrande : 2 ^ H ≤ k) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n := by
  refine ⟨fun _ hj => no_desciende_antes hk hj, ?_⟩
  by_contra hf
  have h := (region_del_fallo hL hR hA hbase hn hk hrR (by omega)).1
  omega

end OcelotasColaParametrica

#print axioms OcelotasColaParametrica.margen_cola
#print axioms OcelotasColaParametrica.semilla_del_fallo
#print axioms OcelotasColaParametrica.log_tiempo_del_fallo
#print axioms OcelotasColaParametrica.region_del_fallo
#print axioms OcelotasColaParametrica.region_del_fallo_corolario
#print axioms OcelotasColaParametrica.cst_en_cola
