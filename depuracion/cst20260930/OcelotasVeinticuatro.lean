import OcelotasVeinticuatroTabla
import OcelotasResiduosFinito
import OcelotasColaParametrica

/-! # Ocelotas: ensamblaje propuesto para 24 rachas bajo LMN

La tabla de 43 intervalos y dos ventanas por prefijos se unen al
certificado interno hasta 4912740 y a la cola paramétrica H=35.
LMN23 es la única hipótesis matemática externa. No se afirma
existencia universal del primer cruce ni llegada a 1.
-/

namespace OcelotasVeinticuatro

open Ocelotas OcelotasTrayectorias OcelotasContador OcelotasLMN OcelotasLMNFuente

theorem descenso_palabra (hL : LMNDebil) {n r : ℕ} {a b : ℕ → ℕ}
    (hn : 2 ≤ n) (hw : Palabra n a b r) (hr : 0 < r) (hr24 : r ≤ 24)
    (hcontador : rachas n (tiempo a b r) ≤ 24)
    (hk : PrimerCruce n (tiempo a b r)) : T^[tiempo a b r] n < n := by
  by_contra h
  have hf : n ≤ T^[tiempo a b r] n := by omega
  by_cases hq : S (tiempo a b r) n < 39123338641
  · have hsmall := OcelotasVeinticuatroTabla.pequeno_de_tabla hw hr hr24 hcontador hk hf hq
    have hd := OcelotasResiduosFinito.descenso_finito hn (by omega : n ≤ 4912740) hk
    omega
  · have hqk : S (tiempo a b r) n < tiempo a b r := by
      have hpow : 2 ^ S (tiempo a b r) n < 2 ^ tiempo a b r :=
        lt_of_le_of_lt (Nat.pow_le_pow_left (by norm_num) _) hk.2
      exact (Nat.pow_lt_pow_iff_right (by norm_num)).1 hpow
    have h35 : (2 : ℕ) ^ 35 = 34359738368 := by norm_num
    have hd := OcelotasColaParametrica.cst_en_cola (R := 24)
      (A := 132046) (c := 5) (H := 35) hL
      (by decide +kernel) (by decide +kernel) (by decide +kernel)
      hn hk hcontador (by omega)
    omega

theorem descenso_contador (hL : LMNDebil) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 24) : T^[k] n < n := by
  by_cases hpar : n % 2 = 0
  · exact OcelotasCierre.descenso_par hn hpar hk
  · obtain ⟨hpos, a, b, hw, he⟩ := palabra_del_cruce (by omega : n % 2 = 1) hk
    have hcontador : rachas n (tiempo a b (rachas n k)) ≤ 24 := by rwa [he]
    have hd := descenso_palabra hL hn hw hpos hr hcontador
    rw [he] at hd
    exact hd hk

theorem cst_veinticuatro_lmn (hL : LMNDebil) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 24) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n :=
  ⟨fun _ hj => no_desciende_antes hk hj, descenso_contador hL hn hk hr⟩

theorem cst_veinticuatro_corolario (hL : LMN23) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 24) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n :=
  cst_veinticuatro_lmn (debil_de_corolario hL) hn hk hr

theorem fallo_exige_veinticinco (hL : LMNDebil) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hf : n ≤ T^[k] n) : 25 ≤ rachas n k := by
  by_contra h
  have hd := descenso_contador hL hn hk (by omega : rachas n k ≤ 24)
  omega

end OcelotasVeinticuatro

#print axioms OcelotasVeinticuatro.descenso_palabra
#print axioms OcelotasVeinticuatro.descenso_contador
#print axioms OcelotasVeinticuatro.cst_veinticuatro_lmn
#print axioms OcelotasVeinticuatro.cst_veinticuatro_corolario
#print axioms OcelotasVeinticuatro.fallo_exige_veinticinco
