import CasaFugitivo

/-! # Dónde puede estar un choque

Ruta B, paso 3 (05-10-2026), con presupuesto acotado. Dos hechos que delimitan la
búsqueda de una contradicción entre los rasgos del fugitivo (`CasaFugitivo`):

* `sin_choque_finito`: para cada horizonte `K` hay números `n ≥ 2` cuyo pronóstico no baja
  de 1 en los `K` primeros pasos (`2^(K+2) - 1`). Ninguna contradicción puede salir de
  mirar sólo un tramo finito del pronóstico: tiene que usar el comportamiento infinito.
* `periodico_iff_acotada`: el patrón de paridades de `n` es finalmente periódico si y sólo
  si la órbita de `n` está acotada. Así, `sin_fugas_iff_periodicidad`: «no hay fugas»
  equivale a «todo número natural tiene patrón finalmente periódico», y
  `muroB_de_periodicidad`: esa periodicidad levanta el muro B.

Compilación: `comprobar_fugitivo.py`, en esta carpeta. -/

namespace CasaChoques

open Ocelotas OcelotasContador CasaPlano CasaFugitivo

/-! ## Sin choque en horizonte finito -/

theorem T_impar_forma {a : ℕ} (ha : 1 ≤ a) : T (2 * a - 1) = 3 * a - 1 := by
  unfold T
  rw [if_neg (by omega)]
  omega

/-- `T^t (2^t b - 1) = 3^t b - 1`: los unos del final de la escritura binaria son subidas. -/
theorem iter_unos : ∀ t b, 1 ≤ b → T^[t] (2 ^ t * b - 1) = 3 ^ t * b - 1
  | 0, b, _ => by simp
  | t + 1, b, hb => by
    have hpos : 1 ≤ 2 ^ t * b := Nat.mul_pos (by positivity) hb
    rw [Function.iterate_succ_apply, show 2 ^ (t + 1) * b = 2 * (2 ^ t * b) by ring,
      T_impar_forma hpos, show 3 * (2 ^ t * b) = 2 ^ t * (3 * b) by ring,
      iter_unos t (3 * b) (by omega), show 3 ^ (t + 1) * b = 3 ^ t * (3 * b) by ring]

theorem unos_impares {K j : ℕ} (hj : j < K) : T^[j] (2 ^ K - 1) % 2 = 1 := by
  obtain ⟨r, rfl⟩ : ∃ r, K = j + (r + 1) := ⟨K - j - 1, by omega⟩
  have h := iter_unos j (2 ^ (r + 1)) Nat.one_le_two_pow
  rw [← pow_add] at h
  rw [h, pow_succ]
  have hc : 1 ≤ 3 ^ j * 2 ^ r := Nat.mul_pos (by positivity) (by positivity)
  rw [show 3 ^ j * (2 ^ r * 2) = 2 * (3 ^ j * 2 ^ r) by ring]
  omega

/-- `2^K - 1` sube en cada uno de sus `K` primeros pasos. -/
theorem sin_cruce_hasta (K : ℕ) : ∀ j, j ≤ K → 2 ^ j ≤ 3 ^ S j (2 ^ K - 1) := by
  intro j hj
  rw [S_impar j _ (fun t ht => unos_impares (by omega))]
  exact Nat.pow_le_pow_left (by norm_num) j

/-- **Sin choque finito.** Para cada horizonte `K` hay `n ≥ 2` cuyo pronóstico no baja de 1
    en los `K` primeros pasos. -/
theorem sin_choque_finito (K : ℕ) : ∃ n, 2 ≤ n ∧ ∀ j, j ≤ K → 2 ^ j ≤ 3 ^ S j n := by
  refine ⟨2 ^ (K + 2) - 1, ?_, fun j hj => sin_cruce_hasta (K + 2) j (by omega)⟩
  have h4 : 2 ^ 2 ≤ 2 ^ (K + 2) := Nat.pow_le_pow_right (by norm_num) (by omega)
  omega

/-! ## Periodicidad de paridades y órbitas acotadas -/

/-- Una repetición `T^i n = T^(i+p) n` deja toda la órbita dentro de sus `i + p` primeros
    valores. -/
