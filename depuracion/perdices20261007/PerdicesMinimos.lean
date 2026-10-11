import PerdicesCola

/-! # Perdices: cola cuantitativa y reinicios en mínimos futuros.

Atajo T. Los pisos se refieren a todos los valores futuros de la órbita;
no se deducen de una inspección finita. No hay hipótesis probabilísticas.
-/

namespace PerdicesMinimos

open Ocelotas CasaPlano CasaRetrato PerdicesTamano PerdicesColisiones PerdicesCola
open PerdicesAporte
open scoped BigOperators

/-- Suma desde un piso fijo; conserva explícitamente el resto geométrico. -/
theorem suma_desde_hasta (A : Finset ℕ) (m : ℕ)
    (hp : ∀ a ∈ A, 2 ^ (100 * m) ≤ a)
    (hc : ∀ r, (A.filter fun a => a < 2 ^ (100 * r)).card ≤ 3 * 2 ^ (99 * r))
    (d : ℕ) :
    (∑ a ∈ A.filter (fun a => a < 2 ^ (100 * (m + d))), (1 : ℝ) / a) * 2 ^ (m + d) +
      2 * (3 * 2 ^ 99) ≤ 2 * (3 * 2 ^ 99) * 2 ^ d := by
  classical
  induction d with
  | zero =>
    have hz : A.filter (fun a => a < 2 ^ (100 * (m + 0))) = ∅ := by
      apply Finset.eq_empty_iff_forall_notMem.mpr
      intro a ha
      have h := Finset.mem_filter.mp ha
      have h' := hp a h.1
      simp only [Nat.add_zero] at h
      omega
    rw [hz]
    simp
  | succ d ih =>
    let B := A.filter fun a => a < 2 ^ (100 * (m + d))
    let D := A.filter fun a => 2 ^ (100 * (m + d)) ≤ a ∧ a < 2 ^ (100 * (m + (d + 1)))
    have he : A.filter (fun a => a < 2 ^ (100 * (m + (d + 1)))) = B ∪ D := by
      have hpow : (2 : ℕ) ^ (100 * (m + d)) ≤ 2 ^ (100 * (m + (d + 1))) :=
        Nat.pow_le_pow_right (by norm_num) (by omega)
      ext a
      simp only [B, D, Finset.mem_filter, Finset.mem_union]
      constructor
      · rintro ⟨ha, hu⟩
        by_cases hl : a < 2 ^ (100 * (m + d))
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
    have hs := suma_anillo A hc (m + d)
    have hmd : m + (d + 1) = m + d + 1 := by omega
    rw [← hmd] at hs
    change (∑ a ∈ D, (1 : ℝ) / a) * 2 ^ (m + d) ≤ _ at hs
    change (∑ a ∈ B, (1 : ℝ) / a) * 2 ^ (m + d) + _ ≤ _ at ih
    rw [he, Finset.sum_union hd, hmd]
    simp only [pow_succ]
    nlinarith only [ih, hs]

theorem suma_finita_piso (A : Finset ℕ) (m : ℕ)
    (hp : ∀ a ∈ A, 2 ^ (100 * m) ≤ a)
    (hc : ∀ r, (A.filter fun a => a < 2 ^ (100 * r)).card ≤ 3 * 2 ^ (99 * r)) :
    (∑ a ∈ A, (1 : ℝ) / a) ≤ 3 * 2 ^ 100 / 2 ^ m := by
  classical
  let d := A.sup id + 1
  have he : A.filter (fun a => a < 2 ^ (100 * (m + d))) = A := by
    apply Finset.filter_eq_self.mpr
    intro a ha
    have ham : a < d := by
      have := Finset.le_sup (f := id) ha
      change a ≤ A.sup id at this
      omega
    have hm : m + d < 2 ^ (100 * (m + d)) := Nat.lt_two_pow_self.trans_le
      (Nat.pow_le_pow_right (by norm_num) (by omega))
    exact (ham.trans_le (Nat.le_add_left _ _)).trans hm
  have h := suma_desde_hasta A m hp hc d
  rw [he, pow_add] at h
  have hcst : (2 : ℝ) * (3 * 2 ^ 99) = 3 * 2 ^ 100 := by norm_num
  rw [hcst] at h
  rw [le_div_iff₀ (by positivity)]
  apply (mul_le_mul_iff_left₀ (show (0 : ℝ) < 2 ^ d by positivity)).mp
  nlinarith only [h]

