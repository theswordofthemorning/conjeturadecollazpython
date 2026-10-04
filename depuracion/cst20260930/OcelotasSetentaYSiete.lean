import OcelotasSetentaYSieteTabla
import OcelotasColaParametrica

/-! # Ocelotas: ensamblaje de 77 rachas bajo dos resultados externos

Se asumen LMN23 y el corolario 5.4 de Rozier-Terracol (v5).
La tabla numerica y la exclusion de la cola se certifican en Lean.
El resultado finito externo NO es un censo comprobado aqui.
-/

namespace OcelotasSetentaYSiete

open Ocelotas OcelotasTrayectorias OcelotasContador OcelotasLMN OcelotasLMNFuente

/-- Consecuencia usada de Rozier-Terracol, arXiv:2502.00948v5, corolario 5.4.
Es una hipotesis explicita; esta definicion no demuestra el corolario externo. -/
def RozierTerracol54 : Prop :=
  ∀ {n k : ℕ}, 2 ≤ n → n ≤ 28000000000000000000 → PrimerCruce n k → T^[k] n < n

theorem descenso_palabra (hL : LMNDebil) (hRT : RozierTerracol54)
    {n r : ℕ} {a b : ℕ → ℕ} (hn : 2 ≤ n) (hw : Palabra n a b r)
    (hr : 0 < r) (hr77 : r ≤ 77) (hcontador : rachas n (tiempo a b r) ≤ 77)
    (hk : PrimerCruce n (tiempo a b r)) : T^[tiempo a b r] n < n := by
  by_contra h
  have hf : n ≤ T^[tiempo a b r] n := by omega
  by_cases hq : S (tiempo a b r) n < 4857481135601629720741
  · have hsmall := OcelotasSetentaYSieteTabla.pequeno_de_tabla hw hr hr77 hcontador hk hf hq
    have hd := hRT hn (by omega) hk
    omega
  · have hqk : S (tiempo a b r) n < tiempo a b r := by
      have hpow : 2 ^ S (tiempo a b r) n < 2 ^ tiempo a b r :=
        lt_of_le_of_lt (Nat.pow_le_pow_left (by norm_num) _) hk.2
      exact (Nat.pow_lt_pow_iff_right (by norm_num)).1 hpow
    have h72 : (2 : ℕ) ^ 72 = 4722366482869645213696 := by norm_num
    have hd := OcelotasColaParametrica.cst_en_cola (R := 77)
      (A := 8691353499027139) (c := 7) (H := 72) hL
      (by decide +kernel) (by decide +kernel) (by decide +kernel)
      hn hk hcontador (by omega)
    omega

theorem descenso_contador (hL : LMNDebil) (hRT : RozierTerracol54)
    {n k : ℕ} (hn : 2 ≤ n) (hk : PrimerCruce n k) (hr : rachas n k ≤ 77) :
    T^[k] n < n := by
  by_cases hpar : n % 2 = 0
  · exact OcelotasCierre.descenso_par hn hpar hk
  · obtain ⟨hpos, a, b, hw, he⟩ := palabra_del_cruce (by omega : n % 2 = 1) hk
    have hcontador : rachas n (tiempo a b (rachas n k)) ≤ 77 := by rwa [he]
    have hd := descenso_palabra hL hRT hn hw hpos hr hcontador
    rw [he] at hd
    exact hd hk

theorem cst_condicional (hL : LMN23) (hRT : RozierTerracol54)
    {n k : ℕ} (hn : 2 ≤ n) (hk : PrimerCruce n k) (hr : rachas n k ≤ 77) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n :=
  ⟨fun _ hj => no_desciende_antes hk hj,
    descenso_contador (debil_de_corolario hL) hRT hn hk hr⟩

theorem fallo_exige_setenta_y_ocho (hL : LMN23) (hRT : RozierTerracol54)
    {n k : ℕ} (hn : 2 ≤ n) (hk : PrimerCruce n k) (hf : n ≤ T^[k] n) :
    78 ≤ rachas n k := by
  by_contra h
  have hd := (cst_condicional hL hRT hn hk (by omega)).2
  omega

end OcelotasSetentaYSiete

#print axioms OcelotasSetentaYSiete.descenso_palabra
#print axioms OcelotasSetentaYSiete.descenso_contador
#print axioms OcelotasSetentaYSiete.cst_condicional
#print axioms OcelotasSetentaYSiete.fallo_exige_setenta_y_ocho