theorem orbita_en_prefijo {n i p : ℕ} (hrep : T^[i] n = T^[i + p] n) (hp : 1 ≤ p) :
    ∀ k, ∃ j, j < i + p ∧ T^[k] n = T^[j] n := by
  intro k
  induction k using Nat.strong_induction_on with
  | _ k ih =>
    by_cases hk : k < i + p
    · exact ⟨k, hk, rfl⟩
    · obtain ⟨j, hj, hjeq⟩ := ih (k - p) (by omega)
      refine ⟨j, hj, ?_⟩
      have e1 : T^[k] n = T^[k - p - i] (T^[i + p] n) := by
        rw [← iter_add, show i + p + (k - p - i) = k by omega]
      have e2 : T^[k - p] n = T^[k - p - i] (T^[i] n) := by
        rw [← iter_add, show i + (k - p - i) = k - p by omega]
      rw [← hjeq, e1, e2, hrep]

theorem acotada_de_repeticion {n i p : ℕ} (hrep : T^[i] n = T^[i + p] n) (hp : 1 ≤ p) :
    ¬ Fuga n := by
  intro hf
  obtain ⟨k, hk⟩ := hf ((Finset.range (i + p)).sum fun j => T^[j] n)
  obtain ⟨j, hj, hjeq⟩ := orbita_en_prefijo hrep hp k
  have hs : T^[j] n ≤ (Finset.range (i + p)).sum fun j => T^[j] n :=
    Finset.single_le_sum (f := fun j => T^[j] n) (fun _ _ => Nat.zero_le _)
      (Finset.mem_range.2 hj)
  omega

/-- El patrón de paridades de `n` es finalmente periódico si y sólo si su órbita está
    acotada. -/
theorem periodico_iff_acotada (n : ℕ) : PatronPeriodico n ↔ ¬ Fuga n := by
  classical
  constructor
  · rintro ⟨i, p, hp1, hper⟩
    exact acotada_de_repeticion (ciclo_de_patron hper) hp1
  · intro hf
    simp only [Fuga, not_forall, not_exists, not_lt] at hf
    obtain ⟨M, hM⟩ := hf
    have hmaps : Set.MapsTo (fun k => T^[k] n) (↑(Finset.range (M + 2)) : Set ℕ)
        (↑(Finset.range (M + 1)) : Set ℕ) := by
      intro k _
      simp only [Finset.mem_coe, Finset.mem_range]
      exact Nat.lt_succ_of_le (hM k)
    obtain ⟨a, -, b, -, hab, heq⟩ :=
      Finset.exists_ne_map_eq_of_card_lt_of_maps_to (by simp) hmaps
    have hrep : ∀ i j, i < j → T^[i] n = T^[j] n → PatronPeriodico n := by
      intro i j hij hq
      refine ⟨i, j - i, by omega, fun l hl => ?_⟩
      rw [show l + (j - i) = j + (l - i) by omega, iter_add, ← hq, ← iter_add,
        show i + (l - i) = l by omega]
    rcases lt_or_gt_of_ne hab with h | h
    · exact hrep a b h heq
    · exact hrep b a h heq.symm

/-- «No hay fugas» equivale a «todo natural tiene patrón de paridades finalmente
    periódico». -/
theorem sin_fugas_iff_periodicidad : (∀ n, ¬ Fuga n) ↔ ∀ n, PatronPeriodico n :=
  ⟨fun h n => (periodico_iff_acotada n).2 (h n), fun h n => (periodico_iff_acotada n).1 (h n)⟩

/-- La periodicidad de los patrones de paridad de los naturales levanta el muro B. -/
theorem muroB_de_periodicidad (h : ∀ n, PatronPeriodico n) : MuroB := by
  intro n _
  by_contra hc
  exact fugitivo_no_periodico hc (h n)

end CasaChoques

#print axioms CasaChoques.sin_cruce_hasta
#print axioms CasaChoques.sin_choque_finito
#print axioms CasaChoques.periodico_iff_acotada
#print axioms CasaChoques.sin_fugas_iff_periodicidad
#print axioms CasaChoques.muroB_de_periodicidad
