import CasaFugitivo

/-! # Casi todo número baja de sí mismo (Terras 1976, Everett 1977)

Ruta B, 05-10-2026. Con la cota de residuos sin cruce de `CasaFugitivo` y una cota
superior del término aditivo de la fórmula de Terras, se demuestra sin hipótesis externas
que los números que nunca bajan de su punto de partida (σ(n) infinito) tienen densidad
natural 0. Son los únicos candidatos a contraejemplo mínimo de Collatz: así, el menor
contraejemplo, si existe, está en un conjunto de densidad 0.

* `cota_superior`: `2^k T^k(n) + 2^k ≤ 3^S_k(n) n + 3^k`;
* `desciende_de_cruce_grande`: si el pronóstico baja de 1 en el paso `k` y `n ≥ 3^k`,
  entonces `n` baja de sí mismo (en ese paso `k`);
* `casi_todos_descienden`: la proporción de `n < N` que nunca bajan de sí mismos
  tiende a 0.

Esto no es Wu 1 («casi todo número llega a 1»), que sigue abierta: bajar una vez no
garantiza seguir bajando.

Compilación: `comprobar_fugitivo.py`, en esta carpeta. -/

namespace CasaCasiTodos

open Ocelotas OcelotasContador CasaPlano CasaFugitivo

