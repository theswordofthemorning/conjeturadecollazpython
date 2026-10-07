import PerdicesEstela

/-! # Perdices: tamaño normalizado y regresos sublineales

Atajo T de Ocelotas; S cuenta las subidas anteriores al instante k.
Este archivo usa exclusivamente la casa vigente. Véase TAMANO.md.
-/

namespace PerdicesTamano

open Ocelotas CasaPlano CasaRetrato PerdicesEstela
open scoped BigOperators

/-- Inverso del pronóstico, en los reales. -/
noncomputable def inverso (n k : ℕ) : ℝ := 2 ^ k / 3 ^ S k n

/-- Tamaño real dividido por el pronóstico. -/
noncomputable def normalizado (n k : ℕ) : ℝ := inverso n k * (T^[k] n : ℝ)

theorem inverso_pos (n k : ℕ) : 0 < inverso n k := by
  unfold inverso
  positivity

theorem inverso_le_uno {n : ℕ} (h : FugaPura n) (k : ℕ) : inverso n k ≤ 1 := by
  unfold inverso
  rw [div_le_one (by positivity)]
  exact_mod_cast nunca_cruza h k

theorem normalizado_paso (n k : ℕ) :
    normalizado n (k + 1) = normalizado n k +
      (if T^[k] n % 2 = 1 then inverso n k / 3 else 0) := by
  have hS : S (k + 1) n = S k n + T^[k] n % 2 := by
    rw [S_add]
    simp [S]
  unfold normalizado inverso
  rw [hS, Function.iterate_succ_apply']
  rcases Nat.mod_two_eq_zero_or_one (T^[k] n) with hp | hp
  · have he : (2 : ℝ) * (T (T^[k] n) : ℝ) = (T^[k] n : ℝ) := by
      exact_mod_cast T_par hp
    rw [hp]
    simp only [reduceCtorEq, ↓reduceIte, add_zero, pow_succ]
    field_simp
    nlinarith [congrArg (fun z : ℝ => (2 : ℝ) ^ k * z) he]
  · have he : (2 : ℝ) * (T (T^[k] n) : ℝ) = 3 * (T^[k] n : ℝ) + 1 := by
      exact_mod_cast T_impar hp
    rw [hp]
    simp only [↓reduceIte, pow_succ]
    field_simp
    nlinarith [congrArg (fun z : ℝ => (2 : ℝ) ^ k * z) he]

theorem identidad_afin (n k : ℕ) :
    normalizado n k = n + ∑ j ∈ Finset.range k,
      if T^[j] n % 2 = 1 then inverso n j / 3 else 0 := by
  induction k with
  | zero => simp [normalizado, inverso, S]
  | succ k ih => rw [normalizado_paso, ih, Finset.sum_range_succ]; ring

theorem normalizado_paso_producto {n : ℕ} (hn : 0 < n) (k : ℕ) :
    normalizado n (k + 1) = normalizado n k *
      (if T^[k] n % 2 = 1 then 1 + 1 / (3 * (T^[k] n : ℝ)) else 1) := by
  rw [normalizado_paso]
  split_ifs
  · have hx : (T^[k] n : ℝ) ≠ 0 := by
      exact_mod_cast Nat.ne_of_gt (iter_pos hn k)
    unfold normalizado
    field_simp
  · ring

theorem identidad_producto {n : ℕ} (hn : 0 < n) (k : ℕ) :
    normalizado n k = n * ∏ j ∈ Finset.range k,
      (if T^[j] n % 2 = 1 then 1 + 1 / (3 * (T^[j] n : ℝ)) else 1) := by
  induction k with
  | zero => simp [normalizado, inverso, S]
  | succ k ih => rw [normalizado_paso_producto hn, ih, Finset.prod_range_succ]; ring

theorem normalizado_cota (n k : ℕ) :
    normalizado n k ≤ n + (∑ j ∈ Finset.range k, inverso n j) / 3 := by
  rw [identidad_afin]
  simp only [div_eq_mul_inv, Finset.sum_mul]
  gcongr with j
  split_ifs
  · rfl
  · exact le_of_lt (div_pos (inverso_pos n j) (by norm_num))

/-- Separación determinista de los tiempos bajos y altos. -/
theorem suma_inversos {n : ℕ} (h : FugaPura n) (k c : ℕ) :
    (∑ j ∈ Finset.range k, inverso n j) ≤
      (((Finset.range k).filter fun j => 3 ^ S j n ≤ 3 ^ c * 2 ^ j).card : ℝ) +
        (k : ℝ) / 3 ^ c := by
  classical
  have hp : ∀ j, inverso n j ≤
      (if 3 ^ S j n ≤ 3 ^ c * 2 ^ j then (1 : ℝ) else 0) + 1 / 3 ^ c := by
    intro j
    split_ifs with hj
    · exact (inverso_le_uno h j).trans (le_add_of_nonneg_right (by positivity))
    · have hj' : (3 : ℝ) ^ c * 2 ^ j ≤ 3 ^ S j n := by
        exact_mod_cast (Nat.le_of_lt (Nat.lt_of_not_ge hj))
      have hr : inverso n j ≤ 1 / 3 ^ c := by
        unfold inverso
        rw [div_le_div_iff₀ (by positivity) (by positivity)]
        nlinarith
      simpa using hr
  calc
    (∑ j ∈ Finset.range k, inverso n j) ≤
        ∑ j ∈ Finset.range k,
          ((if 3 ^ S j n ≤ 3 ^ c * 2 ^ j then (1 : ℝ) else 0) + 1 / 3 ^ c) :=
      Finset.sum_le_sum fun j _ => hp j
    _ = _ := by simp [Finset.sum_add_distrib, div_eq_mul_inv]

theorem normalizado_por_bajos {n : ℕ} (h : FugaPura n) (k c : ℕ) :
    normalizado n k ≤ n +
      ((((Finset.range k).filter fun j => 3 ^ S j n ≤ 3 ^ c * 2 ^ j).card : ℝ) +
        (k : ℝ) / 3 ^ c) / 3 := by
  exact (normalizado_cota n k).trans (by gcongr; exact suma_inversos h k c)

/-- Cota explícita: se pueden elegir c y m sin simular tiempos gigantes. -/
theorem normalizado_cota_explicita {n : ℕ} (h : FugaPura n) (k c m : ℕ) :
    normalizado n k ≤ n +
      ((6 ^ c * ((n : ℝ) + k) + 2 ^ c * 2 ^ (100 * m)) / 16 ^ m +
        (k : ℝ) / 3 ^ c) / 3 := by
  have hb : (((Finset.range k).filter fun j => 3 ^ S j n ≤ 3 ^ c * 2 ^ j).card : ℝ) ≤
      (6 ^ c * ((n : ℝ) + k) + 2 ^ c * 2 ^ (100 * m)) / 16 ^ m := by
    rw [le_div_iff₀ (by positivity)]
    exact_mod_cast tiempos_bajos_mul h c k m
  exact (normalizado_por_bajos h k c).trans (by gcongr)

/-- Para el mismo entero fugitivo, T^k(n)/P_k = o(k). -/
theorem normalizado_sublineal {n : ℕ} (h : FugaPura n) {ε : ℝ} (hε : 0 < ε) :
    ∃ K : ℕ, ∀ k, K ≤ k → normalizado n k ≤ ε * k := by
  obtain ⟨c, hc⟩ := pow_unbounded_of_one_lt (1 / ε) (by norm_num : (1 : ℝ) < 3)
  have hc' : 1 / (3 : ℝ) ^ c ≤ ε := by
    rw [div_le_iff₀ (by positivity)]
    have := (div_lt_iff₀ hε).1 hc
    nlinarith
  obtain ⟨K, hK⟩ := tiempos_bajos_raros h c hε
  refine ⟨max K ⌈3 * (n : ℝ) / ε⌉₊, fun k hk => ?_⟩
  have hn : 3 * (n : ℝ) ≤ ε * k := by
    have hceil : 3 * (n : ℝ) / ε ≤ (k : ℝ) :=
      (Nat.le_ceil _).trans (by exact_mod_cast le_trans (le_max_right _ _) hk)
    rw [div_le_iff₀ hε] at hceil
    linarith
  have hb := hK k (le_trans (le_max_left _ _) hk)
  have ht : (k : ℝ) / 3 ^ c ≤ ε * k := by
    calc (k : ℝ) / 3 ^ c = k * (1 / 3 ^ c) := by ring
      _ ≤ k * ε := mul_le_mul_of_nonneg_left hc' (Nat.cast_nonneg k)
      _ = ε * k := mul_comm _ _
  have hr := normalizado_por_bajos h k c
  linarith

theorem tamano_de_normalizado {n k c : ℕ}
    (hk : 3 ^ S k n ≤ 3 ^ c * 2 ^ k) :
    (T^[k] n : ℝ) ≤ 3 ^ c * normalizado n k := by
  have hp : (3 : ℝ) ^ S k n ≤ 3 ^ c * 2 ^ k := by exact_mod_cast hk
  unfold normalizado inverso
  apply (mul_le_mul_iff_left₀ (by positivity : (0 : ℝ) < 3 ^ S k n)).mp
  field_simp
  nlinarith [mul_le_mul_of_nonneg_right hp (Nat.cast_nonneg (T^[k] n) : (0 : ℝ) ≤ _)]

/-- Los regresos bajo cualquier techo fijo son sublineales en el tiempo. -/
theorem regresos_sublineales {n : ℕ} (h : FugaPura n) (c : ℕ)
    {ε : ℝ} (hε : 0 < ε) :
    ∃ K : ℕ, ∀ k, K ≤ k → 3 ^ S k n ≤ 3 ^ c * 2 ^ k →
      (T^[k] n : ℝ) ≤ ε * k := by
  obtain ⟨K, hK⟩ := normalizado_sublineal h (div_pos hε (by positivity : (0 : ℝ) < 3 ^ c))
  refine ⟨K, fun k hk hb => (tamano_de_normalizado hb).trans ?_⟩
  calc (3 : ℝ) ^ c * normalizado n k ≤ 3 ^ c * (ε / 3 ^ c * k) :=
      mul_le_mul_of_nonneg_left (hK k hk) (by positivity)
    _ = ε * k := by field_simp

/-- Factor elemental del producto ordenado; el telescopio completo es escrito. -/
theorem factor_sexta (r : ℕ) :
    r * (6 * r + 4) ^ 6 ≤ (r + 1) * (6 * r + 3) ^ 6 := by
  have hi : (r + 1) * (6 * r + 3) ^ 6 = r * (6 * r + 4) ^ 6 +
      (729 + 5381 * r + 15624 * r ^ 2 + 22140 * r ^ 3 +
        15120 * r ^ 4 + 3888 * r ^ 5) := by ring
  omega

end PerdicesTamano

#print axioms PerdicesTamano.inverso_pos
#print axioms PerdicesTamano.inverso_le_uno
#print axioms PerdicesTamano.normalizado_paso
#print axioms PerdicesTamano.identidad_afin
#print axioms PerdicesTamano.normalizado_paso_producto
#print axioms PerdicesTamano.identidad_producto
#print axioms PerdicesTamano.normalizado_cota
#print axioms PerdicesTamano.suma_inversos
#print axioms PerdicesTamano.normalizado_por_bajos
#print axioms PerdicesTamano.normalizado_cota_explicita
#print axioms PerdicesTamano.normalizado_sublineal
#print axioms PerdicesTamano.tamano_de_normalizado
#print axioms PerdicesTamano.regresos_sublineales
#print axioms PerdicesTamano.factor_sexta
