import Mathlib.Data.Nat.Basic
import Mathlib.Tactic.SplitIfs

/-! # Perdices: retorno parcial de Yolcu–Aaronson–Heule, proposición 4.15.

La definición incluye cero sólo para las identidades aritméticas. El problema
de terminación corresponde a las semillas positivas. Un paso H equivale a dos
o tres pasos del atajo, según la rama. No se demuestra terminación universal.
-/

namespace PerdicesRetornoH

def H (x : ℕ) : Option ℕ :=
  if x % 4 = 0 then some (3 * x / 4)
  else if x % 8 = 7 then some ((9 * x + 1) / 8)
  else none

def inversa (y : ℕ) : Option ℕ :=
  if y % 3 = 0 then some (4 * y / 3)
  else if y % 9 = 8 then some ((8 * y - 1) / 9)
  else none

/-- Atajo clásico, declarado aquí de forma independiente. -/
def T (n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

theorem caracterizacion (x y : ℕ) : H x = some y ↔
    (x % 4 = 0 ∧ 4 * y = 3 * x) ∨ (x % 8 = 7 ∧ 8 * y = 9 * x + 1) := by
  unfold H
  split_ifs <;> simp_all <;> omega

theorem positiva {x y : ℕ} (hx : 0 < x) (h : H x = some y) : 0 < y := by
  rw [caracterizacion] at h
  omega

/-- Las imágenes de las dos ramas están en 0 mod 3 y 8 mod 9. -/
theorem imagen {x y : ℕ} (h : H x = some y) : y % 3 = 0 ∨ y % 9 = 8 := by
  rw [caracterizacion] at h
  omega

theorem inyectiva {x z y : ℕ} (hx : H x = some y) (hz : H z = some y) : x = z := by
  rw [caracterizacion] at hx hz
  omega

theorem inversa_izquierda {x y : ℕ} (h : H x = some y) : inversa y = some x := by
  rw [caracterizacion] at h
  unfold inversa
  split_ifs <;> (try simp_all) <;> omega

theorem inversa_derecha {x y : ℕ} (h : inversa y = some x) : H x = some y := by
  rw [caracterizacion]
  unfold inversa at h
  split_ifs at h <;> simp_all <;> omega

theorem retorno_D {x : ℕ} (hx : x % 4 = 0) :
    T (T (8 * x + 1)) = 8 * (3 * x / 4) + 1 := by
  unfold T
  split_ifs <;> omega

theorem retorno_E {x : ℕ} (hx : x % 8 = 7) :
    T (T (T (8 * x + 1))) = 8 * ((9 * x + 1) / 8) + 1 := by
  unfold T
  split_ifs <;> omega

theorem fuente {y : ℕ} (h3 : y % 3 ≠ 0) (h9 : y % 9 ≠ 8) :
    ¬ ∃ x, H x = some y := by
  rintro ⟨x, hx⟩
  exact (imagen hx).elim h3 h9

/-- Con u=M*t, ambos extremos son -1 módulo M y la arista es creciente. -/
theorem expansion_residual {u : ℕ} (hu : 1 ≤ u) :
    H (8 * u - 1) = some (9 * u - 1) ∧
    8 * u - 1 < 9 * u - 1 ∧ (9 * u - 1) - (8 * u - 1) = u := by
  rw [caracterizacion]
  omega

end PerdicesRetornoH

#print axioms PerdicesRetornoH.caracterizacion
#print axioms PerdicesRetornoH.positiva
#print axioms PerdicesRetornoH.imagen
#print axioms PerdicesRetornoH.inyectiva
#print axioms PerdicesRetornoH.inversa_izquierda
#print axioms PerdicesRetornoH.inversa_derecha
#print axioms PerdicesRetornoH.retorno_D
#print axioms PerdicesRetornoH.retorno_E
#print axioms PerdicesRetornoH.fuente
#print axioms PerdicesRetornoH.expansion_residual
