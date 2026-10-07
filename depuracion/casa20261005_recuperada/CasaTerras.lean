import CasaCasiTodos

/-! # El teorema de Terras: la distribución del tiempo de parada

Ruta B, 05-10-2026. Terras (1976) demostró que el tiempo de parada σ(n), primer `j ≥ 1`
con `T^j(n) < n`, tiene distribución límite: para cada `K`, la proporción de `n < N` con
`σ(n) > K` tiende a un número `P(K)`, y `P(K) → 0`. Aquí, sin hipótesis externas:

* `terras_distribucion`: la proporción de `n < N` que no bajan de sí mismos en los `K`
  primeros pasos tiende a `d_K / 2^K`, donde `d_K` cuenta los residuos módulo `2^K` cuyo
  pronóstico no baja de 1 en ninguno de esos pasos (`supervivientes K`);
* `terras_limite`: `d_K / 2^K → 0`;
* `terras_error`: el error es a lo sumo `(d_K + 3^K) / N`, explícito.

Así `F(K) = 1 − d_K/2^K` es la función de distribución límite de σ, y `F(K) → 1`.

Compilación: `comprobar_fugitivo.py`, en esta carpeta. -/

namespace CasaTerras

open Ocelotas OcelotasContador CasaPlano CasaFugitivo CasaCasiTodos

/-- El pronóstico de `n` no baja de 1 en ninguno de los `K` primeros pasos. -/
def Sobrevive (K n : ℕ) : Prop := ∀ j ∈ Finset.range (K + 1), 2 ^ j ≤ 3 ^ S j n

/-- `n` no baja de sí mismo en los `K` primeros pasos: σ(n) > K. -/
def NoBajaHasta (K n : ℕ) : Prop := ∀ j ∈ Finset.range (K + 1), n ≤ T^[j] n

instance (K n : ℕ) : Decidable (Sobrevive K n) := by unfold Sobrevive; infer_instance
instance (K n : ℕ) : Decidable (NoBajaHasta K n) := by unfold NoBajaHasta; infer_instance

/-- Residuos módulo `2^K` que sobreviven `K` pasos; `d_K` es su número. -/
def supervivientes (K : ℕ) : Finset ℕ := (Finset.range (2 ^ K)).filter (Sobrevive K)