/-- Cota superior del término aditivo de Terras. -/
theorem cota_superior (n k : ℕ) : 2 ^ k * T^[k] n + 2 ^ k ≤ 3 ^ S k n * n + 3 ^ k := by
  induction k with
  | zero => simp [S]
  | succ k ih =>
    rw [OcelotasFinito.numerador_siguiente, pow_succ, pow_succ, Function.iterate_succ_apply']
    have h23 : 2 ^ k ≤ 3 ^ k := Nat.pow_le_pow_left (by norm_num) k
    by_cases h : T^[k] n % 2 = 0
    · rw [if_pos h]
      have he := T_par h
      generalize 2 ^ k = c at *
      generalize 3 ^ k = d at *
      generalize 3 ^ S k n = e at *
      generalize T (T^[k] n) = y at *
      generalize T^[k] n = m at *
      have hy : c * 2 * y = c * m := by rw [← he]; ring
      linarith
    · rw [if_neg h]
      have he := T_impar (by omega : T^[k] n % 2 = 1)
      generalize 2 ^ k = c at *
      generalize 3 ^ k = d at *
      generalize 3 ^ S k n = e at *
      generalize T (T^[k] n) = y at *
      generalize T^[k] n = m at *
      have hy : c * 2 * y = 3 * (c * m) + c := by rw [mul_assoc, he]; ring
      have he3 : 3 * e * n = 3 * (e * n) := by ring
      linarith

/-- Un cruce en el paso `k` de un número `n ≥ 3^k` es ya un descenso. -/
theorem desciende_de_cruce_grande {n k : ℕ} (hc : 3 ^ S k n < 2 ^ k) (hn : 3 ^ k ≤ n) :
    T^[k] n < n := by
  have h := cota_superior n k
  have hm := Nat.mul_le_mul_right n (show 3 ^ S k n + 1 ≤ 2 ^ k from hc)
  have hpos : 0 < 2 ^ k := by positivity
  by_contra hge
  have hT := Nat.mul_le_mul_left (2 ^ k) (not_lt.mp hge)
  nlinarith

theorem desciende_de_grande {n k : ℕ} (hc : 3 ^ S k n < 2 ^ k) (hn : 3 ^ k ≤ n) :
    Desciende n := by
  refine ⟨k, ?_, desciende_de_cruce_grande hc hn⟩
  rcases Nat.eq_zero_or_pos k with h0 | h0
  · subst h0
    simp [S] at hc
  · exact h0

open Classical in
/-- Números menores que `N` que nunca bajan de sí mismos. -/
noncomputable def noDescienden (N : ℕ) : Finset ℕ :=
  (Finset.range N).filter fun n => ¬ Desciende n

theorem noDescienden_por_residuos (N K : ℕ) :
    (noDescienden N).card ≤ 3 ^ K + (N / 2 ^ K + 1) * (sinCruce K).card := by
  classical
  have hsub : noDescienden N ⊆ Finset.range (3 ^ K) ∪
      (Finset.range N).filter fun n => 2 ^ K ≤ 3 ^ S K n := by
    intro n hn
    have hn' : n < N ∧ ¬ Desciende n := by simpa [noDescienden] using hn
    rw [Finset.mem_union, Finset.mem_range, Finset.mem_filter, Finset.mem_range]
    by_cases hk : n < 3 ^ K
    · exact Or.inl hk
    · refine Or.inr ⟨hn'.1, ?_⟩
      by_contra hc
      exact hn'.2 (desciende_de_grande (not_le.mp hc) (not_lt.mp hk))
  calc (noDescienden N).card
      ≤ (Finset.range (3 ^ K) ∪ (Finset.range N).filter fun n => 2 ^ K ≤ 3 ^ S K n).card :=
        Finset.card_le_card hsub
    _ ≤ (Finset.range (3 ^ K)).card +
          ((Finset.range N).filter fun n => 2 ^ K ≤ 3 ^ S K n).card :=
        Finset.card_union_le _ _
    _ ≤ 3 ^ K + (N / 2 ^ K + 1) * (sinCruce K).card := by
        rw [Finset.card_range]
        exact Nat.add_le_add_left (filtro_por_residuos N K) _

/-- **Terras (1976), Everett (1977).** Casi todo número baja alguna vez de sí mismo: la
    proporción de `n < N` que nunca bajan tiende a 0. -/
theorem casi_todos_descienden :
    Filter.Tendsto (fun N : ℕ => ((noDescienden N).card : ℝ) / N) Filter.atTop (nhds 0) := by
  rw [tendsto_order]
  refine ⟨fun a ha => Filter.Eventually.of_forall fun N => ?_, fun a ha => ?_⟩
  · exact lt_of_lt_of_le ha (by positivity)
  · obtain ⟨K, hK⟩ := exists_pow_lt_of_lt_one (show 0 < a / 4 by linarith) razon_menor
    obtain ⟨M, hM⟩ := exists_nat_gt (2 * 3 ^ K / a)
    rw [Filter.eventually_atTop]
    refine ⟨2 ^ K + M, fun N hN => ?_⟩
    have hK2 : 2 ^ K ≤ N := by omega
    have hKr : (0 : ℝ) < 2 ^ K := by positivity
    have hNpos : (0 : ℝ) < N := lt_of_lt_of_le hKr (by exact_mod_cast hK2)
    have hMN : (M : ℝ) ≤ N := by exact_mod_cast (le_trans (Nat.le_add_left M (2 ^ K)) hN)
    have hcont : ((noDescienden N).card : ℝ) ≤
        3 ^ K + (((N / 2 ^ K : ℕ) : ℝ) + 1) * (sinCruce K).card := by
      exact_mod_cast noDescienden_por_residuos N K
    have hb := cota_bloques hK2
    have hρN := mul_lt_mul_of_pos_right hK hNpos
    have h3 : (3 : ℝ) ^ K < a / 2 * N := by
      have h1 : 2 * (3 : ℝ) ^ K < M * a := (div_lt_iff₀ ha).1 hM
      have h2 : (M : ℝ) * a ≤ N * a := mul_le_mul_of_nonneg_right hMN ha.le
      linarith
    rw [div_lt_iff₀ hNpos]
    linarith

end CasaCasiTodos

#print axioms CasaCasiTodos.cota_superior
#print axioms CasaCasiTodos.desciende_de_cruce_grande
#print axioms CasaCasiTodos.noDescienden_por_residuos
#print axioms CasaCasiTodos.casi_todos_descienden
