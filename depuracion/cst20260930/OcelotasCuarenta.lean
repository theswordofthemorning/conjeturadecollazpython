import OcelotasCuarentaTabla
import OcelotasColaParametrica
import OcelotasCierre

/-! # Ocelotas: 40 rachas con LMN y un censo propio, sin Rozier-Terracol

Se asumen LMN23 y `CensoPropio36`: el descenso en el primer cruce para
2 <= n <= 2^36. Ese censo se calculó fuera de Lean (`censo_cst.py`); aquí es
una hipótesis explícita, no un axioma. Es consecuencia inmediata del corolario
de Rozier-Terracol, pero este enunciado no lo usa.
-/

namespace OcelotasCuarenta

open Ocelotas OcelotasTrayectorias OcelotasContador OcelotasLMN OcelotasLMNFuente

/-- Censo propio: descenso en el primer cruce para 2 <= n <= 2^36. Hipótesis explícita. -/
def CensoPropio36 : Prop :=
  ∀ {n k : ℕ}, 2 ≤ n → n ≤ 68719476736 → PrimerCruce n k → T^[k] n < n

theorem descenso_palabra (hL : LMNDebil) (hC : CensoPropio36)
    {n r : ℕ} {a b : ℕ → ℕ} (hn : 2 ≤ n) (hw : Palabra n a b r)
    (hr : 0 < r) (hr40 : r ≤ 40) (hcontador : rachas n (tiempo a b r) ≤ 40)
    (hk : PrimerCruce n (tiempo a b r)) : T^[tiempo a b r] n < n := by
  by_contra h
  have hf : n ≤ T^[tiempo a b r] n := by omega
  by_cases hq : S (tiempo a b r) n < 2365627332311699
  · have hsmall := OcelotasCuarentaTabla.pequeno_de_tabla hw hr hr40 hk hf hq
    have hd := hC hn (by omega) hk
    omega
  · have hqk : S (tiempo a b r) n < tiempo a b r := by
      have hpow : 2 ^ S (tiempo a b r) n < 2 ^ tiempo a b r :=
        lt_of_le_of_lt (Nat.pow_le_pow_left (by norm_num) _) hk.2
      exact (Nat.pow_lt_pow_iff_right (by norm_num)).1 hpow
    have h51 : (2 : ℕ) ^ 51 = 2251799813685248 := by norm_num
    have hd := OcelotasColaParametrica.cst_en_cola (R := 40)
      (A := 243583605) (c := 7) (H := 51) hL
      (by decide +kernel) (by decide +kernel) (by decide +kernel)
      hn hk hcontador (by omega)
    omega

theorem descenso_contador (hL : LMNDebil) (hC : CensoPropio36)
    {n k : ℕ} (hn : 2 ≤ n) (hk : PrimerCruce n k) (hr : rachas n k ≤ 40) :
    T^[k] n < n := by
  by_cases hpar : n % 2 = 0
  · exact OcelotasCierre.descenso_par hn hpar hk
  · obtain ⟨hpos, a, b, hw, he⟩ := palabra_del_cruce (by omega : n % 2 = 1) hk
    have hcontador : rachas n (tiempo a b (rachas n k)) ≤ 40 := by rwa [he]
    have hd := descenso_palabra hL hC hn hw hpos hr hcontador
    rw [he] at hd
    exact hd hk

theorem cst_condicional (hL : LMN23) (hC : CensoPropio36)
    {n k : ℕ} (hn : 2 ≤ n) (hk : PrimerCruce n k) (hr : rachas n k ≤ 40) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n :=
  ⟨fun _ hj => no_desciende_antes hk hj,
    descenso_contador (debil_de_corolario hL) hC hn hk hr⟩

theorem fallo_exige_cuarenta_y_una (hL : LMN23) (hC : CensoPropio36)
    {n k : ℕ} (hn : 2 ≤ n) (hk : PrimerCruce n k) (hf : n ≤ T^[k] n) :
    41 ≤ rachas n k := by
  by_contra h
  have hd := (cst_condicional hL hC hn hk (by omega)).2
  omega

end OcelotasCuarenta

#print axioms OcelotasCuarenta.descenso_palabra
#print axioms OcelotasCuarenta.descenso_contador
#print axioms OcelotasCuarenta.cst_condicional
#print axioms OcelotasCuarenta.fallo_exige_cuarenta_y_una
