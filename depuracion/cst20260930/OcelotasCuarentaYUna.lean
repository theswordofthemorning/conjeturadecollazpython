import OcelotasCuarentaYUnaTabla
import OcelotasColaParametrica
import OcelotasCierre

/-! # Ocelotas: 41 rachas con LMN y un censo propio, sin Rozier-Terracol

Se asumen LMN23 y `CensoPropio2e11`: el descenso en el primer cruce para
2 <= n <= 2·10^11. Ese censo se calculó fuera de Lean (`censo_cst.py`); aquí es
una hipótesis explícita, no un axioma. Es consecuencia inmediata del corolario
de Rozier-Terracol, pero este enunciado no lo usa.
-/

namespace OcelotasCuarentaYUna

open Ocelotas OcelotasTrayectorias OcelotasContador OcelotasLMN OcelotasLMNFuente

/-- Censo propio: descenso en el primer cruce para 2 <= n <= 2·10^11. Hipótesis explícita. -/
def CensoPropio2e11 : Prop :=
  ∀ {n k : ℕ}, 2 ≤ n → n ≤ 200000000000 → PrimerCruce n k → T^[k] n < n

theorem descenso_palabra (hL : LMNDebil) (hC : CensoPropio2e11)
    {n r : ℕ} {a b : ℕ → ℕ} (hn : 2 ≤ n) (hw : Palabra n a b r)
    (hr : 0 < r) (hr41 : r ≤ 41) (hcontador : rachas n (tiempo a b r) ≤ 41)
    (hk : PrimerCruce n (tiempo a b r)) : T^[tiempo a b r] n < n := by
  by_contra h
  have hf : n ≤ T^[tiempo a b r] n := by omega
  by_cases hq : S (tiempo a b r) n < 2365627332311699
  · have hsmall := OcelotasCuarentaYUnaTabla.pequeno_de_tabla hw hr hr41 hk hf hq
    have hd := hC hn (by omega) hk
    omega
  · have hqk : S (tiempo a b r) n < tiempo a b r := by
      have hpow : 2 ^ S (tiempo a b r) n < 2 ^ tiempo a b r :=
        lt_of_le_of_lt (Nat.pow_le_pow_left (by norm_num) _) hk.2
      exact (Nat.pow_lt_pow_iff_right (by norm_num)).1 hpow
    have h51 : (2 : ℕ) ^ 51 = 2251799813685248 := by norm_num
    have hd := OcelotasColaParametrica.cst_en_cola (R := 41)
      (A := 389733769) (c := 7) (H := 51) hL
      (by decide +kernel) (by decide +kernel) (by decide +kernel)
      hn hk hcontador (by omega)
    omega

theorem descenso_contador (hL : LMNDebil) (hC : CensoPropio2e11)
    {n k : ℕ} (hn : 2 ≤ n) (hk : PrimerCruce n k) (hr : rachas n k ≤ 41) :
    T^[k] n < n := by
  by_cases hpar : n % 2 = 0
  · exact OcelotasCierre.descenso_par hn hpar hk
  · obtain ⟨hpos, a, b, hw, he⟩ := palabra_del_cruce (by omega : n % 2 = 1) hk
    have hcontador : rachas n (tiempo a b (rachas n k)) ≤ 41 := by rwa [he]
    have hd := descenso_palabra hL hC hn hw hpos hr hcontador
    rw [he] at hd
    exact hd hk

theorem cst_condicional (hL : LMN23) (hC : CensoPropio2e11)
    {n k : ℕ} (hn : 2 ≤ n) (hk : PrimerCruce n k) (hr : rachas n k ≤ 41) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n :=
  ⟨fun _ hj => no_desciende_antes hk hj,
    descenso_contador (debil_de_corolario hL) hC hn hk hr⟩

theorem fallo_exige_cuarenta_y_dos (hL : LMN23) (hC : CensoPropio2e11)
    {n k : ℕ} (hn : 2 ≤ n) (hk : PrimerCruce n k) (hf : n ≤ T^[k] n) :
    42 ≤ rachas n k := by
  by_contra h
  have hd := (cst_condicional hL hC hn hk (by omega)).2
  omega

end OcelotasCuarentaYUna

#print axioms OcelotasCuarentaYUna.descenso_palabra
#print axioms OcelotasCuarentaYUna.descenso_contador
#print axioms OcelotasCuarentaYUna.cst_condicional
#print axioms OcelotasCuarentaYUna.fallo_exige_cuarenta_y_dos
