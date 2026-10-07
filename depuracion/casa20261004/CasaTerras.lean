import CasaKorec

/-! # La densidad exacta de Terras

07-10-2026. Explicación en `LEEME.md` de esta carpeta, sección «Una ventana: Korec».

El teorema A de Terras (1976), tal como lo enuncia Lagarias (1985): el conjunto de los números
que bajan de sí mismos en a lo sumo `k` pasos tiene densidad exacta `F(k)`, y `F(k) → 1`.

* `paso_congruente`, `congruentes_mismo_baile`: si `n ≡ n'` módulo `2^k`, sus primeros `k` pasos
  tienen las mismas paridades (el recíproco de `misma_paridad_congruentes`);
* `subidas_iguales`, `cruza_resto`: cruzar en a lo sumo `k` pasos depende sólo del resto módulo
  `2^k`;
* `baja_iff_cruza`: para `n` grande (`k·2^k ≤ 3n`), bajar en a lo sumo `k` pasos es cruzar en a
  lo sumo `k` pasos;
* `cuenta_resto`, `cuenta_periodica`: cuántos números de `[0, N)` tienen el resto en un conjunto
  dado;
* `densidad_terras`: **la densidad de los que bajan en a lo sumo `k` pasos existe y vale
  `F(k) = |A_k|/2^k`**, con `A_k` los restos módulo `2^k` cuyo pronóstico cruza en a lo sumo `k`
  pasos;
* `restos_sin_cruce`, `terras_tiende_a_uno`: **`F(k) → 1`**; con `100m ≤ k`,
  `1 − F(k) ≤ 2/16^m`, una caída exponencial como la del teorema D;
* `teorema_B`: cada patrón de largo `k` corresponde a exactamente un resto módulo `2^k`;
* `primer_cruce_resto`, `teorema_C`: el primer cruce depende sólo del resto módulo `2^k`, y para
  `n` grande el tiempo de parada es exactamente el primer cruce.

Con esto, los teoremas A, B y C de la sección 2 de la reseña de Lagarias (1985) están en Lean, y el
D con un exponente algo peor.

Es una ventana: dice «casi todos». Sin hipótesis externas. Compilación: `comprobar_casa.py`, en
esta carpeta. -/

namespace CasaTerras

open Ocelotas OcelotasContador CasaPlano CasaRetrato CasaTablero CasaPlaneador CasaGrieta
  CasaVentana CasaKorec

/-- Congruentes módulo `2^(k+1)` tienen la misma paridad, y sus imágenes son congruentes
    módulo `2^k`. -/
