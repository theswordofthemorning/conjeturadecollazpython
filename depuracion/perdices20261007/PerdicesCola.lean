import PerdicesColisiones

/-! # Perdices: la cola real del cohete.

El supremo se interpreta como estatura sólo bajo positividad e
inyectividad de toda la órbita. No se identifica con un límite 2-ádico.
-/

namespace PerdicesCola

open Ocelotas CasaPlano CasaRetrato PerdicesTamano PerdicesColisiones
open scoped BigOperators
open Filter Topology

noncomputable def estatura (n : ℕ) : ℝ := ⨆ k, normalizado n k
noncomputable def aumentado (n k : ℕ) : ℝ := normalizado n k + inverso n k
noncomputable def cola (n k : ℕ) : ℝ := (estatura n - normalizado n k) / inverso n k

theorem inverso_paso (n k : ℕ) :
    inverso n (k + 1) =
      if T^[k] n % 2 = 1 then 2 * inverso n k / 3 else 2 * inverso n k := by
  have hs : S (k + 1) n = S k n + T^[k] n % 2 := by
    rw [S_add]
    simp [S]
  unfold inverso
  rw [hs, pow_succ]
  rcases Nat.mod_two_eq_zero_or_one (T^[k] n) with he | he
  · simp [he]; ring
  · simp only [he, ↓reduceIte, pow_succ]
    field_simp

theorem aumentado_paso (n k : ℕ) :
    aumentado n (k + 1) = aumentado n k +
      (if T^[k] n % 2 = 0 then inverso n k else 0) := by
  unfold aumentado
  rw [normalizado_paso, inverso_paso]
  rcases Nat.mod_two_eq_zero_or_one (T^[k] n) with he | he <;> simp [he] <;> ring

theorem aumentado_monotono (n : ℕ) : Monotone (aumentado n) := by
  apply monotone_nat_of_le_succ
  intro k
  rw [aumentado_paso]
  apply le_add_of_nonneg_right
  split_ifs
  · exact (inverso_pos n k).le
  · rfl

theorem identidad_pares (n k : ℕ) :
    aumentado n k = n + 1 + ∑ j ∈ Finset.range k,
      if T^[j] n % 2 = 0 then inverso n j else 0 := by
  induction k with
  | zero => simp [aumentado, normalizado, inverso, S]
  | succ k ih => rw [aumentado_paso, ih, Finset.sum_range_succ]; ring

theorem identidad_todos (n k : ℕ) :
    (∑ j ∈ Finset.range k, inverso n j) =
      4 * (normalizado n k - n) + inverso n k - 1 := by
  induction k with
  | zero => simp [normalizado, inverso, S]
  | succ k ih =>
    rw [Finset.sum_range_succ, ih, normalizado_paso, inverso_paso]
    split_ifs <;> ring

theorem estatura_acota {n : ℕ} (hn : 0 < n)
    (hi : Function.Injective (fun j => T^[j] n)) (k : ℕ) :
    normalizado n k ≤ estatura n := by
  apply le_ciSup
  exact ⟨n * Real.exp (2 ^ 100), fun x ⟨j, hj⟩ => hj ▸ normalizado_acotado hn hi j⟩

theorem estatura_limite {n : ℕ} (hn : 0 < n)
    (hi : Function.Injective (fun j => T^[j] n)) :
    Tendsto (normalizado n) atTop (𝓝 (estatura n)) := by
  apply tendsto_atTop_ciSup (normalizado_monotono n)
  exact ⟨n * Real.exp (2 ^ 100), fun x ⟨j, hj⟩ => hj ▸ normalizado_acotado hn hi j⟩

theorem inverso_pequeno {n : ℕ} (hn : 0 < n)
    (hi : Function.Injective (fun j => T^[j] n)) {ε : ℝ} (hε : 0 < ε) :
    ∃ K, ∀ k, K ≤ k → inverso n k < ε := by
  obtain ⟨K, hK⟩ := pronostico_supera hn hi (1 / ε) (by positivity)
  refine ⟨K, fun k hk => ?_⟩
  have h := (div_lt_div_iff₀ hε (show (0 : ℝ) < 2 ^ k by positivity)).mp (hK k hk)
  unfold inverso
  rw [div_lt_iff₀ (by positivity)]
  nlinarith only [h]

