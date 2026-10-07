import CasaCasiTodos

/-! # El dominó del muro A: cómo tendría que ser una grieta

Ruta B, paso 4 (05-10-2026), con presupuesto acotado. Una **grieta** es un número `n ≥ 2`
cuyo pronóstico baja de 1 (`Cruza n`) pero que nunca baja de sí mismo; el muro A dice que
no hay grietas. Aquí, sin hipótesis externas:

* `grieta_desigualdad`: si el pronóstico de `n` baja de 1 en el paso `k` y `n` no baja de
  sí mismo en ese paso, entonces `(2^k − 3^S_k(n)) n + 2^k ≤ 3^k`;
* `grieta_pequena`: en una grieta, todo paso `k` en que el pronóstico baja de 1 cumple
  `n < 3^k`; en particular, su primer cruce τ(n) cumple `3^τ(n) > n`;
* `minimos_no_bajan`: en toda órbita que no llega a 1 hay, tan lejos como se quiera,
  valores `≥ 2` que nunca bajan de sí mismos (los mínimos de sus colas);
* `contraejemplo_con_muroA`: con el muro A, la órbita de un contraejemplo de Collatz
  contiene infinitos fugitivos.

Compilación: `comprobar_fugitivo.py`, en esta carpeta. -/

namespace CasaDomino

open Ocelotas OcelotasContador CasaPlano CasaFugitivo CasaCasiTodos

/-- Desigualdad de una grieta en un paso de cruce. -/
theorem grieta_desigualdad {n k : ℕ} (hc : 3 ^ S k n < 2 ^ k) (hge : n ≤ T^[k] n) :
    (2 ^ k - 3 ^ S k n) * n + 2 ^ k ≤ 3 ^ k := by
  have h := cota_superior n k
  have hT := Nat.mul_le_mul_left (2 ^ k) hge
  have hsub : (2 ^ k - 3 ^ S k n) * n + 3 ^ S k n * n = 2 ^ k * n := by
    rw [← Nat.add_mul, Nat.sub_add_cancel hc.le]
  omega

/-- En una grieta, cada paso de cruce `k` cumple `n < 3^k`. -/
theorem grieta_pequena {n k : ℕ} (hc : 3 ^ S k n < 2 ^ k) (hd : ¬ Desciende n) : n < 3 ^ k := by
  by_contra h
  exact hd (desciende_de_grande hc (not_lt.mp h))

/-- El valor mínimo de una cola de la órbita no baja de sí mismo. -/
theorem minimo_de_cola (n M : ℕ) : ∃ i, M ≤ i ∧ ∀ j, i ≤ j → T^[i] n ≤ T^[j] n := by
  classical
  have hex : ∃ v, ∃ j, M ≤ j ∧ T^[j] n = v := ⟨_, M, le_rfl, rfl⟩
  obtain ⟨i, hi, hiv⟩ := Nat.find_spec hex
  refine ⟨i, hi, fun j hj => ?_⟩
  rw [hiv]
  exact Nat.find_min' hex ⟨j, le_trans hi hj, rfl⟩

/-- En toda órbita que no llega a 1 hay, tan lejos como se quiera, valores `≥ 2` que nunca
    bajan de sí mismos. -/
theorem minimos_no_bajan {n : ℕ} (hn : 1 ≤ n) (h : ¬ LlegaT n) (M : ℕ) :
    ∃ i, M ≤ i ∧ 2 ≤ T^[i] n ∧ ¬ Desciende (T^[i] n) := by
  obtain ⟨i, hi, hmin⟩ := minimo_de_cola n M
  refine ⟨i, hi, ?_, ?_⟩
  · have h1 := iter_pos hn i
    by_contra h2
    exact h ⟨i, by omega⟩
  · rintro ⟨k, -, hk⟩
    have := hmin (i + k) (by omega)
    rw [iter_add] at this
    omega

/-- Con el muro A, la órbita de un contraejemplo de Collatz contiene infinitos fugitivos. -/
theorem contraejemplo_con_muroA (hA : MuroA) {n : ℕ} (hn : 1 ≤ n) (h : ¬ LlegaT n) (M : ℕ) :
    ∃ i, M ≤ i ∧ 2 ≤ T^[i] n ∧ FugaPura (T^[i] n) := by
  obtain ⟨i, hi, h2, hd⟩ := minimos_no_bajan hn h M
  exact ⟨i, hi, h2, fun hc => hd (hA _ h2 hc)⟩

end CasaDomino

#print axioms CasaDomino.grieta_desigualdad
#print axioms CasaDomino.grieta_pequena
#print axioms CasaDomino.minimo_de_cola
#print axioms CasaDomino.minimos_no_bajan
#print axioms CasaDomino.contraejemplo_con_muroA