theorem paso_congruente {k n n' : ℕ} (h : n % 2 ^ (k + 1) = n' % 2 ^ (k + 1)) :
    n % 2 = n' % 2 ∧ T n % 2 ^ k = T n' % 2 ^ k := by
  have hm : n ≡ n' [MOD 2 ^ (k + 1)] := h
  have h2 : n ≡ n' [MOD 2] := Nat.ModEq.of_dvd (dvd_pow_self 2 (by omega)) hm
  refine ⟨h2, ?_⟩
  have e : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [pow_succ, Nat.mul_comm]
  rw [e] at hm
  have h2' : n % 2 = n' % 2 := h2
  have key : 2 * T n ≡ 2 * T n' [MOD 2 * 2 ^ k] := by
    rcases Nat.mod_two_eq_zero_or_one n with hp | hp
    · have hp' : n' % 2 = 0 := by omega
      rw [T_par hp, T_par hp']
      exact hm
    · have hp' : n' % 2 = 1 := by omega
      rw [T_impar hp, T_impar hp']
      exact Nat.ModEq.add_right 1 (Nat.ModEq.mul_left 3 hm)
  exact Nat.ModEq.mul_left_cancel' (by norm_num) key

/-- **Congruentes, mismo baile**: si `n ≡ n'` módulo `2^k`, sus primeros `k` pasos tienen las
    mismas paridades. -/
theorem congruentes_mismo_baile : ∀ k n n', n % 2 ^ k = n' % 2 ^ k →
    ∀ i, i < k → T^[i] n % 2 = T^[i] n' % 2 := by
  intro k
  induction k with
  | zero => intro n n' _ i hi; omega
  | succ k ih =>
    intro n n' h i hi
    obtain ⟨hpar, hT⟩ := paso_congruente h
    rcases i with _ | i
    · simpa using hpar
    · rw [Function.iterate_succ_apply, Function.iterate_succ_apply]
      exact ih (T n) (T n') hT i (by omega)

/-- Mismas paridades, mismas subidas. -/
theorem subidas_iguales {j n n' : ℕ} (h : ∀ i, i < j → T^[i] n % 2 = T^[i] n' % 2) :
    S j n = S j n' := by
  rw [← card_subidas, ← card_subidas]
  congr 1
  ext i
  simp only [subidas, Finset.mem_filter, Finset.mem_range]
  constructor
  · rintro ⟨hi, h1⟩
    exact ⟨hi, (h i hi) ▸ h1⟩
  · rintro ⟨hi, h1⟩
    exact ⟨hi, (h i hi).symm ▸ h1⟩

/-- **Para `n` grande, bajar en a lo sumo `k` pasos es cruzar en a lo sumo `k` pasos.** -/
theorem baja_iff_cruza {n k : ℕ} (hn : k * 2 ^ k ≤ 3 * n) :
    (∃ j, 1 ≤ j ∧ j ≤ k ∧ T^[j] n < n) ↔ ∃ j, j ≤ k ∧ 3 ^ S j n < 2 ^ j := by
  constructor
  · rintro ⟨j, hj1, hjk, hlt⟩
    by_contra hc
    push Not at hc
    have := no_baja (hc j hjk)
    omega
  · rintro ⟨j, hjk, hj⟩
    obtain ⟨j0, hj0j, hk0⟩ := primer_cruce_antes hj
    refine ⟨j0, primerCruce_pos hk0, le_trans hj0j hjk, desciende_si_grande hk0 ?_⟩
    calc j0 * 2 ^ j0 ≤ k * 2 ^ k :=
          Nat.mul_le_mul (le_trans hj0j hjk) (Nat.pow_le_pow_right (by norm_num) (le_trans hj0j hjk))
      _ ≤ 3 * n := hn

/-- Cruzar en a lo sumo `k` pasos depende sólo del resto módulo `2^k`. -/
theorem cruza_resto (n k : ℕ) :
    (∃ j, j ≤ k ∧ 3 ^ S j n < 2 ^ j) ↔ ∃ j, j ≤ k ∧ 3 ^ S j (n % 2 ^ k) < 2 ^ j := by
  have hb := congruentes_mismo_baile k n (n % 2 ^ k) (Nat.mod_mod n (2 ^ k)).symm
  have hS : ∀ j, j ≤ k → S j n = S j (n % 2 ^ k) := fun j hj =>
    subidas_iguales fun i hi => hb i (by omega)
  constructor
  · rintro ⟨j, hj, h⟩
    exact ⟨j, hj, hS j hj ▸ h⟩
  · rintro ⟨j, hj, h⟩
    exact ⟨j, hj, (hS j hj).symm ▸ h⟩

/-- En `[0, N)`, cada resto `r < P` aparece entre `N/P` y `N/P + 1` veces. -/
theorem cuenta_resto (N P r : ℕ) (hr : r < P) :
    N / P ≤ ((Finset.range N).filter fun n => n % P = r).card ∧
      ((Finset.range N).filter fun n => n % P = r).card ≤ N / P + 1 := by
  have hP : 0 < P := by omega
  constructor
  · rw [← Finset.card_range (N / P)]
    refine Finset.card_le_card_of_injOn (fun q => q * P + r) ?_ ?_
    · intro q hq
      simp only [Finset.mem_coe, Finset.mem_range] at hq
      simp only [Finset.mem_coe, Finset.mem_filter, Finset.mem_range]
      constructor
      · have h1 : (q + 1) * P ≤ N / P * P := Nat.mul_le_mul_right _ hq
        have h2 : N / P * P ≤ N := Nat.div_mul_le_self N P
        nlinarith
      · rw [Nat.add_comm, Nat.add_mul_mod_self_right, Nat.mod_eq_of_lt hr]
    · intro a _ b _ hab
      simp only at hab
      exact Nat.eq_of_mul_eq_mul_right hP (by omega)
  · rw [← Finset.card_range (N / P + 1)]
    refine Finset.card_le_card_of_injOn (fun n => n / P) ?_ ?_
    · intro n hn
      simp only [Finset.mem_coe, Finset.mem_filter, Finset.mem_range] at hn
      simp only [Finset.mem_coe, Finset.mem_range]
      have := Nat.div_le_div_right (c := P) hn.1.le
      omega
    · intro a ha b hb hab
      simp only [Finset.mem_coe, Finset.mem_filter, Finset.mem_range] at ha hb
      simp only at hab
      rw [← Nat.div_add_mod a P, ← Nat.div_add_mod b P, hab, ha.2, hb.2]

/-- Para un conjunto `A` de restos módulo `P`, en `[0, N)` hay entre `|A|·(N/P)` y
    `|A|·(N/P + 1)` números con resto en `A`. -/
theorem cuenta_periodica (N P : ℕ) (A : Finset ℕ) (hA : A ⊆ Finset.range P) :
    A.card * (N / P) ≤ ((Finset.range N).filter fun n => n % P ∈ A).card ∧
      ((Finset.range N).filter fun n => n % P ∈ A).card ≤ A.card * (N / P + 1) := by
  have hfib : ((Finset.range N).filter fun n => n % P ∈ A).card =
      ∑ r ∈ A, ((Finset.range N).filter fun n => n % P = r).card := by
    rw [Finset.card_eq_sum_card_fiberwise (f := fun n => n % P) (t := A)]
    · apply Finset.sum_congr rfl
      intro r hr
      congr 1
      ext n
      simp only [Finset.mem_filter, Finset.mem_range]
      constructor
      · rintro ⟨⟨h1, _⟩, h2⟩
        exact ⟨h1, h2⟩
      · rintro ⟨h1, h2⟩
        exact ⟨⟨h1, h2 ▸ hr⟩, h2⟩
    · intro n hn
      exact (Finset.mem_filter.1 hn).2
  rw [hfib]
  constructor
  · calc A.card * (N / P) = ∑ r ∈ A, N / P := by rw [Finset.sum_const, smul_eq_mul]
      _ ≤ ∑ r ∈ A, ((Finset.range N).filter fun n => n % P = r).card :=
          Finset.sum_le_sum fun r hr => (cuenta_resto N P r (Finset.mem_range.1 (hA hr))).1
  · calc ∑ r ∈ A, ((Finset.range N).filter fun n => n % P = r).card ≤ ∑ r ∈ A, (N / P + 1) :=
          Finset.sum_le_sum fun r hr => (cuenta_resto N P r (Finset.mem_range.1 (hA hr))).2
      _ = A.card * (N / P + 1) := by rw [Finset.sum_const, smul_eq_mul]

open Classical in
/-- **Teorema A de Terras (1976), la densidad exacta**: para cada `k`, los números que bajan de
    sí mismos en a lo sumo `k` pasos tienen densidad `F(k) = |A_k|/2^k`, donde `A_k` son los
    restos módulo `2^k` cuyo pronóstico cruza en a lo sumo `k` pasos. -/
theorem densidad_terras (k : ℕ) :
    Filter.Tendsto (fun N : ℕ => (((Finset.range N).filter fun n =>
        ∃ j, 1 ≤ j ∧ j ≤ k ∧ T^[j] n < n).card : ℝ) / N) Filter.atTop
      (nhds ((((Finset.range (2 ^ k)).filter fun r =>
        ∃ j, j ≤ k ∧ 3 ^ S j r < 2 ^ j).card : ℝ) / 2 ^ k)) := by
  set A := (Finset.range (2 ^ k)).filter fun r => ∃ j, j ≤ k ∧ 3 ^ S j r < 2 ^ j with hA
  set C : ℕ := k * 2 ^ k with hC
  have hPpos : 0 < 2 ^ k := by positivity
  have hAsub : A ⊆ Finset.range (2 ^ k) := Finset.filter_subset _ _
  have hmem : ∀ n, C ≤ 3 * n → ((∃ j, 1 ≤ j ∧ j ≤ k ∧ T^[j] n < n) ↔ n % 2 ^ k ∈ A) := by
    intro n hn
    rw [baja_iff_cruza hn, cruza_resto, hA, Finset.mem_filter, Finset.mem_range]
    exact ⟨fun h => ⟨Nat.mod_lt _ hPpos, h⟩, fun h => h.2⟩
  -- las dos cuentas difieren a lo sumo en C
  have hDle : ∀ N, ((Finset.range N).filter fun n => ∃ j, 1 ≤ j ∧ j ≤ k ∧ T^[j] n < n).card ≤
      ((Finset.range N).filter fun n => n % 2 ^ k ∈ A).card + C := by
    intro N
    have hsub : ((Finset.range N).filter fun n => ∃ j, 1 ≤ j ∧ j ≤ k ∧ T^[j] n < n) ⊆
        ((Finset.range N).filter fun n => n % 2 ^ k ∈ A) ∪ Finset.range C := by
      intro n hn
      simp only [Finset.mem_filter, Finset.mem_range] at hn
      simp only [Finset.mem_union, Finset.mem_filter, Finset.mem_range]
      by_cases h : C ≤ 3 * n
      · exact Or.inl ⟨hn.1, (hmem n h).1 hn.2⟩
      · right
        omega
    calc ((Finset.range N).filter fun n => ∃ j, 1 ≤ j ∧ j ≤ k ∧ T^[j] n < n).card
        ≤ (((Finset.range N).filter fun n => n % 2 ^ k ∈ A) ∪ Finset.range C).card :=
          Finset.card_le_card hsub
      _ ≤ ((Finset.range N).filter fun n => n % 2 ^ k ∈ A).card + (Finset.range C).card :=
          Finset.card_union_le _ _
      _ = ((Finset.range N).filter fun n => n % 2 ^ k ∈ A).card + C := by rw [Finset.card_range]
  have hPle : ∀ N, ((Finset.range N).filter fun n => n % 2 ^ k ∈ A).card ≤
      ((Finset.range N).filter fun n => ∃ j, 1 ≤ j ∧ j ≤ k ∧ T^[j] n < n).card + C := by
    intro N
    have hsub : ((Finset.range N).filter fun n => n % 2 ^ k ∈ A) ⊆
        ((Finset.range N).filter fun n => ∃ j, 1 ≤ j ∧ j ≤ k ∧ T^[j] n < n) ∪ Finset.range C := by
      intro n hn
      simp only [Finset.mem_filter, Finset.mem_range] at hn
      simp only [Finset.mem_union, Finset.mem_filter, Finset.mem_range]
      by_cases h : C ≤ 3 * n
      · exact Or.inl ⟨hn.1, (hmem n h).2 hn.2⟩
      · right
        omega
    calc ((Finset.range N).filter fun n => n % 2 ^ k ∈ A).card
        ≤ (((Finset.range N).filter fun n => ∃ j, 1 ≤ j ∧ j ≤ k ∧ T^[j] n < n) ∪
            Finset.range C).card := Finset.card_le_card hsub
      _ ≤ ((Finset.range N).filter fun n => ∃ j, 1 ≤ j ∧ j ≤ k ∧ T^[j] n < n).card +
            (Finset.range C).card := Finset.card_union_le _ _
      _ = ((Finset.range N).filter fun n => ∃ j, 1 ≤ j ∧ j ≤ k ∧ T^[j] n < n).card + C := by
          rw [Finset.card_range]
  -- en reales
  have hPR : (0 : ℝ) < 2 ^ k := by positivity
  have hcastP : ((2 ^ k : ℕ) : ℝ) = (2 : ℝ) ^ k := by push_cast; ring
  have hfl : ∀ N : ℕ, ((N / 2 ^ k : ℕ) : ℝ) ≤ (N : ℝ) / 2 ^ k := by
    intro N
    rw [← hcastP]
    exact Nat.cast_div_le
  have hfl2 : ∀ N : ℕ, (N : ℝ) / 2 ^ k - 1 ≤ ((N / 2 ^ k : ℕ) : ℝ) := by
    intro N
    have h1 : N < (N / 2 ^ k + 1) * 2 ^ k := by
      have e1 := Nat.div_add_mod N (2 ^ k)
      have e2 := Nat.mod_lt N hPpos
      nlinarith
    have h2 : (N : ℝ) < (((N / 2 ^ k : ℕ) : ℝ) + 1) * 2 ^ k := by
      have : ((N : ℕ) : ℝ) < (((N / 2 ^ k + 1) * 2 ^ k : ℕ) : ℝ) := by exact_mod_cast h1
      push_cast at this
      linarith
    rw [sub_le_iff_le_add, div_le_iff₀ hPR]
    linarith
  set L : ℝ := (A.card : ℝ) / 2 ^ k with hL
  set c : ℝ := (A.card : ℝ) + C with hc
  have hup : ∀ N : ℕ, 1 ≤ N →
      (((Finset.range N).filter fun n => ∃ j, 1 ≤ j ∧ j ≤ k ∧ T^[j] n < n).card : ℝ) / N ≤
        L + c / N := by
    intro N hN
    have hNR : (0 : ℝ) < N := by exact_mod_cast hN
    have e1 : (((Finset.range N).filter fun n => ∃ j, 1 ≤ j ∧ j ≤ k ∧ T^[j] n < n).card : ℝ) ≤
        (((Finset.range N).filter fun n => n % 2 ^ k ∈ A).card : ℝ) + C := by
      exact_mod_cast hDle N
    have e2 : (((Finset.range N).filter fun n => n % 2 ^ k ∈ A).card : ℝ) ≤
        (A.card : ℝ) * (((N / 2 ^ k : ℕ) : ℝ) + 1) := by
      exact_mod_cast (cuenta_periodica N (2 ^ k) A hAsub).2
    have e3 : (A.card : ℝ) * (((N / 2 ^ k : ℕ) : ℝ) + 1) ≤ (A.card : ℝ) * ((N : ℝ) / 2 ^ k + 1) :=
      mul_le_mul_of_nonneg_left (by linarith [hfl N]) (Nat.cast_nonneg _)
    rw [div_le_iff₀ hNR]
    have e4 : (L + c / N) * N = (A.card : ℝ) * ((N : ℝ) / 2 ^ k + 1) + C := by
      rw [hL, hc]
      field_simp
      ring
    rw [e4]
    linarith
  have hlow : ∀ N : ℕ, 1 ≤ N →
      L - c / N ≤
        (((Finset.range N).filter fun n => ∃ j, 1 ≤ j ∧ j ≤ k ∧ T^[j] n < n).card : ℝ) / N := by
    intro N hN
    have hNR : (0 : ℝ) < N := by exact_mod_cast hN
    have e1 : (((Finset.range N).filter fun n => n % 2 ^ k ∈ A).card : ℝ) ≤
        (((Finset.range N).filter fun n => ∃ j, 1 ≤ j ∧ j ≤ k ∧ T^[j] n < n).card : ℝ) + C := by
      exact_mod_cast hPle N
    have e2 : (A.card : ℝ) * ((N / 2 ^ k : ℕ) : ℝ) ≤
        (((Finset.range N).filter fun n => n % 2 ^ k ∈ A).card : ℝ) := by
      exact_mod_cast (cuenta_periodica N (2 ^ k) A hAsub).1
    have e3 : (A.card : ℝ) * ((N : ℝ) / 2 ^ k - 1) ≤ (A.card : ℝ) * ((N / 2 ^ k : ℕ) : ℝ) :=
      mul_le_mul_of_nonneg_left (hfl2 N) (Nat.cast_nonneg _)
    rw [le_div_iff₀ hNR]
    have e4 : (L - c / N) * N = (A.card : ℝ) * ((N : ℝ) / 2 ^ k - 1) - C := by
      rw [hL, hc]
      field_simp
      ring
    rw [e4]
    linarith
  have hg1 : Filter.Tendsto (fun N : ℕ => L - c / N) Filter.atTop (nhds L) := by
    have := (tendsto_const_nhds (x := L)).sub (tendsto_const_div_atTop_nhds_zero_nat c)
    rwa [sub_zero] at this
  have hg2 : Filter.Tendsto (fun N : ℕ => L + c / N) Filter.atTop (nhds L) := by
    have := (tendsto_const_nhds (x := L)).add (tendsto_const_div_atTop_nhds_zero_nat c)
    rwa [add_zero] at this
  refine tendsto_of_tendsto_of_tendsto_of_le_of_le' hg1 hg2 ?_ ?_
  · filter_upwards [Filter.eventually_ge_atTop 1] with N hN
    exact hlow N hN
  · filter_upwards [Filter.eventually_ge_atTop 1] with N hN
    exact hup N hN

open Classical in
/-- Con `100m ≤ k`, los restos módulo `2^k` cuyo pronóstico no cruza en `k` pasos son a lo sumo
    `2·2^k/16^m`. -/
theorem restos_sin_cruce (m k : ℕ) (hmk : 100 * m ≤ k) :
    2 ^ k ≤ ((Finset.range (2 ^ k)).filter fun r => ∃ j, j ≤ k ∧ 3 ^ S j r < 2 ^ j).card +
      2 * (2 ^ k / 16 ^ m) := by
  have h1 := Finset.card_filter_add_card_filter_not (s := Finset.range (2 ^ k))
    (fun r => ∃ j, j ≤ k ∧ 3 ^ S j r < 2 ^ j)
  have hsub : (Finset.range (2 ^ k)).filter (fun r => ¬ ∃ j, j ≤ k ∧ 3 ^ S j r < 2 ^ j) ⊆
      (Finset.range (2 ^ k)).filter (fun r => 2 ^ (100 * m) ≤ 3 ^ S (100 * m) r) := by
    intro r hr
    rw [Finset.mem_filter] at hr ⊢
    refine ⟨hr.1, ?_⟩
    by_contra hc
    push Not at hc
    exact hr.2 ⟨100 * m, hmk, hc⟩
  have h2 := (Finset.card_le_card hsub).trans (cuenta_sin_cruce (2 ^ k) m)
  rw [Finset.card_range] at h1
  have e : 2 ^ (100 * m) = 16 ^ m * 2 ^ (96 * m) := by
    rw [show 100 * m = 4 * m + 96 * m by ring, pow_add, pow_mul]
    norm_num
  have h3 : 2 ^ k / 2 ^ (100 * m) * 2 ^ (96 * m) ≤ 2 ^ k / 16 ^ m := by
    rw [e, ← Nat.div_div_eq_div_mul]
    exact Nat.div_mul_le_self _ _
  have h4 : 2 ^ (96 * m) ≤ 2 ^ k / 16 ^ m := by
    rw [Nat.le_div_iff_mul_le (by positivity), Nat.mul_comm, ← e]
    exact Nat.pow_le_pow_right (by norm_num) hmk
  have h5 : (2 ^ k / 2 ^ (100 * m) + 1) * 2 ^ (96 * m) =
      2 ^ k / 2 ^ (100 * m) * 2 ^ (96 * m) + 2 ^ (96 * m) := by ring
  omega

open Classical in
/-- **Teorema A de Terras (1976), segunda parte**: la densidad `F(k)` de los que bajan en a lo
    sumo `k` pasos tiende a 1. -/
theorem terras_tiende_a_uno :
    Filter.Tendsto (fun k : ℕ => (((Finset.range (2 ^ k)).filter fun r =>
        ∃ j, j ≤ k ∧ 3 ^ S j r < 2 ^ j).card : ℝ) / 2 ^ k) Filter.atTop (nhds 1) := by
  rw [Metric.tendsto_atTop]
  intro ε hε
  obtain ⟨m, hm⟩ := pow_unbounded_of_one_lt (3 / ε) (by norm_num : (1 : ℝ) < 16)
  refine ⟨100 * m, fun k hk => ?_⟩
  have h1 := restos_sin_cruce m k hk
  have hale := Finset.card_filter_le (Finset.range (2 ^ k)) (fun r => ∃ j, j ≤ k ∧ 3 ^ S j r < 2 ^ j)
  rw [Finset.card_range] at hale
  set a := ((Finset.range (2 ^ k)).filter fun r => ∃ j, j ≤ k ∧ 3 ^ S j r < 2 ^ j).card with ha
  have hX : (0 : ℝ) < 2 ^ k := by positivity
  have h16 : (0 : ℝ) < 16 ^ m := by positivity
  have h1R : (2 : ℝ) ^ k ≤ a + 2 * ((2 ^ k / 16 ^ m : ℕ) : ℝ) := by
    have : ((2 ^ k : ℕ) : ℝ) ≤ ((a + 2 * (2 ^ k / 16 ^ m) : ℕ) : ℝ) := by exact_mod_cast h1
    push_cast at this
    exact this
  have hdiv : ((2 ^ k / 16 ^ m : ℕ) : ℝ) ≤ (2 : ℝ) ^ k / 16 ^ m := by
    have : ((2 ^ k / 16 ^ m : ℕ) : ℝ) ≤ ((2 ^ k : ℕ) : ℝ) / ((16 ^ m : ℕ) : ℝ) := Nat.cast_div_le
    push_cast at this
    exact this
  have haleR : (a : ℝ) ≤ 2 ^ k := by exact_mod_cast hale
  have hlo : 1 - 2 / 16 ^ m ≤ (a : ℝ) / 2 ^ k := by
    rw [le_div_iff₀ hX]
    have : (2 : ℝ) ^ k * (2 / 16 ^ m) = 2 * ((2 : ℝ) ^ k / 16 ^ m) := by ring
    nlinarith
  have hhi : (a : ℝ) / 2 ^ k ≤ 1 := by
    rw [div_le_one hX]
    exact haleR
  have hsmall : 2 / (16 : ℝ) ^ m < ε := by
    have h7 : 3 < 16 ^ m * ε := (div_lt_iff₀ hε).1 hm
    rw [div_lt_iff₀ h16]
    nlinarith
  rw [Real.dist_eq, abs_sub_comm, abs_of_nonneg (by linarith)]
  linarith

/-! ## Los teoremas B y C -/

/-- **Teorema B de Terras**: cada patrón de subidas y bajadas de largo `k` corresponde a
    exactamente un resto módulo `2^k`. -/
theorem teorema_B (k : ℕ) (A : Finset ℕ) (hA : A ⊆ Finset.range k) :
    ∃! r, r < 2 ^ k ∧ subidas k r = A := by
  obtain ⟨x, hx, hxA⟩ := patron_realizable k A hA
  refine ⟨x, ⟨hx, hxA⟩, fun y hy => ?_⟩
  have h := congruentes_de_subidas (hy.2.trans hxA.symm)
  rwa [Nat.mod_eq_of_lt hy.1, Nat.mod_eq_of_lt hx] at h

/-- **Teorema C de Terras, (a)**: el primer cruce depende sólo del resto módulo `2^k`; los
    números con primer cruce `k` son una unión de clases módulo `2^k`. -/
theorem primer_cruce_resto (n k : ℕ) : PrimerCruce n k ↔ PrimerCruce (n % 2 ^ k) k := by
  have hb := congruentes_mismo_baile k n (n % 2 ^ k) (Nat.mod_mod n (2 ^ k)).symm
  have hS : ∀ j, j ≤ k → S j n = S j (n % 2 ^ k) := fun j hj =>
    subidas_iguales fun i hi => hb i (by omega)
  unfold PrimerCruce
  constructor
  · rintro ⟨h1, h2⟩
    refine ⟨fun j hj hj1 => ?_, ?_⟩
    · rw [← hS j hj.le]
      exact h1 j hj hj1
    · rw [← hS k le_rfl]
      exact h2
  · rintro ⟨h1, h2⟩
    refine ⟨fun j hj hj1 => ?_, ?_⟩
    · rw [hS j hj.le]
      exact h1 j hj hj1
    · rw [hS k le_rfl]
      exact h2

/-- **Teorema C de Terras, (b)**: si el primer cruce es `k` y `k·2^k ≤ 3n`, el tiempo de parada
    es exactamente `k`: el número no baja antes del paso `k`, y en él baja. -/
theorem teorema_C {n k : ℕ} (hk : PrimerCruce n k) (h : k * 2 ^ k ≤ 3 * n) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n :=
  ⟨fun _ hj => no_desciende_antes hk hj, desciende_si_grande hk h⟩

end CasaTerras

#print axioms CasaTerras.paso_congruente
#print axioms CasaTerras.congruentes_mismo_baile
#print axioms CasaTerras.subidas_iguales
#print axioms CasaTerras.baja_iff_cruza
#print axioms CasaTerras.cruza_resto
#print axioms CasaTerras.cuenta_resto
#print axioms CasaTerras.cuenta_periodica
#print axioms CasaTerras.densidad_terras
#print axioms CasaTerras.restos_sin_cruce
#print axioms CasaTerras.terras_tiende_a_uno
#print axioms CasaTerras.teorema_B
#print axioms CasaTerras.primer_cruce_resto
#print axioms CasaTerras.teorema_C
