import OcelotasRhin
import OcelotasColaParametrica

/-! Cola parametrica bajo Rhin; la cota trascendente sigue como premisa.
El umbral 2 corresponde a la version explicita con exponente 13.3.
La comparacion con LMN mantiene la misma cota geometrica de las rachas.
-/

namespace OcelotasColaRhin

open Ocelotas OcelotasRachas OcelotasTrayectorias OcelotasContador OcelotasRhin

theorem margen_cola {A c H : ℕ}
    (hbase : 8 * A * (14 * (H + 1) + c + 1) + 5 < 5 * 2 ^ H)
    {t : ℕ} (ht : H ≤ t) :
    8 * A * (14 * (t + 1) + c + 1) + 5 < 5 * 2 ^ t := by
  induction t, ht using Nat.le_induction with
  | base => exact hbase
  | succ t ht ih =>
    have hm : 14 * (t + 1 + 1) + c + 1 ≤ 2 * (14 * (t + 1) + c + 1) := by omega
    have hmul := Nat.mul_le_mul_left (8 * A) hm
    rw [pow_succ 2 t]
    nlinarith

theorem log_tiempo_del_fallo {R A c H n r : ℕ} {a b : ℕ → ℕ}
    (hR : RhinDesde 2) (hRc : R ≤ 2 ^ c)
    (hA : 5 * 8 ^ R ≤ (3 * A + 5) * 5 ^ R)
    (hbase : 8 * A * (14 * (H + 1) + c + 1) + 5 < 5 * 2 ^ H)
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ R)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hk2 : 2 ≤ tiempo a b r) : Nat.log 2 (tiempo a b r) < H := by
  by_contra h
  have ht : H ≤ Nat.log 2 (tiempo a b r) := by omega
  have he := hR _ _ hk2 (ventana_cruce hk).2 hk.2
  have hn := fallo_rhin_punto hw hr hk hf he
  have hhi := Nat.lt_pow_succ_log_self (by decide : 1 < 2) (tiempo a b r)
  have hpot := Nat.pow_le_pow_left (Nat.le_of_lt hhi) 14
  have hmul := Nat.mul_le_mul (le_trans hrR hRc) hpot
  have hsem : n < 2 ^ (14 * (Nat.log 2 (tiempo a b r) + 1) + c) := by
    apply lt_of_lt_of_le hn
    calc
      _ ≤ 2 ^ c * (2 ^ (Nat.log 2 (tiempo a b r) + 1)) ^ 14 := hmul
      _ = _ := by
        rw [← pow_mul, ← pow_add]
        congr 1
        omega
  have hn2 : n + 1 < 2 ^ (14 * (Nat.log 2 (tiempo a b r) + 1) + c + 1) := by
    rw [pow_succ]
    omega
  have hc := criba_desde_trayectoria hw hn2
  have hmono := cota_monotona
    (by omega : 1 ≤ 14 * (Nat.log 2 (tiempo a b r) + 1) + c + 1) hrR
  have hgeom := OcelotasGeometrica.cota_lineal hA
    (14 * (Nat.log 2 (tiempo a b r) + 1) + c + 1)
  have hki := OcelotasTiempoRacional.tiempo_del_cruce hk
  have hlo := Nat.pow_log_le_self 2 (by omega : tiempo a b r ≠ 0)
  have hcola := margen_cola hbase ht
  simp only [Nat.mul_assoc] at hcola
  omega

theorem cst_en_cola {R A c H n k : ℕ}
    (hR : RhinDesde 2) (hRc : R ≤ 2 ^ c)
    (hA : 5 * 8 ^ R ≤ (3 * A + 5) * 5 ^ R)
    (hbase : 8 * A * (14 * (H + 1) + c + 1) + 5 < 5 * 2 ^ H)
    (hH : 1 ≤ H) (hn : 2 ≤ n) (hk : PrimerCruce n k)
    (hrR : rachas n k ≤ R) (hgrande : 2 ^ H ≤ k) : T^[k] n < n := by
  by_cases hpar : n % 2 = 0
  · exact OcelotasCierre.descenso_par hn hpar hk
  · by_contra h
    have hf : n ≤ T^[k] n := by omega
    have hk2 : 2 ≤ k := by
      have hp := Nat.pow_le_pow_right (by decide : 1 ≤ 2) hH
      norm_num at hp
      omega
    obtain ⟨hpos, a, b, hw, he⟩ := palabra_del_cruce (by omega : n % 2 = 1) hk
    have hkw : PrimerCruce n (tiempo a b (rachas n k)) := by rwa [he]
    have hfw : n ≤ T^[tiempo a b (rachas n k)] n := by rwa [he]
    have hlog := log_tiempo_del_fallo hR hRc hA hbase hw hpos hrR hkw hfw (by omega)
    rw [he] at hlog
    have hlow := Nat.le_log_of_pow_le (by decide : 1 < 2) hgrande
    omega

theorem cola_ochenta_y_tres (hR : RhinHomogenea 2) {n k : ℕ}
    (hn : 2 ≤ n) (hk : PrimerCruce n k) (hr : rachas n k ≤ 83)
    (hk68 : 2 ^ 68 ≤ k) : T^[k] n < n :=
  cst_en_cola (R := 83) (A := 145816714985534127) (c := 7) (H := 68)
    (desde_homogenea hR) (by decide +kernel) (by decide +kernel)
    (by decide +kernel) (by decide) hn hk hr hk68

end OcelotasColaRhin

#print axioms OcelotasColaRhin.margen_cola
#print axioms OcelotasColaRhin.log_tiempo_del_fallo
#print axioms OcelotasColaRhin.cst_en_cola
#print axioms OcelotasColaRhin.cola_ochenta_y_tres