theorem inverso_limite {n : ℕ} (hn : 0 < n)
    (hi : Function.Injective (fun j => T^[j] n)) :
    Tendsto (inverso n) atTop (𝓝 0) := by
  apply tendsto_order.mpr
  constructor
  · intro a ha
    exact Filter.Eventually.of_forall fun k => ha.trans (inverso_pos n k)
  · intro b hb
    exact Filter.eventually_atTop.mpr (inverso_pequeno hn hi hb)

theorem aumentado_limite {n : ℕ} (hn : 0 < n)
    (hi : Function.Injective (fun j => T^[j] n)) :
    Tendsto (aumentado n) atTop (𝓝 (estatura n)) := by
  change Tendsto (fun k => normalizado n k + inverso n k) atTop (𝓝 (estatura n))
  simpa only [add_zero] using (estatura_limite hn hi).add (inverso_limite hn hi)

theorem aumentado_acota {n : ℕ} (hn : 0 < n)
    (hi : Function.Injective (fun j => T^[j] n)) (k : ℕ) :
    aumentado n k ≤ estatura n :=
  (aumentado_monotono n).ge_of_tendsto (aumentado_limite hn hi) k

theorem cola_identidad (n k : ℕ) :
    cola n k = estatura n * ((3 : ℝ) ^ S k n / 2 ^ k) - T^[k] n := by
  unfold cola normalizado inverso
  field_simp

theorem cola_al_menos_uno {n : ℕ} (hn : 0 < n)
    (hi : Function.Injective (fun j => T^[j] n)) (k : ℕ) : 1 ≤ cola n k := by
  have h := aumentado_acota hn hi k
  unfold aumentado at h
  unfold cola
  rw [le_div_iff₀ (inverso_pos n k)]
  linarith

theorem cola_paso (n k : ℕ) :
    cola n (k + 1) =
      if T^[k] n % 2 = 1 then (3 * cola n k - 1) / 2 else cola n k / 2 := by
  unfold cola
  rw [normalizado_paso, inverso_paso]
  have hp := ne_of_gt (inverso_pos n k)
  split_ifs <;> field_simp <;> ring

theorem cola_par {n : ℕ} (hn : 0 < n)
    (hi : Function.Injective (fun j => T^[j] n)) {k : ℕ} (hk : T^[k] n % 2 = 0) :
    2 ≤ cola n k := by
  have h := cola_al_menos_uno hn hi (k + 1)
  rw [cola_paso] at h
  simp only [hk, reduceCtorEq, ↓reduceIte] at h
  linarith

