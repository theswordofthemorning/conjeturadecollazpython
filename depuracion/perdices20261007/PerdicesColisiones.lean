import PerdicesNovena

/-! # Perdices: colisiones y suma de recíprocos.

Atajo T sobre naturales. Las hipótesis orbitales se declaran en cada lema.
La cuenta finita no presupone que exista una órbita inyectiva positiva.
-/

namespace PerdicesColisiones

open Ocelotas CasaPlano CasaRetrato PerdicesTamano PerdicesCruce
open scoped BigOperators

set_option exponentiation.threshold 2048

/-- Cota afín válida incluso para entradas cero y prefijos que ya cruzaron. -/
theorem cota_afin (n k : ℕ) :
    2 ^ k * (T^[k] n + 1) ≤ 3 ^ S k n * n + 3 ^ k := by
  induction k with
  | zero => simp [S]
  | succ k ih =>
    have hs : S (k + 1) n = S k n + T^[k] n % 2 := by
      rw [S_add]
      simp [S]
    rw [hs, Function.iterate_succ_apply']
    have hp : 2 ^ k ≤ (3 : ℕ) ^ k := Nat.pow_le_pow_left (by norm_num) k
    rcases Nat.mod_two_eq_zero_or_one (T^[k] n) with he | he
    · have ht := T_par he
      simp only [he, add_zero, pow_succ]
      calc 2 ^ k * 2 * (T (T^[k] n) + 1) =
            2 ^ k * (T^[k] n + 1) + 2 ^ k := by
              conv_rhs => rw [← ht]
              ring
           _ ≤ (3 ^ S k n * n + 3 ^ k) + 2 ^ k := Nat.add_le_add_right ih _
           _ ≤ 3 ^ S k n * n + 3 ^ k * 3 := by omega
    · have ht := T_impar he
      simp only [he, pow_succ]
      nlinarith [Nat.mul_le_mul_left (2 ^ k) ht.le,
        Nat.mul_le_mul_left (2 ^ k) ht.ge]

theorem patrones_sesenta (m : ℕ) :
    ((Finset.range (100 * m)).powerset.filter fun A => 60 * m ≤ A.card).card
      ≤ 2 ^ (99 * m) := by
  set B := (Finset.range (100 * m)).powerset.filter fun A => 60 * m ≤ A.card
  have hsuma : ∑ A ∈ (Finset.range (100 * m)).powerset, 2 ^ A.card = 3 ^ (100 * m) := by
    simpa using Finset.sum_pow_mul_eq_add_pow (2 : ℕ) 1 (Finset.range (100 * m))
  have h1 : B.card * 2 ^ (60 * m) ≤ 3 ^ (100 * m) := by
    calc B.card * 2 ^ (60 * m) = ∑ A ∈ B, 2 ^ (60 * m) := by
          rw [Finset.sum_const, smul_eq_mul]
         _ ≤ ∑ A ∈ B, 2 ^ A.card := Finset.sum_le_sum fun A hA =>
          Nat.pow_le_pow_right (by norm_num) (Finset.mem_filter.mp hA).2
         _ ≤ ∑ A ∈ (Finset.range (100 * m)).powerset, 2 ^ A.card :=
          Finset.sum_le_sum_of_subset (Finset.filter_subset _ _)
         _ = 3 ^ (100 * m) := hsuma
  have h2 : 3 ^ (100 * m) ≤ 2 ^ (99 * m) * 2 ^ (60 * m) := by
    rw [← pow_add, show 99 * m + 60 * m = 159 * m by ring, pow_mul, pow_mul]
    exact Nat.pow_le_pow_left (by norm_num) m
  exact Nat.le_of_mul_le_mul_right (h1.trans h2) (by positivity)

theorem entradas_sesenta (m : ℕ) :
    ((Finset.range (2 ^ (100 * m))).filter fun n => 60 * m ≤ S (100 * m) n).card
      ≤ 2 ^ (99 * m) := by
  apply le_trans _ (patrones_sesenta m)
  refine Finset.card_le_card_of_injOn (subidas (100 * m)) ?_ ?_
  · intro n hn
    simp only [Finset.mem_coe, Finset.mem_filter, Finset.mem_powerset, card_subidas]
    exact ⟨subidas_sub _ _, (Finset.mem_filter.mp hn).2⟩
  · intro n hn n' hn' heq
    have h := congruentes_de_subidas heq
    have hn := Finset.mem_range.mp (Finset.mem_filter.mp hn).1
    have hn' := Finset.mem_range.mp (Finset.mem_filter.mp hn').1
    simpa [Nat.mod_eq_of_lt hn, Nat.mod_eq_of_lt hn'] using h

theorem imagen_pocas_subidas {n m : ℕ} (hn : n < 2 ^ (100 * m))
    (hs : S (100 * m) n < 60 * m) : T^[100 * m] n < 2 * 2 ^ (96 * m) := by
  have h3 : 3 ^ S (100 * m) n ≤ (2 : ℕ) ^ (96 * m) := by
    calc 3 ^ S (100 * m) n ≤ 3 ^ (60 * m) :=
          Nat.pow_le_pow_right (by norm_num) hs.le
         _ = (3 ^ 5) ^ (12 * m) := by rw [← pow_mul]; congr 1; ring
         _ ≤ (2 ^ 8) ^ (12 * m) := Nat.pow_le_pow_left (by norm_num) _
         _ = 2 ^ (96 * m) := by rw [← pow_mul]; congr 1; ring
  have h100 : (3 : ℕ) ^ (100 * m) ≤ 2 ^ (159 * m) := by
    rw [pow_mul, pow_mul]
    exact Nat.pow_le_pow_left (by norm_num) m
  have h59 : (2 : ℕ) ^ (59 * m) ≤ 2 ^ (96 * m) :=
    Nat.pow_le_pow_right (by norm_num) (by omega)
  have h := (cota_afin n (100 * m)).trans
    (Nat.add_le_add (Nat.mul_le_mul h3 hn.le) h100)
  have he : (2 : ℕ) ^ (159 * m) = 2 ^ (100 * m) * 2 ^ (59 * m) := by
    rw [← pow_add]; congr 1; ring
  rw [he] at h
  have h' : T^[100 * m] n + 1 ≤ 2 ^ (96 * m) + 2 ^ (59 * m) := by
    exact Nat.le_of_mul_le_mul_left
      (show 2 ^ (100 * m) * (T^[100 * m] n + 1) ≤
        2 ^ (100 * m) * (2 ^ (96 * m) + 2 ^ (59 * m)) by nlinarith) (by positivity)
  omega

/-- Cuenta por imágenes, antes de introducir ninguna órbita. -/
theorem cuenta_imagen (m : ℕ) :
    ((Finset.range (2 ^ (100 * m))).image (T^[100 * m])).card ≤ 3 * 2 ^ (99 * m) := by
  classical
  let A := Finset.range (2 ^ (100 * m))
  let B := A.filter fun n => 60 * m ≤ S (100 * m) n
  have hc : A.image (T^[100 * m]) ⊆
      Finset.range (2 * 2 ^ (96 * m)) ∪ B.image (T^[100 * m]) := by
    intro x hx
    obtain ⟨n, hn, rfl⟩ := Finset.mem_image.mp hx
    by_cases hs : 60 * m ≤ S (100 * m) n
    · exact Finset.mem_union_right _ (Finset.mem_image.mpr
        ⟨n, Finset.mem_filter.mpr ⟨hn, hs⟩, rfl⟩)
    · exact Finset.mem_union_left _ (Finset.mem_range.mpr
        (imagen_pocas_subidas (Finset.mem_range.mp hn) (by omega)))
  have hb : B.card ≤ 2 ^ (99 * m) := entradas_sesenta m
  have hp : (2 : ℕ) ^ (96 * m) ≤ 2 ^ (99 * m) :=
    Nat.pow_le_pow_right (by norm_num) (by omega)
  have h := (Finset.card_le_card hc).trans (Finset.card_union_le _ _)
  rw [Finset.card_range] at h
  have hi := Finset.card_image_le (s := B) (f := T^[100 * m])
  change (A.image (T^[100 * m])).card ≤ _
  omega

/-- Cada iterado es inyectivo en el rango de una órbita inyectiva. -/
theorem inyectiva_en_orbita {n : ℕ} (hi : Function.Injective (fun j => T^[j] n))
    (k : ℕ) : Set.InjOn (T^[k]) (Set.range fun j => T^[j] n) := by
  rintro x ⟨i, rfl⟩ y ⟨j, rfl⟩ he
  rw [← Function.iterate_add_apply, ← Function.iterate_add_apply] at he
  have h := hi he
  have hij : i = j := by omega
  rw [hij]

theorem cuenta_orbita {n : ℕ} (hi : Function.Injective (fun j => T^[j] n))
    (A : Finset ℕ) (ha : ∀ a ∈ A, a ∈ Set.range (fun j => T^[j] n)) (m : ℕ) :
    (A.filter fun a => a < 2 ^ (100 * m)).card ≤ 3 * 2 ^ (99 * m) := by
  classical
  let B := A.filter fun a => a < 2 ^ (100 * m)
  have hiB : Set.InjOn (T^[100 * m]) B :=
    (inyectiva_en_orbita hi _).mono (fun a h => ha a (Finset.mem_filter.mp h).1)
  have hb : B.image (T^[100 * m]) ⊆
      (Finset.range (2 ^ (100 * m))).image (T^[100 * m]) := by
    apply Finset.image_subset_image
    intro a h
    exact Finset.mem_range.mpr (Finset.mem_filter.mp h).2
  calc B.card = (B.image (T^[100 * m])).card := (Finset.card_image_of_injOn hiB).symm
       _ ≤ _ := (Finset.card_le_card hb).trans (cuenta_imagen m)

/-- Contribución de un intervalo geométrico, multiplicada por 2^m. -/
theorem suma_anillo (A : Finset ℕ)
    (hc : ∀ m, (A.filter fun a => a < 2 ^ (100 * m)).card ≤ 3 * 2 ^ (99 * m))
    (m : ℕ) :
    (∑ a ∈ A.filter (fun a => 2 ^ (100 * m) ≤ a ∧ a < 2 ^ (100 * (m + 1))),
      (1 : ℝ) / a) * 2 ^ m ≤ 3 * 2 ^ 99 := by
  classical
  let B := A.filter fun a => 2 ^ (100 * m) ≤ a ∧ a < 2 ^ (100 * (m + 1))
  have hb : B.card ≤ 3 * 2 ^ (99 * (m + 1)) := by
    apply le_trans _ (hc (m + 1))
    apply Finset.card_le_card
    intro a ha
    exact Finset.mem_filter.mpr ⟨(Finset.mem_filter.mp ha).1, (Finset.mem_filter.mp ha).2.2⟩
  have hs : (∑ a ∈ B, (1 : ℝ) / a) * 2 ^ (100 * m) ≤ B.card := by
    rw [Finset.sum_mul]
    calc (∑ a ∈ B, (1 : ℝ) / a * 2 ^ (100 * m)) ≤ ∑ _a ∈ B, (1 : ℝ) := by
          apply Finset.sum_le_sum
          intro a ha
          have hl : (2 : ℝ) ^ (100 * m) ≤ a := by
            exact_mod_cast (Finset.mem_filter.mp ha).2.1
          have hap : (0 : ℝ) < a := lt_of_lt_of_le (by positivity) hl
          rw [one_div, mul_comm, ← div_eq_mul_inv, div_le_one hap]
          exact hl
         _ = B.card := by simp
  have hb' : (B.card : ℝ) ≤ 3 * 2 ^ (99 * (m + 1)) := by exact_mod_cast hb
  have he1 : (2 : ℝ) ^ (100 * m) = 2 ^ m * 2 ^ (99 * m) := by
    rw [← pow_add]; congr 1; omega
  have he2 : (2 : ℝ) ^ (99 * (m + 1)) = 2 ^ 99 * 2 ^ (99 * m) := by
    rw [← pow_add]; congr 1; omega
  rw [he1] at hs
  rw [he2] at hb'
  exact (mul_le_mul_iff_left₀ (show (0 : ℝ) < 2 ^ (99 * m) by positivity)).mp
    (by nlinarith only [hs, hb'])

/-- Una inducción finita suma todos los anillos; no presupone convergencia. -/
theorem suma_hasta (A : Finset ℕ) (hp : ∀ a ∈ A, 0 < a)
    (hc : ∀ m, (A.filter fun a => a < 2 ^ (100 * m)).card ≤ 3 * 2 ^ (99 * m))
    (M : ℕ) :
    (∑ a ∈ A.filter (fun a => a < 2 ^ (100 * M)), (1 : ℝ) / a) * 2 ^ M +
      2 * (3 * 2 ^ 99) ≤ 2 * (3 * 2 ^ 99) * 2 ^ M := by
  classical
  induction M with
  | zero =>
    have hz : A.filter (fun a => a < 2 ^ (100 * 0)) = ∅ := by
      apply Finset.eq_empty_iff_forall_notMem.mpr
      intro a ha
      have ha' := Finset.mem_filter.mp ha
      have := hp a ha'.1
      simp only [mul_zero, pow_zero] at ha'
      omega
    rw [hz]
    simp
  | succ M ih =>
    let B := A.filter fun a => a < 2 ^ (100 * M)
    let D := A.filter fun a => 2 ^ (100 * M) ≤ a ∧ a < 2 ^ (100 * (M + 1))
    have he : A.filter (fun a => a < 2 ^ (100 * (M + 1))) = B ∪ D := by
      have hpow : (2 : ℕ) ^ (100 * M) ≤ 2 ^ (100 * (M + 1)) :=
        Nat.pow_le_pow_right (by norm_num) (by omega)
      ext a
      simp only [B, D, Finset.mem_filter, Finset.mem_union]
      constructor
      · rintro ⟨ha, hu⟩
        by_cases hl : a < 2 ^ (100 * M)
        · exact Or.inl ⟨ha, hl⟩
        · exact Or.inr ⟨ha, by omega, hu⟩
      · rintro (⟨ha, hl⟩ | ⟨ha, _, hu⟩)
        · exact ⟨ha, hl.trans_le hpow⟩
        · exact ⟨ha, hu⟩
    have hd : Disjoint B D := by
      rw [Finset.disjoint_left]
      intro a hb hd
      have := (Finset.mem_filter.mp hb).2
      have := (Finset.mem_filter.mp hd).2.1
      omega
    have hs := suma_anillo A hc M
    change (∑ a ∈ D, (1 : ℝ) / a) * 2 ^ M ≤ _ at hs
    change (∑ a ∈ B, (1 : ℝ) / a) * 2 ^ M + _ ≤ _ at ih
    rw [he, Finset.sum_union hd, pow_succ]
    nlinarith only [ih, hs]

theorem suma_finita (A : Finset ℕ) (hp : ∀ a ∈ A, 0 < a)
    (hc : ∀ m, (A.filter fun a => a < 2 ^ (100 * m)).card ≤ 3 * 2 ^ (99 * m)) :
    (∑ a ∈ A, (1 : ℝ) / a) ≤ 3 * 2 ^ 100 := by
  classical
  let M := A.sup id + 1
  have he : A.filter (fun a => a < 2 ^ (100 * M)) = A := by
    apply Finset.filter_eq_self.mpr
    intro a ha
    have ham : a < M := by
      have := Finset.le_sup (f := id) ha
      change a ≤ A.sup id at this
      omega
    have hm : M < 2 ^ (100 * M) := Nat.lt_two_pow_self.trans_le
      (Nat.pow_le_pow_right (by norm_num) (by omega))
    exact ham.trans hm
  have h := suma_hasta A hp hc M
  rw [he] at h
  have hcst : (2 : ℝ) * (3 * 2 ^ 99) = 3 * 2 ^ 100 := by norm_num
  rw [hcst] at h
  have hp2 : (0 : ℝ) < 2 ^ M := by positivity
  apply (mul_le_mul_iff_left₀ hp2).mp
  nlinarith only [h]

theorem suma_orbital {n : ℕ} (hn : 0 < n)
    (hi : Function.Injective (fun j => T^[j] n)) (k : ℕ) :
    (∑ j ∈ Finset.range k, (1 : ℝ) / (T^[j] n : ℝ)) ≤ 3 * 2 ^ 100 := by
  classical
  let A := (Finset.range k).image fun j => T^[j] n
  have hp : ∀ a ∈ A, 0 < a := by
    intro a ha
    obtain ⟨j, _, rfl⟩ := Finset.mem_image.mp ha
    exact iter_pos hn j
  have ha : ∀ a ∈ A, a ∈ Set.range (fun j => T^[j] n) := by
    intro a ha
    obtain ⟨j, _, rfl⟩ := Finset.mem_image.mp ha
    exact ⟨j, rfl⟩
  have h := suma_finita A hp (cuenta_orbita hi A ha)
  simpa only [A, Finset.sum_image (fun i _ j _ hij => hi hij)] using h

/-- El producto corrector queda acotado uniformemente en el tiempo. -/
theorem normalizado_acotado {n : ℕ} (hn : 0 < n)
    (hi : Function.Injective (fun j => T^[j] n)) (k : ℕ) :
    normalizado n k ≤ n * Real.exp (2 ^ 100) := by
  have hs : (∑ j ∈ Finset.range k, (1 : ℝ) / (3 * (T^[j] n : ℝ))) ≤ 2 ^ 100 := by
    have he : (∑ j ∈ Finset.range k, (1 : ℝ) / (3 * (T^[j] n : ℝ))) =
        (∑ j ∈ Finset.range k, (1 : ℝ) / (T^[j] n : ℝ)) / 3 := by
      simp only [div_eq_mul_inv, Finset.sum_mul]
      apply Finset.sum_congr rfl
      intro j _
      ring
    rw [he]
    have h := suma_orbital hn hi k
    linarith
  rw [identidad_producto hn]
  apply mul_le_mul_of_nonneg_left _ (Nat.cast_nonneg n)
  apply le_trans _ (Real.exp_le_exp.mpr hs)
  rw [Real.exp_sum]
  apply Finset.prod_le_prod
  · intro j _
    split_ifs <;> positivity
  · intro j _
    split_ifs
    · simpa only [add_comm] using Real.add_one_le_exp (1 / (3 * (T^[j] n : ℝ)))
    · exact Real.one_le_exp_iff.mpr (by positivity)

theorem reciprocos_sumables {n : ℕ} (hn : 0 < n)
    (hi : Function.Injective (fun j => T^[j] n)) :
    Summable (fun j => (1 : ℝ) / (T^[j] n : ℝ)) :=
  summable_of_sum_range_le (fun _ => by positivity) (suma_orbital hn hi)

theorem normalizado_monotono (n : ℕ) : Monotone (normalizado n) := by
  apply monotone_nat_of_le_succ
  intro k
  rw [normalizado_paso]
  apply le_add_of_nonneg_right
  split_ifs
  · exact div_nonneg (le_of_lt (inverso_pos n k)) (by norm_num)
  · rfl

open Filter Topology in
theorem normalizado_limite {n : ℕ} (hn : 0 < n)
    (hi : Function.Injective (fun j => T^[j] n)) :
    ∃ ξ : ℝ, n ≤ ξ ∧ ξ ≤ n * Real.exp (2 ^ 100) ∧
      Tendsto (normalizado n) atTop (𝓝 ξ) := by
  have hb : BddAbove (Set.range (normalizado n)) :=
    ⟨n * Real.exp (2 ^ 100), fun x ⟨k, hk⟩ => hk ▸ normalizado_acotado hn hi k⟩
  refine ⟨⨆ k, normalizado n k, ?_, ciSup_le (normalizado_acotado hn hi),
    tendsto_atTop_ciSup (normalizado_monotono n) hb⟩
  have h0 : (n : ℝ) = normalizado n 0 := by simp [normalizado, inverso, S]
  rw [h0]
  exact le_ciSup hb 0

/-- La inyectividad basta para que los valores naturales escapen de cada cota. -/
theorem orbita_supera {n : ℕ} (hi : Function.Injective (fun j => T^[j] n)) (M : ℕ) :
    ∃ K, ∀ k, K ≤ k → M < T^[k] n := by
  have hf : ((fun j => T^[j] n) ⁻¹' Set.Iic M).Finite :=
    (Set.finite_Iic M).preimage hi.injOn
  obtain ⟨K, hK⟩ := hf.bddAbove
  refine ⟨K + 1, fun k hk => ?_⟩
  by_contra hc
  have hm : k ∈ (fun j => T^[j] n) ⁻¹' Set.Iic M := by
    simp only [Set.mem_preimage, Set.mem_Iic]
    omega
  have := hK hm
  omega

/-- El pronóstico supera eventualmente cada techo real positivo. -/
theorem pronostico_supera {n : ℕ} (hn : 0 < n)
    (hi : Function.Injective (fun j => T^[j] n)) (C : ℝ) (hC : 0 < C) :
    ∃ K, ∀ k, K ≤ k → C < (3 : ℝ) ^ S k n / 2 ^ k := by
  obtain ⟨M, hM⟩ := exists_nat_gt (C * (n * Real.exp (2 ^ 100)))
  obtain ⟨K, hK⟩ := orbita_supera hi M
  refine ⟨K, fun k hk => ?_⟩
  have hx : C * (n * Real.exp (2 ^ 100)) < (T^[k] n : ℝ) :=
    hM.trans (by exact_mod_cast hK k hk)
  have hr := normalizado_acotado hn hi k
  have he : (3 : ℝ) ^ S k n / 2 ^ k * normalizado n k = T^[k] n := by
    unfold normalizado inverso
    field_simp
  by_contra hc
  have hc' : (3 : ℝ) ^ S k n / 2 ^ k ≤ C := le_of_not_gt hc
  have h := mul_le_mul hc' hr (by unfold normalizado inverso; positivity) (le_of_lt hC)
  rw [he] at h
  exact (not_le_of_gt hx) h

theorem fuga_supera {n : ℕ} (h : FugaPura n) (c : ℕ) :
    ∃ K, ∀ k, K ≤ k → 3 ^ c * 2 ^ k < 3 ^ S k n := by
  obtain ⟨K, hK⟩ := pronostico_supera (by have := fuga_pura_dos h; omega)
    (rasgo_inyectiva h) ((3 : ℝ) ^ c) (by positivity)
  refine ⟨K, fun k hk => ?_⟩
  have hr := (lt_div_iff₀ (show (0 : ℝ) < 2 ^ k by positivity)).mp (hK k hk)
  exact_mod_cast hr

theorem sin_regresos_infinitos {n : ℕ} (h : FugaPura n) (c : ℕ) :
    ¬ PerdicesExcursiones.InfinitosRegresos n c := by
  intro hi
  obtain ⟨K, hK⟩ := fuga_supera h c
  obtain ⟨j, hj, hb⟩ := hi K
  have hs := hK j hj.le
  exact (not_le_of_gt hs) hb

/-- Niega la segunda alternativa de CasaPlaneador.cohete_o_planeador_intermitente. -/
theorem sin_planeador_intermitente {n : ℕ} (h : FugaPura n) :
    ¬ ∃ c, ∀ K, ∃ k, K ≤ k ∧ 3 ^ S k n ≤ 3 ^ c * 2 ^ k := by
  rintro ⟨c, hc⟩
  obtain ⟨K, hK⟩ := fuga_supera h c
  obtain ⟨k, hk, hb⟩ := hc K
  exact (not_le_of_gt (hK k hk)) hb

#print axioms PerdicesColisiones.cota_afin
#print axioms PerdicesColisiones.patrones_sesenta
#print axioms PerdicesColisiones.entradas_sesenta
#print axioms PerdicesColisiones.imagen_pocas_subidas
#print axioms PerdicesColisiones.cuenta_imagen
#print axioms PerdicesColisiones.inyectiva_en_orbita
#print axioms PerdicesColisiones.cuenta_orbita
#print axioms PerdicesColisiones.suma_anillo
#print axioms PerdicesColisiones.suma_hasta
#print axioms PerdicesColisiones.suma_finita
#print axioms PerdicesColisiones.suma_orbital
#print axioms PerdicesColisiones.normalizado_acotado
#print axioms PerdicesColisiones.reciprocos_sumables
#print axioms PerdicesColisiones.normalizado_monotono
#print axioms PerdicesColisiones.normalizado_limite
#print axioms PerdicesColisiones.orbita_supera
#print axioms PerdicesColisiones.pronostico_supera
#print axioms PerdicesColisiones.fuga_supera
#print axioms PerdicesColisiones.sin_regresos_infinitos
#print axioms PerdicesColisiones.sin_planeador_intermitente

end PerdicesColisiones
