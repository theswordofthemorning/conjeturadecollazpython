import GarnerEnunciado
import GaoLiteral

/-! # Condoras: las dos conjeturas de Wu Jiabang (1992)

Wu, 《Collatz问题中同高连续数所占比例的变化趋势》, J. Huazhong Univ. Sci. Tech. 20 (1992),
n.º 5, 171–174. K cuenta los enteros de [1, M) que están en una w-upla (w ≥ 2) de
consecutivos con la misma altura, y `d(M) = K/(M − 1)`. Wu conjetura `lim d(M) = 1` y
`lim L = ∞`, con L la racha más larga de igual altura en [1, M).

* `wu_dos`: `lim L = ∞`. Sale de la conjetura de Garner (`GarnerEnunciado`, Alpacas).
* `wu_uno`: con `d(x) → 1` de Gao (`GaoLiteral`, Hienas), `lim d(M) = 1` equivale a que los
  n que llegan a 1 tengan densidad natural 1. Esa densidad sigue siendo un problema abierto.

La clave de `wu_uno` es `racha_de_coalescencia`: si n llega a 1 y coalesce con n+1 en el
sentido de Gao, los dos tienen la misma altura. Lo contrario es trivial: tener altura
es llegar a 1. -/

open Filter Topology

namespace CondorasWu

open GarnerEnunciado

/-- n llega a 1 con el mapa clásico. -/
def llega (n : ℕ) : Prop := ∃ h, C^[h] n = 1

/-- n está en una w-upla de Wu (w ≥ 2): comparte altura con n − 1 o con n + 1.
    Con n = 1, `n - 1 = 0` no tiene altura, así que sólo cuenta n + 1. -/
def enRacha (n : ℕ) : Prop := ∃ h, altura n h ∧ (altura (n - 1) h ∨ altura (n + 1) h)

open Classical in
/-- `d(M) = K/(M − 1)` de Wu. -/
noncomputable def dWu (M : ℕ) : ℝ :=
  (((Finset.Ico 1 M).filter enRacha).card : ℝ) / ((M : ℝ) - 1)

open Classical in
/-- Proporción de [1, M) que llega a 1, con la misma normalización. -/
noncomputable def rho (M : ℕ) : ℝ :=
  (((Finset.Ico 1 M).filter llega).card : ℝ) / ((M : ℝ) - 1)

/-- Hay k consecutivos n, …, n+k−1 de igual altura dentro de [1, M). -/
def rachaEn (M k : ℕ) : Prop := ∃ n h, 1 ≤ n ∧ n + k ≤ M ∧ ∀ i, i < k → altura (n + i) h

/-- `L(M)`: el largo de la racha más larga de igual altura dentro de [1, M). -/
noncomputable def Lmax (M : ℕ) : ℕ := sSup {k | rachaEn M k}

/-! ## Conjetura 2: lim L = ∞ -/

theorem acotado (M : ℕ) : BddAbove {k | rachaEn M k} := by
  refine ⟨M, ?_⟩
  rintro k ⟨n, h, hn, hk, -⟩
  omega

/-- Conjetura 2 de Wu: la racha más larga de igual altura en [1, M) crece sin tope. -/
theorem wu_dos : Tendsto Lmax atTop atTop := by
  rw [Filter.tendsto_atTop_atTop]
  intro K
  rcases Nat.eq_zero_or_pos K with rfl | hK
  · exact ⟨0, fun _ _ => Nat.zero_le _⟩
  obtain ⟨n, h, s, hn, hi⟩ := conjetura_garner (K - 1) 1
  refine ⟨n + K, fun M hM => le_csSup (acotado M) ⟨n, h, hn, hM, fun i hik => ?_⟩⟩
  exact (hi i (by omega)).1

/-! ## Conjetura 1: lim d(M) = 1 equivale a densidad 1 de los que llegan a 1 -/

theorem llega_de_racha {n : ℕ} (h : enRacha n) : llega n := by
  obtain ⟨k, hk, -⟩ := h
  exact ⟨k, hk.1⟩

/-- Si n llega a 1 y coalesce con n+1 en el sentido de Gao, n está en una racha:
    n+1 tiene la misma altura que n. -/