theorem suma_orbital_piso {n : ℕ} (hi : Function.Injective (fun j => T^[j] n))
    (m k : ℕ) (hp : ∀ j, 2 ^ (100 * m) ≤ T^[j] n) :
    (∑ j ∈ Finset.range k, (1 : ℝ) / (T^[j] n : ℝ)) ≤ 3 * 2 ^ 100 / 2 ^ m := by
  classical
  let A := (Finset.range k).image fun j => T^[j] n
  have ha : ∀ a ∈ A, a ∈ Set.range (fun j => T^[j] n) := by
    intro a ha
    obtain ⟨j, _, rfl⟩ := Finset.mem_image.mp ha
    exact ⟨j, rfl⟩
  have hpA : ∀ a ∈ A, 2 ^ (100 * m) ≤ a := by
    intro a ha
    obtain ⟨j, _, rfl⟩ := Finset.mem_image.mp ha
    exact hp j
  have h := suma_finita_piso A m hpA (cuenta_orbita hi A ha)
  simpa only [A, Finset.sum_image (fun i _ j _ hij => hi hij)] using h

theorem suma_infinita_piso {n : ℕ} (hi : Function.Injective (fun j => T^[j] n))
    (m : ℕ) (hp : ∀ j, 2 ^ (100 * m) ≤ T^[j] n) :
    (∑' j, (1 : ℝ) / (T^[j] n : ℝ)) ≤ 3 * 2 ^ 100 / 2 ^ m :=
  Real.tsum_le_of_sum_range_le (fun _ => by positivity) (fun k => suma_orbital_piso hi m k hp)

theorem normalizado_piso {n : ℕ} (hn : 0 < n)
    (hi : Function.Injective (fun j => T^[j] n)) (m k : ℕ)
    (hp : ∀ j, 2 ^ (100 * m) ≤ T^[j] n) :
    normalizado n k ≤ n * Real.exp (2 ^ 100 / 2 ^ m) := by
  have hs : (∑ j ∈ Finset.range k, (1 : ℝ) / (3 * (T^[j] n : ℝ))) ≤ 2 ^ 100 / 2 ^ m := by
    calc (∑ j ∈ Finset.range k, (1 : ℝ) / (3 * (T^[j] n : ℝ))) =
          (∑ j ∈ Finset.range k, (1 : ℝ) / (T^[j] n : ℝ)) / 3 := by
            simp only [div_eq_mul_inv, Finset.sum_mul]
            apply Finset.sum_congr rfl
            intro j _
            ring
         _ ≤ (3 * 2 ^ 100 / 2 ^ m) / 3 :=
            div_le_div_of_nonneg_right (suma_orbital_piso hi m k hp) (by norm_num)
         _ = 2 ^ 100 / 2 ^ m := by ring
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

theorem estatura_piso {n : ℕ} (hn : 0 < n)
    (hi : Function.Injective (fun j => T^[j] n)) (m : ℕ)
    (hp : ∀ j, 2 ^ (100 * m) ≤ T^[j] n) :
    estatura n ≤ n * Real.exp (2 ^ 100 / 2 ^ m) :=
  ciSup_le (fun k => normalizado_piso hn hi m k hp)

theorem inyectiva_reinicio {n : ℕ} (hi : Function.Injective (fun j => T^[j] n)) (k : ℕ) :
    Function.Injective (fun j => T^[j] (T^[k] n)) := by
  intro i j he
  change T^[i] (T^[k] n) = T^[j] (T^[k] n) at he
  rw [← iter_add, ← iter_add] at he
  have h := hi he
  omega

theorem normalizado_traslado (n k j : ℕ) :
    normalizado n (k + j) = inverso n k * normalizado (T^[k] n) j := by
  unfold normalizado
  rw [inverso_traslado, iter_add]
  ring

theorem estatura_traslado {n : ℕ} (hn : 0 < n)
    (hi : Function.Injective (fun j => T^[j] n)) (k : ℕ) :
    estatura n = inverso n k * estatura (T^[k] n) := by
  have hp := inverso_pos n k
  have hn' := iter_pos hn k
  have hi' := inyectiva_reinicio hi k
  apply le_antisymm
  · apply ciSup_le
    intro j
    calc normalizado n j ≤ normalizado n (k + j) :=
          normalizado_monotono n (Nat.le_add_left _ _)
         _ = inverso n k * normalizado (T^[k] n) j := normalizado_traslado n k j
         _ ≤ inverso n k * estatura (T^[k] n) :=
          mul_le_mul_of_nonneg_left (estatura_acota hn' hi' j) hp.le
  · have h : estatura (T^[k] n) ≤ estatura n / inverso n k := by
      apply ciSup_le
      intro j
      rw [le_div_iff₀ hp, mul_comm, ← normalizado_traslado]
      exact estatura_acota hn hi (k + j)
    have h' := (le_div_iff₀ hp).mp h
    simpa only [mul_comm] using h'

theorem cola_traslado {n : ℕ} (hn : 0 < n)
    (hi : Function.Injective (fun j => T^[j] n)) (k : ℕ) :
    cola n k = estatura (T^[k] n) - T^[k] n := by
  unfold cola
  rw [estatura_traslado hn hi k]
  unfold normalizado
  have hp := ne_of_gt (inverso_pos n k)
  field_simp

theorem cola_piso {n : ℕ} (hn : 0 < n)
    (hi : Function.Injective (fun j => T^[j] n)) (k m : ℕ)
    (hp : ∀ j, 2 ^ (100 * m) ≤ T^[k + j] n) :
    cola n k ≤ (T^[k] n : ℝ) * (Real.exp (2 ^ 100 / 2 ^ m) - 1) := by
  rw [cola_traslado hn hi k]
  have h := estatura_piso (iter_pos hn k) (inyectiva_reinicio hi k) m
    (fun j => by simpa only [iter_add] using hp j)
  nlinarith only [h]

theorem fuga_piso {n : ℕ} (h : FugaPura n) (m : ℕ) (hm : 2 ^ (100 * m) ≤ n) :
    estatura n - n ≤ n * (Real.exp (2 ^ 100 / 2 ^ m) - 1) := by
  have h' := estatura_piso (by have := fuga_pura_dos h; omega) (rasgo_inyectiva h) m
    (fun j => hm.trans (fuga_pura_no_baja h j))
  nlinarith only [h']

/-- Versión con el inverso del mínimo de pronóstico de CasaTablero. -/
theorem maximo_futuro {n : ℕ} (hn : 0 < n)
    (hi : Function.Injective (fun j => T^[j] n)) (K : ℕ) :
    ∃ k, K ≤ k ∧ ∀ j, k ≤ j → inverso n j ≤ inverso n k := by
  obtain ⟨J, hJ⟩ := inverso_pequeno hn hi (inverso_pos n K)
  have hKB : K ∈ Finset.Icc K (max K J) := Finset.mem_Icc.mpr ⟨le_rfl, le_max_left _ _⟩
  obtain ⟨k, hk, hmax⟩ := (Finset.Icc K (max K J)).exists_max_image (inverso n) ⟨K, hKB⟩
  have hk' := Finset.mem_Icc.mp hk
  refine ⟨k, hk'.1, fun j hj => ?_⟩
  by_cases hjB : j ≤ max K J
  · exact hmax j (Finset.mem_Icc.mpr ⟨hk'.1.trans hj, hjB⟩)
  · have hjJ : J ≤ j := (le_max_right K J).trans (by omega)
    exact (hJ j hjJ).le.trans (hmax K hKB)

theorem fuga_del_maximo (n k : ℕ)
    (h : ∀ j, k ≤ j → inverso n j ≤ inverso n k) : FugaPura (T^[k] n) := by
  rintro ⟨j, hj⟩
  have h1 := h (k + j) (by omega)
  rw [inverso_traslado] at h1
  have h2 : inverso (T^[k] n) j ≤ 1 := by
    have hp := inverso_pos n k
    nlinarith only [h1, hp]
  unfold inverso at h2
  rw [div_le_one (by positivity)] at h2
  have h3 : 2 ^ j ≤ 3 ^ S j (T^[k] n) := by exact_mod_cast h2
  omega

theorem reinicio_grande {n : ℕ} (hn : 0 < n)
    (hi : Function.Injective (fun j => T^[j] n)) (K M : ℕ) :
    ∃ k, K ≤ k ∧ M < T^[k] n ∧ FugaPura (T^[k] n) := by
  obtain ⟨J, hJ⟩ := orbita_supera hi M
  obtain ⟨k, hk, hmax⟩ := maximo_futuro hn hi (max K J)
  exact ⟨k, (le_max_left _ _).trans hk, hJ k ((le_max_right _ _).trans hk),
    fuga_del_maximo n k hmax⟩

theorem reinicio_con_cota {n : ℕ} (hn : 0 < n)
    (hi : Function.Injective (fun j => T^[j] n)) (K m : ℕ) :
    ∃ k, K ≤ k ∧ 2 ^ (100 * m) ≤ T^[k] n ∧ FugaPura (T^[k] n) ∧
      cola n k ≤ (T^[k] n : ℝ) * (Real.exp (2 ^ 100 / 2 ^ m) - 1) := by
  obtain ⟨k, hk, hp, hf⟩ := reinicio_grande hn hi K (2 ^ (100 * m))
  refine ⟨k, hk, hp.le, hf, ?_⟩
  rw [cola_traslado hn hi k]
  exact fuga_piso hf m hp.le

/-- El muro B excluiría todas las órbitas positivas inyectivas, incluso tras un cruce. -/
theorem muroB_sin_inyectivas (hB : MuroB) {n : ℕ} (hn : 0 < n) :
    ¬ Function.Injective (fun j => T^[j] n) := by
  intro hi
  obtain ⟨k, _, hk, hf⟩ := reinicio_grande hn hi 0 1
  exact hf (hB _ (by omega))

theorem muroB_iff_sin_inyectivas :
    MuroB ↔ ∀ n, 0 < n → ¬ Function.Injective (fun j => T^[j] n) := by
  constructor
  · exact fun h n hn => muroB_sin_inyectivas h hn
  · intro h n hn
    by_contra hc
    exact h n (by omega) (rasgo_inyectiva hc)

/-- Tras excluir el planeador, el cruce universal y la ausencia de ciclos bastan. -/
theorem collatz_iff_cruce_sin_circuitos :
    Collatz ↔ MuroB ∧ ∀ x, ¬ Circuito x := by
  constructor
  · intro h
    exact ⟨(muros_de_collatz h).2, muroA_sin_circuitos (muros_de_collatz h).1⟩
  · rintro ⟨hB, hC⟩
    apply collatz_iff_atajo.mpr
    intro n hn
    by_contra hno
    have hi : Function.Injective (fun j => T^[j] n) := by
      intro i j he
      rcases lt_trichotomy i j with hij | hij | hij
      · exact (hC _ (circuito_de_repeticion hn hno hij he)).elim
      · exact hij
      · exact (hC _ (circuito_de_repeticion hn hno hij he.symm)).elim
    exact muroB_sin_inyectivas hB hn hi

/-- La restricción afín de la cola no constituye otra congruencia independiente. -/
theorem intervalo_afin {n y A M B ξ W : ℝ} (hA : 0 < A) (hM : 0 < M)
    (he : M * y = A * n + B) (ht : 1 ≤ ξ * (A / M) - y)
    (hW : ξ - n ≤ W) : B + M ≤ A * W := by
  have h1 : M ≤ A * ξ - M * y := by
    have h := mul_le_mul_of_nonneg_left ht hM.le
    field_simp at h
    nlinarith only [h]
  have h2 := mul_le_mul_of_nonneg_left hW hA.le
  nlinarith only [he, h1, h2]

#print axioms PerdicesMinimos.suma_desde_hasta
#print axioms PerdicesMinimos.suma_finita_piso
#print axioms PerdicesMinimos.suma_orbital_piso
#print axioms PerdicesMinimos.suma_infinita_piso
#print axioms PerdicesMinimos.normalizado_piso
#print axioms PerdicesMinimos.estatura_piso
#print axioms PerdicesMinimos.inyectiva_reinicio
#print axioms PerdicesMinimos.normalizado_traslado
#print axioms PerdicesMinimos.estatura_traslado
#print axioms PerdicesMinimos.cola_traslado
#print axioms PerdicesMinimos.cola_piso
#print axioms PerdicesMinimos.fuga_piso
#print axioms PerdicesMinimos.maximo_futuro
#print axioms PerdicesMinimos.fuga_del_maximo
#print axioms PerdicesMinimos.reinicio_grande
#print axioms PerdicesMinimos.reinicio_con_cota
#print axioms PerdicesMinimos.muroB_sin_inyectivas
#print axioms PerdicesMinimos.muroB_iff_sin_inyectivas
#print axioms PerdicesMinimos.collatz_iff_cruce_sin_circuitos
#print axioms PerdicesMinimos.intervalo_afin

end PerdicesMinimos
