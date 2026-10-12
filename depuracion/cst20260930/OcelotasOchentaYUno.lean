import OcelotasOchentaYUnoTabla
import OcelotasColaParametrica
import OcelotasCierre

/-! # Ocelotas: 81 rachas mediante pesos por racha

Se asumen LMN23 y el corolario 5.4 de Rozier-Terracol (v5). `RozierTerracol54`
repite literalmente la definición de `OcelotasSetentaYSiete`, sin importar
aquel módulo y su árbol de prefijos.
La tabla usa la criba de pesos de `OcelotasPesos`; no hay árbol de prefijos.
El resultado finito externo NO es un censo comprobado aquí.
-/

namespace OcelotasOchentaYUno

open Ocelotas OcelotasTrayectorias OcelotasContador OcelotasLMN OcelotasLMNFuente

/-- Consecuencia usada de Rozier-Terracol, arXiv:2502.00948v5, corolario 5.4.
Es una hipotesis explicita; esta definicion no demuestra el corolario externo. -/
def RozierTerracol54 : Prop :=
  ∀ {n k : ℕ}, 2 ≤ n → n ≤ 28000000000000000000 → PrimerCruce n k → T^[k] n < n

theorem descenso_palabra (hL : LMNDebil) (hRT : RozierTerracol54)
    {n r : ℕ} {a b : ℕ → ℕ} (hn : 2 ≤ n) (hw : Palabra n a b r)
    (hr : 0 < r) (hr81 : r ≤ 81) (hcontador : rachas n (tiempo a b r) ≤ 81)
    (hk : PrimerCruce n (tiempo a b r)) : T^[tiempo a b r] n < n := by
  by_contra h
  have hf : n ≤ T^[tiempo a b r] n := by omega
  by_cases hq : S (tiempo a b r) n < 38887293218019448937881
  · have hsmall := OcelotasOchentaYUnoTabla.pequeno_de_tabla hw hr hr81 hk hf hq
    have hd := hRT hn (by omega) hk
    omega
  · have hqk : S (tiempo a b r) n < tiempo a b r := by
      have hpow : 2 ^ S (tiempo a b r) n < 2 ^ tiempo a b r :=
        lt_of_le_of_lt (Nat.pow_le_pow_left (by norm_num) _) hk.2
      exact (Nat.pow_lt_pow_iff_right (by norm_num)).1 hpow
    have h75 : (2 : ℕ) ^ 75 = 37778931862957161709568 := by norm_num
    have hd := OcelotasColaParametrica.cst_en_cola (R := 81)
      (A := 56959654291224268) (c := 7) (H := 75) hL
      (by decide +kernel) (by decide +kernel) (by decide +kernel)
      hn hk hcontador (by omega)
    omega

theorem descenso_contador (hL : LMNDebil) (hRT : RozierTerracol54)
    {n k : ℕ} (hn : 2 ≤ n) (hk : PrimerCruce n k) (hr : rachas n k ≤ 81) :
    T^[k] n < n := by
  by_cases hpar : n % 2 = 0
  · exact OcelotasCierre.descenso_par hn hpar hk
  · obtain ⟨hpos, a, b, hw, he⟩ := palabra_del_cruce (by omega : n % 2 = 1) hk
    have hcontador : rachas n (tiempo a b (rachas n k)) ≤ 81 := by rwa [he]
    have hd := descenso_palabra hL hRT hn hw hpos hr hcontador
    rw [he] at hd
    exact hd hk

theorem cst_condicional (hL : LMN23) (hRT : RozierTerracol54)
    {n k : ℕ} (hn : 2 ≤ n) (hk : PrimerCruce n k) (hr : rachas n k ≤ 81) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n :=
  ⟨fun _ hj => no_desciende_antes hk hj,
    descenso_contador (debil_de_corolario hL) hRT hn hk hr⟩

theorem fallo_exige_ochenta_y_dos (hL : LMN23) (hRT : RozierTerracol54)
    {n k : ℕ} (hn : 2 ≤ n) (hk : PrimerCruce n k) (hf : n ≤ T^[k] n) :
    82 ≤ rachas n k := by
  by_contra h
  have hd := (cst_condicional hL hRT hn hk (by omega)).2
  omega

end OcelotasOchentaYUno

#print axioms OcelotasOchentaYUno.descenso_palabra
#print axioms OcelotasOchentaYUno.descenso_contador
#print axioms OcelotasOchentaYUno.cst_condicional
#print axioms OcelotasOchentaYUno.fallo_exige_ochenta_y_dos