theorem racha_de_coalescencia {n j : ℕ} (hl : llega n) (hc : Hienas.coalescen n j) :
    enRacha n := by
  have hC : Hienas.C = C := rfl
  obtain ⟨he, -, hs⟩ := hc
  rw [hC] at he hs
  have hl' : ∃ h, C^[h] n = 1 := hl
  obtain ⟨h, hh, hmin⟩ : ∃ h, C^[h] n = 1 ∧ ∀ k, k < h → C^[k] n ≠ 1 :=
    ⟨Nat.find hl', Nat.find_spec hl', fun k hk => Nat.find_min hl' hk⟩
  have hjh : j < h := by
    by_contra hcon
    exact (hs h (by omega)).1 hh
  refine ⟨h, ⟨hh, hmin⟩, Or.inr ⟨?_, ?_⟩⟩
  · have e : C^[h] (n + 1) = C^[h - j] (C^[j] (n + 1)) := by
      rw [← Function.iterate_add_apply, Nat.sub_add_cancel hjh.le]
    rw [e, ← he, ← Function.iterate_add_apply, Nat.sub_add_cancel hjh.le, hh]
  · intro k hk
    by_cases hkj : k ≤ j
    · exact (hs k hkj).2
    · have hjk : j ≤ k := by omega
      have e : C^[k] (n + 1) = C^[k - j] (C^[j] (n + 1)) := by
        rw [← Function.iterate_add_apply, Nat.sub_add_cancel hjk]
      rw [e, ← he, ← Function.iterate_add_apply, Nat.sub_add_cancel hjk]
      exact hmin k hk

open Classical in
/-- Los que llegan a 1 sin estar en una racha no coalescen con su siguiente. -/
theorem cota_llegan (M : ℕ) :
    (((Finset.Ico 1 M).filter llega).card : ℝ) ≤
      (((Finset.Ico 1 M).filter enRacha).card : ℝ) +
        ((M : ℝ) - (((Finset.range M).filter (fun n => ∃ j, Hienas.coalescen n j)).card : ℝ)) := by
  have hGsub : (Finset.range M).filter (fun n => ∃ j, Hienas.coalescen n j) ⊆ Finset.range M :=
    Finset.filter_subset _ _
  have hsub : (Finset.Ico 1 M).filter llega ⊆ (Finset.Ico 1 M).filter enRacha ∪
      (Finset.range M \ (Finset.range M).filter (fun n => ∃ j, Hienas.coalescen n j)) := by
    intro n hn
    rw [Finset.mem_filter, Finset.mem_Ico] at hn
    rw [Finset.mem_union, Finset.mem_sdiff]
    by_cases hc : ∃ j, Hienas.coalescen n j
    · left
      obtain ⟨j, hj⟩ := hc
      exact Finset.mem_filter.2 ⟨Finset.mem_Ico.2 hn.1, racha_de_coalescencia hn.2 hj⟩
    · right
      exact ⟨Finset.mem_range.2 hn.1.2, fun hG => hc (Finset.mem_filter.1 hG).2⟩
  have hcard := Finset.card_le_card hsub
  have hu := Finset.card_union_le ((Finset.Ico 1 M).filter enRacha)
    (Finset.range M \ (Finset.range M).filter (fun n => ∃ j, Hienas.coalescen n j))
  have hsd := Finset.card_sdiff_of_subset hGsub
  rw [Finset.card_range] at hsd
  have hGM : ((Finset.range M).filter (fun n => ∃ j, Hienas.coalescen n j)).card ≤ M := by
    calc _ ≤ (Finset.range M).card := Finset.card_le_card hGsub
      _ = M := Finset.card_range M
  have hnat : ((Finset.Ico 1 M).filter llega).card ≤ ((Finset.Ico 1 M).filter enRacha).card +
      (M - ((Finset.range M).filter (fun n => ∃ j, Hienas.coalescen n j)).card) := by
    omega
  have hr : ((((Finset.Ico 1 M).filter enRacha).card +
      (M - ((Finset.range M).filter (fun n => ∃ j, Hienas.coalescen n j)).card) : ℕ) : ℝ) =
      (((Finset.Ico 1 M).filter enRacha).card : ℝ) +
        ((M : ℝ) - (((Finset.range M).filter (fun n => ∃ j, Hienas.coalescen n j)).card : ℝ)) := by
    rw [Nat.cast_add, Nat.cast_sub hGM]
  rw [← hr]
  exact_mod_cast hnat