theorem cola_ceros (n k a : ℕ) (he : ∀ j, j < a → T^[k + j] n % 2 = 0) :
    cola n k = 2 ^ a * cola n (k + a) := by
  induction a with
  | zero => simp
  | succ a ih =>
    have he' := he a (by omega)
    have hpaso := cola_paso n (k + a)
    simp only [he', reduceCtorEq, ↓reduceIte] at hpaso
    rw [ih (fun j hj => he j (by omega)), pow_succ]
    have ht : k + (a + 1) = k + a + 1 := by omega
    rw [ht, hpaso]
    ring

theorem cola_antes_ceros {n : ℕ} (hn : 0 < n)
    (hi : Function.Injective (fun j => T^[j] n)) (k a : ℕ)
    (he : ∀ j, j < a → T^[k + j] n % 2 = 0) :
    (2 : ℝ) ^ a ≤ cola n k := by
  rw [cola_ceros n k a he]
  exact le_mul_of_one_le_right (by positivity) (cola_al_menos_uno hn hi (k + a))

theorem estatura_al_menos {n : ℕ} (hn : 0 < n)
    (hi : Function.Injective (fun j => T^[j] n)) : (n : ℝ) + 1 ≤ estatura n := by
  have h := aumentado_acota hn hi 0
  simpa [aumentado, normalizado, inverso, S] using h

theorem inverso_le_normalizado {n : ℕ} (hn : 0 < n) (k : ℕ) :
    inverso n k ≤ normalizado n k := by
  unfold normalizado
  apply le_mul_of_one_le_right (inverso_pos n k).le
  exact_mod_cast iter_pos hn k

theorem inversos_sumables {n : ℕ} (hn : 0 < n)
    (hi : Function.Injective (fun j => T^[j] n)) : Summable (inverso n) := by
  apply summable_of_sum_range_le (c := 5 * estatura n) (fun j => (inverso_pos n j).le)
  intro k
  rw [identidad_todos]
  have hr := estatura_acota hn hi k
  have hg := inverso_le_normalizado hn k
  have hnp : (0 : ℝ) ≤ n := Nat.cast_nonneg n
  linarith

theorem suma_inversos_total {n : ℕ} (hn : 0 < n)
    (hi : Function.Injective (fun j => T^[j] n)) :
    (∑' j, inverso n j) = 4 * (estatura n - n) - 1 := by
  have hlim : Tendsto (fun k => ∑ j ∈ Finset.range k, inverso n j) atTop
      (𝓝 (4 * (estatura n - n) - 1)) := by
    simp_rw [identidad_todos]
    have h := ((((estatura_limite hn hi).sub
      (tendsto_const_nhds (x := (n : ℝ)))).const_mul 4).add
      (inverso_limite hn hi)).sub (tendsto_const_nhds (x := (1 : ℝ)))
    simpa only [add_zero] using h
  exact tendsto_nhds_unique (inversos_sumables hn hi).hasSum.tendsto_sum_nat hlim

theorem cola_relativa {n : ℕ} (hn : 0 < n) (k : ℕ) :
    cola n k / (T^[k] n : ℝ) =
      (estatura n - normalizado n k) / normalizado n k := by
  have hx : (T^[k] n : ℝ) ≠ 0 := by exact_mod_cast Nat.ne_of_gt (iter_pos hn k)
  have hp := ne_of_gt (inverso_pos n k)
  unfold cola normalizado
  field_simp

theorem cola_relativa_limite {n : ℕ} (hn : 0 < n)
    (hi : Function.Injective (fun j => T^[j] n)) :
    Tendsto (fun k => cola n k / (T^[k] n : ℝ)) atTop (𝓝 0) := by
  have he : estatura n ≠ 0 := by
    have h := estatura_al_menos hn hi
    have hp : (0 : ℝ) < n := by exact_mod_cast hn
    linarith
  simp_rw [cola_relativa hn]
  change Tendsto ((fun k => estatura n - normalizado n k) / normalizado n) atTop (𝓝 0)
  simpa only [sub_self, zero_div] using
    ((tendsto_const_nhds (x := estatura n)).sub (estatura_limite hn hi)).div
      (estatura_limite hn hi) he

#print axioms PerdicesCola.inverso_paso
#print axioms PerdicesCola.aumentado_paso
#print axioms PerdicesCola.aumentado_monotono
#print axioms PerdicesCola.identidad_pares
#print axioms PerdicesCola.identidad_todos
#print axioms PerdicesCola.estatura_acota
#print axioms PerdicesCola.estatura_limite
#print axioms PerdicesCola.inverso_pequeno
#print axioms PerdicesCola.inverso_limite
#print axioms PerdicesCola.aumentado_limite
#print axioms PerdicesCola.aumentado_acota
#print axioms PerdicesCola.cola_identidad
#print axioms PerdicesCola.cola_al_menos_uno
#print axioms PerdicesCola.cola_paso
#print axioms PerdicesCola.cola_par
#print axioms PerdicesCola.cola_ceros
#print axioms PerdicesCola.cola_antes_ceros
#print axioms PerdicesCola.estatura_al_menos
#print axioms PerdicesCola.inverso_le_normalizado
#print axioms PerdicesCola.inversos_sumables
#print axioms PerdicesCola.suma_inversos_total
#print axioms PerdicesCola.cola_relativa
#print axioms PerdicesCola.cola_relativa_limite

end PerdicesCola