theorem sobrevive_mod (K n : ℕ) : Sobrevive K n ↔ Sobrevive K (n % 2 ^ K) := by
  have h : ∀ j ∈ Finset.range (K + 1), S j n = S j (n % 2 ^ K) := by
    intro j hj
    have hj' : j ≤ K := Nat.lt_succ_iff.1 (Finset.mem_range.1 hj)
    exact S_congr j _ _ (Nat.ModEq.of_dvd (pow_dvd_pow 2 hj') (Nat.mod_modEq n _).symm)
  constructor
  · intro hs j hj
    rw [← h j hj]
    exact hs j hj
  · intro hs j hj
    rw [h j hj]
    exact hs j hj

/-- Para `n ≥ 3^K`, no bajar en `K` pasos equivale a sobrevivir `K` pasos. -/
theorem noBaja_iff_sobrevive {K n : ℕ} (hn : 3 ^ K ≤ n) : NoBajaHasta K n ↔ Sobrevive K n := by
  constructor
  · intro h j hj
    by_contra hc
    have hj' : j ≤ K := Nat.lt_succ_iff.1 (Finset.mem_range.1 hj)
    have h3 : 3 ^ j ≤ n := le_trans (Nat.pow_le_pow_right (by norm_num) hj') hn
    have := desciende_de_cruce_grande (not_le.mp hc) h3
    have := h j hj
    omega
  · intro h j hj
    exact no_baja (h j hj)

/-- Números menores que `N` que no bajan de sí mismos en `K` pasos. -/
def noBajan (K N : ℕ) : Finset ℕ := (Finset.range N).filter (NoBajaHasta K)

/-- Números menores que `N` que sobreviven `K` pasos. -/
def sobreviven (K N : ℕ) : Finset ℕ := (Finset.range N).filter (Sobrevive K)

theorem sobreviven_le (K N : ℕ) :
    (sobreviven K N).card ≤ (N / 2 ^ K + 1) * (supervivientes K).card := by
  rw [← Finset.card_range (N / 2 ^ K + 1), ← Finset.card_product]
  apply Finset.card_le_card_of_injOn (fun n => (n / 2 ^ K, n % 2 ^ K))
  · intro n hn
    have hn' : n < N ∧ Sobrevive K n := by simpa [sobreviven] using hn
    simp only [Finset.coe_product, Set.mem_prod, Finset.mem_coe, Finset.mem_range,
      supervivientes, Finset.mem_filter]
    exact ⟨Nat.lt_succ_of_le (Nat.div_le_div_right hn'.1.le), Nat.mod_lt _ (by positivity),
      (sobrevive_mod K n).1 hn'.2⟩
  · intro a _ b _ hab
    simp only [Prod.mk.injEq] at hab
    rw [← Nat.div_add_mod a (2 ^ K), ← Nat.div_add_mod b (2 ^ K), hab.1, hab.2]

theorem sobreviven_ge (K N : ℕ) :
    (N / 2 ^ K) * (supervivientes K).card ≤ (sobreviven K N).card := by
  have hM : 0 < 2 ^ K := by positivity
  rw [← Finset.card_range (N / 2 ^ K), ← Finset.card_product]
  apply Finset.card_le_card_of_injOn (fun p => p.2 + p.1 * 2 ^ K)
  · intro p hp
    simp only [Finset.coe_product, Set.mem_prod, Finset.mem_coe, Finset.mem_range,
      supervivientes, Finset.mem_filter] at hp
    obtain ⟨hq, hr, hs⟩ := hp
    have hmod : (p.2 + p.1 * 2 ^ K) % 2 ^ K = p.2 := by
      rw [Nat.add_mul_mod_self_right, Nat.mod_eq_of_lt hr]
    have hq1 : (p.1 + 1) * 2 ^ K ≤ N :=
      le_trans (Nat.mul_le_mul_right _ hq) (Nat.div_mul_le_self N _)
    simp only [Finset.coe_filter, Finset.mem_range, Set.mem_setOf_eq, sobreviven]
    refine ⟨by nlinarith, (sobrevive_mod K _).2 (by rw [hmod]; exact hs)⟩
  · intro a ha b hb hab
    simp only [Finset.coe_product, Set.mem_prod, Finset.mem_coe, Finset.mem_range,
      supervivientes, Finset.mem_filter] at ha hb
    have h2 : a.2 = b.2 := by
      have := congrArg (· % 2 ^ K) hab
      simpa [Nat.add_mul_mod_self_right, Nat.mod_eq_of_lt ha.2.1, Nat.mod_eq_of_lt hb.2.1]
        using this
    have h1 : a.1 = b.1 := by
      have := congrArg (· / 2 ^ K) hab
      simpa [Nat.add_mul_div_right _ _ hM, Nat.div_eq_of_lt ha.2.1, Nat.div_eq_of_lt hb.2.1]
        using this
    exact Prod.ext h1 h2

theorem noBajan_le (K N : ℕ) : (noBajan K N).card ≤ (sobreviven K N).card + 3 ^ K := by
  have hsub : noBajan K N ⊆ sobreviven K N ∪ Finset.range (3 ^ K) := by
    intro n hn
    have hn' : n < N ∧ NoBajaHasta K n := by simpa [noBajan] using hn
    rw [Finset.mem_union, Finset.mem_range]
    by_cases hk : n < 3 ^ K
    · exact Or.inr hk
    · exact Or.inl (by
        simpa [sobreviven] using ⟨hn'.1, (noBaja_iff_sobrevive (not_lt.mp hk)).1 hn'.2⟩)
  calc (noBajan K N).card ≤ (sobreviven K N ∪ Finset.range (3 ^ K)).card :=
        Finset.card_le_card hsub
    _ ≤ (sobreviven K N).card + (Finset.range (3 ^ K)).card := Finset.card_union_le _ _
    _ = _ := by rw [Finset.card_range]

theorem sobreviven_le_noBajan (K N : ℕ) :
    (sobreviven K N).card ≤ (noBajan K N).card + 3 ^ K := by
  have hsub : sobreviven K N ⊆ noBajan K N ∪ Finset.range (3 ^ K) := by
    intro n hn
    have hn' : n < N ∧ Sobrevive K n := by simpa [sobreviven] using hn
    rw [Finset.mem_union, Finset.mem_range]
    by_cases hk : n < 3 ^ K
    · exact Or.inr hk
    · exact Or.inl (by
        simpa [noBajan] using ⟨hn'.1, (noBaja_iff_sobrevive (not_lt.mp hk)).2 hn'.2⟩)
  calc (sobreviven K N).card ≤ (noBajan K N ∪ Finset.range (3 ^ K)).card :=
        Finset.card_le_card hsub
    _ ≤ (noBajan K N).card + (Finset.range (3 ^ K)).card := Finset.card_union_le _ _
    _ = _ := by rw [Finset.card_range]

/-- Error explícito: `|#{n < N : σ(n) > K} − N d_K / 2^K| ≤ d_K + 3^K`. -/
theorem terras_error (K N : ℕ) :
    |((noBajan K N).card : ℝ) - N * ((supervivientes K).card / 2 ^ K)| ≤
      (supervivientes K).card + 3 ^ K := by
  have hM : (0 : ℝ) < 2 ^ K := by positivity
  have hd : (0 : ℝ) ≤ (supervivientes K).card := by positivity
  have hq1 : ((N / 2 ^ K : ℕ) : ℝ) ≤ N / 2 ^ K := by
    rw [le_div_iff₀ hM]
    exact_mod_cast Nat.div_mul_le_self N (2 ^ K)
  have hq2 : (N : ℝ) / 2 ^ K - 1 ≤ ((N / 2 ^ K : ℕ) : ℝ) := by
    have h1 := Nat.div_add_mod N (2 ^ K)
    have h2 := Nat.mod_lt N (show 0 < 2 ^ K by positivity)
    have h3 : N < 2 ^ K * (N / 2 ^ K) + 2 ^ K := by omega
    have h4 : (N : ℝ) < 2 ^ K * ((N / 2 ^ K : ℕ) : ℝ) + 2 ^ K := by exact_mod_cast h3
    rw [sub_le_iff_le_add, div_le_iff₀ hM]
    linarith
  have hup : ((noBajan K N).card : ℝ) ≤
      (((N / 2 ^ K : ℕ) : ℝ) + 1) * (supervivientes K).card + 3 ^ K := by
    exact_mod_cast le_trans (noBajan_le K N) (Nat.add_le_add_right (sobreviven_le K N) _)
  have hlo : ((N / 2 ^ K : ℕ) : ℝ) * (supervivientes K).card ≤
      ((noBajan K N).card : ℝ) + 3 ^ K := by
    exact_mod_cast le_trans (sobreviven_ge K N) (sobreviven_le_noBajan K N)
  have e : (N : ℝ) * ((supervivientes K).card / 2 ^ K) =
      (N / 2 ^ K) * (supervivientes K).card := by ring
  have m1 := mul_le_mul_of_nonneg_right hq1 hd
  have m2 := mul_le_mul_of_nonneg_right hq2 hd
  rw [e, abs_le]
  constructor <;> nlinarith

/-- **Terras (1976).** La proporción de `n < N` con tiempo de parada `σ(n) > K` tiende a
    `d_K / 2^K`. -/
theorem terras_distribucion (K : ℕ) :
    Filter.Tendsto (fun N : ℕ => ((noBajan K N).card : ℝ) / N) Filter.atTop
      (nhds ((supervivientes K).card / 2 ^ K)) := by
  rw [Metric.tendsto_atTop]
  intro ε hε
  obtain ⟨N0, hN0⟩ := exists_nat_gt (((supervivientes K).card + 3 ^ K) / ε)
  refine ⟨N0, fun N hN => ?_⟩
  have hC : (0 : ℝ) ≤ (supervivientes K).card + 3 ^ K := by positivity
  have hN0pos : (0 : ℝ) < N0 := lt_of_le_of_lt (div_nonneg hC hε.le) hN0
  have hNpos : (0 : ℝ) < N := lt_of_lt_of_le hN0pos (by exact_mod_cast hN)
  have hNε : ((supervivientes K).card + 3 ^ K : ℝ) < N * ε := by
    have := lt_of_lt_of_le hN0 (show (N0 : ℝ) ≤ N by exact_mod_cast hN)
    rwa [div_lt_iff₀ hε] at this
  have hrw : ((noBajan K N).card : ℝ) / N - (supervivientes K).card / 2 ^ K =
      (((noBajan K N).card : ℝ) - N * ((supervivientes K).card / 2 ^ K)) / N := by
    field_simp
  rw [Real.dist_eq, hrw, abs_div, abs_of_pos hNpos, div_lt_iff₀ hNpos]
  linarith [terras_error K N]

/-- Los supervivientes son a lo sumo los residuos sin cruce en el paso `K`. -/
theorem supervivientes_sub (K : ℕ) : supervivientes K ⊆ sinCruce K := by
  intro r hr
  simp only [supervivientes, sinCruce, Finset.mem_filter] at hr ⊢
  exact ⟨hr.1, hr.2 K (Finset.mem_range.2 (Nat.lt_succ_self K))⟩

/-- **Terras (1976).** `d_K / 2^K → 0`: casi todo número tiene tiempo de parada finito. -/
theorem terras_limite :
    Filter.Tendsto (fun K : ℕ => ((supervivientes K).card : ℝ) / 2 ^ K) Filter.atTop
      (nhds 0) := by
  have hρ0 : 0 ≤ (1 + Real.sqrt 3) / Real.sqrt 2 / 2 := by positivity
  rw [Metric.tendsto_atTop]
  intro ε hε
  obtain ⟨K0, hK0⟩ := exists_pow_lt_of_lt_one hε razon_menor
  refine ⟨K0, fun K hK => ?_⟩
  have hcota : ((supervivientes K).card : ℝ) / 2 ^ K ≤ ((sinCruce K).card : ℝ) / 2 ^ K := by
    gcongr
    exact supervivientes_sub K
  have hmono : ((1 + Real.sqrt 3) / Real.sqrt 2 / 2) ^ K ≤
      ((1 + Real.sqrt 3) / Real.sqrt 2 / 2) ^ K0 :=
    pow_le_pow_of_le_one hρ0 razon_menor.le hK
  rw [Real.dist_eq, sub_zero, abs_of_nonneg (by positivity)]
  linarith [proporcion_sin_cruce K]

end CasaTerras

#print axioms CasaTerras.noBaja_iff_sobrevive
#print axioms CasaTerras.sobreviven_le
#print axioms CasaTerras.sobreviven_ge
#print axioms CasaTerras.terras_error
#print axioms CasaTerras.terras_distribucion
#print axioms CasaTerras.terras_limite