/-- Cuenta real: si `A ≤ B ≤ A + (M − G)` y `G/M` está cerca de 1, `(B − A)/(M − 1)` es chico. -/
theorem cota_real {M A B G ε : ℝ} (hM : 2 ≤ M) (hε : 0 < ε) (hAB : A ≤ B)
    (hB : B ≤ A + (M - G)) (hG : |G / M - 1| < ε / 4) : |(B - A) / (M - 1)| < ε := by
  have hMpos : 0 < M := by linarith
  have hM1 : 0 < M - 1 := by linarith
  have hM0 : M ≠ 0 := hMpos.ne'
  have h1 : 1 - G / M < ε / 4 := by linarith [(abs_lt.1 hG).1]
  have h2 : M - G < ε / 4 * M := by
    have e : (1 - G / M) * M = M - G := by field_simp
    rw [← e]
    exact mul_lt_mul_of_pos_right h1 hMpos
  rw [abs_of_nonneg (div_nonneg (by linarith) hM1.le), div_lt_iff₀ hM1]
  nlinarith

open Classical in
/-- Con `d(x) → 1` de Gao, la densidad de Wu y la de los que llegan a 1 se acercan. -/
theorem diferencia (hD : Hienas.FormaGaoD) :
    Tendsto (fun M => rho M - dWu M) atTop (𝓝 0) := by
  unfold Hienas.FormaGaoD at hD
  rw [Metric.tendsto_atTop] at hD ⊢
  intro ε hε
  obtain ⟨N0, hN0⟩ := hD (ε / 4) (by linarith)
  refine ⟨max N0 2, fun M hM => ?_⟩
  have hM2 : (2 : ℝ) ≤ M := by exact_mod_cast le_trans (le_max_right _ _) hM
  have hdM := hN0 M (le_trans (le_max_left _ _) hM)
  rw [Real.dist_eq] at hdM
  rw [Real.dist_eq, sub_zero]
  have hAB : (((Finset.Ico 1 M).filter enRacha).card : ℝ) ≤
      ((Finset.Ico 1 M).filter llega).card := by
    exact_mod_cast Finset.card_le_card (fun n hn => by
      rw [Finset.mem_filter] at hn ⊢
      exact ⟨hn.1, llega_de_racha hn.2⟩)
  have e : rho M - dWu M = ((((Finset.Ico 1 M).filter llega).card : ℝ) -
      ((Finset.Ico 1 M).filter enRacha).card) / ((M : ℝ) - 1) := by
    unfold rho dWu
    rw [sub_div]
  have hd : Hienas.d M =
      (((Finset.range M).filter (fun n => ∃ j, Hienas.coalescen n j)).card : ℝ) / M := rfl
  rw [hd] at hdM
  rw [e]
  exact cota_real hM2 hε hAB (cota_llegan M) hdM

/-- Con `d(x) → 1`, `lim d(M) = 1` equivale a densidad 1 de los que llegan a 1. -/
theorem wu_uno_equivale (hD : Hienas.FormaGaoD) :
    Tendsto dWu atTop (𝓝 1) ↔ Tendsto rho atTop (𝓝 1) := by
  have hdif := diferencia hD
  constructor
  · intro h
    simpa using h.add hdif
  · intro h
    simpa using h.sub hdif

/-- Conjetura 1 de Wu, reducida: `lim d(M) = 1` si y sólo si los que llegan a 1 tienen
    densidad 1. Usa la conjetura de Gao ya demostrada (`GaoLiteral`). -/
theorem wu_uno : Tendsto dWu atTop (𝓝 1) ↔ Tendsto rho atTop (𝓝 1) :=
  wu_uno_equivale GaoLiteral.conjetura_gao_literal.2

end CondorasWu

#print axioms CondorasWu.wu_dos
#print axioms CondorasWu.wu_uno
