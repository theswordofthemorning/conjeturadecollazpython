import OcelotasVeintidosTabla
import OcelotasResiduosFinito
import OcelotasVeintidosCola
import OcelotasLMNFuente

/-! # Ocelotas: CST hasta veintidos rachas, bajo LMN

La tabla de cuarenta y dos intervalos, las semillas hasta 4912740, dos
certificados por prefijos y el puente desde q >= 4598951775 y la cola desde k >= 2^33 se ensamblan aquí.
La única hipótesis externa es LMN.
No se afirma existencia universal del primer cruce ni llegada a 1.
-/

namespace OcelotasVeintidos

open Ocelotas OcelotasTrayectorias OcelotasContador OcelotasLMN OcelotasLMNFuente

theorem descenso_palabra (hL : LMNDebil) {n r : ℕ} {a b : ℕ → ℕ}
    (hn : 2 ≤ n) (hw : Palabra n a b r) (hr : 0 < r) (hr22 : r ≤ 22)
    (hcontador : rachas n (tiempo a b r) ≤ 22)
    (hk : PrimerCruce n (tiempo a b r)) : T^[tiempo a b r] n < n := by
  by_contra h
  have hf : n ≤ T^[tiempo a b r] n := by omega
  by_cases hq : S (tiempo a b r) n < 4598951775
  · have hsmall := OcelotasVeintidosTabla.pequeno_de_tabla hw hr hr22 hcontador hk hf hq
    have hd := OcelotasResiduosFinito.descenso_finito hn (by omega : n ≤ 4912740) hk
    omega
  · have hqk : S (tiempo a b r) n < tiempo a b r := by
      have hpow : 2 ^ S (tiempo a b r) n < 2 ^ tiempo a b r :=
        lt_of_le_of_lt (Nat.pow_le_pow_left (by norm_num) _) hk.2
      exact (Nat.pow_lt_pow_iff_right (by norm_num)).1 hpow
    have h32 : (2 : ℕ) ^ 32 = 4294967296 := by norm_num
    exact OcelotasVeintidosCola.sin_fallo_cola hL hw hr hr22 hk hf (by omega) (by omega)

theorem descenso_contador (hL : LMNDebil) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 22) : T^[k] n < n := by
  by_cases hpar : n % 2 = 0
  · exact OcelotasCierre.descenso_par hn hpar hk
  · obtain ⟨hpos, a, b, hw, he⟩ := palabra_del_cruce (by omega : n % 2 = 1) hk
    have hcontador : rachas n (tiempo a b (rachas n k)) ≤ 22 := by rwa [he]
    have hd := descenso_palabra hL hn hw hpos hr hcontador
    rw [he] at hd
    exact hd hk

/-- Primer descenso = primer cruce para hasta veintidos rachas, bajo LMNDebil. -/
theorem cst_veintidos_lmn (hL : LMNDebil) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 22) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n :=
  ⟨fun _ hj => no_desciende_antes hk hj, descenso_contador hL hn hk hr⟩

/-- Mismo cierre desde el corolario publicado, especializado en log 2 y log 3. -/
theorem cst_veintidos_corolario (hL : LMN23) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 22) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n :=
  cst_veintidos_lmn (debil_de_corolario hL) hn hk hr

theorem fallo_exige_veintitres (hL : LMNDebil) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hf : n ≤ T^[k] n) : 23 ≤ rachas n k := by
  by_contra h
  have hd := descenso_contador hL hn hk (by omega : rachas n k ≤ 22)
  omega

end OcelotasVeintidos

#print axioms OcelotasVeintidos.descenso_palabra
#print axioms OcelotasVeintidos.descenso_contador
#print axioms OcelotasVeintidos.cst_veintidos_lmn
#print axioms OcelotasVeintidos.cst_veintidos_corolario
#print axioms OcelotasVeintidos.fallo_exige_veintitres
