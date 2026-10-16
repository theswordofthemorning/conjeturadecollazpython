import OcelotasOchentaYTresTabla
import OcelotasColaParametrica
import OcelotasCierre

/-! # Ocelotas: 83 rachas mediante pesos por racha

LMN23 y CSTHastaRecord20260928 son hipotesis explicitas. La segunda es la
extension del argumento de Rozier-Terracol al record confirmado publicado
por Roosendaal el 28-09-2026. Este modulo no verifica ese censo externo.
-/

namespace OcelotasOchentaYTres

open Ocelotas OcelotasTrayectorias OcelotasContador OcelotasLMN OcelotasLMNFuente

/-- CST hasta el nuevo record. Hipotesis externa explicita; no se identifica
con el corolario 5.4 original, cuyo rango era menor. -/
def CSTHastaRecord20260928 : Prop :=
  ∀ {n k : ℕ}, 2 ≤ n → n ≤ 46645791847966786687 → PrimerCruce n k → T^[k] n < n

theorem descenso_palabra (hL : LMNDebil) (hRT : CSTHastaRecord20260928)
    {n r : ℕ} {a b : ℕ → ℕ} (hn : 2 ≤ n) (hw : Palabra n a b r)
    (hr : 0 < r) (hr83 : r ≤ 83) (hcontador : rachas n (tiempo a b r) ≤ 83)
    (hk : PrimerCruce n (tiempo a b r)) : T^[tiempo a b r] n < n := by
  by_contra h
  have hf : n ≤ T^[tiempo a b r] n := by omega
  by_cases hq : S (tiempo a b r) n < 101189215254399926676993
  · have hsmall := OcelotasOchentaYTresTabla.pequeno_de_tabla hw hr hr83 hk hf hq
    have hd := hRT hn (by omega) hk
    omega
  · have hqk : S (tiempo a b r) n < tiempo a b r := by
      have hpow : 2 ^ S (tiempo a b r) n < 2 ^ tiempo a b r :=
        lt_of_le_of_lt (Nat.pow_le_pow_left (by norm_num) _) hk.2
      exact (Nat.pow_lt_pow_iff_right (by norm_num)).1 hpow
    have h76 : (2 : ℕ) ^ 76 = 75557863725914323419136 := by norm_num
    have hd := OcelotasColaParametrica.cst_en_cola (R := 83)
      (A := 145816714985534127) (c := 7) (H := 76) hL
      (by decide +kernel) (by decide +kernel) (by decide +kernel)
      hn hk hcontador (by omega)
    omega

theorem descenso_contador (hL : LMNDebil) (hRT : CSTHastaRecord20260928)
    {n k : ℕ} (hn : 2 ≤ n) (hk : PrimerCruce n k) (hr : rachas n k ≤ 83) :
    T^[k] n < n := by
  by_cases hpar : n % 2 = 0
  · exact OcelotasCierre.descenso_par hn hpar hk
  · obtain ⟨hpos, a, b, hw, he⟩ := palabra_del_cruce (by omega : n % 2 = 1) hk
    have hcontador : rachas n (tiempo a b (rachas n k)) ≤ 83 := by rwa [he]
    have hd := descenso_palabra hL hRT hn hw hpos hr hcontador
    rw [he] at hd
    exact hd hk

theorem cst_condicional (hL : LMN23) (hRT : CSTHastaRecord20260928)
    {n k : ℕ} (hn : 2 ≤ n) (hk : PrimerCruce n k) (hr : rachas n k ≤ 83) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n :=
  ⟨fun _ hj => no_desciende_antes hk hj,
    descenso_contador (debil_de_corolario hL) hRT hn hk hr⟩

theorem fallo_exige_ochenta_y_cuatro (hL : LMN23) (hRT : CSTHastaRecord20260928)
    {n k : ℕ} (hn : 2 ≤ n) (hk : PrimerCruce n k) (hf : n ≤ T^[k] n) :
    84 ≤ rachas n k := by
  by_contra h
  have hd := (cst_condicional hL hRT hn hk (by omega)).2
  omega

end OcelotasOchentaYTres

#print axioms OcelotasOchentaYTres.descenso_palabra
#print axioms OcelotasOchentaYTres.descenso_contador
#print axioms OcelotasOchentaYTres.cst_condicional
#print axioms OcelotasOchentaYTres.fallo_exige_ochenta_y_cuatro
