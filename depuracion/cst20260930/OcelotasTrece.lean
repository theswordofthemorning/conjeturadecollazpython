import OcelotasTreceTabla
import OcelotasTreceFinito
import OcelotasTreceCola
import OcelotasLMNFuente

/-! # Ocelotas: CST hasta trece rachas, bajo LMN

La tabla de cuarenta intervalos, las semillas hasta 31623 y la cola
desde k >= 2^27 están certificadas. La única hipótesis externa es LMN.
No se afirma existencia universal del primer cruce ni llegada a 1.
-/

namespace OcelotasTrece

open Ocelotas OcelotasTrayectorias OcelotasContador OcelotasLMN OcelotasLMNFuente

theorem descenso_palabra (hL : LMNDebil) {n r : ℕ} {a b : ℕ → ℕ}
    (hn : 2 ≤ n) (hw : Palabra n a b r) (hr : 0 < r) (hr13 : r ≤ 13)
    (hk : PrimerCruce n (tiempo a b r)) : T^[tiempo a b r] n < n := by
  by_contra h
  have hf : n ≤ T^[tiempo a b r] n := by omega
  by_cases hq : S (tiempo a b r) n < 171928773
  · have hsmall := OcelotasTreceTabla.pequeno_de_tabla hw hr hr13 hk hf hq
    have hd := OcelotasTreceFinito.descenso_finito hn (by omega : n ≤ 31623) hk
    omega
  · have hqk : S (tiempo a b r) n < tiempo a b r := by
      have hpow : 2 ^ S (tiempo a b r) n < 2 ^ tiempo a b r :=
        lt_of_le_of_lt (Nat.pow_le_pow_left (by norm_num) _) hk.2
      exact (Nat.pow_lt_pow_iff_right (by norm_num)).1 hpow
    have h27 : (2 : ℕ) ^ 27 = 134217728 := by norm_num
    exact OcelotasTreceCola.sin_fallo_cola hL hw hr hr13 hk hf (by omega)

theorem descenso_contador (hL : LMNDebil) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 13) : T^[k] n < n := by
  by_cases hpar : n % 2 = 0
  · exact OcelotasCierre.descenso_par hn hpar hk
  · obtain ⟨hpos, a, b, hw, he⟩ := palabra_del_cruce (by omega : n % 2 = 1) hk
    have hd := descenso_palabra hL hn hw hpos hr
    rw [he] at hd
    exact hd hk

/-- Primer descenso = primer cruce para hasta trece rachas, bajo LMNDebil. -/
theorem cst_trece_lmn (hL : LMNDebil) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 13) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n :=
  ⟨fun _ hj => no_desciende_antes hk hj, descenso_contador hL hn hk hr⟩

/-- Mismo cierre desde el corolario publicado, especializado en log 2 y log 3. -/
theorem cst_trece_corolario (hL : LMN23) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 13) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n :=
  cst_trece_lmn (debil_de_corolario hL) hn hk hr

theorem fallo_exige_catorce (hL : LMNDebil) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hf : n ≤ T^[k] n) : 14 ≤ rachas n k := by
  by_contra h
  have hd := descenso_contador hL hn hk (by omega : rachas n k ≤ 13)
  omega

end OcelotasTrece

#print axioms OcelotasTrece.descenso_palabra
#print axioms OcelotasTrece.descenso_contador
#print axioms OcelotasTrece.cst_trece_lmn
#print axioms OcelotasTrece.cst_trece_corolario
#print axioms OcelotasTrece.fallo_exige_catorce
