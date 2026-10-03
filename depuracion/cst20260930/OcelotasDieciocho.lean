import OcelotasDieciochoTabla
import OcelotasResiduosFinito
import OcelotasDieciochoCola
import OcelotasLMNFuente

/-! # Ocelotas: CST hasta dieciocho rachas, bajo LMN

La tabla de cuarenta y dos intervalos, las semillas hasta 4912740 y la cola
desde k >= 2^31 están certificadas. La única hipótesis externa es LMN.
No se afirma existencia universal del primer cruce ni llegada a 1.
-/

namespace OcelotasDieciocho

open Ocelotas OcelotasTrayectorias OcelotasContador OcelotasLMN OcelotasLMNFuente

theorem descenso_palabra (hL : LMNDebil) {n r : ℕ} {a b : ℕ → ℕ}
    (hn : 2 ≤ n) (hw : Palabra n a b r) (hr : 0 < r) (hr18 : r ≤ 18)
    (hk : PrimerCruce n (tiempo a b r)) : T^[tiempo a b r] n < n := by
  by_contra h
  have hf : n ≤ T^[tiempo a b r] n := by omega
  by_cases hq : S (tiempo a b r) n < 2213511501
  · have hsmall := OcelotasDieciochoTabla.pequeno_de_tabla hw hr hr18 hk hf hq
    have hd := OcelotasResiduosFinito.descenso_finito hn (by omega : n ≤ 4912740) hk
    omega
  · have hqk : S (tiempo a b r) n < tiempo a b r := by
      have hpow : 2 ^ S (tiempo a b r) n < 2 ^ tiempo a b r :=
        lt_of_le_of_lt (Nat.pow_le_pow_left (by norm_num) _) hk.2
      exact (Nat.pow_lt_pow_iff_right (by norm_num)).1 hpow
    have h31 : (2 : ℕ) ^ 31 = 2147483648 := by norm_num
    exact OcelotasDieciochoCola.sin_fallo_cola hL hw hr hr18 hk hf (by omega)

theorem descenso_contador (hL : LMNDebil) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 18) : T^[k] n < n := by
  by_cases hpar : n % 2 = 0
  · exact OcelotasCierre.descenso_par hn hpar hk
  · obtain ⟨hpos, a, b, hw, he⟩ := palabra_del_cruce (by omega : n % 2 = 1) hk
    have hd := descenso_palabra hL hn hw hpos hr
    rw [he] at hd
    exact hd hk

/-- Primer descenso = primer cruce para hasta dieciocho rachas, bajo LMNDebil. -/
theorem cst_dieciocho_lmn (hL : LMNDebil) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 18) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n :=
  ⟨fun _ hj => no_desciende_antes hk hj, descenso_contador hL hn hk hr⟩

/-- Mismo cierre desde el corolario publicado, especializado en log 2 y log 3. -/
theorem cst_dieciocho_corolario (hL : LMN23) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 18) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n :=
  cst_dieciocho_lmn (debil_de_corolario hL) hn hk hr

theorem fallo_exige_diecinueve (hL : LMNDebil) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hf : n ≤ T^[k] n) : 19 ≤ rachas n k := by
  by_contra h
  have hd := descenso_contador hL hn hk (by omega : rachas n k ≤ 18)
  omega

end OcelotasDieciocho

#print axioms OcelotasDieciocho.descenso_palabra
#print axioms OcelotasDieciocho.descenso_contador
#print axioms OcelotasDieciocho.cst_dieciocho_lmn
#print axioms OcelotasDieciocho.cst_dieciocho_corolario
#print axioms OcelotasDieciocho.fallo_exige_diecinueve
