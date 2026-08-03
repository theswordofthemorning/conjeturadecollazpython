/- contracciondegatas.lean
   LA CONTRACCION DE GATAS, demostrada en Lean 4.
   (04-08-2026; el octavo .lean del repo. Nucleo puro, sin Mathlib.)

   El corazon (a) del teorema de Gatas: el par (4t+1, 4t+2) se convierte
   en EXACTAMENTE dos pasos en el par consecutivo fresco (3t+1, 3t+2) -
   la autosimilitud exacta del problema de fusion. Cada identidad es un
   calculo; el nucleo las verifica todas. -/

def T (n : Nat) : Nat := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

theorem paso1_impar (t : Nat) : T (4 * t + 1) = 6 * t + 2 := by
  unfold T
  have h : (4 * t + 1) % 2 = 1 := by omega
  simp [h]
  omega

theorem paso1_par (t : Nat) : T (4 * t + 2) = 2 * t + 1 := by
  unfold T
  have h : (4 * t + 2) % 2 = 0 := by omega
  simp [h]
  omega

theorem paso2_par (t : Nat) : T (6 * t + 2) = 3 * t + 1 := by
  unfold T
  have h : (6 * t + 2) % 2 = 0 := by omega
  simp [h]
  omega

theorem paso2_impar (t : Nat) : T (2 * t + 1) = 3 * t + 2 := by
  unfold T
  have h : (2 * t + 1) % 2 = 1 := by omega
  simp [h]
  omega

-- ── LA CONTRACCION, empaquetada: dos pasos y el par es (3t+1, 3t+2),
--    consecutivo fresco. La composicion la hace el nucleo.
theorem contraccion (t : Nat) :
    T (T (4 * t + 1)) = 3 * t + 1 ∧ T (T (4 * t + 2)) = 3 * t + 2 := by
  rw [paso1_impar, paso1_par, paso2_par, paso2_impar]
  exact ⟨rfl, rfl⟩

-- ── El caso concreto del documento (t = 1: (5, 6) -> (4, 7)? no:
--    (5,6) -> (8,3) -> (4,5)), por el nucleo con decide
theorem caso_t1 : T (T 5) = 4 ∧ T (T 6) = 5 := by decide

#print axioms paso1_impar
#print axioms contraccion
